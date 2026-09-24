# claudiusOS — arbetsinstruktioner

Läs `README.md` först (arkitektur, hårdvaruväg, läslista) och `q4m8t2.md`
(vision, formspråk, varför-frågorna). Upprepa inte deras innehåll här.

## Filnamn är slumpmässiga ID

Alla dokument heter ett kort slump-ID, aldrig ett beskrivande namn. Titel
och ämne står *inuti* filen. Kartan över vad som är vad:

| Fil | Vad det är |
|---|---|
| `q4m8t2.md` | Vision, formspråk, språkval. Huvuddokument. |
| `lisp/v3n8qz.lisp` | Mini Lisp-OS, ~340 rader, single-file. |
| `lisp/z7f4nq.lisp` | Kompilator: Lisp-modell-DSL -> tensor-IR -> PyTorch. Skriver `build/`. |
| `lisp/k9x2m4.lisp` | Symboliskt tidsspråk, bas 57 = 3 x 19. Skiss. |
| `lisp/t8k2vr.lisp` | Testsvit för Lisp-spåret: boot-test + enhetstester. |
| `lisp/x4nb9t.sh` | Kör alla testlager. Enda inkörsporten. |
| `lisp/m2vq7k.sh` | Boot-röktest av `k3p7wq.img` i QEMU. ~32 s. |
| `AIVP/k3m7vz.md` | Ljusfördröjnings-observatörsmall (rå dump), kopplad till `AIVP/v7bpx2.md`. |
| `AIVP/v7bpx2.md` | Hashmarks — sammanslagning av flera projekt, pausad mitt i. |
| `AIVP/x4k9qw.md` | AIVP device-integritet, eget ekosystem — pausad brainstorm, ej godkänd spec. |

Lisp-sidospåret ligger samlat i `lisp/` — bara ett underlag för att
skilja det från huvuddokumenten i roten. Filnamnen är fortfarande
slump-ID, ingen fil har döpts om.

Skills under `.claude/skills/` följer samma regel — katalogen är ett
slump-ID, det beskrivande namnet står i `name:`-fältet:

| Katalog | `name:` | Vad den gör |
|---|---|---|
| `p3wq7m` | `os-status` | En skärm: var projektet står, efter en paus. |
| `t9zb4x` | `qa-logg` | Fångar frågor till `learning/`, utreder på begäran. |
| `h2vk8n` | `erlang-drill` | Ett Erlang/OTP-begrepp per pass, med körbar snutt. |
| `r6dm1c` | `nerves-qemu` | Bygg/kör-loopen för Nerves + QEMU, feltriage. |
| `j4sy5g` | `kallasning` | Guidad läsning av ett stycke ur läslistan. |

Nya filer följer samma regel. Sök på innehåll, inte filnamn.

## Språkval (låst)

**Erlang · BEAM · Lisp.** Inte Elixir.

Huvudspåret är **riktig BEAM på hårdvara** via Nerves — inte BEAM som
metafor. Beslutat 2026-08-29, se `q4m8t2.md`.

`v3n8qz.lisp` är sidospår: OTP-modellen skriven för hand i Lisp, behållen
som studieobjekt. Föreslå inte att den blir huvudspår igen.

## Verifiera alltid Lisp-ändringar

```bash
sh lisp/x4nb9t.sh
```

Kör alla testlager och avslutar med 0 bara om allt är grönt. Committa
aldrig Lisp som inte bootar. `timeout` finns inte på denna maskin —
använd `gtimeout` (coreutils).

## Tester

Tre lager, i den ordning Mezzano validerar: bygget laddar rent, imagen
bootar, tester körs inne i systemet.

| Lager | Kommando | Vad det bevisar |
|---|---|---|
| 1. Lisp på host | `sbcl --non-interactive --load lisp/t8k2vr.lisp` | `v3n8qz.lisp` bootar (`OS BOOT COMPLETE`), evaluator/reflektion/processtabell fungerar, `k9x2m4.lisp` laddar |
| 1b. Kompilatorn | `sbcl --non-interactive --load lisp/z7f4nq.lisp` | Egen självtestsvit, 15 kontroller. Rör den inte. |
| 2. BEAM på host | `cd k3p7wq && MIX_TARGET=host mix test` | Supervisor-trädet är uppe |
| 3. QEMU-boot | `sh lisp/m2vq7k.sh` | `k3p7wq.img` når `iex`-prompten. ~32 s, ingår inte i `x4nb9t.sh`. |

Testidiomet är `check` / `check-error` / `*fails*` från `z7f4nq.lisp` §6 —
kopieras, inte abstraheras. Inget testbibliotek, ingen quicklisp.

## Konventioner i v3n8qz.lisp

- Single file, inga beroenden utanför ANSI CL. Ingen alexandria, ingen
  quicklisp. `hash-table-keys` m.fl. finns inte — skriv `loop`.
- Paketet `:mini-lisp-os` använder `:cl`. Skuggar du en CL-symbol måste
  den in i `(:shadow ...)`, annars ger SBCL package lock-fel.
- Processposten är `(pid name closure state)` — fyra fält. `state` är
  `fourth`, closuren är `third`.
- Specialvariabler (`defvar`) står överst, före all användning.
- Sektionerna är numrerade med `;; ===` -banners. Behåll ordningen.

## Ton i dokumenten

Svenska med engelsk fackterm i parentes vid första förekomsten. Korta
rader, hellre punktlista än stycke. Inga marknadsföringsord.
