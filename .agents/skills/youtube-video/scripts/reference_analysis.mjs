#!/usr/bin/env node
// Offline measurement of a reference video for the drama craft studies in docs/videos/drama-craft/:
// how often it cuts, how much the picture moves between samples, how bright it is, and how much of
// its sound is not silence. ffmpeg does all the measuring, frame by frame, on a file of any length.
// A YouTube video is fetched first by calling yt-dlp as a separate program (it is never bundled:
// Unlicense, and whether to download at all is the owner's call under YouTube's terms). The
// download goes to a temporary directory that is deleted after the run unless --keep is given;
// only the numbers in the JSON are meant for the repository.
//
//   node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <video> [--range 0-240]... [--out <json>]
//   node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url <YouTube id or URL> [--range 0-120] --out <json>
//
// Options
//   --range A-B       seconds to measure, repeatable; B may be left out (to the end); default the whole file
//   --scene T         cut threshold for select='gt(scene,T)' (default 0.3; ffmpeg documents 0.3-0.5)
//   --floor F         lowest score kept in scene_scores (default 0.1), so a lower threshold can be judged without decoding again
//   --step S          seconds between motion samples (default 0.25, the browser probe's step)
//   --silence-db D    silencedetect noise level in dB (default -30)
//   --silence-min S   shortest silence counted, in seconds (default 0.5)
//   --compare <json>  a study record under docs/videos/drama-craft/ (reference-study-*.json): every cut list it holds for
//                     this video id is matched against the cuts measured here, within --tolerance seconds (default 0.3)
//   --yt-dlp <path>   the yt-dlp to call (default: YT_DLP_PATH, else yt-dlp on PATH); ffmpeg is found the way the
//                     video tools find it (FFMPEG_PATH, PATH, the winget package on Windows)
//   --keep            keep the downloaded file (its path is printed) instead of deleting the temporary directory
//   --quiet           no progress or summary on stderr
//
// The JSON goes to --out, or to stdout without it; progress and the summary go to stderr. Exit code 0 on
// success, 2 for a usage error, 1 when a tool is missing or fails.
//
// What the numbers are, how they compare with yt_shot_probe.js, and what they do not show is in
// .agents/skills/youtube-video/references/drama-craft.md (section 8) and docs/videos/drama-craft/README.md.
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

import { locateFfmpeg, ToolMissing } from "../../../../tools/video/assemble/ffmpeg.mjs";

export const TOOL = ".agents/skills/youtube-video/scripts/reference_analysis.mjs";
export const DEFAULTS = Object.freeze({ scene: 0.3, floor: 0.1, step: 0.25, silenceDb: -30, silenceMin: 0.5, tolerance: 0.3, grid: 64, keep: 0.74 });
// The browser probe's motion classes, mean absolute luma difference between samples: under 1 frozen,
// 1-4 slow, over 4 active; 20 or more changes as much as many cuts do.
export const MOTION = Object.freeze({ frozen: 1, slow: 4, high: 20 });
// yt-dlp format: one progressive file at or under 480p when there is one (YouTube's 360p mp4 as a
// rule), else the best video and audio under 480p merged into mp4. Cut detection needs no more, and
// the browser probe read the same 360p streams.
export const FORMAT = "b[height<=480][ext=mp4]/b[height<=480]/bv*[height<=480]+ba/b";

const LINE = /\r?\n/;
const round = (value, digits) => (value === null || value === undefined || !Number.isFinite(value) ? null : Number(value.toFixed(digits)));
const mean = (values) => (values.length ? values.reduce((sum, x) => sum + x, 0) / values.length : null);

/** The quantile yt_shot_probe.js, lint and the craft check use, on an ascending list. */
export const quantile = (sorted, p) => sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))];

/** The 11-character id of a YouTube watch, short, embed or youtu.be link, of a bare id, or null. */
export function youtubeId(text) {
  const given = String(text ?? "").trim();
  const valid = (id) => (/^[\w-]{11}$/.test(id ?? "") ? id : null);
  if (valid(given)) return given;
  let url;
  try {
    url = new URL(given);
  } catch {
    return null;
  }
  const host = url.hostname.toLowerCase().replace(/^(www|m|music)\./, "");
  if (host === "youtu.be") return valid(url.pathname.split("/")[1]);
  if (!/^(youtube\.com|youtube-nocookie\.com)$/.test(host)) return null;
  const v = url.searchParams.get("v");
  if (v) return valid(v);
  const match = /^\/(?:shorts|embed|live|v)\/([\w-]{11})(?:[/?]|$)/.exec(url.pathname);
  return match ? match[1] : null;
}

