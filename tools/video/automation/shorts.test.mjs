// The worker's Shorts round (shorts.mjs): where it goes in `auto`, and the weekly plan, the new
// topics and the weekly report it writes back. The site and the models are a fake fetch.
import assert from "node:assert/strict";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { automationClient } from "./client.mjs";
import { briefTopics, localDay, planItems, rawTable, reportProblems, SHORTS_DIR, SHORTS_STATE, ShortsWorker, slotsAhead } from "./shorts.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const SITE = "https://site.test";
const NOW = new Date("2026-10-05T01:00:00Z"); // a Monday morning in Taipei
const PATTERN = [{ days: 30, counts: [1] }, { days: 60, counts: [2, 1] }];
const SHORTS_SETTINGS = { enabled: true, lines: ["lab", "cut"], weekly_quota: { lab: 5, cut: 2 }, daily_pattern: PATTERN, slot_times: ["12:30", "19:30"], timezone: "Asia/Taipei", stock_days: 5, max_per_day: 2, seconds_min: 25, seconds_max: 55, voice: { provider: "gemini", name: "Sulafat" }, locales: [], campaign_start: "2026-10-01", paused: false };
const slot = (id, date, time = "19:30", extra = {}) => ({ id, starts_at: `${date}T${time === "19:30" ? "11:30" : "04:30"}:00Z`, local_date: date, local_time: time, status: "open", line: null, series: null, topic_slug: null, project_slug: null, ...extra });
const summary = (slug, line = "lab", extra = {}) => ({ slug, line, series: line === "lab" ? "daily" : "ai-model-choice", title: slug, hook: null, status: "ready", origin: "campaign", release_order: null, paid: false, ...extra });
const BUDGET = { period_start: "2026-10-01T00:00:00Z", period_end: "2026-10-31T00:00:00Z", spent_ntd: 0.29, reserved_ntd: 0, unknown: 0, limit_ntd: 3000, soft_ntd: 2400, total_start: "2026-10-01T00:00:00Z", total_spent_ntd: 0.29, total_limit_ntd: 9000, paid_work_allowed: true, reason: null };
const PLAN_JOB = {
  window_start: NOW.toISOString(), window_end: "2026-10-18T16:00:00Z", timezone: "Asia/Taipei", lines: ["lab", "cut"], weekly_quota: { lab: 5, cut: 2 },
  open_slots: [slot("11111111-1111-4111-8111-111111111111", "2026-10-06"), slot("22222222-2222-4222-8222-222222222222", "2026-10-07"), slot("33333333-3333-4333-8333-333333333333", "2026-10-08")],
  planned: [], topics: [summary("shorts-self-check"), summary("shorts-cut-model-choice-1", "cut"), summary("shorts-image-specificity", "lab", { paid: true }), summary("shorts-taiwan-phrases"), summary("drama-episode-1-vertical", "drama")],
  last_week: [], budget: BUDGET,
};
const REPORT_JOB = {
  week_start: "2026-09-28", week_end: "2026-10-04", timezone: "Asia/Taipei",
  published: [
    { slug: "shorts-receipt-total", title: "AI 算得出這張收據嗎？", line: "lab", series: "daily", youtube_video_id: "dQw4w9WgXcQ", published_at: "2026-10-01T11:30:00Z", snapshots: [{ period: "d1", source: "data_api", captured_at: "2026-10-02T12:05:00Z", views: 1843, likes: 57, comments: 6 }, { period: "d3", source: "data_api", captured_at: "2026-10-04T12:10:00Z", views: 4210, likes: 102, comments: 11 }] },
    { slug: "shorts-prompt-check", title: "多一句驗算有用嗎？", line: "lab", series: "prompts", youtube_video_id: "aBcDeFgHiJk", published_at: "2026-10-03T11:30:00Z", snapshots: [] },
  ],
  missed: [slot("44444444-4444-4444-8444-444444444444", "2026-10-02", "19:30", { status: "missed", topic_slug: "shorts-poster-blind", line: "lab" })],
  costs: [{ id: "c1", occurred_at: "2026-10-01T10:00:00Z", project_slug: "shorts-receipt-total", category: "narration", amount: 0.009, currency: "USD", fx_rate: 32, amount_ntd: 0.29, status: "confirmed", source: "auto", note: null, created_at: "2026-10-01T10:00:00Z" }],
  budget: BUDGET,
  next_week: [slot("11111111-1111-4111-8111-111111111111", "2026-10-06", "19:30", { status: "planned", topic_slug: "shorts-self-check", line: "lab" })],
};

