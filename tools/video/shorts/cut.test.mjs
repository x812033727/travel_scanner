// The highlights line as the host worker makes it (cut.mjs): a published tutorial frozen from the
// worker's own checkout, one or two passages chosen once for both of its topics, each told again
// under the Shorts card limits with nothing the tutorial does not say, checked in another
// conversation, then built, heard, checked, packaged and pushed with links back to the full video
// and the article. Nothing here touches a service: the site and every model are a fake fetch, the
// narration is generated tones, and ffprobe's measurement is handed in.
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { automationClient } from '../automation/client.mjs';
import { descriptionUrls } from '../qa/links.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { checkAudio } from './check.mjs';
import { PROFILE, buildTimeline, phrasesOf, sha256, srt, validate, verifyEvidence } from './core.mjs';
import {
  CUT_DIR, CUT_INSTRUCTIONS, CUT_SKILL_FILE, CutShort, PICKS_DIR, SEGMENT_FILE, SOURCE_FILE, cutInstructions, cutProblems, cutRefusal,
  cutScript, latestVerify, longClipKey, ownDescription, seedNarration, segmentFor, segmentProblems, shortsArticleUrl, sourceLines,
} from './cut.mjs';
import { LAB_FILE } from './lab.mjs';
import { composeMetadata, packageBuild } from './package.mjs';
import { push } from './push.mjs';
import { evidenceItem, linksItem, runQa } from './qa.mjs';
import { siteClient } from './site.mjs';
import { phraseKey } from './speech.mjs';

const REPO = fileURLToPath(new URL('../../../', import.meta.url));
const SITE = 'https://site.test';
const TOKEN = `mkv_${'c'.repeat(43)}`;
const env = { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN };
const VOICE = Object.freeze({ provider: 'gemini', name: 'Sulafat' });
const VIDEO_ID = 'dQw4w9WgXcQ';
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
const temp = (t) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'shorts-cut-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};
const tone = (seconds, pitch = 440) => {
  const samples = new Int16Array(Math.round(48_000 * seconds));
  for (let i = 0; i < samples.length; i++) samples[i] = Math.round(Math.sin((2 * Math.PI * pitch * i) / 48_000) * 8000);
  return encodeWav(samples);
};

// A tutorial the worker made: its script, two rounds of fact-check, its claims, its article.
const TUTORIAL = Object.freeze({
  schema_version: 1,
  slug: 'ai-agent-vs-chatbot',
  format: 'slides',
  source_guide: 'ai-agents-explained',
  youtube: { title: 'AI 代理跟聊天機器人差在哪？', description: '一個行程任務看懂。', tags: ['AI代理'] },
  scenes: [
    { id: 'hook', chapter: '會回答，算完成嗎', template: 'title', data: { tag: '2026 年 9 月', title: '會回答，算完成嗎？' }, lines: [
      { id: 'ag001', text: '它說幫你排行程，到底查過資料了嗎？' },
      { id: 'ag002', text: '拿一個週一去博物館的任務，就能看出差別。' },
    ] },
    { id: 'check', chapter: '代理會先查', template: 'bullets', data: { items: ['先查開放時間', '再決定下一步'] }, lines: [
      { id: 'ag010', text: 'AI 代理會先查開放時間，再決定下一步。' },
      { id: 'ag011', text: '聊天機器人只回答你問的那一句。' },
      { id: 'ag012', text: '週一休館的館有 3 間，代理會換掉它們。' },
      { id: 'ag013', text: '這就是代理跟聊天的差別。' },
    ] },
    { id: 'cost', chapter: '代價', template: 'bullets', data: { items: ['每查一次就是一次 API 呼叫'] }, lines: [
      { id: 'ag020', text: '代理每多查一次，就多用一次 API 呼叫。' },
      { id: 'ag021', text: '一個半日行程大約要 12 次查詢。' },
      { id: 'ag022', text: '所以交辦之前，先寫清楚要它查什麼。' },
      { id: 'ag023', text: '一張交辦清單，可以省下一半的查詢。' },
    ] },
  ],
});
const SOURCE = Object.freeze({ slug: TUTORIAL.slug, title: TUTORIAL.youtube.title, format: 'slides', youtube_video_id: VIDEO_ID, youtube_publish_at: '2026-10-01T11:30:00Z', source_guide: 'ai-agents-explained', category: 'ai', series_slug: null, episode_number: null });
const topic = (number) => ({ slug: `ai-agent-vs-chatbot-cut-${number}`, line: 'cut', series: 'ai-agent-vs-chatbot', title: `AI 代理跟聊天機器人差在哪？（精華 ${number}）`, status: 'making', brief: { notes: '從這支已公開的長片挑一段改寫成直式字卡。' }, source_slug: TUTORIAL.slug });
const jobFor = (number, extra = {}) => ({ topic: topic(number), line: 'cut', project_slug: null, resume: false, source: SOURCE, channel_stance: '只寫做過的事。', seconds_min: 10, seconds_max: 55, slot: { id: 'slot-1' }, ...extra });
const SEGMENTS = [
  { line_ids: ['ag010', 'ag011', 'ag012', 'ag013'], point: '代理會先查資料再決定，聊天只回答一句', hook: '週一去博物館', conclusion: '這就是差別', standalone: '用一個任務就講完', estimated_seconds: 30 },
  { line_ids: ['ag020', 'ag021', 'ag022', 'ag023'], point: '代理每查一次都有成本，交辦清單能省一半', hook: '每查一次都要錢', conclusion: '先寫交辦清單', standalone: '只講成本', estimated_seconds: 30 },
];
const LINES = sourceLines(TUTORIAL);
const SCRIPT = {
  titles: ['AI 代理跟聊天機器人差在哪？', '週一去博物館，AI 代理會先查'],
  description: '同一個行程任務，代理會先查開放時間，聊天機器人只回答一句。',
  hashtags: ['AI代理'],
  tags: ['AI代理', '聊天機器人'],
  scenes: [
    { headline: '代理會先查', narration: ['AI 代理會先查開放時間，再決定下一步。'] },
    { headline: '聊天只回答一句', narration: ['聊天機器人只回答你問的那一句。'] },
    { headline: '週一休館 3 間', big: '3', narration: ['週一休館的館有三間，代理會換掉它們。'] },
    { headline: '完整的在長片', narration: ['怎麼交辦給代理，完整的在長片。'] },
  ],
};

