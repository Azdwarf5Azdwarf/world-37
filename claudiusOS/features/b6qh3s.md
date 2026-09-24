# Läge: Lisp -> PyTorch-kompilatorn (2026-08-29, kväll)

Filen är `z7f4nq.lisp` i roten. Kör:

    sbcl --non-interactive --load z7f4nq.lisp

Grönt betyder 15/15 självtest + `build/tiny_net.py` och
`build/mythos_small.py` skrivna. `build/` är gitignorerad.

## Klart

- Frontend: DSL -> tensor-IR (mellanrepresentation) med härledda
  dimensioner. `(linear 128)` räcker, indimensionen bärs framåt.
- Ops: `input linear embedding attention layernorm dropout relu gelu
  tanh sigmoid softmax residual repeat`.
- Backend: IR -> PyTorch som satser i `forward`, inte `Sequential` —
  därför fungerar residual och tuppel-uppackningen från
  `MultiheadAttention`.
- Felen fastnar i IR:n: ojämna attention-huvuden, residual som ändrar
  dimension, op före `input`, okänd op.

## Fel i `features/y8g9e5.md` som inte togs vidare

- `#:data`, `set!`, `(loop n ...)` är Racket/Scheme — varken Common Lisp
  eller LFE. Exemplen i dokumentet kompilerar inte som de står.
- Dokumentet hoppar över formhärledning (shape inference); det är just
  det IR-steget gör.
- `attention` listas som primitiv op i steg 1 — den har egna vikter och
  hör till senare.

## Nästa steg (välj ett)

1. `train`-form i DSL:en: optimerare, loss, epoker -> genererad
   träningsloop.
2. Ingen torch installerad på maskinen — bara `py_compile` har verifierat
   utdatan. Installera torch och kör ett riktigt framåtpass.
3. Koppla kompilatorn till BEAM-spåret: modellen som övervakad port.
