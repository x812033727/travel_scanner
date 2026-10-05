// A Short's picture, scene by scene (docs/videos/SHORTS.md §工具端): every scene is one segment of
// the cut, a background under a camera move for the whole scene and, laid over it, the transparent
// card of each phrase in turn (headline, rows, caption bar, count and progress). The background is
// the scene's picture (a keyframe of the long video, cropped to 9:16 and travelling as its camera
// says) or, for a scene of cards alone, the theme's backdrop drifting; scenes join with a dissolve
// from the previous scene's last frame, the first scene opening on a cut. The camera expressions
// and the dissolve length are the long video's (assemble/drama.mjs), so the two look alike.
import { DISSOLVE_FRAMES, MOTION_SOURCE_SCALE, motionMove, zoompanExpr } from '../assemble/drama.mjs';
import { PROFILE } from './core.mjs';
import { CAPTION_BOX } from './karaoke.mjs';

export { DISSOLVE_FRAMES };
// Folded into the build id: a change here re-encodes every Short. v2: the caption layer input;
// v3: the loop tail, the last frames dissolving into the first.
export const MOTION_VERSION = 'shorts-motion-v3';
// The words a scene's `camera` may say, the long video's shot vocabulary (docs/videos/ILLUSTRATED.md).
export const CAMERA_WORDS = Object.freeze(['push in', 'pull out', 'pan left', 'pan right', 'tilt up', 'tilt down', 'drift']);
// The loop (docs/videos/SHORTS.md §自動品管, `grammar`): YouTube replays a Short from its first
// frame, so the last segment's final frames dissolve into that frame, this many of them, the
// last being the frame itself; then the replay joins without a jump and the first frame, the
// thumbnail, is what the viewer sees at both ends.
export const LOOP_FRAMES = 12;
// What the measurement of a cut's two ends has to score (build.mjs measureFinal, qa.mjs grammar):
// the cover against frame 0, which the build makes identical (infinite), and frame 0 against the
// last frame, which the loop tail makes the same picture encoded twice (around 50 dB).
export const COVER_MIN_PSNR = 40;
export const LOOP_MIN_PSNR = 30;
// A receipt writes a PSNR as a number, so an identical picture (infinite) and anything above
// this are written as this, well above what any re-encode scores.
export const PSNR_CAP = 100;
const { width: WIDTH, height: HEIGHT, fps: FPS } = PROFILE;
const seconds = (frames) => (frames / FPS).toFixed(6);
const COLOUR = 'format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709';

/** The camera move of a scene: its `camera` words, else a drift. */
export const cameraOf = (scene) => motionMove({ camera: scene?.camera });

/**
 * What a scene's background is: its picture when the scene names a camera over an asset (a
 * keyframe of the long video), else the theme's backdrop; an asset without a camera (an
 * experiment's evidence) stays inside the card, legible, over the backdrop.
 */
export const backgroundOf = (scene) => (scene?.asset && scene?.camera ? 'picture' : 'backdrop');

/** The scene's segment and the scene's frames, from the timeline's cues. */
export function sceneSpans(timeline) {
  const spans = [];
  for (const cue of timeline.cues) {
    const last = spans.at(-1);
    if (last && last.sceneIndex === cue.sceneIndex) {
      last.frames += cue.frames;
      last.cues.push(cue);
    } else spans.push({ sceneIndex: cue.sceneIndex, startFrame: cue.startFrame, frames: cue.frames, cues: [cue] });
  }
  return spans;
}

/**
 * The picture chain of a background: the image scaled to cover the upscaled frame (a 16:9
 * keyframe keeps only its middle 32%, which is why the long video's prompts keep the subject in the
 * middle of the picture), cropped, then zoompan's window travelling as the move says, one output
 * frame per looped input frame.
 */
export function backgroundChain(move, frames) {
  const { z, x, y } = zoompanExpr(move, frames);
  const w = Math.round(WIDTH * MOTION_SOURCE_SCALE);
  const h = Math.round(HEIGHT * MOTION_SOURCE_SCALE);
  return [
    `scale=${w}:${h}:force_original_aspect_ratio=increase:flags=lanczos`,
    `crop=${w}:${h}`,
    `zoompan=z='${z}':x='${x}':y='${y}':d=1:s=${WIDTH}x${HEIGHT}:fps=${FPS}`,
    `scale=${WIDTH}:${HEIGHT}:out_color_matrix=bt709:out_range=tv`,
    'format=yuv420p',
    `trim=end_frame=${frames}`,
    'setpts=PTS-STARTPTS',
  ];
}

