import argparse
import sys

from . import common


def main():
    p = argparse.ArgumentParser(prog="kb", description="Lightning knowledge base")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("migrate", help="create tables")
    c = sub.add_parser("crawl", help="phase 1: download sources into raw/")
    c.add_argument("--source", help="docs | wavelength | api")
    c.add_argument("--limit", type=int, help="pages per source (use 5 for a first test)")
    sub.add_parser("index", help="phase 3: chunk, embed, build link graph")
    s = sub.add_parser("search", help="phase 4: retrieve")
    s.add_argument("query")
    s.add_argument("--mode", default="graph", choices=["kw", "vec", "hybrid", "graph"])
    s.add_argument("-k", type=int, default=8)
    s.add_argument("--product", help="lnd, loop, pool, faraday, taproot-assets, lit, wavelength, aperture")
    s.add_argument("--layer", choices=["raw", "wiki"])
    s.add_argument("--json", action="store_true")
    sub.add_parser("eval", help="phase 5: score all four search modes on evals/golden.yaml")
    sub.add_parser("history", help="past eval runs")
    lint_p = sub.add_parser("lint", help="wiki health: broken links, orphans, missing sources")
    lint_p.add_argument("--uncovered", action="store_true", help="list every uncited raw page")
    lint_p.add_argument("--strict", action="store_true", help="exit 1 if there are problems (CI)")
    sub.add_parser("status", help="counts")
    rs = sub.add_parser("reset", help="drop all tables (needed after changing the embedding model)")
    rs.add_argument("database_url", nargs="?", help="default: DATABASE_URL from .env")
    push = sub.add_parser("push", help="build the same index on Supabase/Neon")
    push.add_argument("database_url")
    a = p.parse_args()

    if a.cmd == "migrate":
        common.migrate()
    elif a.cmd == "crawl":
        from . import crawl
        crawl.run(a.source, a.limit)
    elif a.cmd == "index":
        from . import index
        common.migrate()
        index.run()
    elif a.cmd == "search":
        from . import search
        search.run(a.query, a.mode, a.k, a.product, a.layer, a.json)
    elif a.cmd == "eval":
        from . import quality
        quality.run_eval()
    elif a.cmd == "history":
        from . import quality
        quality.history()
    elif a.cmd == "lint":
        from . import quality
        uncovered, n_problems = quality.lint()
        for u in uncovered[:None if a.uncovered else 15]:
            print("  " + u)
        if a.strict and n_problems:
            sys.exit(1)
    elif a.cmd == "status":
        with common.db() as conn:
            for layer, source, n in conn.execute(
                    "select layer, source, count(*) from documents group by 1,2 order by 1,2").fetchall():
                print("%-5s %-11s %5d pages" % (layer, source, n))
            print("chunks: %d   links: %d" % conn.execute(
                "select (select count(*) from chunks), (select count(*) from edges)").fetchone())
    elif a.cmd == "reset":
        with common.db(a.database_url) as conn:
            conn.execute("drop table if exists eval_runs, edges, chunks, documents cascade")
        print("dropped. Run ./kb index to rebuild.")
    elif a.cmd == "push":
        from . import index
        common.migrate(a.database_url)
        index.run(a.database_url)
    else:
        p.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
