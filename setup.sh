#!/usr/bin/env bash
# Phase 0: one-time setup of the Lightning KB on this Mac.
# Safe to re-run. It installs nothing system-wide without asking.
set -euo pipefail
cd "$(dirname "$0")"

say()  { printf "\n\033[1m%s\033[0m\n" "$*"; }
ask()  { read -r -p "$1 [y/N] " a; [[ "$a" =~ ^[Yy]$ ]]; }
have() { command -v "$1" >/dev/null 2>&1; }

say "0/5  Checking prerequisites"
missing=0
have python3 || { echo "  python3 missing: run 'xcode-select --install' or 'brew install python'"; missing=1; }
have git     || { echo "  git missing: run 'xcode-select --install'"; missing=1; }
if ! have docker; then
  echo "  Docker missing: install Docker Desktop (https://www.docker.com/products/docker-desktop/)"; missing=1
elif ! docker info >/dev/null 2>&1; then
  echo "  Docker is installed but not running: open Docker Desktop, then re-run."; missing=1
fi
if ! have ollama; then
  if have brew && ask "  Ollama (local embeddings) is missing. Install it with Homebrew?"; then
    brew install ollama
  else
    echo "  Ollama missing: install from https://ollama.com/download"; missing=1
  fi
fi
[ "$missing" = 0 ] || { echo; echo "Fix the items above and run ./setup.sh again."; exit 1; }
echo "  ok"

say "1/5  Python environment"
# --copies: a venv with symlinks fails on exFAT-formatted external drives.
[ -x .venv/bin/python ] || python3 -m venv --copies .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
echo "  ok"

say "2/5  Postgres + pgvector (Docker, 127.0.0.1:54329)"
docker compose up -d --wait
./kb migrate

say "3/5  Embedding model"
if ! curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
  echo "  starting Ollama in the background"
  (nohup ollama serve >/tmp/ollama-kb.log 2>&1 &)
  for _ in $(seq 1 20); do curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1 && break; sleep 1; done
fi
MODEL="$(grep "^EMBED_MODEL=" .env | cut -d= -f2)"
ollama pull "$MODEL"

say "4/5  Git"
[ -d .git ] || git init -q
# Commits in this repo are authored by Pauloes only (repo-local setting).
git config user.name "pauloes"
git config user.email "pauloes@btechs.io"
echo "  commits here are authored as $(git config user.name) <$(git config user.email)>"

say "5/5  Done. Test it in this order:"
cat <<'EOF'

  ./kb crawl --limit 5      # 15 pages, ~10 seconds: proves the crawl works
  ./kb index                # embeds them
  ./kb search "how do I get my node pubkey"
  ./kb status

  Then the real thing:
  ./kb crawl                # ~700 pages, a few minutes
  ./kb index
  ./kb eval                 # scores keyword vs vector vs hybrid vs graph

  Wiki:  open this folder as a vault in Obsidian, start Claude Code here
         (run: claude) and type /build-wiki. It writes, checks, commits and
         merges one product at a time. The rules it follows are in CLAUDE.md.
EOF
