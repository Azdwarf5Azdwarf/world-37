"""
titel: Temperaturmatning kodad med base57
datum: 2026-09-04
hor ihop med: q3v8mz.md (plan), research/mercury-thermometers-sweden.md

Poangen: kvicksilverpelaren ar ett fysiskt tal. Grader ar en konvention
ovanpa det. base57-strangen ar annu en konvention ovanpa den. Ingen av
konventionerna tillfor information — de gor bara talet transporterbart.

Kor: python3 m4t7bq.py
"""

import sys
from pathlib import Path

BASE57_REPO = Path.home() / "dev" / "base57"
sys.path.insert(0, str(BASE57_REPO))

try:
    from base57 import encode, decode, BASE59
except ModuleNotFoundError:  # pragma: no cover
    sys.exit(f"hittar inte base57.py i {BASE57_REPO}")


# --- lager 1: fysiken -------------------------------------------------------
# Kvicksilver expanderar. Det enda "riktiga" ar pelarens hojd.
COLUMN_MM = 118.4

# --- lager 2: kalibreringen -------------------------------------------------
# Manniskan etsade tva fixpunkter i glaset och drog en rat linje mellan dem.
ICE_POINT_MM = 40.0     # 0 grader C
STEAM_POINT_MM = 240.0  # 100 grader C


def mm_to_celsius(mm: float) -> float:
    span = STEAM_POINT_MM - ICE_POINT_MM
    return (mm - ICE_POINT_MM) / span * 100.0


# --- lager 3: kodningen -----------------------------------------------------
# Centigrader som heltal -> bytes -> base57. Ren notation, inget nytt vetande.
def encode_reading(celsius: float) -> str:
    centidegrees = round(celsius * 100)
    signed = centidegrees.to_bytes(3, "big", signed=True)
    return encode(signed)


def decode_reading(token: str) -> float:
    raw = decode(token)
    raw = raw.rjust(3, b"\x00")
    return int.from_bytes(raw, "big", signed=True) / 100.0


def main() -> None:
    celsius = mm_to_celsius(COLUMN_MM)
    token = encode_reading(celsius)
    back = decode_reading(token)

    print(f"radix (bas)          : {BASE59}")
    print(f"lager 1  pelare      : {COLUMN_MM} mm      <- fysik")
    print(f"lager 2  skala       : {celsius:.2f} grader C  <- manniskans fixpunkter")
    print(f"lager 3  base57      : {token!r}        <- konvention for transport")
    print(f"tillbaka             : {back:.2f} grader C")
    print()
    print(f"URL-form: https://exempel.se/matning/{token}")

    # rundgang for ett par avlasningar, inkl. minusgrader och nollpunkten
    for mm in (ICE_POINT_MM, 10.0, COLUMN_MM, STEAM_POINT_MM):
        c = mm_to_celsius(mm)
        t = encode_reading(c)
        assert abs(decode_reading(t) - c) < 0.01, (mm, c, t)
        print(f"  {mm:6.1f} mm -> {c:7.2f} C -> {t}")


if __name__ == "__main__":
    main()
