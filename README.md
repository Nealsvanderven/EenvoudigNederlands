# Eenvoudig Nederlands

Een plugin en skill voor Claude Code, Codex, Cursor en andere agenten. De plugin laat het model Nederlands schrijven op taalniveau B1, oftewel referentieniveau 2F. Dat is het leesniveau van mbo 1 tot en met mbo 3 en van ongeveer zeventig procent van de Nederlanders.

De plugin werkt op twee plekken tegelijk. In documenten zorgt zij voor korte zinnen, de actieve vorm en gewone woorden. In de chat zorgt zij voor een antwoord van maximaal vijf zinnen in lopende tekst.

Deze plugin is een Nederlandse tegenhanger van [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) van AminBlg, die de regels van ASD-STE100 toepast op Engels. De opbouw komt daarvandaan. De regels zijn nieuw, want Nederlands heeft andere valkuilen: tangconstructies, naamwoordstijl, ambtelijke woorden en samenstellingen.

## Wat het doet

De plugin doet drie dingen:

1. Bij het begin van een sessie laadt een hook de regelset. Je hoeft de skill niet te noemen.
2. Na elke Write of Edit op een Markdown-bestand telt een linter de overtredingen en meldt die aan het model. De linter blokkeert nooit.
3. Aan het eind van een antwoord controleert dezelfde linter het antwoordregister: maximaal vijf zinnen, maximaal 20 woorden per zin, geen koppen en geen vet. Breekt het antwoord de regels, dan blokkeert de hook één keer per sessie, zodat het model het antwoord overdoet.

## Installeren

Voor Claude Code:

```
/plugin marketplace add Nealsvanderven/EenvoudigNederlands
/plugin install eenvoudig-nederlands
```

Voor een omgeving zonder ondersteuning voor plugins: plak het blok uit `prompts/system-prompt.md` in je systeemprompt, je eigen instructies, `AGENTS.md` of `.cursorrules`.

Voor Claude Code als uitvoerstijl: kopieer `output-styles/eenvoudig-nederlands.md` naar `~/.claude/output-styles/` en kies de stijl met `/output-style`.

## Wat het oplevert in tokens

De regels halen opvulling weg. Dat scheelt uitvoertokens. Bij een lange sessie scheelt het ook invoertokens, want het gesprek blijft korter.

De plugin bevat een voorbeeld dat je zelf kunt narekenen. `examples/voor.md` is tekst in de stijl die een model zonder deze regels maakt. `examples/na.md` is dezelfde inhoud onder de regels.

```
python3 evals/tokens.py --vergelijk examples/voor.md examples/na.md
python3 evals/nl_lint.py --type beschrijvend examples/voor.md
python3 evals/nl_lint.py --type beschrijvend examples/na.md
```

| Maat | Voor | Na |
|---|---|---|
| Tokens (schatting) | 554 | 264 |
| Woorden | 261 | 130 |
| Gemiddelde zinslengte | 28,0 woorden | 7,8 woorden |
| Overtredingen | 31 | 0 |

Dat is 52 procent minder tokens voor dezelfde inhoud. Het getal komt uit dit ene voorbeeld en is geen belofte voor elke tekst.

De plugin kost ook tokens. De hook voegt bij het begin van een sessie ongeveer 1600 tokens toe. Vanaf ongeveer zes herschreven documenten of lange antwoorden per sessie levert de plugin meer op dan zij kost. Werk je in één sessie aan één klein bestand, dan kost zij meer dan zij oplevert.

De grootste besparing zit niet in documenten maar in de chat. De grens van vijf zinnen haalt de herhaling, de aanloopjes en de samenvattingen uit elk antwoord.

## Hoe de tokens geteld zijn

Is tiktoken geïnstalleerd, dan telt `evals/tokens.py` echte tokens met de codering `o200k_base`. Ontbreekt tiktoken, dan schat het script het aantal tokens op 3,2 tekens per token.

Dat is de orde van grootte voor Nederlands proza. Engels haalt ongeveer 4 tekens per token en Nederlands minder, want Nederlandse woorden zijn langer.

De tabel hierboven komt uit de schatting. Installeer tiktoken voor een echte meting:

```
pip install tiktoken
python3 evals/tokens.py --vergelijk examples/voor.md examples/na.md
```

## De regels in het kort

Voor documenten:

1. Procedurele zin: maximaal 15 woorden. Beschrijvende zin: maximaal 20 woorden.
2. Voorwaarde voor opdracht, met komma en "dan".
3. Actieve vorm. Noem wie iets doet.
4. Werkwoordstijl, geen naamwoordstijl.
5. Geen tangconstructie en maximaal twee werkwoorden aan het eind van een zin.
6. Modale werkwoorden: kunnen, zullen, moeten. Nooit "dient te" of "zou moeten".
7. Geen ambtelijke woorden en geen afkortingen in lopende tekst.
8. Eén woord, één betekenis in het hele document.
9. Eén aanspreekvorm, "je" of "u", in het hele document.
10. Leg een vakterm uit bij het eerste gebruik.

Voor het antwoord in de chat:

1. Eén punt in lopende tekst, meer punten onder elkaar met één zin per punt.
2. Maximaal vijf zinnen en maximaal 20 woorden per zin.
3. De eerste zin geeft het antwoord.
4. Geen gedachtestreepje, geen aanloopjes, geen afsluiters.

De volledige regelset staat in `skills/eenvoudig-nederlands/SKILL.md`. De genummerde catalogus voor de controlemodus staat in `skills/eenvoudig-nederlands/references/regelcatalogus.md`.

## De linter

`evals/nl_lint.py` telt zeventien soorten mechanische overtredingen. Dit zijn de soorten:

- Zinslengte boven de grens
- Ambtelijke woorden en verboden modale werkwoorden
- Naamwoordstijl, lijdende vorm en voltooide tijden
- Werkwoordclusters en lange tussenzinnen
- Puntkomma's, gedachtestreepjes en afkortingen
- Opsmukwoorden en voorwaarden achteraan
- Synoniemrotatie en een gemengde aanspreekvorm

```
python3 evals/nl_lint.py --type procedureel draaiboek.md
cat tekst.md | python3 evals/nl_lint.py --type beschrijvend -
python3 evals/nl_lint.py --self-test
```

De linter is een reguliere expressie, geen taalkundige ontleder. Hij telt te weinig en hij kan zich vergissen. De getallen vergelijken twee teksten die door dezelfde versie zijn gehaald. Geen enkel hulpmiddel garandeert taalniveau B1. Een lezer uit de doelgroep blijft de beste toets.

## Naast een Engelse schrijfplugin

De hooks controleren alleen Nederlandse tekst. Een eenvoudige telling van woorden die maar in één taal voorkomen bepaalt de taal.

Daardoor kun je deze plugin naast een Engelse schrijfplugin gebruiken, zoals [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish). De Engelse plugin pakt de Engelse tekst en deze plugin de Nederlandse.

Zet `EENVOUDIG_NEDERLANDS_TAALDETECTIE` op 0 als je alles wilt laten controleren.

## Waar de regels niet passen

Reclameteksten, lanceringsberichten en blogs met een eigen stem. De regels halen overtuigingskracht er met opzet uit. Gebruik ze voor de documentatie waar die pagina naar verwijst.

## Bronnen

- Referentiekader Taal en Rekenen, 2010, voor de niveaus 1F tot 4F
- Direct Duidelijk, campagne van het ministerie van Binnenlandse Zaken
- ISO 24495-1:2023, Plain language, deel 1
- [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish), de Engelse plugin waar de opbouw vandaan komt

## Licentie

MIT. Zie `LICENSE`.
