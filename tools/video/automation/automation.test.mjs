import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { lookHash, shotScenes, subtitlesHash } from "../core/drama.mjs";
import { dramaFixture, fixture, sandbox } from "../core/fixtures/load.mjs";
import { readJson, ROOT } from "../core/paths.mjs";
import { pipelineStatus } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { automationClient } from "./client.mjs";
import { EDITORIAL_USER_AGENT, pageReader, pageText, urlsIn } from "./fetch.mjs";
import { Automation, automatedVideos, mainGuide, MAX_PROMPT_FIX_ROUNDS, planProblem, settle, sheetDone } from "./flow.mjs";
import { DRAMA_INSTRUCTIONS, INSTRUCTIONS, instructionsFor, parseAnswer, references } from "./prompts.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const SITE = "https://site.test";

test("a page is read as its text, without scripts, comments or tags", () => {
  const html = `<html><head><title>Plans &amp; pricing</title><script>var x = "<b>no</b>";</script><style>p{}</style></head>
    <body><!-- hidden --><h1>Go</h1><p>NT$270&nbsp;a month &#x2014; tax included</p><ul><li>one</li><li>two</li></ul></body></html>`;
  assert.equal(pageText(html), "Plans & pricing\nGo\nNT$270 a month — tax included\none\ntwo");
  assert.deepEqual(urlsIn("c1｜Go｜https://openai.com/a｜2026\nc2｜Plus｜https://openai.com/a，again https://help.openai.com/b."), ["https://openai.com/a", "https://help.openai.com/b"]);
});

test("pages are read with the editorial agent, a second apart per host, https only", async () => {
  let clock = 1_000_000;
  const waits = [];
  const seen = [];
  const read = pageReader({
    now: () => clock,
    sleep: async (ms) => {
      waits.push(ms);
      clock += ms;
    },
    fetchImpl: async (url, init) => {
      seen.push([url, init.headers["User-Agent"]]);
      if (url.endsWith("/missing")) return new Response("gone", { status: 404, headers: { "content-type": "text/html" } });
      return new Response("<p>" + "字".repeat(50_000) + "</p>", { status: 200, headers: { "content-type": "text/html; charset=utf-8" } });
    },
  });
  const first = await read("https://openai.com/a");
  const second = await read("https://openai.com/missing");
  const other = await read("https://help.openai.com/c");
  const insecure = await read("http://openai.com/a");
  assert.equal(first.ok, true);
  assert.equal(first.truncated, true);
  assert.equal(first.text.length, 40_000);
  assert.deepEqual([second.ok, second.status], [false, 404]);
  assert.equal(other.ok, true);
  assert.equal(insecure.ok, false);
  assert.equal(seen.length, 3, "an http URL is never requested");
  assert.ok(seen.every(([, agent]) => agent === EDITORIAL_USER_AGENT));
  assert.deepEqual(waits, [1100], "only the second request to the same host waited");
});

test("a model's answer is read as JSON, fenced or not", () => {
  assert.deepEqual(parseAnswer('{"a": 1}'), { a: 1 });
  assert.deepEqual(parseAnswer('```json\n{"a": 2}\n```'), { a: 2 });
  assert.deepEqual(parseAnswer('Here it is: {"a": 3} done'), { a: 3 });
  assert.throws(() => parseAnswer("no json here"), SyntaxError);
  assert.deepEqual(Object.keys(INSTRUCTIONS).sort(), ["caption_reviewer", "listener", "planner", "translator", "verifier", "writer"]);
  for (const text of Object.values(INSTRUCTIONS)) assert.match(text, /Never invent an experience/);
  const refs = references(ROOT);
  assert.ok(refs.script_writing.length > 500 && refs.channel.length > 500);
  assert.ok(refs.showcase.scenes.length >= 10, "the showcase has one scene per template");
});

const brief = (options = ["A", "B"]) =>
  [
    "# ChatGPT 廣告怎麼關",
    "## 觀眾",
    "用免費版的人",
    "## 觀眾看完能做到的事",
    "自己關掉廣告",
    "## 站主觀點",
    "（提案）只為了廣告不必升級",
    "## 示範或實算",
    "一年多少錢",
    "## 大綱",
    ...options.flatMap((key) => [`### 選項 ${key}：角度 ${key}`, `一行說明：說明 ${key}`, `開場鉤子：「問題 ${key}？」`, "- 開場 30 秒", "- 主體 400 秒", "- 結論 60 秒"]),
    "## 會過期的事實",
    "價格 https://openai.com/a",
    "## 素材",
    "https://openai.com/a",
    "## 不做的事",
    "不談投資",
    "",
  ].join("\n");

