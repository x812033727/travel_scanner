// How a drama's clips, subtitle strips and music become final.mp4 (docs/videos/DRAMA.md), as pure
// functions beside plan.mjs: the layout of clip and card scenes, how a clip is fitted to its
// scene's frames, the subtitle overlay track, every ffmpeg argument for a clip segment and for
// the music mix, and the drama's own checks.
//
// A clip segment is encoded with the slides' settings apart from the tune, so the segments still
// join with `-c copy`; it has its own encoder version, so a change here never invalidates a
// slides video's cached segments. Nothing here needs a GPU or minterpolate: the worker has 3 GB
// and no GPU, and xfade would force the join to re-encode.
import { createHash } from "node:crypto";

import { isShot } from "../core/drama.mjs";
import { FPS } from "../core/timeline.mjs";
import { HEIGHT, layoutScenes, LOUDNESS, PlanError, WIDTH } from "./plan.mjs";

// Part of every clip segment's cache key: change a setting below and every clip is re-encoded.
export const CLIP_ENCODER_VERSION = "x264-high-crf18-film-g60-bf2-bt709-clip-v1";
// A clip shorter than its narration is slowed no further than this before its last frame holds.
export const MIN_AUTO_SPEED = 0.85;
export const MIN_SLOW_SPEED = 0.5;
// A held last frame longer than this reads as a frozen video; fit "freeze" says it is meant.
export const MAX_FREEZE_FRAMES = 60;
// The first frame of a clip is its keyframe, scaled and encoded twice: it scores well above this.
export const KEYFRAME_MIN_PSNR = 22;
// The music bed under the -14 LUFS mix, without ducking, at most this loud.
export const MAX_BED_LUFS = -24;
export const DISSOLVE_FRAMES = 15;
// The sidechain compressor: the voice sits about this far above the threshold, which is what
// turns the owner's duck_db into a ratio.
export const DUCK_THRESHOLD = 0.03;
export const VOICE_OVER_THRESHOLD_DB = 20;
export const DUCK_ATTACK_MS = 30;
export const DUCK_RELEASE_MS = 500;
const STEREO = "pan=stereo|c0=c0|c1=c0";

const hash16 = (value) => createHash("sha256").update(JSON.stringify(value)).digest("hex").slice(0, 16);
const seconds = (frames) => (frames / FPS).toFixed(6);

/**
 * How a clip of `available` frames fills a scene of `needed` frames. Longer clips are cut at the
 * end (frame 0 is the keyframe, which the checks compare). Shorter ones are slowed, no further
 * than the mode allows, and their last frame is then held: "auto" slows to 0.85x, "slow" to
 * 0.5x, "freeze" and "trim" never slow.
 */
export function fitPlan(available, needed, mode = "auto") {
  if (!Number.isInteger(available) || available <= 0) throw new PlanError(`a clip must have frames, not ${available}`);
  if (!Number.isInteger(needed) || needed <= 0) throw new PlanError(`a scene must have frames, not ${needed}`);
  if (available >= needed) return { mode, speed: 1, source_frames: needed, stretched: needed, pad: 0, trim: available - needed };
  const floor = mode === "slow" ? MIN_SLOW_SPEED : mode === "auto" ? MIN_AUTO_SPEED : 1;
  const speed = Number(Math.max(floor, available / needed).toFixed(4));
  const stretched = Math.min(needed, Math.floor(available / speed));
  return { mode, speed, source_frames: available, stretched, pad: needed - stretched, trim: 0 };
}

/** Why a fitted clip would look frozen, or null. */
export function freezeProblem(scene, fit) {
  if (fit.mode === "freeze" || fit.pad <= MAX_FREEZE_FRAMES) return null;
  return `shot ${scene.id} holds its last frame for ${fit.pad} frames (${(fit.pad / FPS).toFixed(1)} s): the clip is too short for its lines; ask for a longer clip, cut the lines, or set fit "freeze"`;
}

/**
 * Pair the timeline's scenes with the rendered frames and the generated clips: a card scene lays
 * out its stills like a slides video, a shot carries its clip, its fit mode and its transition.
 */
export function layoutDrama(doc, timeline, frames, clips, keyframes = null) {
  if (timeline.scenes.length !== frames.scenes.length) {
    throw new PlanError(`the frames were rendered for ${frames.scenes.length} scenes, the timeline has ${timeline.scenes.length}; run render again`);
  }
  return timeline.scenes.map((scene, index) => {
    const rendered = frames.scenes[index];
    const source = doc.scenes.find((each) => each.id === scene.id);
    if (!source || rendered.id !== scene.id) throw new PlanError(`scene ${scene.id} does not match the rendered frames; run render again`);
    const base = { id: scene.id, frames: scene.end_frame - scene.start_frame, start_frame: scene.start_frame };
    if (!isShot(source)) {
      const [laid] = layoutScenes({ scenes: [scene] }, { scenes: [rendered] });
      return { ...laid, kind: "stills" };
    }
    const clip = clips?.shots?.[scene.id];
    if (!clip?.file) throw new PlanError(`shot ${scene.id} has no clip; run clips first`);
    if (clip.needs_review) throw new PlanError(`shot ${scene.id} failed the clip checks (needs_review in clips/manifest.json); fix the prompt and run clips again`);
    return {
      ...base,
      kind: "clip",
      clip: { file: clip.file, sha256: clip.sha256 ?? null },
      fit: source.data?.fit ?? "auto",
      transition: index > 0 ? (source.data?.transition ?? "cut") : "cut",
      keyframe: keyframes?.shots?.[scene.id]?.file ?? null,
    };
  });
}

