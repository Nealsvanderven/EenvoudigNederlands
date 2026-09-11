# Toepassingen buiten documentatie

Eenvoudig Nederlands helpt overal waar een misverstand geld of tijd kost. Hieronder staat per soort tekst de modus en het patroon.

## Foutmeldingen en uitvoer op de opdrachtregel

Modus: procedureel. Een foutmelding is een instructie aan een gespannen lezer om twee uur 's nachts. Dit levert de meeste winst op.

Patroon: zeg wat er gebeurde (verleden tijd), zeg de oorzaak als je die kent, en geef het commando of de voorwaarde die het oplost.

> Voor: Oeps! Er is iets misgegaan bij het opzetten van de verbinding. Controleer alstublieft of uw gegevens correct zijn geconfigureerd en probeer het opnieuw.
> Na: De verbinding met de database mislukte. Het wachtwoord van gebruiker `app` klopte niet. Zet `DB_PASSWORD` en maak opnieuw verbinding.

## Draaiboeken en werkinstructies

Modus: procedureel, met de grens van 15 woorden hard.

1. Elke stap staat in de gebiedende wijs en bevat één instructie.
2. De voorwaarde staat vooraan, met "dan".
3. Een waarschuwing staat voor de stap waar die bij hoort: eerst de opdracht, dan het risico.
4. De lezer heeft dienst en leest elke zin één keer. De grens van 15 woorden is niet onderhandelbaar.

## Incidentrapporten

Modus: beschrijvend, alleen verleden tijd. Een tijdlijn in de voltooid tegenwoordige tijd verbergt wanneer iets gebeurde.

> Voor: Wij hebben geconstateerd dat er mogelijk sprake is geweest van een verstoring die impact kan hebben gehad op een deel van de gebruikers.
> Na: Tussen 14.02 en 14.31 uur mislukte 12 procent van de aanvragen. Een deploy om 14.00 uur verwijderde de stap die de cache vult.

Schrijf "onbekend" als iets onbekend is. Dat leest eerlijker, want het is eerlijker.

## Commitberichten en beschrijvingen van merge requests

Modus: gebiedende wijs in de titel, beschrijvend in de tekst. Pas de omzettabel toe en houd de grens van 20 woorden aan. Schrap "deze merge request heeft tot doel".

## Releasenotities en changelogs

Modus: beschrijvend. Eén regel, één wijziging, zo mogelijk één zin. Een regel met een breuk volgt het waarschuwingspatroon, opdracht eerst: "Pas je aanroepen naar `v2/users` aan. Het veld `name` is gesplitst in `first_name` en `last_name`."

## Brieven en e-mails aan klanten

Modus: beschrijvend, aanspreekvorm "u", grens van 20 woorden. Zet in de eerste alinea wat er aan de hand is en wat de klant moet doen. Zet de uitleg daaronder. Geen "wij verontschuldigen ons voor het eventuele ongemak", maar "De webshop lag er 18 minuten uit. Bestellingen uit die periode zijn bewaard en worden vandaag verwerkt."

## Instructies voor AI-agenten (prompts, AGENTS.md, skills)

Modus: procedureel. Een systeemprompt is een werkinstructie voor een lezer die niets kan vragen.

1. Eén instructie per zin maakt elke regel citeerbaar en moeilijk half op te volgen.
2. Eén woord met één betekenis voorkomt dat het model "controleren", "verifiëren" en "valideren" als drie handelingen leest.
3. De voorwaarde vooraan ("Als de build mislukt, stop dan") werkt beter dan een voorwaarde achteraan, want die laten modellen vallen.
4. Geen "zou moeten". Een model leest dat als vrijblijvend. Schrijf "moet" of schrap de regel.

## Schermteksten en lege toestanden

Modus: procedureel, met harde lengtegrenzen. Knoppen en labels zijn namen en vallen buiten de regels. De rest volgt ze wel: "Je hebt nog geen projecten. Maak een project om te beginnen."

## Voorbereiding op vertaling

Modus: strikt. Korte zinnen, één betekenis per woord en volledige grammatica halen de meeste dubbelzinnigheid weg. Dat verlaagt de fouten en de kosten van een vertaling, en het verbetert de uitvoer van een vertaalmachine.

## Waar deze regels niet passen

Reclamepagina's, lanceringsberichten, blogs met een eigen stem en merkteksten. Deze regels halen overtuigingskracht er met opzet uit. Schrijf die teksten in je eigen stem. Gebruik de regels daarna voor de documentatie waar die pagina naar verwijst.
