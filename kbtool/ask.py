"""Answer a question from the knowledge base, with every citation checked.

The answer is written by Claude Code running headless on this machine
(`claude -p`), which does its own multi-step retrieval with ./kb search,
./kb graph and ./kb show. This module then verifies the result itself: each
citation must quote text that really is in the cited passage.
"""
import json
import os
import re
import shlex
import shutil
import subprocess

from .common import ROOT, db, split_frontmatter
from .search import search

SKILL = ROOT / ".claude" / "skills" / "ask" / "SKILL.md"
TIMEOUT = int(os.environ.get("KB_ASK_TIMEOUT", "300"))
SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "citations": {"type": "array", "items": {
            "type": "object",
            "properties": {"n": {"type": "integer"}, "chunk_id": {"type": "integer"},
                           "quote": {"type": "string"}},
            "required": ["n", "chunk_id", "quote"]}},
        "searches": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string", "enum": ["supported", "partial", "not_found"]},
    },
    "required": ["answer", "citations", "status"],
}
OUTPUT_RULES = """
## Output for this run

Reply with one JSON object and nothing else:
- "answer": markdown. Every factual sentence ends with one or more markers like [1].
- "citations": one entry per marker: {"n": 1, "chunk_id": <the "id" of the search
  hit>, "quote": "<8 to 30 words copied character for character from that hit's
  content>"}. The quote is checked by a program against the stored passage; a
  paraphrase fails the check.
- "searches": the ./kb commands you ran, in order.
- "gaps": parts of the question the sources did not answer.
- "status": "supported", "partial" or "not_found".
"""


def engine_available():
    return bool(os.environ.get("KB_ASK_CMD")) or shutil.which("claude") is not None


def _rules():
    _, body = split_frontmatter(SKILL.read_text()) if SKILL.exists() else ({}, "")
    return body


def _prompt(question, history):
    parts = [_rules(), OUTPUT_RULES]
    for turn in (history or [])[-3:]:
        parts.append("Earlier question: %s\nEarlier answer: %s" % (turn.get("q", ""), turn.get("a", "")[:1500]))
    parts.append("Question: " + question)
    return "\n\n".join(parts)


def _extract_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except ValueError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


def _run_engine(question, history):
    prompt = _prompt(question, history)
    override = os.environ.get("KB_ASK_CMD")
    if override:                       # test hook: prompt on stdin, answer JSON on stdout
        proc = subprocess.run(shlex.split(override), input=prompt, capture_output=True,
                              text=True, cwd=str(ROOT), timeout=TIMEOUT)
        return _extract_json(proc.stdout)
    cmd = ["claude", "-p", prompt, "--output-format", "json",
           "--json-schema", json.dumps(SCHEMA),
           "--allowedTools", "Bash(./kb search *)", "Bash(./kb graph *)", "Bash(./kb show *)", "Read",
           "--permission-mode", "dontAsk", "--max-turns", "30"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), timeout=TIMEOUT)
    envelope = json.loads(proc.stdout)
    if envelope.get("is_error"):
        raise RuntimeError(str(envelope.get("result") or "Claude Code reported an error")[:300])
    if isinstance(envelope.get("structured_output"), dict):
        return envelope["structured_output"]
    return _extract_json(str(envelope.get("result") or ""))


def _norm(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)     # markdown links -> their text
    return re.sub(r"[\s`*_|\\]+", " ", text).strip().lower()


