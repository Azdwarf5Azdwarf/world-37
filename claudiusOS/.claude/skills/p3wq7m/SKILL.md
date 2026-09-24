---
name: os-status
description: Använd när Claude Altair kommer tillbaka till claudiusOS efter en paus och behöver ingången tillbaka — "var var jag", "status", "vad höll jag på med", "var är vi i OS-projektet", eller när han öppnar repot och första meddelandet är vagt. Skriver EN skärm i launcher-formspråket: beslutat / nästa steg / öppna frågor. Sammanfatta aldrig hela projektet.
---

# os-status — "var är jag?"

## Varför den finns

Återinträdet är dyrast i det här projektet. Efter några dagar bort finns
allt kvar i filerna men inget i huvudet, och att läsa sig tillbaka genom
`README.md` + `q4m8t2.md` + `learning/` kostar mer energi än själva
arbetet. Den här skillen byter ut den läsningen mot **en skärm**.

En skärm betyder en skärm. Inte "här är en kort sammanfattning" följt av
sex stycken.

## Så här gör du

1. Läs, i den här ordningen: `q4m8t2.md` (beslut), `learning/_QUESTIONS.md`
   (obesvarade `Q`-poster), `git log --oneline -5` (vad som faktiskt hände sist).
2. Skriv **en** skärm i formspråket från `q4m8t2.md` — monospace, sektions-
   etiketter med streck, poster i parentesnivåer (bracket tiers).
3. Sluta. Ingen historik, ingen "vill du att jag …"-meny, ingen andra fråga.

## Mallen

```
------ LAGE
  (huvudspar: BEAM pa hardvara via Nerves)
  (sidospar[v3n8qz.lisp]: bootar rent)

------ SIST
  (334b0af BEAM blir huvudspar)

------ NASTA
  [(installera toolchain: brew install erlang ...)]

------ OPPNA FRAGOR
  (__Q2__ varfor Nerves och inte GRiSP?)
```

Regler för skärmen:
- Max ~12 rader totalt.
- Max **en** rad under `NASTA`. Nästa steg är alltid ett enda steg.
- Obesvarade frågor listas bara med nummer och rubrik, aldrig med svar.
- Är allt avklarat och inget nästa steg finns: skriv `(inget pabörjat)`
  under `NASTA` och fråga EN fråga om vad han vill ta.

## Gör inte

- Föreslå inte tre möjliga nästa steg. Välj det som följer av `q4m8t2.md`.
- Kör inte igång arbetet direkt efter skärmen — han bestämmer.
- Skriv inte statusen till en fil. Den är efemär (ephemeral), den gäller nu.