/**
 * An ffconcat list of the scene's cards, each shown for its phrase's frames, the last one named
 * again at the end: the concat demuxer gives the last image its duration only when another entry
 * follows it (assemble/plan.mjs concatList does the same for the subtitle strips), and without
 * that the scene's last frame would show the bare background and the dissolve into the next
 * scene would start from it.
 */
export function cardsList(cards) {
  const quote = (file) => `'${file.replace(/\\/g, '/').replace(/'/g, "'\\''")}'`;
  const lines = ['ffconcat version 1.0'];
  for (const { file, frames } of cards) lines.push(`file ${quote(file)}`, `option framerate ${FPS}`, `duration ${seconds(frames)}`);
  if (cards.length) lines.push(`file ${quote(cards.at(-1).file)}`, `option framerate ${FPS}`);
  return `${lines.join('\n')}\n`;
}

/**
 * The ffmpeg arguments of one scene's segment: the background (input 0) under its move, the
 * cards (input 1, an ffconcat list of transparent PNGs) over it, the previous scene's last frame
 * (input 2) fading away over the first frames when `dissolveFrom` is given, the caption layer
 * (an ffconcat list of the lit caption bars, karaoke.mjs) over the cards at the bar's place when
 * `captionsList` is given, the Short's first frame (`loopTo`, a PNG, on the last scene) fading in
 * over everything through the last LOOP_FRAMES frames so the cut ends on the frame it began
 * with, then the colour tags and the Short's encoder (h264 high, 30 fps, closed GOPs of two
 * seconds, BT.709), the same for every segment so the join copies. Without a caption layer or a
 * loop the arguments are what they were.
 *
 * The loop input is LOOP_FRAMES + 2 frames of the still, faded in by frame count (the first at
 * nothing, the one LOOP_FRAMES later at everything) and moved to the segment's end with setpts;
 * overlay passes the frames before it through untouched and repeats its last frame after it, so
 * the segment's last frame is the still whatever image2 rounds the input's length to.
 */
export function segmentArgs({ background, move, frames, cardsList: list, dissolveFrom = null, captionsList = null, loopTo = null, outFile }) {
  const inputs = ['-loop', '1', '-framerate', String(FPS), '-t', seconds(frames), '-i', background, '-f', 'concat', '-safe', '0', '-i', list];
  let next = 2;
  const dissolveInput = dissolveFrom ? next++ : null;
  const captionsInput = captionsList ? next++ : null;
  const loopInput = loopTo ? next++ : null;
  if (dissolveFrom) inputs.push('-loop', '1', '-framerate', String(FPS), '-t', seconds(DISSOLVE_FRAMES + 2), '-i', dissolveFrom);
  if (captionsList) inputs.push('-f', 'concat', '-safe', '0', '-i', captionsList);
  if (loopTo) inputs.push('-loop', '1', '-framerate', String(FPS), '-t', seconds(LOOP_FRAMES + 2), '-i', loopTo);
  const graph = [`[0:v]${backgroundChain(move, frames).join(',')}[pic]`];
  let last = 'pic';
  if (dissolveFrom) {
    graph.push(`[${dissolveInput}:v]scale=${WIDTH}:${HEIGHT},format=yuva420p,fade=t=out:st=0:d=${seconds(DISSOLVE_FRAMES)}:alpha=1[prev]`);
    graph.push(`[${last}][prev]overlay=0:0:eof_action=pass[dissolved]`);
    last = 'dissolved';
  }
  graph.push('[1:v]format=rgba[cards]');
  graph.push(`[${last}][cards]overlay=0:0:eof_action=pass[carded]`);
  last = 'carded';
  if (captionsList) {
    graph.push(`[${captionsInput}:v]format=rgba[captions]`);
    graph.push(`[${last}][captions]overlay=${CAPTION_BOX.x}:${CAPTION_BOX.y}:eof_action=pass[captioned]`);
    last = 'captioned';
  }
  if (loopTo) {
    graph.push(`[${loopInput}:v]scale=${WIDTH}:${HEIGHT},format=yuva420p,fade=t=in:s=0:n=${LOOP_FRAMES}:alpha=1,setpts=PTS+${seconds(Math.max(0, frames - LOOP_FRAMES - 1))}/TB[loop]`);
    graph.push(`[${last}][loop]overlay=0:0:eof_action=repeat[looped]`);
    last = 'looped';
  }
  graph.push(`[${last}]${COLOUR}[out]`);
  return [
    '-y', '-v', 'error', ...inputs,
    '-filter_complex', graph.join(';'), '-map', '[out]', '-frames:v', String(frames),
    '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '20', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-g', String(FPS * 2), '-keyint_min', String(FPS * 2), '-sc_threshold', '0', '-flags', '+cgop',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(FPS), '-fps_mode', 'cfr', outFile,
  ];
}