/** "A-B" in seconds, "A-" to the end, "-B" from the start: [from, to | null]. */
export function parseRange(text) {
  const match = /^(\d+(?:\.\d+)?)?-(\d+(?:\.\d+)?)?$/.exec(String(text ?? "").trim());
  if (!match || (match[1] === undefined && match[2] === undefined)) throw new Error(`--range wants A-B in seconds (B may be left out), not "${text}"`);
  const from = match[1] === undefined ? 0 : Number(match[1]);
  const to = match[2] === undefined ? null : Number(match[2]);
  if (to !== null && to <= from) throw new Error(`--range ${text}: the end must come after the start`);
  return [from, to];
}

/**
 * One ffmpeg pass does everything, so a long file is decoded once. The cut chain selects every
 * frame whose scene score reaches the floor, prints the score (stderr) and the frame (showinfo,
 * stderr), then consumes it in nullsink. A valid range may have no cut candidates: mapping that
 * branch to an encoded output makes ffmpeg fail when its encoder receives no frame before EOF.
 * The measurements live in the logs and need no encoded cut stream. The motion chain samples
 * the picture every `step` seconds, shrinks it to a grid, drops
 * the bottom rows where burned-in subtitles change, and prints signalstats (stdout); the sound
 * chain runs silencedetect (stderr). Only the floor is in the graph: the threshold is applied to
 * the recorded scores afterwards, so the same pass answers for any threshold above the floor.
 */
export function filterGraph(options, audio) {
  const { scene, floor, step, grid, keep } = options;
  const rows = Math.max(1, Math.floor(grid * keep));
  const rate = Math.round(1e6 / step) / 1e6;
  const chains = [
    "[0:v]split=2[cuts][motion]",
    `[cuts]select='gt(scene,${Math.min(scene, floor)})',metadata=print:key=lavfi.scene_score,showinfo,nullsink`,
    `[motion]fps=${rate},scale=${grid}:${grid}:flags=area,crop=${grid}:${rows}:0:0,signalstats,metadata=print:file=-[motionout]`,
  ];
  if (audio) chains.push(`[0:a]silencedetect=noise=${options.silenceDb}dB:d=${options.silenceMin}[soundout]`);
  return chains.join(";");
}

/** Selected frames from ffmpeg's stderr: time (showinfo) and scene score (metadata), in order. */
export function parseCuts(stderr, from = 0) {
  const times = [];
  const scored = [];
  let pending = null;
  for (const line of stderr.split(LINE)) {
    let match;
    if ((match = /^\[Parsed_showinfo_\d+ @ [^\]]*\] n:\s*\d+\s+pts:\s*-?\d+\s+pts_time:(\S+)/.exec(line))) {
      times.push(Number(match[1]));
    } else if ((match = /^\[Parsed_metadata_\d+ @ [^\]]*\] frame:\s*\d+\s+pts:\s*-?\d+\s+pts_time:(\S+)/.exec(line))) {
      pending = Number(match[1]);
    } else if (pending !== null && (match = /^\[Parsed_metadata_\d+ @ [^\]]*\] lavfi\.scene_score=(\S+)/.exec(line))) {
      scored.push({ t: pending, score: Number(match[1]) });
      pending = null;
    }
  }
  // showinfo is the frame list; the scores belong to the same frames in the same order.
  const same = scored.length === times.length && scored.every((entry, index) => Math.abs(entry.t - times[index]) < 1e-3);
  return times.map((t, index) => ({ t: round(t + from, 3), score: same ? round(scored[index].score, 3) : null }));
}

/** Motion samples from ffmpeg's stdout: time, YDIF (luma change since the sample before), YAVG, SATAVG. */
export function parseMotion(stdout, from = 0) {
  const samples = [];
  let current = null;
  for (const line of stdout.split(LINE)) {
    let match;
    if ((match = /^frame:\s*\d+\s+pts:\s*-?\d+\s+pts_time:(\S+)/.exec(line))) {
      current = { t: round(Number(match[1]) + from, 3) };
      samples.push(current);
    } else if (current && (match = /^lavfi\.signalstats\.(YDIF|YAVG|SATAVG)=(\S+)/.exec(line))) {
      current[match[1].toLowerCase()] = Number(match[2]);
    }
  }
  return samples;
}

