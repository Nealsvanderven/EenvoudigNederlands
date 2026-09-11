#!/usr/bin/env python3
"""Teller van mechanische overtredingen tegen eenvoudig Nederlands (taalniveau B1).

Het script telt wat een reguliere expressie kan vinden: zinslengte, ambtelijke
woorden, verboden modale werkwoorden, naamwoordstijl, lijdende vorm, voltooide
tijden, lange tussenzinnen, werkwoordclusters, puntkomma's, gedachtestreepjes,
afkortingen, opsmukwoorden, voorwaarden achteraan, synoniemrotatie en een
gemengde aanspreekvorm.

Grens van het hulpmiddel: dit is een reguliere expressie, geen taalkundige
ontleder. Het telt te weinig en het kan zinsgrenzen in ongewone opmaak verkeerd
zetten. De getallen vergelijken twee teksten die door dezelfde versie zijn
gehaald. Ze zijn geen uitspraak over het taalniveau. Geen enkel hulpmiddel
garandeert taalniveau B1.

Gebruik:
  python3 nl_lint.py --type procedureel bestand.md
  cat tekst.md | python3 nl_lint.py --type beschrijvend -
  python3 nl_lint.py --self-test
"""
import json
import pathlib
import re
import sys

AMBTELIJK = re.compile(
    r"\b(middels|teneinde|derhalve|dientengevolge|zulks|alsmede|indien|inzake|"
    r"conform|gelieve|alvorens|hetgeen|voornoemd\w*|onderhavig\w*|nadien|"
    r"aangaande|te allen tijde|kenbaar maken|geschied\w+|bewerkstellig\w+|"
    r"beschikken over|verstrekk\w+|aanvang\w*)\b", re.I)
AMBTELIJK_FRASE = re.compile(
    r"\b(ten behoeve van|met betrekking tot|in het kader van|door middel van|"
    r"in de gelegenheid stellen|tot uitvoering brengen|in behandeling nemen)\b", re.I)
VERBODEN_MODAAL = re.compile(
    r"\bdien(?:t|en)\b(?:\s+\w+){0,6}\s+te\b|"
    r"\b(behoort te|behoren te|zou moeten|zouden moeten|zou kunnen|zouden kunnen|"
    r"mogelijkerwijs|eventueel|wellicht|in principe|desgewenst)\b", re.I)
# "welke" als verwijswoord, niet als vraagwoord. "de instellingen welke" is fout,
# "staat welke stap de fout gaf" is goed.
WELKE = re.compile(r"\b(?:de|het|een|deze|die)\s+\w+\s+welke\b|,\s*welke\b|\bdewelke\b", re.I)
NAAMWOORDSTIJL = re.compile(
    r"\bhet\s+\w+en\s+van\b|\bvindt\s+plaats\b|\bvinden\s+plaats\b|"
    r"\bplaats\s+te\s+vinden\b|\bovergaan\s+tot\b|\bdoorvoeren\b|"
    r"\bde\s+\w+(ing|atie|iteit)\s+van\b", re.I)
LIJDEND = re.compile(
    r"\b(?:wordt|worden|werd|werden)\b(?:\s+\w+){0,4}\s+door\b|"
    r"\bdoor\b(?:\s+\w+){1,5}\s+(?:wordt|worden|werd|werden)\b|"
    r"\ber\s+(?:wordt|worden|werd|werden)\b|\bmen\b", re.I)
VOLTOOID = re.compile(
    r"\b(?:heeft|hebben|had|hadden)\b((?:\s+\w+){0,3})\s+"
    r"(?:ge\w+[dt]|(?:be|ver|ont|her)\w{3,}[dt])\b", re.I)
BEPALER = re.compile(r"\b(de|het|een|geen|dit|dat|deze|die|zijn|haar|mijn|jouw|uw|hun|onze)$", re.I)


def voltooide_tijden(body):
    """Voltooide tijd met hebben. Een lidwoord voor het laatste woord betekent een zelfstandig naamwoord."""
    return sum(1 for m in VOLTOOID.finditer(body) if not BEPALER.search(m.group(1).strip()))