test("a planner's brief must have a new slug, the owner's sections and two options", () => {
  const plan = { slug: "chatgpt-ads-off", brief: brief(), source_urls: ["https://openai.com/a"] };
  assert.equal(planProblem(plan, new Set()), null);
  assert.match(planProblem({ ...plan, slug: "Bad Slug" }, new Set()), /kebab-case/);
  assert.match(planProblem(plan, new Set(["chatgpt-ads-off"])), /already used/);
  assert.match(planProblem({ ...plan, brief: brief(["A"]) }, new Set()), /2 or 3 options/);
  assert.match(planProblem({ ...plan, brief: plan.brief.replace("## 站主觀點", "## 觀點") }, new Set()), /站主觀點/);
  assert.match(planProblem({ ...plan, source_urls: ["http://x"] }, new Set()), /https/);
  const used = new Set(["ai-news-gemini-student-offer-20260820"]);
  assert.match(planProblem({ ...plan, source_guide: "ai-news-gemini-student-offer-20260820" }, new Set(), used), /earlier video retells/);
  const cited = { ...plan, source_guide: null, source_urls: ["https://mokaair.com/zh-TW/guides/ai-news-gemini-student-offer-20260820", "https://blog.google/x"] };
  assert.match(planProblem(cited, new Set(), used), /earlier video retells/, "an unnamed article is its first site link");
  assert.equal(mainGuide(cited), "ai-news-gemini-student-offer-20260820");
  assert.equal(planProblem({ ...plan, source_guide: "chatgpt-ads-status" }, new Set(), used), null);
});

test("the CLI entry does not await at its top level, so auto can run sub-commands through it", () => {
  // flow.mjs runs review-pull, tts and the rest by importing ../cli.mjs. When cli.mjs is the
  // process entry and still awaiting main() at its top level, that import never settles and Node
  // exits with 13. Only the real entry shows it; these tests import cli.mjs as a plain module.
  const source = readFileSync(path.join(ROOT, "tools", "video", "cli.mjs"), "utf8");
  const entry = source.slice(source.indexOf("if (process.argv[1]"));
  assert.ok(entry.length > 0, "cli.mjs still starts main when run directly");
  assert.doesNotMatch(entry, /\bawait\b/);
});

test("a worksheet is done only when every line, chapter, title, description and tag is filled", () => {
  const sheet = { lines: [{ id: "k7p2", todo: false, text: "Hi" }], chapters: [{ scene: "hook", text: "Intro" }], title: { text: "T" }, description: { text: "D" }, tags: { text: ["ai"] } };
  assert.equal(sheetDone(sheet), true);
  assert.equal(sheetDone({ ...sheet, lines: [{ id: "k7p2", todo: true, text: "" }] }), false);
  assert.equal(sheetDone({ ...sheet, chapters: [{ scene: "hook", text: "" }] }), false);
  assert.equal(sheetDone({ ...sheet, tags: { text: [] } }), false);
});

