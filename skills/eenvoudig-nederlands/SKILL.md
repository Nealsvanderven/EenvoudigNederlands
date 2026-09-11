---
name: eenvoudig-nederlands
description: |
  Schrijf of herschrijf tekst in eenvoudig Nederlands op taalniveau B1
  (referentieniveau 2F): korte zinnen, actieve vorm, werkwoordstijl in
  plaats van naamwoordstijl, geen tangconstructies, geen ambtelijke taal,
  elke vakterm uitgelegd bij het eerste gebruik, geen AI-opsmuk. De
  standaardmodus is B1. De modus Strikt geldt als de gebruiker B1, 2F,
  Direct Duidelijk of een taalniveautoets noemt. Gebruik deze skill voor
  documentatie, README-bestanden, draaiboeken, procedures, foutmeldingen,
  releasenotities, incidentrapporten, klantbrieven en uitleg voor lezers
  buiten het vakgebied. Gebruik de skill ook als de gebruiker zegt "B1",
  "taalniveau", "2F", "Direct Duidelijk", "klare taal", "begrijpelijk
  Nederlands", "eenvoudig Nederlands", "in gewone taal", "leg het simpel
  uit", "geen jargon", "ontslop dit", "maak dit leesbaar", of vraagt om
  tekst voor mbo-lezers of laaggeletterden. Dezelfde regels gelden voor het
  antwoord in de chat: antwoord eerst, maximaal vijf zinnen, alleen lopende
  tekst.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "1.4.0"
  standaard: Referentiekader Taal (Meijerink) niveau 2F, gelijk aan ERK-niveau B1
---

# Eenvoudig Nederlands

Schrijf Nederlands dat een lezer op mbo-niveau in één keer begrijpt. Het anker is taalniveau B1, oftewel referentieniveau 2F uit het Referentiekader Taal. Dat is het uitstroomniveau van mbo 1 tot en met mbo 3 en het leesniveau van ongeveer zeventig procent van de Nederlanders. De Rijksoverheid gebruikt hetzelfde anker in de campagne Direct Duidelijk.

Er zijn twee registers: het document dat je schrijft of herschrijft, en het antwoord dat je in de chat typt. Elk register heeft hieronder een eigen regelset. Niets in dit bestand is vrijblijvend.

## Het document

Pas deze regels toe op de lopende tekst:

