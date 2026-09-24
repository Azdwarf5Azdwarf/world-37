# Nu

**2026-09-22** — remsan lever, talar och gar att fraga.

## Klart

- Krok `~/.claude/hooks/agent-events.sh` loggar PostToolUse, Notification
  och Stop med ett `err`-falt for roda kanalen.
- `serve.py` pa localhost:8787 serverar sidan, `/events.json`, `/alfabet.json`
  (last direkt ur `../robot/w4k7px.py`) och `/installningar.json`.
- `strip.html` ritar en kolumn per tick i R/G/B.
- Rosten i `tickspeak.js` — tick 1900 Hz, tock 780 Hz, 45 ms. Delad med
  `config.html` och `sprak/sprak.html`.
- `config.html` sparar troskelvarden till disk, inte bara till webblasaren.
- Klick pa en kolumn packar upp den: ord, klockslag och varje handelse bakom
  fargen. Vald kolumn foljer sin tidpunkt medan remsan scrollar.
- Troskelvardena godkanda av Claude Altair ("lagom"). Skruva inte utan att han ber om det.

## Nasta

- [ ] `agent`-nyckel i loggraden, en smal rad per agent i remsan (#7)
- [ ] Grinden i `sprak/forslag.json` — inget tecken talar utan ett ja (#6)
- [ ] Klartextrad i uppackningspanelen: "fyra Bash, ett fel, vantade 12 s" (#5)
- [ ] Kor ett riktigt arbetspass med remsan i ett horn och se vad som kanns fel
- [ ] `sprak/` — Claude Altair satter tecken och tickar for Ka och To

## Vad vi INTE bygger nu

Uttalat parkerat. Ta inte upp dem sjalvmant.

- Wave-baserat ljud istallet for klick — Claude Altair vill lara sig ljudalgoritmer forst.
- Lisp-lager med hex-logos och ffmpeg-export (#3). Hans ord: "tomuch now".
- Docker-container for remsan.
- Erlang/OTP och ESP32. Beslutat som riktning, inte som arbete.
- Bokstavslage — att en kolumn ocksa kan vara en bokstav.
- Kompilator. #8 ar en uppslagning och en dispatch, inget mer. Vaxer det
  forbi hundra rader har vi byggt fel sak.
- `~/dev/tyst-sprak-skiss.html`. Den ligger orord tills Claude Altair oppnar fragan.

## Issues (gitea)

- #1 langa ord blir for langa att lyssna pa
- #2 symboler som blinkar istallet for ord — bar ocksa teckenspraket
- #3 lisp-lager med hex-logos, ffmpeg senare
- #4 skillnaden mellan tystnad och tecknet for tystnad
- #5 packa upp en symbol — "vanta, vad menar du?"
- #6 grinden: inget tecken talar utan ett ja
- #7 flera agenter i samma remsa
- #8 ordet ar ett kommando — uppackning och exekvering ar samma sak

## Att veta

`___` ar ett yttrande, inte ett tomt lage. Att agenten valjer att saga att
ingenting hander ar narvaro — tysta aldrig ner det som "inget att visa".
Ordboken ska darfor forbli mestadels tom: tecken vaxer ur handelser mellan
Claude Altair och agenten, inte ur en tabell nagon hittat pa i forvag. Se #4.

Tick-speak har **tva** symboler, inte tre. `-` tick 1900 Hz, `_` tock 780 Hz.
En WebUI-trad foreslog tre nivaer (`_ - =`) — det stammer inte med alfabetet
i `../robot/w4k7px.py`.

## Spraket

`sprak/` ar egen yta: `README.md`, `sprak.html` (nas fran installningarna)
och `ordbok.json`. Karnan dar — `Ka-To` / `To-Ka` — ar Claude Altairs och skrivs
aldrig om. Tomma falt i ordboken ar avsiktligt tomma.
