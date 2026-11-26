import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  buildCutAudioArgs,
  buildMeasureArgs,
  cutAudioSlice,
  detectAudioSlices,
  invertSilencesToSlices,
  measureAudioFile,
  parseDecodedSeconds,
  parseEbur128Summary,
  parseSilenceIntervals,
} from "./audio/ffmpeg-audio.mjs";
import { detectSyncFolderHazard, resolveChromeProfileDir, resolveRuntimeHome } from "./config.mjs";
import {
  buildDownloadClipExpression,
  buildListClipsExpression,
  buildSessionProbeExpression,
  buildSubmitPromptExpression,
} from "./drivers/chrome-cdp-driver.mjs";
import { classifyMusicError } from "./drivers/driver-interface.mjs";
import {
  allocateTrackFilename,
  buildCueName,
  preflightMusicPlan,
  resolveCollectionPaths,
} from "./guards/music-guards.mjs";

test("config resolves Windows runtime home, isolated profile dir, and flags OneDrive hazards", () => {
  const home = resolveRuntimeHome({
    platform: "win32",
    env: { USERPROFILE: "C:\\Users\\Owner", LOCALAPPDATA: "C:\\Users\\Owner\\AppData\\Local" },
  });
  assert.equal(home, "C:\\Users\\Owner\\AppData\\Local\\mokaair-flow-music");
  assert.ok(resolveChromeProfileDir(home, "member-2").endsWith("profile_member-2"));
  assert.ok(detectSyncFolderHazard("C:\\Users\\Owner\\OneDrive\\travel_scanner", "win32"));
  assert.equal(detectSyncFolderHazard("C:\\dev\\travel_scanner", "win32"), null);
});

test("Route B path boundary blocks tracked repo directories and allows work/music-library", () => {
  const fakeRepo = path.resolve(os.tmpdir(), "fake-music-repo");
  const ok = resolveCollectionPaths("curio-20261126", { repoRoot: fakeRepo });
  assert.equal(ok.collection, "curio-20261126");
  assert.ok(ok.collectionDir.endsWith(path.join("work", "music-library", "curio-20261126")));

  assert.throws(
    () => resolveCollectionPaths("bad", { repoRoot: fakeRepo, workdir: path.join(fakeRepo, "docs", "videos", "music") }),
    /Route B boundary violation/,
  );
  assert.throws(
    () => resolveCollectionPaths("bad2", { repoRoot: fakeRepo, workdir: path.join(fakeRepo, "tools", "video") }),
    /Route B boundary violation/,
  );
});

test("allocateTrackFilename prevents duplicate-title overwrites via -take1/-take2/-take3", () => {
  const cue = buildCueName({ series: "sothatswhy", kind: "bed", name: "sothatswhy-bed-body (Take 2)" });
  assert.equal(cue, "sothatswhy-bed-body");

  const first = allocateTrackFilename({ cue, format: "m4a", existingFiles: [] });
  assert.equal(first.filename, "sothatswhy-bed-body-take1.m4a");
  assert.equal(first.take, 1);

  const third = allocateTrackFilename({
    cue,
    format: "m4a",
    existingFiles: ["sothatswhy-bed-body-take1.m4a", "sothatswhy-bed-body-take2.m4a"],
  });
  assert.equal(third.filename, "sothatswhy-bed-body-take3.m4a");
  assert.equal(third.take, 3);
});

test("preflightMusicPlan enforces no-vocal narration bed guard, copyright block, and cue/sfx trim warnings", () => {
  const clean = preflightMusicPlan(
    [
      { kind: "bed", name: "archive", prompt: "Warm upright bass and brushed drums, 92 bpm" },
      { kind: "cue", name: "reveal", prompt: "Bright chime resolution chord" },
      { kind: "sfx", name: "stamp", prompt: "Crisp wooden rubber stamp impact on paper" },
    ],
    { series: "curio" },
  );
  assert.equal(clean.ok, true);
  assert.equal(clean.summary.beds, 1);
  assert.equal(clean.summary.cues, 1);
  assert.equal(clean.summary.sfx, 1);
  assert.match(clean.normalizedTracks[0].prompt, /no vocals/i);
  assert.ok(clean.warnings.some((w) => w.code === "lyria_cue_trim_reminder"));
  assert.ok(clean.warnings.some((w) => w.code === "lyria_sfx_slice_reminder"));

  const blocked = preflightMusicPlan(
    [
      { kind: "bed", name: "bad-vocal", prompt: "Pop song with female singing vocals and lyrics" },
      { kind: "bed", name: "bad-ip", prompt: "In the style of Studio Ghibli and Joe Hisaishi" },
    ],
    { series: "curio" },
  );
  assert.equal(blocked.ok, false);
  assert.ok(blocked.blockers.some((b) => b.code === "bed_vocal_conflict"));
  assert.ok(blocked.blockers.some((b) => b.code === "copyright_reference"));
});

