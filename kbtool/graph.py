"""Typed API graph: product -> service -> RPC -> messages.

Built by parsing the API reference pages, so every edge is something the page
states. Nothing here is inferred by a model.
"""
import json
import re

from .common import db
from .index import HEAD_RE, MESSAGE_SECTIONS, TAG_RE, api_info

RPC_RE = re.compile(r"rpc\s+(\w+)\s*\(\s*(?:stream\s+)?([\w.]+)\s*\)\s*returns\s*\(\s*(?:stream\s+)?([\w.]+)\s*\)")
MSG_NAME_RE = re.compile(r"^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$")
ANCHOR_RE = re.compile(r"\]\(#([a-z0-9_-]+)\)")


def parse_api_page(body):
    """Return (request, response, {message: set(anchors it links to)})."""
    sig = RPC_RE.search(body)
    request, response = (sig.group(2), sig.group(3)) if sig else (None, None)
    messages, path, current, fence = {}, [], None, False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else HEAD_RE.match(line)
        if m:
            level = len(m.group(1))
            del path[level - 1:]
            name = TAG_RE.sub("", m.group(2)).strip()
            path.append(name)
            in_messages = any(h in MESSAGE_SECTIONS for h in path[:-1])
            current = name if in_messages and MSG_NAME_RE.match(name) else None
            if current:
                messages.setdefault(current, set())
        elif current:
            messages[current].update(ANCHOR_RE.findall(line))
    return request, response, messages


def build(conn, texts):
    """Rebuild entities and relations from the API pages. Cheap, so done in full."""
    doc_ids = dict(conn.execute("select path, id from documents where path like 'raw/api/%'").fetchall())
    ents, rels = {}, set()

    def ent(kind, product, name, doc_id=None):
        key = (kind, product, name)
        if key not in ents or (doc_id and not ents[key]):
            ents[key] = doc_id
        return key

    for rel, (meta, body) in texts.items():
        info = api_info(rel)
        if not info or info[2] in ("index", "rest-endpoints"):
            continue
        product, service, _ = info
        title = str(meta.get("title") or "")
        request, response, messages = parse_api_page(body)
        if not title or (request is None and not messages):
            continue
        p = ent("product", product, product)
        s = ent("service", product, service)
        r = ent("rpc", product, service + "." + title, doc_ids.get(rel))
        rels.add((p, s, "has_service"))
        rels.add((s, r, "has_rpc"))
        by_anchor = {re.sub(r"[^a-z0-9]", "", n.lower()): n for n in messages}
        for name, anchors in messages.items():
            m = ent("message", product, name)
            short = name.split(".")[-1]
            kind = "uses"
            if request and short == request.split(".")[-1]:
                kind = "request"
            elif response and short == response.split(".")[-1]:
                kind = "response"
            rels.add((r, m, kind))
            for a in anchors:
                target = by_anchor.get(re.sub(r"[^a-z0-9]", "", a))
                if target and target != name:
                    rels.add((m, ent("message", product, target), "contains"))

    conn.execute("truncate relations, entities restart identity")
    ids = {}
    for (kind, product, name), doc_id in sorted(ents.items(), key=lambda kv: kv[0]):
        ids[(kind, product, name)] = conn.execute(
            "insert into entities(kind, name, product, doc_id) values (%s,%s,%s,%s) returning id",
            (kind, name, product, doc_id)).fetchone()[0]
    with conn.cursor() as cur:
        cur.executemany("insert into relations(src, dst, kind) values (%s,%s,%s)",
                        sorted((ids[a], ids[b], k) for a, b, k in rels))
    return len(ents), len(rels)


def lookup(conn, name, product=None, limit=8):
    """Entities matching a name, each with its relations in both directions."""
    rows = conn.execute(
        "select e.id, e.kind, e.name, e.product, d.path, d.url, d.version from entities e "
        "left join documents d on d.id = e.doc_id "
        "where (lower(e.name) = lower(%s) or lower(e.name) like '%%.' || lower(%s) "
        "       or replace(lower(e.name), '-', '') like '%%' || replace(lower(%s), '-', '') || '%%') "
        "      and (%s::text is null or e.product = %s) "
        "order by (lower(e.name) = lower(%s) or lower(e.name) like '%%.' || lower(%s)) desc, "
        "         length(e.name), e.product limit %s",
        (name, name, name, product, product, name, name, limit)).fetchall()
    out = []
    for eid, kind, ename, prod, path, url, version in rows:
        item = {"kind": kind, "name": ename, "product": prod, "path": path, "url": url,
                "version": version, "out": {}, "in": {}}
        for k, n, kd in conn.execute(
                "select r.kind, e.name, e.kind from relations r join entities e on e.id = r.dst "
                "where r.src = %s order by 1, 2", (eid,)).fetchall():
            item["out"].setdefault(k, []).append(n)
        for k, n, kd in conn.execute(
                "select r.kind, e.name, e.kind from relations r join entities e on e.id = r.src "
                "where r.dst = %s order by 1, 2", (eid,)).fetchall():
            item["in"].setdefault(k, []).append(n)
        out.append(item)
    return out


LABELS_OUT = {"has_service": "services", "has_rpc": "RPCs", "request": "request message",
              "response": "response message", "uses": "also uses messages", "contains": "contains messages"}
LABELS_IN = {"has_service": "product", "has_rpc": "service", "request": "request of",
             "response": "response of", "uses": "used by RPCs", "contains": "contained in messages"}


def run(name, product, as_json):
    with db() as conn:
        items = lookup(conn, name, product)
    if as_json:
        print(json.dumps(items, indent=2))
        return
    if not items:
        print("No API product, service, RPC or message matches '%s'." % name)
        return
    for it in items:
        print("\n%s  %s  [%s]%s" % (it["kind"].upper(), it["name"], it["product"],
                                     "  " + it["version"] if it["version"] else ""))
        if it["url"]:
            print("  " + it["url"])
        for k, names in it["in"].items():
            print("  %s: %s" % (LABELS_IN.get(k, k), _short(names)))
        for k, names in it["out"].items():
            print("  %s: %s" % (LABELS_OUT.get(k, k), _short(names)))


def _short(names, n=12):
    return ", ".join(names[:n]) + (" ... (%d more)" % (len(names) - n) if len(names) > n else "")
