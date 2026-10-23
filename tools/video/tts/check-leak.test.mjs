import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { LEAKED_WORDS, leakedWord } from "./check.mjs";
import { encodeWav } from "./wav.mjs";

// Kept out of check.test.mjs, which the long-form duration review binds by hash.

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"t".repeat(43)}`;
const line = (text) => ({ id: "x", text });

test("a transcript that opens with a leaked word names it, glued to the sentence or on its own line", () => {
  assert.deepEqual(LEAKED_WORDS, ["thought"]);
  // The two transcripts of 2026-10-15 (H05 h5v109 and an H06 line).
  assert.equal(leakedWord("thoughtIt proves the ransom, not the man.", line("It proves the ransom, not the man.")), "thought");
  assert.equal(leakedWord("thought\nResearchers did not name the children by sight alone.", line("Researchers did not name the children by sight alone.")), "thought");
  assert.equal(leakedWord("Thought. The ship was found.", line("The ship was found.")), "Thought");
  assert.equal(leakedWord("  thought the ship was found", line("The ship was found.")), "thought");
});

test("a line that really starts with the word, or a longer word, is no leak", () => {
  assert.equal(leakedWord("Thought experiments came later.", line("Thought experiments came later.")), null);
  assert.equal(leakedWord("thought experiments came later", line("“Thought experiments” came later.")), null);
  assert.equal(leakedWord("Thoughtful readers asked why.", line("Thoughtful readers asked why.")), null);
  assert.equal(leakedWord("The ship was found.", line("The ship was found.")), null);
  assert.equal(leakedWord("", line("The ship was found.")), null);
});

function writeDub(box, locale, texts) {
  const lines = [...eachLine(fixture())];
  const translation = { locale, lines: Object.fromEntries(lines.map(({ line: each }) => [each.id, { source_hash: textHash(each.text), text: texts[each.id] }])) };
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translation));
  const audioDir = path.join(box.workdir, "dubs", locale, "audio");
  mkdirSync(audioDir, { recursive: true });
  const timeline = { locale, speech_hash: "speech0000000000", translation_hash: "translation00000", total_frames: 0, lines: [] };
  for (const { scene, line: each } of lines) {
    const samples = Int16Array.from({ length: Math.round(SAMPLE_RATE * 0.3) }, (_, index) => Math.round(8000 * Math.sin((2 * Math.PI * 440 * index) / SAMPLE_RATE)));
    writeFileSync(path.join(audioDir, `${each.id}.wav`), encodeWav(samples));
    const frames = Math.ceil(samples.length / SAMPLES_PER_FRAME) + 9;
    timeline.lines.push({ id: each.id, scene: scene.id, start_frame: timeline.total_frames, end_frame: timeline.total_frames + frames, audio_samples: samples.length, tempo: 1 });
    timeline.total_frames += frames;
  }
  writeFileSync(path.join(box.workdir, "dubs", locale, "timeline.json"), JSON.stringify(timeline));
}

test("check-audio flags a dub line whose clip opens with a leaked word even when Jev passes it, and dub --redo gets it", async () => {
  const box = sandbox();
  const ids = [...eachLine(fixture())].map(({ line: each }) => each.id);
  const texts = Object.fromEntries(ids.map((id, index) => [id, `Line ${index + 1} of the English dub says what it means.`]));
  const glued = ids[1], ownLine = ids[3], real = ids[4];
  texts[real] = "Thought experiments came later, the record says.";
  writeDub(box, "en", texts);
  const heard = {
    [glued]: `thought${texts[glued]}`,
    [ownLine]: `thought\n${texts[ownLine]}`,
    [real]: texts[real].toLowerCase(),
  };
  const judged = [];
  let transcribed = 0;
  const fetchImpl = async (url, init) => {
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      const id = ids[transcribed++ % ids.length];
      return Response.json({ text: heard[id] ?? texts[id] });
    }
    if (url.endsWith("/speech/judge")) {
      judged.push(...body.lines.map((each) => each.id));
      return Response.json({ results: body.lines.map((each) => ({ id: each.id, noul: 0.95 })) });
    }
    throw new Error(`unexpected request ${url}`);
  };
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: box.base,
    fetch: fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-10-16T05:00:00Z"),
    sleep: async () => {},
  };
  assert.equal(await main(["check-audio", "--slug", box.slug, "--locale", "en"], ctx), EXIT.lint, out.stderr);
  assert.deepEqual(judged.sort(), [glued, ownLine].sort(), "Jev was asked about both leaked lines and passed them");

  const flags = JSON.parse(readFileSync(path.join(box.workdir, "review", "check-flags.en.json"), "utf8"));
  assert.deepEqual(flags.flags, [glued, ownLine], "the leaks are flagged in line order; the line that starts with Thought is not");
  assert.match(flags.notes[glued], /^leaked word 「thought」 before the line \(Jev 0\.95\): heard 「thought/);
  assert.match(flags.notes[ownLine], /leaked word 「thought」/);
  assert.match(out.stdout, /0 judged fine by Jev, 2 flagged \(below 0\.5, 2 of them for a leaked word\)/);
  assert.match(out.stdout, new RegExp(`${glued}  leaked word 「thought」, Jev 0\\.95`));
  assert.match(out.stdout, new RegExp(`dub --slug ${box.slug} --locale en --redo`));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.equal(state.runs.at(-1).flagged, 2);
  assert.equal(state.runs.at(-1).leaked, 2);
});
