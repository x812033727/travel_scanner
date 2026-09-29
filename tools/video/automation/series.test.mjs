import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { readApprovals } from "../core/approvals.mjs";
import { dramaFixture, explainerFixture, sandbox } from "../core/fixtures/load.mjs";
import { shortsFile } from "../shorts/episode.mjs";
import { readJson } from "../core/paths.mjs";
import { keepSheets, readStore, reuseSheets, sheetKey } from "../media/series-store.mjs";
import { automationClient } from "./client.mjs";
import { answerProblem, discussStep, documentDiscussionPayload, parseSubject, revisedDocumentProblem, unusableReply } from "./discuss.mjs";
import { Automation, automatedVideos, settle } from "./flow.mjs";
import { instructionsFor, SERIES_INSTRUCTIONS } from "./prompts.mjs";
import { eachLine } from "../core/schema.mjs";
import { estimateTimeline, framesFor, frameToSeconds } from "../core/timeline.mjs";
import { lintCompilation } from "../core/compilation.mjs";
import { compilationSlug } from "./compilation.mjs";
import { castFrom, chapterRange, documentPayload, documentProblem, documentVariant, episodeBrief, episodeSlug, isExplainerOneOff, isOneOff, planDocument, retentionNumbers, scriptVerdict, seriesStep } from "./series.mjs";
import { checkBrief } from "../core/lint.mjs";

const TOKEN = `mkv_${"s".repeat(43)}`;
const SITE = "https://site.test";
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

const SERIES = {
  id: "5e1a2b3c-4d5e-4f60-8a7b-9c0d1e2f3a4b", slug: "wenjian", title: "問劍", premise: "兩個少年在正道與魔道之間", aspects: ["world", "bonds", "structure", "mood"],
  tone: "dual-male-leads-subtext", style_preset: "cinematic-3d", target_minutes: 3, planned_episodes: 25, episodes_per_chapter: 10, chapters: 3, open_ended: true,
  status: "active", note: "旁白慢一點", requested_chapter: null, force_next: false, episodes_done: 0, episodes_started: 0, episodes_ready: 10, docs_pending: 0,
  media_usd: 0, clip_seconds: 0, created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T00:00:00Z",
};
const CAST = [
  { id: "shen-lan", name: "沈瀾", role: "lead", appearance: "a young man of twenty, lean, long black hair tied with a white ribbon, a plain grey robe, a bronze bell at his belt", voice: { provider: "gemini", name: "Kore", style: "冷靜低沉" } },
  { id: "chu-ying", name: "楚英", role: "lead", appearance: "a young man of twenty-one, broad-shouldered, hair in a high knot, a black robe with red hems, a cracked jade pendant", voice: { provider: "gemini", name: "Sulafat", style: "溫和" } },
];
const SETTING = { body_md: "# 設定集\n世界。", body_json: { characters: CAST, mysteries: [{ id: "m1", question: "誰敲響了鐘", planted_chapter: 1, reveal_chapter: 5, reserved: false }] } };
const beats = (number, type = "danger") => ({ number, title: `第 ${number} 集`, logline: `L${number}`, hook: "鐘聲", conflict: "衝突", turn: "轉折", cliffhanger: { type, text: "懸念" }, setups: ["m1"], payoffs: [], tension: [2, 3, 3, 4, 5], characters: ["shen-lan", "chu-ying"], locations: ["山門"], theme: "選擇" });
const CHAPTER = { body_md: "# 第一篇", body_json: { chapter: 1, episodes: Array.from({ length: 10 }, (_, index) => beats(index + 1, index % 2 ? "reveal" : "danger")) } };

// A one-off drama (docs/videos/DRAMA-FLOW.md, section 2): a one-episode series whose only document is its story bible.
const ONE_OFF = { ...SERIES, id: "7a1b2c3d-0000-4000-8000-000000000001", slug: "one-off-7a1b2c3d", kind: "one-off", title: "精衛", premise: "精衛填海：炎帝最小的女兒在東海溺水，化成一隻鳥。", aspects: [], style_preset: "ink-wash", target_minutes: 2, planned_episodes: 1, episodes_per_chapter: 1, chapters: 1, open_ended: false, status: "setting", note: null, episodes_ready: 0 };
const ONE_OFF_CAST = [
  { id: "jingwei", name: "精衛", role: "lead", appearance: "a girl of about twelve, small and quick, hair in two loops tied with red cord, a plain linen dress the colour of sand", voice: { provider: "gemini", name: "Kore", style: "清亮" } },
  { id: "yandi", name: "炎帝", role: "support", appearance: "a tall emperor of sixty, broad face, grey beard to the chest, a dark red robe with a bronze crown", voice: { provider: "gemini", name: "Sulafat", style: "低沉" } },
];
const OUTLINE = { title: "精衛填海", logline: "一隻鳥要填平淹死她的海", hook: "很久以前，發鳩山上住著炎帝最小的女兒。", conflict: "海太大，石子太小", turn: "她不再求父親，自己銜石", cliffhanger: { type: "emotion", text: "海面上多了一顆石子" }, characters: ["jingwei", "yandi"], locations: ["發鳩山", "東海"], theme: "明知做不到還是要做" };
const BIBLE = { body_md: "# 精衛填海\n## 故事前提\n…\n## 角色\n…\n## 幕\n…\n## 大綱\n…\n## 素材\n…\n## 不做的事\n…\n", body_json: { characters: ONE_OFF_CAST, acts: [{ number: 1, title: "告別", summary: "s", shots: 4 }, { number: 2, title: "溺水", summary: "s", shots: 5 }, { number: 3, title: "銜石", summary: "s", shots: 4 }], outline: OUTLINE, music: "古琴，慢", not_doing: ["不寫戀愛"], lexicon: {} } };
const oneOffEpisode = (status) => ({ number: 1, chapter_number: 1, title: OUTLINE.title, logline: OUTLINE.logline, beats: OUTLINE, status, slug: null, recap: null, started_at: null, finished_at: null, video: null });

/** The owner's line on a thread as the site hands it to the worker (MessageJob). */
function messageJob(subject, body, { series = ONE_OFF, doc = null, episode = null, thread = [] } = {}) {
  const message = { id: `m-${subject}-${thread.length + 1}`, subject, author: "owner", body_md: body, refers_to: doc ? `v${doc.version}` : null, answered_at: null, created_at: "2026-09-27T03:00:00Z", created_by_user_id: "u1" };
  const target = subject.startsWith("script:") ? "script" : "doc";
  const setting = doc?.kind === "bible" || doc?.kind === "setting" ? null : (series.kind === "one-off" ? { id: "b1", kind: "bible", chapter_number: 0, version: 1, ...BIBLE, status: "approved" } : SETTING);
  return { message, thread: [...thread, message], series, subject, target, doc, episode, context: { series, setting, outline: null, chapter: null, chapter_number: null, chapter_range: null, episode, episodes: episode ? [episode] : [], recaps: [], mysteries: [] } };
}

function job(kind, extra = {}) {
  return { kind, series: SERIES, chapter_number: kind === "chapter" ? 1 : null, episode: null, previous: null, rewrites_left: 2, context: { series: SERIES, setting: SETTING, outline: null, chapter: null, chapter_number: null, chapter_range: null, episode: null, episodes: [], recaps: [], mysteries: SETTING.body_json.mysteries }, ...extra };
}

test("a document the planner returns must have the shape the owner reads, checked before it is filed", () => {
  assert.match(documentProblem("setting", { body_md: "x", body_json: {} }, job("setting")), /characters/);
  assert.match(documentProblem("setting", { body_md: "x", body_json: { characters: CAST } }, job("setting")), /mysteries/);
  assert.equal(documentProblem("setting", SETTING, job("setting")), null);
  assert.match(documentProblem("outline", { body_md: "x", body_json: { chapters: [] } }, job("outline")), /3 chapters/);
  const chapters = [1, 2, 3].map((number) => ({ number, title: `第 ${number} 篇`, episodes: Array.from({ length: chapterRange(SERIES, number)[1] - chapterRange(SERIES, number)[0] + 1 }, (_, index) => ({ number: chapterRange(SERIES, number)[0] + index, title: "t", logline: "l" })) }));
  assert.equal(documentProblem("outline", { body_md: "x", body_json: { chapters } }, job("outline")), null);
  assert.equal(documentProblem("chapter", CHAPTER, job("chapter")), null);
  const flat = structuredClone(CHAPTER);
  flat.body_json.episodes[2].tension = [3, 3, 3, 3, 3];
  assert.match(documentProblem("chapter", flat, job("chapter")), /episode 3 must end tense/);
  const same = structuredClone(CHAPTER);
  same.body_json.episodes[1].cliffhanger.type = "danger";
  assert.match(documentProblem("chapter", same, job("chapter")), /episodes 1 and 2 end on the same kind/);
  const missing = structuredClone(CHAPTER);
  delete missing.body_json.episodes[4].turn;
  assert.match(documentProblem("chapter", missing, job("chapter")), /episode 5 lacks turn/);
  const short = structuredClone(CHAPTER);
  short.body_json.episodes.pop();
  assert.match(documentProblem("chapter", short, job("chapter")), /covers episodes 1 to 10/);
  assert.equal(episodeSlug("wenjian", 7), "wenjian-e007");
  assert.deepEqual(castFrom(SETTING.body_json).map((character) => character.id), ["chu-ying", "shen-lan"], "the cast is listed by id");
  assert.deepEqual(Object.keys(castFrom(SETTING.body_json)[0]), ["id", "name", "appearance", "voice"], "only video.json's keys");
});

