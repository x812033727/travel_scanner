import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";
import { clock, firstBigDrop, pacificDay, retentionPoints, trafficBreakdown, videoSummaries, windowOf } from "./analysis.mjs";
import { main, spans, toCsv } from "./cli.mjs";
import { codeName, withNames } from "./codes.mjs";

const TOKEN = `mkv_${"a".repeat(40)}`;
const NOW = new Date("2026-11-02T12:00:00Z");
const OVERVIEW = {
  linked: true, channel_id: "UCx", channel_title: "Mokaair", analytics_granted: true, synced_at: "2026-11-02T03:00:00Z", sync_due: false, problem: null,
  reports: [{ family: "channel_basic", report_type_id: "channel_basic_a3", days: 30, first_day: "2026-10-01", last_day: "2026-10-31", rows: 90 }],
  waiting_for_first_report: [],
  videos: [{ video_id: "vidAAAAAAA1", slug: "ai-agent-vs-chatbot" }],
  policy: "Rows are YouTube Reporting API data exactly as YouTube generated it.",
};

function harness(answer) {
  const out = [];
  const err = [];
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url: new URL(url), init });
    const { status = 200, body } = answer(new URL(url), init);
    return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
  };
  const overrides = {
    env: { MOKAAIR_SITE: "https://mokaair.example", MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: "/nonexistent",
    fetchImpl,
    now: () => NOW,
    stdout: { write: (text) => out.push(text) },
    stderr: { write: (text) => err.push(text) },
  };
  return { out, err, calls, overrides };
}

const rowsAnswer = (url) => {
  const start = url.searchParams.get("start");
  return { body: { report_type_id: "channel_basic_a3", columns: ["date", "video_id", "views"], rows: [[start, "vidAAAAAAA1", "12"]], days: [start], truncated: false } };
};

test("spans split a long range into pieces the site accepts", () => {
  assert.deepEqual(spans("2026-01-01", "2026-01-03", 2), [["2026-01-01", "2026-01-02"], ["2026-01-03", "2026-01-03"]]);
  assert.equal(spans("2026-01-01", "2026-12-31").length, 4);
  assert.equal(toCsv({ columns: ["a", "b"], rows: [["x,y", 'say "hi"']] }), 'a,b\n"x,y","say ""hi"""\n');
});

test("overview reads the site with the token and says what is kept", async () => {
  const { out, calls, overrides } = harness(() => ({ body: OVERVIEW }));
  assert.equal(await main(["overview"], overrides), 0);
  assert.equal(calls[0].url.href, "https://mokaair.example/api/video/youtube-reports");
  assert.equal(calls[0].init.headers.Authorization, `Bearer ${TOKEN}`);
  assert.match(out.join(""), /channel_basic_a3: 30 days, 2026-10-01 to 2026-10-31/);
});

test("overview exits 3 when the owner has to link again with Analytics", async () => {
  const { overrides } = harness(() => ({ body: { ...OVERVIEW, analytics_granted: false, problem: "頻道授權沒有包含 YouTube Analytics（yt-analytics.readonly）" } }));
  assert.equal(await main(["overview"], overrides), 3);
});

test("rows maps a slug to its video, defaults to the last 28 days with data, and writes CSV", async () => {
  const { out, calls, overrides } = harness((url) => (url.pathname.endsWith("/rows") ? rowsAnswer(url) : { body: OVERVIEW }));
  assert.equal(await main(["rows", "--report", "channel_basic", "--slug", "ai-agent-vs-chatbot"], overrides), 0);
  const asked = calls.find((call) => call.url.pathname.endsWith("/rows")).url.searchParams;
  assert.deepEqual([asked.get("start"), asked.get("end"), asked.getAll("video_id")], ["2026-10-04", "2026-10-31", ["vidAAAAAAA1"]]);
  assert.equal(out.join(""), "date,video_id,views\n2026-10-04,vidAAAAAAA1,12\n");
});

