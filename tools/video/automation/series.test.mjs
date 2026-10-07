import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { runtimePolicyHash, validateAnimePolicy } from "../core/anime-policy.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { dramaFixture, explainerFixture, sandbox, writeAudioFixture } from "../core/fixtures/load.mjs";
import { shortsFile } from "../shorts/episode.mjs";
import { readJson } from "../core/paths.mjs";
import { keepSheets, readStore, reuseSheets, sheetKey } from "../media/series-store.mjs";
import { shotPrompt } from "../media/keyframes.mjs";
import { sheetPrompt } from "../media/look.mjs";
import { resolveLook } from "../core/drama.mjs";
import { planRequests } from "../tts/requests.mjs";
import { AutomationError, automationClient, RUN_PENDING } from "./client.mjs";
import { answerProblem, discussStep, documentDiscussionPayload, parseSubject, revisedDocumentProblem, unusableReply } from "./discuss.mjs";
import { Automation, automatedVideos, DEFER_LIMIT, DEFER_MAX_MS, PENDING_RECHECK_MS, settle } from "./flow.mjs";
import { instructionsFor, SERIES_INSTRUCTIONS } from "./prompts.mjs";
import { eachLine } from "../core/schema.mjs";
import { scriptCheckBinding, scriptCheckMatches } from "../core/script-check.mjs";
import { craftChecks } from "../core/craft.mjs";
import { estimateTimeline, framesFor, frameToSeconds } from "../core/timeline.mjs";
import { lintCompilation } from "../core/compilation.mjs";
import { compilationSlug } from "./compilation.mjs";
import { castFrom, chapterRange, documentInputs, documentKey, documentPayload, documentProblem, documentVariant, episodeBrief, episodeSlug, isExplainerOneOff, isOneOff, LOST_DOCS, planDocument, retentionNumbers, scriptVerdict, seriesStep } from "./series.mjs";
import { checkBrief } from "../core/lint.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"s".repeat(43)}`;
const SITE = "https://site.test";
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

test("the worker refuses changed WAVs before accepting an existing remote audio decision", async () => {
  const box = sandbox("fixture-drama", "drama");
  const timeline = writeAudioFixture(estimateTimeline(dramaFixture()), box.workdir);
  let decisions = 0, pulls = 0;
  const worker = {
    ctx: {}, workdir: () => box.workdir,
    decision: async () => { decisions += 1; return { status: "approved" }; },
    // The pull and its check that the approval was recorded (flow.mjs pulled): recorded.
    pulled: async () => { pulls += 1; return null; },
    block: async (_state, why) => why,
  };
  assert.match(await Automation.prototype.narration.call(worker, { slug: box.slug }), /narration approved/);
  const file = path.join(box.workdir, "audio", `${timeline.lines[0].id}.wav`);
  const bytes = readFileSync(file); bytes[48] ^= 1; writeFileSync(file, bytes);
  assert.match(await Automation.prototype.narration.call(worker, { slug: box.slug }), /needs current audio evidence/);
  assert.equal(decisions, 1, "the changed take never queries or accepts the previous decision");
  assert.equal(pulls, 1);
});

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
  assert.deepEqual(Object.keys(SERIES_INSTRUCTIONS).sort(), ["planner:bible", "planner:chapter", "planner:compilation", "planner:discuss", "planner:outline", "planner:setting", "translator:compilation", "verifier:compilation", "verifier:episode", "verifier:recap", "verifier:series-doc", "writer:discuss", "writer:episode"]);
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

/** A stage run sent and its answer lost, as the web route answers it (client.mjs RUN_UNCERTAIN): it may have run. */
const lostAnswer = () => Response.json({ code: "video_ai_run_uncertain", detail: "no answer within the deadline" }, { status: 504 });
const LOST_WHY = "HTTP 504: no answer within the deadline";

/**
 * The fake site naming `named.job` on every series/next, as the site does while a document waits
 * (the job moves on only when the owner or a filed version moves it). `fail` answers a stage run
 * instead of the fake site when it returns something (or throws, as a connection does); `runs` is
 * every stage run sent. `round()` is a new run of `auto`'s first lane, and no draft is due.
 */
function documentJobs(named, { answers = {}, fail = () => null, decide = null } = {}) {
  const box = sandbox();
  const site = fakeSite({ answers, decide });
  const runs = [];
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    if (pathname === "/api/video/automation/series/next") return Response.json({ job: named.job });
    if (pathname === "/api/video/automation/run") {
      const body = JSON.parse(init.body);
      runs.push(`${body.stage}:${body.variant ?? ""}`);
      const failed = fail(body);
      if (failed) return failed;
    }
    return site.fetchImpl(url, init);
  };
  const { ctx, out } = context(box, fetchImpl, { now: Date.parse("2026-09-27T03:00:00Z") });
  writeFileSync(path.join(box.work, "auto-state.json"), JSON.stringify({ last_draft_at: "2026-09-27T00:00:00Z" }));
  const round = () => {
    const automation = new Automation(ctx, automationClient(ctx), site.settings);
    automation.refs = smallRefs;
    return automation;
  };
  return { box, site, runs, out, round, lostFile: (slug) => path.join(box.work, "_series", slug, LOST_DOCS) };
}

test("a series document whose planner answer was lost is not planned again on its own: the round goes on, the rounds after it hold the document, and the owner's change of the series plans it once", async () => {
  const named = { job: job("setting") };
  let losing = true;
  const server = documentJobs(named, { answers: { "planner:setting": () => SETTING }, fail: () => (losing ? lostAnswer() : null) });
  // The same series' threads (discuss.mjs threads.json) are another file, which the hold leaves alone.
  const threads = path.join(server.box.work, "_series", "wenjian", "threads.json");
  const notes = `${JSON.stringify({ waits: { "m-bible-1": 2 }, lost: {} }, null, 2)}\n`;
  mkdirSync(path.dirname(threads), { recursive: true });
  writeFileSync(threads, notes);

  // Before: the error left the step, `auto` exited 4 every round ahead of the drama and slides
  // requests, the drafts and the Shorts, and every round paid for the planner again.
  const first = server.round();
  assert.equal(await first.step(), `series wenjian: the planner's answer for the setting book may have run on the server without reaching the worker (${LOST_WHY}); it is not asked again on its own, and this series (and the ones after it) wait for the owner`);
  assert.deepEqual([first.halted, server.runs, server.site.calls.docs], [false, ["planner:setting"], []], "the lane goes on, nothing is filed");
  const saved = readJson(server.lostFile("wenjian"));
  assert.deepEqual(saved, { "setting:0:first": { kind: "setting", chapter: 0, previous_version: null, stage: "planner", variant: "setting", inputs: documentInputs(named.job), at: "2026-09-27T03:00:00.000Z", why: LOST_WHY } });
  assert.equal(await first.step(), null, "the site names the same job: it is not asked again, and the lane goes on past the series");
  for (let round = 0; round < 2; round++) {
    const later = server.round();
    assert.equal(await later.step(), null, `round ${round + 2}`);
    assert.equal(await later.step(), null);
  }
  assert.deepEqual(server.runs, ["planner:setting"], "one planner request, however many rounds");
  const held = server.out.stdout.split("\n").filter((line) => line.startsWith("series wenjian: the setting book is not planned again"));
  assert.equal(held.length, 2, "said once a run, in each run after the loss");
  assert.equal(held[0], `series wenjian: the setting book is not planned again: the planner's answer was lost at 2026-09-27T03:00:00.000Z (${LOST_WHY}) and the model may have run; it waits for the owner (a changed series, a line on a rejected version, or withdrawing it), and the series after it wait too`);
  assert.equal(readFileSync(threads, "utf8"), notes, "the threads' notes are untouched");

  // The owner changes the series: one new request, the document is filed, and the hold is gone.
  losing = false;
  named.job = job("setting", { series: { ...SERIES, note: "旁白快一點" } });
  assert.match(await server.round().step(), /^series wenjian: the setting book planned \(version 1\); it waits for the owner on \/admin\/videos$/);
  assert.deepEqual([server.runs, server.site.calls.docs.length], [["planner:setting", "planner:setting"], 1]);
  assert.deepEqual(readJson(server.lostFile("wenjian")), {});
});

test("a rewrite whose planner answer was lost is held under the version it rewrites; once the site names another version's rewrite, that is a new request and the old hold is dropped", async () => {
  const rejected = (id, version) => ({ id, kind: "chapter", chapter_number: 1, version, body_md: `# v${version}`, body_json: CHAPTER.body_json, status: "rejected", note: "第三集再緊一點", decided_at: null, created_at: "2026-09-27T00:00:00Z" });
  const named = { job: job("chapter", { previous: rejected("d1", 1), rewrites_left: 2 }) };
  let losing = true;
  const server = documentJobs(named, { answers: { "planner:chapter": () => CHAPTER }, fail: () => (losing ? lostAnswer() : null) });
  assert.match(await server.round().step(), /^series wenjian: the planner's answer for chapter 1's outline may have run on the server without reaching the worker/);
  assert.deepEqual(Object.keys(readJson(server.lostFile("wenjian"))), ["chapter:1:d1"]);
  assert.equal(readJson(server.lostFile("wenjian"))["chapter:1:d1"].previous_version, 1);
  assert.equal(await server.round().step(), null);
  assert.equal(server.runs.length, 1);
  // The owner's line on the chapter filed a version 2, and the owner sent that back too: another rewrite.
  losing = false;
  named.job = job("chapter", { previous: rejected("d2", 2), rewrites_left: 1 });
  assert.match(await server.round().step(), /^series wenjian: chapter 1's outline rewritten from the owner's note \(version 1\)/);
  assert.deepEqual(server.runs, ["planner:chapter", "planner:chapter"]);
  assert.deepEqual(readJson(server.lostFile("wenjian")), {}, "the hold on version 1's rewrite is dropped");
});

test("a document job's key names the version it rewrites, and its inputs hash what the owner decides, not what the worker moves", () => {
  assert.equal(documentKey(job("setting")), "setting:0:first");
  assert.equal(documentKey(job("chapter", { chapter_number: 3 })), "chapter:3:first");
  assert.equal(documentKey(job("outline", { previous: { id: "d7", version: 2, note: "再緊一點" } })), "outline:0:d7");
  const base = job("chapter", {
    previous: { id: "d1", kind: "chapter", chapter_number: 1, version: 1, body_md: "# v1", body_json: {}, status: "rejected", note: "第三集再緊一點" },
    context: { ...job("chapter").context, setting: { id: "s1", version: 1, ...SETTING }, outline: { id: "o1", version: 2, body_md: "# 總綱", body_json: {} } },
  });
  const hash = documentInputs(base);
  assert.match(hash, /^[0-9a-f]{64}$/);
  const moved = structuredClone(base);
  Object.assign(moved.series, { episodes_done: 4, episodes_started: 5, episodes_ready: 3, docs_pending: 1, status: "chapters", media_usd: 12.5, clip_seconds: 300, updated_at: "2026-10-01T00:00:00Z" });
  Object.assign(moved.context, { recaps: [{ number: 4, recap: "鐘又響了" }], episodes: [{ number: 1, status: "done" }], mysteries: [] });
  moved.rewrites_left = 1;
  assert.equal(documentInputs(moved), hash, "the worker's own progress never releases a held document");
  for (const change of [
    (each) => (each.series.premise = "兩個少年在正道與魔道之間，各自背叛"),
    (each) => (each.series.note = "旁白快一點"),
    (each) => (each.series.hands_off = true),
    (each) => (each.previous.note = "第五集也要更緊"),
    (each) => (each.context.setting.id = "s2"),
    (each) => (each.context.outline.version = 3),
  ]) {
    const changed = structuredClone(base);
    change(changed);
    assert.notEqual(documentInputs(changed), hash, String(change));
  }
});

