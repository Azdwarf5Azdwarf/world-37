# world-37 — for agenter

Filnamnen ar ofta slump-ID. Kartan ar wikin.

## Kolla alltid wikin forst

Innan du andrar nagot i repot: las motsvarande sida i `docs/`.

| Omrade | Wikisida |
|---|---|
| `claudiusOS/AIVP/` | `docs/aivp/oversikt.mdx`, `docs/aivp/protokoll.mdx` |
| `claudiusOS/subjective-clock/` | `docs/subjective-clock/*.mdx` |
| `robot/`, `wisp/sprak/` | `docs/tick-speak.mdx` |
| `wisp/` | `docs/wisp.mdx` |
| `claudiusOS/` ovrigt | `docs/claudiusos.mdx` |

Andrar du nagot som en wikisida beskriver ar wikin inaktuell. Kalla da
underagenten `wiki-vaktare` (nedan) nar ditt jobb ar klart, eller saga
till att wikin behover ses over.

## Underagenter

| Agent | Definition | Ansvar |
|---|---|---|
| `wiki-vaktare` | `.claude/agents/wiki-vaktare.md` | Haller `docs/` i fas med kallfilerna. Uppdaterar sidorna, kontrollerar lankar, rapporterar vad den andrat. |

Spawna den bara nar Claude Altair ber om det, eller efter en andring som
wikin beskriver. En agent i taget.

## Regler som galler alla

- Ratext rors aldrig: filer markerade `RATEXT`, "Karnan", `robot/w4k7px.py`-tabellen.
- Svenska skrivs utan a-ring och prickar (a/a/o), som resten av repot.
- Repot ar publikt. Inget personligt, inga namn pa andra, inga hemligheter.
