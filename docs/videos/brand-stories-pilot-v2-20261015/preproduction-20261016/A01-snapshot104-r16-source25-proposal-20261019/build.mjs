// A01 104 -> proposed 105, offline only. This file has no host, DB, provider or
// production install path. --write is restricted to this new proposal directory.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { buildArtifacts as verifyBridge } from '../A01-r12-snapshot104-six-chapter-bridge-20261018/check.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.dirname(here);
const bridgeDir = path.join(parent, 'A01-r12-snapshot104-six-chapter-bridge-20261018');
const editorialDir = path.join(parent, 'A01-editorial-candidate-20261019-r16');
const sourcePlanDir = path.join(parent, 'A01-r16-source-plan-25-candidate-20261019');
const slug = 'story-rolling-suitcase-v2';
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const editorialManifestSha = '5dade9fcd0f76c03b2c463addef935b0764d8d78eda9c621bb18e9bff462edef';
const editorialReviewSha = '4db1831aef48d21b1f37e28a29caab9be6f289b0909458fed38b969acb81c347';
const sourcePlanManifestSha = '61257b4687f232fa8a963332f4c8fab988a83565ce4f08615c5e0ceeac7d449a';
const sourcePlanReviewSha = 'e95f38ed263c4126b0c5a7278d223c5a1ddd420a44f3634b55cd4496f9915e3f';
const sourcePlanSeriesSha = '123a85e29f309811069c692a821ca24e1b542ef7aff399f32495b9296e3eee3a';
const sourcePlanAlignmentSha = 'fbb54cbac5e37c0b981e5807671491a20fb9eaa86d1f7aa55470f92bce7afeea';
const source104 = 'e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');

