/**
 * Local FFmpeg audio measurement, silence-based slicing, and cutting tools for
 * Mokaair's Flow Music MCP (`mokaair-flow-music`).
 *
 * Implements the exact workflow documented in
 * `docs/videos/explainer-series/music-library/README.md` and
 * `tasks/open/2026-11-17-flow-music.md`:
 *   - Full-decode duration + EBU R128 integrated loudness (`lufs_i`), momentary
 *     max (`lufs_m`), true peak (`peak_dbtp`), and silence count (`silences`).
 *   - Near-silent detection (e.g., `sothatswhy-sfx-splash` at -44.5 LUFS).
 *   - `silencedetect` slicing for Lyria 3.5's ~60s multi-hit SFX & long cues.
 *   - Clean fade-in/fade-out trimming into `*-cut.m4a` / `.wav` with re-measure.
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { sha256File } from "../guards/music-guards.mjs";

export const NEAR_SILENT_LUFS_THRESHOLD = -38;
export const CLIPPING_PEAK_DBTP_THRESHOLD = 0.0;

export function defaultRunFfmpeg(binary, args, { timeoutMs = 120_000 } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(binary, args, {
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });
    let stdout = "";
    let stderr = "";
    let finished = false;
    const timer = setTimeout(() => {
      if (finished) return;
      finished = true;
      try {
        child.kill("SIGTERM");
      } catch {
        // ignore
      }
      reject(new Error(`ffmpeg timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    child.stdout.on("data", (d) => {
      stdout += d.toString("utf8");
    });
    child.stderr.on("data", (d) => {
      stderr += d.toString("utf8");
    });
    child.on("error", (err) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      reject(err);
    });
    child.on("close", (code) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      resolve({ exitCode: code ?? 1, stdout, stderr });
    });
  });
}

/**
 * Parses decoded duration (seconds) from ffmpeg `-progress pipe:1` output.
 */
export function parseDecodedSeconds(progressStdout) {
  const lines = String(progressStdout || "").trim().split(/\r?\n/);
  let micros = null;
  let stamp = null;
  for (const line of lines) {
    const idx = line.indexOf("=");
    if (idx < 0) continue;
    const k = line.slice(0, idx).trim();
    const v = line.slice(idx + 1).trim();
    if (k === "out_time_us" || k === "out_time_ms") {
      const n = Number(v);
      if (Number.isFinite(n) && n > 0) micros = n;
    } else if (k === "out_time") {
      stamp = v;
    }
  }
  if (micros != null) return Number((micros / 1_000_000).toFixed(3));
  const m = /^(\d+):(\d{2}):(\d{2}(?:\.\d+)?)$/.exec(stamp || "");
  if (m) {
    return Number((Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3])).toFixed(3));
  }
  return null;
}

/**
 * Parses EBU R128 Integrated Loudness (`lufs_i`), max momentary (`lufs_m`),
 * and True Peak (`peak_dbtp`) from ffmpeg `ebur128=peak=true` stderr.
 */
export function parseEbur128Summary(stderr) {
  const text = String(stderr || "");
  const intMatch = text.match(/Integrated loudness:[\s\S]*?\bI:\s*(-?\d+(?:\.\d+)?)\s*LUFS/i);
  const peakMatch = text.match(/True peak:[\s\S]*?\bPeak:\s*(-?\d+(?:\.\d+)?)\s*dBFS/i);

  let maxMomentary = null;
  const momentaryRe = /\bM:\s*(-?\d+(?:\.\d+)?)\b/g;
  let m;
  while ((m = momentaryRe.exec(text)) !== null) {
    const val = Number(m[1]);
    if (Number.isFinite(val) && val > -100 && (maxMomentary === null || val > maxMomentary)) {
      maxMomentary = val;
    }
  }

  return {
    lufs_i: intMatch ? Number(Number(intMatch[1]).toFixed(1)) : null,
    lufs_m: maxMomentary != null ? Number(maxMomentary.toFixed(1)) : null,
    peak_dbtp: peakMatch ? Number(Number(peakMatch[1]).toFixed(1)) : null,
  };
}

/**
 * Parses `silencedetect` intervals (`[{ start, end, duration }]`) from ffmpeg stderr.
 */
