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
import { decodedMusicSeconds, run as music } from "../media/music.mjs";
import { MIN_LOOP_SECONDS } from "../core/music-loop.mjs";

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

const shaOf = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

test("a recorded loop lets a short bed under its cut, and only for that file and a cut no longer than it", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const dir = mkdtempSync(path.join(tmpdir(), "music-loop-"));
  try {
    mkdirSync(path.join(dir, "music"));
    const file = path.join(dir, "music", "bed.mp3");
    await runTool(tools.ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", `sine=frequency=330:duration=${MIN_LOOP_SECONDS + 1}`, "-c:a", "libmp3lame", file]);
    const actual = await decodedMusicSeconds(file);
    const doc = dramaFixture();
    const sha256 = shaOf(file);
    const loop = { method: "stream_loop", sha256, track_seconds: actual, cut_seconds: 100, plays: Math.ceil(100 / actual), decided_at: "2026-10-24T00:00:00.000Z" };
    const manifest = { mix_hash: mixHash(doc), source: "generated", file: "music/bed.mp3", sha256, actual_seconds: actual, duration_measurement: "ffmpeg_full_decode", duration_hold: false, loop };
    const manifestFile = path.join(dir, "music", "manifest.json");
    const inputs = async (value, seconds) => { writeFileSync(manifestFile, JSON.stringify(value)); return musicInputs(doc, dir, dir, { requiredSeconds: seconds }); };

    assert.equal((await inputs(manifest, 100)).track.file, file, "the recorded cut");
    assert.equal((await inputs({ ...manifest, duration_hold: true }, 100)).track.file, file, "a held track with its loop recorded");
    assert.match((await inputs(manifest, 101)).problem, /recorded loop covers a 100\.000 s cut .*music --loop/, "a longer cut needs a new decision");
    assert.match((await inputs({ ...manifest, loop: { ...loop, sha256: "0".repeat(64) } }, 100)).problem, /record it again/, "another file");
    assert.match((await inputs({ ...manifest, loop: { ...loop, track_seconds: actual + 1 } }, 100)).problem, /record it again/, "another measured length");
    assert.match((await inputs({ ...manifest, loop: undefined }, 100)).problem, /explicit checked loop \(music --loop\)/, "no decision, no loop");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("music --loop records the loop of an assembled cut's retained track for free, and refuses a cut made with other settings", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  const timeline = writeAudioFixture({ ...estimateTimeline(doc), speech_hash: speechHash(doc, fixtureLexicon()) }, box.workdir);
  mkdirSync(path.join(box.workdir, "music"), { recursive: true });
  const audio = path.join(box.workdir, "music", "bed.mp3");
  await runTool(tools.ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", `sine=frequency=330:duration=${MIN_LOOP_SECONDS + 1}`, "-c:a", "libmp3lame", audio]);
  const manifestFile = path.join(box.workdir, "music", "manifest.json");
  // A track bought before decoded lengths were recorded, as every brand story of 2026-10 has.
  const legacy = { mix_hash: mixHash(doc), source: "generated", file: "music/bed.mp3", sha256: shaOf(audio), seconds: 571, key: "0aa2244555afd2eb" };
  writeFileSync(manifestFile, JSON.stringify(legacy));
  writeFileSync(path.join(box.workdir, ARTIFACTS.video), "cut");
  const checksFile = path.join(box.workdir, ARTIFACTS.checks);
  let stdout = "";
  const ctx = { root: box.root, home: box.base, EXIT, now: () => new Date("2026-10-24T01:00:00Z"), env: { VIDEO_WORKDIR: box.work }, stdout: { write(value) { stdout += value; } }, stderr: { write() {} } };

  writeFileSync(checksFile, JSON.stringify({ ok: true, mix_hash: "another-mix", speech_hash: timeline.speech_hash }));
  await assert.rejects(music("music", ["--slug", box.slug, "--loop"], ctx), /assembled with these music settings/);
  assert.deepEqual(JSON.parse(readFileSync(manifestFile, "utf8")), legacy, "nothing written");

  writeFileSync(checksFile, JSON.stringify({ ok: true, mix_hash: mixHash(doc), speech_hash: timeline.speech_hash }));
  assert.equal(await music("music", ["--slug", box.slug, "--loop"], ctx), EXIT.ok);
  const recorded = JSON.parse(readFileSync(manifestFile, "utf8"));
  const cut = timeline.total_frames / FPS;
  assert.equal(recorded.key, legacy.key, "the purchase record stays");
  assert.equal(recorded.duration_measurement, "ffmpeg_full_decode");
  assert.equal(recorded.duration_hold, false);
  assert.deepEqual(recorded.loop, { method: "stream_loop", sha256: legacy.sha256, track_seconds: recorded.actual_seconds, cut_seconds: cut, plays: Math.ceil(cut / recorded.actual_seconds), decided_at: "2026-10-24T01:00:00.000Z" });
  assert.match(stdout, /recorded in music\/manifest\.json/);
  assert.equal((await musicInputs(doc, box.workdir, box.work)).track.file, audio, "the mix and the dub take it for the current cut");

  writeFileSync(audio, "changed bytes");
  await assert.rejects(music("music", ["--slug", box.slug, "--loop"], ctx), /differs from its saved SHA-256/);
});
