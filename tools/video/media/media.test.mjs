import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { resolveLook } from "../core/drama.mjs";
import { sandbox, tempDir } from "../core/fixtures/load.mjs";
import { cached, forget, forgetJob, mediaKey, pendingJob, readCache, remember, rememberJob } from "./cache.mjs";
import { AVOID, DEFAULT_IMAGE_PROMPT_LIMIT, IMAGE_MODEL_VENDORS, IMAGE_PROMPT_LIMITS, MIN_SHOT_PROMPT_BUDGET, composeShotPrompt, imageModelVendor, imagePromptLimit, promptOverhead, shotPromptBudget } from "./prompt-budget.mjs";
import { EXHAUSTED_CODES, MediaError, PART_BYTES, RETAKE_CODES, downloadFile, judge, locate, mediaStatus, putFile, runJob, scaleBox, stockFetch, stockSearch, submitClip, submitImage, waitForJob } from "./client.mjs";
import { STAGES, exitFor, main, run, statusText } from "./cli.mjs";
import { appendLedger, bookImport, bookJob, capProblem, importedTotals, ledgerTotals, readLedger, release, reserve, reservedEntries, savedTotals } from "./ledger.mjs";
import { VENDOR_NOTICES, assetEntry, candidateText, stockFile, withAsset, withAssets } from "./stock.mjs";
import {
  THRESHOLDS,
  blackdetectArgs,
  clipVerdict,
  dHash,
  duplicates,
  framePsnrArgs,
  hamming,
  parseBlackdetect,
  parseFreezedetect,
  parseProbe,
  parsePsnr,
  parseSceneCuts,
  pictureVerdict,
  sceneCutArgs,
} from "./qc.mjs";

const SITE = "https://mokaair.test";
const TOKEN = `mkv_${"a".repeat(43)}`;
const SHA = (data) => createHash("sha256").update(data).digest("hex");
const noSleep = async () => {};

/** A fake site: `handlers` maps "METHOD path" to a function of (request) → Response. */
function site(handlers) {
  const calls = [];
  const fetchImpl = async (url, init = {}) => {
    const route = `${init.method ?? "GET"} ${new URL(url).pathname.replace("/api/video/media/", "")}${new URL(url).search}`;
    calls.push({ route, headers: init.headers, body: init.body });
    const handler = handlers[route] ?? handlers[route.split("?")[0]];
    if (!handler) return new Response(JSON.stringify({ code: "video_media_route_unknown", detail: `no ${route}` }), { status: 404 });
    return handler({ route, init, calls });
  };
  return { fetchImpl, calls, options: { site: SITE, token: TOKEN, fetchImpl, sleep: noSleep } };
}

const json = (body, status = 200, headers = {}) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...headers } });

test("a request the site keeps refusing is told after its last attempt, with no wait after it", async () => {
  for (const [what, answer] of [
    ["a busy route", () => new Response(JSON.stringify({ code: "rate_limit_exceeded", detail: "slow down" }), { status: 429, headers: { "Retry-After": "60" } })],
    ["a site that is down", () => {
      throw Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("connect ECONNREFUSED"), { code: "ECONNREFUSED" }) });
    }],
  ]) {
    let calls = 0;
    const waits = [];
    const options = { site: SITE, token: TOKEN, fetchImpl: async () => { calls += 1; return answer(); }, sleep: async (ms) => waits.push(ms), attempts: 5 };
    await assert.rejects(mediaStatus(options), (error) => error instanceof MediaError && error.who === "service", what);
    assert.equal(calls, 5, what);
    assert.equal(waits.length, 4, `${what}: a wait between two attempts, none after the last`);
  }
});

test("calls carry the token, and failures say who can fix them", async () => {
  let images = 0;
  const fake = site({
    "GET status": () => json({ enabled: true }),
    "POST images": () => (++images < 3 ? json({ code: "video_media_upstream_busy", detail: "busy" }, 503, { "Retry-After": "1" }) : json({ id: "j1", status: "queued" })),
    "POST clips": () => json({ code: "video_media_budget_exhausted", detail: "spent" }, 429),
    "POST music": () => json({ code: "video_media_reference_missing", detail: "gone" }, 409),
    "POST judge": () => json({ code: "video_tool_token_invalid", detail: "revoked" }, 401),
  });
  assert.deepEqual(await mediaStatus(fake.options), { enabled: true });
  assert.equal(fake.calls[0].headers.Authorization, `Bearer ${TOKEN}`);
  assert.match(fake.calls[0].headers["User-Agent"], /Mokaair-video-cli/);
  const job = await submitImage({ request: { slug: "v", purpose: "keyframe", prompt: "p" }, ...fake.options });
  assert.equal(job.id, "j1", "a busy server is retried");
  assert.equal(fake.calls.filter((call) => call.route === "POST images").length, 3);
  await assert.rejects(submitClip({ request: {}, ...fake.options }), (error) => error instanceof MediaError && error.who === "owner" && error.code === "video_media_budget_exhausted");
  await assert.rejects(judge({ request: {}, ...fake.options }), (error) => error.who === "owner" && error.status === 401);
  await assert.rejects(
    (await import("./client.mjs")).submitMusic({ request: {}, ...fake.options }),
    (error) => error.who === "tool" && error.code === "video_media_reference_missing",
  );
  assert.ok(RETAKE_CODES.has("video_media_rejected") && !RETAKE_CODES.has("video_media_budget_exhausted"));
});

test("locate asks for subject boxes of a stored picture, and a clip is the tool's mistake", async () => {
  const found = { boxes: [{ label: "Jingwei", box: [100, 200, 900, 600], score: 0.93 }], width: 1920, height: 1080, model: "m" };
  let answers = 0;
  const fake = site({
    "POST locate": ({ init }) => {
      const body = JSON.parse(init.body);
      if (body.sha256 === "b".repeat(64)) return json({ code: "video_media_invalid", detail: "locate 只看圖片" }, 422);
      if (body.sha256 === "c".repeat(64)) return ++answers < 2 ? json({ code: "video_media_locate_failed", detail: "no json" }, 502) : json({ ...found, boxes: [] });
      return json(found);
    },
  });
  const request = { slug: "v", sha256: "a".repeat(64), labels: ["Jingwei"] };
  assert.deepEqual(await locate({ request, ...fake.options }), found);
  assert.equal(fake.calls[0].route, "POST locate");
  assert.deepEqual(JSON.parse(fake.calls[0].body), request, "the request goes up as given: slug, sha256, labels");
  assert.deepEqual(scaleBox(found.boxes[0].box, found.width, found.height), { left: 384, top: 108, right: 1152, bottom: 972 });
  assert.deepEqual(scaleBox([-10, 0, 1200, 1000], 100, 50), { left: 0, top: 0, right: 100, bottom: 50 }, "pixels never leave the frame");
  await assert.rejects(locate({ request: { ...request, sha256: "b".repeat(64) }, ...fake.options }), (error) => error instanceof MediaError && error.who === "tool" && error.code === "video_media_invalid" && error.status === 422);
  assert.equal(fake.calls.filter((call) => call.route === "POST locate").length, 2, "a clip is refused once; the tool extracts a frame, it does not retry");
  const empty = await locate({ request: { ...request, sha256: "c".repeat(64) }, ...fake.options });
  assert.deepEqual(empty.boxes, [], "an unusable answer is retried like a failed judge call; nothing found is a plain answer");
});

