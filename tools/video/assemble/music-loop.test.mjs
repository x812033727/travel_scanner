import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { mixHash } from "../core/drama.mjs";
import { dramaFixture, fixtureLexicon, illustratedFixture, sandbox, writeAudioFixture } from "../core/fixtures/load.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { estimateTimeline, FPS, speechHash, visualHash } from "../core/timeline.mjs";
import { EXIT } from "../cli.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "./ffmpeg.mjs";
import { run as assemble } from "./cli.mjs";
import { musicInputs } from "./sound.mjs";
import { decodedMusicSeconds } from "../media/music.mjs";

process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

async function musicTestTool(t) {
  try { return await locateFfmpeg(); }
  catch (error) { if (error instanceof ToolMissing) { t.skip(error.message); return null; } throw error; }
}

test("assembly holds a short generated track, accepts sufficient measured audio, and refuses stale evidence", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const dir = mkdtempSync(path.join(tmpdir(), "music-loop-"));
  try {
    mkdirSync(path.join(dir, "music"));
    const file = path.join(dir, "music", "bed.mp3");
    const { ffmpeg } = tools;
    await runTool(ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=330:duration=2", "-c:a", "libmp3lame", file]);
    const actual = await decodedMusicSeconds(file);
    const doc = dramaFixture();
    const sha256 = createHash("sha256").update(readFileSync(file)).digest("hex");
    const manifestFile = path.join(dir, "music", "manifest.json");
    const manifest = { mix_hash: mixHash(doc), source: "generated", file: "music/bed.mp3", sha256, requested_seconds: 10, actual_seconds: actual, duration_measurement: "ffmpeg_full_decode" };
    writeFileSync(manifestFile, JSON.stringify(manifest));

    const short = await musicInputs(doc, dir, dir, { requiredSeconds: 5 });
    assert.match(short.problem, /shorter than the 5\.000 s cut/);
    assert.match(short.problem, /explicit checked loop/);
    assert.match((await musicInputs(doc, dir, dir, { requiredSeconds: actual + 0.01 })).problem, /shorter than/);
    assert.equal((await musicInputs(doc, dir, dir, { requiredSeconds: 1 })).track.file, file);
    assert.match((await musicInputs(doc, dir, dir)).problem, /no current cut length/);
    mkdirSync(path.dirname(path.join(dir, ARTIFACTS.timeline)), { recursive: true });
    writeFileSync(path.join(dir, ARTIFACTS.timeline), JSON.stringify({ total_frames: 5 * FPS }));
    assert.match((await musicInputs(doc, dir, dir)).problem, /shorter than the 5\.000 s cut/);
    writeFileSync(path.join(dir, ARTIFACTS.timeline), JSON.stringify({ total_frames: FPS }));
    assert.equal((await musicInputs(doc, dir, dir)).track.file, file);

    writeFileSync(manifestFile, JSON.stringify({ ...manifest, mix_hash: null, requested_mix_hash: mixHash(doc), duration_hold: true }));
    assert.match((await musicInputs(doc, dir, dir, { requiredSeconds: 1 })).problem, /duration hold/);

    writeFileSync(manifestFile, JSON.stringify({ ...manifest, actual_seconds: undefined }));
    assert.match((await musicInputs(doc, dir, dir, { requiredSeconds: 1 })).problem, /no fully decoded actual duration/);
    assert.match((await musicInputs(doc, dir, dir)).problem, /no fully decoded actual duration/);
    writeFileSync(manifestFile, JSON.stringify({ ...manifest, sha256: undefined }));
    assert.match((await musicInputs(doc, dir, dir, { requiredSeconds: 1 })).problem, /no SHA-256 binding/);
    writeFileSync(manifestFile, JSON.stringify(manifest));
    writeFileSync(file, "changed bytes");
    assert.match((await musicInputs(doc, dir, dir, { requiredSeconds: 1 })).problem, /no longer matches/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("assemble stops on a held generated track before locating FFmpeg or encoding a segment", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const box = sandbox("fixture-illustrated", "illustrated");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = illustratedFixture();
  doc.music = { prompt: "quiet instrumental, no vocals", gain_db: -20, duck_db: -10 };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const timeline = { ...estimateTimeline(doc), speech_hash: speechHash(doc, fixtureLexicon()) };
  writeAudioFixture(timeline, box.workdir);
  mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
  writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visualHash(doc) }));
  mkdirSync(path.join(box.workdir, "music"), { recursive: true });
  const audio = path.join(box.workdir, "music", "bed.mp3");
  const { ffmpeg } = tools;
  await runTool(ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=330:duration=2", "-c:a", "libmp3lame", audio]);
  writeFileSync(path.join(box.workdir, "music", "manifest.json"), JSON.stringify({
    mix_hash: null, requested_mix_hash: mixHash(doc), source: "generated", file: "music/bed.mp3",
    sha256: createHash("sha256").update(readFileSync(audio)).digest("hex"),
    requested_seconds: 60, actual_seconds: await decodedMusicSeconds(audio), duration_measurement: "ffmpeg_full_decode", duration_hold: true,
  }));
  let ffmpegReached = 0;
  let stderr = "";
  const ctx = {
    root: box.root, home: box.base, EXIT,
    env: { VIDEO_WORKDIR: box.work, get FFMPEG_PATH() { ffmpegReached += 1; throw new Error("ffmpeg sentinel"); } },
    stdout: { write() {} }, stderr: { write(value) { stderr += value; } },
  };
  assert.equal(await assemble("assemble", ["--slug", box.slug], ctx), EXIT.usage);
  assert.match(stderr, /duration hold/);
  assert.equal(ffmpegReached, 0);
  assert.equal(existsSync(path.join(box.workdir, "segments")), false);
});