test("a planner request that lost no answer is not held: a refusal of the model service's, the limiter, an API never reached and a connection never made leave the step as before, and the next round asks again", async (t) => {
  for (const [label, fail, code] of [
    ["the model service refused it", () => Response.json({ code: "video_ai_upstream_failed", detail: "模型服務拒絕了這個請求（HTTP 400）" }, { status: 502 }), "video_ai_upstream_failed"],
    ["the limiter could not count it", () => Response.json({ code: "rate_limit_unavailable", detail: "限流暫時無法使用" }, { status: 503 }), "rate_limit_unavailable"],
    ["the web route never reached the API", () => Response.json({ code: "upstream_unavailable", detail: "API 無法連線" }, { status: 502 }), "upstream_unavailable"],
    ["the connection was never made", () => { throw Object.assign(new TypeError("fetch failed"), { cause: { code: "ECONNREFUSED" } }); }, "network"],
  ]) {
    await t.test(label, async () => {
      const server = documentJobs({ job: job("setting") }, { fail });
      const settled = (error) => error instanceof AutomationError && error.code === code;
      await assert.rejects(server.round().step(), settled);
      const sent = server.runs.length;
      assert.ok(sent >= 1);
      assert.equal(existsSync(server.lostFile("wenjian")), false, "nothing is recorded as lost");
      await assert.rejects(server.round().step(), settled);
      assert.ok(server.runs.length > sent, "nothing ran or the API settled it: the next round asks again");
    });
  }
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

test("a character's look in the setting book is checked before it is filed", () => {
  const withLooks = (looks, voice = CAST[0].voice) => ({ ...SETTING, body_json: { ...SETTING.body_json, characters: [{ ...CAST[0], voice, looks }, CAST[1]] } });
  const look = { id: "no-coat", from: 12, to: 20, appearance: "a young man of twenty, lean, long black hair loose, a torn white under-robe", voice_style: "虛弱、斷續" };
  assert.equal(documentProblem("setting", withLooks([look, { id: "aged", from: 21, appearance: "an old man of seventy" }]), job("setting")), null, "a bounded look and one to the series' end");
  assert.equal(documentProblem("setting", withLooks([]), job("setting")), null);
  assert.match(documentProblem("setting", withLooks({ id: "x" }), job("setting")), /shen-lan: looks must be a list/);
  assert.match(documentProblem("setting", withLooks([{ id: "no-coat", from: 12 }]), job("setting")), /every look needs an id and an appearance/);
  assert.match(documentProblem("setting", withLooks([{ ...look, id: "No Coat" }]), job("setting")), /lowercase ascii/);
  assert.match(documentProblem("setting", withLooks([look, { ...look, from: 30, to: null }]), job("setting")), /two looks are called no-coat/);
  assert.match(documentProblem("setting", withLooks([{ ...look, from: 0 }]), job("setting")), /from must be the number of the first episode/);
  assert.match(documentProblem("setting", withLooks([{ ...look, to: 11 }]), job("setting")), /to must be the number of the last episode/);
  assert.match(documentProblem("setting", withLooks([{ ...look, from: 26, to: 30 }]), job("setting")), /after the last episode \(25\)/);
  assert.match(documentProblem("setting", withLooks([{ ...look, sheet_prompt: "" }]), job("setting")), /sheet_prompt must be text/);
  assert.match(documentProblem("setting", withLooks([look], { provider: "azure", name: "zh-TW-YunJheNeural" }), job("setting")), /voice_style needs the character's own Gemini voice/);
  assert.match(documentProblem("setting", withLooks([look, { id: "aged", from: 20, appearance: "an old man" }]), job("setting")), /looks no-coat and aged both cover episode 20/);
});

test("a look covering an episode changes that episode's sheet, keyframes and voice, and no other episode's", () => {
  const box = sandbox("wenjian-e001", "drama");
  const example = dramaFixture();
  const drenched = { id: "drenched", from: 2, to: 2, appearance: "a girl of about twelve, soaked black hair loose over her shoulders, torn pale green hanfu dark with seawater, small and slight", voice_style: "嗆水後沙啞、斷續" };
  const book = { characters: example.characters.map((character) => (character.id === "jingwei" ? { ...character, looks: [drenched] } : character)), mysteries: [{ id: "m1", question: "?" }] };
  assert.equal(documentProblem("setting", { body_md: "x", body_json: book }, job("setting")), null);
  // Without a look, or outside it, the cast is the book's as before: same prompts, same sheet keys.
  const plain = castFrom({ characters: example.characters });
  assert.deepEqual(castFrom(book), plain, "no episode, no look");
  assert.deepEqual(castFrom(book, 1), plain);
  assert.deepEqual(castFrom(book, 3), plain, "the look ends with its last episode");
  assert.deepEqual(castFrom({ characters: example.characters }, 2), plain, "a book without looks gives every episode the same cast");
  const second = castFrom(book, 2);
  const jingwei = (cast) => cast.find((character) => character.id === "jingwei");
  assert.deepEqual(Object.keys(jingwei(second)), ["id", "name", "appearance", "voice"], "still only video.json's keys");
  assert.equal(jingwei(second).appearance, drenched.appearance);
  assert.deepEqual(jingwei(second).voice, { ...jingwei(plain).voice, style: drenched.voice_style });
  assert.deepEqual(second.find((character) => character.id === "yandi"), plain.find((character) => character.id === "yandi"));

  // Two episodes of one series, each settled with the cast its series.json carries.
  const episode = (number, cast) => settle(structuredClone(example), { slug: `wenjian-e00${number}`, settings: { voice: { provider: "gemini", name: "Sulafat" }, drama: {} }, sourceGuide: null, root: box.root, format: "drama", series: { slug: "wenjian", episode: number, chapter: 1 }, cast });
  const first = episode(1, castFrom(book, 1));
  const later = episode(2, second);
  const shot = (doc) => {
    const scene = doc.scenes.find((each) => each.id === "opening");
    return shotPrompt(scene, resolveLook(doc.look), doc.characters.filter((character) => scene.data.characters.includes(character.id)));
  };
  assert.ok(shot(later).includes(drenched.appearance), "the second episode's keyframe prompt names the look");
  assert.ok(!shot(first).includes(drenched.appearance) && shot(first).includes(jingwei(plain).appearance), "the first episode's names the book's appearance");
  assert.ok(sheetPrompt(jingwei(later.characters), resolveLook(later.look)).includes(drenched.appearance));
  assert.ok(sheetPrompt(jingwei(first.characters), resolveLook(first.look)).includes(jingwei(plain).appearance));
  const style = (doc) => planRequests(doc, {}).find((request) => request.speaker === "jingwei").body.style;
  assert.match(style(later), /^嗆水後沙啞、斷續。/, "her lines in the look's episode take its voice style");
  assert.match(style(first), /^清亮、倔強的少女聲/);
  assert.equal(planRequests(episode(1, plain), {}).map((request) => request.key).join(), planRequests(first, {}).map((request) => request.key).join(), "an episode outside the look narrates as before");

  // The look's sheet is kept beside the base one and approved once: the next episode it covers
  // reuses it, and an episode after it reuses the base sheet again.
  assert.notEqual(sheetKey(jingwei(later.characters), later.look), sheetKey(jingwei(first.characters), first.look));
  const keep = (doc, file, content) => {
    const workdir = path.join(box.work, doc.slug);
    mkdirSync(path.join(workdir, "characters", "jingwei"), { recursive: true });
    writeFileSync(path.join(workdir, file), content);
    const manifest = { look_hash: "h", characters: { jingwei: { candidates: [{ n: 1, seed: 1, file, sha256: createHash("sha256").update(content).digest("hex"), judge: { overall: 9, passed: true, problems: [] } }] } } };
    return keepSheets({ workBase: box.work, workdir, seriesSlug: "wenjian", doc, manifest, chosen: { jingwei: 1 } });
  };
  assert.equal(keep(first, "characters/jingwei/001.png", "png-base"), 1);
  assert.equal(keep(later, "characters/jingwei/001.png", "png-drenched"), 1);
  const store = readStore(box.work, "wenjian");
  assert.deepEqual(Object.values(store.sheets).map((sheet) => [sheet.id, sheet.from]), [["jingwei", "wenjian-e001"], ["jingwei", "wenjian-e002"]], "the base sheet is kept, the look's beside it");
  const third = episode(3, castFrom(book, 3));
  const reused = reuseSheets({ workBase: box.work, workdir: path.join(box.work, "wenjian-e003"), seriesSlug: "wenjian", characters: third.characters, look: third.look });
  assert.equal(readFileSync(path.join(box.work, "wenjian-e003", reused.reused.jingwei.file), "utf8"), "png-base");
  const again = reuseSheets({ workBase: box.work, workdir: path.join(box.work, "wenjian-e004"), seriesSlug: "wenjian", characters: castFrom({ characters: [{ ...book.characters[0], looks: [{ ...drenched, to: 4 }] }] }, 4), look: later.look });
  assert.equal(readFileSync(path.join(box.work, "wenjian-e004", again.reused.jingwei.file), "utf8"), "png-drenched", "a later episode the look covers reuses its approved sheet");
});

test("the worker drafts an episode with the looks that cover it, in series.json and the brief", async () => {
  const box = sandbox();
  const site = fakeSite();
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T01:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  const loose = "a young man of twenty, lean, long black hair loose, a torn white under-robe, no bell";
  const setting = { ...SETTING, body_json: { ...SETTING.body_json, characters: [{ ...CAST[0], looks: [{ id: "no-bell", from: 2, appearance: loose }] }, CAST[1]] } };
  const cast = {};
  for (const number of [1, 2]) {
    const slug = episodeSlug("wenjian", number);
    await automation.draftEpisode({ id: `r${number}`, slug, title: "", premise: SERIES.premise, target_minutes: 3 }, { series: SERIES, setting, episodes: [], recaps: [], mysteries: [] }, { ...beats(number), chapter_number: 1, beats: beats(number) });
    cast[number] = readJson(path.join(box.root, "docs", "videos", slug, "series.json")).characters.find((character) => character.id === "shen-lan");
    assert.equal(readFileSync(path.join(box.root, "docs", "videos", slug, "brief.md"), "utf8").includes(loose), number === 2, `episode ${number}'s brief`);
  }
  assert.equal(cast[1].appearance, CAST[0].appearance);
  assert.equal(cast[2].appearance, loose);
  assert.equal(cast[1].looks, undefined, "series.json carries the cast as video.json wants it");
});

test("an approved production plan reaches each episode's writer/checker/listener context and overrides the old stills tier", async () => {
  const box = sandbox();
  const site = fakeSite();
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T01:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  const production = {
    schema_version: 1,
    source_binding: { source_sha256: "a".repeat(64) },
    narrator: { voice_name: "Erinome", performance: "冷靜敘述" },
    profile: { visual_tier: "clips", subtitles: { burn_in: false }, phases: {
      primary: { locale: "zh-TW" },
      localization: { locales: ["ja", "ko", "en"], start_after: "approved-chinese-final", readiness: "planned-not-implemented-for-drama" },
    } },
    visual_direction: "full animation", opening_30s: [{ id: "opening" }], prop_rules: ["keep the ring"],
    characters: [{ id: CAST[0].id, look_states: [{ id: "present", appearance: "blue coat" }] }],
    episodes: [1, 2].map((episode) => ({ episode, characters: [CAST[0].id], hero_shot: { action: `action ${episode}` } })),
    audio_plan: "Taiwan Mandarin", acceptance_checks: ["listen to character names"],
  };
  const settingMd = `${SETTING.body_md}\n<!-- BEGIN GENERATED PRODUCTION DIRECTION -->\nFuture episode 40 production spoiler\n<!-- END GENERATED PRODUCTION DIRECTION -->\nOwner note kept after the appendix`;
  for (const number of [1, 2]) {
    const slug = episodeSlug("wenjian", number);
    await automation.draftEpisode({ id: `production${number}`, slug, title: "", premise: SERIES.premise, target_minutes: 3 }, {
      series: { ...SERIES, visual_tier: "stills" }, setting: { ...SETTING, body_md: settingMd, body_json: { ...SETTING.body_json, production_design: production } }, episodes: [], recaps: [], mysteries: [],
    }, { ...beats(number), chapter_number: 1, beats: beats(number) });
    const info = readJson(path.join(box.root, "docs", "videos", slug, "series.json"));
    const state = readJson(path.join(box.work, slug, "auto.json"));
    assert.equal(state.series.visual_tier, "clips");
    assert.equal(info.visual_tier, "clips");
    assert.equal(info.series.visual_tier, "clips");
    const retention = readJson(path.join(box.work, slug, "localization-retention.json"));
    assert.equal(retention.series_slug, "wenjian");
    assert.equal(retention.plans[0].source_sha256, production.source_binding.source_sha256);
    assert.deepEqual(retention.plans[0].planned_locales, ["ja", "ko", "en"]);
    const payload = automation.seriesPayload(state);
    assert.equal(payload.production.episode.episode, number);
    assert.equal(payload.production.opening_30s.length, number === 1 ? 1 : 0);
    assert.deepEqual(payload.production.audio_plan, production.audio_plan);
    assert.deepEqual(payload.production.acceptance_checks, production.acceptance_checks);
    assert.equal(info.setting_md, settingMd, "the complete approved book stays on disk");
    assert.ok(payload.setting_md.includes(SETTING.body_md));
    assert.ok(payload.setting_md.includes("Owner note kept after the appendix"));
    assert.ok(!payload.setting_md.includes("Future episode 40 production spoiler"));
    assert.equal(payload.setting, undefined, "the full setting JSON never duplicates all production episodes");
    assert.equal(payload.production.episodes, undefined);
  }
});

test("approved shot-look catalogs survive cast preparation and replace writer-invented variants", () => {
  const example = dramaFixture();
  const variants = [{ id: "present", appearance: "adult woman, modern blue jacket, short hair" }];
  example.characters[0].shot_looks = variants;
  const cast = castFrom({ characters: example.characters }, 1);
  assert.deepEqual(cast[0].shot_looks, variants);
  const writer = structuredClone(example);
  writer.characters[0].shot_looks = [{ id: "invented", appearance: "unapproved" }];
  writer.scenes[1].data.character_looks = { jingwei: "present" };
  const settled = settle(writer, { slug: "wenjian-e001", root: ".", settings: { voice: example.voice, drama: {} }, format: "drama", series: { slug: "wenjian", episode: 1, chapter: 1 }, cast });
  assert.deepEqual(settled.characters[0].shot_looks, variants);
  assert.deepEqual(settled.characters[0].voice, example.characters[0].voice);
  assert.deepEqual(settled.scenes[1].data.character_looks, { jingwei: "present" });
  assert.equal(documentProblem("setting", { ...SETTING, body_json: { ...SETTING.body_json, characters: [{ ...CAST[0], shot_looks: variants }] } }, job("setting")), null);
  assert.match(documentProblem("setting", { ...SETTING, body_json: { ...SETTING.body_json, characters: [{ ...CAST[0], shot_looks: [{ id: "bad", appearance: "x", voice: {} }] }] } }, job("setting")), /only id/);
});

test("production settle preserves canonical local readings for every speaker while retaining the episode's injury voice", () => {
  const video = dramaFixture();
  const character = structuredClone(video.characters[0]);
  character.looks = [{ id: "injured", from: 2, appearance: character.appearance, voice_style: "台灣國語，受傷後短句、停頓，低聲但不換音色" }];
  const cast = castFrom({ characters: [character, video.characters[1]] }, 2);
  const canonical = { 精衛: "ㄐㄧㄥ ㄨㄟˋ", 炎帝: "ㄧㄢˊ ㄉㄧˋ" };
  const production = { source_binding: { source_sha256: "a".repeat(64) }, profile: { phases: {
    primary: { locale: "zh-TW" },
    localization: { locales: ["ja", "ko", "en"], start_after: "approved-chinese-final", readiness: "planned-not-implemented-for-drama" },
  } }, narrator: { voice_name: "Erinome", performance: "冷靜敘述" }, pronunciation_hints: canonical };
  video.pronunciation_hints = { 精衛: "writer invented reading" };
  video.localization_plan = { retain_source_media: false, planned_locales: [] };
  const settled = settle(video, { slug: "wenjian-e002", root: ".", settings: { voice: video.voice, drama: {} }, format: "drama", series: { slug: "wenjian", episode: 2, chapter: 1 }, cast, production });
  assert.deepEqual(settled.pronunciation_hints, canonical);
  assert.notEqual(settled.pronunciation_hints, canonical, "the saved map is independent of the context object");
  assert.equal(settled.localization_plan.retain_source_media, true, "the writer cannot disable the approved later-language promise");
  assert.equal(settled.localization_plan.source_sha256, production.source_binding.source_sha256);
  assert.deepEqual(settled.localization_plan.planned_locales, ["ja", "ko", "en"]);
  assert.equal(settled.characters.find((entry) => entry.id === character.id).voice.style, character.looks[0].voice_style);
  const sample = { ...settled, scenes: [{ id: "readings", lines: [
    { id: "name1", text: "精衛在這裡。", speaker: "narrator" },
    { id: "name2", text: "炎帝在這裡。", speaker: character.id, emotion: "說完留半拍" },
  ] }] };
  const requests = planRequests(sample, { terms: {} });
  assert.equal(requests[0].body.voice, "gemini:Erinome");
  assert.match(requests[0].body.style, /精衛＝ㄐㄧㄥ ㄨㄟˋ/);
  assert.equal(requests[1].body.voice, `gemini:${character.voice.name}`);
  assert.match(requests[1].body.style, /受傷後短句.*說完留半拍.*炎帝＝ㄧㄢˊ ㄉㄧˋ/);
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

/**
 * An episode of the series written, checked, heard and sent to the script gate, where its
 * screenplay waits for the owner: the state a line on its screenplay thread finds.
 */
async function screenplayAtTheGate() {
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
  const { ctx, out } = context(box, site.fetchImpl, { now: Date.parse("2026-09-27T01:00:00Z") });
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
  return { box, slug, episode, site, ctx, out, dir, pushes, state, answers, script };
}

test("the writer answers the owner on a screenplay: a question gets a reply, a change rewrites video.json, and the script is checked, heard and sent again", async () => {
  const { slug, episode, site, ctx, dir, pushes, state } = await screenplayAtTheGate();
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

test("a line on a screenplay waits while the video's writer is still running on the server: no second writer request goes out, the thread is not answered for it, and the line is taken up once the video is at rest", async () => {
  const { slug, episode, site, ctx, out, state, answers, script } = await screenplayAtTheGate();
  // The owner sends the screenplay back, so the next round has the writer fix it, and writes a line on its thread.
  Object.assign(site.reviewsOf(slug)[0], { status: "rejected", note: "第一句太平" });
  answers["writer:episode"] = (body) => {
    const draft = script();
    if (body.payload.fix) draft.video.scenes[0].lines[0].text = `${draft.video.scenes[0].lines[0].text}！`;
    return draft;
  };
  // As the site hands lines over: the oldest one still unanswered, on every call until it is answered.
  const waiting = [messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode })];
  const fetchWithMessages = async (url, init) => {
    const { pathname } = new URL(url);
    if (pathname === "/api/video/automation/series/messages/next") return Response.json({ job: waiting[0] ?? null });
    if (pathname.endsWith("/answer")) waiting.shift();
    return site.fetchImpl(url, init);
  };
  const api = automationClient({ ...ctx, fetch: fetchWithMessages });
  // The fix is a job still running on the server (client.mjs RUN_PENDING), as a durable writer's is for minutes.
  let running = true;
  const sent = [];
  const run = api.run;
  api.run = async (stage, video, instructions, payload, tokens, format, variant) => {
    sent.push(`${stage}:${variant ?? ""}`);
    if (running && stage === "writer" && variant === "episode") throw Object.assign(new AutomationError("the saved stage run is still pending; its receipt will be recovered next round", { code: RUN_PENDING }), { slug: video, stage });
    return run(stage, video, instructions, payload, tokens, format, variant);
  };
  const worker = new Automation({ ...ctx, fetch: fetchWithMessages }, api, site.settings);
  worker.refs = smallRefs;
  assert.equal(await worker.step(), "wenjian-e001: writer is still running; its saved receipt will be checked next round");
  assert.equal(worker.halted, false, "since 2026-10-06 a pending writer does not end the run, so the discussion step comes next");
  // Before: this unit sent writer/discuss for the same video while its fix was in flight, and the rewrite it saved left the fix's paid answer matching no request.
  assert.equal(await worker.step(), null);
  assert.equal(await worker.step(), null);
  assert.deepEqual(sent, ["writer:episode"], "one writer request for the video: the pending fix");
  assert.deepEqual(site.calls.answers, [], "and the owner is not told there is nothing to answer either");
  assert.equal(waiting.length, 1, "the line stays unanswered on the site");
  assert.equal(out.stdout.split("\n").filter((line) => line === "wenjian-e001: the owner's line on script:1 waits; the video is being worked on or waits on its own, and the line is answered once it is at rest").length, 1, "said once a run");
  // The same while another lane is moving the video, or a lane set it aside in this run.
  worker.pendingUntil.clear();
  for (const held of [worker.busy, worker.skipped]) {
    held.add(slug);
    assert.equal(await discussStep(worker), null);
    held.clear();
  }
  // And while it waits on its own from an earlier round (the read of its reviews failed twice
  // before the lookup of the fix): this run passes it over, so its writer was never looked up.
  const pendingFix = state();
  worker.persist({ ...pendingFix, deferred_until: "2026-09-27T03:00:00.000Z", defer_count: 2 });
  assert.equal(await worker.step(), null, "neither the video nor its line moves");
  worker.persist(pendingFix);
  assert.deepEqual([sent, site.calls.answers], [["writer:episode"], []]);

  // The fix arrives and the video goes through its own stages; at rest again, its line is answered.
  running = false;
  const lines = [];
  for (let line = await worker.step(); line; line = await worker.step()) lines.push(line);
  assert.match(lines[0], /^wenjian-e001: screenplay rewritten after the owner's note \(round 1\); it is checked again$/);
  assert.equal(lines.at(-1), "wenjian-e001: the writer answered the owner on script:1");
  assert.deepEqual([sent.filter((each) => each === "writer:discuss").length, sent.at(-1)], [1, "writer:discuss"], "after the video's own stages, once");
  assert.deepEqual([site.calls.answers.length, waiting.length], [1, 0]);
  assert.equal(state().status, "active");
});

/**
 * The site of screenplayAtTheGate with the durable writer route (automation/run/jobs) as the API
 * keeps it: a job per request key, running until the test finishes it (with the answer the fake
 * site gives the same request) or loses it (its lookup then answers `lost`, as after the worker
 * was paired again). `waiting` is the owner's lines as the site hands them over (the oldest
 * unanswered one, on every call until it is answered), and `listed` the videos on /admin/videos,
 * which take what the worker reports. `round()` is a new run of `auto`: its own client, and two
 * lanes that share what cli.mjs shares.
 */
function durableDiscussion({ site, ctx, box }, { waiting = [], listed = [], setup = null } = {}) {
  // No scheduled draft takes the place a blocked video leaves: these tests are about the video there is.
  Object.assign(site.settings, { durable_stage_runs: true, max_waiting_drafts: 0 });
  const jobs = new Map();
  const lost = new Map();
  const submitted = [];
  let refusing = null;
  let failing = null;
  const refusedRuns = new Map();
  const view = ({ request: _request, ...job }) => job;
  const fetch = async (url, init = {}) => {
    const { pathname } = new URL(url);
    if (pathname === "/api/video/automation/videos") return Response.json(listed);
    if (pathname === "/api/video/automation/series/messages/next") return Response.json({ job: waiting[0] ?? null });
    if (pathname.endsWith("/answer")) {
      if (refusing) return Response.json(refusing.body, { status: refusing.status });
      waiting.shift();
    }
    if (pathname === "/api/video/automation/run" && init.method === "POST") {
      const { stage, variant } = JSON.parse(init.body);
      const refused = refusedRuns.get(`${stage}:${variant ?? ""}`);
      if (refused) return Response.json(refused.body, { status: refused.status });
    }
    if (pathname === "/api/video/automation/run/jobs") {
      const { request_key: key, ...request } = JSON.parse(init.body);
      if (!jobs.has(key)) {
        submitted.push(`${request.stage}:${request.variant ?? ""}`);
        jobs.set(key, { id: key, request_key: key, request_hash: "a".repeat(64), input_hash: "b".repeat(64), provider: "anthropic", model: "claude-sonnet-5", status: "running", result: null, error_code: null, error_detail: null, error_status: null, retry_after: null, request, ...(failing ?? {}) });
      }
      return Response.json(view(jobs.get(key)));
    }
    if (pathname.startsWith("/api/video/automation/run/jobs/")) {
      const id = pathname.split("/").at(-1);
      if (lost.has(id)) return Response.json(lost.get(id).body, { status: lost.get(id).status });
      return Response.json(view(jobs.get(id)));
    }
    const reported = init.method === "PUT" ? /^\/api\/video\/reviews\/([a-z0-9-]+)$/.exec(pathname) : null;
    const video = reported ? listed.find((each) => each.slug === reported[1]) : null;
    if (video) {
      const body = JSON.parse(init.body);
      Object.assign(video, { stage: body.stage, checklist: body.checklist, retry_acknowledged_id: body.retry_acknowledged_id ?? video.retry_acknowledged_id ?? null });
    }
    return site.fetchImpl(url, init);
  };
  const round = async () => {
    const run = { ...ctx, fetch };
    const api = automationClient(run, { durablePollMs: 2_000 });
    await api.settings();
    const shared = { busy: new Set(), skipped: new Set(), pendingUntil: new Map() };
    return [false, true].map((secondary) => {
      const lane = new Automation(run, api, site.settings, { ...shared, secondary });
      lane.refs = smallRefs;
      setup?.(lane);
      return lane;
    });
  };
  const journals = (slug, sub = "") => {
    const dir = path.join(box.work, slug, "run-receipts", sub);
    return existsSync(dir) ? readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => readJson(path.join(dir, name))) : [];
  };
  return {
    submitted, round, journals,
    running: () => [...jobs.values()].filter((job) => job.status === "running"),
    finish: async (job) => {
      const answer = await site.fetchImpl(`${SITE}/api/video/automation/run`, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: JSON.stringify(job.request) });
      Object.assign(job, { status: "succeeded", result: await answer.json() });
    },
    lose: (job, status, body) => lost.set(job.id, { status, body }),
    // The site's answer route refuses every answer until it is called with nothing.
    refuseAnswers: (status = null, body = {}) => { refusing = status ? { status, body } : null; },
    // Every durable job sent from now on comes back as these fields say, until called with nothing.
    failJobs: (fields = null) => { failing = fields; },
    // A plain (not durable) run of this stage and variant is refused, until called with no status.
    refuseRuns: (key, status = null, body = {}) => (status ? refusedRuns.set(key, { status, body }) : refusedRuns.delete(key)),
  };
}

/** A round as `auto` drives its first lane (cli.mjs): units until nothing moves or the lane halts. */
async function roundLines(server) {
  const [first] = await server.round();
  const said = [];
  for (let unit = 0; unit < 40; unit++) {
    const line = await first.step();
    if (!line) break;
    said.push(line);
    if (first.halted) break;
  }
  return said;
}

/** The video of screenplayAtTheGate as /admin/videos lists it, taking what the worker reports. */
const listedVideo = (slug) => ({ slug, title: slug, stage: "script", checklist: [], dropped_at: null, dropped_note: null, youtube_video_id: null, retry_request_id: null, retry_acknowledged_id: null });

/** The owner presses retry on the video's card. */
const ownerRetries = (listed, request) => Object.assign(listed, { retry_request_id: request, retry_acknowledged_id: null });

const STILL_RUNNING = "wenjian-e001: writer is still running; its saved receipt will be checked next round";

test("a discussion whose writer job is still running holds its video: no lane sends the video's own writer request beside it, in the same run or in the next round, and its answer is taken before the video moves again", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, ctx, out, state } = gate;
  const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting });

  // The owner's line arrives while the screenplay waits at its gate: the writer's answer is a durable job, still running when the unit ends.
  let [first, second] = await server.round();
  assert.equal(await first.step(), STILL_RUNNING);
  assert.deepEqual(server.submitted, ["writer:discuss"]);
  // The owner sends the screenplay back while the job runs. Before: the video was in no list, so
  // the second lane of the same run found it active and free and sent writer/episode beside the job.
  Object.assign(site.reviewsOf(slug)[0], { status: "rejected", note: "第一句太平" });
  assert.equal(await second.step(), null, "the second lane leaves the video alone");
  assert.deepEqual(server.submitted, ["writer:discuss"]);
  assert.deepEqual([first.halted, [...first.pendingUntil.keys()]], [false, [slug]], "the video is set aside as for its own pending writer, and the lane goes on");
  assert.equal(await first.step(), null, "the line waits with its video");
  assert.deepEqual(server.submitted, ["writer:discuss"]);
  // A long run: past the recheck time the second lane still leaves the video to the first, which looks the job up once more.
  await ctx.sleep(PENDING_RECHECK_MS);
  assert.equal(await second.step(), null);
  assert.equal(await first.step(), STILL_RUNNING);
  assert.deepEqual(server.submitted, ["writer:discuss"]);
  assert.equal(server.journals(slug)[0].receipt.status, "running");

  // The next round, the job still running: both lanes start at once, as `auto` drives them.
  // Before: the video's own unit came first, took the rejection and sent writer/episode beside
  // the job; the discussion's saved request then no longer matched the rewritten script, and its
  // paid answer was set aside and bought again.
  [first, second] = await server.round();
  assert.deepEqual(await Promise.all([first.step(), second.step()]), [STILL_RUNNING, null]);
  assert.deepEqual(server.submitted, ["writer:discuss"]);
  assert.deepEqual([site.calls.answers.length, waiting.length, state().prompt_fixes?.script], [0, 1, undefined], "nothing is answered or rewritten meanwhile");

  // The job finishes between rounds: its answer is taken first, with no new request, and then the video moves on the owner's rejection.
  await server.finish(server.running()[0]);
  [first, second] = await server.round();
  assert.equal(await first.step(), "wenjian-e001: the writer answered the owner on script:1");
  assert.deepEqual(site.calls.answers, [{ id: asked.message.id, reply_md: "因為沈瀾此時不能說破。", revised: null }]);
  assert.deepEqual([waiting.length, server.journals(slug).length], [0, 0], "the line is answered and its saved run settled");
  assert.equal(await first.step(), STILL_RUNNING, "now the writer fixes the screenplay the owner sent back");
  assert.deepEqual(server.submitted, ["writer:discuss", "writer:episode"], "one discussion, then one fix");
  assert.equal(out.stdout.split("\n").filter((line) => line.includes("the owner's line on script:1 waits")).length, 1, "the held line was said once");
});

