---
name: qa-logg
description: Använd när Claude Altair kastar ur sig en fråga mitt i arbetet i claudiusOS — "fråga:", "skriv upp det där", "det där undrar jag över", "varför ...?" utan att vänta på svar — eller när han senare säger "utred Q3", "svara på frågan om X". Skriver frågan till learning/_QUESTIONS.md och svaret till learning/_ANSWERS.md. Svara ALDRIG direkt när han bara vill fånga frågan.
---

# qa-logg — frågan in, svaret sen

## Varför den finns

En fråga som dyker upp mitt i ett bygge har två dåliga utgångar: han
släpper spåret och utreder den nu, eller så glömmer han bort den. Loggen
i `learning/` finns för att ge en tredje: **skriv ner, gå vidare**.

Därför är fångst och utredning två skilda handlingar. Blandar du ihop dem
förstör du poängen — han fick ett svar han inte bad om, och tappade det
han höll på med.

## Läge 1 — fånga (standard)

Han nämner en fråga i förbifarten. Du:

1. Läs `learning/_QUESTIONS.md`, hitta högsta `Q`-numret, ta nästa.
2. Lägg till sist i filen:

```
## Q<n> — <frågan, hans ord>
<ÅÅÅÅ-MM-DD>
```

3. Svara med **en rad**: `Q<n> uppskriven.` Inget mer. Inget svar på frågan,
   ingen "vill du att jag utreder den nu?".

Frågan skrivs med hans formulering, inte en snyggare version. Han ska känna
igen den när han kommer tillbaka.

## Läge 2 — utreda

Han säger uttryckligen "utred Q3" / "svara på Q3" / "vad blev det med
frågan om X". Då:

1. Utred på riktigt. Svaret får vara långt — det är ett dokument, inte
   ett chattsvar.
2. Skriv i `learning/_ANSWERS.md` under rubriken `## A<n> — <samma rubrik>`.
   Svenska, engelsk fackterm i parentes första gången, korta rader.
3. Märk frågan i `_QUESTIONS.md` med ` [besvarad]` sist i rubrikraden.
4. I chatten: svaret i en mening + var det står. Inte hela utredningen igen.

## Regler som inte förhandlas

- **Stryk aldrig en fråga.** Inte ens en dum, inte ens en som blev
  irrelevant. Markera `[besvarad]` — historiken är poängen.
- Ändrar ett beslut ett tidigare svar: skriv en efterskrift överst i
  `A<n>`, som den i `A1`. Skriv inte om svaret.
- Numren är löpande och återanvänds aldrig.
