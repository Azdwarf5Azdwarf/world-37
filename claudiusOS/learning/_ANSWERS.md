---
title: Svar
---

## A1 — Varför QEMU och BEAM?

> **Efterskrift 2026-08-29:** utredningen nedan landade i "ta BEAM:s idé,
> inte BEAM". Beslutet blev det motsatta — riktig BEAM, huvudspår, via
> Nerves. Analysen står kvar för att den förklarar *varför* de två spåren
> drar åt olika håll, inte för att den avgjorde något.


**De hör inte ihop. Du har fångat en riktig hopblandning.**

Det är två separata spår som glidit in i varandra:

**QEMU-spåret** handlar om att komma ner till metallen. Ett Lisp-OS som
bootar själv, utan Mac eller Windows under sig. QEMU är bara en emulator
(emulator) — en fejkad dator att testa på så du slipper bränna USB-stickor.
Det spåret slutar i Mezzano, multiboot, GDB.

**BEAM-spåret** handlar om samtidighet (concurrency). BEAM är en virtuell
maskin som körs *ovanpå* ett existerande OS — Linux, macOS. Den bootar inte
bar metall. Den ger dig miljontals lätta processer, meddelanden mellan dem,
och supervisors som startar om det som dör.

Blandar du dem får du två projekt som drar åt olika håll: ett som vill bort
från värd-OS:et, ett som förutsätter ett.

### Vad du faktiskt vill ha

Du vill inte köra BEAM. Du vill ha **BEAM:s idé** — supervisor-trädet,
"Arise" — inne i ditt Lisp-OS.

Det är precis vad `v3n8qz.lisp` redan gör: `*process-table*`,
`spawn-agent`, `scheduler-tick`. Det är OTP:s modell, skriven i Lisp.
Ingen Erlang inblandad.

Så:
- **BEAM/OTP** = förebild för processlagret. Läs Erlang för mönstren.
- **QEMU** = testbänk för när Lisp-lagret ska boota utan värd-OS.
- De möts aldrig i koden. Bara i huvudet.

### Om du ändå ville köra riktig BEAM bare metal

Det finns: GRiSP, Nerves, och det gamla forskningsspåret Erlang-on-Xen.
Men då är det inte längre ett Lisp-OS. Välj ett.
