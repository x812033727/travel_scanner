import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { installOfflineFixture, OFFLINE_CONSTANTS, planOfflineInstallation } from './installer.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const prior = path.resolve(here, '../A01-round10-candidate');
const next = path.resolve(here, '../A01-round11-candidate');
const release = 'a'.repeat(40);
const rules = 'b'.repeat(64);
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const put = (file, bytes) => { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, bytes); };
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const source = (key) => fs.readFileSync(path.join(prior, 'source', 'chapters', `${key}.json`));
const target = (key) => fs.readFileSync(path.join(next, 'candidate', 'chapters', `${key}.json`));

function fixture(t) {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-round11-fixture-'));
  assert.ok(path.resolve(base).startsWith(path.resolve(os.tmpdir()) + path.sep));
  t.after(() => {
    const resolved = fs.realpathSync(base);
    assert.ok(resolved.startsWith(fs.realpathSync(os.tmpdir()) + path.sep));
    assert.ok(path.basename(resolved).startsWith('a01-round11-fixture-'));
    fs.rmSync(resolved, { recursive: true, force: false });
  });
  const root = path.join(base, 'repo');
  const workdir = path.join(base, 'work', OFFLINE_CONSTANTS.slug);
  const docs = path.join(root, 'docs', 'videos', OFFLINE_CONSTANTS.slug);
  fs.mkdirSync(docs, { recursive: true });
  fs.mkdirSync(path.join(workdir, 'story', 'chapters'), { recursive: true });
  fs.mkdirSync(path.join(workdir, 'story', 'recheck-audit'), { recursive: true });
  fs.mkdirSync(path.join(workdir, 'review'), { recursive: true });
  put(path.join(root, 'A01-ROUND11-OFFLINE-FIXTURE.json'), json({ schema_version: 1, slug: OFFLINE_CONSTANTS.slug, offline_fixture: true }));
  put(path.join(workdir, 'STOP'), 'A01 round11 offline fixture STOP\n');
  for (const key of OFFLINE_CONSTANTS.keys) put(path.join(workdir, 'story', 'chapters', `${key}.json`), source(key));
  put(path.join(workdir, 'review', 'narrative.json'), fs.readFileSync(path.join(prior, 'evidence', 'round9-narrative.json')));
  put(path.join(docs, 'series.json'), fs.readFileSync(path.join(prior, 'evidence', 'round9-series.json')));
  put(path.join(docs, 'video.json'), fs.readFileSync(path.join(prior, 'evidence', 'round9-composed-video.json')));
  put(path.join(docs, 'script.md'), '# Fixture script from round 9\n');
  put(path.join(docs, 'claims.md'), '# Fixture claims from round 9\n');
  put(path.join(docs, 'verify-1.md'), '# Fixture checker report from round 9\n');
  const state = {
    slug: OFFLINE_CONSTANTS.slug, format: 'drama', status: 'blocked', blocked_kind: 'prompt_fixes:narrative',
    blocked: 'the storytelling panel still fails', verified: true, listener_done: true,
    verify_rounds: 1, notes: ['round9 FAIL preserved'],
    story: { narrative: { rounds: 9, passed: false, failed: ['chapters_link', 'payoffs', 'one_thread'] },
      narrative_fixes: 2, owner_note: null,
      chapters: Object.fromEntries(OFFLINE_CONSTANTS.keys.map((key) => [key, {
        written: 1, lint: null, lint_fixes: 0, checked: true, check_rounds: 2, listened: true,
      }])),
    },
  };
  put(path.join(workdir, 'auto.json'), json(state));
  const tipFile = 'story/recheck-audit/round9-tip.json';
  put(path.join(workdir, ...tipFile.split('/')), json({
    link_count: 80, after_source_composite_sha256: OFFLINE_CONSTANTS.historicComposite,
    previous_audit_sha256: 'c'.repeat(64), status: 'fixture-tip-only',
  }));
  const files = {
    'auto.json': path.join(workdir, 'auto.json'),
    'review/narrative.json': path.join(workdir, 'review', 'narrative.json'),
    'series.json': path.join(docs, 'series.json'),
    'video.json': path.join(docs, 'video.json'),
    'script.md': path.join(docs, 'script.md'),
    'claims.md': path.join(docs, 'claims.md'),
    'verify-1.md': path.join(docs, 'verify-1.md'),
    ...Object.fromEntries(OFFLINE_CONSTANTS.keys.map((key) => [`story/chapters/${key}.json`, path.join(workdir, 'story', 'chapters', `${key}.json`)])),
  };
  const observedAt = '2026-10-16T00:00:00.000Z';
  const evidence = {
    schema_version: 1, slug: OFFLINE_CONSTANTS.slug, observed_at: observedAt,
    historical_source_composite_sha256: OFFLINE_CONSTANTS.historicComposite,
    source_chapter_bundle_sha256: OFFLINE_CONSTANTS.sourceBundleDigest,
    approved_release_sha: release, observed_release_sha: release,
    approved_panel_rules_sha256: rules, observed_panel_rules_sha256: rules,
    worker: { lease_active: false, pending_stage_jobs: 0, pending_media_jobs: 0, pending_journal_entries: 0 },
    project: { status: 'blocked', retry_request_id: null, retry_acknowledged_id: null },
    settings: { drama_auto_approve_final: false, series_auto_continue: false },
    budget: { slug: OFFLINE_CONSTANTS.slug, limit_usd: '25.000000', reserved_usd: '0.000000',
      settled_usd: '0.000000', uncertain_usd: '0.000000', remaining_usd: '25.000000', operation_count: 0 },
    files: Object.fromEntries(Object.entries(files).map(([rel, file]) => [rel, sha(fs.readFileSync(file))])),
    audit: { link_count: 80, source_composite_sha256: OFFLINE_CONSTANTS.historicComposite,
      tip_file: tipFile, tip_sha256: sha(fs.readFileSync(path.join(workdir, ...tipFile.split('/')))) },
  };
  const evidencePath = path.join(base, 'safety-evidence.json');
  const saveEvidence = () => put(evidencePath, json(evidence));
  saveEvidence();
  return { base, root, workdir, docs, state, evidence, evidencePath, files, saveEvidence,
    options: { root, workdir, evidencePath, approvedReleaseSha256: release, approvedPanelRulesSha256: rules, now: Date.parse(observedAt) + 1_000 },
  };
}

