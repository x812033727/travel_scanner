// How a drama's clips, subtitle strips and music become final.mp4 (docs/videos/DRAMA.md), as pure
// functions beside plan.mjs: the layout of clip, still and card scenes, how a clip is fitted to
// its scene's frames, how a still shot's keyframe is animated, the subtitle overlay track, every
// ffmpeg argument for a clip or motion segment and for the music mix, and the drama's own checks.
//
// A clip segment is encoded with the slides' settings apart from the tune, so the segments still
// join with `-c copy`; it has its own encoder version, so a change here never invalidates a
// slides video's cached segments. A motion segment (a shot marked visual "still", docs/videos/
// BINGE.md) is the keyframe under a slow zoompan move, encoded exactly like a clip segment, with
// its own version again. Nothing here needs a GPU or minterpolate: the worker has 3 GB and no
// GPU, and xfade would force the join to re-encode.
import { createHash } from "node:crypto";

import { isShot, shotVisual } from "../core/drama.mjs";
import { FPS } from "../core/timeline.mjs";
import { HEIGHT, layoutScenes, LOUDNESS, PlanError, WIDTH } from "./plan.mjs";

// Part of every clip segment's cache key: change a setting below and every clip is re-encoded.
export const CLIP_ENCODER_VERSION = "x264-high-crf18-film-g60-bf2-bt709-clip-v1";
// The same for a motion segment: the zoompan expressions below are part of what it versions.
export const MOTION_ENCODER_VERSION = "x264-high-crf18-film-g60-bf2-bt709-motion-v3";
// A card of an illustrated slides video (docs/videos/ILLUSTRATED.md) may drift like a still: its
// segment key carries this too, so a change to how cards move never touches a drama's keys.
export const MOTION_CARD_VERSION = "card-motion-v1";
// The moves single-state cards take, in turn, so two cards in a row never move the same way.
export const CARD_MOVES = ["drift", "push-in"];
// How far a push-in or pull-out travels over the shot, as a share of the picture; a pan or tilt
// sits at a fixed zoom and slides the window; a drift barely moves at all. Small on purpose: a
// still is meant to read as a held shot with life in it, not as a camera move.
export const MOTION_ZOOM = 0.10;
export const MOTION_PAN_ZOOM = 1.08;
export const MOTION_DRIFT_ZOOM = 0.04;
// The keyframe is upscaled this much before zoompan crops it, so the crop window is never
// smaller than the output and no frame is enlarged from fewer pixels than it shows.
export const MOTION_SOURCE_SCALE = 1.25;
// A move's travel grows with the shot up to this many seconds, so the picture moves at about
// one speed in a short shot and a long one instead of hurrying through a short one; a shorter
// shot keeps at least MOTION_TRAVEL_MIN of the travel. The long video's stills ease their move
// (smoothstep) and scale it; a Short (shorts/motion.mjs) asks for the plain linear expressions.
export const MOTION_TRAVEL_SECONDS = 6;
export const MOTION_TRAVEL_MIN = 0.5;
// Where a drifting picture goes: its shot id decides, so two drifts in a row rarely go one way.
export const DRIFT_DIRECTIONS = ["right", "left"];
// A scene change of an illustrated slides video is a cut, like an editor's, except after a
// pause beat at least this long on the line before (the register's beats: 900 ms after the cold
// open, 600 before an 其實), where the picture dissolves (docs/videos/ILLUSTRATED.md).
export const DISSOLVE_BEAT_MS = 600;
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
/**
 * The transition into a scene of an illustrated slides video (docs/videos/ILLUSTRATED.md): the
 * writer's word when the scene carries one; else a hard cut into the first scene and into every
 * chapter opener (the chapter card is the beat), a dissolve after a pause beat on the line
 * before (`previous` is that scene), and a cut everywhere else: an editor cuts, and dissolves
 * where the story breathes, while a dissolve into every picture is the slideshow a viewer
 * reads as automated.
 */