/** The worker's checkout and work base: the tutorial's files, its article, its narration clips. */
function workspace(t, { verify = true, video = TUTORIAL } = {}) {
  const work = temp(t);
  const root = path.join(work, 'checkout');
  const dir = path.join(root, 'docs', 'videos', TUTORIAL.slug);
  mkdirSync(dir, { recursive: true });
  if (video) writeFileSync(path.join(dir, 'video.json'), `${JSON.stringify(video, null, 2)}\n`);
  if (verify) {
    writeFileSync(path.join(dir, 'verify-1.md'), '# 第 1 輪\n\n有兩處要改。\n');
    writeFileSync(path.join(dir, 'verify-2.md'), '# 第 2 輪\n\n全部對得上。\n');
  }
  writeFileSync(path.join(dir, 'claims.md'), '- 週一休館 3 間\n');
  const packs = path.join(root, 'apps', 'api', 'app', 'guides', 'content');
  mkdirSync(packs, { recursive: true });
  writeFileSync(path.join(packs, 'ai-agents-explained.json'), JSON.stringify({ slug: 'ai-agents-explained', kind: 'ai', locales: { 'zh-TW': {} } }));
  // The tutorial's own narration: ag010 in the channel voice, ag011 in another.
  const audio = path.join(work, TUTORIAL.slug, 'audio');
  mkdirSync(audio, { recursive: true });
  writeFileSync(path.join(audio, 'ag010.wav'), tone(2.1, 300));
  writeFileSync(path.join(audio, 'ag011.wav'), tone(2.1, 310));
  writeFileSync(path.join(audio, 'cache.json'), JSON.stringify({ lines: { ag010: longClipKey(VOICE, LINES[2].text), ag011: longClipKey({ provider: 'gemini', name: 'Kore' }, LINES[3].text) } }));
  return { work, root, base: path.join(work, '_shorts') };
}

