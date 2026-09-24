---
title: Frågor
---

Rå lista. Frågan skrivs här när den dyker upp. Svar hamnar i `_ANSWERS.md`
under samma rubrik. Stryk aldrig en fråga — markera den `[besvarad]`.

---

## Q1 — Varför QEMU och BEAM? Varför blanda ihop dem? [besvarad]
2026-08-29

## Q2 — Väljer systemet färgen, eller gör du det?
2026-08-29

`k9x2m4.lisp` härleder färgen ur tempus: `choose-color` ger `:past` grön
och `:future` blå. `features/q3w8n1.md` §III säger tvärtom att färgen är
ett *svar du måste ge* när rutan öppnas — röd för ja, blå för nej-kanske,
grön för det ännu okända.

Det är två olika språk. Antingen är färgen härledd (då är den redundant
information om tempus) eller så är den ett val (då ska `when-time` ta emot
den, inte räkna fram den). Koden gör det första, manifestet det andra.