export function illustratedTransition(source, index, previous = null) {
  if (index === 0) return "cut";
  if (source.data?.transition) return source.data.transition;
  if (source.chapter) return "cut";
  const beat = previous?.lines?.at(-1)?.pause_after_ms ?? 0;
  return beat >= DISSOLVE_BEAT_MS ? "dissolve" : "cut";
}

/**
 * Pair the timeline's scenes with the rendered frames and the generated clips. `options` are for
 * illustrated slides: `transitionRule(source, index)` decides how a shot or a moving card is
 * entered (a drama takes the shot's own word, else a cut), and `cardMotion` lays a single-state
 * card out as a motion scene, its still drifting like a keyframe, so a title or a big number is
 * never a frozen picture; a card with reveals keeps its entrances as its motion.
 */
export function layoutDrama(doc, timeline, frames, clips, keyframes = null, { transitionRule = null, cardMotion = false } = {}) {
  if (timeline.scenes.length !== frames.scenes.length) {
    throw new PlanError(`the frames were rendered for ${frames.scenes.length} scenes, the timeline has ${timeline.scenes.length}; run render again`);
  }
  let moved = 0;
  return timeline.scenes.map((scene, index) => {
    const rendered = frames.scenes[index];
    const source = doc.scenes.find((each) => each.id === scene.id);
    if (!source || rendered.id !== scene.id) throw new PlanError(`scene ${scene.id} does not match the rendered frames; run render again`);
    const base = { id: scene.id, frames: scene.end_frame - scene.start_frame, start_frame: scene.start_frame };
    const previous = index > 0 ? (doc.scenes.find((each) => each.id === timeline.scenes[index - 1].id) ?? null) : null;
    if (!isShot(source)) {
      if (cardMotion && rendered.states.length === 1 && rendered.states[0].still) {
        const move = CARD_MOVES[moved % CARD_MOVES.length];
        // Drifting cards take turns going right and left, as the shots' drifts do.
        const direction = move === "drift" ? { direction: DRIFT_DIRECTIONS[Math.floor(moved / CARD_MOVES.length) % DRIFT_DIRECTIONS.length] } : {};
        moved += 1;
        const transition = transitionRule ? transitionRule(source, index, previous) : "cut";
        return { ...base, kind: "motion", card: true, keyframe: { file: rendered.states[0].still, sha256: null }, move: { name: move, startsAtIdentity: IDENTITY_START.has(move), ...direction }, transition, fit: null };
      }
      const [laid] = layoutScenes({ scenes: [scene] }, { scenes: [rendered] });
      return { ...laid, kind: "stills" };
    }
    const transition = transitionRule ? transitionRule(source, index, previous) : index > 0 ? (source.data?.transition ?? "cut") : "cut";
    if (shotVisual(source) === "still") {
      // The keyframes manifest is the source; the clips manifest carries the same file and hash
      // for every still, so a work directory missing one still assembles from the other.
      const keyframe = keyframes?.shots?.[scene.id] ?? (clips?.shots?.[scene.id]?.still ? clips.shots[scene.id] : null);
      if (!keyframe?.file) throw new PlanError(`shot ${scene.id} is a still with no keyframe; run keyframes first`);
      if (keyframe.needs_review) throw new PlanError(`shot ${scene.id} is a still whose keyframe failed its checks (needs_review in keyframes/manifest.json); fix the prompt and run keyframes again`);
      return { ...base, kind: "motion", keyframe: { file: keyframe.file, sha256: keyframe.sha256 ?? null }, move: motionMove(source.data, scene.id), transition, fit: null };
    }
    const clip = clips?.shots?.[scene.id];
    if (!clip?.file || clip.still) throw new PlanError(`shot ${scene.id} has no clip; run clips first`);
    if (clip.needs_review) throw new PlanError(`shot ${scene.id} failed the clip checks (needs_review in clips/manifest.json); fix the prompt and run clips again`);
    return {
      ...base,
      kind: "clip",
      clip: { file: clip.file, sha256: clip.sha256 ?? null },
      fit: source.data?.fit ?? "auto",
      transition,
      keyframe: keyframes?.shots?.[scene.id]?.file ?? null,
    };
  });
}