function originalHashes(f) { return Object.fromEntries(Object.entries(f.files).map(([rel, file]) => [rel, sha(fs.readFileSync(file))])); }
function noLiveChanges(f, before) {
  assert.deepEqual(originalHashes(f), before);
  assert.deepEqual(fs.readdirSync(path.join(f.workdir, 'story', 'recheck-audit')), ['round9-tip.json']);
}

test('round11 fixture install creates exact backup, inverse, audit and only intended invalidation', (t) => {
  const f = fixture(t);
  const before = originalHashes(f);
  const plan = planOfflineInstallation(f.options);
  assert.equal(Object.keys(plan.replacements).length, 5);
  assert.deepEqual(Object.keys(plan.replacements), ['story/chapters/origin.json', 'story/chapters/idea.json', 'story/chapters/turn.json', 'story/chapters/now.json', 'auto.json']);
  const result = installOfflineFixture(f.options);
  assert.equal(result.receipt.status, 'OFFLINE_ONLY_NOT_APPROVED');
  assert.equal(result.receipt.paid_calls, 0);
  assert.equal(result.receipt.link_count, 81);
  assert.equal(fs.readFileSync(path.join(f.workdir, 'STOP'), 'utf8'), 'A01 round11 offline fixture STOP\n');
  for (const key of OFFLINE_CONSTANTS.keys) {
    const file = f.files[`story/chapters/${key}.json`];
    assert.ok(fs.readFileSync(file).equals(target(key)), key);
    assert.ok(fs.readFileSync(path.join(result.backup, 'before', 'story', 'chapters', `${key}.json`)).equals(source(key)), `backup ${key}`);
  }
  const after = readJson(f.files['auto.json']);
  assert.equal(after.verified, false);
  assert.equal(after.listener_done, false);
  assert.equal(after.story.narrative.rounds, 9);
  assert.equal(after.story.narrative_fixes, 2);
  assert.deepEqual(after.story.narrative.failed, f.state.story.narrative.failed);
  for (const key of OFFLINE_CONSTANTS.keys) {
    assert.equal(after.story.chapters[key].checked, !['origin', 'now'].includes(key));
    assert.equal(after.story.chapters[key].listened, !['origin', 'now'].includes(key));
    assert.equal(after.story.chapters[key].check_rounds, 2);
  }
  assert.equal(sha(fs.readFileSync(f.files['review/narrative.json'])), OFFLINE_CONSTANTS.historicNarrative);
  for (const rel of ['series.json', 'video.json', 'script.md', 'claims.md', 'verify-1.md', 'story/chapters/hook.json', 'story/chapters/engine.json']) {
    assert.equal(sha(fs.readFileSync(f.files[rel])), before[rel], `unchanged ${rel}`);
  }
  const inverse = readJson(path.join(result.backup, 'inverse-manifest.json'));
  assert.equal(inverse.inverse['auto.json'].before_sha256, before['auto.json']);
  assert.equal(inverse.inverse['auto.json'].after_sha256, sha(fs.readFileSync(f.files['auto.json'])));
  assert.equal(readJson(result.auditFile).previous_audit_sha256, f.evidence.audit.tip_sha256);
  assert.throws(() => installOfflineFixture(f.options), /source origin|live file drift/, 'duplicate install refused');
});

