"""
titel: tick-speak genom base59 -- en av misstag vacker koppling
datum: 2026-09-11
hor ihop med: base57/base57.py (kodningen), roboten i
              ~/.claude/worktrees/tickspeak/robot/w4k7px.py (alfabetet, agda av roboten)

Roboten pratar bara i tick (-) och tock (_) -- rent binart, en bit per klick.
En base59-strang ar ocksa bara ett stort heltal i en annan kladsel. Sa vad
hander om robotens rost packas som bytes och kors genom base57s encode()?

Den blir en URL. Inget mer djupt an sa -- men de tva formaten delar samma
grund (heltal, radix, bitar) utan att ha planerat det.

Kor: python3 bridges/2bfjc5.py [ord]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "base57"))
from base57 import encode, decode  # noqa: E402

# Kopia av robotens tabell -- den riktiga agas av roboten och bor i
# ~/.claude/worktrees/tickspeak/robot/w4k7px.py, inte har.
ALFABET = {
    "a": "-_", "e": "__", "h": "--", "j": "-_-", "b": "--_-",
    "n": "---", "t": "___", "r": "--_", "s": "__-", "l": "-__", "d": "_--", "m": "_-_",
    "k": "----", "g": "____", "v": "-_-_", "f": "_-_-", "p": "--__", "c": "__--",
    "w": "-__-", "x": "_--_", "z": "_---", "q": "---_",
}


def text_till_klick(text: str) -> str:
    """Konsonanterna i text, konkatenerade -- inga skiljetecken mellan bokstaverna."""
    return "".join(ALFABET[c] for c in text.lower() if c in ALFABET)


def klick_till_bytes(klick: str) -> bytes:
    """- = 1, _ = 0. Paddar med 0 till narmaste byte."""
    if not klick:
        return b""
    bitar = klick.replace("-", "1").replace("_", "0")
    bitar += "0" * ((-len(bitar)) % 8)
    return int(bitar, 2).to_bytes(len(bitar) // 8, "big")


def bytes_till_klick(data: bytes, langd: int) -> str:
    """Motsatsen -- klipper till langd bitar (paddningen syns inte har)."""
    bitar = "".join(f"{b:08b}" for b in data)[:langd]
    return bitar.replace("1", "-").replace("0", "_")


def main():
    ord_ = sys.argv[1] if len(sys.argv) > 1 else "hej"

    klick = text_till_klick(ord_)
    if not klick:
        sys.exit(f"inget att koda -- ingen av bokstaverna i {ord_!r} finns i alfabetet")

    data = klick_till_bytes(klick)
    url = encode(data)

    tillbaka_data = decode(url)
    tillbaka_klick = bytes_till_klick(tillbaka_data, len(klick))

    print(f"ord        : {ord_}")
    print(f"tick-speak : {klick}")
    print(f"bytes      : {data!r}")
    print(f"base59     : {url}")
    print(f"tillbaka   : {tillbaka_klick}")

    assert tillbaka_klick == klick, "bron lacker -- klicken kom inte tillbaka ratt"
    print()
    print("bron haller: klicken korsade bas-59-gransen och kom tillbaka oforandrade.")


if __name__ == "__main__":
    main()
