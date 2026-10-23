import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { test } from 'node:test';
import { EventEmitter } from 'node:events';
import { PassThrough } from 'node:stream';
import { assess, captureStep, checkDestination, finalizeCaptureReport, parseHostState,
  parseJsonOutput, SLUG } from './capture.mjs';

function fixture() {
  const state = {
    git_sha: 'a'.repeat(40),
    deploy_hold: 'absent',
    worker: {
      slug: SLUG,
      audit_events: Array.from({ length: 104 }, (_, index) => ({
        name: 'event-' + index, index: { present: true },
      })),
      controls: {
        a01_stop: { present: true },
        a01_lease: { present: false },
      },
    },
  };
  const db = {
    series: { slug: 'series' },
    episode: { slug: SLUG },
    project: { slug: SLUG },
    a01_stage_jobs: [],
    a01_media_jobs: [],
    global_nonterminal_stage_jobs: [],
    global_nonterminal_media_jobs: [],
  };
  const budget = { slug: SLUG, limit_usd: '25.00', reserved_usd: '0.00',
    settled_usd: '0.00', operations: [] };
  return { state, db, budget };
}

test('104 complete events and unchanged two-readback evidence are a capture only', () => {
  const { state, db, budget } = fixture();
  assert.deepEqual(assess(state, state, db, db, budget, budget), []);
});

test('the old 80-event capture cannot pass as current evidence', () => {
  const { state, db, budget } = fixture();
  state.worker.audit_events.length = 80;
  assert.ok(assess(state, state, db, db, budget, budget).includes('AUDIT_INCOMPLETE'));
});

test('drift, missing STOP and unrelated paid job remain explicit holds', () => {
  const { state, db, budget } = fixture();
  const after = structuredClone(state);
  after.worker.controls.a01_stop.present = false;
  const newer = structuredClone(db);
  newer.global_nonterminal_stage_jobs.push({ id: 'other-job', status: 'running' });
  const issues = assess(state, after, db, newer, budget, budget);
  for (const issue of ['HOST_STATE_DRIFT', 'DB_DRIFT', 'A01_STOP_MISSING', 'GLOBAL_JOB_ACTIVE']) {
    assert.ok(issues.includes(issue));
  }
});

test('complete evidence remains HOLD while an unrelated job is active', () => {
  const report = { status: 'HOLD', production_adoption_allowed: false,
    files: Object.fromEntries(Array.from({ length: 7 }, (_, index) => [index, {}])) };
  finalizeCaptureReport(report, ['GLOBAL_JOB_ACTIVE']);
  assert.equal(report.capture_complete, true);
  assert.equal(report.capture_consistent, false);
  assert.equal(report.operational_gate, 'HOLD');
  assert.equal(report.production_adoption_allowed, false);
});

test('an uncertain A01 stage job remains on HOLD even if the global projection misses it', () => {
  const { state, db, budget } = fixture();
  db.a01_stage_jobs.push({ id: 'a01-uncertain', status: 'uncertain' });
  const issues = assess(state, state, db, db, budget, budget);
  assert.ok(issues.includes('A01_STAGE_UNRESOLVED'));
  const report = { status: 'HOLD', production_adoption_allowed: false,
    files: Object.fromEntries(Array.from({ length: 7 }, (_, index) => [index, {}])) };
  finalizeCaptureReport(report, issues);
  assert.equal(report.operational_gate, 'HOLD');
});

test('destination must be new, absolute, outside Git and free of linked ancestors', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'a01-capture-test-'));
  const fresh = join(directory, 'new');
  assert.equal(await checkDestination(fresh), fresh);
  const forwardSlash = join(directory, 'forward-slash').replaceAll('\\', '/');
  assert.equal(await checkDestination(forwardSlash), resolve(forwardSlash));
  if (process.platform === 'win32') {
    const actualWindowsExample = `C:/Users/x8120/AppData/Local/Temp/a01-fresh-test-${Date.now()}`;
    assert.equal(await checkDestination(actualWindowsExample), resolve(actualWindowsExample));
  }
  await mkdir(fresh);
  await assert.rejects(checkDestination(fresh), /OUT_ALREADY_EXISTS/);
  await assert.rejects(checkDestination('relative-output'), /OUT_NOT_ABSOLUTE/);
  await assert.rejects(checkDestination(join(process.cwd(), 'capture')), /OUT_INSIDE_REPOSITORY/);
  const linked = join(directory, 'linked');
  await symlink(directory, linked, 'junction');
  await assert.rejects(checkDestination(join(linked, 'capture')), /OUT_PARENT_NOT_CANONICAL|OUT_PARENT_LINKED/);
});

test('binary tar stream survives capture without shell or text conversion', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'a01-capture-stream-'));
  const payload = Buffer.from([0, 255, 10, 13, 42, 0]);
  const fakeSpawn = (program, args, options) => {
    assert.equal(program, 'plink.exe');
    assert.deepEqual(args.slice(0, 6), ['-batch', '-T', '-load', 'hostinger2', '-l', 'root']);
    assert.equal(args[6], 'remote read only');
    assert.equal(options.windowsHide, true);
    const child = new EventEmitter();
    child.stdin = new PassThrough();
    child.stdout = new PassThrough();
    child.stderr = new PassThrough();
    child.kill = () => {};
    child.stdin.on('finish', () => {
      child.stdout.end(payload);
      child.stderr.end();
      child.emit('close', 0, null);
    });
    return child;
  };
  const result = await captureStep('plink.exe', directory, 'a01-source.tar',
    'remote read only', Buffer.from('script'), fakeSpawn);
  assert.equal(result.bytes, payload.length);
  assert.deepEqual(await readFile(join(directory, 'a01-source.tar')), payload);
});

test('remote output protocols reject extra text and malformed host state', () => {
  const host = `GIT ${'a'.repeat(40)}\nDEPLOY_HOLD absent\n{"slug":"${SLUG}"}\n`;
  assert.equal(parseHostState(host).worker.slug, SLUG);
  assert.deepEqual(parseJsonOutput('{"operations":[]}\n', 'BUDGET'), { operations: [] });
  assert.throws(() => parseJsonOutput('warning\n{"operations":[]}\n', 'BUDGET'),
    /BUDGET_NOT_SINGLE_JSON/);
  assert.throws(() => parseHostState(`welcome\n${host}`), /HOST_STATE_FORMAT/);
});

test('host-state requests python3, the executable used by the video-worker image build', async () => {
  const script = await readFile(new URL('./host-state.sh', import.meta.url), 'utf8');
  assert.match(script, /video-worker python3 - <<'PY'/);
  assert.doesNotMatch(script, /video-worker python -/);
  assert.match(script, /tools_video_runtime_inventory_sha256/);
});
