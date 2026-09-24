---
titel: Hashmarks - sammanslagning av flera projekt (ej klar, pagaende dump)
datum: 2026-09-13
status: pausad mitt i, Claude Altair dumpar mer kontext senare
---

# Var vi ar

Ny overgripande ide: **Hashmark** = en observation (moment + plats/observator +
strukturerad data) kodad som s-uttryck, tidsstämplad, kryptografiskt ankrad
(BLAKE3 + YubiKey namndes), verifierbar/komponerbar av andra agenter/personer.

Kom fran Haiku-4.5-prompts Claude Altair klistrade in - han slar ihop flera egna
projekt under detta paraply:

- **ai-lisp-erlang** - distribuerade agenter (manniska+AI) som pratar via meddelanden
- **numbers-to-geometry** - observationer som s-uttryck (triangel, sats-om-sinus)
- **9i/tech-kami** - moment ankrade i rumtid + kryptografiskt bevis. "9i" =
  ljusfordrojning som komplext tal (imaginardelen ar fordrojningen). Kochab-
  observation 11 september namnd som mojligt forsta konkreta exempel.
- **veridoc** - rost -> blockchain -> fax (fanga observation -> bevis -> leverans)
- **nullclaw** - agent som organiserar/koordinerar observationer
- **brain-force** - metodik for kollaborativ problemlosning, multi-agent-konvergens

# Kopplingen till AIVP + subjective-clock (redan bekraftad i konversationen)

`~/dev/subjective-clock` (STJARNZERO.md) och AIVP:s vittnesprotokoll (PROTOCOL.md)
ar redan samma monster i miniatyr:
- stjarnzero = (ogonblick, plats, hogsta stjarnan, signatur) ovanpa en riktig hemlighet
- AIVP-vittne = (ogonblick, agent, meddelande, signatur)
Bada ar Hashmarks i praktiken, bara olika domaner.

Loser ocksa en oppen fraga i STJARNZERO.md ("en agent per stjarna, kollision?"):
tva som delar samma stjarna/ogonblick ar INTE en kollision - det ar bevis pa
delad narvaro.

# Faktacheck gjord under samtalet (håll kvar dessa)

- **GPS ger position+tid i samma losning** (klockbias ar en av de 4 okanda) -
  stammer, sa fungerar riktiga stratum-1 NTP-servrar. Bra som Hashmark-tidskalla.
- MEN: civil GPS-signal ar OSIGNERAD -> spoofbar. Duger som kontext for
  Hashmarks i allmanhet, INTE som sakerhetsankare i AIVP:s vittnes-/
  integritetslager (samma regel som stjarnzero: kontext ovanpa hemlighet,
  aldrig i stallet for den).
- Claude Altairs observationsmetod just nu (ogon + AR/VR-app) ar samma kategori:
  en kalla, oforankrad, ej dubbelkollad. OK som inspiration, inte som bevis.
  Han sjalv flaggade ratt: uppfinn inte egna namn/"monster" runt en
  oforankrad observation som om den vore faststalld.

# Ihopkopplat men separat fran

Enhets-integritet/anti-manipulation-tradet (Magisk/Frida, eget ekosystem,
hard blockering) ar en ANNAN pausad trad - se `x4k9qw.md` i samma repo.
Samma AIVP-projekt, olika grenar.

# Extra ankare-ide (Claude Altair, kul-lage): Starlink

Han ser Starlink-satelliter i sina VR/AR-appar och vill lagga till dem som
extra ankare. Fyndigt varfor: en Starlink-passage syns bara i en snav
tvaminuters-vinkel (satelliten rusar over himlen), medan "hogsta stjarnan"
(stjarnzero) star kvar over huvudet i typ 30-60 minuter. Att identifiera
VILKEN satellit man sag ger darfor mycket skarpare TID-upplosning an en
stjarna - nastan som GPS: publikt berakningsbara banor (TLE-data), position+
tid i en och samma observation. Samma regel galler dock: kul extra kontext-
ankare for Hashmarks, INTE en sakerhetsankare (vem som helst med TLE-data
kan pasta sig ha sett en passage utan att faktiskt ha gjort det).

# Konkret exempel-schema (Claude Altair, ej klart, mer personligt spar)

Skiss pa hur en Hashmark-post konkret kan se ut (person 2 gor X i det
ogonblicket, stjarnzero = Y, narmaste Starlink = Z, tid = unix O):

```
(hashmark
  (person  <vem>)
  (handling <X>)
  (unix    <O>)
  (stjarnzero <Y>)
  (starlink-narmast <Z>)
)
```

Inte exakt sa an - "nagot liknande" enligt honom sjalv, forma inte om det till
nagot mer faststallt an sa.

**Bekraftat: ja, det finns oppna API:er for bada halvorna, ingen ny
infrastruktur behovs:**
- Stjarnpositioner: samma oppna katalogdata som `stjarnor.py`/`sjalvklocka.py`
  i subjective-clock redan raknar pa - gratis, ingen nyckel.
- Starlink-position: Celestrak publicerar TLE-data (bandata) for hela
  Starlink-flottan gratis och oppet - ingen inloggning, ingen Google-typ
  gatekeeper. Matchar samma "eget ekosystem, inget vendor-beroende"-onskan
  som device-integritets-tradet (x4k9qw.md) redan valde.

# Karnan ur Untitled 1.md (resten lamnad ororda dar, se not nedan)

Gammal AI-dialog i `~/claudius-journeys/Untitled 1.md` eskalerade till
oforankrad numerologi ("37 = the nothing point", "prime 57 for att
universum valde det", "identitet utan losenord - systemet vet redan vem
du ar"). Den delen ar INTE tagen med har - skonlitteratur, inte teknik,
lamnad orord i sin fil.

En sak dar var dock ratt och saknades i schemat ovan: en Hashmark bevisar
just nu NAR (unix) och VAR (stjarnzero/Starlink), men inte VEM med nagot
verkligt. Fixen ar inte "fake-time entropy-signatur" - det ar bara det
AIVP redan har: en riktig kryptografisk signatur (GPG/YubiKey via
ENCRYPTION/-ritualen). Uppdaterat schema:

```
(hashmark
  (person   <vem>)
  (handling <X>)
  (unix     <O>)
  (stjarnzero <Y>)
  (starlink-narmast <Z>)
  (signatur <riktig GPG/YubiKey-signatur, inte en "kansla" om ett tal>)
)
```

# Status / nasta steg

INTE klar - Claude Altair sa "inte klart an", mer kontext kommer. Skapa ingen spec
eller plan forran han sager att dumpen ar klar. Redan nu klart: 6+ projekt
(ai-lisp-erlang, numbers-to-geometry, 9i/tech-kami, veridoc, nullclaw,
brain-force) + AIVP + subjective-clock ar for manga for en (1) spec -
maste delas upp per superpowers:brainstorming nar han ar redo att bygga
nagot av det har.