/** The site as the worker sees it: settings, topics, the model runner, reviews, drama requests and source pages. */
function fakeSite({ settings = {}, answers = {}, budgetLeft = Infinity, paused = false, videos = [], dramaRequests = [] } = {}) {
  const calls = { run: [], reviews: [], reports: [], pages: [], drama: [] };
  const requests = dramaRequests.map((request) => ({ status: "queued", slug: null, ...request }));
  const projects = new Map();
  // /admin/videos as a list: videos made elsewhere, then whatever the worker reports.
  const listed = new Map(videos.map((video) => [video.slug, { dropped_at: null, dropped_note: null, source_guide: null, ...video }]));
  const reviewsOf = (slug) => projects.get(slug) ?? projects.set(slug, []).get(slug);
  const current = {
    enabled: true, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3,
    topic_scope: ["AI"], topic_avoid: ["投資建議"], topic_from_site: true, topic_from_search: true,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" },
    target_minutes_min: 1, target_minutes_max: 12, caption_locales: ["en"], max_drafts_per_month: 8,
    monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true, ...settings,
  };
  const json = (body, status = 200) => Response.json(body, { status });
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    if (!url.startsWith(SITE)) {
      calls.pages.push(url);
      return new Response(`<title>Source</title><p>Go costs NT$270 a month at ${url}</p>`, { status: 200, headers: { "content-type": "text/html" } });
    }
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return json(current);
    if (pathname === "/api/video/automation/videos") return json([...listed.values()]);
    if (pathname === "/api/video/automation/topics") return json({ topics: [{ source: "site", title: "ChatGPT 廣告", summary: "s", url: "https://mokaair.com/zh-TW/guides/chatgpt-ads-status", slug: "chatgpt-ads-status", date: "2026-09-24" }], notes: [] });
    if (pathname === "/api/video/automation/drama-requests/next") return json({ request: requests.find((request) => request.status === "queued") ?? null });
    const drama = /^\/api\/video\/automation\/drama-requests\/([^/]+)\/(start|done)$/.exec(pathname);
    if (drama) {
      const request = requests.find((each) => each.id === drama[1]);
      calls.drama.push({ id: drama[1], action: drama[2], slug: body?.slug ?? null });
      if (!request) return json({ code: "video_drama_request_not_found", detail: "no" }, 404);
      Object.assign(request, drama[2] === "start" ? { status: "started", slug: body.slug } : { status: "done" });
      return json(request);
    }
    if (pathname === "/api/video/automation/run") {
      calls.run.push(body);
      if (paused) return json({ code: "video_ai_subscription_paused", detail: "every Claude account is at or above 80%" }, 429);
      if (budgetLeft-- <= 0) return json({ code: "video_ai_budget_exhausted", detail: "本月模型 token 已用完" }, 429);
      const answer = answers[body.stage]?.(body) ?? {};
      return json({ text: JSON.stringify(answer), provider: "anthropic", model: "claude-sonnet-5", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 20_000_000, drafts: 1, draft_budget: 8, calls: 1, failed_calls: 0 } });
    }
    const match = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (match) {
      const [, slug, sub] = match;
      if (init.method === "PUT") {
        calls.reports.push({ slug, ...body });
        const known = listed.get(slug) ?? { slug, dropped_at: null, dropped_note: null, source_guide: null };
        listed.set(slug, { ...known, title: body.title, source_guide: body.source_guide ?? known.source_guide });
        return json({ slug, reviews: reviewsOf(slug) });
      }
      if (sub && init.method === "POST") {
        const list = reviewsOf(slug);
        const same = list.find((review) => review.gate === body.gate && review.content_sha256 === body.content_sha256 && (review.subject ?? null) === (body.subject ?? null));
        if (same) return json(same);
        const review = { id: `r${list.length + 1}`, status: "pending", choice: null, note: null, decided_at: null, created_at: new Date().toISOString(), ...body };
        list.unshift(review);
        calls.reviews.push(review);
        return json(review);
      }
      if (!projects.has(slug)) return json({ code: "video_project_not_found", detail: "no" }, 404);
      return json({ slug, title: slug, stage: "x", checklist: [], youtube_video_id: null, reviews: reviewsOf(slug) });
    }
    return json({ code: "not_found", detail: pathname }, 404);
  };
  return { calls, fetchImpl, reviewsOf, listed, settings: current, requests };
}

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
      EXIT,
    },
  };
}

const smallRefs = { script_writing: "short sentences", formats: "tutorial", channel: "Mokaair", showcase: { scenes: [] }, minimal: fixture() };

function answersFor(slug) {
  const video = { ...fixture(), slug };
  return {
    planner: (body) => ({ slug, title: "ChatGPT 廣告怎麼關", source_guide: "chatgpt-ads-status", source_urls: ["https://openai.com/a"], brief: body.payload.owner_note ? brief(["A", "C"]) : brief() }),
    writer: () => ({ video, claims: "c1｜Go 每月 270 元｜https://openai.com/a｜2026-09-25｜hook\n", lexicon_additions: { Sulafat: null, "bad term!": "x" } }),
    verifier: () => ({ report: "# 查核第 1 輪\n", video: null, claims: "c1｜Go 每月 270 元｜https://openai.com/a｜2026-09-25｜hook｜CONFIRMED\n", changed_facts: 0 }),
    listener: () => ({ video, edits: [] }),
  };
}

