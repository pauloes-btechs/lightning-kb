# Lightning KB

A local, free knowledge base over the Lightning Labs docs: an LLM-maintained
wiki you read in Obsidian, plus a Postgres + pgvector index with a link
graph and a retrieval eval.

## Phases

| # | Phase | Command | Output |
|---|---|---|---|
| 0 | Setup | `./setup.sh` | venv, Postgres in Docker, embedding model |
| 1 | Ingest | `./kb crawl` | `raw/` (about 700 markdown pages) |
| 2 | Wiki | Claude Code: `/build-wiki` | `wiki/` pages with citations |
| 3 | Index | `./kb index` | chunks, embeddings, link graph |
| 4 | Retrieve | `./kb search "..."` | ranked chunks with source URLs |
| 5 | Evaluate | `./kb eval`, `./kb lint` | hit@1, hit@5, MRR per mode; wiki health |

Sources are listed in `sources.yaml`. The agent's rules are in `CLAUDE.md`.
Golden questions are in `evals/golden.yaml`.

## First run on a new machine

    git clone https://github.com/pauloes-btechs/lightning-kb.git
    cd lightning-kb && ./setup.sh
    ./kb crawl && ./kb index && ./kb eval

`raw/` and the database are not in git; these commands rebuild both.

## Autonomous wiki build

Start Claude Code in this folder and run `/build-wiki`. It works one product
at a time:

| Role | Where it is defined | What it does |
|---|---|---|
| Orchestrator | `.claude/skills/build-wiki/SKILL.md` | Picks the next scope, branches, delegates, commits, pushes, opens the PR, merges |
| Writer | `.claude/agents/wiki-writer.md` | Writes wiki pages from `raw/` with a citation per paragraph |
| Checker | `.claude/agents/wiki-checker.md` | Read-only; re-verifies every claim against the cited source, returns PASS or FAIL |
| CI | `.github/workflows/checks.yml` | Structural lint on every pull request |

A scope merges only when the checker passes, `./kb lint --strict` is clean
and CI is green. Merges are fast-forward, and `.claude/settings.json` turns
off Claude Code's commit and PR attribution, so every commit is authored by
the repo's configured git user alone.

## Moving the index to Supabase or Neon

    ./kb push "postgresql://USER:PASSWORD@HOST/DB?sslmode=require"

This creates the same tables there and rebuilds the index from the local
files. To make it the default, put that URL in `.env` as `DATABASE_URL`.

## Changing the embedding model

Edit `EMBED_MODEL` and `EMBED_DIM` in `.env`, then
`ollama pull <model> && ./kb reset && ./kb index && ./kb eval`.
`./kb history` shows whether the change helped.

## Publishing the wiki

`.github/workflows/pages.yml` builds `wiki/` into a site with graph view
and search. It only runs when you start it from the Actions tab.
