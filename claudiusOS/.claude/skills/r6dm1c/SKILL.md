---
name: nerves-qemu
description: Använd för bygg- och körloopen i claudiusOS huvudspår — "bygg firmware", "kör i QEMU", "det bootar inte", "installera toolchain", "bränn kortet", eller när ett mix nerves-kommando ger fel. Håller kommandokedjan, triagerar de vanliga miljöfelen, och frågar ALLTID innan mix firmware.burn.
---

# nerves-qemu — bygg, kör, triagera

## Varför den finns

Miljöstrul äter sessioner. En saknad `fwup` eller fel `MIX_TARGET` ser ut
som ett projektfel men är en enrads-fix, och letandet kostar hela dagen som
skulle gått till OS:et. Skillen håller kedjan så att felet blir *ett steg*
i stället för en utredning.

## Kedjan

Engångs, se `README.md`:

```bash
brew install erlang elixir fwup squashfs coreutils xz pkg-config
mix archive.install hex nerves_bootstrap
```

Nytt projekt:

```bash
mix nerves.new blinky --target rpi4
```

Bygga och köra:

```bash
export MIX_TARGET=rpi4      # eller: host, för att köra på Mac
mix deps.get
mix firmware
```

QEMU först. Alltid — det är regeln i `README.md`, inte en åsikt.

## Innan mix firmware.burn — fråga

`mix firmware.burn` skriver till ett fysiskt kort och är **oåterkalleligt**.
Kör det aldrig självmant. Ställ EN fråga: vilken enhet, och är kortet rätt?
Kör `diskutil list` och visa raden, så han ser vad som skrivs över.

Svarar han inte tydligt ja: gör ingenting.

## Vanliga fel → fix

| Symptom | Trolig orsak |
|---|---|
| `command not found: mix` | Elixir inte installerat, eller inte i PATH |
| `Nerves.Env: no target` | `MIX_TARGET` inte satt i det skalet |
| `fwup: not found` | `brew install fwup` |
| bygget hänger på `nerves_system_*` | första bygget hämtar en toolchain — det tar lång tid, avbryt inte |
| `no such file or directory` på `.fw` | fel `MIX_TARGET` mellan `firmware` och `burn` |

Är felet inte i tabellen: läs det faktiska felmeddelandet, gissa inte, och
föreslå ett steg i taget.

## tmux

Första bygget hämtar en hel toolchain och tar lång tid. Påminn om att köra
det i **tmux (terminalmultiplexer / terminal multiplexer)** så det överlever
att fönstret stängs:

```bash
tmux new -s fw 'mix firmware'
```

## Gör inte

- Föreslå inte Elixir som språk för applikationskoden. Erlang är låst.
  Elixirs `mix` är bara byggverktyget i Nerves — det är hela dess roll här.
- Byt inte till GRiSP på eget bevåg. Det är alternativet i `q4m8t2.md`
  *om* Linux-lagret stör, och det är hans beslut.