test("sync repeats while files remain and stops for the owner when Analytics is missing", async () => {
  let round = 0;
  const { out, calls, overrides } = harness(() => {
    round += 1;
    return { body: { status: round < 3 ? "partial" : "synced", remaining: round < 3, downloaded: 10, replaced: 0, skipped: 0, jobs_created: [], problem: null } };
  });
  assert.equal(await main(["sync"], overrides), 0);
  assert.equal(calls.length, 3);
  assert.deepEqual(calls.map((call) => JSON.parse(call.init.body).force), [false, true, true]);
  assert.match(out.join(""), /30 files/);
  const relink = harness(() => ({ body: { status: "needs_relink", remaining: false, downloaded: 0, replaced: 0, jobs_created: [], problem: "relink" } }));
  assert.equal(await main(["sync"], relink.overrides), 3);
});

test("export writes the overview and one CSV per family", async () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "yt-reports-"));
  try {
    const { overrides } = harness((url) => (url.pathname.endsWith("/rows") ? rowsAnswer(url) : { body: OVERVIEW }));
    assert.equal(await main(["export", "--out", dir, "--days", "7"], overrides), 0);
    assert.equal(JSON.parse(readFileSync(path.join(dir, "overview.json"), "utf8")).channel_id, "UCx");
    assert.equal(readFileSync(path.join(dir, "channel_basic.csv"), "utf8"), "date,video_id,views\n2026-10-25,vidAAAAAAA1,12\n");
    assert.match(readFileSync(path.join(dir, "README.txt"), "utf8"), /exactly as YouTube/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a refusal from the site exits 4, a missing token or bad option exits 2", async () => {
  const refused = harness(() => ({ status: 401, body: { code: "video_tool_token_invalid", detail: "bad" } }));
  assert.equal(await main(["overview"], refused.overrides), 4);
  assert.match(refused.err.join(""), /401 video_tool_token_invalid/);
  const anonymous = harness(() => ({ body: {} }));
  anonymous.overrides.env = { MOKAAIR_SITE: "https://mokaair.example" };
  assert.equal(await main(["overview"], anonymous.overrides), 2);
  const bad = harness(() => ({ body: OVERVIEW }));
  assert.equal(await main(["rows", "--report", "channel_basic", "--from", "yesterday"], bad.overrides), 2);
});


test("codes are named from the dimensions page and an unknown one is shown as itself", () => {
  assert.equal(codeName("traffic_source_type", "5"), "YouTube search");
  assert.equal(codeName("device_type", "104"), "Mobile phone");
  assert.equal(codeName("traffic_source_type", "99"), "code 99");
  const named = withNames({ columns: ["date", "traffic_source_type", "views"], rows: [["2026-10-01", "24", "5"]] });
  assert.deepEqual(named.columns, ["date", "traffic_source_type", "traffic_source_type_name", "views"]);
  assert.deepEqual(named.rows[0], ["2026-10-01", "24", "Shorts", "5"]);
});

test("a video's window starts on its Pacific publishing day and stops at the newest data", () => {
  assert.equal(pacificDay("2026-10-21T03:00:00Z"), "2026-10-20");
  assert.deepEqual(windowOf({ published_at: "2026-10-21T03:00:00Z" }, 7, "2026-10-31"), { start: "2026-10-20", end: "2026-10-26", complete: true });
  assert.deepEqual(windowOf({ published_at: "2026-10-28T20:00:00Z" }, 7, "2026-10-31"), { start: "2026-10-28", end: "2026-10-31", complete: false });
  assert.equal(windowOf({ published_at: "2026-11-05T00:00:00Z" }, 7, "2026-10-31"), null);
});

