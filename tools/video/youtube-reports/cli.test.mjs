import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";
import { main, spans, toCsv } from "./cli.mjs";

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
