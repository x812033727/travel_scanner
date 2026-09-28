// The Shorts tool beyond the pilot: the second script format, the themes, the narration sources,
// the listener's check, the twelve quality checks, the upload package, the push and the import.
// Nothing here touches a service: the site, the speech server and the links are handed in.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { encodeWav } from '../tts/wav.mjs';
import { loudnessProblems, profileProblems } from './build.mjs';
import { audioHash, checkPhrases } from './check.mjs';
import { main } from './cli.mjs';
import { PROFILE, buildTimeline, lineOf, parseSrt, phrasesOf, sceneHtml, sha256, srt, validate } from './core.mjs';
import { captionTimingProblems, scriptFromImport, timelineFromCaptions } from './import.mjs';
import { THEMES, themeOf } from './layouts.mjs';
import { composeDescription, composeMetadata, disclosureOf, metadataProblems, packageBuild, packageItems, packageReport, PACKAGE_ITEM_IDS } from './package.mjs';
import { PART_BYTES, evidenceRole, finalReview, projectBody, publishReview, push } from './push.mjs';
import { ITEM_IDS, captionsItem, evidenceItem, factsItem, layoutItem, linksItem, loudnessItem, metadataItem, narrationItem, policyItem, profileItem, qaReport, scriptShape, siteHistory, varietyItem } from './qa.mjs';
import { CHANNEL_VOICE, SiteError, siteClient } from './site.mjs';
import { defaultSource, flaggedPhrases, narrate, phraseBody, phraseKey, serverNarration } from './speech.mjs';