/** Silences from ffmpeg's stderr as [start, end] in absolute seconds; one still open at the end closes at `to`. */
export function parseSilences(stderr, from = 0, to = null) {
  const found = [];
  let open = null;
  for (const line of stderr.split(LINE)) {
    let match;
    if ((match = /silence_start:\s*(-?[\d.]+)/.exec(line))) open = Math.max(from, Number(match[1]) + from);
    else if (open !== null && (match = /silence_end:\s*(-?[\d.]+)/.exec(line))) {
      found.push([round(open, 3), round(Number(match[1]) + from, 3)]);
      open = null;
    }
  }
  if (open !== null && to !== null && to > open) found.push([round(open, 3), round(to, 3)]);
  return found;
}

/** The shot statistics yt_shot_probe.js's stats() writes, from cut times inside [from, to]. */
export function shotStats(cuts, from, to) {
  const inside = [...cuts].filter((t) => t > from && t < to).sort((a, b) => a - b);
  const edges = [from, ...inside, to];
  const lengths = edges.slice(1).map((t, index) => round(t - edges[index], 2));
  const sorted = [...lengths].sort((a, b) => a - b);
  const p10 = quantile(sorted, 0.1);
  const p90 = quantile(sorted, 0.9);
  const starts = edges.slice(0, -1);
  return {
    range: [from, to],
    shots: lengths.length,
    mean: round((to - from) / lengths.length, 2),
    median: quantile(sorted, 0.5),
    p10,
    p90,
    longest: sorted[sorted.length - 1],
    over_6s: lengths.filter((x) => x > 6).length,
    opening_10s: starts.filter((t) => t < from + 10).length,
    opening_30s: starts.filter((t) => t < from + 30).length,
    spread_p90_over_p10: p10 > 0 ? round(p90 / p10, 2) : null,
    cuts: inside,
    lengths,
  };
}

/**
 * Motion shares over the samples inside shots. A sample at t measures the change over
 * (t - step, t]; one that holds a cut is left out, as the probe leaves out its flagged samples,
 * with half a source frame of slack because the fps filter takes the frame nearest each grid time,
 * so a cut that close to a grid time is left out of both neighbouring samples.
 */
export function motionStats(samples, cuts, step, frameSeconds = 0) {
  const sorted = [...cuts].sort((a, b) => a - b);
  const slack = frameSeconds / 2;
  const inside = [];
  let k = 0;
  for (const sample of samples.slice(1)) {
    while (k < sorted.length && sorted[k] <= sample.t - step - slack) k += 1;
    const holdsCut = k < sorted.length && sorted[k] <= sample.t + slack;
    if (!holdsCut && Number.isFinite(sample.ydif)) inside.push(sample.ydif);
  }
  const share = (keep) => (inside.length ? round(inside.filter(keep).length / inside.length, 3) : null);
  return {
    samples: samples.length,
    inside_shots: inside.length,
    step_seconds: step,
    frozen_share: share((x) => x < MOTION.frozen),
    slow_share: share((x) => x >= MOTION.frozen && x <= MOTION.slow),
    active_share: share((x) => x > MOTION.slow),
    high_motion_share: share((x) => x >= MOTION.high),
    mean_difference: round(mean(inside), 2),
  };
}

/** Brightness and colour over every sample: mean luma (0-255), its 10th and 90th percentiles, mean saturation. */
export function pictureStats(samples) {
  const luma = samples.map((s) => s.yavg).filter(Number.isFinite).sort((a, b) => a - b);
  const saturation = samples.map((s) => s.satavg).filter(Number.isFinite);
  return {
    luma_mean: round(mean(luma), 1),
    luma_p10: luma.length ? round(quantile(luma, 0.1), 1) : null,
    luma_p90: luma.length ? round(quantile(luma, 0.9), 1) : null,
    saturation_mean: round(mean(saturation), 1),
  };
}

