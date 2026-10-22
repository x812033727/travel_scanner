import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const source = path.join(here, '../A01-editorial-candidate-20261019-r46');
const read = (name) => fs.readFileSync(path.join(source, name));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const sourceManifestSha = 'd6b9e59358d7616a97c333368b6533f5f45745f5625887276e91a2095df6d794';
assert.equal(sha(read('manifest.json')), sourceManifestSha, 'frozen r46 manifest drift');
const sourceManifest = JSON.parse(read('manifest.json'));
for (const [name, hash] of Object.entries(sourceManifest.outputs_sha256)) assert.equal(sha(read(name)), hash, name);
const sourceVideo = JSON.parse(read('candidate/video.json'));
const video = structuredClone(sourceVideo);
const series = JSON.parse(read('candidate/series.json'));
const lexicon = JSON.parse(read('candidate/lexicon.json'));
const authoredBytes = fs.readFileSync(path.join(here, 'narration-delta.json'));
const authored = JSON.parse(authoredBytes);
assert.equal(authored.changes.length, 6);
assert.deepEqual(authored.changes.map((row) => row.line), ['r44l001', 'r44l041', 'r44l042', 'r44l044', 'r44l045', 'r44l047']);
for (const change of authored.changes) {
  const scene = video.scenes.find((row) => row.id === change.scene);
  assert.equal(scene.lines.length, 1);
  assert.equal(scene.lines[0].id, change.line);
  assert.equal(scene.lines[0].text, change.before);
  assert.ok(change.after && change.after !== change.before);
  scene.lines[0].text = change.after;
}
const oldChapter = video.scenes.find((row) => row.id === 'now-zipper').chapter;
assert.equal(oldChapter, '最後卻放不進機艙');
assert.equal(video.scenes.find((row) => row.id === 'now-aisle').chapter, undefined);
delete video.scenes.find((row) => row.id === 'now-zipper').chapter;
video.scenes.find((row) => row.id === 'now-aisle').chapter = oldChapter;
const removedIndex = video.scenes.findIndex((row) => row.id === 'now-answer');
const [removedScene] = video.scenes.splice(removedIndex, 1);
assert.deepEqual(removedScene.claims, ['q055']);
assert.equal(removedScene.lines[0].id, 'r44l050');
assert.equal(removedScene.lines.length, 1);
const openingLoop = video.loops.find((row) => row.setup === 'r44l001');
assert.equal(openingLoop.payoff, 'r44l048');
openingLoop.what = '記者的箱子為何放不下；外袋加物使外形變大，取物後才收好';
const restored = structuredClone(video);
for (const change of authored.changes) restored.scenes.find((row) => row.id === change.scene).lines[0].text = change.before;
delete restored.scenes.find((row) => row.id === 'now-aisle').chapter;
restored.scenes.find((row) => row.id === 'now-zipper').chapter = oldChapter;
restored.scenes.splice(removedIndex, 0, removedScene);
restored.loops = sourceVideo.loops;
assert.deepEqual(restored, sourceVideo, 'change outside declared narration, chapter marker, removed scene and loop wording');
assert.deepEqual(video.scenes.find((row) => row.id === 'now-outro'), sourceVideo.scenes.find((row) => row.id === 'now-outro'));
assert.equal(video.scenes.length, 50);
assert.equal(video.scenes.flatMap((row) => row.lines).length, 52);
assert.equal(video.loops.length, 8);
const oldClaims = read('candidate/claims.md').toString('utf8');
const removedClaimLines = oldClaims.split('\n').filter((row) => row.startsWith('q055｜'));
assert.equal(removedClaimLines.length, 1);
const claims = oldClaims.split('\n').filter((row) => !row.startsWith('q055｜')).join('\n');
const claimRows = claims.split(/\r?\n/).filter((row) => /^q\d+｜/.test(row));
assert.equal(claimRows.length, 54);
assert.ok(claimRows.every((row) => row.endsWith('｜PENDING')));
const activeIds = new Set(video.scenes.flatMap((row) => row.claims ?? []));
assert.deepEqual(activeIds, new Set(claimRows.map((row) => row.split('｜')[0])));
const alignment = JSON.parse(read('source-alignment.json'));
alignment.status = 'R47_PENDING_EXACT_SOURCE_ALIGNMENT';
alignment.derives_from_r46_sha256 = sha(read('source-alignment.json'));
alignment.counts.scenes = 50;
alignment.counts.lines = 52;
alignment.counts.claims = 54;
alignment.claim_source_rows = alignment.claim_source_rows.filter((row) => row.id !== 'q055');
assert.equal(alignment.claim_source_rows.length, 54);
for (const row of alignment.claim_source_rows) {
  assert.ok(activeIds.has(row.id));
  assert.equal(row.public_source_index, row.plan_source_index);
  assert.equal(row.plan_source_index, row.research_source_index);
  assert.equal(video.sources[row.public_source_index].url, row.url);
}
const historicalMap = JSON.parse(read('source-map.json'));
const sourceMap = {
  schema_version: 1, status: 'R47_PENDING_SOURCE_MAP',
  historical_r46_source_map_sha256: sha(read('source-map.json')),
  source_snapshot104: historicalMap.source_snapshot104,
  active_claims: 54, all_claims_pending: true,
  source_index: historicalMap.source_index.map((row) => ({ ...row, claim_ids: row.claim_ids.filter((id) => activeIds.has(id)) })),
  prototype_product_caveat: historicalMap.prototype_product_caveat,
  exact_year_caveat: historicalMap.exact_year_caveat,
  removed_duplicate_claim: { id: 'q055', scene: 'now-answer', preserved_support: ['q042', 'q050', 'q051', 'q052', 'q053'] },
  host_adoption_allowed: false, paid_media_allowed: false,
};
series.series.note = 'A01 r47：沿用站主選定的 Rollaboard 主線與 7–8 分鐘例外；修正開場劇透、末章銜接和重述。新稿待獨立審查，275 CPM 紙面正文低於 420 秒，實際 TTS 420–480 秒門檻未豁免；未取得正式章稿、匯入、付費或媒體核准。';
const brief = read('brief.md').toString('utf8').replace(
  'r46 只改五行旁白與鉤子回收表，補足新版 45 秒節奏；本版待獨立審查，正式章稿與媒體驗收仍待完成。',
  'r47 修正開場劇透、末章銜接和重述，保留新版 45 秒節奏；本版待獨立審查，275 CPM 紙面正文低於 420 秒，實際音訊 420–480 秒門檻未豁免。',
);
assert.ok(brief.includes('r47 修正開場'));
const imports = (name) => import(pathToFileURL(path.join(repo, name)));
const [{ screenplay }, { estimateTimeline }, { lintVideo }, { cuteStoryVisualProblems }, { validateVideo }, { hookCadenceProblems, TIGHT_CADENCE }] = await Promise.all([
  imports('tools/video/core/screenplay.mjs'), imports('tools/video/core/timeline.mjs'), imports('tools/video/core/lint.mjs'),
  imports('tools/video/automation/story.mjs'), imports('tools/video/core/schema.mjs'), imports('tools/video/core/narrative.mjs'),
]);
assert.deepEqual(TIGHT_CADENCE, { gap: 45, loopsPer10: 8 });
assert.deepEqual(validateVideo(video), []);
assert.deepEqual(cuteStoryVisualProblems(video), []);
const estimates = {}, currentChecks = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const lint = lintVideo(video, { lexicon, brief, translations: {}, others: [], series, cpm });
  const cadence = hookCadenceProblems(video, timeline, TIGHT_CADENCE.gap);
  assert.deepEqual(lint.errors, [], `lint errors at ${cpm}`);
  assert.deepEqual(cadence, [], `cadence gaps at ${cpm}`);
  assert.ok(!lint.warnings.some((row) => /no open loop between|outro.*(?:three|3).*sentence|(?:three|3).*outro/i.test(row.message)));
  estimates[cpm] = {
    body_seconds: Number((timeline.scenes.find((row) => row.id === 'now-outro').start_frame / 30).toFixed(1)),
    timeline_seconds_before_final_branding: Number((timeline.total_frames / 30).toFixed(1)),
  };
  currentChecks[cpm] = { lint_errors: lint.errors, lint_warnings: lint.warnings, cadence_problems: cadence };
}
const estimatedBand = estimates[275].body_seconds >= 420 && estimates[275].body_seconds <= 480;
const validation = {
  status: 'R47_NARRATIVE_REVIEW_AND_ACTUAL_DURATION_HOLD', scenes: 50, lines: 52, claims: 54, loops: 8,
  all_claims_pending: true, target_actual_body_seconds: [420, 480], estimates_not_real_tts: estimates,
  cadence: TIGHT_CADENCE, checks_by_cpm: currentChecks, schema_errors: [], cute_visual_errors: [],
  retained_claims_sources_prompts_unchanged: true, estimated_band_at_275_passed: estimatedBand,
  actual_tts_duration_not_measured: true, duration_gate_passed: false,
  duration_hold_reason: 'The 275 CPM paper estimate is below 420 seconds. The actual 420–480-second requirement remains unchanged; no filler, slowed delivery or pauses were added.',
  independent_r47_reviews: 'NOT_YET_ISSUED_AT_BUILD', formal_chapter_reviews: 'NOT_YET_ISSUED',
  host_adoption_allowed: false, paid_media_started: false,
};
const delta = {
  source_manifest_sha256: sourceManifestSha, changes: authored.changes,
  chapter_marker: { from: 'now-zipper', to: 'now-aisle', title: oldChapter, chronological_scene_order_unchanged: true, q047_moves_from: 'now', q047_moves_to: 'turn' },
  removed_scene: removedScene, removed_claim_row: removedClaimLines[0], removed_claim_reason: 'Duplicate summary, already supported by retained q042 and q050–q053.',
  loops: { pairs_unchanged: true, previous_opening: sourceVideo.loops.find((row) => row.setup === 'r44l001'), current_opening: openingLoop },
  retained_claim_rows_and_scene_membership_unchanged: true, retained_picture_prompts_unchanged: true,
  public_urls_lexicon_title_thumbnail_unchanged: true, outro_three_original_sentences_unchanged: true,
  metadata_changes: ['series.series.note and brief record r47 status', 'source-alignment and source-map reflect 54 claims / 50 scenes / 52 lines'],
  original_reviews_not_reissued: true,
};
const diffReport = '# A01 r46 → r47 narrative delta\n\nAuthor report. Both r46 reader reports remain failed historical evidence; new r47 review is pending.\n\n' +
  authored.changes.map((row) => `## ${row.scene} / ${row.line}\n\nBefore: ${row.before}\n\nAfter: ${row.after}\n\nReason: ${row.reason}\n\nExisting evidence: ${row.evidence_claims.join(', ')}. ${row.limit}\n`).join('\n') +
  '\n## Structural changes\n\nMove only the final chapter marker from now-zipper to now-aisle. The zipper fact is answered in the packing/testing chapter, with no change to historical scene order. q047 therefore moves from now to turn in the canonical handoff. Delete now-answer/r44l050/q055 because it only repeated ground-versus-storage results. Preserve all three original outro sentences. The retained 50 prompts and 54 claim statements/source URLs are unchanged. All eight loop pairs remain; only the opening loop explanation changes.\n\n' +
  `## Duration HOLD\n\nBody at 250/275/300 CPM: ${[250, 275, 300].map((cpm) => estimates[cpm].body_seconds).join(' / ')} seconds. All three speeds have zero 45-second cadence gaps and zero lint errors. The 275 CPM estimate is below 420 seconds. Actual TTS remains unmeasured; the real 420–480-second body requirement is unchanged. No padding or speed adjustment was added.\n`;