test("every series prompt carries the tension rules, and a stage's variant picks it", () => {
  assert.deepEqual(Object.keys(SERIES_INSTRUCTIONS).sort(), ["planner:bible", "planner:chapter", "planner:compilation", "planner:discuss", "planner:outline", "planner:setting", "translator:compilation", "verifier:episode", "verifier:recap", "verifier:series-doc", "writer:discuss", "writer:episode"]);
  assert.match(instructionsFor("planner", "drama", "", "bible"), /STORY BIBLE[\s\S]*ONE outline, not options/);
  assert.match(instructionsFor("planner", "drama", "", "discuss"), /OWNER'S LINE[\s\S]*300 characters[\s\S]*"revised" is null[\s\S]*Never change a document above/);
  assert.match(instructionsFor("writer", "drama", "", "discuss"), /OWNER'S LINE[\s\S]*revised\.video[\s\S]*keep every other scene, line and id/);
  assert.match(instructionsFor("planner", "drama", "", "setting"), /SETTING BOOK[\s\S]*conflict engine[\s\S]*RESERVED/);
  assert.match(instructionsFor("planner", "drama", "", "outline"), /stakes rise chapter by chapter/);
  assert.match(instructionsFor("planner", "drama", "", "chapter"), /HOOK inside the first 20 seconds[\s\S]*never end on the same cliffhanger type/);
  assert.match(instructionsFor("writer", "drama", "", "episode"), /"fix" is present[\s\S]*EPISODE OF A LONG SERIES/);
  assert.match(instructionsFor("verifier", "drama", "", "episode"), /coverage/);
  assert.match(instructionsFor("verifier", "drama", "", "recap"), /150 characters/);
  assert.match(instructionsFor("planner", "drama", "旁白慢", "setting"), /standing instructions[\s\S]*\n旁白慢$/);
  for (const text of Object.values(SERIES_INSTRUCTIONS)) assert.match(text, /original|existing work/i);
});

function context(box, fetchImpl, clock) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date(clock.now),
      sleep: async (ms) => {
        clock.now += ms;
      },
      EXIT: { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 },
    },
  };
}

/** A site with the series routes: `jobs` is what next answers in turn; everything sent is recorded. */
function fakeSite({ jobs = [], answers = {}, settings = {}, messages = [], decide = null, series = SERIES, compilation = null, episodeBeats = beats, oneOffStart = null } = {}) {
  const calls = { run: [], docs: [], episodes: [], reports: [], reviews: [], answers: [], compilations: [] };
  const projects = new Map();
  const reviewsOf = (slug) => projects.get(slug) ?? projects.set(slug, []).get(slug);
  const current = {
    enabled: true, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 1, topic_scope: ["AI"], topic_avoid: [], topic_from_site: true, topic_from_search: false,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" }, target_minutes_min: 1, target_minutes_max: 12, caption_locales: ["en"],
    max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true,
    drama: { drama_enabled: true, style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [] }, ...settings,
  };
  const json = (body, status = 200) => Response.json(body, { status });
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return json(current);
    if (pathname === "/api/video/automation/videos") return json([]);
    if (pathname === "/api/video/automation/drama-requests/next") return json({ request: null });
    if (pathname === "/api/video/automation/series/next") return json({ job: jobs.shift() ?? null });
    // The discussion threads (docs/videos/DRAMA-FLOW.md, section 3): `messages` is what next answers in turn.
    if (pathname === "/api/video/automation/series/messages/next") return json({ job: messages.shift() ?? null });
    const answer = /^\/api\/video\/automation\/series\/messages\/([^/]+)\/answer$/.exec(pathname);
    if (answer) {
      calls.answers.push({ id: answer[1], ...body });
      const revision = body.revised ? { id: `d${calls.docs.length + 1}`, kind: "bible", chapter_number: 0, version: 2, body_md: body.revised.body_md, body_json: body.revised.body_json, status: "review" } : null;
      return json({ reply: { id: `m${calls.answers.length}`, subject: "bible", author: "planner", body_md: body.reply_md, refers_to: revision ? "v2" : "v1", answered_at: new Date().toISOString(), created_at: new Date().toISOString(), created_by_user_id: null }, revision });
    }
    const docs = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/docs$/.exec(pathname);
    if (docs) {
      calls.docs.push({ series: docs[1], ...body });
      // A hands-off series' site decides on the verdict (docs/videos/BINGE.md); `decide` plays it.
      const decided = decide?.(body) ?? { status: "review", note: null };
      return json({ id: `d${calls.docs.length}`, ...body, version: calls.docs.filter((doc) => doc.kind === body.kind && doc.chapter_number === body.chapter_number).length, ...decided }, 201);
    }
    const compiling = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/compilation\/(start|done)$/.exec(pathname);
    if (compiling) {
      calls.compilations.push({ series: compiling[1], action: compiling[2], ...(body ?? {}) });
      if (compiling[2] === "done") return json({ ...series, compilation_finished_at: "2026-09-27T09:00:00Z" });
      if (compilation?.refuse) return json({ code: compilation.refuse.code, detail: compilation.refuse.detail }, 409);
      return json({ series: { ...series, compilation_slug: body.slug }, episodes: compilation?.episodes ?? [], context: { series, setting: SETTING, outline: null, chapter: null, chapter_number: null, chapter_range: null, episode: null, episodes: [], recaps: [], mysteries: [], all_recaps: compilation?.recaps ?? [] } });
    }
    const episode = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/episodes\/(\d+)\/(start|recap|done)$/.exec(pathname);
    if (episode) {
      calls.episodes.push({ series: episode[1], number: Number(episode[2]), action: episode[3], ...(body ?? {}) });
      if (episode[3] === "start") {
        const number = Number(episode[2]);
        // Another one-off (an explainer) answers with its own series, bible and episode.
        if (oneOffStart) return json(oneOffStart(body));
        if (episode[1] === ONE_OFF.slug) {
          // A one-off's bible stands where the setting book does; its outline is the episode's beats.
          const context = { series: ONE_OFF, setting: { id: "b1", kind: "bible", chapter_number: 0, version: 1, ...BIBLE, status: "approved" }, outline: null, chapter: null, chapter_number: 1, chapter_range: [1, 1], episode: null, episodes: [oneOffEpisode("ready")], recaps: [], mysteries: [] };
          return json({ request: { id: "one-off-request", premise: ONE_OFF.premise, title: "精衛", source_guide: null, style_preset: "ink-wash", target_minutes: 2, note: null, status: "started", slug: body.slug, series_slug: ONE_OFF.slug, episode_number: 1 }, episode: { ...oneOffEpisode("started"), slug: body.slug }, context });
        }
        const context = { series, setting: SETTING, outline: null, chapter: CHAPTER, chapter_number: 1, chapter_range: [1, 10], episode: null, episodes: CHAPTER.body_json.episodes.map((each) => ({ ...each, chapter_number: 1, status: "ready", beats: each })), recaps: [{ number: 0, title: "序", recap: "鐘響了", state: {} }], mysteries: SETTING.body_json.mysteries };
        return json({ request: { id: `r${number}`, premise: `第 ${number} 集`, title: null, source_guide: null, style_preset: "cinematic-3d", target_minutes: 3, note: null, status: "started", slug: body.slug }, episode: { ...episodeBeats(number), chapter_number: 1, status: "started", slug: body.slug, beats: episodeBeats(number) }, context });
      }
      return json({ number: Number(episode[2]), status: episode[3] === "done" ? "done" : "started" });
    }
    if (pathname === "/api/video/automation/run") {
      calls.run.push(body);
      const answer = answers[body.variant ? `${body.stage}:${body.variant}` : body.stage]?.(body) ?? {};
      return json({ text: JSON.stringify(answer), provider: "anthropic", model: "claude-sonnet-5", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 20_000_000, drafts: 1, draft_budget: 8, calls: 1, failed_calls: 0 } });
    }
    const match = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (match) {
      const [, slug, sub] = match;
      if (init.method === "PUT") {
        calls.reports.push({ slug, ...body });
        return json({ slug, reviews: reviewsOf(slug) });
      }
      if (sub && init.method === "POST") {
        const review = { id: `r${reviewsOf(slug).length + 1}`, status: "pending", choice: null, note: null, decided_at: null, created_at: new Date().toISOString(), ...body };
        reviewsOf(slug).unshift(review);
        calls.reviews.push(review);
        return json(review);
      }
      return json({ slug, title: slug, stage: "x", checklist: [], youtube_video_id: null, reviews: reviewsOf(slug) });
    }
    return json({ code: "not_found", detail: pathname }, 404);
  };
  return { calls, fetchImpl, reviewsOf, settings: current, jobs };
}

const smallRefs = { script_writing: "short sentences", formats: "tutorial", channel: "Mokaair", showcase: { scenes: [] }, minimal: dramaFixture(), drama: "the drama route", drama_example: dramaFixture(), drama_brief: "# brief", series: "the series route" };