/** Silence over [from, to]: seconds, shares and the list; non-silence is sound of any kind. */
export function soundStats(silences, from, to, { silenceDb, silenceMin }) {
  const clipped = silences.map(([a, b]) => [Math.max(a, from), Math.min(b, to)]).filter(([a, b]) => b > a);
  const silent = clipped.reduce((sum, [a, b]) => sum + (b - a), 0);
  const total = to - from;
  return {
    silence_db: silenceDb,
    min_silence_seconds: silenceMin,
    silent_seconds: round(silent, 2),
    silent_share: round(silent / total, 3),
    non_silent_share: round(1 - silent / total, 3),
    silences: clipped.length,
    longest_silence: clipped.length ? round(Math.max(...clipped.map(([a, b]) => b - a)), 2) : 0,
    silence_times: clipped.map(([a, b]) => [round(a, 2), round(b, 2)]),
  };
}

/** Two cut lists matched one to one within `tolerance` seconds; what is left on either side is listed. */
export function compareCuts(here, recorded, tolerance = DEFAULTS.tolerance) {
  const mine = [...here].sort((a, b) => a - b);
  const theirs = [...recorded].sort((a, b) => a - b);
  const used = new Set();
  const onlyRecorded = [];
  // A gap of exactly the tolerance counts; 1.3 - 1.0 is a hair over 0.3 in floating point.
  const within = tolerance + 1e-9;
  let matched = 0;
  for (const t of theirs) {
    let best = -1;
    let bestGap = Infinity;
    for (let i = 0; i < mine.length; i++) {
      if (mine[i] > t + within) break;
      if (used.has(i)) continue;
      const gap = Math.abs(mine[i] - t);
      if (gap <= within && gap < bestGap) {
        best = i;
        bestGap = gap;
      }
    }
    if (best >= 0) {
      used.add(best);
      matched += 1;
    } else onlyRecorded.push(t);
  }
  return { tolerance, recorded: theirs.length, here: mine.length, matched, only_here: mine.filter((_, i) => !used.has(i)), only_recorded: onlyRecorded };
}

/**
 * The cut lists a study record holds for a video id: the cumulative `lengths` of each measured
 * range (as yt_shot_probe.js's stats() wrote them; the last edge is the range end or where a cut
 * list was truncated, not a cut), the start times of a per-shot table, and a cross-check
 * verifier's cut times. Each comes with the seconds it covers.
 */
export function recordedCuts(study, id) {
  const lists = [];
  for (const video of study.videos ?? []) {
    if (video.id !== id) continue;
    for (const entry of video.ranges ?? []) {
      if (!Array.isArray(entry.range) || !Array.isArray(entry.lengths) || !entry.lengths.length) continue;
      let t = entry.range[0];
      const edges = entry.lengths.map((length) => (t = round(t + length, 2)));
      lists.push({ name: `ranges ${entry.range[0]}-${entry.range[1]} lengths`, covers: [entry.range[0], edges[edges.length - 1]], cuts: edges.slice(0, -1) });
    }
    const column = Array.isArray(video.shot_columns) ? video.shot_columns.indexOf("start") : -1;
    if (column >= 0 && Array.isArray(video.shots) && video.shots.length > 1) {
      const starts = video.shots.map((row) => Number(row[column])).filter(Number.isFinite);
      const end = Number(video.measured_to ?? video.shots[video.shots.length - 1][column + 1]);
      lists.push({ name: "shots start times", covers: [starts[0], Number.isFinite(end) ? end : starts[starts.length - 1]], cuts: starts.slice(1) });
    }
  }
  for (const check of study.cross_check ?? []) {
    if (check.id !== id || !Array.isArray(check.verifier_cut_times) || !check.verifier_cut_times.length) continue;
    const video = (study.videos ?? []).find((entry) => entry.id === id) ?? {};
    const covers = [Number(video.measured_from ?? 0), Number(video.measured_to ?? check.verifier_cut_times[check.verifier_cut_times.length - 1])];
    lists.push({ name: "cross_check verifier_cut_times", covers, cuts: check.verifier_cut_times });
  }
  return lists;
}

/** Every recorded list that overlaps a measured range, compared over the seconds both cover. */
export function compareWithStudy(study, id, measured, tolerance = DEFAULTS.tolerance) {
  const out = [];
  for (const range of measured) {
    for (const list of recordedCuts(study, id)) {
      const from = Math.max(range.range[0], list.covers[0]);
      const to = Math.min(range.range[1], list.covers[1]);
      if (to <= from) continue;
      const within = (t) => t > from && t < to;
      out.push({ range: range.range, list: list.name, covered: [from, to], ...compareCuts(range.cuts.filter(within), list.cuts.filter(within), tolerance) });
    }
  }
  return out;
}