// The camera words a writer uses, in the order they are tried; the first that matches wins, and
// a shot that names none drifts. A move is named for what the viewer sees the picture do, which
// for a pan is the opposite of the camera's word: a camera panning left sends the picture to the
// right, so "pan left" (and "left to right", the picture's own direction) is pan-right. Tilts
// keep the camera's word, as the writers use it: "tilt up", "crane up" and "rise" are tilt-up.
const MOVES = [
  ["push-in", /push|dolly in|zoom in|closer|move in/],
  ["pull-out", /pull|zoom out|widen|back away/],
  ["pan-right", /pan (?:to the )?left|left to right/],
  ["pan-left", /pan (?:to the )?right|right to left/],
  ["tilt-up", /tilt up|crane up|rise/],
  ["tilt-down", /tilt down|crane down|descend/],
];
// Moves whose first frame is the whole keyframe at zoom 1.0, so frame 0 can be checked against it.
const IDENTITY_START = new Set(["push-in", "drift"]);

/** Which way a shot drifts: its id decides, so a run of drifting pictures does not all go one way. */
export const driftDirection = (id) => DRIFT_DIRECTIONS[[...String(id ?? "")].reduce((sum, char) => sum + char.charCodeAt(0), 0) % DRIFT_DIRECTIONS.length];

/**
 * Which camera move animates a still shot, read from the shot's camera direction first and its
 * motion prompt second: { name, startsAtIdentity }, a drift adding the direction its shot id
 * gives it.
 */
export function motionMove(data, id = null) {
  for (const text of [data?.camera, data?.motion]) {
    if (typeof text !== "string") continue;
    const lower = text.toLowerCase();
    const found = MOVES.find(([, pattern]) => pattern.test(lower));
    if (found) return { name: found[0], startsAtIdentity: IDENTITY_START.has(found[0]) };
  }
  return { name: "drift", startsAtIdentity: true, direction: driftDirection(id) };
}

const round4 = (value) => Number(value.toFixed(4));

/**
 * zoompan's zoom, x and y expressions for a move over `frames` output frames, in terms of `on`
 * (the output frame number) so the move ends exactly on the last frame. x and y are the crop
 * window's top-left corner in the upscaled keyframe: a window sliding right shows what lies to
 * the right, so the picture travels left. pan-right therefore slides the window from the right
 * edge to the left edge, and tilt-up (the camera tilting up) slides it from the bottom to the top.
 * The move's progress is linear unless `eased` (smoothstep, 3t² − 2t³: it starts and settles
 * like a hand on a tripod head rather than a motor), and `travel` scales how far it goes.
 */
export function zoompanExpr(move, frames, { eased = false, travel = 1 } = {}) {
  const name = typeof move === "string" ? move : move?.name;
  const direction = typeof move === "string" ? undefined : move?.direction;
  const n = Math.max(frames - 1, 1);
  const t = `on/${n}`;
  const p = eased ? `((${t})*(${t})*(3-2*(${t})))` : t;
  const run = travel === 1 ? p : `${round4(travel)}*${p}`;
  const zoom = round4(MOTION_ZOOM * travel);
  const drift = round4(MOTION_DRIFT_ZOOM * travel);
  const centreX = "iw/2-(iw/zoom/2)";
  const centreY = "ih/2-(ih/zoom/2)";
  const midX = "(iw-iw/zoom)/2";
  const midY = "(ih-ih/zoom)/2";
  const forward = (size) => `(${size}-${size}/zoom)*${run}`;
  const backward = (size) => `(${size}-${size}/zoom)*(1-${run})`;
  switch (name) {
    case "push-in":
      return { z: `1+${zoom}*${p}`, x: centreX, y: centreY };
    case "pull-out":
      return { z: `${round4(1 + zoom)}-${zoom}*${p}`, x: centreX, y: centreY };
    case "pan-right":
      return { z: `${MOTION_PAN_ZOOM}`, x: backward("iw"), y: midY };
    case "pan-left":
      return { z: `${MOTION_PAN_ZOOM}`, x: forward("iw"), y: midY };
    case "tilt-up":
      return { z: `${MOTION_PAN_ZOOM}`, x: midX, y: backward("ih") };
    case "tilt-down":
      return { z: `${MOTION_PAN_ZOOM}`, x: midX, y: forward("ih") };
    default:
      return { z: `1+${drift}*${p}`, x: `${midX}${direction === "left" ? "-" : "+"}(iw-iw/zoom)*0.15*${run}`, y: centreY };
  }
}

