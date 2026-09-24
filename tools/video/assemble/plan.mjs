// How the frames and the narration become final.mp4, as pure functions: which image is on screen
// for how many frames, the concat lists ffmpeg reads, every ffmpeg argument, and the checks.
//
// Each scene is encoded on its own with identical settings and the segments are joined with
// `-c copy`, so editing one scene re-encodes one segment. Every segment is cut to an exact frame
// count, which is what keeps the picture on the same 30 fps grid the narration was built on.
import { createHash } from "node:crypto";

import { FPS } from "../core/timeline.mjs";

export const WIDTH = 1920;
export const HEIGHT = 1080;
export const LOUDNESS = { integrated: -14, truePeak: -1, range: 11 };
export const LOUDNESS_TOLERANCE = 1;
// A frame showing its intended image scores about 47 dB; the neighbouring image scores 34 or less.
export const MIN_PSNR = 40;
// Part of every segment's cache key: change an encoder setting and every segment is redone.
export const ENCODER_VERSION = "x264-high-crf18-stillimage-g60-bf2-bt709-v2";

export class PlanError extends Error {}

/**
 * Pair the rendered states with the timeline's and lay out each scene as images and frame counts.
 * A state shows its transition frames first, one frame each, then its still for the rest.
 */
export function layoutScenes(timeline, manifest) {
  if (timeline.scenes.length !== manifest.scenes.length) {
    throw new PlanError(`the frames were rendered for ${manifest.scenes.length} scenes, the timeline has ${timeline.scenes.length}; run render again`);
  }
  return timeline.scenes.map((scene, index) => {
    const rendered = manifest.scenes[index];
    if (rendered.id !== scene.id || rendered.states.length !== scene.states.length) {
      throw new PlanError(`scene ${scene.id} does not match the rendered frames; run render again`);
    }
    const entries = [];
    scene.states.forEach((state, stateIndex) => {
      const frames = state.end_frame - state.start_frame;
      const picture = rendered.states[stateIndex];
      const transition = picture.transition.slice(0, Math.max(0, frames - 1));
      for (const file of transition) entries.push({ file, frames: 1 });
      if (frames - transition.length > 0) entries.push({ file: picture.still, frames: frames - transition.length });
    });
    return { id: scene.id, frames: scene.end_frame - scene.start_frame, start_frame: scene.start_frame, entries };
  });
}

const quote = (file) => `'${file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`;

/**
 * An ffconcat list whose durations are rounded from the cumulative time, so rounding never
 * accumulates. The last file is listed again: the concat demuxer ignores the last duration.
 *
 * Each image is opened at 30 fps. Left to its default, the image demuxer uses a 1/25 s time base,
 * every 1/30 s duration lands on a 40 ms grid, and the fps filter then drops and repeats frames:
 * the frame count still comes out right, which is why assemble also compares frames by number.
 */
export function concatList(entries, resolve) {
  const lines = ["ffconcat version 1.0"];
  const file = (name) => [`file ${quote(resolve(name))}`, `option framerate ${FPS}`];
  let frames = 0;
  let previous = 0;
  for (const entry of entries) {
    frames += entry.frames;
    const end = Math.round((frames / FPS) * 1e6);
    lines.push(...file(entry.file), `duration ${((end - previous) / 1e6).toFixed(6)}`);
    previous = end;
  }
  if (entries.length) lines.push(...file(entries.at(-1).file));
  return `${lines.join("\n")}\n`;
}

export function segmentKey(scene) {
  return createHash("sha256").update(JSON.stringify([ENCODER_VERSION, scene.frames, scene.entries])).digest("hex").slice(0, 16);
}

/** PNG (sRGB) to H.264 High in BT.709, tagged so players do not guess BT.601. */
export function segmentArgs(listFile, outFile, frames) {
  return [
    "-hide_banner", "-y", "-loglevel", "error",
    "-f", "concat", "-safe", "0", "-i", listFile,
    // PNG frames carry no colour description, and x264 takes it from the frames: setparams puts
    // BT.709 on them, and the x264 parameters write it into the stream's VUI as well.
    "-vf", `fps=${FPS},scale=${WIDTH}:${HEIGHT}:flags=lanczos:out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709`,
    "-frames:v", String(frames),
    "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-tune", "stillimage",
    "-bf", "2", "-g", String(FPS * 2), "-keyint_min", String(FPS),
    "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-r", String(FPS), "-fps_mode", "cfr", "-an", outFile,
  ];
}

export function joinArgs(listFile, outFile) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listFile, "-c", "copy", outFile];
}

const loudnormFilter = (extra = "") =>
  `loudnorm=I=${LOUDNESS.integrated}:TP=${LOUDNESS.truePeak}:LRA=${LOUDNESS.range}${extra}`;

// The narration is mono, the upload stereo. EBU R128 sums the channels, so the same voice copied
// to both reads 3 LU louder: normalize after going stereo, in both passes.
const STEREO = "pan=stereo|c0=c0|c1=c0";

export function measureLoudnessArgs(narration) {
  return ["-hide_banner", "-nostats", "-i", narration, "-af", `${STEREO},${loudnormFilter(":print_format=json")}`, "-f", "null", "-"];
}

/** The loudnorm JSON block ffmpeg prints at the end of stderr. */
export function parseLoudnorm(stderr) {
  const match = /\{[^{}]*"input_i"[^{}]*\}/s.exec(stderr);
  if (!match) throw new PlanError("loudnorm printed no measurement");
  return JSON.parse(match[0]);
}