/** The site and every model: answers by stage and variant, reviews kept, what was sent recorded. */
function fakeSite({ answers = {}, source = { slug: SOURCE.slug, youtube_video_id: VIDEO_ID, youtube_publish_at: SOURCE.youtube_publish_at, dropped_at: null, reviews: [] } } = {}) {
  const calls = { run: [], reports: [], reviews: [], done: [], policy: [] };
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
      return json({ text: typeof value === 'string' ? value : JSON.stringify(value), provider: 'claude_code', model: 'claude-checker', input_tokens: 100, output_tokens: 50, usage: { tokens: 150, token_budget: 20_000_000 } });
    }
    if (pathname === '/api/video/automation/shorts/settings') return json({ enabled: true, voice: VOICE, seconds_min: 10, seconds_max: 55, locales: [], made_for_kids: false });
    if (pathname === '/api/video/automation/judge/policy') {
      calls.policy.push(body);
      return json({ passed: true, note: 'Jev 照頻道立場讀過，可以上' });
    }
    const done = /^\/api\/video\/automation\/shorts\/([a-z0-9-]+)\/done$/.exec(pathname);
    if (done) {
      calls.done.push({ topic: done[1], ...body });
      return json({ slug: done[1], status: body.outcome });
    }
    const review = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (review) {
      const [, slug, sub] = review;
      if (slug === SOURCE.slug && !sub && (init.method ?? 'GET') === 'GET') return source ? json(source) : json({ code: 'not_found', detail: slug }, 404);
      const list = reviews.get(slug) ?? [];
      reviews.set(slug, list);
      if (init.method === 'PUT') {
        calls.reports.push({ slug, ...body });
        return json({ slug, reviews: list });
      }
      if (sub && init.method === 'POST') {
        const same = list.find((each) => each.gate === body.gate && each.content_sha256 === body.content_sha256);
        if (same) return json(same);
        const made = { id: `r${list.length + 1}`, status: 'approved', note: null, ...body };
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

const PICKED = { segments: SEGMENTS, note: '兩段各講一件事' };
const CHECKED = { ok: true, claims: [{ text: '代理會先查開放時間', ok: true, evidence: 'ag010' }], problems: [] };
const ANSWERS = () => ({ 'planner:shorts-cut': PICKED, 'writer:shorts-cut': { script: SCRIPT }, 'verifier:shorts-cut': CHECKED });

/** A build without a browser or ffmpeg, as in lab.test.mjs: tones for the phrases, a stand-in cut. */
function fakeTools() {
  const builds = [];
  const linked = [];
  const build = async ({ file, sourceBase, workdir, speech }) => {
    const bytes = readFileSync(file);
    const doc = JSON.parse(bytes);
    assert.deepEqual(validate(doc), []);
    const evidence = verifyEvidence(doc, sourceBase);
    builds.push({ speech, scenes: doc.scenes.length });
    const directory = path.join(workdir, doc.slug, `build-${builds.length}`);
    for (const sub of ['audio', 'upload', 'evidence']) mkdirSync(path.join(directory, sub), { recursive: true });
    writeFileSync(path.join(directory, 'script.json'), bytes);
    for (const item of evidence) writeFileSync(path.join(directory, 'evidence', item.path), item.bytes);
    const phrases = phrasesOf(doc);
    phrases.forEach((_phrase, index) => writeFileSync(path.join(directory, 'audio', `${String(index).padStart(3, '0')}.wav`), tone(3.5, 400 + index * 10)));
    const timeline = buildTimeline(doc, phrases.map(() => 3.5), { minSeconds: 10, maxSeconds: 55 });
    writeFileSync(path.join(directory, 'timeline.json'), JSON.stringify(timeline));
    writeFileSync(path.join(directory, 'checks.json'), JSON.stringify({ ok: true, layout: timeline.cues.map((cue) => ({ cue: cue.index, problems: [] })) }));
    writeFileSync(path.join(directory, 'upload', 'final.mp4'), Buffer.from(`a stand-in cut of ${doc.slug}, build ${builds.length}`));
    writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), srt(timeline));
    writeFileSync(path.join(directory, 'upload', 'cover.png'), Buffer.from('cover'));
    writeFileSync(path.join(directory, 'usage.json'), JSON.stringify({ narration: { seconds: timeline.seconds, characters: 40, calls: phrases.length, provider: 'gemini' }, stages: {}, checks: {} }));
    return { directory, seconds: timeline.seconds };
  };
  const heard = (args) => {
    const phrases = phrasesOf(JSON.parse(readFileSync(path.join(args.directory, 'script.json'), 'utf8')));
    let index = 0;
    return checkAudio({ ...args, transcribeImpl: async () => phrases[index++], judgeImpl: async ({ lines }) => new Map(lines.map((line) => [line.id, 0.1])) });
  };
  const measured = async (final) => {
    const timeline = JSON.parse(readFileSync(path.join(path.dirname(path.dirname(final)), 'timeline.json'), 'utf8'));
    return {
      video: { width: PROFILE.width, height: PROFILE.height, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: String(timeline.frames) },
      audio: { codec_name: 'aac', sample_rate: '48000', duration: String(timeline.seconds) },
      format: {},
      loudness: { input_i: '-14.1', input_tp: '-1.5' },
    };
  };
  const qa = (args) => runQa({ ...args, measureImpl: measured, tools: {}, linkCheck: async (url) => (linked.push(url), { url, ok: true, status: 200 }), history: [] });
  return { builds, linked, tools: { build, checkAudio: heard, runQa: qa, packageBuild, push } };
}

function cutFor(t, site, { tools = {}, space = workspace(t), job = jobFor(1), slug = 'ai-agent-vs-chatbot-cut-1' } = {}) {
  const clock = { now: Date.parse('2026-10-05T01:00:00Z') };
  const ctx = { env, home: space.work, root: space.root, fetch: site.fetchImpl, sleep: async () => {}, now: () => new Date((clock.now += 1000)), stdout: { write: () => {} } };
  const short = new CutShort({ ctx, api: automationClient(ctx), site: siteClient({ env, home: space.work, fetch: site.fetchImpl, sleep: async () => {} }), job, slug, base: space.base, settings: { max_verify_rounds: 3 }, shortsSettings: { voice: VOICE, locales: [] }, tools });
  return { short, ...space };
}

