import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { inspectExport } from './inspect-export.mjs';

const slug = 'story-rolling-suitcase-v2';
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const authored = JSON.parse(readFileSync(new URL('../../series.json', import.meta.url), 'utf8'));
const sha = (value) => createHash('sha256').update(value).digest('hex');
const id = (digit) => `${digit}`.repeat(8) + '-0000-4000-8000-' + `${digit}`.repeat(12);

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'a01-export-fixture-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const file = (rel) => path.join(root, ...rel.split('/'));
  const write = (rel, value) => {
    mkdirSync(path.dirname(file(rel)), { recursive: true });
    writeFileSync(file(rel), value);
  };
  const hash = (rel) => sha(readFileSync(file(rel)));
  const docs = `docs/videos/${slug}`;
  for (const rel of [`${docs}/video.json`, `${docs}/series.json`, `${docs}/claims.md`,
    `${docs}/script.md`, 'docs/videos/lexicon.json', `${slug}/review/narrative.json`]) write(rel, `${rel}\n`);
  for (const key of keys) write(`${slug}/story/chapters/${key}.json`, `${key}\n`);
  write(`${slug}/auto.json`, 'auto-80\n');
  const source = (n) => ({ auto: sha(`auto-${n}\n`), video: hash(`${docs}/video.json`),
    series: hash(`${docs}/series.json`), claims: hash(`${docs}/claims.md`),
    script: hash(`${docs}/script.md`), lexicon: hash('docs/videos/lexicon.json'),
    narrative: hash(`${slug}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(keys.map((key) => [key, hash(`${slug}/story/chapters/${key}.json`)])) });
  const first = source(0);
  const installed = { 'docs/video.json': first.video, 'docs/series.json': first.series,
    'docs/claims.md': first.claims, 'docs/script.md': first.script, 'work/auto.json': first.auto,
    ...Object.fromEntries(keys.map((key) => [`work/story/chapters/${key}.json`, first.chapters[key]])) };
  const receipt = `${slug}/manual-revisions/first/installation-receipt.json`;
  write(receipt, `${JSON.stringify({ schema_version: 1, kind: 'a01-candidate-installation', slug,
    installed_sha256: installed })}\n`);
  const manifest = [];
  for (let n = 0; n < 80; n++) {
    const event = `e${String(n).padStart(3, '0')}`;
    const dir = `${slug}/story/recheck-audit/${event}`;
    const journal = Buffer.from(`${n}\n`), journalName = `${sha(journal)}.json`;
    write(`${dir}/${journalName}`, journal);
    const before = source(n), after = source(n + 1);
    const index = { schema_version: 1, slug, install_receipt_sha256: hash(receipt),
      before_source_sha256: sha(JSON.stringify(before)), after_source_sha256: sha(JSON.stringify(after)),
      before, after, journals: [{ name: journalName, sha256: sha(journal) }] };
    write(`${dir}/index.json`, `${JSON.stringify(index)}\n`);
    manifest.push({ id: event, index_sha256: hash(`${dir}/index.json`) });
  }
  const pins = { id: 'synthetic', links: 80, install_receipt_sha256: hash(receipt),
    tip_index_sha256: manifest.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  const state = {
    schema_version: 1, slug, observed_at: '2026-10-16T06:00:00Z',
    release: { git_sha: 'a'.repeat(40), worker_sha256: 'b'.repeat(64), panel_rules_sha256: 'c'.repeat(64) },
    archive: { source_composite_sha256: pins.source_composite_sha256,
      audit_manifest_sha256: pins.archive_index_manifest_sha256, tip_index_sha256: pins.tip_index_sha256 },
    filesystem: { global_stop: { present: false, sha256: null },
      scoped_stop: { present: true, sha256: 'd'.repeat(64) },
      lease: { present: false, sha256: null }, unresolved_journals: 0, run_receipts: [], media_assets: [] },
    db: {
      series: { id: id('1'), slug: authored.slug, kind: authored.kind, status: 'active',
        title: authored.title, premise: authored.premise, note: authored.note,
        target_minutes: authored.target_minutes, planned_episodes: authored.planned_episodes,
        episodes_per_day: authored.episodes_per_day, image_model: authored.image_model,
        look: authored.look, style_preset: authored.style_preset, hands_off: authored.hands_off,
        visual_tier: authored.visual_tier, compilation: authored.compilation },
      episode: { id: id('2'), series_id: id('1'), number: 1, slug, status: 'started' },
      project: { slug, format: 'drama', series_slug: 'brand-stories-curio-pilot-v2', episode_number: 1,
        stage: 'blocked', retry_request_id: null, retry_acknowledged_id: null },
      budget: { slug, limit_usd: '25.000000', reserved_usd: '0', settled_usd: '0',
        remaining_usd: '25.000000', total_over_limit: false, over_limit_usd: '0.000000',
        uncertain_operations: 0, overrun_operations: 0, operations: [] },
      stage_jobs: [], media_jobs: [],
    },
  };
  const pinsFile = file('pins.json'), stateFile = file('state.json');
  const save = (repin = false) => {
    const bytes = `${JSON.stringify(state)}\n`;
    if (repin) pins.state_sha256 = sha(bytes);
    write('pins.json', `${JSON.stringify(pins)}\n`);
    write('state.json', bytes);
  };
  save(true);
  return { root, file, write, pins, state, pinsFile, stateFile, save,
    run: () => inspectExport({ snapshotRoot: root, pinsFile, stateFile }) };
}

test('full synthetic 80-event archive and state readback bind offline, with production held', (t) => {
  const f = fixture(t), report = f.run();
  assert.equal(report.result, 'LOCAL_INSPECTION_ONLY');
  assert.equal(report.source_integrity, 'LOCAL_SNAPSHOT_INTEGRITY_PASS');
  assert.equal(report.binding, 'LOCAL_READBACK_BINDING_PASS');
  assert.equal(report.production_status, 'HOLD');
  assert.equal(report.installation_allowed, false);
  assert.equal(report.paid_work_allowed, false);
  assert.equal(report.state_summary.budget.operation_count, 0);
});

test('source, state manifest and budget drift fail closed', (t) => {
  const source = fixture(t);
  source.write('docs/videos/lexicon.json', 'drift\n');
  assert.equal(source.run().errors[0].code, 'SOURCE_DRIFT_FROM_TIP');
  const state = fixture(t);
  state.state.archive.tip_index_sha256 = 'f'.repeat(64); state.save(true);
  assert.equal(state.run().errors[0].code, 'ARCHIVE_STATE_BINDING_MISMATCH');
  const budget = fixture(t);
  budget.state.db.budget.remaining_usd = '24.000000'; budget.save(true);
  assert.equal(budget.run().errors[0].code, 'BUDGET_TOTAL_MISMATCH');
});

test('duplicate operation and mismatched media link fail closed', (t) => {
  const f = fixture(t);
  const op = { operation_id: 'op1', status: 'released', category: 'image', provider: 'minimax',
    model: 'image-01', max_usd: '1.000000', actual_usd: null, attempts: 1,
    receipt_ref: null, release_reason: 'no charge', created_at: '2026-10-16T06:00:00Z',
    updated_at: '2026-10-16T06:00:00Z', media_jobs: [] };
  f.state.db.budget.operations = [op, { ...op }]; f.save(true);
  assert.equal(f.run().errors[0].code, 'INVALID_OPERATION');
  f.state.db.budget.operations = [{ ...op, media_jobs: [{ id: id('3'), status: 'failed' }] }]; f.save(true);
  assert.equal(f.run().errors[0].code, 'MEDIA_OPERATION_LINK_MISMATCH');
});

test('SQL media job omitted from budget CLI linked jobs is rejected', (t) => {
  const f = fixture(t);
  f.state.db.budget.operations = [{ operation_id: 'op1', status: 'released', category: 'image',
    provider: 'minimax', model: 'image-01', max_usd: '1.000000', actual_usd: null,
    attempts: 1, receipt_ref: null, release_reason: 'no charge',
    created_at: '2026-10-16T06:00:00Z', updated_at: '2026-10-16T06:00:00Z', media_jobs: [] }];
  f.state.db.media_jobs = [{ id: id('3'), status: 'failed', kind: 'image', operation_id: 'op1' }];
  f.save(true);
  assert.equal(f.run().errors[0].code, 'MEDIA_OPERATION_LINK_MISMATCH');
});

test('every A01 media kind without a budget operation ID fails closed', (t) => {
  for (const kind of ['image', 'clip', 'music']) {
    const f = fixture(t);
    f.state.db.media_jobs = [{ id: id('3'), status: 'queued', kind, operation_id: null }];
    f.save(true);
    assert.equal(f.run().errors[0].code, 'MEDIA_BUDGET_LINK_MISSING', kind);
  }
});

test('A01 series and active started blocked state must match the authored plan', (t) => {
  for (const [part, key, value, code] of [
    ['series', 'slug', 'other-series', 'SERIES_PLAN_DRIFT'],
    ['series', 'target_minutes', 13, 'SERIES_PLAN_DRIFT'],
    ['series', 'hands_off', false, 'SERIES_PLAN_DRIFT'],
    ['series', 'image_model', 'other-model', 'SERIES_PLAN_DRIFT'],
    ['series', 'status', 'paused', 'SERIES_PLAN_DRIFT'],
    ['series', 'look', { preset: 'other' }, 'SERIES_PLAN_DRIFT'],
    ['series', 'style_preset', 'cinematic-3d', 'SERIES_PLAN_DRIFT'],
    ['series', 'visual_tier', 'clips', 'SERIES_PLAN_DRIFT'],
    ['series', 'compilation', true, 'SERIES_PLAN_DRIFT'],
    ['series', 'episodes_per_day', 2, 'SERIES_PLAN_DRIFT'],
    ['series', 'planned_episodes', 100, 'SERIES_PLAN_DRIFT'],
    ['series', 'title', 'other title', 'SERIES_PLAN_DRIFT'],
    ['series', 'premise', 'other premise', 'SERIES_PLAN_DRIFT'],
    ['series', 'note', 'other note', 'SERIES_PLAN_DRIFT'],
    ['episode', 'status', 'ready', 'INVALID_EPISODE_PLAN'],
    ['project', 'stage', 'ready', 'INVALID_PROJECT_READBACK'],
  ]) {
    const f = fixture(t);
    f.state.db[part][key] = value;
    f.save(true);
    assert.equal(f.run().errors[0].code, code, `${part}.${key}`);
  }
});

test('inventory path escape and unknown DB fields are rejected', (t) => {
  const f = fixture(t);
  f.state.filesystem.media_assets = [{ path: '../secret', sha256: 'a'.repeat(64), bytes: 1 }]; f.save(true);
  assert.equal(f.run().errors[0].code, 'INVALID_MEDIA_INVENTORY');
  f.state.filesystem.media_assets = []; f.state.db.secret = 'never export'; f.save(true);
  assert.equal(f.run().errors[0].code, 'INVALID_DB_READBACK');
});

test('state bytes changed after independently pinned capture are rejected first', (t) => {
  const f = fixture(t);
  f.state.db.project.stage = 'ready';
  f.save();
  assert.equal(f.run().errors[0].code, 'STATE_PIN_MISMATCH');
});
