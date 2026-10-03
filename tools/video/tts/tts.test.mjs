import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { SAMPLES_PER_FRAME, SAMPLE_RATE, speechHash } from "../core/timeline.mjs";
import { LONG_ANIME_POLICY, runtimePolicyHash } from "../core/anime-policy.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { buildCues } from "../core/captions.mjs";
import { approve, approvalState } from "../core/approvals.mjs";
import { SpeechError, speechStatus, synthesize } from "./client.mjs";
import { credentialsFile, readCredentials, writeCredentials } from "./credentials.mjs";
import { MAX_REQUEST_CHARACTERS, billableForRequest, planRequests, spokenParts } from "./requests.mjs";
import { plausibleSplit, silenceRuns, splitAtSilences, trimSilence } from "./split.mjs";
import { buildNarration, flaggedLines, synthesizeRequest } from "./synthesis.mjs";
import { concatSamples, encodeWav, parseWav, requireNarrationFormat, WavError } from "./wav.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

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
  // A slides clip's key is the voice fields and the parts, as it was before dramas had speakers:
  // the audio caches of every published video depend on it.
  const pinned = createHash("sha256").update(JSON.stringify([{ voice: "zh-TW-HsiaoChenNeural", rate: "+0%" }, [{ text: "另一個場景。" }]])).digest("hex").slice(0, 16);
  assert.equal(requests[2].lines[0].key, pinned);
  assert.ok(requests.every((request) => request.speaker === "narrator"));
  // Each Chinese character is billed twice, plus the break markup.
  assert.equal(billableForRequest({ voice: "zh-TW-X", segments: [{ parts: [{ text: "中文A" }], break_after_ms: 800 }] }), 3 + 2 + '<break time="800ms"/>'.length);
});

test("a drama's requests change with the speaker, and a line's emotion rides in the Gemini style", () => {
  const doc = {
    format: "drama",
    voice: { provider: "gemini", name: "Sulafat", style: "說書人" },
    characters: [
      { id: "jingwei", name: "精衛", voice: { provider: "gemini", name: "Kore", style: "少女" } },
      { id: "yandi", name: "炎帝", voice: { provider: "azure", name: "zh-TW-YunJheNeural" } },
    ],
    scenes: [
      {
        id: "s",
        lines: [
          { id: "n1", text: "旁白一。" },
          { id: "n2", text: "旁白二。" },
          { id: "j1", text: "父王。", speaker: "jingwei", emotion: "急" },
          { id: "j2", text: "我去了。", speaker: "jingwei", emotion: "急" },
          { id: "j3", text: "再見。", speaker: "jingwei" },
          { id: "y1", text: "早點回來。", speaker: "yandi", emotion: "擔心" },
          { id: "n3", text: "旁白三。", speaker: "narrator" },
        ],
      },
    ],
  };
  const requests = planRequests(doc, { terms: {} });
  // Consecutive lines by one speaker with one emotion share a request; anything else starts a new one.
  assert.deepEqual(requests.map((request) => request.lines.map((line) => line.id)), [["n1", "n2"], ["j1", "j2"], ["j3"], ["y1"], ["n3"]]);
  assert.deepEqual(requests.map((request) => request.speaker), ["narrator", "jingwei", "jingwei", "yandi", "narrator"]);
  assert.deepEqual(requests.map((request) => request.id), ["s#0", "s#1", "s#2", "s#3", "s#4"]);
  assert.equal(requests[0].body.voice, "gemini:Sulafat");
  assert.equal(requests[0].body.style, "說書人");
  assert.equal(requests[1].body.voice, "gemini:Kore");
  assert.equal(requests[1].body.style, "少女。急");
  assert.equal(requests[2].body.style, "少女");
  // Azure has no style prompt, so the emotion goes nowhere (lint warns about it).
  assert.deepEqual(requests[3].body, { voice: "zh-TW-YunJheNeural", rate: "+0%", segments: [{ parts: [{ text: "早點回來。" }], break_after_ms: 0 }] });
  // The same words in another emotion are another take, and a request of their own; the line
  // after them keeps its take.
  const calmer = structuredClone(doc);
  calmer.scenes[0].lines[2].emotion = "平靜";
  const retaken = planRequests(calmer, { terms: {} });
  assert.deepEqual(retaken.map((request) => request.lines.map((line) => line.id)), [["n1", "n2"], ["j1"], ["j2"], ["j3"], ["y1"], ["n3"]]);
  assert.notEqual(retaken[1].lines[0].key, requests[1].lines[0].key);
  assert.equal(retaken[2].lines[0].key, requests[1].lines[1].key);
  // A long style plus an emotion is cut at the server's 400 characters.
  const verbose = structuredClone(doc);
  verbose.characters[0].voice.style = "字".repeat(398);
  assert.equal(planRequests(verbose, { terms: {} })[1].body.style.length, 400);
});

