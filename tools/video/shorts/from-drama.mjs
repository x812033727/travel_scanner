// `from-drama`: a vertical Short cut from an approved 16:9 drama episode (docs/videos/SHORTS.md
// §三條內容線, §工具端). The cheap route to a drama Short: no picture is generated. The episode's
// final.mp4 is cut between --from and --to, and a 9:16 window (WINDOW, 608×1080 of the 1920×1080
// picture) is cropped out of it and scaled to the Shorts frame. The window follows the subject:
// one `locate` call a shot (the shot's keyframe when the work directory has it, else a frame
// pulled out of the cut by number) gives the main character's box, the window centres on it,
// holds through the shot and moves linearly over the last MOVE_FRAMES before the next shot, so
// a cut lands framed on the next subject; a card scene keeps the centre. The episode's own sound
// (voice, music, effects) is kept and brought to the Short's loudness.
//
// The captions are the Shorts caption layer (core.mjs captionHtml, lit by karaoke.mjs's timing),
// never libass: one transparent picture a lit state, laid over the moving picture at the caption
// bar (motion.mjs lays the same list over a card), measured inside the Shorts safe area, so
// `layout` can pass where an import's cannot. What comes out is a build of this tool: check-audio,
// qa, package and push take the directory as any other (`line: "drama"`, `source.slug`).
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

import { DISSOLVE_FRAMES, frameArgs } from '../assemble/drama.mjs';
import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { HEIGHT as SOURCE_HEIGHT, WIDTH as SOURCE_WIDTH, muxArgs } from '../assemble/plan.mjs';
import { approvalState } from '../core/approvals.mjs';
import { appliedBranding, presentationTimeline } from '../core/branding.mjs';
import { ROOT, docDir as docDirOf, readJson, resolveWorkBase, resolveWorkdir, stopRequested, videoFile } from '../core/paths.mjs';
import { locate, mediaStatus, putFile, scaleBox } from '../media/client.mjs';
import { parseWav, requireNarrationFormat } from '../tts/wav.mjs';
import { embeddedFont, loudnessProblems, loudnessResult, measureFinal, profileProblems } from './build.mjs';
import { PROFILE, SCRIPT_FILE, USAGE_FILE, captionHtml, parseSrt, saveJson, sha256, srt, validate } from './core.mjs';
import { timelineFromCaptions } from './import.mjs';
import { CAPTION_BOX, captionLines, captionsOption, captionsSummary, phraseGroups, timingFile } from './karaoke.mjs';
import { themeOf } from './layouts.mjs';
import { cardsList, firstFrameArgs } from './motion.mjs';

// Folded into the build id with this module's own code hash: a change here is another cut.
export const REFRAME_VERSION = 'shorts-reframe-v1';
// The 9:16 window of a 1080-high picture: 1080 × 9 / 16 is 607.5, taken even.
export const WINDOW = Object.freeze({ width: 608, height: SOURCE_HEIGHT });
export const SOURCE = Object.freeze({ width: SOURCE_WIDTH, height: SOURCE_HEIGHT });
// The window moves over this many frames before a shot change: the drama's own dissolve length,
// so at a dissolve the move hides inside the blend and at a cut it is a half-second settle.
export const MOVE_FRAMES = DISSOLVE_FRAMES;
// Where an episode's zh-TW captions are, in the order they are looked for: the captions stage
// writes the first, package copies it to the second.
export const CAPTION_FILES = Object.freeze(['captions/zh-TW.srt', 'upload/captions/zh-TW.srt', 'upload/zh-TW.srt']);
// What --meta may say about the Short; the tool decides its line, source and scenes.
export const META_KEYS = Object.freeze(['slug', 'series', 'titles', 'description', 'hashtags', 'tags', 'links', 'headlines', 'synthetic_media']);
// A Short needs this many phrases: fewer make no script (core.mjs validate wants 3 scenes).
export const MIN_PHRASES = 3;
// How many phrases a scene of the script holds when --meta names no headlines; a scene is a
// span of the variety check's structure, nothing on the picture.
export const PHRASES_PER_SCENE = 3;
export const MAX_SCENES = 12;
export const CENTRE_X = (SOURCE.width - WINDOW.width) / 2;
const COLOUR = 'format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709';
// The Short's encoder, as motion.mjs encodes a segment: one output, so no join is needed.
const ENCODER = ['-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '20', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', String(PROFILE.fps * 2), '-keyint_min', String(PROFILE.fps * 2), '-sc_threshold', '0', '-flags', '+cgop', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(PROFILE.fps), '-fps_mode', 'cfr'];
const number = (i) => String(i).padStart(3, '0');
const secondsOf = (frames) => Number((frames / PROFILE.fps).toFixed(3));

