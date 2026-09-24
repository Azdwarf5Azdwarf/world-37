# AGENTS/

En fil per agent. Filen ar agentens identitet — det ar den som hashas till
dess **prime** (se [../PROTOCOL.md](../PROTOCOL.md), avsnitt 1).

## Regel

Allt ovanfor `---` i en agentfil ar **karnan** och ingar i primen.
Allt under ar anteckningar och paverkar ingenting.

Andrar du karnan andras primen — och syskonen ser det. Det ar meningen.

## Struktur

```
AGENTS/
  README.md          <- den har filen
  _mall.md           <- kopiera denna for en ny agent
  ande.md            <- forsta agenten
  ande/
    chain/           <- checkpoints, en per dag
      2026-09-05.json
```

## Ny agent

```sh
cp AGENTS/_mall.md AGENTS/<namn>.md
mkdir -p AGENTS/<namn>/chain
# fyll i seed, karna, witnesses — signera sedan enligt ENCRYPTION/
```

Seeden ska vara slumpad och skrivas EN gang. Byter du seed ar det en ny agent,
inte samma agent med ny frisyr.