/**
 * The subtitle overlay for one scene: the strips shown for its frames, in order, with the blank
 * strip wherever nobody speaks, adding up to exactly the scene's frames.
 */
export function subtitleTrack(scene, cues, blank) {
  const start = scene.start_frame;
  const end = start + scene.frames;
  const inside = cues.filter((cue) => cue.end_frame > start && cue.start_frame < end).sort((a, b) => a.start_frame - b.start_frame);
  const entries = [];
  let at = start;
  const push = (file, frames) => {
    if (frames <= 0) return;
    const last = entries.at(-1);
    if (last && last.file === file) last.frames += frames;
    else entries.push({ file, frames });
  };
  for (const cue of inside) {
    const from = Math.max(cue.start_frame, at);
    const to = Math.min(cue.end_frame, end);
    if (to <= from) continue;
    push(blank, from - at);
    push(cue.file, to - from);
    at = to;
  }
  push(blank, end - at);
  return entries;
}

/** The frames a probed clip holds on the 30 fps grid. */
export function clipFrames(probe) {
  const video = probe.streams?.find((stream) => stream.codec_type === "video");
  if (!video) throw new PlanError("the clip has no video stream");
  if (video.r_frame_rate === `${FPS}/1` && Number(video.nb_read_packets) > 0) return Number(video.nb_read_packets);
  const duration = Number(video.duration);
  if (!(duration > 0)) throw new PlanError("the clip has no duration");
  return Math.max(1, Math.round(duration * FPS));
}

export function clipSegmentKey(scene, fit, subtitles = null, previous = null) {
  return hash16([CLIP_ENCODER_VERSION, scene.frames, scene.clip.file, scene.clip.sha256, fit, subtitles, scene.transition, previous]);
}

const COLOUR = `format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709`;

/**
 * Encode one shot: the clip scaled and padded to 1920x1080, slowed and held as its fit says, cut
 * to the scene's frames, the previous scene's last frame dissolving away over it when asked, and
 * the subtitle strips laid over the bottom. Same H.264 settings as a slide segment but tuned for
 * film, so the segments still join without re-encoding.
 */
export function clipSegmentArgs({ clip, frames, fit, subtitlesList = null, dissolveFrom = null, outFile }) {
  const inputs = ["-i", clip];
  // Input 1 is the subtitle strips when there are any; the dissolve frame comes after them.
  const subtitlesInput = subtitlesList ? 1 : null;
  if (subtitlesList) inputs.push("-f", "concat", "-safe", "0", "-i", subtitlesList);
  const dissolveInput = dissolveFrom ? (subtitlesList ? 2 : 1) : null;
  if (dissolveFrom) inputs.push("-loop", "1", "-framerate", String(FPS), "-t", seconds(DISSOLVE_FRAMES + 2), "-i", dissolveFrom);
  const chain = [
    `scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease:flags=lanczos`,
    `pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2`,
    ...(fit.speed !== 1 ? [`setpts=PTS/${fit.speed}`] : []),
    `fps=${FPS}`,
    ...(fit.pad > 0 ? [`tpad=stop_mode=clone:stop_duration=${seconds(fit.pad)}`] : []),
    `trim=end_frame=${frames}`,
    "setpts=PTS-STARTPTS",
  ];
  const graph = [`[0:v]${chain.join(",")}[pic]`];
  let last = "pic";
  if (dissolveFrom) {
    graph.push(`[${dissolveInput}:v]scale=${WIDTH}:${HEIGHT},format=yuva420p,fade=t=out:st=0:d=${seconds(DISSOLVE_FRAMES)}:alpha=1[prev]`);
    graph.push(`[${last}][prev]overlay=0:0:eof_action=pass[dissolved]`);
    last = "dissolved";
  }
  if (subtitlesList) {
    graph.push(`[${subtitlesInput}:v]format=rgba[strips]`);
    graph.push(`[${last}][strips]overlay=0:main_h-overlay_h:eof_action=pass[captioned]`);
    last = "captioned";
  }
  graph.push(`[${last}]${COLOUR}[out]`);
  return [
    "-hide_banner", "-y", "-loglevel", "error",
    ...inputs,
    "-filter_complex", graph.join(";"),
    "-map", "[out]",
    "-frames:v", String(frames),
    "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-tune", "film",
    "-bf", "2", "-g", String(FPS * 2), "-keyint_min", String(FPS),
    "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-r", String(FPS), "-fps_mode", "cfr", "-an", outFile,
  ];
}