/** How far a still of `frames` travels: the full move from MOTION_TRAVEL_SECONDS up, at least MOTION_TRAVEL_MIN of it below. */
export const motionTravel = (frames) => Math.max(MOTION_TRAVEL_MIN, Math.min(1, frames / (MOTION_TRAVEL_SECONDS * FPS)));

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

export function motionSegmentKey(scene, move, subtitles = null, previous = null) {
  return hash16([MOTION_ENCODER_VERSION, scene.frames, scene.keyframe.file, scene.keyframe.sha256, move.name, move.direction ?? null, subtitles, scene.transition, previous, ...(scene.card ? [MOTION_CARD_VERSION] : [])]);
}

const COLOUR = `format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709`;

/**
 * The inputs after the picture (input 0): the subtitle strips as input 1 when there are any,
 * then the previous scene's last frame, looped, for a dissolve.
 */
export function overlayInputs(subtitlesList, dissolveFrom) {
  const inputs = [];
  if (subtitlesList) inputs.push("-f", "concat", "-safe", "0", "-i", subtitlesList);
  if (dissolveFrom) inputs.push("-loop", "1", "-framerate", String(FPS), "-t", seconds(DISSOLVE_FRAMES + 2), "-i", dissolveFrom);
  return { inputs, subtitlesInput: subtitlesList ? 1 : null, dissolveInput: dissolveFrom ? (subtitlesList ? 2 : 1) : null };
}

/**
 * The rest of the graph once [pic] holds the scene's frames: the previous scene's last frame
 * dissolving away over it when asked, the subtitle strips laid over the bottom, then the colour
 * tags. Shared by clip and motion segments so the two encode identically.
 */
export function overlayGraph(picChain, { subtitlesInput, dissolveInput }) {
  const graph = [`[0:v]${picChain.join(",")}[pic]`];
  let last = "pic";
  if (dissolveInput !== null) {
    graph.push(`[${dissolveInput}:v]scale=${WIDTH}:${HEIGHT},format=yuva420p,fade=t=out:st=0:d=${seconds(DISSOLVE_FRAMES)}:alpha=1[prev]`);
    graph.push(`[${last}][prev]overlay=0:0:eof_action=pass[dissolved]`);
    last = "dissolved";
  }
  if (subtitlesInput !== null) {
    graph.push(`[${subtitlesInput}:v]format=rgba[strips]`);
    graph.push(`[${last}][strips]overlay=0:main_h-overlay_h:eof_action=pass[captioned]`);
    last = "captioned";
  }
  graph.push(`[${last}]${COLOUR}[out]`);
  return graph.join(";");
}

/** Same H.264 settings as a slide segment but tuned for film, so the segments still join without re-encoding. */
export function encodeArgs(inputs, graph, frames, outFile) {
  return [
    "-hide_banner", "-y", "-loglevel", "error",
    ...inputs,
    "-filter_complex", graph,
    "-map", "[out]",
    "-frames:v", String(frames),
    "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-tune", "film",
    "-bf", "2", "-g", String(FPS * 2), "-keyint_min", String(FPS),
    "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-r", String(FPS), "-fps_mode", "cfr", "-an", outFile,
  ];
}