test("auto takes a video from a topic to the outline, waits for the owner, then writes, checks and edits it", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug) });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /planned from 1 topics; outline sent/);
  const dir = path.join(box.root, "docs", "videos", slug);
  assert.ok(existsSync(path.join(dir, "brief.md")));
  assert.equal(site.calls.reviews[0].gate, "outline");
  assert.deepEqual(site.calls.reviews[0].payload.options.map((option) => option.key), ["A", "B"]);
  assert.equal(site.calls.run[0].stage, "planner");
  assert.equal(site.calls.run[0].payload.earlier_videos[0].slug, "fixture-minimal", "the planner sees the earlier videos");
  assert.equal(await automation.step(), null, "the outline waits for the owner and the next draft is not due");

  site.reviewsOf(slug)[0].status = "approved";
  site.reviewsOf(slug)[0].choice = "B";
  assert.match(await automation.step(), /chose outline B/);
  assert.match(readFileSync(path.join(box.work, slug, "approvals.json"), "utf8"), /"gate": "outline"/);

  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.equal(writer.payload.chosen_option.key, "B");
  assert.deepEqual(writer.payload.sources.map((page) => page.url), ["https://mokaair.com/zh-TW/guides/chatgpt-ads-status", "https://openai.com/a"]);
  assert.equal(writer.payload.line_ids.length, 140);
  const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
  assert.deepEqual([video.slug, video.voice.name], [slug, "Sulafat"]);
  assert.equal(video.source_guide, undefined, "an article with no content pack in this repository is not linked by pack");
  assert.equal(video.voice.model, undefined, "a null setting is not written into the script");
  assert.equal(video.voice.rate, undefined, "a Gemini voice has no rate");
  const lexicon = JSON.parse(readFileSync(path.join(box.root, "docs", "videos", "lexicon.json"), "utf8"));
  assert.equal(lexicon.terms.Sulafat, null);
  assert.equal("bad term!" in lexicon.terms, false);

  assert.match(await automation.step(), /fact-check round 1, 0 facts changed/);
  assert.ok(existsSync(path.join(dir, "verify-1.md")));
  const verifier = site.calls.run.find((call) => call.stage === "verifier");
  assert.equal(verifier.payload.round, 1);
  assert.ok(verifier.payload.sources.every((page) => page.ok));
  assert.match(await automation.step(), /listener edit, 0 changes/);

  const status = await pipelineStatus({ slug, root: box.root, workdir: path.join(box.work, slug) });
  assert.equal(status.next.id, "narration synthesized");
  assert.deepEqual(automatedVideos(box.work).map((state) => [state.slug, state.verified, state.listener_done]), [[slug, true, true]]);
});

test("the planner sees every video on /admin/videos and may not retell an article one of them used", async () => {
  const box = sandbox();
  const elsewhere = { slug: "gemini-student-offer", title: "Gemini 學生方案", source_guide: "chatgpt-ads-status" };
  const site = fakeSite({ answers: answersFor("chatgpt-ads-off"), videos: [elsewhere] });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /not usable \(the site article "chatgpt-ads-status" is what an earlier video retells/);
  const [first, second] = site.calls.run;
  assert.ok(first.payload.earlier_videos.some((video) => video.slug === "gemini-student-offer" && video.source_guide === "chatgpt-ads-status"));
  assert.deepEqual(first.payload.used_guides, ["chatgpt-ads-status"]);
  assert.match(second.payload.previous_problem, /chatgpt-ads-status/, "the second try is told why the first failed");
  assert.equal(site.calls.reviews.length, 0, "nothing reaches the owner");
});

test("a video the owner drops is left alone, frees its place and keeps its topic taken", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug), settings: { max_waiting_drafts: 1, draft_interval_hours: 1 } });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  await automation.step();
  assert.equal(site.calls.reports[0].source_guide, "chatgpt-ads-status", "the site learns the article");
  Object.assign(site.listed.get(slug), { dropped_at: "2026-09-25T09:30:00Z", dropped_note: "第二批做過了" });
  assert.match(await automation.step(), /the owner dropped it \(第二批做過了\)/);
  assert.equal(automatedVideos(box.work)[0].status, "dropped");
  assert.equal(await automation.step(), null, "a dropped video is not advanced");

  clock.now += 2 * 3600_000;
  const planned = site.calls.run.length;
  assert.match(await automation.step(), /not usable/, "the dropped video no longer blocks a new draft");
  const payload = site.calls.run[planned].payload;
  assert.ok(payload.earlier_videos.some((video) => video.slug === slug && video.dropped === true));
  assert.deepEqual(payload.used_guides, ["chatgpt-ads-status"], "its article still counts as used");
});