test("exhausted media requests require a source change instead of another service retry", async () => {
  const detail = "這個請求已經失敗 3 次；改提示詞或 seed 再試";
  const waits = [];
  const fake = site({
    "POST images": () => json({ code: "video_media_job_exhausted", detail }, 409),
    "POST clips": () => json({ code: "video_media_job_exhausted", detail }, 409),
  });
  const EXIT = { owner: 3, external: 4, usage: 2 };
  for (const submit of [submitImage, submitClip]) {
    await assert.rejects(
      submit({ request: { slug: "held", prompt: "unchanged", seed: 1 }, ...fake.options, attempts: 5, sleep: async (ms) => waits.push(ms) }),
      (error) => {
        assert.ok(error instanceof MediaError);
        assert.equal(error.code, "video_media_job_exhausted");
        assert.equal(error.status, 409);
        assert.equal(error.message, detail);
        // The code is the stages' to act on (keyframes moves to the next seed; an owner retry
        // shifts every seed), not the owner's as such; where a stage lets it escape it still
        // exits 3, which parks that video alone, where exit 4 would end every round on it.
        assert.ok(EXHAUSTED_CODES.has(error.code), "a spent request is its own kind, apart from the owner's settings and keys");
        assert.equal(error.who, "owner");
        assert.equal(exitFor(error, EXIT), EXIT.owner, "Automation blocks only this video on exit 3");
        return true;
      },
    );
  }
  assert.equal(fake.calls.length, 2, "each refused operation is submitted only once");
  assert.deepEqual(waits, []);
  assert.ok(!RETAKE_CODES.has("video_media_job_exhausted"), "no identical or blind seed retake after exhaustion");
  assert.deepEqual([...EXHAUSTED_CODES], ["video_media_job_exhausted"]);

  const other = site({ "POST images": () => json({ code: "video_media_upstream_invalid", detail: "invalid" }, 409) });
  await assert.rejects(
    submitImage({ request: {}, ...other.options }),
    (error) => error.who === "service" && error.code === "video_media_upstream_invalid" && exitFor(error, EXIT) === EXIT.external,
    "an unrelated 409 keeps its existing classification",
  );
});

test("a job is polled until it is terminal, honouring the server's retry_after and the STOP file", async () => {
  let polls = 0;
  const waits = [];
  const fake = site({
    "POST clips": () => json({ id: "j2", status: "queued", retry_after_seconds: 5 }, 202),
    "GET jobs/j2": () => {
      polls += 1;
      if (polls < 3) return json({ id: "j2", status: "submitted", retry_after_seconds: 15 });
      return json({ id: "j2", status: "ready", file: { sha256: "x" }, retry_after_seconds: 0 });
    },
  });
  const seen = [];
  const done = await runJob({ submit: submitClip, request: { slug: "v" }, onPoll: (job) => seen.push(job.status), ...fake.options, sleep: async (ms) => waits.push(ms) });
  assert.equal(done.status, "ready");
  assert.deepEqual(seen, ["submitted", "submitted"]);
  assert.deepEqual(waits, [15_000, 15_000], "the server's retry_after sets the pace");
  polls = 0;
  let stops = 0;
  await assert.rejects(
    waitForJob({ jobId: "j2", stop: () => ++stops > 1, ...fake.options }),
    (error) => error.code === "stopped" && error.job.status === "submitted",
  );
  polls = 0;
  let clock = 0;
  await assert.rejects(
    waitForJob({ jobId: "j2", timeoutMs: 10, ...fake.options, now: () => (clock += 100), sleep: noSleep }),
    (error) => error.code === "timeout",
  );
});

test("a download is verified by its hash and never leaves a partial file behind", async () => {
  const base = tempDir("video-media-");
  const clip = Buffer.from("ftyp fake clip bytes");
  const fake = site({
    [`GET files/v/${SHA(clip)}`]: () => new Response(clip, { headers: { "Content-Type": "video/mp4", "Content-Length": String(clip.length) } }),
    [`GET files/v/${"b".repeat(64)}`]: () => new Response(clip, { headers: { "Content-Type": "video/mp4" } }),
    [`GET files/v/${"c".repeat(64)}`]: () => json({ code: "video_media_file_not_found", detail: "gone" }, 404),
  });
  const file = path.join(base, "clips", "a.mp4");
  const got = await downloadFile({ slug: "v", sha256: SHA(clip), file, ...fake.options });
  assert.equal(got.bytes, clip.length);
  assert.equal(readFileSync(file).toString(), clip.toString());
  await assert.rejects(downloadFile({ slug: "v", sha256: "b".repeat(64), file: path.join(base, "bad.mp4"), ...fake.options }), (error) => error.code === "hash_mismatch");
  assert.ok(!existsSync(path.join(base, "bad.mp4")) && !existsSync(path.join(base, "bad.mp4.partial")));
  await assert.rejects(downloadFile({ slug: "v", sha256: "c".repeat(64), file: path.join(base, "c.mp4"), ...fake.options }), (error) => error.status === 404);
  await assert.rejects(downloadFile({ slug: "v", sha256: SHA(clip), file: path.join(base, "d.mp4"), maxBytes: 5, ...fake.options }), (error) => error.code === "too_large");
});

test("a local file goes up in parts with its query until the server says it is complete", async () => {
  const base = tempDir("video-media-");
  const file = path.join(base, "frame.png");
  const data = Buffer.alloc(PART_BYTES + 10, 7);
  writeFileSync(file, data);
  const uploaded = [];
  const fake = site({
    [`PUT files/v/${SHA(data)}`]: ({ route, init }) => {
      uploaded.push({ route, size: init.body.length });
      return json({ received: [0, 1].slice(0, uploaded.length), complete: uploaded.length === 2 });
    },
  });
  const result = await putFile({ slug: "v", file, ...fake.options });
  assert.equal(result.sha256, SHA(data));
  assert.deepEqual(uploaded.map((call) => call.size), [PART_BYTES, 10]);
  assert.match(uploaded[0].route, new RegExp(`part=0&parts=2&size=${data.length}$`));
});

