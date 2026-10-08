/**
 * The offline reference analysis the youtube-video skill ships
 * (.agents/skills/youtube-video/scripts/reference_analysis.mjs).
 *
 * What is pinned: the shot statistics are the browser probe's, so a record this script writes
 * compares with the ones in docs/videos/drama-craft/ (the cumulative lengths of four recorded
 * ranges give back every published number); the cut lists those records hold are read the way
 * the ticket counts them (46 cuts below 120 s for xVXEefk1vWs); ffmpeg's three outputs are read
 * from real lines; and, where ffmpeg is installed, a lavfi-made clip with cuts at 2.0 and 3.6 s, a
 * rotating middle shot and two silences is measured end to end, including the --url path through
 * a stand-in yt-dlp that copies the clip instead of fetching anything. Nothing here touches the
 * network, and yt-dlp itself is never bundled or installed by the script.
 */
import assert from "node:assert/strict";
import test, { after } from "node:test";
import { spawnSync } from "node:child_process";
import { chmodSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  DEFAULTS,
  FORMAT,
  compareCuts,
  compareWithStudy,
  filterGraph,
  formatJson,
  frameShape,
  motionStats,
  parseArgs,
  parseCuts,
  parseMotion,
  parseRange,
  parseSilences,
  recordedCuts,
  shotStats,
  soundStats,
  youtubeId,
} from "../.agents/skills/youtube-video/scripts/reference_analysis.mjs";
import { locateFfmpeg } from "./video/assemble/ffmpeg.mjs";

const SCRIPT = fileURLToPath(new URL("../.agents/skills/youtube-video/scripts/reference_analysis.mjs", import.meta.url));
const SOURCE = readFileSync(SCRIPT, "utf8");
const STUDY_20261003 = JSON.parse(readFileSync(new URL("../docs/videos/drama-craft/reference-study-20261003.json", import.meta.url), "utf8"));
const STUDY_20261004 = JSON.parse(readFileSync(new URL("../docs/videos/drama-craft/reference-study-20261004-budaimiao.json", import.meta.url), "utf8"));

const tools = await locateFfmpeg().catch(() => null);
const withFfmpeg = { skip: tools ? false : "ffmpeg is not installed here (web-checks has none; ci.yml's video-tests job installs it and fails on this skip)" };
const withStandIn = { skip: withFfmpeg.skip || (process.platform === "win32" ? "a stand-in executable needs a POSIX shell" : false) };

const near = (actual, expected, within, message) => assert.ok(Math.abs(actual - expected) <= within, `${message ?? ""}: ${actual} is not within ${within} of ${expected}`);
const cumulative = (start, lengths) => {
  let t = start;
  return lengths.map((length) => (t = Number((t + length).toFixed(2))));
};

test("a YouTube id is read from the forms a link takes, and from nothing else", () => {
  for (const [given, expected] of [
    ["xVXEefk1vWs", "xVXEefk1vWs"],
    ["https://www.youtube.com/watch?v=xVXEefk1vWs", "xVXEefk1vWs"],
    ["https://www.youtube.com/watch?t=120&v=m2qhz2n9618&list=PL1", "m2qhz2n9618"],
    ["https://m.youtube.com/watch?v=QNPMAbMp3kY", "QNPMAbMp3kY"],
    ["https://youtu.be/fC18EKAGdL8?t=30", "fC18EKAGdL8"],
    ["https://www.youtube.com/shorts/qbyEeolMKDk", "qbyEeolMKDk"],
    ["https://www.youtube-nocookie.com/embed/wdXB1HC1F9c", "wdXB1HC1F9c"],
    ["https://www.youtube.com/live/5QcL49ezzG0?feature=share", "5QcL49ezzG0"],
    [" xVXEefk1vWs\n", "xVXEefk1vWs"],
    ["xVXEefk1vW", null],
    ["https://example.com/watch?v=xVXEefk1vWs", null],
    ["https://www.youtube.com/@channel", null],
    ["a reference video", null],
    ["", null],
  ]) {
    assert.equal(youtubeId(given), expected, given);
  }
});