/** The last frame of a segment as a PNG, for the dissolve into the next scene. */
export function lastFrameArgs(segment, frames, outFile) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", segment, "-vf", `select=eq(n\\,${frames - 1})`, "-fps_mode", "passthrough", "-frames:v", "1", outFile];
}

/** The compressor ratio that takes about duck_db off the music while the voice speaks. */
export function duckRatio(duckDb) {
  const duck = Math.min(Math.abs(duckDb), VOICE_OVER_THRESHOLD_DB - 1);
  if (duck <= 0) return 1;
  return Number((VOICE_OVER_THRESHOLD_DB / (VOICE_OVER_THRESHOLD_DB - duck)).toFixed(3));
}

/**
 * The music bed alone, as it sits under the voice: cut to the video, faded in and out, at
 * gain_db. Input 1 is the music, looped by the caller so a short track covers a long video.
 */
export function bedFilter(music, totalSeconds, label = "bed") {
  const fadeIn = Math.max(0, music.fade_in_ms) / 1000;
  const fadeOut = Math.min(Math.max(0, music.fade_out_ms) / 1000, totalSeconds);
  return [
    "[1:a]aformat=sample_rates=48000:channel_layouts=stereo",
    `atrim=0:${totalSeconds.toFixed(6)}`,
    "asetpts=PTS-STARTPTS",
    `afade=t=in:st=0:d=${fadeIn.toFixed(3)}`,
    `afade=t=out:st=${Math.max(0, totalSeconds - fadeOut).toFixed(6)}:d=${fadeOut.toFixed(3)}`,
    `volume=${music.gain_db}dB[${label}]`,
  ].join(",");
}

/**
 * Voice and music into one stereo mix: the voice (input 0) is copied to both channels and also
 * drives a compressor on the bed, so the music drops by about duck_db under speech and comes
 * back between lines; amix keeps the voice's length exactly, so the video's checks still hold.
 */
export function mixFilter(music, totalSeconds) {
  return [
    bedFilter(music, totalSeconds),
    `[0:a]aformat=sample_rates=48000:channel_layouts=mono,${STEREO},asplit=2[voice][side]`,
    `[bed][side]sidechaincompress=threshold=${DUCK_THRESHOLD}:ratio=${duckRatio(music.duck_db)}:attack=${DUCK_ATTACK_MS}:release=${DUCK_RELEASE_MS}:makeup=1:level_sc=1[ducked]`,
    "[voice][ducked]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]",
  ].join(";");
}

const loudnorm = (extra = "") => `loudnorm=I=${LOUDNESS.integrated}:TP=${LOUDNESS.truePeak}:LRA=${LOUDNESS.range}${extra}`;

const musicInput = (music, totalSeconds) => ["-stream_loop", "-1", "-t", totalSeconds.toFixed(6), "-i", music];

/** First loudnorm pass over the mix. */
export function measureMixArgs(narration, musicFile, music, totalSeconds) {
  return [
    "-hide_banner", "-nostats", "-i", narration, ...musicInput(musicFile, totalSeconds),
    "-filter_complex", `${mixFilter(music, totalSeconds)};[mix]${loudnorm(":print_format=json")}[out]`,
    "-map", "[out]", "-f", "null", "-",
  ];
}

/** Second loudnorm pass over the mix with the first pass's measurement, linear, to AAC-LC stereo 48 kHz. */
export function mixArgs(narration, musicFile, music, totalSeconds, measured, outFile) {
  const second = `:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`;
  return [
    "-hide_banner", "-y", "-loglevel", "error", "-i", narration, ...musicInput(musicFile, totalSeconds),
    "-filter_complex", `${mixFilter(music, totalSeconds)};[mix]${loudnorm(second)},aresample=48000[out]`,
    "-map", "[out]", "-c:a", "aac", "-b:a", "384k", "-ar", "48000", outFile,
  ];
}

/** The bed alone through ebur128, to know how loud the music sits before the voice is added. */
export function bedLoudnessArgs(narration, musicFile, music, totalSeconds) {
  return [
    "-hide_banner", "-nostats", "-i", narration, ...musicInput(musicFile, totalSeconds),
    "-filter_complex", `${bedFilter(music, totalSeconds)};[bed]ebur128=peak=true[out]`,
    "-map", "[out]", "-f", "null", "-",
  ];
}

/**
 * Where the bed ends up in the final mix: loudnorm's linear pass moves the whole mix from the
 * measured loudness to the target, and the bed with it.
 */
export function bedLevel(bedIntegrated, measured) {
  return Number((bedIntegrated + (LOUDNESS.integrated - Number(measured.input_i))).toFixed(1));
}

export function checkBed(level) {
  return level > MAX_BED_LUFS ? [`music bed at ${level} LUFS in the mix, above ${MAX_BED_LUFS}; lower music.gain_db`] : [];
}

/** Why a shot's first frame does not look like its keyframe, or null. */
export function keyframeProblem(scene, psnr) {
  if (psnr >= KEYFRAME_MIN_PSNR) return null;
  return `shot ${scene.id} frame 0 does not look like its keyframe (PSNR ${psnr.toFixed(1)} dB, below ${KEYFRAME_MIN_PSNR})`;
}
