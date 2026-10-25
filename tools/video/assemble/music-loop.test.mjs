import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { LONG_ANIME_POLICY } from "../core/anime-policy.mjs";
import { mixHash } from "../core/drama.mjs";
import { dramaFixture, fixtureLexicon, illustratedFixture, sandbox, storySeries, writeAudioFixture } from "../core/fixtures/load.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { estimateTimeline, FPS, speechHash, visualHash } from "../core/timeline.mjs";
import { EXIT } from "../cli.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "./ffmpeg.mjs";
import { run as assemble } from "./cli.mjs";
import { musicInputs } from "./sound.mjs";
import { mediaKey } from "../media/cache.mjs";
import { decodedMusicSeconds, HANDS_OFF_MAX_PLAYS, loopDecidedByChecks, run as music, trackSeconds } from "../media/music.mjs";
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

test("music --loop records the loop of an assembled cut's retained track for free, and refuses a track made for other settings", async (t) => {
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

  writeFileSync(checksFile, JSON.stringify({ ok: true, mix_hash: mixHash(doc), speech_hash: timeline.speech_hash }));
  const older = { ...legacy, mix_hash: "another-mix" };
  writeFileSync(manifestFile, JSON.stringify(older));
  await assert.rejects(music("music", ["--slug", box.slug, "--loop"], ctx), /made for older music settings/);
  assert.deepEqual(JSON.parse(readFileSync(manifestFile, "utf8")), older, "nothing written");

  writeFileSync(manifestFile, JSON.stringify(legacy));
  assert.equal(await music("music", ["--slug", box.slug, "--loop"], ctx), EXIT.ok);
  const recorded = JSON.parse(readFileSync(manifestFile, "utf8"));
  const cut = timeline.total_frames / FPS;
  assert.equal(recorded.key, legacy.key, "the purchase record stays");
  assert.equal(recorded.duration_measurement, "ffmpeg_full_decode");
  assert.equal(recorded.duration_hold, false);
  assert.deepEqual(recorded.loop, { method: "stream_loop", sha256: legacy.sha256, track_seconds: recorded.actual_seconds, cut_seconds: cut, plays: Math.ceil(cut / recorded.actual_seconds), basis: "assembled_cut", decided_by: "command", decided_at: "2026-10-24T01:00:00.000Z" });
  assert.match(stdout, /as the assembled cut does; recorded in music\/manifest\.json/);
  assert.doesNotMatch(stdout, /next: /, "a published cut has nothing to assemble");
  assert.equal((await musicInputs(doc, box.workdir, box.work)).track.file, audio, "the mix and the dub take it for the current cut");

  writeFileSync(audio, "changed bytes");
  await assert.rejects(music("music", ["--slug", box.slug, "--loop"], ctx), /differs from its saved SHA-256/);
});