test("Chrome CDP expressions target verified Flow Music endpoints and Fail-Fast error classifier works", () => {
  assert.match(buildSessionProbeExpression(), /__api\/user\/me/);
  assert.match(buildListClipsExpression("u-42", 50), /__api\/clips\/user\/.*public_only=false/);
  assert.match(buildDownloadClipExpression("clip-9", "wav"), /__api\/download\/audio\/.*format=.*wav/);
  assert.match(buildSubmitPromptExpression({ prompt: "Jazz mystery", title: "curio-bed-jazz" }), /selector_drift/);

  const authErr = classifyMusicError({ statusCode: 401, message: "Unauthorized" });
  assert.equal(authErr.code, "auth_expired");
  assert.equal(authErr.retryable, false);

  const rateErr = classifyMusicError({ statusCode: 429, message: "Rate limit" });
  assert.equal(rateErr.code, "rate_limited");
  assert.equal(rateErr.retryable, false);
});

test("FFmpeg audio parser extracts decoded seconds, EBU R128 loudness, silence intervals, and slices", async () => {
  assert.equal(parseDecodedSeconds("out_time_us=12450000\nprogress=end\n"), 12.45);
  const ebu = parseEbur128Summary(
    "M: -18.2 S: -20.1\nM: -12.4 S: -15.0\nIntegrated loudness:\n  I: -16.4 LUFS\nTrue peak:\n  Peak: -0.5 dBFS\n",
  );
  assert.equal(ebu.lufs_i, -16.4);
  assert.equal(ebu.lufs_m, -12.4);
  assert.equal(ebu.peak_dbtp, -0.5);

  const silences = parseSilenceIntervals(
    "[silencedetect] silence_start: 1.50\n[silencedetect] silence_end: 3.00 | silence_duration: 1.50\n[silencedetect] silence_start: 4.20\n",
    6.0,
  );
  assert.equal(silences.length, 2);
  const slices = invertSilencesToSlices(silences, 6.0, { minSliceSec: 0.2, padSec: 0.05 });
  assert.equal(slices.length, 2);
  assert.equal(slices[0].startSec, 0);
  assert.equal(slices[0].endSec, 1.55);
  assert.equal(slices[1].startSec, 2.95);
  assert.equal(slices[1].endSec, 4.25);

  const measureArgs = buildMeasureArgs({ filePath: "a.m4a", padSec: 1 });
  assert.ok(measureArgs.some((a) => a.includes("apad=pad_dur=1") && a.includes("ebur128=peak=true")));

  const cutArgs = buildCutAudioArgs({ inputPath: "in.m4a", outputPath: "out-cut.m4a", startSec: 2, endSec: 5.5 });
  assert.ok(cutArgs.includes("-ss") && cutArgs.includes("2") && cutArgs.includes("-t") && cutArgs.includes("3.5"));

  // Mocked measure + detectSlices + cutAudioSlice end-to-end
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-audio-"));
  try {
    const src = path.join(dir, "sfx.m4a");
    const dst = path.join(dir, "sfx-cut.m4a");
    fs.writeFileSync(src, Buffer.from("fake-audio"));

    const fakeFfmpeg = async (_bin, args) => {
      const last = args[args.length - 1];
      if (last !== "pipe:1") {
        fs.writeFileSync(last, Buffer.from("trimmed-audio"));
        return { exitCode: 0, stdout: "", stderr: "" };
      }
      return {
        exitCode: 0,
        stdout: "out_time_us=10000000\nprogress=end\n",
        stderr:
          "silence_start: 1.2\nsilence_end: 3.8 | silence_duration: 2.6\nM: -14.2\nIntegrated loudness:\n  I: -16.8 LUFS\nTrue peak:\n  Peak: -1.2 dBFS\n",
      };
    };

    const m = await measureAudioFile(src, { runFfmpeg: fakeFfmpeg });
    assert.equal(m.lufs_i, -16.8);
    assert.equal(m.nearSilent, false);

    const det = await detectAudioSlices(src, { runFfmpeg: fakeFfmpeg });
    assert.equal(det.slices.length, 2);

    const cut = await cutAudioSlice({ inputPath: src, outputPath: dst, startSec: 0, endSec: 1.2, runFfmpeg: fakeFfmpeg });
    assert.ok(fs.existsSync(dst));
    assert.equal(cut.cut.endSec, 1.2);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});