/** The site `auto` reads: the tutorials' settings, the Shorts' settings and jobs, the models. */
function fakeSite({ settings = {}, shorts = SHORTS_SETTINGS, jobs = [], answers = {}, library = [], refusePlan = null } = {}) {
  const calls = { all: [], run: [], plan: [], topics: [], report: [], start: [], videos: [] };
  const queue = [...jobs];
  const fetchImpl = async (url, init = {}) => {
    const { pathname, search } = new URL(url);
    calls.all.push(`${init.method ?? "GET"} ${pathname}${search}`);
    const body = typeof init.body === "string" ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return Response.json({ enabled: true, max_waiting_drafts: 0, draft_interval_hours: 72, max_verify_rounds: 3, channel_stance: "", ...settings });
    if (pathname === "/api/video/automation/videos") {
      calls.videos.push(search);
      return Response.json(search.includes("state=library") ? library : []);
    }
    if (!shorts && pathname.startsWith("/api/video/automation/shorts/")) return Response.json({ code: "not_found", detail: pathname }, { status: 404 });
    if (pathname === "/api/video/automation/shorts/settings") return Response.json(shorts);
    if (pathname === "/api/video/automation/shorts/next") return Response.json(queue.shift() ?? { kind: null, holds: ["沒有事"] });
    if (pathname === "/api/video/automation/run") {
      calls.run.push(body);
      const reply = answers[`${body.stage}:${body.variant}`];
      const value = typeof reply === "function" ? reply(body, calls) : reply;
      return Response.json({ text: typeof value === "string" ? value : JSON.stringify(value ?? {}), provider: "claude_code", model: "claude-planner", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 20_000_000 } });
    }
    if (pathname === "/api/video/automation/shorts/plan") {
      calls.plan.push(body);
      if (refusePlan && body.items.length) return Response.json({ code: "video_shorts_plan_invalid", detail: refusePlan }, { status: 422 });
      return Response.json({ planned: body.items.map((item) => ({ id: item.slot_id })) });
    }
    if (pathname === "/api/video/automation/shorts/topics") {
      calls.topics.push(body);
      return Response.json({ created: body.topics.length, updated: 0, skipped: 0, items: [] });
    }
    if (pathname === "/api/video/automation/shorts/report") {
      calls.report.push(body);
      return Response.json({ id: "r1", week_start: body.week_start, body_md: body.body_md, rows: [], plan: [], generated_at: NOW.toISOString(), updated_at: NOW.toISOString() });
    }
    const start = /^\/api\/video\/automation\/shorts\/([a-z0-9-]+)\/start$/.exec(pathname);
    if (start) {
      calls.start.push(start[1]);
      return Response.json({ topic: {}, project_slug: `${start[1]}-2`, created: true });
    }
    if (/^\/api\/video\/reviews\/[a-z0-9-]+$/.test(pathname) && init.method === "PUT") return Response.json({ reviews: [] });
    return Response.json({ code: "not_found", detail: pathname }, { status: 404 });
  };
  return { calls, fetchImpl };
}

function context(box, site, extra = {}) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
    home: box.base,
    fetch: site.fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => NOW,
    sleep: async () => {},
    runCommand: async () => assert.fail("no media stage runs in these tests"),
    ...extra,
  };
  return { ctx, out };
}

// --- the pieces ------------------------------------------------------------------------------------

test("the run's pattern says how many Shorts the coming days need", () => {
  const settings = { campaign_start: "2026-10-01", daily_pattern: PATTERN, slot_times: ["12:30", "19:30"] };
  assert.equal(slotsAhead(settings, "2026-10-05", 5), 5, "one a day in the first thirty days");
  assert.equal(slotsAhead(settings, "2026-10-30", 4), 1 + 2 + 1 + 2, "then two and one in turn");
  assert.equal(slotsAhead(settings, "2026-09-28", 5), 2, "nothing before the first day");
  assert.equal(slotsAhead(settings, "2027-01-05", 5), 0, "nothing after the last");
  assert.equal(slotsAhead({ ...settings, campaign_start: null }, "2026-10-05", 5), 0);
  assert.equal(slotsAhead({ ...settings, slot_times: ["19:30"] }, "2026-10-31", 2), 2, "never more a day than there are slot times");
  assert.equal(localDay(NOW, "Asia/Taipei"), "2026-10-05");
  assert.equal(localDay(new Date("2026-10-04T17:00:00Z"), "Asia/Taipei"), "2026-10-05");
});