test("summaries add counts and recompute averages from their parts, inside each window", () => {
  const video = { video_id: "vidAAAAAAA1", slug: "a", title: "A", shorts: false, published_at: "2026-10-20T20:00:00Z" };
  const windows = new Map([["vidAAAAAAA1", { start: "2026-10-20", end: "2026-10-21", complete: true }]]);
  const basic = [
    { date: "2026-10-20", video_id: "vidAAAAAAA1", views: "100", watch_time_minutes: "200", average_view_duration_percentage: "40", subscribers_gained: "3", subscribers_lost: "1" },
    { date: "2026-10-21", video_id: "vidAAAAAAA1", views: "300", watch_time_minutes: "300", average_view_duration_percentage: "20", subscribers_gained: "", subscribers_lost: "" },
    { date: "2026-10-22", video_id: "vidAAAAAAA1", views: "999", watch_time_minutes: "999" },
  ];
  const reach = [
    { date: "2026-10-20", video_id: "vidAAAAAAA1", video_thumbnail_impressions: "1000", video_thumbnail_impressions_ctr: "0.05" },
    { date: "2026-10-21", video_id: "vidAAAAAAA1", video_thumbnail_impressions: "3000", video_thumbnail_impressions_ctr: "0.01" },
  ];
  const [summary] = videoSummaries([video], windows, basic, reach);
  assert.equal(summary.views, 400, "the day after the window is left out");
  assert.equal(summary.average_view_duration_seconds, 75, "500 minutes over 400 views");
  assert.equal(summary.average_view_duration_percentage, 25, "weighted by views, not 30");
  assert.equal(summary.thumbnail_ctr, 0.02, "weighted by impressions, not 0.03");
  assert.equal(summary.subscribers_net, 2);
  assert.equal(summary.likes, null, "a column YouTube did not give stays empty, not zero");
});

test("traffic is grouped by source with its top search terms", () => {
  const sources = trafficBreakdown([
    { traffic_source_type: "5", traffic_source_detail: "ai agent", views: "30", watch_time_minutes: "60" },
    { traffic_source_type: "5", traffic_source_detail: "chatbot", views: "10", watch_time_minutes: "20" },
    { traffic_source_type: "5", traffic_source_detail: "ai agent", views: "5", watch_time_minutes: "5" },
    { traffic_source_type: "24", traffic_source_detail: "", views: "55", watch_time_minutes: "10" },
  ]);
  assert.deepEqual(sources.map((item) => [item.name, item.views, item.share_of_views]), [["Shorts", 55, 0.55], ["YouTube search", 45, 0.45]]);
  assert.deepEqual(sources[1].top_details, [{ detail: "ai agent", views: 35 }, { detail: "chatbot", views: 10 }]);
  assert.equal(sources[1].detail_kind, "search term");
});

test("videos reads the rows of each video's window and labels the numbers as self-computed", async () => {
  const overview = {
    ...OVERVIEW,
    reports: [...OVERVIEW.reports, { family: "channel_reach_basic", report_type_id: "channel_reach_basic_a1", days: 30, first_day: "2026-10-01", last_day: "2026-10-31", rows: 30 }],
    videos: [
      { video_id: "vidAAAAAAA1", slug: "ai-agent-vs-chatbot", title: "A", shorts: false, published_at: "2026-10-20T20:00:00Z" },
      { video_id: "vidSSSSSSS1", slug: "ai-short", title: "S", shorts: true, published_at: "2026-10-22T20:00:00Z" },
    ],
  };
  const answer = (url) => {
    if (!url.pathname.endsWith("/rows")) return { body: overview };
    const report = url.searchParams.get("report");
    const columns = report === "channel_basic" ? ["date", "video_id", "views", "watch_time_minutes"] : ["date", "video_id", "video_thumbnail_impressions", "video_thumbnail_impressions_ctr"];
    const row = report === "channel_basic" ? ["2026-10-21", "vidAAAAAAA1", "50", "100"] : ["2026-10-21", "vidAAAAAAA1", "500", "0.04"];
    return { body: { report_type_id: report, columns, rows: [row], days: ["2026-10-21"], truncated: false } };
  };
  const { out, calls, overrides } = harness(answer);
  assert.equal(await main(["videos", "--long", "--format", "json"], overrides), 0);
  const result = JSON.parse(out.join(""));
  assert.match(result.note, /Self-computed/);
  assert.deepEqual(result.videos.map((item) => [item.slug, item.views, item.thumbnail_impressions, item.average_view_duration_seconds]), [["ai-agent-vs-chatbot", 50, 500, 120]]);
  const asked = calls.filter((call) => call.url.pathname.endsWith("/rows")).map((call) => [call.url.searchParams.get("report"), call.url.searchParams.get("start"), call.url.searchParams.get("end"), call.url.searchParams.getAll("video_id")]);
  assert.deepEqual(asked, [["channel_basic", "2026-10-20", "2026-10-26", ["vidAAAAAAA1"]], ["channel_reach_basic", "2026-10-20", "2026-10-26", ["vidAAAAAAA1"]]]);
  const md = harness(answer);
  assert.equal(await main(["videos"], md.overrides), 0);
  assert.match(md.out.join(""), /^First 7 days after publishing[\s\S]*Self-computed[\s\S]*\| ai-agent-vs-chatbot \|/);
});

