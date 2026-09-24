import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { SAMPLES_PER_FRAME, SAMPLE_RATE } from "../core/timeline.mjs";
import { SpeechError, speechStatus, synthesize } from "./client.mjs";
import { credentialsFile, readCredentials, writeCredentials } from "./credentials.mjs";
import { MAX_REQUEST_CHARACTERS, billableForRequest, planRequests, spokenParts } from "./requests.mjs";
import { plausibleSplit, silenceRuns, splitAtSilences, trimSilence } from "./split.mjs";
import { buildNarration, flaggedLines, synthesizeRequest } from "./synthesis.mjs";
import { concatSamples, encodeWav, parseWav, requireNarrationFormat, WavError } from "./wav.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const ms = (value) => Math.round((value / 1000) * SAMPLE_RATE);
const tone = (milliseconds) => Int16Array.from({ length: ms(milliseconds) }, (_, index) => Math.round(8000 * Math.sin(index / 7)));
const quiet = (milliseconds) => new Int16Array(ms(milliseconds));

test("WAV round-trips, tolerates a streamed data size, and must be 48 kHz 16-bit mono", () => {
  const samples = Int16Array.from([0, 1, -1, 32767, -32768]);
  const wav = encodeWav(samples);
  assert.deepEqual([...requireNarrationFormat(parseWav(wav))], [...samples]);
  const streamed = Buffer.from(wav);
  streamed.writeUInt32LE(0xffffffff, 40);
  assert.equal(parseWav(streamed).samples.length, 5);
  assert.throws(() => requireNarrationFormat(parseWav(encodeWav(samples, 24000))), /24000 Hz/);
  assert.throws(() => parseWav(Buffer.from("not audio")), WavError);
});

test("a scene is cut at its longest silences, not at the short pauses inside sentences", () => {
  const scene = concatSamples([quiet(100), tone(1000), quiet(250), tone(400), quiet(800), tone(2000), quiet(800), tone(500), quiet(120)]);
  assert.equal(silenceRuns(scene).length, 2);
  const ranges = splitAtSilences(scene, 3);
  const pieces = ranges.map((range) => trimSilence(scene.slice(range.start, range.end)));
  const seconds = pieces.map((piece) => piece.length / SAMPLE_RATE);
  assert.ok(Math.abs(seconds[0] - 1.73) < 0.05, `first piece ${seconds[0]}`);
  assert.ok(Math.abs(seconds[1] - 2.08) < 0.05, `second piece ${seconds[1]}`);
  assert.ok(Math.abs(seconds[2] - 0.58) < 0.05, `third piece ${seconds[2]}`);
  assert.equal(splitAtSilences(scene, 4), null, "not enough silences for four lines");
  assert.ok(plausibleSplit(pieces.map((piece) => piece.length), [16, 20, 5]));
  assert.ok(!plausibleSplit(pieces.map((piece) => piece.length), [5, 20, 16]));
});

test("dictionary terms become parts with their spoken form, whole words only, longest first", () => {
  const lexicon = { schema_version: 1, terms: { LLM: "L L M", "Claude Code": "Claude Code 工具", Claude: null } };
  assert.deepEqual(spokenParts("用 Claude Code 跑 LLM，不是 LLMs。", lexicon), [
    { text: "用 " },
    { text: "Claude Code", alias: "Claude Code 工具" },
    { text: " 跑 " },
    { text: "LLM", alias: "L L M" },
    { text: "，不是 LLMs。" },
  ]);
  assert.deepEqual(spokenParts("純中文", { terms: {} }), [{ text: "純中文" }]);
});

test("requests follow scenes, stay under the server's limit and change key when their words do", () => {
  // Two of these fill the 1,500-character limit exactly; the short third line starts a new request.
  const long = "字".repeat(750);
  const doc = {
    voice: { provider: "azure", name: "zh-TW-HsiaoChenNeural" },
    scenes: [
      { id: "a", lines: [{ id: "a1", text: long }, { id: "a2", text: long }, { id: "a3", text: "短句。" }] },
      { id: "b", lines: [{ id: "b1", text: "另一個場景。" }] },
    ],
  };
  const requests = planRequests(doc, { terms: {} });
  assert.deepEqual(requests.map((request) => request.lines.map((line) => line.id)), [["a1", "a2"], ["a3"], ["b1"]]);
  assert.deepEqual(requests[0].body.segments.map((segment) => segment.break_after_ms), [800, 0]);
  for (const request of requests) assert.ok(request.body.segments.reduce((sum, segment) => sum + segment.parts[0].text.length, 0) <= MAX_REQUEST_CHARACTERS);
  const changed = structuredClone(doc);
  changed.scenes[1].lines[0].text = "改過的場景。";
  const again = planRequests(changed, { terms: {} });
  assert.equal(again[0].key, requests[0].key);
  assert.notEqual(again[2].key, requests[2].key);
  // Each Chinese character is billed twice, plus the break markup.
  assert.equal(billableForRequest({ voice: "zh-TW-X", segments: [{ parts: [{ text: "中文A" }], break_after_ms: 800 }] }), 3 + 2 + '<break time="800ms"/>'.length);
});

