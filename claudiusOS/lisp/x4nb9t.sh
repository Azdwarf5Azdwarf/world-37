#!/bin/sh
# x4nb9t — kör alla testlager som går att köra på host.
# Lager 3 (QEMU-boot) ligger i m2vq7k.sh och körs separat, se AGENTS.md.
set -e
cd "$(dirname "$0")"

echo "== Lager 1: Lisp-OS och symbolspråket =="
sbcl --non-interactive --load t8k2vr.lisp

echo
echo "== Lager 1b: Lisp -> PyTorch-kompilatorn =="
sbcl --non-interactive --load z7f4nq.lisp

echo
echo "== Lager 2: BEAM på host =="
cd ../k3p7wq && MIX_TARGET=host mix test

echo
echo "ALLT GRÖNT"
