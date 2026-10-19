// Build fresh A01 104 -> 105 target bytes. The r23 offline manuscript is
// evidence/input, never a file bundle copied wholesale to the host.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { SLUG, CHAPTERS, changedPaths, sourceHash,
  auditInventory, afterTuple, PRODUCTION_104_PINS,
  REJECTED_R23_MANIFEST_SHA256 } from './transaction.mjs';
import { verifySource104 } from './source-104.mjs';
import { verifyFresh104 } from './verify-fresh-104.mjs';

const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const exact = (file) => {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
};
const parse = (file) => JSON.parse(exact(file));
const claimRow = /^([a-z]\d+[a-z]?)｜([^｜]+)｜(https:\/\/[^｜]+)｜(\d{4}-\d{2}-\d{2})｜([^｜]+)｜PENDING$/u;
const VERIFIED_104 = PRODUCTION_104_PINS;
const R23_MANIFEST_SHA256 = 'a5978f8318c87e62f48d9e00330fcdc45ffaf50161601d99017922f4af888cf4';
const R23_OUTPUTS = Object.freeze([
  'candidate/video.json', 'candidate/series.json', 'candidate/lexicon.json',
  'candidate/script.md', 'candidate/claims.md', 'source-map.json',
  'source-alignment.json', 'validation.json', 'plan-source-addition.json',
  'proposed-25-source-series.json',
]);