function exact(file) {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
}
const parse = (file) => JSON.parse(exact(file).toString('utf8'));
function inventory(root) {
  assert.ok(path.isAbsolute(root), 'absolute capture path required');
  const rows = [];
  function visit(dir, rel = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      assert.ok(!entry.isSymbolicLink(), 'capture symlink refused');
      const name = rel ? `${rel}/${entry.name}` : entry.name;
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(file, name);
      else { assert.ok(entry.isFile(), 'capture special file refused'); rows.push([name, sha(exact(file))]); }
    }
  }
  visit(root);
  rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { count: rows.length, sha256: sha(rows.map(([rel, hash]) => `${rel}\0${hash}\n`).join('')), rows };
}
function claimRows(file) {
  const rows = new Map();
  let key = null;
  for (const line of exact(file).toString('utf8').split(/\r?\n/u)) {
    const heading = /^## .*（(hook|origin|idea|engine|turn|now)）$/u.exec(line);
    if (heading) { key = heading[1]; continue; }
    if (!/^[a-z]\d+[a-z]?｜/u.test(line)) continue;
    const cells = line.split('｜');
    assert.equal(cells.length, 6, 'claim row format drift');
    const [id, claim, url, checked, scene, verdict] = cells;
    assert.ok(key && claim && /^https:\/\//u.test(url) && /^\d{4}-\d{2}-\d{2}$/u.test(checked));
    assert.equal(verdict, 'PENDING', `editorial claim ${id} falsely reviewed`);
    assert.ok(!rows.has(id), `duplicate claim ${id}`);
    rows.set(id, { id, claim, url, checked, scene, chapter: key });
  }
  return rows;
}
function ids(chapters, field) {
  const result = new Map();
  for (const key of keys) {
    for (const scene of chapters[key].scenes) {
      if (field === 'scene') result.set(scene.id, { chapter: key, value: scene });
      if (field === 'line') for (const line of scene.lines ?? []) result.set(line.id, { chapter: key, scene: scene.id, value: line });
    }
    if (field === 'claim') for (const claim of chapters[key].claims ?? []) result.set(claim.id, { chapter: key, scene: claim.scene, value: claim });
  }
  return result;
}
function mapIds(before, after, field) {
  const left = ids(before, field), right = ids(after, field);
  return {
    retired: [...left.keys()].filter((id) => !right.has(id)).sort(),
    added: [...right.keys()].filter((id) => !left.has(id)).sort(),
    retained: [...right.keys()].filter((id) => left.has(id)).sort().map((id) => ({
      id, before_sha256: sha(JSON.stringify(left.get(id).value)),
      proposed_sha256: sha(JSON.stringify(right.get(id).value)),
      before_chapter: left.get(id).chapter, proposed_chapter: right.get(id).chapter,
    })),
  };
}

export async function buildProposal({ snapshotRoot, currentRoot, verifiedFile, workerFile, workerRoot }) {
  for (const value of [snapshotRoot, currentRoot, verifiedFile, workerFile, workerRoot])
    assert.ok(path.isAbsolute(value), 'all evidence and worker paths must be absolute');
  // Existing bridge checks the independently verified 104-link receipt, the 254-file
  // historical snapshot, current 254-file capture, and their sole shared-lexicon delta.
  const baseline = verifyBridge(snapshotRoot, verifiedFile, currentRoot);
  for (const [rel, bytes] of baseline)
    assert.ok(exact(path.join(bridgeDir, rel)).equals(bytes), `104 bridge drift: ${rel}`);
  const currentInventory = inventory(currentRoot);
  assert.equal(currentInventory.count, 254);
  assert.equal(currentInventory.sha256,
    JSON.parse(baseline.get('current-capture-assessment.json')).current_capture_inventory_sha256);
  const sourceRoot = path.join(currentRoot, slug);
  const eventRoot = path.join(sourceRoot, 'story', 'recheck-audit');
  const eventDirs = fs.readdirSync(eventRoot, { withFileTypes: true });
  assert.equal(eventDirs.length, 104, '104 event directories required');
  assert.ok(eventDirs.every((item) => item.isDirectory() && !item.isSymbolicLink()));
  const oldAuditInventory = inventory(eventRoot);
  const tips = eventDirs.map((item) => ({ id: item.name, index: parse(path.join(eventRoot, item.name, 'index.json')) }))
    .filter(({ index }) => index.after_source_sha256 === source104);
  assert.equal(tips.length, 1, '104 tip must be unique');
  const tip = tips[0];
  assert.equal(sha(JSON.stringify(tip.index.after)), source104, '104 source composite drift');
  assert.equal(tip.index.pilot ?? tip.index.after.pilot, null, 'old script review receipt unexpectedly present');
  const oldChapters = Object.fromEntries(keys.map((key) => [key,
    parse(path.join(sourceRoot, 'story', 'chapters', `${key}.json`))]));
  for (const key of keys)
    assert.equal(sha(exact(path.join(sourceRoot, 'story', 'chapters', `${key}.json`))), tip.index.after.chapters[key]);
  const oldAuto = parse(path.join(sourceRoot, 'auto.json'));
  assert.equal(sha(exact(path.join(sourceRoot, 'auto.json'))), tip.index.after.auto);
  const capturedSeriesBytes = exact(path.join(currentRoot, 'docs', 'videos', slug, 'series.json'));
  assert.equal(sha(capturedSeriesBytes), tip.index.after.series, '104 live series drift');
  assert.equal(JSON.parse(capturedSeriesBytes).plan.sources.length, 13, '104 live source count drift');
  assert.equal(oldAuto.status, 'blocked');
  assert.equal(oldAuto.blocked_kind, 'prompt_fixes:narrative');
  assert.equal(oldAuto.story.narrative.passed, false);
  assert.equal(oldAuto.story.narrative.rounds, 11);
  assert.equal(oldAuto.target_minutes, 10);
  assert.deepEqual(parse(path.join(currentRoot, 'docs', 'videos', slug, 'video.json')).target_minutes, [9, 11]);
  assert.equal(sha(exact(path.join(editorialDir, 'manifest.json'))), editorialManifestSha, 'r16 manifest drift');
  const manifest = parse(path.join(editorialDir, 'manifest.json'));
  const reviewBytes = exact(path.join(editorialDir, 'independent-review-20261019.md'));
  const reviewText = reviewBytes.toString('utf8');
  assert.equal(sha(reviewBytes), editorialReviewSha, 'r16 offline review drift');
  assert.ok(reviewText.includes(editorialManifestSha.toUpperCase())
    && reviewText.includes('P0 = 0') && reviewText.includes('P1 = 0')
    && reviewText.includes('P2 = 0') && reviewText.includes('HOLD'),
  'r16 offline review conclusion drift');
  assert.ok(manifest.status.includes('HOLD') && manifest.authorizes_host_install_or_paid_media === false);
  assert.equal(sha(exact(path.join(editorialDir, 'build.mjs'))), manifest.build_sha256);
  assert.equal(sha(exact(path.join(editorialDir, 'README.md'))), manifest.readme_sha256);
  for (const [rel, hash] of Object.entries(manifest.outputs_sha256))
    assert.equal(sha(exact(path.join(editorialDir, rel))), hash, `r16 output drift: ${rel}`);
  const editorial = parse(path.join(editorialDir, 'candidate', 'video.json'));
  const editorialSeries = parse(path.join(editorialDir, 'candidate', 'series.json'));
  assert.equal(sha(exact(path.join(sourcePlanDir, 'manifest.json'))), sourcePlanManifestSha,
    'corrected 25-source plan manifest drift');
  const sourcePlanManifest = parse(path.join(sourcePlanDir, 'manifest.json'));
  assert.equal(sourcePlanManifest.status, 'HOLD_OFFLINE_SOURCE_PLAN_METADATA_ONLY');
  assert.equal(sourcePlanManifest.correction_only, 'plan.sources[23].publisher');
  assert.equal(sourcePlanManifest.direct_host_adoption_allowed, false);
  const sourcePlanReview = exact(path.join(sourcePlanDir, 'independent-review-20261019.md'));
  assert.equal(sha(sourcePlanReview), sourcePlanReviewSha, 'corrected source-plan review drift');
  const sourcePlanReviewText = sourcePlanReview.toString('utf8');
  assert.ok(sourcePlanReviewText.includes(sourcePlanManifestSha.toUpperCase())
    && sourcePlanReviewText.includes('P0 = 0') && sourcePlanReviewText.includes('P1 = 0')
    && sourcePlanReviewText.includes('P2 = 0') && sourcePlanReviewText.includes('HOLD'),
  'corrected source-plan limited-review conclusion drift');
  assert.equal(sourcePlanManifest.outputs_sha256['candidate/series.json'], sourcePlanSeriesSha);
  assert.equal(sourcePlanManifest.outputs_sha256['source-alignment.json'], sourcePlanAlignmentSha);
  assert.equal(sourcePlanManifest.input_sha256.bridge_series, sha(baseline.get('candidate/series.json')));
  assert.equal(sha(exact(path.join(sourcePlanDir, 'build.mjs'))), sourcePlanManifest.build_sha256);
  assert.equal(sha(exact(path.join(sourcePlanDir, 'README.md'))), sourcePlanManifest.readme_sha256);
  assert.equal(sha(exact(path.join(sourcePlanDir, 'candidate', 'series.json'))), sourcePlanSeriesSha);
  assert.equal(sha(exact(path.join(sourcePlanDir, 'source-alignment.json'))), sourcePlanAlignmentSha);
  const series = parse(path.join(sourcePlanDir, 'candidate', 'series.json'));
  const bridgeSeries = JSON.parse(baseline.get('candidate/series.json'));
  assert.equal(bridgeSeries.plan.sources[23].publisher, 'Plath 2024 年校友刊自述（第 17 頁）');
  assert.equal(series.plan.sources[23].publisher, 'West Seattle High School Alumni Association《Chinook》');
  const revertedSeries = structuredClone(series);
  revertedSeries.plan.sources[23].publisher = bridgeSeries.plan.sources[23].publisher;
  assert.deepEqual(revertedSeries, bridgeSeries, 'source plan must change only index 23 publisher');
  const alignment = parse(path.join(sourcePlanDir, 'source-alignment.json'));
  assert.deepEqual(alignment.counts, {
    live_snapshot104_plan_sources_reported: 13, editorial_plan_sources: 23,
    proposed_plan_sources: 25, cited_public_sources: 18, cited_claims: 78,
  });
  assert.equal(alignment.live_snapshot104_series_sha256_reported_not_recomputed_by_this_check,
    sha(capturedSeriesBytes), 'source-plan captured 104 series hash drift');
  assert.equal(alignment.formal_script_review_receipt_issued, false);
  const alignedClaims = new Map(alignment.claim_source_rows.map((row) => [row.id, row]));
  assert.equal(alignment.claim_source_rows.length, 78);
  assert.equal(alignedClaims.size, 78);
  assert.deepEqual(editorial.target_minutes, [7, 8]);
  assert.equal(editorial.scenes.length, 65);
  assert.equal(editorial.scenes.flatMap((scene) => scene.lines ?? []).length, 77);
  assert.equal(editorial.sources.length, 18);
  assert.equal(editorialSeries.plan.sources.length, 23);
  assert.equal(series.plan.sources.length, 25);
  assert.deepEqual(editorialSeries.plan.sources.map((s) => s.url), series.plan.sources.slice(0, 23).map((s) => s.url));
  assert.deepEqual(editorialSeries.plan.must_verify, series.plan.must_verify, 'must_verify source indices drift');
  const editorialClaims = claimRows(path.join(editorialDir, 'candidate', 'claims.md'));
  assert.equal(editorialClaims.size, 78);
  const bridgeChapters = Object.fromEntries(keys.map((key) => [key,
    JSON.parse(baseline.get(`candidate/chapters/${key}.json`))]));
  const bridgeClaims = ids(bridgeChapters, 'claim');
  assert.equal(bridgeClaims.size, 78);
  const sourceByUrl = new Map(series.plan.sources.map((item, index) => [item.url, index]));
  const publicUrls = new Set(editorial.sources.map((item) => item.url));
  assert.equal(publicUrls.size, 18);
  assert.equal(series.plan.sources.filter((item) => !publicUrls.has(item.url)).length, 7);
  const chapters = {};
  for (const key of keys) {
    const original = bridgeChapters[key];
    const scenes = editorial.scenes.filter((scene) => scene.id.startsWith(`${key}-`));
    assert.ok(scenes.length > 0);
    const sceneIds = new Set(scenes.map((scene) => scene.id));
    assert.equal(scenes[0].chapter, original.title, `chapter title drift ${key}`);
    const claims = [...editorialClaims.values()].filter((row) => row.chapter === key).map((row) => {
      const before = bridgeClaims.get(row.id);
      assert.ok(before && before.chapter === key && before.value.claim === row.claim
        && before.scene === row.scene && sceneIds.has(row.scene), `claim binding drift ${row.id}`);
      assert.equal(series.plan.sources[before.value.source].url, row.url, `source binding drift ${row.id}`);
      const sourceAlignment = alignedClaims.get(row.id);
      assert.ok(sourceAlignment && sourceAlignment.plan_source_index === before.value.source
        && sourceAlignment.url === row.url
        && editorial.sources[sourceAlignment.public_source_index]?.url === row.url,
      `corrected source-plan alignment drift ${row.id}`);
      return { ...before.value, verdict: 'UNCHECKED' };
    });
    for (const scene of scenes) {
      assert.deepEqual(scene.claims ?? [], claims.filter((row) => row.scene === scene.id).map((row) => row.id), `scene claim drift ${scene.id}`);
      assert.ok(scene.lines.every((line) => line.id && line.text));
    }
    chapters[key] = { ...original,
      scenes: scenes.map(({ chapter: _chapter, claims: _claims, ...scene }) => scene),
      claims, report: 'OFFLINE_PROPOSAL_ONLY: formal verifier, listener and narrative review must rerun on exact saved bytes.' };
  }
  assert.equal(ids(chapters, 'scene').size, 65);
  assert.equal(ids(chapters, 'line').size, 77);
  assert.equal(ids(chapters, 'claim').size, 78);
  const workerBytes = exact(workerFile);
  const { composeStory } = await import(pathToFileURL(workerFile).href);
  assert.equal(typeof composeStory, 'function');
  const composed = composeStory({ slug, info: series, chapters, voice: editorial.voice, root: workerRoot,
    videoId: editorial.youtube?.video_id ?? null });
  assert.deepEqual(composed.target_minutes, [7, 8], '#1563 duration behavior missing');
  assert.equal(composed.scenes.length, 65);
  assert.equal(composed.sources.length, 25, 'source-filter assumption changed; re-review proposal');
  assert.equal(composed.sources[23].url, series.plan.sources[23].url);
  assert.equal(composed.sources[23].title, series.plan.sources[23].publisher,
    'corrected source publisher must propagate to diagnostic video title');
  for (let index = 0; index < 65; index++) {
    const a = composed.scenes[index], b = editorial.scenes[index];
    assert.equal(a.id, b.id);
    assert.deepEqual(a.lines, b.lines, `line drift ${a.id}`);
    assert.deepEqual(a.data, b.data, `visual drift ${a.id}`);
    assert.deepEqual(a.claims ?? [], b.claims?.length ? b.claims : [], `claim-ref drift ${a.id}`);
  }
  const state = structuredClone(oldAuto);
  state.target_minutes = 8;
  state.verified = false;
  state.listener_done = false;
  state.status = 'blocked';
  state.blocked_kind = 'pilot_script_review';
  state.blocked = 'OFFLINE PROPOSAL ONLY: 104→105 chapter revision, public-source filter, formal checks and owner-scoped adoption pending.';
  state.story.narrative = null;
  state.story.narrative_fixes = 0;
  state.story.length = null;
  state.story.audio_review = null;
  state.story.owner_note = null;
  for (const key of keys) {
    const entry = state.story.chapters[key];
    assert.ok(entry.written && entry.checked && entry.listened, `old chapter state drift ${key}`);
    entry.checked = false;
    entry.listened = false;
    entry.check_rounds = 0;
    entry.lint_fixes = 0;
    entry.lint = null;
    delete entry.changed;
  }
  const eventId = `r16-existing-revision-${editorialManifestSha.slice(0, 16)}`;
  const changes = new Map([
    [`${slug}/auto.json`, json(state)],
    [`docs/videos/${slug}/series.json`, json(series)],
    [`docs/videos/${slug}/video.json`, json(composed)],
    ...keys.map((key) => [`${slug}/story/chapters/${key}.json`, json(chapters[key])]),
  ]);
  const after = structuredClone(tip.index.after);
  after.auto = sha(changes.get(`${slug}/auto.json`));
  after.series = sha(changes.get(`docs/videos/${slug}/series.json`));
  after.video = sha(changes.get(`docs/videos/${slug}/video.json`));
  for (const key of keys) after.chapters[key] = sha(changes.get(`${slug}/story/chapters/${key}.json`));
  assert.equal(after.pilot, null);
  for (const key of ['claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify'])
    assert.deepEqual(after[key], tip.index.after[key], `historical ${key} changed`);
  const afterSha = sha(JSON.stringify(after));
  const mapping = { schema_version: 1, status: 'OFFLINE_R16_MAPPING_HOLD',
    source104_sha256: source104, r16_manifest_sha256: editorialManifestSha,
    ids: Object.fromEntries(['scene', 'line', 'claim'].map((field) => [field, mapIds(oldChapters, chapters, field)])),
    claim_id_note: 'turn-09/t7b is provisional; formal verifier numberClaims may renumber it. Rebuild all bound hashes after saved verifier output.',
    claims_reset_to_unchecked: 78, old_claim_verdicts_not_inherited: true };
  const gates = { schema_version: 1, status: 'PROPOSAL_ONLY_HOLD',
    before_links: 104, proposed_links: 105, before_source_sha256: source104,
    proposed_source_sha256: afterSha, capture_inventory_sha256: currentInventory.sha256,
    editorial_manifest_sha256: editorialManifestSha, worker_story_sha256: sha(workerBytes),
    editorial_offline_review_sha256: editorialReviewSha,
    corrected_source_plan_manifest_sha256: sourcePlanManifestSha,
    corrected_source_plan_limited_review_sha256: sourcePlanReviewSha,
    corrected_source_plan_series_sha256: sourcePlanSeriesSha,
    corrected_source_plan_alignment_sha256: sourcePlanAlignmentSha,
    owner_body_target_minutes: [7, 8], persisted_proposed_body_target_minutes: composed.target_minutes,
    captured_live_plan_sources: 13, editorial_plan_sources: 23,
    plan_sources_retained: 25, composed_public_sources_now: composed.sources.length,
    editorial_public_sources_required: 18, separate_a01_public_source_filter_required: true,
    source_filter_deployed: false, production_worker_1563_deployed: false,
    source_capture_provenance_freshness_requires_recheck: true,
    current_host_stop_lease_jobs_budget_requires_recheck: true,
    provisional_claim_id_t7b_requires_formal_rebind: true,
    stale_script_claims_verify_narrative_are_not_approvals: true,
    exact_formal_verifier_listener_two_reader_review_and_receipt_required: true,
    review_receipt_issued: false, production_status: 'HOLD',
    installation_allowed: false, paid_work_allowed: false };
  const event = { schema_version: 1, slug, id: eventId,
    result_kind: 'OFFLINE_PROPOSAL_ONLY_DO_NOT_INSTALL',
    before_source_sha256: source104, after_source_sha256: afterSha,
    before: tip.index.after, after, journals: [],
    source_manifest_sha256: editorialManifestSha, worker_story_sha256: sha(workerBytes),
    editorial_offline_review_sha256: editorialReviewSha,
    corrected_source_plan_manifest_sha256: sourcePlanManifestSha,
    corrected_source_plan_limited_review_sha256: sourcePlanReviewSha,
    corrected_source_plan_series_sha256: sourcePlanSeriesSha,
    old_index_sha256: sha(exact(path.join(eventRoot, tip.id, 'index.json'))),
    old_event_count: 104, old_audit_files_immutable: true,
    old_audit_inventory_sha256: oldAuditInventory.sha256,
    old_audit_file_count: oldAuditInventory.count,
    proposed_changed_paths: [...changes.keys()],
    retained_stale_outputs: ['claims.md', 'script.md', 'verify-1.md', 'review/narrative.json'],
    status: 'HOLD', approval_or_production_write: false };
  const outputs = new Map([
    ...keys.map((key) => [`candidate/chapters/${key}.json`, json(chapters[key])]),
    ['candidate/series.json', json(series)], ['candidate/video.json', json(composed)],
    ['candidate/auto.json', json(state)], ['mapping.json', json(mapping)],
    ['gates.json', json(gates)], ['event-proposal.json', json(event)],
  ]);
  return { outputs, changes, gates, event, currentInventory };
}

function argsFromCli(argv) {
  assert.ok(argv.length === 11 && ['--write', '--check'].includes(argv[0])
    && argv[1] === '--snapshot' && argv[3] === '--verified'
    && argv[5] === '--current' && argv[7] === '--worker'
    && argv[9] === '--worker-root',
  'use --check|--write --snapshot ABS --verified ABS --current ABS --worker ABS --worker-root ABS');
  return { mode: argv[0], snapshotRoot: argv[2], verifiedFile: argv[4],
    currentRoot: argv[6], workerFile: argv[8], workerRoot: argv[10] };
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { mode, ...options } = argsFromCli(process.argv.slice(2));
    const { outputs, gates } = await buildProposal(options);
    const manifest = { schema_version: 1, status: 'OFFLINE_PROPOSAL_HOLD',
      r16_manifest_sha256: editorialManifestSha, r16_offline_review_sha256: editorialReviewSha,
      corrected_source_plan_manifest_sha256: sourcePlanManifestSha,
      corrected_source_plan_limited_review_sha256: sourcePlanReviewSha,
      build_sha256: sha(exact(path.join(here, 'build.mjs'))),
      readme_sha256: sha(exact(path.join(here, 'README.md'))),
      fixture_sha256: sha(exact(path.join(here, 'fixture.mjs'))),
      fixture_test_sha256: sha(exact(path.join(here, 'fixture.test.mjs'))),
      outputs_sha256: Object.fromEntries([...outputs].map(([rel, bytes]) => [rel, sha(bytes)])),
      host_writes: 0, paid_calls: 0, production_status: 'HOLD' };
    outputs.set('manifest.json', json(manifest));
    for (const [rel, bytes] of outputs) {
      const file = path.join(here, rel);
      assert.ok(file.startsWith(here + path.sep), 'proposal path escaped');
      if (mode === '--write') {
        assert.ok(!fs.existsSync(file), `refuse to overwrite: ${rel}`);
        fs.mkdirSync(path.dirname(file), { recursive: true });
        fs.writeFileSync(file, bytes, { flag: 'wx' });
      } else assert.ok(exact(file).equals(bytes), `proposal replay mismatch: ${rel}`);
    }
    console.log(JSON.stringify({ status: gates.status, files: outputs.size, before_links: 104,
      proposed_links: 105, chapters: 6, scenes: 65, lines: 77, claims: 78,
      current_public_sources: 25, required_public_sources: 18, writes: mode === '--write' ? outputs.size : 0 }));
  } catch (error) { console.error(`HOLD: ${error.message}`); process.exitCode = 2; }
}
