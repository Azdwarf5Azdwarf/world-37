---
title: world-37 x kaimon/poimon — plan for python-julia-bro (LLM-to-Science)
date: 2026-09-04
tags: [plan, bridge, julia, python, kaimon, poimon, LLM-to-Science]
branch: julia-bridge
---

# Ja, det haller ihop

Samma karna som i `q3v8mz.md`: **fysiken gor jobbet, manniskan hittar pa
avlasningen.** En LLM (stor sprakmodell / large language model) ar en
avlasnings-maskin. Den ar bra pa lager 3 (notation) och opalitlig pa lager 1
(fysik). Bron finns for att halla dem isar.

## De tre lagren, oversatta

| lager | termometern | den har bron | kod |
|---|---|---|---|
| 1 fysik | kvicksilverpelaren | den faktiska berakningen | **Julia** |
| 2 kalibrering | is = 0, kok = 100 | enheter, fixpunkter, schema | **Python-bron** |
| 3 notation | grader, base57 | tokens, kort, JSON | **LLM / kaimon** |

Kvicksilvret vet inte vad temperatur ar. Julia vet inte vad prompten betydde.
LLM:en vet inte om siffran ar sann. Var och en gor sin sak.

## Vad kaimon/poimon bidrar med

kaimon (= poimon = `~/dev/kantimon`) har redan formen: **ett kort ar en
notation, varlden ar simuleringen.** `src/cards/types.ts` beskriver hp,
attack, speed — rena tal utan mening. `src/world/` ar det som faktiskt rors.

Det ar exakt samma delning. Skillnaden: i kaimon ar "fysiken" fejkad i
TypeScript. Bron byter ut den mot riktig fysik i Julia — och da blir kortet
ett vetenskapligt experiment istallet for en spelmekanik.

## Riktningen: LLM-to-Science

En LLM kan skriva Python hela dagen. Den kan inte rakna. Julia raknar snabbt
och med enheter. Bron ger LLM:en en **liten, tydlig yta** att prata mot:

```
LLM  ->  Python-funktion (typad, enhetsforsedd)  ->  Julia  ->  tal tillbaka
```

Poangen ar inte prestanda. Poangen ar att **notationen aldrig far rora
berakningen**. LLM:en far bestamma vad som ska raknas, aldrig vad svaret blir.

## Teknik — vad som faktiskt ska anvandas

- **`juliacall` / `PythonCall.jl`** — tvavagsbro. Python startar Julia i samma
  process. Ingen serialisering over natet, inga subprocesser.
  (`pip install juliacall`)
- **`Unitful.jl`** — enheter i typsystemet. mm, grader C, sekunder. Fel enhet
  = kompileringsfel, inte fel svar. Detta ar lager 2 gjort pa allvar.
- **`DifferentialEquations.jl`** — nar experimentet ar en modell over tid.
- **base57** (`~/dev/base57`) — lager 3 for transport, precis som i
  `m4t7bq.py`. Ett resultat blir en URL-saker strang.

## Plan — sma steg

1. **`bridges/`-mapp i world-37.** Beslutet som stod oppet i `q3v8mz.md`
   avgors har: ja, egen mapp. Bara for broar, inte for research.
2. **Minsta mojliga bro.** ~~En Julia-fil med en (1) funktion. En Python-fil
   som kallar den via `juliacall` och skriver ut svaret. Inget mer.~~
   **BYGGD** pa branch `julia-bridge-steg2`: `bridges/j4x9pt.jl` (fysik,
   funktionen `kvadrat`) och `bridges/r7w2kd.py` (anropet). Ingen server,
   ingen HTTP, samma process. Kor: `python3 bridges/r7w2kd.py`.
3. **Ta om `m4t7bq.py` over bron.** Samma termometer, men `mm_to_celsius`
   flyttas till Julia med Unitful. Samma utskrift. Om siffrorna ar identiska
   ar bron bevisad.
4. **Enhets-porten.** Python-sidan far en dekorator eller ett litet
   `Reading`-objekt som barer enhet. Det ar har LLM:en stoppas fran att skicka
   in ett nake tal.
5. **Kaimon-kopplingen.** Ett kort i `~/dev/kantimon` vars `speed` inte ar en
   siffra i TS utan en berakning over bron. Bevisar att spelet och
   vetenskapen ar samma form.
6. **Notera skillnaden.** En kort note: "fixpunkt vs alfabete vs enhet" — tre
   satt att forankra ett tal. Fortsatter serien fran `q3v8mz.md`.

## Vad som INTE ska goras

- **Inte sla ihop repona.** world-37, kantimon och base57 forblir separata.
  Bron ar en tredje sak, inte en sammanslagning.
- **Ingen server, ingen HTTP.** `juliacall` i samma process. Nar det blir en
  REST-API har poangen redan gatt forlorad.
- **Inte lata LLM:en generera Julia-koden fritt.** Bron ar en fast, liten yta.
  Det ar hela sakerheten.
- **Inte skriva om `research/mercury-thermometers-sweden.md`.** Ratext.

## Oppen fraga

Ska `bridges/` ligga i world-37 eller bli ett eget repo? Argument for
world-37: bron ar en *note* om lager, inte ett verktyg. Argument for eget:
kaimon ska ocksa kunna anvanda den. **Forslag: borja i world-37, bryt ut om
kaimon faktiskt behover den.**
