import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { readApprovals } from "../core/approvals.mjs";
import { dramaFixture, sandbox } from "../core/fixtures/load.mjs";
import { readJson } from "../core/paths.mjs";
import { keepSheets, readStore, reuseSheets, sheetKey } from "../media/series-store.mjs";
import { automationClient } from "./client.mjs";
import { Automation, automatedVideos, settle } from "./flow.mjs";
import { instructionsFor, SERIES_INSTRUCTIONS } from "./prompts.mjs";
import { castFrom, chapterRange, documentPayload, documentProblem, episodeSlug, planDocument, seriesStep } from "./series.mjs";

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
  assert.deepEqual(Object.keys(SERIES_INSTRUCTIONS).sort(), ["planner:chapter", "planner:outline", "planner:setting", "verifier:episode", "verifier:recap", "writer:episode"]);
  assert.match(instructionsFor("planner", "drama", "", "setting"), /SETTING BOOK[\s\S]*conflict engine[\s\S]*RESERVED/);
  assert.match(instructionsFor("planner", "drama", "", "outline"), /stakes rise chapter by chapter/);
  assert.match(instructionsFor("planner", "drama", "", "chapter"), /HOOK inside the first 20 seconds[\s\S]*never end on the same cliffhanger type/);
  assert.match(instructionsFor("writer", "drama", "", "episode"), /"fix" is present[\s\S]*EPISODE OF A LONG SERIES/);
  assert.match(instructionsFor("verifier", "drama", "", "episode"), /coverage/);
  assert.match(instructionsFor("verifier", "drama", "", "recap"), /150 characters/);
  assert.match(instructionsFor("planner", "drama", "旁白慢", "setting"), /standing instructions[\s\S]*\n旁白慢$/);
  for (const text of Object.values(SERIES_INSTRUCTIONS)) assert.match(text, /original|existing work/);
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
function fakeSite({ jobs = [], answers = {}, settings = {} } = {}) {
  const calls = { run: [], docs: [], episodes: [], reports: [], reviews: [] };
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
    const docs = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/docs$/.exec(pathname);
    if (docs) {
      calls.docs.push({ series: docs[1], ...body });
      return json({ id: `d${calls.docs.length}`, ...body, version: calls.docs.filter((doc) => doc.kind === body.kind && doc.chapter_number === body.chapter_number).length, status: "review" }, 201);
    }
    const episode = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/episodes\/(\d+)\/(start|recap|done)$/.exec(pathname);
    if (episode) {
      calls.episodes.push({ series: episode[1], number: Number(episode[2]), action: episode[3], ...(body ?? {}) });
      if (episode[3] === "start") {
        const number = Number(episode[2]);
        const context = { series: SERIES, setting: SETTING, outline: null, chapter: CHAPTER, chapter_number: 1, chapter_range: [1, 10], episode: null, episodes: CHAPTER.body_json.episodes.map((each) => ({ ...each, chapter_number: 1, status: "ready", beats: each })), recaps: [{ number: 0, title: "序", recap: "鐘響了", state: {} }], mysteries: SETTING.body_json.mysteries };
        return json({ request: { id: `r${number}`, premise: `第 ${number} 集`, title: null, source_guide: null, style_preset: "cinematic-3d", target_minutes: 3, note: null, status: "started", slug: body.slug }, episode: { ...beats(number), chapter_number: 1, status: "started", slug: body.slug, beats: beats(number) }, context });
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
  assert.match(await planDocument(automation, job("outline")), /could not write the outline \(body_json.chapters must list exactly 3 chapters/);
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
  assert.deepEqual(state().series, { slug: "wenjian", episode: 1, chapter: 1 });
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
