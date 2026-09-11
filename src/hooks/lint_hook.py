#!/usr/bin/env python3
"""Adviserende schrijfcontrole voor Claude Code. Blokkeert nooit.

PostToolUse (Write of Edit op een .md-bestand): controleer het bestand met
evals/nl_lint.py. Staan er overtredingen in, schrijf dan een korte samenvatting
naar stderr en stop met code 2, zodat het model die samenvatting ziet. Code 2 na
PostToolUse is adviserend, want het hulpmiddel heeft al gedraaid. Markdown van de
agent zelf, zoals geheugenbestanden in de Claude-configuratiemap, slaat het script
over. De schrijfregels gelden daar niet en een samenvatting kost alleen tokens.
Zet EENVOUDIG_NEDERLANDS_LINT_EXCLUDE om meer paden over te slaan.

Stop: lees `last_assistant_message`, controleer het antwoordregister (maximaal vijf
zinnen, punten in een opsomming meegeteld, geen koppen, opsommingen, vet of
gedachtestreepjes) en geef alleen een systemMessage terug als het antwoord de regels
breekt. Stop altijd met code 0, zodat de sessie nooit in een lus komt.
"""
import fnmatch
import json
import os
import pathlib
import re
import sys

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parent.parent
sys.path.insert(0, str(WORTEL / "evals"))

MAX_ZINNEN = 5
CLAUDE_MAP = ".claude"
AANLOOP = re.compile(r"^\s*(zeker[,!]|natuurlijk[,!]|goede vraag|je hebt helemaal gelijk|absoluut[,!]|prima[,!])", re.I)
AFSLUITER = re.compile(r"(ik hoop dat dit helpt|laat het me weten|laat gerust weten|mocht je nog vragen)", re.I)


def laad_linter():
    try:
        import nl_lint  # noqa: WPS433
        return nl_lint
    except Exception:  # noqa: BLE001
        return None


def strip_code(tekst):
    tekst = re.sub(r"```.*?```", " ", tekst, flags=re.S)
    return re.sub(r"`[^`]*`", " ", tekst)


def absoluut(pad, cwd=None):
    """Maak het pad absoluut. De harnas kan het pad relatief aan de sessiemap sturen."""
    return pathlib.Path(cwd or ".", pathlib.Path(pad).expanduser()).absolute()


def varianten(pad):
    """Het pad zoals het er staat en het pad met opgeloste symlinks.

    Een symlink verbergt een mapnaam in twee richtingen. `notities.md` kan naar
    `.claude` wijzen, en `.claude` kan zelf naar een dotfiles-map wijzen. Beide
    vormen moeten buiten de uitsluiting vallen voordat het bestand de linter bereikt.
    """
    return {pathlib.Path(os.path.normpath(pad)), pad.resolve()}


def uitgesloten(doel):
    """Waar voor Markdown van de agent zelf en voor de paden die de gebruiker uitsluit."""
    configmappen = varianten(absoluut(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_MAP}"))
    ruw = os.environ.get("EENVOUDIG_NEDERLANDS_LINT_EXCLUDE", "").split(os.pathsep)
    patronen = [os.path.expanduser(p) for p in ruw if p]
    for vorm in varianten(doel):
        if CLAUDE_MAP in vorm.parts or any(vorm.is_relative_to(d) for d in configmappen):
            return True
        if any(fnmatch.fnmatch(str(vorm), p) for p in patronen):
            return True
    return False


def post_tool_use(gebeurtenis):
    pad = (gebeurtenis.get("tool_input") or {}).get("file_path") or ""
    if not pad.endswith(".md"):
        return 0
    doel = absoluut(pad, gebeurtenis.get("cwd"))
    if uitgesloten(doel):
        return 0
    lint = laad_linter()
    if lint is None:
        return 0
    try:
        tekst = doel.read_text(encoding="utf-8")
    except OSError:
        return 0
    rapport = lint.lint(tekst, "beschrijvend")
    treffers = {k: v for k, v in rapport["violations"].items() if v}
    if not treffers:
        return 0
    samenvatting = ", ".join(f"{k} {v}" for k, v in treffers.items())
    sys.stderr.write(
        f"eenvoudig-nederlands: {doel.name} heeft {rapport['violations_total']} overtredingen "
        f"({samenvatting}). Los deze op in het bestand dat je net schreef en ga daarna verder.\n"
    )
    return 2


def stop(gebeurtenis):
    antwoord = gebeurtenis.get("last_assistant_message") or ""
    problemen = []
    lint = laad_linter()
    if lint is not None:
        c = lint.reader_check(antwoord)["counts"]
        if c["over_cap"]:
            problemen.append(f"{c['sentences']} zinnen, punten in een opsomming meegeteld (grens {MAX_ZINNEN})")
        if c["zin_te_lang"]:
            problemen.append(f"{c['zin_te_lang']} zin boven de 20 woorden")
        for sleutel, label in (("em_dash", "gedachtestreepje"), ("bold_spans", "vet stuk"),
                               ("headers", "kop"), ("puntkomma", "puntkomma"),
                               ("opsomming_in_zin", "opsomming in lopende tekst"),
                               ("punt_meerdere_zinnen", "opsommingspunt met meer dan één zin"),
                               ("spreektaal", "samentrekking")):
            if c[sleutel]:
                problemen.append(f"{c[sleutel]} {label}")
        opsmuk = lint.lint(strip_code(antwoord), "beschrijvend")["violations"].get("opsmukwoord", 0)
        if opsmuk:
            problemen.append(f"{opsmuk} opsmukwoord")
    if AANLOOP.search(antwoord):
        problemen.append("een aanloopje")
    if AFSLUITER.search(antwoord):
        problemen.append("een afsluiter")
    if problemen:
        print(json.dumps({"systemMessage": "eenvoudig-nederlands controle: " + "; ".join(problemen)
                          + ". Antwoord in lopende tekst, met maximaal vijf zinnen."}, ensure_ascii=False))
    return 0


def main():
    try:
        gebeurtenis = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0
    try:
        naam = gebeurtenis.get("hook_event_name", "")
        if naam == "PostToolUse":
            return post_tool_use(gebeurtenis)
        if naam == "Stop":
            return stop(gebeurtenis)
    except Exception:  # noqa: BLE001  adviserende hook: een fout mag de sessie nooit blokkeren
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