test("a range is A-B in seconds, with either end optional", () => {
  assert.deepEqual(parseRange("0-240"), [0, 240]);
  assert.deepEqual(parseRange("1800-1920"), [1800, 1920]);
  assert.deepEqual(parseRange("1800-"), [1800, null]);
  assert.deepEqual(parseRange("-120"), [0, 120]);
  assert.deepEqual(parseRange("12.5-13.25"), [12.5, 13.25]);
  for (const bad of ["-", "240", "240-0", "a-b", "0-240-300"]) assert.throws(() => parseRange(bad), /--range/, bad);
});

test("the shot statistics are the probe's: the recorded ranges come back from their own lengths", () => {
  // Four ranges whose lengths cover the whole range, and one that starts at 30 minutes.
  const checked = [];
  for (const video of STUDY_20261003.videos) {
    for (const entry of video.ranges) {
      const sum = Number(entry.lengths.reduce((a, b) => a + b, 0).toFixed(2));
      if (sum !== entry.range[1] - entry.range[0] || entry.lengths.length !== entry.shots) continue;
      const cuts = cumulative(entry.range[0], entry.lengths).slice(0, -1);
      const stats = shotStats(cuts, entry.range[0], entry.range[1]);
      for (const key of ["shots", "mean", "median", "p10", "p90", "longest", "over_6s", "opening_10s", "opening_30s", "spread_p90_over_p10"]) {
        if (key in entry) assert.equal(stats[key], entry[key], `${video.id} ${entry.range.join("-")} ${key}`);
      }
      assert.deepEqual(stats.lengths, entry.lengths, `${video.id} ${entry.range.join("-")} lengths`);
      checked.push(`${video.id} ${entry.range.join("-")}`);
    }
  }
  assert.deepEqual(checked, ["xVXEefk1vWs 1800-1920", "QNPMAbMp3kY 0-240", "wdXB1HC1F9c 0-240", "fC18EKAGdL8 0-240", "qbyEeolMKDk 0-240"]);
  // Cuts outside the range are ignored, and the opening counts include the first shot.
  const stats = shotStats([0, 1, 3.5, 5.5, 120, 121], 0, 120);
  assert.deepEqual(stats.cuts, [1, 3.5, 5.5]);
  assert.deepEqual(stats.lengths, [1, 2.5, 2, 114.5]);
  assert.equal(stats.opening_10s, 4);
  assert.equal(stats.over_6s, 1);
  assert.equal(stats.spread_p90_over_p10, 114.5);
  assert.equal(shotStats([], 0, 10).shots, 1);
});

test("a study record's cut lists are read as the ticket counts them", () => {
  const lists = recordedCuts(STUDY_20261003, "xVXEefk1vWs");
  assert.deepEqual(lists.map((list) => [list.name, list.covers, list.cuts.length]), [
    ["ranges 0-240 lengths", [0, 215.25], 80],
    ["ranges 1800-1920 lengths", [1800, 1920], 44],
  ]);
  // The 46 cuts below 120 s that the re-run ticket names; the truncated list's last edge is no cut.
  assert.equal(lists[0].cuts.filter((t) => t < 120).length, 46);
  assert.deepEqual(lists[0].cuts.slice(0, 5), [1, 3.5, 5.5, 7.75, 10.25]);
  assert.ok(!lists[0].cuts.includes(215.25));
  assert.ok(!lists[1].cuts.includes(1920));

  const budaimiao = recordedCuts(STUDY_20261004, "m2qhz2n9618");
  assert.deepEqual(budaimiao.map((list) => [list.name, list.covers, list.cuts.length]), [
    ["shots start times", [0, 266.5], 286],
    ["cross_check verifier_cut_times", [0, 266.5], 154],
  ]);
  assert.deepEqual(recordedCuts(STUDY_20261004, "not-a-video"), []);
});

test("two cut lists are matched one to one within the tolerance", () => {
  const result = compareCuts([2, 3.6, 7, 9.1], [2.25, 3.5, 3.7, 5, 9], 0.3);
  assert.deepEqual(result, { tolerance: 0.3, recorded: 5, here: 4, matched: 3, only_here: [7], only_recorded: [3.7, 5] });
  assert.deepEqual(compareCuts([], [1], 0.3).only_recorded, [1]);
  assert.equal(compareCuts([1.0], [1.31], 0.3).matched, 0);
  assert.equal(compareCuts([1.0], [1.3], 0.3).matched, 1);
});

