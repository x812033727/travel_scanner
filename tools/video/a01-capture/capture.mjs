#!/usr/bin/env node
// Local, read-only A01 evidence capture through the saved PuTTY session.
import { createHash } from 'node:crypto';
import { createReadStream, createWriteStream } from 'node:fs';
import { lstat, mkdir, readFile, realpath, stat, writeFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { pipeline } from 'node:stream/promises';
import { dirname, isAbsolute, join, parse, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SLUG = 'story-rolling-suitcase-v2';
const HERE = dirname(fileURLToPath(import.meta.url));
const SESSION = 'hostinger2';
const DEFAULT_PLINK = 'C:\\Program Files\\PuTTY\\plink.exe';
const REMOTE = Object.freeze({
  state: 'cd /root/travel_scanner && bash -se',
  archive: 'cd /root/travel_scanner && bash -se',
  db: 'cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T postgres psql -X -q -t -A -U travel -d travel_scanner -v ON_ERROR_STOP=1 -f -',
  budget: 'cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2',
});

function parseArgs(args) {
  if (args.length === 1 && args[0] === '--help') return { help: true };
  const options = {};
  for (let index = 0; index < args.length; index += 2) {
    const key = args[index];
    if (!['--out', '--plink'].includes(key) || !args[index + 1] || options[key]) {
      throw new Error('ARGUMENTS');
    }
    options[key] = args[index + 1];
  }
  if (!options['--out']) throw new Error('OUT_REQUIRED');
  return { out: options['--out'], plink: options['--plink'] ?? DEFAULT_PLINK };
}

async function exists(path) {
  try { await lstat(path); return true; }
  catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}

export async function checkDestination(target) {
  if (!isAbsolute(target)) throw new Error('OUT_NOT_ABSOLUTE');
  const normalized = resolve(target);
  if (await exists(normalized)) throw new Error('OUT_ALREADY_EXISTS');
  const parent = dirname(normalized);
  if ((await realpath(parent)).toLowerCase() !== parent.toLowerCase()) {
    throw new Error('OUT_PARENT_NOT_CANONICAL');
  }
  for (let current = parent; ; current = dirname(current)) {
    const info = await lstat(current);
    if (info.isSymbolicLink() || !info.isDirectory()) throw new Error('OUT_PARENT_LINKED');
    if (await exists(join(current, '.git'))) throw new Error('OUT_INSIDE_REPOSITORY');
    if (current === parse(current).root) break;
  }
  return normalized;
}

async function sha256File(path) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(path)) hash.update(chunk);
  const info = await stat(path);
  return { sha256: hash.digest('hex'), bytes: info.size };
}

export async function captureStep(plink, out, name, remote, input, spawnChild = spawn) {
  const path = join(out, name);
  const child = spawnChild(plink, ['-batch', '-T', '-load', SESSION, '-l', 'root', remote], {
    windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'],
  });
  child.stderr.resume(); // Never print credentials, responses or vendor IDs.
  child.stdin.on('error', () => {}); // A failed batch SSH can close stdin early.
  const timeout = setTimeout(() => child.kill(), 600_000);
  const closed = new Promise((resolveClose, rejectClose) => {
    child.once('error', rejectClose);
    child.once('close', (code, signal) => resolveClose({ code, signal }));
  });
  const copied = pipeline(child.stdout, createWriteStream(path, { flags: 'wx', mode: 0o600 }));
  child.stdin.end(input ?? '');
  try {
    const [exit] = await Promise.all([closed, copied]);
    if (exit.code !== 0) throw new Error('REMOTE_STEP_FAILED');
    const info = await sha256File(path);
    if (info.bytes === 0) throw new Error('EMPTY_REMOTE_OUTPUT');
    return info;
  } finally {
    clearTimeout(timeout);
  }
}

export function parseJsonOutput(contents, name) {
  const lines = contents.trim().split(/\r?\n/).map(line => line.trim()).filter(Boolean);
  if (lines.length !== 1 || !lines[0].startsWith('{') || !lines[0].endsWith('}')) {
    throw new Error(`${name}_NOT_SINGLE_JSON`);
  }
  return JSON.parse(lines[0]);
}

export function parseHostState(contents) {
  const lines = contents.trim().split(/\r?\n/);
  if (lines.length !== 3 || !/^GIT [a-f0-9]{40}$/.test(lines[0])
      || !/^DEPLOY_HOLD (present|absent)$/.test(lines[1])) {
    throw new Error('HOST_STATE_FORMAT');
  }
  const worker = JSON.parse(lines[2]);
  return { git_sha: lines[0].slice(4), deploy_hold: lines[1].slice(12), worker };
}

