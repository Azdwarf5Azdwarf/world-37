"""
titel: Minsta mojliga bron — Python-sidan
datum: 2026-09-04
hor ihop med: z5k9tr.md (plan, steg 2), j4x9pt.jl (Julia-sidan)

Steg 2 i planen: en Julia-fil med en funktion, en Python-fil som kallar
den. Inget mer. Ingen server, ingen HTTP, ingen subprocess — juliacall
startar Julia i samma process.

Kor: python3 bridges/r7w2kd.py
Krav: pip install juliacall   (drar ner Julia sjalv forsta gangen)
"""

import sys
from pathlib import Path

JULIA_FILE = Path(__file__).with_name("j4x9pt.jl")

try:
    from juliacall import Main as jl
except ModuleNotFoundError:
    sys.exit(
        "juliacall saknas. Installera med:\n"
        "    pip install juliacall\n"
        "Forsta importen laddar ner Julia (nagra hundra MB) automatiskt."
    )


def bro():
    """Laddar Julia-filen en gang och lamnar tillbaka funktionen kvadrat."""
    jl.include(str(JULIA_FILE))
    return jl.J4X9PT.kvadrat


def main() -> None:
    kvadrat = bro()

    print(f"julia-fil : {JULIA_FILE.name}")
    print(f"funktion  : kvadrat")
    print()

    for x in (2, 7, -3, 1.5):
        y = kvadrat(x)
        print(f"  {x!r:>6} -> {y!r:<8} ({type(x).__name__} -> {type(y).__name__})")

    # Bron ar bevisad nar talet kommer tillbaka oforandrat i mening.
    assert kvadrat(12) == 144
    assert abs(kvadrat(1.5) - 2.25) < 1e-12
    print()
    print("bron haller: talet korsade gransen och kom tillbaka.")


if __name__ == "__main__":
    main()
