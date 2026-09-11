# Voor en na

De bestanden `voor.md` en `na.md` bevatten dezelfde inhoud. `voor.md` is de stijl die een model zonder deze regels maakt. `na.md` is de stijl onder de regels. Reken de verschillen na met:

```
python3 ../evals/tokens.py --vergelijk voor.md na.md
python3 ../evals/nl_lint.py --type beschrijvend voor.md
python3 ../evals/nl_lint.py --type beschrijvend na.md
```

## Foutmelding

> Voor: Oeps! Er is iets misgegaan bij het opzetten van de verbinding. Controleer alstublieft of uw gegevens correct zijn geconfigureerd en probeer het opnieuw.

> Na: De verbinding met de database mislukte. Het wachtwoord van gebruiker `app` klopte niet. Zet `DB_PASSWORD` en maak opnieuw verbinding.

## Ambtelijke zin met tangconstructie

> Voor: De klant kan, indien hij het pakket binnen veertien dagen na ontvangst retourneert, aanspraak maken op terugbetaling van het aankoopbedrag.

> Na: De klant krijgt het aankoopbedrag terug. Hij stuurt het pakket binnen veertien dagen terug.

## Naamwoordstijl

> Voor: Het uitvoeren van de migratie dient plaats te vinden na het inloggen.

> Na: Je voert de migratie uit nadat je bent ingelogd.

## Incidentmelding

> Voor: Wij hebben geconstateerd dat er mogelijk sprake is geweest van een verstoring die impact kan hebben gehad op een deel van onze gebruikers.

> Na: Tussen 14.02 en 14.31 uur mislukte 12 procent van de aanvragen. De oorzaak is nog onbekend.

## Antwoord in de chat

> Voor: **Goede vraag!** De storing komt voort uit leader election in de control plane tijdens pod churn — hier hoef je je geen zorgen over te maken. Laat het me weten als je nog vragen hebt!

> Na: De pods zijn opnieuw gestart en de wachtrij had even geen leider. Dat is vanzelf hersteld. Je hoeft niets te doen.
