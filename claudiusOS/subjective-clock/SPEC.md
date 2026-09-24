# SPEC — klockan med tva koordinater

Karnan star i [KARNAN.md](KARNAN.md), ordagrant. Det har ar vad den sager,
utskrivet.

---

## 1. Problemet

En arab foljer mankalendern. En kines foljer en annan. De trafffas pa samma
plats — och deras kalendrar sager olika saker. Objektiv tid ar inte en tid,
det ar en hog av oense system.

Samtidigt: **solen gick upp**. For bada. Pa olika platser, vid olika ogonblick,
men det handelsen ar densamma. Det ar den enda klockan alla redan har.

---

## 2. De tva koordinaterna

| | **Objektiv** | **Subjektiv** |
|---|---|---|
| Vad | unix-tid, sekunder sen 1970-01-01 UTC | sekunder sen solen gick upp dar du vaknade |
| Vem delar den | alla, overallt, alltid | bara du |
| Andras av resa | nej | ja — men inte direkt |
| Nollpunkt | godtycklig, bestamd av en kommitte | soluppgangen. Ingen bestamde den |

Unix ar unix. Den ar redan universell och behover inte forbattras.
Det som saknas ar den andra koordinaten.

```
subjektiv_tid(t) = t - soluppgang_zero
```

`soluppgang_zero` ar unix-tidsstampeln for soluppgangen **dar du vaknade** —
inte dar du ar nu. Den flyttar sig inte for att du satter dig pa ett flyg.
Den flyttar sig nar du sover.

---

## 3. Invarianten

Det har ar hela poangen, och det ar den som ar ny.

Tva personer, A och B. Var och en har sitt `soluppgang_zero`.

```
delta = zero_A - zero_B
```

Karnan sager det sa har:

> "if the Chinese guy travels to Iraq, based on where he woke up, there will
> still be the same difference. Now if you flip the scenario, the difference
> of the Arabian guy going to China or the Chinese guy going to Arab, which
> when you either choose, the difference will still be the same."

Alltsa: **det spelar ingen roll vem som reser.** Deltat mellan tva subjektiva
nollpunkter ar detsamma i bada riktningarna. Det ar en egenskap hos paret,
inte hos nagon av dem.

Det ar darfor det gar att bygga nagot pa. En storhet som tva parter kan rakna
fram var for sig och komma till samma svar — utan att skicka nagot mellan sig.

---

## 4. Vad det INTE ar

- **Inte en tidszon.** Tidszoner ar politiska och delas av miljoner.
  Ditt `zero` ar ditt.
- **Inte soltid.** Soltid foljer solen kontinuerligt. Det har ar en *handelse*,
  inte en vinkel: solen gick upp, en gang, dar du vaknade.
- **Inte en ny kalender.** Kalendrarna far vara kvar. Det har ligger under dem.
- **Inte jetlag** — men jetlag ar deltat gjort kroppsligt. Karnan noterar det:
  *"Whatever you call jet lag, I have no idea. Jet lag works."*

---

## 5. Vad som foljer

Om deltat ar invariant och privat kan det anvandas som delad hemlighet.
Tva som har traffats vet varandras `zero`. Ingen annan gor det.

Det ar dar [OTP.md](OTP.md) tar vid.