const bedOf = async (ffmpeg, file, seconds) => runTool(ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", `sine=frequency=330:duration=${seconds}`, "-c:a", "libmp3lame", file]);

test("music --loop before the first assembly takes the current timeline's cut and keeps every check", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  const mix = mixHash(doc);
  const speech = speechHash(doc, fixtureLexicon());
  mkdirSync(path.join(box.workdir, "music"), { recursive: true });
  const audio = path.join(box.workdir, "music", "bed.mp3");
  await bedOf(tools.ffmpeg, audio, MIN_LOOP_SECONDS + 1);
  const actual = await decodedMusicSeconds(audio);
  const cut = 50;
  const timelineFile = path.join(box.workdir, ARTIFACTS.timeline);
  writeFileSync(timelineFile, JSON.stringify({ speech_hash: speech, total_frames: cut * FPS }));
  // What the music stage leaves when the track it bought decodes shorter than the cut (e001, 2026-10-24).
  const held = { mix_hash: null, requested_mix_hash: mix, source: "generated", file: "music/bed.mp3", sha256: shaOf(audio), requested_seconds: cut + 5, actual_seconds: actual, duration_measurement: "ffmpeg_full_decode", duration_hold: true, prompt: doc.music.prompt, key: "492fc5d7b55364a4" };
  const manifestFile = path.join(box.workdir, "music", "manifest.json");
  writeFileSync(manifestFile, JSON.stringify(held));
  let stdout = "";
  const ctx = { root: box.root, home: box.base, EXIT, now: () => new Date("2026-10-24T09:00:00Z"), env: { VIDEO_WORKDIR: box.work }, stdout: { write(value) { stdout += value; } }, stderr: { write() {} } };
  const loop = () => music("music", ["--slug", box.slug, "--loop"], ctx);
  assert.match((await musicInputs(doc, box.workdir, box.work)).problem, /duration hold/, "assembly cannot start without the loop");

  writeFileSync(timelineFile, JSON.stringify({ speech_hash: "older", total_frames: cut * FPS }));
  await assert.rejects(loop(), /built for an older script/);
  assert.deepEqual(JSON.parse(readFileSync(manifestFile, "utf8")), held, "a stale timeline writes nothing");
  writeFileSync(timelineFile, JSON.stringify({ speech_hash: speech, total_frames: cut * FPS }));
  const older = { ...held, requested_mix_hash: "another-mix" };
  writeFileSync(manifestFile, JSON.stringify(older));
  await assert.rejects(loop(), /made for older music settings/);
  assert.deepEqual(JSON.parse(readFileSync(manifestFile, "utf8")), older, "a track bought for other settings writes nothing");
  writeFileSync(manifestFile, JSON.stringify(held));

  // A cut assembled earlier with other settings is no basis for the loop, and no obstacle either.
  writeFileSync(path.join(box.workdir, ARTIFACTS.video), "older cut");
  writeFileSync(path.join(box.workdir, ARTIFACTS.checks), JSON.stringify({ ok: true, mix_hash: "another-mix", speech_hash: speech }));
  assert.equal(await loop(), EXIT.ok);
  const recorded = JSON.parse(readFileSync(manifestFile, "utf8"));
  assert.equal(recorded.key, held.key, "the paid request stays");
  assert.equal(recorded.mix_hash, mix);
  assert.equal(recorded.duration_hold, false);
  assert.deepEqual(recorded.loop, { method: "stream_loop", sha256: held.sha256, track_seconds: actual, cut_seconds: cut, plays: 2, basis: "timeline", decided_by: "command", decided_at: "2026-10-24T09:00:00.000Z" });
  assert.match(stdout, /plays 2 times under the 50\.000 s cut; recorded in music\/manifest\.json/);
  assert.match(stdout, /next: node tools\/video\/cli\.mjs assemble --slug fixture-drama/);
  assert.equal((await musicInputs(doc, box.workdir, box.work)).track.file, audio, "assembly takes it for the timeline's cut");
  writeFileSync(timelineFile, JSON.stringify({ speech_hash: speech, total_frames: (cut + 1) * FPS }));
  assert.match((await musicInputs(doc, box.workdir, box.work)).problem, /record it again \(music --loop\)/, "a longer cut needs a new decision");

  const jingle = path.join(box.workdir, "music", "jingle.mp3");
  await bedOf(tools.ffmpeg, jingle, 2);
  const short = { ...held, file: "music/jingle.mp3", sha256: shaOf(jingle), actual_seconds: await decodedMusicSeconds(jingle) };
  writeFileSync(manifestFile, JSON.stringify(short));
  await assert.rejects(loop(), new RegExp(`under the ${MIN_LOOP_SECONDS} s a looped bed needs`));
  assert.deepEqual(JSON.parse(readFileSync(manifestFile, "utf8")), short, "a jingle is not looped");
});

const TOKEN = `mkv_${"c".repeat(43)}`;
const STATUS = { enabled: true, music_enabled: true, music: { provider: "gemini", model: "lyria-3.5", configured: true } };

