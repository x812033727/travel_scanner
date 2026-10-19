import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { SLUG, CHAPTERS, changedPaths, sourceTuple, sourceHash, auditInventory,
  afterTuple, draftReadbackExpectation, plannedWritePaths, applyAdoption,
  inspectRecovery, recoverBefore, RELEASE_LOCKS,
  REJECTED_R23_MANIFEST_SHA256 } from './transaction.mjs';
import { planInitialStoryLexicon } from '../core/story-lexicon.mjs';

const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
function put(file, bytes) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, bytes);
}
function pathFor(roots, logical) {
  return logical.startsWith('docs/videos/')
    ? path.join(roots.docs, logical.slice('docs/videos/'.length))
    : path.join(roots.work, logical);
}
function targetSource(logical) {
  const name = path.basename(logical, '.json');
  if (name === 'video') return { slug: SLUG, target_minutes: [7, 8],
    sources: Array.from({ length: 18 }, (_, i) => ({ url: `https://example.com/${i}` })) };
  if (name === 'series') return { slug: SLUG, target_minutes: 10,
    plan: { sources: Array.from({ length: 25 }, (_, i) => ({ url: `https://example.com/${i}` })) } };
  if (name === 'auto') return { slug: SLUG, status: 'blocked',
    blocked_kind: 'pilot_script_review', verified: false, listener_done: false,
    story: { narrative: null } };
  return { key: name, scenes: [{ id: `${name}-01`, lines: [{ id: '1', text: 'text' }] }],
    claims: [{ id: `${name}1`, fact: null, verdict: 'UNCHECKED' }] };
}
function buildFixture() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-adoption-fixture-'));
  const roots = { docs: path.join(base, 'docs', 'videos'), work: path.join(base, 'work') };
  const doc = path.join(roots.docs, SLUG);
  const work = path.join(roots.work, SLUG);
  const sharedLexicon = json({ schema_version: 1, terms: {} });
  put(path.join(roots.docs, 'lexicon.json'), sharedLexicon);
  const lexiconPlan = planInitialStoryLexicon({ slug: SLUG, sharedBytes: sharedLexicon });
  for (const entry of lexiconPlan.files)
    put(path.join(doc, 'story-lexicon', entry.relative), entry.bytes);
  put(path.join(doc, 'claims.md'), Buffer.from('old claims\n'));
  put(path.join(doc, 'script.md'), Buffer.from('old script\n'));
  put(path.join(work, 'review', 'narrative.json'), json({ old: true }));
  put(path.join(work, 'STOP'), Buffer.from('A01 review hold\n'));
  put(path.join(roots.work, 'STOP'), Buffer.from('synthetic global queue fence\n'));
  for (const logical of changedPaths()) put(pathFor(roots, logical),
    json({ old: logical, ...(logical.endsWith('/auto.json')
      ? { status: 'blocked', blocked_kind: 'prompt_fixes:narrative' } : {}) }));
  const before = sourceTuple(roots);
  const beforeSha = sourceHash(before);
  const audit = path.join(work, 'story', 'recheck-audit');
  for (let i = 1; i <= 104; i++) {
    const id = `event-${String(i).padStart(3, '0')}`;
    put(path.join(audit, id, 'index.json'), json(i === 104
      ? { before_source_sha256: 'f'.repeat(64), after_source_sha256: beforeSha, after: before }
      : { after_source_sha256: '0'.repeat(64) }));
  }
  // Mirror the real 104 event's 222-file shape without pretending these are real events.
  const oldInventory = auditInventory(audit);
  assert.equal(oldInventory.count, 104);
  const targets = Object.fromEntries(changedPaths().map((logical) =>
    [logical, json(targetSource(logical))]));
  const targetHashes = Object.fromEntries(Object.entries(targets).map(([name, bytes]) =>
    [name, sha(bytes)]));
  const beforeHashes = Object.fromEntries(changedPaths().map((logical) =>
    [logical, sha(fs.readFileSync(pathFor(roots, logical)))]));
  const plan = { schema_version: 1, kind: 'a01_r23_105_install_plan',
    slug: SLUG, event_id: 'r23-existing-revision-aaaaaaaaaaaaaaaa',
    before_source_sha256: beforeSha, old_event_id: 'event-104',
    old_index_sha256: sha(fs.readFileSync(path.join(audit, 'event-104', 'index.json'))),
    old_audit_file_count: oldInventory.count,
    old_audit_inventory_sha256: oldInventory.sha256,
    before_files_sha256: beforeHashes, changed_files_sha256: targetHashes,
    editorial_manifest_sha256: '1'.repeat(64),
    capture_manifest_sha256: '2'.repeat(64), release_sha: '3'.repeat(40),
    independent_capture_receipt_sha256: '6'.repeat(64),
    tools_video_tree_sha: '7'.repeat(40), worker_image_id: `sha256:${'8'.repeat(64)}`,
    tools_video_runtime_inventory_sha256: 'a'.repeat(64),
    tools_video_runtime_file_count: 99,
    worker_story_sha256: '4'.repeat(64), public_filter_sha256: '4'.repeat(64),
    a01_stop_sha256: sha(fs.readFileSync(path.join(work, 'STOP'))),
    public_source_urls: Array.from({ length: 18 }, (_, i) => `https://example.com/${i}`),
    target_bytes: Object.fromEntries(Object.entries(targets).map(([name, bytes]) =>
      [name, bytes.toString('base64')])),
  };
  plan.after_source_sha256 = sourceHash(afterTuple(before, plan));
  const syntheticTestPins = { source_sha256: beforeSha,
    tip_index_sha256: plan.old_index_sha256,
    audit_inventory_sha256: plan.old_audit_inventory_sha256,
    audit_file_count: plan.old_audit_file_count };
  const grant = { schema_version: 1, slug: SLUG, event_id: plan.event_id,
    approved: true, plan_sha256: sha(json(plan)),
    owner_approval_ref: 'synthetic-test-only-owner-grant',
    write_paths: plannedWritePaths(roots, plan) };
  const releaseGuard = { kind: 'reviewed_self_owned_release_hold_and_four_locks',
    release_dir: path.join(base, 'host-release-guard'), hold_sha256: '5'.repeat(64),
    verify() { return true; } };
  const admissionFence = { kind: 'reviewed_durable_a01_db_admission_fence',
    token: '9'.repeat(64), verify() { return true; } };
  const probe = async () => ({ schema_version: 1, slug: SLUG,
    release_sha: plan.release_sha,
    capture_manifest_sha256: plan.capture_manifest_sha256,
    independent_capture_receipt_sha256: plan.independent_capture_receipt_sha256,
    worker_story_sha256: plan.worker_story_sha256,
    public_filter_sha256: plan.public_filter_sha256,
    tools_video_tree_sha: plan.tools_video_tree_sha,
    tools_video_runtime_inventory_sha256: plan.tools_video_runtime_inventory_sha256,
    tools_video_runtime_file_count: plan.tools_video_runtime_file_count,
    worker_image_id: plan.worker_image_id,
    a01_stop_sha256: plan.a01_stop_sha256,
    global_stop_sha256: sha(fs.readFileSync(path.join(roots.work, 'STOP'))),
    release_hold: { owner: 'self', target_sha: plan.release_sha,
      release_dir: releaseGuard.release_dir, sha256: releaseGuard.hold_sha256 },
    release_locks_owned_exactly: RELEASE_LOCKS,
    a01_admission_fence: { kind: 'durable_db_row_guard', owner: 'self',
      token: admissionFence.token, reserve_rejected: true,
      text_stage_dispatch_rejected: true },
    staged_release: false,
    global_stop: true, foreign_intent: false,
    global_nonterminal_stage_jobs: [], global_nonterminal_media_jobs: [],
    a01_unsettled_journals: [], a01_media_assets: 0,
    budget: { limit_usd: 25, spent_usd: 0, reserved_usd: 0, unsettled_operations: 0 } });
  const globalFence = { kind: 'reviewed_global_queue_worker_fence',
    global_stop_sha256: sha(fs.readFileSync(path.join(roots.work, 'STOP'))),
    verify() { return true; } };
  return { base, roots, plan, grant, probe, globalFence, releaseGuard,
    admissionFence, syntheticTestPins, beforeSha };
}
function clearFixture(fixture) {
  assert.ok(path.resolve(fixture.base).startsWith(`${path.resolve(os.tmpdir())}${path.sep}`)
    && path.basename(fixture.base).startsWith('a01-adoption-fixture-'));
  const stat = fs.lstatSync(fixture.base);
  assert.ok(stat.isDirectory() && !stat.isSymbolicLink());
  fs.rmSync(fixture.base, { recursive: true, force: true });
}
function recoveryGrant(f) {
  return { approved: true, kind: 'a01_explicit_preindex_recovery',
    event_id: f.plan.event_id, plan_sha256: sha(json(f.plan)),
    write_paths: [
      ...changedPaths().flatMap((logical) => {
        const file = pathFor(f.roots, logical);
        return [file, `${file}.a01-${f.plan.event_id}-restore.new`];
      }),
      ...[f.roots.docs, f.roots.work].map((root) =>
        path.join(root, '.a01-adoption', SLUG, f.plan.event_id, 'recovery.json')),
      path.join(f.roots.work, SLUG, 'LEASE'),
    ] };
}

