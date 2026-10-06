// The experiments line as the host worker makes it (lab.mjs): the spec frozen before any run, the
// tested model asked once under each condition and every request kept, numbers scored by the
// program, a script written from the evidence alone and checked in another conversation, then the
// Short built, heard, checked, packaged and pushed. Nothing here touches a service: the site and
// every model are a fake fetch, the narration is generated tones, and ffprobe's measurement is
// handed in.
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { automationClient } from '../automation/client.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { checkAudio } from './check.mjs';
import { PROFILE, buildTimeline, phrasesOf, sha256, srt, verifyEvidence } from './core.mjs';
import {
  LAB_DIR, LAB_FILE, LabShort, PROTOCOL_FILE, SCORES_FILE, answerFile, followsUp, freezeProtocol, htmlOf, keyProblems,
  labRefusal, labScript, normalNumber, normalTime, numbersIn, scoreAnswers, scriptProblems, specOf, subjectPrompt,
} from './lab.mjs';
import { packageBuild } from './package.mjs';
import { SHORTS_INSTRUCTIONS, SKILL_COPIES, shortsInstructions } from './prompts.mjs';
import { push } from './push.mjs';
import { runQa } from './qa.mjs';
import { siteClient } from './site.mjs';

const REPO = fileURLToPath(new URL('../../../', import.meta.url));
const SITE = 'https://site.test';
const TOKEN = `mkv_${'a'.repeat(43)}`;
const env = { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
const temp = (t) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'shorts-lab-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};
const tone = (seconds, pitch = 440) => {
  const samples = new Int16Array(Math.round(48_000 * seconds));
  for (let i = 0; i < samples.length; i++) samples[i] = Math.round(Math.sin((2 * Math.PI * pitch * i) / 48_000) * 8000);
  return encodeWav(samples);
};

// The campaign's first experiment, as the server's make job carries it.
const TOPIC = Object.freeze({
  slug: 'shorts-receipt-total',
  line: 'lab',
  series: 'daily',
  title: '收據總額',
  hook: 'AI 算得出這張收據嗎？',
  status: 'making',
  brief: {
    test_protocol: {
      setup: '自製虛構收據，輸入純文字。',
      input: '湯 85 元 × 2、茶 45 元 × 3、折扣 −30 元、收據印刷合計 300 元。',
      condition_a: '核對這張收據，告訴我正確總額與印刷合計是否正確。',
      condition_b: '相同輸入與問題，另加：先自行核對算式與限制，再提供簡短驗算。',
      runs: '每組一次、全新對話。',
      scoring: '各組兩項：總額 275 元、辨認印刷合計多算 25 元；兩項皆符才算答對。',
      failure_path: '任一組失敗或輸出不完整照實保留。',
    },
    truth_check: ['85 × 2 + 45 × 3 − 30 = 275；300 − 275 = 25', '若兩組皆正確，結論只說這次都算對'],
    acceptance: ['原始兩組回答有留存'],
    requires: [],
  },
});
const JOB = Object.freeze({ topic: TOPIC, line: 'lab', project_slug: null, resume: false, channel_stance: '只寫做過的事。', seconds_min: 10, seconds_max: 55, slot: { id: 'slot-1' } });
const KEY = [
  { id: 'q1', question: '正確總額', kind: 'number', expected: '275', source: '85 × 2 + 45 × 3 − 30 = 275' },
  { id: 'q2', question: '印刷合計多算多少', kind: 'number', expected: '25', source: '300 − 275 = 25' },
];
const ANSWER_A = '正確總額是 275 元；印刷合計 300 元多算了 25 元。';
const ANSWER_B = '驗算：85×2=170，45×3=135，170+135−30=275。總額 275 元，印刷合計多算 25 元。';
const READ = {
  a: [{ id: 'q1', quote: '正確總額是 275 元', value: '275' }, { id: 'q2', quote: '多算了 25 元', value: '25' }],
  b: [{ id: 'q1', quote: '總額 275 元', value: '275' }, { id: 'q2', quote: '多算 25 元', value: '25' }],
};
const SCRIPT = {
  titles: ['AI 算得出這張收據嗎？', '一張收據，兩種問法'],
  description: '同一張收據，兩種問法各問一次。',
  experiment_summary: '同一個模型、兩種問法、各問一次，對照先寫好的答案。',
  limitations: '只有一題、各一次，不能代表模型整體的能力。',
  hashtags: ['AI', '實測'],
  scenes: [
    { headline: 'AI 算得出總額嗎？', narration: ['一張自己做的收據', '我們請 AI 核對總額'] },
    { headline: '題目長這樣', body: ['湯 85 元 × 2', '茶 45 元 × 3', '折扣 30 元'], narration: ['湯兩碗，茶三杯', '再扣掉三十元的折扣'] },
    { headline: '先寫好的答案', big: '275', note: '印刷合計 300 元多算 25 元', narration: ['答案是兩百七十五元'] },
    { headline: '兩種問法都算對', body: ['A：275 元', 'B：275 元'], narration: ['兩種問法都答對', '這一題打成平手'] },
    { headline: '這次能說什麼', note: '只測一題、各一次', narration: ['一題不能代表全部'] },
  ],
};

/** The site and every model: answers by stage and variant, reviews kept, what was sent recorded. */
function fakeSite({ answers = {}, finalStatus = 'approved' } = {}) {
  const calls = { run: [], reports: [], reviews: [], done: [], policy: 0 };
  const reviews = new Map();
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    if (/^\/api\/video\/reviews\/[a-z0-9-]+\/files\/[0-9a-f]{64}$/.test(pathname)) return json({ received: [0], complete: true });
    const body = typeof init.body === 'string' ? JSON.parse(init.body) : null;
    if (pathname === '/api/video/automation/run') {
      calls.run.push(body);
      const reply = answers[`${body.stage}:${body.variant}`];
      const value = typeof reply === 'function' ? reply(body, calls) : reply;
      if (value instanceof Response) return value;
      if (value === undefined) return json({ code: 'not_found', detail: `no answer for ${body.stage}:${body.variant}` }, 404);
      const text = typeof value === 'string' ? value : JSON.stringify(value);
      return json({ text, provider: 'claude_code', model: body.stage === 'subject' ? `model-${body.variant}` : 'claude-checker', input_tokens: 100, output_tokens: 50, usage: { tokens: 150, token_budget: 20_000_000 } });
    }
    if (pathname === '/api/video/automation/shorts/settings') return json({ enabled: true, voice: { provider: 'gemini', name: 'Sulafat' }, seconds_min: 10, seconds_max: 55, locales: [], made_for_kids: false });
    if (pathname === '/api/video/automation/judge/policy') {
      calls.policy++;
      return json({ passed: true, note: 'Jev 照頻道立場讀過，可以上' });
    }
    const done = /^\/api\/video\/automation\/shorts\/([a-z0-9-]+)\/done$/.exec(pathname);
    if (done) {
      calls.done.push({ topic: done[1], ...body });
      return json({ slug: done[1], status: 'made' });
    }
    const review = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (review) {
      const [, slug, sub] = review;
      const list = reviews.get(slug) ?? [];
      reviews.set(slug, list);
      if (init.method === 'PUT') {
        calls.reports.push({ slug, ...body });
        return json({ slug, reviews: list });
      }
      if (sub && init.method === 'POST') {
        const same = list.find((each) => each.gate === body.gate && each.content_sha256 === body.content_sha256);
        if (same) return json(same);
        const made = { id: `r${list.length + 1}`, status: body.gate === 'final' ? finalStatus : 'approved', note: null, ...body };
        list.unshift(made);
        calls.reviews.push(made);
        return json(made);
      }
      return json({ slug, reviews: list });
    }
    return json({ code: 'not_found', detail: pathname }, 404);
  };
  return { calls, reviews, fetchImpl };
}