/** JSON with each list of numbers on one line, as the study records are written. */
export function formatJson(value, indent = "") {
  if (Array.isArray(value)) {
    const flat = (item) => item === null || typeof item !== "object";
    const inline = (list) => `[${list.map((item) => (Array.isArray(item) ? inline(item) : JSON.stringify(item))).join(", ")}]`;
    if (value.every((item) => flat(item) || (Array.isArray(item) && item.every(flat)))) return inline(value);
    return `[\n${value.map((item) => `${indent}  ${formatJson(item, `${indent}  `)}`).join(",\n")}\n${indent}]`;
  }
  if (value && typeof value === "object") {
    const entries = Object.entries(value).filter(([, item]) => item !== undefined);
    if (!entries.length) return "{}";
    return `{\n${entries.map(([key, item]) => `${indent}  ${JSON.stringify(key)}: ${formatJson(item, `${indent}  `)}`).join(",\n")}\n${indent}}`;
  }
  return JSON.stringify(value);
}

/** Run a program with an argument list (no shell, so Windows paths and quotes pass through as given). */
export function run(file, args, { stderr = "pipe" } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(file, args, { windowsHide: true, stdio: ["ignore", "pipe", stderr] });
    const out = [];
    const err = [];
    child.stdout.on("data", (chunk) => out.push(chunk));
    if (stderr === "pipe") child.stderr.on("data", (chunk) => err.push(chunk));
    child.on("error", reject);
    child.on("close", (code) => {
      const result = { code, stdout: Buffer.concat(out).toString("utf8"), stderr: Buffer.concat(err).toString("utf8") };
      if (code === 0) resolve(result);
      else {
        const tail = result.stderr.trim().split(LINE).slice(-6).join("\n");
        reject(Object.assign(new Error(`${path.basename(file)} exited with ${code}${tail ? `:\n${tail}` : ""}`), result));
      }
    });
  });
}

const rational = (text) => {
  const [num, den] = String(text ?? "").split("/").map(Number);
  return num > 0 && den > 0 ? num / den : null;
};

/** Stream facts from ffprobe: size, frame rate, duration, whether there is sound. */
export async function probeFile(ffprobe, file) {
  const { stdout } = await run(ffprobe, ["-v", "error", "-print_format", "json", "-show_format", "-show_streams", file]);
  const data = JSON.parse(stdout);
  const streams = data.streams ?? [];
  const video = streams.find((s) => s.codec_type === "video" && s.disposition?.attached_pic !== 1);
  if (!video) throw new Error(`${file}: no video stream`);
  const duration = Number(data.format?.duration ?? video.duration);
  if (!(duration > 0)) throw new Error(`${file}: ffprobe reports no duration`);
  return {
    width: video.width,
    height: video.height,
    fps: rational(video.avg_frame_rate) ?? rational(video.r_frame_rate) ?? 25,
    duration,
    audio: streams.some((s) => s.codec_type === "audio"),
    codec: video.codec_name,
    container: data.format?.format_name,
  };
}

/** "16:9", "9:16" or "2.33:1" from a frame size, as the study records write it. */
export function frameShape(width, height) {
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  const g = gcd(width, height) || 1;
  const named = `${width / g}:${height / g}`;
  return ["16:9", "9:16", "4:3", "3:4", "1:1", "3:2", "2:3"].includes(named) ? named : `${round(width / height, 2)}:1`;
}

function sha256(file) {
  return createHash("sha256").update(readFileSync(file)).digest("hex");
}

/** One range through ffmpeg, in the shape of a study record's ranges[] entry plus the motion, picture and sound blocks. */
export async function analyzeRange(ffmpeg, file, probe, [from, to], options) {
  const args = ["-hide_banner", "-nostats", "-nostdin", "-loglevel", "info"];
  if (from > 0) args.push("-ss", String(from));
  args.push("-t", String(round(to - from, 3)), "-i", file, "-filter_complex", filterGraph(options, probe.audio), "-map", "[motionout]");
  if (probe.audio) args.push("-map", "[soundout]");
  args.push("-f", "null", "-");
  const { stdout, stderr } = await run(ffmpeg, args);
  const candidates = parseCuts(stderr, from).filter((c) => c.t > from && c.t < to);
  const cuts = candidates.filter((c) => c.score === null || c.score >= options.scene).map((c) => c.t);
  const samples = parseMotion(stdout, from);
  const stats = shotStats(cuts, from, to);
  const motion = motionStats(samples, cuts, options.step, 1 / probe.fps);
  return {
    ...stats,
    near_frozen_share: motion.frozen_share,
    high_motion_share: motion.high_motion_share,
    scene_threshold: options.scene,
    scene_scores: candidates.map((c) => [c.t, c.score]),
    motion,
    picture: pictureStats(samples),
    sound: probe.audio ? soundStats(parseSilences(stderr, from, to), from, to, options) : null,
  };
}