test("a discussion's saved writer job the server no longer has blocks its video as job_gone instead of ending every round; the line stays unanswered, and the owner's retry sends the discussion exactly once more", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, out, state } = gate;
  const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
  const waiting = [asked];
  const listed = { slug, title: slug, stage: "script", checklist: [], dropped_at: null, dropped_note: null, youtube_video_id: null, retry_request_id: null, retry_acknowledged_id: null };
  const server = durableDiscussion(gate, { waiting, listed: [listed] });
  // A round as `auto` drives its first lane (cli.mjs): units until nothing moves or the lane halts.
  const lines = async () => {
    const [first] = await server.round();
    const said = [];
    for (let unit = 0; unit < 40; unit++) {
      const line = await first.step();
      if (!line) break;
      said.push(line);
      if (first.halted) break;
    }
    return said;
  };
  assert.deepEqual(await lines(), [STILL_RUNNING]);
  const [original] = server.journals(slug);
  assert.deepEqual([original.request.variant, original.receipt.status], ["discuss", "running"]);
  // The worker is paired again: the server has no such job under the new token.
  server.lose(server.running()[0], 404, { code: "video_ai_job_not_found", detail: "找不到這個權杖的影片工作" });

  // Before: the lookup's 404 left the discussion step as an exception, every round: `auto` ended
  // there (exit 4) ahead of the series, the drama requests and the scheduled draft, the journal
  // stayed, and no retry could reach it because no video was blocked for it.
  const reason = "saved writer job gone from the server; a retry answers the owner's line on script:1 once more (video_ai_job_not_found: 找不到這個權杖的影片工作)";
  assert.deepEqual(await lines(), [`${slug}: blocked — ${reason}`]);
  assert.deepEqual([state().status, state().blocked, state().blocked_kind], ["blocked", reason, "job_gone:writer"]);
  assert.deepEqual([listed.stage, listed.checklist[0].key], ["blocked", "blocked"], "the owner reads it on the card");
  // The journal stays (the old job may still be running under the old token), and the owner is not told there is no screenplay.
  assert.deepEqual([server.journals(slug).length, server.journals(slug, "archive").length, server.submitted.length], [1, 0, 1]);
  assert.deepEqual([site.calls.answers, waiting.length], [[], 1]);
  assert.deepEqual(await lines(), [], "a round later nothing is thrown, sent or answered");
  assert.deepEqual([site.calls.answers, waiting.length, server.submitted.length], [[], 1, 1]);
  assert.ok(out.stdout.includes("wenjian-e001: the owner's line on script:1 waits; its video is blocked until the owner's retry sets the saved writer job aside, and the line is answered after it\n"));

  // The owner's retry: one more lookup, still gone, so the journal is set aside and the line is sent once.
  const request = "7a2b9c1d-3e4f-4a5b-8c6d-0e1f2a3b4c5d";
  Object.assign(listed, { retry_request_id: request, retry_acknowledged_id: null });
  assert.deepEqual(await lines(), [STILL_RUNNING]);
  const [archived] = server.journals(slug, "archive");
  assert.equal(archived.request_key, original.request_key);
  assert.equal(archived.owner_retry.reason, "the server no longer has this job (404 video_ai_job_not_found)");
  assert.deepEqual([state().status, state().blocked_kind, listed.retry_acknowledged_id], ["active", undefined, request]);
  assert.deepEqual(server.submitted, ["writer:discuss", "writer:discuss"], "exactly one new discussion request");
  assert.notEqual(server.journals(slug)[0].request_key, original.request_key);

  await server.finish(server.running().at(-1));
  assert.deepEqual(await lines(), ["wenjian-e001: the writer answered the owner on script:1"]);
  assert.deepEqual([site.calls.answers.map((answer) => answer.id), waiting.length, server.submitted.length], [[asked.message.id], 0, 2]);
});