const ANSWERS = () => ({
  'verifier:shorts-lab-key': { items: KEY },
  'subject:a': ANSWER_A,
  'subject:b': ANSWER_B,
  'verifier:shorts-lab-score': READ,
  'writer:shorts-lab': { script: SCRIPT },
  'verifier:shorts-lab': { ok: true, claims: [{ text: '兩種問法都算出 275 元', ok: true, evidence: 'scores' }], problems: [] },
});

/**
 * A build without a browser or ffmpeg: the script and its evidence copied, a generated tone for
 * every phrase, the timeline, the captions and a stand-in cut. `tooLong` makes the first build
 * refuse the narration's length, as build.mjs does.
 */
function fakeTools({ tooLong = false, flagOnce = false } = {}) {
  const builds = [];
  let heardOnce = false;
  const build = async ({ file, sourceBase, workdir, speech, redo }) => {
    const bytes = readFileSync(file);
    const doc = JSON.parse(bytes);
    const evidence = verifyEvidence(doc, sourceBase);
    builds.push({ speech, redo, scenes: doc.scenes.length });
    if (tooLong && builds.length === 1) throw new Error('narration is 71.20s; edit script to fit 10–55s (never truncate speech)');
    const directory = path.join(workdir, doc.slug, `build-${builds.length}`);
    for (const sub of ['audio', 'upload', 'evidence']) mkdirSync(path.join(directory, sub), { recursive: true });
    writeFileSync(path.join(directory, 'script.json'), bytes);
    for (const item of evidence) writeFileSync(path.join(directory, 'evidence', item.path), item.bytes);
    const phrases = phrasesOf(doc);
    phrases.forEach((_phrase, index) => writeFileSync(path.join(directory, 'audio', `${String(index).padStart(3, '0')}.wav`), tone(1.5, 400 + index * 10)));
    const timeline = buildTimeline(doc, phrases.map(() => 1.5), { minSeconds: 10, maxSeconds: 55 });
    writeFileSync(path.join(directory, 'timeline.json'), JSON.stringify(timeline));
    writeFileSync(path.join(directory, 'checks.json'), JSON.stringify({ ok: true, layout: timeline.cues.map((cue) => ({ cue: cue.index, problems: [] })) }));
    writeFileSync(path.join(directory, 'upload', 'final.mp4'), Buffer.from(`a stand-in cut of ${doc.slug}, build ${builds.length}`));
    writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), srt(timeline));
    writeFileSync(path.join(directory, 'upload', 'cover.png'), Buffer.from('cover'));
    writeFileSync(path.join(directory, 'usage.json'), JSON.stringify({ narration: { seconds: timeline.seconds, characters: 40, calls: phrases.length, provider: 'gemini' }, stages: {}, checks: {} }));
    return { directory, seconds: timeline.seconds };
  };
  const heard = async (args) => {
    const phrases = phrasesOf(JSON.parse(readFileSync(path.join(args.directory, 'script.json'), 'utf8')));
    let index = 0;
    return checkAudio({
      ...args,
      // The first check of a flagOnce run hears the second phrase wrong; Jev doubts it.
      transcribeImpl: async () => {
        const said = phrases[index];
        index++;
        if (flagOnce && !heardOnce && index === 2) {
          heardOnce = true;
          return '完全不同的一句話';
        }
        return said;
      },
      judgeImpl: async ({ lines }) => new Map(lines.map((line) => [line.id, 0.1])),
    });
  };
  const measured = async (final) => {
    const timeline = JSON.parse(readFileSync(path.join(path.dirname(path.dirname(final)), 'timeline.json'), 'utf8'));
    return {
      video: { width: PROFILE.width, height: PROFILE.height, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: String(timeline.frames) },
      audio: { codec_name: 'aac', sample_rate: '48000', duration: String(timeline.seconds) },
      format: {},
      loudness: { input_i: '-14.1', input_tp: '-1.5' },
      grammar: { cover_psnr: Infinity, loop_psnr: 48.1 },
    };
  };
  const qa = (args) => runQa({ ...args, measureImpl: measured, tools: {}, linkCheck: async (url) => ({ url, ok: true, status: 200 }), history: [] });
  return { builds, tools: { build, checkAudio: heard, runQa: qa, packageBuild, push } };
}

