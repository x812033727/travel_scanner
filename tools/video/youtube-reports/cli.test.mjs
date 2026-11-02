import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";
import { pacificDay, trafficBreakdown, videoSummaries, windowOf } from "./analysis.mjs";
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