test("a discussion whose writer answer was lost blocks its video as uncertain:writer once instead of ending every round; the line waits, and the owner's retry sends it exactly once more", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, out, state } = gate;
  const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
  const waiting = [asked];
  const listed = listedVideo(slug);
  const server = durableDiscussion(gate, { waiting, listed: [listed] });
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  const [original] = server.journals(slug);
  // The model's answer was lost after the job was dispatched: the server keeps it as uncertain, with no answer to fetch.
  Object.assign(server.running()[0], { status: "uncertain", error_code: "video_ai_job_uncertain", error_detail: "the gateway lost the answer", error_status: 409 });

  // Before: RUN_UNCERTAIN left the discussion step as an exception, every round, ahead of the
  // series and the drafts; no video was blocked, so no retry could set the journal aside.
  const reason = "writer (the owner's line on script:1) may have run on the server without its answer reaching the worker (the gateway lost the answer); it is not asked again until the owner retries";
  assert.deepEqual(await roundLines(server), [`${slug}: blocked — ${reason}`]);
  assert.deepEqual([state().status, state().blocked, state().blocked_kind, state().blocked_line], ["blocked", reason, "uncertain:writer", asked.message.id]);
  assert.deepEqual([listed.stage, listed.checklist[0].key], ["blocked", "blocked"], "the owner reads it on the card");
  assert.deepEqual([server.journals(slug).length, server.submitted.length, site.calls.answers.length, waiting.length], [1, 1, 0, 1], "the journal stays, and the owner is not told there is no screenplay");
  assert.deepEqual(await roundLines(server), [], "a round later nothing is thrown, sent or answered");
  assert.deepEqual([server.submitted.length, site.calls.answers.length, waiting.length], [1, 0, 1]);
  assert.ok(out.stdout.includes(`${slug}: the owner's line on script:1 waits; its video is blocked until the owner's retry sets aside the writer run whose answer was lost, and the line is answered after it\n`));

  // The owner's retry sets the uncertain journal aside, and the line is sent once more.
  const request = "8b3c0d2e-4f5a-4b6c-9d7e-1f2a3b4c5d6e";
  ownerRetries(listed, request);
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  assert.equal(server.journals(slug, "archive")[0].request_key, original.request_key);
  assert.deepEqual([state().status, state().blocked_kind, state().blocked_line, listed.retry_acknowledged_id], ["active", undefined, undefined, request]);
  assert.deepEqual(server.submitted, ["writer:discuss", "writer:discuss"], "exactly one new discussion request");
  await server.finish(server.running().at(-1));
  assert.deepEqual(await roundLines(server), [`${slug}: the writer answered the owner on script:1`]);
  assert.deepEqual([site.calls.answers.map((answer) => answer.id), waiting.length, server.submitted.length], [[asked.message.id], 0, 2]);
});