function fakeServer({ status = {}, failures = [] } = {}) {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    const failure = failures.shift();
    if (failure) return new Response(JSON.stringify({ code: failure.code, detail: failure.detail ?? failure.code }), { status: failure.status, headers: { "Content-Type": "application/json", ...(failure.headers ?? {}) } });
    if (url.endsWith("/api/video/speech/status")) {
      return Response.json({ configured: true, region: "eastasia", voices: ["zh-TW-HsiaoChenNeural", "zh-TW-YunJheNeural"], output_format: "riff-48khz-16bit-mono-pcm", max_request_characters: 1500, monthly_limit: 450000, used: 0, remaining: 450000, ...status });
    }
    const body = JSON.parse(init.body);
    // Speech takes 60 ms a character, then the requested break.
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60), quiet(segment.break_after_ms)]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { calls, fetchImpl };
}

test("the client retries throttling with Retry-After and sorts failures by who can fix them", async () => {
  const slept = [];
  const server = fakeServer({ failures: [{ status: 429, code: "video_speech_upstream_busy", headers: { "Retry-After": "7" } }] });
  const options = { site: "https://mokaair.com", token: TOKEN, fetchImpl: server.fetchImpl, sleep: async (value) => slept.push(value) };
  const result = await synthesize({ ...options, body: { voice: "v", segments: [{ parts: [{ text: "好" }] }] } });
  assert.equal(parseWav(result.wav).sampleRate, SAMPLE_RATE);
  assert.deepEqual(slept, [7000]);
  assert.equal(new Headers(server.calls[0].init.headers).get("authorization"), `Bearer ${TOKEN}`);

  const revoked = fakeServer({ failures: [{ status: 401, code: "video_tool_token_invalid" }] });
  await assert.rejects(speechStatus({ ...options, fetchImpl: revoked.fetchImpl }), (error) => error instanceof SpeechError && error.who === "owner");
  const spent = fakeServer({ failures: [{ status: 429, code: "video_speech_budget_exhausted" }] });
  await assert.rejects(synthesize({ ...options, fetchImpl: spent.fetchImpl, body: {} }), (error) => error.who === "service" && spent.calls.length === 1);
  const down = fakeServer({ failures: Array.from({ length: 5 }, () => ({ status: 502, code: "video_speech_upstream_failed" })) });
  await assert.rejects(synthesize({ ...options, fetchImpl: down.fetchImpl, body: {} }), /video_speech_upstream_failed/);
  assert.equal(down.calls.length, 5);
});

test("credentials live in the home directory, and environment variables override them", () => {
  const home = mkdtempSync(path.join(tmpdir(), "video-home-"));
  assert.equal(readCredentials({ env: {}, home }).token, null);
  const file = writeCredentials({ site: "https://mokaair.com", token: TOKEN }, { home });
  assert.equal(file, credentialsFile(home));
  assert.equal(readCredentials({ env: {}, home }).token, TOKEN);
  assert.equal(readCredentials({ env: { MOKAAIR_SITE: "http://localhost:3000/" }, home }).site, "http://localhost:3000");
  assert.throws(() => writeCredentials({ site: "https://mokaair.com", token: "eyJhbGciOi.session" }, { home }), /mkv_/);
  assert.throws(() => writeCredentials({ site: "http://evil.example", token: TOKEN }, { home }), /https/);
});

