#!/usr/bin/env python3
"""
ogat — vision-loopen
Titel: Roboten tittar, tanker en tanke, sager den i tick och tock
Datum: 2026-09-03

Var N:e sekund: ta en bild -> fraga claude-cli vad den ser ->
fa tillbaka EN reaktion ur vokabularen plus ETT kort ord ->
spela ordet i tick och tock.

Ingen text-till-tal. Ingen inspelning sparas. Bara ogonblicket.

    python3 v8n4rq.py                 # kor loopen, overlay pa :8080
    python3 v8n4rq.py --torr          # ingen kamera, ingen claude — testa flodet
    python3 v8n4rq.py --intervall 8   # langsammare

Overlay: http://<robotens-ip>:8080  (telefonen pa samma hotspot)
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer

HAR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HAR)

import importlib.util
_spec = importlib.util.spec_from_file_location("tickspeak", os.path.join(HAR, "w4k7px.py"))
tickspeak = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tickspeak)

OVERLAY = os.path.join(HAR, "k9x3mt.html")

# ---------------------------------------------------------------- vokabularen
# Robotens hela kansloregister. Fler an sa och han slutar vara en valp.
REAKTIONER = {
    "nyfiken":  "lutar sig fram, tittar",
    "hej":      "halsar",
    "vad":      "forstar inte, undrar",
    "skratt":   "tycker nagot ar roligt",
    "protest":  "vagrar, haller inte med",
    "forlat":   "ber om ursakt, backar",
    "flykt":    "drar sig undan",
    "trott":    "orkar inte mer",
}

PROMPT = """Du ar en liten robot pa gatan. Du ser den har bilden: {bild}

Las bilden och svara som roboten skulle reagera — nyfiket, valpigt, aldrig hotfullt.

Svara med ENBART en rad kompakt JSON, inget annat:
{{"reaktion": "<en av: {taggar}>", "ord": "<ett eller tva korta svenska ord>", "varfor": "<max 8 ord, vad du sag>"}}