/**
 * Encode one shot: the clip scaled and padded to 1920x1080, slowed and held as its fit says, cut
 * to the scene's frames, the previous scene's last frame dissolving away over it when asked, and
 * the subtitle strips laid over the bottom. Same H.264 settings as a slide segment but tuned for
 * film, so the segments still join without re-encoding.
 */
export function clipSegmentArgs({ clip, frames, fit, subtitlesList = null, dissolveFrom = null, outFile }) {
  const overlays = overlayInputs(subtitlesList, dissolveFrom);
  const chain = [
    `scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease:flags=lanczos`,
    `pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2`,
    ...(fit.speed !== 1 ? [`setpts=PTS/${fit.speed}`] : []),
    `fps=${FPS}`,
    ...(fit.pad > 0 ? [`tpad=stop_mode=clone:stop_duration=${seconds(fit.pad)}`] : []),
    `trim=end_frame=${frames}`,
    "setpts=PTS-STARTPTS",
  ];
  return encodeArgs(["-i", clip, ...overlays.inputs], overlayGraph(chain, overlays), frames, outFile);
}

/** The keyframe upscaled, then zoompan's crop window travelling as the move says, eased and scaled to the shot: one output frame per input frame. */
function motionChain(move, frames) {
  const { z, x, y } = zoompanExpr(move, frames, { eased: true, travel: motionTravel(frames) });
  return [
    `scale=${WIDTH * MOTION_SOURCE_SCALE}:${HEIGHT * MOTION_SOURCE_SCALE}:flags=lanczos`,
    `zoompan=z='${z}':x='${x}':y='${y}':d=1:s=${WIDTH}x${HEIGHT}:fps=${FPS}`,
  ];
}

/**
 * Encode one still shot: its keyframe looped for the scene's length, upscaled and animated by
 * zoompan (d=1, so every looped input frame becomes one output frame and the -t on the input,
 * the trim and -frames:v all agree on exactly `frames`), then the same dissolve, strips and
 * colour chain and the same encoder flags as a clip segment, so the join still copies.
 */
export function motionSegmentArgs({ keyframe, frames, move, subtitlesList = null, dissolveFrom = null, outFile }) {
  const overlays = overlayInputs(subtitlesList, dissolveFrom);
  // The keyframe is RGB and carries no colour description: converted here with the BT.709 matrix
  // (as the slides path does), or format=yuv420p in COLOUR would use swscale's default BT.601
  // and setparams would label the result BT.709, off-colour against the neighbouring clips.
  const chain = [...motionChain(move, frames), `scale=${WIDTH}:${HEIGHT}:out_color_matrix=bt709:out_range=tv`, "format=yuv420p", `trim=end_frame=${frames}`, "setpts=PTS-STARTPTS"];
  const inputs = ["-loop", "1", "-framerate", String(FPS), "-t", seconds(frames), "-i", keyframe, ...overlays.inputs];
  return encodeArgs(inputs, overlayGraph(chain, overlays), frames, outFile);
}

/**
 * Compare the first frame a motion segment would show with the keyframe itself, straight from
 * the picture chain: the strips carry the first line's text from frame 0 and a dissolve opens
 * on the previous scene, so the encoded segment's frame 0 is not the picture to measure. For a
 * move that starts at identity, this is the keyframe upscaled and scaled back, and a low score
 * means the zoompan expressions no longer open on the whole picture.
 */
