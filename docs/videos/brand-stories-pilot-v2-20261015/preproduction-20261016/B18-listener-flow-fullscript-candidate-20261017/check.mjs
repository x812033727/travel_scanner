import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const pilot = resolve(here, '../..');
const parent = resolve(here, '../B18-attribution-flow-candidate-20261017');
const predecessor = resolve(here, '../B18-fullscript-candidate-20261017');
const read = (path) => readFileSync(path, 'utf8');
const sha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

const historical = join(pilot, 'scripts/B18.md');
const historicalReview = join(pilot, 'scripts/reviews/B18.md');
const preAdoptionRow = resolve(here, '../B18-active-before-attribution-flow-20261017/episodes-B18.json');
const scriptPath = join(here, 'B18.md');
const parentRow = join(parent, 'B18.json');
const parentVerification = JSON.parse(read(join(parent, 'verification.json')));
assert.equal(sha(join(parent, 'sha256.json')), '8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754', 'flow parent manifest drift');
const flowManifest = JSON.parse(read(join(parent, 'sha256.json')));
for (const [relative, expected] of Object.entries(flowManifest.files)) {
  assert.equal(sha(join(parent, relative)), expected, `flow parent file drift: ${relative}`);
}
assert.equal(sha(join(parent, 'README.md')), flowManifest.README_sha256, 'flow parent README drift');
assert.equal(sha(join(parent, 'build.mjs')), flowManifest.build_sha256, 'flow parent build drift');
assert.equal(sha(join(predecessor, 'B18.md')), '41d3e8d321bdfbb94fefb8039df3713303e5380779ede982165d1d0f1596dfa6', 'reviewed first fullscript drift');
assert.equal(sha(join(predecessor, 'INDEPENDENT-FULLSCRIPT-REVIEW.md')), 'f2bd4d5c3b91d085a9f998355346347be4e97b1afda8c97c652c34cd162cb082', 'first independent review drift');

assert.equal(sha(historical), '5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724', 'historical script drift');
assert.equal(sha(historicalReview), '1583b36311fde688a49f70aa546bb1c30b53ab294afeb1119bb576c73a479cdb', 'historical review drift');
assert.equal(sha(preAdoptionRow), '21122b7db5f97957ca89399b249a02e47e0b4465003e3653efbbf422b6043e9d', 'pre-adoption row snapshot drift');
assert.equal(sha(parentRow), 'c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681', 'candidate row drift');
assert.equal(parentVerification.canonical_story_sha256, 'd0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648', 'parent story drift');
assert.equal(parentVerification.scene_claims, 65, 'parent scene-claim count drift');
assert.equal(parentVerification.all_scene_claims_unchecked, true, 'unexpected formal source check');
assert.notEqual(sha(parentRow), sha(preAdoptionRow), 'candidate row unexpectedly identical to pre-adoption row');