export function parseSilenceIntervals(stderr, totalSeconds = null) {
  const text = String(stderr || "");
  const intervals = [];
  let currentStart = null;

  for (const line of text.split(/\r?\n/)) {
    const startMatch = line.match(/silence_start:\s*(-?\d+(?:\.\d+)?)/i);
    if (startMatch) {
      currentStart = Math.max(0, Number(startMatch[1]));
      continue;
    }
    const endMatch = line.match(/silence_end:\s*(-?\d+(?:\.\d+)?)(?:\s*\|\s*silence_duration:\s*(-?\d+(?:\.\d+)?))?/i);
    if (endMatch) {
      const end = Math.max(0, Number(endMatch[1]));
      const start = currentStart != null ? currentStart : Math.max(0, end - Number(endMatch[2] || 0));
      intervals.push({
        start: Number(start.toFixed(3)),
        end: Number(end.toFixed(3)),
        duration: Number(Math.max(0, end - start).toFixed(3)),
      });
      currentStart = null;
    }
  }

  if (currentStart != null && Number.isFinite(totalSeconds) && totalSeconds > currentStart) {
    intervals.push({
      start: Number(currentStart.toFixed(3)),
      end: Number(totalSeconds.toFixed(3)),
      duration: Number((totalSeconds - currentStart).toFixed(3)),
    });
  }

  return intervals;
}

/**
 * Inverts silence spans into non-silent sound slices suitable for splitting
 * Lyria 3.5's multi-hit ~60s SFX and long cues.
 */
export function invertSilencesToSlices(silences, totalSeconds, { minSliceSec = 0.2, padSec = 0.04 } = {}) {
  if (!Number.isFinite(totalSeconds) || totalSeconds <= 0) return [];
  const sorted = [...(silences || [])].sort((a, b) => a.start - b.start);
  const slices = [];
  let cursor = 0;

  for (const s of sorted) {
    if (s.start > cursor) {
      const startSec = Number(Math.max(0, cursor - padSec).toFixed(3));
      const endSec = Number(Math.min(totalSeconds, s.start + padSec).toFixed(3));
      const durationSec = Number((endSec - startSec).toFixed(3));
      if (durationSec >= minSliceSec) {
        slices.push({ index: slices.length + 1, startSec, endSec, durationSec });
      }
    }
    cursor = Math.max(cursor, s.end);
  }

  if (totalSeconds > cursor) {
    const startSec = Number(Math.max(0, cursor - padSec).toFixed(3));
    const endSec = Number(totalSeconds.toFixed(3));
    const durationSec = Number((endSec - startSec).toFixed(3));
    if (durationSec >= minSliceSec) {
      slices.push({ index: slices.length + 1, startSec, endSec, durationSec });
    }
  }

  return slices;
}

export function buildMeasureArgs({ filePath, silenceNoiseDb = -45, minSilenceSec = 0.4, padSec = 0 } = {}) {
  const filterParts = [];
  if (padSec > 0) filterParts.push(`apad=pad_dur=${padSec}`);
  filterParts.push(`silencedetect=noise=${silenceNoiseDb}dB:d=${minSilenceSec}`);
  filterParts.push("ebur128=peak=true");
  return [
    "-nostats",
    "-i",
    filePath,
    "-map",
    "0:a:0",
    "-af",
    filterParts.join(","),
    "-f",
    "null",
    "-",
    "-progress",
    "pipe:1",
  ];
}