const FIXTURE = fileURLToPath(new URL('./fixtures/smoke/', import.meta.url));
const REPO = fileURLToPath(new URL('../../../', import.meta.url));
const script = () => JSON.parse(readFileSync(path.join(FIXTURE, 'script.json'), 'utf8'));
const cut = (changes = {}) => {
  const { evidence: _evidence, experiment_summary: _summary, limitations: _limits, ...doc } = script();
  return { ...doc, slug: 'cut-model-choice', line: 'cut', series: 'ai-model-choice', source: { slug: 'ai-model-choice', url: 'https://youtu.be/dQw4w9WgXcQ', start_seconds: 62, end_seconds: 118 }, ...changes };
};
const temp = (t, prefix = 'shorts-test-') => {
  const dir = mkdtempSync(path.join(os.tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};
const TOKEN = `mkv_${'a'.repeat(43)}`;
const env = { MOKAAIR_SITE: 'https://site.test', MOKAAIR_VIDEO_TOKEN: TOKEN };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
const tone = (seconds = 1, pitch = 440) => {
  const samples = new Int16Array(Math.round(48_000 * seconds));
  for (let i = 0; i < samples.length; i++) samples[i] = Math.round(Math.sin((2 * Math.PI * pitch * i) / 48_000) * 8000);
  return encodeWav(samples);
};

// --- the script --------------------------------------------------------------------------------

test('the second format takes three content lines, each with what it has to say', () => {
  assert.deepEqual(validate(script()), []);
  assert.deepEqual(validate(cut()), []);
  assert.equal(lineOf(script()), 'lab');
  assert.equal(lineOf({ schema_version: 1 }), 'lab', 'the pilots knew only experiments');
  const { source: _source, ...rootless } = cut();
  assert.ok(validate(rootless).includes('source.slug required'), 'a highlight names the video it was cut from');
  assert.deepEqual(validate(cut({ source: { slug: 'ai-model-choice' } })), [], 'its address may come from the site');
  assert.ok(validate(cut({ source: { slug: 'x', url: 'https://example.com/watch' } })).some((e) => e.includes('YouTube address')));
  assert.ok(validate(cut({ source: { slug: 'x', start_seconds: 90, end_seconds: 30 } })).some((e) => e.includes('after start_seconds')));
  assert.ok(validate(cut({ series: 'Not A Slug' })).includes('series must be the slug of the source'));
  assert.ok(validate({ ...script(), series: 'weekly' }).includes('invalid series'));
  const { evidence: _evidence, ...bare } = script();
  assert.ok(validate(bare).includes('evidence required'), 'an experiment shows its evidence');
  const { limitations: _limits, ...unbounded } = script();
  assert.ok(validate(unbounded).includes('limitations required'));
  assert.ok(validate({ ...script(), hashtags: ['a', 'b', 'c', 'd'] }).some((e) => e.includes('hashtags')));
  assert.ok(validate({ ...script(), hashtags: ['two words'] }).some((e) => e.includes('hashtags')));
  assert.ok(validate({ ...script(), links: [{ label: '文章', url: 'http://mokaair.com/x' }] }).some((e) => e.includes('https')));
  assert.ok(validate({ ...script(), titles: ['<b>粗體</b>', '第二個'] }).some((e) => e.includes('angle brackets')));
  assert.ok(validate({ ...script(), line: 'travel' }).some((e) => e.startsWith('line must be')));
  assert.deepEqual(validate({ ...script(), schema_version: 3 }), ['schema_version must be 1 or 2']);
});

test('the three pilots stay valid in the format they were written in', () => {
  for (const slug of ['shorts-receipt-total', 'shorts-poster-blind', 'shorts-prompt-check']) {
    const doc = JSON.parse(readFileSync(path.join(REPO, 'docs/videos/ai-shorts/pilots', `${slug}.json`), 'utf8'));
    assert.equal(doc.schema_version, 1);
    assert.deepEqual(validate(doc), []);
    assert.ok(themeOf(doc).id.startsWith('lab-'), 'and get the look of their series');
  }
});

test('each series and the highlights have a look of their own inside the same safe area', () => {
  const looks = [['lab', 'daily'], ['lab', 'blind'], ['lab', 'prompts'], ['cut', 'ai-model-choice']].map(([line, series]) => themeOf({ schema_version: 2, line, series }));
  assert.equal(new Set(looks.map((theme) => theme.id)).size, 4);
  assert.equal(new Set(looks.map((theme) => theme.colors.background)).size, 4);
  assert.equal(new Set(looks.map((theme) => theme.kicker)).size, 4);
  assert.equal(new Set(looks.map((theme) => theme.rows)).size, 3, 'rows are stacked, compared or numbered');
  assert.equal(themeOf({ schema_version: 2, line: 'lab', series: 'unknown' }), THEMES['lab:daily']);
  const cue = { sceneIndex: 1, text: '咖啡兩杯，蛋糕三塊' };
  const pages = [script(), { ...script(), series: 'blind' }, { ...script(), series: 'prompts' }, cut()].map((doc) => sceneHtml(doc, cue));
  // What the build measures never moves: the content box, the caption bar and the frame.
  for (const page of pages) {
    assert.match(page, /\.content\{position:absolute;left:80px;top:258px;width:820px;height:1120px/);
    assert.match(page, /\.caption\{position:absolute;left:80px;top:1430px;width:820px;height:165px/);
    assert.match(page, /width:1080px;height:1920px/);
  }
  assert.match(pages[0], /data-theme="lab-daily"/);
  assert.match(pages[1], /class="row side-a">咖啡 85 元 × 2<.*class="row side-b">蛋糕/s);
  assert.match(pages[2], /class="row numbered"><span class="n">1<\/span>/);
  assert.match(pages[3], /MOKAAIR \/ 長片精華.*完整影片在說明欄/s);
  assert.ok(!sceneHtml({ ...script(), scenes: [{ headline: '<script>x</script>', narration: ['a'] }] }, { sceneIndex: 0, text: 'a' }).includes('<script>x'));
});

test('a caption file reads back as the timeline it was written from', () => {
  const timeline = buildTimeline(script(), phrasesOf(script()).map(() => 3));
  const cues = parseSrt(`\uFEFF${srt(timeline).replace(/\n/g, '\r\n')}`);
  assert.equal(cues.length, 11);
  assert.deepEqual(cues[0], { start: 0, end: timeline.cues[0].endFrame / 30, text: '一張手寫的發票' });
  assert.throws(() => parseSrt('1\nno time here\nwords'), /no time line/);
  assert.throws(() => parseSrt('1\n00:00:02,000 --> 00:00:01,000\nwords'), /ends before/);
  assert.throws(() => parseSrt('1\n00:00:01,000 --> 00:00:02,000\n'), /empty/);
  assert.throws(() => buildTimeline(script(), phrasesOf(script()).map(() => 3), { minSeconds: 40, maxSeconds: 55 }), /fit 40–55s/, 'the length is the owner\'s setting');
});

// --- narration ---------------------------------------------------------------------------------

test('a server phrase is asked for once, in the owner\'s voice, and again only when flagged', async (t) => {
  const cacheDir = path.join(temp(t), 'cache');
  const asked = [];
  const synthesizeImpl = async ({ body, site, token }) => {
    asked.push({ body, site, token });
    return { wav: tone(1, 300 + asked.length), billable: 7 };
  };
  const client = { site: 'https://site.test', token: TOKEN };
  const phrases = ['一張手寫的發票', '再扣掉三十元的折價券', '一張手寫的發票'];
  const first = await serverNarration({ phrases, voice: CHANNEL_VOICE, cacheDir, client, synthesizeImpl });
  assert.equal(asked.length, 2, 'the same words in the same voice are one clip');
  assert.deepEqual(asked[0].body, { voice: 'gemini:Sulafat', style: CHANNEL_VOICE.style, segments: [{ parts: [{ text: '一張手寫的發票' }], break_after_ms: 0 }] });
  assert.equal(asked[0].token, TOKEN);
  assert.deepEqual([first.calls, first.characters, first.provider, first.clips.length], [2, 14, 'gemini', 3]);
  assert.deepEqual(first.clips[0], first.clips[2]);
  const again = await serverNarration({ phrases, voice: CHANNEL_VOICE, cacheDir, client, synthesizeImpl });
  assert.deepEqual([again.calls, again.characters, asked.length], [0, 0, 2], 'a second build costs nothing');
  const redone = await serverNarration({ phrases, voice: CHANNEL_VOICE, cacheDir, client, redo: [1], synthesizeImpl });
  assert.deepEqual([redone.calls, asked.length], [1, 3]);
  assert.notDeepEqual(redone.clips[1], first.clips[1]);
  const other = await serverNarration({ phrases: phrases.slice(0, 1), voice: { ...CHANNEL_VOICE, name: 'Kore' }, cacheDir, client, synthesizeImpl });
  assert.equal(other.calls, 1, 'another voice is another clip');
  assert.notEqual(phraseKey(CHANNEL_VOICE, 'API 是什麼'), phraseKey(CHANNEL_VOICE, 'API 是什麼', { terms: { API: 'A P I' } }));
  assert.deepEqual(phraseBody({ provider: 'azure', name: 'zh-TW-HsiaoChenNeural' }, '你好').voice, 'zh-TW-HsiaoChenNeural');
});

test('the three sources, and which one a build takes when none is named', async (t) => {
  assert.equal(defaultSource('win32'), 'windows');
  assert.equal(defaultSource('linux'), 'server');
  const dir = temp(t);
  const doc = { slug: 'x', scenes: [{ narration: ['一', '二'] }] };
  writeFileSync(path.join(dir, '000.wav'), tone(1, 300));
  writeFileSync(path.join(dir, '001.wav'), tone(1, 400));
  const supplied = await narrate({ doc, source: 'files', workBase: dir, audioDir: dir });
  assert.deepEqual([supplied.provider, supplied.calls, supplied.clips.length], ['files', 0, 2]);
  await assert.rejects(narrate({ doc, source: 'files', workBase: dir }), /--audio-dir/);
  await assert.rejects(narrate({ doc, source: 'server', workBase: dir }), /login/);
  await assert.rejects(narrate({ doc, source: 'radio', workBase: dir }), /server, windows, files/);
  writeFileSync(path.join(dir, 'check.json'), JSON.stringify({ flagged_lines: [{ index: 4 }, { index: 9 }] }));
  assert.deepEqual(flaggedPhrases(path.join(dir, 'check.json')), [4, 9]);
  assert.deepEqual(flaggedPhrases(path.join(dir, 'none.json')), []);
});

test('the listener passes what says the script and asks Jev about the rest', async () => {
  const phrases = ['一張手寫的發票', '再扣掉三十元的折價券', '答案是兩百七十五元', '這一題打成平手'];
  const clips = phrases.map((_phrase, index) => tone(1, 300 + index * 10));
  // 券 and 卷 sound the same, but 30 is not written 三十; 局 is not 手.
  const heard = ['一張手寫的發票。', '再扣掉30元的折價卷', '答案是兩百七十五元', '這一題打成平局'];
  const sent = [];
  const transcribe = async ({ wav, terms }) => {
    sent.push({ bytes: wav.length, terms });
    return heard[sent.length - 1];
  };
  const judged = [];
  const judge = async ({ lines }) => {
    judged.push(lines);
    return new Map([['p001', 0.92], ['p003', 0.2]]);
  };
  const check = await checkPhrases({ phrases, clips, transcribe, judge });
  assert.deepEqual(check.results.map((result) => result.verdict), ['exact', 'judge', 'exact', 'judge']);
  assert.equal(judged.length, 1, 'one Jev call for everything in doubt');
  assert.deepEqual(judged[0].map((line) => line.id), ['p001', 'p003']);
  assert.deepEqual(Object.keys(judged[0][0]).sort(), ['heard', 'id', 'intended', 'spoken_form']);
  assert.deepEqual([check.ok, check.lines, check.checked, check.flagged, check.judge_calls], [false, 4, 4, 1, 1]);
  assert.deepEqual(check.flagged_lines, [{ index: 3, text: '這一題打成平手', heard: '這一題打成平局', noul: 0.2 }]);
  const alike = await checkPhrases({ phrases: ['這一題打成平手'], clips: clips.slice(0, 1), transcribe: async () => '這一提打成平守', judge: async () => assert.fail('same sounds need no judge') });
  assert.deepEqual([alike.ok, alike.results[0].verdict], [true, 'sound']);
  assert.equal(check.audio_sha256, audioHash(clips));
  assert.ok(sent.every((clip) => clip.bytes < clips[0].length), 'the transcriber takes 16 kHz');
  const silent = await checkPhrases({ phrases: phrases.slice(1, 2), clips: clips.slice(1, 2), transcribe: async () => '別的話', judge: async () => new Map() });
  assert.deepEqual([silent.ok, silent.flagged_lines[0].noul], [false, null], 'no answer is a doubt, never a pass');
  const fine = await checkPhrases({ phrases: phrases.slice(0, 1), clips: clips.slice(0, 1), transcribe: async () => '一張手寫的發票', judge: async () => assert.fail('nothing to judge') });
  assert.deepEqual([fine.ok, fine.judge_calls], [true, 0]);
  await assert.rejects(checkPhrases({ phrases, clips: clips.slice(1), transcribe, judge }), /4 phrases but 3 clips/);
});

// --- the quality check ---------------------------------------------------------------------------

const measured = (changes = {}) => ({
  video: { width: 1080, height: 1920, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: '1050', ...changes.video },
  audio: { codec_name: 'aac', sample_rate: '48000', duration: '35.01', ...changes.audio },
  loudness: { input_i: '-14.20', input_tp: '-1.50', ...changes.loudness },
});

test('the twelve items are the site\'s twelve, in its order', () => {
  const source = readFileSync(path.join(REPO, 'apps/api/app/video_automation/judge.py'), 'utf8');
  const tuple = (name) => [...source.match(new RegExp(`${name}: tuple\\[str, \\.\\.\\.\\] = \\(([^)]*)\\)`))[1].matchAll(/"([a-z_]+)"/g)].map((match) => match[1]);
  assert.deepEqual([...ITEM_IDS], tuple('SHORTS_QA_ITEMS'));
  assert.deepEqual([...PACKAGE_ITEM_IDS], tuple('SHORTS_PACKAGE_ITEMS'));
  const items = ITEM_IDS.map((id) => ({ id, ok: true, detail: '' }));
  assert.deepEqual(qaReport(items, 'f'.repeat(64), 'lab'), { ok: true, final_sha256: 'f'.repeat(64), kind: 'shorts', line: 'lab', items });
  assert.equal(qaReport([{ ...items[0], ok: false }, ...items.slice(1)], 'f'.repeat(64), 'cut').ok, false);
  assert.throws(() => qaReport(items.slice(1), 'f'.repeat(64), 'lab'), /exactly profile/);
  assert.throws(() => qaReport([items[1], items[0], ...items.slice(2)], 'f'.repeat(64), 'lab'), /exactly profile/);
});

test('the cut is a Short: its size, its frames, its length and its loudness', () => {
  assert.equal(profileItem({ measured: measured(), frames: 1050 }).ok, true);
  assert.deepEqual(profileProblems(measured(), 1050), []);
  assert.match(profileItem({ measured: measured({ video: { width: 1920, height: 1080 } }), frames: 1050 }).detail, /1920×1080, not 1080×1920/);
  assert.match(profileItem({ measured: measured({ video: { nb_frames: '1049' } }), frames: 1050 }).detail, /1049 frames, the timeline has 1050/);
  assert.match(profileItem({ measured: measured({ audio: { duration: '35.2' } }), frames: 1050 }).detail, /audio runs 35.2s/);
  assert.match(profileItem({ measured: measured({ video: { r_frame_rate: '25/1' } }), frames: 1050 }).detail, /frame rate is 25\/1/);
  assert.match(profileItem({ measured: measured({ audio: { sample_rate: '44100' } }), frames: 1050 }).detail, /44100 Hz/);
  assert.match(profileItem({ measured: measured(), frames: 1050, range: { minSeconds: 40, maxSeconds: 55 } }).detail, /35.00s is outside 40–55s/);
  assert.equal(loudnessItem(measured()).ok, true);
  assert.deepEqual(loudnessProblems({ input_i: '-15.2', input_tp: '-0.5' }), ['-15.2 LUFS is outside −14 ± 1', 'the true peak -0.5 dBTP is above −0.8']);
  assert.equal(PROFILE.fps, 30);
});

test('the cards were measured, the clips were heard, the evidence is the script\'s', () => {
  const layout = [{ cue: 0, problems: [] }, { cue: 1, problems: [] }];
  assert.equal(layoutItem({ checks: { layout }, cues: 2 }).ok, true);
  assert.match(layoutItem({ checks: { layout }, cues: 3 }).detail, /2 cues measured of 3/);
  assert.match(layoutItem({ checks: { layout: [{ cue: 0, problems: ['caption outside safe area'] }] }, cues: 1 }).detail, /cue 0: caption outside/);
  assert.match(layoutItem({ checks: { imported: true }, cues: 2 }).detail, /safe-area overlay/);
  assert.equal(layoutItem({ checks: null, cues: 2 }).ok, false);

  const check = { ok: true, audio_sha256: 'a'.repeat(64), lines: 11, checked: 11, flagged: 0, flagged_lines: [] };
  assert.equal(narrationItem({ check, audioSha256: 'a'.repeat(64), phrases: 11 }).ok, true);
  assert.match(narrationItem({ check, audioSha256: 'b'.repeat(64), phrases: 11 }).detail, /other audio/);
  assert.match(narrationItem({ check: { ...check, checked: 9 }, audioSha256: 'a'.repeat(64), phrases: 11 }).detail, /9 of 11/);
  assert.match(narrationItem({ check: { ...check, ok: false, flagged: 1, flagged_lines: [{ index: 3, heard: '平守' }] }, audioSha256: 'a'.repeat(64), phrases: 11 }).detail, /#3 heard 「平守」/);
  assert.match(narrationItem({ check: null, audioSha256: 'a'.repeat(64), phrases: 11 }).detail, /run check-audio/);

  assert.equal(evidenceItem({ doc: script() }).ok, true);
  assert.deepEqual(evidenceItem({ doc: script(), evidenceError: 'evidence changed: evidence/result.json' }), { id: 'evidence', ok: false, detail: 'evidence changed: evidence/result.json' });
  const now = new Date('2026-10-10T00:00:00Z');
  const onSite = { youtube_video_id: 'dQw4w9WgXcQ', youtube_publish_at: '2026-10-01T11:30:00Z', reviews: [] };
  assert.equal(evidenceItem({ doc: cut(), source: onSite, now }).ok, true);
  assert.match(evidenceItem({ doc: cut(), source: { ...onSite, youtube_publish_at: '2026-11-01T11:30:00Z' }, now }).detail, /neither public nor approved/);
  assert.equal(evidenceItem({ doc: cut(), source: { reviews: [{ gate: 'final', status: 'approved' }] }, now }).ok, true);
  assert.match(evidenceItem({ doc: cut(), source: { ...onSite, dropped_at: '2026-10-02T00:00:00Z' }, now }).detail, /was dropped/);
  assert.match(evidenceItem({ doc: cut(), source: null, now }).detail, /has no video ai-model-choice/);
});

test('the facts were checked for this script, and Jev read the narration', () => {
  const digest = 'd'.repeat(64);
  const verify = { ok: true, document_sha256: digest, checked_by: 'claude-opus-5-5', claims: [{ text: '兩個 AI 都回答 275', ok: true }], problems: [] };
  assert.deepEqual(factsItem({ verify, documentSha256: digest }), { id: 'facts', ok: true, detail: '1 claims backed by the evidence, checked by claude-opus-5-5' });
  assert.match(factsItem({ verify, documentSha256: 'e'.repeat(64) }).detail, /another version/);
  assert.match(factsItem({ verify: { ...verify, claims: [{ text: 'B 比較快', ok: false }] }, documentSha256: digest }).detail, /not backed by the evidence: B 比較快/);
  assert.match(factsItem({ verify: { ...verify, problems: ['「最準」沒有依據'] }, documentSha256: digest }).detail, /「最準」沒有依據/);
  assert.match(factsItem({ verify: { ...verify, claims: [] }, documentSha256: digest }).detail, /lists no claim/);
  assert.equal(factsItem({ verify: { ...verify, ok: false }, documentSha256: digest }).ok, false);
  assert.match(factsItem({ verify: null, documentSha256: digest }).detail, /verify.json is missing/);
  assert.deepEqual(policyItem({ passed: true, note: 'Jev：符合立場 0.81，通過' }), { id: 'policy', ok: true, detail: 'Jev：符合立場 0.81，通過' });
  assert.equal(policyItem({ passed: false, stance: 0.3 }).ok, false);
  assert.equal(policyItem({ note: 'no verdict' }).ok, false);
});

test('the metadata fits YouTube, the captions sit on the timeline, the links open', () => {
  const doc = script();
  const timeline = buildTimeline(doc, phrasesOf(doc).map(() => 3));
  const metadata = composeMetadata({ doc, finalSha256: 'f'.repeat(64), seconds: timeline.seconds });
  assert.equal(metadataItem({ metadata }).ok, true);
  assert.deepEqual(metadataProblems({ ...metadata, titles: ['x'.repeat(101), '<b>'], description: '好'.repeat(1700), tags: Array.from({ length: 60 }, (_x, i) => `tag number ${i}`), hashtags: ['#a', '#b', '#c', '#d'] }).map((problem) => problem.split(' (')[0].slice(0, 28)), [
    'a title of 101 characters',
    'a title with an angle bracke',
    'the description is 5100 byte',
    'the tags are 949 characters ',
    '4 hashtags',
  ]);
  const captions = new Map([['zh-TW', srt(timeline)]]);
  assert.equal(captionsItem({ captions, timeline }).ok, true);
  assert.match(captionsItem({ captions: new Map(), timeline }).detail, /zh-TW.srt is missing/);
  assert.match(captionsItem({ captions: new Map([['zh-TW', srt(timeline).replace('一張手寫的發票', '一張發票')]]), timeline }).detail, /caption 1 says another phrase/);
  assert.match(captionsItem({ captions: new Map([['zh-TW', srt(timeline).replace('00:00:00,000', '00:00:00,500')]]), timeline }).detail, /caption 1 is off the timeline/);
  assert.match(captionsItem({ captions, timeline, locales: ['en'] }).detail, /en.srt is missing/);
  const english = srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: `line ${cue.index}` })) });
  assert.equal(captionsItem({ captions: new Map([...captions, ['en', english]]), timeline, locales: ['en'] }).ok, true, 'a translation says other words on the same clock');
  const opened = [{ url: 'https://youtu.be/dQw4w9WgXcQ', ok: true, status: 200 }];
  assert.equal(linksItem({ results: opened, metadata: composeMetadata({ doc: cut(), finalSha256: 'f'.repeat(64), seconds: 35, sourceUrl: 'https://youtu.be/dQw4w9WgXcQ' }) }).ok, true);
  assert.match(linksItem({ results: [{ url: 'https://mokaair.com/x', ok: false, status: 404, error: 'HTTP 404' }], metadata }).detail, /1 of 1 links do not open/);
  assert.match(linksItem({ results: [], metadata: composeMetadata({ doc: cut({ source: { slug: 'ai-model-choice' } }), finalSha256: 'f'.repeat(64), seconds: 35 }) }).detail, /does not lead back/);
  assert.equal(linksItem({ results: [], metadata }).detail, 'the description has no links');
});

