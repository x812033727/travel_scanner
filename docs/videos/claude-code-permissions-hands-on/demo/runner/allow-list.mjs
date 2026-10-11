// Prints the allow rules of a rules file, one a line, for --allowedTools.
// With --count: how many allow, ask and deny rules a settings file holds (0 0 0 for none).
// Usage: node allow-list.mjs [--count] <file>
import { existsSync, readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const count = args[0] === '--count';
const file = args.at(-1);
const permissions = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')).permissions ?? {} : {};
if (count) {
  console.log(`allow ${(permissions.allow ?? []).length}, ask ${(permissions.ask ?? []).length}, deny ${(permissions.deny ?? []).length}`);
} else {
  for (const rule of permissions.allow ?? []) console.log(rule);
}
