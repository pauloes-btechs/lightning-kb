"""Phase 3: chunk + embed raw/ and wiki/ into Postgres and rebuild the link graph.

Incremental: only files whose content hash changed are re-embedded.
"""
import posixpath
import re

from .common import ROOT, db, embed, norm_url, sha, split_frontmatter, vec_literal

MAX_CHARS = 1600
HEAD_RE = re.compile(r"^(#{1,4})\s+(.*)$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PRODUCTS = ["taproot-assets", "lightning-terminal", "wavelength", "aperture",
            "faraday", "pool", "loop", "lnd", "lit"]
SKIP = {"wiki/log.md"}


def chunk(body):
    """Split on headings (outside code fences), then cap section size."""
    sections, path, buf, fence = [], [], [], False

    def flush():
        text = "\n".join(buf).strip()
        if len(text) >= 20:
            sections.append((" > ".join(path), text))
        del buf[:]

    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else HEAD_RE.match(line)
        if m:
            flush()
            level = len(m.group(1))
            del path[level - 1:]
            path.append(m.group(2).strip())
        else:
            buf.append(line)
    flush()

    out = []
    for heading, text in sections:
        if len(text) <= MAX_CHARS:
            out.append((heading, text))
            continue
        cur = ""
        for para in re.split(r"\n\s*\n", text):
            while len(para) > MAX_CHARS:
                if cur:
                    out.append((heading, cur))
                    cur = ""
                out.append((heading, para[:MAX_CHARS]))
                para = para[MAX_CHARS:]
            if cur and len(cur) + len(para) + 2 > MAX_CHARS:
                out.append((heading, cur))
                cur = para
            else:
                cur = (cur + "\n\n" + para) if cur else para
        if cur.strip():
            out.append((heading, cur))
    return out


def _product(path):
    segs = path.lower().split("/")
    for p in PRODUCTS:
        if p in segs:
            return "lit" if p == "lightning-terminal" else p
    return None


def _files():
    for layer in ("raw", "wiki"):
        base = ROOT / layer
        if base.exists():
            for f in sorted(base.rglob("*.md")):
                rel = f.relative_to(ROOT).as_posix()
                if rel not in SKIP and not f.name.startswith("._"):
                    yield layer, rel, f


def run(url=None):
    seen, texts = {}, {}
    n_embedded = 0
    with db(url) as conn:
        existing = dict(conn.execute("select path, sha256 from documents").fetchall())
        for layer, rel, f in _files():
            raw_text = f.read_text(errors="replace")
            meta, body = split_frontmatter(raw_text)
            digest = sha(raw_text)
            seen[rel] = True
            texts[rel] = (meta, body)
            if existing.get(rel) == digest:
                continue
            title = str(meta.get("title") or f.stem)
            parts = rel.split("/")
            source = parts[1] if layer == "raw" and len(parts) > 2 else layer
            doc_id = conn.execute(
                """insert into documents(path, layer, source, product, title, url, sha256)
                   values (%s,%s,%s,%s,%s,%s,%s)
                   on conflict (path) do update set layer=excluded.layer, source=excluded.source,
                     product=excluded.product, title=excluded.title, url=excluded.url,
                     sha256=excluded.sha256, updated_at=now()
                   returning id""",
                (rel, layer, source, _product(rel), title, meta.get("source_url"), digest),
            ).fetchone()[0]
            conn.execute("delete from chunks where doc_id=%s", (doc_id,))
            chunks = chunk(body)
            for i in range(0, len(chunks), 16):
                batch = chunks[i:i + 16]
                vecs = embed([(title + " > " + h + "\n" + c)[:6000] for h, c in batch])
                for j, ((h, c), v) in enumerate(zip(batch, vecs)):
                    conn.execute(
                        "insert into chunks(doc_id, ord, heading, content, embedding) "
                        "values (%s,%s,%s,%s,%s::vector)",
                        (doc_id, i + j, h, c, vec_literal(v)))
            n_embedded += 1
            if n_embedded % 25 == 0:
                print("  embedded %d files" % n_embedded)

        gone = [p for p in existing if p not in seen]
        if gone:
            conn.execute("delete from documents where path = any(%s)", (gone,))

        # ---- link graph (cheap, so rebuilt in full every run) ----
        rows = conn.execute("select id, path, url from documents").fetchall()
        by_path = {p: i for i, p, _ in rows}
        by_url = {norm_url(u): i for i, _, u in rows if u}
        by_stem = {}
        for i, p, _ in rows:
            if p.startswith("wiki/"):
                by_stem[posixpath.basename(p)[:-3].lower()] = i
        edges = set()
        for rel, (meta, body) in texts.items():
            src = by_path.get(rel)
            if src is None:
                continue
            for target in WIKILINK_RE.findall(body):
                dst = by_stem.get(posixpath.basename(target.strip()).lower())
                if dst and dst != src:
                    edges.add((src, dst, "wikilink"))
            base_url = meta.get("source_url")
            for href in MDLINK_RE.findall(body):
                dst = None
                if href.startswith("http"):
                    dst = by_url.get(norm_url(href))
                elif not href.startswith(("#", "mailto:")):
                    cand = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href.split("#")[0]))
                    dst = by_path.get(cand) or by_path.get(cand + ".md")
                    if dst is None and base_url:
                        from urllib.parse import urljoin
                        dst = by_url.get(norm_url(urljoin(base_url, href)))
                if dst and dst != src:
                    edges.add((src, dst, "mdlink"))
            cited = meta.get("sources") or []
            for s in cited if isinstance(cited, list) else []:
                dst = by_path.get(str(s)) or by_url.get(norm_url(str(s)))
                if dst and dst != src:
                    edges.add((src, dst, "cites"))
        conn.execute("truncate edges")
        with conn.cursor() as cur:
            cur.executemany("insert into edges(src, dst, kind) values (%s,%s,%s)", sorted(edges))

        d, c, e = conn.execute(
            "select (select count(*) from documents), (select count(*) from chunks), "
            "(select count(*) from edges)").fetchone()
    print("indexed: %d files re-embedded, %d removed. Now %d documents, %d chunks, %d links."
          % (n_embedded, len(gone), d, c, e))