test("the plan keeps only what the server can take and this worker can make", () => {
  const [first, second, third] = PLAN_JOB.open_slots.map((each) => each.id);
  const { items, dropped, problem } = planItems({ items: [
    { slot_id: first, topic_slug: "shorts-self-check", reason: "已驗證的題型" },
    { slot_id: second, topic_slug: "shorts-cut-model-choice-1" },
    { slot_id: third, topic_slug: "shorts-image-specificity" },
    { slot_id: third, topic_slug: "shorts-self-check" },
    { slot_id: "99999999-9999-4999-8999-999999999999", topic_slug: "shorts-taiwan-phrases" },
    { slot_id: third, topic_slug: "shorts-invented" },
    { slot_id: third, topic_slug: "drama-episode-1-vertical" },
  ] }, PLAN_JOB);
  assert.equal(problem, null);
  assert.deepEqual(items, [{ slot_id: first, topic_slug: "shorts-self-check" }, { slot_id: second, topic_slug: "shorts-cut-model-choice-1" }], "the reason stays with the worker: the server takes slot and slug only; a highlight is made too");
  assert.deepEqual(dropped.map((line) => line.split(":")[1].trim()), ["needs a generated picture", "twice in the plan", "not an open slot", "not a topic of the pool", "the worker does not make drama yet"]);
  assert.equal(planItems({ note: "nothing" }, PLAN_JOB).problem, "the answer has no items list");
});

test("new topics go up in the server's shape: experiments only, with every field it takes and nothing else", () => {
  const job = { ideas: [{ slug: "shorts-owner-idea", line: "lab", series: "prompts", status: "idea" }], existing: [summary("shorts-receipt-total"), summary("shorts-owner-idea", "lab", { status: "idea" })] };
  const protocol = { setup: "s", input: "17×24 等於多少？", condition_a: "直接回答。", condition_b: "先驗算再回答。", runs: "各一次", scoring: "比對 408", failure_path: "照實說", extra: "dropped" };
  const { topics, dropped } = briefTopics({ topics: [
    { slug: "shorts-multiply-check", line: "lab", series: "prompts", title: "乘法驗算", hook: "AI 會算錯乘法嗎？", brief: { test_protocol: protocol, truth_check: ["17 × 24 = 408"], acceptance: ["兩組都展示"], requires: ["sandbox"], estimated_seconds: 40, invented: true }, assets_needed: [{ key: "x", label: "y" }], release_order: 3 },
    { slug: "shorts-owner-idea", line: "cut", series: "blind", title: "站主的想法", brief: { test_protocol: protocol, truth_check: ["t"], acceptance: ["a"] } },
    { slug: "shorts-receipt-total", line: "lab", series: "daily", title: "重複", brief: {} },
    { slug: "Bad Slug", line: "lab", series: "daily", title: "x" },
    { slug: "shorts-highlight", line: "cut", series: "ai-model-choice", title: "精華" },
    { slug: "shorts-weekly", line: "lab", series: "weekly", title: "週" },
  ] }, job);
  assert.deepEqual(topics.map((topic) => topic.slug), ["shorts-multiply-check", "shorts-owner-idea"]);
  const [made, completed] = topics;
  assert.deepEqual(Object.keys(made).sort(), ["brief", "hook", "line", "series", "slug", "title"]);
  assert.deepEqual(Object.keys(made.brief.test_protocol).sort(), ["condition_a", "condition_b", "failure_path", "input", "runs", "scoring", "setup"]);
  assert.equal("requires" in made.brief, false, "the worker never asks for a tool it lacks");
  assert.equal(made.brief.estimated_seconds, 40);
  assert.deepEqual([completed.line, completed.series], ["lab", "prompts"], "an idea keeps its line and series");
  assert.equal(dropped.length, 4);
});