/** Second loudnorm pass with the first pass's measurement, linear, then AAC-LC stereo 48 kHz. */
export function normalizeArgs(narration, measured, outFile) {
  const second = `:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`;
  return [
    "-hide_banner", "-y", "-loglevel", "error", "-i", narration,
    "-af", `${STEREO},${loudnormFilter(second)},aresample=48000`,
    "-c:a", "aac", "-b:a", "384k", "-ar", "48000", outFile,
  ];
}

export function muxArgs(video, audio, outFile) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", outFile];
}

export function probeArgs(file) {
  return ["-v", "error", "-count_packets", "-show_entries", "stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,color_space,color_primaries,color_transfer,nb_read_packets,sample_rate,channels,duration", "-of", "json", file];
}

export function ebur128Args(file) {
  return ["-hide_banner", "-nostats", "-i", file, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"];
}

/** Integrated loudness and true peak from the ebur128 summary. */
export function parseEbur128(stderr) {
  const summary = stderr.slice(stderr.lastIndexOf("Summary:"));
  const integrated = /I:\s*(-?[\d.]+)\s*LUFS/.exec(summary);
  const peak = /Peak:\s*(-?[\d.]+|-inf)\s*dBFS/.exec(summary);
  if (!integrated) throw new PlanError("ebur128 printed no summary");
  return { integrated: Number(integrated[1]), truePeak: peak ? (peak[1] === "-inf" ? -Infinity : Number(peak[1])) : null };
}

/**
 * Compare frame `n` of a video with an image. Frames are picked by number, not by seeking:
 * a seek in the joined file lands on the wrong frame often enough to fail a correct video.
 */
export function psnrArgs(video, n, image) {
  return [
    "-hide_banner", "-nostats", "-i", video, "-i", image,
    "-lavfi", `[0:v]select=eq(n\\,${n}),format=rgb24[a];[1:v]scale=${WIDTH}:${HEIGHT},format=rgb24[b];[a][b]psnr`,
    "-frames:v", "1", "-f", "null", "-",
  ];
}

export function parsePsnr(stderr) {
  const match = /PSNR .*average:(inf|[\d.]+)/.exec(stderr);
  if (!match) throw new PlanError("psnr printed no result");
  return match[1] === "inf" ? Infinity : Number(match[1]);
}

/** Every way the probed file differs from what YouTube recommends and the timeline expects. */
export function checkProbe(probe, { frames }) {
  const problems = [];
  const video = probe.streams?.find((stream) => stream.codec_type === "video");
  const audio = probe.streams?.find((stream) => stream.codec_type === "audio");
  if (!video) return ["no video stream"];
  if (video.codec_name !== "h264" || !/high/i.test(video.profile ?? "")) problems.push(`video is ${video.codec_name} ${video.profile}, expected H.264 High`);
  if (video.width !== WIDTH || video.height !== HEIGHT) problems.push(`video is ${video.width}x${video.height}`);
  if (video.r_frame_rate !== `${FPS}/1`) problems.push(`frame rate ${video.r_frame_rate}`);
  if (video.pix_fmt !== "yuv420p") problems.push(`pixel format ${video.pix_fmt}`);
  if (video.color_space !== "bt709" || video.color_primaries !== "bt709" || video.color_transfer !== "bt709") problems.push("colour is not tagged BT.709");
  if (Number(video.nb_read_packets) !== frames) problems.push(`${video.nb_read_packets} video frames, the timeline has ${frames}`);
  if (!audio) problems.push("no audio stream");
  else {
    if (audio.codec_name !== "aac") problems.push(`audio is ${audio.codec_name}`);
    if (Number(audio.sample_rate) !== 48000) problems.push(`audio at ${audio.sample_rate} Hz`);
    if (audio.channels !== 2) problems.push(`${audio.channels} audio channels, expected stereo`);
    const videoSeconds = frames / FPS;
    if (Math.abs(Number(audio.duration) - videoSeconds) > 1 / FPS + 0.03) {
      problems.push(`audio lasts ${Number(audio.duration).toFixed(3)} s, video ${videoSeconds.toFixed(3)} s`);
    }
  }
  return problems;
}

export function checkLoudness({ integrated, truePeak }) {
  const problems = [];
  if (Math.abs(integrated - LOUDNESS.integrated) > LOUDNESS_TOLERANCE) problems.push(`loudness ${integrated} LUFS, target ${LOUDNESS.integrated} ± ${LOUDNESS_TOLERANCE}`);
  if (truePeak !== null && truePeak > LOUDNESS.truePeak + 0.5) problems.push(`true peak ${truePeak} dBFS, above ${LOUDNESS.truePeak}`);
  return problems;
}

/**
 * Frames to compare in each scene's segment: the first, the second (inside a transition, where a
 * time-base error shows first) and the last, which a drift inside the scene would have moved.
 * The segments are joined without re-encoding, so checking them checks the final video.
 */
export function segmentSamples(scene) {
  const images = scene.entries.flatMap((entry) => Array.from({ length: entry.frames }, () => entry.file));
  const frames = [...new Set([0, 1, images.length - 1])].filter((n) => n >= 0 && n < images.length);
  return frames.map((n) => ({ n, file: images[n] }));
}
