"""Shared config, DB access, embeddings and markdown helpers."""
import hashlib
import math
import os
import pathlib
import re

import httpx
import psycopg
import yaml

ROOT = pathlib.Path(os.environ.get("KB_ROOT") or pathlib.Path(__file__).resolve().parent.parent)


def _load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://kb:kb@127.0.0.1:54329/kb")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:4b")
EMBED_DIM = int(os.environ.get("EMBED_DIM", "2560"))
# Prepended to search queries only (never to documents). Qwen3 embedding
# models are trained to expect it; leave empty for models that are not.
EMBED_QUERY_PREFIX = os.environ.get("EMBED_QUERY_PREFIX", "").replace("\\n", "\n")
# pgvector can only build an HNSW index on vectors of up to 2000 dimensions.
ANN_MAX_DIM = 2000
KB_EMBED = os.environ.get("KB_EMBED", "ollama")


def db(url=None):
    return psycopg.connect(url or DATABASE_URL, autocommit=True)


def migrate(url=None):
    if EMBED_DIM <= ANN_MAX_DIM:
        vec_index = ("create index if not exists chunks_vec_idx on chunks "
                     "using hnsw (embedding vector_cosine_ops);")
        how = "HNSW index"
    else:
        # Too wide for an index, so vector search is an exact scan: every
        # chunk is compared. Perfect recall, and fast at this corpus size.
        vec_index = "drop index if exists chunks_vec_idx;"
        how = "exact scan, no ANN index"
    with db(url) as conn:
        have = conn.execute(
            "select a.atttypmod from pg_attribute a join pg_class c on c.oid = a.attrelid "
            "where c.relname = 'chunks' and a.attname = 'embedding' "
            "and pg_table_is_visible(c.oid)").fetchone()
        if have and have[0] != EMBED_DIM:
            raise SystemExit("The index was built for %d-dim vectors but EMBED_DIM is now %d. "
                             "Run ./kb reset, then ./kb index." % (have[0], EMBED_DIM))
        for f in sorted((ROOT / "sql").glob("*.sql")):
            conn.execute(f.read_text().replace("{{DIM}}", str(EMBED_DIM))
                         .replace("{{VEC_INDEX}}", vec_index))
    print("schema ready (%s, %d dims, %s)" % (EMBED_MODEL, EMBED_DIM, how))


# ---------- embeddings ----------

def _hash_embed(text):
    vec = [0.0] * EMBED_DIM
    for tok in re.findall(r"[a-z0-9]+", text.lower()):
        vec[int(hashlib.md5(tok.encode()).hexdigest(), 16) % EMBED_DIM] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def embed(texts, query=False):
    """Return one vector per input text."""
    if KB_EMBED == "hash":
        return [_hash_embed(t) for t in texts]
    if query and EMBED_QUERY_PREFIX:
        texts = [EMBED_QUERY_PREFIX + t for t in texts]
    try:
        r = httpx.post(OLLAMA_URL + "/api/embed",
                       json={"model": EMBED_MODEL, "input": texts}, timeout=300)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise SystemExit("Embedding failed (%s). Is Ollama running and is '%s' pulled? "
                         "Try: ollama pull %s" % (e, EMBED_MODEL, EMBED_MODEL))
    vecs = r.json()["embeddings"]
    if vecs and len(vecs[0]) != EMBED_DIM:
        raise SystemExit("%s returns %d-dim vectors but EMBED_DIM=%d. Fix .env, then "
                         "./kb reset && ./kb index." % (EMBED_MODEL, len(vecs[0]), EMBED_DIM))
    return vecs


def vec_literal(v):
    return "[" + ",".join("%.6f" % x for x in v) + "]"


# ---------- markdown ----------

FM_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def split_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[m.end():]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_url(u):
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return u[:-3] if u.endswith(".md") else u
