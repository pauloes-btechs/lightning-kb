"""Phase 1: copy the source docs into raw/ as markdown, one file per page.

Re-runnable: a page is rewritten only when its content changed.
"""
import datetime
import re
import time
from urllib.parse import urljoin, urlparse

import httpx
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

from . import living
from .common import ROOT, sha, split_frontmatter

UA = "lightning-kb/1.0 (personal docs mirror for local search)"
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
DROP = ["nav", "footer", "script", "style", "button", "aside",
        ".theme-doc-breadcrumbs", ".pagination-nav", ".hash-link",
        ".theme-doc-toc-mobile", ".theme-doc-footer"]


def _get(client, url):
    for attempt in range(4):
        try:
            r = client.get(url)
            if r.status_code == 200:
                return r.text
            if r.status_code in (404, 410):
                return None
        except httpx.HTTPError:
            pass
        time.sleep(1.5 * (attempt + 1))
    return None


def _dest(source, url):
    """raw/<source>/<url path>.md, guaranteed to stay inside raw/<source>."""
    parts = [re.sub(r"[^A-Za-z0-9._-]", "-", p)
             for p in urlparse(url).path.split("/") if p and p not in (".", "..")]
    if not parts:
        parts = ["index"]
    if parts[-1].endswith(".md"):
        parts[-1] = parts[-1][:-3]
    base = (ROOT / "raw" / source).resolve()
    dest = (base.joinpath(*parts)).with_name(parts[-1] + ".md").resolve()
    if base not in dest.parents:
        raise ValueError("unsafe path from " + url)
    return dest


def _save(source, url, title, body):
    body = body.strip() + "\n"
    dest = _dest(source, url)
    rel = dest.relative_to(ROOT).as_posix()
    digest = sha(body)
    status, old_sha = "new", None
    if dest.exists():
        old_text = dest.read_text()
        meta, _ = split_frontmatter(old_text)
        old_sha = meta.get("sha256")
        if old_sha == digest:
            return "same", rel
        # Keep the superseded version so an old spec stays distinguishable.
        stamp = str(meta.get("fetched") or "unknown")
        keep = ROOT / "history" / (rel[:-3] + "." + stamp + ".md")
        keep.parent.mkdir(parents=True, exist_ok=True)
        keep.write_text(old_text)
        status = "changed"
    meta = {"title": title, "source": source, "source_url": url, "sha256": digest,
            "fetched": datetime.date.today().isoformat()}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n" + body)
    living.record(status, source, rel, url, old_sha, digest)
    return ("new" if status in ("new", "changed") else status), rel


def _title_from_md(body, fallback):
    m = re.search(r"^#\s+(.+)$", body, re.M)
    return m.group(1).strip() if m else fallback


def _html_to_md(html):
    soup = BeautifulSoup(html, "html.parser")
    node = soup.find("article") or soup.find("main") or soup.body or soup
    for sel in DROP:
        for el in node.select(sel):
            el.decompose()
    h1 = node.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else (soup.title.get_text(strip=True) if soup.title else "")
    md = markdownify(str(node), heading_style="ATX", bullets="-")
    md = re.sub(r"\n{3,}", "\n\n", md)
    return title, md


def _crawl_llms(client, src, limit):
    index = _get(client, src["url"])
    if index is None:
        raise SystemExit("could not fetch " + src["url"])
    host = urlparse(src["url"]).netloc
    seen, pages = set(), []
    for title, href in LINK_RE.findall(index):
        url = urljoin(src["url"], href)
        if urlparse(url).netloc == host and url not in seen:
            seen.add(url)
            pages.append((title, url))
    return [(t, u, "md") for t, u in pages[:limit]]


def _crawl_sitemap(client, src, limit):
    xml = _get(client, src["url"])
    if xml is None:
        raise SystemExit("could not fetch " + src["url"])
    host = urlparse(src["url"]).netloc
    urls = [u.strip() for u in re.findall(r"<loc>([^<]+)</loc>", xml)]
    inc = src.get("include") or [""]
    urls = [u for u in urls if urlparse(u).netloc == host and any(i in u for i in inc)]
    return [("", u, "html") for u in sorted(set(urls))[:limit]]


def run(only=None, limit=None, delay=0.25):
    sources = yaml.safe_load((ROOT / "sources.yaml").read_text())["sources"]
    limit = limit or 10 ** 9
    with httpx.Client(headers={"User-Agent": UA}, follow_redirects=True, timeout=30) as client:
        for src in sources:
            if only and src["name"] != only:
                continue
            pages = (_crawl_llms if src["type"] == "llms_txt" else _crawl_sitemap)(client, src, limit)
            stats = {"new": 0, "same": 0, "failed": 0}
            failed, kept = [], set()
            for i, (title, url, kind) in enumerate(pages, 1):
                text = _get(client, url)
                if not text or not text.strip():
                    stats["failed"] += 1
                    failed.append(url)
                    continue
                if kind == "html":
                    title, body = _html_to_md(text)
                else:
                    body = text
                    title = _title_from_md(body, title)
                status, rel = _save(src["name"], url, title or url, body)
                stats[status] += 1
                kept.add(rel)
                if i % 25 == 0:
                    print("  %s: %d/%d" % (src["name"], i, len(pages)))
                time.sleep(delay)
            print("%-11s %d pages: %d new/changed, %d unchanged, %d failed"
                  % (src["name"], len(pages), stats["new"], stats["same"], stats["failed"]))
            for u in failed[:10]:
                print("   failed: " + u)
            # Pages the site no longer lists. Only judged on a complete, clean crawl.
            base = ROOT / "raw" / src["name"]
            if limit >= 10 ** 9 and not failed and base.exists():
                gone = [f.relative_to(ROOT).as_posix() for f in base.rglob("*.md")
                        if f.relative_to(ROOT).as_posix() not in kept]
                already = set(c["path"] for c in living.read_changes(kinds=("removed",)))
                for rel in gone:
                    if rel not in already:
                        living.record("removed", src["name"], rel, "")
                if gone:
                    print("   %d page(s) no longer on the site (kept locally; see ./kb changes)" % len(gone))
