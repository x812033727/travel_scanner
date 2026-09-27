import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { createHash, randomBytes } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { lookHash, shotScenes, subtitlesHash } from "../core/drama.mjs";
import { dramaFixture, fixture, sandbox } from "../core/fixtures/load.mjs";
import { atomicWrite, readJson, ROOT } from "../core/paths.mjs";
import { eachLine } from "../core/schema.mjs";
import { pipelineStatus } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { ITEM_IDS } from "../qa/checks.mjs";
import { jpegBytes } from "../qa/test-images.mjs";
import { PART_BYTES } from "../review/sync.mjs";
import { automationClient } from "./client.mjs";
import { EDITORIAL_USER_AGENT, pageReader, pageText, urlsIn } from "./fetch.mjs";
import { Automation, automatedVideos, mainGuide, MAX_PROMPT_FIX_ROUNDS, MAX_REPLANS, MAX_REWRITE_ROUNDS, planProblem, settle, sheetDone } from "./flow.mjs";
import { DRAMA_INSTRUCTIONS, INSTRUCTIONS, instructionsFor, LISTENER_REWRITE, parseAnswer, references, STANCE_HEADING } from "./prompts.mjs";

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

// The channel stance the owner writes on the settings tab (docs/videos/HANDS-OFF.md §頻道立場).
const STANCE = "1. 先把帳算清楚再花錢：付費是為了真的用得到的額度。\n2. 官方原文優先：價格以官方頁面當天的寫法為準。\n3. 每支影片都給觀眾一個看完就能做的動作。";

