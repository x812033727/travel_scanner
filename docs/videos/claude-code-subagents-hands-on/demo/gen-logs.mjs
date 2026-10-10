// Writes the six log files of the practice project and the list of what is planted in them.
// Deterministic: a fixed pseudo-random generator, and the first seed whose result meets the
// constraints below. Running it again writes the same bytes. It is NOT copied into the practice
// project, and neither is truth.json: a session must work the answer out from the logs.
// No session, no model.
// Usage: node <seed>/gen-logs.mjs          (rewrites log-lab/logs/ and truth.json)
//        node <seed>/gen-logs.mjs --check  (writes nothing; exits 1 if the files on disk differ)
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seedDir = dirname(fileURLToPath(import.meta.url));
const DAYS = ['2026-10-01', '2026-10-02', '2026-10-03', '2026-10-04', '2026-10-05', '2026-10-06'];
const KINDS = ['resize', 'thumb', 'geotag', 'export'];
const CRASHES = 7; // jobs that start and never log done
const WORKERS = 3;

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const clock = (second) => [Math.floor(second / 3600), Math.floor(second / 60) % 60, second % 60]
  .map((part) => String(part).padStart(2, '0')).join(':');

function build(seed) {
  const random = mulberry32(seed);
  const pick = (low, high) => low + Math.floor(random() * (high - low + 1));
  const end = DAYS.length * 86400;
  const lines = DAYS.map(() => []);
  const say = (at, text) => lines[Math.floor(at / 86400)].push(`${clock(at % 86400)} ${text}`);
  const jobs = [];
  const active = [];
  let now = pick(20, 200);
  let next = 1001;
  // Which jobs crash: one in every stretch of about thirty, at a position the generator draws.
  const crashAt = new Set();
  while (crashAt.size < CRASHES) crashAt.add(1001 + crashAt.size * 30 + pick(4, 26));
  while (now < end) {
    const closing = now > end - 3600; // the last hour starts nothing new, so every live job can end
    const roll = random();
    if (active.length < WORKERS && !closing && roll < 0.3) {
      const job = { id: `J${next}`, steps: pick(1, 3), at: 0, crash: crashAt.has(next), startDay: Math.floor(now / 86400), startLine: 0, retried: false };
      next += 1;
      job.dieAfter = job.crash ? pick(0, job.steps) : -1;
      say(now, `start ${job.id} ${KINDS[pick(0, 3)]} IMG_${String(pick(1, 9999)).padStart(4, '0')}.jpg`);
      job.startLine = lines[job.startDay].length;
      jobs.push(job);
      if (job.crash && job.dieAfter === 0) job.dead = true; else active.push(job);
    } else if (active.length && (roll < 0.9 || closing)) {
      const job = active[pick(0, active.length - 1)];
      if (!job.retried && random() < 0.12) {
        job.retried = true;
        say(now, `retry ${job.id} ${random() < 0.5 ? 'timeout' : 'disk-busy'}`);
      } else if (job.at < job.steps) {
        job.at += 1;
        say(now, `step  ${job.id} ${job.at}/${job.steps}`);
        if (job.crash && job.at >= job.dieAfter) { job.dead = true; active.splice(active.indexOf(job), 1); }
      } else {
        say(now, `done  ${job.id} ${pick(180, 4200)}ms`);
        job.doneDay = Math.floor(now / 86400);
        active.splice(active.indexOf(job), 1);
      }
    } else {
      say(now, `beat  queue=${pick(0, 6)} workers=${active.length}`);
    }
    now += closing && active.length ? pick(20, 90) : pick(120, 760);
  }
  const file = (day) => `logs/queue-${DAYS[day]}.log`;
  const unfinished = jobs.filter((job) => job.doneDay === undefined);
  const crossFile = jobs.filter((job) => job.doneDay !== undefined && job.doneDay !== job.startDay);
  return {
    seed, lines, jobs: jobs.length,
    stillActive: active.length,
    unfinished: unfinished.map((job) => ({ id: job.id, file: file(job.startDay), line: job.startLine })),
    crossFile: crossFile.map((job) => ({ id: job.id, startFile: file(job.startDay), doneFile: file(job.doneDay) })),
    retriedAndDone: jobs.filter((job) => job.retried && job.doneDay !== undefined).length,
    files: DAYS.map((_, day) => file(day)),
  };
}

function acceptable(result) {
  const sizes = result.lines.map((each) => each.length);
  const spread = new Set(result.unfinished.map((job) => job.file)).size;
  return result.stillActive === 0 && result.unfinished.length === CRASHES && spread >= 4
    && result.crossFile.length >= 2 && result.crossFile.length <= 3
    && sizes.every((size) => size >= 185 && size <= 215);
}

let result;
for (let seed = 1; seed < 5000; seed += 1) {
  result = build(seed);
  if (acceptable(result)) break;
  result = null;
}
if (!result) { console.error('no seed under 5000 meets the constraints'); process.exit(2); }

const texts = result.lines.map((each) => `${each.join('\n')}\n`);
const truth = {
  note: 'What gen-logs.mjs planted. Not copied into the practice project.',
  generatorSeed: result.seed,
  jobs: result.jobs,
  unfinished: result.unfinished,
  finishedInTheNextFile: result.crossFile,
  retriedAndStillDone: result.retriedAndDone,
};
const truthText = `${JSON.stringify(truth, null, 2)}\n`;
const sha = (text) => createHash('sha256').update(text).digest('hex').slice(0, 16);

if (process.argv.includes('--check')) {
  let same = true;
  result.files.forEach((name, at) => {
    const path = join(seedDir, 'log-lab', name);
    const ok = existsSync(path) && readFileSync(path, 'utf8') === texts[at];
    if (!ok) same = false;
    console.log(`${ok ? 'same     ' : 'DIFFERENT'} log-lab/${name}`);
  });
  const ok = existsSync(join(seedDir, 'truth.json')) && readFileSync(join(seedDir, 'truth.json'), 'utf8') === truthText;
  if (!ok) same = false;
  console.log(`${ok ? 'same     ' : 'DIFFERENT'} truth.json`);
  process.exit(same ? 0 : 1);
}

mkdirSync(join(seedDir, 'log-lab', 'logs'), { recursive: true });
result.files.forEach((name, at) => writeFileSync(join(seedDir, 'log-lab', name), texts[at]));
writeFileSync(join(seedDir, 'truth.json'), truthText);
console.log(`generator seed ${result.seed} | ${result.jobs} jobs | ${texts.reduce((sum, text) => sum + text.length, 0)} bytes`);
result.files.forEach((name, at) => console.log(`${sha(texts[at])}  ${String(result.lines[at].length).padStart(4)} lines  ${name}`));
console.log(`unfinished (${truth.unfinished.length}): ${truth.unfinished.map((job) => `${job.id} ${job.file.slice(11, 21)}:${job.line}`).join(', ')}`);
console.log(`finished in the next file (${truth.finishedInTheNextFile.length}): ${truth.finishedInTheNextFile.map((job) => job.id).join(', ')}`);
console.log(`retried and still done: ${truth.retriedAndStillDone}`);