test('known rejected r23 editorial manifest cannot enter the adoption transaction', async () => {
  const f = buildFixture();
  try {
    f.plan.editorial_manifest_sha256 = REJECTED_R23_MANIFEST_SHA256;
    await assert.rejects(applyAdoption(f), /R23_EDITORIAL_REJECTED_AWAIT_R24/);
    assert.equal(sourceHash(sourceTuple(f.roots)), f.beforeSha);
    assert.equal(fs.existsSync(path.join(f.roots.work, SLUG, 'LEASE')), false);
  } finally { clearFixture(f); }
});

test('arbitrary replacement editorial SHA cannot unlock production adoption', async () => {
  const f = buildFixture();
  try {
    f.plan.editorial_manifest_sha256 = 'd'.repeat(64);
    delete f.syntheticTestPins;
    await assert.rejects(applyAdoption(f),
      /R24_EDITORIAL_REVIEW_GATE_NOT_CONFIGURED/);
    assert.equal(sourceHash(sourceTuple(f.roots)), f.beforeSha);
  } finally { clearFixture(f); }
});

test('successful synthetic 105 publication retains STOP and 104 audit', async () => {
  const f = buildFixture();
  try {
    const oldInventory = auditInventory(path.join(f.roots.work, SLUG, 'story', 'recheck-audit'));
    const result = await applyAdoption(f);
    assert.equal(result.status, 'HOLD_PENDING_INDEPENDENT_READBACK');
    const draft = draftReadbackExpectation(f.plan, {
      ...sourceTuple(f.roots),
      auto: f.plan.before_files_sha256[`${SLUG}/auto.json`],
      video: f.plan.before_files_sha256[`docs/videos/${SLUG}/video.json`],
      series: f.plan.before_files_sha256[`docs/videos/${SLUG}/series.json`],
      chapters: Object.fromEntries(CHAPTERS.map((key) =>
        [key, f.plan.before_files_sha256[`${SLUG}/story/chapters/${key}.json`]])),
    }, f.grant);
    assert.equal(draft.kind, 'a01_r23_105_readback_expectation_draft');
    assert.equal(Object.keys(draft.event_files_sha256).length, 2);
    assert.equal(sourceHash(sourceTuple(f.roots)), f.plan.after_source_sha256);
    assert.equal(inspectRecovery(f).status, 'INDEX_PRESENT_VERIFY_INDEPENDENTLY');
    assert.equal(sha(fs.readFileSync(path.join(f.roots.work, SLUG, 'STOP'))),
      f.plan.a01_stop_sha256);
    const oldIndex = path.join(f.roots.work, SLUG, 'story', 'recheck-audit',
      'event-104', 'index.json');
    assert.equal(sha(fs.readFileSync(oldIndex)), f.plan.old_index_sha256);
    assert.equal(oldInventory.count, 104);
    assert.equal(fs.existsSync(path.join(f.roots.work, SLUG, 'story', 'recheck-audit',
      f.plan.event_id, 'index.json')), true);
    assert.equal(fs.existsSync(path.join(f.roots.work, SLUG, 'LEASE')), false);
    await assert.rejects(recoverBefore({ ...f, adoptionGrant: f.grant, grant: {} }),
      /EXACT_RECOVERY_GRANT_REQUIRED/);
  } finally { clearFixture(f); }
});