/** A planner's brief; `applies` names the stance points 站主觀點 opens with, null for the old proposal line. */
const brief = (options = ["A", "B"], { applies = null } = {}) =>
  [
    "# ChatGPT 廣告怎麼關",
    "## 觀眾",
    "用免費版的人",
    "## 觀眾看完能做到的事",
    "自己關掉廣告",
    "## 站主觀點",
    ...(applies ? [`套用立場：${applies}`, "只為了廣告不必升級，先算一年多少錢。"] : ["（提案）只為了廣告不必升級"]),
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

// The items the site requires on a final cut and on an upload package (judge.py QA_ITEMS, PACKAGE_ITEMS).
const QA_ITEMS = ["assemble", "render", "narration", "pace", "captions", "metadata", "facts", "links", "thumbnail", "policy", "disclosure"];
const PACKAGE_ITEMS = ["files", "descriptions", "captions", "disclosure"];

/** Jev's answer on an outline, as the judge endpoint shapes it (judge.py OutlinePick). */
function jevPick(choice, { passed = true, stance = 0.9, demo = 0.8, advice = 0.1, keys = ["A", "B"] } = {}) {
  const options = Object.fromEntries(keys.map((key) => [key, key === choice ? { stance, demo } : { stance: 0.5, demo: 0.5 }]));
  const probabilities = Object.fromEntries(keys.map((key) => [key, key === choice ? 0.74 : 0.26 / (keys.length - 1)]));
  const body = `符合立場 ${stance.toFixed(2)}、有示範 ${demo.toFixed(2)}、建議 ${advice.toFixed(2)}`;
  const note = passed ? `Jev 挑了 ${choice}（0.74）：${body}，依設定自動核准` : `Jev 挑了 ${choice}（0.74）：${body}；沒過關（有示範 ${demo.toFixed(2)} 低於 0.6）`;
  return { choice, probabilities, options, advice, passed, note };
}

/**
 * The site as the worker sees it: settings, topics, the model runner, the judge, reviews and
 * their files, drama requests and source pages. Reviews are decided on arrival by the server's
 * own rules (apps/api/app/video_automation/judge.py, settings.py): Jev's pick on an outline, the
 * quality check on a final cut, the package check on a publish, Jev's line check on a narration.
 * `judge(body)` answers the outline judgement (an object, or a Response for an error) once the
 * stance is written and the switch on; otherwise the site answers 409 as it does.
 */
function fakeSite({ settings = {}, answers = {}, budgetLeft = Infinity, paused = false, videos = [], dramaRequests = [], judge = null } = {}) {
  const calls = { run: [], reviews: [], reports: [], pages: [], drama: [], judge: [] };
  const files = new Map();
  const requests = dramaRequests.map((request) => ({ status: "queued", slug: null, ...request }));
  const projects = new Map();
  // /admin/videos as a list: videos made elsewhere, then whatever the worker reports.
  const listed = new Map(videos.map((video) => [video.slug, { dropped_at: null, dropped_note: null, source_guide: null, youtube_video_id: null, ...video }]));
  const reviewsOf = (slug) => projects.get(slug) ?? projects.set(slug, []).get(slug);
  const current = {
    enabled: true, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3,
    topic_scope: ["AI"], topic_avoid: ["投資建議"], topic_from_site: true, topic_from_search: true,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" },
    target_minutes_min: 1, target_minutes_max: 12, caption_locales: ["en"], max_drafts_per_month: 8,
    monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true,
    channel_stance: "", auto_pick_outline: true, auto_approve_final: true, ...settings,
  };
  const json = (body, status = 200) => Response.json(body, { status });
  const number = (value) => (typeof value === "number" && Number.isFinite(value) ? value : null);
  const pickPassed = (payload) => {
    const pick = payload.pick;
    if (!pick || typeof pick.choice !== "string" || !pick.options) return false;
    if (Array.isArray(payload.options) && !payload.options.some((option) => option.key === pick.choice)) return false;
    const chosen = pick.options[pick.choice];
    const [stance, demo, advice] = [number(chosen?.stance), number(chosen?.demo), number(pick.advice)];
    return stance !== null && demo !== null && advice !== null && stance >= 0.6 && demo >= 0.6 && advice <= 0.3;
  };
  const itemsPassed = (report, sha, required) =>
    report?.ok === true && report.final_sha256 === sha && Array.isArray(report.items) && required.every((id) => report.items.some((item) => item.id === id && item.ok === true));
  const audioPassed = (payload) => payload.check?.lines > 0 && payload.check.checked === payload.check.lines && payload.check.flagged === 0 && !(payload.flagged_lines?.length);
  const decideOnArrival = (review) => {
    let note = null;
    if (review.gate === "audio" && current.auto_approve_audio && audioPassed(review.payload)) note = "Jev 判斷每一句都唸對了，依設定自動核准";
    else if (review.gate === "outline" && current.auto_pick_outline && current.channel_stance.trim() && pickPassed(review.payload)) {
      note = review.payload.pick.note;
      review.choice = review.payload.pick.choice;
    } else if (review.gate === "final" && current.auto_approve_final && itemsPassed(review.payload.qa, review.content_sha256, QA_ITEMS)) note = "自動品管 11 項全過，依設定自動核准";
    else if (review.gate === "publish" && current.auto_approve_final && itemsPassed(review.payload.package, review.content_sha256, PACKAGE_ITEMS)) note = "上傳包 4 項齊全，依設定自動核准";
    if (note) Object.assign(review, { status: "approved", note, decided_at: new Date().toISOString() });
  };
  const fetchImpl = async (url, init = {}) => {
    const { pathname, searchParams } = new URL(url);
    if (!url.startsWith(SITE)) {
      calls.pages.push(url);
      return new Response(`<title>Source</title><p>Go costs NT$270 a month at ${url}</p>`, { status: 200, headers: { "content-type": "text/html" } });
    }
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const upload = /^\/api\/video\/reviews\/([a-z0-9-]+)\/files\/([0-9a-f]{64})$/.exec(pathname);
    if (upload) {
      const parts = files.get(upload[2]) ?? [];
      parts[Number(searchParams.get("part"))] = Buffer.from(init.body);
      files.set(upload[2], parts);
      return json({ received: parts.map((_, index) => index), complete: parts.filter(Boolean).length === Number(searchParams.get("parts")) });
    }
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return json(current);
    if (pathname === "/api/video/automation/videos") return json([...listed.values()]);
    if (pathname === "/api/video/automation/judge/outline") {
      calls.judge.push(body);
      if (!current.auto_pick_outline || !current.channel_stance.trim()) return json({ code: "video_judge_not_enabled", detail: "頻道立場還是空白，或「由 Jev 挑大綱」關著；大綱照舊等站主" }, 409);
      const answer = judge ? judge(body) : json({ code: "not_found", detail: pathname }, 404);
      return answer instanceof Response ? answer : json(answer);
    }
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
        const known = listed.get(slug) ?? { slug, dropped_at: null, dropped_note: null, source_guide: null, youtube_video_id: null };
        // As the server does (admin_service.upsert_project): a report without the id clears it.
        listed.set(slug, { ...known, title: body.title, source_guide: body.source_guide ?? known.source_guide, youtube_video_id: body.youtube_video_id ?? null });
        return json({ slug, reviews: reviewsOf(slug) });
      }
      if (sub && init.method === "POST") {
        const list = reviewsOf(slug);
        const same = list.find((review) => review.gate === body.gate && review.content_sha256 === body.content_sha256 && (review.subject ?? null) === (body.subject ?? null));
        if (same && same.status !== "pending") return json(same);
        if (same) {
          // The same file sent again while it waits: the newer payload replaces the older one and the rules run again.
          Object.assign(same, { summary: body.summary, payload: body.payload, files: body.files });
          decideOnArrival(same);
          return json(same);
        }
        for (const older of list) if (older.gate === body.gate && older.status === "pending" && (older.subject ?? null) === (body.subject ?? null)) older.status = "superseded";
        const review = { id: `r${list.length + 1}`, status: "pending", choice: null, note: null, decided_at: null, created_at: new Date().toISOString(), ...body };
        decideOnArrival(review);
        list.unshift(review);
        calls.reviews.push(review);
        return json(review);
      }
      if (!projects.has(slug)) return json({ code: "video_project_not_found", detail: "no" }, 404);
      return json({ slug, title: slug, stage: "x", checklist: [], youtube_video_id: listed.get(slug)?.youtube_video_id ?? null, reviews: reviewsOf(slug) });
    }
    return json({ code: "not_found", detail: pathname }, 404);
  };
  return { calls, fetchImpl, reviewsOf, listed, settings: current, requests, files };
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

