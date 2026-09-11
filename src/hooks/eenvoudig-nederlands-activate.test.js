#!/usr/bin/env node
// Test zonder pakketten: node src/hooks/eenvoudig-nederlands-activate.test.js
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const m = require('./eenvoudig-nederlands-activate.js');

const WORTEL = path.join(__dirname, '..', '..');

// Zonder prompt valt de hook terug op de korte regelset.
assert.strictEqual(m.bouwContext(''), m.TERUGVAL);

// De frontmatter gaat eraf.
assert.strictEqual(m.zonderFrontmatter('---\nnaam: test\n---\ntekst\n'), 'tekst\n');

// Alleen het blok tussen de eerste twee scheidingslijnen gaat mee.
assert.strictEqual(m.regelblok('kop\n\n---\n\nregels\n\n---\n\nrest\n').trim(), 'regels');

// Het echte bestand levert een blok onder de grens op.
const prompt = fs.readFileSync(path.join(WORTEL, 'prompts', 'system-prompt.md'), 'utf8');
const uit = m.bouwContext(prompt);
assert.ok(uit.length <= m.MAX_TEKENS, `blok is ${uit.length} tekens`);
assert.ok(uit.startsWith('SKILL EENVOUDIG NEDERLANDS AUTOMATISCH ACTIEF'));
assert.ok(uit.includes('taalniveau B1'));
assert.ok(uit.includes('maximaal vijf zinnen') || uit.includes('vijf zinnen'));
assert.ok(!uit.includes('Korte versie'), 'de korte versie hoort er niet in te staan');

// Een blok boven de grens valt terug op de korte regelset.
const tegroot = 'kop\n\n---\n\n' + 'a'.repeat(m.MAX_TEKENS + 10) + '\n\n---\n';
assert.strictEqual(m.bouwContext(tegroot), m.TERUGVAL);

// Een ontbrekend bestand levert een lege tekst op.
assert.strictEqual(m.leesEersteBestand(['/bestaat/niet.md']), '');

console.log('zelftest in orde:', uit.length, 'tekens in het blok');