"ord" ar det roboten sager. Det spelas i klickljud utan vokaler, sa hall det
kort och konsonantrikt. Inga namn pa personer. Inga fragor om kanslig info."""


# ---------------------------------------------------------------- kameran
def hitta_kamera():
    """-> (namn, argumentbyggare) eller (None, None)"""
    kandidater = [
        ("rpicam-still",  lambda ut: ["rpicam-still", "-n", "-t", "300", "--width", "1024",
                                      "--height", "768", "-o", ut]),
        ("libcamera-still", lambda ut: ["libcamera-still", "-n", "-t", "300", "--width", "1024",
                                        "--height", "768", "-o", ut]),
        ("fswebcam",      lambda ut: ["fswebcam", "-q", "-r", "1024x768", "--no-banner", ut]),
        ("imagesnap",     lambda ut: ["imagesnap", "-q", ut]),
    ]
    for namn, bygg in kandidater:
        if shutil.which(namn):
            return namn, bygg
    return None, None


def ta_bild(bygg, sokvag):
    subprocess.run(bygg(sokvag), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
    return os.path.exists(sokvag) and os.path.getsize(sokvag) > 0


# ---------------------------------------------------------------- tanken
def fraga_claude(bildsokvag, timeout=60):
    """claude-cli laser bilden och svarar med JSON. -> dict

    Prompten gar via stdin — annars ater --allowed-tools upp den som
    ytterligare ett verktygsnamn."""
    prompt = PROMPT.format(bild=bildsokvag, taggar=", ".join(REAKTIONER))
    kommandon = [
        ["claude", "-p", "--allowed-tools", "Read"],
        ["claude", "-p", "--allowedTools", "Read"],
        ["claude", "-p"],
    ]
    sista = "claude misslyckades"
    for kmd in kommandon:
        try:
            r = subprocess.run(kmd, input=prompt, capture_output=True,
                               text=True, timeout=timeout)
        except FileNotFoundError:
            return {"fel": "claude-cli saknas i PATH"}
        except subprocess.TimeoutExpired:
            return {"fel": "claude svarade inte i tid"}
        if r.returncode == 0:
            return tolka(r.stdout)
        sista = (r.stderr or "").strip()[:200] or sista
        if "unknown option" not in sista.lower():
            break
    return {"fel": sista}


def tolka(text):
    """Plocka ut forsta JSON-objektet ur claudes svar."""
    start = text.find("{")
    while start != -1:
        djup = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                djup += 1
            elif text[i] == "}":
                djup -= 1
                if djup == 0:
                    try:
                        d = json.loads(text[start:i + 1])
                        if "reaktion" in d:
                            return d
                    except json.JSONDecodeError:
                        pass
                    break
        start = text.find("{", start + 1)
    return {"fel": "kunde inte lasa JSON ur svaret", "rasvar": text.strip()[:200]}


# ---------------------------------------------------------------- rosten
def sag(ord_):
    """Spela ordet i tick och tock. -> monsterstrangen som visas i overlayen."""
    monster, saknade = tickspeak.koda(ord_, behall_vokaler=False)
    if not monster:
        return "", saknade
    prov = tickspeak.rendera(monster)
    fd, tmp = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        tickspeak.skriv_wav(prov, tmp)
        tickspeak.spela(tmp)
    finally:
        os.unlink(tmp)
    return "  ".join(", ".join(o) for o in monster), saknade


# ---------------------------------------------------------------- tillstandet
class Tillstand:
    """Det roboten just nu tanker. Delas med overlayen, sparas aldrig."""

    def __init__(self):
        self.las = threading.Lock()
        self.d = {"status": "startar", "varv": 0, "reaktion": None, "ord": None,
                  "monster": None, "varfor": None, "fel": None, "tid": None,
                  "kamera": None, "intervall": None}

    def uppdatera(self, **kv):
        with self.las:
            self.d.update(kv, tid=time.strftime("%H:%M:%S"))

    def las_av(self):
        with self.las:
            return dict(self.d)


# ---------------------------------------------------------------- overlayen
def starta_server(tillstand, port):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path.startswith("/tillstand"):
                kropp = json.dumps(tillstand.las_av()).encode()
                typ = "application/json"
            else:
                try:
                    with open(OVERLAY, "rb") as f:
                        kropp = f.read()
                except FileNotFoundError:
                    kropp = b"overlayen k9x3mt.html saknas"
                    typ = "text/plain; charset=utf-8"
                else:
                    typ = "text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", typ)
            self.send_header("Content-Length", str(len(kropp)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(kropp)

    srv = HTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# ---------------------------------------------------------------- loopen
def main():
    p = argparse.ArgumentParser(description="Robotens vision-loop.")
    p.add_argument("-i", "--intervall", type=float, default=5.0,
                   help="sekunder mellan blickar (default 5)")
    p.add_argument("-p", "--port", type=int, default=8080, help="overlayens port")
    p.add_argument("--torr", action="store_true",
                   help="torrkorning: ingen kamera, ingen claude — testa flodet")
    p.add_argument("--tyst", action="store_true", help="visa men spela inget ljud")
    a = p.parse_args()

    tillstand = Tillstand()
    tillstand.uppdatera(intervall=a.intervall)
    starta_server(tillstand, a.port)
    print(f"overlay:  http://localhost:{a.port}   (och robotens IP fran telefonen)")

    kameranamn, bygg = (None, None) if a.torr else hitta_kamera()
    if not a.torr and not bygg:
        print("ingen kamera hittad (rpicam-still/libcamera-still/fswebcam/imagesnap)",
              file=sys.stderr)
        print("kor --torr for att testa resten av flodet", file=sys.stderr)
        return 1
    tillstand.uppdatera(kamera=kameranamn or "torrkorning", status="tittar")

    torra = [{"reaktion": "nyfiken", "ord": "vem", "varfor": "torrkorning"},
             {"reaktion": "vad", "ord": "hur sa", "varfor": "torrkorning"},
             {"reaktion": "flykt", "ord": "nej nej", "varfor": "torrkorning"},
             {"reaktion": "forlat", "ord": "forlat", "varfor": "torrkorning"}]

    varv = 0
    fd, bild = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    try:
        while True:
            varv += 1
            tillstand.uppdatera(varv=varv, status="tittar", fel=None)

            if a.torr:
                svar = torra[(varv - 1) % len(torra)]
            else:
                try:
                    if not ta_bild(bygg, bild):
                        tillstand.uppdatera(status="vantar", fel="kameran gav ingen bild")
                        time.sleep(a.intervall)
                        continue
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                    tillstand.uppdatera(status="vantar", fel=f"kamerafel: {e}")
                    time.sleep(a.intervall)
                    continue
                tillstand.uppdatera(status="tanker")
                svar = fraga_claude(bild)

            if svar.get("fel"):
                tillstand.uppdatera(status="vantar", fel=svar["fel"])
                time.sleep(a.intervall)
                continue

            reaktion = svar.get("reaktion", "vad")
            ord_ = (svar.get("ord") or reaktion).strip()
            tillstand.uppdatera(status="sager", reaktion=reaktion, ord=ord_,
                                varfor=svar.get("varfor"))
            print(f"[{varv}] {reaktion:8} {ord_!r}  — {svar.get('varfor', '')}", flush=True)

            if a.tyst:
                monster, saknade = tickspeak.koda(ord_, behall_vokaler=False)
                monster = "  ".join(", ".join(o) for o in monster)
            else:
                monster, saknade = sag(ord_)
            tillstand.uppdatera(monster=monster, status="tittar",
                                fel=f"saknas i alfabetet: {' '.join(saknade)}" if saknade else None)
            time.sleep(a.intervall)
    except KeyboardInterrupt:
        print("\nhejda")
        return 0
    finally:
        if os.path.exists(bild):
            os.unlink(bild)


if __name__ == "__main__":
    sys.exit(main())
