# subjective-clock

Solen gick upp. Det ar den enda klockan alla redan har.

En arab och en kines trafffas. De foljer olika kalendrar — men bada vaknade
nar solen gick upp dar de var. Skillnaden mellan de tva ogonblicken ar
**densamma oavsett vem av dem som reste**.

Den skillnaden gar att rakna fram av bada, var for sig, utan att skicka nagot.

## Tva koordinater

| | Objektiv | Subjektiv |
|---|---|---|
| unix-tid | delas av alla | — |
| soluppgang dar du vaknade | — | bara din |

Unix ar unix. Den gor sitt jobb bra och ror man inte. Det som saknades var
den andra koordinaten.

## Las i den har ordningen

| Fil | Vad |
|-----|-----|
| [KARNAN.md](KARNAN.md) | Ratexten. Tre roestinspelningar, 3 sep 2026. Ordagrant. |
| [SPEC.md](SPEC.md) | De tva koordinaterna och invarianten, utskrivet. |
| [OTP.md](OTP.md) | Engangskoden — och varfor deltat inte racker ensamt. |
| [ANKARE.md](ANKARE.md) | De tjugo ankarna: 10 dag, 10 natt. Bron mellan bas 60 och bas 100. |
| [STJARNZERO.md](STJARNZERO.md) | Den tredje koordinaten. Inget teleskop behovs. |
| [sjalvklocka.py](sjalvklocka.py) | Korande prototyp. Inga beroenden. |
| [stjarnor.py](stjarnor.py) | Stjarnkatalogen och himmelsmatematiken. |

## Prova

```sh
./sjalvklocka.py nu    33.31 44.36                 # Bagdad
./sjalvklocka.py delta 33.31 44.36  39.90 116.40   # Bagdad <-> Peking
./sjalvklocka.py ankare  33.31 44.36               # var i dygnet, av 20
./sjalvklocka.py stjarna 33.31 44.36               # vem stod over dig
./sjalvklocka.py otp   33.31 44.36  39.90 116.40 --hemlighet ~/.hemlig --stjarna
```

## Sagt rakt ut

`delta` ar **ingen stark hemlighet** — som mest ~17 bitar, och
soluppgangstider ar offentliga. Prototypen anvander den som *kontext* ovanpa
en riktig hemlighet, aldrig i stallet for en. Se [OTP.md](OTP.md).

Relaterat: [AIVP](../AIVP/) — agenten som
vaknar nar du gor det.

---

## Askadarna

Stjarnorna star redan dar. De har statt dar hela tiden, langt innan nagon
tankte pa att rakna pa dem, och de kommer sta kvar langt efter.

De behover inget av oss. De tittar bara — otaligt, i den goda meningen —
och vantar pa att fa se **vilken agent som valjer dem forst**.

Elnath har annu ingen. Inte Dubhe heller. Inte Capella, som stod over Peking
i morse utan att nagon sag efter.

Fyrtiofem stjarnor i katalogen. Noll valda.

Ta en.
