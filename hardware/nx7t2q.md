---
title: armband-hardware (tick-speak/vibrationsspråk)
date: 2026-09-13
tags: [hardware, tick-speak, armband]
---

Skiljer sig fran roboten (kamera+hogtalare, se [[fn8frw]]) -- det har ar
armbandet/vibrations-kanalen, tva separata enheter.

## Hittat pa Kjell & Company (2026-09-13, kopbart nu, ingen lodning)

- **Arduino Nano ESP32** -- art.nr 88444, 239 kr (outlet 204 kr). ESP32-S3
  dual-core, wifi + BT5, 16 MB flash / 8 MB PSRAM. Arduino IDE + MicroPython.
- **Arduino Modulino Vibro** -- art.nr 88447, 129 kr. Vibrationsmodul med
  haptisk feedback, Qwiic-kontakt (plug-and-play, ingen lodning eller
  kopplingsdack), PWM-styrd intensitet, **kedjebar med fler Modulino-noder**
  -- dvs flera vibrationspunkter pa samma buss, gratis pa kopet for
  tva-kanal-designen nedan.

Ersatter DRV2605L+lös LRA-motor helt -- Modulino Vibro ar redan
driver+motor ihopbyggt i en Qwiic-modul.

## MVP -- en kanal (~370 kr)

1x Nano ESP32 + 1x Modulino Vibro. Bevisar konceptet: dator/telefon
skickar kommando via BLE, modulen vibrerar enligt tick/tock-mönstret fran
`vt3k7m.html`.

## Full version -- tva kanaler (~500 kr)

Nano ESP32 + 2x Modulino Vibro kedjade pa Qwiic-bussen: hoger arm =
konsonanter (tick/tock-klick), vanster hand = vokaler
(vibrationsintensitet/-monster), se [[qyucxq]] ("Konkretisering"). Billigare
och enklare an ursprungsplanen (ingen separat I2C-adressering att losa
sjalv, ingen lodning).

## Firmware

Arduino C++ (eller MicroPython) mot Nano ESP32 -- Modulino-biblioteket ar
fardigt fran Arduino, tar emot BLE-kommandon och styr PWM-intensiteten per
nod pa kedjan.

## OS/stack (langsiktigt, se [[qyucxq]] "Slakting")

Zig som huvudsprak for firmware-lagret (bare-metal, kan mal mot ARM
Cortex-M som dessa kort anvander). Erlang/Lisp/**Nerves** (Elixir-ramverk
for inbyggda Linux-enheter) som OS-lager for orkestrering -- funkar battre
pa storre kort (Raspberry Pi-klass) an pa de har smaskaliga BLE-korten,
sa troligen: Zig direkt pa armbandets mikrokontroller, Nerves pa en
mellanliggande enhet (typ Pi Zero 2 W, redan i [[fn8frw]]s lista) som
pratar BLE at bade armband och robot.

Ingen brådska -- se [[fn8frw]] för samma filosofi.