function claims(file) {
  const rows = new Map();
  let chapter = null;
  for (const line of exact(file).toString('utf8').split(/\r?\n/u)) {
    const header = /^## .*（(hook|origin|idea|engine|turn|now)）$/u.exec(line);
    if (header) { chapter = header[1]; continue; }
    const match = claimRow.exec(line);
    if (!match) continue;
    const [, id, claim, url, checked, scene] = match;
    assert.ok(chapter && !rows.has(id));
    rows.set(id, { id, claim, url, checked, scene, chapter });
  }
  assert.equal(rows.size, 74, 'r23 claim count changed');
  return rows;
}
function checkEditorial(editorialDir) {
  assert.equal(fs.realpathSync(editorialDir), path.resolve(editorialDir),
    'editorial directory link refused');
  const manifestBytes = exact(path.join(editorialDir, 'manifest.json'));
  assert.equal(sha(manifestBytes), R23_MANIFEST_SHA256, 'reviewed r23 manifest changed');
  const manifest = JSON.parse(manifestBytes);
  assert.equal(manifest.slug, SLUG);
  assert.equal(manifest.status, 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE');
  assert.equal(manifest.authorizes_host_install_or_paid_media, false);
  assert.deepEqual(Object.keys(manifest.outputs_sha256).sort(), [...R23_OUTPUTS].sort(),
    'r23 output allowlist changed');
  for (const [relative, digest] of Object.entries(manifest.outputs_sha256)) {
    const file = path.join(editorialDir, relative);
    assert.equal(fs.realpathSync(file), path.resolve(file), 'editorial output link refused');
    assert.equal(sha(exact(file)), digest,
      `editorial output changed: ${relative}`);
  }
  assert.equal(sha(exact(path.join(editorialDir, 'build.mjs'))), manifest.build_sha256);
  const video = parse(path.join(editorialDir, 'candidate', 'video.json'));
  const series = parse(path.join(editorialDir, 'proposed-25-source-series.json'));
  const alignment = parse(path.join(editorialDir, 'source-alignment.json'));
  assert.deepEqual(video.target_minutes, [7, 8]);
  assert.equal(video.scenes.length, 65);
  assert.equal(video.scenes.flatMap((scene) => scene.lines ?? []).length, 76);
  assert.equal(video.sources.length, 18);
  assert.equal(new Set(video.sources.map((item) => item.url)).size, 18);
  assert.equal(series.plan.sources.length, 25);
  assert.equal(alignment.claim_source_rows.length, 74);
  assert.equal(alignment.counts.cited_public_sources, 18);
  assert.equal(alignment.counts.proposed_plan_sources, 25);
  return { manifestSha: sha(manifestBytes), video, series, alignment,
    claimRows: claims(path.join(editorialDir, 'candidate', 'claims.md')) };
}
export function chapterHeading(key, scenes) {
  assert.ok(scenes.length > 0 && typeof scenes[0].chapter === 'string'
    && scenes[0].chapter.trim().length > 0, `chapter heading missing: ${key}`);
  assert.ok(scenes.every((scene) => scene.id.startsWith(`${key}-`)),
    `chapter scene leaked across sections: ${key}`);
  assert.ok(scenes.slice(1).every((scene) => scene.chapter === undefined),
    `chapter heading appears after first scene: ${key}`);
  return scenes[0].chapter;
}
export function reviewedChapterLoops(video) {
  assert.equal(video.loops?.length, 11, 'r23 loop count changed');
  const lineOrder = new Map();
  let order = 0;
  for (const scene of video.scenes) {
    const key = CHAPTERS.find((name) => scene.id.startsWith(`${name}-`));
    assert.ok(key, `scene outside six chapters: ${scene.id}`);
    for (const line of scene.lines ?? []) {
      assert.ok(typeof line.id === 'string' && !lineOrder.has(line.id),
        `missing or duplicate line ID: ${line.id}`);
      lineOrder.set(line.id, { key, order: order++ });
    }
  }
  const loops = Object.fromEntries(CHAPTERS.map((key) => [key, []]));
  const seen = new Set();
  for (const loop of video.loops) {
    const setup = lineOrder.get(loop.setup);
    const payoff = lineOrder.get(loop.payoff);
    assert.ok(setup && payoff && setup.order < payoff.order
      && typeof loop.what === 'string' && loop.what.trim().length > 0
      && !seen.has(loop.setup), `invalid reviewed loop: ${loop.setup}`);
    seen.add(loop.setup);
    loops[setup.key].push({ setup: loop.setup, payoff: loop.payoff, what: loop.what });
  }
  return loops;
}
function chapterTarget(roots, editorial) {
  const aligned = new Map(editorial.alignment.claim_source_rows.map((row) => [row.id, row]));
  assert.equal(aligned.size, 74);
  const current = Object.fromEntries(CHAPTERS.map((key) => [key,
    parse(path.join(roots.work, SLUG, 'story', 'chapters', `${key}.json`))]));
  const r23Loops = reviewedChapterLoops(editorial.video);
  const thumbnailShot = editorial.video.thumbnail?.data?.shot;
  assert.ok(typeof thumbnailShot === 'string' && editorial.video.scenes.some((scene) =>
    scene.id === thumbnailShot && scene.id.startsWith('hook-') && scene.template === 'shot'),
  'r23 thumbnail shot changed');
  const chapters = {};
  for (const key of CHAPTERS) {
    const scenes = editorial.video.scenes.filter((scene) => scene.id.startsWith(`${key}-`));
    const title = chapterHeading(key, scenes);
    const sceneIds = new Set(scenes.map((scene) => scene.id));
    const rows = [...editorial.claimRows.values()].filter((row) => row.chapter === key);
    const claimData = rows.map((row) => {
      const reference = aligned.get(row.id);
      assert.ok(reference && reference.url === row.url
        && editorial.series.plan.sources[reference.plan_source_index]?.url === row.url
        && editorial.video.sources[reference.public_source_index]?.url === row.url,
      `claim source mismatch: ${row.id}`);
      assert.ok(sceneIds.has(row.scene), `claim scene absent: ${row.id}`);
      return { id: row.id, claim: row.claim, scene: row.scene,
        source: reference.plan_source_index, fact: null, verdict: 'UNCHECKED' };
    });
    for (const scene of scenes) {
      assert.deepEqual(scene.claims ?? [],
        claimData.filter((claim) => claim.scene === scene.id).map((claim) => claim.id),
      `scene claim IDs changed: ${scene.id}`);
    }
    assert.equal(current[key].key, key, `104 chapter key drift: ${key}`);
    chapters[key] = { key, title,
      scenes: scenes.map(({ chapter: _chapter, claims: _claims, ...scene }) => scene),
      claims: claimData,
      ...(r23Loops[key].length ? { loops: r23Loops[key] } : {}),
      ...(key === 'hook' ? { thumbnail_shot: thumbnailShot } : {}),
      report: 'A01 104→105 saved r23 chapter revision. Formal verifier, listener and narrative review required.' };
  }
  assert.equal(Object.values(chapters).flatMap((chapter) => chapter.scenes).length, 65);
  assert.equal(Object.values(chapters).flatMap((chapter) => chapter.claims).length, 74);
  return chapters;
}
function autoTarget(roots) {
  const auto = structuredClone(parse(path.join(roots.work, SLUG, 'auto.json')));
  assert.equal(auto.status, 'blocked');
  assert.equal(auto.blocked_kind, 'prompt_fixes:narrative');
  assert.equal(auto.story?.narrative?.passed, false);
  auto.target_minutes = 8;
  auto.verified = false;
  auto.listener_done = false;
  auto.status = 'blocked';
  auto.blocked_kind = 'pilot_script_review';
  auto.blocked = 'A01 r23 104→105 saved; formal chapter verification, listener, narrative review and owner-scoped script review remain pending.';
  auto.story.narrative = null;
  auto.story.narrative_fixes = 0;
  auto.story.length = null;
  auto.story.audio_review = null;
  auto.story.owner_note = null;
  for (const key of CHAPTERS) {
    const entry = auto.story.chapters[key];
    assert.ok(entry?.written && entry.checked && entry.listened);
    entry.checked = false;
    entry.listened = false;
    entry.check_rounds = 0;
    entry.lint_fixes = 0;
    entry.lint = null;
    delete entry.changed;
  }
  return auto;
}

/**
 * Prepare against a VERIFIED FRESH extracted capture and a worker file whose
 * SHA is read back from the deployed worker. This recomputes archive and full
 * immutable 104-chain evidence. The future host wrapper must independently
 * validate current DB/budget and live host gates before any adoption write.
 */
export async function prepareAdoption({ roots, editorialDir, workerFile, workerRoot,
  captureManifestFile, verifiedCaptureReceiptFile, repoRoot, deployed }) {
  for (const value of [editorialDir, workerFile, workerRoot, captureManifestFile,
    verifiedCaptureReceiptFile, repoRoot])
    assert.ok(path.isAbsolute(value), 'absolute input paths required');
  assert.equal(path.resolve(workerRoot), path.resolve(repoRoot),
    'composeStory root must be the deployed checkout');
  assert.equal(fs.realpathSync(repoRoot), path.resolve(repoRoot),
    'deployed checkout symlink refused');
  assert.ok(deployed && /^[0-9a-f]{40}$/u.test(deployed.release_sha));
  assert.match(deployed.tools_video_tree_sha, /^[0-9a-f]{40}$/u);
  assert.match(deployed.worker_image_id, /^sha256:[0-9a-f]{64}$/u);
  assert.match(deployed.tools_video_runtime_inventory_sha256, /^[0-9a-f]{64}$/u);
  assert.ok(Number.isInteger(deployed.tools_video_runtime_file_count)
    && deployed.tools_video_runtime_file_count > 0,
  'container tools/video file count required');
  assert.equal(path.basename(captureManifestFile), 'capture-report.json',
    'fresh capture manifest path required');
  const independent = parse(verifiedCaptureReceiptFile);
  const recomputed = await verifyFresh104(path.dirname(captureManifestFile));
  assert.deepEqual(independent, recomputed,
    'independent receipt differs from newly verified capture and 104 chain');
  assert.equal(independent.kind, 'a01_fresh_104_capture_independent_verification');
  assert.equal(independent.status, 'PASS');
  assert.equal(independent.verification_scope,
    'ARCHIVE_MEMBERSHIP_AND_IMMUTABLE_104_ONLY');
  assert.equal(independent.production_adoption_allowed, false);
  assert.equal(independent.source_sha256, VERIFIED_104.source_sha256);
  assert.equal(independent.old_index_sha256, VERIFIED_104.tip_index_sha256);
  assert.equal(independent.old_audit_inventory_sha256, VERIFIED_104.audit_inventory_sha256);
  assert.equal(independent.capture_manifest_sha256, sha(exact(captureManifestFile)));
  assert.equal(independent.release_sha, deployed.release_sha,
    'capture worker release differs from pinned deployed checkout');
  assert.equal(path.resolve(workerFile),
    path.join(path.resolve(repoRoot), 'tools', 'video', 'automation', 'story.mjs'));
  assert.equal(execFileSync('git', ['rev-parse', 'HEAD'], { cwd: repoRoot, encoding: 'utf8' }).trim(),
    deployed.release_sha, 'local worker checkout is not the deployed release');
  assert.equal(execFileSync('git', ['rev-parse', 'HEAD:tools/video'],
    { cwd: repoRoot, encoding: 'utf8' }).trim(),
  deployed.tools_video_tree_sha, 'deployed tools/video tree pin missing or changed');
  assert.equal(execFileSync('git', ['status', '--porcelain', '--', 'tools/video'],
    { cwd: repoRoot, encoding: 'utf8' }).trim(), '',
  'local worker dependencies modified');
  const runtimeInventory = auditInventory(path.join(repoRoot, 'tools', 'video'));
  assert.equal(runtimeInventory.count, deployed.tools_video_runtime_file_count,
    'container tools/video file count differs from release checkout');
  assert.equal(runtimeInventory.sha256, deployed.tools_video_runtime_inventory_sha256,
    'container tools/video bytes differ from release checkout');
  assert.equal(deployed.worker_story_sha256, sha(exact(workerFile)),
    'worker does not match captured deployed runtime');
  assert.equal(deployed.public_filter_sha256, deployed.worker_story_sha256,
    'public filter must be in the pinned story worker');
  const captured = verifySource104(roots);
  assert.equal(captured.source, independent.source_sha256, 'fresh capture changed after review');
  assert.equal(captured.oldIndexSha, independent.old_index_sha256,
    'fresh 104 tip changed after review');
  assert.equal(captured.oldAudit.sha256, independent.old_audit_inventory_sha256,
    'fresh audit inventory changed after review');
  const stop = exact(path.join(roots.work, SLUG, 'STOP'));
  assert.ok(stop.length > 0, 'scoped STOP required');
  const editorial = checkEditorial(editorialDir);
  assert.notEqual(editorial.manifestSha, REJECTED_R23_MANIFEST_SHA256,
    'R23_EDITORIAL_REJECTED_AWAIT_R24');
  assert.equal(editorial.alignment.live_snapshot104_series_sha256_reported_not_recomputed_by_this_check,
    captured.before.series, 'editorial 104 plan baseline changed');
  const chapters = chapterTarget(roots, editorial);
  const { composeStory } = await import(pathToFileURL(workerFile).href);
  assert.equal(typeof composeStory, 'function', 'deployed story worker does not compose');
  const video = composeStory({ slug: SLUG, info: editorial.series, chapters,
    voice: editorial.video.voice, root: workerRoot,
    videoId: editorial.video.youtube?.video_id ?? null });
  assert.deepEqual(video.target_minutes, [7, 8], 'owner duration rule not deployed');
  assert.equal(video.scenes.length, 65);
  assert.deepEqual(video.sources.map((source) => source.url),
    editorial.video.sources.map((source) => source.url),
  'deployed 18-source public filter missing or changed');
  assert.deepEqual(video.scenes, editorial.video.scenes,
    'compiled scenes differ from reviewed r23 candidate');
  const loopsBySetup = (loops) => [...loops].sort((left, right) =>
    left.setup < right.setup ? -1 : left.setup > right.setup ? 1 : 0);
  assert.deepEqual(loopsBySetup(video.loops), loopsBySetup(editorial.video.loops),
    'compiled hooks differ from reviewed r23 candidate');
  for (const field of ['voice', 'look', 'characters', 'series', 'music', 'subtitles',
    'youtube', 'thumbnail', 'sources', 'assets'])
    assert.deepEqual(video[field], editorial.video[field],
      `compiled ${field} differs from reviewed r23 candidate`);
  assert.deepEqual(video, editorial.video,
    'full compiled video differs from reviewed r23 candidate');
  for (let i = 0; i < 65; i++) {
    assert.equal(video.scenes[i].id, editorial.video.scenes[i].id);
    assert.deepEqual(video.scenes[i].lines, editorial.video.scenes[i].lines);
    assert.deepEqual(video.scenes[i].data, editorial.video.scenes[i].data);
  }
  const targets = new Map([
    ...CHAPTERS.map((key) => [`${SLUG}/story/chapters/${key}.json`, json(chapters[key])]),
    [`docs/videos/${SLUG}/series.json`, json(editorial.series)],
    [`docs/videos/${SLUG}/video.json`, json(video)],
    [`${SLUG}/auto.json`, json(autoTarget(roots))],
  ]);
  assert.deepEqual([...targets.keys()], changedPaths(), 'nine target path order changed');
  const targetHashes = Object.fromEntries([...targets].map(([name, bytes]) => [name, sha(bytes)]));
  const beforeHashes = Object.fromEntries(changedPaths().map((logical) => {
    const key = path.basename(logical, '.json');
    const digest = key === 'auto' ? captured.before.auto
      : key === 'video' ? captured.before.video
        : key === 'series' ? captured.before.series : captured.before.chapters[key];
    return [logical, digest];
  }));
  const eventId = `r23-existing-revision-${editorial.manifestSha.slice(0, 16)}`;
  const draft = { schema_version: 1, kind: 'a01_r23_105_install_plan', slug: SLUG,
    event_id: eventId, before_source_sha256: captured.source,
    old_event_id: captured.oldEventId, old_index_sha256: captured.oldIndexSha,
    old_audit_file_count: captured.oldAudit.count,
    old_audit_inventory_sha256: captured.oldAudit.sha256,
    before_files_sha256: beforeHashes, changed_files_sha256: targetHashes,
    editorial_manifest_sha256: editorial.manifestSha,
    capture_manifest_sha256: sha(exact(captureManifestFile)),
    independent_capture_receipt_sha256: sha(exact(verifiedCaptureReceiptFile)),
    tools_video_tree_sha: deployed.tools_video_tree_sha,
    tools_video_runtime_inventory_sha256: deployed.tools_video_runtime_inventory_sha256,
    tools_video_runtime_file_count: deployed.tools_video_runtime_file_count,
    worker_image_id: deployed.worker_image_id,
    release_sha: deployed.release_sha, worker_story_sha256: deployed.worker_story_sha256,
    public_filter_sha256: deployed.public_filter_sha256,
    a01_stop_sha256: sha(stop),
    public_source_urls: editorial.video.sources.map((source) => source.url),
    target_bytes: Object.fromEntries([...targets].map(([name, bytes]) =>
      [name, bytes.toString('base64')])),
  };
  draft.after_source_sha256 = sourceHash(afterTuple(captured.before, draft));
  return draft;
}

export function saveNewPlan(file, plan) {
  assert.ok(path.isAbsolute(file), 'absolute new plan file required');
  const fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, json(plan)); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  return sha(exact(file));
}