test("the setting book is planned from the owner's series, refused once for its shape, and filed for the owner", async () => {
  const box = sandbox();
  let calls = 0;
  const site = fakeSite({
    jobs: [job("setting")],
    answers: { "planner:setting": (body) => (calls++ === 0 ? { body_md: "# 設定集", body_json: { characters: CAST } } : { body_md: "# 設定集 v2", body_json: { ...SETTING.body_json, note: body.payload.previous_problem } }) },
  });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  // A scheduled draft is not due, so the second unit shows the series alone has nothing left.
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  const done = await automation.step();
  assert.match(done, /series wenjian: the setting book planned \(version 1\); it waits for the owner/);
  assert.equal(site.calls.run.length, 2, "the first answer lacked the mysteries; the second was asked with the reason");
  assert.equal(site.calls.run[0].variant, "setting");
  assert.equal(site.calls.run[0].slug, "series-wenjian");
  assert.match(site.calls.run[0].instructions, /SETTING BOOK/);
  assert.equal(site.calls.run[0].payload.series.premise, SERIES.premise);
  assert.deepEqual(site.calls.run[0].payload.series.aspects, SERIES.aspects);
  assert.match(site.calls.run[1].payload.previous_problem, /mysteries/);
  assert.deepEqual(site.calls.docs.map((doc) => [doc.kind, doc.chapter_number]), [["setting", 0]]);
  assert.equal(site.calls.docs[0].body_json.note, site.calls.run[1].payload.previous_problem);
  assert.equal(await automation.step(), null, "nothing else to do: every series waits for the owner");
});

