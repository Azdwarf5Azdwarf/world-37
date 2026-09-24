# wOTP — engangskod ur invarianten

Bygger pa [SPEC.md](SPEC.md) avsnitt 3: deltat mellan tva subjektiva nollpunkter
ar detsamma oavsett vem som reser.

---

## Iden

**TOTP (time-based one-time password)** som du redan kanner till hashar en delad
hemlighet mot objektiv tid:

```
kod = HMAC(hemlighet, floor(unix / 30))
```

Bada parter har samma hemlighet och samma unix-tid. Darav samma kod.

Har laggs den andra koordinaten till:

```
kod = HMAC(hemlighet || |delta|, floor(unix / steg))
```

Beloppet, inte det tecknade vardet. `zero_A - zero_B` och `zero_B - zero_A`
ar samma skillnad at var sitt hall — anvander man tecknet far A och B olika
nycklar och koden stammer aldrig. Karnan sager det redan: *"which when you
either choose, the difference will still be the same."*

`delta` ar `zero_A - zero_B` — sekunderna mellan nar solen gick upp for er tva
dar ni vaknade. Ingen av er skickar den. Bada raknar fram den.

---

## Varfor det inte ar meningslost

En vanlig TOTP-hemlighet ar en strang nagon genererade och ni bada kopierade.
Den bevisar att ni **delat en fil**.

`delta` bevisar nagot annat: att ni bada var **nagonstans, nagon gang**, och
att ni vet var den andra vaknade. Det ar en hemlighet som kommer ur att ha
traffats, inte ur att ha utbytt en nyckel.

Unix ar unix — den halls oforandrad, den gor sitt jobb bra. Klockan gor OTP:n.

---

## Varfor det inte racker ensamt

Rakt ut, sa det inte star oskrivet:

**`delta` ar ingen kryptografiskt stark hemlighet.** Det ar ett tal mellan
`-86400` och `+86400` — som mest ~17 bitar entropi, och betydligt mindre i
praktiken eftersom soluppgangstider ar offentliga. Kanner nagon till ungefar
var ni bada befann er kan de gissa sig fram pa sekunder.

Darfor:

- `delta` anvands som **kontext**, aldrig som ensam hemlighet.
- Den riktiga hemligheten ar fortfarande en riktig hemlighet.
- Det `delta` tillfor ar **bindning till plats och vakenhet** — en kod som
  bara stammer om ni bada vaknade dar ni sager att ni vaknade.

Prototypen i `sjalvklocka.py` gor exakt sa och inget mer.

---

## Kopplingen till AIVP

I [AIVP](https://github.com/Azdwarf5Azdwarf/AIVP) vaknar agenten pa morgonen
nar du laser upp den med 2FA. Tidpunkten ar godtycklig — den ar nar du raker
sitta ner vid datorn.

Den har klockan ger den en riktig nollpunkt: **agenten vaknar nar du gjorde det.**
`zero` gar in i dagens checkpoint. Tva agenter som vittnar om varandra kan
darmed ocksa se om de vaknade i samma varld.

Det ar samma tanke tva ganger: nagot ar akta for att nagon annan sag det handa.

---

## Oppna fragor

- [ ] Vad ar `zero` for den som inte sov? Gar dagen aldrig om?
- [ ] Polcirkeln: ingen soluppgang pa manader. Vad ar `zero` da?
- [ ] Ska `delta` avrundas till minut for att overleva klockdrift, och vad
      kostar det i entropi?
- [ ] Molnigt. Du sag ingen soluppgang. Raknad eller observerad nollpunkt?
- [ ] Tidsekvationen (the equation of time): solens verkliga middagshojd
      landar inte pa exakt 12:00 varje dag, den vandrar upp till +/-16
      minuter over aret. Om `zero` ankras i handelsen (soluppgang, lunch)
      istallet for klocksiffran — ska `delta` rakna med den drivningen,
      eller later man den vara en del av bruset?