test("cache keys ignore field order, and entries vanish with their files", () => {
  const key = mediaKey("image", { prompt: "p", seed: 1, references: [{ sha256: "a", role: "character" }] });
  assert.equal(key, mediaKey("image", { references: [{ role: "character", sha256: "a" }], seed: 1, prompt: "p" }));
  assert.notEqual(key, mediaKey("image", { prompt: "p", seed: 2, references: [] }));
  assert.notEqual(key, mediaKey("clip", { prompt: "p", seed: 1, references: [{ sha256: "a", role: "character" }] }));
  const workdir = tempDir("video-media-");
  mkdirSync(path.join(workdir, "keyframes"));
  writeFileSync(path.join(workdir, "keyframes", "a.png"), "x");
  remember(workdir, key, { file: "keyframes/a.png", sha256: SHA("x"), bytes: 1, job_id: "j", provider: "gemini", model: "m", cost_usd: 0.134 });
  assert.equal(cached(workdir, key).file, "keyframes/a.png");
  assert.equal(cached(workdir, "nope"), null);
  rememberJob(workdir, "k2", { job_id: "j2", kind: "clip", target: "clips/b.mp4" });
  assert.equal(pendingJob(workdir, "k2").job_id, "j2");
  forgetJob(workdir, "k2");
  assert.equal(pendingJob(workdir, "k2"), null);
  assert.deepEqual(forget(workdir, [key, "nope"]), [key]);
  assert.ok(!existsSync(path.join(workdir, "keyframes", "a.png")));
  assert.deepEqual(readCache(workdir).entries, {});
});