test("a discussion whose writer request the site refuses blocks its video with the reason and holds the line until the owner's retry; a busy service defers the video and the line waits with it", async (t) => {
  await t.test("refused", async () => {
    const gate = await screenplayAtTheGate();
    const { slug, episode, site, state } = gate;
    const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
    const waiting = [asked];
    const listed = listedVideo(slug);
    const server = durableDiscussion(gate, { waiting, listed: [listed] });
    assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
    Object.assign(server.running()[0], { status: "failed", error_code: "video_ai_project_dropped", error_status: 409, error_detail: "這支影片的專案已經放棄" });
    const reason = "the site refused the writer request for the owner's line on script:1 (video_ai_project_dropped): 這支影片的專案已經放棄";
    assert.deepEqual(await roundLines(server), [`${slug}: blocked — ${reason}`]);
    assert.deepEqual([state().status, state().blocked, state().blocked_kind, state().blocked_line], ["blocked", reason, undefined, asked.message.id]);
    assert.deepEqual(await roundLines(server), [], "the line is held, not answered with 'no screenplay here'");
    assert.deepEqual([server.submitted.length, site.calls.answers.length, waiting.length], [1, 0, 1]);
    ownerRetries(listed, "9c4d1e3f-5a6b-4c7d-8e9f-2a3b4c5d6e7f");
    assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
    assert.deepEqual([state().status, state().blocked_line], ["active", undefined]);
    assert.deepEqual(server.submitted, ["writer:discuss", "writer:discuss"], "sent once more after the retry");
  });

  // A job the server failed before it reached the model (a queue that lost it): asking later may
  // go through. A vendor that is busy after dispatch ends as uncertain instead, like the case above.
  const BEFORE_DISPATCH = { status: "failed", error_code: "video_ai_job_interrupted_before_dispatch", error_status: 409, error_detail: "工作在派送前中斷" };
  const DEFERRED = (slug) => new RegExp(`^${slug}: the writer request for the owner's line on script:1 could not finish \\(video_ai_job_interrupted_before_dispatch: 工作在派送前中斷\\); deferred until `);

  await t.test("failed before dispatch", async () => {
    const gate = await screenplayAtTheGate();
    const { slug, episode, site, ctx, state } = gate;
    const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
    const waiting = [asked];
    const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)] });
    assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
    Object.assign(server.running()[0], BEFORE_DISPATCH);
    const [lane] = await server.round();
    assert.match(await lane.step(), DEFERRED(slug));
    assert.equal(lane.halted, false, "the round goes on without ending");
    assert.equal(await lane.step(), null);
    assert.deepEqual([state().status, state().defer_count, state().blocked_line, state().line_defers], ["active", 1, undefined, { id: asked.message.id, count: 1, shared: 0 }]);
    assert.deepEqual(await roundLines(server), [], "the line waits with its video");
    assert.deepEqual([server.submitted.length, site.calls.answers.length, waiting.length], [1, 0, 1]);
    await ctx.sleep(DEFER_MAX_MS);
    assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
    assert.deepEqual(server.submitted, ["writer:discuss", "writer:discuss"], "asked once more once the wait is over");
  });

  await t.test("never getting through", async () => {
    const gate = await screenplayAtTheGate();
    const { slug, episode, site, ctx, state } = gate;
    const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
    const waiting = [asked];
    const listed = listedVideo(slug);
    const server = durableDiscussion(gate, { waiting, listed: [listed] });
    server.failJobs(BEFORE_DISPATCH);
    // Before: the video's own visit after each wait ended the row of deferrals (moved), so the line
    // was deferred at 1 for ever, sent again every wait, and never reached the card.
    for (let tries = 1; tries <= DEFER_LIMIT; tries++) {
      const [line] = await roundLines(server);
      assert.match(line, DEFERRED(slug));
      assert.equal(state().defer_count, tries, `the row grows: ${tries}`);
      if (tries >= 2) assert.ok(listed.checklist.some((row) => row.key === "deferred"), "the card shows the wait");
      await ctx.sleep(DEFER_MAX_MS);
    }
    const [blocked] = await roundLines(server);
    assert.match(blocked, new RegExp(`^${slug}: blocked — still could not move after ${DEFER_LIMIT + 1} tries: the writer request for the owner's line on script:1 could not finish`));
    assert.deepEqual([state().status, state().blocked_kind, state().blocked_line, state().line_defers], ["blocked", "deferred:writer", asked.message.id, undefined]);
    assert.deepEqual(await roundLines(server), [], "held until the owner's retry");
    assert.deepEqual([server.submitted.length, site.calls.answers.length, waiting.length], [DEFER_LIMIT + 1, 0, 1]);
    server.failJobs();
    ownerRetries(listed, "1d5e2f4a-6b7c-4d8e-9f0a-3b4c5d6e7f80");
    assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
    assert.deepEqual([server.submitted.length, state().blocked_line, state().line_defers], [DEFER_LIMIT + 2, undefined, undefined], "sent once more after the retry");
  });
});

const SITE_AWAY = [502, { code: "upstream_unavailable", detail: "網站暫時無法使用" }];

test("a writer's answer the site does not take is kept and posted on a later round, and its run is not left as an answer still to take", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, box } = gate;
  const asked = messageJob("script:1", "沈瀾為什麼不回答？", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)] });
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  await server.finish(server.running()[0]);
  server.refuseAnswers(...SITE_AWAY);
  await assert.rejects(roundLines(server), /網站暫時無法使用/);
  assert.deepEqual(readJson(path.join(box.work, slug, "discussion-answer.json")), { message_id: asked.message.id, body: { reply_md: "因為沈瀾此時不能說破。", revised: null } });
  server.refuseAnswers();
  assert.deepEqual(await roundLines(server), [`${slug}: the writer's answer on script:1, kept when the site did not take it, is posted`]);
  assert.deepEqual([site.calls.answers, waiting.length, server.submitted.length], [[{ id: asked.message.id, reply_md: "因為沈瀾此時不能說破。", revised: null }], 0, 1], "posted once, with no second request");
  assert.equal(existsSync(path.join(box.work, slug, "discussion-answer.json")), false);
  // The finished run is bound to the kept answer, so it is no discussion still open on this video.
  const [lane] = await server.round();
  assert.equal(lane.discussionOpen(slug), false);
  assert.ok(server.journals(slug).every((journal) => journal.adopted), "no succeeded run is left untaken");
});

test("a rewrite whose answer the site does not take is posted later even when the video is blocked meanwhile, and the writer is paid once", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, dir, state } = gate;
  const asked = messageJob("script:1", "第一句改成感嘆句。", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)] });
  const first = readJson(path.join(dir, "video.json")).scenes[0].lines[0].text;
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  await server.finish(server.running()[0]);
  server.refuseAnswers(...SITE_AWAY);
  await assert.rejects(roundLines(server), /網站暫時無法使用/);
  assert.equal(readJson(path.join(dir, "video.json")).scenes[0].lines[0].text, `${first}！`, "the rewrite is saved");
  // Before the line comes back, the video's own checks run on the rewrite and one of them blocks it.
  server.refuseAnswers();
  server.refuseRuns("verifier:episode", 409, { code: "video_ai_project_dropped", detail: "這支影片的專案已經放棄" });
  const [blocked, ...after] = await roundLines(server);
  assert.match(blocked, /^wenjian-e001: blocked — the site refused the verifier request/);
  assert.equal(state().status, "blocked");
  // Before: the line was answered with the block ("劇本先不動"), the paid reply was never posted,
  // and an owner who asked again paid the writer for a change already made.
  assert.deepEqual(after, [`${slug}: the writer's answer on script:1, kept when the site did not take it, is posted`]);
  assert.deepEqual(site.calls.answers, [{ id: asked.message.id, reply_md: "第一句改成感嘆句。", revised: null }]);
  assert.deepEqual(await roundLines(server), []);
  assert.deepEqual([server.submitted.filter((each) => each === "writer:discuss").length, readJson(path.join(dir, "video.json")).scenes[0].lines[0].text], [1, `${first}！`], "paid once, rewritten once");
});

test("a discussion rewrite whose lint repair is still running when the visit ends keeps its reply: the video checks the rewrite, and the line is answered once with no second request", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, box, state, answers, dir } = gate;
  // The writer's repair puts a line back into the scene the owner emptied.
  answers["writer:episode"] = (body) => {
    if (!body.payload.lint_errors) return gate.script();
    const video = structuredClone(body.payload.video);
    video.scenes[0].lines = [{ ...body.payload.video.scenes[1].lines[0], id: body.payload.line_ids?.[0] ?? "zz" }];
    return { video, claims: "原創\n", lexicon_additions: {} };
  };
  const asked = messageJob("script:1", "刪掉第一場所有台詞。", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)] });
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  await server.finish(server.running()[0]);
  // The rewrite fails lint, and its repair is a durable job still running when the visit ends: the
  // video is set aside for it, the rewrite is marked unchecked, and the kept reply is posted on the
  // next unit. Before: the reply was lost, the video took the repair up, and the line was asked,
  // and paid for, again.
  assert.deepEqual(await roundLines(server), [STILL_RUNNING, `${slug}: the writer's answer on script:1, kept when the site did not take it, is posted`]);
  assert.deepEqual([state().verified, state().listener_done, existsSync(path.join(box.work, slug, "discussion-answer.json"))], [false, false, false]);
  assert.deepEqual([site.calls.answers.map((answer) => [answer.id, answer.reply_md]), waiting.length], [[[asked.message.id, "刪了第一場所有台詞。"]], 0]);
  // The video's own unit takes the repair up and checks the rewrite.
  for (let round = 0; round < 6 && server.running().length; round++) {
    for (const job of server.running()) await server.finish(job);
    await roundLines(server);
  }
  assert.equal(server.submitted.filter((each) => each === "writer:discuss").length, 1, "the line is asked once");
  assert.equal(readJson(path.join(dir, "video.json")).scenes[0].lines.length, 1, "the repaired rewrite is the script");
  assert.equal(site.calls.answers.length, 1);
});