for (const phase of ['docs-intent', 'work-intent',
  `backup:docs:${changedPaths()[0]}`, `backup:work:${changedPaths()[8]}`,
  'before-replace', `replace:${changedPaths()[0]}`,
  `replace:${changedPaths()[8]}`, 'amendment', 'receipt', 'index-temp', 'index']) {
  test(`injected ${phase} crash stays HOLD and never silently retries`, async () => {
    const f = buildFixture();
    try {
      await assert.rejects(applyAdoption({ ...f, fault(point) {
        if (point === phase) throw Error(`CRASH:${phase}`);
      } }), new RegExp(`CRASH:${phase}`));
      const state = inspectRecovery(f);
      assert.ok(state.status.startsWith('HOLD_') ||
        state.status === 'INDEX_PRESENT_VERIFY_INDEPENDENTLY');
      assert.equal(sha(fs.readFileSync(path.join(f.roots.work, SLUG, 'STOP'))),
        f.plan.a01_stop_sha256);
      assert.equal(sha(fs.readFileSync(path.join(f.roots.work, SLUG, 'story',
        'recheck-audit', 'event-104', 'index.json'))), f.plan.old_index_sha256);
      await assert.rejects(applyAdoption(f),
        /EVENT_ALREADY_EXISTS|FOREIGN_OR_OLD_INTENT_PRESENT|SOURCE_104_DRIFT/);
      if (phase.startsWith('replace:') || phase === 'amendment' || phase === 'receipt') {
        const doc = path.join(f.roots.docs, '.a01-adoption', SLUG, f.plan.event_id);
        const work = path.join(f.roots.work, '.a01-adoption', SLUG, f.plan.event_id);
        assert.equal(fs.existsSync(path.join(doc, 'intent.json')), true);
        assert.equal(fs.existsSync(path.join(work, 'intent.json')), true);
      }
      if (phase === 'receipt') {
        const recovered = await recoverBefore({ ...f, adoptionGrant: f.grant,
          grant: recoveryGrant(f) });
        assert.equal(recovered.status, 'HOLD_RECOVERED_BEFORE_104');
      }
    } finally { clearFixture(f); }
  });
}