const script = read(scriptPath);
const chapterHeaders = [...script.matchAll(/^## 第([一二三四五六])章｜([^\r\n]+)$/gm)].map((match) => `${match[1]}:${match[2]}`);
assert.equal(chapterHeaders.length, 6, 'expected six chapters');
assert.deepEqual(chapterHeaders.map((chapter) => chapter.slice(0, 1)), ['一', '二', '三', '四', '五', '六']);

const narration = [...script.matchAll(/^> (.+)$/gm)].map((match) => match[1]);
const sectionTexts = script.split(/^## 第[一二三四五六]章｜[^\r\n]+$/m).slice(1);
const voicedByChapter = sectionTexts.map((section) => [...section.matchAll(/^> (.+)$/gm)].map((match) => match[1]));
assert.equal(voicedByChapter.length, 6);
assert(voicedByChapter.every((chapter) => chapter.length >= 3), 'every chapter needs full narration');
assert.equal(narration.length, 25, 'expected 25 voiced paragraphs');
const noteIds = [...script.matchAll(/^\*\*製作註 ([HOIETN]\d{2})（不朗讀）\*\*/gm)].map((match) => match[1]);
assert.equal(noteIds.length, narration.length, 'every voiced paragraph needs source-bound production note');
assert.equal(new Set(noteIds).size, noteIds.length, 'duplicate production note');
const narrationById = Object.fromEntries(noteIds.map((id, index) => [id, narration[index]]));
for (const id of ['H02', 'I01', 'I02', 'I03', 'E04', 'T03']) {
  assert(narrationById[id]?.includes('J-Net21'), `${id} must say the attributed source aloud`);
}
assert(narrationById.I03.includes('同一篇報導'), 'i6 source must be audible from the immediately prior sentence');
assert(narrationById.I04.startsWith('報導還記載'), 'i7 source must audibly carry over from i5/i6');
assert(narrationById.I04.includes('白石的兒子後來回憶') && narrationById.I04.includes('這是家屬的回想與推測'), 'family recollection must not become an independent fact');
assert(narrationById.T01.includes('發明協會記載') && narrationById.T04.includes('發明協會記錄'), 'fact 6/9 must be audibly attributed');
for (const ref of [...script.matchAll(/^\*\*製作註 [^\r\n]+$/gm)].flatMap((line) => [...line[0].matchAll(/\[(\d+)\]/g)].map((match) => Number(match[1])))) {
  assert(ref >= 0 && ref <= 4, `unknown source reference ${ref}`);
}

const spoken = narration.join('');
for (const banned of ['一九七八', '1978', '一九六〇', '1960', '一九九一', '1991', '二〇二三', '2023', '給茶']) {
  assert(!spoken.includes(banned), `banned or unresolved oral tangent: ${banned}`);
}
for (const required of ['一九四八', '一九五七', '一九五八', '一九六二', '一九七〇', '一九七二', '一九八〇', '一九八五', '一九八六', '二〇二一']) {
  assert(spoken.includes(required), `missing required chronological anchor ${required}`);
}
assert(script.includes('既有 5 秒片頭') && script.includes('既有 21 秒片尾'), 'missing intro/outro cue');
assert(script.includes('未通過新版企劃審稿') && script.includes('本稿也不是可直接匯入'), 'missing HOLD notice');
assert(script.includes('法院') && script.includes('判決說的是這一項權利'), 'legal scope needs explicit limit');
assert(narrationById.H02.includes('西口站前') && narrationById.H02.includes('後場') && narrationById.H02.includes('轉角'), 'hook needs three visible setups');
assert(!narrationById.H02.includes('客人會怎麼看') && !narrationById.H02.includes('畫成什麼樣'), 'hook must not regress to table-of-contents questions');
const loops = [...script.matchAll(/^\| H02 /gm)].length;
assert.equal(loops, 3, 'three opening loops must be collected');
const finalSentenceCount = narration.at(-1).match(/[。！？]/g)?.length ?? 0;
assert.equal(finalSentenceCount, 3, 'outro narration should contain exactly three sentences');

const hanAndDigits = [...spoken.matchAll(/[\p{Script=Han}0-9]/gu)].length;
const visible = [...spoken].length;
const hookHanAndDigits = [...voicedByChapter[0].join('').matchAll(/[\p{Script=Han}0-9]/gu)].length;
const oralSourceNameParagraphs = narration.filter((paragraph) => paragraph.includes('J-Net21')).length;
const oralSourceFamilyParagraphs = narration.filter((paragraph) => /J-Net21|記載|報導|記錄|協會|判決|年表/.test(paragraph)).length;
assert(oralSourceNameParagraphs <= 6, 'J-Net21 spoken in too many paragraphs');
assert(oralSourceFamilyParagraphs <= 10, 'source-family phrasing has regressed toward the review HOLD');
const estimatedBodySeconds = Math.round(hanAndDigits / 300 * 60);
const estimatedHookSeconds = Math.round(hookHanAndDigits / 300 * 60);
const minutesAndSeconds = (seconds) => `${Math.floor(seconds / 60)} 分 ${String(seconds % 60).padStart(2, '0')} 秒`;
assert(script.includes(`${hanAndDigits.toLocaleString('en-US')} 個漢字或阿拉伯數字`), 'displayed count drift');
assert(script.includes(`正文約 ${minutesAndSeconds(estimatedBodySeconds)}`), 'displayed body estimate drift');
assert(script.includes(`片尾約 ${minutesAndSeconds(estimatedBodySeconds + 26)}`), 'displayed cut estimate drift');
assert(estimatedHookSeconds <= 30, 'historical hook estimate exceeds current story budget');
assert(estimatedBodySeconds >= 510, 'historical body estimate under current 10-minute lower planning bound');
const report = {
  schema_version: 1,
  status: 'OFFLINE_SCRIPT_STRUCTURE_ONLY_HOLD',
  parent_canonical_story_sha256: parentVerification.canonical_story_sha256,
  parent_flow_manifest_sha256: sha(join(parent, 'sha256.json')),
  reviewed_first_fullscript_sha256: sha(join(predecessor, 'B18.md')),
  first_independent_review_sha256: sha(join(predecessor, 'INDEPENDENT-FULLSCRIPT-REVIEW.md')),
  historical_script_sha256: sha(historical),
  historical_review_sha256: sha(historicalReview),
  pre_adoption_row_sha256: sha(preAdoptionRow),
  candidate_row_sha256: sha(parentRow),
  candidate_script_sha256: sha(scriptPath),
  chapter_count: chapterHeaders.length,
  chapter_voiced_paragraphs: voicedByChapter.map((chapter) => chapter.length),
  voiced_paragraphs: narration.length,
  source_bound_notes: noteIds.length,
  voiced_visible_characters: visible,
  voiced_han_and_digits: hanAndDigits,
  oral_j_net21_name_paragraphs: oralSourceNameParagraphs,
  oral_source_family_paragraphs: oralSourceFamilyParagraphs,
  estimated_body_seconds_at_historical_300_per_minute: estimatedBodySeconds,
  estimated_hook_seconds_at_historical_300_per_minute: estimatedHookSeconds,
  estimated_cut_seconds_plus_5s_intro_21s_outro: estimatedBodySeconds + 26,
  opening_loops_and_payoffs: loops,
  formal_new_fullscript_review_complete: false,
  formal_worker_scene_claims_checked: false,
  tts_measured: false,
  import_approved: false,
  paid_calls: 0,
};

if (process.argv.includes('--write')) {
  writeFileSync(join(here, 'verification.json'), `${JSON.stringify(report, null, 2)}\n`);
} else if (process.argv.includes('--check')) {
  assert.deepEqual(JSON.parse(read(join(here, 'verification.json'))), report, 'verification receipt drift');
} else {
  throw new Error('usage: node check.mjs --write|--check');
}
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
