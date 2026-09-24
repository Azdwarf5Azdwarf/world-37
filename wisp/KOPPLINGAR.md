# Kopplingar

Kartan over vad i `~/dev` som hor hemma i wisp. Inventerad 2026-09-22 av
tva Explore-agenter. **Gor inte om inventeringen — uppdatera den har filen.**

Status: `levande` = fungerar och anvands · `stubb` = paborjat, litet ·
`dott` = avsiktsforklaring utan kod, eller overgivet.

## Kopplas in

| Repo | Filen | Vad vi lanar | Status |
|---|---|---|---|
| `~/dev/self-recursive-symbolic-skills` | `vocab/kors.lisp` | grinden: `(kors :hej)` ar ett FORSLAG, ingenting kors utan mansklig ja | stubb men fardig ide |
| `~/dev/lisp-swarm-test` | `speaker-tags.lisp`, `movement.lisp` | varje yttrande taggat med vem som sa det, i en delad `*transcript*`; nasta agent blir vittne | levande |
| `~/dev/Erlang-Nils` | `erlang/ai_supervisor.erl`, `lisp/eliza.lisp` | riktig OTP-genserver + supervisor, och en offline monstermatchare (426 rader Norvig-ELIZA) som kan packa upp symboler utan natverk | levande |

## Vart att veta om, men inte byggt

| Repo | Filen | Varfor den namns |
|---|---|---|
| `~/dev/pixel-to-voice` | `.worktrees/v1-implementation/` — `app.js`, `server.py` | fardig index-adresserad rutnatsmotor med polling. Narmaste tekniska forlagan for #2, blinkande symboler. Ligger pa branch `feature/v1-implementation`, inte pa main. |
| `~/dev/encoder-decoder` | `ennead-mbti-lisp/eval.lisp` | `(analyze who)` slar upp en kort kod och packar upp den till full forklaring — ratt arkitektur for #5. 89 rader. Resten av mappen ar klonade tredjepartsrepon. |
| `~/dev/kaimon-claudius` | `torus.jl`, `w7q4nx.md` | 3d-uttryck. `index.html` dar ar samma poll-arkitektur som remsan — bekraftar riktningen. `w7q4nx.md` ar ett levt exempel pa Father-Turing-safe: fjarrkorningen installerad men aldrig kvitterad. |
| `~/dev/world-37/bridges` | `j4x9pt.jl` | bron Julia↔Python finns redan inuti det har repot. En funktion, vars hela poang ar att ett tal kan korsa gransen utan att nagon konvention rors. |
| `~/dev/3d-math` | `trajectory.jl` | 190 rader Plots.jl-baserad 3d-banvisualiserare. Battre startlage an donuten om 3d ska bli pa riktigt. |
| `~/dev/android-spirit` | `ideas/k3p9x2.md` | statusmappning idle/thinking/awaiting_input/done/error → ogonform, gloed, rorelse. For den dagen remsan ska bo pa en gammal telefon. Noll kod i repot. |
| `~/dev/files` | `q4w8k2.py` | liten VLM (SmolVLM-256M) som kor pa CPU. Relevant om remsan nagonsin ska tolka vad en agent gor visuellt. 104 rader. |
| `~/dev/erlang-exercise` | `car_lights.erl` | en Erlang-process som ar en tillstandsmaskin rod→gron→gul→rod. Ren analogi till remsans farger, inget mer. |

## Tittat pa och lamnat

- `~/dev/brainfuck-interpreter` — inlarningsprojekt, Python-tolk pa 50 rader.
  Ingen sprakmotor. Principen "en instruktion i taget" ar det enda som bar.
- `~/dev/sumerian-grammar-ticks` — krympt till en README pa 20 rader, kallar
  sig sjalvt "onodigt sprakprojekt". Enda iden vard att minnas: determinativ
  markerar klass, inte ljud — en symbol som taggar kategori istallet for att
  stava ut ett ord.
- `~/dev/hello-sound` — noll kodrader, en avsiktsforklaring fran juni.
- `~/dev/recursion-and-backpropegration` — 55 rader Common Lisp, en neuron.
  Bara tematisk koppling: langsam, stegvis berakning.
- `~/dev/BEAM-erlang` — rebar3-skal dar alla funktioner kastar `not_implemented`.
- `~/dev/grokbot-inspired-erlang` — noll commits, ingen Erlang-fil trots namnet.
  Konceptet (supervisor-trad + godkannandesteg) lever vidare i grinden istallet.
- `~/dev/poimon.jl` — fork av `kahliburke/Kaimon.jl`, tredjepartskod.

## Regeln

Ett repo flyttar fran "vart att veta om" till "kopplas in" nar det finns en
issue som pekar pa det. Inte forr. Listan far vaxa langsamt.