test("a request whose silences do not match its text is redone line by line", async () => {
  const request = { id: "s#0", lines: [{ id: "a", parts: [{ text: "一二三四" }], weight: 4 }, { id: "b", parts: [{ text: "五" }], weight: 1 }], body: { voice: "v", segments: [] } };
  const bodies = [];
  // The whole-request answer has no silence to cut at; the single-line answers are fine.
  const fake = async (body) => {
    bodies.push(body);
    const length = body.segments.length === 0 ? 3000 : body.segments[0].parts[0].text.length * 200;
    return { wav: encodeWav(tone(length)), billable: 5 };
  };
  const result = await synthesizeRequest(request, fake);
  assert.equal(result.fallback, true);
  assert.equal(bodies.length, 3);
  assert.equal(result.billable, 15);
  assert.deepEqual([...result.clips.keys()], ["a", "b"]);
});

test("narration is each clip followed by silence up to its end frame", () => {
  const timeline = { lines: [{ id: "a", start_frame: 0, end_frame: 3, audio_samples: 2000 }, { id: "b", start_frame: 3, end_frame: 4, audio_samples: 1600 }] };
  const clips = new Map([["a", tone(2000 / 48)], ["b", tone(1600 / 48)]]);
  clips.set("a", clips.get("a").slice(0, 2000));
  clips.set("b", clips.get("b").slice(0, 1600));
  const narration = buildNarration(timeline, clips);
  assert.equal(narration.length, 4 * SAMPLES_PER_FRAME);
  assert.equal(narration[2000], 0);
  assert.throws(() => buildNarration(timeline, new Map([["a", new Int16Array(5)], ["b", new Int16Array(1600)]])), /expects 2000/);
  assert.deepEqual([...flaggedLines({ flags: ["a"] })], ["a"]);
  assert.deepEqual([...flaggedLines({ lines: { a: true, b: false } })], ["a"]);
});

function capture(overrides) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-24T05:00:00Z"),
      sleep: async () => {},
      ...overrides,
    },
  };
}

test("tts writes frame-aligned narration and a timeline, then only redoes what changed", async () => {
  const box = sandbox();
  const server = fakeServer();
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const first = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  const narration = parseWav(readFileSync(path.join(box.workdir, "narration.wav")));
  assert.equal(narration.samples.length, timeline.total_frames * SAMPLES_PER_FRAME);
  assert.equal(timeline.lines.length, 7);
  assert.match(timeline.speech_hash, /^[0-9a-f]{16}$/);
  for (const line of timeline.lines) assert.ok(existsSync(path.join(box.workdir, "audio", `${line.id}.wav`)));
  const synthesized = server.calls.filter((call) => call.url.endsWith("/api/video/speech")).length;
  assert.equal(synthesized, 3, "one request per scene");

  const second = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  await main(["tts", "--slug", box.slug], second.ctx);
  assert.equal(server.calls.filter((call) => call.url.endsWith("/api/video/speech")).length, synthesized, "nothing to redo");

  const file = path.join(box.dir, "video.json");
  writeFileSync(file, readFileSync(file, "utf8").replace("第二個問題是", "第二個問題則是"));
  const third = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  await main(["tts", "--slug", box.slug], third.ctx);
  assert.equal(server.calls.filter((call) => call.url.endsWith("/api/video/speech")).length, synthesized + 1, "only the changed scene");

  const status = capture({ root: box.root, env, home: box.base });
  await main(["status", "--slug", box.slug], status.ctx);
  assert.match(status.out.stdout, /\[x\] narration synthesized/);
});

test("tts without a token, or against an unconfigured card, needs the owner", async () => {
  const box = sandbox();
  const none = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base });
  assert.equal(await main(["tts", "--slug", box.slug], none.ctx), EXIT.owner);
  assert.match(none.out.stderr, /login/);
  const unconfigured = fakeServer({ status: { configured: false } });
  const ctx = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: box.base, fetch: unconfigured.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], ctx.ctx), EXIT.owner);
  const dry = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base });
  assert.equal(await main(["tts", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok);
  assert.match(dry.out.stdout, /3 requests, 3 to synthesize; about \d+ billable characters/);
});

test("audition writes one clip per allowed voice and a page to compare them", async () => {
  const box = sandbox();
  const server = fakeServer();
  const sample = path.join(box.base, "sample.txt");
  writeFileSync(sample, "﻿排行榜第一名，不一定最適合你。");
  const { ctx, out } = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["audition", "--text-file", sample], ctx), EXIT.ok, out.stderr);
  const page = /open (.+index\.html)/.exec(out.stdout)[1];
  const html = readFileSync(page, "utf8");
  assert.match(html, /zh-TW-HsiaoChenNeural\.wav/);
  assert.match(html, /zh-TW-YunJheNeural\.wav/);
  assert.ok(existsSync(path.join(path.dirname(page), "zh-TW-YunJheNeural.wav")));
  const refused = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["audition", "--text-file", sample, "--voices", "en-GB-SoniaNeural"], refused.ctx), EXIT.owner);
});

