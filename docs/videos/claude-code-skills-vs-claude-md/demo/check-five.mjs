// Checks that the five-procedure CLAUDE.md and the five skills carry the same text, so the two
// arms of the 2026-10-11 runs differ only in where a procedure is kept. No session, no model.
//   node <seed>/check-five.mjs
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const variants = join(dirname(fileURLToPath(import.meta.url)), 'variants');
const read = (name) => readFileSync(join(variants, name), 'utf8');
const five = read('CLAUDE.five.md');
const one = read('CLAUDE.release.md');

// A section of CLAUDE.five.md: the lines under "## <title>" up to the next "## " at column 0.
function section(title) {
  const lines = five.split('\n');
  const start = lines.indexOf(`## ${title}`);
  if (start < 0) return null;
  const rest = lines.slice(start + 1);
  const end = rest.findIndex((line) => /^## /.test(line));
  return (end < 0 ? rest : rest.slice(0, end)).join('\n').trim();
}
// A skill file's body: what follows its "# <title>" line.
function body(name) {
  const text = read(name);
  const title = /^# (.+)$/m.exec(text)[1];
  return { title, text: text.slice(text.indexOf(`# ${title}`) + title.length + 2).trim() };
}

let failed = 0;
const report = (ok, what) => { console.log(`${ok ? 'same' : 'DIFFERENT'} | ${what}`); if (!ok) failed += 1; };
report(five.startsWith(one), 'CLAUDE.five.md begins with CLAUDE.release.md, byte for byte');
for (const name of ['changelog-entry', 'add-converter', 'bug-report', 'readme-example']) {
  const skill = body(`${name}.skill.md`);
  report(section(skill.title) === skill.text, `${name}.skill.md body = CLAUDE.five.md section "${skill.title}"`);
}
const release = body('release-prep.specific.skill.md');
const kept = section(release.title).split('\n');
const differing = release.text.split('\n').filter((line, at) => line !== kept[at]);
console.log(`release-prep.specific.skill.md body against CLAUDE.five.md section "${release.title}": ${differing.length} of ${release.text.split('\n').length} lines differ (step 4 names template.md; CLAUDE.md lists the three headings instead)`);
console.log(`lines: CLAUDE.release.md ${one.trimEnd().split('\n').length}, CLAUDE.five.md ${five.trimEnd().split('\n').length} | characters: ${[...one].length}, ${[...five].length}`);
process.exit(failed ? 1 : 0);
