"""Keeping the knowledge base current: change log, stale wiki pages, refresh, schedule."""
import datetime
import json
import os
import pathlib
import subprocess
import sys

from .common import ROOT, split_frontmatter

CHANGELOG = ROOT / "changes.jsonl"
LABEL = "com.lightning-kb.crawl"


def record(kind, source, path, url, old_sha=None, new_sha=None):
    """Append one line to the change log. Called by the crawler."""
    line = {"date": datetime.date.today().isoformat(), "kind": kind, "source": source,
            "path": path, "url": url, "old": (old_sha or "")[:12], "new": (new_sha or "")[:12]}
    with open(CHANGELOG, "a") as f:
        f.write(json.dumps(line) + "\n")


def read_changes(since=None, kinds=None):
    if not CHANGELOG.exists():
        return []
    out = []
    for line in CHANGELOG.read_text().splitlines():
        try:
            c = json.loads(line)
        except ValueError:
            continue
        if since and c["date"] < since:
            continue
        if kinds and c["kind"] not in kinds:
            continue
        out.append(c)
    return out


def changes(since, show_all):
    kinds = None if show_all else ("changed", "removed")
    items = read_changes(since, kinds)
    if not items:
        print("No %schanges recorded%s." % ("" if show_all else "content ", " since " + since if since else ""))
        if not show_all:
            print("(First-time downloads are logged as 'new'; use --all to list them.)")
        return
    for c in items:
        print("%s  %-8s %s" % (c["date"], c["kind"], c["path"]))
    counts = {}
    for c in items:
        counts[c["kind"]] = counts.get(c["kind"], 0) + 1
    print("\n" + ", ".join("%d %s" % (n, k) for k, n in sorted(counts.items())))
    print("Previous versions of changed pages are kept under history/.")


def stale_pages():
    """Wiki pages citing a source that changed after the page was last updated."""
    out = []
    wiki = ROOT / "wiki"
    for f in sorted(wiki.rglob("*.md")) if wiki.exists() else []:
        meta, _ = split_frontmatter(f.read_text(errors="replace"))
        updated = str(meta.get("updated") or "")
        newer = []
        for s in meta.get("sources") or []:
            src = ROOT / str(s)
            if not src.exists():
                continue
            smeta, _ = split_frontmatter(src.read_text(errors="replace"))
            fetched = str(smeta.get("fetched") or "")
            if updated and fetched and fetched > updated:
                newer.append((str(s), fetched))
        if newer:
            out.append((f.relative_to(ROOT).as_posix(), updated, newer))
    return out


def stale():
    items = stale_pages()
    if not items:
        print("No stale wiki pages: no cited source has changed since its page was updated.")
        return 0
    for path, updated, newer in items:
        print("%s (updated %s)" % (path, updated))
        for s, fetched in newer:
            print("    source changed %s: %s" % (fetched, s))
    print("\n%d wiki page(s) need a re-check. In Claude Code: /build-wiki refresh" % len(items))
    return len(items)


def refresh():
    """Crawl, re-index what changed, then report changes and stale wiki pages."""
    from . import crawl
    today = datetime.date.today().isoformat()
    crawl.run()
    try:
        from . import common, index
        common.migrate()
        index.run()
    except Exception as e:  # database or Ollama not running
        print("\nCrawl finished, but indexing did not run (%s)." % str(e).splitlines()[0])
        print("Start Docker and Ollama, then run ./kb index.")
    print("\nChanges today:")
    changes(today, False)
    print()
    stale()


def _plist_path():
    return pathlib.Path.home() / "Library" / "LaunchAgents" / (LABEL + ".plist")


def schedule(action):
    """Weekly background crawl on macOS (launchd). It only downloads and logs
    changes; indexing still happens when you run ./kb index or ./kb refresh."""
    if sys.platform != "darwin":
        print("Scheduling is only implemented for macOS (launchd).")
        return
    plist = _plist_path()
    if action == "status":
        print("installed: %s" % plist if plist.exists() else "not installed")
        return
    if action == "remove":
        if plist.exists():
            subprocess.call(["launchctl", "unload", str(plist)])
            plist.unlink()
        print("removed")
        return
    (ROOT / "logs").mkdir(exist_ok=True)
    plist.parent.mkdir(parents=True, exist_ok=True)
    plist.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>%s</string>
  <key>ProgramArguments</key><array><string>%s</string><string>crawl</string></array>
  <key>StartCalendarInterval</key><dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>%s</string>
  <key>StandardErrorPath</key><string>%s</string>
</dict></plist>
""" % (LABEL, ROOT / "kb", ROOT / "logs" / "crawl.log", ROOT / "logs" / "crawl.log"))
    subprocess.call(["launchctl", "unload", str(plist)], stderr=subprocess.DEVNULL)
    code = subprocess.call(["launchctl", "load", "-w", str(plist)])
    print("Weekly crawl scheduled for Mondays 09:00 (log: logs/crawl.log)." if code == 0
          else "Wrote %s but launchctl refused to load it." % plist)
    print("It needs the drive mounted at that time. Check for changes with ./kb changes.")
