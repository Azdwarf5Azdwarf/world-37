# Underagenter

Vem som far gora vad har inne. Spawna inte nagon om Claude Altair inte ber om det.

| Agent | Nar | Rakraden |
|---|---|---|
| `Explore` | leta i world-37 nar du inte vet var nagot bor | "hitta var X definieras, medium bredd" |
| `general-purpose` | flerstegsjobb som inte ska ata kontext har | ge den ETT avgransat mal |
| `python-pro` | om `serve.py` vaxer till nagot med tillstand | typning och tester, inte stil |
| `fork` | nar ett sidospar riskerar att tappa huvudtraden | forken arver kontexten |

## Regler

- En agent i taget. Claude Altair blir overbelastad av parallella rapporter.
- Visa agentens egna ord rakt av. Sammanfatta inte at honom.
- Ingen agent ror `../robot/w4k7px.py`-tabellen eller Claude Altairs egen ratext.
- Langa jobb i tmux, inte i forgrunden.

## Vad som faktiskt gjorts

2026-09-22: tva Explore-agenter pa sonnet, parallellt, en rapport var —
en pa sprak- och ljudrepon, en pa runtime och symbolik. Ingen tredje agent,
ingen Plan-agent. Det rackte, och resultatet star i KOPPLINGAR.md.

Dosen att harma: **tva agenter, tydligt delad yta, en rapport var.**
Fler an sa ger overlappande svar som Claude Altair sen far sortera.

## Framtid

Nar flera agenter matar samma remsa far var och en en `agent`-nyckel i
loggraden. Da kan remsan visa ett band per agent istallet for ett enda.
