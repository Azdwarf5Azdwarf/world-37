#!/usr/bin/env python3
"""
tick-speak — robotens ljudvokabular
Titel: Konsonantsprak for rollspelsroboten
Datum: 2026-09-03

Roboten talar i tick (-) och tock (_). Inga vokaler i gatulaget:
lyssnaren maste fylla i dem sjalv. Det ar hela poangen.

    hej  ->  --, __, -_-      (fullt lage, -f)
    hej  ->  --, -_-          (konsonantlage, default)  "h-j"

Tabellen nedan ar din. Fyll pa den. Koden ror den aldrig.
"""
import argparse, math, os, struct, subprocess, sys, tempfile, wave

# ---------------------------------------------------------------- tabellen
# Din karna. - = tick, _ = tock.
#
# Principen: vanligast = kortast, och de vanligaste paren ligger sa
# langt ifran varandra som mojligt (n ar fyra tick, t ar fyra tock).
# Da spelar det ingen roll om en klick dranks i trafikbrus.
#
#   langd 2  dina egna + fragepartikeln
#   langd 3  de sju vanligaste konsonanterna
#   langd 4  resten
ALFABET = {
    # dina, ororda
    "a": "-_",
    "e": "__",
    "h": "--",
    "j": "-_-",
    "b": "--_-",
    # langd 3 — vanliga
    "n": "---",
    "t": "___",
    "r": "--_",
    "s": "__-",
    "l": "-__",
    "d": "_--",
    "m": "_-_",
    # langd 4 — resten
    "k": "----",
    "g": "____",
    "v": "-_-_",
    "f": "_-_-",
    "p": "--__",
    "c": "__--",
    "w": "-__-",
    "x": "_--_",
    "z": "_---",
    "q": "---_",
}

# Robotens enda icke-bokstav: ett fragande "hm?".
# Den lediga langd-2-platsen — han behover kunna undra.
PARTIKLAR = {
    "?": "_-",
}

# De tre sista ar a-ring, a-prickar och o-prickar. De star som escape-koder
# sa filen ar fri fran sjalva tecknen — men roboten kanner igen dem anda,
# om claude skickar tillbaka ett ord som innehaller nagot av dem.
VOKALER = set("aeiouy\u00e5\u00e4\u00f6")

# ---------------------------------------------------------------- ljudet
SR = 22050
TICK_HZ = 1900      # tick  = ljus klick
TOCK_HZ = 780       # tock  = mork klick
SYMBOL_MS = 45      # langd pa en klick
GAP_SYM_MS = 55     # tystnad mellan tick/tock i samma bokstav
GAP_BOK_MS = 210    # tystnad mellan bokstaver
GAP_ORD_MS = 520    # tystnad mellan ord


def _ton(hz, ms):
    n = int(SR * ms / 1000)
    ut = []
    for i in range(n):
        # snabb attack, mjuk release — ska lata som en klick, inte ett pip
        env = min(1.0, i / (SR * 0.004)) * (1.0 - i / n) ** 2.2
        ut.append(int(0.55 * env * 32767 * math.sin(2 * math.pi * hz * i / SR)))
    return ut


def _tyst(ms):
    return [0] * int(SR * ms / 1000)


def rendera(monster_per_ord):
    """monster_per_ord: lista av listor av monsterstrangar."""
    prov = []
    for oi, ord_ in enumerate(monster_per_ord):
        if oi:
            prov += _tyst(GAP_ORD_MS)
        for bi, monster in enumerate(ord_):
            if bi:
                prov += _tyst(GAP_BOK_MS)
            for si, sym in enumerate(monster):
                if si:
                    prov += _tyst(GAP_SYM_MS)
                prov += _ton(TICK_HZ if sym == "-" else TOCK_HZ, SYMBOL_MS)
    return prov


def skriv_wav(prov, sokvag):
    with wave.open(sokvag, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", max(-32768, min(32767, s))) for s in prov))


def spela(sokvag):
    for kmd in (["afplay", sokvag], ["aplay", "-q", sokvag], ["paplay", sokvag]):
        try:
            subprocess.run(kmd, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


# ---------------------------------------------------------------- kodning
def koda(text, behall_vokaler=False):
    """-> (monster_per_ord, saknade_bokstaver)"""
    ord_ut, saknade = [], []
    for ord_ in text.lower().split():
        bokstaver = []
        for tecken in ord_:
            if tecken in PARTIKLAR:
                bokstaver.append(PARTIKLAR[tecken])
                continue
            if not tecken.isalpha():
                continue
            if not behall_vokaler and tecken in VOKALER:
                continue
            monster = ALFABET.get(tecken)
            if monster:
                bokstaver.append(monster)
            else:
                saknade.append(tecken)
        if bokstaver:
            ord_ut.append(bokstaver)
    return ord_ut, sorted(set(saknade))


def main():
    p = argparse.ArgumentParser(description="Roboten talar i tick och tock.")
    p.add_argument("text", nargs="*", help="det roboten ska saga")
    p.add_argument("-f", "--fullt", action="store_true",
                   help="behall vokalerna (annars fyller lyssnaren i dem)")
    p.add_argument("-o", "--ut", help="spara wav hit istallet for att spela")
    p.add_argument("-l", "--lista", action="store_true",
                   help="visa tabellen och vilka bokstaver som saknas")
    a = p.parse_args()

    if a.lista:
        for bok in "abcdefghijklmnopqrstuvwxyz\u00e5\u00e4\u00f6":
            marke = "vokal" if bok in VOKALER else "     "
            print(f"  {bok}  {marke}  {ALFABET.get(bok, '— saknas')}")
        for tecken, monster in PARTIKLAR.items():
            print(f"  {tecken}  parti  {monster}")
        return 0

    if not a.text:
        p.error("sag nagot: w4k7px.py hej")

    text = " ".join(a.text)
    monster, saknade = koda(text, behall_vokaler=a.fullt)

    if not monster:
        print(f"inget att saga — ingen av bokstaverna i {text!r} finns i tabellen",
              file=sys.stderr)
        return 1

    print("  ".join(", ".join(o) for o in monster))
    if saknade:
        print(f"(saknas i tabellen: {' '.join(saknade)})", file=sys.stderr)

    prov = rendera(monster)
    if a.ut:
        skriv_wav(prov, a.ut)
        print(f"-> {a.ut}", file=sys.stderr)
    else:
        fd, tmp = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            skriv_wav(prov, tmp)
            if not spela(tmp):
                print("hittade ingen spelare (afplay/aplay/paplay) — anvand -o",
                      file=sys.stderr)
                return 1
        finally:
            os.unlink(tmp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