test("a discussion rewrite whose lint repair request fails is sorted as the line's request: the video waits, the kept reply is posted, and the line is not asked again", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, state, answers } = gate;
  answers["writer:episode"] = (body) => (body.payload.lint_errors ? { video: body.payload.video, claims: "原創\n", lexicon_additions: {} } : gate.script());
  const asked = messageJob("script:1", "刪掉第一場所有台詞。", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)] });
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  await server.finish(server.running()[0]);
  // The repair the rewrite needs is lost by the queue before it reaches the model.
  server.failJobs({ status: "failed", error_code: "video_ai_job_interrupted_before_dispatch", error_status: 409, error_detail: "工作在派送前中斷" });
  // Before: the error left the step as an exception, the run ended, and the reply was lost.
  const [deferred, posted, ...rest] = await roundLines(server);
  assert.match(deferred, new RegExp(`^${slug}: the writer's lint repair of the rewrite for the owner's line on script:1 could not finish \\(video_ai_job_interrupted_before_dispatch: 工作在派送前中斷\\); deferred until `));
  assert.equal(posted, `${slug}: the writer's answer on script:1, kept when the site did not take it, is posted`);
  assert.deepEqual(rest, []);
  assert.deepEqual([state().status, state().verified, state().listener_done, state().line_defers?.id], ["active", false, false, asked.message.id]);
  assert.deepEqual([site.calls.answers.map((answer) => answer.reply_md), waiting.length, server.submitted.filter((each) => each === "writer:discuss").length], [["刪了第一場所有台詞。"], 0, 1]);
});

test("a long anime's change plan is paid once though an act of the rewrite meets a busy service: the plan's answer stays saved through the wait", async () => {
  const gate = await screenplayAtTheGate();
  const { slug, episode, site, ctx, state, answers, box } = gate;
  writeFileSync(path.join(box.work, slug, "auto.json"), `${JSON.stringify({ ...state(), production_policy: "long-anime-v1" }, null, 2)}\n`);
  answers["writer:anime-discuss-plan"] = () => ({ reply: "要改第二幕。", change_required: true, revised: null });
  // The plan is durable; each act is a plain request, as writeAnimeActs sends it.
  const setup = (lane) => {
    const payload = lane.scriptPayload.bind(lane);
    lane.scriptPayload = (st, extra) => {
      const { production_policy: _policy, ...rest } = st;
      return { ...payload(rest, extra), category: "anime" };
    };
    lane.animeRewrite = async function (st, extra, video, stage) {
      await this.stage(stage, st.slug, { act: 1, message: extra.message }, 1000, "drama", "anime-act", st.series);
      return { video };
    };
  };
  const asked = messageJob("script:1", "第二幕改一下", { series: SERIES, episode });
  const waiting = [asked];
  const server = durableDiscussion(gate, { waiting, listed: [listedVideo(slug)], setup });
  assert.deepEqual(await roundLines(server), [STILL_RUNNING]);
  await server.finish(server.running()[0]);
  server.refuseRuns("writer:anime-act", 503, { code: "video_ai_upstream_busy", detail: "模型服務忙碌中" });
  const [deferred] = await roundLines(server);
  assert.match(deferred, /could not finish \(video_ai_upstream_busy: 模型服務忙碌中\); deferred until /);
  // Before: the step settled the plan's answer with the deferral, and the next visit paid for a new plan.
  assert.deepEqual(server.journals(slug).map((journal) => [journal.request.variant, journal.receipt?.status]), [["anime-discuss-plan", "succeeded"]]);
  server.refuseRuns("writer:anime-act");
  await ctx.sleep(DEFER_MAX_MS);
  for (let round = 0; round < 3 && waiting.length; round++) await roundLines(server);
  assert.deepEqual([server.submitted.filter((each) => each === "writer:anime-discuss-plan").length, site.calls.answers.map((answer) => answer.reply_md), waiting.length], [1, ["要改第二幕。"], 0]);
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

test("a hands-off document whose checker's answer was lost is not judged a second time: the planner's answer, paid for, is filed without a verdict and waits for the owner", async () => {
  const named = { job: job("setting", { series: BINGE }) };
  const server = documentJobs(named, {
    answers: { "planner:setting": () => SETTING, "verifier:series-doc": () => verdict("setting") },
    fail: (body) => (body.stage === "verifier" ? lostAnswer() : null),
    decide: (body) => (body.judge ? { status: "approved", note: null } : { status: "review", note: null }),
  });
  const automation = server.round();
  // Before: the error left the step, and the next round paid for the planner and the checker again.
  assert.equal(await automation.step(), "series rebirth: the setting book planned (version 1); it waits for the owner on /admin/videos");
  assert.deepEqual(server.runs, ["planner:setting", "verifier:series-doc"], "one planner request, and one checker request, not two");
  assert.equal(server.site.calls.docs[0].judge, undefined, "no verdict travels with it, so the site leaves it for the owner");
  assert.ok(server.out.stdout.includes(`  the checker's verdict on setting may have run on the server without reaching the worker (${LOST_WHY}); it is not asked again, and the document waits for the owner\n`));
  assert.equal(existsSync(server.lostFile("rebirth")), false, "the document was filed: nothing is held");
  named.job = null;
  assert.equal(await automation.step(), null);
  assert.deepEqual(server.runs, ["planner:setting", "verifier:series-doc"]);
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
    // Short lines, so the four shots open inside ten seconds: the craft rows (core/craft.mjs
    // CRAFT_GATE_ROWS) send a slow opening back before the checker's verdict is even read.
    for (const scene of video.scenes) for (const line of scene.lines) line.text = line.text.slice(0, 4);
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


for (const [name, edit, changes] of [
  ["longer hook", (doc) => { doc.scenes[0].lines[0].text = "她終於回到當年離開的城市卻發現眼前那個人早已不是她記憶中曾經熟悉的模樣"; }, true],
  ["removed payoff", (doc) => { doc.scenes[1].lines.pop(); }, true],
  ["moved payoff", (doc) => { doc.scenes[1].lines.reverse(); }, true],
  ["changed ending", (doc) => { doc.scenes.at(-1).lines.at(-1).text = "結局已變。"; }, true],
  ["changed pause", (doc) => { doc.scenes[0].lines[0].pause_after_ms = 500; }, true],
  ["no-op", () => {}, false],
  ["media prompt only", (doc) => { doc.scenes[0].data.prompt += ", soft light"; }, false],
]) {
  test(`listener ${name}: the exact saved narrative and timing require fresh evidence`, async () => {
    const slug = "listener-check-e001";
    const box = sandbox(slug, "drama");
    const series = { slug: "listener-check", episode: 1, chapter: 1, genre: "rebirth-revenge", hands_off: false, compilation: true };
    const settings = { voice: { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin" }, max_verify_rounds: 3, drama: { style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [] } };
    let video = dramaFixture();
    video.scenes = video.scenes.filter((scene) => scene.template !== "outro");
    video.scenes.at(-1).chapter = "End";
    video.scenes[0].lines = video.scenes[0].lines.slice(0, 1);
    video.scenes[0].lines[0].text = "她回來了。";
    video.sources = [];
    video = settle(video, { slug, settings, root: box.root, format: "drama", series, cast: video.characters });
    const ids = [...eachLine(video)].map(({ line }) => line.id);
    const retention = { hook_line: ids[0], satisfaction_lines: [ids[1], ids[2]], cliffhanger_line: ids.at(-1) };
    const coverage = { hook: "有", conflict: "有", turn: "有", cliffhanger: "有", satisfaction: "有" };
    writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(video));
    writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ slug: series.slug, episode: 1, chapter: 1, characters: video.characters, series, beats: { turn: "不得刪除" }, setting_md: "World rules", chapter_md: "Chapter outline", recaps: [{ number: 0, recap: "Earlier events" }] }));
    mkdirSync(path.join(box.workdir, "review"), { recursive: true });
    const checkFile = path.join(box.workdir, "review", "script-check.json");
    const check = { ...scriptCheckBinding(video), coverage, problems: [], similar_works: [], retention: retentionNumbers(video, retention) };
    writeFileSync(checkFile, JSON.stringify(check));
    const candidate = structuredClone(video);
    edit(candidate);
    const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, now: () => new Date("2026-09-28T12:00:00Z"), stdout: { write() {} }, fetch: async () => { throw new Error("unexpected network"); } };
    const automation = new Automation(ctx, {}, settings);
    automation.refs = smallRefs;
    const stages = [];
    automation.stage = async (stage, _slug, payload) => {
      stages.push(stage);
      assert.equal(payload.setting_md, "World rules");
      assert.deepEqual(payload.beats, { turn: "不得刪除" });
      if (stage === "listener") return { video: candidate, edits: [] };
      assert.equal(stage, "verifier", JSON.stringify(payload.lint_errors));
      assert.deepEqual(payload.video, readJson(path.join(box.dir, "video.json")));
      return { report: "# Fresh verification", changed_facts: 0, coverage, problems: [], retention };
    };
    const state = { slug, format: "drama", status: "active", series, notes: [], source_urls: [], verify_rounds: 1, verified: true, listener_done: false, prompt_fixes: {} };
    await automation.listen(state);
    const saved = readJson(path.join(box.dir, "video.json"));
    assert.equal(state.verified, !changes);
    assert.equal(state.listener_done, true);
    assert.equal(scriptCheckMatches(readJson(checkFile), saved), !changes);
    if (changes) {
      // This is the next real worker stage. Listener completion survives it: no loop.
      if (name === "longer hook" || name === "changed ending") {
        state.series.hands_off = name === "changed ending";
        if (state.series.hands_off) settings.drama.series_script_gate = false;
        // Both manual and automatic gate paths refuse an old report before looking
        // for a prior approval or allowing the settings bypass.
        await automation.scriptGate(state);
      } else {
        await automation.verify(state);
      }
      assert.equal(state.verified, true);
      assert.equal(state.listener_done, true);
      const fresh = readJson(checkFile);
      assert.ok(scriptCheckMatches(fresh, saved));
      assert.deepEqual(fresh.retention, retentionNumbers(saved, retention));
      if (name === "longer hook") {
        assert.equal(scriptVerdict(check, series).passed, true);
        assert.equal(scriptVerdict(fresh, series).passed, false);
        assert.equal(fresh.retention.hook_seconds, 8.4);
      }
      assert.deepEqual(stages, ["listener", "verifier"]);
    } else {
      assert.deepEqual(stages, ["listener"]);
    }
  });
}

for (const [name, edit, recheck] of [
  ["pause", (video) => { video.scenes[0].lines[0].pause_after_ms = 500; }, true],
  ["spoken form", (video) => { const line = video.scenes[0].lines[0]; line.say = "這句口白現在更長了。"; line.say_for = createHash("sha256").update(line.text).digest("hex").slice(0, 12); }, true],
  ["media prompt", (video) => { video.scenes[0].data.prompt += ", soft lighting"; }, false],
]) {
  test(`resumed approved episode with a changed ${name} rechecks evidence before media when needed`, async () => {
    const { approve, approvalState } = await import("../core/approvals.mjs");
    const { writeScreenplay } = await import("../core/screenplay.mjs");
    const { pipelineStatus } = await import("../core/state.mjs");
    const slug = "resumed-check-e001";
    const box = sandbox(slug, "drama");
    const series = { slug: "resumed-check", episode: 1, chapter: 1, hands_off: false };
    const settings = { voice: { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin" }, max_verify_rounds: 3, drama: { style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [] } };
    let video = dramaFixture();
    video.sources = [];
    video = settle(video, { slug, settings, root: box.root, format: "drama", series, cast: video.characters });
    writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(video));
    writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ slug: series.slug, episode: 1, chapter: 1, series, characters: video.characters, beats: {}, setting_md: "World", chapter_md: "Chapter", recaps: [] }));
    writeFileSync(path.join(box.dir, "verify-1.md"), "# Previous verification");
    writeScreenplay(box.dir, video);
    mkdirSync(path.join(box.workdir, "review"), { recursive: true });
    const checkFile = path.join(box.workdir, "review", "script-check.json");
    writeFileSync(checkFile, JSON.stringify(scriptCheckBinding(video)));
    for (const gate of ["outline", "script"]) await approve({ gate, docDir: box.dir, workdir: box.workdir });
    edit(video);
    writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(video));
    writeScreenplay(box.dir, video);
    assert.equal((await approvalState({ gate: "script", docDir: box.dir, workdir: box.workdir })).status, recheck ? "stale" : "approved", "spoken form and pauses invalidate the previous approval");
    assert.equal((await pipelineStatus({ slug, root: box.root, workdir: box.workdir })).next.id, recheck ? "script approved" : "look generated", "the real pipeline requires a new approval only for changed speech");
    const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, now: () => new Date("2026-09-28T12:00:00Z"), stdout: { write() {} }, fetch: async () => { throw new Error("unexpected network"); } };
    const automation = new Automation(ctx, {}, settings);
    automation.refs = smallRefs;
    const calls = [];
    automation.stage = async (stage, _slug, payload) => {
      calls.push(stage);
      assert.equal(stage, "verifier");
      assert.deepEqual(payload.video, video);
      return { report: "# Current verification", changed_facts: 0 };
    };
    automation.media = async (_state, command) => { calls.push(`media:${command}`); return "media"; };
    const state = { slug, format: "drama", status: "active", series, notes: [], source_urls: [], verify_rounds: 1, verified: true, listener_done: true, prompt_fixes: {} };
    await automation.advance(state);
    assert.deepEqual(calls, recheck ? ["verifier"] : ["media:look"]);
    assert.equal(state.listener_done, true);
    assert.equal(state.verified, true);
    assert.ok(scriptCheckMatches(readJson(checkFile), video));
  });
}