test("a measured range is compared with every recorded list over the seconds both cover", () => {
  const study = {
    videos: [{ id: "v", ranges: [{ range: [0, 10], lengths: [2, 3, 5] }], shot_columns: ["start", "end"], measured_to: 12, shots: [[0, 2], [2, 5.2], [5.2, 12]] }],
    cross_check: [{ id: "v", verifier_cut_times: [2, 5, 11] }],
  };
  const measured = [{ range: [0, 8], cuts: [2.0, 5.1] }];
  const out = compareWithStudy(study, "v", measured, 0.3);
  assert.deepEqual(
    out.map((c) => [c.list, c.covered, c.recorded, c.matched, c.only_here, c.only_recorded]),
    [
      ["ranges 0-10 lengths", [0, 8], 2, 2, [], []],
      ["shots start times", [0, 8], 2, 2, [], []],
      ["cross_check verifier_cut_times", [0, 8], 2, 2, [], []],
    ],
  );
  assert.deepEqual(compareWithStudy(study, "v", [{ range: [20, 30], cuts: [] }], 0.3), []);
});

test("ffmpeg's three outputs are read from the lines it writes", () => {
  const stderr = [
    "[Parsed_metadata_1 @ 0x55d6c5867a00] frame:0    pts:25600   pts_time:2",
    "[Parsed_metadata_1 @ 0x55d6c5867a00] lavfi.scene_score=0.400000",
    "[Parsed_showinfo_2 @ 0x55d6c5da5bc0] n:   0 pts:  25600 pts_time:2       duration:    512 duration_time:0.04    fmt:yuv420p cl:left sar:1/1 s:320x180 i:P iskey:0 type:P checksum:3649F710 plane_checksum:[1CCC0B1C CBE8BF0C 5D752CE8] mean:[41 240 110] stdev:[0.0 0.0 0.0]",
    "[Parsed_showinfo_2 @ 0x55d6c5da5bc0] color_range:unknown color_space:unknown color_primaries:unknown color_trc:unknown",
    "[Parsed_metadata_1 @ 0x55d6c5867a00] frame:1    pts:45056   pts_time:3.52",
    "[Parsed_metadata_1 @ 0x55d6c5867a00] lavfi.scene_score=0.801218",
    "[Parsed_showinfo_2 @ 0x55d6c5da5bc0] n:   1 pts:  45056 pts_time:3.52    duration:    512 duration_time:0.04    fmt:yuv420p cl:left sar:1/1 s:320x180 i:P iskey:0 type:P checksum:83879642 plane_checksum:[23E43023 B1C19B1E B813CAF2] mean:[121 130 126] stdev:[56.8 77.2 80.8]",
    "[silencedetect @ 0x564a88e8a300] silence_start: 1.00267",
    "[silencedetect @ 0x564a88e8a300] silence_end: 2.00533 | silence_duration: 1.00267",
    "[silencedetect @ 0x564a88e8a300] silence_start: 5.5",
    "",
  ].join("\r\n");
  assert.deepEqual(parseCuts(stderr), [
    { t: 2, score: 0.4 },
    { t: 3.52, score: 0.801 },
  ]);
  // Times are shifted by the range start when ffmpeg was seeked; scores that do not line up with showinfo are dropped.
  assert.deepEqual(parseCuts(stderr, 1800).map((c) => c.t), [1802, 1803.52]);
  assert.deepEqual(parseCuts(stderr.replace("frame:1    pts:45056   pts_time:3.52", "frame:1    pts:45056   pts_time:3.0")), [
    { t: 2, score: null },
    { t: 3.52, score: null },
  ]);
  assert.deepEqual(parseSilences(stderr, 0, 6), [
    [1.003, 2.005],
    [5.5, 6],
  ]);
  assert.deepEqual(parseSilences(stderr, 10), [[11.003, 12.005]]);

  const stdout = [
    "frame:0    pts:0       pts_time:0",
    "lavfi.signalstats.YMIN=81",
    "lavfi.signalstats.YAVG=81",
    "lavfi.signalstats.SATAVG=118",
    "lavfi.signalstats.YDIF=0",
    "frame:1    pts:1       pts_time:0.25",
    "lavfi.signalstats.YAVG=81.5",
    "lavfi.signalstats.SATAVG=118",
    "lavfi.signalstats.YDIF=47.5961",
    "",
  ].join("\n");
  assert.deepEqual(parseMotion(stdout, 2), [
    { t: 2, yavg: 81, satavg: 118, ydif: 0 },
    { t: 2.25, yavg: 81.5, satavg: 118, ydif: 47.5961 },
  ]);
});