test("the report's table is printed by the program, and the report may cite no number it does not have", () => {
  const table = rawTable(REPORT_JOB);
  assert.match(table, /\| AI 算得出這張收據嗎？（shorts-receipt-total，dQw4w9WgXcQ） \| 實測 \| daily \| 2026-10-01 19:30 \| 第 1 天 \| YouTube Data API \| 2026-10-02 20:05 \| 1843 \| 57 \| 6 \|/);
  assert.match(table, /\| 第 3 天 \| YouTube Data API \| 2026-10-04 20:10 \| 4210 \| 102 \| 11 \|/);
  assert.match(table, /多一句驗算有用嗎？.*\| 還沒有讀到 \|/);
  assert.match(table, /2026-10-02 19:30：shorts-poster-blind（實測）/);
  assert.match(table, /\| narration \| shorts-receipt-total \| 0\.009 \| USD \| 0\.29 \| confirmed \|/);
  assert.match(table, /2026-10-06 19:30：shorts-self-check（實測，planned）/);
  assert.doesNotMatch(table, /engaged|平均/, "only the columns YouTube filled");
  const fine = "## 上週發了什麼\n收據那支第 3 天讀到 4210 次觀看、102 個喜歡（YouTube Data API，2026-10-04 20:10）。驗算那支還沒有數字。";
  assert.deepEqual(reportProblems(fine, table), []);
  assert.match(reportProblems("兩支平均 3027 次觀看", table)[0], /these numbers are not in raw_values: 3027/);
  assert.match(reportProblems("收據那支的觀看是驗算那支的 2.3 倍", table)[0], /2\.3/);
  assert.match(reportProblems("收據那支排名第一", table)[0], /排名/);
  assert.deepEqual(reportProblems("", table), ["body_md is empty"]);
});

// --- the round in `auto` -------------------------------------------------------------------------

test("auto writes the week's report through the planner, and refuses a report that computes", async () => {
  const box = sandbox();
  let tries = 0;
  const answers = {
    "planner:shorts-report": () => (++tries === 1
      ? { body_md: "## 數字怎麼看\n兩支平均 3027 次觀看，收據那支表現最好。", notes: {} }
      : { body_md: "## 上週發了什麼\n收據那支第 3 天讀到 4210 次觀看（YouTube Data API）。驗算那支還沒有讀到數字。", notes: { "shorts-self-check": "自我檢查是新角度，排在週二。" } }),
  };
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "report", holds: [], report: REPORT_JOB }], answers });
  const { ctx, out } = context(box, site);
  assert.equal(await main(["auto"], ctx), EXIT.ok);
  assert.equal(out.stdout, "shorts: the report on the week of 2026-09-28 is on the site (2 snapshots cited)\nautomatic drafts are off in the settings on /admin/videos; nothing to do\n", "the Shorts go by their own settings, whatever the tutorials' switch says");
  assert.equal(site.calls.run.length, 2);
  const [first, second] = site.calls.run;
  assert.deepEqual([first.stage, first.variant, first.format, first.slug], ["planner", "shorts-report", "shorts", "shorts-report-2026-09-28"]);
  assert.match(first.instructions, /Do not output any score, rank, ranking, average, median/);
  assert.equal(first.payload.raw_values, rawTable(REPORT_JOB));
  assert.match(second.payload.previous_problem, /these numbers are not in raw_values: 3027/);
  const [report] = site.calls.report;
  assert.equal(report.week_start, "2026-09-28");
  assert.ok(report.body_md.endsWith(rawTable(REPORT_JOB)), "the raw values close the report, copied by the program");
  assert.deepEqual(report.rows, [{ youtube_video_id: "dQw4w9WgXcQ", period: "d1", source: "data_api" }, { youtube_video_id: "dQw4w9WgXcQ", period: "d3", source: "data_api" }]);
  assert.deepEqual(report.plan, [{ starts_at: "2026-10-06T11:30:00Z", topic_slug: "shorts-self-check", line: "lab", note: "自我檢查是新角度，排在週二。" }]);
  assert.deepEqual([report.provider, report.model], ["claude_code", "claude-planner"]);
});