test("the ledger sums what a video paid for and refuses to pass the per-video cap", () => {
  const workdir = tempDir("video-media-");
  assert.deepEqual(ledgerTotals(workdir), { usd: 0, images: 0, clip_seconds: 0, music: 0, judge_calls: 0, reserved: 0, reservations: 0 });
  appendLedger(workdir, { stage: "keyframes", kind: "image", id: "opening", provider: "gemini", model: "m", key: "k", cost_usd: 0.134, status: "ready" });
  appendLedger(workdir, { stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", seconds: 8, cost_usd: 1.2, status: "ready" });
  appendLedger(workdir, { stage: "clips", kind: "judge", id: "opening", provider: "gemini", model: "m", key: "k2", cost_usd: 0.01, status: "judged" });
  appendLedger(workdir, { stage: "music", kind: "music", id: "bgm", provider: "gemini", model: "lyria", key: "k3", cost_usd: 0.08, status: "ready" });
  const totals = ledgerTotals(workdir);
  assert.deepEqual(totals, { usd: 1.424, images: 1, clip_seconds: 8, music: 1, judge_calls: 1, reserved: 0, reservations: 0 });
  assert.equal(readLedger(workdir).entries.length, 4);
  assert.equal(capProblem(workdir, 1.2, 200), null);
  assert.match(capProblem(workdir, 1.2, 2), /US\$1\.42 .* US\$1\.20.* cap of US\$2/);
  assert.match(capProblem(workdir, 1.2, 2), /the next generation costs/);
  assert.match(capProblem(workdir, 0.01, 1.43, "judge call"), /the next judge call costs about US\$0\.01/);
  assert.equal(capProblem(workdir, 1.2, 0), null, "no cap means no refusal");
});

test("money is held before it is spent: a reservation counts toward the cap until the job's charge replaces it or it is released", () => {
  const workdir = tempDir("video-media-");
  const at = new Date("2026-10-05T10:00:00Z");
  appendLedger(workdir, { stage: "keyframes", kind: "image", id: "opening", provider: "gemini", model: "m", key: "k1", job_id: "img-1", cost_usd: 0.134, status: "ready" }, at);
  // The hold is a row of its own, at list price, keyed by the request.
  const held = reserve(workdir, { stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", seconds: 8, cost_usd: 1.2 }, at);
  assert.deepEqual(held, { usd: 1.334, images: 1, clip_seconds: 8, music: 0, judge_calls: 0, reserved: 1.2, reservations: 1 });
  assert.deepEqual(reservedEntries(readLedger(workdir).entries), [{ at: at.toISOString(), stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", seconds: 8, cost_usd: 1.2, status: "reserved" }]);
  assert.throws(() => reserve(workdir, { stage: "clips", kind: "clip", id: "opening", cost_usd: 1 }), /needs the request key/);
  // The cap sees the held money, and says so.
  assert.equal(capProblem(workdir, 0.6, 2), null);
  assert.match(capProblem(workdir, 0.7, 2), /spent US\$1\.33 \(US\$1\.20 of it reserved for 1 request not yet reconciled\) and the next generation costs about US\$0\.70, past the per-video cap of US\$2/);
  // Reserving the same key again holds the money once (a submission repeated after a lost answer).
  reserve(workdir, { stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", seconds: 8, cost_usd: 1.2 }, at);
  assert.deepEqual([readLedger(workdir).entries.length, ledgerTotals(workdir).reserved], [2, 1.2]);
  // The server's charge replaces the hold: fewer dollars than the list price, no second row.
  const booked = bookJob(workdir, { stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", job_id: "clip-1", seconds: 8, cost_usd: 0.9, status: "ready" }, at);
  assert.deepEqual(booked, { usd: 1.034, images: 1, clip_seconds: 8, music: 0, judge_calls: 0, reserved: 0, reservations: 0 });
  assert.deepEqual(readLedger(workdir).entries.map((entry) => [entry.key, entry.status, entry.cost_usd]), [["k1", "ready", 0.134], ["k2", "ready", 0.9]]);
  // A failed job reconciles the hold at what it cost (zero), not at the estimate; a later success under the same id updates that row.
  reserve(workdir, { stage: "clips", kind: "clip", id: "farewell", provider: "gemini", model: "m", key: "k3", seconds: 6, cost_usd: 0.9 }, at);
  bookJob(workdir, { stage: "clips", kind: "clip", id: "farewell", provider: "gemini", model: "m", key: "k3", job_id: "clip-2", seconds: 6, cost_usd: 0, status: "failed", error: "video_media_upstream_failed" }, at);
  assert.deepEqual(readLedger(workdir).entries.at(-1), { at: at.toISOString(), stage: "clips", kind: "clip", id: "farewell", provider: "gemini", model: "m", key: "k3", job_id: "clip-2", seconds: 6, cost_usd: 0, status: "failed", error: "video_media_upstream_failed" });
  reserve(workdir, { stage: "clips", kind: "clip", id: "farewell", provider: "gemini", model: "m", key: "k3", seconds: 6, cost_usd: 0.9 }, at);
  bookJob(workdir, { stage: "clips", kind: "clip", id: "farewell", provider: "gemini", model: "m", key: "k3", job_id: "clip-2", seconds: 6, cost_usd: 0.9, status: "ready" }, at);
  assert.deepEqual(readLedger(workdir).entries.map((entry) => [entry.key, entry.status, entry.cost_usd]), [["k1", "ready", 0.134], ["k2", "ready", 0.9], ["k3", "ready", 0.9]], "the resubmission's hold goes with the job's own row");
  // Nothing submitted: the hold is released, and releasing a key that holds nothing changes nothing.
  reserve(workdir, { stage: "music", kind: "music", id: "bgm", provider: "gemini", model: "lyria", key: "k4", cost_usd: 0.08 }, at);
  assert.equal(ledgerTotals(workdir).reservations, 1);
  assert.deepEqual(release(workdir, "k4"), { usd: 1.934, images: 1, clip_seconds: 14, music: 0, judge_calls: 0, reserved: 0, reservations: 0 });
  assert.deepEqual(release(workdir, "k4"), ledgerTotals(workdir));
  assert.equal(readLedger(workdir).entries.length, 3);
  // An import's hold is replaced by its booking, which does not carry the key; importing the same file again replaces the row and drops a new hold.
  reserve(workdir, { stage: "clips", kind: "clip", id: "bird", provider: "hailuo-web", plan: "pro", credits: 60, key: "import:bird:abc", seconds: 0, cost_usd: 0.5 }, at);
  bookImport(workdir, { stage: "clips", id: "bird", provider: "hailuo-web", plan: "pro", credits: 60, seconds: 5, cost_usd: 0.5, file: "clips/bird-import-1.mp4", sha256: "abc", key: "import:bird:abc" }, at);
  assert.deepEqual(readLedger(workdir).entries.at(-1), { at: at.toISOString(), stage: "clips", id: "bird", provider: "hailuo-web", plan: "pro", credits: 60, seconds: 5, cost_usd: 0.5, file: "clips/bird-import-1.mp4", sha256: "abc", kind: "clip", status: "imported" });
  reserve(workdir, { stage: "clips", kind: "clip", id: "bird", provider: "hailuo-web", plan: "pro", credits: 60, key: "import:bird:abc", seconds: 0, cost_usd: 0.6 }, at);
  bookImport(workdir, { stage: "clips", id: "bird", provider: "hailuo-web", plan: "pro", credits: 60, seconds: 5, cost_usd: 0.6, file: "clips/bird-import-1.mp4", sha256: "abc", key: "import:bird:abc" }, at);
  assert.deepEqual([readLedger(workdir).entries.length, importedTotals(readLedger(workdir).entries).usd, ledgerTotals(workdir).reservations], [4, 0.6, 0]);
});

test("a ledger written before reservations existed reads as before", () => {
  const workdir = tempDir("video-media-");
  mkdirSync(path.join(workdir, "media"), { recursive: true });
  const entries = [
    { at: "2026-09-29T00:00:00.000Z", stage: "keyframes", kind: "image", id: "opening", provider: "gemini", model: "m", key: "k", job_id: "img-1", seconds: 0, cost_usd: 0.134, status: "ready" },
    { at: "2026-09-29T00:00:00.000Z", stage: "keyframes", kind: "judge", id: "opening", provider: "gemini", model: "j", key: null, cost_usd: 0.01, status: "judged" },
    { at: "2026-09-29T00:00:00.000Z", stage: "clips", kind: "clip", id: "bird", provider: "gemini", model: "m", source: { shot: "opening", from_s: 1 }, saved_seconds: 4, saved_usd: 0.6, status: "cut", seconds: 0, cost_usd: 0 },
  ];
  writeFileSync(path.join(workdir, "media", "ledger.json"), JSON.stringify({ entries, totals: { usd: 0.144, images: 1, clip_seconds: 0, music: 0, judge_calls: 1 } }));
  assert.deepEqual(ledgerTotals(workdir), { usd: 0.144, images: 1, clip_seconds: 0, music: 0, judge_calls: 1, reserved: 0, reservations: 0 });
  assert.deepEqual(reservedEntries(readLedger(workdir).entries), []);
  assert.equal(capProblem(workdir, 0.134, 0.3), null);
  assert.match(capProblem(workdir, 0.2, 0.3), /spent US\$0\.14 and the next generation/, "no reservation, no mention of one");
  // A job booked against it without a hold behaves as it always did, and the totals are rewritten in the new shape.
  bookJob(workdir, { stage: "keyframes", kind: "image", id: "farewell", provider: "gemini", model: "m", key: "k2", job_id: "img-2", seconds: 0, cost_usd: 0.134, status: "ready" });
  assert.equal(readLedger(workdir).entries.length, 4);
  assert.deepEqual(readLedger(workdir).totals, { usd: 0.278, images: 2, clip_seconds: 0, music: 0, judge_calls: 1, reserved: 0, reservations: 0 });
  assert.deepEqual(savedTotals(readLedger(workdir).entries), { clip_seconds: 4, usd: 0.6, cuts: 1 });
});

test("ffmpeg logs are parsed into intervals, cuts, shapes and PSNR", () => {
  const probe = parseProbe({ streams: [{ codec_name: "h264", width: 1920, height: 1080, avg_frame_rate: "24/1", nb_read_packets: "192", duration: "8.000" }], format: { duration: "8.02" } });
  assert.deepEqual(probe, { codec: "h264", width: 1920, height: 1080, fps: 24, frames: 192, duration: 8 });
  assert.deepEqual(parseBlackdetect("[blackdetect @ 0x1] black_start:0 black_end:0.5 black_duration:0.5\nother\n[blackdetect @ 0x1] black_start:7.1 black_end:8 black_duration:0.9"), [{ start: 0, end: 0.5 }, { start: 7.1, end: 8 }]);
  assert.deepEqual(parseFreezedetect("[freezedetect @ 0x1] lavfi.freezedetect.freeze_start: 3.5\n[freezedetect @ 0x1] lavfi.freezedetect.freeze_end: 5.0\n[freezedetect @ 0x1] lavfi.freezedetect.freeze_start: 7.0\n", 8), [{ start: 3.5, end: 5 }, { start: 7, end: 8 }]);
  assert.deepEqual(parseSceneCuts("[Parsed_showinfo_1 @ 0x1] n:   0 pts:  96 pts_time:4.0 ...\n[Parsed_showinfo_1 @ 0x1] n:   1 pts: 120 pts_time:5.0"), [4, 5]);
  assert.equal(parsePsnr("[Parsed_psnr_0 @ 0x1] PSNR y:40.1 u:45 v:45 average:41.20 min:41.20 max:41.20"), 41.2);
  assert.equal(parsePsnr("PSNR ... average:inf min:inf max:inf"), Infinity);
  assert.equal(parsePsnr("nothing"), null);
  assert.ok(blackdetectArgs("c.mp4").join(" ").includes("blackdetect=d=0.3:pic_th=0.98"));
  assert.ok(sceneCutArgs("c.mp4").join(" ").includes("gt(scene,0.5)"));
  assert.ok(framePsnrArgs("c.mp4", 0, "k.png", 1920, 1080).join(" ").includes("select=eq(n\\,0)"));
});

test("dHash reads 9x8 grey pixels and hamming counts differing bits", () => {
  const rising = Buffer.from(Array.from({ length: 72 }, (_, index) => index % 9));
  const falling = Buffer.from(Array.from({ length: 72 }, (_, index) => 8 - (index % 9)));
  assert.equal(dHash(rising), "ffffffffffffffff");
  assert.equal(dHash(falling), "0000000000000000");
  assert.equal(hamming(dHash(rising), dHash(falling)), 64);
  assert.equal(hamming("00ff", "00f0"), 4);
  assert.throws(() => dHash(Buffer.alloc(10)), /72 grey pixels/);
  assert.deepEqual(duplicates([{ id: "a", hash: "0000000000000000" }, { id: "b", hash: "0000000000000003" }, { id: "c", hash: "ffffffffffffffff" }]), [{ a: "a", b: "b", distance: 2 }]);
});

test("a clip fails on the faults viewers notice and passes when clean", () => {
  const probe = { width: 1920, height: 1080, fps: 24, frames: 192, duration: 8 };
  const clean = clipVerdict({ probe, requested_s: 8, needed_s: 6.5, keyframe_psnr: 35, judge: { passed: true, overall: 8.5 } });
  assert.deepEqual(clean.problems, []);
  assert.ok(clean.ok && clean.metrics.keyframe_psnr === 35);
  const bad = clipVerdict({
    probe: { ...probe, width: 1024, height: 576, fps: 16, duration: 7.5 },
    requested_s: 8,
    needed_s: 6.5,
    black: [{ start: 0, end: 0.4 }],
    freezes: [{ start: 2, end: 4 }, { start: 7, end: 8 }],
    cuts: [0.04, 3.2],
    keyframe_psnr: 25,
    rival_psnr: 24,
    judge: { passed: false, overall: 5.5, problems: ["six fingers"] },
  });
  assert.ok(!bad.ok);
  assert.equal(bad.problems.length, 8, bad.problems.join("\n"));
  assert.match(bad.problems.join("\n"), /1024x576.*\n.*16\.00 fps.*\n.*7\.50 s.*\n.*black.*\n.*frozen from 2\.00 s to 4\.00 s.*\n.*cut at 3\.20 s.*\n.*neighbouring keyframe/s);
  const outside = clipVerdict({ probe, requested_s: 8, needed_s: 6.5, freezes: [{ start: 7, end: 8 }], keyframe_psnr: 20 });
  assert.deepEqual(outside.problems, ["the first frame does not show the keyframe (PSNR 20.0 dB)"], "a freeze after the narrated part is fine; a wrong first frame is not");
  assert.equal(THRESHOLDS.keyframe_min_psnr, 22);
  assert.deepEqual(pictureVerdict({ width: 1920, height: 1080, judge: { passed: true } }).problems, []);
  assert.equal(pictureVerdict({ width: 512, height: 512, judge: { passed: false, overall: 3, problems: ["blurry"] } }).problems.length, 2);
});

test("media-status prints the server's choices and the video's spend; unbuilt stages name their ticket", async () => {
  const status = {
    enabled: true,
    music_enabled: true,
    image: { provider: "gemini", model: "gemini-3-pro-image", configured: true },
    clip: { provider: "gemini", model: "gemini-omni-1.1-flash", configured: false, resolution: "1080p", seconds: 8 },
    music: { provider: "gemini", model: "lyria-3.5", configured: true },
    budgets: { clip_seconds: { unit: "seconds", limit: 3000, used: 16, remaining: 2984 } },
    estimated_usd: 2.5,
    max_usd_per_video: 200,
    judge_min_score: 7,
    store: { used_bytes: 1.5e9, max_total_bytes: 30e9, writable: true },
  };
  const text = statusText(status, { usd: 1.42, images: 1, clip_seconds: 8, music: 1, judge_calls: 1 });
  assert.match(text, /drama: on; music on\nimage: gemini gemini-3-pro-image\nclip: gemini gemini-omni-1.1-flash 1080p, 8 s \(NO KEY on the site\)/);
  assert.match(text, /budget clip_seconds: 16 of 3000 seconds used this month, 2984 left/);
  assert.match(text, /this video: US\$1\.42 \(1 images, 8 clip seconds, 1 tracks, 1 judge calls\)/);

  const out = { stdout: "", stderr: "" };
  const EXIT = { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 };
  const ctx = { EXIT, env: { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: tempDir("video-home-"), stdout: { write: (t) => (out.stdout += t) }, stderr: { write: (t) => (out.stderr += t) }, fetch: site({ "GET status": () => json(status) }).fetchImpl, sleep: noSleep, mediaHere: tempDir("video-media-none-") };
  assert.equal(await run("media-status", [], ctx), EXIT.ok);
  assert.match(out.stdout, /judge threshold 7\/10/);
  for (const command of Object.keys(STAGES)) {
    assert.equal(await run(command, ["--slug", "x"], ctx), EXIT.missing, command);
  }
  assert.match(out.stderr, /2026-09-26-video-drama-look-keyframes/);
  assert.match(out.stderr, /2026-09-26-video-drama-clips-music/);
  const noToken = { ...ctx, env: {}, home: tempDir("video-home-") };
  assert.equal(await run("media-status", [], noToken), EXIT.owner);
});

// A 1×1 PNG: what a fetched stock photo is to these tests, which never decode it.
const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", "base64");
const PEXELS_CREDIT = {
  provider: "pexels",
  author: "Lukas Rodriguez",
  author_url: "https://www.pexels.com/@lukas-rodriguez-1845331",
  url: "https://www.pexels.com/photo/seoul-at-night-3573351/",
  license: "Pexels License",
  license_url: "https://www.pexels.com/license/",
  text: "Photo by Lukas Rodriguez on Pexels",
};
const PIXABAY_CREDIT = {
  provider: "pixabay",
  author: "Josch13",
  author_url: "https://pixabay.com/users/Josch13-48777/",
  url: "https://pixabay.com/photos/seoul-korea-195893/",
  license: "Pixabay Content License",
  license_url: "https://pixabay.com/service/license-summary/",
  text: "Image by Josch13 from Pixabay",
};
const SEARCH_ANSWER = {
  query: "Seoul skyline",
  candidates: [
    { provider: "pexels", id: "3573351", width: 3066, height: 3968, thumbnail: "https://images.pexels.com/photos/3573351/p.png?h=350", preview: "https://images.pexels.com/photos/3573351/p.png?w=940&h=650", alt: "Seoul skyline at night", credit: PEXELS_CREDIT },
    { provider: "pixabay", id: "195893", width: 4000, height: 2250, thumbnail: "https://cdn.pixabay.com/photo/seoul-195893_150.jpg", preview: "https://pixabay.com/get/195893_640.jpg", alt: "seoul, korea, city", credit: PIXABAY_CREDIT },
  ],
  total: { pexels: 8000, pixabay: 1200 },
  problems: [],
};
const FETCH_ANSWER = { sha256: SHA(PNG), size: PNG.length, content_type: "image/png", width: 1, height: 1, credit: PEXELS_CREDIT };

test("stock search and fetch carry the token to the stock routes, and their failures say who can fix them", async () => {
  let failed = 0;
  let busy = 0;
  const fake = site({
    "POST stock/search": ({ init }) => {
      const body = JSON.parse(init.body);
      if (body.query === "nokey") return json({ code: "video_media_stock_unavailable", detail: "網站的 Pexels 或 Pixabay 金鑰還沒設定，圖庫照片不能用" }, 503);
      if (body.query === "flaky") return ++failed < 3 ? json({ code: "video_media_stock_failed", detail: "Pexels 回的不是 JSON" }, 502) : json(SEARCH_ANSWER);
      if (body.query === "busy") return ++busy < 2 ? json({ code: "video_media_upstream_busy", detail: "Pixabay 的額度用完或太忙" }, 429, { "Retry-After": "2" }) : json(SEARCH_ANSWER);
      return json(SEARCH_ANSWER);
    },
    "POST stock/fetch": ({ init }) => {
      const body = JSON.parse(init.body);
      if (body.id === "404") return json({ code: "video_media_stock_not_found", detail: "Pexels 沒有這張照片" }, 404);
      return json(FETCH_ANSWER);
    },
  });
  const request = { query: "Seoul skyline", orientation: "landscape", per_page: 15, page: 1 };
  assert.deepEqual(await stockSearch({ request, ...fake.options }), SEARCH_ANSWER);
  assert.equal(fake.calls[0].route, "POST stock/search");
  assert.equal(fake.calls[0].headers.Authorization, `Bearer ${TOKEN}`);
  assert.deepEqual(JSON.parse(fake.calls[0].body), request, "the request goes up as given");
  assert.deepEqual(await stockFetch({ request: { slug: "v", provider: "pexels", id: "3573351" }, ...fake.options }), FETCH_ANSWER);
  await assert.rejects(stockSearch({ request: { query: "nokey" }, ...fake.options }), (error) => error instanceof MediaError && error.who === "owner" && error.code === "video_media_stock_unavailable" && error.status === 503);
  assert.equal(fake.calls.filter((call) => call.route === "POST stock/search").length, 2, "a missing key is not retried");
  await assert.rejects(stockFetch({ request: { slug: "v", provider: "pexels", id: "404" }, ...fake.options }), (error) => error.who === "tool" && error.code === "video_media_stock_not_found" && error.status === 404);
  assert.equal(fake.calls.filter((call) => call.route === "POST stock/fetch").length, 2, "a wrong id is refused once; the tool picks another candidate");
  assert.deepEqual(await stockSearch({ request: { query: "flaky" }, ...fake.options }), SEARCH_ANSWER, "a vendor that answered badly is asked again, like a failed locate call");
  assert.equal(failed, 3);
  const waits = [];
  assert.deepEqual(await stockSearch({ request: { query: "busy" }, ...fake.options, sleep: async (ms) => waits.push(ms) }), SEARCH_ANSWER);
  assert.deepEqual(waits, [2000], "a busy vendor sets the pace with its Retry-After");
});

test("a fetched photo is named by its bytes under stock/ and its credit becomes one assets[] entry", () => {
  assert.equal(stockFile("a".repeat(64), "image/jpeg"), `stock/${"a".repeat(64)}.jpg`);
  assert.equal(stockFile("b".repeat(64), "image/png; charset=binary"), `stock/${"b".repeat(64)}.png`);
  assert.equal(stockFile("c".repeat(64), "image/webp"), `stock/${"c".repeat(64)}.webp`);
  assert.throws(() => stockFile("d".repeat(64), "video/mp4"), (error) => error instanceof MediaError && error.who === "tool");
  assert.throws(() => stockFile("not-a-hash", "image/png"), (error) => error instanceof MediaError && error.who === "tool");
  const asset = assetEntry(PEXELS_CREDIT, "stock/x.jpg");
  assert.deepEqual(asset, { path: "stock/x.jpg", source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" }, "the vendor's own wording, the licence, the photographer and the photo page");
  const own = { path: "apps/web/public/d.svg", source: "Mokaair 自有圖解", license: "© Mokaair" };
  assert.deepEqual(withAsset(undefined, asset), [asset]);
  assert.deepEqual(withAsset([own], asset), [own, asset]);
  assert.deepEqual(withAsset([own, { ...asset, source: "older" }], asset), [own, asset], "the same photo again replaces its entry");
  const doc = { slug: "v", sources: [], scenes: [] };
  assert.deepEqual(Object.keys(withAssets(doc, [asset])), ["slug", "sources", "assets", "scenes"], "a document without assets[] gets it before the scenes");
  assert.deepEqual(Object.keys(withAssets({ slug: "v", assets: [], scenes: [] }, [asset])), ["slug", "assets", "scenes"]);
  assert.deepEqual(withAssets({ slug: "v" }, [asset]).assets, [asset]);
});

test("stock search prints each candidate with its credit and the notices the vendors ask for", () => {
  const text = candidateText(SEARCH_ANSWER, "seoul-guide");
  assert.match(text, /^pexels 3573351  3066×3968 portrait  Photo by Lukas Rodriguez on Pexels  https:\/\/www\.pexels\.com\/photo\/seoul-at-night-3573351\/\n  Seoul skyline at night\n/);
  assert.match(text, /\npixabay 195893  4000×2250 landscape  Image by Josch13 from Pixabay  https:\/\/pixabay\.com\/photos\/seoul-korea-195893\/\n/);
  assert.match(text, /\nmatches: pexels 8,000, pixabay 1,200\n/);
  assert.match(text, new RegExp(`\\n${VENDOR_NOTICES.pexels.replace(/[()./]/g, "\\$&")} · ${VENDOR_NOTICES.pixabay.replace(/[()./]/g, "\\$&")}\\n`));
  assert.match(text, /Pixabay's preview links expire after a day/);
  assert.match(text, /\nnext: node tools\/video\/media\/cli\.mjs stock fetch --slug seoul-guide --provider pexels --id 3573351\n$/);
  const one = candidateText({ ...SEARCH_ANSWER, candidates: [SEARCH_ANSWER.candidates[0]], total: { pexels: 1 }, problems: ["Pixabay 的額度用完或太忙"] });
  assert.match(one, /\nnote: Pixabay 的額度用完或太忙\n/);
  assert.doesNotMatch(one, /Images from Pixabay|expire after a day/, "a vendor that did not answer is not named as a source");
  assert.match(candidateText({ query: "nothing", candidates: [], total: { pexels: 0 }, problems: [] }), /^no photos for "nothing"\nmatches: pexels 0\n/);
});

test("stock fetch stores the photo under <workdir>/stock/<sha256>.<ext> and writes its credit into video.json assets[]", async () => {
  const box = sandbox();
  const EXIT = { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 };
  let fetches = 0;
  let downloads = 0;
  const fake = site({
    "POST stock/search": () => json(SEARCH_ANSWER),
    "POST stock/fetch": ({ init }) => {
      fetches += 1;
      const body = JSON.parse(init.body);
      assert.deepEqual(body, { slug: "fixture-minimal", provider: "pexels", id: "3573351" });
      return json(FETCH_ANSWER);
    },
    [`GET files/fixture-minimal/${SHA(PNG)}`]: () => {
      downloads += 1;
      return new Response(PNG, { headers: { "Content-Type": "image/png", "Content-Length": String(PNG.length) } });
    },
  });
  const out = { stdout: "", stderr: "" };
  const ctx = { EXIT, root: box.root, env: { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN, VIDEO_WORKDIR: box.work }, home: tempDir("video-home-"), stdout: { write: (t) => (out.stdout += t) }, stderr: { write: (t) => (out.stderr += t) }, fetch: fake.fetchImpl, sleep: noSleep, now: () => new Date("2026-10-05T12:00:00Z") };

  assert.equal(await run("stock", ["search", "--query", "  Seoul   skyline ", "--slug", box.slug, "--per-page", "2", "--orientation", "landscape"], ctx), EXIT.ok);
  assert.deepEqual(JSON.parse(fake.calls[0].body), { query: "Seoul skyline", per_page: 2, page: 1, orientation: "landscape" }, "the query is tidied; provider is sent only when asked");
  assert.match(out.stdout, /pexels 3573351 .*Photo by Lukas Rodriguez on Pexels/);
  assert.match(out.stdout, /Photos provided by Pexels/);
  assert.match(out.stdout, /stock fetch --slug fixture-minimal --provider pexels --id 3573351/);

  out.stdout = "";
  assert.equal(await run("stock", ["fetch", "--slug", box.slug, "--provider", "pexels", "--id", "3573351"], ctx), EXIT.ok, out.stderr);
  const file = path.join(box.workdir, "stock", `${SHA(PNG)}.png`);
  assert.ok(existsSync(file), "the photo is kept under the work directory");
  assert.deepEqual(readFileSync(file), PNG);
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const expected = { path: `stock/${SHA(PNG)}.png`, source: "Photo by Lukas Rodriguez on Pexels", license: "Pexels License", author: "Lukas Rodriguez", url: "https://www.pexels.com/photo/seoul-at-night-3573351/" };
  assert.deepEqual(doc.assets, [expected]);
  assert.deepEqual(Object.keys(doc).indexOf("assets"), Object.keys(doc).indexOf("scenes") - 1, "assets[] sits before the scenes");
  assert.equal(doc.scenes.length, 3, "the rest of the script is as it was");
  assert.match(out.stdout, new RegExp(`^stock/${SHA(PNG)}\\.png  1×1 square, 0\\.0 MB\\n`));
  assert.match(out.stdout, /Photo by Lukas Rodriguez on Pexels · Pexels License · https:\/\/www\.pexels\.com\/photo\/seoul-at-night-3573351\/\n/);
  assert.match(out.stdout, /assets\[\]: docs\/videos\/fixture-minimal\/video\.json now lists 1 pictures; package writes the credit into the description\n/);
  assert.match(out.stdout, new RegExp(`"image": "stock/${SHA(PNG)}\\.png"`));

  // The same photo again: one file, one entry, no second download.
  out.stdout = "";
  assert.equal(await run("stock", ["fetch", "--slug", box.slug, "--provider", "pexels", "--id", "3573351", "--json"], ctx), EXIT.ok);
  assert.equal(fetches, 2);
  assert.equal(downloads, 1, "a file named by its bytes is not downloaded twice");
  assert.deepEqual(JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8")).assets, [expected]);
  const printed = JSON.parse(out.stdout);
  assert.deepEqual(printed, { file: expected.path, asset: expected, width: 1, height: 1, size: PNG.length, downloaded: false });

  // A torn or replaced copy is fetched again.
  writeFileSync(file, "not the photo");
  assert.equal(await run("stock", ["fetch", "--slug", box.slug, "--provider", "pexels", "--id", "3573351"], ctx), EXIT.ok);
  assert.equal(downloads, 2);
  assert.deepEqual(readFileSync(file), PNG);

  // Usage mistakes are the tool's; a site that does not forward the routes is the owner's deploy.
  for (const args of [["search"], ["fetch", "--slug", box.slug, "--provider", "unsplash", "--id", "1"], ["fetch", "--slug", box.slug, "--provider", "pexels", "--id", "abc"], ["fetch", "--provider", "pexels", "--id", "1"], ["nope"]]) {
    assert.equal(await main(["stock", ...args], ctx), EXIT.usage, args.join(" "));
  }
  const unknown = { ...ctx, fetch: site({}).fetchImpl, stderr: { write: (t) => (out.stderr += t) } };
  out.stderr = "";
  assert.equal(await run("stock", ["search", "--query", "Busan"], unknown), EXIT.owner);
  assert.match(out.stderr, /does not serve the stock photo routes yet/);
  assert.equal(await main(["stock", "search", "--query", "Busan"], { ...ctx, env: {}, home: tempDir("video-home-") }), EXIT.owner, "no token yet");
});

// The vendor module the budget mirrors: what it puts between the prompt and the negative
// prompt, and the length it refuses at.
const MINIMAX_SOURCE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "apps", "api", "app", "video_media", "providers", "minimax.py");

test("a shot's prompt is composed under the image model's limit: corrections go first, from the last, then the scene is cut at a word, and the look never", () => {
  const source = readFileSync(MINIMAX_SOURCE, "utf8");
  assert.equal(source.match(/f"\{request\.prompt\}(\. Avoid: )\{request\.negative_prompt\}"/)[1], AVOID, "AVOID is what minimax.py appends");
  assert.equal(Number(source.match(/^IMAGE_PROMPT_LIMIT = (\d+)$/m)[1]), IMAGE_PROMPT_LIMITS.minimax, "the table carries minimax.py's limit");
  assert.equal(DEFAULT_IMAGE_PROMPT_LIMIT, 4000, "schemas.py MAX_PROMPT_CHARS");

  // A riso look takes about a thousand characters of a 1500 request: the scene gets what is left.
  const look = resolveLook({ preset: "riso-teal" });
  const overhead = promptOverhead({ look, camera: "push in" });
  assert.equal(overhead, `. Style: ${look.style}`.length + ". Camera: push in".length + `${AVOID}${look.negative}`.length);
  const budget = shotPromptBudget({ look, camera: "push in", limit: 1500 });
  assert.equal(budget, 1500 - 1 - overhead);
  assert.ok(budget >= 400 && budget <= 520, `a riso look leaves ${budget} characters for the scene`);
  assert.ok(shotPromptBudget({ look, camera: "push in", cast: "阿明: a tall man", limit: 1500 }) < budget, "a cast takes from the scene's budget");
  assert.equal(shotPromptBudget({ look: { style: "ink", negative: "" }, limit: 100 }), 100 - 1 - ". Style: ink".length, "no negative, no avoidance text");

  // Four corrections of 150 characters beside a 300-character prompt: the last three go, in order.
  const fixes = ["a", "b", "c", "d"].map((letter) => letter.repeat(150));
  const fits = (composed) => composed.prompt.length + AVOID.length + look.negative.length < 1500;
  const corrected = composeShotPrompt({ prompt: "p".repeat(300), look, camera: "push in", fixes, limit: 1500 });
  assert.equal(corrected.droppedFixes, 3);
  assert.equal(corrected.cutChars, 0);
  assert.ok(corrected.prompt.endsWith(`. Camera: push in. Corrections: ${fixes[0]}`), corrected.prompt.slice(-200));
  assert.ok(corrected.prompt.startsWith(`${"p".repeat(300)}. Style: ${look.style}`));
  assert.ok(fits(corrected));
  const whole = composeShotPrompt({ prompt: "p".repeat(300), look, camera: "push in", fixes: fixes.slice(0, 1), limit: 1500 });
  assert.deepEqual([whole.droppedFixes, whole.cutChars], [0, 0], "what fits is sent whole");
  assert.equal(whole.prompt, corrected.prompt);

  // A scene the look leaves no room for is cut at the last word that fits, and the look stays whole.
  const words = Array.from({ length: 120 }, () => "word").join(" ");
  const cut = composeShotPrompt({ prompt: words, look, camera: "push in", fixes, limit: 1500 });
  assert.equal(cut.droppedFixes, 4);
  assert.ok(cut.cutChars > 0 && cut.cutChars < words.length);
  assert.ok(fits(cut));
  const scene = cut.prompt.slice(0, cut.prompt.indexOf(". Style: "));
  assert.ok(scene.length <= budget && scene.length > budget - 6, `cut to ${scene.length} of ${budget}`);
  assert.match(scene, /word$/, "ends on a whole word");
  assert.ok(cut.prompt.includes(`. Style: ${look.style}. Camera: push in`), "the look and the camera are never cut");
  assert.doesNotMatch(cut.prompt, /Corrections/);
  // Whatever the scene and the fixes, the request with the avoidance text is under the limit.
  for (const length of [10, 480, 504, 505, 700, 1000]) {
    for (const given of [[], fixes.slice(0, 2), fixes]) {
      const composed = composeShotPrompt({ prompt: "x ".repeat(length / 2), look, camera: "pan left", fixes: given, limit: 1500 });
      assert.ok(fits(composed), `${length} characters with ${given.length} fixes: ${composed.prompt.length}`);
    }
  }
  assert.equal(composeShotPrompt({ prompt: "a gull", fixes: ["no lettering"] }).prompt, "a gull. Corrections: no lettering", "no look: the prompt and its corrections, as retakePrompt composes them");

  // A look written for a model with a longer limit is the owner's to shorten, not the shot's.
  const heavy = { style: "s".repeat(1000), negative: "n".repeat(500) };
  assert.throws(() => shotPromptBudget({ look: heavy, limit: 1500 }), (error) => error instanceof MediaError && error.code === "video_media_prompt_budget" && error.who === "owner" && /style is 1000 characters and its negative 500/.test(error.message));
  assert.throws(() => composeShotPrompt({ prompt: "x".repeat(100), look: heavy, limit: 1500 }), /video_media_prompt_budget|leaves -?\d+ characters/);
  assert.ok(shotPromptBudget({ look: heavy, limit: 4000 }) > MIN_SHOT_PROMPT_BUDGET, "the same look is fine under the server's field limit");

  // Which limit applies: the server's word for the vendor, then its word for itself, then the table, then the field limit.
  const limits = { image_prompt_chars_minimax: 1200, image_prompt_chars: 3000 };
  assert.equal(imagePromptLimit({ provider: "minimax", model: "image-01" }, { limits }), 1200);
  assert.equal(imagePromptLimit({ provider: "gemini", model: "flash" }, { limits }), 3000);
  assert.equal(imagePromptLimit({ provider: "minimax", model: "image-01" }, { limits: {} }), 1500, "an older server: the table");
  assert.equal(imagePromptLimit({ provider: "minimax", model: "image-01" }, {}), 1500);
  assert.equal(imagePromptLimit({ provider: "gemini", model: "flash" }, { limits: {} }), 4000);
  assert.equal(imagePromptLimit(null, undefined), 4000);
});

// The catalog the vendor table mirrors: every image model's id and vendor.
const CATALOG_SOURCE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "apps", "api", "app", "video_media", "catalog.py");

test("the vendor of an image model named by id alone is the catalog's, so the first draft hears the budget of the model that will draw it", () => {
  const source = readFileSync(CATALOG_SOURCE, "utf8");
  const images = Object.fromEntries([...source.matchAll(/MediaModel\(\s*"([^"]+)",\s*"([^"]+)",\s*"image",/g)].map((match) => [match[1], match[2]]));
  assert.ok(Object.keys(images).length >= 3, "the catalog's image models were read");
  assert.deepEqual(IMAGE_MODEL_VENDORS, images, "IMAGE_MODEL_VENDORS is catalog.py's image models");
  assert.equal(imageModelVendor("image-01"), "minimax");
  assert.equal(imageModelVendor("gemini-3.1-flash-image"), "gemini");
  assert.equal(imageModelVendor("gemini-4-image-preview"), "gemini", "a Gemini id the table does not know yet reads as Gemini");
  assert.equal(imageModelVendor("hailuo-image", "minimax"), "minimax", "an unknown id is the caller's fallback");
  assert.equal(imageModelVendor(null), null);
  assert.equal(imageModelVendor(""), null);
});