test("production readings follow only spoken names, aliases and terms, and bind speech/request caches without changing CC", () => {
  const doc = {
    format: "drama", voice: { provider: "gemini", name: "Kore", style: "平靜，咬字清楚" },
    pronunciation_hints: { 沈亦微: "微讀ㄨㄟˊ", 老鄧: "ㄌㄠˇ ㄉㄥˋ", 青釐盞: "釐讀ㄌㄧˊ", 釐: "不得取代完整術語", 秦硯山: "硯四聲", 安歲散: null },
    scenes: [{ id: "scene", lines: [{ id: "name1", text: "老鄧，把青釐盞交給沈亦微。" }, { id: "plain", text: "先把門關上。" }] }],
  };
  const before = JSON.stringify(doc);
  const planned = planRequests(doc, { terms: { LLM: "L L M" } });
  assert.equal(planned.length, 2, "only the line saying these terms carries their metadata");
  assert.match(planned[0].body.style, /老鄧＝ㄌㄠˇ ㄉㄥˋ.*青釐盞＝釐讀ㄌㄧˊ.*沈亦微＝微讀ㄨㄟˊ/);
  assert.ok(!planned[0].body.style.includes("不得取代完整術語"));
  assert.ok(!planned[0].body.style.includes("秦硯山"));
  assert.equal(planned[1].body.style, doc.voice.style);
  assert.deepEqual(planned[0].body.segments[0].parts, [{ text: doc.scenes[0].lines[0].text }]);
  assert.equal(JSON.stringify(doc), before);
  const changed = structuredClone(doc);
  changed.pronunciation_hints.沈亦微 = "沈三聲，微二聲";
  const updated = planRequests(changed, { terms: {} });
  assert.notEqual(updated[0].lines[0].key, planned[0].lines[0].key);
  assert.equal(updated[1].lines[0].key, planned[1].lines[0].key);
  assert.notEqual(speechHash(changed, { terms: {} }), speechHash(doc, { terms: {} }));
  changed.pronunciation_hints = { ...doc.pronunciation_hints, 秦硯山: "未說出的另一讀法" };
  assert.equal(speechHash(changed, { terms: {} }), speechHash(doc, { terms: {} }));
  const tooLong = structuredClone(doc);
  tooLong.voice.style = "字".repeat(390);
  assert.throws(() => planRequests(tooLong, { terms: {} }), /exceeds 400/);
});