export async function measureAudioFile(
  filePath,
  {
    ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
    silenceNoiseDb = -45,
    minSilenceSec = 0.4,
    padSec = 0,
    runFfmpeg = defaultRunFfmpeg,
  } = {},
) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Audio file not found: ${filePath}`);
  }
  const args = buildMeasureArgs({ filePath, silenceNoiseDb, minSilenceSec, padSec });
  const res = await runFfmpeg(ffmpegBin, args);
  if (res.exitCode !== 0) {
    throw new Error(`ffmpeg audio measurement failed (exit ${res.exitCode}): ${res.stderr.slice(-300)}`);
  }

  const rawSeconds = parseDecodedSeconds(res.stdout);
  const seconds = rawSeconds != null ? Number(Math.max(0, rawSeconds - padSec).toFixed(3)) : null;
  const ebu = parseEbur128Summary(res.stderr);
  const silences = parseSilenceIntervals(res.stderr, seconds);

  return {
    file: path.basename(filePath),
    filePath,
    sha256: sha256File(filePath),
    seconds,
    lufs_i: ebu.lufs_i,
    lufs_m: ebu.lufs_m,
    peak_dbtp: ebu.peak_dbtp,
    silences: silences.length,
    silenceIntervals: silences,
    nearSilent: ebu.lufs_i != null && ebu.lufs_i < NEAR_SILENT_LUFS_THRESHOLD,
    clipping: ebu.peak_dbtp != null && ebu.peak_dbtp > CLIPPING_PEAK_DBTP_THRESHOLD,
  };
}

export async function detectAudioSlices(
  filePath,
  {
    ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
    noiseDb = -40,
    minSilenceSec = 0.35,
    minSliceSec = 0.2,
    padSec = 0.04,
    runFfmpeg = defaultRunFfmpeg,
  } = {},
) {
  const measured = await measureAudioFile(filePath, {
    ffmpegBin,
    silenceNoiseDb: noiseDb,
    minSilenceSec,
    runFfmpeg,
  });
  const slices = invertSilencesToSlices(measured.silenceIntervals, measured.seconds, {
    minSliceSec,
    padSec,
  });
  return {
    file: measured.file,
    filePath,
    seconds: measured.seconds,
    lufs_i: measured.lufs_i,
    peak_dbtp: measured.peak_dbtp,
    nearSilent: measured.nearSilent,
    silenceCount: measured.silences,
    slices,
  };
}

export function buildCutAudioArgs({
  inputPath,
  outputPath,
  startSec,
  endSec,
  fadeInSec = 0.01,
  fadeOutSec = 0.08,
  sampleRate = 48000,
  bitrate = "160k",
} = {}) {
  const start = Math.max(0, Number(startSec) || 0);
  const end = Number(endSec);
  const duration = Number((end - start).toFixed(3));
  if (!Number.isFinite(duration) || duration <= 0.05) {
    throw new Error(`Invalid cut range [${startSec}, ${endSec}]: duration must be > 0.05s.`);
  }

  const filters = [];
  if (fadeInSec > 0 && fadeInSec < duration / 2) {
    filters.push(`afade=t=in:st=0:d=${Number(fadeInSec).toFixed(3)}`);
  }
  if (fadeOutSec > 0 && fadeOutSec < duration / 2) {
    const outStart = Math.max(0, Number((duration - fadeOutSec).toFixed(3)));
    filters.push(`afade=t=out:st=${outStart}:d=${Number(fadeOutSec).toFixed(3)}`);
  }

  const ext = path.extname(outputPath).toLowerCase();
  const codecArgs =
    ext === ".wav"
      ? ["-c:a", "pcm_s16le", "-ar", String(sampleRate), "-ac", "2"]
      : ext === ".mp3"
        ? ["-c:a", "libmp3lame", "-b:a", bitrate, "-ar", String(sampleRate), "-ac", "2"]
        : ["-c:a", "aac", "-b:a", bitrate, "-ar", String(sampleRate), "-ac", "2", "-movflags", "+faststart"];

  const args = ["-y", "-ss", String(start), "-t", String(duration), "-i", inputPath, "-vn"];
  if (filters.length > 0) {
    args.push("-af", filters.join(","));
  }
  args.push(...codecArgs, outputPath);
  return args;
}

export async function cutAudioSlice({
  inputPath,
  outputPath,
  startSec,
  endSec,
  fadeInSec = 0.01,
  fadeOutSec = 0.08,
  bitrate = "160k",
  ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
  runFfmpeg = defaultRunFfmpeg,
} = {}) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  const args = buildCutAudioArgs({ inputPath, outputPath, startSec, endSec, fadeInSec, fadeOutSec, bitrate });
  const res = await runFfmpeg(ffmpegBin, args);
  if (res.exitCode !== 0) {
    throw new Error(`ffmpeg cut failed (exit ${res.exitCode}): ${res.stderr.slice(-300)}`);
  }

  // Pad short clips by 1s during measurement so ebur128 captures <400ms SFX cleanly
  const measured = await measureAudioFile(outputPath, {
    ffmpegBin,
    padSec: endSec - startSec < 1.5 ? 1 : 0,
    runFfmpeg,
  });

  return {
    inputPath,
    outputPath,
    file: path.basename(outputPath),
    cut: {
      startSec: Number(startSec),
      endSec: Number(endSec),
      fadeInSec: Number(fadeInSec),
      fadeOutSec: Number(fadeOutSec),
    },
    sha256: measured.sha256,
    seconds: measured.seconds,
    lufs_i: measured.lufs_i,
    lufs_m: measured.lufs_m,
    peak_dbtp: measured.peak_dbtp,
    nearSilent: measured.nearSilent,
    clipping: measured.clipping,
  };
}
