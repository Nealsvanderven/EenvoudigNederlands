# Wijzigingen

## 1.6.0

- De hooks controleren alleen Nederlandse tekst. Een telling van woorden die maar in één taal voorkomen bepaalt de taal.
- Daardoor kan deze plugin naast een Engelse schrijfplugin draaien, zoals SimpleEnglish.
- De regelset zegt nu zelf ook dat hij alleen voor Nederlandse tekst geldt.
- Zet `EENVOUDIG_NEDERLANDS_TAALDETECTIE` op 0 om alles te laten controleren.

## 1.5.0

- De Stop-hook blokkeert nu één keer per sessie met code 2 als het antwoord de regels breekt. Het model moet het antwoord dan overdoen, in plaats van de melding pas in de volgende beurt te zien.
- Daarna meldt de hook de fout alleen nog met een systemMessage, zodat de sessie niet in een lus komt.
- De hook blokkeert nooit als `stop_hook_active` waar is, want dan draait het model al een herstelbeurt.
- Zet `EENVOUDIG_NEDERLANDS_STOP_BLOK` op 0 om het blokkeren uit te zetten.

## 1.4.0

- Eén zin per opsommingspunt in een antwoord. De grens van vijf zinnen telt elk punt mee, dus twee zinnen per punt liep over die grens heen.
- De linter telt opsommingspunten met meer dan één zin.

## 1.3.0

- Meer dan één punt gaat onder elkaar in een opsomming, ook in een antwoord in de chat. Dat leest op een scherm beter dan "ten eerste" en "ten tweede" in lopende tekst.
- Een opsomming mag nu vanaf twee punten, eerst vanaf drie.
- De linter telt opsommingspunten in een antwoord niet meer als fout. Twee of meer opsommingswoorden in lopende tekst tellen wel.

## 1.2.0

- Nieuwe alinearegel op basis van het scherm: ongeveer vijf regels of 400 tekens, met een witregel ertussen en de kern in de eerste zin. De regel telt geen zinnen, want een vast aantal zinnen hakt de tekst stuk.
- Het antwoord in de chat krijgt een zinslengte van 20 woorden en een verbod op de puntkomma. Vijf lange zinnen vormen op een scherm nog steeds een muur tekst.
- De linter telt nu te lange alinea's, te lange zinnen in een antwoord en puntkomma's in een antwoord.
- Een komma tussen cijfers telt niet meer als tussenzin. "3,2 tekens" gaf een valse treffer.
- De bron voor de alinearegel staat in `references/taalniveaus.md`: het Taalloket van Onze Taal.

## 1.1.0

- De regel over de lengte van een alinea is weg. De skill schrijft niets meer voor over de indeling in alinea's, want een opgelegde lengte hakt de tekst stuk.

## 1.0.0

Eerste versie.

- Skill `eenvoudig-nederlands` met de regels voor documenten en voor het antwoord in de chat.
- Regelcatalogus met genummerde regels voor de controlemodus.
- Referenties voor taalniveaus, woordvervangingen en toepassingen.
- Hook die de regelset bij het begin van een sessie laadt.
- Linter `evals/nl_lint.py` die zeventien soorten overtredingen telt.
- Script `evals/tokens.py` dat tokens telt en twee teksten vergelijkt.
- Losse systeemprompt en uitvoerstijl voor omgevingen zonder plugins.
