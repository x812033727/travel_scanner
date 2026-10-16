import assert from 'node:assert/strict';
import { createHash, randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// OFFLINE FIXTURE ONLY. This module has no CLI, network, model or host adapter.
// A production adapter must be separately reviewed against fresh live evidence.
const here = path.dirname(fileURLToPath(import.meta.url));
const prior = path.resolve(here, '../A01-round10-candidate');
const next = path.resolve(here, '../A01-round11-candidate');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const changedChapters = ['origin', 'idea', 'turn', 'now'];
const slug = 'story-rolling-suitcase-v2';
const historicComposite = 'cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b';
const historicNarrative = 'dd458ee2b6eee90a3b358408c605620c108ca4387afb94249fd555abc01babab';
const sourceBundleDigest = 'b4d1eb3955f3d1f1db26cee70ad4c75c3b84a2c1e1fa03f1f90bdc7daeb3b821';
const targetBundleDigest = 'b0a5703742da75189a834f1c921b05099a54ab1685840afc8525ffa6fa54179f';
const expectedFailed = ['chapters_link', 'payoffs', 'one_thread'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const jsonBytes = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const chPath = (workdir, key) => path.join(workdir, 'story', 'chapters', `${key}.json`);
const own = (object, key) => Object.hasOwn(object, key);

function regular(file) {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
}

function inside(child, parent) {
  const rel = path.relative(parent, child);
  return rel === '' || (rel !== '..' && !rel.startsWith(`..${path.sep}`) && !path.isAbsolute(rel));
}

function safeFixtureRoots(root, workdir) {
  assert.equal(path.isAbsolute(root), true, 'absolute fixture root required');
  assert.equal(path.isAbsolute(workdir), true, 'absolute fixture workdir required');
  const resolvedRoot = fs.realpathSync(root);
  const resolvedWorkdir = fs.realpathSync(workdir);
  assert.equal(root, resolvedRoot, 'fixture root must have no symlink/alias');
  assert.equal(workdir, resolvedWorkdir, 'fixture workdir must have no symlink/alias');
  assert.ok(!inside(resolvedWorkdir, resolvedRoot) && !inside(resolvedRoot, resolvedWorkdir), 'workdir and root must be separate');
  const temporary = fs.realpathSync(os.tmpdir());
  assert.ok(inside(resolvedRoot, temporary) && inside(resolvedWorkdir, temporary), 'offline fixture must be under the OS temp directory');
  const marker = readJson(path.join(root, 'A01-ROUND11-OFFLINE-FIXTURE.json'));
  assert.deepEqual(marker, { schema_version: 1, slug, offline_fixture: true });
  return { root, workdir };
}

function assertTreeRegular(root, workdir) {
  for (const dir of [
    path.join(root, 'docs'), path.join(root, 'docs', 'videos'), path.join(root, 'docs', 'videos', slug),
    path.join(workdir, 'story'), path.join(workdir, 'story', 'chapters'),
    path.join(workdir, 'story', 'recheck-audit'), path.join(workdir, 'review'),
  ]) {
    const stat = fs.lstatSync(dir);
    assert.ok(stat.isDirectory() && !stat.isSymbolicLink(), `real directory required: ${dir}`);
  }
}

function bundleDigest(hashes) {
  return sha(Buffer.from(`${keys.map((key) => `${key}:${hashes[key]}`).join('\n')}\n`));
}

function packageFiles() {
  const round10 = readJson(path.join(prior, 'manifest.json'));
  const round11 = readJson(path.join(next, 'manifest.json'));
  const prompts = readJson(path.join(next, 'exact-delta.json'));
  assert.equal(round10.round9_source_composite_sha256, historicComposite);
  assert.equal(round10.round9_narrative_sha256, historicNarrative);
  assert.deepEqual(round10.round9_failed, expectedFailed);
  assert.equal(round11.base.round10_manifest_sha256, sha(regular(path.join(prior, 'manifest.json'))));
  assert.equal(round11.exact_delta_sha256, sha(regular(path.join(next, 'exact-delta.json'))));
  assert.equal(round11.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
  assert.equal(round11.authorizes_worker_or_media, false);
  assert.equal(prompts.changes.length, 6);
  assert.deepEqual(prompts.changes.map((row) => row.scene_id), round11.changed_scene_ids);
  const source = {};
  const target = {};
  for (const key of keys) {
    source[key] = regular(path.join(prior, 'source', 'chapters', `${key}.json`));
    target[key] = regular(path.join(next, 'candidate', 'chapters', `${key}.json`));
    assert.equal(sha(source[key]), round10.source_chapters_sha256[key], `frozen source ${key}`);
    assert.equal(sha(target[key]), round11.candidate_chapters_sha256[key], `frozen target ${key}`);
  }
  assert.equal(bundleDigest(Object.fromEntries(keys.map((key) => [key, sha(source[key])]))), sourceBundleDigest);
  assert.equal(bundleDigest(Object.fromEntries(keys.map((key) => [key, sha(target[key])]))), targetBundleDigest);
  assert.equal(sha(regular(path.join(prior, 'evidence', 'round9-narrative.json'))), historicNarrative);
  const panel = readJson(path.join(prior, 'evidence', 'round9-narrative.json'));
  assert.equal(panel.round, 9);
  assert.equal(panel.passed, false);
  assert.deepEqual(panel.failed, expectedFailed);
  // Precisely nine semantic edits: two spoken lines, one claim, six image prompts.
  const edited = Object.fromEntries(keys.map((key) => [key, structuredClone(JSON.parse(source[key]))]));
  const origin = edited.origin.scenes.find((scene) => scene.id === 'origin-01');
  const now = edited.now.scenes.find((scene) => scene.id === 'now-01');
  assert.equal(origin.lines[0].id, 'zc7k');
  assert.equal(now.lines[0].id, '7asx');
  const [originLine, nowLine, claim] = round10.changes;
  assert.deepEqual([originLine.line_id, nowLine.line_id, claim.claim_id], ['zc7k', '7asx', 'n1']);
  assert.equal(origin.lines[0].text, originLine.before);
  assert.equal(now.lines[0].text, nowLine.before);
  origin.lines[0].text = originLine.after;
  now.lines[0].text = nowLine.after;
  const n1 = edited.now.claims.find((row) => row.id === 'n1');
  assert.equal(n1.claim, claim.before);
  assert.deepEqual([n1.source, n1.fact, n1.verdict], [11, 9, 'PLAN']);
  n1.claim = claim.after;
  for (const row of prompts.changes) {
    const scene = edited[row.chapter].scenes.find((item) => item.id === row.scene_id);
    assert.ok(scene, `prompt scene ${row.scene_id}`);
    assert.equal(scene.data.prompt, row.before, `prompt before ${row.scene_id}`);
    assert.deepEqual(scene.lines.map((line) => line.id), row.line_ids, `line ids ${row.scene_id}`);
    scene.data.prompt = row.after;
  }
  for (const key of keys) {
    assert.deepEqual(edited[key], JSON.parse(target[key]), `unexpected semantic change in ${key}`);
    if (!changedChapters.includes(key)) assert.ok(source[key].equals(target[key]), `${key} must remain byte identical`);
  }
  return { source, target, round10, round11, prompts };
}

function requiredFiles(root, workdir) {
  const docs = path.join(root, 'docs', 'videos', slug);
  return {
    'auto.json': path.join(workdir, 'auto.json'),
    'review/narrative.json': path.join(workdir, 'review', 'narrative.json'),
    'series.json': path.join(docs, 'series.json'),
    'video.json': path.join(docs, 'video.json'),
    'script.md': path.join(docs, 'script.md'),
    'claims.md': path.join(docs, 'claims.md'),
    'verify-1.md': path.join(docs, 'verify-1.md'),
    ...Object.fromEntries(keys.map((key) => [`story/chapters/${key}.json`, chPath(workdir, key)])),
  };
}

function stateAssertions(state) {
  assert.equal(state.slug, slug);
  assert.equal(state.format, 'drama');
  assert.equal(state.status, 'blocked');
  assert.equal(state.blocked_kind, 'prompt_fixes:narrative');
  assert.equal(state.verified, true);
  assert.equal(state.listener_done, true);
  assert.equal(state.story?.narrative?.rounds, 9);
  assert.equal(state.story?.narrative?.passed, false);
  assert.deepEqual(state.story?.narrative?.failed, expectedFailed);
  assert.equal(state.story?.narrative_fixes, 2, 'narrative_fixes drift');
  assert.ok(state.story?.owner_note === null || state.story?.owner_note === undefined, 'owner note must be cleared');
  for (const key of keys) {
    const entry = state.story?.chapters?.[key];
    assert.equal(entry?.checked, true, `${key} checked`);
    assert.equal(entry?.listened, true, `${key} listened`);
    assert.ok(Number.isInteger(entry?.check_rounds) && entry.check_rounds >= 1, `${key} check rounds`);
  }
}

function safetyAssertions({ root, workdir, evidencePath, approvedReleaseSha256, approvedPanelRulesSha256, now }, packageData) {
  assert.match(approvedReleaseSha256 ?? '', /^[0-9a-f]{40}$/);
  assert.match(approvedPanelRulesSha256 ?? '', /^[0-9a-f]{64}$/);
  const evidenceBytes = regular(evidencePath);
  const e = JSON.parse(evidenceBytes);
  assert.equal(e.schema_version, 1);
  assert.equal(e.slug, slug);
  assert.equal(e.historical_source_composite_sha256, historicComposite, 'historical_source_composite mismatch');
  assert.equal(e.source_chapter_bundle_sha256, sourceBundleDigest, 'source_chapter_bundle mismatch');
  assert.equal(e.approved_release_sha, approvedReleaseSha256, 'approved_release_sha mismatch');
  assert.equal(e.observed_release_sha, approvedReleaseSha256, 'observed_release_sha mismatch');
  assert.equal(e.approved_panel_rules_sha256, approvedPanelRulesSha256, 'approved_panel_rules_sha256 mismatch');
  assert.equal(e.observed_panel_rules_sha256, approvedPanelRulesSha256, 'observed_panel_rules_sha256 mismatch');
  assert.ok(Number.isFinite(Date.parse(e.observed_at)), 'valid observation time');
  assert.ok(now - Date.parse(e.observed_at) >= 0 && now - Date.parse(e.observed_at) <= 300_000, 'safety evidence is stale');
  assert.equal(e.worker?.lease_active, false, 'lease_active must be false');
  assert.equal(e.worker?.pending_stage_jobs, 0, 'pending_stage_jobs must be zero');
  assert.equal(e.worker?.pending_media_jobs, 0, 'pending_media_jobs must be zero');
  assert.equal(e.worker?.pending_journal_entries, 0, 'pending_journal_entries must be zero');
  assert.equal(e.project?.retry_request_id, e.project?.retry_acknowledged_id, 'retry_request_id is pending');
  assert.equal(e.project?.status, 'blocked', 'project must remain blocked');
  assert.equal(e.settings?.drama_auto_approve_final, false, 'final auto-approval must be off');
  assert.equal(e.settings?.series_auto_continue, false, 'series auto-continuation must be off');
  assert.deepEqual(e.budget, {
    slug, limit_usd: '25.000000', reserved_usd: '0.000000', settled_usd: '0.000000',
    uncertain_usd: '0.000000', remaining_usd: '25.000000', operation_count: 0,
  }, 'budget ledger must be empty with USD25 remaining');
  const stop = path.join(workdir, 'STOP');
  assert.equal(regular(stop).toString('utf8'), 'A01 round11 offline fixture STOP\n', 'scoped STOP must be present');
  assert.equal(fs.existsSync(path.join(path.dirname(workdir), 'STOP')), false, 'global STOP is outside this transaction');
  for (const rel of ['story/reviews/script-review.json', 'timeline.json', 'final.mp4']) {
    assert.equal(fs.existsSync(path.join(workdir, rel)), false, `unexpected paid/review artifact ${rel}`);
  }
  const paths = requiredFiles(root, workdir);
  const originals = {};
  assert.deepEqual(Object.keys(e.files).sort(), Object.keys(paths).sort(), 'safety evidence file inventory');
  for (const [rel, file] of Object.entries(paths)) {
    originals[rel] = regular(file);
    assert.equal(sha(originals[rel]), e.files[rel], `live file drift ${rel}`);
  }
  for (const key of keys) {
    assert.equal(sha(originals[`story/chapters/${key}.json`]), packageData.round10.source_chapters_sha256[key], `source ${key}`);
  }
  assert.equal(bundleDigest(Object.fromEntries(keys.map((key) => [key, sha(originals[`story/chapters/${key}.json`])]))), sourceBundleDigest);
  assert.equal(sha(originals['review/narrative.json']), historicNarrative);
  assert.equal(sha(originals['series.json']), readJson(path.join(prior, 'prior-two-line', 'manifest.json')).source_series_sha256);
  assert.equal(sha(originals['video.json']), readJson(path.join(prior, 'prior-two-line', 'manifest.json')).source_video_sha256);
  const panel = JSON.parse(originals['review/narrative.json']);
  assert.equal(panel.round, 9);
  assert.equal(panel.passed, false);
  assert.deepEqual(panel.failed, expectedFailed);
  const state = JSON.parse(originals['auto.json']);
  stateAssertions(state);
  assert.equal(e.audit?.link_count, 80);
  assert.equal(e.audit?.source_composite_sha256, historicComposite);
  assert.match(e.audit?.tip_file ?? '', /^story\/recheck-audit\/[A-Za-z0-9._-]+\.json$/);
  const tip = regular(path.join(workdir, ...e.audit.tip_file.split('/')));
  assert.equal(sha(tip), e.audit.tip_sha256, 'audit tip drift');
  const tipRecord = JSON.parse(tip);
  assert.equal(tipRecord.link_count, 80, 'audit tip link count mismatch');
  assert.equal(tipRecord.after_source_composite_sha256, historicComposite, 'audit tip source composite mismatch');
  return { evidence: e, evidenceBytes, originals, paths, state, tip };
}

function postState(state) {
  const after = structuredClone(state);
  for (const key of ['origin', 'now']) {
    after.story.chapters[key].checked = false;
    after.story.chapters[key].listened = false;
  }
  after.verified = false;
  after.listener_done = false;
  return after;
}

function writeExact(file, bytes) {
  const temp = `${file}.${process.pid}.${randomUUID()}.tmp`;
  fs.writeFileSync(temp, bytes, { flag: 'wx' });
  fs.renameSync(temp, file);
}

function backupOriginals(workdir, originals, evidenceBytes, id, fault) {
  const base = path.join(workdir, 'manual-revisions', id);
  const parent = path.dirname(base);
  if (!fs.existsSync(parent)) fs.mkdirSync(parent);
  const parentStat = fs.lstatSync(parent);
  assert.ok(parentStat.isDirectory() && !parentStat.isSymbolicLink(), 'manual-revisions must be a real directory');
  assert.ok(inside(fs.realpathSync(parent), fs.realpathSync(workdir)), 'manual-revisions escaped the fixture');
  fs.mkdirSync(base, { recursive: false });
  for (const [rel, bytes] of Object.entries(originals)) {
    const target = path.join(base, 'before', ...rel.split('/'));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, bytes, { flag: 'wx' });
    assert.equal(sha(regular(target)), sha(bytes), `backup readback ${rel}`);
    fault(`after-backup-copy:${rel}`);
  }
  fs.writeFileSync(path.join(base, 'safety-evidence.json'), evidenceBytes, { flag: 'wx' });
  assert.equal(sha(regular(path.join(base, 'safety-evidence.json'))), sha(evidenceBytes));
  return base;
}

/** Inspect a local fixture. No writes; the historic composite is separately asserted from its audit tip. */
export function planOfflineInstallation(options) {
  const { root, workdir, evidencePath, approvedReleaseSha256, approvedPanelRulesSha256, now = Date.now() } = options;
  safeFixtureRoots(root, workdir);
  assertTreeRegular(root, workdir);
  const packageData = packageFiles();
  const pre = safetyAssertions({ root, workdir, evidencePath, approvedReleaseSha256, approvedPanelRulesSha256, now }, packageData);
  const nextState = postState(pre.state);
  const replacements = {
    ...Object.fromEntries(changedChapters.map((key) => [`story/chapters/${key}.json`, packageData.target[key]])),
    'auto.json': jsonBytes(nextState),
  };
  const inverse = Object.fromEntries(Object.entries(replacements).map(([rel, bytes]) => [rel, {
    before_sha256: sha(pre.originals[rel]), after_sha256: sha(bytes),
  }]));
  return { packageData, pre, replacements, inverse, targetBundleDigest };
}

/** Local fixture transaction only. A fault hook exists solely to exercise rollback tests. */
export function installOfflineFixture(options) {
  const plan = planOfflineInstallation(options);
  const { root, workdir, evidencePath, approvedReleaseSha256, approvedPanelRulesSha256, now = Date.now(), fault = () => {} } = options;
  const id = `offline-a01-round11-${new Date(now).toISOString().replaceAll(/[:.]/g, '-')}-${randomUUID()}`;
  const backup = backupOriginals(workdir, plan.pre.originals, plan.pre.evidenceBytes, id, fault);
  const manifest = {
    schema_version: 1, status: 'OFFLINE_FIXTURE_TRANSACTION', slug, id,
    historic_round9_composite_sha256: historicComposite,
    source_chapter_bundle_sha256: sourceBundleDigest,
    target_chapter_bundle_sha256: targetBundleDigest,
    previous_narrative_sha256: historicNarrative,
    previous_audit_sha256: plan.pre.evidence.audit.tip_sha256,
    safety_evidence_sha256: sha(plan.pre.evidenceBytes),
    inverse: plan.inverse,
    changed_semantic_fields: ['origin-01/zc7k/text', 'now-01/7asx/text', 'now/n1/claim', ...plan.packageData.prompts.changes.map((row) => `${row.scene_id}/prompt`)],
    untouched_history: true,
  };
  const manifestBytes = jsonBytes(manifest);
  fault('before-inverse-write');
  fs.writeFileSync(path.join(backup, 'inverse-manifest.json'), manifestBytes, { flag: 'wx' });
  assert.equal(sha(regular(path.join(backup, 'inverse-manifest.json'))), sha(manifestBytes));
  fault('after-inverse-write');
  const touched = [];
  const auditFile = path.join(workdir, 'story', 'recheck-audit', `${id}.json`);
  try {
    fault('after-backup');
    for (const [rel, bytes] of Object.entries(plan.pre.originals)) {
      assert.equal(sha(regular(path.join(backup, 'before', ...rel.split('/')))), sha(bytes), `backup drift ${rel}`);
    }
    assert.equal(sha(regular(path.join(backup, 'safety-evidence.json'))), sha(plan.pre.evidenceBytes), 'backup evidence drift');
    // Recheck every source byte and all external safety evidence immediately before commit.
    const fresh = planOfflineInstallation({ root, workdir, evidencePath, approvedReleaseSha256, approvedPanelRulesSha256, now });
    assert.deepEqual(fresh.inverse, plan.inverse, 'precommit drift');
    assert.equal(sha(fresh.pre.evidenceBytes), sha(plan.pre.evidenceBytes), 'precommit safety evidence drift');
    for (const [rel, bytes] of Object.entries(plan.replacements)) {
      writeExact(plan.pre.paths[rel], bytes);
      touched.push(rel);
      fault(`after-write:${rel}`);
    }
    for (const [rel, bytes] of Object.entries(plan.replacements)) {
      assert.equal(sha(regular(plan.pre.paths[rel])), sha(bytes), `replacement readback ${rel}`);
    }
    for (const rel of Object.keys(plan.pre.paths).filter((name) => !own(plan.replacements, name))) {
      assert.equal(sha(regular(plan.pre.paths[rel])), sha(plan.pre.originals[rel]), `untouched readback ${rel}`);
    }
    assert.equal(bundleDigest(Object.fromEntries(keys.map((key) => [key, sha(regular(chPath(workdir, key)))]))), targetBundleDigest);
    assert.deepEqual(readJson(path.join(workdir, 'auto.json')), postState(plan.pre.state));
    assert.equal(sha(regular(path.join(workdir, 'review', 'narrative.json'))), historicNarrative);
    fault('before-audit');
    const audit = {
      schema_version: 1, kind: 'offline_a01_round11_install', slug, id,
      link_count: 81, previous_audit_sha256: plan.pre.evidence.audit.tip_sha256,
      before_historic_source_composite_sha256: historicComposite,
      before_chapter_bundle_sha256: sourceBundleDigest,
      after_chapter_bundle_sha256: targetBundleDigest,
      before_narrative_sha256: historicNarrative,
      after_narrative_sha256: sha(regular(path.join(workdir, 'review', 'narrative.json'))),
      backup_manifest_sha256: sha(manifestBytes),
      safety_evidence_sha256: sha(plan.pre.evidenceBytes),
      paid_calls: 0,
    };
    fs.writeFileSync(auditFile, jsonBytes(audit), { flag: 'wx' });
    assert.deepEqual(readJson(auditFile), audit);
    fault('after-audit');
    const receipt = { ...audit, status: 'OFFLINE_ONLY_NOT_APPROVED', audit_sha256: sha(regular(auditFile)) };
    fs.writeFileSync(path.join(backup, 'receipt.json'), jsonBytes(receipt), { flag: 'wx' });
    assert.deepEqual(readJson(path.join(backup, 'receipt.json')), receipt);
    return { backup, auditFile, receipt };
  } catch (error) {
    let rollbackError = null;
    try {
      for (const rel of touched.reverse()) {
        const current = sha(regular(plan.pre.paths[rel]));
        assert.ok([plan.inverse[rel].before_sha256, plan.inverse[rel].after_sha256].includes(current), `unexpected concurrent edit of ${rel}`);
        writeExact(plan.pre.paths[rel], plan.pre.originals[rel]);
        assert.equal(sha(regular(plan.pre.paths[rel])), plan.inverse[rel].before_sha256, `rollback readback ${rel}`);
      }
      if (fs.existsSync(auditFile)) {
        // Preserve the attempted audit as evidence. It is explicitly marked rolled back.
        fs.writeFileSync(path.join(backup, 'rolled-back-audit.json'), regular(auditFile), { flag: 'wx' });
        fs.unlinkSync(auditFile);
      }
      for (const [rel, bytes] of Object.entries(plan.pre.originals)) {
        assert.equal(sha(regular(plan.pre.paths[rel])), sha(bytes), `full rollback ${rel}`);
      }
    } catch (failure) { rollbackError = failure; }
    fs.writeFileSync(path.join(backup, 'failure.json'), jsonBytes({
      status: rollbackError ? 'MANUAL_RECOVERY_REQUIRED' : 'ROLLED_BACK',
      original_error: String(error), rollback_error: rollbackError ? String(rollbackError) : null,
    }), { flag: 'wx' });
    if (rollbackError) throw new AggregateError([error, rollbackError], `offline fixture rollback failed: ${backup}`);
    throw error;
  }
}

export const OFFLINE_CONSTANTS = Object.freeze({ slug, keys, historicComposite, historicNarrative, sourceBundleDigest, targetBundleDigest });
