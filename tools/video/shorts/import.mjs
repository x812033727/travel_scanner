// `import`: a Short made by another tool becomes a build of this one (docs/videos/SHORTS.md
// §工具端), so it goes through the same checks and the same push.
//
// The directory holds final.mp4, zh-TW.srt and meta.json:
//   { slug, line, series, titles: [a, b], description, source?, hashtags?, tags?, links?,
//     experiment_summary?, limitations?, synthetic_media?, headlines?: [...] }
// The captions are taken for the narration, phrase by phrase, and the audio is cut at their times
// so the listener's check can hear each phrase. Nothing the other tool measured is taken over:
// the cut is measured again, and what cannot be measured from a finished file (where the cards
// sit inside the frame) is left for the owner to look at once.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { ROOT, resolveWorkBase } from '../core/paths.mjs';
import { measureFinal } from './build.mjs';
import { PROFILE, SCRIPT_FILE, USAGE_FILE, parseSrt, sha256, srt, validate } from './core.mjs';

const saveJson = (file, data) => writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
const number = (i) => String(i).padStart(3, '0');
// How many phrases a card of an imported cut holds when its maker named no headlines.
const PHRASES_PER_SCENE = 3;

/** The timeline of a finished cut, from its captions: one cue per caption, on the frame grid. */
export function timelineFromCaptions(cues, scenes) {
  let phrase = 0;
  const built = [];
  for (const [sceneIndex, scene] of scenes.entries()) {
    for (const text of scene.narration) {
      const cue = cues[phrase];
      const startFrame = Math.round(cue.start * PROFILE.fps);
      const endFrame = Math.round(cue.end * PROFILE.fps);
      built.push({ text, sceneIndex, index: phrase, startFrame, endFrame, frames: endFrame - startFrame, audioSeconds: cue.end - cue.start });
      phrase += 1;
    }
  }
  return built;
}

/**
 * The script of a finished cut: meta.json's fields, and its captions as the narration. The
 * cards' headlines are the maker's when meta.json lists them, one for each run of phrases.
 */
export function scriptFromImport(meta, cues) {
  const headlines = Array.isArray(meta.headlines) && meta.headlines.length ? meta.headlines : null;
  const count = headlines ? headlines.length : Math.max(3, Math.min(12, Math.ceil(cues.length / PHRASES_PER_SCENE)));
  const size = Math.ceil(cues.length / count);
  const scenes = Array.from({ length: count }, (_unused, index) => ({
    headline: headlines ? headlines[index] : [...cues[Math.min(index * size, cues.length - 1)].text].slice(0, 36).join(''),
    narration: cues.slice(index * size, (index + 1) * size).map((cue) => cue.text),
  })).filter((scene) => scene.narration.length);
  const { headlines: _headlines, ...fields } = meta;
  return { schema_version: 2, format: 'shorts', locale: 'zh-TW', ...fields, scenes };
}

/** Why a finished cut's captions cannot be its timeline; empty when they can. */
export function captionTimingProblems(cues, seconds) {
  const problems = [];
  for (const [index, cue] of cues.entries()) {
    if (index && cue.start < cues[index - 1].end - 0.001) problems.push(`caption ${index + 1} starts before caption ${index} ends`);
  }
  if (cues.length && cues.at(-1).end > seconds + 0.05) problems.push(`the captions run to ${cues.at(-1).end.toFixed(2)}s, the cut to ${seconds.toFixed(2)}s`);
  return problems;
}

/**
 * Why a finished cut's picture is not on the Shorts frame grid; empty when it is. Checked before
 * the captions, because a cut at another rate reads as the wrong length on this grid and would be
 * blamed on its captions.
 */
export function frameRateProblem(video) {
  const rate = String(video?.r_frame_rate ?? '');
  if (rate === `${PROFILE.fps}/1`) return '';
  const [numerator, denominator] = rate.split('/').map(Number);
  const fps = denominator ? numerator / denominator : NaN;
  const named = Number.isFinite(fps) ? `${Number(fps.toFixed(3))} fps (${rate})` : `an unreadable frame rate (${rate || 'none'})`;
  return `the cut runs at ${named}, not the Shorts profile's ${PROFILE.fps} fps: re-encode it to ${PROFILE.fps} fps (ffmpeg -vf fps=${PROFILE.fps}) and import it again`;
}

