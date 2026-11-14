---
name: build-wiki
description: Orchestrates the autonomous wiki build - one product at a time through writer, checker, commit, push, PR, checks and merge. Run as /build-wiki, optionally with a scope such as "/build-wiki loop".
---
# Build the wiki

You are the orchestrator. You do not write wiki pages yourself: you plan,
delegate to the `wiki-writer` and `wiki-checker` subagents, run the checks,
and handle git. Work through scopes in order, one branch per scope.

## Before the first scope

1. `git status` must be clean and on `main`; `git pull --ff-only`.
2. `git config user.email` must print `pauloes@btechs.io`. If not, stop and
   say so. Never pass `--author`, never add `Co-Authored-By` or any other
   trailer or AI credit to a commit message or PR body.
3. `./kb status` must show raw pages. If `raw/` is empty, run `./kb crawl`
   then `./kb index`.

## Plan first

If `wiki-plan.yaml` does not exist, write it before any page: every page you
intend to create, as `pages: [{slug, title, type, scope}]`. Slugs are the
future file names. Lint accepts links to planned slugs, so products can be
built and merged one at a time and still link to each other. Commit the plan
on its own branch and merge it. Remove nothing from it as pages land; lint
reports how many planned pages are still unwritten.

## Scope order

If the scope is `refresh`, run `./kb stale` and send each listed page back
through the writer and checker against its changed sources, one branch for
the batch. If the user named any other scope, do only that. Otherwise take the first of these
that `./kb lint --uncovered` shows still has uncited raw files:

    loop, pool, faraday, lit, taproot-assets, lnd, aperture, wavelength,
    then the concept pages under raw/docs (the-lightning-network)

A scope is the raw files whose path contains that product name, from the
guide, the API reference and (for wavelength) `raw/wavelength/`. Split a
scope of more than about 40 raw files into parts (for lnd: one part per
group of services) and treat each part as its own branch.

## For each scope

1. `git checkout -b wiki/<scope>` from an up-to-date `main`.
2. **Write.** Start `wiki-writer` with the scope name and its raw file list.
3. **Index and lint.** `./kb index` then `./kb lint --strict`. Problems go
   back to the writer.
4. **Check.** Start `wiki-checker` with the list of pages the writer
   returned. It must be a fresh subagent each time.
5. **Fix loop.** On FAIL, send the findings to `wiki-writer`, then repeat
   steps 3 and 4. At most three rounds.
6. **Evaluate.** `./kb eval`. If MRR for the best mode dropped compared with
   the previous run in `./kb history`, note it in the PR body; it is not a
   blocker.
7. **Commit.** `git add wiki evals` and commit with a message of the form
   `wiki: add <scope> (<n> pages)`. One commit per scope, plus one per fix
   round if you prefer.
8. **Push and PR.** `git push origin wiki/<scope>`, then
   `gh pr create --base main --title "wiki: <scope>" --body <body>`. The body
   holds: pages added, raw coverage before and after, the checker's final
   verdict line, and the eval table. If `gh` is not installed, skip the PR.
9. **Gate.** `gh pr checks --watch`. Merge only if all of these hold:
   checker verdict PASS, `./kb lint --strict` clean, GitHub checks green.
10. **Merge.** `git checkout main && git merge --ff-only wiki/<scope> &&
    git push origin main`, then delete the branch locally and on origin.
    Fast-forward only, so every commit on `main` keeps its author.
11. **If the gate fails** after three rounds: push what you have, leave the
    PR open with the remaining findings in its body, switch back to `main`,
    and go on to the next scope.

## Stop and ask before

- anything that deletes files outside `wiki/`, rewrites history or force
  pushes;
- changing `CLAUDE.md`, `sources.yaml`, the schema or the workflows;
- running the "Publish wiki to GitHub Pages" workflow for the first time;
- anything that costs money or needs a new credential.

## When you finish (or stop)

Report: scopes merged, scopes left open and why, wiki page count, raw
coverage, and the latest eval line.