/** The last frame of a segment as a PNG, for the dissolve into the next scene. */
export function lastFrameArgs(segment, frames, outFile) {
  return ['-y', '-v', 'error', '-i', segment, '-vf', `select=eq(n\\,${frames - 1})`, '-fps_mode', 'passthrough', '-frames:v', '1', outFile];
}

/** The first frame of a segment as a PNG: the cover and the contact sheet. */
export function firstFrameArgs(segment, outFile) {
  return ['-y', '-v', 'error', '-i', segment, '-frames:v', '1', outFile];
}

/**
 * The PSNR of frame `n` of a cut against an image, or against frame `m` of a cut when `m` is
 * given, both as RGB on the same clock (the way firstFrameArgs writes the cover): ffmpeg prints
 * `PSNR ... average:` on stderr, which parsePsnr reads. An identical picture averages `inf`.
 */
export function framePsnrArgs(cut, n, other, m = null) {
  const frame = (input, index) => `[${input}:v]select=eq(n\\,${index}),setpts=PTS-STARTPTS,format=rgb24`;
  const b = m === null ? '[1:v]format=rgb24[b]' : `${frame(1, m)}[b]`;
  return ['-hide_banner', '-nostats', '-i', cut, '-i', other, '-lavfi', `${frame(0, n)}[a];${b};[a][b]psnr`, '-frames:v', '1', '-f', 'null', '-'];
}

/** The average PSNR ffmpeg's psnr filter printed, Infinity for identical pictures; throws when it printed none. */
export function parsePsnr(stderr) {
  const match = /PSNR .*average:(inf|[\d.]+)/.exec(String(stderr));
  if (!match) throw new Error('ffmpeg did not report a PSNR');
  return match[1] === 'inf' ? Infinity : Number(match[1]);
}

/** A PSNR as a receipt writes it: two decimals, at most PSNR_CAP. */
export const psnrValue = (psnr) => Math.min(PSNR_CAP, Number(Number(psnr).toFixed(2)));

/** A PSNR as a sentence says it. */
export const psnrText = (psnr) => (psnr === Infinity ? 'inf, identical' : Number.isFinite(psnr) ? `${Number(psnr).toFixed(1)} dB` : 'not measured');

/**
 * Why a cut's two ends are not a loop's; empty when they are. `measured` is measureFinal's
 * `grammar`: { cover_psnr, loop_psnr }, the cover against frame 0 and frame 0 against the last
 * frame; null when there was no cover to measure against.
 */
export function loopProblems(measured) {
  if (!measured) return ['the first and last frames were not measured against the cover'];
  const problems = [];
  if (!(measured.cover_psnr >= COVER_MIN_PSNR)) problems.push(`the cover is not the first frame (PSNR ${psnrText(measured.cover_psnr)}, below ${COVER_MIN_PSNR} dB)`);
  if (!(measured.loop_psnr >= LOOP_MIN_PSNR)) problems.push(`the last frame does not return to the first (PSNR ${psnrText(measured.loop_psnr)}, below ${LOOP_MIN_PSNR} dB)`);
  return problems;
}

/**
 * Where a Short's sound effects fall (docs/videos/ILLUSTRATED.md §配樂與音效, the same three
 * sounds as the long video): a stamp as each scene after the first opens, a pop on a phrase that
 * shows the scene's big number, a whoosh five frames before a dissolve when the scene carries no
 * stamp; never two within 1.5 seconds, never at frame 0.
 */
export function shortSfxPlan(doc, timeline, { dissolves = true } = {}) {
  const wanted = [];
  const spans = sceneSpans(timeline);
  spans.forEach((span, index) => {
    const scene = doc.scenes[span.sceneIndex];
    if (index > 0) wanted.push({ frame: span.startFrame, sound: 'stamp', scene: span.sceneIndex });
    else if (dissolves && index > 0) wanted.push({ frame: Math.max(0, span.startFrame - 5), sound: 'whoosh', scene: span.sceneIndex });
    if (scene?.big) wanted.push({ frame: span.cues[0].startFrame, sound: 'pop', scene: span.sceneIndex });
  });
  wanted.sort((a, b) => a.frame - b.frame);
  const events = [];
  let last = -Infinity;
  for (const event of wanted) {
    if (event.frame <= 0 || event.frame - last < Math.round(1.5 * FPS)) continue;
    events.push(event);
    last = event.frame;
  }
  return events;
}
