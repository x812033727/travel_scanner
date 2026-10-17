// Isolated A01 r5 metadata correction. Verifies frozen r4 and preserves all script/video bytes.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const r4 = path.resolve(here, '../A01-story-depth-candidate-20261018-r4');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const baseRead = (name) => fs.readFileSync(path.join(here, 'base', name));
const r4ManifestBytes = baseRead('r4-manifest.json');
const expectedR4Manifest = 'e56db0625c2b48c43b732351c1c073dee3e3034c41eb9726c142bec214cfeac0';
assert.equal(sha(r4ManifestBytes), expectedR4Manifest, 'frozen r4 manifest snapshot drift');
assert.equal(sha(fs.readFileSync(path.join(r4, 'manifest.json'))), expectedR4Manifest, 'frozen r4 manifest drift');
const r4Manifest = JSON.parse(r4ManifestBytes);
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];
for (const name of candidateNames) {
  const bytes = baseRead(name);
  assert.equal(sha(bytes), r4Manifest.outputs_sha256['candidate/' + name], 'r4 snapshot drift: ' + name);
  assert.ok(fs.readFileSync(path.join(r4, 'candidate', name)).equals(bytes), 'r4 candidate drift: ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  const bytes = baseRead('r4-' + name);
  assert.equal(sha(bytes), r4Manifest.outputs_sha256[name], 'r4 snapshot drift: ' + name);
  assert.ok(fs.readFileSync(path.join(r4, name)).equals(bytes), 'r4 metadata drift: ' + name);
}
assert.equal(sha(baseRead('r4-README.md')), r4Manifest.readme_sha256, 'r4 README snapshot drift');
assert.ok(fs.readFileSync(path.join(r4, 'README.md')).equals(baseRead('r4-README.md')), 'r4 README drift');

const priorClaim = 'o34｜同篇 1939 年當地報導寫安妮塔出席時有黑色披肩、實用帽子、一只帶輪子的行李箱和另一只放遺漏物品的袋子；只證該場，不能識別箱子實物';
const correctedClaim = priorClaim.replace('黑色披肩', '黑色斗篷');
let claims = baseRead('claims.md').toString('utf8');
assert.equal(claims.split(priorClaim).length, 2, 'expected one old o34 claim');
claims = claims.replace(priorClaim, correctedClaim);
claims += [
  '',
  '## 年份分歧（審稿註記；不是新增播出主張）',
  '',
  'Travelpro 公司沿革將 Plath 直立 Rollaboard 設計記為 1987 年：https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage 。Smithsonian Magazine 回顧稱 Rollaboard 在 1987 年改變登機箱，但未獨立記載車庫製作日期：https://www.smithsonianmag.com/history/history-humble-suitcase-180951376/ 。Plath 在 2024 年《Chinook》校友刊第 17 頁的第一人稱簡歷則自述 1988 年發明直立 Travelpro Rollaboard：https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf 。原旁白保留「依 Travelpro 回顧」的歸屬，兩個年份尚未定讞，t7／t31／h6 仍待獨立覆核。',
  '',
].join('\n');
const claimRows = (value) => [...value.matchAll(/^([a-z]\d+)｜/gm)].map((match) => match[1]);
assert.deepEqual(claimRows(claims), claimRows(baseRead('claims.md').toString('utf8')), 'claim IDs or row order changed');
assert.equal(claimRows(claims).length, 73, 'claim count drift');

const sourceMap = JSON.parse(baseRead('r4-source-map.json'));
sourceMap.derives_from_r4_manifest_sha256 = expectedR4Manifest;
sourceMap.r5_metadata_only = true;
sourceMap.year_conflict_review_note = {
  status: 'UNRESOLVED_INDEPENDENT_REVIEW_REQUIRED',
  affected_claim_ids: ['h6', 't7', 't31'],
  narration_and_visuals_unchanged: true,
  evidence: [
    { url: 'https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage', location: 'How Today’s Wheeled Suitcase Was Invented; What Is A Rollaboard Suitcase?', statement_scope: 'company retrospective dates upright Rollaboard design to 1987' },
    { url: 'https://www.smithsonianmag.com/history/history-humble-suitcase-180951376/', location: 'The History of the Humble Suitcase, carry-on paragraph', statement_scope: 'retrospective dates Rollaboard transformation of carry-on luggage to 1987; not independent evidence for garage build date' },
    { url: 'https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf', location: 'Chinook, May 2024, p. 17, Robert Plath first-person alumni entry', statement_scope: 'Plath dates his invention of vertical rolling Travelpro Rollaboard to 1988' },
  ],
  editorial_boundary: 'Keep existing attributed Travelpro 1987 narration as an attributed claim; do not assert that 1987 or 1988 is the settled single year.',
};
sourceMap.caveats.push('Travelpro dates the upright Rollaboard design to 1987 and Smithsonian dates its carry-on impact to 1987, while Plath’s 2024 first-person alumni note says he invented it in 1988. These sources conflict; the existing attributed Travelpro narration is unchanged and the year is not settled.');
sourceMap.caveats.push('The 1939 newspaper describes a black cape, not a shawl; o34 claim metadata now matches the already-correct narration and illustration.');

const validation = JSON.parse(baseRead('r4-validation.json'));
assert.equal(validation.status, 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED');
assert.equal(validation.duration_540_gate, 'HOLD');
assert.equal(validation.explicit_45_second_gate, 'HOLD');
validation.derives_from_r4_manifest_sha256 = expectedR4Manifest;
validation.r5_metadata_only = true;
validation.r5_script_and_video_unchanged = true;
validation.r5_claim_rows_unchanged = true;
validation.r5_year_conflict_review = 'UNRESOLVED';

const outputs = new Map([
  ['candidate/video.json', baseRead('video.json')],
  ['candidate/series.json', baseRead('series.json')],
  ['candidate/lexicon.json', baseRead('lexicon.json')],
  ['candidate/script.md', baseRead('script.md')],
  ['candidate/claims.md', Buffer.from(claims)],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
for (const name of ['video.json', 'script.md']) {
  assert.equal(sha(outputs.get('candidate/' + name)), r4Manifest.outputs_sha256['candidate/' + name], 'narration or video changed');
}
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: 'story-rolling-suitcase-v2',
  derives_from_r4_manifest_sha256: expectedR4Manifest,
  source_snapshot: r4Manifest.source_snapshot,
  base_sha256: Object.fromEntries(['r4-manifest.json', 'r4-source-map.json', 'r4-validation.json', 'r4-README.md', ...candidateNames].map((name) => [name, sha(baseRead(name))])),
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  script_and_video_bytes_unchanged_from_r4: true,
  r4_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r5');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: manifest.status, r4_manifest_sha256: expectedR4Manifest, scenes: validation.scenes, lines: validation.lines, claims: validation.claims, spoken_units: validation.narration_spoken_units, seconds_250: validation.estimated_timing_not_tts['250'].candidate_seconds, seconds_275: validation.estimated_timing_not_tts['275'].candidate_seconds, seconds_300: validation.estimated_timing_not_tts['300'].candidate_seconds, duration_540_gate: validation.duration_540_gate, explicit_45_second_gate: validation.explicit_45_second_gate, video_sha256: manifest.outputs_sha256['candidate/video.json'], script_sha256: manifest.outputs_sha256['candidate/script.md'] }));
