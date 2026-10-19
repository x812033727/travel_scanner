import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r44 = path.join(here, '../A01-editorial-candidate-20261019-r44');
const read = (name) => fs.readFileSync(path.join(r44, name));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const sourceManifestSha = 'a2a82be58698b6062e343a55e375c5bccd88ccd4d2ee596fc6ded400bc9db234';
assert.equal(sha(read('manifest.json')), sourceManifestSha);
const original = JSON.parse(read('manifest.json'));
for (const [name, hash] of Object.entries(original.outputs_sha256)) assert.equal(sha(read(name)), hash, name);
const reviews = {
  'independent-blind-story-review.md': '2c408d3b77e426578294374236c91d80c5ea59b6bbfc6e550d80c6834ff64343',
  'independent-source-review.md': 'cdb5687bc114717d6399e60d813ba888aa87c3dd6ad9e69ad680fb19cf16a147',
  'independent-visual-fact-audit.md': '167d8ce246d734b33424bb8901388fbed3be75cf462027fec7b33fe4d6396b16',
};
for (const [name, hash] of Object.entries(reviews)) assert.equal(sha(read(name)), hash, name);
// The owner approved the original r44 identity. Preserve that receipt verbatim;
// portable repackaging is equivalent only when every generated output is unchanged.
const ownerApprovedManifestSha = '62cec617460b882309a48ca76c69615ec20789502538149cc94e47a632144190';
const historicalManifestBytes = fs.readFileSync(path.join(here,
  '../portability-20261019/historical-manifests/A01-editorial-candidate-20261019-r44.json'));
assert.equal(sha(historicalManifestBytes), ownerApprovedManifestSha, 'historical approved manifest drift');
const historicalManifest = JSON.parse(historicalManifestBytes);
assert.deepEqual(original.outputs_sha256, historicalManifest.outputs_sha256, 'portable r44 content changed');
const direction = JSON.parse(read('owner-direction-20261019.json'));
assert.equal(direction.candidate_manifest_sha256, ownerApprovedManifestSha);
assert.equal(direction.editorial_direction, 'APPROVED');
assert.equal(direction.owner_reply, '採用 r44 Rollaboard 單線故事（建議）');