test("audio_ref requires an earlier original's speaker, spoken content and effective voice, never implicit deduplication", () => {
  const doc = { format: "drama", voice: { provider: "gemini", name: "Kore" }, scenes: [{ id: "scene", lines: [
    { id: "base1", text: "你看到我的哨子嗎？" }, { id: "copy1", text: "你看到我的哨子嗎？", audio_ref: "base1", pause_after_ms: 900 },
  ] }] };
  assert.equal(planRequests(doc, { terms: {} })[1].audio_ref, "base1");
  const noRef = structuredClone(doc);
  delete noRef.scenes[0].lines[1].audio_ref;
  assert.ok(planRequests(noRef, { terms: {} }).every((request) => !request.audio_ref));
  assert.notEqual(speechHash(doc, { terms: {} }), speechHash(noRef, { terms: {} }));
  for (const change of [
    (copy) => { copy.scenes[0].lines[1].audio_ref = "copy1"; },
    (copy) => { copy.scenes[0].lines[0].audio_ref = "copy1"; },
    (copy) => { copy.scenes[0].lines[1].text = "另一句"; },
    (copy) => { copy.scenes[0].lines[1].speaker = "different"; },
    (copy) => { copy.scenes[0].lines[1].emotion = "小聲"; },
    (copy) => { copy.scenes[0].lines.push({ ...copy.scenes[0].lines[1], id: "copy2", audio_ref: "copy1" }); },
  ]) {
    const invalid = structuredClone(doc); change(invalid);
    assert.throws(() => planRequests(invalid, { terms: {} }), /earlier original take/);
  }
});

function fakeServer({ status = {}, failures = [], gain = () => 1 } = {}) {
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
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60).map((sample) => Math.round(sample * gain())), quiet(segment.break_after_ms)]));
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
  const timeline = { total_frames: 4, lines: [{ id: "a", start_frame: 0, end_frame: 3, audio_samples: 2000 }, { id: "b", start_frame: 3, end_frame: 4, audio_samples: 1600 }] };
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

