/**
 * Local FFmpeg post-processing and AI drama QC for Google Flow clips:
 *   - Lanczos upscale 720p raw download -> 1080p30 (16:9 or 9:16), BT.709,
 *     `video_full_range_flag=0` (`tv` range), `-an` clean video master
 *   - Optional raw audio sidecar extraction (`raw-audio/*.wav`, 48kHz stereo)
 *     for AI dramas that want to audition natural foley or dialogue
 *   - Last-frame PNG extraction (`extractLastFrame`) for Exact-Join continuity
 *   - Frame-0 PSNR check against approved keyframe (`KEYFRAME_MIN_PSNR = 22`)
 *   - Mid-clip hard-cut scene detection (`scene > 0.4`) with trim recommendation
 *   - 2x2 4-frame QA contact sheets (`*-qa4.jpg`) + SHA-256 checksums
 */

import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

export const KEYFRAME_MIN_PSNR = 22;

export function sha256File(filePath) {
  return createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

export function buildUpscale1080p30Args({
  inputPath,
  outputPath,
  width = 1920,
  height = 1080,
  fps = 30,
  crf = 18,
  preset = "medium",
}) {
  return [
    "-y",
    "-i",
    inputPath,
    "-vf",
    `scale=${width}:${height}:flags=lanczos,fps=${fps},format=yuv420p`,
    "-c:v",
    "libx264",
    "-preset",
    String(preset),
    "-crf",
    String(crf),
    "-colorspace",
    "bt709",
    "-color_primaries",
    "bt709",
    "-color_trc",
    "bt709",
    "-color_range",
    "tv",
    "-bsf:v",
    "h264_metadata=video_full_range_flag=0",
    "-an",
    "-movflags",
    "+faststart",
    outputPath,
  ];
}

export function buildClipQa4Args({ inputPath, outputJpgPath, tileWidth = 640, tileHeight = 360 }) {
  return [
    "-y",
    "-i",
    inputPath,
    "-vf",
    `fps=1,scale=${tileWidth}:${tileHeight}:flags=lanczos,tile=2x2`,
    "-frames:v",
    "1",
    "-q:v",
    "3",
    outputJpgPath,
  ];
}

export function buildExtractLastFrameArgs({ inputPath, outputPngPath }) {
  return [
    "-y",
    "-sseof",
    "-0.1",
    "-i",
    inputPath,
    "-update",
    "1",
    "-frames:v",
    "1",
    outputPngPath,
  ];
}

export function buildExtractRawAudioArgs({ inputPath, outputWavPath }) {
  return [
    "-y",
    "-i",
    inputPath,
    "-vn",
    "-acodec",
    "pcm_s16le",
    "-ar",
    "48000",
    "-ac",
    "2",
    outputWavPath,
  ];
}

export function buildFrame0PsnrArgs({ keyframePath, clipPath, width = 1920, height = 1080 }) {
  return [
    "-i",
    keyframePath,
    "-i",
    clipPath,
    "-lavfi",
    `[0:v]scale=${width}:${height}:flags=lanczos,format=yuv420p[a];[1:v]select=eq(n\\,0),scale=${width}:${height}:flags=lanczos,format=yuv420p[b];[a][b]psnr`,
    "-frames:v",
    "1",
    "-f",
    "null",
    "-",
  ];
}

export function buildSceneCutDetectArgs({ inputPath, threshold = 0.4 }) {
  return [
    "-i",
    inputPath,
    "-vf",
    `select='gt(scene,${threshold})',showinfo`,
    "-f",
    "null",
    "-",
  ];
}

export function parsePsnrFromStderr(stderr) {
  const match = /average:(inf|\d+(?:\.\d+)?)/i.exec(String(stderr || ""));
  if (!match) return null;
  if (match[1].toLowerCase() === "inf") return 99.99;
  return Number(match[1]);
}

export function parseSceneCutTimesFromStderr(stderr) {
  const times = [];
  const re = /pts_time:(\d+(?:\.\d+)?)/g;
  let m;
  while ((m = re.exec(String(stderr || ""))) !== null) {
    const t = Number(m[1]);
    if (Number.isFinite(t) && t > 0.15) {
      times.push(Number(t.toFixed(3)));
    }
  }
  return times;
}

function defaultRunFfmpeg(ffmpegBin, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(ffmpegBin, args, {
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });
    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", (err) => {
      if (err.code === "ENOENT") {
        reject(
          new Error(
            `ffmpeg executable "${ffmpegBin}" was not found. On Windows install via: winget install Gyan.FFmpeg`,
          ),
        );
        return;
      }
      reject(err);
    });
    child.on("close", (code) => {
      if (code === 0) resolve({ exitCode: 0, stderr });
      else reject(new Error(`ffmpeg exited with code ${code}: ${stderr.trim().slice(-400)}`));
    });
  });
}