test('explicit pre-index recovery restores exactly old bytes and retains HOLD evidence', async () => {
  const f = buildFixture();
  try {
    await assert.rejects(applyAdoption({ ...f, fault(point) {
      if (point === `replace:${changedPaths()[3]}`) throw Error('CRASH');
    } }), /CRASH/);
    assert.equal(inspectRecovery(f).status, 'HOLD_PARTIAL_REQUIRES_EXPLICIT_RECOVERY');
    const grant = recoveryGrant(f);
    const oldIndex = path.join(f.roots.work, SLUG, 'story', 'recheck-audit',
      'event-001', 'index.json');
    const oldBytes = fs.readFileSync(oldIndex);
    fs.writeFileSync(oldIndex, Buffer.from('drift\n'));
    await assert.rejects(recoverBefore({ ...f, adoptionGrant: f.grant, grant }),
      /OLD_AUDIT_DRIFT/);
    fs.writeFileSync(oldIndex, oldBytes);
    const racingIndex = path.join(f.roots.work, SLUG, 'story', 'recheck-audit',
      f.plan.event_id, 'index.json');
    let probeCalls = 0;
    await assert.rejects(recoverBefore({ ...f, adoptionGrant: f.grant, grant, async probe() {
      if (++probeCalls === 2) put(racingIndex, Buffer.from('concurrent index\n'));
      return f.probe();
    } }), /INDEX_PRESENT_NO_ROLLBACK/);
    fs.unlinkSync(racingIndex);
    fs.rmdirSync(path.dirname(racingIndex));
    const result = await recoverBefore({ ...f, adoptionGrant: f.grant, grant });
    assert.equal(result.status, 'HOLD_RECOVERED_BEFORE_104');
    assert.equal(sourceHash(sourceTuple(f.roots)), f.beforeSha);
    assert.equal(inspectRecovery(f).status, 'HOLD_NO_SOURCE_CHANGE');
    assert.equal(fs.existsSync(path.join(f.roots.work, '.a01-adoption', SLUG,
      f.plan.event_id, 'intent.json')), true);
    assert.equal(fs.existsSync(path.join(f.roots.work, '.a01-adoption', SLUG,
      f.plan.event_id, 'recovery.json')), true);
  } finally { clearFixture(f); }
});

test('missing admission or global fence or owner grant blocks before a source write', async () => {
  const f = buildFixture();
  try {
    await assert.rejects(applyAdoption({ ...f, admissionFence: null }),
      /DURABLE_A01_DB_ADMISSION_FENCE_REQUIRED/);
    await assert.rejects(applyAdoption({ ...f, admissionFence: {
      ...f.admissionFence, verify() { return false; },
    } }), /A01_DB_ADMISSION_FENCE_LOST/);
    await assert.rejects(applyAdoption({ ...f, globalFence: null }), /GLOBAL_QUEUE_FENCE_REQUIRED/);
    await assert.rejects(applyAdoption({ ...f, grant: { ...f.grant, write_paths: [] } }),
      /OWNER_PATH_SCOPE_DRIFT/);
    await assert.rejects(applyAdoption({ ...f, plan: {
      ...f.plan, old_index_sha256: 'a'.repeat(64),
    } }), /INDEPENDENT_104_PINS_REQUIRED/);
    assert.throws(() => inspectRecovery({ ...f, plan: {
      ...f.plan, old_event_id: '../elsewhere',
    } }), /INDEPENDENT_104_PINS_REQUIRED/);
    put(path.join(f.roots.work, SLUG, 'LEASE'), Buffer.from('stale lease\n'));
    await assert.rejects(applyAdoption(f), /PREEXISTING_PROJECT_LEASE_REFUSED/);
    assert.deepEqual(fs.readdirSync(path.join(f.roots.work, SLUG)).filter((name) =>
      name.startsWith('LEASE.')), []);
    assert.equal(sourceHash(sourceTuple(f.roots)), f.beforeSha);
  } finally { clearFixture(f); }
});
