# Robotens alfabet — tick och tock
2026-09-03 · `-` = tick (ljus) · `_` = tock (mork)

Vanligast = kortast. n och t ar varandras motsatser, likasa r/s och l/d —
tappar du en klick i trafikbrus blir det anda inte fel bokstav.

## Dina egna (ororda)

| | |
|---|---|
| a | `-_` |
| e | `__` |
| h | `--` |
| j | `-_-` |
| b | `--_-` |

## Vanliga — tre klick

| | | | |
|---|---|---|---|
| n | `---` | t | `___` |
| r | `--_` | s | `__-` |
| l | `-__` | d | `_--` |
| m | `_-_` | | |

## Resten — fyra klick

| | | | |
|---|---|---|---|
| k | `----` | g | `____` |
| v | `-_-_` | f | `_-_-` |
| p | `--__` | c | `__--` |
| w | `-__-` | x | `_--_` |
| z | `_---` | q | `---_` |

## Fragepartikeln

| | |
|---|---|
| ? | `_-` |

Den lediga langd-2-platsen. Roboten maste kunna undra.

## Sa later scenerna

```
hej            --, -_-
kom tillbaka   ----, _-_   ___, -__, -__, --_-, ----
forlat         _-_-, --_, -__, ___
vem ar du?     -_-_, _-_   --_   _--, _-
```

## Kvar at dig

Sju vokaler saknas fortfarande i tabellen — men de sags aldrig pa gatan,
sa det bradskar inte. Kor `w4k7px.py -l` for att se exakt vilka.
Lagg till dem bara om du vill ha fullt lage hemma.

## Kor

```
python3 robot/w4k7px.py "kom tillbaka"      # konsonantlage
python3 robot/w4k7px.py -f hej              # med vokaler
python3 robot/w4k7px.py -l                  # hela tabellen
```