const video = JSON.parse(read('candidate/video.json'));
const series = JSON.parse(read('candidate/series.json'));
const lexicon = JSON.parse(read('candidate/lexicon.json'));
const changes = [];
for (const [id, expected] of [
  ['engine-patent-stow', '同一份專利把輪子嵌進箱角，只露出一小截。它設計時還在想：怎麼過機艙窄走道、收進座位下。'],
  ['turn-fabric', '旅途碰撞和推擠沒傷到尼龍箱；另一個問題是，它能裝多少。'],
]) {
  const scene = video.scenes.find((row) => row.id === id);
  assert.equal(scene.lines.length, 1);
  assert.equal(scene.lines[0].text, expected);
  scene.lines[0].text = expected.slice(0, -1) + '？';
  changes.push({ scene: id, line: scene.lines[0].id, before: expected, after: scene.lines[0].text, kind: 'question_punctuation_only' });
}
const outro = video.scenes.find((row) => row.id === 'now-outro');
assert.equal(outro.lines.length, 2);
const sourceLine = { id: 'r45out3', text: '資料來源放在說明欄，想追細節可以接著看。' };
outro.lines.splice(1, 0, sourceLine);
changes.push({ scene: 'now-outro', line: sourceLine.id, before: null, after: sourceLine.text, kind: 'source_link_closing_line' });
// A patent's design goal is not a demonstrated result for the later commercial unit.
// Do not add a misleading patent-to-test payoff to the already reviewed loop table.
assert.deepEqual(video.loops, JSON.parse(read('candidate/video.json')).loops);
assert.deepEqual(video.scenes.map((row) => row.data), JSON.parse(read('candidate/video.json')).scenes.map((row) => row.data));
series.series.note = 'A01 r45：站主於 2026-10-19 選定 r44 Rollaboard 主線、標題與縮圖；本版僅兩處問句標點與一句片尾來源提示。方向已定，正式章稿與媒體關卡仍待完成；不含新合併、部署、匯入或上架授權。';
const brief = read('brief.md').toString('utf8').replace(
  '狀態：ALTERNATE_PROPOSAL／HOLD。這不是已核准的 A01 Macy\'s／Sadow 企劃，標題、縮圖與主線都待站主另審。',
  '狀態：EDITORIAL_DIRECTION_APPROVED／PRODUCTION_HOLD。站主已選定 r44 Rollaboard 主線、標題與縮圖；r45 是兩處問句標點與一句片尾來源提示的窄修，正式章稿與媒體驗收仍待完成。',
);
assert.ok(brief.includes('EDITORIAL_DIRECTION_APPROVED'));
const [{ screenplay }, { estimateTimeline }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  'tools/video/core/screenplay.mjs', 'tools/video/core/timeline.mjs',
  'tools/video/core/lint.mjs', 'tools/video/automation/story.mjs',
].map((name) => import(pathToFileURL(path.join(repo, name)))));
const context = { lexicon, brief, translations: {}, others: [], series };
const lint = lintVideo(video, context);
const fastLint = lintVideo(video, { ...context, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.deepEqual(lint.errors, []);
assert.deepEqual(fastLint.errors, []);
assert.deepEqual(cute, []);
const remainingNarrativeWarnings = lint.warnings.filter((row) => /no open loop between|outro.*(?:three|3).*sentence|(?:three|3).*outro/i.test(row.message));
assert.deepEqual(remainingNarrativeWarnings, []);
const estimates = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  estimates[cpm] = {
    body_seconds: Number((timeline.scenes.find((row) => row.id === 'now-outro').start_frame / 30).toFixed(1)),
    timeline_seconds_before_final_branding: Number((timeline.total_frames / 30).toFixed(1)),
  };
}
const validation = {
  status: 'EDITORIAL_DIRECTION_APPROVED_PRODUCTION_HOLD',
  scenes: video.scenes.length, lines: video.scenes.flatMap((row) => row.lines).length,
  claims: 55, all_claims_pending: true, target_body_seconds: [420, 480],
  estimates_not_real_tts: estimates, lint_errors: lint.errors, lint_warnings: lint.warnings,
  fast_300_cpm_errors: fastLint.errors, cute_visual_errors: cute,
  prior_three_main_warnings_resolved: true,
  independent_r45_delta_review: 'NOT_YET_ISSUED_AT_BUILD',
  formal_chapter_reviews: 'NOT_YET_ISSUED', host_adoption_allowed: false, paid_media_started: false,
};
const outputs = new Map([
  ['candidate/video.json', json(video)], ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', read('candidate/lexicon.json')], ['candidate/script.md', Buffer.from(screenplay(video))],
  ['candidate/claims.md', read('candidate/claims.md')], ['brief.md', Buffer.from(brief)],
  ['source-alignment.json', read('source-alignment.json')], ['source-map.json', read('source-map.json')],
  ['delta.json', json({ source_manifest_sha256: sourceManifestSha, changes, factual_claims_and_picture_prompts_unchanged: true,
    source_maps_retained_as_r44_provenance: true, original_reviews_not_reissued: true })],
  ['validation.json', json(validation)],
]);
const dependencies = ['tools/video/core/screenplay.mjs', 'tools/video/core/timeline.mjs',
  'tools/video/core/lint.mjs', 'tools/video/core/duration.mjs', 'tools/video/core/narrative.mjs', 'tools/video/automation/story.mjs'];
const manifest = {
  schema_version: 1, status: validation.status, slug: video.slug,
  source_manifest_sha256: sourceManifestSha, source_review_hashes: reviews,
  owner_approved_manifest_sha256: ownerApprovedManifestSha,
  owner_direction_sha256: sha(read('owner-direction-20261019.json')),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
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
  lines: validation.lines, body_seconds_275: estimates[275].body_seconds, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, prior_three_main_warnings_resolved: true }));
