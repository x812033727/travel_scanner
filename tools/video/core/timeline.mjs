// The timeline: when each line is spoken, when each slide state is on screen, where chapters start.
//
// Sync is guaranteed by construction rather than checked afterwards. Audio is 48 kHz and video
// 30 fps, so one frame is exactly 1,600 samples. Every line's clip plus the pause after it is
// padded with silence to a whole number of frames, so every line starts on a frame boundary and
// there is no rounding error anywhere to accumulate over two thousand lines. Only captions,
// which have millisecond precision, subdivide a line.
import { createHash } from "node:crypto";

import { eachLine, spokenText } from "./schema.mjs";

export const FPS = 30;
export const SAMPLE_RATE = 48_000;
export const SAMPLES_PER_FRAME = SAMPLE_RATE / FPS;
// The same speaking-rate estimate video_kit.py uses for the recorded route, so both routes agree.
export const DEFAULT_CPM = 250;
export const DEFAULT_PAUSE_MS = 300;
// Extra silence after a scene's last line, so a slide change never lands mid-breath.
export const SCENE_GAP_MS = 700;
export const TAIL_MS = 1500;
export const MIN_CHAPTERS = 3;
export const CHAPTER_MIN_SECONDS = 10;

const CJK = /[぀-ヿ㐀-鿿豈-﫿가-힯]/u;
const SPOKEN_TOKEN = /[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[぀-ヿ㐀-鿿豈-﫿가-힯]/gu;

/** Characters as they are spoken: a CJK character is one, a Latin word or a run of digits two. */
export function spokenUnits(text) {
  let units = 0;
  for (const token of String(text).match(SPOKEN_TOKEN) ?? []) units += CJK.test(token) ? 1 : 2;
  return units;
}

export const msToSamples = (ms) => Math.round((ms * SAMPLE_RATE) / 1000);
export const samplesToMs = (samples) => (samples * 1000) / SAMPLE_RATE;
export const framesFor = (samples) => Math.ceil(samples / SAMPLES_PER_FRAME);
export const frameToMs = (frame) => (frame * 1000) / FPS;
export const frameToSeconds = (frame) => frame / FPS;

export function estimateSamples(line, cpm = DEFAULT_CPM) {
  return Math.max(SAMPLES_PER_FRAME, Math.round(((spokenUnits(spokenText(line)) * 60) / cpm) * SAMPLE_RATE));
}

/**
 * Lay out every line on the frame grid.
 * `samplesById` maps line id to the length of its synthesized clip in samples (the TTS stage), or
 * pass `estimatedSamples(doc)` before any audio exists.
 */
export function buildTimeline(doc, samplesById) {
  const lines = [];
  const scenes = [];
  const chapters = [];
  let frame = 0;
  let scene = null;
  for (const { scene: source, line, last } of eachLine(doc)) {
    if (scene?.id !== source.id) {
      scene = { id: source.id, template: source.template, start_frame: frame, end_frame: frame, states: [{ reveal: 0, start_frame: frame }] };
      scenes.push(scene);
      if (source.chapter) chapters.push({ title: source.chapter, scene: source.id, start_frame: frame });
    }
    const samples = samplesById[line.id];
    if (!Number.isInteger(samples) || samples <= 0) throw new Error(`no audio length for line ${line.id}`);
    if (line.reveal) {
      const current = scene.states.at(-1);
      const reveal = current.reveal + line.reveal;
      // A reveal on the scene's first line changes the opening state instead of adding a
      // zero-length one.
      if (current.start_frame === frame) current.reveal = reveal;
      else scene.states.push({ reveal, start_frame: frame });
    }
    const isLastLine = last && source === doc.scenes.at(-1);
    const pauseMs = (line.pause_after_ms ?? DEFAULT_PAUSE_MS) + (last ? (isLastLine ? TAIL_MS : SCENE_GAP_MS) : 0);
    const frames = framesFor(samples + msToSamples(pauseMs));
    // A drama line carries its speaker so the review pages and the subtitle prefix know who talks.
    lines.push({ id: line.id, scene: source.id, start_frame: frame, end_frame: frame + frames, audio_samples: samples, ...(line.speaker ? { speaker: line.speaker } : {}) });
    frame += frames;
    scene.end_frame = frame;
  }
  for (const each of scenes) {
    each.states.forEach((state, index) => {
      state.end_frame = index + 1 < each.states.length ? each.states[index + 1].start_frame : each.end_frame;
    });
  }
  return { fps: FPS, sample_rate: SAMPLE_RATE, total_frames: frame, scenes, lines, chapters };
}

export function estimatedSamples(doc, cpm = DEFAULT_CPM) {
  const result = {};
  for (const { line } of eachLine(doc)) result[line.id] = estimateSamples(line, cpm);
  return result;
}

export function estimateTimeline(doc, cpm = DEFAULT_CPM) {
  return buildTimeline(doc, estimatedSamples(doc, cpm));
}

/** mm:ss, or h:mm:ss past an hour: the form YouTube reads as a chapter timestamp. */
export function formatClock(seconds) {
  const total = Math.floor(seconds);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const secs = total % 60;
  const pad = (value) => String(value).padStart(2, "0");
  return hours ? `${hours}:${pad(minutes)}:${pad(secs)}` : `${pad(minutes)}:${pad(secs)}`;
}

/**
 * Chapters with whole-second start times. Seconds are floored, so a chapter marker never lands
 * after the chapter's first word.
 */
export function chapterList(timeline, titles = {}) {
  return timeline.chapters.map((chapter, index) => {
    const next = timeline.chapters[index + 1]?.start_frame ?? timeline.total_frames;
    return {
      title: titles[chapter.scene] ?? chapter.title,
      scene: chapter.scene,
      start: Math.floor(frameToSeconds(chapter.start_frame)),
      seconds: frameToSeconds(next - chapter.start_frame),
    };
  });
}

/** YouTube builds a chapter bar only when these hold (support.google.com/youtube/answer/9884579). */
export function checkChapters(timeline) {
  const problems = [];
  const chapters = chapterList(timeline);
  if (chapters.length < MIN_CHAPTERS) problems.push(`${chapters.length} chapters; YouTube needs at least ${MIN_CHAPTERS}`);
  if (chapters.length && chapters[0].start !== 0) problems.push("the first chapter must start at 00:00");
  for (const chapter of chapters) {
    if (chapter.seconds < CHAPTER_MIN_SECONDS) {
      problems.push(`chapter "${chapter.title}" lasts ${chapter.seconds.toFixed(1)} s; YouTube needs ${CHAPTER_MIN_SECONDS} s`);
    }
  }
  return problems;
}

export function chapterText(timeline, titles = {}) {
  return chapterList(timeline, titles)
    .map((chapter) => `${formatClock(chapter.start)} ${chapter.title}`)
    .join("\n");
}

/**
 * Hash of everything that changes the audio: the voice, the spoken words, the pauses and the
 * dictionary entries those words use. The TTS stage stores it in timeline.json, and status
 * treats a timeline whose hash no longer matches video.json as stale.
 */
export function speechHash(doc, lexicon) {
  const hash = createHash("sha256");
  hash.update(JSON.stringify(doc.voice));
  hash.update(JSON.stringify(lexicon?.terms ?? {}));
  // A drama's audio also depends on who speaks each line and with which voice. Slides keep the
  // original hash, so their timelines stay valid across this change.
  const drama = doc.format === "drama";
  if (drama) hash.update(JSON.stringify((doc.characters ?? []).map((character) => [character.id, character.voice])));
  for (const { scene, line, last } of eachLine(doc)) {
    const fields = [scene.id, line.id, spokenText(line), line.pause_after_ms ?? null, last];
    if (drama) fields.push(line.speaker ?? "narrator", line.emotion ?? null);
    hash.update(JSON.stringify(fields));
  }
  return hash.digest("hex").slice(0, 16);
}

/** Hash of everything that changes the pictures, for the render stage's cache and status. */
export function visualHash(doc) {
  const hash = createHash("sha256");
  hash.update(JSON.stringify(doc.thumbnail ?? null));
  for (const scene of doc.scenes) {
    hash.update(JSON.stringify([scene.id, scene.template, scene.chapter ?? null, scene.data, scene.lines.map((line) => [line.id, line.reveal ?? 0])]));
  }
  return hash.digest("hex").slice(0, 16);
}