test('an opening is not said twice, and two Shorts of a series are not built alike', () => {
  const doc = script();
  const mine = scriptShape(doc);
  assert.deepEqual(mine, { opening: '一張手寫的發票', structure: '30-23-2b0n-22-20n' });
  const others = [
    { slug: 'blind-poster', series: 'blind', opening: '兩張海報', structure: mine.structure },
    { slug: 'daily-menu', series: 'daily', opening: '一張菜單', structure: '3-2-2' },
  ];
  assert.equal(varietyItem({ doc, history: others }).ok, true, 'another series may be built the same way');
  assert.match(varietyItem({ doc, history: [{ slug: 'daily-old', series: 'daily', opening: '一張手寫的發票！', structure: '1' }] }).detail, /daily-old opens with the same words/);
  assert.match(varietyItem({ doc, history: [{ slug: 'daily-menu', series: 'daily', opening: 'x', structure: mine.structure }] }).detail, /built exactly like daily-menu/);
  assert.equal(varietyItem({ doc, history: [{ slug: doc.slug, series: 'daily', ...mine }] }).ok, true, 'it is not compared with itself');
  assert.equal(varietyItem({ doc, history: [...Array.from({ length: 30 }, (_x, i) => ({ slug: `s${i}`, series: 'blind', opening: `o${i}`, structure: 'x' })), { slug: 'old', series: 'daily', opening: mine.opening, structure: 'y' }] }).ok, true, 'only the latest thirty count');
  assert.match(varietyItem({ doc, history: null }).detail, /could not be read/);
});