export function motionFramePsnrArgs(keyframe, move, frames) {
  return [
    "-hide_banner", "-nostats", "-i", keyframe, "-i", keyframe,
    "-lavfi", `[0:v]${motionChain(move, frames).join(",")},select=eq(n\\,0),format=rgb24[a];[1:v]scale=${WIDTH}:${HEIGHT},format=rgb24[b];[a][b]psnr`,
    "-frames:v", "1", "-f", "null", "-",
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
export function mixFilter(music, totalSeconds, sfxInput = null) {
  // With sound effects (docs/videos/ILLUSTRATED.md) a third stereo track joins the mix as it is:
  // it is placed on the frame grid and gained already, and the voice is not ducked under it.
  const effects = sfxInput === null ? [] : [`[${sfxInput}:a]aformat=sample_rates=48000:channel_layouts=stereo[effects]`];
  const mixed = sfxInput === null ? "[voice][ducked]amix=inputs=2" : "[voice][ducked][effects]amix=inputs=3";
  return [
    bedFilter(music, totalSeconds),
    `[0:a]aformat=sample_rates=48000:channel_layouts=mono,${STEREO},asplit=2[voice][side]`,
    `[bed][side]sidechaincompress=threshold=${DUCK_THRESHOLD}:ratio=${duckRatio(music.duck_db)}:attack=${DUCK_ATTACK_MS}:release=${DUCK_RELEASE_MS}:makeup=1:level_sc=1[ducked]`,
    ...effects,
    `${mixed}:duration=first:dropout_transition=0:normalize=0[mix]`,
  ].join(";");
}

/** Voice and sound effects with no music bed: the voice to stereo, the effects laid over it. */
export function effectsFilter() {
  return [`[0:a]aformat=sample_rates=48000:channel_layouts=mono,${STEREO}[voice]`, "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[effects]", "[voice][effects]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]"].join(";");
}

const loudnorm = (extra = "") => `loudnorm=I=${LOUDNESS.integrated}:TP=${LOUDNESS.truePeak}:LRA=${LOUDNESS.range}${extra}`;

const musicInput = (music, totalSeconds) => ["-stream_loop", "-1", "-t", totalSeconds.toFixed(6), "-i", music];

/**
 * The inputs and the filter of the sound: the narration, the music bed when there is a track
 * (looped to the video's length), the effects track when there is one. `{ inputs, filter }`.
 */
export function soundGraph(narration, { musicFile = null, music = null, sfxFile = null }, totalSeconds) {
  if (musicFile) {
    return { inputs: ["-i", narration, ...musicInput(musicFile, totalSeconds), ...(sfxFile ? ["-i", sfxFile] : [])], filter: mixFilter(music, totalSeconds, sfxFile ? 2 : null) };
  }
  if (sfxFile) return { inputs: ["-i", narration, "-i", sfxFile], filter: effectsFilter() };
  throw new PlanError("soundGraph needs a music track or an effects track; plain narration uses plan.mjs normalizeArgs");
}

/** First loudnorm pass over the mix. `sound` is `{ musicFile, music, sfxFile }` or, as before, the music file alone. */
export function measureMixArgs(narration, musicFile, music, totalSeconds, sfxFile = null) {
  const { inputs, filter } = soundGraph(narration, { musicFile, music, sfxFile }, totalSeconds);
  return ["-hide_banner", "-nostats", ...inputs, "-filter_complex", `${filter};[mix]${loudnorm(":print_format=json")}[out]`, "-map", "[out]", "-f", "null", "-"];
}

/** The codec of the cut's own audio: AAC-LC at 384 kb/s; a dub (dubs/encode.mjs) may ask for its upload format instead. */
export const MIX_CODEC = ["-c:a", "aac", "-b:a", "384k"];

/** Second loudnorm pass over the mix with the first pass's measurement, linear, to stereo 48 kHz in `codec`. */
export function mixArgs(narration, musicFile, music, totalSeconds, measured, outFile, sfxFile = null, codec = MIX_CODEC) {
  const second = `:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`;
  const { inputs, filter } = soundGraph(narration, { musicFile, music, sfxFile }, totalSeconds);
  return ["-hide_banner", "-y", "-loglevel", "error", ...inputs, "-filter_complex", `${filter};[mix]${loudnorm(second)},aresample=48000[out]`, "-map", "[out]", ...codec, "-ar", "48000", outFile];
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
