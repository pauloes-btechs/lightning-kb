"""Phase 3: chunk + embed raw/ and wiki/ into Postgres and rebuild the link graph.

Incremental: only files whose content hash changed are re-embedded.
"""
import hashlib
import os
import posixpath
import re
import time

from .common import ROOT, db, embed, norm_url, sha, split_frontmatter, vec_literal

MAX_CHARS = 1600
HEAD_RE = re.compile(r"^(#{1,4})\s+(.*)$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PRODUCTS = ["taproot-assets", "lightning-terminal", "wavelength", "aperture",
            "faraday", "pool", "loop", "lnd", "lit"]
SKIP = {"wiki/log.md", "wiki/index.md"}
# Sections left out of the index (raw/ keeps them, so the wiki writer can still
# read them). Matched against heading text, case-insensitive. Set in .env:
#   KB_SKIP_SECTIONS=agent instructions,code samples
# - "agent instructions": boilerplate the docs site appends to every page.
# - "code samples": near-identical client boilerplate on every API method page,
#   roughly two thirds of the API text. The RPC signature, REST path and field
#   tables sit outside it and are always indexed.
SKIP_HEADINGS = tuple(h.strip().lower() for h in os.environ.get(
    "KB_SKIP_SECTIONS", "agent instructions,code samples").split(",") if h.strip())
TAG_RE = re.compile(r"<[^>]+>")
# Bump when chunking or embedding-input rules change: every file is redone.
CHUNK_VERSION = "4|" + ",".join(SKIP_HEADINGS)
API_RE = re.compile(r"^raw/api/api-docs/api/([^/]+)/([^/]+)/([^/]+)\.md$")
COMMIT_RE = re.compile(r"github\.com/[\w.-]+/([\w.-]+)/blob/([0-9a-f]{7,40})/")
MESSAGE_SECTIONS = ("Messages", "Nested Messages")


def api_info(rel):
    """(product, service, method-slug) for an API method page, else None."""
    m = API_RE.match(rel)
    return m.groups() if m else None


def contextualize(rel, title, heading):
    """Return (stored_heading, embed_prefix) for one chunk.

    An API page's own title is just the RPC name ("GetInfo"), which five
    products share. The stored heading and the embedded text therefore carry
    the product and service. Message tables are the exception: the same table
    appears on every page whose RPC uses it, so its prefix names only the
    product and the message. Identical tables then share one embedding.
    """
    parts = [h for h in heading.split(" > ") if h] if heading else []
    if parts and parts[0] == title:
        parts = parts[1:]
    info = api_info(rel)
    if not info:
        stored = " > ".join([title] + parts)
        return stored, stored
    product, service, _ = info
    crumb = "%s / %s / %s" % (product, service, title)
    stored = " > ".join([crumb] + parts)
    if len(parts) >= 2 and parts[0] in MESSAGE_SECTIONS:
        return stored, "%s message %s" % (product, parts[-1])
    return stored, stored


def strip_sections(body):
    """The body without the sections the index skips (used by ./kb show)."""
    out, path, fence, skipping = [], [], False, False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else HEAD_RE.match(line)
        if m:
            level = len(m.group(1))
            del path[level - 1:]
            path.append(TAG_RE.sub("", m.group(2)).strip())
            skipping = any(k in h.lower() for h in path for k in SKIP_HEADINGS)
        if not skipping:
            out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def chunk(body):
    """Split on headings (outside code fences), then cap section size."""
    sections, path, buf, fence = [], [], [], False

    def flush():
        text = "\n".join(buf).strip()
        skip = any(k in h.lower() for h in path for k in SKIP_HEADINGS)
        if len(text) >= 20 and not skip:
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
            path.append(TAG_RE.sub("", m.group(2)).strip())   # drop anchor tags
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


