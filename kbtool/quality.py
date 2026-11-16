"""Phase 5: evaluation of retrieval, plus the wiki lint pass."""
import json
import posixpath
import re

import yaml

from .common import EMBED_MODEL, KB_EMBED, ROOT, db, split_frontmatter
from .index import WIKILINK_RE
from .search import MODES, search


def _first_hit(hits, expect):
    for rank, h in enumerate(hits, 1):
        hay = ((h["url"] or "") + " " + h["path"] + " " + " ".join(h.get("also_in") or [])).lower()
        if any(e.lower() in hay for e in expect):
            return rank
    return None


def run_eval(show_misses=True):
    golden = yaml.safe_load((ROOT / "evals" / "golden.yaml").read_text())["questions"]
    model = EMBED_MODEL if KB_EMBED == "ollama" else "hash (smoke test)"
    print("%d questions, embeddings: %s\n" % (len(golden), model))
    print("%-8s %7s %7s %7s" % ("mode", "hit@1", "hit@5", "MRR"))
    best = None
    with db() as conn:
        for mode in MODES:
            ranks, tops = [], []
            for item in golden:
                # Ranks count distinct pages. Look 50 deep so a miss reports
                # where the page actually ranked, and keep the top 3 to show.
                hits = search(conn, item["q"], mode, 50)
                ranks.append(_first_hit(hits, item["expect"]))
                tops.append([h["path"] for h in hits[:3]])
            n = float(len(ranks))
            h1 = sum(1 for r in ranks if r == 1) / n
            h5 = sum(1 for r in ranks if r and r <= 5) / n
            mrr = sum(1.0 / r for r in ranks if r and r <= 10) / n
            print("%-8s %7.2f %7.2f %7.2f" % (mode, h1, h5, mrr))
            detail = [{"q": g["q"], "rank": r, "level": g.get("level"), "top": t}
                      for g, r, t in zip(golden, ranks, tops)]
            conn.execute(
                "insert into eval_runs(mode, embed_model, questions, hit_at_1, hit_at_5, mrr, detail) "
                "values (%s,%s,%s,%s,%s,%s,%s)",
                (mode, model, len(ranks), h1, h5, mrr, json.dumps(detail)))
            if best is None or mrr > best[1]:
                best = (mode, mrr, detail)
    if show_misses and best:
        misses = [d for d in best[2] if not d["rank"] or d["rank"] > 5]
        print("\nBest mode: %s. Questions it did not answer in the top 5: %d" % (best[0], len(misses)))
        for d in misses:
            where = "expected page ranked %d" % d["rank"] if d["rank"] else "expected page not in the top 50"
            print("  - %s (%s)" % (d["q"], where))
            for path in d["top"]:
                print("      ranked above: " + path)
        levels = sorted(set(d["level"] for d in best[2] if d["level"] is not None))
        if levels:
            print("\nBy level (%s mode), share answered in the top 5:" % best[0])
            for lv in levels:
                ds = [d for d in best[2] if d["level"] == lv]
                ok = sum(1 for d in ds if d["rank"] and d["rank"] <= 5)
                print("  level %s: %d of %d" % (lv, ok, len(ds)))
    print("\nSaved to eval_runs. Compare over time: ./kb history")


def history():
    with db() as conn:
        rows = conn.execute(
            "select to_char(created_at, 'YYYY-MM-DD HH24:MI'), mode, embed_model, questions, "
            "hit_at_1, hit_at_5, mrr from eval_runs order by id desc limit 24").fetchall()
    print("%-17s %-7s %-20s %3s %6s %6s %6s" % ("when", "mode", "embeddings", "n", "hit@1", "hit@5", "MRR"))
    for r in rows:
        print("%-17s %-7s %-20s %3d %6.2f %6.2f %6.2f" % r)


def lint():
    """Karpathy's 'lint' operation: structural health of the wiki."""
    wiki = ROOT / "wiki"
    pages = {}
    for f in sorted(wiki.rglob("*.md")):
        if f.name.startswith("._"):
            continue
        pages[f.relative_to(ROOT).as_posix()] = split_frontmatter(f.read_text(errors="replace"))
    stems = {posixpath.basename(p)[:-3].lower(): p for p in pages}
    special = {"wiki/index.md", "wiki/log.md"}
    # Pages listed in wiki-plan.yaml may be linked before they are written.
    planned = set()
    plan_file = ROOT / "wiki-plan.yaml"
    if plan_file.exists():
        for item in (yaml.safe_load(plan_file.read_text()) or {}).get("pages") or []:
            planned.add(str(item.get("slug", "")).lower())
    pending = planned - set(stems)
    inbound, problems, cited = set(), [], set()
    has_raw = (ROOT / "raw").exists()   # raw/ is not in git, so CI cannot check it
    for path, (meta, body) in pages.items():
        for target in WIKILINK_RE.findall(body):
            hit = stems.get(posixpath.basename(target.strip()).lower())
            if hit:
                inbound.add(hit)
            elif posixpath.basename(target.strip()).lower() not in planned:
                problems.append("broken link  %s -> [[%s]]" % (path, target))
        if path in special:
            continue
        sources = meta.get("sources") or []
        if not sources:
            problems.append("no sources   %s" % path)
        for s in sources if isinstance(sources, list) else []:
            cited.add(str(s))
            if has_raw and str(s).startswith("raw/") and not (ROOT / str(s)).exists():
                problems.append("dead source  %s -> %s" % (path, s))
        if not re.search(r"\((\.\./)*raw/|\]\(https?://", body) and sources:
            problems.append("no inline citations  %s" % path)
        # Every citation link must point at a real source file that the page
        # also lists in `sources:`. Only checkable where raw/ is present.
        if has_raw:
            listed = set(str(s) for s in sources) if isinstance(sources, list) else set()
            seen_targets = set()
            for href in re.findall(r"\]\(((?:\.\./)+raw/[^)\s#]+)", body):
                target = posixpath.normpath(posixpath.join(posixpath.dirname(path), href))
                if target in seen_targets:
                    continue
                seen_targets.add(target)
                if not (ROOT / target).exists():
                    problems.append("dead citation  %s -> %s" % (path, target))
                elif target not in listed:
                    problems.append("unlisted source  %s cites %s but does not list it" % (path, target))
    for path in pages:
        if path not in special and path not in inbound:
            problems.append("orphan       %s" % path)
    raw = [f.relative_to(ROOT).as_posix() for f in (ROOT / "raw").rglob("*.md")] if (ROOT / "raw").exists() else []
    uncovered = [r for r in raw if r not in cited]
    for p in problems:
        print(p)
    print("\n%d wiki pages, %d problems. Raw coverage: %d of %d source pages cited by the wiki."
          % (len(pages) - len(special & set(pages)), len(problems), len(raw) - len(uncovered), len(raw)))
    if pending:
        print("Planned in wiki-plan.yaml but not written yet: %d" % len(pending))
    if uncovered:
        print("Next uncited sources (./kb lint --uncovered for all):")
    return uncovered, len(problems)
