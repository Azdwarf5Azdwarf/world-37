#!/usr/bin/env python3
"""Klockan med tva koordinater: unix-tid och din egen soluppgang.

Inga beroenden. Solberakningen ar NOAA:s algoritm, noggrann till nagon minut,
vilket racker gott for det har.

    ./sjalvklocka.py nu       33.31 44.36        # Bagdad
    ./sjalvklocka.py delta    33.31 44.36  39.90 116.40
    ./sjalvklocka.py ankare   33.31 44.36
    ./sjalvklocka.py stjarna  33.31 44.36
    ./sjalvklocka.py otp      33.31 44.36  39.90 116.40  --hemlighet fil
"""

import argparse
import hashlib
import hmac
import math
import struct
import sys
import time

import stjarnor

SEKUNDER_PER_DYGN = 86400


# --- solen ------------------------------------------------------------------

def soluppgang_unix(lat, lon, dagens_unix, nedgang=False):
    """Unix-tidsstampeln for soluppgangen pa den dag `dagens_unix` ligger i.

    `nedgang=True` ger solnedgangen samma dygn i stallet.

    Returnerar None dar solen inte gar upp alls (polarnatt) eller aldrig gar
    ner (midnattssol) — se den oppna fragan om polcirkeln i OTP.md.
    """
    # julianskt dagnummer for dygnets mitt i UTC
    dag = math.floor(dagens_unix / SEKUNDER_PER_DYGN)
    jdag = dag + 2440587.5 + 0.5

    n = jdag - 2451545.0 + 0.0008
    # soluppgang ligger fore middag, sa vi soker mot den lokala middagen
    j_stjarna = n - lon / 360.0
    M = (357.5291 + 0.98560028 * j_stjarna) % 360.0
    Mr = math.radians(M)
    C = 1.9148 * math.sin(Mr) + 0.02 * math.sin(2 * Mr) + 0.0003 * math.sin(3 * Mr)
    L = (M + C + 180.0 + 102.9372) % 360.0
    Lr = math.radians(L)

    j_transit = 2451545.0 + j_stjarna + 0.0053 * math.sin(Mr) - 0.0069 * math.sin(2 * Lr)

    # solens deklination
    sin_dekl = math.sin(Lr) * math.sin(math.radians(23.4397))
    dekl = math.asin(sin_dekl)

    latr = math.radians(lat)
    # -0.833 grader: solskivans radie plus refraktion vid horisonten
    taljare = math.sin(math.radians(-0.833)) - math.sin(latr) * math.sin(dekl)
    namnare = math.cos(latr) * math.cos(dekl)
    cos_w = taljare / namnare
    if cos_w > 1 or cos_w < -1:
        return None  # ingen soluppgang detta dygn pa den har breddgraden

    w = math.degrees(math.acos(cos_w))
    j = j_transit + (w if nedgang else -w) / 360.0
    return int(round((j - 2440587.5) * SEKUNDER_PER_DYGN))


def solnedgang_efter(lat, lon, efter_ts):
    """Forsta solnedgangen vid eller efter `efter_ts`."""
    for dagar in range(0, 400):
        k = soluppgang_unix(lat, lon, efter_ts + dagar * SEKUNDER_PER_DYGN, nedgang=True)
        if k is not None and k >= efter_ts:
            return k
    return None


def zero(lat, lon, nu=None):
    """Din subjektiva nollpunkt: senaste soluppgangen dar du vaknade.

    Har solen inte gatt upp an idag galler gardagens — dagen borjar nar solen
    gick upp, inte vid midnatt.
    """
    nu = int(nu if nu is not None else time.time())
    for dagar_bak in range(0, 400):
        kandidat = soluppgang_unix(lat, lon, nu - dagar_bak * SEKUNDER_PER_DYGN)
        if kandidat is not None and kandidat <= nu:
            return kandidat
    return None  # polarnatt sedan over ett ar; det ar inte ett fel, det ar norr


def subjektiv_tid(lat, lon, nu=None):
    nu = int(nu if nu is not None else time.time())
    z = zero(lat, lon, nu)
    return None if z is None else nu - z