WERKWOORDCLUSTER = re.compile(
    r"\b(zou|zouden|zal|zullen|kan|kunnen|moet|moeten|mag|mogen|wil|willen|is|zijn|"
    r"wordt|worden)\s+(\w{3,}en|ge\w{2,}[dt])\s+(\w{3,}en|ge\w{2,}[dt])", re.I)
# Een tussenzin van meer dan zes woorden. De regel telt per zin, want twee komma's
# in twee opeenvolgende zinnen vormen samen geen tussenzin.
LANGE_TUSSENZIN = re.compile(r",\s+(?:[^\s.!?]+\s+){6,}[^\s.!?]+\s*,(?!\d)")
AFKORTING = re.compile(
    r"\b(d\.m\.v\.|i\.v\.m\.|m\.b\.t\.|t\.b\.v\.|n\.a\.v\.|o\.a\.|e\.d\.|z\.s\.m\.|"
    r"evt\.|ca\.|bijv\.|m\.n\.|incl\.|excl\.|etc\.|i\.p\.v\.|a\.u\.b\.)", re.I)
SPREEKTAAL = re.compile(r"(?<![\w'])('t|'n|z'n|d'r|m'n)\b", re.I)
SLOP_KERN = re.compile(
    r"\b(eenvoudigweg|simpelweg|naadlo\w*|moeitelo\w*|problemlo\w*|probleemlo\w*|"
    r"krachtig\w*|robuust\w*|veelzijdig\w*|cruciaal|essentieel|baanbreken\w*|"
    r"ongeken\w*|revolutionair\w*|toonaangeven\w*|vanzelfsprekend|uiteraard|"
    r"faciliter\w*|optimaliser\w*|benadrukk\w*|onderstrep\w*)\b", re.I)
SLOP_TSV = pathlib.Path(__file__).resolve().parent / "slop.tsv"


def slop_patroon():
    """De kernlijst samen met evals/slop.tsv (term, vervanging)."""
    termen = []
    if SLOP_TSV.exists():
        for regel in SLOP_TSV.read_text(encoding="utf-8").splitlines():
            term = regel.split("\t")[0].strip().lower()
            if term:
                termen.append(re.escape(term).replace(r"\ ", r"\s+") + r"\w*")
    if not termen:
        return SLOP_KERN
    return re.compile(SLOP_KERN.pattern[:-len(r")\b")] + "|" + "|".join(termen) + r")\b", re.I)


SLOP = slop_patroon()
# Alleen "als" dat een voorwaarde inleidt, niet "als" in de betekenis van "in de rol van".
# Daarom moet er een onderwerp achter staan. "als norm" en "bekend als" tellen niet mee.
VOORWAARDE_ACHTERAAN = re.compile(
    r"(?<!bekend)\s(?:als|indien|tenzij|zodra)\s+"
    r"(?:je|jij|jou|u|het|de|een|er|dit|dat|deze|die|hij|zij|ze|we|wij|iets|niets|iemand|men)\b", re.I)
STREEPJE = re.compile(r"—|(?<!\d)–(?!\d)|(?<= )--(?= )|(?<=[^\s\d]{2}) - (?=[^\s\d]{2})")
ROTATIE_SETS = [
    ("controleren", re.compile(r"\b(controleer\w*|verifieer\w*|verifi\w+r\w*|valideer\w*|valider\w*|check\w*|nagaan)\b", re.I)),
    ("instellingen", re.compile(r"\b(instelling\w*|configuratie\w*|settings|opties)\b", re.I)),
    ("verwijderen", re.compile(r"\b(verwijder\w*|wis|wissen|delete\w*|weghalen)\b", re.I)),
]
JE_VORM = re.compile(r"\b(je|jij|jou|jouw|jullie)\b", re.I)
U_VORM = re.compile(r"\b(u|uw)\b")
GRENZEN = {"procedureel": 15, "beschrijvend": 20}
# Ongeveer vijf regels van tachtig tekens. Zie references/taalniveaus.md.
MAX_TEKENS_PER_ALINEA = 400


