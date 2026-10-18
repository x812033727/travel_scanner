// Measures every seed file: SHA-256 (first 16 hex digits), lines, the longest line in characters
// and in terminal columns (East Asian wide characters count two), whether it has a BOM or CR,
// and whether it fits a card: 64 columns for the files a code card shows, 44 visible characters
// for the requests a chat card shows. No session, no model.
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
// The coordinator's own scripts are not shown on cards; neither are the hand-test input (one
// JSON-RPC message per line cannot be wrapped) and the ten-tool server of the "wide" arms.
const shown = (name) => /^(gear-lab|hook-log|prompts)\/|^variants\/mcp\./.test(name) && !name.endsWith('hand.jsonl');

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
  const request = name.startsWith('prompts/');
  const fits = request ? [...text.trim()].length <= 44 : widest <= 64;
  const card = !shown(name) ? '-   ' : fits ? 'fits' : 'WIDE';
  console.log(`${hash}  ${String(lines.length).padStart(5)}  ${String(longest).padStart(9)}  ${String(widest).padStart(11)}  ${bom ? 'yes' : 'no '}  ${text.includes('\r') ? 'yes' : 'no'}  ${card}  ${name}`);
  if (card === 'WIDE') console.log(`                  lines over 64 columns: ${lines.map((line, at) => (columns(line) > 64 ? `${at + 1} (${columns(line)})` : null)).filter(Boolean).join(', ')}`);
  if (name.startsWith('prompts/')) console.log(`                  visible characters (a chat card holds 44): ${[...text.trim()].length}`);
}