test("on a hands-off drama series the music stage records the loop itself, within two plays; otherwise the owner's command does", async (t) => {
  const tools = await musicTestTool(t);
  if (!tools) return;
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  const speech = speechHash(doc, fixtureLexicon());
  mkdirSync(path.join(box.workdir, "music"), { recursive: true });
  const audio = path.join(box.workdir, "music", "bed.mp3");
  await bedOf(tools.ffmpeg, audio, MIN_LOOP_SECONDS + 1);
  const actual = await decodedMusicSeconds(audio);
  const requests = [];
  const fetchImpl = async (url, init = {}) => {
    const route = `${init.method ?? "GET"} ${new URL(url).pathname}`;
    requests.push(route);
    return route === "GET /api/video/media/status" ? Response.json(STATUS) : Response.json({ detail: "this test buys nothing" }, { status: 500 });
  };
  const timelineFile = path.join(box.workdir, ARTIFACTS.timeline);
  const manifestFile = path.join(box.workdir, "music", "manifest.json");
  // The short track the stage bought for a cut of `cut` seconds, held as it is before this run.
  const retain = (cut) => {
    writeFileSync(timelineFile, JSON.stringify({ speech_hash: speech, total_frames: cut * FPS }));
    const seconds = trackSeconds(cut * FPS);
    const key = mediaKey("music", { provider: STATUS.music.provider, model: STATUS.music.model, prompt: doc.music.prompt, seconds });
    writeFileSync(manifestFile, JSON.stringify({ mix_hash: null, requested_mix_hash: mixHash(doc), source: "generated", file: "music/bed.mp3", sha256: shaOf(audio), requested_seconds: seconds, actual_seconds: actual, duration_measurement: "ffmpeg_full_decode", duration_hold: true, prompt: doc.music.prompt, key }));
  };
  const stage = async (now) => {
    const out = { stdout: "", stderr: "" };
    const ctx = {
      root: box.root, home: box.base, EXIT, fetch: fetchImpl, now: () => new Date(now),
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" },
      stdout: { write: (value) => (out.stdout += value) }, stderr: { write: (value) => (out.stderr += value) },
    };
    const code = await music("music", ["--slug", box.slug], ctx);
    return { code, ...out, manifest: JSON.parse(readFileSync(manifestFile, "utf8")) };
  };
  const seriesFile = path.join(box.dir, "series.json");
  const episodeOf = (handsOff) => writeFileSync(seriesFile, JSON.stringify({ slug: "fixture-series", episode: 1, chapter: 1, series: { genre: "xianxia-bonds", compilation: true, hands_off: handsOff } }));

  retain(50);
  for (const handsOff of [null, false]) {
    if (handsOff !== null) episodeOf(handsOff);
    const owner = await stage("2026-10-24T09:00:00Z");
    assert.equal(owner.code, EXIT.owner, owner.stderr);
    assert.match(owner.stderr, /music needs the owner: decoded track is shorter than the 50\.000 s cut\. Keep this paid file; record a checked loop \(node tools\/video\/cli\.mjs music --slug fixture-drama --loop\)/);
    assert.equal(owner.manifest.duration_hold, true);
    assert.equal(owner.manifest.loop, undefined, handsOff === null ? "a one-off video" : "a series with its gates on");
  }

  episodeOf(true);
  const auto = await stage("2026-10-24T09:05:00Z");
  assert.equal(auto.code, EXIT.ok, auto.stderr);
  assert.deepEqual(auto.manifest.loop, { method: "stream_loop", sha256: shaOf(audio), track_seconds: actual, cut_seconds: 50, plays: 2, basis: "timeline", decided_by: "hands_off", decided_at: "2026-10-24T09:05:00.000Z" });
  assert.equal(auto.manifest.mix_hash, mixHash(doc));
  assert.equal(auto.manifest.duration_hold, false);
  assert.match(auto.stdout, /reused/);
  assert.match(auto.stdout, /plays 2 times under the 50\.000 s cut \(a hands-off series' checks recorded the loop/);
  assert.equal((await musicInputs(doc, box.workdir, box.work)).track.file, audio, "assembly takes it");
  assert.deepEqual([...new Set(requests)], ["GET /api/video/media/status"], "nothing is bought");

  const again = await stage("2026-10-24T10:00:00Z");
  assert.equal(again.code, EXIT.ok, again.stderr);
  assert.deepEqual(again.manifest.loop, auto.manifest.loop, "a rerun keeps the decision made for this file and cut");
  assert.match(again.stdout, /the loop already recorded for this file and cut/);

  retain(Math.ceil(actual * HANDS_OFF_MAX_PLAYS) + 1);
  const far = await stage("2026-10-24T11:00:00Z");
  assert.equal(far.code, EXIT.owner, far.stderr);
  assert.match(far.stderr, /It would play 3 times, more than the 2 a hands-off series loops on its own\./);
  assert.equal(far.manifest.duration_hold, true);
  assert.equal(far.manifest.loop, undefined);
});

test("only a hands-off drama series has its checks decide a loop; a brand story's stays the owner's command", () => {
  assert.equal(loopDecidedByChecks(null), false);
  assert.equal(loopDecidedByChecks({ series: { hands_off: true } }), true);
  assert.equal(loopDecidedByChecks({ series: { hands_off: false } }), false);
  const anime = { production_policy: LONG_ANIME_POLICY, category: "anime" };
  assert.equal(loopDecidedByChecks({ ...anime, series: { ...anime, kind: "series", hands_off: true } }), false, "a long anime keeps the owner's gates");
  assert.equal(loopDecidedByChecks({ series: { ...anime, hands_off: true } }), false);
  assert.equal(loopDecidedByChecks({ hands_off: true }), false, "the flag lives in the series block");
  const story = storySeries();
  assert.equal(story.kind, "story");
  assert.equal(loopDecidedByChecks({ ...story, series: { ...story.series, hands_off: true } }), false);
});