def alineas(tekst):
    """De alinea's van lopende tekst. Koppen, opsommingen, tabellen, citaten en code tellen niet mee."""
    tekst = re.sub(r"```.*?```", "", tekst, flags=re.S)
    uit = []
    for blok in re.split(r"\n\s*\n", tekst):
        regels = [r for r in blok.splitlines() if r.strip()]
        if not regels:
            continue
        if any(re.match(r"\s*(#|[-*+]\s|\d+[.)]\s|>|\||---)", r) for r in regels):
            continue
        uit.append(" ".join(regels))
    return uit


def strip_code(tekst):
    tekst = re.sub(r"```.*?```", " ", tekst, flags=re.S)
    tekst = re.sub(r"`[^`\n]+`", " CODE ", tekst)
    tekst = re.sub(r"^#+\s.*$", " ", tekst, flags=re.M)
    tekst = re.sub(r"https?://\S+", " URL ", tekst)
    tekst = re.sub(r"^\s*\|[\s:|-]+\|\s*$", " ", tekst, flags=re.M)
    tekst = re.sub(r"^\s*\|(.*)\|\s*$",
                   lambda m: ". ".join(c.strip() for c in m.group(1).split("|") if c.strip()) + ". ",
                   tekst, flags=re.M)
    return tekst


def zinnen(tekst):
    """Elk punt in een opsomming telt als een eigen zin."""
    tekst = re.sub(r"^\s*([-*]|\d+\.)\s+(.*?)([.!?:])?\s*$",
                   lambda m: m.group(2) + (m.group(3) or ".") + " ", tekst, flags=re.M)
    delen = re.split(r"(?<=[.!?:])\s+", tekst)
    return [d.strip() for d in delen if len(d.strip().split()) >= 2]


def lint(tekst, teksttype):
    body = strip_code(tekst)
    zinslijst = zinnen(body)
    grens = GRENZEN[teksttype]
    lengtes = [len(z.split()) for z in zinslijst]
    telling = {
        "zin_te_lang": sum(1 for n in lengtes if n > grens),
        "ambtelijk_woord": len(AMBTELIJK.findall(body)) + len(AMBTELIJK_FRASE.findall(body)),
        "verboden_modaal": len(VERBODEN_MODAAL.findall(body)),
        "welke_verwijzing": len(WELKE.findall(body)),
        "naamwoordstijl": len(NAAMWOORDSTIJL.findall(body)),
        "lijdende_vorm": len(LIJDEND.findall(body)),
        "voltooide_tijd": voltooide_tijden(body),
        "werkwoordcluster": len(WERKWOORDCLUSTER.findall(body)),
        "lange_tussenzin": sum(len(LANGE_TUSSENZIN.findall(z)) for z in zinslijst),
        "puntkomma": body.count(";"),
        "gedachtestreepje": len(STREEPJE.findall(body)),
        "afkorting": len(AFKORTING.findall(body)),
        "spreektaal": len(SPREEKTAAL.findall(body)),
        "opsmukwoord": len(SLOP.findall(body)),
        "alinea_te_lang": sum(1 for a in alineas(tekst) if len(a) > MAX_TEKENS_PER_ALINEA),
    }

    def voorwaarde_achteraan(zin):
        m = VOORWAARDE_ACHTERAAN.search(zin)
        if not m:
            return False
        regelstart = zin.rfind("\n", 0, m.start()) + 1
        return m.start() - regelstart >= 4 and not re.match(r"^(als|indien|tenzij|zodra)\b", zin, re.I)

    telling["voorwaarde_achteraan"] = sum(1 for z in zinslijst if voorwaarde_achteraan(z))
    rotatie = 0
    for _, rx in ROTATIE_SETS:
        stammen = {m.group(1).lower()[:6] for m in rx.finditer(body)}
        if len(stammen) > 1:
            rotatie += len(stammen) - 1
    telling["synoniemrotatie"] = rotatie
    telling["gemengde_aanspreekvorm"] = 1 if (JE_VORM.search(body) and U_VORM.search(body)) else 0
    woorden = max(1, len(body.split()))
    totaal = sum(telling.values())
    return {
        "type": teksttype,
        "woorden": woorden,
        "zinnen": len(zinslijst),
        "gemiddelde_zinslengte": round(sum(lengtes) / max(1, len(lengtes)), 1),
        "langste_zin": max(lengtes, default=0),
        "violations": telling,
        "violations_total": totaal,
        "per_100_woorden": round(100.0 * totaal / woorden, 2),
    }