def verify(conn, result):
    """Attach the cited passages and check each quote against its passage."""
    cites = result.get("citations") or []
    ids = [c.get("chunk_id") for c in cites if isinstance(c.get("chunk_id"), int)]
    rows = {r[0]: r[1:] for r in conn.execute(
        "select c.id, c.heading, c.content, d.path, d.url, d.layer, d.version, d.title "
        "from chunks c join documents d on d.id = c.doc_id where c.id = any(%s)", (ids,)).fetchall()}
    out = []
    for c in cites:
        row = rows.get(c.get("chunk_id"))
        item = {"n": c.get("n"), "chunk_id": c.get("chunk_id"), "quote": c.get("quote", "")}
        if not row:
            item.update(verified=False, problem="cited passage does not exist")
        else:
            heading, content, path, url, layer, version, title = row
            quote = _norm(item["quote"])
            ok = len(quote) >= 12 and quote in _norm(content)
            item.update(verified=ok, heading=heading or title, passage=content, path=path, url=url,
                        layer=layer, version=version,
                        problem=None if ok else "quote not found in the cited passage")
        out.append(item)
    answer = result.get("answer", "")
    markers = set(int(m) for m in re.findall(r"\[(\d+)\]", answer))
    known = set(c["n"] for c in out)
    paragraphs = [p for p in re.split(r"\n\s*\n", answer) if p.strip() and not p.lstrip().startswith(("#", "```"))]
    uncited = sum(1 for p in paragraphs if not re.search(r"\[\d+\]", p))
    result["citations"] = out
    result["check"] = {
        "verified": sum(1 for c in out if c["verified"]),
        "failed": sum(1 for c in out if not c["verified"]),
        "markers_without_source": sorted(markers - known),
        "uncited_paragraphs": uncited if result.get("status") != "not_found" else 0,
    }
    return result


def _passages_only(conn, question, note):
    hits = search(conn, question, "graph", 6)
    cites = [{"n": i, "chunk_id": h["id"], "quote": "", "verified": True, "heading": h["heading"] or h["title"],
              "passage": h["content"], "path": h["path"], "url": h["url"], "layer": h["layer"],
              "version": h["version"], "problem": None} for i, h in enumerate(hits, 1)]
    return {"answer": "", "citations": cites, "searches": ['./kb search "%s"' % question], "gaps": [],
            "status": "passages_only", "note": note,
            "check": {"verified": 0, "failed": 0, "markers_without_source": [], "uncited_paragraphs": 0}}


def answer(question, history=None, passages_only=False):
    with db() as conn:
        if passages_only:
            return _passages_only(conn, question, "Passages only: no written answer was requested.")
        if not engine_available():
            return _passages_only(conn, question, "Claude Code (the `claude` command) was not found, so "
                                  "there is no written answer. These are the best-matching passages.")
        try:
            result = _run_engine(question, history)
        except subprocess.TimeoutExpired:
            return _passages_only(conn, question, "The answer took longer than %d seconds and was stopped. "
                                  "These are the best-matching passages." % TIMEOUT)
        except Exception as e:
            msg = str(e)
            hint = ""
            if any(w in msg.lower() for w in ("authenticat", "oauth", "log in", "login", "401")):
                hint = (" Claude Code is signed out: run `claude` in a terminal, type /login, "
                        "then ask again (the chat does not need restarting).")
            return _passages_only(conn, question, "Claude Code could not produce an answer (%s).%s These are "
                                  "the best-matching passages." % (msg[:200], hint))
        return verify(conn, result)


def run(question, as_json, passages_only):
    result = answer(question, None, passages_only)
    if as_json:
        print(json.dumps(result, indent=2))
        return
    if result.get("note"):
        print(result["note"] + "\n")
    if result["answer"]:
        print(result["answer"] + "\n")
    for c in result["citations"]:
        mark = "    " if result["status"] == "passages_only" else ("ok  " if c["verified"] else "FAIL")
        print("[%s] %s %s" % (c["n"], mark, c.get("heading") or ""))
        print("      " + (c.get("url") or c.get("path") or "?") + ("  (%s)" % c["version"] if c.get("version") else ""))
        if c.get("problem"):
            print("      " + c["problem"])
    chk = result["check"]
    if result["answer"]:
        print("\nCitation check: %d verified, %d failed%s%s" % (
            chk["verified"], chk["failed"],
            ", %d paragraph(s) without a citation" % chk["uncited_paragraphs"] if chk["uncited_paragraphs"] else "",
            ", markers with no source: %s" % chk["markers_without_source"] if chk["markers_without_source"] else ""))
    for g in result.get("gaps") or []:
        print("Not covered by the sources: " + g)
