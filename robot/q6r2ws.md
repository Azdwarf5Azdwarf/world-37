# Roboten — planen
2026-09-03 · branch `worktree-tickspeak`

> ## NASTA HANDLING
> **Sag till Claude: "kor steg 4".**
>
> Du behover inte minnas nagot mer an det. Allt annat i den har filen
> ar till for att lasas at dig, inte av dig.

En liten robot som gar bredvid mig pa gatan och vi ar oense.
Han talar aldrig. Han klickar. Folk skrattar och fragar vad fan som hander —
och det ar vagen in till AI pa riktigt.

Malet ar inte funktionalitet. Malet ar att ga genom en stad en gang
och prata med honom.

---

## Var vi ar

| | steg | status |
|---|---|---|
| 1 | Hardvara — kort, kamera, hogtalare, powerbank | ✅ kort valt |
| 2 | Ljudvokabular — tick och tock | ✅ `w4k7px.py` |
| 3 | Seendet — bild → claude-cli → en reaktion | ✅ `v8n4rq.py` |
| 4 | **BLE-narhet — han flyr nar jag kommer nara** | ← harnast |
| 5 | Regi — kiosken, familjen, jakten | inte borjat |
| 6 | Repetition — en gang hemma, en gang pa gatan | inte borjat |

## Filerna

```
robot/w4k7px.py    rosten — 22 tecken i tick och tock
robot/m2q7bd.md    alfabetet, lasbart i telefonen
robot/v8n4rq.py    ogat — vision-loopen + overlay-servern
robot/k9x3mt.html  overlayen, byggd for solsken och en hand
robot/q6r2ws.md    den har filen
```

## Kor

```
python3 robot/v8n4rq.py            # pa kortet, overlay pa :8080
python3 robot/v8n4rq.py --torr     # utan kamera, testa flodet
python3 robot/w4k7px.py "hej"      # bara rosten
```

Kor i `tmux new -s robot` pa kortet sa overlever den att SSH stangs.

---

## Steg 4 — BLE-narheten (harnast)

Det som gor hela scenen. Han ska veta var jag ar, och dra sig undan
nar jag narmar mig. Ingen positionering, ingen karta — bara stark
eller svag signal.

Minsta vagen:

1. Telefonen sander en BLE-beacon. Vilken enkel app som helst duger —
   ingen egen Android-app behovs for MVP.
2. Roboten skannar med `bluetoothctl` / `bleak` och laser **RSSI**.
3. Tre lagen, inget mer:
   - svag signal → jag ar langt bort → han gar mot mig, nyfiken
   - mellan → han star still och tittar
   - stark → jag ar nara → han backar och sager `_-_-, --_, -__, ___` (forlat)
4. Slata vardet over ~5 matningar. Ra RSSI hoppar for mycket.

Oppen fraga: hur ofta ska han byta lage? For snabbt = ryckigt.
For langsamt = han reagerar inte pa att jag springer.

## Steg 5 — regin

Tre scener, skrivna i forvag. Mina repliker ar ord. Hans ar ljud.

- **Kiosken** — han tittar pa skylten, jag fragar varfor han saljer SIM-kort
- **Familjen** — han cirklar runt dem och klickar, jag sager
  "forlat, han ar bara ett barn, han lar sig fortfarande"
- **Jakten** — jag ropar "ey kom tillbaka", han backar och ber om ursakt
  medan folk ser mig jaga honom

---

## Regler som inte far glida

- **Inget tal.** Ingen text-till-tal. Bara klick.
- **Ingen inspelning.** Bilden gar till claude och slangs. Inget sparas.
- **Inga ansikten, inga namn.** Prompten sager det redan.
- **Konsonanter pa gatan.** Vokalerna fyller lyssnaren i sjalv — det ar
  hela grejen. Fullt lage (`-f`) ar bara for hemma.
- **Alfabetet ar mitt.** Tabellen i `w4k7px.py` skrivs inte om av nagon annan.

## Sen, nar det finns resurser

Egna voice-agents. Da kan han fa en riktig rost — men forst ska
klick-versionen ha gatt genom en stad en gang.