/** The frames of the episode the Short covers: --from and --to in seconds, on the frame grid, inside the Shorts length. */
export function spanFrames(from, to, totalFrames, range = PROFILE) {
  const seconds = (value, name) => {
    const count = Number(value);
    if (typeof value === 'boolean' || value === '' || value === null || value === undefined || !Number.isFinite(count) || count < 0) throw new Error(`--${name} must be a number of seconds from the start of the episode`);
    return count;
  };
  const startFrame = Math.round(seconds(from, 'from') * PROFILE.fps);
  const endFrame = Math.round(seconds(to, 'to') * PROFILE.fps);
  if (endFrame <= startFrame) throw new Error('--to must come after --from');
  if (endFrame > totalFrames) throw new Error(`--to ${to} is past the end of the episode (${secondsOf(totalFrames)} s)`);
  const length = (endFrame - startFrame) / PROFILE.fps;
  if (length < range.minSeconds || length > range.maxSeconds) throw new Error(`the span is ${length.toFixed(2)}s; a Short is ${range.minSeconds}–${range.maxSeconds}s (move --from or --to; never speed the picture up)`);
  return { startFrame, endFrame, frames: endFrame - startFrame };
}

/**
 * A caption's words as one phrase: the drama's cue was broken into two lines for the 16:9 strip,
 * and the Shorts bar breaks it again for its own width (karaoke.mjs captionLines). A line break
 * between two Latin words keeps a space; between two CJK characters it goes.
 */
export function cueText(text) {
  return String(text).replace(/\s*\n\s*/g, (match, offset, whole) => {
    const before = whole[offset - 1] ?? '';
    const after = whole[offset + match.length] ?? '';
    return /[A-Za-z0-9]/.test(before) && /[A-Za-z0-9]/.test(after) ? ' ' : '';
  }).trim();
}

/**
 * The episode's captions inside the span, on the Short's own clock ({ start, end, text } in
 * seconds from --from). A caption the span cuts in half is refused with the times that would
 * not: the voice is cut with it, and the listener's check would flag the half.
 */
export function spanCues(cues, startFrame, endFrame) {
  const inside = [];
  for (const [index, cue] of cues.entries()) {
    const start = Math.round(cue.start * PROFILE.fps);
    const end = Math.round(cue.end * PROFILE.fps);
    if (end <= startFrame || start >= endFrame) continue;
    if (start < startFrame || end > endFrame) {
      const edge = start < startFrame ? 'from' : 'to';
      const better = edge === 'from' ? [`--from ${secondsOf(start)}`, `--from ${secondsOf(end)}`] : [`--to ${secondsOf(end)}`, `--to ${secondsOf(start)}`];
      throw new Error(`caption ${index + 1} (${secondsOf(start)}–${secondsOf(end)} s, 「${cueText(cue.text)}」) is cut by --${edge}: use ${better.join(' or ')}, so no phrase is cut in half`);
    }
    if (end > start) inside.push({ start: secondsOf(start - startFrame), end: secondsOf(end - startFrame), text: cueText(cue.text) });
  }
  return inside;
}

/**
 * The episode's scenes inside the span, clipped to it, on the Short's frames: `picture_frame` is
 * the episode frame in the middle of the clipped part, the frame to locate the subject on when
 * the shot has no keyframe here. The timeline's scenes are contiguous, so the spans are too.
 */
export function shotSpans(timeline, startFrame, endFrame) {
  const spans = [];
  for (const scene of timeline?.scenes ?? []) {
    if (scene.end_frame <= startFrame || scene.start_frame >= endFrame) continue;
    const first = Math.max(scene.start_frame, startFrame);
    const start = first - startFrame;
    const end = Math.min(scene.end_frame, endFrame) - startFrame;
    spans.push({ id: scene.id, template: scene.template ?? 'shot', start, end, picture_frame: first + Math.floor((end - start) / 2) });
  }
  const frames = endFrame - startFrame;
  if (!spans.length || spans[0].start !== 0 || spans.at(-1).end !== frames || spans.some((span, index) => index > 0 && span.start !== spans[index - 1].end)) {
    throw new Error('the episode timeline does not cover the span: its scenes have a gap, or end before --to');
  }
  return spans;
}

/** The window's left edge for a subject centred at `centre` (source pixels): inside the picture. */
export const windowX = (centre) => Math.min(Math.max(Math.round(centre - WINDOW.width / 2), 0), SOURCE.width - WINDOW.width);

/** The window's left edge for a located box (0–1000 scale) of a `picture` of that size: centred on the box. */
export function windowFor(box, picture = SOURCE) {
  const pixels = scaleBox(box, picture.width, picture.height);
  return windowX(((pixels.left + pixels.right) / 2) * (SOURCE.width / picture.width));
}

/**
 * The subject the window follows among the boxes locate returned: the first of the shot's
 * characters that was found, by label; else the box the model is surest of; null for none,
 * when the window stays at the centre.
 */