/** An episode on disk as the worker left it after the writer: the script, its series and a worker to move it. */
function checkedEpisode(slug) {
  const box = sandbox(slug, "drama");
  const series = { slug: slug.replace(/-e001$/, ""), episode: 1, chapter: 1, hands_off: false };
  const settings = { voice: { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin" }, max_verify_rounds: 3, drama: { style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [] } };
  let video = dramaFixture();
  video.sources = [];
  video = settle(video, { slug, settings, root: box.root, format: "drama", series, cast: video.characters });
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(video));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ slug: series.slug, episode: 1, chapter: 1, series, characters: video.characters, beats: {}, setting_md: "World", chapter_md: "Chapter", recaps: [] }));
  mkdirSync(path.join(box.workdir, "review"), { recursive: true });
  const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, now: () => new Date("2026-09-28T12:00:00Z"), stdout: { write() {} }, fetch: async () => { throw new Error("unexpected network"); } };
  const automation = new Automation(ctx, {}, settings);
  automation.refs = smallRefs;
  const state = { slug, format: "drama", status: "active", series, notes: [], source_urls: [], verify_rounds: 0, verified: false, listener_done: false, prompt_fixes: {} };
  return { box, video, automation, state, checkFile: path.join(box.workdir, "review", "script-check.json") };
}

for (const [name, reshape] of [
  ["the voice's keys in another order", (doc) => { doc.voice = Object.fromEntries(Object.entries(doc.voice).reverse()); }],
  ["the cast in another order", (doc) => { doc.characters.reverse(); }],
  ["no voice", (doc) => { delete doc.voice; }],
]) {
  test(`a checker's answer with ${name} is the script that was saved: its report is bound, not refused`, async () => {
    const { box, video, automation, state, checkFile } = checkedEpisode("checker-echo-e001");
    const candidate = structuredClone(video);
    candidate.scenes.at(-1).lines.at(-1).text = "結局已變。";
    reshape(candidate);
    automation.stage = async (stage) => {
      assert.equal(stage, "verifier", "lint has nothing to repair");
      return { report: "# Verification", changed_facts: 1, video: candidate };
    };
    const line = await automation.verify(state);
    assert.match(line, /fact-check round 1, 1 facts changed/);
    assert.equal(state.verified, true);
    assert.equal(state.failures?.verifier, undefined, "the round did not count as a failure");
    const saved = readJson(path.join(box.dir, "video.json"));
    assert.equal(saved.scenes.at(-1).lines.at(-1).text, "結局已變。");
    assert.deepEqual(saved.voice, video.voice, "the owner's voice is what is saved");
    assert.deepEqual(saved.characters.map((character) => character.id), video.characters.map((character) => character.id));
    assert.ok(scriptCheckMatches(readJson(checkFile), saved));
  });
}

test("a checker's answer lint had to repair is not the script that was saved: its report is refused", async () => {
  const { box, video, automation, state, checkFile } = checkedEpisode("checker-repair-e001");
  const candidate = structuredClone(video);
  candidate.scenes[0].lines[0].text = "";
  const stages = [];
  automation.stage = async (stage, _slug, payload) => {
    stages.push(stage);
    if (stage === "verifier") return { report: "# Verification", changed_facts: 1, video: candidate };
    assert.ok(payload.lint_errors.length > 0);
    const repaired = structuredClone(candidate);
    repaired.scenes[0].lines[0].text = "她回來了。";
    return { video: repaired };
  };
  const line = await automation.verify(state);
  assert.match(line, /the lint repair changed the checked script/);
  assert.deepEqual(stages, ["verifier", "writer"]);
  assert.equal(state.verified, false);
  assert.equal(state.failures.verifier, 1);
  assert.equal(readJson(path.join(box.dir, "video.json")).scenes[0].lines[0].text, "她回來了。");
  assert.equal(existsSync(checkFile), false, "no report is written for a script the checker did not read");
});

for (const [name, gates, expected] of [
  ["past the script gate goes on without another check", ["outline", "script"], ["media:look"]],
  ["ahead of the script gate is checked again", ["outline"], ["verifier"]],
]) {
  test(`an episode whose report was written before reports named their script, ${name}`, async () => {
    const { approve } = await import("../core/approvals.mjs");
    const { writeScreenplay } = await import("../core/screenplay.mjs");
    const { box, video, automation, state, checkFile } = checkedEpisode("unbound-check-e001");
    writeFileSync(path.join(box.dir, "verify-1.md"), "# Previous verification");
    writeScreenplay(box.dir, video);
    const unbound = { round: 1, coverage: { hook: "有" }, problems: [], similar_works: [], retention: { passed: true } };
    writeFileSync(checkFile, JSON.stringify(unbound));
    for (const gate of gates) await approve({ gate, docDir: box.dir, workdir: box.workdir });
    const calls = [];
    automation.stage = async (stage) => {
      calls.push(stage);
      assert.equal(stage, "verifier");
      return { report: "# Current verification", changed_facts: 0 };
    };
    automation.media = async (_state, command) => { calls.push(`media:${command}`); return "media"; };
    Object.assign(state, { verify_rounds: 1, verified: true, listener_done: true });
    await automation.advance(state);
    assert.deepEqual(calls, expected);
    assert.equal(state.verified, true);
    const report = readJson(checkFile);
    if (gates.includes("script")) assert.deepEqual(report, unbound, "the old report is left as it was");
    else assert.ok(scriptCheckMatches(report, video), "the new report names the script it read");
  });
}

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

const ANIME_SERIES = { ...SERIES, slug: "borrowed-dawn", title: "借來的黎明", kind: "series", category: "anime", genre: "custom", lead: "ensemble", tone: "no-romance", style_preset: "anime-2d", target_minutes: 22, planned_episodes: 120, episodes_per_chapter: 12, chapters: 10, open_ended: false, hands_off: false, compilation: false, production_policy: "long-anime-v1", runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 } };
const sourceSeason = (number) => JSON.parse(readFileSync(new URL(`../../../docs/videos/series-plans/borrowed-dawn/season-${String(number).padStart(2, "0")}.json`, import.meta.url), "utf8"));

test("source-native anime chapters validate all 120 episodes without invented retention fields", () => {
  let previous = [];
  for (let number = 1; number <= 10; number++) {
    const body = sourceSeason(number);
    assert.equal(documentProblem("chapter", { body_md: "原作", body_json: body }, { series: ANIME_SERIES, chapter_number: number, context: { episodes: previous } }), null);
    assert.ok(body.episodes.every((episode) => !episode.hook_type && !episode.satisfaction));
    previous = body.episodes;
  }
  const final = sourceSeason(10);
  final.episodes.at(-1).closed_ending = false;
  assert.match(documentProblem("chapter", { body_md: "原作", body_json: final }, { series: ANIME_SERIES, chapter_number: 10 }), /end tense/);
});

test("quiet ending exception is explicit, closed, final and positively resolved", () => {
  const last = sourceSeason(10);
  const check = (series, body) => documentProblem("chapter", { body_md: "原作", body_json: body }, { series, chapter_number: 10 });
  assert.match(check({ ...ANIME_SERIES, open_ended: true }, last), /end tense/);
  assert.match(check({ ...ANIME_SERIES, production_policy: null, runtime_spec: null }, last), /end tense/);
  const incorrect = structuredClone(last); incorrect.episodes.at(-1).cliffhanger.type = "danger";
  assert.match(check(ANIME_SERIES, incorrect), /quiet final resolution/);
  const earlier = sourceSeason(1); earlier.episodes[0].closed_ending = true;
  assert.match(documentProblem("chapter", { body_md: "原作", body_json: earlier }, { series: ANIME_SERIES, chapter_number: 1 }), /only the planned closed finale/);
  const good = { coverage: { hook: "有", conflict: "有", turn: "有", closure: "有", high_tension: ["有", "有"], consequences: "有" }, problems: [], continuity_problems: [], similar_works: [] };
  const context = { ...ANIME_SERIES, episode: 120, closed_ending: true };
  assert.equal(scriptVerdict(good, context).passed, true);
  assert.equal(scriptVerdict({ ...good, coverage: { ...good.coverage, closure: "弱" } }, context).passed, false);
  assert.equal(scriptVerdict(good, { ...context, episode: 119 }).passed, false);
  assert.equal(scriptVerdict({ ...good, continuity_problems: ["角色提前知道答案"] }, context).passed, false);
});

test("anime rejects lost stakes/state and requires local payoffs across chapter boundaries", () => {
  const body = sourceSeason(1);
  body.episodes[0].high_tension[1].stakes = "";
  assert.match(documentProblem("chapter", { body_md: "原作", body_json: body }, { series: ANIME_SERIES, chapter_number: 1 }), /stakes/);
  const missing = sourceSeason(1); delete missing.episodes[0].state.evidence;
  assert.match(documentProblem("chapter", { body_md: "原作", body_json: missing }, { series: ANIME_SERIES, chapter_number: 1 }), /complete source state/);
  const next = sourceSeason(2); const previous = sourceSeason(1).episodes.slice(-3);
  for (const episode of [...previous, next.episodes[0]]) { episode.payoffs = []; episode.general_payoffs = []; }
  assert.match(documentProblem("chapter", { body_md: "原作", body_json: next }, { series: ANIME_SERIES, chapter_number: 2, context: { episodes: previous } }), /episodes 10 to 13.*local payoff/);
});

test("anime prompts remain independent of legacy short-drama genre instructions", () => {
  for (const [stage, variant] of [["planner", "setting"], ["planner", "chapter"], ["writer", "anime-act"], ["verifier", "episode"], ["verifier", "series-doc"], ["listener", "anime-act"]]) {
    const text = instructionsFor(stage, "drama", "", variant, "", ANIME_SERIES);
    assert.match(text, /long-anime-v1/);
    assert.doesNotMatch(text, /2–4 min|dual-male|MIN_SATISFACTION|FIRST_SATISFACTION|satisfaction_schedule/);
  }
  assert.match(instructionsFor("writer", "drama", "", "anime-act", "", ANIME_SERIES), /ONLY the supplied act/);
  assert.match(instructionsFor("verifier", "drama", "", "episode", "", ANIME_SERIES), /without returning or rewriting video.json/);
  const regular = instructionsFor("writer", "drama", "", "episode", "", { ...SERIES, category: "anime", style_preset: "anime-2d" });
  assert.match(regular, /2 to 4/);
});