# --- de tjugo ankarna -------------------------------------------------------

ANKARE_PER_BAGE = 10          # 10 pa dagen, 10 pa natten
ANKARE_PER_DYGN = 2 * ANKARE_PER_BAGE


def ankare(lat, lon, nu=None):
    """Vilket av dygnets tjugo ankare du befinner dig i.

    Dagsbagen (soluppgang -> solnedgang) delas i tio, natbagen
    (solnedgang -> nasta soluppgang) i tio. Ankare 0-9 ar dag, 10-19 ar natt.

    Bagarna ar olika langa och det ar meningen: ett ankare i december ar
    kortare pa dagen och langre pa natten. Ankaret ar en andel av bagen,
    inte ett matt i sekunder.

    Returnerar (index, andel_inom_ankaret) eller None utan soluppgang.
    """
    nu = int(nu if nu is not None else time.time())
    gryning = zero(lat, lon, nu)
    if gryning is None:
        return None
    skymning = solnedgang_efter(lat, lon, gryning)
    if skymning is None:
        return None

    if nu < skymning:                       # dag
        bage_start, bage_slut, forskjutning = gryning, skymning, 0
    else:                                   # natt
        nasta = zero(lat, lon, nu + SEKUNDER_PER_DYGN)
        if nasta is None or nasta <= skymning:
            nasta = skymning + SEKUNDER_PER_DYGN
        bage_start, bage_slut, forskjutning = skymning, nasta, ANKARE_PER_BAGE

    langd = bage_slut - bage_start
    if langd <= 0:
        return None
    t = (nu - bage_start) / langd * ANKARE_PER_BAGE
    i = min(int(t), ANKARE_PER_BAGE - 1)
    return forskjutning + i, t - i


# --- invarianten ------------------------------------------------------------

def delta(lat_a, lon_a, lat_b, lon_b, nu=None):
    """zero_A - zero_B. Samma tal oavsett vem av dem som reste."""
    za = zero(lat_a, lon_a, nu)
    zb = zero(lat_b, lon_b, nu)
    if za is None or zb is None:
        return None
    return za - zb


# --- otp --------------------------------------------------------------------

