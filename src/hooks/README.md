# Hooks

Twee hooks, allebei adviserend. Ze blokkeren nooit een sessie.

## eenvoudig-nederlands-activate.js

Draait bij SessionStart. Het script leest `prompts/system-prompt.md`, haalt het regelblok tussen de eerste twee scheidingslijnen eruit en schrijft dat naar stdout. Claude Code voegt die uitvoer toe aan de context van de sessie.

Claude Code kapt de uitvoer van een hook af op 10.000 tekens. Blijft het blok boven 9500 tekens, dan schrijft het script een korte terugvalregelset en een waarschuwing naar stderr.

Test: `node src/hooks/eenvoudig-nederlands-activate.test.js`

## lint_hook.py

Draait bij PostToolUse (Write en Edit) en bij Stop.

Bij PostToolUse controleert het script een Markdown-bestand met `evals/nl_lint.py`. Staan er overtredingen in, dan schrijft het een samenvatting naar stderr en stopt het met code 2. Code 2 na PostToolUse is adviserend, want het hulpmiddel heeft al gedraaid. Het model leest de samenvatting en kan het bestand herstellen.

Bij Stop controleert het script het laatste antwoord op het antwoordregister: maximaal vijf zinnen, geen koppen, opsommingen, vet of gedachtestreepjes. Het script stopt altijd met code 0, zodat de sessie nooit in een lus komt.

Markdown van de agent zelf slaat het script over. Dat zijn bestanden in `.claude` en in de map die `CLAUDE_CONFIG_DIR` aanwijst. Zet `EENVOUDIG_NEDERLANDS_LINT_EXCLUDE` om meer paden over te slaan. Scheid de patronen met een dubbele punt:

```
export EENVOUDIG_NEDERLANDS_LINT_EXCLUDE="$HOME/notities/*:/project/vendor/*"
```

Test: `python3 src/hooks/test_lint_hook.py`