test("a report that cannot be written twice in a row is saved saying so, with the raw values", async () => {
  const box = sandbox();
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "report", holds: [], report: REPORT_JOB }, { kind: "report", holds: [], report: REPORT_JOB }], answers: { "planner:shorts-report": "not JSON at all" } });
  const first = context(box, site);
  await main(["auto"], first.ctx);
  assert.match(first.out.stdout, /^shorts: the report gave nothing usable \(planner \(shorts-report\) answered something that is not JSON.*; the next round tries once more/);
  assert.equal(site.calls.report.length, 0);
  assert.equal(readdirSync(path.join(box.work, SHORTS_DIR, "answers")).length, 1);
  const second = context(box, site);
  await main(["auto"], second.ctx);
  assert.match(second.out.stdout, /shorts: the report failed 2 times in a row .*a report saying so, with the raw values, is on the site instead/);
  const [saved] = site.calls.report;
  assert.match(saved.body_md, /^## 這一週的報告沒有寫成\n\n企劃模型連續兩次交不出能用的報告/);
  assert.ok(saved.body_md.endsWith(rawTable(REPORT_JOB)));
  assert.equal("model" in saved, false, "no model wrote it");
  assert.deepEqual(JSON.parse(readFileSync(path.join(box.work, SHORTS_DIR, SHORTS_STATE), "utf8")).failures, {});
});

test("the plan goes to the server as slots and slugs; refused twice, an empty plan is recorded", async () => {
  const box = sandbox();
  const [first] = PLAN_JOB.open_slots.map((each) => each.id);
  const answers = { "planner:shorts-plan": { items: [{ slot_id: first, topic_slug: "shorts-self-check", reason: "已驗證" }, { slot_id: PLAN_JOB.open_slots[1].id, topic_slug: "drama-episode-1-vertical" }], note: "其餘留空" } };
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "plan", holds: [], plan: PLAN_JOB }], answers });
  const { ctx, out } = context(box, site);
  await main(["auto"], ctx);
  assert.match(out.stdout, /^shorts: planned 1 of 3 open slots until 2026-10-19 00:00 \(left out: drama-episode-1-vertical: the worker does not make drama yet\)\n/);
  assert.deepEqual(site.calls.plan, [{ items: [{ slot_id: first, topic_slug: "shorts-self-check" }] }]);
  assert.equal(site.calls.run[0].payload.today, "2026-10-05");
  assert.deepEqual(site.calls.run[0].payload.topics, PLAN_JOB.topics);
  assert.ok(existsSync(path.join(box.work, SHORTS_DIR, "plans", "2026-10-05.json")), "the planner's reasons stay beside the calendar");

  const refused = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "plan", holds: [], plan: PLAN_JOB }, { kind: "plan", holds: [], plan: PLAN_JOB }], answers, refusePlan: "2026-10-05 那一週排了 8 支，超過各內容線配額合計 7 支" });
  const other = sandbox();
  const one = context(other, refused);
  await main(["auto"], one.ctx);
  assert.match(one.out.stdout, /the plan gave nothing usable \(the site refused it: 2026-10-05 那一週排了 8 支/);
  assert.match(refused.calls.run[1].payload.previous_problem, /超過各內容線配額合計/, "the second try is told why");
  const two = context(other, refused);
  await main(["auto"], two.ctx);
  assert.match(two.out.stdout, /the plan failed 2 times in a row .*an empty plan was recorded/);
  assert.deepEqual(refused.calls.plan.at(-1), { items: [] });
});

test("new topics are written back, and a brief that fails twice waits half a day", async () => {
  const box = sandbox();
  const job = { lines: ["lab"], weekly_quota: { lab: 5 }, have: 3, want: 10, by_line: { lab: 3 }, ideas: [], existing: [summary("shorts-receipt-total")] };
  const good = { topics: [{ slug: "shorts-multiply-check", line: "lab", series: "prompts", title: "乘法驗算", brief: { test_protocol: { input: "17×24？" }, truth_check: ["17 × 24 = 408"], acceptance: ["展示兩組"] } }] };
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "brief", holds: [], brief: job }], answers: { "planner:shorts-brief": good } });
  const { ctx, out } = context(box, site);
  await main(["auto"], ctx);
  assert.match(out.stdout, /^shorts: 1 new topics, 0 ideas completed\n/);
  assert.equal(site.calls.topics[0].topics[0].slug, "shorts-multiply-check");

  const empty = fakeSite({ settings: { enabled: false }, jobs: Array(3).fill({ kind: "brief", holds: [], brief: job }), answers: { "planner:shorts-brief": { topics: [] } } });
  const other = sandbox();
  await main(["auto"], context(other, empty).ctx);
  const second = context(other, empty);
  await main(["auto"], second.ctx);
  assert.match(second.out.stdout, /the brief failed 2 times in a row .*new topics wait half a day/);
  const asked = empty.calls.run.length;
  const third = context(other, empty);
  await main(["auto"], third.ctx);
  assert.equal(empty.calls.run.length, asked, "no model is asked while the brief waits");
  assert.equal(third.out.stdout, "automatic drafts are off in the settings on /admin/videos; nothing to do\n");
});