const outputs = new Map([
  ['candidate/video.json', json(video)], ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', read('candidate/lexicon.json')], ['candidate/script.md', Buffer.from(screenplay(video))],
  ['candidate/claims.md', Buffer.from(claims)], ['brief.md', Buffer.from(brief)],
  ['source-alignment.json', json(alignment)], ['source-map.json', json(sourceMap)],
  ['delta.json', json(delta)], ['diff-report.md', Buffer.from(diffReport)], ['validation.json', json(validation)],
]);
const dependencies = ['tools/video/core/screenplay.mjs', 'tools/video/core/timeline.mjs', 'tools/video/core/schema.mjs',
  'tools/video/core/lint.mjs', 'tools/video/core/duration.mjs', 'tools/video/core/narrative.mjs', 'tools/video/automation/story.mjs'];
const manifest = {
  schema_version: 1, status: validation.status, slug: video.slug, source_manifest_sha256: sourceManifestSha,
  source_outputs_sha256: sourceManifest.outputs_sha256, owner_direction_inherited_as_story_direction_only: true,
  r47_editorial_review_required: true, duration_gate_passed: false,
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))), authored_narration_delta_sha256: sha(authoredBytes),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  dependency_sha256: Object.fromEntries(dependencies.map((name) => [name, sha(fs.readFileSync(path.join(repo, name)))])),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])), authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--write', '--check'].includes(action), 'use --write (create only) or --check');
for (const [name, bytes] of outputs) {
  const dest = path.join(here, name);
  if (action === '--write') {
    assert.ok(!fs.existsSync(dest), 'output exists: ' + name);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, bytes, { flag: 'wx' });
  } else assert.ok(fs.readFileSync(dest).equals(bytes), 'output drift: ' + name);
}
console.log(JSON.stringify({ action, manifest_sha256: sha(json(manifest)), scenes: 50, lines: 52, claims: 54, loops: 8,
  estimates, duration_gate_passed: false, lint_errors: currentChecks[250].lint_errors.length,
  lint_warnings: currentChecks[250].lint_warnings.length, tight_cadence_gaps_at_250_275_300: [0, 0, 0] }));