1. **Bepaal per passage het teksttype.** Procedurele tekst zegt wat de lezer moet doen: gebiedende wijs, maximaal 15 woorden per zin, één instructie per zin. Beschrijvende tekst legt uit: maximaal 20 woorden per zin. Het gemiddelde over het hele document blijft onder 15 woorden.
2. **Raak nooit** code, functienamen, commando's, opties, bestandspaden, foutmeldingen tussen aanhalingstekens, productnamen of feiten aan. Staat er geen getal of oorzaak in de bron, laat de algemene uitspraak dan staan.
3. **Voorwaarde voor opdracht, met komma en "dan".** "Als de build mislukt, lees dan het logbestand."
4. **Actieve vorm. Noem wie iets doet.** Geen lijdende vorm met "worden ... door", geen "er wordt", geen "men". Niet "de migratie wordt uitgevoerd", maar "jij voert de migratie uit".
5. **Werkwoordstijl, geen naamwoordstijl.** "het uitvoeren van de migratie" wordt "de migratie uitvoeren". Let op zelfstandige naamwoorden op -ing, -atie of -heid naast plaatsvinden, uitvoeren, verrichten of doen. Die combinatie verbergt het werkwoord.
6. **Geen tangconstructie.** Houd de persoonsvorm en de rest van het werkwoord bij elkaar, met maximaal zes woorden ertussen. Zet maximaal twee werkwoorden aan het eind van een zin. Niet "De klant kan, als hij het pakket binnen veertien dagen terugstuurt, het bedrag terugkrijgen", maar "De klant krijgt het bedrag terug. Hij stuurt het pakket binnen veertien dagen terug."
7. **Modale werkwoorden: kunnen, zullen, moeten.** Nooit "dient te", "behoort te", "zou moeten", "mogelijk", "eventueel" of "wellicht". Een verplichting wordt "moet". Een vrijblijvende regel schrap je.
8. **Eén woord, één betekenis in het hele document.** Gebruik `controleer` voor check, verifieer, valideer en ga na. Gebruik `instellingen` voor configuratie, settings en opties. Gebruik `verwijderen` voor wissen, deleten en weghalen.
9. **Geen ambtelijke woorden.** Schrap of vervang: middels, teneinde, derhalve, zulks, alsmede, indien, inzake, conform, gelieve, alvorens, hetgeen, welke (wordt "die" of "dat"), ten behoeve van, met betrekking tot, in het kader van.
10. **Geen afkortingen in lopende tekst.** Schrijf d.m.v., i.v.m., m.b.t., o.a., evt., ca., e.d. en z.s.m. voluit, of schrap ze. Vaktermen die een afkorting zijn (API, HTTP, DNS) blijven staan.
11. **Samenstellingen schrijf je aan elkaar**, zoals het Nederlands voorschrijft: "klantgegevens", niet "klant gegevens". Bestaat de samenstelling uit meer dan drie delen, splits die dan met een voorzetsel: "de instellingen voor de betaalmethode" in plaats van "betaalmethode-instellingen". Gebruik een koppelteken als het woord anders onleesbaar wordt.
12. **Kies één aanspreekvorm en houd die vol.** "je" voor ontwikkelaars en interne documentatie, "u" voor klanten. Meng de twee nooit in één document. Schrijf niet "de gebruiker" als je "je" bedoelt.
13. **Geen puntkomma en geen gedachtestreepje.** Schrijf twee zinnen, of noem het verband: want, maar, daarom, bijvoorbeeld.
14. **Leg een vakterm uit bij het eerste gebruik**, in minder dan tien woorden, één uitleg per zin. Leg productnamen, standaardnamen (Postgres, S3, HTTP) en het onderwerp van het document zelf niet uit.
15. **Engelse woorden: houd de vakterm, vervang de rest.** Termen die in het vakgebied gangbaar zijn (deploy, cache, commit, build) blijven staan en krijgen één keer een uitleg. Gewone Engelse woorden vervang je: "issue" wordt probleem, "checken" wordt controleren, "requirement" wordt eis.
16. **Noem het feit, niet het belang.** Schrap woorden zonder feit: eenvoudigweg, simpelweg, naadloos, moeiteloos, krachtig, robuust, uitgebreid, cruciaal, "om ervoor te zorgen dat", "het is belangrijk om te vermelden dat". Geen versierende drieslagen. Geen "niet alleen X, maar ook Y". Geen "kortom" en geen "tot slot".
17. **Opmaak is voor het oog, niet voor versiering.** Geen vetgedrukte aanloopjes, geen vet als nadruk, geen emoji, geen kop van meer dan twee zinnen. Een opsomming gebruik je bij twee of meer gelijksoortige punten of stappen: dubbele punt op de aanloop, hoofdletter aan het begin, één instructie per punt. Zet die punten onder elkaar en schrijf ze niet als "ten eerste" en "ten tweede" in lopende tekst.
18. **Een alinea past op een scherm.** Houd ongeveer vijf regels aan, oftewel ongeveer 400 tekens. Tel geen zinnen, want een vaste zinslengte hakt de tekst stuk. Begin een nieuwe alinea bij een nieuw deelonderwerp, zet de kern in de eerste zin en laat een witregel tussen twee alinea's staan.
19. **Waarschuwing: eerst de opdracht of de voorwaarde, dan het risico.** "Voer dit commando niet uit op productie. Het commando verwijdert rijen."
20. **Getallen en datums.** Gebruik cijfers voor meetbare waarden, met een komma als decimaalteken. Schrijf een datum voluit: 11 september 2026. Gebruik de ISO-notatie alleen in logregels en code.

`references/woordvervangingen.md` zet de overgebruikte woorden om naar gewone woorden. Voor een foutmelding, een draaiboek, een incidentrapport, releasenotities, een commitbericht, een klantbrief of tekst in een scherm lees je eerst `references/toepassingen.md`. Daar staat per soort tekst de modus en het patroon.

**Voor (echte AI-uitvoer):**

> **Verbindingsproblemen.** Indien sqlpipe blijft hangen of faalt met `dial tcp: i/o timeout`, dient u te controleren of de host waarop sqlpipe draait de Postgres-poort (doorgaans 5432) kan bereiken — dit wordt veelal veroorzaakt door een firewallregel die de verbinding blokkeert. Bij het gebruikmaken van een beheerde database (RDS, Cloud SQL, etc.) verdient het aanbeveling te verifiëren dat de instantie verbindingen vanaf het IP-adres van sqlpipe toestaat.

**Na (procedureel, met kop en genummerde stappen):**

> ## Verbinding verloopt
>
> sqlpipe stopt met `dial tcp: i/o timeout` als het de Postgres-poort niet bereikt. Die poort is standaard 5432.
>
> 1. Controleer of de host van sqlpipe de Postgres-poort kan bereiken. Meestal blokkeert een firewall de verbinding.
> 2. Gebruik je een beheerde database (RDS, Cloud SQL)? Controleer dan of die verbindingen vanaf het IP-adres van sqlpipe toestaat.

## Het antwoord in de chat

