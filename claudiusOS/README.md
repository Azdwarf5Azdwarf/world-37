---
title: claudiusOS
date: 2026-08-29
---

# claudiusOS

Huvudspår: **BEAM på riktig hårdvara** via Nerves. Se `q4m8t2.md`.

Lisp-OS-materialet nedan är sidospår — behållet som studieobjekt, inte
som byggmål. Undantag: **Mezzano** (`## Mezzano på M1` nedan) är sedan
2026-09-15 ett aktivt sidospår — vi bygger faktiskt på det, inte bara läser
källan. BEAM/Nerves förblir huvudspåret.

## Vad som finns

- `q4m8t2.md` — vision, formspråk, beslut. Huvuddokument.
- `k3p7wq/` — Nerves-projektet (huvudspår). Elixir-skal runt BEAM,
  target `x86_64`. Firmware byggd 2026-08-29: `k3p7wq/k3p7wq.img` (785 MB).
  Bootar i QEMU till `iex`-prompt, verifierat 2026-08-29 (~32 s).
- `features/` — rå idélista, en fil per idé. Inget beslutat.
- `learning/` — `_QUESTIONS.md` och `_ANSWERS.md`. Frågor och utredningar.
- `AIVP/` — **Agent Identity Verification Protocol** (agentidentitetsverifikationsprotokoll),
  eget projekt sammanslaget hit 2026-09-15 (egen git-historik bevarad på
  github.com/Azdwarf5Azdwarf/AIVP.git). Multi-agent-autentisering: morgon-2FA-upplåsning
  (phone + computer), prime-signaturer i en witness-blockchain (agenter känner igen
  varandra och upptäcker drift), dubbelkanals-kommunikation (konsonanter/ticking utåt,
  vibrationer/vowels inåt). Spec-stadium, inget kört ännu — läs `AIVP/README.md` för
  läsordning. Två pausade sidotankar ligger som `AIVP/v7bpx2.md` (Hashmarks-sammanslagning)
  och `AIVP/x4k9qw.md` (device-integritet).
- `lisp/` — Lisp-sidospåret, samlat i en undermapp. Filnamnen är
  fortfarande slump-ID, se kartan i `AGENTS.md`.
  - `v3n8qz.lisp` — mini Lisp-OS: metacirkulär evaluator (metacircular
    evaluator), reflektionsprimitiver, processtabell, schemaläggare.
    Kör: `sbcl --load lisp/v3n8qz.lisp`
    Status: bootar rent under SBCL (verifierat 2026-08-29).
  - `k9x2m4.lisp` — symboliskt tidsspråk: bas 57 = 3 x 19, triangeln
    kvadreras när tid nämns. Skiss.
    Kör: `sbcl --non-interactive --load lisp/k9x2m4.lisp`
    Bakgrund: `features/k9x2m4.md` (rå diktering), `features/q3w8n1.md`
    (manifest).

## Tester

```bash
sh lisp/x4nb9t.sh
```

Kör alla lager som går att köra på host. Tre lager, samma ordning som
Mezzano validerar i — bygget laddar rent, imagen bootar, tester körs inne
i systemet. Detaljerna står i `AGENTS.md` under "Tester".

## Arkitektur (destillerad)

Stacken, uppifrån och ner. Poängen: allt ovanför kislet är homoikoniskt
(homoiconic) — kod är data — så varje lager kan läsa och skriva om lagret
under sig.

```
User space (appar, dokument)
AI orchestration (planering, minne, verktyg)
Reflective runtime (självmodifierande Lisp-image)
Lisp microkernel / VM
Bare-metal Lisp (GC, trådar, drivrutiner)
Silicon
```

Tre sorters traversering (traversal):
- **Vertikal** — `(source-of 'f)` ger källkoden som lista; `(redefine 'f ...)`
  byter den i drift.
- **Horisontell** — introspektion av den levande objektgrafen.
- **Temporal** — hela systemet är en image: snapshot, revert, diff.

Inga syscalls. Istället *capabilities* som AI:n kan läsa, förstå och
föreslå ändringar i.

## BEAM-vägen (huvudspår)