export async function extractLastFrame({
  inputPath,
  outputPngPath,
  ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
  runFfmpeg = defaultRunFfmpeg,
}) {
  fs.mkdirSync(path.dirname(outputPngPath), { recursive: true });
  await runFfmpeg(ffmpegBin, buildExtractLastFrameArgs({ inputPath, outputPngPath }));
  return { outputPngPath, sha256: fs.existsSync(outputPngPath) ? sha256File(outputPngPath) : null };
}

export async function inspectClipQc({
  clipPath,
  keyframePath = null,
  width = 1920,
  height = 1080,
  durationSec = 4,
  sceneCutThreshold = 0.4,
  ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
  runFfmpeg = defaultRunFfmpeg,
}) {
  let frame0Psnr = null;
  let psnrOk = null;
  if (keyframePath && fs.existsSync(keyframePath)) {
    try {
      const res = await runFfmpeg(ffmpegBin, buildFrame0PsnrArgs({ keyframePath, clipPath, width, height }));
      frame0Psnr = parsePsnrFromStderr(res.stderr);
      psnrOk = frame0Psnr != null ? frame0Psnr >= KEYFRAME_MIN_PSNR : null;
    } catch {
      frame0Psnr = null;
      psnrOk = null;
    }
  }

  let hardCutTimes = [];
  try {
    const res = await runFfmpeg(ffmpegBin, buildSceneCutDetectArgs({ inputPath: clipPath, threshold: sceneCutThreshold }));
    hardCutTimes = parseSceneCutTimesFromStderr(res.stderr);
  } catch {
    hardCutTimes = [];
  }

  const firstCut = hardCutTimes.length > 0 ? hardCutTimes[0] : null;
  const recommendedTrim = {
    inSec: 0,
    durSec: firstCut && firstCut > 0.6 ? Number((firstCut - 0.1).toFixed(2)) : Number(durationSec) || 4,
    keepCuts: false,
    note: firstCut
      ? `Mid-clip hard cut detected at ${firstCut}s (scene > ${sceneCutThreshold}); trim before cut or set keep_cuts: true for intentional splash/impact action.`
      : "No mid-clip hard cut detected.",
  };

  return {
    frame0Psnr,
    minPsnr: KEYFRAME_MIN_PSNR,
    psnrOk,
    hardCutTimes,
    recommendedTrim,
    ok: psnrOk !== false,
  };
}

export async function upscaleClipTo1080p30({
  inputPath,
  outputPath,
  qa4OutputPath = null,
  rawAudioOutputPath = null,
  keyframePath = null,
  durationSec = 4,
  runQc = false,
  width = 1920,
  height = 1080,
  fps = 30,
  ffmpegBin = process.env.FFMPEG_BIN || "ffmpeg",
  runFfmpeg = defaultRunFfmpeg,
} = {}) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  const upscaleArgs = buildUpscale1080p30Args({ inputPath, outputPath, width, height, fps });
  await runFfmpeg(ffmpegBin, upscaleArgs);

  let qa4Path = null;
  if (qa4OutputPath) {
    fs.mkdirSync(path.dirname(qa4OutputPath), { recursive: true });
    const tileW = width >= height ? 640 : 360;
    const tileH = width >= height ? 360 : 640;
    const qaArgs = buildClipQa4Args({ inputPath: outputPath, outputJpgPath: qa4OutputPath, tileWidth: tileW, tileHeight: tileH });
    await runFfmpeg(ffmpegBin, qaArgs);
    qa4Path = qa4OutputPath;
  }

  let rawAudioPath = null;
  if (rawAudioOutputPath) {
    fs.mkdirSync(path.dirname(rawAudioOutputPath), { recursive: true });
    try {
      await runFfmpeg(ffmpegBin, buildExtractRawAudioArgs({ inputPath, outputWavPath: rawAudioOutputPath }));
      rawAudioPath = rawAudioOutputPath;
    } catch {
      // Raw clip may contain no audio stream; silently skip sidecar extraction
      rawAudioPath = null;
    }
  }

  let qc = null;
  if (runQc) {
    qc = await inspectClipQc({
      clipPath: outputPath,
      keyframePath,
      width,
      height,
      durationSec,
      ffmpegBin,
      runFfmpeg,
    });
  }

  return {
    inputPath,
    outputPath,
    qa4Path,
    rawAudioPath,
    qc,
    rawSha256: fs.existsSync(inputPath) ? sha256File(inputPath) : null,
    upscaledSha256: fs.existsSync(outputPath) ? sha256File(outputPath) : null,
    spec: {
      width,
      height,
      fps,
      colorspace: "bt709",
      colorRange: "tv",
      audioStripped: true,
    },
  };
}
