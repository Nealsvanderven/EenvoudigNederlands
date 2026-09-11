#!/usr/bin/env python3
"""Test zonder pakketten: python3 src/hooks/test_lint_hook.py"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import lint_hook  # noqa: E402


def draai(gebeurtenis):
    """Draai de hook als los proces en geef de afsluitcode en de uitvoer terug."""
    proces = subprocess.run(
        [sys.executable, str(HIER / "lint_hook.py")],
        input=json.dumps(gebeurtenis), text=True, capture_output=True, check=False)
    return proces.returncode, proces.stdout, proces.stderr


def test_uitsluiting():
    thuis = pathlib.Path(os.path.expanduser("~"))
    assert lint_hook.uitgesloten(thuis / ".claude" / "geheugen" / "notitie.md")
    assert lint_hook.uitgesloten(pathlib.Path("/project/.claude/skills/x.md"))
    assert not lint_hook.uitgesloten(pathlib.Path("/project/docs/handleiding.md"))
    os.environ["EENVOUDIG_NEDERLANDS_LINT_EXCLUDE"] = "/project/extern/*"
    try:
        assert lint_hook.uitgesloten(pathlib.Path("/project/extern/vendor.md"))
    finally:
        del os.environ["EENVOUDIG_NEDERLANDS_LINT_EXCLUDE"]


def test_slecht_bestand_geeft_code_2():
    with tempfile.TemporaryDirectory() as map_:
        pad = pathlib.Path(map_) / "slecht.md"
        pad.write_text("Indien de build faalt, dient u middels het logbestand na te gaan "
                       "wat er eenvoudigweg naadloos is misgegaan.\n", encoding="utf-8")
        code, uit, fout = draai({"hook_event_name": "PostToolUse",
                                 "tool_input": {"file_path": str(pad)}})
        assert code == 2, (code, uit, fout)
        assert "eenvoudig-nederlands:" in fout


def test_goed_bestand_geeft_code_0():
    with tempfile.TemporaryDirectory() as map_:
        pad = pathlib.Path(map_) / "goed.md"
        pad.write_text("Als de build mislukt, lees dan het logbestand. "
                       "Daarin staat welke stap de fout gaf.\n", encoding="utf-8")
        code, _, fout = draai({"hook_event_name": "PostToolUse",
                               "tool_input": {"file_path": str(pad)}})
        assert code == 0, (code, fout)


def test_niet_markdown_wordt_overgeslagen():
    code, _, _ = draai({"hook_event_name": "PostToolUse",
                        "tool_input": {"file_path": "/project/src/main.py"}})
    assert code == 0


def test_antwoord_met_opmaak_geeft_melding():
    code, uit, _ = draai({"hook_event_name": "Stop",
                          "last_assistant_message": "**Ja** — dat klopt.\n\n## Waarom\n- Een punt.\n- Twee punten.\n"})
    assert code == 0
    melding = json.loads(uit)["systemMessage"]
    assert "gedachtestreepje" in melding and "kop" in melding


def test_schoon_antwoord_geeft_geen_melding():
    code, uit, _ = draai({"hook_event_name": "Stop",
                          "last_assistant_message": "Ja, dat klopt. De wachtrij liep vol."})
    assert code == 0 and uit.strip() == ""


def test_kapotte_invoer_blokkeert_niet():
    proces = subprocess.run([sys.executable, str(HIER / "lint_hook.py")],
                            input="geen json", text=True, capture_output=True, check=False)
    assert proces.returncode == 0


if __name__ == "__main__":
    for naam, functie in sorted(globals().items()):
        if naam.startswith("test_"):
            functie()
            print("ok", naam)
    print("alle tests in orde")