test("a writer that answers without a script is asked once a run, and the video is blocked the second time", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const answers = { ...answersFor(slug), writer: () => ({ note: "The sources have no official page." }) };
  const site = fakeSite({ answers });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx, out } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  await automation.step();
  Object.assign(site.reviewsOf(slug)[0], { status: "approved", choice: "B" });
  const writers = () => site.calls.run.filter((call) => call.stage === "writer").length;

  assert.equal(await main(["auto"], ctx), EXIT.ok, out.stderr);
  assert.match(out.stdout, /chose outline B/);
  assert.match(out.stdout, /writer gave nothing usable \(the script the answer has no video object; the answer is in answers[\\/]writer-/);
  assert.equal(writers(), 1, "one try in a run, not forty");
  const state = automatedVideos(box.work)[0];
  assert.deepEqual([state.status, state.failures], ["active", { writer: 1 }]);
  const [kept] = readdirSync(path.join(box.work, slug, "answers"));
  assert.match(readFileSync(path.join(box.work, slug, "answers", kept), "utf8"), /no official page/);

  assert.equal(await main(["auto"], ctx), EXIT.ok, out.stderr);
  assert.equal(writers(), 2);
  assert.equal(automatedVideos(box.work)[0].status, "blocked");
  assert.match(site.calls.reports.at(-1).checklist[0].label, /^卡住，需要人處理：writer failed 2 times in a row/);
  assert.equal(await main(["auto"], ctx), EXIT.ok);
  assert.equal(writers(), 2, "a blocked video is not asked again");
});

test("an outline sent back is re-planned with the owner's note, and a spent budget stops auto for the owner", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug) });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  await automation.step();
  Object.assign(site.reviewsOf(slug)[0], { status: "rejected", note: "換一個角度" });
  assert.match(await automation.step(), /brief rewritten after the owner's note; outline re-sent/);
  const replan = site.calls.run.at(-1);
  assert.equal(replan.slug, slug);
  assert.equal(replan.payload.owner_note, "換一個角度");
  assert.deepEqual(site.reviewsOf(slug)[0].payload.options.map((option) => option.key), ["A", "C"]);

  const spent = fakeSite({ answers: answersFor("other"), budgetLeft: 0 });
  const other = sandbox();
  const run = context(other, spent.fetchImpl, clock);
  assert.equal(await main(["auto", "--once"], run.ctx), EXIT.owner);
  assert.match(run.out.stderr, /本月模型 token 已用完/);

  const waiting = fakeSite({ answers: answersFor("other"), paused: true });
  const pause = context(sandbox(), waiting.fetchImpl, clock);
  assert.equal(await main(["auto", "--once"], pause.ctx), EXIT.external);
  assert.equal(waiting.calls.run.length, 1, "a paused subscription is not retried within the run");
  assert.match(pause.out.stderr, /at or above 80%/);

  const off = fakeSite({ settings: { enabled: false } });
  const quiet = context(sandbox(), off.fetchImpl, clock);
  assert.equal(await main(["auto"], quiet.ctx), EXIT.ok);
  assert.match(quiet.out.stdout, /off in the settings/);
  assert.equal(off.calls.run.length, 0);
});

const DRAMA_SETTINGS = { drama_enabled: true, style_preset: "ink-wash", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [{ provider: "gemini", name: "Kore", hint: "少女" }] };