Poängen: du får OTP, supervisors, hot code loading och distribution
gratis — och slipper skriva GC och trådar själv.

Toolchain (redan installerad 2026-08-29):

```bash
brew install erlang elixir fwup squashfs coreutils xz pkg-config
mix archive.install hex nerves_bootstrap
```

### Läget i `k3p7wq/`

Projektet är skapat, deps hämtade, firmware byggd för target `x86_64`.
Det som återstår är att faktiskt boota imagen.

```bash
cd k3p7wq
export MIX_TARGET=x86_64        # måste sättas i varje nytt skal
mix deps.get                    # bara om deps saknas
mix firmware                    # bygger om k3p7wq.img
```

Boota i QEMU:

```bash
qemu-system-x86_64 -m 1024 -drive file=k3p7wq.img,format=raw,if=virtio \
  -serial mon:stdio -display none
```

Konsolen kommer ut på seriell port. Slutläge: Nerves-bannern och en
`iex(1)>`-prompt. Noden är onamngiven — Erlang distribution startas inte
automatiskt (se `k3p7wq/mix.exs`). Ctrl-A sedan X avslutar QEMU.

Samma sak automatiserat: `sh lisp/m2vq7k.sh` (avslutar 0 när prompten nås).

`-nographic` går inte att kombinera med `-serial stdio` — QEMU vill
lägga båda på stdio och vägrar. Använd `-serial mon:stdio -display none`.

`mix firmware.burn` skriver till SD-kort/USB — kör aldrig utan att först
kontrollera vilken disk som väljs.

Vet du inte var du står: skriv `status` i Claude Code, eller använd
skillen `r6dm1c` (nerves-qemu) för bygg- och körloopen.

## Hårdvaruväg (sidospår: bare-metal Lisp)

QEMU först. Alltid.

1. SBCL på Mac/Linux — bygg reflektionstornet. Här ligger allt som spelar roll.
2. QEMU x86-64 — multiboot-kernel, serie-REPL på COM1, GDB via `-s -S`.
3. Riktig x86-64-hårdvara — bara för att bevisa att du inte fuskade.

Raspberry Pi bare metal är en fälla: VideoCore-firmware bootar före CPU:n,
device tree, MMU direkt, ingen serieport by default. ~2000 rader assembler
innan första `cons`. Pi Pico + uLisp är däremot en bra mellanstation om du
vill känna metallen.

## Mezzano på M1

**Aktivt sidospår sedan 2026-09-15** — inte bara läslista längre, vi
bygger och kör faktiskt Mezzano. BEAM/Nerves förblir huvudspåret.

Mezzano är x86-64. På Apple Silicon körs den under QEMU TCG (emulering,
ingen KVM).

```bash
brew install sbcl qemu git
git clone https://github.com/froggey/Mezzano.git && cd Mezzano
sbcl --dynamic-space-size 4096 --load build.lisp
qemu-system-x86_64 -m 2048 -hda mezzano.image \
  -vga std -serial stdio -display none -cpu qemu64 -smp 4
```

Läs källan i denna ordning: `supervisor/entry.lisp` (första Lisp efter
assembler) → `supervisor/interrupt.lisp` → `supervisor/gc.lisp` (GC:n är
skriven i Lisp) → `compiler/lap.lisp`.

Fork-strategi: gren `ai-substrate`, strippa GUI, boota till serie-REPL,
injicera egen evaluator, kapa `eval`. Mezzano har redan trådar, GC och
filsystem — bygg inte om dem.

## Läslista

- **SICP** kap. 4 — den metacirkulära evaluatorn. Icke förhandlingsbart.
- **Lisp in Small Pieces**, Queinnec — samma sak som ingenjörsmanual.
- **AMOP**, Kiczales — metaobjektprotokoll, industriell reflektion.
- **PAIP**, Norvig — riktiga AI-system i Common Lisp.
- Brian C. Smith, *Reflection and Semantics in Lisp* (1982) — roten till
  hela traverserings-idén. 3-Lisp.
- Alan Kay, *Steps Toward the Reinvention of Programming* — hela systemet
  på 20 000 rader. Nordstjärnan.
- Mezzano (`supervisor/`), Movitz, Open Genera.