test("anime brief preserves complete source beats and settle overrides model authority", () => {
  const row = sourceSeason(1).episodes[0];
  const brief = episodeBrief(ANIME_SERIES, row, CAST, row);
  for (const field of [row.high_tension[0].stakes, row.high_tension[1].consequence, row.state.evidence, row.general_payoffs[0]]) assert.ok(brief.includes(field));
  assert.match(brief, /1320/);
  const video = settle({ ...dramaFixture(), production_policy: "other", runtime_spec: {}, category: "other", target_minutes: [3, 3], look: { preset: "cinematic-3d" }, series: { planned_episodes: 999 } }, { slug: "borrowed-dawn-e001", settings: { voice: dramaFixture().voice, drama: {} }, root: ".", format: "drama", series: { ...ANIME_SERIES, episode: 1, chapter: 1, closed_ending: false }, cast: dramaFixture().characters });
  assert.equal(video.production_policy, "long-anime-v1");
  assert.equal(video.category, "anime");
  assert.deepEqual(video.target_minutes, [22, 22]);
  assert.equal(video.look.preset, "anime-2d");
  assert.equal(video.series.planned_episodes, 120);
  assert.equal(video.series.lead, "ensemble");
  const legacy = settle({ ...dramaFixture(), production_policy: "long-anime-v1", runtime_spec: ANIME_SERIES.runtime_spec }, { slug: "old", settings: { voice: dramaFixture().voice, drama: {} }, root: ".", format: "drama" });
  assert.equal(legacy.production_policy, undefined, "a model cannot grant a new production policy");
});

test("anime draft first report is categorized and script approval remains manual with global gate off", async () => {
  const box = sandbox(); const site = fakeSite({ settings: { drama: { drama_enabled: true, series_script_gate: false } } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-10-02T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings); automation.refs = smallRefs;
  const row = sourceSeason(1).episodes[0]; const slug = "borrowed-dawn-e001";
  await automation.draftEpisode({ id: "anime-request", slug, target_minutes: 3 }, { series: ANIME_SERIES, setting: SETTING, episodes: [], recaps: [], mysteries: [] }, { ...row, chapter_number: 1, beats: row });
  const state = automation.states().find((entry) => entry.slug === slug);
  assert.equal(state.category, "anime"); assert.equal(state.target_minutes, 22);
  assert.equal(site.calls.reports[0].category, "anime");
  assert.deepEqual(site.calls.reports[0].runtime_spec, ANIME_SERIES.runtime_spec);
  const seriesFile = readJson(path.join(box.root, "docs/videos", slug, "series.json"));
  assert.deepEqual(seriesFile.beats, row);
  assert.equal(seriesFile.series.production_policy, "long-anime-v1");
  assert.equal(seriesFile.series.planned_episodes, 120);
  const video = automation.settled(state, dramaFixture());
  assert.deepEqual(validateAnimePolicy(seriesFile), []);
  assert.equal(runtimePolicyHash(seriesFile), runtimePolicyHash(video), "snapshot and final script bind the same approved per-episode identity and finale");
  const dir = path.join(box.root, "docs/videos", slug);
  writeFileSync(path.join(dir, "video.json"), JSON.stringify(video));
  mkdirSync(path.join(automation.workdir(slug), "review"), { recursive: true });
  writeFileSync(path.join(automation.workdir(slug), "review", "script-check.json"), JSON.stringify(scriptCheckBinding(video)));
  let pushed = false; ctx.runCommand = async () => { pushed = true; return { code: 0, out: "sent" }; };
  assert.match(await automation.scriptGate(state), /sent to \/admin\/videos/);
  assert.equal(pushed, true);
  assert.equal(readApprovals(automation.workdir(slug)).approvals.some((entry) => entry.gate === "script"), false, "global auto-approval cannot approve an explicit long anime");
});

test("a stale worker job cannot start or draft a planning-only imported series", async () => {
  let started = false;
  const automation = { settings: { drama: { drama_enabled: true } }, api: { seriesNext: async () => ({ kind: "episode", series: { ...ANIME_SERIES, planning_only: true }, episode: { number: 1 } }), episodeStart: async () => { started = true; } }, room: () => true };
  assert.equal(await seriesStep(automation), null);
  assert.equal(started, false);
});

test("Automation long-anime writer and repairs use scoped acts with source authority and full native beats", async () => {
  const box = sandbox(); const site = fakeSite({ answers: { "writer:anime-act": ({ payload }) => ({ act_id: payload.act.id, video: { ...dramaFixture(), scenes: payload.video?.scenes ?? [{ id: `${payload.act.scene_prefix}shot`, chapter: "原作", template: "shot", data: { prompt: "Steam rises as a worker turns a valve", camera: "medium", motion: "the worker turns the valve", characters: [] }, lines: [{ id: payload.line_ids[0], text: "先把管路關上。", speaker: "narrator" }] }] } }) } });
  const { ctx } = context(box, site.fetchImpl, { now: Date.parse("2026-10-02T00:00:00Z") });
  const automation = new Automation(ctx, automationClient(ctx), site.settings); automation.refs = smallRefs;
  const row = sourceSeason(1).episodes[0]; const slug = "borrowed-dawn-e001";
  await automation.draftEpisode({ id: "bounded-request", slug, target_minutes: 3 }, { series: ANIME_SERIES, setting: SETTING, episodes: [], recaps: [], mysteries: [] }, { ...row, chapter_number: 1, beats: row });
  const state = automation.states().find((entry) => entry.slug === slug);
  state.target_minutes = null;
  const result = await automation.animeRewrite(state, { brief: "原作故事" });
  assert.equal(result.video.scenes.length, 5);
  assert.equal(state.target_minutes, 22, "lost target restores from authoritative runtime, never the three-minute fallback");
  assert.equal(site.calls.run.length, 5);
  for (const call of site.calls.run) {
    assert.equal(call.max_output_tokens, 32000);
    assert.equal(call.variant, "anime-act");
    assert.deepEqual(call.payload.beats, row);
    assert.deepEqual(call.payload.runtime_spec, ANIME_SERIES.runtime_spec);
    assert.deepEqual(call.payload.target_minutes, [22, 22]);
    assert.equal(call.payload.series.kind, "series");
    assert.match(call.instructions, /ONLY the supplied act/);
  }
  const before = site.calls.run.length;
  await automation.animeRewrite(state, { fix: { problems: ["只修台詞"] } }, result.video, "writer", "owner-fix");
  assert.equal(site.calls.run.length - before, 5);
  assert.ok(site.calls.run.slice(before).every((call) => call.payload.video.scenes.length === 1), "a repair never asks for a whole episode output");
});

test("a native silent-action edit rechecks and returns to owner script review before any paid stage", async () => {
  const { approve, approvalState } = await import("../core/approvals.mjs");
  const { writeScreenplay } = await import("../core/screenplay.mjs");
  const { lintVideo } = await import("../core/lint.mjs");
  const { fixtureLexicon } = await import("../core/fixtures/load.mjs");
  const box = sandbox("borrowed-dawn-e001", "drama");
  const series = { ...ANIME_SERIES, episode: 1, chapter: 1, closed_ending: false };
  const doc = dramaFixture();
  const shot = doc.scenes.find((scene) => scene.template === "shot");
  doc.scenes = Array.from({ length: 250 }, (_, index) => ({ ...structuredClone(shot), id: `approved-shot-${index}`, ...(index % 85 === 0 ? { chapter: `故事第${index + 1}幕` } : {}), data: { ...shot.data, fit: "trim", prompt: `${shot.data.prompt}, composition ${index + 1}` }, lines: [{ ...shot.lines[0], id: index.toString(36).padStart(6, "0"), text: "沈澈扶起受傷的工人，塔拉關上漏氣的管線。", speaker: "narrator" }] }));
  doc.scenes[0].lines = [];
  doc.scenes[0].action_seconds = 6;
  doc.scenes[0].data.motion = "the girl pulls the worker away from escaping steam";
  doc.thumbnail.data.shot = doc.scenes[0].id;
  const settings = { voice: doc.voice, drama: { series_script_gate: false } };
  const video = settle(doc, { slug: box.slug, settings, root: box.root, format: "drama", series, cast: doc.characters });
  const snapshot = { ...series, characters: video.characters, series, beats: {} };
  assert.deepEqual(lintVideo(video, { brief: readFileSync(path.join(box.dir, "brief.md"), "utf8"), lexicon: fixtureLexicon(), series: snapshot }).errors, [], "the long fixture actually clears production lint");
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(video));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify(snapshot));
  writeFileSync(path.join(box.dir, "verify-1.md"), "# Checked\n");
  mkdirSync(path.join(box.workdir, "review"), { recursive: true });
  const check = path.join(box.workdir, "review", "script-check.json");
  writeFileSync(check, JSON.stringify(scriptCheckBinding(video)));
  writeScreenplay(box.dir, video);
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  await approve({ gate: "script", docDir: box.dir, workdir: box.workdir });
  const changed = structuredClone(video);
  changed.scenes[0].data.motion = "the girl pushes the worker toward escaping steam";
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(changed));
  const stages = [];
  const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, now: () => new Date("2026-10-02T00:00:00Z"), stdout: { write() {} }, runCommand: async (command) => { assert.equal(command[0], "review-push", "no paid media command is allowed"); stages.push("owner review"); return { code: 0, out: "sent" }; } };
  const automation = new Automation(ctx, { reviews: async () => ({ reviews: [] }) }, settings);
  automation.refs = smallRefs;
  automation.verify = async (state) => { stages.push("verify"); state.verified = true; writeFileSync(check, JSON.stringify(scriptCheckBinding(changed))); return "reverified"; };
  automation.media = async () => { throw new Error("paid media reached stale script approval"); };
  const state = { slug: box.slug, format: "drama", status: "active", production_policy: series.production_policy, runtime_spec: series.runtime_spec, category: "anime", series, verified: true, listener_done: true, notes: [], prompt_fixes: {}, source_urls: [] };
  assert.equal(await automation.advance(state), "reverified");
  assert.equal((await approvalState({ gate: "script", docDir: box.dir, workdir: box.workdir })).status, "stale");
  assert.match(await automation.advance(state), /sent to \/admin\/videos/);
  assert.deepEqual(stages, ["verify", "owner review"], "fresh verifier evidence cannot replace the owner's action approval");
});

test("the script verdict reads the craft rows on the script itself: the opening and coverage rows send it back, the pace rows do not", () => {
  const passing = { coverage: { hook: "有", conflict: "有", turn: "有", cliffhanger: "有" }, problems: [], similar_works: [] };
  const narrated = dramaFixture();
  const craft = craftChecks(narrated, { timeline: estimateTimeline(narrated) });
  assert.ok(craft.applies && craft.checks.some((check) => check.id === "pace.median" && !check.ok), "the fixture misses the pace rows");
  const verdict = scriptVerdict(passing, SERIES, craft);
  assert.equal(verdict.passed, false);
  assert.match(verdict.problems.join("\n"), /craft hook\.opening: shots that start in the first 10 s 2, target ≥ 4; open inside the event/);
  assert.ok(!verdict.problems.some((problem) => /pace\./.test(problem)), "the pace rows are warnings the writer answers, not a reason to send the script back");
  assert.deepEqual(scriptVerdict(passing, SERIES, null), { passed: true, problems: [] }, "without a report (a long anime, no cast) nothing is added");
  assert.deepEqual(scriptVerdict(passing, SERIES, { applies: false, checks: [] }), { passed: true, problems: [] });
});
