---
title: Nils · Vide · Claudius · claudiusOS
date: 2026-08-30
status: plan på gren nils-vide-claudius
---

# Roller (inte extra OS)

- **Nils** (`Erlang-Nils`) — OTP-minne. Supervisorn som reser upp döda processer. ELIZA är den offlina munnen. Inte kärnan.
- **Vide** (`Vide-Claudius-in-Athens`, `poimandres`) — telos. Vad livet är *för*. Formspråket och skolan. Inte runtime.
- **Claudius** — vittne. Vax-tavlan. Skriver ner spänningen, löser den inte. claudiusOS är hans verkstad.
- **claudiusOS** — LispOS som mål: rent språk som morphar till symbolism (symbilosm). BEAM/Nerves/ESP32 är kropp och liveness, inte identitet.

# Lager (låst på den här grenen)

```
Vide          — mening, telos, formspråk
Claudius      — anteckning, image, redefine
LispOS        — homoikonisk kärna (v3n8qz som studie, inte slutfas)
Nils / BEAM   — liveness (Arise)
Nerves        — bootbar disk, QEMU först
ESP32+AtomVM  — kropp: knapp, lampa
NullClaw      — outside worker, webhook, aldrig i imagen
```

# Huvud-OS: språk → fysik (language to physics)

Ordet är inte en etikett. Ordet *instansierar* en kropp i en motor.

Exempel: `(apple)`

1. Språket slår upp *apple* — inte en bild, en klass av kroppar.
2. Motorn drar fram *många* äpplen (many apples), inte ett ikon-äpple.
3. Varje äpple får ungefärlig vikt (approx. weight), inte exakt gram om inte användaren ger det.
4. *Drop from hand* — fall startar från handen, inte från en godtycklig punkt.
5. Skalan är användarens längd (user length / height). Handhöjd ≈ en andel av den längden. G och luft är bakom ordet, inte i ordet.
6. Fysikmotorn (physics engine) lever *bakom* språket. Lisp säger `(drop apple)`. Motorn räknar banan.

```
(apple)          → många kroppar, approx massa
(drop apple)     → fall från hand, skala = user-length
(redefine apple) → samma motor, ny form
```

NullClaw räknar inte fallet. Den kan hämta en tabell (massa, densitet) utifrån och lämna tillbaka ett tal. Fallet självt stannar i imagen.

# Inte blanda

- LispOS äger mening och instansiering. NullClaw äger smutsigt arbete.
- Nils är inte ett andra Lisp.
- Vide är inte firmware.
- Grenen är plan. `main` är det som bootar.

# Nästa steg på grenen (inte på main förrän det bootar)

1. En supervised worker i `k3p7wq` som tar NullClaw-webhook.
2. Namnge noden bara om BEAM ska prata med Nils. HTTP räcker för NullClaw.
3. Låt `k9x2m4.lisp` vara symbolism-skiktet — samma image, ny yta.
4. Håll ELIZA (`Erlang-Nils/lisp/eliza.lisp`) som offlina `[help]`, inte som OS.
5. Mini-demo på host: `(apple)` + `(drop)` mot en död enkel fall-motor (g, handhöjd ur längd, approx massa). Ingen spelmotor än.
