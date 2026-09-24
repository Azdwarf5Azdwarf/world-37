# wisp

Agentaktivitet som en fargremsa du laser utan att titta, och hor utan att lyssna.

En krok i Claude Code skriver varje handelse till en logg. En liten lokal
server laser loggen. En sida ritar en kolumn per tick och spelar samma
kolumn som ett ord i tick och tock.

```
hook  ->  ~/.agent-events.log  ->  serve.py :8787  ->  strip.html
```

## Kom igang

```sh
python3 ~/dev/world-37/wisp/serve.py      # http://localhost:8787
```

Klicka **ljud av** nere till hoger for att sla pa rosten.
Konfiguration: <http://localhost:8787/config.html>

Overlever fonsterstangning:

```sh
tmux new -s wisp -d 'python3 ~/dev/world-37/wisp/serve.py'
```

## Fargerna

| Farg | Betyder | Kalla |
|---|---|---|
| rod | fel och misslyckade verktygsanrop | `err: true` i loggen |
| gron | lyckade verktygsanrop | `PostToolUse` |
| bla | vantar pa dig — behorighet, avslutad tur | `Notification`, `Stop` |

En frisk session ar gron. Blatt = stillastaende. Rott = nagot brast.

## Filerna

| Fil | Vad |
|---|---|
| `serve.py` | lokal server, serverar sidan och `/events.json` |
| `strip.html` | remsan sjalv — ritar och talar |
| `config.html` | troskelvarden och alfabetet |
| `~/.claude/hooks/agent-events.sh` | kroken som skriver loggen |
| `../robot/w4k7px.py` | rosten, tick-speak-alfabetet |

## Lasa mer

- [VISION.md](VISION.md) — vart det ska
- [CURRENT.md](CURRENT.md) — var det star nu
- [CLAUDE.md](CLAUDE.md) — for agenter som jobbar har