test('the latest Shorts are read from their final reviews on the site', async () => {
  const asked = [];
  const client = {
    videos: async (query) => {
      asked.push(query);
      return [{ slug: 'a', shorts_series: 'daily' }, { slug: 'b', shorts_series: 'blind' }, { slug: 'c', shorts_series: 'daily' }];
    },
    project: async (slug) => ({
      a: { reviews: [{ gate: 'publish', status: 'approved', payload: {} }, { gate: 'final', status: 'approved', payload: { script: { opening: '一', structure: '3-2' } } }] },
      b: { reviews: [{ gate: 'final', status: 'superseded', payload: { script: { opening: '舊', structure: '1' } } }] },
      c: null,
    })[slug],
  };
  assert.deepEqual(await siteHistory(client), [{ slug: 'a', series: 'daily', opening: '一', structure: '3-2' }]);
  assert.deepEqual(asked, [{ shorts: 'only', limit: '60' }]);
});

// --- the upload package --------------------------------------------------------------------------

test('the description leads back to the full video, and says what an experiment tested', () => {
  assert.equal(composeDescription(script()), '工具的煙霧測試用腳本：畫面與旁白都是替身，沒有問過任何模型。\n\n實測範圍：同一題算式各問一次，對照先寫好的答案。\n限制：只測一題、各一次，不能代表模型整體的能力。\n\n#AI #實測\n');
  const highlight = composeDescription(cut({ links: [{ label: '文章', url: 'https://mokaair.com/zh-TW/guides/ai-model-choice' }], hashtags: undefined }), { sourceUrl: 'https://youtu.be/dQw4w9WgXcQ' });
  assert.ok(highlight.startsWith('完整影片：https://youtu.be/dQw4w9WgXcQ\n\n'), 'a Short\'s related video cannot be set through the API');
  assert.match(highlight, /文章：https:\/\/mokaair\.com\/zh-TW\/guides\/ai-model-choice\n\n#AI\n$/);
  assert.ok(!highlight.includes('實測範圍'));
  const metadata = composeMetadata({ doc: cut({ source: { slug: 'ai-model-choice' } }), finalSha256: 'f'.repeat(64), seconds: 35.2, settings: { made_for_kids: false }, sourceUrl: 'https://youtu.be/dQw4w9WgXcQ' });
  assert.deepEqual([metadata.kind, metadata.line, metadata.category_id, metadata.default_language, metadata.made_for_kids], ['shorts', 'cut', '28', 'zh-TW', false]);
  assert.deepEqual(metadata.source, { slug: 'ai-model-choice', url: 'https://youtu.be/dQw4w9WgXcQ' });
  assert.deepEqual([metadata.title, metadata.titles.length, metadata.tags, metadata.hashtags], [script().titles[0], 2, ['AI 實測', 'AI', '實測'], ['#AI', '#實測']]);
  assert.deepEqual(disclosureOf(script()), { synthetic: false, reason: '字卡、實測紀錄與合成旁白，沒有擬真的生成或變造內容' });
  assert.equal(disclosureOf({ ...script(), synthetic_media: true }).synthetic, true);
  assert.deepEqual([disclosureOf({ schema_version: 2, line: 'drama' }).synthetic, composeMetadata({ doc: { ...cut(), line: 'drama' }, finalSha256: 'f', seconds: 30 }).category_id], [true, '24']);
});

function builtDirectory(t, { qaOk = true, doc = script() } = {}) {
  const directory = temp(t, 'shorts-build-');
  for (const sub of ['upload', 'audio', 'evidence/evidence']) mkdirSync(path.join(directory, sub), { recursive: true });
  const timeline = buildTimeline(doc, phrasesOf(doc).map(() => 3));
  const finalBytes = Buffer.from('not really an mp4, but the same bytes every time');
  writeFileSync(path.join(directory, 'script.json'), `${JSON.stringify(doc, null, 2)}\n`);
  writeFileSync(path.join(directory, 'timeline.json'), JSON.stringify(timeline));
  writeFileSync(path.join(directory, 'usage.json'), JSON.stringify({ narration: { seconds: 33, characters: 96, calls: 11, provider: 'gemini' }, stages: {}, checks: {} }));
  writeFileSync(path.join(directory, 'check.json'), JSON.stringify({ ok: true }));
  writeFileSync(path.join(directory, 'contact-sheet.png'), 'sheet');
  writeFileSync(path.join(directory, 'upload', 'final.mp4'), finalBytes);
  writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), srt(timeline));
  writeFileSync(path.join(directory, 'upload', 'cover.png'), 'cover');
  writeFileSync(path.join(directory, 'upload', 'manifest.json'), JSON.stringify({ slug: doc.slug, status: 'built' }));
  for (const evidence of doc.evidence ?? []) writeFileSync(path.join(directory, 'evidence', evidence.path), readFileSync(path.join(FIXTURE, evidence.path)));
  const items = ITEM_IDS.map((id) => ({ id, ok: qaOk || id !== 'facts', detail: '' }));
  writeFileSync(path.join(directory, 'qa.json'), JSON.stringify({ ...qaReport(items, sha256(finalBytes), lineOf(doc)), script: scriptShape(doc), checked_at: '2026-10-01T00:00:00Z' }));
  return { directory, finalSha: sha256(finalBytes), timeline };
}