test("while the library runs low the Shorts go before the tutorials, otherwise after them", async () => {
  const order = (site) => site.calls.all.filter((call) => call.includes("/shorts/next") || call.includes("videos?shorts=exclude")).map((call) => (call.includes("next") ? "shorts" : "tutorials"));
  // Five days ahead hold five slots; the library has two Shorts.
  const low = fakeSite({ library: [{ slug: "a" }, { slug: "b" }] });
  await main(["auto"], context(sandbox(), low).ctx);
  assert.deepEqual(order(low), ["shorts", "tutorials"]);
  assert.ok(low.calls.videos.includes("?shorts=only&state=library&limit=200"));
  const full = fakeSite({ library: Array.from({ length: 5 }, (_, index) => ({ slug: `s${index}` })) });
  await main(["auto"], context(sandbox(), full).ctx);
  assert.deepEqual(order(full), ["tutorials", "shorts"]);
  // Before the run has a first day there is no stock to keep: after the tutorials.
  const before = fakeSite({ shorts: { ...SHORTS_SETTINGS, campaign_start: null } });
  await main(["auto"], context(sandbox(), before).ctx);
  assert.deepEqual(order(before), ["tutorials", "shorts"]);
  assert.ok(!before.calls.videos.some((query) => query.includes("state=library")), "no stock to read before the run");
});

test("the tutorial and drama rounds ask the video list without the Shorts", async () => {
  const site = fakeSite();
  const box = sandbox();
  await main(["auto"], context(box, site).ctx);
  assert.ok(site.calls.videos.includes("?shorts=exclude"));
  assert.ok(site.calls.videos.every((query) => query.startsWith("?shorts=")), "every list is filtered");
  const { ctx } = context(box, site);
  await automationClient(ctx).videos();
  assert.equal(site.calls.videos.at(-1), "?shorts=exclude", "the client's default is the tutorials' list");
});

test("Shorts off, a STOP file or a site without Shorts: the round asks no Shorts job", async () => {
  const off = fakeSite({ shorts: { ...SHORTS_SETTINGS, enabled: false } });
  await main(["auto"], context(sandbox(), off).ctx);
  assert.ok(!off.calls.all.some((call) => call.includes("/shorts/next")));
  const none = fakeSite({ shorts: null });
  const quiet = context(sandbox(), none);
  await main(["auto"], quiet.ctx);
  assert.equal(quiet.out.stdout, "nothing to do now: every video waits on the owner, or the next draft is not due\n", "a site from before Shorts gets not a word about them");
  const box = sandbox();
  writeFileSync(path.join(box.work, "STOP"), "");
  const stopped = fakeSite();
  await main(["auto"], context(box, stopped).ctx);
  assert.ok(!stopped.calls.all.some((call) => call.includes("/shorts/next")));
});

test("a Short to make starts its topic and goes to the lab; one that needs a sandbox is not started", async () => {
  const topic = { slug: "shorts-self-check", line: "lab", series: "prompts", title: "回答後自我檢查", status: "ready", brief: { test_protocol: { input: "17×24", condition_a: "只列答案。", condition_b: "請驗算。", scoring: "答案 408" }, truth_check: ["17×24=408"], acceptance: ["a"], requires: [] } };
  const make = { slot: PLAN_JOB.open_slots[0], topic, line: "lab", project_slug: null, resume: false, channel_stance: "", seconds_min: 25, seconds_max: 55 };
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "make", holds: [], make }], answers: { "verifier:shorts-lab-key": { items: [] } } });
  const box = sandbox();
  const { ctx, out } = context(box, site, { shortsTools: {} });
  await main(["auto"], ctx);
  assert.deepEqual(site.calls.start, ["shorts-self-check"]);
  assert.deepEqual(site.calls.run.map((call) => [call.stage, call.variant, call.slug]), [["verifier", "shorts-lab-key", "shorts-self-check-2"]], "made under the video the server named");
  assert.match(out.stdout, /^shorts-self-check-2: freeze gave nothing usable \(the answer key does not come from the spec/);
  assert.ok(existsSync(path.join(box.work, SHORTS_DIR, "shorts-self-check-2", "lab.json")), "the Short's files stay under _shorts, away from the tidy");

  const sandboxed = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "make", holds: [], make: { ...make, topic: { ...topic, slug: "shorts-boba-game", brief: { ...topic.brief, requires: ["sandbox"] } } } }] });
  const refused = context(sandbox(), sandboxed);
  await main(["auto"], refused.ctx);
  assert.match(refused.out.stdout, /^shorts: cannot make shorts-boba-game: 「shorts-boba-game」要真的執行模型寫的程式/);
  assert.deepEqual(sandboxed.calls.start, []);
  assert.equal(sandboxed.calls.run.length, 0);
});

