#!/bin/sh
# m2vq7k — boot-röktest: k3p7wq.img ska nå iex-prompten på seriell konsol.
# Mezzanos steg 2. Verifierad 2026-08-29: prompten nås efter ~32 s.
# Bootar den inte: skillen r6dm1c triagerar felen. `timeout` finns inte på
# denna maskin — gtimeout kommer från coreutils.
set -e
cd "$(dirname "$0")"

IMG=../k3p7wq/k3p7wq.img
LOG=${LOG:-/tmp/k3p7wq-boot.log}
WAIT=${WAIT:-180}
# Erlang distribution startas inte automatiskt (se mix.exs), sa noden
# ar onamngiven: prompten blir iex(1)> och inte iex(k3p7wq@...)1>.
PROMPT='iex('

[ -f "$IMG" ] || { echo "saknar $IMG — kör 'mix firmware' först"; exit 2; }
command -v gtimeout >/dev/null || { echo "gtimeout saknas: brew install coreutils"; exit 2; }

: > "$LOG"
gtimeout "$WAIT" qemu-system-x86_64 -m 1024 \
  -drive file="$IMG",format=raw,if=virtio \
  -serial stdio -display none > "$LOG" 2>&1 &
QEMU=$!

i=0
while [ "$i" -lt "$WAIT" ]; do
  if grep -q "$PROMPT" "$LOG"; then
    kill "$QEMU" 2>/dev/null || true
    echo "BOOT OK — $PROMPT nådd efter ${i}s"
    exit 0
  fi
  kill -0 "$QEMU" 2>/dev/null || break
  sleep 1
  i=$((i + 1))
done

kill "$QEMU" 2>/dev/null || true
echo "BOOT MISSLYCKADES — ingen prompt inom ${WAIT}s. Logg: $LOG"
tail -30 "$LOG"
exit 1