function labFor(t, site, { tools, base = temp(t), job = JOB, settings = { max_verify_rounds: 3 }, slug = 'shorts-receipt-total' } = {}) {
  const clock = { now: Date.parse('2026-10-05T01:00:00Z') };
  const out = [];
  const ctx = { env, home: base, fetch: site.fetchImpl, sleep: async () => {}, now: () => new Date((clock.now += 1000)), stdout: { write: (text) => out.push(text) } };
  const api = automationClient(ctx);
  const lab = new LabShort({ ctx, api, subjectApi: automationClient(ctx, { attempts: 1 }), site: siteClient({ env, home: base, fetch: site.fetchImpl, sleep: async () => {} }), job, slug, base, settings, shortsSettings: { locales: [] }, tools });
  return { lab, base, out, ctx };
}

// --- the pieces ------------------------------------------------------------------------------------

test('numbers are compared as numbers: grouping, leading zeros, full-width digits and clock times', () => {
  assert.deepEqual(numbersIn('總額 1,275 元，09:45 再過 95 分鐘；２７５ 與 45.50'), ['1275', '9', '45', '95', '275', '45.5']);
  assert.equal(normalNumber('0275'), '275');
  assert.equal(normalNumber('2.50'), '2.5');
  assert.equal(normalNumber('abc'), null);
  assert.equal(normalTime('上午 9:05'), '09:05');
  assert.equal(normalTime('11：20'), '11:20');
  assert.equal(normalTime('25:00'), null);
});