test("motion shares leave out the samples that hold a cut, as the probe leaves out its flagged ones", () => {
  const samples = [];
  for (let i = 0; i <= 24; i++) samples.push({ t: i * 0.25, ydif: i * 0.25 <= 2 ? 0.2 : i * 0.25 <= 3.6 ? 50 : 2 });
  // Cuts at 2.0 and 3.6: the sample ending at 3.75 holds 3.6 (it falls in (3.5, 3.75]); 2.0 sits on a
  // grid time, so with half a frame of slack the samples ending at 2.0 and 2.25 are both left out.
  const motion = motionStats(samples, [2, 3.6], 0.25, 0.04);
  assert.equal(motion.samples, 25);
  assert.equal(motion.inside_shots, 21);
  assert.equal(motion.frozen_share, Number((7 / 21).toFixed(3)));
  assert.equal(motion.high_motion_share, Number((5 / 21).toFixed(3)));
  assert.equal(motion.slow_share, Number((9 / 21).toFixed(3)));
  assert.equal(motion.active_share, Number((5 / 21).toFixed(3)));
  // Without slack the cut on the grid time is in one sample only.
  assert.equal(motionStats(samples, [2, 3.6], 0.25, 0).inside_shots, 22);
  assert.deepEqual(motionStats([{ t: 0, ydif: 0 }], [], 0.25).frozen_share, null);
});

test("sound is silence clipped to the range; non-silence is any sound", () => {
  const sound = soundStats([[-1, 1], [4.5, 5.2], [9, 12]], 0, 10, DEFAULTS);
  assert.equal(sound.silent_seconds, 2.7);
  assert.equal(sound.silent_share, 0.27);
  assert.equal(sound.non_silent_share, 0.73);
  assert.equal(sound.silences, 3);
  assert.equal(sound.longest_silence, 1);
  assert.deepEqual(sound.silence_times, [[0, 1], [4.5, 5.2], [9, 10]]);
});

test("the filter graph is one pass: cuts at the floor with showinfo, motion at the probe's grid, silence only with sound", () => {
  const graph = filterGraph(DEFAULTS, true);
  assert.match(graph, /\[cuts\]select='gt\(scene,0\.1\)',metadata=print:key=lavfi\.scene_score,showinfo\[cutsout\]/);
  assert.match(graph, /\[motion\]fps=4,scale=64:64:flags=area,crop=64:47:0:0,signalstats,metadata=print:file=-\[motionout\]/);
  assert.match(graph, /\[0:a\]silencedetect=noise=-30dB:d=0\.5\[soundout\]/);
  assert.doesNotMatch(filterGraph(DEFAULTS, false), /silencedetect/);
  assert.match(filterGraph({ ...DEFAULTS, scene: 0.05, step: 0.125 }, false), /gt\(scene,0\.05\)/);
  assert.match(filterGraph({ ...DEFAULTS, step: 0.125 }, false), /fps=8,/);
});

test("options have the documented defaults and refuse what cannot be measured", () => {
  const options = parseArgs(["--file", "a.mp4"], {});
  assert.equal(options.scene, 0.3);
  assert.equal(options.floor, 0.1);
  assert.equal(options.step, 0.25);
  assert.equal(options.silenceDb, -30);
  assert.equal(options.silenceMin, 0.5);
  assert.equal(options.tolerance, 0.3);
  assert.equal(options.ytDlp, "yt-dlp");
  assert.deepEqual(options.ranges, []);
  assert.equal(parseArgs(["--url", "xVXEefk1vWs"], { YT_DLP_PATH: "C:\\tools\\yt-dlp.exe" }).ytDlp, "C:\\tools\\yt-dlp.exe");
  assert.deepEqual(parseArgs(["--file", "a.mp4", "--range", "0-120", "--range", "1800-", "--scene", "0.4", "--keep"], {}).ranges, [[0, 120], [1800, null]]);
  for (const [argv, reason] of [
    [[], /exactly one of --file and --url/],
    [["--file", "a.mp4", "--url", "b"], /exactly one/],
    [["--file", "a.mp4", "--scene", "2"], /--scene/],
    [["--file", "a.mp4", "--step", "0"], /--step/],
    [["--file", "a.mp4", "--range"], /--range needs a value/],
    [["--file", "a.mp4", "--bogus"], /unknown option --bogus/],
  ]) {
    assert.throws(() => parseArgs(argv, {}), reason, argv.join(" "));
  }
});