test('source, STOP, worker, retry, setting, budget, counter, release and audit mismatches fail before writes', async (t) => {
  const cases = [
    ['source byte drift', (f) => put(f.files['story/chapters/origin.json'], Buffer.concat([fs.readFileSync(f.files['story/chapters/origin.json']), Buffer.from(' ')])), /live file drift|source origin/],
    ['historic composite drift', (f) => { f.evidence.historical_source_composite_sha256 = '0'.repeat(64); f.saveEvidence(); }, /historical_source_composite/],
    ['STOP missing', (f) => fs.unlinkSync(path.join(f.workdir, 'STOP')), /ENOENT|STOP/],
    ['active lease', (f) => { f.evidence.worker.lease_active = true; f.saveEvidence(); }, /lease_active/],
    ['pending stage', (f) => { f.evidence.worker.pending_stage_jobs = 1; f.saveEvidence(); }, /pending_stage_jobs/],
    ['pending media', (f) => { f.evidence.worker.pending_media_jobs = 1; f.saveEvidence(); }, /pending_media_jobs/],
    ['pending journal', (f) => { f.evidence.worker.pending_journal_entries = 1; f.saveEvidence(); }, /pending_journal_entries/],
    ['pending retry', (f) => { f.evidence.project.retry_request_id = 'new'; f.saveEvidence(); }, /retry_request_id/],
    ['final auto approval enabled', (f) => { f.evidence.settings.drama_auto_approve_final = true; f.saveEvidence(); }, /final auto-approval/],
    ['series auto continuation enabled', (f) => { f.evidence.settings.series_auto_continue = true; f.saveEvidence(); }, /series auto-continuation/],
    ['uncertain cost', (f) => { f.evidence.budget.uncertain_usd = '0.010000'; f.saveEvidence(); }, /budget/],
    ['counter drift', (f) => { const s = readJson(f.files['auto.json']); s.story.narrative_fixes = 1; put(f.files['auto.json'], json(s)); f.evidence.files['auto.json'] = sha(fs.readFileSync(f.files['auto.json'])); f.saveEvidence(); }, /narrative_fixes/],
    ['unapproved release', (f) => { f.evidence.observed_release_sha = 'd'.repeat(40); f.saveEvidence(); }, /observed_release_sha/],
    ['unapproved rules', (f) => { f.evidence.observed_panel_rules_sha256 = 'd'.repeat(64); f.saveEvidence(); }, /observed_panel_rules_sha256/],
    ['stale evidence', (f) => { f.evidence.observed_at = '2026-10-15T23:00:00.000Z'; f.saveEvidence(); }, /safety evidence is stale/],
    ['audit tip hash drift', (f) => put(path.join(f.workdir, ...f.evidence.audit.tip_file.split('/')), '{}\n'), /audit tip drift/],
    ['audit tip composite drift with refreshed hash', (f) => {
      const tip = path.join(f.workdir, ...f.evidence.audit.tip_file.split('/'));
      const record = readJson(tip);
      record.after_source_composite_sha256 = 'd'.repeat(64);
      put(tip, json(record));
      f.evidence.audit.tip_sha256 = sha(fs.readFileSync(tip));
      f.saveEvidence();
    }, /audit tip source composite mismatch/],
    ['foreign script receipt', (f) => put(path.join(f.workdir, 'story', 'reviews', 'script-review.json'), '{}\n'), /script-review\.json/],
  ];
  for (const [name, mutate, expected] of cases) {
    await t.test(name, (sub) => {
      const f = fixture(sub);
      mutate(f);
      const before = originalHashes(f);
      assert.throws(() => installOfflineFixture(f.options), expected);
      noLiveChanges(f, before);
      assert.equal(fs.existsSync(path.join(f.workdir, 'manual-revisions')), false, 'preflight refusal cannot start a backup');
    });
  }
});