test("natural visual actions align actual narration samples before, between and after spoken clips", () => {
  const timeline = { total_frames: 12, lines: [{ id: "a", start_frame: 2, end_frame: 5, audio_samples: 2000 }, { id: "b", start_frame: 8, end_frame: 10, audio_samples: 1600 }] };
  const clips = new Map([["a", new Int16Array(2000).fill(1234)], ["b", new Int16Array(1600).fill(2345)]]);
  const narration = buildNarration(timeline, clips);
  assert.equal(narration.length, 12 * SAMPLES_PER_FRAME);
  assert.ok(narration.subarray(0, 2 * SAMPLES_PER_FRAME).every((sample) => sample === 0));
  assert.equal(narration[2 * SAMPLES_PER_FRAME], 1234);
  assert.ok(narration.subarray(5 * SAMPLES_PER_FRAME, 8 * SAMPLES_PER_FRAME).every((sample) => sample === 0));
  assert.equal(narration[8 * SAMPLES_PER_FRAME], 2345);
  assert.ok(narration.subarray(10 * SAMPLES_PER_FRAME).every((sample) => sample === 0));
  assert.throws(() => buildNarration({ ...timeline, lines: [timeline.lines[0], { ...timeline.lines[1], start_frame: 4 }] }, clips), /overlaps/);
  assert.throws(() => buildNarration({ ...timeline, total_frames: 9 }, clips), /ends before/);
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

test("long-anime TTS measures directed action without empty synthesis and reuses words when its budget changes", async () => {
  const box = sandbox("fixture-drama", "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  Object.assign(doc, { category: "anime", production_policy: LONG_ANIME_POLICY, target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "original-anime", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false } });
  doc.look.preset = "anime-2d";
  for (const scene of doc.scenes) delete scene.data.fit;
  doc.scenes.splice(1, 0, { id: "silent-escape", template: "shot", action_seconds: 3, data: { prompt: "The girl jumps onto a collapsing stone bridge", motion: "stones shatter and fall into the river", characters: ["jingwei"] }, lines: [] });
  writeFileSync(file, JSON.stringify(doc));
  const saveSeries = () => writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ ...doc.series, category: doc.category, style_preset: doc.look.preset, production_policy: doc.production_policy, runtime_spec: doc.runtime_spec, target_minutes: 22, characters: doc.characters }));
  saveSeries();
  assert.deepEqual(lintProject(loadProject({ slug: box.slug, root: box.root })).errors, []);
  const server = fakeServer({ status: { gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 0 } });
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const run = () => capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  const initial = run();
  assert.equal(await main(["tts", "--slug", box.slug], initial.ctx), EXIT.ok, initial.out.stderr + initial.out.stdout);
  const posts = () => server.calls.filter((call) => call.url.endsWith("/api/video/speech"));
  const paidRequests = posts().length;
  assert.ok(paidRequests > 0, "all calls are local fake-provider fixtures");
  assert.ok(posts().every((call) => JSON.parse(call.init.body).segments.every((segment) => segment.parts.some((part) => part.text.trim()))));
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  const narration = requireNarrationFormat(parseWav(readFileSync(path.join(box.workdir, "narration.wav"))));
  assert.equal(timeline.timing_basis, "measured");
  assert.equal(narration.length, timeline.total_frames * SAMPLES_PER_FRAME);
  const action = timeline.actions[0];
  assert.equal(action.end_frame - action.start_frame, 90);
  assert.ok(narration.subarray(action.start_frame * SAMPLES_PER_FRAME, action.end_frame * SAMPLES_PER_FRAME).every((sample) => sample === 0));
  assert.equal(timeline.lines.some((line) => line.scene === "silent-escape"), false);
  assert.equal(existsSync(path.join(box.workdir, "audio", "silent-escape.wav")), false);
  doc.runtime_spec.op_ed_budget_seconds = 120;
  doc.runtime_spec.slot_reserve_seconds = 360;
  writeFileSync(file, JSON.stringify(doc));
  saveSeries();
  const again = run();
  assert.equal(await main(["tts", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(posts().length, paidRequests, "budget changes do not buy unchanged spoken clips again");
  const updated = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  assert.equal(updated.speech_hash, timeline.speech_hash);
  assert.notEqual(updated.runtime_policy_hash, timeline.runtime_policy_hash);
  assert.equal(updated.runtime_policy_hash, runtimePolicyHash(doc));
  assert.deepEqual(readFileSync(path.join(box.workdir, "narration.wav")), encodeWav(narration));
});

test("explicit repeated takes buy only the original, preserve bytes and independent CC timing, and retake as one family", async () => {
  const box = sandbox("fixture-drama", "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  const original = doc.scenes[1].lines[0];
  original.text = "父王，我回來了。";
  doc.pronunciation_hints = { 父王: "ㄈㄨˋ ㄨㄤˊ" };
  doc.scenes[3].lines = [
    { ...original, id: "copy1", audio_ref: original.id, pause_after_ms: 100 },
    { ...original, id: "copy2", audio_ref: original.id, pause_after_ms: 900 },
  ];
  writeFileSync(file, JSON.stringify(doc));
  const server = fakeServer({ status: { gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 0 } });
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const run = () => capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  const posts = () => server.calls.filter((call) => call.url.endsWith("/api/video/speech"));
  const initial = run();
  assert.equal(await main(["tts", "--slug", box.slug], initial.ctx), EXIT.ok, initial.out.stderr);
  assert.equal(posts().length, 5, "the two explicit repeats make no paid request");
  assert.equal(posts().filter((call) => JSON.parse(call.init.body).style?.includes("父王＝")).length, 1);
  const audioFile = (id) => path.join(box.workdir, "audio", `${id}.wav`);
  assert.deepEqual(readFileSync(audioFile("copy1")), readFileSync(audioFile(original.id)));
  assert.deepEqual(readFileSync(audioFile("copy2")), readFileSync(audioFile(original.id)));
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json")));
  const family = timeline.lines.filter((line) => [original.id, "copy1", "copy2"].includes(line.id));
  assert.equal(new Set(family.map((line) => line.audio_samples)).size, 1);
  assert.equal(new Set(family.map((line) => line.start_frame)).size, 3);
  const texts = Object.fromEntries(doc.scenes.flatMap((scene) => scene.lines.map((line) => [line.id, line.text])));
  const captions = buildCues(timeline, texts, "zh-TW").cues.filter((cue) => [original.id, "copy1", "copy2"].includes(cue.line));
  assert.equal(captions.length, 3);
  assert.ok(captions.every((cue) => !cue.text.includes("ㄈ")));
  assert.ok(captions[0].end_ms < captions[1].start_ms && captions[1].end_ms <= captions[2].start_ms);
  const cacheFile = path.join(box.workdir, "audio", "cache.json");
  const cache = JSON.parse(readFileSync(cacheFile));
  assert.equal(cache.references.copy1.source, original.id);
  assert.equal(cache.references.copy1.source_sha256, cache.sha256[original.id]);
  const again = run();
  assert.equal(await main(["tts", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(posts().length, 5);

  const flags = path.join(box.work, "flags.json");
  writeFileSync(flags, JSON.stringify({ flags: ["copy2"] }));
  const retake = run();
  assert.equal(await main(["tts", "--slug", box.slug, "--redo", flags], retake.ctx), EXIT.ok, retake.out.stderr);
  assert.equal(posts().length, 6, "a flagged replay retakes its one original, never its own new variant");
  assert.deepEqual(readFileSync(audioFile("copy2")), readFileSync(audioFile(original.id)));

  // A corrupted source blocks the entire next run before an unrelated changed line is paid for.
  doc.scenes[0].lines[0].text += "真的。";
  writeFileSync(file, JSON.stringify(doc));
  const good = readFileSync(audioFile(original.id));
  const corrupt = Buffer.from(good); corrupt[corrupt.length - 1] ^= 1;
  writeFileSync(audioFile(original.id), corrupt);
  const failed = run();
  assert.notEqual(await main(["tts", "--slug", box.slug], failed.ctx), EXIT.ok);
  assert.match(failed.out.stderr, /matching saved WAV SHA256/);
  assert.equal(posts().length, 6);
  writeFileSync(audioFile(original.id), good);
  const oldCache = JSON.parse(readFileSync(cacheFile)); delete oldCache.sha256[original.id];
  writeFileSync(cacheFile, JSON.stringify(oldCache));
  const legacy = run();
  assert.notEqual(await main(["tts", "--slug", box.slug], legacy.ctx), EXIT.ok);
  assert.match(legacy.out.stderr, /explicitly retake/);
  assert.equal(posts().length, 6);
});

test("same-duration exact-take retakes invalidate listening approval; legacy evidence refresh is offline and cannot buy a missing take", async () => {
  const box = sandbox("fixture-drama", "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file));
  const original = doc.scenes[1].lines[0];
  doc.scenes[3].lines = [{ ...original, id: "copy1", audio_ref: original.id }];
  writeFileSync(file, JSON.stringify(doc));
  let gain = 1;
  const server = fakeServer({ status: { gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 0 }, gain: () => gain });
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const ctx = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl }).ctx;
  assert.equal(await main(["tts", "--slug", box.slug], ctx), EXIT.ok);
  const places = { gate: "audio", docDir: box.dir, workdir: box.workdir };
  await approve(places);
  const timelineFile = path.join(box.workdir, "timeline.json");
  const before = JSON.parse(readFileSync(timelineFile));
  gain = 0.75;
  const flags = path.join(box.work, "flags.json");
  writeFileSync(flags, JSON.stringify({ flags: ["copy1"] }));
  assert.equal(await main(["tts", "--slug", box.slug, "--redo", flags], ctx), EXIT.ok);
  const after = JSON.parse(readFileSync(timelineFile));
  assert.equal(after.total_frames, before.total_frames);
  assert.equal(after.speech_hash, before.speech_hash);
  assert.notEqual(after.audio_evidence.narration_sha256, before.audio_evidence.narration_sha256);
  assert.equal(after.lines.find((line) => line.id === "copy1").audio_sha256, after.lines.find((line) => line.id === original.id).audio_sha256);
  assert.equal((await approvalState(places)).status, "stale");
  // A legacy review is bound to an unverified timeline: refresh keeps WAVs and requires a new review.
  delete after.audio_evidence;
  for (const line of after.lines) delete line.audio_sha256;
  writeFileSync(timelineFile, JSON.stringify(after));
  const offline = capture({ root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, fetch: () => { throw new Error("offline refresh contacted server"); } });
  assert.equal(await main(["tts", "--slug", box.slug, "--refresh-evidence"], offline.ctx), EXIT.ok, offline.out.stderr);
  assert.equal((await approvalState(places)).status, "stale");
  const cacheFile = path.join(box.workdir, "audio", "cache.json");
  const cache = JSON.parse(readFileSync(cacheFile)); delete cache.lines[original.id];
  writeFileSync(cacheFile, JSON.stringify(cache));
  assert.equal(await main(["tts", "--slug", box.slug, "--refresh-evidence"], offline.ctx), EXIT.usage);
  assert.match(offline.out.stderr, /never synthesizes/);
});

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

  // A cache from before clips had their own keys holds the request key; it still counts, and is
  // rewritten to the clip's key so the edit below keeps the rest of the scene.
  const cacheFile = path.join(box.workdir, "audio", "cache.json");
  const requestKeys = Object.fromEntries(planRequests(JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8")), fixtureLexicon()).flatMap((request) => request.lines.map((line) => [line.id, request.key])));
  writeFileSync(cacheFile, JSON.stringify({ lines: requestKeys }));
  const second = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  await main(["tts", "--slug", box.slug], second.ctx);
  assert.equal(server.calls.filter((call) => call.url.endsWith("/api/video/speech")).length, synthesized, "nothing to redo");
  assert.notDeepEqual(JSON.parse(readFileSync(cacheFile, "utf8")).lines, requestKeys, "old keys rewritten");

  const file = path.join(box.dir, "video.json");
  writeFileSync(file, readFileSync(file, "utf8").replace("第二個問題是", "第二個問題則是"));
  const third = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  await main(["tts", "--slug", box.slug], third.ctx);
  const speech = server.calls.filter((call) => call.url.endsWith("/api/video/speech"));
  assert.equal(speech.length, synthesized + 1, "only the changed scene");
  assert.equal(JSON.parse(speech.at(-1).init.body).segments.length, 1, "and in it only the changed line");

  const status = capture({ root: box.root, env, home: box.base });
  await main(["status", "--slug", box.slug], status.ctx);
  assert.match(status.out.stdout, /\[x\] narration synthesized/);
});

test("tts --redo retakes only the flagged line and keeps the rest of its scene", async () => {
  const box = sandbox();
  const server = fakeServer();
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const first = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  const scene = timeline.lines.find((line, index, all) => all.filter((other) => other.scene === line.scene).length > 1).scene;
  const [kept, flagged] = timeline.lines.filter((line) => line.scene === scene);
  const clip = (id) => readFileSync(path.join(box.workdir, "audio", `${id}.wav`));
  const keptBefore = clip(kept.id);
  const speechCalls = () => server.calls.filter((call) => call.url.endsWith("/api/video/speech"));
  const before = speechCalls().length;

  const flags = path.join(box.work, "flags.json");
  writeFileSync(flags, JSON.stringify({ flags: [flagged.id] }));
  const redo = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug, "--redo", flags], redo.ctx), EXIT.ok, redo.out.stderr);
  const retakes = speechCalls().slice(before);
  assert.equal(retakes.length, 1, "one request, for the flagged line alone");
  assert.equal(JSON.parse(retakes[0].init.body).segments.length, 1);
  assert.match(redo.out.stdout, /1 of \d+ lines retaken/);
  assert.deepEqual(clip(kept.id), keptBefore, "the line that passed keeps its take");

  const again = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  await main(["tts", "--slug", box.slug], again.ctx);
  assert.equal(speechCalls().length, before + 1, "the retake counts as current afterwards");
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

test("tts on a drama gives each speaker their voice, and names the character whose voice the site lacks", async () => {
  const box = sandbox("fixture-drama", "drama");
  const server = fakeServer({ status: { gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 1000 } });
  const env = { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" };
  const dry = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  assert.match(dry.out.stdout, /^7 requests, 7 to synthesize;/m);
  assert.match(dry.out.stdout, /^voices: gemini:Sulafat \d+ characters \(narrator\); gemini:Kore \d+ characters \(jingwei \(精衛\)\); gemini:Charon \d+ characters \(yandi \(炎帝\)\)$/m);
  assert.match(dry.out.stdout, /^server: voice gemini:Sulafat ready; voice gemini:Kore ready; voice gemini:Charon ready; gemini: 299000 characters left this month$/m);

  const run = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  const bodies = server.calls.filter((call) => call.url.endsWith("/api/video/speech")).map((call) => JSON.parse(call.init.body));
  assert.deepEqual(
    bodies.map((body) => body.voice),
    ["gemini:Sulafat", "gemini:Kore", "gemini:Charon", "gemini:Sulafat", "gemini:Sulafat", "gemini:Kore", "gemini:Sulafat"],
  );
  assert.equal(bodies[1].style, "清亮、倔強的少女聲，標準國語，咬字清楚，台北人平常說話的語調。開心、有點急", "the retired accent wording leaves with the request");
  assert.equal(bodies[2].style, "低沉、緩慢的長者聲，標準國語，咬字清楚，台北人平常說話的語調。溫和但擔心");
  assert.equal(bodies[3].style, "沉穩的說書人語氣，標準國語，咬字清楚，台北人平常說話的語調，語速稍慢", "the narrator's own words stay");
  assert.match(run.out.stdout, /^farewell#1 \[yandi \(炎帝\)\]: 1 lines$/m);
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  assert.equal(timeline.lines.find((line) => line.id === "x9fe").speaker, "jingwei");
  assert.equal(timeline.lines.length, 10);
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.deepEqual(state.runs.at(-1).voices, ["gemini:Sulafat", "gemini:Kore", "gemini:Charon"]);

  // Editing one character's line retakes that line alone, with that character's voice.
  const file = path.join(box.dir, "video.json");
  writeFileSync(file, readFileSync(file, "utf8").replace("早點回來。", "早些回來。"));
  const edited = capture({ root: box.root, env, home: box.base, fetch: server.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], edited.ctx), EXIT.ok, edited.out.stderr);
  const retakes = server.calls.filter((call) => call.url.endsWith("/api/video/speech")).slice(bodies.length).map((call) => JSON.parse(call.init.body));
  assert.equal(retakes.length, 1);
  assert.equal(retakes[0].voice, "gemini:Charon");

  // A character voiced by an Azure voice the admin card does not allow stops tts, naming the character.
  const azure = JSON.parse(readFileSync(file, "utf8"));
  azure.characters[1].voice = { provider: "azure", name: "zh-TW-YunJheNeural" };
  writeFileSync(file, JSON.stringify(azure));
  const strict = fakeServer({ status: { gemini_configured: true, voices: ["zh-TW-HsiaoChenNeural"] } });
  const refused = capture({ root: box.root, env, home: box.base, fetch: strict.fetchImpl });
  assert.equal(await main(["tts", "--slug", box.slug], refused.ctx), EXIT.owner);
  assert.match(refused.out.stderr, /voice zh-TW-YunJheNeural is not on the admin card's allowlist \(spoken by yandi \(炎帝\)\)/);
  assert.equal(strict.calls.filter((call) => call.url.endsWith("/api/video/speech")).length, 0, "nothing synthesized");
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