/** Fetch one video with yt-dlp into a fresh temporary directory; returns the file, its info JSON and the directory. */
export async function download(target, tools, options, log) {
  const id = youtubeId(target);
  const url = id ? `https://www.youtube.com/watch?v=${id}` : target;
  const dir = mkdtempSync(path.join(tmpdir(), "reference-analysis-"));
  const args = [
    "--no-playlist", "--no-write-playlist-metafiles", "--no-simulate", "--write-info-json", "--print", "after_move:filepath",
    "-f", FORMAT, "--merge-output-format", "mp4", "-o", path.join(dir, "%(id)s.%(ext)s"),
  ];
  if (path.isAbsolute(tools.ffmpeg)) args.push("--ffmpeg-location", path.dirname(tools.ffmpeg));
  args.push(url);
  log(`fetching ${url} with ${options.ytDlp} into a temporary directory (quiet; a long video takes a few minutes)`);
  try {
    const { stdout } = await run(options.ytDlp, args, { stderr: "inherit" });
    const file = stdout.trim().split(LINE).filter(Boolean).pop();
    if (!file || !existsSync(file)) throw new Error("yt-dlp did not print the path of a downloaded file");
    const infoName = readdirSync(dir).find((name) => name.endsWith(".info.json"));
    const info = infoName ? JSON.parse(readFileSync(path.join(dir, infoName), "utf8")) : {};
    return { dir, file, info };
  } catch (error) {
    rmSync(dir, { recursive: true, force: true });
    if (error.code === "ENOENT") {
      throw new ToolMissing(`${options.ytDlp} was not found: install yt-dlp (pip install yt-dlp; Windows: winget install yt-dlp.yt-dlp) or pass --yt-dlp <path>; it is called as a separate program and never bundled`);
    }
    throw error;
  }
}

/** The record in the shape of the study records under docs/videos/drama-craft/ (reference-study-*.json). */
export function buildRecord({ options, tools, file, probe, info, ranges, downloaded }) {
  const id = info.id ?? path.basename(file, path.extname(file));
  const heights = (info.formats ?? []).map((f) => f.height).filter(Number.isFinite);
  const published = /^\d{8}$/.test(info.upload_date ?? "") ? `${info.upload_date.slice(0, 4)}-${info.upload_date.slice(4, 6)}-${info.upload_date.slice(6)}` : null;
  const measured = ranges.map(({ range, ...rest }) => ({ range, ...rest }));
  return {
    schema_version: 1,
    checked_on: new Date().toISOString().slice(0, 10),
    method: {
      tool: TOOL,
      where: downloaded
        ? "offline: yt-dlp fetched the file into a temporary directory, ffmpeg measured it, the file was deleted (or kept outside the repository with --keep); only these numbers are kept"
        : "offline: ffmpeg over a local file; only these numbers are kept",
      ffmpeg: tools.version,
      yt_dlp: info._version?.version ?? null,
      step_seconds: options.step,
      cut_rule: `select='gt(scene,${options.scene})' on every decoded frame: ffmpeg's scene score is min(d, |d - d_prev|) / 100, where d is the mean absolute luma difference (0-255) between a frame and the one before it, so a cut is a jump of at least ${Math.round(options.scene * 100)}/255 that is also a spike against the previous frame pair; the first frame of the new shot is the cut time; scores from ${options.floor} up are listed in scene_scores. A dissolve or a slow wipe can be missed; a flash, an explosion growing or a whip pan can be counted.`,
      motion_rule: `signalstats YDIF between samples ${options.step} s apart on a ${options.grid}x${options.grid} luma downsample without its bottom ${Math.round((1 - options.keep) * 100)}% (where burned-in subtitles change), as the browser probe measured: under ${MOTION.frozen}/255 frozen, ${MOTION.frozen}-${MOTION.slow} slow, over ${MOTION.slow} active, ${MOTION.high} or more as much as a cut; samples that hold a cut are left out. It says how much the frame changes, not what moves.`,
      sound_rule: `silencedetect at ${options.silenceDb} dB for at least ${options.silenceMin} s on the whole mix: non-silence is sound of any kind, so with music under the lines it is an upper bound on speech, not speech.`,
      not_checked: [
        "what the pictures show: shot sizes, faces, inserts, who is speaking",
        "soft transitions whose score stays under the threshold, and whether a counted cut is a flash",
        "whether a non-silent second is speech, music or effects",
        downloaded ? "anything on the page beyond yt-dlp's metadata (title, channel, upload date, views, formats, caption tracks)" : "anything about the video's page: a local file carries no metadata",
      ],
    },
    videos: [
      {
        id,
        url: info.webpage_url ?? (downloaded ? `https://www.youtube.com/watch?v=${id}` : null),
        title: info.title ?? null,
        channel: info.channel ?? info.uploader ?? null,
        published,
        duration_seconds: round(info.duration ?? probe.duration, 0),
        views_at_check: info.view_count ?? null,
        frame: frameShape(probe.width, probe.height),
        stream: `${probe.width}x${probe.height}`,
        fps: round(probe.fps, 3),
        highest_quality: heights.length ? `${Math.max(...heights)}p` : null,
        caption_tracks: Object.keys(info.subtitles ?? {}),
        source: { file: path.basename(file), bytes: statSync(file).size, sha256: sha256(file), container: probe.container ?? null, codec: probe.codec ?? null, audio: probe.audio, downloaded: Boolean(downloaded) },
        ranges: measured,
      },
    ],
  };
}

