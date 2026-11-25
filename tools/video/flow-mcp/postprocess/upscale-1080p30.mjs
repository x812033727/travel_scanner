/**
 * Local FFmpeg post-processing for Google Flow clips:
 *   - Lanczos upscale 720p raw download -> 1920x1080 @ 30fps (0 extra Flow credits)
 *   - Explicit BT.709 color tags + `video_full_range_flag=0` (`tv` range) to prevent
 *     FFmpeg filter-graph rebuilds that drop the Mokaair watermark on concat
 *     (FLOW-PRODUCTION-RULES.md §2 & §7.3)
 *   - Strip native model audio (`-an`)
 *   - Generate 2x2 4-frame QA contact sheets (`*-qa4.jpg`) + SHA-256 checksums
 */

import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

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
  // Select 4 evenly distributed frames across a typical 4s @ 30fps clip (0.4s, 1.4s, 2.4s, 3.4s)
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

export async function upscaleClipTo1080p30({
  inputPath,
  outputPath,
  qa4OutputPath = null,
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
    const qaArgs = buildClipQa4Args({ inputPath: outputPath, outputJpgPath: qa4OutputPath });
    await runFfmpeg(ffmpegBin, qaArgs);
    qa4Path = qa4OutputPath;
  }

  return {
    inputPath,
    outputPath,
    qa4Path,
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
