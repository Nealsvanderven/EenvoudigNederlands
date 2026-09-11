#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

// Claude Code kapt de uitvoer van een hook af op 10.000 tekens. Alles daarboven
// gaat naar een bestand en wordt vervangen door een voorbeeld. Dan werkt de hook niet meer.
const MAX_TEKENS = 9500;

const TERUGVAL = `SKILL EENVOUDIG NEDERLANDS AUTOMATISCH ACTIEF

Schrijf Nederlands op taalniveau B1. Gebruik korte zinnen, de actieve vorm, werkwoordstijl in plaats van naamwoordstijl, en zet de voorwaarde voor de opdracht. Vermijd ambtelijke woorden en tangconstructies. Raak code, functienamen, commando's en geciteerde foutmeldingen niet aan. Antwoord in de chat in lopende tekst, met maximaal vijf zinnen.`;

const KOP = [
  'SKILL EENVOUDIG NEDERLANDS AUTOMATISCH ACTIEF',
  '',
  'Volg deze schrijfregels zonder te wachten tot de gebruiker de skill noemt. De volledige skill staat in skills/eenvoudig-nederlands/SKILL.md in deze plugin, met de regelcatalogus en de controlemodus. Lees dat bestand voor een controle of voor de modus Strikt.',
  '',
].join('\n');

function kandidaten(pluginRoot, hookMap, relatief) {
  const wortels = [];
  if (pluginRoot) {
    wortels.push(pluginRoot);
  }
  wortels.push(path.join(hookMap, '..', '..'), path.join(hookMap, '..'));
  return wortels.map((wortel) => path.join(wortel, ...relatief));
}

function promptKandidaten(pluginRoot, hookMap) {
  return kandidaten(pluginRoot, hookMap, ['prompts', 'system-prompt.md']);
}

function leesEersteBestand(lijst) {
  for (const kandidaat of lijst) {
    try {
      return fs.readFileSync(kandidaat, 'utf8');
    } catch (fout) {
      // Bestand ontbreekt, is onleesbaar of is een map: probeer de volgende.
    }
  }
  return '';
}

function zonderFrontmatter(inhoud) {
  return inhoud.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '');
}

// prompts/system-prompt.md is een pagina voor mensen: een titel, een alinea die zegt
// waar je het blok plakt, het regelblok tussen twee "---" regels, en daarna een korte
// versie. Het model krijgt alleen het blok ertussen.
function regelblok(inhoud) {
  const scheiding = /^---[ \t]*\r?$/m;
  const eerste = inhoud.search(scheiding);
  if (eerste === -1) {
    return inhoud;
  }
  const rest = inhoud.slice(eerste).replace(scheiding, '');
  const tweede = rest.search(scheiding);
  return tweede === -1 ? rest : rest.slice(0, tweede);
}

function bouwContext(promptTekst) {
  if (!promptTekst) {
    return TERUGVAL;
  }
  const uit = KOP + regelblok(zonderFrontmatter(promptTekst)).trim();
  if (uit.length > MAX_TEKENS) {
    process.stderr.write(`eenvoudig-nederlands hook: het blok is ${uit.length} tekens en dat is meer dan de grens van ${MAX_TEKENS}. De korte regelset gaat mee.\n`);
    return TERUGVAL;
  }
  return uit;
}

function main() {
  const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT;
  process.stdout.write(bouwContext(leesEersteBestand(promptKandidaten(pluginRoot, __dirname))));
}

if (require.main === module) {
  main();
}

module.exports = {
  TERUGVAL,
  MAX_TEKENS,
  bouwContext,
  promptKandidaten,
  leesEersteBestand,
  regelblok,
  zonderFrontmatter,
};