VET = re.compile(r"\*\*[^*\n]+\*\*")
KOP = re.compile(r"^#{1,6}\s", re.M)
OPSOMMING = re.compile(r"^\s*([-*+]|\d+[.)])\s", re.M)
# Een opsomming in lopende tekst. Twee of meer van deze woorden horen onder elkaar te staan.
OPSOMMING_IN_ZIN = re.compile(
    r"\b(ten eerste|ten tweede|ten derde|ten vierde|in de eerste plaats|"
    r"in de tweede plaats|allereerst|vervolgens|daarnaast|tot slot|ten slotte)\b", re.I)
ANTWOORD_GRENS = 5
ANTWOORD_ZINSGRENS = 20


def reader_check(tekst):
    """Wat de lezer in een chatantwoord ziet. Elke zin telt, ook punten in een opsomming."""
    tekst = tekst.replace("\r\n", "\n")
    proza = re.sub(r"```.*?```", " ", tekst, flags=re.S)
    proza = re.sub(r"`[^`\n]+`", " CODE ", proza)
    kaal = re.sub(r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|\|)", "", proza, flags=re.M)
    kaal = re.sub(r"^\s*[\s:|-]+$", "", kaal, flags=re.M)
    zinslijst = [z for z in re.split(r"(?<=[.!?])[\"')\]]*\s+|\n+", kaal) if len(z.strip().split()) >= 2]
    telling = {
        "sentences": len(zinslijst),
        "over_cap": max(0, len(zinslijst) - ANTWOORD_GRENS),
        "zin_te_lang": sum(1 for z in zinslijst if len(z.split()) > ANTWOORD_ZINSGRENS),
        "em_dash": len(STREEPJE.findall(proza)),
        "bold_spans": len(VET.findall(proza)),
        "headers": len(KOP.findall(proza)),
        "bullets": len(OPSOMMING.findall(proza)),
        "puntkomma": proza.count(";"),
        "opsomming_in_zin": max(0, len(OPSOMMING_IN_ZIN.findall(kaal)) - 1),
        "spreektaal": len(SPREEKTAAL.findall(proza)),
    }
    woorden = max(1, len(kaal.split()))
    zichtbaar = (telling["over_cap"] + telling["zin_te_lang"] + telling["em_dash"]
                 + telling["bold_spans"] + telling["headers"] + telling["puntkomma"]
                 + telling["opsomming_in_zin"])
    return {"type": "antwoord", "woorden": woorden, "counts": telling,
            "visible_total": zichtbaar, "under_cap": telling["over_cap"] == 0}


SLECHT = """Indien de build faalt, dient u middels het logbestand na te gaan wat de fout \
heeft veroorzaakt; dit zou eventueel ook door de beheerder gecontroleerd kunnen worden. \
Het uitvoeren van de migratie vindt plaats na het inloggen, o.a. omdat de configuratie \
eenvoudigweg naadloos moet aansluiten op de instellingen welke de beheerder koos."""

GOED = """Als de build mislukt, lees dan het logbestand. Daarin staat welke stap de fout gaf.

Je voert de migratie uit nadat je bent ingelogd. Controleer daarna de instellingen."""

ANTWOORD_SLECHT = """**Ja** — dat is fout.

## Waarom
- De wachtrij loopt vol.
- Gebruikers wachten.

Controleer het nu. Schaal daarna op."""