function answersFor(slug, { applies = null } = {}) {
  const video = { ...fixture(), slug };
  return {
    planner: (body) => ({ slug, title: "ChatGPT 廣告怎麼關", source_guide: "chatgpt-ads-status", source_urls: ["https://openai.com/a"], brief: body.payload.owner_note ? brief(["A", "C"], { applies }) : brief(["A", "B"], { applies }) }),
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

  assert.match(await automation.step(), /planned from 1 topics; outline sent to \/admin\/videos for the owner \(頻道立場還是空白/);
  const dir = path.join(box.root, "docs", "videos", slug);
  assert.ok(existsSync(path.join(dir, "brief.md")));
  assert.equal(site.calls.reviews[0].gate, "outline");
  assert.deepEqual(site.calls.reviews[0].payload.options.map((option) => option.key), ["A", "B"]);
  assert.equal("pick" in site.calls.reviews[0].payload, false, "a site whose judge is off gets no pick");
  assert.equal(site.calls.reviews[0].status, "pending");
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
  assert.match(await automation.step(), /brief rewritten after the owner's note \(round 1\); outline sent to \/admin\/videos for the owner/);
  const replan = site.calls.run.at(-1);
  assert.equal(replan.slug, slug);
  assert.equal(replan.payload.owner_note, "換一個角度");
  assert.equal(replan.payload.sent_back_by, "owner");
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

// auto_pick_look is the drama-look ticket's switch (docs/videos/HANDS-OFF.md); the server applies it on look reviews.
const DRAMA_SETTINGS = { drama_enabled: true, style_preset: "ink-wash", subtitle_burn_in: true, music_enabled: false, auto_pick_look: false, character_voice_pool: [{ provider: "gemini", name: "Kore", hint: "少女" }] };

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

test("the owner's standing instructions from the settings tab end a stage's prompt, and a run names its format", async () => {
  assert.equal(instructionsFor("writer", "slides", "  "), INSTRUCTIONS.writer, "blank instructions add nothing");
  assert.match(instructionsFor("writer", "drama", " 結尾留懸念 "), /"fix" is present[\s\S]*## The owner's standing instructions\n[\s\S]*結尾留懸念$/);
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug), settings: { stage_instructions: { planner: "每集結尾留下一集的懸念" } } });
  const clock = { now: Date.parse("2026-09-25T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /planned from 1 topics/);
  const run = site.calls.run[0];
  assert.equal(run.stage, "planner");
  assert.equal(run.format, "slides", "the server files the prompt under the video's format");
  assert.match(run.instructions, /## The owner's standing instructions\n[\s\S]*每集結尾留下一集的懸念$/);
});

test("the channel stance ends the planner's and the writer's prompts, and a 站主觀點 that names no stance point is refused", () => {
  const planner = instructionsFor("planner", "slides", "", null, STANCE);
  assert.match(planner, /## The channel's stance\n[\s\S]*1\. 先把帳算清楚再花錢/);
  assert.ok(planner.startsWith(INSTRUCTIONS.planner), "the stance comes after the stage's own text");
  assert.match(INSTRUCTIONS.planner, /FIRST line reads 「套用立場：N、M」/);
  assert.match(DRAMA_INSTRUCTIONS.planner, /FIRST line reads 「套用立場：N、M」/);
  assert.match(instructionsFor("writer", "drama", "結尾留懸念", null, STANCE), /## The channel's stance\n[\s\S]*3\. 每支影片都給觀眾一個看完就能做的動作。\n\n## The owner's standing instructions\n[\s\S]*結尾留懸念$/, "the stance before the standing instructions");
  assert.match(instructionsFor("planner", "drama", "", "chapter", STANCE), /## The channel's stance/, "the series variants that plan episodes read it too");
  assert.match(instructionsFor("writer", "drama", "", "episode", STANCE), /## The channel's stance/);
  assert.equal(instructionsFor("verifier", "slides", "", null, STANCE), INSTRUCTIONS.verifier, "only the planner and the writer read the stance");
  assert.equal(instructionsFor("planner", "slides", "", null, "  "), INSTRUCTIONS.planner, "a blank stance adds nothing");
  assert.equal(STANCE_HEADING.split("\n")[0], "## The channel's stance");

  const plan = { slug: "chatgpt-ads-off", brief: brief(), source_urls: ["https://openai.com/a"] };
  assert.equal(planProblem(plan, new Set(), new Set(), "slides", ""), null, "without a stance the old rule holds");
  assert.match(planProblem(plan, new Set(), new Set(), "slides", STANCE), /站主觀點 does not apply the channel stance: the first line of "## 站主觀點" must read 「套用立場：N、M」/);
  assert.equal(planProblem({ ...plan, brief: brief(["A", "B"], { applies: "1、3" }) }, new Set(), new Set(), "slides", STANCE), null);
  assert.match(planProblem({ ...plan, brief: brief(["A", "B"], { applies: "4" }) }, new Set(), new Set(), "slides", STANCE), /names point 4, but the stance has only 1, 2, 3/);
});

test("with the stance written, Jev picks the outline and the site approves it on arrival, so the writer starts without the owner", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug, { applies: "1、3" }), settings: { channel_stance: STANCE }, judge: () => jevPick("B") });
  const clock = { now: Date.parse("2026-09-27T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  assert.match(await automation.step(), /planned from 1 topics; Jev picked outline B; outline sent to \/admin\/videos$/);
  assert.match(site.calls.run[0].instructions, /## The channel's stance\n[\s\S]*\n1\. 先把帳算清楚再花錢/);
  const [asked] = site.calls.judge;
  assert.deepEqual(Object.keys(asked), ["slug", "brief", "options"], "the judge's strict request model");
  assert.equal(asked.slug, slug);
  assert.match(asked.brief, /^# ChatGPT 廣告怎麼關\n/);
  assert.deepEqual(asked.options, [
    { key: "A", title: "角度 A", summary: "說明 A", hook: "問題 A？" },
    { key: "B", title: "角度 B", summary: "說明 B", hook: "問題 B？" },
  ]);
  const [review] = site.calls.reviews;
  assert.equal(review.gate, "outline");
  assert.deepEqual(review.payload.pick, jevPick("B"), "the whole answer travels as the pick");
  assert.deepEqual([review.status, review.choice], ["approved", "B"]);
  assert.match(review.summary, /企劃書與 2 個大綱選項（自動產生）；Jev 挑了 B/);
  assert.equal(automatedVideos(box.work)[0].last_pick.choice, "B");

  assert.match(await automation.step(), /Jev chose outline B \(Jev 挑了 B（0\.74）/);
  assert.match(readFileSync(path.join(box.work, slug, "approvals.json"), "utf8"), /"gate": "outline"/);
  assert.equal(automatedVideos(box.work)[0].chosen, "B");
  assert.match(await automation.step(), /script drafted and passes lint/);
  const writer = site.calls.run.find((call) => call.stage === "writer");
  assert.equal(writer.payload.chosen_option.key, "B");
  assert.match(writer.instructions, /## The channel's stance/);
});

test("an outline Jev does not pass goes back to the planner with Jev's note, and after MAX_REPLANS it waits for the owner with the last pick attached", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const site = fakeSite({ answers: answersFor(slug, { applies: "2" }), settings: { channel_stance: STANCE }, judge: (body) => jevPick("A", { passed: false, demo: 0.4, keys: body.options.map((option) => option.key) }) });
  const clock = { now: Date.parse("2026-09-27T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;

  const line = await automation.step();
  assert.match(line, /planned from 1 topics; brief rewritten after Jev's note \(round 1\); brief rewritten after Jev's note \(round 2\); Jev found no outline that passes after 2 rewrites \(Jev 挑了 A（0\.74）.*沒過關/);
  assert.match(line, /outline sent to \/admin\/videos for the owner, pick attached$/);
  const planners = site.calls.run.filter((call) => call.stage === "planner");
  assert.equal(planners.length, 1 + MAX_REPLANS, "the first plan and every rewrite Jev is allowed");
  for (const rewrite of planners.slice(1)) {
    assert.match(rewrite.payload.owner_note, /^Jev 挑了 A（0\.74）：.*沒過關（有示範 0\.40 低於 0\.6）$/);
    assert.equal(rewrite.payload.sent_back_by, "jev");
    assert.ok(rewrite.payload.previous_brief.includes("## 站主觀點"));
  }
  assert.equal(site.calls.judge.length, 1 + MAX_REPLANS, "every version was judged");
  const [review] = site.calls.reviews;
  assert.equal(review.status, "pending", "the owner decides now");
  assert.equal(review.payload.pick.passed, false, "the card shows Jev's table");
  assert.match(review.summary, /Jev 沒有挑出過關的大綱，請站主選/);
  const state = automatedVideos(box.work)[0];
  assert.equal(state.replans, MAX_REPLANS);
  assert.equal(state.notes.filter((note) => note.startsWith("outline sent back by Jev: ")).length, MAX_REPLANS);
  assert.equal(await automation.step(), null, "the outline waits for the owner");

  Object.assign(site.reviewsOf(slug)[0], { status: "approved", choice: "C", note: "C 比較好" });
  assert.match(await automation.step(), /the owner chose outline C \(C 比較好\)/);
  assert.equal(automatedVideos(box.work)[0].chosen, "C");
});

test("Jev being down ends the run and the next one asks again; a judge switched off means the owner chooses without a pick", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  let down = true;
  const site = fakeSite({
    answers: answersFor(slug, { applies: "1" }),
    settings: { channel_stance: STANCE },
    judge: () => (down ? Response.json({ code: "video_judge_upstream_failed", detail: "Jev 暫時無法判斷" }, { status: 502 }) : jevPick("A")),
  });
  const clock = { now: Date.parse("2026-09-27T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  assert.match(await automation.step(), /planned from 1 topics; Jev could not judge the outline \(Jev 暫時無法判斷\); the next run asks again$/);
  assert.equal(automation.halted, true, "nothing else would move this round");
  assert.equal(site.calls.reviews.length, 0, "the outline was not sent");
  assert.equal(automatedVideos(box.work)[0].status, "active");
  assert.ok(site.calls.judge.length >= 1);

  down = false;
  automation.halted = false;
  assert.match(await automation.step(), /^chatgpt-ads-off: Jev picked outline A; outline sent to \/admin\/videos$/);
  assert.equal(site.calls.run.filter((call) => call.stage === "planner").length, 1, "the brief was kept, not planned again");
  assert.deepEqual([site.calls.reviews[0].status, site.calls.reviews[0].choice], ["approved", "A"]);

  // The switch off: the site answers 409 and the owner chooses, whatever the stance says.
  const off = fakeSite({ answers: answersFor("other-video", { applies: "1" }), settings: { channel_stance: STANCE, auto_pick_outline: false }, judge: () => jevPick("A") });
  const quiet = context(sandbox(), off.fetchImpl, clock);
  const second = new Automation(quiet.ctx, automationClient(quiet.ctx), off.settings);
  second.refs = smallRefs;
  assert.match(await second.step(), /outline sent to \/admin\/videos for the owner \(頻道立場還是空白，或「由 Jev 挑大綱」關著/);
  assert.equal(off.calls.reviews[0].status, "pending");
  assert.equal("pick" in off.calls.reviews[0].payload, false);
});

/** A translator that fills every todo entry, so the captions pipeline runs end to end. */
function filledSheet(sheet) {
  const { locale } = sheet;
  return {
    ...sheet,
    title: { ...sheet.title, text: sheet.title.text || `${locale} title` },
    description: { ...sheet.description, text: sheet.description.text || `${locale} description` },
    tags: { ...sheet.tags, text: sheet.tags.text?.length ? sheet.tags.text : [`${locale} tag`] },
    chapters: sheet.chapters.map((chapter) => ({ ...chapter, text: chapter.text || `${locale} ${chapter.scene}` })),
    lines: sheet.lines.map((line) => ({ ...line, text: line.text || `${locale} ${line.id}` })),
  };
}

test("from the picked outline to YouTube without the owner: the final gate sends the quality check, the package check confirms the upload with every file attached, and the pasted id completes the video", async () => {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  const answers = {
    ...answersFor(slug, { applies: "1、2" }),
    translator: (body) => ({ worksheet: filledSheet(body.payload.worksheet) }),
    caption_reviewer: (body) => ({ worksheet: body.payload.worksheet, fixes: [] }),
  };
  const site = fakeSite({ answers, settings: { channel_stance: STANCE, caption_locales: ["en"] }, judge: () => jevPick("B") });
  const clock = { now: Date.parse("2026-09-27T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  // review-push encodes a preview with ffmpeg; here it writes a stand-in.
  ctx.encode = async (kind, source, target) => writeFileSync(target, Buffer.from(`${kind} of ${path.basename(source)}`));
  const workdir = path.join(box.work, slug);
  const docFile = path.join(box.root, "docs", "videos", slug, "video.json");
  const lexicon = () => readJson(path.join(box.root, "docs", "videos", "lexicon.json"));
  const runs = [];
  // The media stages, the narration check and the quality check play here without any vendor;
  // i18n-sheet, i18n-merge, captions, review-push (which asks this fake for qa), review-pull
  // and package are the real commands.
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    const [name] = command;
    const video = existsSync(docFile) ? readJson(docFile) : null;
    const write = (file, data) => atomicWrite(path.join(workdir, file), JSON.stringify(data));
    if (name === "tts") {
      mkdirSync(workdir, { recursive: true });
      writeSyntheticNarration(video, lexicon(), workdir);
      return { code: 0, out: "narration" };
    }
    if (name === "check-audio") {
      write("review/check.json", { lines: Object.fromEntries([...eachLine(video)].map(({ line }) => [line.id, { match: true, match_kind: "exact" }])) });
      return { code: 0, out: "every line passed" };
    }
    if (name === "render") {
      write("frames/manifest.json", { visual_hash: visualHash(video), theme_hash: "t", fps: 30, size: { width: 1920, height: 1080 }, scenes: [], thumbnail: "thumbnail.jpg" });
      writeFileSync(path.join(workdir, "thumbnail.jpg"), jpegBytes(1280, 720));
      return { code: 0, out: "rendered" };
    }
    if (name === "assemble") {
      writeFileSync(path.join(workdir, "final.mp4"), randomBytes(PART_BYTES + 10));
      write("checks.json", { ok: true, speech_hash: speechHash(video, lexicon()), visual_hash: visualHash(video), problems: [], metrics: { frames: 900, loudness: { integrated: -14 }, psnr: [] } });
      return { code: 0, out: "assembled" };
    }
    if (name === "qa") {
      write("review/qa.json", { ok: true, final_sha256: sha(path.join(workdir, "final.mp4")), items: ITEM_IDS.map((id) => ({ id, ok: true, detail: `${id} fine` })) });
      return { code: 0, out: "11 of 11 checks passed" };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  const state = () => automatedVideos(box.work)[0];
  const reviews = (gate) => site.reviewsOf(slug).filter((review) => review.gate === gate);

  assert.match(await automation.step(), /Jev picked outline B/);
  assert.match(await automation.step(), /Jev chose outline B/);
  assert.match(await automation.step(), /script drafted and passes lint/);
  assert.match(await automation.step(), /fact-check round 1/);
  assert.match(await automation.step(), /listener edit/);
  assert.match(await automation.step(), /narration synthesized/);
  assert.match(await automation.step(), /narration checked \(Jev passed every line\) and sent for review/);
  assert.equal(reviews("audio")[0].status, "approved", "Jev's line check stands for the owner");
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "audio"));
  assert.match(await automation.step(), /frames rendered/);
  assert.match(await automation.step(), /video assembled/);
  assert.match(await automation.step(), /en captions translated and reviewed/);
  assert.match(await automation.step(), /captions written/);

  // The final gate: review-push runs qa and sends its report; the site approves on arrival.
  assert.match(await automation.step(), /final sent to \/admin\/videos/);
  assert.ok(runs.includes(`qa --slug ${slug}`), "review-push --gate final ran the quality check first");
  const [final] = reviews("final");
  assert.equal(final.content_sha256, sha(path.join(workdir, "final.mp4")));
  assert.equal(final.payload.qa.final_sha256, final.content_sha256, "the report names the final.mp4 the gate hashes");
  assert.deepEqual(final.payload.qa.items.map((item) => item.id), ITEM_IDS);
  assert.match(final.summary, /自動品管 11 項全過/);
  assert.deepEqual([final.status, final.note], ["approved", "自動品管 11 項全過，依設定自動核准"]);
  assert.deepEqual(final.files.map((file) => file.role), ["preview", "thumbnail"]);
  assert.match(await automation.step(), /the final is approved \(自動品管 11 項全過，依設定自動核准\)/);
  assert.ok(readApprovals(workdir).approvals.some((entry) => entry.gate === "final"));

  // The package, checked as it is written; the disclosure answer is in metadata.json.
  assert.match(await automation.step(), /upload package written/);
  const metadata = readJson(path.join(workdir, "upload", "metadata.json"));
  assert.deepEqual([metadata.contains_synthetic_media, metadata.disclosure_reason], [false, "slides read by a stock TTS voice; YouTube's disclosure covers realistic synthetic people, events and places"]);
  assert.deepEqual(Object.keys(metadata).slice(-2), ["contains_synthetic_media", "disclosure_reason"], "the same two keys last, as qa writes them");
  assert.deepEqual(metadata.captions, ["captions/en.srt", "captions/zh-TW.srt"]);
  assert.deepEqual(Object.keys(metadata.skipped_caption_locales), ["ja", "ko", "zh-CN"], "every configured locale without a file says why");
  const uploadMd = readFileSync(path.join(workdir, "upload", "UPLOAD.md"), "utf8");
  assert.doesNotMatch(uploadMd, /- \[ \]/, "no self-check list: the automatic checks cover it");
  assert.match(uploadMd, /「變造或合成內容」：不用勾/);

  // The publish gate: every file of the package goes up, with the package check; the site approves on arrival.
  assert.match(await automation.step(), /publish confirmation sent to \/admin\/videos/);
  const [publish] = reviews("publish");
  assert.equal(publish.content_sha256, sha(path.join(workdir, "upload", "metadata.json")));
  assert.deepEqual(publish.payload.package.final_sha256, publish.content_sha256);
  assert.deepEqual(publish.payload.package.items.map((item) => [item.id, item.ok]), [["files", true], ["descriptions", true], ["captions", true], ["disclosure", true]]);
  assert.deepEqual(publish.files.map((file) => [file.role, file.content_type]), [
    ["captions_en", "text/plain"],
    ["captions_zh-TW", "text/plain"],
    ["description_en", "text/plain"],
    ["description_zh-TW", "text/plain"],
    ["final", "video/mp4"],
    ["metadata", "application/json"],
    ["thumbnail", "image/jpeg"],
  ]);
  const finalUpload = publish.files.find((file) => file.role === "final");
  assert.equal(finalUpload.sha256, sha(path.join(workdir, "final.mp4")), "the package's final.mp4 is the approved cut");
  assert.equal(site.files.get(finalUpload.sha256).length, 2, "over one part, so it went up in two");
  assert.equal(Buffer.concat(site.files.get(finalUpload.sha256)).equals(readFileSync(path.join(workdir, "final.mp4"))), true);
  assert.equal(publish.payload.chapters, 3);
  assert.equal(typeof publish.payload.minutes, "number");
  assert.deepEqual(publish.payload.locales, ["zh-TW", "en"]);
  assert.deepEqual(publish.payload.zh, { title: metadata.title, description: metadata.description, tags: metadata.tags });
  assert.deepEqual(publish.payload.disclosure, { synthetic: false, reason: metadata.disclosure_reason });
  assert.match(publish.summary, /上傳包 4 項齊全：請確認可以上架/);
  assert.deepEqual([publish.status, publish.note], ["approved", "上傳包 4 項齊全，依設定自動核准"]);
  assert.match(await automation.step(), /the upload is confirmed \(上傳包 4 項齊全，依設定自動核准\); the owner uploads it in YouTube Studio/);
  assert.equal(state().status, "done");
  assert.equal(await automation.step(), null, "nothing left but the owner's upload");

  // The owner uploaded it and pasted the address on /admin/videos: the id comes back into the script.
  site.listed.get(slug).youtube_video_id = "dQw4w9WgXcQ";
  assert.match(await automation.step(), /^chatgpt-ads-off: on YouTube as dQw4w9WgXcQ; video\.json records it and the video is complete$/);
  assert.equal(readJson(docFile).youtube.video_id, "dQw4w9WgXcQ");
  assert.equal(state().youtube_video_id, "dQw4w9WgXcQ");
  const last = site.calls.reports.at(-1);
  assert.deepEqual([last.stage, last.youtube_video_id], ["on YouTube", "dQw4w9WgXcQ"], "the report carries the id, so the site keeps it");
  assert.ok(last.checklist.every((item) => item.done), "every step reads as done");
  const status = await pipelineStatus({ slug, root: box.root, workdir });
  assert.equal(status.next, null);
  assert.equal(await automation.step(), null, "recorded once");
  assert.equal(site.listed.get(slug).youtube_video_id, "dQw4w9WgXcQ");
});

// The narration line Jev keeps hearing wrong (docs/videos/HANDS-OFF.md §旁白): the fixture's
// x9fe, 它 heard as 他, which the same-sound rule would pass in the real check but stands here for
// any line that is flagged after every retake.
const ORIGINAL = fixture().scenes[1].lines[0].text;
const HEARD_WRONG = "第一個問題是，你要他做什麼工作。";

/**
 * A tutorial taken to the narration gate with one retake allowed: the fake check-audio flags
 * x9fe while `stillFlagged(video)` says so, writing check.json and check-flags.json as the real
 * one does; the listener's rewrite pass answers `rewrite(body)`. tts writes a synthetic
 * narration for the script as it stands; review-push and review-pull are the real commands.
 */
async function narrationGate({ rewrite, stillFlagged }) {
  const box = sandbox();
  const slug = "chatgpt-ads-off";
  assert.equal(fixture().scenes[1].lines[0].id, "x9fe");
  const video = { ...fixture(), slug };
  const answers = { ...answersFor(slug, { applies: "1、2" }), listener: (body) => (body.variant === "rewrite" ? rewrite(body) : { video, edits: [] }) };
  const site = fakeSite({ answers, settings: { channel_stance: STANCE, max_retake_rounds: 1 }, judge: () => jevPick("B") });
  const clock = { now: Date.parse("2026-09-27T09:00:00Z") };
  const { ctx } = context(box, site.fetchImpl, clock);
  ctx.encode = async (kind, source, target) => writeFileSync(target, Buffer.from(`${kind} of ${path.basename(source)}`));
  const workdir = path.join(box.work, slug);
  const docFile = path.join(box.root, "docs", "videos", slug, "video.json");
  const lexicon = () => readJson(path.join(box.root, "docs", "videos", "lexicon.json"));
  const runs = [];
  const redos = [];
  ctx.runCommand = async (command, runCtx) => {
    runs.push(command.join(" "));
    const [name] = command;
    const current = existsSync(docFile) ? readJson(docFile) : null;
    const write = (file, data) => atomicWrite(path.join(workdir, file), JSON.stringify(data));
    if (name === "tts") {
      mkdirSync(workdir, { recursive: true });
      writeSyntheticNarration(current, lexicon(), workdir);
      const redo = command.indexOf("--redo");
      if (redo >= 0) redos.push([path.basename(command[redo + 1]), readJson(command[redo + 1]).flags]);
      return { code: 0, out: "narration" };
    }
    if (name === "check-audio") {
      const lines = Object.fromEntries([...eachLine(current)].map(({ line }) => [line.id, { match: true, match_kind: "exact", intended: line.text, heard: line.text, noul: null }]));
      const flagged = stillFlagged(current);
      if (flagged) Object.assign(lines.x9fe, { match: false, match_kind: null, heard: HEARD_WRONG, noul: 0.2 });
      write("review/check.json", { lines });
      write("review/check-flags.json", { slug, speech_hash: "s", flags: flagged ? ["x9fe"] : [], notes: flagged ? { x9fe: `Jev 0.20: heard 「${HEARD_WRONG}」` } : {} });
      return { code: flagged ? 1 : 0, out: flagged ? "1 flagged" : "every line passed" };
    }
    const { main: cli } = await import("../cli.mjs");
    let out = "";
    const sink = { write: (text) => (out += text) };
    const code = await cli(command, { ...runCtx, stdout: sink, stderr: sink });
    return { code, out };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  for (const expected of [/Jev picked outline B/, /Jev chose outline B/, /script drafted/, /fact-check round 1/, /listener edit/, /narration synthesized/]) assert.match(await automation.step(), expected);
  return {
    site,
    automation,
    workdir,
    runs,
    redos,
    state: () => automatedVideos(box.work)[0],
    reviews: (gate) => site.reviewsOf(slug).filter((review) => review.gate === gate),
    lineText: () => readJson(docFile).scenes[1].lines[0].text,
    rewriteCalls: () => site.calls.run.filter((call) => call.stage === "listener" && call.variant === "rewrite"),
  };
}

test("with the retakes spent, the listener rewords the line Jev keeps hearing wrong, only that line is retaken, and the re-check lets the site approve the narration", async () => {
  const REWRITE = "第一個問題是，你要它做哪一種工作。";
  const gate = await narrationGate({ rewrite: () => ({ lines: [{ id: "x9fe", text: REWRITE }] }), stillFlagged: (video) => video.scenes[1].lines[0].text === ORIGINAL });
  assert.match(await gate.automation.step(), /narration checked \(Jev passed every line; 1 lines rewritten in 1 rewrite round\) and sent for review$/);
  const [asked] = gate.rewriteCalls();
  assert.equal(gate.rewriteCalls().length, 1);
  assert.deepEqual(asked.payload.lines, [{ id: "x9fe", text: ORIGINAL, heard: HEARD_WRONG, jev: 0.2 }], "only the flagged line, with what was heard");
  assert.ok(asked.payload.lexicon.includes("Sulafat"), "the dictionary's terms, the writer's additions included");
  assert.equal(asked.payload.round, 1);
  assert.equal("previous_problems" in asked.payload, false);
  assert.deepEqual([asked.format, asked.variant], ["slides", "rewrite"]);
  assert.ok(asked.instructions.startsWith(LISTENER_REWRITE));
  assert.match(LISTENER_REWRITE, /Rewrite ONLY these sentences' wording[\s\S]*「和」→「跟」[\s\S]*「答」→「回答」[\s\S]*「旗艦」→「旗艦模型」[\s\S]*\{"lines": \[\{"id"/);
  assert.equal(instructionsFor("listener", "drama", "", "rewrite"), LISTENER_REWRITE, "the same text for a drama");
  assert.equal(gate.lineText(), REWRITE, "the script line is the rewrite");
  assert.deepEqual(gate.redos, [["check-flags.json", ["x9fe"]], ["rewrite-flags.json", ["x9fe"]]], "one retake from the check's flags, then exactly the rewritten line");
  assert.equal(gate.runs.filter((run) => run.startsWith("check-audio")).length, 3, "the first check, the one after the retake, the one after the rewrite");
  const rewrites = readJson(path.join(gate.workdir, "review", "rewrites.json"));
  assert.deepEqual(rewrites, [{ id: "x9fe", before: ORIGINAL, after: REWRITE, heard: HEARD_WRONG }]);
  const [audio] = gate.reviews("audio");
  assert.deepEqual(audio.payload.rewrites, rewrites, "the review card gets the list");
  assert.equal(audio.payload.check.flagged, 0);
  assert.match(audio.summary, /Jev 標記 0 句；改寫 1 句$/);
  assert.deepEqual([audio.status, audio.note], ["approved", "Jev 判斷每一句都唸對了，依設定自動核准"], "the re-check passed every line and the owner's switch is on");
  assert.ok(readApprovals(gate.workdir).approvals.some((entry) => entry.gate === "audio"));
  const state = gate.state();
  assert.deepEqual([state.retakes, state.rewrites], [1, 1]);
  assert.ok(state.notes.includes(`narration rewritten: x9fe 「${ORIGINAL}」 → 「${REWRITE}」`));
  assert.equal(MAX_REWRITE_ROUNDS, 2);
});

test("a rewrite that changes a number is dropped, the line keeps its text, and after the rounds the narration waits for the owner with the reasons in the notes", async () => {
  const gate = await narrationGate({ rewrite: () => ({ lines: [{ id: "x9fe", text: "第 1 個問題是，你要它做什麼工作。" }] }), stillFlagged: (video) => video.scenes[1].lines[0].text === ORIGINAL });
  assert.match(await gate.automation.step(), /narration checked \(some lines flagged; 0 lines rewritten in 2 rewrite rounds\) and sent for review$/);
  const asked = gate.rewriteCalls();
  assert.equal(asked.length, MAX_REWRITE_ROUNDS);
  assert.equal("previous_problems" in asked[0].payload, false);
  assert.deepEqual(asked[1].payload.previous_problems, ["x9fe: number 1 was added"], "the second round is told why the first was refused");
  assert.equal(gate.lineText(), ORIGINAL, "the line keeps its text");
  assert.deepEqual(gate.redos, [["check-flags.json", ["x9fe"]]], "nothing was retaken for a dropped rewrite");
  assert.equal(gate.runs.filter((run) => run.startsWith("check-audio")).length, 2, "the same clips are not checked again");
  assert.deepEqual(readJson(path.join(gate.workdir, "review", "rewrites.json")), []);
  const [audio] = gate.reviews("audio");
  assert.equal(audio.status, "pending", "the owner decides");
  assert.deepEqual(audio.payload.rewrites, []);
  assert.equal(audio.payload.flagged_lines.length, 1);
  assert.match(audio.summary, /Jev 標記 1 句$/);
  assert.equal(gate.state().rewrites, MAX_REWRITE_ROUNDS);
  assert.deepEqual(gate.state().notes.filter((note) => note.startsWith("narration rewrite")), ["narration rewrite dropped: x9fe: number 1 was added", "narration rewrite dropped: x9fe: number 1 was added"]);
  assert.equal(await gate.automation.step(), null, "the narration waits for the owner");
});

test("two rewrite rounds that Jev still flags send the narration to the owner with both rewrites listed", async () => {
  const texts = { 1: "第一個問題是，你要它做哪一種工作。", 2: "第一個問題是，你要它處理哪一種工作。" };
  const gate = await narrationGate({ rewrite: (body) => ({ lines: [{ id: "x9fe", text: texts[body.payload.round] }] }), stillFlagged: () => true });
  assert.match(await gate.automation.step(), /narration checked \(some lines flagged; 2 lines rewritten in 2 rewrite rounds\) and sent for review$/);
  const asked = gate.rewriteCalls();
  assert.deepEqual(asked.map((call) => call.payload.lines[0].text), [ORIGINAL, texts[1]], "the second round rewrites the line as the first round left it");
  assert.deepEqual(asked.map((call) => call.payload.round), [1, 2]);
  assert.equal(gate.lineText(), texts[2]);
  assert.deepEqual(gate.redos, [["check-flags.json", ["x9fe"]], ["rewrite-flags.json", ["x9fe"]], ["rewrite-flags.json", ["x9fe"]]]);
  assert.equal(gate.runs.filter((run) => run.startsWith("check-audio")).length, 4);
  const [audio] = gate.reviews("audio");
  assert.equal(audio.status, "pending");
  assert.deepEqual(audio.payload.rewrites, [
    { id: "x9fe", before: ORIGINAL, after: texts[1], heard: HEARD_WRONG },
    { id: "x9fe", before: texts[1], after: texts[2], heard: HEARD_WRONG },
  ]);
  assert.match(audio.summary, /Jev 標記 1 句；改寫 2 句$/);
  assert.equal(gate.state().rewrites, MAX_REWRITE_ROUNDS);
  assert.equal(gate.state().notes.filter((note) => note.startsWith("narration rewritten: ")).length, 2);
  assert.equal(await gate.automation.step(), null, "the owner decides");
});