const percent = (share) => (share === null || share === undefined ? "n/a" : `${round(share * 100, 1)}%`);

/** A few lines per range for the terminal. */
export function summary(record) {
  const lines = [];
  for (const video of record.videos) {
    for (const r of video.ranges) {
      lines.push(
        `${video.id} ${r.range[0]}-${r.range[1]} s: ${r.shots} shots, median ${r.median} s, p10-p90 ${r.p10}-${r.p90} s, longest ${r.longest} s, over 6 s: ${r.over_6s}, opening 10/30 s: ${r.opening_10s}/${r.opening_30s} (scene ${r.scene_threshold})`,
      );
      lines.push(
        `  motion: frozen ${percent(r.motion.frozen_share)}, active ${percent(r.motion.active_share)}, high ${percent(r.motion.high_motion_share)} of ${r.motion.inside_shots} samples inside shots at ${r.motion.step_seconds} s; luma ${r.picture.luma_mean} (p10 ${r.picture.luma_p10}, p90 ${r.picture.luma_p90}), saturation ${r.picture.saturation_mean}`,
      );
      lines.push(
        r.sound
          ? `  sound: non-silent ${percent(r.sound.non_silent_share)} (${r.sound.silence_db} dB, ${r.sound.min_silence_seconds} s); ${r.sound.silences} silences, longest ${r.sound.longest_silence} s`
          : "  sound: no audio stream",
      );
    }
  }
  for (const c of record.comparison ?? []) {
    lines.push(`  compared with ${c.list} over ${c.covered[0]}-${c.covered[1]} s: ${c.matched} of ${c.recorded} recorded cuts matched within ${c.tolerance} s; ${c.only_here.length} only here, ${c.only_recorded.length} only recorded`);
  }
  return lines.join("\n");
}

const USAGE = `usage: node ${TOOL} (--file <video> | --url <YouTube id or URL>) [--range A-B]... [--out <json>]
       [--scene 0.3] [--floor 0.1] [--step 0.25] [--silence-db -30] [--silence-min 0.5]
       [--compare <study.json>] [--tolerance 0.3] [--yt-dlp <path>] [--keep] [--quiet]`;

