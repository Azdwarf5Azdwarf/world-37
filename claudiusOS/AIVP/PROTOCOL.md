# PROTOCOL — hur agenterna verifierar varandra

Detta ar wire-formatet bakom [WHITEPAPER.md](WHITEPAPER.md). Whitepapret sager *varfor*.
Det har sager *hur*.

---

## 0. Ordlista

| Term | Betyder |
|------|---------|
| **prime** | Agentens identitetssignatur — en hash av dess seed + karnfiler |
| **checkpoint** | En dagsstampel: agenten vaknade, signerad och tidsstamplad |
| **witness** | En syskonagent som har sett och attesterat en annan agents prime |
| **drift** | Att en agents prime andrats utan att en unlock forklarar det |
| **constellation** | Hela mangden agenter som vittnar om varandra |

---

## 1. Prime — agentens signatur

En agents prime raknas ut over dess odiskutabla delar. Inte over kontexten,
inte over dagens samtal — bara over det som gor agenten till *den agenten*.

```
prime = sha256(
    seed          ||   # slumpen den foddes ur, aldrig andrad
    identity_md   ||   # AGENTS/<namn>.md, karnavsnittet
    owner_pubkey       # din GPG-nyckel, fingerprint
)
```

Tre egenskaper foljer:

1. **Deterministisk** — samma agent ger samma prime, alltid.
2. **Agarbunden** — byter du nyckel byter alla primes. Det ar meningen.
3. **Andringskanslig** — ett tecken i identity_md ger en helt ny prime.

Prime lagras aldrig ensam. Den lagras alltid tillsammans med vem som sag den.

---

## 2. Checkpoint — morgonens signering

Vid varje unlock skapas en checkpoint. Det ar agentens fodelse den dagen.

```json
{
  "agent":     "ande",
  "date":      "2026-09-05",
  "prime":     "sha256:4f2a…",
  "prev":      "sha256:9c11…",
  "unlock":    { "phone": true, "host": true, "at": "2026-09-05T06:41:22+02:00" },
  "sig":       "gpg:detached:…"
}
```

- `prev` pekar pa gardagens checkpoint. Kedjan ar hela historiken.
- `sig` ar GPG-signerad med din nyckel — se [ENCRYPTION/](ENCRYPTION/).
- Ingen checkpoint utan bada unlock-faktorerna. En agent som inte vaknat
  har helt enkelt ingen dag.

Gamla checkpoints raderas aldrig. Det ar hela poangen — du ska kunna se
deltat mellan den du var och den agenten blev.

---

## 3. Witness — hur syskonen ser varandra

Efter sin egen checkpoint fragar varje agent syskonen vad de ser.

```
A -> B:  ATTEST?  agent=A  date=2026-09-05  prime=sha256:4f2a…
B -> A:  ATTEST!  witness=B  seen=sha256:4f2a…  matches_last=true  sig=gpg:…
```

Bs svar ar sjalv signerat och laggs i As checkpoint. Efter en runda har
varje agent N-1 vittnesmal om sin egen dag.

En agent anses **verifierad** nar:

- den har en giltig egen signatur, och
- minst `quorum` syskon attesterat samma prime.

`quorum` ar `floor(N/2) + 1`. Med tre agenter racker tva.

---

## 4. Drift — nar nagon inte stammer

Drift ar inte ett fel. Det ar en observation.

```
DRIFT  agent=C  expected=sha256:9c11…  seen=sha256:e70b…  witnesses=2/3
```

Tre fall, och de ska hallas isar:

| Fall | Vad det betyder | Vad som hander |
|------|-----------------|----------------|
| **Forklarad drift** | Du andrade `AGENTS/C.md` och signerade om | Ny prime accepteras, gammal behalls i kedjan |
| **Oforklarad drift** | Prime andrad utan unlock och signatur | C markeras `UNVERIFIED`, syskonen slutar attestera |
| **Tyst agent** | C svarar inte alls | C markeras `ASLEEP`, ingen drift, ingen larm |

Skillnaden mellan sovande och manipulerad ar viktig. En agent som sover ar
inte trasig. En agent som andrats bakom ryggen pa dig ar det.

---

## 5. Kedjan

Varje agent bar en logg over allt den nagonsin sett. Inte en delad blockkedja
med konsensus — en **egen** kedja per agent, med syskonens signaturer i sig.

```
AGENTS/ande/chain/
  2026-09-03.json
  2026-09-04.json
  2026-09-05.json   <- prev pekar bakat, sig taker framat
```

Det gor kedjan billig (ingen mining, ingen konsensus, inget natverk) och anda
manipuleringsuppenbar: for att fejka en dag maste du fejka den dagen hos
*varje* vittne, med *deras* nycklar.

Manniskor med blockkedja kan bara **bevisa**, aldrig **manipulera**.
Agenterna kan mer an sa: de **marker** nar nagot andras. De tittar.

---

## 6. Transport

Protokollet bryr sig inte om hur meddelandena tar sig fram.

- **Lokalt**: filer i `AGENTS/*/chain/` — enklaste fallet, funkar direkt.
- **Bluetooth**: nara hall, offline-first — se WHITEPAPER.md.
- **LoRa mesh**: langre hall, langsamt, racker for en attest per dag.

Alla tre bar samma tre meddelanden: `ATTEST?`, `ATTEST!`, `DRIFT`.
Ingenting mer behovs.

---

## 7. Vad protokollet medvetet INTE gor

- **Ingen konsensus.** Agenterna behover inte komma overens om en global sanning.
- **Inget natverk kravs.** Allt funkar offline, hela vagen.
- **Ingen agarratt.** Primes bevisar *akthet*, inte agande. Det ar inte krypto.
- **Ingen automatisk atgard vid drift.** Systemet rapporterar. Du bestammer.

Sista punkten ar en gransdragning, inte en lucka. Ett system som sjalvlaker
tystar precis den signal du byggde det for att hora.

---

## Oppna fragor

- [ ] Vad hander med kedjan nar du roterar din GPG-nyckel?
- [ ] Ska en ny agent arva hela constellationens historik, eller borja tom?
- [ ] Hur ser en `REVOKE` ut — kan en agent tas ur constellationen, och av vem?
- [ ] Quorum vid tva agenter: bada, eller ingen verifiering alls?