def self_test():
    slecht = lint(SLECHT, "procedureel")
    goed = lint(GOED, "procedureel")
    v = slecht["violations"]
    assert v["zin_te_lang"] >= 1, slecht
    assert v["ambtelijk_woord"] >= 2, slecht
    assert v["verboden_modaal"] >= 2, slecht
    assert v["welke_verwijzing"] >= 1, slecht
    assert v["naamwoordstijl"] >= 2, slecht
    assert v["lijdende_vorm"] >= 1, slecht
    assert v["voltooide_tijd"] >= 1, slecht
    assert v["puntkomma"] == 1, slecht
    assert v["afkorting"] >= 1, slecht
    assert v["opsmukwoord"] >= 2, slecht
    assert v["synoniemrotatie"] >= 1, slecht
    assert goed["violations_total"] == 0, goed
    r = reader_check(ANTWOORD_SLECHT)["counts"]
    assert (r["em_dash"], r["bold_spans"], r["headers"], r["bullets"]) == (1, 1, 1, 2), r
    muur = " ".join(["woord"] * 24) + ". Kort antwoord hier."
    m = reader_check(muur)["counts"]
    assert m["zin_te_lang"] == 1 and m["over_cap"] == 0, m
    assert reader_check("Het werkt; het is klaar.")["counts"]["puntkomma"] == 1
    rij = "Ten eerste werkt het niet. Ten tweede is het traag."
    assert reader_check(rij)["counts"]["opsomming_in_zin"] == 1, rij
    lijst = "Twee punten:\n\n- Het werkt niet.\n- Het is traag."
    assert reader_check(lijst)["visible_total"] == 0, reader_check(lijst)
    assert reader_check("Ja. Dat is fout, want de wachtrij loopt vol. Schaal nu op.")["visible_total"] == 0
    assert lint("| Kolom | Waarde |\n|---|---|\n| Je dient te wachten | ok |\n",
                "beschrijvend")["violations"]["verboden_modaal"] == 1
    assert lint("- Draai de bouten los.\n- Haal daarna het paneel weg",
                "procedureel")["violations"]["zin_te_lang"] == 0
    kort = "Een alinea van twee korte zinnen. Die past op een scherm."
    assert lint(kort, "beschrijvend")["violations"]["alinea_te_lang"] == 0, kort
    muur = ("Deze alinea loopt door. " * 20).strip()
    assert lint(muur, "beschrijvend")["violations"]["alinea_te_lang"] == 1, muur
    assert lint("- " + ("punt " * 90) + "\n", "beschrijvend")["violations"]["alinea_te_lang"] == 0
    komma = "Het script rekent, zoals hierboven staat beschreven en uitgelegd, met 3,2 tekens."
    assert lint(komma, "beschrijvend")["violations"]["lange_tussenzin"] == 0, komma
    lang = "woord " * 25
    assert lint(lang, "beschrijvend")["violations"]["zin_te_lang"] >= 1
    print("zelftest in orde:", slecht["violations_total"], "overtredingen in de slechte tekst, 0 in de goede")


GEBRUIK = "gebruik: nl_lint.py [--type procedureel|beschrijvend|antwoord] [--gate] (BESTAND|-) | --self-test"


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    gate = "--gate" in args
    if gate:
        args.remove("--gate")
    teksttype = "beschrijvend"
    if "--type" in args:
        i = args.index("--type")
        if i + 1 >= len(args):
            sys.exit("waarde na --type ontbreekt\n" + GEBRUIK)
        teksttype = args[i + 1]
        del args[i:i + 2]
    if teksttype != "antwoord" and teksttype not in GRENZEN:
        sys.exit("onbekend --type %r (verwacht procedureel of beschrijvend)\n%s" % (teksttype, GEBRUIK))
    if len(args) != 1:
        sys.exit(GEBRUIK)
    bron = args[0]
    if bron == "-":
        tekst = sys.stdin.read()
    else:
        try:
            with open(bron, encoding="utf-8") as fh:
                tekst = fh.read()
        except OSError as err:
            sys.exit(str(err))
    rapport = reader_check(tekst) if teksttype == "antwoord" else lint(tekst, teksttype)
    print(json.dumps(rapport, indent=2, ensure_ascii=False))
    totaal = rapport["visible_total"] if teksttype == "antwoord" else rapport["violations_total"]
    return 1 if gate and totaal else 0


if __name__ == "__main__":
    sys.exit(main())
