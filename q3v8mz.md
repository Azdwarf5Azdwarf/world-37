---
title: world-37 x base57 — plan for koppling
date: 2026-09-04
tags: [plan, base57, kodning, kalibrering]
---

# Hur base57 passar in i world-37

## Kort svar
Ja, det haller. Bada repona handlar om samma sak: **fysiken gor jobbet,
manniskan hittar pa avlasningen.**

## Den gemensamma karnan

| | termometer | base57 |
|---|---|---|
| det som "bara ar" | kvicksilver expanderar (termisk utvidgning) | byte-strangen ar ett heltal |
| det manniskan hittade pa | skalan: is = 0, kokpunkt = 100 | alfabetet: vilka 59 tecken som blir siffror |
| resultatet | grader | en URL-saker strang |

Kvicksilvret vet inte vad temperatur ar. Heltalet vet inte vad "NQJxuMD49iYwDi2"
betyder. I bada fallen ar **radix (bas)** respektive fixpunkter det verkliga,
och notationen ren konvention.

## Externaliserad intelligens
Termometer-noten sager: intelligensen ligger utanfor kroppen, i designen.
En **encoder (kodare)** ar samma sak i mjukvara — den bar en overenskommelse
du slipper halla i huvudet. base57 ar det i sin renaste, dummaste form:
inget skydd, ingen validering, bara ett avtal om tecken.

## Vad base57-repot redan bidrar med
- `docs/e1mnb9.md`: base64 ar kodning, inte sakerhet. Samma poang som
  "kalibrering gor rorelsen lasbar" — den gor den inte sann.
- `docs/osi-under-url.md`: lagermodell. Skalan pa termometern ar ocksa ett lager
  ovanpa fysiken.
- Sjalva skamtet (57 = 3x19, sa den riktiga basen blev 59): namnet ar konvention,
  matematiken ar det som galler. Exakt samma spanning som i note-serien.

## Plan — sma steg
1. Lagg in det har som `research/`-granne eller egen mapp `bridges/`. (Beslut kvar.)
2. Skriv en kort note: "fixpunkt vs alfabete" — de tva satten att forankra en skala.
3. Las in `docs/e1mnb9.md`-resonemanget i termometer-noten som referens, inte kopia.
4. Eventuellt: en liten demo som kodar en temperaturmatning med base57 — skamt
   och illustration i ett. Bara om det kanns kul, inte som krav.

## Vad som INTE ska goras
- Inte sla ihop repona.
- Inte skriva om `research/mercury-thermometers-sweden.md` — den ar ratext.
