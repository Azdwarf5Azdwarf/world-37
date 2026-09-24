# Maskinen

Vart eget brainfuck, skrivet i tick och tock. Inspirerat av brainfuck,
inte en klon — det enda vi lanar ar iden att atta instruktioner racker.

## Passformen

Brainfuck har exakt atta instruktioner. Tick-speak har exakt atta monster
av langd tre. En till en, inget over, inget under.

| monster | order | brainfuck | ocksa bokstaven |
|---|---|---|---|
| `---` | hoger | `>` | n |
| `___` | vanster | `<` | t |
| `--_` | upp | `+` | r |
| `__-` | ner | `-` | s |
| `-__` | ut | `.` | l |
| `_--` | in | `,` | d |
| `-_-` | borja | `[` | j |
| `_-_` | slut | `]` | m |

Monstren ar samma som atta av robotens bokstaver. Det ar ingen krock —
**laget avgor**. I maskinlage ar `---` hoger, i talat lage ar det n.
Ett sprak, tva lasningar.

## Kor

```sh
python3 maskin.py hej.tick              # Hello World!
python3 maskin.py --lista               # tabellen
python3 maskin.py --fran-text '+++.'    # brainfuck in, monster ut
echo '--_ --_ -__' | python3 maskin.py -
python3 maskin.py hej.tick --spela      # hor programmet i robotens rost
```

## Den arliga varningen

`hej.tick` ar 106 order for att saga "Hello World!". Uppspelat i robotens
takt — 245 ms per order plus 210 ms paus — tar det **omkring 48 sekunder**
att lyssna pa.

Det ar precis Claude Altairs invandning: enorma rader for nagot litet. Den ar ratt.
Darfor ar maskinen inte remsans rost och blir det aldrig. Den ar en egen
yta att leka pa, och ett bevis pa att alfabetet racker till berakning.

Vill du ha nagot kort som sager mycket — det ar `Ka-To`, inte det har.
Se `../README.md`, avsnittet "Delningen".

## Vad den inte ar

- Ingen kompilator. En uppslagning och en dispatch, 170 rader.
- Inte kopplad till remsan, loggen eller grinden.
- Inte Claude Altairs karna. Den har far skrivas om fritt.
