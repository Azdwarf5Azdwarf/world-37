#!/usr/bin/env python3
"""Stjarnzero — vilken stjarna som stod hogst over dig nar du vaknade.

Inget teleskop. Himlen ar berakningsbar: stjarnornas positioner ligger i
katalog, och vilken som stod hogst kraver bara lat, lon och tid.

Katalogen ar de ~45 ljusstarkaste stjarnorna, J2000, rektascension och
deklination i grader. Egenrorelse ignoreras — den flyttar dem brakdelar av
en bagminut per ar, vilket inte betyder nagot for det har.
"""

import math

SEKUNDER_PER_DYGN = 86400

# namn, rektascension (grader), deklination (grader), skenbar magnitud
KATALOG = [
    ("Sirius",          101.287, -16.716, -1.46),
    ("Canopus",          95.988, -52.696, -0.74),
    ("Rigil Kentaurus", 219.902, -60.834, -0.27),
    ("Arcturus",        213.915,  19.182, -0.05),
    ("Vega",            279.234,  38.784,  0.03),
    ("Capella",          79.172,  45.998,  0.08),
    ("Rigel",            78.634,  -8.202,  0.13),
    ("Procyon",         114.825,   5.225,  0.34),
    ("Achernar",         24.429, -57.237,  0.46),
    ("Betelgeuse",       88.793,   7.407,  0.50),
    ("Hadar",           210.956, -60.373,  0.61),
    ("Altair",          297.696,   8.868,  0.77),
    ("Acrux",           186.650, -63.099,  0.77),
    ("Aldebaran",        68.980,  16.509,  0.85),
    ("Spica",           201.298, -11.161,  1.04),
    ("Antares",         247.352, -26.432,  1.09),
    ("Pollux",          116.329,  28.026,  1.14),
    ("Fomalhaut",       344.413, -29.622,  1.16),
    ("Deneb",           310.358,  45.280,  1.25),
    ("Mimosa",          191.930, -59.689,  1.25),
    ("Regulus",         152.093,  11.967,  1.35),
    ("Adhara",          104.656, -28.972,  1.50),
    ("Castor",          113.650,  31.888,  1.58),
    ("Shaula",          263.402, -37.104,  1.62),
    ("Gacrux",          187.791, -57.113,  1.63),
    ("Bellatrix",        81.283,   6.350,  1.64),
    ("Elnath",           81.573,  28.608,  1.65),
    ("Miaplacidus",     138.300, -69.717,  1.67),
    ("Alnilam",          84.053,  -1.202,  1.69),
    ("Alnair",          332.058, -46.961,  1.74),
    ("Alnitak",          85.190,  -1.943,  1.77),
    ("Alioth",          193.507,  55.960,  1.77),
    ("Dubhe",           165.932,  61.751,  1.79),
    ("Mirfak",           51.081,  49.861,  1.79),
    ("Wezen",           107.098, -26.393,  1.83),
    ("Kaus Australis",  276.043, -34.385,  1.85),
    ("Alkaid",          206.885,  49.313,  1.86),
    ("Sargas",          264.330, -42.998,  1.86),
    ("Avior",           125.628, -59.510,  1.86),
    ("Menkalinan",       89.882,  44.947,  1.90),
    ("Atria",           252.166, -69.028,  1.91),
    ("Alhena",           99.428,  16.399,  1.93),
    ("Peacock",         306.412, -56.735,  1.94),
    ("Polaris",          37.955,  89.264,  1.98),
    ("Mirzam",           95.675, -17.956,  1.98),
]


def gmst_grader(unix_ts):
    """Greenwich medelstjarntid i grader for en unix-tidsstampel."""
    jd = unix_ts / SEKUNDER_PER_DYGN + 2440587.5
    d = jd - 2451545.0
    t = d / 36525.0
    g = (280.46061837 + 360.98564736629 * d
         + 0.000387933 * t * t - t * t * t / 38710000.0)
    return g % 360.0


def alt_az(ra, dek, lat, lon, unix_ts):
    """Hojd och azimut i grader for en stjarna sedd fran (lat, lon).

    lon ar positiv ostvart. Hojd < 0 betyder under horisonten.
    """
    lst = (gmst_grader(unix_ts) + lon) % 360.0
    ha = math.radians((lst - ra) % 360.0)
    dr, lr = math.radians(dek), math.radians(lat)

    sin_alt = math.sin(dr) * math.sin(lr) + math.cos(dr) * math.cos(lr) * math.cos(ha)
    alt = math.asin(max(-1.0, min(1.0, sin_alt)))

    az = math.atan2(-math.sin(ha) * math.cos(dr),
                    math.sin(dr) * math.cos(lr) - math.cos(dr) * math.sin(lr) * math.cos(ha))
    return math.degrees(alt), math.degrees(az) % 360.0


def stjarnzero(lat, lon, zero_ts):
    """Stjarnan som stod hogst over dig i ogonblicket du vaknade.

    Returnerar (namn, hojd, azimut, magnitud), eller None om ingen katalogstjarna
    var over horisonten — vilket i praktiken aldrig hander utanfor rakneglapp.

    Att solen samtidigt gick upp och slog ut synligheten spelar ingen roll.
    Stjarnan stod dar. Det ar inte en fraga om vad du sag.
    """
    basta = None
    for namn, ra, dek, mag in KATALOG:
        alt, az = alt_az(ra, dek, lat, lon, zero_ts)
        if alt <= 0:
            continue
        if basta is None or alt > basta[1]:
            basta = (namn, alt, az, mag)
    return basta


def stjarnbindning(lat, lon, zero_ts):
    """En kort, stabil strang for stjarnzero — avsedd att ga in i OTP-nyckeln.

    Hojden avrundas till hel grad sa att sma skillnader i koordinat eller
    klockdrift inte andrar bindningen. Se sakerhetsnoten i OTP.md: det har ar
    kontext, inte hemlighet — vem som helst med din position och tid kan
    rakna fram samma strang.
    """
    s = stjarnzero(lat, lon, zero_ts)
    if s is None:
        return b""
    namn, alt, _az, _mag = s
    return f"{namn}@{round(alt)}".encode()