def _eta(seconds):
    m = int(seconds // 60)
    return "%dh%02dm" % (m // 60, m % 60) if m >= 60 else ("%dm" % m if m else "under 1m")


def run(url=None):
    seen, texts, todo = {}, {}, []
    with db(url) as conn:
        existing = dict(conn.execute("select path, sha256 from documents").fetchall())
        for layer, rel, f in _files():
            raw_text = f.read_text(errors="replace")
            meta, body = split_frontmatter(raw_text)
            digest = sha(CHUNK_VERSION + raw_text)
            seen[rel] = True
            texts[rel] = (meta, body)
            if existing.get(rel) != digest:
                todo.append((layer, rel, f, meta, body, digest))
        if todo:
            print("%d files to embed (%d already up to date)" % (len(todo), len(seen) - len(todo)))
        start, n_chunks, n_reused = time.time(), 0, 0
        for n, (layer, rel, f, meta, body, digest) in enumerate(todo, 1):
            title = str(meta.get("title") or f.stem)
            parts = rel.split("/")
            source = parts[1] if layer == "raw" and len(parts) > 2 else layer
            chunks = []
            for h, c in chunk(body):
                stored, prefix = contextualize(rel, title, h)
                key = hashlib.md5((prefix + "\n" + c).encode("utf-8")).hexdigest()
                chunks.append((stored, prefix, c, key))
            ver = COMMIT_RE.search(body) if layer == "raw" else None
            version = "%s@%s" % (ver.group(1), ver.group(2)[:7]) if ver else None
            # One transaction per file: if the run is interrupted, a half-embedded
            # file is rolled back and redone next time. Safe to Ctrl-C and resume.
            with conn.transaction():
                doc_id = conn.execute(
                    """insert into documents(path, layer, source, product, title, url, sha256, version)
                       values (%s,%s,%s,%s,%s,%s,%s,%s)
                       on conflict (path) do update set layer=excluded.layer, source=excluded.source,
                         product=excluded.product, title=excluded.title, url=excluded.url,
                         sha256=excluded.sha256, version=excluded.version, updated_at=now()
                       returning id""",
                    (rel, layer, source, _product(rel), title, meta.get("source_url"), digest, version),
                ).fetchone()[0]
                conn.execute("delete from chunks where doc_id=%s", (doc_id,))
                # Text that was already embedded (same prefix, same content) reuses
                # its stored vector instead of going back to the model.
                keys = [k for _, _, _, k in chunks]
                vec_by_key = dict(conn.execute(
                    "select distinct on (ekey) ekey, embedding::text from chunks "
                    "where ekey = any(%s) and embedding is not null", (keys,)).fetchall())
                need, queued = [], set()
                for stored, prefix, c, k in chunks:
                    if k not in vec_by_key and k not in queued:
                        queued.add(k)
                        need.append((k, prefix, c))
                for i in range(0, len(need), 16):
                    batch = need[i:i + 16]
                    vecs = embed([(prefix + "\n" + c)[:6000] for _, prefix, c in batch])
                    for (k, _, _), v in zip(batch, vecs):
                        vec_by_key[k] = vec_literal(v)
                n_reused += len(chunks) - len(need)
                for j, (stored, prefix, c, k) in enumerate(chunks):
                    conn.execute(
                        "insert into chunks(doc_id, ord, heading, content, embedding, ekey) "
                        "values (%s,%s,%s,%s,%s::vector,%s)", (doc_id, j, stored, c, vec_by_key[k], k))
            n_chunks += len(chunks)
            if n % 25 == 0 or n == len(todo):
                elapsed = time.time() - start
                left = elapsed / n * (len(todo) - n)
                print("  embedded %d/%d files, %d chunks (%d reused), %s elapsed, about %s left"
                      % (n, len(todo), n_chunks, n_reused, _eta(elapsed), _eta(left)), flush=True)
        n_embedded = len(todo)

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

        from .graph import build as build_api_graph
        n_ent, n_rel = build_api_graph(conn, texts)

        d, c, e = conn.execute(
            "select (select count(*) from documents), (select count(*) from chunks), "
            "(select count(*) from edges)").fetchone()
    print("indexed: %d files re-embedded, %d removed. Now %d documents, %d chunks, %d links, "
          "%d API entities, %d API relations."
          % (n_embedded, len(gone), d, c, e, n_ent, n_rel))
