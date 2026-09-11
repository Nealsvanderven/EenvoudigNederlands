#!/usr/bin/env python3
"""Tel tekens, woorden en tokens van een tekst, en vergelijk twee teksten.

Is tiktoken geïnstalleerd, dan telt het script echte tokens met de codering
o200k_base. Ontbreekt tiktoken, dan schat het script het aantal tokens met
een deler. De standaarddeler is 3,2 tekens per token. Dat is de orde van
grootte voor Nederlands proza bij de coderingen die de grote taalmodellen
gebruiken. Engels haalt ongeveer 4 tekens per token, Nederlands minder,
want Nederlandse woorden zijn langer en samenstellingen vallen uiteen.

Een schatting is geen meting. Zeg dat erbij als je het getal gebruikt.

Gebruik:
  python3 tokens.py bestand.md
  python3 tokens.py --vergelijk voor.md na.md
  cat tekst.md | python3 tokens.py -
  python3 tokens.py --self-test
"""
import json
import sys

TEKENS_PER_TOKEN = 3.2


def codering():
    try:
        import tiktoken
        return tiktoken.get_encoding("o200k_base")
    except Exception:
        return None


def tel(tekst, enc=None):
    tekens = len(tekst)
    woorden = len(tekst.split())
    if enc is not None:
        tokens = len(enc.encode(tekst))
        bron = "tiktoken o200k_base"
    else:
        tokens = round(tekens / TEKENS_PER_TOKEN)
        bron = "schatting %s tekens per token" % str(TEKENS_PER_TOKEN).replace(".", ",")
    return {"tekens": tekens, "woorden": woorden, "tokens": tokens, "bron": bron}


def vergelijk(voor, na, enc=None):
    a = tel(voor, enc)
    b = tel(na, enc)
    verschil = a["tokens"] - b["tokens"]
    procent = round(100.0 * verschil / max(1, a["tokens"]), 1)
    return {"voor": a, "na": b, "tokens_bespaard": verschil, "procent_bespaard": procent}


def lees(pad):
    if pad == "-":
        return sys.stdin.read()
    with open(pad, encoding="utf-8") as fh:
        return fh.read()


def self_test():
    r = tel("een twee drie", None)
    assert r["woorden"] == 3 and r["tekens"] == 13, r
    v = vergelijk("a" * 320, "a" * 160, None)
    assert v["tokens_bespaard"] == 50 and v["procent_bespaard"] == 50.0, v
    print("zelftest in orde")


GEBRUIK = "gebruik: tokens.py (BESTAND|-) | --vergelijk VOOR NA | --self-test"


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    enc = codering()
    if "--vergelijk" in args:
        args.remove("--vergelijk")
        if len(args) != 2:
            sys.exit(GEBRUIK)
        rapport = vergelijk(lees(args[0]), lees(args[1]), enc)
    else:
        if len(args) != 1:
            sys.exit(GEBRUIK)
        rapport = tel(lees(args[0]), enc)
    print(json.dumps(rapport, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