export async function importShort({ from, workdir, tools = null, measureImpl = measureFinal, now = () => new Date() }) {
  for (const name of ['final.mp4', 'zh-TW.srt', 'meta.json']) if (!existsSync(path.join(from, name))) throw new Error(`${from} has no ${name}`);
  const meta = JSON.parse(readFileSync(path.join(from, 'meta.json'), 'utf8'));
  const cues = parseSrt(readFileSync(path.join(from, 'zh-TW.srt'), 'utf8'));
  const doc = scriptFromImport(meta, cues);
  const errors = validate(doc);
  if (errors.length) throw new Error(`meta.json and the captions do not make a script:\n${errors.join('\n')}`);
  // An imported experiment would need its evidence too; that is a build, not an import.
  if (doc.evidence?.length) throw new Error('an imported cut carries no evidence files: build an experiment from its script instead');
  const { ffmpeg, ffprobe } = tools ?? (await locateFfmpeg());
  const finalBytes = readFileSync(path.join(from, 'final.mp4'));
  const base = resolveWorkBase({ flag: workdir, root: ROOT });
  const directory = path.join(base, doc.slug, `import-${sha256(finalBytes).slice(0, 16)}-${now().getTime()}`);
  for (const sub of ['audio', 'upload', 'evidence']) mkdirSync(path.join(directory, sub), { recursive: true });
  const final = path.join(directory, 'upload', 'final.mp4');
  copyFileSync(path.join(from, 'final.mp4'), final);
  const measured = await measureImpl(final, { ffmpeg, ffprobe });
  const rateProblem = frameRateProblem(measured.video);
  if (rateProblem) throw new Error(rateProblem);
  const frames = Number(measured.video?.nb_frames);
  // The cut's own length, as its video stream reports it; the frame count on the grid only when
  // the stream carries no duration.
  const streamSeconds = Number(measured.video?.duration);
  const seconds = Number.isFinite(streamSeconds) && streamSeconds > 0 ? streamSeconds : frames / PROFILE.fps;
  const timing = captionTimingProblems(cues, seconds);
  if (timing.length) throw new Error(timing.join('\n'));
  const timeline = { fps: PROFILE.fps, frames, seconds, cues: timelineFromCaptions(cues, doc.scenes) };
  for (const cue of timeline.cues) {
    // Each phrase as the listener's check takes it: 48 kHz, mono, cut at its caption's times.
    await runTool(ffmpeg, ['-y', '-v', 'error', '-ss', (cue.startFrame / PROFILE.fps).toFixed(3), '-t', (cue.frames / PROFILE.fps).toFixed(3), '-i', final, '-vn', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', path.join(directory, 'audio', `${number(cue.index)}.wav`)]);
  }
  await runTool(ffmpeg, ['-y', '-v', 'error', '-i', final, '-frames:v', '1', path.join(directory, 'upload', 'cover.png')]);
  const scriptBytes = `${JSON.stringify(doc, null, 2)}\n`;
  writeFileSync(path.join(directory, SCRIPT_FILE), scriptBytes);
  // Written from the timeline, on the frame grid: the package's captions are the ones the
  // checks read, whatever clock the other tool wrote its own on.
  writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), srt(timeline));
  saveJson(path.join(directory, 'upload', 'titles.json'), doc.titles);
  saveJson(path.join(directory, 'timeline.json'), timeline);
  saveJson(path.join(directory, 'checks.json'), { ok: false, imported: true, profile: PROFILE, seconds, frames, layout: null, loudness: measured.loudness, final_sha256: sha256(finalBytes), checked_at: now().toISOString() });
  saveJson(path.join(directory, USAGE_FILE), { narration: { seconds: 0, characters: 0, calls: 0, provider: 'files' }, stages: {}, checks: {} });
  saveJson(path.join(directory, 'upload', 'manifest.json'), { schema_version: 2, slug: doc.slug, line: doc.line, series: doc.series, build_id: `import-${sha256(finalBytes).slice(0, 16)}`, status: 'imported', created_at: now().toISOString(), document_sha256: sha256(scriptBytes), narrator: { source: 'imported' }, evidence: [], files: ['final.mp4', 'zh-TW.srt', 'cover.png', 'titles.json'].map((name) => ({ name, sha256: sha256(readFileSync(path.join(directory, 'upload', name))) })) });
  return { directory, final, seconds, status: 'imported', phrases: timeline.cues.length };
}