export function parseArgs(argv, env = process.env) {
  const options = { ...DEFAULTS, file: null, url: null, out: null, ranges: [], compare: null, ytDlp: env.YT_DLP_PATH || "yt-dlp", keepFile: false, quiet: false, help: false };
  const numeric = { "--scene": "scene", "--floor": "floor", "--step": "step", "--silence-db": "silenceDb", "--silence-min": "silenceMin", "--tolerance": "tolerance" };
  const text = { "--file": "file", "--url": "url", "--out": "out", "--compare": "compare", "--yt-dlp": "ytDlp" };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const value = () => {
      if (i + 1 >= argv.length) throw new Error(`${arg} needs a value`);
      return argv[++i];
    };
    if (arg === "--help" || arg === "-h") options.help = true;
    else if (arg === "--keep") options.keepFile = true;
    else if (arg === "--quiet") options.quiet = true;
    else if (arg === "--range") options.ranges.push(parseRange(value()));
    else if (arg in numeric) {
      const given = Number(value());
      if (!Number.isFinite(given)) throw new Error(`${arg} wants a number`);
      options[numeric[arg]] = given;
    } else if (arg in text) options[text[arg]] = value();
    else throw new Error(`unknown option ${arg}`);
  }
  if (options.help) return options;
  if (!options.file === !options.url) throw new Error("give exactly one of --file and --url");
  if (!(options.scene > 0 && options.scene <= 1)) throw new Error("--scene must be above 0 and at most 1");
  if (!(options.floor > 0 && options.floor <= 1)) throw new Error("--floor must be above 0 and at most 1");
  if (!(options.step > 0)) throw new Error("--step must be above 0");
  if (!(options.silenceMin > 0)) throw new Error("--silence-min must be above 0");
  if (!(options.tolerance >= 0)) throw new Error("--tolerance must not be negative");
  return options;
}

export async function main(argv, { stdout = process.stdout, stderr = process.stderr, env = process.env } = {}) {
  const say = (line) => stderr.write(`${line}\n`);
  let options;
  try {
    options = parseArgs(argv, env);
  } catch (error) {
    say(error.message);
    say(USAGE);
    return 2;
  }
  if (options.help) {
    stdout.write(`${USAGE}\n`);
    return 0;
  }
  const note = (line) => {
    if (!options.quiet) say(line);
  };
  let tools;
  try {
    tools = await locateFfmpeg(env);
  } catch (error) {
    say(error.message);
    return 1;
  }
  let temp = null;
  try {
    let file = options.file;
    let info = {};
    if (options.url) {
      temp = await download(options.url, tools, options, note);
      file = temp.file;
      info = temp.info;
    } else if (!existsSync(file)) throw new Error(`${file}: no such file`);
    const probe = await probeFile(tools.ffprobe, file);
    const ranges = (options.ranges.length ? options.ranges : [[0, null]]).map(([from, to]) => {
      let end = to ?? probe.duration;
      if (end > probe.duration + 0.05) {
        note(`range ${from}-${to}: the file ends at ${round(probe.duration, 2)} s, measuring to there`);
        end = probe.duration;
      }
      if (from >= end) throw new Error(`range ${from}-${to}: starts at or after the end of the file (${round(probe.duration, 2)} s)`);
      return [from, round(end, 2)];
    });
    const measured = [];
    for (const range of ranges) {
      note(`measuring ${range[0]}-${range[1]} s of ${path.basename(file)} (${probe.width}x${probe.height}, ${round(probe.fps, 2)} fps${probe.audio ? "" : ", no audio"})`);
      measured.push(await analyzeRange(tools.ffmpeg, file, probe, range, options));
    }
    const record = buildRecord({ options, tools, file, probe, info, ranges: measured, downloaded: Boolean(temp) });
    if (options.compare) {
      const study = JSON.parse(readFileSync(options.compare, "utf8"));
      record.comparison = compareWithStudy(study, record.videos[0].id, measured, options.tolerance);
      if (!record.comparison.length) note(`${options.compare} holds no cut list for ${record.videos[0].id} over the measured seconds`);
    }
    const text = `${formatJson(record)}\n`;
    if (options.out) {
      mkdirSync(path.dirname(path.resolve(options.out)), { recursive: true });
      writeFileSync(options.out, text);
      note(`wrote ${options.out}`);
    } else stdout.write(text);
    note(summary(record));
    return 0;
  } catch (error) {
    say(error instanceof ToolMissing ? error.message : `reference_analysis: ${error.message}`);
    return 1;
  } finally {
    if (temp) {
      if (options.keepFile) say(`kept ${temp.file}`);
      else rmSync(temp.dir, { recursive: true, force: true });
    }
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
