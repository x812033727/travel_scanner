// Prints one settings file made of two: the logging hook and a rules file (the "local" arm puts
// both in .claude/settings.local.json). No session, no model.
// Usage: node merge.mjs <hooks.json> <rules.json>
import { readFileSync } from 'node:fs';

const [hooks, rules] = process.argv.slice(2).map((file) => JSON.parse(readFileSync(file, 'utf8')));
console.log(JSON.stringify({ ...rules, ...hooks }, null, 2));
