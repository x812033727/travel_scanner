import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, spokenText } from "../core/schema.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { comparable, matches, spokenForm } from "./check.mjs";
import { concatSamples, downsample, encodeWav } from "./wav.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const sine = (rate, hz, seconds) => Int16Array.from({ length: Math.round(rate * seconds) }, (_, index) => Math.round(8000 * Math.sin((2 * Math.PI * hz * index) / rate)));
const rms = (samples, from = 0, to = samples.length) => {
  let sum = 0;
  for (let index = from; index < to; index++) sum += samples[index] ** 2;
  return Math.sqrt(sum / (to - from));
};

test("comparison ignores punctuation, spacing and case, and knows the dictionary's spoken forms", () => {
  assert.equal(comparable("用 AI 挑模型，對吧？"), comparable("用ai挑模型對吧"));
  const lexicon = { schema_version: 1, terms: { AI: "A I", LLM: "L L M" } };
  const line = { id: "k7p2", text: "用 AI 挑模型。" };
  assert.equal(spokenForm(line, lexicon), "用 A I 挑模型。");
  assert.ok(matches("用AI挑模型", line, lexicon));
  assert.ok(matches("用 A I 挑模型", line, lexicon));
  assert.ok(!matches("用 AI 調模型", line, lexicon));
  const said = { id: "p5vs", text: "2026/9/24 上架", say: "二〇二六年九月二十四日上架", say_for: "x" };
  assert.ok(matches("二〇二六年九月二十四日上架", said, lexicon));
});

test("downsampling keeps what 16 kHz can carry and removes what it cannot", () => {
  const low = downsample(sine(48_000, 1000, 0.1), 3);
  const ideal = sine(16_000, 1000, 0.1);
  assert.equal(low.length, ideal.length);
  let worst = 0;
  for (let index = 100; index < low.length - 100; index++) worst = Math.max(worst, Math.abs(low[index] - ideal[index]));
  assert.ok(worst <= 16, `largest error ${worst} of 8000`);
  // 12 kHz is above the new 8 kHz Nyquist frequency: it must not fold back as a 4 kHz tone.
  const aliased = downsample(sine(48_000, 12_000, 0.1), 3);
  assert.ok(rms(aliased, 100, aliased.length - 100) < 0.02 * rms(sine(48_000, 12_000, 0.1)));
});

/** A site that synthesizes tones, transcribes clips in narration order, and judges with Jev. */
function site({ heardFor, noul }) {
  const calls = { speech: 0, transcribe: [], judge: [] };
  const tone = (milliseconds) => sine(SAMPLE_RATE, 440, milliseconds / 1000);
  const quiet = (milliseconds) => new Int16Array(Math.round((milliseconds / 1000) * SAMPLE_RATE));
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/speech/status")) {
      return Response.json({ configured: true, region: "eastasia", voices: ["zh-TW-HsiaoChenNeural"], output_format: "riff-48khz-16bit-mono-pcm", max_request_characters: 1500, monthly_limit: 0, used: 0, remaining: null });
    }
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      const wav = Buffer.from(body.audio, "base64");
      assert.equal(wav.readUInt32LE(24), 16_000, "clips go out at 16 kHz");
      calls.transcribe.push(wav.length);
      return Response.json({ text: heardFor(calls.transcribe.length - 1) });
    }
    if (url.endsWith("/speech/judge")) {
      calls.judge.push(body.lines);
      return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: noul(line) })) });
    }
    calls.speech += 1;
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60), quiet(segment.break_after_ms)]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { calls, fetchImpl };
}

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-24T05:00:00Z"),
      sleep: async () => {},
    },
  };
}

test("check-audio flags only the line Jev doubts, writes a redo file, and reuses its work", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const lexicon = fixtureLexicon();
  const wrong = lines[2].id;
  // Line 0 comes back in the spoken form, line 1 without punctuation, line 2 with a word missing.
  const heardFor = (count) => {
    const index = count % lines.length;
    if (index === 0) return spokenForm(lines[0], lexicon);
    if (index === 1) return spokenText(lines[1]).replace(/[，。？、]/g, "");
    if (index === 2) return spokenText(lines[2]).slice(0, 4);
    return spokenText(lines[index]);
  };
  const server = site({ heardFor, noul: (line) => (line.id === wrong ? 0.08 : 0.95) });

  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);

  const first = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], first.ctx), EXIT.lint, first.out.stderr);
  assert.equal(server.calls.transcribe.length, lines.length);
  assert.equal(server.calls.judge.length, 1, "one Jev call for the one scene with a difference");
  assert.deepEqual(server.calls.judge[0].map((line) => line.id), [wrong]);
  const flags = JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.json"), "utf8"));
  assert.deepEqual(flags.flags, [wrong]);
  assert.match(flags.notes[wrong], /Jev 0\.08/);
  assert.match(first.out.stdout, new RegExp(`${lines.length} lines: ${lines.length - 1} match`));
  assert.match(first.out.stdout, /--redo/);

  const again = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug], again.ctx), EXIT.lint);
  assert.equal(server.calls.transcribe.length, lines.length, "unchanged clips are not transcribed again");
  assert.equal(server.calls.judge.length, 1, "judged lines are not asked again");

  const forced = context(box, server.fetchImpl);
  await main(["check-audio", "--slug", box.slug, "--force"], forced.ctx);
  assert.equal(server.calls.transcribe.length, lines.length * 2);
});
