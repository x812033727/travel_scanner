// Runner: the logging hook prints the last four characters of each tool-call id ("id=XXXX").
// This writes them "id=cN", N being the order in which an id first appears; "id=----" (an event
// without an id) is left as it is. stdin to stdout.
import { readFileSync } from 'node:fs';

const seen = new Map();
const out = readFileSync(0, 'utf8').replace(/\bid=([A-Za-z0-9_-]{4})(?= )/g, (whole, id) => {
  if (id === '----') return whole;
  if (!seen.has(id)) seen.set(id, seen.size + 1);
  return `id=c${seen.get(id)}`;
});
process.stdout.write(out);
