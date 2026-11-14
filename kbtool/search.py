"""Phase 4: retrieval. Four modes so the eval can tell you which one earns its keep.

  kw      Postgres full-text (good for exact RPC names, flags, error strings)
  vec     pgvector cosine similarity (good for "how do I..." questions)
  hybrid  reciprocal-rank fusion of kw + vec
  graph   hybrid, then a boost for chunks whose page is linked to other strong hits
"""
import json
import re

from .common import db, embed, vec_literal

MODES = ("kw", "vec", "hybrid", "graph")
CAND = 50
RRF_K = 60
# Ranking weights. These are hypotheses, not tuned constants: change one,
# run ./kb eval, and compare in ./kb history.
W_VEC = 1.0          # weight of the vector ranking in the fusion
W_KW = 0.7           # keyword ranking counts for less: common API words ("call",
                     # "return") match hundreds of chunks and carry little signal
GRAPH_BOOST = 0.25   # share of a linked page's score added in graph mode
HUB_DEGREE = 25      # pages with more links than this (category and index pages)
                     # link to everything, so they do not boost their neighbours
PRODUCT_BOOST = 1.5  # multiplier when the question names a product and the chunk
                     # belongs to it ("LiT GetInfo" should not return lnd's GetInfo)
PRODUCT_ALIASES = {
    "lnd": ["lnd", "lncli"],
    "loop": ["loop", "loopd"],
    "pool": ["pool", "poold"],
    "faraday": ["faraday", "frcli"],
    "taproot-assets": ["taproot assets?", "tapd", "tapcli"],
    "lit": ["lit", "litd", "litcli", "lightning terminal"],
    "aperture": ["aperture"],
    "wavelength": ["wavelength", "wavecli"],
}


def products_named(q):
    return [p for p, names in PRODUCT_ALIASES.items()
            if re.search(r"\b(" + "|".join(names) + r")\b", q, re.I)]


def _or_query(q):
    terms = re.findall(r"[A-Za-z0-9_]+", q)
    return " OR ".join(terms) if terms else ""


def search(conn, q, mode="graph", k=8, product=None, layer=None):
    scores, sim = {}, {}
    if mode in ("vec", "hybrid", "graph"):
        qv = vec_literal(embed([q], query=True)[0])
        rows = conn.execute(
            "select id, 1 - (embedding <=> %s::vector) from chunks "
            "order by embedding <=> %s::vector limit %s", (qv, qv, CAND)).fetchall()
        for rank, (cid, s) in enumerate(rows, 1):
            scores[cid] = scores.get(cid, 0.0) + W_VEC / (RRF_K + rank)
            sim[cid] = float(s)
    if mode in ("kw", "hybrid", "graph") and _or_query(q):
        rows = conn.execute(
            "select id from chunks, websearch_to_tsquery('english', %s) t "
            "where tsv @@ t order by ts_rank_cd(tsv, t) desc limit %s",
            (_or_query(q), CAND)).fetchall()
        w = 1.0 if mode == "kw" else W_KW
        for rank, (cid,) in enumerate(rows, 1):
            scores[cid] = scores.get(cid, 0.0) + w / (RRF_K + rank)
    if not scores:
        return []

    meta = {r[0]: r[1:] for r in conn.execute(
        "select c.id, c.doc_id, c.heading, c.content, d.path, d.layer, d.product, d.title, d.url "
        "from chunks c join documents d on d.id = c.doc_id where c.id = any(%s)",
        (list(scores),)).fetchall()}

    if mode != "kw":
        named = products_named(q)
        if named:
            for cid in scores:
                if meta[cid][5] in named:
                    scores[cid] *= PRODUCT_BOOST

    if mode == "graph":
        doc_score = {}
        for cid, s in scores.items():
            doc = meta[cid][0]
            doc_score[doc] = max(doc_score.get(doc, 0.0), s)
        docs = list(doc_score)
        degree = dict(conn.execute(
            "select d, count(*) from (select src as d from edges where src = any(%s) "
            "union all select dst from edges where dst = any(%s)) e group by d", (docs, docs)).fetchall())
        neigh = {}
        for a, b in conn.execute(
                "select src, dst from edges where src = any(%s) and dst = any(%s)", (docs, docs)).fetchall():
            if degree.get(a, 0) <= HUB_DEGREE:
                neigh.setdefault(b, set()).add(a)
            if degree.get(b, 0) <= HUB_DEGREE:
                neigh.setdefault(a, set()).add(b)
        base = dict(scores)
        for cid in scores:
            doc = meta[cid][0]
            if doc in neigh:
                scores[cid] = base[cid] + GRAPH_BOOST * max(doc_score[n] for n in neigh[doc])

    # Collapse identical chunks: show the best-ranked copy once and list the
    # other pages that contain the same text.
    out, by_text = [], {}
    for cid, s in sorted(scores.items(), key=lambda kv: -kv[1]):
        doc_id, heading, content, path, lyr, prod, title, url = meta[cid]
        if product and prod != product:
            continue
        if layer and lyr != layer:
            continue
        if content in by_text:
            dup = by_text[content]
            if path != dup["path"] and path not in dup["also_in"]:
                dup["also_in"].append(path)
            continue
        if len(out) >= k:
            continue
        hit = {"score": round(s, 5), "similarity": round(sim[cid], 3) if cid in sim else None,
               "layer": lyr, "product": prod, "title": title, "heading": heading,
               "path": path, "url": url, "content": content, "also_in": []}
        by_text[content] = hit
        out.append(hit)
    return out


def run(q, mode, k, product, layer, as_json):
    with db() as conn:
        hits = search(conn, q, mode, k, product, layer)
    if as_json:
        print(json.dumps(hits, indent=2))
        return
    if not hits:
        print("No matches. Nothing in the knowledge base supports an answer.")
        return
    for i, h in enumerate(hits, 1):
        simtxt = "" if h["similarity"] is None else "  sim %.2f" % h["similarity"]
        print("\n%d. [%s] %s%s%s" % (i, h["layer"], h["title"],
                                     " > " + h["heading"] if h["heading"] else "", simtxt))
        print("   " + (h["url"] or h["path"]))
        if h["also_in"]:
            print("   same text on %d other page(s)" % len(h["also_in"]))
        snippet = " ".join(h["content"].split())
        print("   " + snippet[:300] + ("..." if len(snippet) > 300 else ""))
