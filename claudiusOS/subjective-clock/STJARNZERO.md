# STJARNZERO — den tredje koordinaten

Inget teleskop behovs. Himlen ar **berakningsbar (computable)**.

Stjarnornas positioner ligger i katalog sedan lange. Att veta vad som stod
over ditt huvud kraver bara latitud, longitud och tid — samma tre saker
soluppgangen redan behovde.

---

## Vad det ar

```
stjarnzero = den katalogstjarna som stod hogst over dig
             i ogonblicket du vaknade
```

Ogonblicket ar `zero` fran [SPEC.md](SPEC.md) — soluppgangen dar du vaknade.
Att solen samtidigt slog ut synligheten spelar ingen roll. **Stjarnan stod dar.**
Det ar inte en fraga om vad du sag.

```sh
./sjalvklocka.py stjarna 33.31 44.36
```

```
nollpunkt:   2026-09-05 02:40:27Z
stjarnzero:  Elnath
             78.0 grader over horisonten, azimut 109.7
             magnitud 1.65
bindning:    Elnath@78
```

---

## Varfor det loser polcirkeln

Den oppna fragan i [OTP.md](OTP.md) var: vad ar `zero` nar solen inte gar upp
pa manader?

Stjarnorna slutar aldrig. Kiruna i januari, mitt i polarnatten:

```
Dubhe, 70.4 grader over horisonten
```

Solen kan utebli. Himlen gor det inte.

---

## Katalogen

De ~45 ljusstarkaste stjarnorna, J2000, i `stjarnor.py`. Rektascension och
deklination i grader.

Egenrorelse ar utelamnad — den flyttar stjarnorna brakdelar av en bagminut
per ar, vilket inte betyder nagot nar hojden anda avrundas till hel grad.

Verifierat mot tva kanda fall:

| Kontroll | Vantat | Fatt |
|---|---|---|
| Polaris hojd fran lat 59.33 | ~59.3 (+0.74 grader polavstand) | 60.00 |
| Sirius kulmination fran Stockholm | 13.9 grader, azimut ~180 | 14.0, azimut 180.7 |

---

## I OTP:n

```sh
./sjalvklocka.py otp 33.31 44.36 39.90 116.40 --hemlighet ~/.hemlig --stjarna
```

Bada parternas bindningar gar in, **sorterade**:

```
nyckel = hemlighet || |delta| || min(b_A, b_B) || max(b_A, b_B)
```

Sorteringen ar samma sak som `abs()` runt deltat, en niva upp. Utan den far
A och B olika nycklar beroende pa vem som star forst i anropet, och koden
stammer aldrig.

**Samma forbehall som forut:** stjarnzero ar berakningsbar av vem som helst
som kanner din position och tid. Den ar **kontext, inte hemlighet**. Vad den
tillfor ar bindning till en plats pa jorden och ett ogonblick i himlen —
ovanpa en riktig hemlighet, aldrig i stallet for en.

---

## Oppna fragor

- [ ] Vid hojd nara ett gradskifte kan avrundningen tippa at olika hall for
      tva narliggande positioner. Bredare korg, eller acceptera missar?
- [ ] Ska magnituden vaga in — hogsta stjarnan, eller ljusaste over en viss hojd?
- [ ] En agent per stjarna: vad hander nar tva agenter valjer samma?