test("login --paste checks the token against the server before saving it", async () => {
  const box = sandbox();
  const server = fakeServer();
  const { ctx, out } = capture({ root: box.root, env: {}, home: box.base, fetch: server.fetchImpl, readSecret: async () => TOKEN });
  assert.equal(await main(["login", "--paste"], ctx), EXIT.ok);
  assert.equal(readCredentials({ env: {}, home: box.base }).token, TOKEN);
  assert.match(out.stdout, /speech configured/);
  const bad = capture({ root: box.root, env: {}, home: box.base, readSecret: async () => "nope" });
  assert.equal(await main(["login", "--paste"], bad.ctx), EXIT.usage);
});

/** A site that answers "pending" a few times, then the given final poll answer. */
function pairingServer({ pendingPolls = 2, final = { status: "approved", token: TOKEN, token_name: "配對：影片工具" } } = {}) {
  const speech = fakeServer();
  const calls = [];
  let polls = 0;
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    if (url.endsWith("/api/video/pairings")) {
      return Response.json(
        { device_code: "d".repeat(43), user_code: "BCDF-GHJK", verification_path: "/zh-TW/admin/settings?provider=azure_speech&video_pairing=BCDFGHJK", expires_in: 600, interval: 5 },
        { status: 201 },
      );
    }
    if (url.endsWith("/api/video/pairings/poll")) {
      polls += 1;
      return Response.json(polls <= pendingPolls ? { status: "pending", interval: 5, token: null } : { interval: 5, ...final });
    }
    return speech.fetchImpl(url, init);
  };
  return { calls, fetchImpl };
}

test("login pairs by default: it prints the code and link, never the token, and saves it", async () => {
  const box = sandbox();
  const server = pairingServer();
  const slept = [];
  const { ctx, out } = capture({ root: box.root, env: {}, home: box.base, fetch: server.fetchImpl, sleep: async (value) => slept.push(value) });
  assert.equal(await main(["login", "--name", "工作室筆電"], ctx), EXIT.ok, out.stderr);
  assert.match(out.stdout, /code: BCDF-GHJK/);
  assert.match(out.stdout, /https:\/\/mokaair\.com\/zh-TW\/admin\/settings\?provider=azure_speech&video_pairing=BCDFGHJK/);
  assert.ok(!out.stdout.includes(TOKEN) && !out.stderr.includes(TOKEN), "the token is never printed");
  assert.equal(readCredentials({ env: {}, home: box.base }).token, TOKEN);
  assert.deepEqual(slept, [5000, 5000, 5000]);
  const start = server.calls.find((call) => call.url.endsWith("/api/video/pairings"));
  assert.deepEqual(JSON.parse(start.init.body), { client_name: "工作室筆電" });
  assert.equal(new Headers(start.init.headers).get("authorization"), null);
  const polls = server.calls.filter((call) => call.url.endsWith("/pairings/poll"));
  assert.ok(polls.every((call) => JSON.parse(call.init.body).device_code === "d".repeat(43)));
});

test("a denied or expired pairing needs the owner and saves nothing", async () => {
  const box = sandbox();
  const denied = capture({ root: box.root, env: {}, home: box.base, fetch: pairingServer({ final: { status: "denied" } }).fetchImpl });
  assert.equal(await main(["login"], denied.ctx), EXIT.owner);
  assert.match(denied.out.stderr, /denied/);
  assert.equal(readCredentials({ env: {}, home: box.base }).token, null);

  // The clock runs out while the owner has not answered.
  let clock = Date.parse("2026-09-24T05:00:00Z");
  const expired = capture({
    root: box.root,
    env: {},
    home: box.base,
    fetch: pairingServer({ pendingPolls: 1000 }).fetchImpl,
    now: () => new Date(clock),
    sleep: async (value) => {
      clock += value;
    },
  });
  assert.equal(await main(["login"], expired.ctx), EXIT.owner);
  assert.match(expired.out.stderr, /expired/);
});

test("login explains a site that does not offer pairing yet", async () => {
  const box = sandbox();
  const old = capture({ root: box.root, env: {}, home: box.base, fetch: async () => new Response("not found", { status: 404 }) });
  assert.equal(await main(["login"], old.ctx), EXIT.external);
  assert.match(old.out.stderr, /--paste/);
});