test("a drama is settled with the settings tab's preset, subtitles and music, and its brief has the bible's sections", () => {
  const settings = { voice: { provider: "gemini", name: "Sulafat", style: "s", model: null, rate: "+0%" }, drama: DRAMA_SETTINGS };
  const video = { ...dramaFixture(), slug: "x" };
  delete video.look.preset;
  const settled = settle(video, { slug: "jingwei", settings, sourceGuide: null, root: ROOT, format: "drama" });
  assert.equal(settled.format, "drama");
  assert.equal(settled.look.preset, "ink-wash", "the settings tab's preset when the writer named none");
  assert.equal(settled.look.style, video.look.style, "the writer's own style stays");
  assert.equal(settled.subtitles.burn_in, true);
  assert.equal(settled.music, undefined, "music is off in the settings");
  assert.equal(settled.voice.name, "Sulafat");
  const kept = settle({ ...dramaFixture(), slug: "x" }, { slug: "y", settings: { ...settings, drama: { ...DRAMA_SETTINGS, music_enabled: true } }, sourceGuide: null, root: ROOT, format: "drama" });
  assert.equal(kept.look.preset, "cinematic-3d", "the writer's preset wins");
  assert.ok(kept.music);
  const slides = settle(fixture(), { slug: "z", settings, sourceGuide: null, root: ROOT });
  assert.notEqual(slides.format, "drama", "a slides video is untouched");
  assert.equal(slides.look, undefined);

  const bible = "# 精衛\n## 故事前提\n溺水化鳥\n## 角色\n精衛\n## 站主觀點\n（提案）\n## 幕\n三幕\n## 大綱\n### 選項 A：告別\n一行說明：先告別\n開場鉤子：「很久以前」\n### 選項 B：風暴\n一行說明：先風暴\n開場鉤子：「那一天」\n";
  assert.equal(planProblem({ slug: "jingwei", brief: bible, source_urls: [] }, new Set(), new Set(), "drama"), null);
  assert.match(planProblem({ slug: "jingwei", brief: bible.replace("## 角色", "## 人物"), source_urls: [] }, new Set(), new Set(), "drama"), /角色/);
  assert.match(planProblem({ slug: "jingwei", brief: bible, source_urls: [] }, new Set()), /觀眾看完能做到的事/, "a tutorial's brief wants its own sections");

  assert.deepEqual(Object.keys(DRAMA_INSTRUCTIONS).sort(), ["listener", "planner", "verifier", "writer"]);
  assert.match(instructionsFor("writer", "drama"), /"fix" is present/);
  assert.match(instructionsFor("planner", "drama"), /## 故事前提/);
  assert.equal(instructionsFor("translator", "drama"), INSTRUCTIONS.translator);
  assert.equal(instructionsFor("writer"), INSTRUCTIONS.writer);
  assert.ok(references(ROOT).drama_example.format === "drama");
});

const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

test("an owner's drama request is planned first, its failed sheets go back to the writer, the gates wait for the owner, and a spent cap blocks the clips", async () => {
  const box = sandbox();
  const slug = "jingwei-fills-the-sea";
  const example = dramaFixture();
  const bible = [
    "# 精衛填海",
    "## 故事前提",
    "炎帝最小的女兒在東海溺水，化成一隻鳥。",
    "## 角色",
    "- jingwei 精衛：a girl of about twelve",
    "- yandi 炎帝：a tall emperor",
    "## 站主觀點",
    "（提案）明知做不到還是要做。",
    "## 幕",
    "三幕。",
    "## 大綱",
    "### 選項 A：從告別講起",
    "一行說明：先給告別。",
    "開場鉤子：「很久以前，發鳩山上住著炎帝最小的女兒。」",
    "### 選項 B：從風暴講起",
    "一行說明：先給風暴。",
    "開場鉤子：「那一天，東海起了大風。」",
    "",
  ].join("\n");
  const answers = {
    planner: (body) => ({ slug, title: "精衛填海", source_guide: null, source_urls: ["https://zh.wikisource.org/wiki/x"], brief: bible }),
    writer: (body) => {
      if (body.payload.fix) {
        const video = structuredClone(body.payload.video);
        for (const target of body.payload.fix.targets) {
          const character = video.characters.find((each) => each.id === target.id);
          if (character) character.appearance = `${character.appearance}, plain bronze crown without gems`;
        }
        return { video };
      }
      return { video: { ...structuredClone(example), slug }, claims: "原創：山海經北山經\n", lexicon_additions: {} };
    },
    verifier: () => ({ report: "# 連貫性第 1 輪\n", video: null, claims: "原創\n", changed_facts: 0 }),
    listener: (body) => ({ video: body.payload.video, edits: [] }),
  };
  const request = { id: "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b", premise: "精衛填海：炎帝最小的女兒在東海溺水，化成一隻鳥。", title: null, source_guide: null, style_preset: "cinematic-3d", target_minutes: 2, note: "旁白慢一點" };
  // One video at a time: the owner's request takes the place, so no scheduled draft starts beside it.
  const site = fakeSite({ answers, settings: { drama: DRAMA_SETTINGS, max_waiting_drafts: 1 }, dramaRequests: [request] });
  const clock = { now: Date.parse("2026-09-26T10:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const workdir = path.join(box.work, slug);
  const docFile = () => path.join(box.root, "docs", "videos", slug, "video.json");
  const currentVideo = () => JSON.parse(readFileSync(docFile(), "utf8"));
  const lexicon = () => readJson(path.join(box.root, "docs", "videos", "lexicon.json"));
  const runs = [];
  let lookRuns = 0;
  // The media stages, the narration and the uploads play here without any vendor; review-pull is real.
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    const [name] = command;
    const video = existsSync(docFile()) ? currentVideo() : null;
    const write = (file, data) => {
      mkdirSync(path.dirname(path.join(workdir, file)), { recursive: true });
      writeFileSync(path.join(workdir, file), JSON.stringify(data));
    };
    if (name === "tts") {
      writeSyntheticNarration(video, lexicon(), workdir);
      return { code: 0, out: "narration" };
    }
    if (name === "check-audio") return { code: 0, out: "every line passed" };
    if (name === "look") {
      const candidate = (passed) => [{ n: 1, seed: 1, file: "characters/x/001.png", sha256: "1".repeat(64), judge: { overall: passed ? 8 : 4, passed, problems: passed ? [] : ["wrong crown"] } }];
      const failing = lookRuns++ === 0;
      write("characters/manifest.json", {
        look_hash: lookHash(video),
        characters: {
          jingwei: { name: "精衛", candidates: candidate(true), suggested: 1, needs_review: false },
          yandi: { name: "炎帝", candidates: candidate(!failing), suggested: failing ? null : 1, needs_review: failing },
        },
      });
      return failing ? { code: 1, out: "ERROR yandi: no candidate passed the judge: wrong crown\nrewrite the appearance" } : { code: 0, out: "2 characters" };
    }
    if (name === "keyframes") {
      write("keyframes/manifest.json", { look_hash: lookHash(video), visual_hash: visualHash(video), shots: Object.fromEntries(shotScenes(video).map((scene) => [scene.id, { file: `keyframes/${scene.id}-1.png`, sha256: "2".repeat(64), needs_review: false, judge: { overall: 8, problems: [] } }])) });
      return { code: 0, out: "4 keyframes" };
    }
    if (name === "render") {
      write("frames/manifest.json", { visual_hash: visualHash(video), speech_hash: speechHash(video, lexicon()), subtitles_hash: subtitlesHash(video), theme_hash: "t", scenes: [], subtitles: { style: "drama", blank: "frames/sub-blank.png", cues: [] }, thumbnail: null });
      return { code: 0, out: "rendered" };
    }
    if (name === "clips") return { code: 3, out: "this video has spent US$180.00 and the next generation costs about US$1.20, past the per-video cap of US$180; raise max_usd_per_video on /admin/videos or stop here" };
    if (name === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      const list = site.reviewsOf(slug);
      if (gate === "look") {
        const manifest = readJson(path.join(workdir, "characters", "manifest.json"));
        for (const id of Object.keys(manifest.characters)) list.unshift({ id: `look-${id}-${list.length}`, gate: "look", subject: id, status: "pending", choice: null, note: null, decided_at: null, content_sha256: sha(path.join(workdir, "characters", "manifest.json")), payload: { options: [{ key: "A", index: 1 }] } });
      }
      if (gate === "audio") list.unshift({ id: `audio-${list.length}`, gate: "audio", status: "approved", choice: null, note: "Jev passed every line", decided_at: "2026-09-26T10:30:00Z", content_sha256: sha(path.join(workdir, "timeline.json")), payload: {} });
      // The server approves a storyboard on its own when the judge passed every shot and the owner allows it.
      if (gate === "storyboard") list.unshift({ id: `board-${list.length}`, gate: "storyboard", status: "approved", choice: null, note: null, decided_at: "2026-09-26T10:40:00Z", content_sha256: sha(path.join(workdir, "keyframes", "manifest.json")), payload: { shots: [], judge: { overall: 8, problems: [] } } });
      return { code: 0, out: `${gate} submitted` };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, runCommand: undefined, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = { ...smallRefs, drama: "the drama route", drama_example: example, drama_brief: bible };

  assert.match(await automation.step(), /drama: jingwei-fills-the-sea planned from the owner's request; outline sent/);
  const planner = site.calls.run[0];
  assert.equal(planner.stage, "planner");
  assert.equal(planner.payload.premise, request.premise);
  assert.deepEqual(planner.payload.target_minutes, [2, 2]);
  assert.match(planner.instructions, /story bible/);
  assert.deepEqual(site.calls.drama, [{ id: request.id, action: "start", slug }]);
  assert.equal(site.requests[0].status, "started");
  assert.equal(site.calls.reports.at(-1).format, "drama");
  const state = () => automatedVideos(box.work).find((each) => each.slug === slug);
  assert.equal(state().format, "drama");
  assert.equal(state().request_id, request.id);
  assert.deepEqual(state().notes, ["owner request: 旁白慢一點"]);
  assert.equal(await automation.step(), null, "the outline waits for the owner");

  Object.assign(site.reviewsOf(slug)[0], { status: "approved", choice: "A" });
  assert.match(await automation.step(), /chose outline A/);
  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.match(writer.instructions, /"format": "drama"/);
  assert.equal(writer.payload.drama_settings.style_preset, "cinematic-3d", "the request's preset");
  assert.deepEqual(writer.payload.target_minutes, [2, 2]);
  const written = currentVideo();
  assert.equal(written.format, "drama");
  assert.equal(written.music, undefined, "music is off in the settings");
  assert.equal(written.characters.length, 2);
  assert.match(await automation.step(), /fact-check round 1/);
  assert.match(site.calls.run.find((call) => call.stage === "verifier").instructions, /continuity checker/);
  assert.match(await automation.step(), /listener edit/);
  assert.match(site.calls.run.find((call) => call.stage === "listener").instructions, /"speaker"/);

  // look: the first run leaves 炎帝 without a passed sheet; the writer fixes the appearance; the second run passes.
  assert.match(await automation.step(), /look prompts fixed \(round 1\) for yandi; look runs again next/);
  const fix = site.calls.run.at(-1);
  assert.equal(fix.stage, "writer");
  assert.deepEqual(fix.payload.fix, { kind: "look", targets: [{ id: "yandi", problems: ["wrong crown"] }], problems: ["wrong crown"], owner_note: null });
  assert.match(currentVideo().characters[1].appearance, /plain bronze crown/);
  assert.equal(state().prompt_fixes.look, 1);
  assert.match(await automation.step(), /look done/);
  assert.equal(runs.filter((run) => run.startsWith("look ")).length, 2);
  assert.equal(state().prompt_fixes.look, undefined, "a passed stage clears its fix count");

  assert.match(await automation.step(), /character sheets sent to \/admin\/videos/);
  assert.equal(site.reviewsOf(slug).filter((review) => review.gate === "look").length, 2);
  assert.equal(await automation.step(), null, "the sheets wait for the owner");
  for (const review of site.reviewsOf(slug).filter((each) => each.gate === "look")) Object.assign(review, { status: "approved", choice: review.subject === "jingwei" ? "A" : null, decided_at: "2026-09-26T10:20:00Z" });
  assert.match(await automation.step(), /the owner chose the character sheets/);
  assert.deepEqual(readJson(path.join(workdir, "characters", "choice.json")).chosen, { jingwei: 1, yandi: 1 });
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "look"));

  assert.match(await automation.step(), /narration synthesized/);
  assert.match(await automation.step(), /narration checked \(Jev passed every line\) and sent for review/);
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "audio"), "the site's approval is pulled at once");
  assert.match(await automation.step(), /keyframes done/);
  assert.match(await automation.step(), /storyboard sent to \/admin\/videos/);
  assert.match(await automation.step(), /the owner approved the storyboard/);
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "storyboard"));
  assert.match(await automation.step(), /frames rendered/);
  assert.match(await automation.step(), /blocked — clips needs the owner: .*past the per-video cap/);
  assert.equal(state().status, "blocked");
  assert.match(site.calls.reports.at(-1).checklist[0].label, /^卡住，需要人處理：clips needs the owner/);
  // A blocked video frees its place: the next unit is a scheduled draft (not due to fail here), never the clips again.
  assert.match((await automation.step()) ?? "", /^draft:/);
  assert.equal(runs.filter((run) => run.startsWith("clips")).length, 1, "a blocked drama is not touched again");
  assert.ok(MAX_PROMPT_FIX_ROUNDS >= 2);
});
