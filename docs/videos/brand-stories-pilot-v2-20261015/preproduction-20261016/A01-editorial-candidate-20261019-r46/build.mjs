import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

// New successor only. Read the frozen r45 bytes without running its historical builder.
const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const source = path.join(here, '../A01-editorial-candidate-20261019-r45');
const read = (name) => fs.readFileSync(path.join(source, name));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const sourceManifestSha = '896615541683e620eb6e79468d8d304f146ad932700a7f044d5a1eb9784888f6';
assert.equal(sha(read('manifest.json')), sourceManifestSha, 'frozen portable r45 manifest drift');
const sourceManifest = JSON.parse(read('manifest.json'));
for (const [name, hash] of Object.entries(sourceManifest.outputs_sha256)) assert.equal(sha(read(name)), hash, name);
const sourceVideo = JSON.parse(read('candidate/video.json'));
const video = structuredClone(sourceVideo);
const series = JSON.parse(read('candidate/series.json'));
const lexicon = JSON.parse(read('candidate/lexicon.json'));
const authoredBytes = fs.readFileSync(path.join(here, 'narration-delta.json'));
const authored = JSON.parse(authoredBytes);
assert.equal(authored.changes.length, 5);
assert.deepEqual(authored.changes.map((row) => row.scene), ['origin-return', 'engine-crew', 'engine-public-sight', 'turn-wait', 'now-space']);
for (const change of authored.changes) {
  const scene = video.scenes.find((row) => row.id === change.scene);
  assert.equal(scene.lines.length, 1);
  assert.equal(scene.lines[0].id, change.line);
  assert.equal(scene.lines[0].text, change.before);
  assert.ok(change.after && change.after !== change.before);
  scene.lines[0].text = change.after;
}
const retainedSetups = new Set(['r44l003', 'r44l004', 'r44l005', 'r44l001', 'r44l020']);
const retainedLoops = sourceVideo.loops.filter((loop) => retainedSetups.has(loop.setup));
assert.equal(retainedLoops.length, 5);
const addedLoops = [
  { setup: 'r44l023', payoff: 'r44l024', what: '機組員開始使用後，車庫是否容得下生意；需求使製作搬入倉庫' },
  { setup: 'r44l028', payoff: 'r44l029', what: '旅客如何買到早期輪子登機箱；1993 報導回顧 Travelpro 郵購販售' },
  { setup: 'r44l047', payoff: 'r44l049', what: '收納失敗後 Dash 是否還喜歡這只箱；Travelpro 仍是偏愛款式之一' },
];
video.loops = [...retainedLoops, ...addedLoops];
assert.equal(video.loops.length, 8);
// All factual rows and their scene membership stay unchanged. New questions add no answer claims.
const restored = structuredClone(video);
for (const change of authored.changes) restored.scenes.find((row) => row.id === change.scene).lines[0].text = change.before;
restored.loops = sourceVideo.loops;
assert.deepEqual(restored, sourceVideo, 'change outside five narration lines and loop metadata');
series.series.note = 'A01 r46：沿用站主選定的 r44 Rollaboard 主線、標題、縮圖及 7–8 分鐘例外；只改五行旁白與鉤子回收表，配合 45 秒節奏。新稿待獨立審查，未取得新的正式審稿、匯入、配音、合併、部署或上架核准。';
const brief = read('brief.md').toString('utf8').replace(
  'r45 是兩處問句標點與一句片尾來源提示的窄修，正式章稿與媒體驗收仍待完成。',
  'r46 只改五行旁白與鉤子回收表，補足新版 45 秒節奏；本版待獨立審查，正式章稿與媒體驗收仍待完成。',
);
assert.ok(brief.includes('r46 只改五行'));
const imports = (name) => import(pathToFileURL(path.join(repo, name)));
const [{ screenplay }, { estimateTimeline }, { lintVideo }, { cuteStoryVisualProblems }, { validateVideo }, { hookCadenceProblems, TIGHT_CADENCE }] = await Promise.all([
  imports('tools/video/core/screenplay.mjs'), imports('tools/video/core/timeline.mjs'), imports('tools/video/core/lint.mjs'),
  imports('tools/video/automation/story.mjs'), imports('tools/video/core/schema.mjs'), imports('tools/video/core/narrative.mjs'),
]);
assert.deepEqual(TIGHT_CADENCE, { gap: 45, loopsPer10: 8 }, 'cadence policy drift');
assert.deepEqual(validateVideo(video), []);
assert.deepEqual(cuteStoryVisualProblems(video), []);
const context = { lexicon, brief, translations: {}, others: [], series };
const estimates = {};
const currentChecks = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const lint = lintVideo(video, { ...context, cpm });
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
assert.ok(estimates[275].body_seconds >= 420 && estimates[275].body_seconds <= 480);
const oldCadence = hookCadenceProblems(sourceVideo, estimateTimeline(sourceVideo, 250), TIGHT_CADENCE.gap);
assert.equal(oldCadence.length, 5, 'source tight-cadence baseline drift');
const removedLoops = sourceVideo.loops.filter((loop) => !retainedSetups.has(loop.setup));
const validation = {
  status: 'R46_CADENCE_ADAPTATION_PENDING_INDEPENDENT_REVIEW', scenes: video.scenes.length,
  lines: video.scenes.flatMap((row) => row.lines).length, claims: 55, loops: video.loops.length,
  all_claims_pending: true, target_body_seconds: [420, 480], estimates_not_real_tts: estimates,
  cadence: TIGHT_CADENCE, source_r45_cadence_problems_at_250: oldCadence, checks_by_cpm: currentChecks,
  schema_errors: [], cute_visual_errors: [], factual_claims_sources_prompts_unchanged: true,
  estimated_band_at_275_passed: true, actual_tts_duration_not_measured: true,
  independent_r46_reviews: 'NOT_YET_ISSUED_AT_BUILD', formal_chapter_reviews: 'NOT_YET_ISSUED',
  host_adoption_allowed: false, paid_media_started: false,
};
const delta = {
  source_manifest_sha256: sourceManifestSha, changes: authored.changes,
  loops: { retained: retainedLoops, removed: removedLoops, added: addedLoops },
  loop_note: 'The prototype-to-commercial-case comparison is not a same-object payoff. The market transition and duplicated cabin question remain spoken but are not counted again as separate promises. Security and curb questions reinforce the existing opening promises.',
  factual_claim_rows_and_scene_claim_ids_unchanged: true, picture_prompts_unchanged: true,
  all_public_urls_and_lexicon_unchanged: true, title_thumbnail_direction_unchanged: true,
  metadata_changes: ['series.series.note records r46 status', 'brief status line records r46 scope'],
  source_maps_retained_as_historical_r44_provenance: true, original_reviews_not_reissued: true,
};
const diffReport = '# A01 r45 → r46 narration and loop delta\n\nAuthor report; independent review pending. No old receipt is inherited as r46 approval.\n\n' +
  authored.changes.map((row) => `## ${row.scene} / ${row.line}\n\nBefore: ${row.before}\n\nAfter: ${row.after}\n\nReason: ${row.reason}\n\nExisting evidence: ${row.evidence_claims.join(', ')}. Payoff: ${row.payoff_lines.join(', ')}. ${row.limit}\n`).join('\n') +
  '\n## Loop bookkeeping\n\nRetain the four opening promises and idea-next → engine-crew. Replace the prototype/commercial comparison, market transition, and repeated cabin prompt entries with the garage-capacity, mail-order-channel and final-verdict micro-stories. Their exact IDs are in delta.json. There are eight tracked loops; the added security/curb questions strengthen existing opening promises rather than inflate this count. No screw-on prototype is identified as the 1993 commercial case.\n\n' +
  `## Mechanical estimate\n\nBody at 250/275/300 CPM: ${[250, 275, 300].map((cpm) => estimates[cpm].body_seconds).join(' / ')} seconds. All three speeds have zero 45-second cadence gaps and zero lint errors. Actual TTS is not measured; the 300 CPM estimate is below seven minutes. The A01 exception remains 420–480 seconds of real body audio.\n`;
