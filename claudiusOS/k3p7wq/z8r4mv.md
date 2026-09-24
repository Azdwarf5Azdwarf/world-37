---
title: k3p7wq — var jag var
date: 2026-08-29
---

Nerves-projektet i claudiusOS huvudspår. Elixir är bara skalet — det som
körs är BEAM.

## Läge

- Target: `x86_64`. Deps hämtade, `mix firmware` kört.
- `k3p7wq.img` finns, 785 MB, byggd 2026-08-29 11:20.
- **Bootad 2026-08-29.** Nerves-banner och `iex(1)>` efter ~32 s i QEMU.

## Kör den

```bash
cd k3p7wq
export MIX_TARGET=x86_64
qemu-system-x86_64 -m 1024 -drive file=k3p7wq.img,format=raw,if=virtio \
  -serial mon:stdio -display none
```

Väntat: kernel-loggar, Nerves-banner, sedan `iex(1)>`. Noden är
onamngiven — Erlang distribution startas inte automatiskt (`mix.exs`).
Avsluta QEMU: Ctrl-A, sedan X.

Automatiserat röktest från repo-roten: `sh m2vq7k.sh`.

Bootar den inte: skillen `r6dm1c` (nerves-qemu) triagerar de vanliga felen.

## Rör inte

`_build/` och `deps/` är genererade. `mix firmware.burn` skriver till fysisk
disk — kör inte utan att kontrollera målenheten först.
