#!/usr/bin/env python3
"""
wisp/serve.py — liten lokal server for fargremsan.

Serverar strip.html pa / och handelseloggen som JSON pa /events.json.
Loggen skrivs av ~/.claude/hooks/agent-events.sh.

    python3 serve.py            # port 8787
    python3 serve.py 9000
"""
import http.server, json, os, pathlib, sys

HAR = pathlib.Path(__file__).parent
LOGG = pathlib.Path.home() / ".agent-events.log"
ROST = HAR.parent / "robot" / "w4k7px.py"      # Claude Altairs alfabet — enda kallan
INST = HAR / "installningar.json"              # troskelvarden fran config.html
FORSLAG = HAR / "sprak" / "forslag.json"       # grinden: vantar pa ett ja
ORDBOK = HAR / "sprak" / "ordbok.json"


def las_logg(max_rader=5000):
    if not LOGG.exists():
        return []
    rader = LOGG.read_text(errors="replace").splitlines()[-max_rader:]
    ut = []
    for rad in rader:
        try:
            ut.append(json.loads(rad))
        except json.JSONDecodeError:
            continue
    return ut


def las_alfabet():
    """Plockar ALFABET och PARTIKLAR ur robot/w4k7px.py utan att importera den."""
    if not ROST.exists():
        return {}
    import ast
    trad = ast.parse(ROST.read_text())
    ut = {}
    for nod in trad.body:
        if not isinstance(nod, ast.Assign):
            continue
        for mal in nod.targets:
            if getattr(mal, "id", None) in ("ALFABET", "PARTIKLAR"):
                ut.update(ast.literal_eval(nod.value))
    return ut


def las_installningar():
    if INST.exists():
        try:
            return json.loads(INST.read_text())
        except json.JSONDecodeError:
            pass
    return {}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HAR), **kw)

    def _json(self, data):
        kropp = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(kropp)))
        self.end_headers()
        self.wfile.write(kropp)

    def _kropp(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n))

    def _godkann(self, stavelse):
        """Grinden. Ett forslag flyttar in i ordboken forst nar nagon sagt ja.

        Lanat rakt av fran ~/dev/self-recursive-symbolic-skills/vocab/kors.lisp:
        'jag kor inte sjalv. jag visar. du sager ja. forst da finns korningen.'
        """
        f = json.loads(FORSLAG.read_text())
        kvar, flyttad = [], None
        for post in f.get("forslag", []):
            if post.get("stavelse") == stavelse and flyttad is None:
                flyttad = post
            else:
                kvar.append(post)
        if flyttad is None:
            return {"godkand": False, "varfor": "hittade inget sadant forslag"}

        bok = json.loads(ORDBOK.read_text())
        bok.setdefault("stavelser", {})[stavelse] = {
            "betyder": flyttad.get("betyder"),
            "tecken": flyttad.get("tecken"),
            "tick": flyttad.get("tick"),
        }
        ORDBOK.write_text(json.dumps(bok, indent=2, ensure_ascii=False) + "\n")
        f["forslag"] = kvar
        FORSLAG.write_text(json.dumps(f, indent=2, ensure_ascii=False) + "\n")
        return {"godkand": True, "stavelse": stavelse}

    def do_POST(self):
        if self.path.startswith("/godkann"):
            try:
                data = self._kropp()
            except json.JSONDecodeError:
                self.send_error(400, "trasig json")
                return
            self._json(self._godkann(data.get("stavelse", "")))
            return
        if self.path.startswith("/installningar.json"):
            n = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(n))
            except json.JSONDecodeError:
                self.send_error(400, "trasig json")
                return
            INST.write_text(json.dumps(data, indent=2) + "\n")
            self._json({"sparat": True})
            return
        self.send_error(404)

    def do_GET(self):
        if self.path.startswith("/alfabet.json"):
            self._json(las_alfabet())
            return
        if self.path.startswith("/installningar.json"):
            self._json(las_installningar())
            return
        if self.path.startswith("/events.json"):
            kropp = json.dumps(las_logg()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(kropp)))
            self.end_headers()
            self.wfile.write(kropp)
            return
        if self.path in ("/", ""):
            self.path = "/strip.html"
        return super().do_GET()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    print(f"wisp-remsan: http://localhost:{port}   (logg: {LOGG})")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