export function pickSubject(boxes, labels = []) {
  const usable = (Array.isArray(boxes) ? boxes : []).filter((each) => Array.isArray(each?.box) && each.box.length === 4);
  if (!usable.length) return null;
  const fold = (value) => String(value ?? '').trim().toLowerCase();
  const found = labels.map((label) => usable.find((each) => fold(each.label) === fold(label))).find(Boolean)
    ?? [...usable].sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0))[0];
  return { label: String(found.label ?? 'subject'), score: Number(found.score) || 0, box: found.box };
}

/** The names of a shot's characters, in the script's order (the main character first), for locate's labels. */
export function shotLabels(video, shotId) {
  if (!video) return [];
  const scene = (video.scenes ?? []).find((each) => each.id === shotId);
  const names = new Map((video.characters ?? []).map((character) => [character.id, character.name]));
  return [...new Set((scene?.data?.characters ?? []).map((id) => String(names.get(id) ?? id).trim()).filter(Boolean))];
}

/**
 * The window over the Short, piece by piece: each shot holds its window, and where the next
 * shot's window is elsewhere, the last `moveFrames` of the shot (fewer in a shorter shot) move
 * linearly to it, so the first frame after the change is already framed. `spans` are
 * [{ start, end, x }] contiguous on the Short's frames; the pieces cover them exactly, two
 * scenes at the same window holding as one piece.
 */
export function cropPieces(spans, moveFrames = MOVE_FRAMES) {
  const pieces = [];
  const hold = (from, to, x) => {
    const last = pieces.at(-1);
    if (last && last.x0 === x && last.x1 === x && last.to === from) last.to = to;
    else pieces.push({ from, to, x0: x, x1: x });
  };
  spans.forEach((span, index) => {
    const next = spans[index + 1];
    const move = next && next.x !== span.x ? Math.min(moveFrames, span.end - span.start) : 0;
    const holdEnd = span.end - move;
    if (holdEnd > span.start) hold(span.start, holdEnd, span.x);
    if (move > 0) pieces.push({ from: holdEnd, to: span.end, x0: span.x, x1: next.x });
  });
  return pieces;
}

/** The window's left edge at output frame `n`, as the crop expression computes it. */
export function windowAt(pieces, n) {
  const piece = pieces.find((each) => n >= each.from && n < each.to) ?? pieces.at(-1);
  if (!piece) return CENTRE_X;
  if (piece.x0 === piece.x1) return piece.x0;
  return Math.round(piece.x0 + ((piece.x1 - piece.x0) * (n - piece.from + 1)) / (piece.to - piece.from));
}

/**
 * The crop filter's x as an expression of the output frame number `n`: a hold is its number, a
 * move runs from x0 on its first frame to x1 on its last (a cut then lands on the next shot's
 * window), the pieces nested as `if(lt(n, to), piece, rest)`.
 */
export function cropExpr(pieces) {
  if (!pieces.length) return String(CENTRE_X);
  const term = (piece) => (piece.x0 === piece.x1 ? String(piece.x0) : `${piece.x0}+(${piece.x1 - piece.x0})*(n-${piece.from}+1)/${piece.to - piece.from}`);
  let expr = term(pieces.at(-1));
  for (let index = pieces.length - 2; index >= 0; index -= 1) expr = `if(lt(n,${pieces[index].to}),${term(pieces[index])},${expr})`;
  return expr;
}

/** The picture chain: the span by frame number (never by seeking), the window cropped out as the expression says, scaled to the Shorts frame. */
export function reframeChain(startFrame, endFrame, expr) {
  return [
    `trim=start_frame=${startFrame}:end_frame=${endFrame}`,
    'setpts=PTS-STARTPTS',
    `crop=${WINDOW.width}:${WINDOW.height}:x='${expr}':y=0`,
    `scale=${PROFILE.width}:${PROFILE.height}:flags=lanczos`,
  ];
}

/**
 * The ffmpeg arguments of the Short's picture: the episode (input 0) reframed, the caption
 * layer (input 1, an ffconcat list of the lit caption bars and the blank between phrases) laid
 * over it at the bar, the colour tags and the Short's encoder; no sound here.
 */
export function reframeArgs({ final, startFrame, endFrame, expr, captionsList, outFile }) {
  const graph = [
    `[0:v]${reframeChain(startFrame, endFrame, expr).join(',')}[pic]`,
    '[1:v]format=rgba[captions]',
    `[pic][captions]overlay=${CAPTION_BOX.x}:${CAPTION_BOX.y}:eof_action=pass[captioned]`,
    `[captioned]${COLOUR}[out]`,
  ].join(';');
  return ['-y', '-v', 'error', '-i', final, '-f', 'concat', '-safe', '0', '-i', captionsList, '-filter_complex', graph, '-map', '[out]', '-frames:v', String(endFrame - startFrame), '-an', ...ENCODER, outFile];
}

