// Measures every seed file: SHA-256 (first 16 hex digits), lines, the longest line in characters
// and in terminal columns (East Asian wide characters count two), whether it has a BOM or CR,
// and whether it fits a card: 64 columns for the files a code card shows. It also looks for
// anything a secret scanner would stop at. No session, no model.
// Usage: node <seed>/measure-seed.mjs
import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const walk = (dir) => readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  return statSync(path).isDirectory() ? walk(path) : [path];
});
const columns = (text) => [...text].reduce((total, char) => {
  const code = char.codePointAt(0);
  const wide = (code >= 0x1100 && code <= 0x115f) || (code >= 0x2e80 && code <= 0xa4cf) || (code >= 0xac00 && code <= 0xd7a3) ||
    (code >= 0xf900 && code <= 0xfaff) || (code >= 0xfe30 && code <= 0xfe4f) || (code >= 0xff00 && code <= 0xff60) || (code >= 0xffe0 && code <= 0xffe6) || code >= 0x20000;
  return total + (wide ? 2 : 1);
}, 0);
// The coordinator's own scripts are not shown on cards; the project, the rules, the placed files,
// the requests and the logging hook's script are. hooks.json is shown as an excerpt at most.
const shown = (name) => /^(lab|rules|placed|prompts)\//.test(name) || name === 'hook-log/seen.mjs';
// Shapes of real keys: none may appear anywhere in the seed.
const KEYLIKE = /sk-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{8,}|-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-|eyJ[A-Za-z0-9_-]{10,}\./;

let bad = 0;
const names = [];
console.log('sha256[0:16]      lines  max chars  max columns  bom  cr  card  file');
for (const file of walk(seed).sort()) {
  const bytes = readFileSync(file);
  const text = bytes.toString('utf8');
  const lines = text.replace(/\n$/, '').split('\n');
  const hash = createHash('sha256').update(bytes).digest('hex').slice(0, 16);
  const longest = Math.max(...lines.map((line) => line.length));
  const widest = Math.max(...lines.map(columns));
  const bom = bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf;
  const name = relative(seed, file).replaceAll('\\', '/');
  names.push(name);
  const card = !shown(name) ? '-   ' : widest <= 64 ? 'fits' : 'WIDE';
  if (card === 'WIDE' || bom || text.includes('\r') || KEYLIKE.test(text)) bad += 1;
  console.log(`${hash}  ${String(lines.length).padStart(5)}  ${String(longest).padStart(9)}  ${String(widest).padStart(11)}  ${bom ? 'yes' : 'no '}  ${text.includes('\r') ? 'yes' : 'no'}  ${card}  ${name}${KEYLIKE.test(text) ? '  <- KEY-SHAPED STRING' : ''}`);
  if (card === 'WIDE') console.log(`                  lines over 64 columns: ${lines.map((line, at) => (columns(line) > 64 ? `${at + 1} (${columns(line)})` : null)).filter(Boolean).join(', ')}`);
}
const forbidden = names.filter((name) => /\.test\.|\.log$|(^|\/)\.claude\/|(^|\/)settings(\.local)?\.json$|(^|\/)\.env|(^|\/)\.mcp\.json$|(^|\/)CLAUDE\.md$/.test(name));
console.log(`files: ${names.length} | names a repository would mind (*.test.*, *.log, .claude/, settings.json, .env*, .mcp.json, CLAUDE.md): ${forbidden.length ? forbidden.join(' ') : 'none'} | key-shaped strings, BOM, CR or too-wide card files: ${bad}`);
process.exitCode = bad || forbidden.length ? 1 : 0;