def otp(hemlighet: bytes, delta_s: int, nu=None, steg=30, siffror=6,
        bindning: bytes = b""):
    """HMAC(hemlighet || delta, floor(unix / steg)).

    Beloppet anvands, inte det tecknade vardet: invarianten ar *skillnaden*,
    och den ar densamma vem av de tva som an raknar. Utan abs() far A och B
    olika nycklar och koderna stammer aldrig.

    OBS: delta ar INTE en stark hemlighet — som mest ~17 bitar, och
    soluppgangstider ar offentliga. Den binder koden till plats och vakenhet.
    Den ersatter inte `hemlighet`. Se OTP.md.

    `bindning` ar stjarnzero-strangen fran stjarnor.stjarnbindning(), om den
    anvands. Samma forbehall: kontext, inte hemlighet.
    """
    nu = int(nu if nu is not None else time.time())
    nyckel = hemlighet + struct.pack(">Q", abs(delta_s)) + bindning
    rakn = struct.pack(">Q", nu // steg)
    mac = hmac.new(nyckel, rakn, hashlib.sha256).digest()
    # dynamisk trunkering, samma som RFC 4226
    off = mac[-1] & 0x0F
    kod = struct.unpack(">I", mac[off:off + 4])[0] & 0x7FFFFFFF
    return str(kod % (10 ** siffror)).zfill(siffror)


# --- cli --------------------------------------------------------------------

def _hhmmss(s):
    tecken = "-" if s < 0 else ""
    s = abs(s)
    return f"{tecken}{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main(argv=None):
    p = argparse.ArgumentParser(description="klockan med tva koordinater")
    sub = p.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("nu", help="din objektiva och subjektiva tid")
    n.add_argument("lat", type=float)
    n.add_argument("lon", type=float)

    d = sub.add_parser("delta", help="invarianten mellan tva observatorer")
    for namn in ("lat_a", "lon_a", "lat_b", "lon_b"):
        d.add_argument(namn, type=float)

    ak = sub.add_parser("ankare", help="vilket av dygnets tjugo ankare du ar i")
    ak.add_argument("lat", type=float)
    ak.add_argument("lon", type=float)

    st = sub.add_parser("stjarna", help="stjarnan som stod hogst nar du vaknade")
    st.add_argument("lat", type=float)
    st.add_argument("lon", type=float)

    o = sub.add_parser("otp", help="engangskod bunden till invarianten")
    for namn in ("lat_a", "lon_a", "lat_b", "lon_b"):
        o.add_argument(namn, type=float)
    o.add_argument("--hemlighet", required=True,
                   help="fil med den riktiga hemligheten (delta racker inte)")
    o.add_argument("--steg", type=int, default=30)
    o.add_argument("--stjarna", action="store_true",
                   help="bind koden till stjarnzero ocksa")

    a = p.parse_args(argv)

    if a.cmd == "nu":
        z = zero(a.lat, a.lon)
        if z is None:
            print("ingen soluppgang pa over ett ar — se OTP.md, polcirkeln")
            return 1
        nu = int(time.time())
        print(f"objektiv (unix):  {nu}")
        print(f"nollpunkt:        {z}  ({time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime(z))})")
        print(f"subjektiv:        {_hhmmss(nu - z)} sedan solen gick upp")
        return 0

    if a.cmd == "ankare":
        r = ankare(a.lat, a.lon)
        if r is None:
            print("ingen soluppgang eller nedgang — se STJARNZERO.md, polcirkeln")
            return 1
        i, andel = r
        bage = "dag" if i < ANKARE_PER_BAGE else "natt"
        print(f"ankare:  {i} av {ANKARE_PER_DYGN}  ({bage})")
        print(f"         {andel * 100:.1f}% in i ankaret")
        print(f"bas 60:  {i * 3} av 60")
        print(f"bas 100: {i * 5} av 100")
        return 0

    if a.cmd == "stjarna":
        z = zero(a.lat, a.lon)
        if z is None:
            print("ingen soluppgang pa over ett ar — se OTP.md, polcirkeln")
            return 1
        s = stjarnor.stjarnzero(a.lat, a.lon, z)
        if s is None:
            print("ingen katalogstjarna over horisonten")
            return 1
        namn, alt, az, mag = s
        print(f"nollpunkt:   {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime(z))}")
        print(f"stjarnzero:  {namn}")
        print(f"             {alt:.1f} grader over horisonten, azimut {az:.1f}")
        print(f"             magnitud {mag}")
        print(f"bindning:    {stjarnor.stjarnbindning(a.lat, a.lon, z).decode()}")
        return 0

    if a.cmd == "delta":
        v = delta(a.lat_a, a.lon_a, a.lat_b, a.lon_b)
        if v is None:
            print("en av observatorerna har ingen soluppgang")
            return 1
        print(f"delta: {v} s  ({_hhmmss(v)})")
        print("samma tal aat bada hallen — det ar poangen")
        return 0

    if a.cmd == "otp":
        v = delta(a.lat_a, a.lon_a, a.lat_b, a.lon_b)
        if v is None:
            print("en av observatorerna har ingen soluppgang")
            return 1
        with open(a.hemlighet, "rb") as f:
            hemlighet = f.read().strip()
        if len(hemlighet) < 16:
            print("hemligheten ar for kort — minst 16 byte", file=sys.stderr)
            return 2
        bindning = b""
        if a.stjarna:
            # bada parternas stjarnzero, sorterade — annars far A och B
            # olika nycklar beroende pa vem som star forst i anropet
            ba = stjarnor.stjarnbindning(a.lat_a, a.lon_a, zero(a.lat_a, a.lon_a))
            bb = stjarnor.stjarnbindning(a.lat_b, a.lon_b, zero(a.lat_b, a.lon_b))
            bindning = b"|".join(sorted((ba, bb)))
        print(otp(hemlighet, v, steg=a.steg, bindning=bindning))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