/**
 * The Short's sound: the span of the episode's mix, to stereo 48 kHz, through loudnorm's two
 * passes (measured without `measured`, then applied linearly) to the Short's −14 LUFS, as
 * build.mjs normalizes a plain narration.
 */
export function cutAudioArgs(final, startSeconds, seconds, outFile, measured = null) {
  const cut = `atrim=start=${startSeconds.toFixed(6)}:end=${(startSeconds + seconds).toFixed(6)},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo`;
  if (!measured) return ['-hide_banner', '-nostats', '-i', final, '-vn', '-af', `${cut},loudnorm=I=-14:TP=-1:LRA=11:print_format=json`, '-f', 'null', '-'];
  const second = `measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`;
  return ['-y', '-hide_banner', '-loglevel', 'error', '-i', final, '-vn', '-af', `${cut},loudnorm=I=-14:TP=-1:LRA=11:${second},aresample=48000`, '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '192k', outFile];
}

/**
 * The caption layer of a reframed drama: core.mjs captionHtml draws the words alone, because on
 * a card the bar's background is the card's. Here there is no card, so the bar gets the theme's
 * background on the layer itself: one rule added, nothing in the layout moves.
 */
export function dramaCaptionHtml(doc, options = {}) {
  return captionHtml(doc, options).replace('</style>', `\n.caption{background:${themeOf(doc).colors.caption}}\n</style>`);
}

/**
 * The layer's list over the whole Short: each phrase's states in turn, held for their frames,
 * the blank picture wherever nobody speaks, together exactly the Short's frames. `fileOf(cue,
 * state)` names a state's picture.
 */
export function captionLayerEntries(timeline, phrases, blank, fileOf) {
  const entries = [];
  const push = (file, frames) => {
    if (frames <= 0) return;
    const last = entries.at(-1);
    if (last && last.file === file) last.frames += frames;
    else entries.push({ file, frames });
  };
  let at = 0;
  for (const cue of timeline.cues) {
    const phrase = phrases.find((each) => each.cue === cue.index);
    if (!phrase) throw new Error(`no caption states for phrase ${cue.index}`);
    push(blank, cue.startFrame - at);
    phrase.states.forEach((state, index) => push(fileOf(cue.index, index), state.frames));
    at = cue.endFrame;
  }
  push(blank, timeline.frames - at);
  const total = entries.reduce((sum, entry) => sum + entry.frames, 0);
  if (total !== timeline.frames) throw new Error(`the caption layer covers ${total} frames of a ${timeline.frames}-frame Short`);
  return entries;
}

/** The Short's slug: the episode's, the span's frames after it, inside the slug's 80 characters. */
export function shortSlugOf(slug, startFrame, endFrame) {
  const suffix = `-short-${startFrame}-${endFrame}`;
  return `${String(slug).slice(0, 80 - suffix.length).replace(/-+$/, '')}${suffix}`;
}

/** The Short's series: the work the episode belongs to, else the episode itself. */
export const seriesOf = (video, slug) => String(video?.series?.slug ?? slug).slice(0, 40).replace(/-+$/, '');

/**
 * The phrases in scenes, as evenly as they divide: three a scene, between three and twelve
 * scenes, the larger scenes first; --meta's headlines, when given, make one scene each. A
 * scene's headline is its first phrase (a drama Short shows no card; the headline names the
 * scene in the script and on the site).
 */
export function phraseScenes(cues, headlines = null) {
  const named = Array.isArray(headlines) && headlines.length > 0;
  const count = named ? headlines.length : Math.max(MIN_PHRASES, Math.min(MAX_SCENES, Math.ceil(cues.length / PHRASES_PER_SCENE)));
  if (cues.length < count) throw new Error(`${cues.length} phrases cannot fill ${count} scenes${named ? ': fewer headlines in --meta' : ''}`);
  const scenes = [];
  let at = 0;
  for (let index = 0; index < count; index += 1) {
    const size = Math.ceil((cues.length - at) / (count - index));
    const slice = cues.slice(at, at + size);
    scenes.push({ headline: named ? headlines[index] : [...slice[0].text].slice(0, 36).join(''), narration: slice.map((each) => each.text) });
    at += size;
  }
  return scenes;
}

/**
 * The Short's script: the captions as its phrases, in scenes, the episode's YouTube title and
 * description unless --meta says otherwise, leading back to the episode and the span it was
 * cut from.
 */
export function shortScript({ slug, video = null, meta = null, cues, startFrame, endFrame }) {
  if (meta !== null && (typeof meta !== 'object' || Array.isArray(meta))) throw new Error('--meta must be a JSON object');
  const strange = Object.keys(meta ?? {}).filter((key) => !META_KEYS.includes(key));
  if (strange.length) throw new Error(`--meta may set ${META_KEYS.join(', ')}; not ${strange.join(', ')} (the tool decides the line, the source and the scenes)`);
  if (cues.length < MIN_PHRASES) throw new Error(`only ${cues.length} captions between --from and --to; a Short needs at least ${MIN_PHRASES} phrases`);
  const title = meta?.titles?.[0] ?? video?.youtube?.title;
  const description = meta?.description ?? video?.youtube?.description;
  if (!title || !description) throw new Error(`no title or description for the Short (${video ? "the episode's video.json names none" : `${slug} has no video.json in this checkout`}): give --meta with titles and description`);
  const spare = [...`${cues[0].text}｜${title}`].slice(0, 100).join('');
  const tags = (meta?.tags ?? video?.youtube?.tags ?? []).filter((tag) => typeof tag === 'string' && tag.trim() && [...tag].length <= 30 && !/[<>,]/.test(tag)).slice(0, 15);
  return {
    schema_version: 2,
    slug: meta?.slug ?? shortSlugOf(slug, startFrame, endFrame),
    format: 'shorts',
    locale: 'zh-TW',
    line: 'drama',
    series: meta?.series ?? seriesOf(video, slug),
    titles: meta?.titles ?? [title, spare],
    description,
    source: { slug, start_seconds: secondsOf(startFrame), end_seconds: secondsOf(endFrame) },
    ...(tags.length ? { tags } : {}),
    ...(meta?.hashtags !== undefined ? { hashtags: meta.hashtags } : {}),
    ...(meta?.links !== undefined ? { links: meta.links } : {}),
    ...(meta?.synthetic_media !== undefined ? { synthetic_media: meta.synthetic_media } : {}),
    scenes: phraseScenes(cues, meta?.headlines ?? null),
  };
}

/**
 * The episode as the Short reads it: its approved cut, its timeline as presented (a branded cut
 * carries the channel's intro before the body, and the captions already count it), its zh-TW
 * captions, its script when this checkout has it (titles and the characters' names) and its
 * keyframes when the work directory has them.
 */
export function readEpisode({ slug, workdir, root = ROOT }) {
  const final = path.join(workdir, 'final.mp4');
  if (!existsSync(final)) throw new Error(`no final.mp4 in ${workdir}: assemble ${slug} first`);
  const body = readJson(path.join(workdir, 'timeline.json'), null);
  if (!body) throw new Error(`no timeline.json in ${workdir}: run tts for ${slug} first`);
  const timeline = presentationTimeline(body, appliedBranding(readJson(path.join(workdir, 'checks.json'), null)));
  const captionFile = CAPTION_FILES.map((name) => path.join(workdir, name)).find((file) => existsSync(file));
  if (!captionFile) throw new Error(`no zh-TW captions in ${workdir} (${CAPTION_FILES.join(', ')}): run captions for ${slug} first`);
  return {
    slug,
    workdir,
    final,
    timeline,
    cues: parseSrt(readFileSync(captionFile, 'utf8')),
    captionFile,
    video: readJson(videoFile(slug, root), null),
    keyframes: readJson(path.join(workdir, 'keyframes', 'manifest.json'), null),
    docDir: docDirOf(slug, root),
  };
}

// Runs in the page: the bar's words inside the bar, the bar above the Shorts interface and the
// words clear of its sides (docs/videos/SHORTS.md: content x 78–902, the caption above y 1600).
function measureLayer() {
  const problems = [];
  const caption = document.querySelector('.caption');
  const words = document.querySelector('.caption .words');
  if (caption.scrollHeight > caption.clientHeight + 2 || caption.scrollWidth > caption.clientWidth + 2) problems.push('caption layer: overflow (the bar holds two lines of fifteen full-width characters)');
  const bar = caption.getBoundingClientRect();
  if (bar.bottom > 1600) problems.push('caption layer outside safe area');
  const text = words.getBoundingClientRect();
  if (text.left < 78 || text.right > 902) problems.push('caption words outside the safe sides');
  return problems;
}

/**
 * Draw the caption layer: the blank picture, and for each phrase one transparent picture a state,
 * clipped to the bar, the group being spoken lit, after the page was measured. Returns the
 * layout report, one entry a phrase; a phrase the bar cannot hold ends the build, naming it.
 */
async function renderCaptionLayer({ doc, phrases, directory, channel, fontCss, blank, fileOf }) {
  const { chromium } = await import('@playwright/test');
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  const layout = [];
  try {
    const context = await browser.newContext({ viewport: { width: PROFILE.width, height: PROFILE.height }, deviceScaleFactor: 1, javaScriptEnabled: false });
    await context.route('**/*', (route) => route.abort());
    const page = await context.newPage();
    page.setDefaultTimeout(20000);
    const ready = async (label) => {
      let timer;
      try {
        await Promise.race([
          page.evaluate(() => document.fonts.ready.then(() => true)),
          new Promise((_resolve, reject) => { timer = setTimeout(() => reject(new Error(`${label}: fonts timed out`)), 20000); }),
        ]);
      } finally { clearTimeout(timer); }
    };
    await page.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:transparent"></body></html>');
    await page.screenshot({ path: blank, clip: { ...CAPTION_BOX }, omitBackground: true });
    for (const phrase of phrases) {
      if (stopRequested(directory)) throw new Error('STOP requested');
      await page.setContent(dramaCaptionHtml(doc, { fontCss, lines: phrase.lines, groups: phrase.groups, active: phrase.states[0]?.group ?? -1 }));
      await ready(`caption ${phrase.cue}`);
      const problems = await page.evaluate(measureLayer);
      layout.push({ cue: phrase.cue, problems });
      if (problems.length) throw new Error(`caption ${phrase.cue + 1} 「${phrase.text}」: ${problems.join('; ')}; pick a span without it, or shorten that line in the episode`);
      for (const [state, { group }] of phrase.states.entries()) {
        await page.evaluate((active) => {
          document.querySelectorAll('.caption .g').forEach((element, index) => element.classList.toggle('on', index === active));
        }, group);
        await page.screenshot({ path: fileOf(phrase.cue, state), clip: { ...CAPTION_BOX }, omitBackground: true });
      }
    }
  } finally { await browser.close(); }
  return layout;
}

/**
 * Where the subject is in every shot of the span: one picture a shot in the media store (the
 * keyframe this work directory has, else the frame in the middle of the shot pulled out of the
 * cut), one locate call a shot, the shot's characters as the labels. A card scene asks nothing
 * and keeps the centre. Returns the shots with their windows and what the calls answered.
 */
async function locateShots({ shots, episode, media, maxLabels, ffmpeg, directory, stop }) {
  const located = [];
  let calls = 0;
  let model = null;
  for (const shot of shots) {
    if (stop()) throw new Error('STOP requested');
    if (shot.template !== 'shot') {
      located.push({ shot: shot.id, template: shot.template, start: shot.start, end: shot.end, picture: 'card', subject: null, x: CENTRE_X });
      continue;
    }
    const keyframe = episode.keyframes?.shots?.[shot.id]?.file;
    let file;
    let picture;
    if (typeof keyframe === 'string' && existsSync(path.join(episode.workdir, keyframe))) {
      file = path.join(episode.workdir, keyframe);
      picture = 'keyframe';
    } else {
      file = path.join(directory, 'build', `frame-${shot.id}.png`);
      await runTool(ffmpeg, frameArgs(episode.final, shot.picture_frame, file));
      picture = 'frame';
    }
    const labels = shotLabels(episode.video, shot.id).slice(0, maxLabels);
    const { sha256: digest } = await putFile({ slug: episode.slug, file, ...media });
    const answer = await locate({ request: { slug: episode.slug, sha256: digest, ...(labels.length ? { labels } : {}) }, ...media });
    calls += 1;
    model = answer.model ?? model;
    const subject = pickSubject(answer.boxes, labels);
    const x = subject ? windowFor(subject.box, { width: answer.width || SOURCE.width, height: answer.height || SOURCE.height }) : CENTRE_X;
    located.push({ shot: shot.id, template: 'shot', start: shot.start, end: shot.end, picture, ...(picture === 'frame' ? { frame: shot.picture_frame } : {}), sha256: digest, labels, boxes: Array.isArray(answer.boxes) ? answer.boxes.length : 0, subject, x });
  }
  return { located, calls, model };
}

/**
 * Cut a vertical Short from an approved drama episode. `client` is the site (shorts/site.mjs):
 * the Shorts settings give the length a Short may have, and its token asks the media server
 * where the subjects are. `episodeWorkdir` is the work base the episode's directory sits in (the
 * same --workdir `tts` and `assemble` took); `workdir` is where the Short's builds go.
 */
export async function fromDrama({ slug, from, to, workdir, episodeWorkdir, meta = null, captions, channel = process.platform === 'win32' ? 'msedge' : undefined, client, root = ROOT, env = process.env, home, locateFfmpegImpl = locateFfmpeg, now = () => new Date() }) {
  if (!slug) throw new Error('--slug required: the drama episode');
  if (!client) throw new Error('the site is needed: locate answers where the subject is');
  const episode = readEpisode({ slug, workdir: resolveWorkdir({ flag: episodeWorkdir, env, slug, root, home }), root });
  const approval = await approvalState({ gate: 'final', docDir: episode.docDir, workdir: episode.workdir });
  if (approval.status !== 'approved') {
    const why = approval.status === 'stale' ? 'is not the cut that was approved' : 'is not approved';
    throw new Error(`the final cut of ${slug} ${why} (${episode.final}): run review-pull, or approve --gate final, before cutting a Short from it`);
  }
  const captionStyle = captionsOption(captions, env);
  const base = resolveWorkBase({ flag: workdir, env, root, home });
  const settings = await client.settings();
  const range = { minSeconds: settings?.seconds_min ?? PROFILE.minSeconds, maxSeconds: settings?.seconds_max ?? PROFILE.maxSeconds };
  const span = spanFrames(from, to, episode.timeline.total_frames, range);
  const cues = spanCues(episode.cues, span.startFrame, span.endFrame);
  const shots = shotSpans(episode.timeline, span.startFrame, span.endFrame);
  const doc = shortScript({ slug, video: episode.video, meta, cues, startFrame: span.startFrame, endFrame: span.endFrame });
  const errors = validate(doc);
  if (errors.length) throw new Error(`the Short's script is not valid:\n${errors.join('\n')}`);
  const timeline = { fps: PROFILE.fps, frames: span.frames, seconds: span.frames / PROFILE.fps, cues: timelineFromCaptions(cues, doc.scenes) };
  // Before anything is asked of the site: a STOP file, or a machine that has no ffmpeg to cut
  // with, ends the build with nothing spent; the site must have locate at all.
  if (stopRequested(path.join(base, doc.slug))) throw new Error('STOP requested');
  const { ffmpeg, ffprobe, version } = await locateFfmpegImpl();
  const media = { site: client.site, token: client.token, fetchImpl: client.fetch, sleep: client.sleep };
  const status = await mediaStatus(media);
  const maxLabels = Number(status?.limits?.locate_labels);
  if (!(maxLabels > 0)) throw new Error('the site has no locate yet (GET /video/media/status lists no limits.locate_labels): update the site before reframing a drama');

  const documentBytes = Buffer.from(`${JSON.stringify(doc, null, 2)}\n`);
  const codeHash = sha256(['from-drama.mjs', 'build.mjs', 'core.mjs', 'karaoke.mjs', 'layouts.mjs', 'motion.mjs'].map((file) => readFileSync(new URL(file, import.meta.url), 'utf8')).join('\n') + REFRAME_VERSION);
  const buildId = sha256(JSON.stringify({ document: sha256(documentBytes), source: approval.sha256, span: [span.startFrame, span.endFrame], codeHash, captions: captionStyle, channel: channel ?? null })).slice(0, 16);
  // Every attempt is its own directory, as build.mjs makes them: a failed rerun never leaves an
  // old manifest beside new bytes.
  const directory = path.join(base, doc.slug, `${buildId}-${now().getTime()}`);
  const stop = () => stopRequested(directory) || stopRequested(path.join(base, doc.slug));
  for (const sub of ['audio', 'captions', 'upload', 'evidence', 'build']) mkdirSync(path.join(directory, sub), { recursive: true });
  writeFileSync(path.join(directory, SCRIPT_FILE), documentBytes);

  console.error(`${doc.slug}: locate the subject of ${shots.filter((shot) => shot.template === 'shot').length} shots (${span.frames} frames of ${slug} from ${secondsOf(span.startFrame)} s)`);
  const { located, calls, model } = await locateShots({ shots, episode, media, maxLabels, ffmpeg, directory, stop });
  const pieces = cropPieces(located.map((shot) => ({ start: shot.start, end: shot.end, x: shot.x })));
  const expr = cropExpr(pieces);

  // The sound first: the phrases' clips come from it, and the karaoke timing from those.
  console.error(`${doc.slug}: cut and normalize the sound`);
  const audioFile = path.join(directory, 'build', 'audio.m4a');
  const measuredMix = loudnessResult((await runTool(ffmpeg, cutAudioArgs(episode.final, span.startFrame / PROFILE.fps, timeline.seconds, audioFile))).stderr);
  await runTool(ffmpeg, cutAudioArgs(episode.final, span.startFrame / PROFILE.fps, timeline.seconds, audioFile, measuredMix));
  const wavs = [];
  for (const cue of timeline.cues) {
    if (stop()) throw new Error('STOP requested');
    // Each phrase as the listener's check takes it: 48 kHz, mono, cut at its caption's times.
    const clip = path.join(directory, 'audio', `${number(cue.index)}.wav`);
    await runTool(ffmpeg, ['-y', '-v', 'error', '-ss', (cue.startFrame / PROFILE.fps).toFixed(3), '-t', (cue.frames / PROFILE.fps).toFixed(3), '-i', audioFile, '-vn', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', clip]);
    const wav = parseWav(readFileSync(clip));
    requireNarrationFormat(wav);
    wavs.push(wav);
  }
  const timing = captionStyle === 'karaoke' ? timingFile(timeline, wavs) : null;
  // Plain captions are the same layer with nothing lit: one state a phrase, the words in the
  // theme's text colour; karaoke lights the group being spoken (karaoke.mjs, estimated timing).
  const phrases = timeline.cues.map((cue) => timing?.phrases.find((phrase) => phrase.cue === cue.index) ?? { cue: cue.index, text: cue.text, lines: captionLines(cue.text), groups: phraseGroups(cue.text), states: [{ group: -1, frames: cue.frames }] });

  console.error(`${doc.slug}: draw ${phrases.reduce((sum, phrase) => sum + phrase.states.length, 0)} caption states (${captionStyle})`);
  const fontCss = embeddedFont(timeline.cues.map((cue) => cue.text).join('') + '0123456789');
  const blank = path.join(directory, 'captions', 'blank.png');
  const fileOf = (cue, state) => path.join(directory, 'captions', `${number(cue)}-${String(state).padStart(2, '0')}.png`);
  const layout = await renderCaptionLayer({ doc, phrases, directory, channel, fontCss, blank, fileOf });
  const captionsList = path.join(directory, 'build', 'captions.txt');
  writeFileSync(captionsList, cardsList(captionLayerEntries(timeline, phrases, blank, fileOf)));

  console.error(`${doc.slug}: reframe ${span.frames} frames (${located.length} scenes, ${pieces.filter((piece) => piece.x0 !== piece.x1).length} moves)`);
  if (stop()) throw new Error('STOP requested');
  const video = path.join(directory, 'build', 'video.mp4');
  await runTool(ffmpeg, reframeArgs({ final: episode.final, startFrame: span.startFrame, endFrame: span.endFrame, expr, captionsList, outFile: video }));
  const final = path.join(directory, 'upload', 'final.mp4');
  await runTool(ffmpeg, muxArgs(video, audioFile, final));
  const measured = await measureFinal(final, { ffmpeg, ffprobe });
  const wrong = profileProblems(measured, timeline.frames);
  if (wrong.length) throw new Error(`the reframed cut failed the profile checks: ${wrong.join('; ')}`);
  const loudWrong = loudnessProblems(measured.loudness);
  if (loudWrong.length) throw new Error(`the reframed cut's loudness failed: ${loudWrong.join('; ')}`);
  await runTool(ffmpeg, firstFrameArgs(final, path.join(directory, 'upload', 'cover.png')));

  writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), srt(timeline));
  saveJson(path.join(directory, 'upload', 'titles.json'), doc.titles);
  saveJson(path.join(directory, 'timeline.json'), timeline);
  if (timing) saveJson(path.join(directory, 'timing.json'), timing);
  const { video: stream, audio } = measured;
  saveJson(path.join(directory, 'checks.json'), {
    ok: true,
    profile: PROFILE,
    range,
    seconds: timeline.seconds,
    frames: timeline.frames,
    layout,
    // The windows the picture was cut with, one a scene, and the pieces the crop followed: what
    // the Shorts tab can draw over the preview, and what a reviewer compares the cut with.
    reframe: {
      version: REFRAME_VERSION,
      source: { slug, final_sha256: approval.sha256, start_frame: span.startFrame, end_frame: span.endFrame, width: SOURCE.width, height: SOURCE.height },
      window: WINDOW,
      move_frames: MOVE_FRAMES,
      shots: located,
      pieces,
      locate: { calls, model },
    },
    captions: captionsSummary(timing),
    loudness: measured.loudness,
    video: { codec: stream.codec_name, width: stream.width, height: stream.height, fps: stream.r_frame_rate },
    audio: { codec: audio.codec_name, sample_rate: audio.sample_rate },
    audio_sha256: sha256(wavs.map((_wav, index) => sha256(readFileSync(path.join(directory, 'audio', `${number(index)}.wav`)))).join('')),
    final_sha256: sha256(readFileSync(final)),
    checked_at: now().toISOString(),
  });
  // Nothing was synthesized: the voice is the episode's, paid for with the episode. The locate
  // calls are booked by the site itself on the judge meter (video_media/locate.py), so they are
  // not reported under `stages`, where a call on a billed provider would be entered as an
  // unknown amount (video_shorts/costs.py); checks.json carries their count.
  saveJson(path.join(directory, USAGE_FILE), { narration: { seconds: 0, characters: 0, calls: 0, provider: 'episode' }, stages: {}, checks: {} });
  const uploadFiles = ['final.mp4', 'zh-TW.srt', 'cover.png', 'titles.json'];
  const manifest = {
    schema_version: 2,
    slug: doc.slug,
    line: 'drama',
    series: doc.series,
    build_id: buildId,
    status: 'built',
    created_at: now().toISOString(),
    document_sha256: sha256(documentBytes),
    code_sha256: codeHash,
    reframe: REFRAME_VERSION,
    ffmpeg: version,
    narrator: { source: 'episode', provider: 'episode', voice: null },
    source: { slug, final_sha256: approval.sha256, start_seconds: secondsOf(span.startFrame), end_seconds: secondsOf(span.endFrame) },
    evidence: [],
    files: uploadFiles.map((name) => ({ name, sha256: sha256(readFileSync(path.join(directory, 'upload', name))) })),
  };
  saveJson(path.join(directory, 'upload', 'manifest.json'), manifest);
  return { directory, final, seconds: timeline.seconds, buildId, status: manifest.status, phrases: timeline.cues.length, shots: located.length, locate: { calls, model } };
}
