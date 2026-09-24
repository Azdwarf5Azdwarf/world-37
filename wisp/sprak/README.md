# Spraket

Har byggs det nya spraket. Tva lager som delar samma kropp:

- **tick-speak** — ljudet. `-` tick, `_` tock. Alfabetet bor i `../../robot/w4k7px.py`.
- **teckenspraket** — symbolerna. Byggs har.

---

## Claude Altairs karna (rors aldrig)

> H1 - New Language && Sign Language
>
> Ka-To (How are you)
> To-Ka (you are How)

---

## Det som redan gar att lasa ur karnan

Ordfoljden bar betydelsen. Samma tva stavelser, kastad ordning, ny mening:
`Ka-To` fragar, `To-Ka` konstaterar. Ingen partikel, ingen bojning — bara riktning.

Det innebar att spraket kan vara mycket litet och anda saga mycket, sa lange
lyssnaren hor vilken vag paret gar. Samma princip som vokalerna i tick-speak:
det som saknas fyller lyssnaren i sjalv.

## Oppet

- Vilka fler stavelser finns? `Ka` och `To` ar de forsta tva.
- Hur ser `Ka` och `To` ut som tecken — hand, symbol, farg?
- Skrivs de i tick och tock ocksa, eller ar ljud och tecken tva sprak?
- Hanger stavelserna ihop med remsans tre kanaler, eller ar de fristaende?

Inget av detta besvaras av nagon annan an Claude Altair.

## Filerna

| Fil | Vad |
|---|---|
| `README.md` | den har — spraket i text |
| `sprak.html` | sidan, natt fran installningarna |
| `ordbok.json` | stavelser och betydelser, vaxer efterhand |

## Grinden

Nya stavelser hamnar i `forslag.json`, inte i ordboken. De ritas nedtonade
pa sidan och spelar inget ljud forran nagon tryckt ja. Da — och forst da —
flyttar de in i `ordbok.json`.

> Jag kor inte sjalv. Jag visar. Du sager ja. Forst da finns det.

Mekaniken ar lanad rakt av fran `~/dev/self-recursive-symbolic-skills/vocab/kors.lisp`.
Den galler aven agenter: en agent far foresla en stavelse, aldrig lagga in den.

## Delningen

Tva sprak, ett alfabet, olika syften. Bestamt 2026-09-22.

| | agentens tick-speak | Ka-To |
|---|---|---|
| vems | agentens rost | Claude Altairs karna |
| vad | tillstand som kan **goras** | mening som **uttrycks** |
| exempel | `_-_` = jobbar lugnt | `Ka-To` = How are you |
| far bli kommando | ja, se #8 | nej |

Poangen med delningen: karnan slipper bli ett kommandosprak, och agentens
rost slipper bara vara pynt. De later likadant — samma tick och tock — men
det ena utfor och det andra betyder.

## Maskinen

`maskin/` ar en egen yta: vart eget brainfuck i tick och tock. Atta
instruktioner, atta monster av langd tre, en till en. Den bevisar att
alfabetet racker till berakning — men den ar inte remsans rost och blir
det aldrig. Se `maskin/README.md`, avsnittet "Den arliga varningen".