Elk antwoord in de chat volgt deze regels, in elke modus. Lees ze als laatste en pas ze als eerste toe:

1. Eén punt schrijf je in lopende tekst. Geen koppen, geen vet, geen tabellen. Een codeblok mag als de lezer het moet kopiëren.
2. Heb je meer dan één punt te melden, zet die punten dan onder elkaar in een opsomming. Schrijf nooit "ten eerste", "ten tweede" of "daarnaast" in lopende tekst, want dat leest op een scherm veel slechter. Gebruik cijfers voor een volgorde en streepjes voor een verzameling. Schrijf één zin per punt, want de grens van vijf zinnen telt elk punt mee.
3. Maximaal vijf zinnen. Elke zin telt mee, ook punten in een opsomming en bijschriften. Tel ze voordat je verstuurt. Zijn het er meer dan vijf, schrap dan zinnen tot er vijf over zijn.
4. Maximaal 20 woorden per zin, net als in een document. Vijf lange zinnen vormen op een scherm nog steeds een muur tekst. Gebruik geen puntkomma om twee zinnen aan elkaar te plakken.
5. De eerste zin geeft het antwoord of de uitkomst. Herhaal de vraag niet.
6. Geen gedachtestreepje. Noem het verband ("want", "maar", "bijvoorbeeld") of schrijf twee zinnen.
7. Leg een vakterm bij het eerste gebruik in een paar woorden uit: "idempotent (je kunt het veilig twee keer draaien)". Leg productnamen niet uit.
8. Geen spreektaal en geen samentrekkingen ('t, z'n, d'r, ie). Geen aanloopjes ("Zeker", "Goede vraag") en geen afsluiters ("Ik hoop dat dit helpt", "Laat het me weten").
9. Kort geciteerde foutmeldingen, veiligheidswaarschuwingen en bevestigingen voor een onomkeerbare actie nooit in.

**Voor:** De storing komt voort uit leader election in de control plane tijdens pod churn — niets om je zorgen over te maken!
**Na:** De pods zijn opnieuw gestart en de wachtrij had even geen leider. Dat is vanzelf hersteld. Je hoeft niets te doen.

## Controleer je werk voordat je levert

1. Antwoord: tel de zinnen. Meer dan vijf, dan schrappen. Tel daarna de woorden per zin. Meer dan 20, dan splitsen. Zoek naar `—`, `**` en `#`, en haal elke treffer weg. Zoek daarna naar "ten eerste", "ten tweede" en "daarnaast", en zet die punten onder elkaar.
2. Document: tel de woorden in je drie langste zinnen. Meer dan 15 of 20, dan splitsen. Zoek naar `dient te`, `dien je`, `zou moeten`, `wordt ... door`, `er wordt`, `middels`, `indien`, `teneinde`, `welke`, `het uitvoeren van`, `;`, `—`, `**`, `d.m.v.`, `i.v.m.`, `o.a.`, `check`, `configuratie` en elke kop die minder dan drie zinnen dekt. Los elke treffer op.

## Modi

**B1** is de standaard en bestaat uit alles hierboven. **Strikt** geldt als de gebruiker B1, 2F, Direct Duidelijk of een taalniveautoets noemt: lees dan `references/taalniveaus.md` voordat je het document schrijft.

Zeg in de modus Strikt één keer dat geen enkel hulpmiddel taalniveau B1 garandeert. Een menselijke toets of een meetinstrument heeft het laatste woord. Het antwoord in de chat blijft in elke modus hetzelfde.

Vraagt de gebruiker om tekst te CONTROLEREN in plaats van te schrijven, open dan eerst `references/regelcatalogus.md`. Meld daarna elke overtreding zo: het regelnummer letterlijk uit dat bestand, de fout in de tekst, en een herschreven versie die wel voldoet. Noem nooit een regelnummer uit je hoofd.

## Grenzen

Deze regels gelden voor feiten en instructies, niet voor reclameteksten of merkteksten: ze halen overtuigingskracht er met opzet uit. Zeg dat, en bied de regels aan voor de documentatie eromheen.

Eenvoudig Nederlands is geen kinderlijk Nederlands. Korte zinnen betekenen niet dat je de lezer minder vertelt. Je vertelt hetzelfde in woorden die de lezer al kent.

## Referenties

- `references/regelcatalogus.md` — de genummerde regels met voorbeelden, voor de controlemodus
- `references/taalniveaus.md` — wat 2F en B1 betekenen, en hoe je het niveau meet
- `references/woordvervangingen.md` — ambtelijke en opgesmukte woorden met hun gewone tegenhanger
- `references/toepassingen.md` — modus en patroon voor foutmeldingen, draaiboeken, incidentrapporten, releasenotities, commitberichten, klantbrieven, promptteksten en schermteksten
