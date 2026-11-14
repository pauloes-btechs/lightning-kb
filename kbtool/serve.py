"""Local chat UI: ./kb serve, then open http://127.0.0.1:8787

Loopback only. No dependencies beyond the standard library.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import ask, graph
from .common import EMBED_MODEL, ROOT, db
from .search import MODES, search

UI = ROOT / "kbtool" / "ui.html"


class Handler(BaseHTTPRequestHandler):
    server_version = "lightning-kb"

    def log_message(self, fmt, *args):
        pass

    def _host_ok(self):
        # Reject requests addressed to any other name (DNS rebinding) and
        # cross-site requests from pages on other origins.
        host = (self.headers.get("Host") or "").split(":")[0]
        if host not in ("127.0.0.1", "localhost"):
            return False
        origin = self.headers.get("Origin")
        return not origin or urlparse(origin).hostname in ("127.0.0.1", "localhost")

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        if ctype == "text/html":
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
                             "connect-src 'self'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self._host_ok():
            return self._send(403, {"error": "forbidden"})
        url = urlparse(self.path)
        q = parse_qs(url.query)
        try:
            if url.path == "/":
                return self._send(200, UI.read_bytes(), "text/html")
            if url.path == "/api/status":
                with db() as conn:
                    docs, chunks, wiki, ents = conn.execute(
                        "select (select count(*) from documents), (select count(*) from chunks), "
                        "(select count(*) from documents where layer='wiki'), "
                        "(select count(*) from entities)").fetchone()
                return self._send(200, {"documents": docs, "chunks": chunks, "wiki_pages": wiki,
                                        "api_entities": ents, "embed_model": EMBED_MODEL,
                                        "engine": ask.engine_available()})
            if url.path == "/api/search":
                mode = q.get("mode", ["graph"])[0]
                with db() as conn:
                    hits = search(conn, q.get("q", [""])[0][:500], mode if mode in MODES else "graph", 8)
                return self._send(200, hits)
            if url.path == "/api/chunk":
                cid = int(q.get("id", ["0"])[0])
                with db() as conn:
                    row = conn.execute(
                        "select c.doc_id, c.ord, c.heading, c.content, d.path, d.url, d.version, d.layer "
                        "from chunks c join documents d on d.id = c.doc_id where c.id = %s", (cid,)).fetchone()
                    if not row:
                        return self._send(404, {"error": "no such passage"})
                    around = conn.execute(
                        "select ord, heading, content from chunks where doc_id = %s and ord between %s and %s "
                        "order by ord", (row[0], row[1] - 1, row[1] + 1)).fetchall()
                return self._send(200, {"id": cid, "heading": row[2], "content": row[3], "path": row[4],
                                        "url": row[5], "version": row[6], "layer": row[7],
                                        "around": [{"ord": o, "heading": h, "content": c, "current": o == row[1]}
                                                   for o, h, c in around]})
            if url.path == "/api/graph":
                with db() as conn:
                    return self._send(200, graph.lookup(conn, q.get("name", [""])[0][:200]))
            return self._send(404, {"error": "not found"})
        except Exception as e:
            return self._send(500, {"error": str(e).splitlines()[0][:300]})

    def do_POST(self):
        if not self._host_ok() or "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._send(403, {"error": "forbidden"})
        if urlparse(self.path).path != "/api/ask":
            return self._send(404, {"error": "not found"})
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 200000)
            body = json.loads(self.rfile.read(length) or b"{}")
            question = str(body.get("question") or "").strip()[:2000]
            if not question:
                return self._send(400, {"error": "empty question"})
            history = body.get("history") if isinstance(body.get("history"), list) else []
            return self._send(200, ask.answer(question, history, bool(body.get("passages_only"))))
        except Exception as e:
            return self._send(500, {"error": str(e).splitlines()[0][:300]})


def run(port):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("Lightning KB chat: http://127.0.0.1:%d   (Ctrl-C to stop)" % port)
    if not ask.engine_available():
        print("Note: the `claude` command was not found, so answers will be passages only.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