test("traffic prints each source and its search terms for a video", async () => {
  const answer = (url) => (url.pathname.endsWith("/rows")
    ? { body: { report_type_id: "channel_traffic_source_a3", columns: ["date", "video_id", "traffic_source_type", "traffic_source_detail", "views", "watch_time_minutes"], rows: [["2026-10-21", "vidAAAAAAA1", "5", "ai agent 是什麼", "12", "30"]], days: ["2026-10-21"], truncated: false } }
    : { body: OVERVIEW });
  const { out, overrides } = harness(answer);
  assert.equal(await main(["traffic", "--slug", "ai-agent-vs-chatbot"], overrides), 0);
  assert.match(out.join(""), /YouTube search \| 5 \| 12 \| 1 \|[\s\S]*top search term[\s\S]*- ai agent 是什麼 \(12 views\)/);
});

// --- retention ---------------------------------------------------------------------------------

/** 100 points: a slow slide, a sharp fall between 9% and 10%, a bigger one at 50% (past 30%). */
function retentionRows() {
  const rows = [];
  for (let step = 1; step <= 100; step += 1) {
    const watch = 1 - step * 0.004 - (step >= 10 ? 0.2 : 0) - (step >= 50 ? 0.3 : 0);
    rows.push([step / 100, Number(watch.toFixed(4)), 0.42]);
  }
  return rows;
}
const RETENTION = {
  video_id: "vidAAAAAAA1", title: "AI 代理", published_at: "2026-10-20T03:00:00+00:00", duration_seconds: 785,
  start: "2026-10-19", end: "2026-11-02", audience: "all",
  columns: ["elapsedVideoTimeRatio", "audienceWatchRatio", "relativeRetentionPerformance"], rows: retentionRows(),
  policy: "Rows are YouTube Analytics API data exactly as YouTube returned it.",
};

test("the first big drop is the largest neighbouring fall within the first 30%, in seconds", () => {
  const points = retentionPoints({ columns: RETENTION.columns, rows: [...RETENTION.rows].reverse() });
  assert.equal(points[0].ratio, 0.01, "points are put in elapsed order");
  const drop = firstBigDrop(points, { duration: 785 });
  assert.deepEqual([drop.from_ratio, drop.to_ratio, drop.fall], [0.09, 0.1, 0.204]);
  assert.deepEqual([drop.from_seconds, drop.to_seconds], [70.6, 78.5]);
  assert.equal(drop.share_lost, Number((0.204 / 0.964).toFixed(4)));
  assert.equal(firstBigDrop(points).from_seconds, null, "no duration, no seconds");
  assert.equal(firstBigDrop(retentionPoints({ columns: RETENTION.columns, rows: [[0.01, 1, 0.5], [0.02, 1.1, 0.5]] })), null);
  assert.equal(clock(78.5), "1:18.5");
});

