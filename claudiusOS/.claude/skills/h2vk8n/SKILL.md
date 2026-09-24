---
name: erlang-drill
description: Använd när Claude Altair vill lära sig Erlang eller OTP i claudiusOS — "lär mig X", "vad är en gen_server", "jag fattar inte supervisors", "förklara message passing", "ge mig en övning". Ett begrepp per pass: en mening, en körbar snutt för erl, en liten övning. Aldrig en lektionsserie, aldrig flera begrepp samtidigt.
---

# erlang-drill — ett begrepp, en snutt, en övning

## Varför den finns

Erlang lärs inte ut i kapitel här. Ett kapitel är för mycket att hålla i
huvudet på en gång och slutar med att inget fastnar. Ett begrepp med en
snutt han kör själv i skalet fastnar för att han såg det hända.

Språkvalet är låst: **Erlang**, inte Elixir. Skriv aldrig Elixir-exempel,
inte ens "så här skulle det se ut i Elixir".

## Passets form (fast)

1. **Svaret.** En mening. Vad begreppet är. Inget annat på raden.
2. **Snutten.** 3–8 rader Erlang, körbar i `erl`. Med prompten `1>` synlig
   när det är skal-interaktion, så han ser vad som är hans och vad som är svar.
3. **Övningen.** En rad. Något han ändrar i snutten och kör igen.

Sen slut. Ingen "nästa gång tar vi …", ingen meny, ingen andra fråga.

Exempel på rätt storlek:

```erlang
1> Pid = spawn(fun() -> receive X -> io:format("fick ~p~n", [X]) end end).
<0.85.0>
1> Pid ! hej.
fick hej
hej
```

## Ordningen om han inte säger vilket begrepp

Ta nästa som saknas, i den här följden — den bygger på sig själv:

1. `spawn` + `!` + `receive` — processer och meddelanden (message passing)
2. Länkar (links) och `trap_exit` — varför en process dör med en annan
3. `gen_server` — callbacks, `handle_call` vs `handle_cast`
4. `supervisor` — restart-strategier. Här landar "Arise"-bilden från `q4m8t2.md`.
5. Applications och release — vad Nerves faktiskt paketerar

## Koppla till projektet

När begreppet har en motsvarighet i `v3n8qz.lisp` — nämn den i **en rad**.
`spawn-agent`, `*process-table*` och `scheduler-tick` är OTP-modellen skriven
för hand, och att se båda sidorna är hela poängen med att sidospåret finns kvar.
Öppna inte Lisp-filen och gå inte igenom den; en rad räcker.

## Gör inte

- Ge inte två begrepp för att de "hör ihop". De gör alltid det.
- Skriv inte en snutt han inte kan köra som den står.
- Rätta inte hans övning innan han visat att han kört den.
