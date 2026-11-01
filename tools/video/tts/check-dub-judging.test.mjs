// check-audio's judging of dubs and its second-opinion failures (ticket
// 2026-10-09-dub-skipped-because-jev-still-hears, measured 2026-11-01). Kept apart from
// check.test.mjs, which the long-form duration review binds byte for byte.
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, spokenText, textHash } from "../core/schema.mjs";
import { SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { concatSamples, encodeWav } from "./wav.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"t".repeat(43)}`;
const sine = (rate, hz, seconds) => Int16Array.from({ length: Math.round(rate * seconds) }, (_, index) => Math.round(8000 * Math.sin((2 * Math.PI * hz * index) / rate)));

/** A site that synthesizes tones, transcribes clips in narration order, and judges with Jev. */
function site({ heardFor, noul }) {
  const calls = { transcribe: 0, judge: [], judgeTracks: [] };
  const tone = (milliseconds) => sine(SAMPLE_RATE, 440, milliseconds / 1000);
  const quiet = (milliseconds) => new Int16Array(Math.round((milliseconds / 1000) * SAMPLE_RATE));
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/speech/status")) {
      return Response.json({ configured: true, region: "eastasia", voices: ["zh-TW-HsiaoChenNeural"], output_format: "riff-48khz-16bit-mono-pcm", max_request_characters: 1500, monthly_limit: 0, used: 0, remaining: null });
    }
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      calls.transcribe += 1;
      return Response.json({ text: heardFor(calls.transcribe - 1) });
    }
    if (url.endsWith("/speech/judge")) {
      calls.judge.push(body.lines);
      calls.judgeTracks.push(body.track);
      return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: noul(line) })) });
    }
    if (url.endsWith("/speech/align")) return new Response("not found", { status: 404 });
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 200), quiet(segment.break_after_ms)]));
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

/** A dub track of the fixture, its clips already recorded. */
function writeDub(box, locale, texts) {
  const lines = [...eachLine(fixture())];
  const translation = { locale, lines: Object.fromEntries(lines.map(({ line }) => [line.id, { source_hash: textHash(line.text), text: texts[line.id] }])) };
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translation));
  const audioDir = path.join(box.workdir, "dubs", locale, "audio");
  mkdirSync(audioDir, { recursive: true });
  const timeline = { locale, speech_hash: "speech0000000000", translation_hash: "translation00000", total_frames: 0, lines: [] };
  for (const { scene, line } of lines) {
    const samples = sine(SAMPLE_RATE, 440, 0.3);
    writeFileSync(path.join(audioDir, `${line.id}.wav`), encodeWav(samples));
    const frames = Math.ceil(samples.length / SAMPLES_PER_FRAME) + 9;
    timeline.lines.push({ id: line.id, scene: scene.id, start_frame: timeline.total_frames, end_frame: timeline.total_frames + frames, audio_samples: samples.length, tempo: 1 });
    timeline.total_frames += frames;
  }
  writeFileSync(path.join(box.workdir, "dubs", locale, "timeline.json"), JSON.stringify(timeline));
  return timeline;
}

test("a dub is judged on what the line says; the narration word for word, the server's default", async () => {
  const box = sandbox();
  const ids = [...eachLine(fixture())].map(({ line }) => line.id);
  const texts = Object.fromEntries(ids.map((id, index) => [id, `Line number ${index + 1} costs US$ 250.`]));
  writeDub(box, "pt", texts);
  // The voice reads the currency sign as its name (daily-ai-20261029 pt mby2).
  const heardFor = (count) => (count === 1 ? "Line number 2 costs 250 dollars." : texts[ids[count % ids.length]]);
  const server = site({ heardFor, noul: () => 0.9 });
  const dub = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "pt"], dub.ctx), EXIT.ok, dub.out.stdout);
  assert.deepEqual(server.calls.judgeTracks, ["dub"], "checking.py DUB_JUDGE_INSTRUCTIONS");

  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const narrationServer = site({ heardFor: (count) => (count === 2 ? spokenText(lines[2]).slice(0, 4) : spokenText(lines[count % lines.length])), noul: () => 0.9 });
  const plain = sandbox();
  assert.equal(await main(["tts", "--slug", plain.slug], context(plain, narrationServer.fetchImpl).ctx), EXIT.ok);
  const narration = context(plain, narrationServer.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", plain.slug], narration.ctx), EXIT.ok, narration.out.stdout);
  assert.deepEqual(narrationServer.calls.judgeTracks, [undefined], "no track field for the narration");
});

test("doubts no second transcriber has heard wait for it when it fails, instead of standing as misreadings", async () => {
  const box = sandbox();
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  const misheard = lines[2];
  const heardFor = (count) => {
    const line = lines[count % lines.length];
    return line === misheard ? spokenText(line).slice(0, 4) : spokenText(line);
  };
  const server = site({ heardFor, noul: (question) => (question.heard === question.intended ? 0.9 : 0.1) });
  assert.equal(await main(["tts", "--slug", box.slug], context(box, server.fetchImpl).ctx), EXIT.ok);

  // The transcriber is configured but fails (2026-10-19..24 on the host): the run ends as a vendor away.
  const broken = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--second-opinion", `${process.execPath} ${path.join(box.base, "missing.mjs")}`], broken.ctx), EXIT.external);
  assert.match(broken.out.stdout, /1 doubted lines wait for the second transcriber, which failed \(.+\); run check-audio again later/);
  const transcribed = server.calls.transcribe;

  // It answers on the next run: the cached Gemini transcript is not bought again, and the line clears.
  const script = path.join(box.base, "second.mjs");
  writeFileSync(script, [
    'import path from "node:path";',
    "const [, ...files] = process.argv.slice(2);",
    `const canned = ${JSON.stringify({ [`${misheard.id}.wav`]: spokenText(misheard) })};`,
    'for (const file of files) console.log(`${path.basename(file)} ${canned[path.basename(file)] ?? ""}`);',
  ].join("\n"));
  const fixed = context(box, server.fetchImpl);
  assert.equal(await main(["check-audio", "--slug", box.slug, "--second-opinion", `${process.execPath} ${script}`], fixed.ctx), EXIT.ok, fixed.out.stdout);
  assert.match(fixed.out.stdout, /1 cleared by a second transcript, 0 flagged/);
  assert.equal(server.calls.transcribe, transcribed, "nothing transcribed again");

  // Without a transcriber configured at all, a doubt still stands as it always did.
  const fresh = sandbox();
  assert.equal(await main(["tts", "--slug", fresh.slug], context(fresh, server.fetchImpl).ctx), EXIT.ok);
  assert.equal(await main(["check-audio", "--slug", fresh.slug], context(fresh, server.fetchImpl).ctx), EXIT.lint);
});
