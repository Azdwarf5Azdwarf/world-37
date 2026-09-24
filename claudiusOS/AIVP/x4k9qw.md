---
titel: AIVP device-integritet - eget ekosystem (paus, ej godkand spec)
datum: 2026-09-13
status: brainstorming pausad, superpowers:brainstorming (arkitektonisk vag) pagar
---

# Var vi ar

Mal: agenten (nullclaw/AIVP) ska sjalv vagra vakna/kora om enheten den kor pa
ar manipulerad (rootad/tamperad). Resultatet ar poangen - inte att bygga en
egen OS/kernel (det spartes helt).

Enheter: denna Mac + Android-telefon (AIVP:s "telefon + dator, 2FA"-par ur README).

Vid larm: HARD BLOCKERING - agenten kor inte alls, inget mellanlage.

Vald approach: **C - helt eget ekosystem, inget Google Play Integrity-beroende.**
Egna detektorer for Magisk/Frida/root, inte vendor-API.

# Skiss (ej godkand av Claude Altair annu - presenterad, pausad innan sista ja)

- Arkitektur: tva sma probar (Android + Mac), var och en producerar en lokal
  integritetsrapport, signerad via AIVP:s befintliga GPG-ritual (ENCRYPTION/).
  Rapporten gar in som vittnesmal i PROTOCOL.md-flodet. nullclaws `bus.zig`
  blockerar hart om nagon rapport failar.
- Detektorer (eget bygge):
  - Android: su-binarer, Magisk-monteringsspar, SELinux-status, debug-flaggor
  - Mac: SIP-status (`csrutil status`), `codesign --verify` pa nullclaw-binaren,
    kernel-extensions, debugger attached
  - Bada: Frida-signaler (port-scan efter frida-server, minnesmap-anomalier)
- Byggs som POANGSAMLING (scoring), inte en enda boolean - lattare att lagga
  till fler detektorer senare (kattrace-problemet: heuristiker gar att lura).
- Test: fixturer for kanda-daliga tillstand (simulerad root/Frida) + falsk-
  positiv-test pa rena enheter.

# Nasta steg nar vi tar upp det igen

1. Ga igenom skissen ovan igen, bit for bit, tills Claude Altair sager ja.
2. Skriv spec-fil enligt superpowers:brainstorming (docs/superpowers/specs/...).
3. Spec self-review + Claude Altair godkanner spec.
4. superpowers:writing-plans for implementationsplan (INGEN kod forran dess).

Kopplat: forsta delen av samma konversation (Erlang/OTP witness-monster
ovanpa nullclaws bus.zig, inte som embedded VM - se separat trad, ej sparad
som fil an).