// --- the pieces ------------------------------------------------------------------------------------

test('the prompts are the originals, the skill keeps the same texts, and the checker reads no stance', () => {
  const text = readFileSync(path.join(REPO, '.agents', 'skills', 'youtube-video', 'references', 'prompts', CUT_SKILL_FILE), 'utf8');
  const blocks = [...text.matchAll(/^## `([a-z:-]+)`\n\n```text\n([\s\S]*?)\n```$/gm)].map((match) => [match[1], match[2]]);
  assert.deepEqual(blocks.map(([key]) => key), Object.keys(CUT_INSTRUCTIONS));
  for (const [key, body] of blocks) assert.equal(body, CUT_INSTRUCTIONS[key], `${CUT_SKILL_FILE}: ${key} is the original word for word`);
  assert.match(CUT_INSTRUCTIONS['writer:shorts-cut'], /add no claim, no example, no number and no Latin-script word/);
  assert.match(CUT_INSTRUCTIONS['planner:shorts-cut'], /Two passages never say the same thing/);
  assert.match(cutInstructions('writer', 'shorts-cut', '只寫做過的事。'), /## The channel's stance\n只寫做過的事。$/);
  assert.doesNotMatch(cutInstructions('verifier', 'shorts-cut', '只寫做過的事。'), /stance/i);
  assert.throws(() => cutInstructions('writer', 'shorts-lab'), /no highlight prompt/);
});

test('a highlight is cut only from a public tutorial that is the topic\'s own source', () => {
  const now = new Date('2026-10-05T01:00:00Z');
  assert.equal(cutRefusal(jobFor(1), now), null);
  assert.match(cutRefusal({ ...jobFor(1), line: 'lab' }, now), /不是長片精華/);
  assert.match(cutRefusal({ ...jobFor(1), topic: { ...topic(1), source_slug: null } }, now), /沒有來源影片/);
  assert.match(cutRefusal({ ...jobFor(1), source: null }, now), /伺服器沒有給來源影片/);
  assert.match(cutRefusal({ ...jobFor(1), source: { ...SOURCE, slug: 'why-openai-killed-sora' } }, now), /來源不符：題目指向 ai-agent-vs-chatbot，伺服器給的是 why-openai-killed-sora/);
  assert.match(cutRefusal({ ...jobFor(1), source: { ...SOURCE, format: 'drama' } }, now), /不是投影片教學長片/);
  assert.match(cutRefusal({ ...jobFor(1), source: { ...SOURCE, youtube_video_id: null } }, now), /還沒有 YouTube 影片/);
  assert.match(cutRefusal({ ...jobFor(1), source: { ...SOURCE, youtube_publish_at: '2026-10-09T11:30:00Z' } }, now), /還沒公開/, 'scheduled is not public');
  assert.match(cutRefusal({ ...jobFor(1), source: { ...SOURCE, youtube_publish_at: null } }, now), /還沒公開/);
});

test('the passages name lines of the tutorial in order, fit the length and never share a line or a point', () => {
  const seconds = { min: 25, max: 55 };
  assert.deepEqual(segmentProblems(PICKED, { lines: LINES, seconds }), []);
  assert.deepEqual(segmentProblems({ segments: [], note: '每一段都要靠前文' }, { lines: LINES, seconds }), [], 'nothing stands alone, and the note says why');
  const problems = (segments, note) => segmentProblems({ segments, note }, { lines: LINES, seconds });
  assert.match(problems([]).join(), /needs a note/);
  assert.match(problems([...SEGMENTS, SEGMENTS[0]]).join(), /at most 2/);
  assert.match(problems([{ ...SEGMENTS[0], line_ids: ['ag010', 'ag099'] }]).join(), /ag099 is not a line of the tutorial/);
  assert.match(problems([{ ...SEGMENTS[0], line_ids: ['ag012', 'ag010'] }]).join(), /follow the tutorial's order/);
  assert.match(problems([{ ...SEGMENTS[0], line_ids: ['ag010'] }]).join(), /at least two lines/);
  assert.match(problems([SEGMENTS[0], { ...SEGMENTS[1], line_ids: ['ag013', 'ag020'] }]).join(), /ag013 is in segment 1 too; two passages share no line/);
  assert.match(problems([SEGMENTS[0], { ...SEGMENTS[1], point: SEGMENTS[0].point }]).join(), /the same point/);
  assert.match(problems([{ ...SEGMENTS[0], estimated_seconds: 70 }]).join(), /estimated_seconds must be 25 to 55/);
  assert.match(problems([{ ...SEGMENTS[0], standalone: '' }]).join(), /standalone is missing/);
});

test('each highlight topic of a tutorial takes the next passage nobody has taken', () => {
  const picks = { segments: SEGMENTS, taken: {} };
  assert.equal(segmentFor(picks, 'a-cut-1'), 0);
  picks.taken['a-cut-1'] = 0;
  assert.equal(segmentFor(picks, 'a-cut-1'), 0, 'the same topic keeps its passage');
  assert.equal(segmentFor(picks, 'a-cut-2'), 1);
  picks.taken['a-cut-2'] = 1;
  assert.equal(segmentFor(picks, 'owner-idea'), null, 'none left');
  assert.equal(segmentFor({ segments: [], taken: {} }, 'a-cut-1'), null);
});

test('a number or a Latin-script word the tutorial does not have is refused, and the end leads back', () => {
  const sourceText = [...LINES.map((line) => line.text), '2026 年 9 月'].join('\n');
  const source = { slug: TUTORIAL.slug, url: `https://youtu.be/${VIDEO_ID}`, youtube_video_id: VIDEO_ID, line_ids: SEGMENTS[0].line_ids };
  const article = shortsArticleUrl({ slug: 'ai-agents-explained', kind: 'ai' }, 'ai-agent-vs-chatbot-cut-1');
  const doc = (script) => cutScript({ script }, { slug: 'ai-agent-vs-chatbot-cut-1', series: TUTORIAL.slug, source, article });
  assert.deepEqual(cutProblems(doc(SCRIPT), { sourceText }), [], 'the numbers and words of the tutorial, an article line the program wrote');
  const scenes = (edit) => SCRIPT.scenes.map((scene, index) => (index === 2 ? { ...scene, ...edit } : scene));
  assert.match(cutProblems(doc({ ...SCRIPT, scenes: scenes({ headline: '週一休館 4 間' }) }), { sourceText }).join(), /scene 2 headline: the number 4 is not in the tutorial's script/);
  assert.match(cutProblems(doc({ ...SCRIPT, scenes: scenes({ note: '用 GPT-5 也一樣' }) }), { sourceText }).join(), /scene 2 note: "GPT-5" is not in the tutorial's script/);
  assert.match(cutProblems(doc({ ...SCRIPT, titles: ['2027 年的 AI 代理', SCRIPT.titles[1]] }), { sourceText }).join(), /titles\[0\]: the number 2027/);
  assert.match(cutProblems(doc({ ...SCRIPT, hashtags: ['OpenAI'] }), { sourceText }).join(), /hashtags\[0\]: "OpenAI"/, 'a hashtag is seen too');
  assert.deepEqual(cutProblems(doc({ ...SCRIPT, scenes: scenes({ note: 'ai 代理在 2026 年' }) }), { sourceText }), [], 'a word in another case and a number on the cards count');
  assert.match(cutProblems(doc({ ...SCRIPT, scenes: SCRIPT.scenes.slice(0, 3) }), { sourceText }).join(), /last narration phrase must send the viewer to the full video/);
  assert.match(cutProblems(doc({ ...SCRIPT, scenes: scenes({ narration: ['這是一句超過三十八個字的旁白，這是一句超過三十八個字的旁白，真的很長很長很長。'] }) }), { sourceText }).join(), /narration phrases 1–38 characters/);
  const written = doc(SCRIPT);
  assert.deepEqual([written.line, written.format, written.series, written.source], ['cut', 'shorts', TUTORIAL.slug, source], 'the worker sets what is not the writer\'s');
  assert.equal(ownDescription(written.description), SCRIPT.description);
});

test('the description leads back to the full video first and the article next; qa checks both links and the source', async () => {
  const article = shortsArticleUrl({ slug: 'ai-agents-explained', kind: 'ai' }, 'ai-agent-vs-chatbot-cut-1');
  assert.equal(article, 'https://mokaair.com/zh-TW/guides/ai/ai-agents-explained?utm_source=youtube&utm_medium=shorts&utm_campaign=ai-agent-vs-chatbot-cut-1');
  assert.equal(shortsArticleUrl({ slug: 'taipei-rain', kind: 'life' }, 'x'), 'https://mokaair.com/zh-TW/life/taipei-rain?utm_source=youtube&utm_medium=shorts&utm_campaign=x');
  assert.equal(shortsArticleUrl(null, 'x'), null);
  const source = { slug: TUTORIAL.slug, url: `https://youtu.be/${VIDEO_ID}`, youtube_video_id: VIDEO_ID, line_ids: SEGMENTS[0].line_ids };
  const doc = cutScript({ script: SCRIPT }, { slug: 'ai-agent-vs-chatbot-cut-1', series: TUTORIAL.slug, source, article });
  const metadata = composeMetadata({ doc, finalSha256: 'f'.repeat(64), seconds: 30, sourceUrl: source.url });
  const [first, second] = metadata.description.split('\n\n');
  assert.equal(first, `完整影片：https://youtu.be/${VIDEO_ID}`);
  assert.equal(second, `完整文章：${article}`);
  assert.deepEqual(metadata.source.line_ids, SEGMENTS[0].line_ids, 'the lines it tells again go with the package');
  assert.deepEqual(descriptionUrls([metadata.description]), [`https://youtu.be/${VIDEO_ID}`, article]);
  assert.equal(linksItem({ results: [{ url: source.url, ok: true, status: 200 }, { url: article, ok: false, status: 404 }], metadata }).ok, false, 'an article that does not answer fails');
  assert.equal(linksItem({ results: [{ url: source.url, ok: true, status: 200 }, { url: article, ok: true, status: 200 }], metadata }).ok, true);
  const now = new Date('2026-10-05T01:00:00Z');
  assert.equal(evidenceItem({ doc, source: { youtube_video_id: VIDEO_ID, youtube_publish_at: SOURCE.youtube_publish_at, reviews: [] }, now }).ok, true);
  assert.match(evidenceItem({ doc, source: { youtube_video_id: VIDEO_ID, youtube_publish_at: SOURCE.youtube_publish_at, dropped_at: '2026-10-04T00:00:00Z' }, now }).detail, /was dropped/);
  assert.equal(evidenceItem({ doc, source: null, now }).ok, false, 'a source the site does not have');
  assert.equal(evidenceItem({ doc, source: { youtube_video_id: null, reviews: [] }, now }).ok, false, 'a source not public');
});

test('a phrase the tutorial says word for word in the same voice comes from its narration, not the synthesizer', (t) => {
  const space = workspace(t);
  const cacheDir = path.join(space.base, '.speech-server');
  const longAudioDir = path.join(space.work, TUTORIAL.slug, 'audio');
  const phrases = [LINES[2].text, LINES[3].text, '週一休館的館有三間，代理會換掉它們。'];
  assert.equal(seedNarration({ phrases, voice: VOICE, video: TUTORIAL, longAudioDir, cacheDir }), 1, 'ag010 only: ag011 was spoken in another voice, the third was rewritten');
  const seeded = path.join(cacheDir, `${phraseKey(VOICE, LINES[2].text)}.wav`);
  assert.ok(readFileSync(seeded).equals(readFileSync(path.join(longAudioDir, 'ag010.wav'))));
  assert.equal(existsSync(path.join(cacheDir, `${phraseKey(VOICE, LINES[3].text)}.wav`)), false);
  assert.equal(seedNarration({ phrases, voice: VOICE, video: TUTORIAL, longAudioDir, cacheDir }), 0, 'already there');
  assert.equal(seedNarration({ phrases, voice: { ...VOICE, style: '說書' }, video: TUTORIAL, longAudioDir, cacheDir: path.join(space.base, 'other') }), 0, 'another style is another voice');
  assert.equal(seedNarration({ phrases, voice: null, video: TUTORIAL, longAudioDir, cacheDir }), 0);
});

test('the latest fact-check round is the one a highlight reads', (t) => {
  const dir = path.join(workspace(t).root, 'docs', 'videos', TUTORIAL.slug);
  writeFileSync(path.join(dir, 'verify-10.md'), '第 10 輪\n');
  writeFileSync(path.join(dir, 'verify-p1-20260929.md'), '別的檔\n');
  assert.deepEqual(latestVerify(dir), { file: 'verify-10.md', text: '第 10 輪\n' });
  assert.equal(latestVerify(path.join(dir, 'nowhere')), null);
});

// --- one highlight, start to finish ------------------------------------------------------------------

test('a highlight goes from the frozen tutorial to the site, told again from its lines and leading back', async (t) => {
  const site = fakeSite({ answers: ANSWERS() });
  const { builds, linked, tools } = fakeTools();
  const { short, base } = cutFor(t, site, { tools });
  const line = await short.run();
  assert.match(line, /source frozen: ai-agent-vs-chatbot \(10 lines, verify-2\.md\)/);
  assert.match(line, /passage 1 of 2: 代理會先查資料再決定/);
  assert.match(line, /script written \(4 scenes, 4 phrases\)/);
  assert.match(line, /fact-checked: 1 claims backed by the tutorial/);
  assert.match(line, /built .*; 1 phrases from the tutorial's narration/);
  assert.match(line, /quality check: all 12 items pass/);
  assert.match(line, /pushed: final approved, upload package approved/);
  assert.equal(short.state.status, 'done');

  assert.deepEqual(site.calls.run.map((call) => `${call.stage}:${call.variant}`), ['planner:shorts-cut', 'writer:shorts-cut', 'verifier:shorts-cut']);
  assert.ok(site.calls.run.every((call) => call.format === 'shorts' && call.slug === 'ai-agent-vs-chatbot-cut-1'));
  const [planner, writer, verifier] = site.calls.run;
  assert.deepEqual(planner.payload.lines, LINES, 'the planner reads the whole tutorial');
  assert.equal(planner.payload.verify_report, '# 第 2 輪\n\n全部對得上。\n', 'with its latest fact-check');
  assert.deepEqual(writer.payload.segment.lines.map((each) => each.id), SEGMENTS[0].line_ids, 'the writer gets its passage');
  assert.equal(writer.payload.other_segment.point, SEGMENTS[1].point, 'and what the other highlight says, not to repeat it');
  assert.match(writer.instructions, /## The channel's stance\n只寫做過的事。/);
  assert.deepEqual(verifier.payload.segment.lines.map((each) => each.id), SEGMENTS[0].line_ids);

  const cutDir = path.join(base, 'ai-agent-vs-chatbot-cut-1', CUT_DIR);
  const frozen = readFileSync(path.join(cutDir, SOURCE_FILE));
  assert.equal(short.state.source_sha256, sha256(frozen), 'the hash recorded is the file that was used');
  const script = JSON.parse(readFileSync(path.join(cutDir, 'script.json'), 'utf8'));
  assert.deepEqual(script.source, { slug: TUTORIAL.slug, url: `https://youtu.be/${VIDEO_ID}`, youtube_video_id: VIDEO_ID, line_ids: SEGMENTS[0].line_ids });
  assert.deepEqual(script.evidence.map((each) => each.path), [SOURCE_FILE, SEGMENT_FILE]);
  assert.equal(JSON.parse(readFileSync(path.join(base, PICKS_DIR, `${TUTORIAL.slug}.json`), 'utf8')).taken['ai-agent-vs-chatbot-cut-1'], 0);

  assert.equal(builds.length, 1);
  const seeded = path.join(base, '.speech-server', `${phraseKey(VOICE, LINES[2].text)}.wav`);
  assert.ok(existsSync(seeded), 'the phrase the tutorial says word for word is in the cache before the build');
  const qa = JSON.parse(readFileSync(path.join(short.state.build, 'qa.json'), 'utf8'));
  assert.equal(qa.line, 'cut');
  assert.match(qa.items.find((item) => item.id === 'evidence').detail, /cut from ai-agent-vs-chatbot, public since/);
  assert.deepEqual(linked, [`https://youtu.be/${VIDEO_ID}`, 'https://mokaair.com/zh-TW/guides/ai/ai-agents-explained?utm_source=youtube&utm_medium=shorts&utm_campaign=ai-agent-vs-chatbot-cut-1']);
  assert.deepEqual(Object.keys(site.calls.policy[0]).sort(), ['script', 'slug', 'viewpoint'], 'the policy reading is asked as for any Short: the site picks the questions by the line');

  const [final, publish] = site.calls.reviews;
  assert.equal(final.gate, 'final');
  assert.ok(final.files.some((file) => file.role === 'evidence_source'), 'what it was cut from goes up with it');
  assert.equal(publish.gate, 'publish');
  assert.deepEqual(site.calls.done, [{ topic: 'ai-agent-vs-chatbot-cut-1', outcome: 'made' }]);
  assert.ok(site.calls.reports.length && site.calls.reports.every((report) => report.format === 'shorts' && report.shorts_line === 'cut'), 'reported as a highlight, so the policy reading leaves out the demonstration');
  assert.equal(JSON.parse(readFileSync(path.join(base, 'ai-agent-vs-chatbot-cut-1', LAB_FILE), 'utf8')).line, 'cut', 'the worker follows it as a highlight');
  assert.equal(await short.run(), null, 'a finished Short does nothing more');
});

test('the tutorial\'s second highlight takes the other passage without asking again; a third is dropped', async (t) => {
  const space = workspace(t);
  const first = cutFor(t, fakeSite({ answers: ANSWERS() }), { space, tools: { build: async () => { throw new Error('stop here'); } } });
  await first.short.run();
  const site = fakeSite({ answers: ANSWERS() });
  const second = cutFor(t, site, { space, job: jobFor(2), slug: 'ai-agent-vs-chatbot-cut-2', tools: { build: async () => { throw new Error('stop here'); } } });
  assert.match(await second.short.run(), /passage 2 of 2: 代理每查一次都有成本/);
  assert.deepEqual(site.calls.run.map((call) => `${call.stage}:${call.variant}`).slice(0, 1), ['writer:shorts-cut'], 'the passages were chosen once for the tutorial');
  assert.equal(site.calls.run[0].payload.other_segment.point, SEGMENTS[0].point);

  const third = fakeSite({ answers: ANSWERS() });
  const owner = cutFor(t, third, { space, job: { ...jobFor(3), topic: { ...topic(3), slug: 'owner-agent-highlight' } }, slug: 'owner-agent-highlight' });
  assert.match(await owner.short.run(), /no passage left for this topic; dropped/);
  assert.deepEqual(third.calls.done, [{ topic: 'owner-agent-highlight', outcome: 'dropped', note: '這支長片只有 2 段值得單獨成片，已經由另一支精華用掉' }]);
  assert.equal(third.calls.run.length, 0);
  assert.equal(owner.short.state.status, 'done');
});

test('a tutorial with nothing that stands alone gives no highlight: the topic is dropped with the reason', async (t) => {
  const site = fakeSite({ answers: { ...ANSWERS(), 'planner:shorts-cut': { segments: [], note: '每一段都要靠前面的示範' } } });
  const { short } = cutFor(t, site);
  assert.match(await short.run(), /no passage left for this topic; dropped \(這支長片沒有能單獨成片的段落：每一段都要靠前面的示範\)/);
  assert.deepEqual(site.calls.done.map((each) => each.outcome), ['dropped']);
});

test('a source that does not match, is not public or is not on this worker blocks the highlight with the reason', async (t) => {
  const mismatched = fakeSite({ answers: ANSWERS() });
  const one = cutFor(t, mismatched, { job: jobFor(1, { source: { ...SOURCE, slug: 'why-openai-killed-sora' } }) });
  assert.match(await one.short.run(), /blocked — 來源不符：題目指向 ai-agent-vs-chatbot，伺服器給的是 why-openai-killed-sora/);
  assert.equal(mismatched.calls.run.length, 0, 'no model is asked');
  assert.equal(mismatched.calls.reports.at(-1).stage, 'blocked');
  assert.equal(mismatched.calls.reports.at(-1).shorts_line, 'cut');
  assert.deepEqual(mismatched.calls.reports.at(-1).checklist.map((item) => [item.key, item.done]), [['blocked', false], ['source', false], ['pick', false], ['write', false], ['build', false], ['qa', false], ['push', false]], 'the highlight\'s own steps on /admin/videos');

  const scheduled = fakeSite({ answers: ANSWERS() });
  const two = cutFor(t, scheduled, { job: jobFor(1, { source: { ...SOURCE, youtube_publish_at: '2026-10-09T11:30:00Z' } }) });
  assert.match(await two.short.run(), /blocked — 來源 ai-agent-vs-chatbot 還沒公開/);

  const missing = fakeSite({ answers: ANSWERS() });
  const three = cutFor(t, missing, { space: workspace(t, { video: null }) });
  assert.match(await three.short.run(), /blocked — 來源長片 ai-agent-vs-chatbot 的稿子不在工人的工作區/);

  const unchecked = fakeSite({ answers: ANSWERS() });
  const four = cutFor(t, unchecked, { space: workspace(t, { verify: false }) });
  assert.match(await four.short.run(), /blocked — 來源長片 ai-agent-vs-chatbot 沒有查核報告/);

  const other = fakeSite({ answers: ANSWERS() });
  const five = cutFor(t, other, { space: workspace(t, { video: { ...TUTORIAL, slug: 'another-video' } }) });
  assert.match(await five.short.run(), /blocked — 來源不符：docs\/videos\/ai-agent-vs-chatbot\/video\.json 寫的是 another-video/);
});

test('a script with what the tutorial does not say is sent back, and blocks the second time in a row', async (t) => {
  const invented = { ...SCRIPT, scenes: SCRIPT.scenes.map((scene, index) => (index === 2 ? { ...scene, headline: '週一休館 5 間' } : scene)) };
  const site = fakeSite({ answers: { ...ANSWERS(), 'writer:shorts-cut': { script: invented } } });
  const { short } = cutFor(t, site);
  assert.match(await short.run(), /write gave nothing usable \(the script does not pass the check: scene 2 headline: the number 5 is not in the tutorial's script/);
  const writes = site.calls.run.filter((call) => call.stage === 'writer');
  assert.equal(writes.length, 2, 'asked again at once with the problems');
  assert.match(writes[1].payload.problems[0], /the number 5/);
  assert.match(await short.run(), /blocked — write failed 2 times in a row/);
});

test('a changed source.json stops the highlight', async (t) => {
  const site = fakeSite({ answers: { ...ANSWERS(), 'writer:shorts-cut': () => json({ code: 'video_ai_upstream_busy', detail: 'busy' }, 503) } });
  const { short, base } = cutFor(t, site);
  assert.match(await short.run(), /write is waiting on a service \(busy\)/);
  const file = path.join(base, 'ai-agent-vs-chatbot-cut-1', CUT_DIR, SOURCE_FILE);
  writeFileSync(file, readFileSync(file, 'utf8').replace('3 間', '4 間'));
  assert.match(await short.run(), /blocked — source\.json 在凍結之後被改過/);
});
