import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { cached, forget, forgetJob, mediaKey, pendingJob, readCache, remember, rememberJob } from "./cache.mjs";
import { MediaError, PART_BYTES, RETAKE_CODES, downloadFile, judge, mediaStatus, putFile, runJob, submitClip, submitImage, waitForJob } from "./client.mjs";
import { STAGES, run, statusText } from "./cli.mjs";
import { appendLedger, capProblem, ledgerTotals, readLedger } from "./ledger.mjs";
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
  const base = mkdtempSync(path.join(tmpdir(), "video-media-"));
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
  const base = mkdtempSync(path.join(tmpdir(), "video-media-"));
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
  const workdir = mkdtempSync(path.join(tmpdir(), "video-media-"));
  mkdirSync(path.join(workdir, "keyframes"));
  writeFileSync(path.join(workdir, "keyframes", "a.png"), "x");
  remember(workdir, key, { file: "keyframes/a.png", sha256: "s", bytes: 1, job_id: "j", provider: "gemini", model: "m", cost_usd: 0.134 });
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
  const workdir = mkdtempSync(path.join(tmpdir(), "video-media-"));
  assert.deepEqual(ledgerTotals(workdir), { usd: 0, images: 0, clip_seconds: 0, music: 0, judge_calls: 0 });
  appendLedger(workdir, { stage: "keyframes", kind: "image", id: "opening", provider: "gemini", model: "m", key: "k", cost_usd: 0.134, status: "ready" });
  appendLedger(workdir, { stage: "clips", kind: "clip", id: "opening", provider: "gemini", model: "m", key: "k2", seconds: 8, cost_usd: 1.2, status: "ready" });
  appendLedger(workdir, { stage: "clips", kind: "judge", id: "opening", provider: "gemini", model: "m", key: "k2", cost_usd: 0.01, status: "judged" });
  appendLedger(workdir, { stage: "music", kind: "music", id: "bgm", provider: "gemini", model: "lyria", key: "k3", cost_usd: 0.08, status: "ready" });
  const totals = ledgerTotals(workdir);
  assert.deepEqual(totals, { usd: 1.424, images: 1, clip_seconds: 8, music: 1, judge_calls: 1 });
  assert.equal(readLedger(workdir).entries.length, 4);
  assert.equal(capProblem(workdir, 1.2, 200), null);
  assert.match(capProblem(workdir, 1.2, 2), /US\$1\.42 .* US\$1\.20.* cap of US\$2/);
  assert.equal(capProblem(workdir, 1.2, 0), null, "no cap means no refusal");
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
  const ctx = { EXIT, env: { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: mkdtempSync(path.join(tmpdir(), "video-home-")), stdout: { write: (t) => (out.stdout += t) }, stderr: { write: (t) => (out.stderr += t) }, fetch: site({ "GET status": () => json(status) }).fetchImpl, sleep: noSleep, mediaHere: mkdtempSync(path.join(tmpdir(), "video-media-none-")) };
  assert.equal(await run("media-status", [], ctx), EXIT.ok);
  assert.match(out.stdout, /judge threshold 7\/10/);
  for (const command of Object.keys(STAGES)) {
    assert.equal(await run(command, ["--slug", "x"], ctx), EXIT.missing, command);
  }
  assert.match(out.stderr, /2026-09-26-video-drama-look-keyframes/);
  assert.match(out.stderr, /2026-09-26-video-drama-clips-music/);
  const noToken = { ...ctx, env: {}, home: mkdtempSync(path.join(tmpdir(), "video-home-")) };
  assert.equal(await run("media-status", [], noToken), EXIT.owner);
});