test('precommit backup or inverse setup failure leaves live source untouched and an incomplete revision for manual review', async (t) => {
  for (const [name, phase, completedBackup, inverseExists] of [
    ['partial backup copy', 'after-backup-copy:auto.json', false, false],
    ['inverse not yet written', 'before-inverse-write', true, false],
    ['inverse written but transaction not entered', 'after-inverse-write', true, true],
  ]) {
    await t.test(name, (sub) => {
      const f = fixture(sub);
      const before = originalHashes(f);
      const tip = path.join(f.workdir, ...f.evidence.audit.tip_file.split('/'));
      const beforeTip = sha(fs.readFileSync(tip));
      assert.throws(() => installOfflineFixture({ ...f.options, fault(actual) {
        if (actual === phase) throw new Error(`synthetic setup failure: ${phase}`);
      } }), /synthetic setup failure/);
      noLiveChanges(f, before);
      assert.equal(sha(fs.readFileSync(tip)), beforeTip, 'old audit tip must remain byte identical');
      assert.equal(fs.readFileSync(path.join(f.workdir, 'STOP'), 'utf8'), 'A01 round11 offline fixture STOP\n');
      const revisions = fs.readdirSync(path.join(f.workdir, 'manual-revisions'));
      assert.equal(revisions.length, 1);
      const backup = path.join(f.workdir, 'manual-revisions', revisions[0]);
      assert.equal(fs.existsSync(path.join(backup, 'receipt.json')), false);
      assert.equal(fs.existsSync(path.join(backup, 'failure.json')), false);
      assert.equal(fs.existsSync(path.join(backup, 'inverse-manifest.json')), inverseExists);
      assert.ok(fs.readFileSync(path.join(backup, 'before', 'auto.json')).equals(fs.readFileSync(f.files['auto.json'])));
      if (completedBackup) {
        for (const [rel, file] of Object.entries(f.files)) {
          assert.equal(sha(fs.readFileSync(path.join(backup, 'before', ...rel.split('/')))), sha(fs.readFileSync(file)), rel);
        }
        assert.equal(sha(fs.readFileSync(path.join(backup, 'safety-evidence.json'))), sha(fs.readFileSync(f.evidencePath)));
      } else {
        assert.deepEqual(fs.readdirSync(path.join(backup, 'before')), ['auto.json']);
        assert.equal(fs.existsSync(path.join(backup, 'safety-evidence.json')), false);
      }
      if (inverseExists) assert.equal(readJson(path.join(backup, 'inverse-manifest.json')).inverse['auto.json'].before_sha256, before['auto.json']);
    });
  }
});