test("a chapter outline sent back is rewritten from the owner's note with the recaps in hand", async () => {
  const box = sandbox();
  const previous = { id: "d1", kind: "chapter", chapter_number: 1, version: 1, body_md: "# v1", body_json: CHAPTER.body_json, status: "rejected", note: "第三集再緊一點", decided_at: null, created_at: "2026-09-27T00:00:00Z" };
  const site = fakeSite({ jobs: [job("chapter", { previous, rewrites_left: 1, context: { ...job("chapter").context, outline: { body_md: "# 總綱", body_json: { chapters: [{ number: 1, title: "第一篇", theme: "t", end_state: "e", episodes: [] }] } }, recaps: [{ number: 0, recap: "序" }] } })], answers: { "planner:chapter": () => CHAPTER } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /chapter 1's outline rewritten from the owner's note \(version 1\)/);
  const payload = site.calls.run[0].payload;
  assert.equal(payload.previous.owner_note, "第三集再緊一點");
  assert.deepEqual(payload.chapter_range, [1, 10]);
  assert.equal(payload.chapter_outline.title, "第一篇");
  assert.deepEqual(payload.recaps, [{ number: 0, recap: "序" }]);
  assert.equal(site.calls.docs[0].chapter_number, 1);
});

test("the planner's document payload carries the setting and the outline, and a bad answer twice is tried again next run", async () => {
  const box = sandbox();
  const site = fakeSite({ jobs: [job("outline")], answers: { "planner:outline": () => ({ body_md: "# x", body_json: { chapters: [] } }) } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  const payload = documentPayload(automation, job("outline"));
  assert.equal(payload.setting.body_json.characters.length, 2);
  assert.deepEqual(payload.chapter_ranges, [[1, 10], [11, 20], [21, 25]]);
  assert.match(await planDocument(automation, job("outline")), /could not write the series outline \(body_json.chapters must list exactly 3 chapters/);
  assert.equal(site.calls.docs.length, 0);
  assert.equal(automation.halted, true, "the run ends; the next one asks again");
});

test("a series step finds nothing on a site without the route, and nothing while the drama is off", async () => {
  const box = sandbox();
  const site = fakeSite();
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const off = new Automation(ctx, automationClient(ctx), { ...site.settings, drama: { drama_enabled: false } });
  assert.equal(await seriesStep(off), null);
  const gone = new Automation(ctx, automationClient({ ...ctx, fetch: async () => Response.json({ code: "not_found", detail: "no" }, { status: 404 }) }), site.settings);
  assert.equal(await seriesStep(gone), null);
});

test("an episode is started from the chapter outline, written from the cast word for word, checked for its beats, and read by the owner before the sheets", async () => {
  const box = sandbox();
  const slug = "wenjian-e001";
  const example = dramaFixture();
  const script = () => {
    // The writer names the cast, out of order and with a drifted appearance: settle restores the book's.
    const video = structuredClone(example);
    video.characters = [
      { id: "shen-lan", name: "沈瀾", appearance: "wrong", voice: { provider: "gemini", name: "Kore" } },
      { id: "chu-ying", name: "楚英", appearance: "wrong too", voice: { provider: "gemini", name: "Sulafat" } },
    ].reverse();
    for (const scene of video.scenes) {
      if (scene.data?.characters) scene.data.characters = scene.data.characters.map((id) => (id === "jingwei" ? "shen-lan" : "chu-ying"));
      for (const line of scene.lines) if (line.speaker && line.speaker !== "narrator") line.speaker = line.speaker === "jingwei" ? "shen-lan" : "chu-ying";
    }
    if (video.thumbnail?.data) delete video.thumbnail.data.shot;
    return { video: { ...video, slug }, claims: "原創\n", lexicon_additions: {} };
  };
  let fixes = 0;
  const answers = {
    "writer:episode": (body) => {
      if (body.payload.fix) {
        fixes += 1;
        const video = structuredClone(body.payload.video);
        video.scenes[0].lines[0].text = `${video.scenes[0].lines[0].text}！`;
        return { video };
      }
      return script();
    },
    "verifier:episode": () => ({ report: "# 連貫性與張力第 1 輪\n", video: null, claims: "原創\n", changed_facts: 0, coverage: { hook: "有", conflict: "有", turn: "弱", cliffhanger: "有" }, problems: ["轉折來得太晚"], similar_works: [] }),
    listener: (body) => ({ video: body.payload.video, edits: [] }),
  };
  const site = fakeSite({ jobs: [job("episode", { episode: { ...beats(1), chapter_number: 1, status: "ready", slug: null, beats: beats(1) } })], answers });
  const clock = { now: Date.parse("2026-09-27T01:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const dir = path.join(box.root, "docs", "videos", slug);
  const workdir = path.join(box.work, slug);
  const runs = [];
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    if (command[0] === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      const list = site.reviewsOf(slug);
      if (gate === "script") list.unshift({ id: `script-${list.length}`, gate: "script", status: "pending", choice: null, note: null, decided_at: null, content_sha256: sha(path.join(dir, "script.md")), payload: {} });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /series wenjian: episode 1 \(wenjian-e001\) started from the chapter outline/);
  assert.deepEqual(site.calls.episodes, [{ series: "wenjian", number: 1, action: "start", slug }]);
  const brief = readFileSync(path.join(dir, "brief.md"), "utf8");
  assert.match(brief, /## 故事前提[\s\S]*## 角色[\s\S]*沈瀾[\s\S]*## 站主觀點[\s\S]*## 幕[\s\S]*鐘聲[\s\S]*## 大綱\n+### 選項 A：第 1 集/);
  const info = readJson(path.join(dir, "series.json"));
  assert.deepEqual(info.characters.map((character) => character.id), ["chu-ying", "shen-lan"]);
  assert.equal(info.beats.hook, "鐘聲");
  assert.equal(info.next_logline, "L2");
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "outline"), "no outline to pick: the chapter was approved");
  assert.equal(site.calls.reports.at(-1).series_slug, "wenjian");
  assert.equal(site.calls.reports.at(-1).episode_number, 1);
  const state = () => automatedVideos(box.work).find((each) => each.slug === slug);
  assert.deepEqual(state().series, { slug: "wenjian", episode: 1, chapter: 1, genre: "xianxia-bonds", lead: "dual-male", visual_tier: "clips", compilation: false, hands_off: false });
  assert.deepEqual(state().notes, ["series note: 旁白慢一點"]);

  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.equal(writer.variant, "episode");
  assert.equal(writer.payload.beats.hook, "鐘聲");
  assert.equal(writer.payload.cast.length, 2);
  assert.equal(writer.payload.series.tone, "dual-male-leads-subtext");
  assert.match(writer.instructions, /EPISODE OF A LONG SERIES/);
  const written = readJson(path.join(dir, "video.json"));
  assert.deepEqual(written.series, { slug: "wenjian", episode: 1, chapter: 1 });
  assert.deepEqual(written.characters.map((character) => [character.id, character.appearance]), CAST.slice().sort((a, b) => (a.id < b.id ? -1 : 1)).map((character) => [character.id, character.appearance]), "the book's cast, word for word, by id");

  assert.match(await automation.step(), /fact-check round 1/);
  const verifier = site.calls.run.find((call) => call.stage === "verifier");
  assert.equal(verifier.variant, "episode");
  assert.equal(verifier.payload.beats.turn, "轉折");
  assert.deepEqual(readJson(path.join(workdir, "review", "script-check.json")).coverage, { hook: "有", conflict: "有", turn: "弱", cliffhanger: "有" });
  assert.match(await automation.step(), /listener edit/);

  assert.match(await automation.step(), /screenplay sent to \/admin\/videos/);
  assert.ok(existsSync(path.join(dir, "script.md")));
  assert.equal(await automation.step(), null, "the owner reads it");
  Object.assign(site.reviewsOf(slug)[0], { status: "rejected", note: "沈瀾第一句太直白" });
  assert.match(await automation.step(), /screenplay rewritten after the owner's note \(round 1\); it is checked again/);
  assert.equal(fixes, 1);
  assert.deepEqual(site.calls.run.at(-1).payload.fix, { kind: "script", targets: [], problems: ["沈瀾第一句太直白"], owner_note: "沈瀾第一句太直白" });
  assert.match(await automation.step(), /fact-check round 2/);
  assert.match(await automation.step(), /listener edit/);
  assert.match(await automation.step(), /screenplay sent to \/admin\/videos/);
  assert.equal(site.reviewsOf(slug).filter((review) => review.gate === "script").length, 2, "a rewritten script is a new review");
  Object.assign(site.reviewsOf(slug)[0], { status: "approved", note: null, decided_at: "2026-09-27T02:00:00Z" });
  assert.match(await automation.step(), /the owner approved the screenplay/);
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "script"));
  assert.equal(runs.filter((run) => run.startsWith("look")).length, 0, "no image was paid for before the owner read the script");
});

test("a series keeps the sheets the owner chose, and the next episode reuses them unless the character changed", () => {
  const box = sandbox("wenjian-e001", "drama");
  const doc = { ...dramaFixture(), slug: "wenjian-e001", series: { slug: "wenjian", episode: 1, chapter: 1 } };
  const workdir = box.workdir;
  mkdirSync(path.join(workdir, "characters", "jingwei"), { recursive: true });
  writeFileSync(path.join(workdir, "characters", "jingwei", "001.png"), "png-a");
  const manifest = { look_hash: "h", characters: { jingwei: { candidates: [{ n: 1, seed: 1, file: "characters/jingwei/001.png", sha256: "a".repeat(64), judge: { overall: 9, passed: true, problems: [] } }] }, yandi: { candidates: [] } } };
  assert.equal(keepSheets({ workBase: box.work, workdir, seriesSlug: "wenjian", doc, manifest, chosen: { jingwei: 1, yandi: 2 }, now: new Date("2026-09-27T00:00:00Z") }), 1, "only the chosen sheet that exists is kept");
  const jingwei = doc.characters.find((character) => character.id === "jingwei");
  const store = readStore(box.work, "wenjian");
  assert.equal(store.sheets[sheetKey(jingwei, doc.look)].from, "wenjian-e001");

  const next = path.join(box.work, "wenjian-e002");
  const reused = reuseSheets({ workBase: box.work, workdir: next, seriesSlug: "wenjian", characters: doc.characters, look: doc.look });
  assert.deepEqual(Object.keys(reused.reused), ["jingwei"]);
  assert.deepEqual(reused.missing.map((character) => character.id), ["yandi"]);
  assert.equal(readFileSync(path.join(next, reused.reused.jingwei.file), "utf8"), "png-a");
  assert.equal(reused.reused.jingwei.judge.overall, 9);
  const changed = reuseSheets({ workBase: box.work, workdir: next, seriesSlug: "wenjian", characters: [{ ...jingwei, appearance: `${jingwei.appearance}, a scar` }], look: doc.look });
  assert.deepEqual(Object.keys(changed.reused), [], "a changed appearance is drawn anew");

  const settled = settle({ ...dramaFixture(), characters: [...dramaFixture().characters].reverse() }, { slug: "wenjian-e002", settings: { voice: { provider: "gemini", name: "Sulafat" }, drama: {} }, sourceGuide: null, root: box.root, format: "drama", series: { slug: "wenjian", episode: 2, chapter: 1 }, cast: doc.characters });
  assert.deepEqual(settled.characters.map((character) => character.id), ["jingwei", "yandi"]);
  assert.deepEqual(settled.series, { slug: "wenjian", episode: 2, chapter: 1 });
});

test("a story bible has the cast, the acts and one outline, and only a one-off has one", () => {
  const bibleJob = job("bible", { series: ONE_OFF, chapter_number: null, context: { ...job("bible").context, series: ONE_OFF, setting: null, mysteries: [] } });
  assert.equal(documentProblem("bible", BIBLE, bibleJob), null);
  assert.match(documentProblem("bible", { body_md: "x", body_json: { characters: ONE_OFF_CAST, outline: OUTLINE } }, bibleJob), /acts/);
  assert.match(documentProblem("bible", { body_md: "x", body_json: { characters: ONE_OFF_CAST, acts: [{}], outline: "x" } }, bibleJob), /outline/);
  assert.match(documentProblem("bible", { body_md: "x", body_json: { acts: [{}], outline: OUTLINE } }, bibleJob), /characters/);
  assert.ok(isOneOff(ONE_OFF) && !isOneOff(SERIES));
  const brief = episodeBrief(ONE_OFF, oneOffEpisode("ready"), castFrom(BIBLE.body_json), OUTLINE);
  assert.match(brief, /^# 精衛填海\n/, "a one-off's brief is the story's, not episode 1 of a series");
  assert.match(brief, /一句話：一隻鳥要填平淹死她的海[\s\S]*## 角色\n- jingwei 精衛[\s\S]*## 大綱\n\n### 選項 A：精衛填海/);
  assert.deepEqual(parseSubject("chapter:3"), ["chapter", 3]);
  assert.deepEqual(parseSubject("script:12"), ["script", 12]);
  assert.deepEqual(parseSubject("bible"), ["bible", 0]);
  assert.throws(() => parseSubject("boss"));
  assert.equal(answerProblem({ reply: "好", revised: null }), null);
  assert.match(answerProblem({ revised: null }), /no reply/);
  assert.match(answerProblem({ reply: "好", revised: "x" }), /revised must be null or an object/);
  assert.match(unusableReply("沒有 JSON"), /沒有給出可用的回覆（沒有 JSON）/);
});

test("a one-off goes from its story bible to the script gate: the bible is planned, the episode is drafted from it with the drama prompts, and the owner reads the screenplay", async () => {
  const box = sandbox();
  const slug = "one-off-7a1b2c3d-e001";
  const example = dramaFixture();
  const answers = {
    "planner:bible": () => BIBLE,
    writer: (body) => (body.payload.fix ? { video: structuredClone(body.payload.video) } : { video: { ...structuredClone(example), slug }, claims: "原創：山海經北山經\n", lexicon_additions: {} }),
    verifier: () => ({ report: "# 連貫性第 1 輪\n", video: null, claims: "原創\n", changed_facts: 0 }),
    listener: (body) => ({ video: body.payload.video, edits: [] }),
  };
  const site = fakeSite({ jobs: [job("bible", { series: ONE_OFF, chapter_number: null, context: { ...job("bible").context, series: ONE_OFF, setting: null, mysteries: [] } }), job("episode", { series: { ...ONE_OFF, status: "active", episodes_ready: 1 }, episode: oneOffEpisode("ready") })], answers });
  const clock = { now: Date.parse("2026-09-27T01:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const dir = path.join(box.root, "docs", "videos", slug);
  const workdir = path.join(box.work, slug);
  const runs = [];
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    if (command[0] === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      const list = site.reviewsOf(slug);
      if (gate === "script") list.unshift({ id: `script-${list.length}`, gate: "script", status: "pending", choice: null, note: null, decided_at: null, content_sha256: sha(path.join(dir, "script.md")), payload: {} });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /series one-off-7a1b2c3d: the story bible planned \(version 1\); it waits for the owner/);
  assert.equal(site.calls.run[0].variant, "bible");
  assert.match(site.calls.run[0].instructions, /STORY BIBLE/);
  assert.equal(site.calls.run[0].payload.series.premise, ONE_OFF.premise);
  assert.deepEqual(site.calls.docs.map((doc) => [doc.kind, doc.chapter_number]), [["bible", 0]]);

  // The owner approved the bible: the site's next job is the episode, with the bible as the setting.
  assert.match(await automation.step(), /one-off one-off-7a1b2c3d: one-off-7a1b2c3d-e001 started from the approved story bible/);
  assert.deepEqual(site.calls.episodes, [{ series: ONE_OFF.slug, number: 1, action: "start", slug }]);
  const brief = readFileSync(path.join(dir, "brief.md"), "utf8");
  assert.match(brief, /^# 精衛填海\n[\s\S]*## 角色\n- jingwei 精衛[\s\S]*## 大綱\n\n### 選項 A：精衛填海/);
  assert.deepEqual(readJson(path.join(dir, "series.json")).characters.map((character) => character.id), ["jingwei", "yandi"]);
  const outline = readApprovals(workdir).approvals.find((entry) => entry.gate === "outline");
  assert.equal(outline.note, "依故事聖經", "no outline to pick: the owner approved the bible");
  const state = () => automatedVideos(box.work).find((each) => each.slug === slug);
  assert.deepEqual(state().series, { slug: ONE_OFF.slug, episode: 1, chapter: 1, kind: "one-off" });
  assert.equal(state().title, "精衛");
  assert.equal(site.calls.reports.at(-1).series_slug, ONE_OFF.slug);

  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.equal(writer.variant, undefined, "a one-off is written with the drama prompts, not a long series' episode prompt");
  assert.match(writer.instructions, /"format": "drama"/);
  assert.equal(writer.payload.cast.length, 2, "the bible's cast travels as an episode's does");
  assert.equal(writer.payload.setting_md, BIBLE.body_md);
  assert.deepEqual(readJson(path.join(dir, "video.json")).characters.map((character) => character.appearance), ONE_OFF_CAST.map((character) => character.appearance), "the bible's cast, word for word");
  assert.match(await automation.step(), /fact-check round 1/);
  assert.equal(site.calls.run.find((call) => call.stage === "verifier").variant, undefined);
  assert.match(await automation.step(), /listener edit/);
  assert.match(await automation.step(), /screenplay sent to \/admin\/videos/);
  assert.equal(await automation.step(), null, "the owner reads the screenplay");
  assert.equal(runs.filter((run) => run.startsWith("look")).length, 0, "no image was paid for before the owner read the script");
  Object.assign(site.reviewsOf(slug)[0], { status: "approved", note: null, decided_at: "2026-09-27T02:00:00Z" });
  assert.match(await automation.step(), /the owner approved the screenplay/);
});

test("the planner answers the owner's question on a document with a reply alone, and a request for a change with a new version", async () => {
  const box = sandbox();
  const bible = { id: "b1", kind: "bible", chapter_number: 0, version: 1, ...BIBLE, status: "review", note: null, decided_at: null, created_at: "2026-09-27T02:00:00Z", unanswered: 1 };
  const question = messageJob("bible", "第二幕為什麼要死一個人？", { doc: bible });
  const change = messageJob("bible", "把炎帝改成沉默寡言。", { doc: bible, thread: [question.message, { ...question.message, id: "m-reply", author: "planner", body_md: "因為…", answered_at: "2026-09-27T03:01:00Z" }] });
  const revised = structuredClone(BIBLE);
  revised.body_json.characters[1].personality = "沉默寡言";
  const site = fakeSite({
    // The series job is asked only after the threads are answered: none here.
    messages: [question, change, messageJob("bible", "再給我兩個開場。", { doc: bible })],
    answers: {
      "planner:discuss": (body) => {
        if (body.payload.message.includes("為什麼")) return { reply: "因為第二幕要有代價。", revised: null };
        if (body.payload.message.includes("沉默")) return { reply: "改了炎帝的性格：沉默寡言。", revised };
        return { reply: "開場 A…開場 B…", revised: { body_md: "# x", body_json: {} } };
      },
    },
  });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T03:00:00Z") });
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  const payload = documentDiscussionPayload(automation, question);
  assert.equal(payload.kind, "bible");
  assert.equal(payload.document.version, 1);
  assert.equal(payload.thread.length, 1);
  assert.equal(payload.series.kind, "one-off");
  assert.equal(payload.setting, undefined, "the bible is the top document: nothing above it");
  assert.equal(revisedDocumentProblem(null, question), null);
  assert.match(revisedDocumentProblem({ body_md: "x", body_json: {} }, question), /characters/);

  assert.match(await automation.step(), /series one-off-7a1b2c3d: the planner answered the owner on bible$/);
  assert.equal(site.calls.run[0].variant, "discuss");
  assert.equal(site.calls.run[0].stage, "planner");
  assert.match(site.calls.run[0].instructions, /OWNER'S LINE/);
  assert.deepEqual(site.calls.answers[0], { id: question.message.id, reply_md: "因為第二幕要有代價。", revised: null }, "a question gets a reply and no version");

  assert.match(await automation.step(), /the planner answered the owner on bible with version 2 for the owner/);
  assert.equal(site.calls.answers[1].id, change.message.id);
  assert.equal(site.calls.answers[1].reply_md, "改了炎帝的性格：沉默寡言。");
  assert.equal(site.calls.answers[1].revised.body_json.characters[1].personality, "沉默寡言");
  assert.equal(site.calls.run[1].payload.thread.length, 3, "the whole thread travels with the line");

  // A revision the checks refuse is dropped and the reply says so; the thread is still answered.
  assert.match(await automation.step(), /the planner answered the owner on bible$/);
  assert.equal(site.calls.answers[2].revised, null);
  assert.match(site.calls.answers[2].reply_md, /^開場 A…開場 B…\n\n（新版本沒有存下來：body_json.characters must list the cast）$/);
  assert.equal(await automation.step(), null, "every thread answered, every series waiting");
});

test("a model that gives nothing usable on a thread is answered for, and the thread waits for the owner", async () => {
  const box = sandbox();
  const site = fakeSite({
    messages: [messageJob("bible", "問題一"), messageJob("bible", "問題二")],
    answers: { "planner:discuss": (body) => (body.payload.message === "問題一" ? "not json at all" : { revised: null }) },
  });
  // The fake site wraps the planner's answer as JSON text; make the first one plain text instead.
  const fetchImpl = async (url, init) => {
    const response = await site.fetchImpl(url, init);
    if (!url.endsWith("/automation/run")) return response;
    const body = await response.json();
    if (body.text === JSON.stringify("not json at all")) return Response.json({ ...body, text: "not json at all" });
    return Response.json(body);
  };
  const { ctx } = context(box, fetchImpl, { now: Date.parse("2026-09-27T03:00:00Z") });
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /the planner gave no usable answer on bible \(planner answered something that is not JSON/);
  assert.match(site.calls.answers[0].reply_md, /^模型這一輪沒有給出可用的回覆（planner answered something that is not JSON/);
  assert.equal(site.calls.answers[0].revised, null);
  assert.match(await automation.step(), /the planner gave no usable answer on bible \(the answer has no reply text\)/);
  assert.equal(site.calls.answers.length, 2, "each line is answered once; nothing is retried");
  assert.equal(automation.halted, false, "the run goes on: the owner was told");
});

test("the writer answers the owner on a screenplay: a question gets a reply, a change rewrites video.json, and the script is checked, heard and sent again", async () => {
  const box = sandbox();
  const slug = "wenjian-e001";
  const example = dramaFixture();
  const episode = { ...beats(1), chapter_number: 1, status: "started", slug, beats: beats(1) };
  const script = () => {
    const video = structuredClone(example);
    video.characters = [
      { id: "shen-lan", name: "沈瀾", appearance: "wrong", voice: { provider: "gemini", name: "Kore" } },
      { id: "chu-ying", name: "楚英", appearance: "wrong too", voice: { provider: "gemini", name: "Sulafat" } },
    ];
    for (const scene of video.scenes) {
      if (scene.data?.characters) scene.data.characters = scene.data.characters.map((id) => (id === "jingwei" ? "shen-lan" : "chu-ying"));
      for (const line of scene.lines) if (line.speaker && line.speaker !== "narrator") line.speaker = line.speaker === "jingwei" ? "shen-lan" : "chu-ying";
    }
    if (video.thumbnail?.data) delete video.thumbnail.data.shot;
    return { video: { ...video, slug }, claims: "原創\n", lexicon_additions: {} };
  };
  const answers = {
    // A lint fix gets nothing usable, so a revision lint refuses stays refused.
    "writer:episode": (body) => (body.payload.lint_errors ? {} : script()),
    "verifier:episode": () => ({ report: "# 連貫性與張力\n", video: null, claims: "原創\n", changed_facts: 0, coverage: { hook: "有", conflict: "有", turn: "有", cliffhanger: "有" }, problems: [], similar_works: [] }),
    listener: (body) => ({ video: body.payload.video, edits: [] }),
    "writer:discuss": (body) => {
      if (body.payload.message.includes("為什麼")) return { reply: "因為沈瀾此時不能說破。", revised: null };
      if (body.payload.message.includes("刪掉")) {
        const video = structuredClone(body.payload.video);
        video.scenes[0].lines = [];
        return { reply: "刪了第一場所有台詞。", revised: { video } };
      }
      const video = structuredClone(body.payload.video);
      video.scenes[0].lines[0].text = `${video.scenes[0].lines[0].text}！`;
      return { reply: "第一句改成感嘆句。", revised: { video } };
    },
  };
  const site = fakeSite({ jobs: [job("episode", { episode: { ...episode, status: "ready", slug: null } })], answers });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T01:00:00Z") });
  const dir = path.join(box.root, "docs", "videos", slug);
  const pushes = [];
  ctx.runCommand = async (command, runCtx) => {
    if (command[0] === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      pushes.push(gate);
      const list = site.reviewsOf(slug);
      if (gate === "script") list.unshift({ id: `script-${list.length}`, gate: "script", status: "pending", choice: null, note: null, decided_at: null, content_sha256: sha(path.join(dir, "script.md")), payload: {} });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  for (const expected of [/started from the chapter outline/, /script drafted/, /fact-check round 1/, /listener edit/, /screenplay sent/]) assert.match(await automation.step(), expected);
  const state = () => automatedVideos(box.work).find((each) => each.slug === slug);
  const firstLine = () => readJson(path.join(dir, "video.json")).scenes[0].lines[0].text;
  const before = firstLine();

  // The owner's lines arrive one per round; a video that has work of its own moves first.
  const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
  const queue = [asked, messageJob("script:1", "第一句改成感嘆句。", { series: SERIES, episode }), messageJob("script:1", "刪掉第一場所有台詞。", { series: SERIES, episode }), messageJob("script:2", "第二集呢？", { series: SERIES, episode: { ...episode, number: 2, slug: "wenjian-e002" } })];
  const fetchWithMessages = async (url, init) => {
    if (new URL(url).pathname === "/api/video/automation/series/messages/next") return Response.json({ job: queue.shift() ?? null });
    return site.fetchImpl(url, init);
  };
  const talking = new Automation({ ...ctx, fetch: fetchWithMessages }, automationClient({ ...ctx, fetch: fetchWithMessages }), site.settings);
  talking.refs = smallRefs;

  // A question: a reply, nothing rewritten, the script still waits for the owner.
  assert.match(await talking.step(), /wenjian-e001: the writer answered the owner on script:1$/);
  const discuss = site.calls.run.at(-1);
  assert.equal(discuss.stage, "writer");
  assert.equal(discuss.variant, "discuss");
  assert.match(discuss.instructions, /OWNER'S LINE/);
  assert.equal(discuss.payload.message, "沈瀾為什麼不回答？");
  assert.ok(discuss.payload.screenplay.length > 0, "the writer reads the screenplay as the owner does");
  assert.equal(discuss.payload.cast.length, 2);
  assert.deepEqual(site.calls.answers.at(-1), { id: asked.message.id, reply_md: "因為沈瀾此時不能說破。", revised: null });
  assert.equal(firstLine(), before);
  assert.equal(state().verified, true);

  // A change: video.json is rewritten (every id kept), and the following rounds check it, hear it and send it up anew.
  assert.match(await talking.step(), /the writer answered the owner on script:1; the screenplay is rewritten and will be checked, heard and sent again/);
  assert.equal(firstLine(), `${before}！`);
  assert.deepEqual(site.calls.answers.at(-1), { id: "m-script:1-1", reply_md: "第一句改成感嘆句。", revised: null });
  assert.equal(state().verified, false);
  assert.equal(state().listener_done, false);
  assert.ok(state().notes.some((note) => note.startsWith("script discussed: 第一句改成感嘆句")));
  assert.match(await talking.step(), /fact-check round 2/);
  assert.match(await talking.step(), /listener edit/);
  assert.match(await talking.step(), /screenplay sent to \/admin\/videos/);
  assert.deepEqual(pushes, ["script", "script"]);
  assert.equal(site.reviewsOf(slug).filter((review) => review.gate === "script").length, 2, "the rewritten screenplay is a new review");

  // A change lint refuses is put back, and the reply says so.
  assert.match(await talking.step(), /the writer answered the owner on script:1$/);
  assert.equal(firstLine(), `${before}！`, "the refused revision left the script as it was");
  assert.match(site.calls.answers.at(-1).reply_md, /^刪了第一場所有台詞。\n\n（新版本沒有存下來：/);
  assert.equal(state().verified, true, "nothing changed, nothing to check again");

  // A thread about an episode this worker does not have is answered for.
  assert.match(await talking.step(), /series wenjian: no video for script:2 here; the owner is told/);
  assert.match(site.calls.answers.at(-1).reply_md, /這台工人沒有 wenjian-e002 的劇本/);
  assert.equal(await talking.step(), null, "every line answered; the screenplay waits for the owner");
});

// A binge series (docs/videos/BINGE.md): hands-off, a retention genre, a compilation at the end.
const BINGE = { ...SERIES, slug: "rebirth", title: "她磨好了刀", genre: "rebirth-revenge", lead: "female", visual_tier: "clips", compilation: true, hands_off: true, total_minutes: 30, planned_episodes: 10, episodes_per_chapter: 10, chapters: 1, tone: "hetero-leads" };
const retentionBeats = (number, changes = {}) => ({
  ...beats(number, number % 2 ? "danger" : "reveal"),
  hook_type: number % 2 ? "danger" : "question",
  lead_arc: number % 2 ? "wins" : "mixed",
  satisfaction: [{ beat: "opening", type: "face_slap" }, { beat: "ending", type: "reversal" }],
  payoffs: number % 3 === 0 ? ["m1"] : [],
  ...changes,
});
const RETENTION_CHAPTER = { body_md: "# 第一篇", body_json: { chapter: 1, episodes: Array.from({ length: 10 }, (_, index) => retentionBeats(index + 1)) } };
const verdict = (kind, changes = {}) => ({ verdicts: Object.fromEntries({ setting: ["originality", "conflict_engine", "genre_fit", "cast_playable"], outline: ["originality", "escalation", "midpoint_reveal", "chapter_turns", "satisfaction_schedule"], chapter: ["originality", "tension_rules", "hooks", "satisfaction", "alternation", "escalation"] }[kind].map((key) => [key, "有"])), problems: [], similar_works: [], notes: "ok", ...changes });

test("a retention genre's chapter outline names the hook type, the lead's arc and the satisfaction beats, as the site demands", () => {
  const binge = job("chapter", { series: BINGE });
  assert.equal(documentProblem("chapter", RETENTION_CHAPTER, binge), null);
  assert.equal(documentProblem("chapter", CHAPTER, job("chapter")), null, "the classic series keeps its rules");
  const bare = structuredClone(RETENTION_CHAPTER);
  delete bare.body_json.episodes[2].hook_type;
  assert.match(documentProblem("chapter", bare, binge), /episode 3 needs hook_type/);
  const few = structuredClone(RETENTION_CHAPTER);
  few.body_json.episodes[3].satisfaction.pop();
  assert.match(documentProblem("chapter", few, binge), /episode 4 needs at least 2 satisfaction beats/);
  const late = structuredClone(RETENTION_CHAPTER);
  late.body_json.episodes[4].satisfaction = [{ beat: "ending", type: "reversal" }, { beat: "ending", type: "face_slap" }];
  assert.match(documentProblem("chapter", late, binge), /first half/);
  const odd = structuredClone(RETENTION_CHAPTER);
  odd.body_json.episodes[5].satisfaction[0].type = "kiss";
  assert.match(documentProblem("chapter", odd, binge), /genre's types/);
  const suffering = structuredClone(RETENTION_CHAPTER);
  suffering.body_json.episodes[1].lead_arc = "suffers";
  suffering.body_json.episodes[2].lead_arc = "suffers";
  assert.match(documentProblem("chapter", suffering, binge), /episodes 2 and 3 both leave the lead suffering/);
  const dry = structuredClone(RETENTION_CHAPTER);
  for (const episode of dry.body_json.episodes) episode.payoffs = [];
  assert.match(documentProblem("chapter", dry, binge), /pay nothing off/);
  const payload = documentPayload({ reference: () => smallRefs, dramaPayload: () => ({ drama_settings: {} }) }, binge);
  assert.equal(payload.series.genre, "rebirth-revenge");
  assert.equal(payload.genre_spec.label, "重生復仇");
  assert.match(instructionsFor("planner", "drama", "", "chapter", "", BINGE), /Genre and retention[\s\S]*Retention rules[\s\S]*Compilation mode/);
  assert.doesNotMatch(instructionsFor("planner", "drama", "", "chapter", "", SERIES), /Retention rules/, "the classic series gets no retention section");
  assert.doesNotMatch(instructionsFor("listener", "drama", "", null, "", BINGE), /Genre and retention/, "the listener needs no genre");
});

test("the retention numbers are measured on the script's estimated timeline, and the verdict mirrors the site's rule", () => {
  const video = dramaFixture();
  const ids = [...eachLine(video)].map(({ line }) => line.id);
  const numbers = retentionNumbers(video, { hook_line: ids[0], satisfaction_lines: [ids[1], ids[3]], cliffhanger_line: ids.at(-1) });
  assert.ok(numbers.hook_seconds > 0 && numbers.hook_seconds < 15, `the hook ends at ${numbers.hook_seconds} s`);
  // The hook is measured where its words end, without the pause after the line or the gap to the next shot.
  const hookLine = estimateTimeline(video).lines.find((line) => line.id === ids[0]);
  assert.equal(numbers.hook_seconds, Number(frameToSeconds(hookLine.start_frame + framesFor(hookLine.audio_samples)).toFixed(1)));
  assert.ok(numbers.hook_seconds < frameToSeconds(hookLine.end_frame));
  assert.equal(numbers.satisfaction.count, 2);
  assert.equal(numbers.satisfaction.first_seconds, numbers.satisfaction.positions[0]);
  assert.equal(numbers.cliffhanger_last, true);
  assert.equal(retentionNumbers(video, { hook_line: ids[0], satisfaction_lines: [], cliffhanger_line: ids[0] }).cliffhanger_last, false);
  assert.equal(retentionNumbers(video, null), null);

  const passing = { coverage: { hook: "有", conflict: "有", turn: "弱", cliffhanger: "有", satisfaction: "有" }, problems: [], similar_works: [], retention: { hook_seconds: 6.2, satisfaction: { count: 2, first_seconds: 20, positions: [20, 100] }, cliffhanger_last: true } };
  assert.deepEqual(scriptVerdict(passing, BINGE), { passed: true, problems: [] });
  assert.deepEqual(scriptVerdict({ ...passing, retention: null }, SERIES), { passed: true, problems: [] }, "the classic series has no timing rule");
  assert.match(scriptVerdict({ ...passing, retention: null }, BINGE).problems.join(" "), /named no hook/);
  assert.match(scriptVerdict({ ...passing, retention: { ...passing.retention, hook_seconds: 12 } }, BINGE).problems.join(" "), /hook line ends at 12 s; shorten it/);
  // A hook_line the script does not have measures as null; the site refuses a null, so the worker must too.
  assert.match(scriptVerdict({ ...passing, retention: { ...passing.retention, hook_seconds: null } }, BINGE).problems.join(" "), /hook_line is not a line of the script/);
  assert.match(scriptVerdict({ ...passing, retention: { ...passing.retention, satisfaction: { count: 0, first_seconds: null, positions: [] } } }, BINGE).problems.join(" "), /only 0 satisfaction beats[\s\S]*satisfaction_lines are not lines/);
  assert.match(scriptVerdict({ ...passing, retention: { ...passing.retention, cliffhanger_last: false } }, BINGE).problems.join(" "), /cliffhanger is not the last line/);
  assert.match(scriptVerdict({ ...passing, coverage: { ...passing.coverage, turn: "無" } }, SERIES).problems.join(" "), /turn is missing/);
  assert.match(scriptVerdict({ ...passing, coverage: { ...passing.coverage, hook: "弱" } }, SERIES).problems.join(" "), /more than one beat/);
  assert.match(scriptVerdict({ ...passing, similar_works: ["某作的門派"] }, SERIES).problems.join(" "), /resembles an existing work/);
  assert.match(scriptVerdict(null, SERIES).problems.join(" "), /no verdict on the hook/);
});

test("a hands-off series' document goes through the checker and is filed with the verdict; the site's decision is reported", async () => {
  const box = sandbox();
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const decisions = [];
  const site = fakeSite({
    jobs: [job("setting", { series: BINGE }), job("setting", { series: BINGE }), job("setting", { series: BINGE })],
    answers: {
      "planner:setting": () => SETTING,
      "verifier:series-doc": (body) => (decisions.length === 0 ? verdict("setting") : decisions.length === 1 ? verdict("setting", { problems: ["反派沒有動機"] }) : { nonsense: true }),
    },
    decide: (body) => {
      decisions.push(body.judge ?? null);
      if (!body.judge) return { status: "review", note: null };
      return body.judge.problems.length ? { status: "rejected", note: `[auto] 查核沒過：${body.judge.problems.join("；")}` } : { status: "approved", note: "查核：originality 有，依作品設定自動核准" };
    },
  });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /series rebirth: the setting book planned \(version 1\) and approved on the checker's verdict/);
  const judge = site.calls.run.find((call) => call.variant === "series-doc");
  assert.equal(judge.stage, "verifier");
  assert.equal(judge.payload.kind, "setting");
  assert.deepEqual(judge.payload.document.body_json.characters.map((character) => character.id), CAST.map((character) => character.id));
  assert.match(judge.instructions, /PLANNED DOCUMENT[\s\S]*Genre and retention/);
  assert.deepEqual(site.calls.docs[0].judge, verdict("setting"));
  assert.match(await automation.step(), /the checker sent it back for a rewrite \(\[auto\] 查核沒過：反派沒有動機\)/);
  assert.deepEqual(site.calls.docs[1].judge.problems, ["反派沒有動機"]);
  assert.match(await automation.step(), /it waits for the owner on \/admin\/videos/, "no usable verdict: the owner decides, as on a classic series");
  assert.equal(site.calls.docs[2].judge, undefined);
  assert.equal(site.calls.run.filter((call) => call.variant === "series-doc").length, 4, "the checker is asked twice before the document is left to the owner");
});

test("a compilation the site refuses to start ends the run with the site's reason instead of failing every round", async () => {
  const box = sandbox();
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const job = { kind: "compilation", series: { ...BINGE, status: "finished" }, chapter_number: null, episode: null, previous: null, rewrites_left: 0, context: null };
  const site = fakeSite({ jobs: [job], series: { ...BINGE, status: "finished" }, compilation: { refuse: { code: "video_drama_request_slug_taken", detail: "rebirth-full 已經是另一支影片" } } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /series rebirth: the site refused to start the compilation rebirth-full: rebirth-full 已經是另一支影片/);
  assert.equal(automation.halted, true);
  assert.equal(existsSync(path.join(box.root, "docs", "videos", "rebirth-full")), false, "no document is written for a compilation the site did not start");
});

test("the compilation of a finished series is started under <series>-full with a document that passes lint", async () => {
  const box = sandbox();
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const episodes = [1, 2, 3].map((number) => ({ number, chapter_number: 1, title: `第 ${number} 集的名字`, logline: `L${number}`, beats: {}, status: "done", slug: `rebirth-e00${number}`, recap: `R${number}`, started_at: null, finished_at: null, video: null }));
  const site = fakeSite({ jobs: [{ kind: "compilation", series: { ...BINGE, status: "finished" }, chapter_number: null, episode: null, previous: null, rewrites_left: 0, context: null }], series: { ...BINGE, status: "finished" }, compilation: { episodes, recaps: episodes.map((episode) => ({ number: episode.number, title: episode.title, recap: episode.recap })) } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /series rebirth: compilation rebirth-full started from 3 episodes/);
  assert.deepEqual(site.calls.compilations, [{ series: "rebirth", action: "start", slug: "rebirth-full" }]);
  const slug = compilationSlug("rebirth");
  const dir = path.join(box.root, "docs", "videos", slug);
  const video = readJson(path.join(dir, "video.json"));
  assert.deepEqual(video.compilation.episodes, ["rebirth-e001", "rebirth-e002", "rebirth-e003"]);
  assert.equal(video.compilation.series, "rebirth");
  assert.equal(video.scenes.length, 4, "a chapter card per episode and the outro");
  // The site serialises the voice with a null model and a "+0%" rate, which lint refuses; the
  // document carries the voice as settle writes it, or the compilation could never leave its first step.
  assert.deepEqual(video.voice, { provider: "gemini", name: "Sulafat", style: "Relaxed" });
  assert.deepEqual(lintCompilation(video).errors, [], "the compilation's document passes lint as written");
  assert.equal(readJson(path.join(dir, "compilation.json")).all_recaps.length, 3);
  const state = automatedVideos(box.work).find((each) => each.slug === slug);
  assert.deepEqual(state.compilation, { series: "rebirth", episodes: ["rebirth-e001", "rebirth-e002", "rebirth-e003"] });
  assert.equal(state.series.slug, "rebirth");
  assert.equal(state.series.episode, undefined, "a compilation is no episode");
  const report = site.calls.reports.at(-1);
  assert.equal(report.series_slug, "rebirth");
  assert.equal(report.episode_number, undefined);
  assert.equal(report.format, "drama");
  assert.match(report.checklist.map((item) => item.label).join(" "), /合集|標題/);
});

test("a hands-off episode's screenplay is fixed from the checker's verdict before anything is sent, then the site approves it on arrival", async () => {
  const box = sandbox();
  const slug = "rebirth-e001";
  const example = dramaFixture();
  const ids = [...eachLine(example)].filter(({ scene }) => scene.template !== "outro").map(({ line }) => line.id);
  const script = () => {
    const video = structuredClone(example);
    video.characters = [
      { id: "shen-lan", name: "沈瀾", appearance: "wrong", voice: { provider: "gemini", name: "Kore" } },
      { id: "chu-ying", name: "楚英", appearance: "wrong too", voice: { provider: "gemini", name: "Sulafat" } },
    ];
    for (const scene of video.scenes) {
      if (scene.data?.characters) scene.data.characters = scene.data.characters.map((id) => (id === "jingwei" ? "shen-lan" : "chu-ying"));
      for (const line of scene.lines) if (line.speaker && line.speaker !== "narrator") line.speaker = line.speaker === "jingwei" ? "shen-lan" : "chu-ying";
    }
    if (video.thumbnail?.data) delete video.thumbnail.data.shot;
    // A compilation episode ends on its cliffhanger; the compilation adds the cards. The
    // fixture's outro carried its third chapter label, so the last shot takes it.
    video.scenes = video.scenes.filter((scene) => scene.template !== "outro");
    video.scenes.at(-1).chapter = "結尾";
    return { video: { ...video, slug }, claims: "原創\n", lexicon_additions: {} };
  };
  let checks = 0;
  const fixes = [];
  const answers = {
    "writer:episode": (body) => {
      if (body.payload.fix) {
        fixes.push(body.payload.fix);
        const video = structuredClone(body.payload.video);
        video.scenes[0].lines[0].text = `${video.scenes[0].lines[0].text}！`;
        return { video };
      }
      return script();
    },
    // The first check finds the cliffhanger buried mid-script; the second finds it last.
    "verifier:episode": () => ({ report: "# 查核\n", video: null, claims: "原創\n", changed_facts: 0, coverage: { hook: "有", conflict: "有", turn: "有", cliffhanger: "有", satisfaction: "有" }, problems: [], similar_works: [], retention: { hook_line: ids[0], satisfaction_lines: [ids[1], ids[2]], cliffhanger_line: checks++ === 0 ? ids[1] : ids.at(-1) } }),
    listener: (body) => ({ video: body.payload.video, edits: [] }),
  };
  const site = fakeSite({ series: BINGE, episodeBeats: (number) => retentionBeats(number), jobs: [{ ...job("episode", { series: BINGE, episode: { ...retentionBeats(1), chapter_number: 1, status: "ready", slug: null, beats: retentionBeats(1) } }), context: { ...job("episode").context, series: BINGE } }], answers });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T01:00:00Z") });
  const dir = path.join(box.root, "docs", "videos", slug);
  const runs = [];
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    if (command[0] === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      // The site approves a passing screenplay on arrival (apps/api: auto_approves_script).
      if (gate === "script") site.reviewsOf(slug).unshift({ id: `script-${runs.length}`, gate: "script", status: "approved", choice: null, note: "查核對照細綱：四個節拍都在、沒有連貫性問題，依作品設定自動核准", decided_at: "2026-09-27T02:00:00Z", content_sha256: sha(path.join(dir, "script.md")), payload: {} });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /episode 1 \(rebirth-e001\) started/);
  assert.match(readFileSync(path.join(dir, "brief.md"), "utf8"), /冷開場：第一句就是鉤子[\s\S]*爽點：opening｜face_slap/);
  const info = readJson(path.join(dir, "series.json"));
  assert.equal(info.visual_tier, "clips");
  assert.equal(info.series.genre, "rebirth-revenge");
  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.match(writer.instructions, /Genre and retention[\s\S]*Retention rules/);
  assert.equal(writer.payload.series.genre, "rebirth-revenge");
  assert.match(await automation.step(), /fact-check round 1/);
  const check = readJson(path.join(box.work, slug, "review", "script-check.json"));
  assert.equal(check.retention.cliffhanger_last, false);
  assert.equal(check.retention.satisfaction.count, 2);
  assert.match(await automation.step(), /listener edit/);
  assert.match(await automation.step(), /screenplay rewritten after the checker's note \(round 1\); it is checked again/);
  assert.equal(fixes.length, 1);
  assert.match(fixes[0].problems[0], /cliffhanger is not the last line/);
  assert.equal(runs.filter((run) => run.startsWith("review-push")).length, 0, "nothing was sent while the checker failed the script");
  assert.match(await automation.step(), /fact-check round 2/);
  assert.equal(readJson(path.join(box.work, slug, "review", "script-check.json")).retention.cliffhanger_last, true);
  assert.match(await automation.step(), /listener edit/);
  assert.match(await automation.step(), /screenplay sent to \/admin\/videos/);
  assert.match(await automation.step(), /the site approved the screenplay/);
  assert.ok(readApprovals(path.join(box.work, slug)).approvals.some((entry) => entry.gate === "script"));
  const state = automatedVideos(box.work).find((each) => each.slug === slug);
  assert.equal(state.prompt_fixes.script, 1);
  assert.equal(state.series.hands_off, true);
});

test("an explainer one-off plans a question's bible with no cast, and its brief has the explainer's sections", () => {
  const explainer = { ...ONE_OFF, title: "雷聲", premise: "為什麼雷聲總比閃電晚到？", style_preset: "flat-explainer" };
  assert.equal(isExplainerOneOff(explainer), true);
  assert.equal(isExplainerOneOff(ONE_OFF), false);
  assert.equal(isExplainerOneOff({ ...SERIES, style_preset: "flat-explainer" }), false, "a long series is never an explainer");
  assert.equal(documentVariant("bible", explainer), "bible-explainer");
  assert.equal(documentVariant("bible", ONE_OFF), "bible");
  assert.equal(documentVariant("setting", SERIES), "setting");
  assert.match(instructionsFor("planner", "drama", "", "bible-explainer"), /BIBLE of ONE explainer episode/);

  const outline = { title: "為什麼雷聲總比閃電晚到？", logline: "光比聲音快太多。", question: "為什麼雷聲總比閃電晚到？", answer: "光比聲音快太多。", reasons: ["光速約每秒三十萬公里", "聲速約每秒三百四十公尺"], hook: "閃電亮了，你數到幾？", closing: "下一題：彩虹為什麼是彎的？", sources: ["https://en.wikipedia.org/wiki/Speed_of_sound"] };
  const bible = { body_md: "# 雷聲\n## 問題\n…\n", body_json: { characters: [], acts: [{ number: 1, title: "光先到", summary: "s", shots: 4 }], outline, music: "輕快", not_doing: [], lexicon: {} } };
  const explainerJob = { ...job("bible"), series: explainer };
  assert.equal(documentProblem("bible", bible, explainerJob), null);
  assert.match(documentProblem("bible", { ...bible, body_json: { ...bible.body_json, characters: ONE_OFF_CAST } }, explainerJob), /must be empty/);
  assert.match(documentProblem("bible", { ...bible, body_json: { ...bible.body_json, outline: { ...outline, answer: "" } } }, explainerJob), /outline\.answer/);
  assert.match(documentProblem("bible", { ...bible, body_json: { ...bible.body_json, outline: { ...outline, sources: ["http://x"] } } }, explainerJob), /https pages/);
  assert.match(documentProblem("bible", bible, { ...job("bible"), series: ONE_OFF }), /characters must list the cast/, "a story one-off still needs its cast");

  const brief = episodeBrief(explainer, { number: 1, title: outline.title, logline: outline.logline }, [], outline);
  assert.deepEqual(checkBrief(brief, "drama", "flat-explainer"), []);
  assert.match(brief, /## 一句答案\n光比聲音快太多。/);
  assert.match(brief, /### 選項 A：為什麼雷聲總比閃電晚到？\n一行說明：光比聲音快太多。\n開場鉤子：「閃電亮了，你數到幾？」/);
  assert.match(brief, /- https:\/\/en\.wikipedia\.org\/wiki\/Speed_of_sound/);
  assert.doesNotMatch(brief, /## 角色/);
});

test("an explainer one-off goes from its question's bible to a narrator-only script with its two Shorts", async () => {
  const box = sandbox();
  const explainer = { ...ONE_OFF, title: "雷聲", premise: "為什麼雷聲總比閃電晚到？", style_preset: "flat-explainer" };
  const slug = "one-off-7a1b2c3d-e001";
  const outline = { title: "為什麼雷聲總比閃電晚到？", logline: "光比聲音快太多。", question: "為什麼雷聲總比閃電晚到？", answer: "光比聲音快太多。", reasons: ["光速約每秒三十萬公里", "聲速約每秒三百四十公尺"], hook: "閃電亮了，你數到幾？", sources: ["https://en.wikipedia.org/wiki/Speed_of_sound"] };
  const bible = { body_md: "# 雷聲\n## 問題\n…\n", body_json: { characters: [], acts: [{ number: 1, title: "光先到", summary: "s", shots: 4 }], outline, music: "輕快", not_doing: [], lexicon: {} } };
  const drafted = JSON.parse(readFileSync(new URL("../core/fixtures/explainer/shorts.json", import.meta.url), "utf8")).map(({ titles, description, scenes }) => ({ titles, description, scenes }));
  const answers = {
    "planner:bible-explainer": () => bible,
    "writer:explainer": () => ({ video: { ...explainerFixture(), slug, look: {} }, claims: "c1｜光速｜https://en.wikipedia.org/wiki/Speed_of_sound｜2026-09-28｜race\n", lexicon_additions: {}, shorts: drafted }),
  };
  const episode = { number: 1, chapter_number: 1, title: outline.title, logline: outline.logline, beats: outline, status: "ready", slug: null, recap: null, started_at: null, finished_at: null, video: null };
  const setting = { id: "b1", kind: "bible", chapter_number: 0, version: 1, ...bible, status: "approved" };
  const oneOffStart = (body) => ({
    request: { id: "explainer-request", premise: explainer.premise, title: "雷聲", source_guide: null, style_preset: "flat-explainer", target_minutes: 8, note: null, status: "started", slug: body.slug, series_slug: explainer.slug, episode_number: 1 },
    episode: { ...episode, status: "started", slug: body.slug },
    context: { series: explainer, setting, outline: null, chapter: null, chapter_number: 1, chapter_range: [1, 1], episode: null, episodes: [episode], recaps: [], mysteries: [] },
  });
  const site = fakeSite({ jobs: [job("bible", { series: explainer, chapter_number: null, context: { ...job("bible").context, series: explainer, setting: null, mysteries: [] } }), job("episode", { series: { ...explainer, status: "active", episodes_ready: 1 }, episode })], answers, oneOffStart });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-28T01:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /the story bible planned \(version 1\)/);
  assert.equal(site.calls.run[0].variant, "bible-explainer");
  assert.match(site.calls.run[0].instructions, /BIBLE of ONE explainer episode/);

  assert.match(await automation.step(), /started from the approved story bible/);
  const dir = path.join(box.root, "docs", "videos", slug);
  assert.match(readFileSync(path.join(dir, "brief.md"), "utf8"), /^# 為什麼雷聲總比閃電晚到？\n\n## 問題\n/);
  const state = automatedVideos(box.work).find((each) => each.slug === slug);
  assert.equal(state.style_preset, "flat-explainer");
  assert.deepEqual(state.source_urls, outline.sources, "the checker reads the pages the bible names");

  assert.match(await automation.step(), /script drafted and passes lint; 2 Shorts drafted/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.equal(writer.variant, "explainer");
  const video = readJson(path.join(dir, "video.json"));
  assert.equal(video.look.preset, "flat-explainer", "the writer cannot drop the explainer preset");
  assert.deepEqual(video.characters, []);
  assert.deepEqual(JSON.parse(readFileSync(shortsFile(slug, box.root), "utf8")).map((short) => short.slug), [`${slug}-short-1`, `${slug}-short-2`]);
  assert.match(await automation.step(), /fact-check round 1/);
  assert.equal(site.calls.run.find((call) => call.stage === "verifier").variant, "explainer");
});
