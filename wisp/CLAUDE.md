# wisp — for dig som jobbar har

Remsan som visar agentaktivitet i farg och tick-speak.
Lokal, offline, ingen molntjanst.

## Las forst

| Fil | Nar |
|---|---|
| [README.md](README.md) | vad det ar och hur du startar det |
| [CURRENT.md](CURRENT.md) | **borja har** — var arbetet star just nu |
| [VISION.md](VISION.md) | vart det ska, och Claude Altairs egen karna |
| [SUB_AGENTS.md](SUB_AGENTS.md) | vilka agenter som far gora vad |
| [SKILLS.md](SKILLS.md) | vilka skills som galler har |
| [KOPPLINGAR.md](KOPPLINGAR.md) | vad i `~/dev` som hor hit — gor inte om inventeringen |

## Hus regler

- **Alfabetet i `../robot/w4k7px.py` ar Claude Altairs.** Koden ror det aldrig. Inte du heller.
- Troskelvardena ar godkanda ("lagom" 2026-09-22). Skruva bara pa begaran.
- Tick-speak har TVA symboler: `-` tick 1900 Hz, `_` tock 780 Hz. Inte tre.
- **Inget nytt tecken talar utan ett uttryckligt ja.** Forslag hamnar i
  `sprak/forslag.json` och ritas nedtonat tills Claude Altair godkant dem.
- Allt lokalt. Ingen del av det har gar till molnet.
- Nar du andrat nagot: uppdatera `CURRENT.md`, inte den har filen.

## Kedjan

```
~/.claude/hooks/agent-events.sh   krok, en rad JSON per handelse
        v
~/.agent-events.log               {t, e, tool, err}
        v
serve.py :8787                    /events.json
        v
strip.html                        en kolumn per tick, R/G/B + rost
```