test('the answer key must come from the spec word for word, before anything runs', () => {
  const spec = specOf(TOPIC);
  assert.deepEqual(keyProblems(KEY, spec), []);
  assert.ok(keyProblems([{ ...KEY[0], expected: '276' }], spec).some((problem) => problem.includes('276 is not in its source')), 'an answer the spec does not give');
  assert.ok(keyProblems([{ ...KEY[0], source: '總額應為 275' }], spec).some((problem) => problem.includes('word for word')), 'a source the spec does not have');
  assert.ok(keyProblems([], spec).length, 'an empty key');
  assert.ok(keyProblems([KEY[0], KEY[0]], spec).some((problem) => problem.includes('once each')));
  const time = { ...TOPIC, brief: { ...TOPIC.brief, truth_check: ['09:45 + 60 分鐘 + 35 分鐘 = 11:20'] } };
  assert.deepEqual(keyProblems([{ id: 'q1', question: '時間', kind: 'time', expected: '11:20', source: '09:45 + 60 分鐘 + 35 分鐘 = 11:20' }], specOf(time)), []);
});

test('the protocol freezes the requests: the input and the question, never the answers', () => {
  const protocol = freezeProtocol({ topic: TOPIC, slug: 'shorts-receipt-total', key: KEY, now: new Date('2026-10-05T01:00:00Z') });
  assert.equal(protocol.subject.a.instructions, `${TOPIC.brief.test_protocol.input}\n\n${TOPIC.brief.test_protocol.condition_a}`);
  assert.equal(protocol.subject.b.instructions, `${TOPIC.brief.test_protocol.input}\n\n${TOPIC.brief.test_protocol.condition_b}`);
  for (const variant of ['a', 'b']) assert.doesNotMatch(protocol.subject[variant].instructions, /275|25 元/, 'the tested model never sees the answer');
  assert.deepEqual(protocol.answer_key.map((item) => item.expected), ['275', '25']);
  assert.equal(protocol.rules.attempts, 2);
  // A second question asked in the same conversation (the self-check experiment) follows a's answer.
  const self = { ...TOPIC, brief: { ...TOPIC.brief, test_protocol: { ...TOPIC.brief.test_protocol, condition_b: '在同一個context追加：請逐題核對你的答案。' } } };
  assert.equal(followsUp(specOf(self)), true);
  assert.equal(subjectPrompt(specOf(self), 'b'), subjectPrompt(specOf(self), 'a'));
  assert.equal(freezeProtocol({ topic: self, slug: 's', key: KEY, now: new Date() }).subject.b.follows, 'a');
});

test('the program scores numbers against the key; a wrong answer is a result, a quote that is not there is not', () => {
  const answers = { a: ANSWER_A, b: '總額 300 元，沒有問題。' };
  const read = { a: READ.a, b: [{ id: 'q1', quote: '總額 300 元', value: '300' }, { id: 'q2', quote: '', value: null }] };
  const scores = scoreAnswers({ key: KEY, answers, read });
  assert.deepEqual(scores.problems, []);
  assert.deepEqual(scores.totals, { a: 2, b: 0 });
  assert.equal(scores.tie, false);
  assert.equal(scores.items[0].b.value, '300');
  assert.equal(scores.items[0].b.by, 'program');
  assert.equal(scores.items[1].b.note, '回答裡沒有這一題的答案');
  // The checker may not put words in the model's mouth, nor a number its quote does not have.
  const invented = scoreAnswers({ key: KEY, answers, read: { a: [{ id: 'q1', quote: '總額 275 元整', value: '275' }, READ.a[1]], b: read.b } });
  assert.ok(invented.problems.some((problem) => problem.includes('not in the answer')));
  const misread = scoreAnswers({ key: KEY, answers, read: { a: [{ id: 'q1', quote: '正確總額是 275 元', value: '300' }, READ.a[1]], b: read.b } });
  assert.ok(misread.problems.some((problem) => problem.includes('not in its quote')));
  // No answer at all under a condition: every item fails, which is a result.
  const missing = scoreAnswers({ key: KEY, answers: { a: ANSWER_A, b: null }, read: { a: READ.a } });
  assert.deepEqual([missing.problems, missing.totals], [[], { a: 2, b: 0 }]);
});

