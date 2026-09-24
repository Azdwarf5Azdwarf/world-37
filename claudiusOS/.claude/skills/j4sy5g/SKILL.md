---
name: kallasning
description: Använd när Claude Altair vill läsa källor eller källkod till claudiusOS — "läs SICP med mig", "vad gör supervisor/entry.lisp", "förklara metacirkulära evaluatorn", "ta ett stycke ur läslistan". Läser ETT litet stycke, förklarar på svenska med koppling till projektet, och lägger resultatet i learning/ som en ny slump-ID-fil. Aldrig ett helt kapitel.
---

# kallasning — ett stycke i taget

## Varför den finns

Läslistan i `README.md` är tung: SICP kap. 4, *Lisp in Small Pieces*, AMOP,
Brian Smiths 3-Lisp, Mezzanos `supervisor/`. Öppnar man dem i fel storlek
händer inget alls — texten är för stor att börja på, och då blir det ingen
läsning den dagen.

Rätt storlek är **ett stycke**: en funktion, ett avsnitt, en idé.

## Passets form

1. **Välj stycket.** Säger han inte vilket: ta nästa oläst enligt ordningen
   nedan. Säg vilket du tog, en rad.
2. **Läs det.** Har vi filen lokalt (t.ex. en klonad Mezzano) — läs den.
   Annars: läs det du säkert vet och säg rakt ut vad du inte har framför dig.
   Hitta aldrig på radnummer eller kod ur en källa du inte läst.
3. **Förklara.** Max ~10 rader. Svenska, engelsk fackterm i parentes första
   gången. Vad koden gör, inte varför den är fin.
4. **Koppla.** En rad: vad det här betyder för claudiusOS.
5. **Skriv ner.** Ny fil i `learning/` med slump-ID som namn (t.ex. `w8k3nq.md`),
   titel och datum i frontmatter — aldrig i filnamnet.

## Ordningen

**Mezzano** (`supervisor/`), när repot är klonat:
`entry.lisp` → `interrupt.lisp` → `gc.lisp` → `compiler/lap.lisp`.
Ordningen är från `README.md` och är vald: första Lisp efter assembler först.

**SICP kap. 4** — den metacirkulära evaluatorn (metacircular evaluator),
i småbitar: `eval`/`apply`-paret → omgivningar (environments) → special forms
→ `analyze`-varianten.

**Brian C. Smith, 3-Lisp** — sist. Den är roten till traverserings-idén i
`README.md` men svårast att gå in i kall.

## Filmall

```markdown
---
title: <vad stycket var>
källa: <bok/fil>
date: <ÅÅÅÅ-MM-DD>
---

<förklaringen>

## För claudiusOS
<en rad>
```

## Gör inte

- Läs inte vidare till nästa stycke i samma svar, hur naturligt det än följer.
- Sammanfatta inte en hel bok. Det finns redan i `README.md`s läslista.
- Skriv inte in läsningen i `_ANSWERS.md` — den filen hör till `qa-logg`
  och besvarar numrerade frågor. Läsning är egna filer.
