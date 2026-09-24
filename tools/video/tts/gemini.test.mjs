import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { validateVideo } from "../core/schema.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { billableForRequest, geminiText, planRequests, voiceFields } from "./requests.mjs";
import { encodeWav, parseWav, toNarrationRate, upsample } from "./wav.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const sine = (rate, hz, seconds, amplitude = 8000) =>
  Int16Array.from({ length: Math.round(rate * seconds) }, (_, index) => Math.round(amplitude * Math.sin((2 * Math.PI * hz * index) / rate)));

test("upsampling keeps every original sample and fills the rest with the band-limited curve", () => {
  const source = sine(24_000, 1000, 0.1);
  const doubled = upsample(source, 2);
  assert.equal(doubled.length, source.length * 2);
  for (let index = 0; index < source.length; index++) assert.equal(doubled[index * 2], source[index]);
  // Away from the edges the new samples sit on the same 1 kHz sine sampled at 48 kHz.
  const ideal = sine(48_000, 1000, 0.1);
  let worst = 0;
  for (let index = 200; index < doubled.length - 200; index++) worst = Math.max(worst, Math.abs(doubled[index] - ideal[index]));
  assert.ok(worst <= 8, `largest error ${worst} of 8000`);
  assert.deepEqual([...upsample(new Int16Array(64), 3)], new Array(192).fill(0));
  assert.throws(() => upsample(source, 1.5));
});

test("a 24 kHz clip from the server comes out on the 48 kHz grid; a 48 kHz one is untouched", () => {
  const narrow = encodeWav(sine(24_000, 440, 0.05), 24_000);
  const wide = parseWav(toNarrationRate(narrow));
  assert.equal(wide.sampleRate, SAMPLE_RATE);
  assert.equal(wide.samples.length, 2400);
  const native = encodeWav(sine(48_000, 440, 0.05));
  assert.equal(toNarrationRate(native), native);
  const odd = encodeWav(sine(22_050, 440, 0.05), 22_050);
  assert.equal(parseWav(toNarrationRate(odd)).sampleRate, 22_050, "left for requireNarrationFormat to refuse");
});

test("voice fields: Azure gets a name and a rate, Gemini a prefixed voice, a style and a model", () => {
  assert.deepEqual(voiceFields({ provider: "azure", name: "zh-TW-HsiaoChenNeural", rate: "+5%" }), { voice: "zh-TW-HsiaoChenNeural", rate: "+5%" });
  assert.deepEqual(voiceFields({ provider: "azure", name: "zh-TW-YunJheNeural" }), { voice: "zh-TW-YunJheNeural", rate: "+0%" });
  assert.deepEqual(voiceFields({ provider: "gemini", name: "Sulafat", style: "relaxed", model: "gemini-3.8-flash-lite-tts" }), {
    voice: "gemini:Sulafat",
    style: "relaxed",
    model: "gemini-3.8-flash-lite-tts",
  });
  assert.deepEqual(voiceFields({ provider: "gemini", name: "Kore" }), { voice: "gemini:Kore" });
});

test("the Gemini transcript matches the server's, and it is what the month counts", () => {
  const segments = [
    { parts: [{ text: "用 " }, { text: "LLM", alias: "L L M" }, { text: " 算 <laugh>" }], break_after_ms: 800 },
    { parts: [{ text: "下一句" }], break_after_ms: 300 },
    { parts: [{ text: "最後一句" }], break_after_ms: 0 },
  ];
  // The same case as test_the_transcript_uses_spoken_forms_and_pause_tags_and_drops_angle_brackets.
  assert.equal(geminiText(segments), "用 L L M 算  laugh  <long pause> 下一句 <short pause> 最後一句");
  assert.equal(billableForRequest({ voice: "gemini:Kore", segments }), geminiText(segments).length);
});

test("a video can name a Gemini voice, and planned requests carry its style instead of a rate", () => {
  const doc = fixture();
  doc.voice = { provider: "gemini", name: "Sulafat", style: "relaxed, like explaining to a friend" };
  assert.deepEqual(validateVideo(doc), []);
  const [request] = planRequests(doc, { schema_version: 1, terms: {} });
  assert.equal(request.body.voice, "gemini:Sulafat");
  assert.equal(request.body.style, "relaxed, like explaining to a friend");
  assert.equal("rate" in request.body, false);

  const paths = (voice) => validateVideo({ ...fixture(), voice }).map((error) => error.path);
  assert.deepEqual(paths({ provider: "gemini", name: "Sulafat", rate: "+5%" }), ["voice.rate"]);
  assert.deepEqual(paths({ provider: "gemini", name: "gemini:Sulafat" }), ["voice.name"]);
  assert.deepEqual(paths({ provider: "gemini", name: "Kore", model: "gemini-9-tts" }), ["voice.model"]);
  assert.deepEqual(paths({ provider: "azure", name: "zh-TW-HsiaoChenNeural", style: "calm" }), ["voice"]);
});

test("audition asks the server for Gemini voices with the style and saves 48 kHz clips", async () => {
  const box = sandbox();
  const bodies = [];
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/api/video/speech/status")) {
      return Response.json({
        configured: false,
        region: null,
        voices: [],
        output_format: "riff-48khz-16bit-mono-pcm",
        max_request_characters: 1500,
        monthly_limit: 450000,
        used: 0,
        remaining: 450000,
        gemini_configured: true,
        gemini_models: ["gemini-3.8-flash-tts"],
        gemini_voices: ["gemini:Sulafat"],
        gemini_monthly_limit: 300000,
        gemini_used: 0,
      });
    }
    bodies.push(JSON.parse(init.body));
    return new Response(encodeWav(sine(24_000, 220, 0.5), 24_000), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "20" } });
  };
  const sample = path.join(box.base, "sample.txt");
  writeFileSync(sample, "排行榜第一名，不一定最適合你。");
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: box.base,
    fetch: fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-09-24T05:00:00Z"),
    sleep: async () => {},
  };
  const args = ["audition", "--text-file", sample, "--voices", "gemini:Sulafat,gemini:Achird", "--style", "relaxed"];
  assert.equal(await main(args, ctx), EXIT.ok, out.stderr);
  assert.deepEqual(
    bodies.map((body) => [body.voice, body.style, "rate" in body]),
    [
      ["gemini:Sulafat", "relaxed", false],
      ["gemini:Achird", "relaxed", false],
    ],
  );
  const clip = /gemini:Sulafat: (.+\.wav)/.exec(out.stdout)[1];
  assert.equal(path.basename(clip), "gemini-Sulafat.wav");
  assert.equal(parseWav(readFileSync(clip)).sampleRate, SAMPLE_RATE);

  // An Azure voice still needs the Azure card, which this server does not have.
  out.stderr = "";
  assert.equal(await main(["audition", "--text-file", sample, "--voices", "zh-TW-HsiaoChenNeural"], ctx), EXIT.owner);
  assert.match(out.stderr, /Azure/);
});