test('fault after a chapter write restores every source byte and retains rollback evidence', (t) => {
  const f = fixture(t);
  const before = originalHashes(f);
  assert.throws(() => installOfflineFixture({ ...f.options, fault(phase) { if (phase === 'after-write:story/chapters/idea.json') throw new Error('synthetic interruption'); } }), /synthetic interruption/);
  noLiveChanges(f, before);
  const revisions = fs.readdirSync(path.join(f.workdir, 'manual-revisions'));
  assert.equal(revisions.length, 1);
  const backup = path.join(f.workdir, 'manual-revisions', revisions[0]);
  assert.equal(readJson(path.join(backup, 'failure.json')).status, 'ROLLED_BACK');
  assert.equal(fs.existsSync(path.join(backup, 'receipt.json')), false);
});

test('fault after audit restores files and preserves rolled-back audit in backup', (t) => {
  const f = fixture(t);
  const before = originalHashes(f);
  assert.throws(() => installOfflineFixture({ ...f.options, fault(phase) { if (phase === 'after-audit') throw new Error('audit interruption'); } }), /audit interruption/);
  noLiveChanges(f, before);
  const revisions = fs.readdirSync(path.join(f.workdir, 'manual-revisions'));
  const backup = path.join(f.workdir, 'manual-revisions', revisions[0]);
  assert.equal(readJson(path.join(backup, 'failure.json')).status, 'ROLLED_BACK');
  assert.equal(readJson(path.join(backup, 'rolled-back-audit.json')).kind, 'offline_a01_round11_install');
});

test('backup corruption before commit is refused without changing live files', (t) => {
  const f = fixture(t);
  const before = originalHashes(f);
  assert.throws(() => installOfflineFixture({ ...f.options, fault(phase) {
    if (phase === 'after-backup') {
      const revision = fs.readdirSync(path.join(f.workdir, 'manual-revisions'))[0];
      put(path.join(f.workdir, 'manual-revisions', revision, 'before', 'auto.json'), 'tampered');
    }
  } }), /backup drift auto\.json/);
  noLiveChanges(f, before);
});

test('safety evidence drift after backup is refused before replacing chapters', (t) => {
  const f = fixture(t);
  const before = originalHashes(f);
  assert.throws(() => installOfflineFixture({ ...f.options, fault(phase) {
    if (phase === 'after-backup') {
      f.evidence.observed_at = '2026-10-16T00:00:01.000Z';
      f.saveEvidence();
    }
  } }), /precommit safety evidence drift/);
  noLiveChanges(f, before);
});

test('unexpected concurrent edit during rollback requires manual recovery and preserves backup', (t) => {
  const f = fixture(t);
  assert.throws(() => installOfflineFixture({ ...f.options, fault(phase) {
    if (phase === 'after-write:story/chapters/origin.json') {
      put(f.files['story/chapters/origin.json'], 'concurrent writer\n');
      throw new Error('synthetic race');
    }
  } }), /rollback failed/);
  const revision = fs.readdirSync(path.join(f.workdir, 'manual-revisions'))[0];
  const backup = path.join(f.workdir, 'manual-revisions', revision);
  assert.equal(readJson(path.join(backup, 'failure.json')).status, 'MANUAL_RECOVERY_REQUIRED');
  assert.ok(fs.readFileSync(path.join(backup, 'before', 'story', 'chapters', 'origin.json')).equals(source('origin')));
  assert.equal(fs.readFileSync(f.files['story/chapters/origin.json'], 'utf8'), 'concurrent writer\n');
});

function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
