// Works the answer out from the six log files a second way, without the generator, and compares
// it with truth.json: every job id that has a start line and no done line anywhere. Also shows
// what a reader who judged each file by itself would report, which is the planted trap.
// No session, no model.
// Usage: node <seed>/check-logs.mjs
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const dir = join(seed, 'log-lab', 'logs');
const truth = JSON.parse(readFileSync(join(seed, 'truth.json'), 'utf8'));
const started = new Map();
const done = new Set();
const perFile = [];
let lines = 0;
let bytes = 0;
const verbs = {};
for (const name of readdirSync(dir).sort()) {
  const text = readFileSync(join(dir, name), 'utf8');
  bytes += text.length;
  const startedHere = new Set();
  const doneHere = new Set();
  text.replace(/\n$/, '').split('\n').forEach((line, at) => {
    lines += 1;
    const [, verb, job] = line.split(/\s+/);
    verbs[verb] = (verbs[verb] ?? 0) + 1;
    if (verb === 'start') { started.set(job, `logs/${name}:${at + 1}`); startedHere.add(job); }
    if (verb === 'done') { done.add(job); doneHere.add(job); }
  });
  perFile.push(...[...startedHere].filter((job) => !doneHere.has(job)));
}
const unfinished = [...started.keys()].filter((job) => !done.has(job));
const planted = truth.unfinished.map((job) => job.id);
const nextFile = truth.finishedInTheNextFile.map((job) => job.id);
const same = (a, b) => a.length === b.length && a.every((each) => b.includes(each));
console.log(`${lines} lines, ${bytes} bytes, ${started.size} jobs started | lines by verb: ${Object.entries(verbs).map(([verb, count]) => `${verb} ${count}`).join(', ')}`);
console.log(`start without done anywhere (${unfinished.length}): ${unfinished.map((job) => `${job} ${started.get(job).slice(11)}`).join(', ')}`);
console.log(`the same as truth.json, ids and start lines: ${same(unfinished, planted) && truth.unfinished.every((job) => started.get(job.id) === `${job.file}:${job.line}`) ? 'yes' : 'NO'}`);
console.log(`judging each file by itself (${perFile.length}): ${perFile.join(' ')}`);
console.log(`the extra ones are the jobs that finish in the next file: ${same(perFile.filter((job) => !planted.includes(job)), nextFile) ? 'yes' : 'NO'} (${nextFile.join(' ')})`);
console.log(`done without a start in any file: ${[...done].filter((job) => !started.has(job)).length}`);
process.exitCode = same(unfinished, planted) ? 0 : 1;