test('the script may only say numbers the evidence has, and show only a quiet HTML answer', () => {
  const evidence = [{ path: 'protocol.json', sha256: 'a'.repeat(64) }];
  const doc = labScript({ script: { ...SCRIPT, slug: 'other', series: 'blind', line: 'cut', format: 'x' } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.deepEqual([doc.slug, doc.series, doc.line, doc.format, doc.schema_version], ['shorts-receipt-total', 'daily', 'lab', 'shorts', 2], 'the worker owns these');
  const evidenceText = JSON.stringify({ input: TOPIC.brief.test_protocol.input, truth: TOPIC.brief.truth_check, a: ANSWER_A });
  assert.deepEqual(scriptProblems(doc, { evidenceText }), []);
  const boast = labScript({ script: { ...SCRIPT, scenes: [...SCRIPT.scenes.slice(0, 4), { headline: '準確率 99%', narration: ['一題不能代表全部'] }] } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.ok(scriptProblems(boast, { evidenceText }).some((problem) => problem.includes('99 is not in the protocol')));
  const shown = labScript({ script: { ...SCRIPT, scenes: [...SCRIPT.scenes.slice(0, 4), { ...SCRIPT.scenes[4], asset: 'subject-a.json' }] } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.ok(scriptProblems(shown, { evidenceText }).some((problem) => problem.includes('asset may only be an HTML answer')));
  // The six beats travel with the script, and the grammar the quality check holds the cut to is
  // refused here first: a call to action, a first card too long for a thumbnail.
  const beaten = labScript({ script: { ...SCRIPT, scenes: SCRIPT.scenes.map((scene, index) => ({ ...scene, beat: ['hook', 'setup', 'turn', 'proof', 'payoff'][index] })) } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.deepEqual(beaten.scenes.map((scene) => scene.beat), ['hook', 'setup', 'turn', 'proof', 'payoff'], 'the writer\'s beats travel with the script');
  assert.deepEqual(scriptProblems(beaten, { evidenceText }), []);
  const backwards = labScript({ script: { ...SCRIPT, scenes: SCRIPT.scenes.map((scene, index) => ({ ...scene, beat: ['hook', 'proof', 'setup', 'payoff', 'loop'][index] })) } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.ok(scriptProblems(backwards, { evidenceText }).some((problem) => problem.includes('scene 2: beat setup comes after proof')));
  const asking = labScript({ script: { ...SCRIPT, scenes: [...SCRIPT.scenes.slice(0, 4), { ...SCRIPT.scenes[4], narration: ['一題不能代表全部', '記得訂閱頻道'] }] } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.ok(scriptProblems(asking, { evidenceText }).some((problem) => problem.includes('scene 4 narration asks the viewer to act (記得訂閱)')));
  const wide = labScript({ script: { ...SCRIPT, scenes: [{ ...SCRIPT.scenes[0], headline: 'AI 到底算不算得出這張收據的總額' }, ...SCRIPT.scenes.slice(1)] } }, { slug: 'shorts-receipt-total', series: 'daily', evidence });
  assert.ok(scriptProblems(wide, { evidenceText }).some((problem) => problem.includes('the first card is the thumbnail: its headline is 17 characters')));
  assert.deepEqual(htmlOf('海報：\n```html\n<html><body><div>夜市</div></body></html>\n```'), { html: '<html><body><div>夜市</div></body></html>', usable: true });
  assert.equal(htmlOf('<html><body><script>alert(1)</script></body></html>').usable, false);
  assert.equal(htmlOf('<html><body><img src="https://example.com/a.png"></body></html>').usable, false);
  assert.equal(htmlOf('只有文字的回答'), null);
});

test('the topics a text-only worker cannot make wait for what they need', () => {
  assert.equal(labRefusal(TOPIC), null);
  assert.match(labRefusal({ ...TOPIC, slug: 'shorts-boba-game', brief: { requires: ['sandbox'] } }), /隔離的執行環境/);
  assert.match(labRefusal({ ...TOPIC, brief: { requires: ['image_generation'] } }), /生圖/);
  assert.match(labRefusal({ ...TOPIC, line: 'cut' }), /不是實測線/);
});

test('the prompts are the originals, the skill keeps the same texts, and the report computes nothing', () => {
  const base = path.join(REPO, '.agents', 'skills', 'youtube-video', 'references', 'prompts');
  const copied = [];
  for (const [file, keys] of Object.entries(SKILL_COPIES)) {
    const text = readFileSync(path.join(base, file), 'utf8');
    const blocks = [...text.matchAll(/^## `([a-z:-]+)`\n\n```text\n([\s\S]*?)\n```$/gm)].map((match) => [match[1], match[2]]);
    assert.deepEqual(blocks.map(([key]) => key), keys, `${file} holds its prompts in order`);
    for (const [key, body] of blocks) assert.equal(body, SHORTS_INSTRUCTIONS[key], `${file}: ${key} is the original word for word`);
    copied.push(...keys);
  }
  assert.deepEqual(copied.sort(), Object.keys(SHORTS_INSTRUCTIONS).sort(), 'every prompt has its copy');
  const report = SHORTS_INSTRUCTIONS['planner:shorts-report'];
  assert.match(report, /Do not output any score, rank, ranking, average, median, sum, ratio, growth rate or percentage\s+you computed yourself/);
  assert.match(report, /a check refuses any other number/);
  assert.match(SHORTS_INSTRUCTIONS['writer:shorts-lab'], /tie \(平手\)/);
  assert.match(SHORTS_INSTRUCTIONS['writer:shorts-lab'], /Six beats in this order, every scene naming its "beat"/);
  assert.match(SHORTS_INSTRUCTIONS['writer:shorts-lab'], /The first card is the thumbnail: its headline at most 14 characters/);
  assert.match(SHORTS_INSTRUCTIONS['writer:shorts-lab'], /No call to action anywhere/);
  assert.match(shortsInstructions('writer', 'shorts-lab', '只寫做過的事。'), /## The channel's stance\n只寫做過的事。$/);
  assert.doesNotMatch(shortsInstructions('verifier', 'shorts-lab', '只寫做過的事。'), /stance/i, 'the checker reads the evidence, not the stance');
  assert.throws(() => shortsInstructions('writer', 'shorts-cut'), /no Shorts prompt/);
});

// --- one Short, start to finish --------------------------------------------------------------------

test('an experiment goes from its frozen spec to the site, every step on its evidence', async (t) => {
  const site = fakeSite({ answers: ANSWERS() });
  const { builds, tools } = fakeTools({ tooLong: true, flagOnce: true });
  const { lab, base } = labFor(t, site, { tools });
  const line = await lab.run();
  assert.match(line, /protocol frozen \(2 answers in the key, sha256 [0-9a-f]{12}\)/);
  assert.match(line, /the tested model answered under a \(model-a, 1 request\)/);
  assert.match(line, /scored: a 2\/2, b 2\/2 \(a tie\)/);
  assert.match(line, /length: back to the writer \(fix round 1 of 2\)/);
  assert.match(line, /1 phrases flagged; synthesized again/);
  assert.match(line, /quality check: all 13 items pass/);
  assert.match(line, /pushed: final approved, upload package approved/);
  assert.equal(lab.state.status, 'done');

  const labDir = path.join(base, 'shorts-receipt-total', LAB_DIR);
  const protocolBytes = readFileSync(path.join(labDir, PROTOCOL_FILE));
  assert.equal(lab.state.protocol_sha256, sha256(protocolBytes), 'the hash recorded is the file that was used');
  const a = JSON.parse(readFileSync(path.join(labDir, answerFile('a')), 'utf8'));
  assert.deepEqual([a.raw, a.model, a.provider, a.conversation, a.retries, a.attempts.length], [ANSWER_A, 'model-a', 'claude_code', 'fresh', 0, 1]);
  assert.equal(a.protocol_sha256, lab.state.protocol_sha256);
  const scores = JSON.parse(readFileSync(path.join(labDir, SCORES_FILE), 'utf8'));
  assert.deepEqual([scores.totals, scores.tie, scores.items[0].a.by], [{ a: 2, b: 2 }, true, 'program']);

  const stages = site.calls.run.map((call) => `${call.stage}:${call.variant}`);
  assert.deepEqual(stages, [
    'verifier:shorts-lab-key', 'subject:a', 'subject:b', 'verifier:shorts-lab-score',
    'writer:shorts-lab', 'verifier:shorts-lab',
    // The first build found the narration too long: the writer, then the checker again.
    'writer:shorts-lab', 'verifier:shorts-lab',
  ]);
  assert.ok(site.calls.run.every((call) => call.format === 'shorts'), 'every call is filed under Shorts');
  const [subjectA, subjectB] = site.calls.run.filter((call) => call.stage === 'subject');
  assert.equal(subjectA.instructions, `${TOPIC.brief.test_protocol.input}\n\n${TOPIC.brief.test_protocol.condition_a}`);
  assert.deepEqual(subjectA.payload, {});
  assert.doesNotMatch(subjectB.instructions, /275/, 'the answer never reaches the tested model');
  const writer = site.calls.run.find((call) => call.stage === 'writer');
  assert.deepEqual(Object.keys(writer.payload).sort(), ['evidence', 'evidence_files', 'protocol', 'scores', 'seconds', 'series'], 'the writer gets the spec, the evidence and the scores');
  assert.equal(writer.payload.evidence.a.model, 'model-a');
  assert.match(writer.instructions, /## The channel's stance\n只寫做過的事。/);
  const rewrite = site.calls.run.filter((call) => call.stage === 'writer')[1];
  assert.match(rewrite.payload.problems[0], /旁白長度不對：narration is 71\.20s/);
  assert.deepEqual(rewrite.payload.previous_script.scenes, SCRIPT.scenes);

  // The narration check flagged a phrase once: it was synthesized again, the rest from the cache.
  assert.deepEqual(builds.map((each) => [each.speech, each.redo === null ? null : path.basename(each.redo)]), [['server', null], ['server', null], ['server', 'build-2']]);
  const build = lab.state.build;
  assert.equal(path.basename(build), 'build-3');
  assert.deepEqual(JSON.parse(readFileSync(path.join(build, 'verify.json'), 'utf8')).document_sha256, sha256(readFileSync(path.join(labDir, 'script.json'))), 'the check is bound to the script that was built');
  const qa = JSON.parse(readFileSync(path.join(build, 'qa.json'), 'utf8'));
  assert.equal(qa.ok, true, JSON.stringify(qa.items.filter((item) => !item.ok)));

  const [final, publish] = site.calls.reviews;
  assert.equal(final.gate, 'final');
  assert.deepEqual(Object.keys(final.payload.usage.stages).sort(), ['subject/a', 'subject/b', 'verifier/shorts-lab', 'verifier/shorts-lab-key', 'verifier/shorts-lab-score', 'writer/shorts-lab']);
  assert.deepEqual(final.payload.usage.stages['writer/shorts-lab'].calls, 2);
  assert.ok(final.files.some((file) => file.role === 'evidence_protocol'), 'the frozen protocol goes up as evidence');
  assert.ok(final.files.some((file) => file.role === 'evidence_subject-a'));
  assert.ok(final.files.some((file) => file.role === 'evidence_verify'));
  assert.equal(publish.gate, 'publish');
  assert.deepEqual(site.calls.done, [{ topic: 'shorts-receipt-total', outcome: 'made' }]);
  assert.ok(site.calls.reports.every((report) => report.format === 'shorts' && report.shorts_line === 'lab'));
  assert.equal(await lab.run(), null, 'a finished Short does nothing more');
});

test('a technical failure of the tested model is asked once more, and both requests are kept', async (t) => {
  let tries = 0;
  const answers = { ...ANSWERS(), 'subject:a': () => (++tries === 1 ? json({ code: 'video_ai_upstream_failed', detail: '模型服務拒絕了這次請求（HTTP 500）' }, 502) : ANSWER_A) };
  const site = fakeSite({ answers });
  const { lab, base } = labFor(t, site, { tools: { build: async () => { throw new Error('stop here'); } } });
  const first = await lab.run();
  assert.match(first, /the tested model \(a\) failed technically .*asked once more next round/);
  assert.equal(lab.state.phase, 'subject-a');
  assert.equal(lab.state.status, 'active');
  assert.equal(site.calls.run.filter((call) => call.stage === 'subject').length, 1, 'the client does not repeat a request to the tested model on its own');
  await lab.run();
  const a = JSON.parse(readFileSync(path.join(base, 'shorts-receipt-total', LAB_DIR, answerFile('a')), 'utf8'));
  assert.deepEqual(a.attempts.map((attempt) => attempt.ok), [false, true]);
  assert.equal(a.attempts[0].code, 'video_ai_upstream_failed');
  assert.equal(a.retries, 1);
  assert.equal(a.raw, ANSWER_A);
});

test('two technical failures stop the experiment: no raw answer, no conclusion, the owner decides', async (t) => {
  const answers = { ...ANSWERS(), 'subject:a': () => json({ code: 'video_ai_upstream_failed', detail: 'HTTP 500' }, 502) };
  const site = fakeSite({ answers });
  const { lab, base } = labFor(t, site, { tools: {} });
  await lab.run();
  const line = await lab.run();
  assert.match(line, /blocked — 受測模型（a）兩次都技術失敗/);
  const a = JSON.parse(readFileSync(path.join(base, 'shorts-receipt-total', LAB_DIR, answerFile('a')), 'utf8'));
  assert.deepEqual([a.raw, a.attempts.length, a.model], [null, 2, '未回傳']);
  const report = site.calls.reports.at(-1);
  assert.equal(report.stage, 'blocked');
  assert.match(report.checklist[0].label, /^卡住，需要人處理：受測模型/);
  assert.equal(await lab.run(), null, 'a blocked Short is not asked again');
});

test('nothing reaches the tested model while the owner has not chosen one, and that is not an attempt', async (t) => {
  const answers = { ...ANSWERS(), 'subject:a': () => json({ code: 'video_ai_subject_not_chosen', detail: 'Shorts 設定還沒選受測模型' }, 409) };
  const site = fakeSite({ answers });
  const { lab } = labFor(t, site, { tools: {} });
  assert.match(await lab.run(), /waits for the owner at subject-a: Shorts 設定還沒選受測模型/);
  assert.deepEqual(lab.state.attempts.a, []);
  assert.equal(lab.state.status, 'active');
});

test('a writer that gives nothing usable twice in a row blocks the Short, with its answers kept', async (t) => {
  const answers = { ...ANSWERS(), 'writer:shorts-lab': { script: { ...SCRIPT, titles: ['只有一個標題'] } } };
  const site = fakeSite({ answers });
  const { lab, base } = labFor(t, site, { tools: {} });
  assert.match(await lab.run(), /write gave nothing usable \(the script does not pass the lint: two titles/);
  assert.equal(site.calls.run.filter((call) => call.stage === 'writer').length, 2, 'asked again at once with the lint\'s problems');
  assert.match(await lab.run(), /blocked — write failed 2 times in a row/);
  assert.equal(readdirSync(path.join(base, 'shorts-receipt-total', 'answers')).length, 2);
  assert.equal(site.calls.reports.at(-1).stage, 'blocked');
});

test('an answer key the spec does not back is not frozen, and a changed protocol stops everything', async (t) => {
  const site = fakeSite({ answers: { ...ANSWERS(), 'verifier:shorts-lab-key': { items: [{ ...KEY[0], expected: '280' }] } } });
  const { lab, base } = labFor(t, site, { tools: {} });
  assert.match(await lab.run(), /freeze gave nothing usable \(the answer key does not come from the spec: q1: the expected number 280/);
  assert.equal(existsSync(path.join(base, 'shorts-receipt-total', LAB_DIR, PROTOCOL_FILE)), false);

  const honest = fakeSite({ answers: { ...ANSWERS(), 'verifier:shorts-lab-score': () => json({ code: 'video_ai_upstream_busy', detail: 'busy' }, 503) } });
  const second = labFor(t, honest, { tools: {} });
  assert.match(await second.lab.run(), /score is waiting on a service \(busy\)/);
  assert.deepEqual(second.lab.state.failures, {}, 'a service that is down does not count');
  const file = path.join(second.base, 'shorts-receipt-total', LAB_DIR, PROTOCOL_FILE);
  writeFileSync(file, readFileSync(file, 'utf8').replace('275', '276'));
  assert.match(await second.lab.run(), /blocked — protocol\.json 在凍結之後被改過/);
});

test('a STOP file is read between units', async (t) => {
  const site = fakeSite({ answers: ANSWERS() });
  const base = temp(t);
  writeFileSync(path.join(base, 'STOP'), '');
  const { lab } = labFor(t, site, { tools: {}, base });
  assert.equal(await lab.run(), 'STOP found; stopping between units');
  assert.equal(site.calls.run.length, 0);
});

test('a cut that waits for the owner is followed: approved, its upload package goes', async (t) => {
  const site = fakeSite({ answers: ANSWERS(), finalStatus: 'pending' });
  const { tools } = fakeTools();
  const { lab, base } = labFor(t, site, { tools });
  assert.match(await lab.run(), /pushed; the final cut waits for the owner/);
  assert.equal(lab.state.status, 'awaiting');
  assert.deepEqual(site.calls.done, [{ topic: 'shorts-receipt-total', outcome: 'made' }], 'the topic is made: the calendar does not wait for this Short');
  assert.equal(await lab.follow(), null, 'still pending');
  site.reviews.get('shorts-receipt-total').find((review) => review.gate === 'final').status = 'approved';
  const again = new LabShort({ ...lab, job: lab.job, slug: lab.slug, base });
  assert.match(await again.follow(), /pushed: final approved, upload package approved/);
  assert.equal(JSON.parse(readFileSync(path.join(base, 'shorts-receipt-total', LAB_FILE), 'utf8')).status, 'done');
  assert.equal(site.calls.done.length, 1, 'done is said once');
});
