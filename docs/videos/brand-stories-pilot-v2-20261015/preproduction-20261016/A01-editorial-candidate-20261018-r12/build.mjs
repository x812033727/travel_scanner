// A01-only offline r12 correction over frozen r11; no host or paid-media actions.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r11 = path.resolve(here, '../A01-editorial-candidate-20261018-r11');
const expected = {
  r11_manifest: '39bcc9e69c4d89eea044e145abb592c587183796e92bb13646c83f82511d289a',
  r11_review: '2ed2f086af582ea75dde7abfdf43fb032d3fa7da2feb3917b249c7c890d774ac',
  r11_addendum: 'ed0c8932dbe71440cce9e7a3e6d55ec791ef2785010b53f282357c52ceddf1d7',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR11 = (name) => fs.readFileSync(path.join(r11, name));
assert.equal(sha(readR11('manifest.json')), expected.r11_manifest, 'r11 manifest drift');
assert.equal(sha(readR11('independent-full-review-20261018.md')), expected.r11_review, 'r11 review drift');
assert.equal(sha(readR11('independent-full-review-addendum-20261018.md')), expected.r11_addendum, 'r11 P1 addendum drift');
const r11Manifest = JSON.parse(readR11('manifest.json'));
for (const [name, digest] of Object.entries(r11Manifest.outputs_sha256)) {
  assert.equal(sha(readR11(name)), digest, 'r11 output drift ' + name);
}
assert.equal(sha(readR11('build.mjs')), r11Manifest.build_sha256, 'r11 builder drift');
assert.equal(sha(readR11('README.md')), r11Manifest.readme_sha256, 'r11 README drift');

const previous = JSON.parse(readR11('candidate/video.json'));
const video = structuredClone(previous);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8]);
const now = video.scenes.filter((scene) => scene.id === 'now-06');
assert.equal(now.length, 1, 'r11 now-06 drift');
const scene = now[0];
assert.deepEqual(scene.claims, ['n14'], 'r11 now-06 claim drift');
assert.deepEqual(scene.lines, [{
  id: 'tszs',
  text: '到了樓梯前，旅客仍得提起箱子；輪子省得了拖行，省不了重量。',
}], 'r11 now-06 narration drift');
assert.equal(scene.data.prompt,
  'Medium shot beside a short flight of terminal stairs. One generic traveler lifts a closed ordinary wheeled suitcase by its carrying handle, with the wheels hanging clear of the floor. The hand, suitcase and first step occupy the middle third. Soft lamp light, no other people, words or logos',
  'r11 now-06 visual drift');
scene.lines[0].text = '到了樓梯前，有些人推輪箱也會犯難；平地好走，不代表每一段路都順手。';
scene.data.prompt = 'Cute medium shot of a generic traveler approaching a short flight of stairs in an unbranded public concourse. A closed ordinary wheeled suitcase stays upright on the level floor, both wheels touching the ground. The traveler pauses with one hand near the carry handle, considering the steps. Do not depict lifting or climbing as mandatory for every traveler; this illustrates a possible difficulty for some travelers. No words, logos, airline marks or real-person likeness.';

const source = {
  title: 'Travelpro 官方比較：旅行袋與輪子行李箱',
  url: 'https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases',
  checked_on: '2026-10-18',
};
assert.ok(!video.sources.some((item) => item.url === source.url), 'new r12 source already in r11');
video.sources.push(source);