export function assess(before, after, dbBefore, dbAfter, budgetBefore, budgetAfter) {
  const issues = [];
  if (JSON.stringify(before) !== JSON.stringify(after)) issues.push('HOST_STATE_DRIFT');
  if (JSON.stringify(dbBefore) !== JSON.stringify(dbAfter)) issues.push('DB_DRIFT');
  if (JSON.stringify(budgetBefore) !== JSON.stringify(budgetAfter)) issues.push('BUDGET_DRIFT');
  const state = after?.worker;
  if (state?.slug !== SLUG || !Array.isArray(state.audit_events)
      || state.audit_events.length < 104
      || state.audit_events.some(item => !item.index?.present)) issues.push('AUDIT_INCOMPLETE');
  if (dbAfter?.episode?.slug !== SLUG || dbAfter?.project?.slug !== SLUG
      || !dbAfter?.series || !Array.isArray(dbAfter?.a01_stage_jobs)
      || !Array.isArray(dbAfter?.a01_media_jobs)
      || !Array.isArray(dbAfter?.global_nonterminal_stage_jobs)
      || !Array.isArray(dbAfter?.global_nonterminal_media_jobs)) issues.push('DB_INCOMPLETE');
  if (budgetAfter?.slug !== SLUG || !Array.isArray(budgetAfter.operations)) {
    issues.push('BUDGET_INCOMPLETE');
  } else if (Number(budgetAfter.limit_usd) !== 25
      || Number(budgetAfter.reserved_usd) !== 0
      || Number(budgetAfter.settled_usd) !== 0
      || budgetAfter.operations.length !== 0) {
    issues.push('BUDGET_CHANGED');
  }
  if (before.deploy_hold !== 'absent' || after.deploy_hold !== 'absent') {
    issues.push('DEPLOY_HOLD_PRESENT');
  }
  if (state?.controls?.a01_lease?.present) issues.push('A01_LEASE_PRESENT');
  if (!state?.controls?.a01_stop?.present) issues.push('A01_STOP_MISSING');
  if (dbAfter?.global_nonterminal_stage_jobs?.length
      || dbAfter?.global_nonterminal_media_jobs?.length) issues.push('GLOBAL_JOB_ACTIVE');
  if (dbAfter?.a01_stage_jobs?.some(job =>
    !['succeeded', 'failed', 'canceled', 'cancelled'].includes(job?.status))) {
    issues.push('A01_STAGE_UNRESOLVED');
  }
  if (dbAfter?.a01_media_jobs?.length) issues.push('A01_MEDIA_EXISTS');
  return [...new Set(issues)];
}

export function finalizeCaptureReport(report, issues) {
  report.issues = issues;
  report.capture_consistent = issues.length === 0;
  report.capture_complete = Object.keys(report.files).length === 7;
  report.operational_gate = issues.length ? 'HOLD' : 'REVIEW_REQUIRED';
  return report;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write('node tools/video/a01-capture/capture.mjs --out C:\\absolute\\new-folder [--plink C:\\path\\plink.exe]\n');
    return;
  }
  const out = await checkDestination(args.out);
  if (!isAbsolute(args.plink) || !(await stat(args.plink)).isFile()) {
    throw new Error('PLINK_NOT_FOUND');
  }
  await mkdir(out, { mode: 0o700 });
  const report = {
    schema_version: 1, slug: SLUG, status: 'HOLD', production_adoption_allowed: false,
    started_at: new Date().toISOString(), files: {}, issues: [],
    capture_complete: false, operational_gate: 'HOLD',
  };
  try {
    const stateScript = await readFile(join(HERE, 'host-state.sh'));
    const archiveScript = await readFile(join(HERE, 'archive.sh'));
    const sql = await readFile(join(HERE, 'readback.sql'));
    const steps = [
      ['host-state-before.txt', REMOTE.state, stateScript],
      ['db-before.json', REMOTE.db, sql],
      ['budget-before.json', REMOTE.budget, null],
      ['a01-source.tar', REMOTE.archive, archiveScript],
      ['host-state-after.txt', REMOTE.state, stateScript],
      ['db-after.json', REMOTE.db, sql],
      ['budget-after.json', REMOTE.budget, null],
    ];
    for (const [name, remote, input] of steps) {
      report.files[name] = await captureStep(args.plink, out, name, remote, input);
    }
    const [before, after, dbBefore, dbAfter, budgetBefore, budgetAfter] = await Promise.all([
      readFile(join(out, 'host-state-before.txt'), 'utf8').then(parseHostState),
      readFile(join(out, 'host-state-after.txt'), 'utf8').then(parseHostState),
      readFile(join(out, 'db-before.json'), 'utf8').then(text => parseJsonOutput(text, 'DB_BEFORE')),
      readFile(join(out, 'db-after.json'), 'utf8').then(text => parseJsonOutput(text, 'DB_AFTER')),
      readFile(join(out, 'budget-before.json'), 'utf8').then(text => parseJsonOutput(text, 'BUDGET_BEFORE')),
      readFile(join(out, 'budget-after.json'), 'utf8').then(text => parseJsonOutput(text, 'BUDGET_AFTER')),
    ]);
    finalizeCaptureReport(report,
      assess(before, after, dbBefore, dbAfter, budgetBefore, budgetAfter));
    report.audit_events = after.worker.audit_events.length;
    report.release_sha = after.git_sha;
  } catch (error) {
    report.issues.push(error?.message?.startsWith('REMOTE_') ? error.message : 'CAPTURE_FAILED');
    report.capture_consistent = false;
  }
  report.files_captured = Object.keys(report.files).length;
  report.finished_at = new Date().toISOString();
  await writeFile(join(out, 'capture-report.json'), JSON.stringify(report, null, 2) + '\n', {
    flag: 'wx', mode: 0o600,
  });
  process.stdout.write(`A01 read-only capture: ${out}\nStatus: HOLD; `
    + `files_captured=${report.files_captured}/7; `
    + `capture_complete=${report.capture_complete}; `
    + `issues=${report.issues.length ? report.issues.join(',') : 'none'}\n`);
  if (!report.capture_complete) process.exitCode = 2;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => {
    process.stderr.write(`Capture not started: ${error.message}\n`);
    process.exitCode = 2;
  });
}