test("retention asks the site for one video and prints the curve and the self-computed drop", async () => {
  const { out, calls, overrides } = harness((url) => (url.pathname.endsWith("/retention") ? { body: RETENTION } : { body: OVERVIEW }));
  assert.equal(await main(["retention", "--slug", "ai-agent-vs-chatbot", "--organic", "--from", "2026-10-20", "--to", "2026-11-01"], overrides), 0);
  const asked = calls.find((call) => call.url.pathname.endsWith("/retention")).url;
  assert.equal(asked.pathname, "/api/video/youtube-reports/retention");
  assert.deepEqual(Object.fromEntries(asked.searchParams), { video_id: "vidAAAAAAA1", start: "2026-10-20", end: "2026-11-01", organic: "true" });
  const text = out.join("");
  assert.match(text, /duration: 785 s, from the video's length on YouTube/);
  assert.match(text, /first big drop \(self-computed\): 9% -> 10% of the video \(1:10\.6 -> 1:18\.5\): audience watch ratio 0\.964 -> 0\.76, a fall of 0\.204/);
  assert.match(text, /Self-computed from the YouTube Analytics API retention curve/);
  assert.match(text, /\| 0\.1 \| 1:18\.5 \| 0\.76 \| 0\.42 \|/);
  assert.equal(text.split("\n").filter((line) => /^\| 0?\.?\d/.test(line) || /^\| 1 \|/.test(line)).length, 100);
});

test("retention writes CSV with --duration overriding YouTube's length, and JSON with the derived block apart", async () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "yt-retention-"));
  try {
    const file = path.join(dir, "curve.csv");
    const { err, overrides } = harness(() => ({ body: { ...RETENTION, duration_seconds: null } }));
    assert.equal(await main(["retention", "--video", "vidAAAAAAA1", "--duration", "100", "--format", "csv", "--out", file], overrides), 0);
    const lines = readFileSync(file, "utf8").trim().split("\n");
    assert.equal(lines[0], "elapsedVideoTimeRatio,audienceWatchRatio,relativeRetentionPerformance,elapsed_seconds_self_computed");
    assert.equal(lines.length, 101);
    assert.equal(lines[10], "0.1,0.76,0.42,10");
    assert.match(err.join(""), /100 points[\s\S]*first big drop \(self-computed\): 9% -> 10% of the video \(0:09\.0 -> 0:10\.0\)/);
    const json = harness(() => ({ body: RETENTION }));
    assert.equal(await main(["retention", "--video", "vidAAAAAAA1", "--format", "json"], json.overrides), 0);
    const parsed = JSON.parse(json.out.join(""));
    assert.deepEqual(parsed.rows, RETENTION.rows, "YouTube's rows untouched");
    assert.equal(parsed.derived.first_big_drop.to_seconds, 78.5);
    assert.match(parsed.derived.note, /Self-computed/);
    const unknown = harness(() => ({ body: { ...RETENTION, duration_seconds: null } }));
    assert.equal(await main(["retention", "--video", "vidAAAAAAA1"], unknown.overrides), 0);
    assert.match(unknown.out.join(""), /duration: unknown[\s\S]*9% -> 10% of the video: audience/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("retention exits 3 for the owner, 4 for YouTube's refusals, 2 for bad options", async () => {
  const relink = harness(() => ({ status: 409, body: { code: "video_youtube_analytics_missing", detail: "頻道授權沒有包含 YouTube Analytics（yt-analytics.readonly）：到設定分頁按「重新連結」" } }));
  assert.equal(await main(["retention", "--video", "vidAAAAAAA1"], relink.overrides), 3);
  assert.match(relink.err.join(""), /重新連結/);
  for (const [status, code] of [[503, "video_youtube_analytics_disabled"], [404, "video_youtube_retention_no_data"], [404, "video_youtube_retention_other_channel"], [429, "video_youtube_analytics_quota"]]) {
    const refused = harness(() => ({ status, body: { code, detail: "說明" } }));
    assert.equal(await main(["retention", "--video", "vidAAAAAAA1"], refused.overrides), 4, code);
    assert.match(refused.err.join(""), new RegExp(code));
  }
  for (const args of [[], ["--video", "vidAAAAAAA1", "--slug", "x"], ["--video", "a b"], ["--video", "vidAAAAAAA1", "--duration", "-1"], ["--video", "vidAAAAAAA1", "--format", "xml"], ["--video", "vidAAAAAAA1", "--from", "2026-11-02", "--to", "2026-11-01"]]) {
    const bad = harness(() => ({ body: RETENTION }));
    assert.equal(await main(["retention", ...args], bad.overrides), 2, args.join(" "));
    assert.equal(bad.calls.length, 0);
  }
});