const rows = readR11('candidate/claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const oldClaim = 'n14｜樓梯前仍須提起行李箱；輪子不消除箱子和內容物的重量｜｜｜now-06｜PENDING';
const newClaim = 'n14｜Travelpro 官方比較指出，對部分旅客，推輪箱走樓梯可能困難；不支持所有旅客在樓梯前必須提起輪箱的通則｜' + source.url + '｜2026-10-18｜now-06｜PENDING';
assert.equal(rows.filter((row) => row === oldClaim).length, 1, 'r11 n14 claim drift');
rows[rows.indexOf(oldClaim)] = newClaim;
const claims = Buffer.from(rows.join('\n'));
const claimEntries = rows.filter((row) => /^[a-z]\d+[a-z]?｜/.test(row)).map((row) => row.split('｜'));
const sceneByClaim = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(sceneByClaim.size, video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0), 'duplicate claim ID');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(sceneByClaim.keys()), 'claim rows and scene IDs must match');
const datesByUrl = new Map();
const claimIdsByUrl = new Map();
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], sceneByClaim.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'approval must not be inherited');
  if (!cells[2]) continue;
  assert.ok(/^2026-\d\d-\d\d$/.test(cells[3]), 'missing checked_on ' + cells[0]);
  if (!datesByUrl.has(cells[2]) || cells[3] > datesByUrl.get(cells[2])) datesByUrl.set(cells[2], cells[3]);
  if (!claimIdsByUrl.has(cells[2])) claimIdsByUrl.set(cells[2], []);
  claimIdsByUrl.get(cells[2]).push(cells[0]);
}
assert.equal(video.sources.length, previous.sources.length + 1, 'source delta must be exactly one');
assert.equal(new Set(video.sources.map((item) => item.url)).size, video.sources.length, 'duplicate public source URL');
assert.deepEqual(new Set(video.sources.map((item) => item.url)), new Set(datesByUrl.keys()), 'public sources must exactly match claim URL set');
for (const item of video.sources) {
  assert.ok(item.title && /^https:\/\//.test(item.url), 'invalid public source');
  assert.equal(item.checked_on, datesByUrl.get(item.url), 'source checked_on mismatch ' + item.url);
}
assert.deepEqual(claimIdsByUrl.get(source.url), ['n14']);

const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  import(pathToFileURL(path.join(repo, 'tools/video/core/screenplay.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/timeline.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/automation/story.mjs'))),
]);
assert.equal(screenplay(previous), readR11('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r11 screenplay drift');
const script = Buffer.from(screenplay(video));
const series = JSON.parse(readR11('candidate/series.json'));
const lexicon = JSON.parse(readR11('candidate/lexicon.json'));
const lintContext = {
  lexicon,
  brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(video, lintContext);
const lintAt300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'video lint errors: ' + JSON.stringify(lint.errors));
assert.equal(lintAt300.errors.length, 0, '300-CPM video lint errors: ' + JSON.stringify(lintAt300.errors));
assert.equal(cute.length, 0, 'cute visual errors: ' + JSON.stringify(cute));
const timing = Object.fromEntries([250, 275, 300].map((cpm) => [cpm, Number((estimateTimeline(video, cpm).total_frames / 30).toFixed(1))]));
const allLines = video.scenes.flatMap((item) => item.lines);
const sourceMap = {
  status: 'PENDING_INDEPENDENT_FULL_R12_REVIEW',
  derives_from_r11_manifest_sha256: expected.r11_manifest,
  r11_review_sha256_not_inherited: expected.r11_review,
  resolves_r11_p1_addendum_sha256: expected.r11_addendum,
  source_index: [...claimIdsByUrl].map(([url, ids]) => ({ url, claim_ids: ids })),
  changed_line_ids: ['tszs'],
  changed_visual_scene_ids: ['now-06'],
  changed_claim_ids: ['n14'],
  added_source_url: source.url,
  guard: 'Travelpro describes stairs as tricky for some travelers; neither a universal lift requirement nor a historical prototype performance claim is established.',
  host_adoption_guard: 'PENDING: add approved source to live A01 plan only after independent review and compare all worker-remerged public source URLs to cited claims.',
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  target_body_seconds: [420, 480],
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: claimEntries.length,
  loops: video.loops.length,
  spoken_units: allLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
  estimated_body_seconds_not_tts: timing,
  estimated_300_cpm_in_owner_range: timing[300] >= 420 && timing[300] <= 480,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  public_sources: video.sources.length,
  claim_source_urls: datesByUrl.size,
  source_index_matches_claims: true,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r12_review: 'NOT_RUN',
  host_worker_source_merge_and_duration_gate: 'NOT_CHECKED_OR_INSTALLED',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const planSourceAddition = {
  status: 'PROPOSED_NOT_IMPORTED_OR_HOST_REVIEWED',
  applies_to: { series: 'brand-stories-curio-pilot-v2', episode: 1, slug: video.slug, claim_id: 'n14' },
  source: {
    url: source.url,
    publisher: 'Travelpro 官方',
    kind: 'official',
    supports: '官方比較指出：對部分旅客，推輪箱走樓梯或顛簸人行道可能困難；不支持所有旅客必須提箱的通則。',
    checked: '2026-10-18',
  },
  append_only_after_host_review: true,
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readR11('candidate/series.json')],
  ['candidate/lexicon.json', readR11('candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', json(planSourceAddition)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r11_manifest_sha256: expected.r11_manifest,
  r11_review_sha256_not_inherited: expected.r11_review,
  resolves_r11_p1_addendum_sha256: expected.r11_addendum,
  source_snapshot: r11Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r11_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r12');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, claims: validation.claims, loops: validation.loops, sources: validation.public_sources, spoken_units: validation.spoken_units, seconds_250: timing[250], seconds_275: timing[275], seconds_300: timing[300], in_range_at_300: validation.estimated_300_cpm_in_owner_range, lint_errors: lint.errors.length, cute_errors: cute.length }));