const outputs = new Map([
  ['candidate/video.json', json(video)], ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', read('candidate/lexicon.json')], ['candidate/script.md', Buffer.from(screenplay(video))],
  ['candidate/claims.md', read('candidate/claims.md')], ['brief.md', Buffer.from(brief)],
  ['source-alignment.json', read('source-alignment.json')], ['source-map.json', read('source-map.json')],
  ['delta.json', json(delta)], ['diff-report.md', Buffer.from(diffReport)], ['validation.json', json(validation)],
]);
const dependencies = ['tools/video/core/screenplay.mjs', 'tools/video/core/timeline.mjs', 'tools/video/core/schema.mjs',
  'tools/video/core/lint.mjs', 'tools/video/core/duration.mjs', 'tools/video/core/narrative.mjs', 'tools/video/automation/story.mjs'];
const manifest = {
  schema_version: 1, status: validation.status, slug: video.slug, source_manifest_sha256: sourceManifestSha,
  source_outputs_sha256: sourceManifest.outputs_sha256,
  owner_direction_inherited_as_story_direction_only: true, r46_editorial_review_required: true,
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))), authored_narration_delta_sha256: sha(authoredBytes),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  dependency_sha256: Object.fromEntries(dependencies.map((name) => [name, sha(fs.readFileSync(path.join(repo, name)))])),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  authorizes_host_install_or_paid_media: false,
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
console.log(JSON.stringify({ action, manifest_sha256: sha(json(manifest)), scenes: validation.scenes,
  lines: validation.lines, loops: video.loops.length, body_seconds_275: estimates[275].body_seconds,
  lint_errors: currentChecks[250].lint_errors.length, lint_warnings: currentChecks[250].lint_warnings.length,
  tight_cadence_gaps_at_250_275_300: [0, 0, 0] }));
