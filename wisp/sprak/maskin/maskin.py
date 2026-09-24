#!/usr/bin/env python3
"""
maskin.py — vart eget brainfuck, skrivet i tick och tock.

Inspirerat av brainfuck, men inte en klon. Det enda vi lanar ar iden att
atta instruktioner racker. Resten kommer ur tick-speak.

Passformen som gjorde det vart att bygga:
brainfuck har exakt atta instruktioner. Tick-speak har exakt atta monster
av langd tre. En till en, inget over, inget under.

    ---  hoger      flytta bandet at hoger
    ___  vanster    flytta bandet at vanster
    --_  upp        oka rutan med ett
    __-  ner        minska rutan med ett
    -__  ut         skriv ut rutan som tecken
    _--  in         las ett tecken in i rutan
    -_-  borja      hoppa framat forbi slutet om rutan ar noll
    _-_  slut       hoppa tillbaka till borja om rutan inte ar noll

Samma monster ar ocksa bokstaverna n t r s l d j m i robotens alfabet.
Det ar ingen krock — laget avgor. I maskinlage ar `---` hoger, i talat
lage ar det n. Ett sprak, tva lasningar.

    python3 maskin.py program.tick
    python3 maskin.py program.tick --spela    # hor programmet i robotens rost
    python3 maskin.py --fran-text "+++.'"     # brainfuck in, tick ut
    echo '--_ --_ -__' | python3 maskin.py -

Ingen kompilator. En uppslagning och en dispatch. Se issue #8.
"""
import argparse, pathlib, sys

# ---------------------------------------------------------------- tabellen
ORDER = {
    "---": "hoger",
    "___": "vanster",
    "--_": "upp",
    "__-": "ner",
    "-__": "ut",
    "_--": "in",
    "-_-": "borja",
    "_-_": "slut",
}

# brainfuck -> vart monster, for den som vill ta med sig ett gammalt program
FRAN_BF = {
    ">": "---", "<": "___", "+": "--_", "-": "__-",
    ".": "-__", ",": "_--", "[": "-_-", "]": "_-_",
}

BANDET = 30000


def las(kalla):
    """Plockar ut monstren ur en text. Allt som inte ar - eller _ ar luft."""
    monster, biten = [], ""
    for tecken in kalla:
        if tecken in "-_":
            biten += tecken
            if len(biten) == 3:
                if biten not in ORDER:
                    raise ValueError(f"okant monster: {biten}")
                monster.append(biten)
                biten = ""
        elif biten:
            raise ValueError(f"halv order: {biten!r}")
    if biten:
        raise ValueError(f"halv order sist: {biten!r}")
    return monster


def para_hopp(monster):
    """Parar ihop borja och slut i forvag, sa loopen slipper leta."""
    stack, par = [], {}
    for i, m in enumerate(monster):
        if ORDER[m] == "borja":
            stack.append(i)
        elif ORDER[m] == "slut":
            if not stack:
                raise ValueError(f"slut utan borja vid order {i}")
            j = stack.pop()
            par[i], par[j] = j, i
    if stack:
        raise ValueError(f"borja utan slut vid order {stack[-1]}")
    return par


def kor(monster, indata="", tak=1_000_000):
    par = para_hopp(monster)
    band = bytearray(BANDET)
    huvud = pekare = steg = 0
    inpos, ut = 0, []

    while pekare < len(monster):
        if steg > tak:
            raise RuntimeError(f"stannade efter {tak} steg — loopen tar inte slut")
        order = ORDER[monster[pekare]]
        if order == "hoger":
            huvud = (huvud + 1) % BANDET
        elif order == "vanster":
            huvud = (huvud - 1) % BANDET
        elif order == "upp":
            band[huvud] = (band[huvud] + 1) % 256
        elif order == "ner":
            band[huvud] = (band[huvud] - 1) % 256
        elif order == "ut":
            ut.append(chr(band[huvud]))
        elif order == "in":
            band[huvud] = ord(indata[inpos]) if inpos < len(indata) else 0
            inpos += 1
        elif order == "borja" and band[huvud] == 0:
            pekare = par[pekare]
        elif order == "slut" and band[huvud] != 0:
            pekare = par[pekare]
        pekare += 1
        steg += 1
    return "".join(ut)


def spela_monster(monster):
    """Later roboten lasa programmet hogt. Lanar rosten ur robot/w4k7px.py."""
    import importlib.util, os, tempfile
    rost = pathlib.Path(__file__).resolve().parents[3] / "robot" / "w4k7px.py"
    spec = importlib.util.spec_from_file_location("rost", rost)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    sekunder = len(monster) * (3 * modul.SYMBOL_MS + 2 * modul.GAP_SYM_MS
                               + modul.GAP_BOK_MS) / 1000
    print(f"{len(monster)} order, ungefar {sekunder:.0f} sekunder",
          file=sys.stderr)

    prov = modul.rendera([monster])          # ett ord, en order per bokstav
    fd, tmp = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        modul.skriv_wav(prov, tmp)
        if not modul.spela(tmp):
            print("hittade ingen spelare (afplay/aplay/paplay)", file=sys.stderr)
            return 1
    finally:
        os.unlink(tmp)
    return 0


def fran_bf(text):
    return " ".join(FRAN_BF[t] for t in text if t in FRAN_BF)


def main():
    p = argparse.ArgumentParser(description="Vart eget brainfuck i tick och tock.")
    p.add_argument("fil", nargs="?", help="programfil, eller - for stdin")
    p.add_argument("-i", "--in", dest="indata", default="", help="indata till 'in'")
    p.add_argument("--fran-text", help="oversatt ett brainfuck-program till monster")
    p.add_argument("-l", "--lista", action="store_true", help="visa tabellen")
    p.add_argument("--spela", action="store_true",
                   help="las programmet hogt i robotens rost istallet for att kora det")
    a = p.parse_args()

    if a.lista:
        for m, namn in ORDER.items():
            bf = next(k for k, v in FRAN_BF.items() if v == m)
            print(f"  {m}  {namn:<8} {bf}")
        return 0

    if a.fran_text:
        print(fran_bf(a.fran_text))
        return 0

    if not a.fil:
        p.error("ge en fil, eller - for stdin")

    kalla = sys.stdin.read() if a.fil == "-" else open(a.fil).read()
    if a.spela:
        try:
            return spela_monster(las(kalla))
        except ValueError as fel:
            print(f"maskinen stannade: {fel}", file=sys.stderr)
            return 1
    try:
        sys.stdout.write(kor(las(kalla), a.indata))
    except (ValueError, RuntimeError) as fel:
        print(f"maskinen stannade: {fel}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