test('the package is what the site sets on the video, checked against the cut that was checked', (t) => {
  const { directory, finalSha } = builtDirectory(t);
  const { metadata, report } = packageBuild({ directory, settings: { made_for_kids: false }, now: () => new Date('2026-10-01T00:00:00Z') });
  assert.deepEqual(report.items.map((each) => [each.id, each.ok]), [['files', true], ['descriptions', true], ['captions', true], ['disclosure', true]]);
  const written = readFileSync(path.join(directory, 'upload', 'metadata.json'));
  assert.deepEqual([report.ok, report.kind, report.final_sha256], [true, 'shorts', sha256(written)], 'bound to metadata.json, as the publish review is');
  assert.equal(metadata.final_sha256, finalSha);
  assert.equal(readFileSync(path.join(directory, 'upload', 'description.zh-TW.txt'), 'utf8'), metadata.description);
  const manifest = JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8'));
  assert.equal(manifest.status, 'qa-passed');
  assert.deepEqual(manifest.files.map((file) => file.name), ['final.mp4', 'zh-TW.srt', 'cover.png', 'metadata.json', 'description.zh-TW.txt']);
  assert.throws(() => packageReport(report.items.slice(1), 'x'), /exactly files/);

  writeFileSync(path.join(directory, 'upload', 'final.mp4'), 'another cut');
  const stale = packageBuild({ directory });
  assert.match(stale.report.items[0].detail, /quality check is of another final cut/);
  assert.equal(JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8')).status, 'unchecked');
});

test('the manifest says how the check went, and a package item names what is missing', (t) => {
  const { directory, timeline } = builtDirectory(t, { qaOk: false });
  packageBuild({ directory });
  assert.equal(JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8')).status, 'qa-failed');
  const metadata = composeMetadata({ doc: script(), finalSha256: 'f'.repeat(64), seconds: 35 });
  const items = packageItems({ files: new Map([['metadata.json', Buffer.from('{}')]]), metadata: { ...metadata, contains_synthetic_media: undefined }, timeline, qa: null });
  assert.deepEqual(items.map((each) => each.ok), [false, false, false, false]);
  assert.match(items[0].detail, /final.mp4 is missing; zh-TW.srt is missing; cover.png is missing/);
  assert.match(items[1].detail, /description.zh-TW.txt is missing/);
  assert.match(items[3].detail, /does not answer/);
  assert.throws(() => packageBuild({ directory: os.tmpdir() }), /not a finished build/);
});

// --- the push ------------------------------------------------------------------------------------

function fakeSite({ finalStatus = 'approved', publishStatus = 'approved' } = {}) {
  const calls = [];
  const stored = new Set();
  return {
    calls,
    client: {
      report: async (slug, body) => {
        calls.push(['report', slug, body]);
        return {};
      },
      part: async (slug, digest, bytes, query) => {
        calls.push(['part', digest, bytes.length, query]);
        stored.add(digest);
        return { received: [Number(query.part)], complete: Number(query.part) === Number(query.parts) - 1 };
      },
      submit: async (slug, review) => {
        calls.push(['submit', slug, review]);
        const status = review.gate === 'final' ? finalStatus : publishStatus;
        return { id: 'r', gate: review.gate, status, note: status === 'approved' ? '依設定自動核准' : null };
      },
    },
  };
}

test('a Short whose cut is approved goes on to its upload package', async (t) => {
  const { directory, finalSha } = builtDirectory(t);
  packageBuild({ directory });
  const { client, calls } = fakeSite();
  const result = await push({ directory, client });
  assert.deepEqual([result.slug, result.final.status, result.publish.status, result.waits], ['shorts-smoke-receipt', 'approved', 'approved', null]);
  const reported = calls.find(([kind]) => kind === 'report')[2];
  assert.deepEqual([reported.format, reported.shorts_line, reported.shorts_series, reported.title, reported.stage], ['shorts', 'lab', 'daily', script().titles[0], 'final']);
  assert.deepEqual(calls.filter(([kind]) => kind === 'report').map(([, , body]) => body.stage), ['final', 'publish'], 'at its final cut until that is approved');
  assert.deepEqual(reported.checklist.map((step) => [step.key, step.done]), [['built', true], ['audio', true], ['qa', true], ['package', true]]);
  assert.ok(!('source_slug' in reported));
  const [final, publish] = calls.filter(([kind]) => kind === 'submit').map(([, , review]) => review);
  assert.deepEqual([final.gate, final.content_sha256], ['final', finalSha]);
  assert.deepEqual(final.files.map((file) => [file.role, file.content_type]), [['preview', 'video/mp4'], ['thumbnail', 'image/png'], ['contact_sheet', 'image/png'], ['evidence_evidence_result', 'application/json']]);
  assert.deepEqual([final.payload.qa.kind, final.payload.qa.final_sha256, final.payload.qa.items.length], ['shorts', finalSha, 12]);
  assert.ok(!('checked_at' in final.payload.qa) && !('script' in final.payload.qa), 'the report goes as the site reads it');
  assert.deepEqual(final.payload.usage.narration, { seconds: 33, characters: 96, calls: 11, provider: 'gemini' });
  assert.deepEqual(final.payload.script, { series: 'daily', opening: '一張手寫的發票', structure: '30-23-2b0n-22-20n' });
  assert.match(final.summary, /^Shorts 35\.\d 秒，Shorts 自動品管 12 項全過$/);
  const metadataSha = sha256(readFileSync(path.join(directory, 'upload', 'metadata.json')));
  assert.deepEqual([publish.gate, publish.content_sha256, publish.payload.package.final_sha256, publish.payload.package.kind], ['publish', metadataSha, metadataSha, 'shorts']);
  assert.deepEqual(publish.files.map((file) => file.role), ['metadata', 'final', 'captions_zh-TW', 'description_zh-TW'], 'no thumbnail: the site would set it on YouTube');
  assert.deepEqual(publish.files.map((file) => file.content_type), ['application/json', 'video/mp4', 'application/x-subrip', 'text/plain']);
  assert.equal(publish.summary, 'Shorts 上傳包 4 項齊全：照月曆上架');
  assert.deepEqual(publish.payload.disclosure, { synthetic: false, reason: '字卡、實測紀錄與合成旁白，沒有擬真的生成或變造內容' });
  assert.ok(calls.filter(([kind]) => kind === 'part').every(([, , length, query]) => length <= PART_BYTES && query.parts === '1'));
});

test('a cut that waits for the owner stops the push before the package', async (t) => {
  const { directory } = builtDirectory(t, { qaOk: false });
  packageBuild({ directory });
  const waiting = fakeSite({ finalStatus: 'pending' });
  const result = await push({ directory, client: waiting.client });
  assert.deepEqual([result.final.status, result.publish, result.waits], ['pending', null, 'the final cut waits for the owner on /admin/videos']);
  const [final] = waiting.calls.filter(([kind]) => kind === 'submit').map(([, , review]) => review);
  assert.equal(final.summary.split('，')[1], 'Shorts 自動品管 1 項沒過：facts');
  assert.equal(waiting.calls.filter(([kind]) => kind === 'submit').length, 1);
  assert.equal(waiting.calls.find(([kind]) => kind === 'report')[2].stage, 'final');
  const sentBack = await push({ directory, client: fakeSite({ finalStatus: 'rejected' }).client });
  assert.match(sentBack.waits, /sent the cut back/);
  const unpackaged = builtDirectory(t);
  assert.match((await push({ directory: unpackaged.directory, client: fakeSite().client })).waits, /run package, then push again/);
  const held = fakeSite({ publishStatus: 'pending' });
  const { directory: ready } = builtDirectory(t);
  packageBuild({ directory: ready });
  assert.equal((await push({ directory: ready, client: held.client })).waits, 'the upload package waits for the owner on /admin/videos');
});

test('what the site is told about a highlight and about a cut of another version', () => {
  const body = projectBody({ doc: cut(), qa: { ok: true }, check: { ok: true }, report: null });
  assert.deepEqual([body.format, body.shorts_line, body.shorts_series, body.source_slug, body.stage], ['shorts', 'cut', 'ai-model-choice', 'ai-model-choice', 'final']);
  assert.equal(projectBody({ doc: cut(), qa: null, check: null, report: null, stage: 'publish' }).stage, 'publish');
  assert.equal(projectBody({ doc: { ...cut(), line: 'drama' }, qa: null, check: null, report: null }).format, 'drama', 'a vertical drama short keeps the drama format');
  const timeline = { seconds: 35.02 };
  const stale = finalReview({ doc: script(), qa: { ok: true, final_sha256: 'a'.repeat(64), kind: 'shorts', items: [] }, usage: null, timeline, finalSha256: 'b'.repeat(64) });
  assert.ok(!('qa' in stale.payload) && !('usage' in stale.payload), 'a report of another cut is not sent');
  assert.equal(stale.summary, 'Shorts 35.0 秒，Shorts 自動品管沒有結果');
  const failed = publishReview({ metadata: composeMetadata({ doc: script(), finalSha256: 'f', seconds: 35 }), report: { ok: false, kind: 'shorts', final_sha256: 'm', items: [{ id: 'captions', ok: false }], checked_at: 'x' }, metadataSha256: 'm' });
  assert.deepEqual([failed.summary, 'checked_at' in failed.payload.package], ['Shorts 上傳包 1 項沒過：captions', false]);
  assert.equal(evidenceRole('experiments/raw outputs/plain.json'), 'evidence_experiments_raw_outputs_plain');
  assert.ok(evidenceRole(`deep/${'x'.repeat(80)}.txt`).length <= 40);
  assert.match(evidenceRole('圖片/海報.png'), /^evidence_[A-Za-z0-9_-]*$/);
});

// --- a cut made elsewhere ------------------------------------------------------------------------

test('a finished cut\'s captions become its narration and its timeline', () => {
  const cues = parseSrt(Array.from({ length: 10 }, (_x, i) => `${i + 1}\n00:00:${String(i * 3).padStart(2, '0')},000 --> 00:00:${String(i * 3 + 3).padStart(2, '0')},000\n第 ${i + 1} 句旁白`).join('\n\n'));
  const meta = { slug: 'cut-imported', line: 'cut', series: 'ai-model-choice', titles: ['怎麼挑模型', '挑模型的三件事'], description: '從長片切出來的重點。', source: { slug: 'ai-model-choice' } };
  const doc = scriptFromImport(meta, cues);
  assert.deepEqual(validate(doc), []);
  assert.deepEqual([doc.schema_version, doc.scenes.length, phrasesOf(doc).length], [2, 4, 10]);
  assert.deepEqual(doc.scenes[0], { headline: '第 1 句旁白', narration: ['第 1 句旁白', '第 2 句旁白', '第 3 句旁白'] });
  const named = scriptFromImport({ ...meta, headlines: ['開場', '三件事', '結論'] }, cues);
  assert.deepEqual([named.scenes.map((scene) => scene.headline), named.scenes.map((scene) => scene.narration.length), 'headlines' in named], [['開場', '三件事', '結論'], [4, 4, 2], false]);
  const timeline = timelineFromCaptions(cues, doc.scenes);
  assert.deepEqual([timeline.length, timeline[3].sceneIndex, timeline[3].startFrame, timeline[3].endFrame, timeline[3].frames], [10, 1, 270, 360, 90]);
  assert.deepEqual(captionTimingProblems(cues, 30), []);
  assert.deepEqual(captionTimingProblems(cues, 25), ['the captions run to 30.00s, the cut to 25.00s']);
  assert.deepEqual(captionTimingProblems([{ start: 0, end: 3 }, { start: 2, end: 5 }], 10), ['caption 2 starts before caption 1 ends']);
});

// --- the site ------------------------------------------------------------------------------------

test('the settings are the Shorts\' own, else the channel\'s voice, else the defaults', async () => {
  const seen = [];
  const answers = { 'automation/shorts/settings': () => json({ detail: 'Not Found' }, 404), 'automation/settings': () => json({ voice: { provider: 'gemini', name: 'Kore' }, enabled: false }) };
  const fetchImpl = async (url, init) => {
    seen.push([init.method, url.replace('https://site.test/api/video/', ''), init.headers.Authorization, init.headers.Cookie]);
    return answers[url.replace('https://site.test/api/video/', '')]();
  };
  const client = siteClient({ env, fetch: fetchImpl, sleep: async () => {} });
  assert.deepEqual(await client.settings(), { voice: { provider: 'gemini', name: 'Kore' }, seconds_min: 25, seconds_max: 55, locales: [], made_for_kids: false });
  assert.deepEqual(seen, [['GET', 'automation/shorts/settings', `Bearer ${TOKEN}`, undefined], ['GET', 'automation/settings', `Bearer ${TOKEN}`, undefined]]);
  answers['automation/shorts/settings'] = () => json({ voice: CHANNEL_VOICE, seconds_min: 30, seconds_max: 50, locales: ['en'], made_for_kids: false, paused: false });
  assert.equal((await client.settings()).seconds_min, 30);
  answers['automation/settings'] = () => json({ detail: 'x' }, 404);
  answers['automation/shorts/settings'] = () => json({ detail: 'x' }, 404);
  assert.deepEqual((await client.settings()).voice, CHANNEL_VOICE);
  assert.throws(() => siteClient({ env: {}, home: os.tmpdir(), fetch: fetchImpl }), (error) => error instanceof SiteError && error.who === 'owner');
});

test('a call is tried again when the site is busy, and an owner\'s problem is named as one', async () => {
  let attempts = 0;
  const busy = siteClient({ env, sleep: async () => {}, fetch: async () => (++attempts < 3 ? json({ detail: 'busy' }, 503) : json([{ slug: 'a' }])) });
  assert.deepEqual(await busy.videos({ shorts: 'only' }), [{ slug: 'a' }]);
  assert.equal(attempts, 3);
  const refused = siteClient({ env, sleep: async () => {}, fetch: async () => json({ code: 'video_tool_token_invalid', detail: '權杖已撤銷' }, 401) });
  await assert.rejects(refused.videos(), (error) => error.who === 'owner' && error.status === 401 && error.message === '權杖已撤銷');
  const invalid = siteClient({ env, sleep: async () => {}, fetch: async () => json({ code: 'video_review_files_missing', detail: '檔案還沒上傳完' }, 409) });
  await assert.rejects(invalid.submit('x', {}), (error) => error.who === 'service' && error.code === 'video_review_files_missing');
  const asked = [];
  const listing = siteClient({ env, fetch: async (url) => (asked.push(url), json([])) });
  await listing.videos({ shorts: 'exclude', limit: '5' });
  assert.deepEqual(asked, ['https://site.test/api/video/automation/videos?shorts=exclude&limit=5']);
});

test('the worker\'s knock does what is due, and is quiet on a site that has no calendar yet', async (t) => {
  const printed = [];
  t.mock.method(console, 'log', (line) => printed.push(line));
  const asked = [];
  const answer = { status: 200, body: { locked: 1, sent: 0, snapshots: 2 } };
  const fetchImpl = async (url, init) => {
    asked.push([init.method, url]);
    return json(answer.body, answer.status);
  };
  assert.equal(await main(['tick'], { env, fetch: fetchImpl }), 0);
  assert.deepEqual(asked, [['POST', 'https://site.test/api/video/automation/shorts/tick']]);
  assert.deepEqual(JSON.parse(printed[0]), { locked: 1, sent: 0, snapshots: 2 });
  Object.assign(answer, { status: 404, body: { detail: 'Not Found' } });
  assert.equal(await main(['tick'], { env, fetch: fetchImpl }), 0);
  assert.match(printed[1], /no Shorts calendar yet/);
  await assert.rejects(main(['tick'], { env: {}, home: os.tmpdir(), fetch: fetchImpl }), /no video tool token/);
  await assert.rejects(main(['publish']), /unknown command publish/);
});


test('translated captions keep every timestamp while allowing different text', () => {
  const timeline = buildTimeline(script(), phrasesOf(script()).map(() => 3));
  const chinese = srt(timeline);
  for (const locale of ['en', 'ja', 'ko', 'zh-CN']) {
    const translated = srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translated line' })) });
    const captions = new Map([['zh-TW', chinese], [locale, translated]]);
    assert.equal(captionsItem({ captions, timeline, locales: [locale] }).ok, true);
    for (const shifted of [
      translated.replace('00:00:00,000', '00:00:00,500'),
      srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translated line', startFrame: cue.startFrame + 1800, endFrame: cue.endFrame + 1800 })) }),
    ]) {
      const result = captionsItem({ captions: new Map([['zh-TW', chinese], [locale, shifted]]), timeline, locales: [locale] });
      assert.equal(result.ok, false, locale);
      assert.match(result.detail, /off the timeline/);
    }
  }
});

test('selected translated captions must be current in the upload package', (t) => {
  const { directory } = builtDirectory(t);
  const timeline = JSON.parse(readFileSync(path.join(directory, 'timeline.json'), 'utf8'));
  const settings = { locales: ['en'] };
  const missing = packageBuild({ directory, settings });
  assert.equal(missing.report.ok, false);
  assert.match(missing.report.items.find((each) => each.id === 'captions').detail, /en.srt is missing/);
  const translated = srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translation' })) });
  writeFileSync(path.join(directory, 'upload', 'en.srt'), translated.replace('00:00:00,000', '00:00:00,500'));
  const stale = packageBuild({ directory, settings });
  assert.equal(stale.report.ok, false);
  assert.match(stale.report.items.find((each) => each.id === 'captions').detail, /off the timeline/);
  writeFileSync(path.join(directory, 'upload', 'en.srt'), translated);
  const current = packageBuild({ directory, settings });
  assert.equal(current.report.ok, true);
  assert.deepEqual(current.metadata.locales, ['en']);
  const manifest = JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8'));
  assert.ok(manifest.files.some((file) => file.name === 'en.srt'));
});

test('push includes exactly the selected translated caption roles for server upload', async (t) => {
  const { directory } = builtDirectory(t);
  const timeline = JSON.parse(readFileSync(path.join(directory, 'timeline.json'), 'utf8'));
  const translated = srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translation' })) });
  for (const locale of ['en', 'ja', 'ko', 'zh-CN']) writeFileSync(path.join(directory, 'upload', locale + '.srt'), translated);
  packageBuild({ directory, settings: { locales: ['en', 'zh-CN'] } });
  const { client, calls } = fakeSite();
  const result = await push({ directory, client });
  assert.equal(result.publish.status, 'approved');
  const review = calls.filter(([kind]) => kind === 'submit').map(([, , value]) => value).find((value) => value.gate === 'publish');
  assert.deepEqual(review.payload.locales, ['zh-TW', 'en', 'zh-CN']);
  assert.deepEqual(review.files.filter((file) => file.role.startsWith('captions_')).map((file) => file.role), ['captions_zh-TW', 'captions_en', 'captions_zh-CN']);
  assert.ok(!review.files.some((file) => file.role === 'thumbnail'));
});

test('a package settings failure preserves the preceding files and returns failure', async (t) => {
  const { directory, timeline } = builtDirectory(t);
  writeFileSync(path.join(directory, 'upload', 'en.srt'), srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translation' })) }));
  packageBuild({ directory, settings: { locales: ['en'], made_for_kids: true } });
  const names = ['upload/metadata.json', 'upload/description.zh-TW.txt', 'upload/manifest.json', 'package.json'];
  const previous = names.map((name) => readFileSync(path.join(directory, name), 'utf8'));
  let requests = 0;
  await assert.rejects(main(['package', '--dir', directory], {
    env,
    fetch: async () => {
      requests++;
      return new Response(JSON.stringify({ detail: 'settings unavailable' }), { status: 503, headers: { 'content-type': 'application/json', 'retry-after': '0.001' } });
    },
  }), (error) => error instanceof SiteError && error.status === 503);
  assert.equal(requests, 4);
  assert.deepEqual(names.map((name) => readFileSync(path.join(directory, name), 'utf8')), previous);
});

for (const change of ['clock', 'text']) {
  test(`changed translated caption ${change} cannot reuse an approved package hash`, async (t) => {
    const { directory, timeline } = builtDirectory(t);
    const captions = srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translation' })) });
    const captionFile = path.join(directory, 'upload', 'en.srt');
    writeFileSync(captionFile, captions);
    packageBuild({ directory, settings: { locales: ['en'] } });
    const initial = fakeSite();
    assert.equal((await push({ directory, client: initial.client })).publish.status, 'approved');
    const oldSha = sha256(readFileSync(path.join(directory, 'upload', 'metadata.json')));
    const changed = change === 'clock' ? captions.replace('00:00:00,000', '00:00:00,500') : captions.replaceAll('Translation', 'Corrected translation');
    writeFileSync(captionFile, changed);
    const stale = fakeSite();
    const result = await push({ directory, client: stale.client });
    assert.equal(result.publish, null);
    assert.match(result.waits, /captions.*package again/);
    assert.deepEqual(stale.calls, [], 'reject before uploads or an idempotent approved review can be reused');
    assert.equal(sha256(readFileSync(path.join(directory, 'upload', 'metadata.json'))), oldSha);
    if (change === 'text') {
      const repackaged = packageBuild({ directory, settings: { locales: ['en'] } });
      assert.equal(repackaged.report.ok, true);
      assert.notEqual(repackaged.report.final_sha256, oldSha, 'new caption bytes create a new approval identity');
      const fresh = fakeSite();
      assert.equal((await push({ directory, client: fresh.client })).publish.status, 'approved');
      const review = fresh.calls.filter(([kind]) => kind === 'submit').map(([, , value]) => value).find((value) => value.gate === 'publish');
      assert.equal(review.content_sha256, repackaged.report.final_sha256);
      assert.equal(review.files.find((file) => file.role === 'captions_en').sha256, sha256(changed));
    }
  });
}

test('a legacy package without caption bindings must be repackaged', async (t) => {
  const { directory } = builtDirectory(t);
  const { metadata, report } = packageBuild({ directory });
  delete metadata.captions_sha256;
  const bytes = JSON.stringify(metadata);
  writeFileSync(path.join(directory, 'upload', 'metadata.json'), bytes);
  writeFileSync(path.join(directory, 'package.json'), JSON.stringify({ ...report, final_sha256: sha256(bytes) }));
  const legacy = fakeSite();
  const result = await push({ directory, client: legacy.client });
  assert.equal(result.publish, null);
  assert.match(result.waits, /captions.*package again/);
  assert.deepEqual(legacy.calls, []);
});

for (const changedFile of ['metadata.json', 'en.srt']) {
  test(`${changedFile} changing during push cannot create a publish review`, async (t) => {
    const { directory, timeline } = builtDirectory(t);
    writeFileSync(path.join(directory, 'upload', 'en.srt'), srt({ ...timeline, cues: timeline.cues.map((cue) => ({ ...cue, text: 'Translation' })) }));
    packageBuild({ directory, settings: { locales: ['en'] } });
    const { client, calls } = fakeSite();
    const submit = client.submit;
    client.submit = async (slug, review) => {
      const answer = await submit(slug, review);
      if (review.gate === 'final') {
        const file = path.join(directory, 'upload', changedFile);
        const before = readFileSync(file, 'utf8');
        writeFileSync(file, changedFile === 'en.srt' ? before.replaceAll('Translation', 'Edited during push') : before + ' ');
      }
      return answer;
    };
    const result = await push({ directory, client });
    assert.equal(result.publish, null);
    assert.match(result.waits, /changed during push/);
    assert.deepEqual(calls.filter(([kind]) => kind === 'submit').map(([, , review]) => review.gate), ['final']);
  });
}