test("a frame shape is written the way the study records write it", () => {
  assert.equal(frameShape(640, 360), "16:9");
  assert.equal(frameShape(360, 640), "9:16");
  assert.equal(frameShape(854, 366), "2.33:1");
  assert.equal(frameShape(1920, 1080), "16:9");
});

test("the JSON keeps every list of numbers on one line, as the study records are written", () => {
  const text = formatJson({ a: [1, 2.5, 3], b: [[2, 0.51], [3.6, 0.38]], c: { d: null, e: undefined, f: "x" }, g: [{ h: 1 }], i: [] });
  assert.equal(text, '{\n  "a": [1, 2.5, 3],\n  "b": [[2, 0.51], [3.6, 0.38]],\n  "c": {\n    "d": null,\n    "f": "x"\n  },\n  "g": [\n    {\n      "h": 1\n    }\n  ],\n  "i": []\n}');
  assert.deepEqual(JSON.parse(text), { a: [1, 2.5, 3], b: [[2, 0.51], [3.6, 0.38]], c: { d: null, f: "x" }, g: [{ h: 1 }], i: [] });
});

test("yt-dlp is called as a program, never imported or bundled", () => {
  assert.doesNotMatch(SOURCE, /from\s+["'][^"']*yt[-_]?dlp/);
  assert.doesNotMatch(SOURCE, /require\(/);
  assert.match(SOURCE, /spawn\(file, args/);
  assert.match(SOURCE, /"--print", "after_move:filepath"/);
});

// --- With ffmpeg: a lavfi-made clip, 160x120 at 25 fps: red 0-2 s, a rotating test pattern 2-3.6 s,
// blue 3.6-6 s; a 440 Hz tone silent at 1-2 s and 4.5-5.2 s. Cuts at 2.0 and 3.6 s, exactly on frames.
const box = tools ? mkdtempSync(path.join(tmpdir(), "reference-analysis-test-")) : null;
after(() => {
  if (box) rmSync(box, { recursive: true, force: true });
});

let clipPromise = null;
function clip() {
  clipPromise ??= (async () => {
    const file = path.join(box, "synthetic.mp4");
    const made = spawnSync(
      tools.ffmpeg,
      [
        "-hide_banner", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=red:size=160x120:rate=25:duration=2",
        "-f", "lavfi", "-i", "testsrc2=size=160x120:rate=25:duration=1.6,rotate=PI*t:fillcolor=black",
        "-f", "lavfi", "-i", "color=c=blue:size=160x120:rate=25:duration=2.4",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=6",
        "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v];[3:a]volume='if(between(t,1,2)+between(t,4.5,5.2),0,1)':eval=frame[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", file,
      ],
      { encoding: "utf8", windowsHide: true },
    );
    assert.equal(made.status, 0, made.stderr);
    const silent = path.join(box, "no-audio.mp4");
    const stripped = spawnSync(tools.ffmpeg, ["-hide_banner", "-y", "-loglevel", "error", "-i", file, "-an", "-c:v", "copy", silent], { encoding: "utf8", windowsHide: true });
    assert.equal(stripped.status, 0, stripped.stderr);
    return { file, silent };
  })();
  return clipPromise;
}

function runScript(args, env = {}) {
  const result = spawnSync(process.execPath, [SCRIPT, ...args], { encoding: "utf8", windowsHide: true, env: { ...process.env, ...env } });
  return { ...result, record: result.status === 0 && result.stdout.trim().startsWith("{") ? JSON.parse(result.stdout) : null };
}

test("a clip with two cuts, a moving shot and two silences is measured as made", withFfmpeg, async () => {
  const { file } = await clip();
  const out = path.join(box, "whole.json");
  const result = runScript(["--file", file, "--out", out]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, "");
  assert.match(result.stderr, /synthetic 0-6 s: 3 shots, median 2 s, p10-p90 1\.6-2\.4 s, longest 2\.4 s, over 6 s: 0, opening 10\/30 s: 3\/3 \(scene 0\.3\)/);
  assert.match(result.stderr, /sound: non-silent 7\d(\.\d)?% \(-30 dB, 0\.5 s\); 2 silences, longest 1 s/);
  const record = JSON.parse(readFileSync(out, "utf8"));
  assert.equal(record.schema_version, 1);
  assert.match(record.checked_on, /^\d{4}-\d{2}-\d{2}$/);
  assert.equal(record.method.tool, ".agents/skills/youtube-video/scripts/reference_analysis.mjs");
  assert.equal(record.method.step_seconds, 0.25);
  assert.match(record.method.cut_rule, /gt\(scene,0\.3\)/);
  assert.match(record.method.sound_rule, /upper bound on speech/);
  const [video] = record.videos;
  assert.equal(video.id, "synthetic");
  assert.equal(video.url, null);
  assert.equal(video.frame, "4:3");
  assert.equal(video.stream, "160x120");
  assert.equal(video.fps, 25);
  assert.equal(video.duration_seconds, 6);
  assert.deepEqual({ ...video.source, sha256: video.source.sha256.length }, { file: "synthetic.mp4", bytes: video.source.bytes, sha256: 64, container: "mov,mp4,m4a,3gp,3g2,mj2", codec: "h264", audio: true, downloaded: false });
  const [range] = video.ranges;
  assert.deepEqual(range.range, [0, 6]);
  assert.deepEqual(range.cuts, [2, 3.6]);
  assert.deepEqual(range.lengths, [2, 1.6, 2.4]);
  assert.deepEqual([range.shots, range.mean, range.median, range.p10, range.p90, range.longest, range.over_6s, range.opening_10s, range.opening_30s, range.spread_p90_over_p10], [3, 2, 2, 1.6, 2.4, 2.4, 0, 3, 3, 1.5]);
  // Every candidate at or above the floor is listed with its score; the two cuts clear the threshold.
  const scored = Object.fromEntries(range.scene_scores);
  assert.ok(scored[2] >= 0.3 && scored[3.6] >= 0.3, JSON.stringify(range.scene_scores));
  assert.ok(range.scene_scores.every(([, score]) => score >= 0.1));
  assert.equal(range.scene_threshold, 0.3);
  // 24 samples; the first has nothing before it and the two that hold a cut are left out.
  assert.equal(range.motion.samples, 24);
  assert.ok(range.motion.inside_shots >= 20 && range.motion.inside_shots <= 21, String(range.motion.inside_shots));
  near(range.motion.frozen_share, 0.75, 0.06, "frozen share: the red and blue shots");
  near(range.motion.high_motion_share, 0.25, 0.06, "high motion share: the rotating shot");
  assert.equal(range.motion.slow_share, 0);
  assert.equal(range.near_frozen_share, range.motion.frozen_share);
  assert.equal(range.high_motion_share, range.motion.high_motion_share);
  assert.ok(range.motion.mean_difference > 5);
  assert.ok(range.picture.luma_mean > 40 && range.picture.luma_mean < 100, String(range.picture.luma_mean));
  assert.ok(range.picture.luma_p10 <= range.picture.luma_mean && range.picture.luma_mean <= range.picture.luma_p90);
  assert.ok(range.picture.saturation_mean > 0);
  assert.equal(range.sound.silences, 2);
  near(range.sound.silent_seconds, 1.7, 0.05, "silent seconds");
  near(range.sound.non_silent_share, 0.717, 0.01, "non-silent share");
  near(range.sound.silence_times[0][0], 1, 0.02, "first silence starts");
  near(range.sound.silence_times[0][1], 2, 0.02, "first silence ends");
  near(range.sound.silence_times[1][0], 4.5, 0.02, "second silence starts");
  near(range.sound.silence_times[1][1], 5.2, 0.02, "second silence ends");
  assert.equal(range.sound.longest_silence, 1);
  // The file itself keeps every list on one line.
  assert.match(readFileSync(out, "utf8"), /\n {10}"lengths": \[2, 1\.6, 2\.4\],\n/);
});

test("ranges are measured where they are asked, times stay absolute, and the end is clamped to the file", withFfmpeg, async () => {
  const { file } = await clip();
  const result = runScript(["--file", file, "--range", "1-5", "--range", "3-", "--range", "0-99"]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stderr, /range 0-99: the file ends at 6 s, measuring to there/);
  const ranges = result.record.videos[0].ranges;
  assert.deepEqual(ranges.map((r) => [r.range, r.cuts, r.lengths]), [
    [[1, 5], [2, 3.6], [1, 1.6, 1.4]],
    [[3, 6], [3.6], [0.6, 2.4]],
    [[0, 6], [2, 3.6], [2, 1.6, 2.4]],
  ]);
  assert.deepEqual(ranges[0].sound.silence_times.map(([a, b]) => [Math.round(a * 10) / 10, Math.round(b * 10) / 10]), [[1, 2]]);
  assert.deepEqual(ranges[1].sound.silence_times.map(([a, b]) => [Math.round(a * 10) / 10, Math.round(b * 10) / 10]), [[4.5, 5.2]]);
  assert.ok(ranges[1].motion.frozen_share > 0.7, "the blue shot is frozen");
  // A range beyond the file is refused.
  const refused = runScript(["--file", file, "--range", "6-10", "--quiet"]);
  assert.equal(refused.status, 1);
  assert.match(refused.stderr, /range 6-10: starts at or after the end of the file/);
});

test("a higher threshold drops a cut from the list but not from the scores, and no sound gives no sound block", withFfmpeg, async () => {
  const { file, silent } = await clip();
  const strict = runScript(["--file", file, "--scene", "0.45", "--quiet"]);
  assert.equal(strict.status, 0, strict.stderr);
  const [range] = strict.record.videos[0].ranges;
  assert.deepEqual(range.cuts, [2]);
  assert.equal(range.scene_threshold, 0.45);
  assert.ok(range.scene_scores.some(([t]) => t === 3.6), "the 3.6 s candidate stays in scene_scores");
  const noSound = runScript(["--file", silent]);
  assert.equal(noSound.status, 0, noSound.stderr);
  assert.match(noSound.stderr, /no audio\)/);
  assert.match(noSound.stderr, /sound: no audio stream/);
  assert.equal(noSound.record.videos[0].source.audio, false);
  assert.equal(noSound.record.videos[0].ranges[0].sound, null);
  assert.deepEqual(noSound.record.videos[0].ranges[0].cuts, [2, 3.6]);
});

test("--compare matches the measured cuts against a study record's lists", withFfmpeg, async () => {
  const { file } = await clip();
  const study = path.join(box, "study.json");
  writeFileSync(
    study,
    JSON.stringify({
      videos: [{ id: "synthetic", ranges: [{ range: [0, 6], lengths: [2, 1.5, 2.5] }] }],
      cross_check: [{ id: "synthetic", verifier_cut_times: [2.25, 3.5, 5] }],
    }),
  );
  const result = runScript(["--file", file, "--compare", study]);
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(
    result.record.comparison.map((c) => [c.list, c.covered, c.recorded, c.matched, c.only_here, c.only_recorded]),
    [
      ["ranges 0-6 lengths", [0, 6], 2, 2, [], []],
      ["cross_check verifier_cut_times", [0, 5], 2, 2, [], []],
    ],
  );
  assert.match(result.stderr, /compared with ranges 0-6 lengths over 0-6 s: 2 of 2 recorded cuts matched within 0\.3 s; 0 only here, 0 only recorded/);
  const strange = runScript(["--file", file, "--compare", study, "--tolerance", "0.05"]);
  assert.equal(strange.status, 0, strange.stderr);
  assert.deepEqual(strange.record.comparison.map((c) => [c.matched, c.only_here, c.only_recorded]), [[1, [3.6], [3.5]], [0, [2, 3.6], [2.25, 3.5]]]);
  // A range with no cuts on either side still reports every list that covers it.
  const other = runScript(["--file", file, "--compare", study, "--range", "4-6"]);
  assert.equal(other.status, 0, other.stderr);
  assert.deepEqual(other.record.comparison, [
    { range: [4, 6], list: "ranges 0-6 lengths", covered: [4, 6], tolerance: 0.3, recorded: 0, here: 0, matched: 0, only_here: [], only_recorded: [] },
    { range: [4, 6], list: "cross_check verifier_cut_times", covered: [4, 5], tolerance: 0.3, recorded: 0, here: 0, matched: 0, only_here: [], only_recorded: [] },
  ]);
});

/** A stand-in yt-dlp: a POSIX script that runs a small node program copying the clip and writing an info JSON. */
function standIn(file, log) {
  const program = path.join(box, "stand-in.mjs");
  writeFileSync(
    program,
    [
      'import { copyFileSync, writeFileSync } from "node:fs";',
      'import path from "node:path";',
      "const args = process.argv.slice(2);",
      'const template = args[args.indexOf("-o") + 1];',
      "const url = args[args.length - 1];",
      'const id = new URL(url).searchParams.get("v");',
      "const dir = path.dirname(template);",
      "const file = path.join(dir, `${id}.mp4`);",
      `copyFileSync(${JSON.stringify(file)}, file);`,
      'writeFileSync(path.join(dir, `${id}.info.json`), JSON.stringify({ id, title: "A test", channel: "Test channel", upload_date: "20260912", view_count: 123, duration: 6, webpage_url: url, formats: [{ height: 360 }, { height: 720 }], subtitles: { "zh-Hant": [] }, automatic_captions: { en: [] }, _version: { version: "stand-in" } }));',
      `writeFileSync(${JSON.stringify(log)}, JSON.stringify({ args, dir }));`,
      "console.log(file);",
    ].join("\n"),
  );
  const script = path.join(box, "stand-in-yt-dlp");
  writeFileSync(script, `#!/bin/sh\nexec ${JSON.stringify(process.execPath)} ${JSON.stringify(program)} "$@"\n`);
  chmodSync(script, 0o755);
  return script;
}

test("--url calls yt-dlp for the file and its metadata, measures it, and deletes the download unless --keep", withStandIn, async () => {
  const { file } = await clip();
  const log = path.join(box, "stand-in.json");
  const script = standIn(file, log);
  const result = runScript(["--url", "https://youtu.be/abcdefghijk?t=3", "--yt-dlp", script]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stderr, /fetching https:\/\/www\.youtube\.com\/watch\?v=abcdefghijk with .*stand-in-yt-dlp into a temporary directory/);
  const called = JSON.parse(readFileSync(log, "utf8"));
  assert.equal(called.args[called.args.length - 1], "https://www.youtube.com/watch?v=abcdefghijk");
  for (const flag of ["--no-playlist", "--no-simulate", "--write-info-json", "--merge-output-format"]) assert.ok(called.args.includes(flag), flag);
  assert.deepEqual(called.args.slice(called.args.indexOf("--print"), called.args.indexOf("--print") + 2), ["--print", "after_move:filepath"]);
  assert.equal(called.args[called.args.indexOf("-f") + 1], FORMAT);
  assert.ok(called.args[called.args.indexOf("-o") + 1].endsWith(`${path.sep}%(id)s.%(ext)s`));
  assert.equal(existsSync(called.dir), false, "the temporary directory is deleted after the run");
  const [video] = result.record.videos;
  assert.equal(video.id, "abcdefghijk");
  assert.equal(video.url, "https://www.youtube.com/watch?v=abcdefghijk");
  assert.equal(video.title, "A test");
  assert.equal(video.channel, "Test channel");
  assert.equal(video.published, "2026-09-12");
  assert.equal(video.views_at_check, 123);
  assert.equal(video.highest_quality, "720p");
  assert.deepEqual(video.caption_tracks, ["zh-Hant"]);
  assert.equal(video.source.downloaded, true);
  assert.equal(video.source.file, "abcdefghijk.mp4");
  assert.equal(result.record.method.yt_dlp, "stand-in");
  assert.match(result.record.method.where, /deleted/);
  assert.deepEqual(video.ranges[0].cuts, [2, 3.6]);

  const kept = runScript(["--url", "abcdefghijk", "--yt-dlp", script, "--keep", "--quiet"]);
  assert.equal(kept.status, 0, kept.stderr);
  const keptCall = JSON.parse(readFileSync(log, "utf8"));
  assert.ok(existsSync(path.join(keptCall.dir, "abcdefghijk.mp4")), "--keep leaves the download in place");
  assert.match(kept.stderr, /^kept .*abcdefghijk\.mp4\s*$/m);
  rmSync(keptCall.dir, { recursive: true, force: true });
});

test("a missing yt-dlp is reported with how to get it, and the file path is never read from the repository", withFfmpeg, () => {
  const result = runScript(["--url", "abcdefghijk", "--yt-dlp", path.join(box, "no-such-yt-dlp")]);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /no-such-yt-dlp was not found: install yt-dlp .* never bundled/);
});
