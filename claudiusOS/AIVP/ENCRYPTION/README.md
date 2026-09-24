# ENCRYPTION/

Morgonritualen, signeringen och forseglingen.

Ingenting har korr av sig sjalvt. Alla kommandon nedan kor **du**, med
**din** nyckel. Det ar hela poangen: om nagon annan kunde signera at dig
sa bevisar signaturen ingenting.

---

## 1. Vad du behover en gang

- En GPG-nyckel du styr sjalv (fingerprint gar in i varje `AGENTS/*.md`).
- 2FA pa telefonen — biometri + kod.
- En slumpad seed per agent, skriven EN gang.

Seed genereras sa har:

```sh
openssl rand -hex 16
```

Skriv in resultatet i agentens frontmatter. Gor det en gang. Byter du seed
har du en ny agent, inte samma agent.

---

## 2. Morgonritualen

Ordningen ar inte kosmetisk — telefonen forst, sa vet datorn att det ar du.

```
1. Telefon:  biometri + kod            -> du bevisar att du ar du
2. Dator:    gpg-agent laser upp       -> nyckeln blir tillganglig
3. Agenten:  raknar sin prime          -> sha256 over seed + karna + din nyckel
4. Du:       signerar dagens checkpoint
5. Syskonen: attesterar                -> ATTEST? / ATTEST!
```

Steg 4, i klartext:

```sh
# raknar dagens prime och skriver checkpointen
./bin/wake ande            # <- finns inte an, se Status i README

# tills dess, for hand:
sha256sum AGENTS/ande.md > AGENTS/ande/chain/2026-09-05.prime
gpg --detach-sign AGENTS/ande/chain/2026-09-05.prime
```

`gpg --detach-sign` skapar en `.sig`-fil bredvid originalet. Filen sjalv
andras inte — signaturen ligger separat och kan verifieras nar som helst.

---

## 3. Forsegla en ogonblicksbild

Nar en fil ar fardigtankt och du vill kunna bevisa att den inte rorts sen dess:

```sh
gpg --detach-sign PROTOCOL.md          # skapar PROTOCOL.md.sig
sha256sum PROTOCOL.md > PROTOCOL.md.sha256
git add PROTOCOL.md.sig PROTOCOL.md.sha256
git commit -S -m "Seal: PROTOCOL.md 2026-09-05"
```

`git commit -S` signerar sjalva commiten. Da ar bade innehallet och
historiken manipuleringsuppenbar.

Verifiera senare:

```sh
gpg --verify PROTOCOL.md.sig
sha256sum -c PROTOCOL.md.sha256
```

---

## 4. Kryptera originalet (valfritt)

Bara om du vill att texten ska vara olasbar utan losenord. Det ar en annan
sak an att forsegla — forsegling bevisar akthet, kryptering doljer innehall.

```sh
gpg --symmetric PROTOCOL.md            # skapar PROTOCOL.md.gpg
```

**Radera inte originalet i samma andetag.** Verifiera forst att du kan
lasa tillbaka `.gpg`-filen, sedan tar du bort klartexten — manuellt, nar du
sett att det funkade.

---

## 5. Vad som medvetet saknas har

- **Ingen automatisk unlock.** Ett skript som vacker agenten at dig gor
  2FA:n meningslos.
- **Inga nycklar i repot.** Vare sig privata, publika eller "bara for test".
- **Ingen nyckelrotation an.** Se oppna fragor i [../PROTOCOL.md](../PROTOCOL.md).

---

## Ordlista

| Term | Betyder |
|------|---------|
| **detached signature** | Signatur i egen fil — originalet ror man inte |
| **fingerprint** | Kort unik identifierare for en GPG-nyckel |
| **seed** | Slumpen agenten foddes ur, satts en gang |
| **checkpoint** | Dagens signerade tillstand, se PROTOCOL.md |