test("a highlight to make starts its topic and goes to cut.mjs; one from a source not public yet is blocked, not asked every round", async () => {
  const source = { slug: "ai-model-choice", title: "怎麼選模型", format: "slides", youtube_video_id: "dQw4w9WgXcQ", youtube_publish_at: "2026-10-01T11:30:00Z", source_guide: null, category: null, series_slug: null, episode_number: null };
  const topic = { slug: "ai-model-choice-cut-1", line: "cut", series: "ai-model-choice", title: "怎麼選模型（精華 1）", status: "ready", brief: { notes: "挑一段" }, source_slug: "ai-model-choice" };
  const make = { slot: PLAN_JOB.open_slots[0], topic, line: "cut", project_slug: null, resume: false, source, channel_stance: "", seconds_min: 25, seconds_max: 55 };
  const box = sandbox();
  const tutorial = path.join(box.root, "docs", "videos", "ai-model-choice");
  mkdirSync(tutorial, { recursive: true });
  writeFileSync(path.join(tutorial, "video.json"), JSON.stringify({ slug: "ai-model-choice", scenes: [{ id: "a", chapter: "開場", lines: [{ id: "m1", text: "第一句。" }, { id: "m2", text: "第二句。" }] }] }));
  writeFileSync(path.join(tutorial, "verify-1.md"), "全部對得上。\n");
  const site = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "make", holds: [], make }], answers: { "planner:shorts-cut": { segments: "none" } } });
  const { ctx, out } = context(box, site, { shortsTools: {} });
  await main(["auto"], ctx);
  assert.deepEqual(site.calls.start, ["ai-model-choice-cut-1"]);
  assert.deepEqual(site.calls.run.map((call) => [call.stage, call.variant, call.slug]), [["planner", "shorts-cut", "ai-model-choice-cut-1-2"], ["planner", "shorts-cut", "ai-model-choice-cut-1-2"]], "made under the video the server named, asked again at once with the problems");
  assert.match(out.stdout, /^ai-model-choice-cut-1-2: source frozen: ai-model-choice \(2 lines, verify-1\.md; no article to link\)\nai-model-choice-cut-1-2: pick gave nothing usable/);
  assert.equal(JSON.parse(readFileSync(path.join(box.work, SHORTS_DIR, "ai-model-choice-cut-1-2", "lab.json"), "utf8")).line, "cut");

  const later = fakeSite({ settings: { enabled: false }, jobs: [{ kind: "make", holds: [], make: { ...make, source: { ...source, youtube_publish_at: "2026-10-09T11:30:00Z" } } }] });
  const scheduled = context(sandbox(), later, { shortsTools: {} });
  await main(["auto"], scheduled.ctx);
  assert.deepEqual(later.calls.start, ["ai-model-choice-cut-1"], "started, so the calendar can pass it by");
  assert.match(scheduled.out.stdout, /^ai-model-choice-cut-1-2: blocked — 來源 ai-model-choice 還沒公開/);
  assert.equal(later.calls.run.length, 0);
});

test("a Shorts problem is a line, never the end of the tutorials' round", async () => {
  const box = sandbox();
  const site = fakeSite({ jobs: [{ kind: "plan", holds: [] }] });
  const { ctx, out } = context(box, site);
  assert.equal(await main(["auto"], ctx), EXIT.ok);
  assert.match(out.stdout, /shorts: the site named a plan job without its contents/);
  const worker = new ShortsWorker(ctx, automationClient(ctx), {});
  worker.step = async () => {
    throw new Error("something broke");
  };
  const { shortsStep } = await import("./shorts.mjs");
  assert.deepEqual(await shortsStep(worker), ["shorts: stopped by an error (something broke); the round goes on"]);
});
