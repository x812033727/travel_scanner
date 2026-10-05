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
// Folded into the build id: a change here re-encodes every Short. v2: the caption layer input.
export const MOTION_VERSION = 'shorts-motion-v2';
// The words a scene's `camera` may say, the long video's shot vocabulary (docs/videos/ILLUSTRATED.md).
export const CAMERA_WORDS = Object.freeze(['push in', 'pull out', 'pan left', 'pan right', 'tilt up', 'tilt down', 'drift']);
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
 * (the last input, an ffconcat list of the lit caption bars, karaoke.mjs) over the cards at the
 * bar's place when `captionsList` is given, then the colour tags and the Short's encoder (h264
 * high, 30 fps, closed GOPs of two seconds, BT.709), the same for every segment so the join
 * copies. Without a caption layer the arguments are what they were.
 */
export function segmentArgs({ background, move, frames, cardsList: list, dissolveFrom = null, captionsList = null, outFile }) {
  const inputs = ['-loop', '1', '-framerate', String(FPS), '-t', seconds(frames), '-i', background, '-f', 'concat', '-safe', '0', '-i', list];
  if (dissolveFrom) inputs.push('-loop', '1', '-framerate', String(FPS), '-t', seconds(DISSOLVE_FRAMES + 2), '-i', dissolveFrom);
  if (captionsList) inputs.push('-f', 'concat', '-safe', '0', '-i', captionsList);
  const graph = [`[0:v]${backgroundChain(move, frames).join(',')}[pic]`];
  let last = 'pic';
  if (dissolveFrom) {
    graph.push(`[2:v]scale=${WIDTH}:${HEIGHT},format=yuva420p,fade=t=out:st=0:d=${seconds(DISSOLVE_FRAMES)}:alpha=1[prev]`);
    graph.push(`[${last}][prev]overlay=0:0:eof_action=pass[dissolved]`);
    last = 'dissolved';
  }
  graph.push('[1:v]format=rgba[cards]');
  graph.push(`[${last}][cards]overlay=0:0:eof_action=pass[carded]`);
  last = 'carded';
  if (captionsList) {
    graph.push(`[${dissolveFrom ? 3 : 2}:v]format=rgba[captions]`);
    graph.push(`[${last}][captions]overlay=${CAPTION_BOX.x}:${CAPTION_BOX.y}:eof_action=pass[captioned]`);
    last = 'captioned';
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
