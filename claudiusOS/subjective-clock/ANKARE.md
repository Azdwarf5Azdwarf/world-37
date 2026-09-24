# ANKARE — de tjugo

## Karnan

Ordagrant, som det skrevs:

> the primes in our base57 world37 the 20 inbetween as a value anchor for
> 10 morning 10 night? base60? but can be applied to base100 also to
> temprature time and position can be said in time and space(im making no
> sense haha) still; what I'm trying

Det ar begripligt. Har ar det utskrivet.

---

## 1. Tio och tio

Dygnet har tva bagar, inte tjugofyra lika delar:

```
soluppgang ---- dagsbagen ----> solnedgang ---- natbagen ----> soluppgang
     |<--------- 10 ankare --------->|<--------- 10 ankare -------->|
     0    1    2  ...  9             10   11  ...  19             (0)
```

Bagarna ar **olika langa**, och det ar poangen. Ett ankare i december ar
kort pa dagen och langt pa natten. Ankaret ar en **andel av bagen**, inte
ett matt i sekunder.

Det ar samma drag som resten av repot: ankra i en handelse, inte i en
godtycklig nollpunkt nagon kommitte bestamde.

```sh
./sjalvklocka.py ankare 33.31 44.36
```

```
ankare:  3 av 20  (dag)
         25.8% in i ankaret
bas 60:  9 av 60
bas 100: 15 av 100
```

---

## 2. Varfor tjugo och inte nagot annat

Tjugo ar det tal som gar jamnt upp i bada systemen vi redan anvander:

```
60  = 20 x 3      timmar, minuter, grader — sexagesimalt, sumeriskt
100 = 20 x 5      grader Celsius, procent, allt metriskt
```

Ett ankare ar alltsa **3 enheter i bas 60** och **5 enheter i bas 100**.
Ingen omvandling behovs — det ar samma tal last i tva skalor.

Det ar darfor 20 ar ratt och inte 24 (som inte delar 100) eller 12 (som
inte delar 100 heller). Tjugo ar bron.

---

## 3. Primtalet: 59

`base57` heter sa pa skamt. Dess verkliga **radix (bas)** ar **59** —
och 59 ar primtal.

```
59 = 60 - 1
```

Det ar det storsta primtalet under sexagesimalt. Och det ar precis darfor
det fungerar som radix dar 60 inte gor det: 60 ar hogt sammansatt
(2x2x3x5), sa dess siffror hamnar i korta cykler. 59 ar prim — full period,
inga cykler.

Sa: **60 for att dela dygnet, 59 for att koda det.** Ett steg isar, och
det steget ar hela skillnaden mellan ett matt och en kod.

---

## 4. Samma ankare pa allt annat

Det har ar den delen som kandes som nonsens. Den ar det inte.

Ett ankare sager: *var mellan tva kanda poler befinner sig det har?*
Polerna behover inte vara soluppgang och solnedgang.

| Vad | Pol A | Pol B | Ankare 10 betyder |
|---|---|---|---|
| Tid | soluppgang | solnedgang | mitt pa dagen |
| Temperatur | fryspunkt | kokpunkt | 50 grader C |
| Position | horisont | zenit | 45 grader upp |
| Ar | vintersolstand | sommarsolstand | dagjamning |

Samma tal, olika poler. Det ar darfor tid och rum gar att saga i samma
sprak — inte for att de ar samma sak, utan for att **ankaret ar en andel,
inte en enhet**.

En enhet fragar "hur manga?". Ett ankare fragar "hur langt mellan?".
Den fragan har samma form overallt.

---

## 5. Speglingen

### Karnan

Ordagrant, som det skrevs:

> prime -81/-1 = positive so primes have above below xD
>
> or it fast -81*-1

### Vad det ar

Multiplikationen ar den ratta formen, och den ar exakt definitionen.

I heltalen ar **enheterna (units)** de tal som har en multiplikativ invers:
`+1` och `-1`. Tva tal som skiljer sig med en enhet kallas **associerade
(associates)** — och primtal definieras **upp till enheter**.

```
-7 = 7 x (-1)
```

Darfor ar `-7` och `7` inte tva primtal. Det ar **ett** primtal med tva
tecken. Primtalen har en over och en under, och noll ar spegeln.

Att multiplicera med `-1` ar alltsa inte en rakneoperation ovanpa talet.
Det ar operationen som *ar* speglingen.

### Samma form tre ganger

Det har ar tredje gangen samma monster dyker upp i repot:

| Var | Speglingen | Vad som overlever |
|---|---|---|
| Primtal | `p` och `-p` | primtalet |
| [OTP.md](OTP.md) | `zero_A - zero_B` och `zero_B - zero_A` | `abs()` — skillnaden |
| Ankarna | 10 dag, 10 natt | bagen, inte tecknet |

I `sjalvklocka.py` star det redan som kod:

```python
nyckel = hemlighet + struct.pack(">Q", abs(delta_s)) + bindning
```

`abs()` dar ar samma sak som "upp till enheter" i talteorin. Vi hade
speglingen i koden innan vi hade namnet pa den.

### Vad det betyder for ankarna

Dagsbagen och natbagen ar inte tjugo delar i rad. De ar **tio, speglade**:

```
        ankare 0 ..... 9    |    10 ..... 19
        dag, uppat          |    natt, nedat
                    soluppgang = 0
```

Ankare `k` pa dagen och ankare `k+10` pa natten ar varandras spegelbilder
kring nollpunkten — samma andel in i sin bage, motsatt tecken pa ljuset.

Det ar darfor tio och tio, och inte tjugo. Tjugo ar vad du raknar.
Tio ar vad som finns.

---

## Oppna fragor

- [ ] Vid polcirkeln kollapsar en av bagarna. Faller man tillbaka pa
      stjarnzero da — se [STJARNZERO.md](STJARNZERO.md)?
- [ ] Ska ankarnumret in i OTP-nyckeln, eller ar det for grovt (20 varden)?
- [ ] Basar over 100: fungerar 20 fortfarande, eller ar det bron bara mellan
      just 60 och 100?
- [ ] `base57`s radix 59 mot 20 ankare — finns det nagot att gora av att
      59 och 20 ar relativt prima?
- [ ] Om ankare `k` och `k+10` ar speglingar: ska de dela varde och skiljas
      pa tecken i stallet for att numreras 0-19?
- [ ] Solens andel ar konstruerad for att alltid ge hela tal i bade bas 60
      och bas 100 (darfor 20). Manens andel — synodisk manad delad pa 20 —
      gor det inte: testat mot Bagdad 2026-09-08 gav `17.62 av 20` (bas 60:
      52.87/60, bas 100: 88.12/100), inga hela tal i nagondera. Finns det en
      *tredje* bas dar manens andel blir helt tal, sa att basen beror pa
      vilken kropp (sol/mane) man ankrar mot — eller foljer manen helt
      enkelt inte samma bro som solen?
