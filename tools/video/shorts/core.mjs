import { createHash } from 'node:crypto';
import { readFileSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { isInside } from '../core/paths.mjs';
import { themeOf } from './layouts.mjs';

export const PROFILE = Object.freeze({ width: 1080, height: 1920, fps: 30, minSeconds: 25, maxSeconds: 55 });
// The three content lines of the Shorts tab (docs/videos/SHORTS.md): an experiment, a highlight cut
// from a tutorial, a vertical short of a drama. The card pipeline here makes the first two; a
// drama short is made by the drama pipeline and only passes through `import`.
export const LINES = Object.freeze(['lab', 'cut', 'drama']);
export const LAB_SERIES = Object.freeze(['daily', 'blind', 'prompts']);
export const SLUG = /^[a-z][a-z0-9-]{2,79}$/;
// The slug of any video on the site (apps/api/app/video_reviews/storage.py), which a source is.
export const VIDEO_SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
export const YOUTUBE_URL = /^https:\/\/(?:(?:www\.)?youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)[A-Za-z0-9_-]{11}(?:[?&#][^\s<>]*)?$/;
const SERIES = /^[a-z0-9][a-z0-9-]{0,39}$/;
const HASHTAG = /^#?[\p{L}\p{N}_]{1,30}$/u;
export const MAX_HASHTAGS = 3;
export const MAX_LINKS = 5;
export const MAX_TAGS = 15;
// What a build directory holds besides the cut: the script it was made from, as filmed, and
// what making it used.
export const SCRIPT_FILE = 'script.json';
export const USAGE_FILE = 'usage.json';
export const sha256 = (value) => createHash('sha256').update(value).digest('hex');
export const esc = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text = (value) => typeof value === 'string' && value.trim().length > 0;

// A build directory has one writer, so a report is written in place: a rename over a file
// written a moment ago is refused now and then on Windows, while a scanner holds it.
export const saveJson = (file, data) => writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);

/** The content line of a script: version 1 knew only experiments. */
export const lineOf = (doc) => (doc?.schema_version === 1 ? 'lab' : doc?.line);
export const phrasesOf = (doc) => doc.scenes.flatMap((scene) => scene.narration);

function sceneErrors(doc, errors) {
  if (!Array.isArray(doc?.scenes) || doc.scenes.length < 3 || doc.scenes.length > 12) errors.push('3–12 scenes required');
  for (const [i, scene] of (doc?.scenes ?? []).entries()) {
    if (typeof scene.headline !== 'string' || !scene.headline.trim() || scene.headline.length > 36) errors.push(`scene ${i}: headline 1–36 characters`);
    if (!Array.isArray(scene.narration) || !scene.narration.length || scene.narration.some(t => typeof t !== 'string' || !t.trim() || [...t].length > 38)) errors.push(`scene ${i}: narration phrases 1–38 characters`);
    if (scene.body && (!Array.isArray(scene.body) || scene.body.length > 5 || scene.body.some(t => typeof t !== 'string' || t.length > 85))) errors.push(`scene ${i}: up to five body rows of 85 characters`);
    if (scene.asset && !doc.evidence?.some(e => e.path === scene.asset)) errors.push(`scene ${i}: asset must be evidence-bound`);
  }
}

function evidenceErrors(doc, errors) {
  for (const item of doc?.evidence ?? []) if (!item.path || !/^[a-f0-9]{64}$/.test(item.sha256 ?? '')) errors.push('evidence requires path and sha256');
}

// Version 1 is what the three pilots were written in (docs/videos/ai-shorts/pilots): they stay
// valid as they are, byte for byte, so this branch never changes.
function validateV1(doc) {
  const errors = [];
  if (!SLUG.test(doc?.slug ?? '')) errors.push('invalid slug');
  if (doc?.format !== 'shorts') errors.push('format must be shorts');
  if (doc?.locale !== 'zh-TW') errors.push('locale must be zh-TW');
  if (!LAB_SERIES.includes(doc?.series)) errors.push('invalid series');
  if (!Array.isArray(doc?.titles) || doc.titles.length !== 2 || doc.titles.some(t => typeof t !== 'string' || !t.trim() || t.length > 100)) errors.push('two titles of 1–100 characters required');
  for (const field of ['description', 'experiment_summary', 'limitations']) if (!text(doc?.[field])) errors.push(`${field} required`);
  if (!Array.isArray(doc?.evidence) || !doc.evidence.length) errors.push('evidence required');
  evidenceErrors(doc, errors);
  sceneErrors(doc, errors);
  return errors;
}

function validateV2(doc) {
  const errors = [];
  if (!SLUG.test(doc?.slug ?? '')) errors.push('invalid slug');
  if (doc?.format !== 'shorts') errors.push('format must be shorts');
  if (doc?.locale !== 'zh-TW') errors.push('locale must be zh-TW');
  if (!LINES.includes(doc?.line)) errors.push(`line must be one of ${LINES.join(', ')}`);
  if (doc?.line === 'lab' ? !LAB_SERIES.includes(doc?.series) : !SERIES.test(doc?.series ?? '')) errors.push(doc?.line === 'lab' ? 'invalid series' : 'series must be the slug of the source');
  if (!Array.isArray(doc?.titles) || doc.titles.length !== 2 || doc.titles.some(t => typeof t !== 'string' || !t.trim() || t.length > 100 || /[<>]/.test(t))) errors.push('two titles of 1–100 characters without angle brackets required');
  if (!text(doc?.description)) errors.push('description required');
  if (doc?.line === 'lab') {
    // An experiment says what was tested and what the test cannot tell, and shows its evidence.
    for (const field of ['experiment_summary', 'limitations']) if (!text(doc?.[field])) errors.push(`${field} required`);
    if (!Array.isArray(doc?.evidence) || !doc.evidence.length) errors.push('evidence required');
  } else {
    // A highlight or a vertical short leads back to the video it was cut from. Its address may
    // be left out: `package` reads it from the site, which knows the video once it is public.
    const source = doc?.source;
    if (!VIDEO_SLUG.test(source?.slug ?? '')) errors.push('source.slug required');
    if (source?.url !== undefined && !YOUTUBE_URL.test(source.url)) errors.push('source.url must be the YouTube address of the full video');
    for (const field of ['start_seconds', 'end_seconds']) if (source?.[field] !== undefined && !(Number.isFinite(source[field]) && source[field] >= 0)) errors.push(`source.${field} must be a number of seconds`);
    if (Number.isFinite(source?.start_seconds) && Number.isFinite(source?.end_seconds) && source.end_seconds <= source.start_seconds) errors.push('source.end_seconds must come after start_seconds');
  }
  if (doc?.evidence !== undefined && !Array.isArray(doc.evidence)) errors.push('evidence must be a list');
  evidenceErrors(doc, errors);
  if (doc?.hashtags !== undefined && (!Array.isArray(doc.hashtags) || doc.hashtags.length > MAX_HASHTAGS || doc.hashtags.some(t => typeof t !== 'string' || !HASHTAG.test(t)))) errors.push(`up to ${MAX_HASHTAGS} hashtags of letters and digits`);
  if (doc?.links !== undefined && (!Array.isArray(doc.links) || doc.links.length > MAX_LINKS || doc.links.some(l => !text(l?.label) || !/^https:\/\/[^\s<>]+$/.test(l?.url ?? '')))) errors.push(`up to ${MAX_LINKS} links, each { label, url } with an https address`);
  if (doc?.tags !== undefined && (!Array.isArray(doc.tags) || doc.tags.length > MAX_TAGS || doc.tags.some(t => typeof t !== 'string' || !t.trim() || [...t].length > 30 || /[<>,]/.test(t)))) errors.push(`up to ${MAX_TAGS} tags of 1–30 characters`);
  if (doc?.synthetic_media !== undefined && typeof doc.synthetic_media !== 'boolean') errors.push('synthetic_media must be true or false');
  sceneErrors(doc, errors);
  return errors;
}

export function validate(doc) {
  if (doc?.schema_version === 1) return validateV1(doc);
  if (doc?.schema_version === 2) return validateV2(doc);
  return ['schema_version must be 1 or 2'];
}

// Resolve real paths too: a symlink must not allow an artifact to read outside its source tree.
export function sourcePath(base, relative) {
  if (typeof relative !== 'string' || path.isAbsolute(relative)) throw new Error('source path must be relative');
  const file = realpathSync(path.resolve(base, relative));
  if (!isInside(file, realpathSync(base))) throw new Error(`source outside campaign: ${relative}`);
  return file;
}

export function verifyEvidence(doc, sourceBase) {
  return (doc.evidence ?? []).map(item => {
    const file = sourcePath(sourceBase, item.path);
    const bytes = readFileSync(file);
    if (sha256(bytes) !== item.sha256) throw new Error(`evidence changed: ${item.path}`);
    return { ...item, file, bytes };
  });
}

/** The cues of a run of phrases: `range` is the length a Short may have, the owner's setting. */
export function buildTimeline(doc, durations, range = PROFILE) {
  const phrases = doc.scenes.flatMap((scene, sceneIndex) => scene.narration.map(text => ({ text, sceneIndex })));
  if (durations.length !== phrases.length || durations.some(d => !Number.isFinite(d) || d <= 0)) throw new Error('positive measured audio duration required for every phrase');
  let frame = 0;
  const cues = phrases.map((phrase, i) => {
    const frames = Math.ceil((durations[i] + 0.18) * PROFILE.fps);
    const cue = { ...phrase, index: i, startFrame: frame, endFrame: frame + frames, frames, audioSeconds: durations[i] };
    frame += frames;
    return cue;
  });
  const seconds = frame / PROFILE.fps;
  if (seconds < range.minSeconds || seconds > range.maxSeconds) throw new Error(`narration is ${seconds.toFixed(2)}s; edit script to fit ${range.minSeconds}–${range.maxSeconds}s (never truncate speech)`);
  return { fps: PROFILE.fps, frames: frame, seconds, cues };
}

const stamp = (frame) => {
  const ms = Math.round(frame * 1000 / PROFILE.fps);
  return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')},${String(ms%1000).padStart(3,'0')}`;
};
export function srt(timeline) { return timeline.cues.map((c,i) => `${i+1}\n${stamp(c.startFrame)} --> ${stamp(c.endFrame)}\n${c.text}\n`).join('\n'); }

/** The cues of a caption file: [{ start, end, text }] in seconds; throws on a file it cannot read. */
export function parseSrt(source) {
  const seconds = (value) => {
    const match = /^(\d{2}):(\d{2}):(\d{2})[,.](\d{3})$/.exec(value.trim());
    if (!match) throw new Error(`not a caption time: ${value}`);
    return Number(match[1]) * 3600 + Number(match[2]) * 60 + Number(match[3]) + Number(match[4]) / 1000;
  };
  return String(source).replace(/^\uFEFF/, '').replace(/\r/g, '').trim().split(/\n{2,}/).filter(Boolean).map((block, index) => {
    const lines = block.split('\n');
    const timing = lines.findIndex((line) => line.includes('-->'));
    if (timing < 0) throw new Error(`caption ${index + 1} has no time line`);
    const [start, end] = lines[timing].split('-->').map(seconds);
    const words = lines.slice(timing + 1).join('\n').trim();
    if (!words) throw new Error(`caption ${index + 1} is empty`);
    if (!(end > start)) throw new Error(`caption ${index + 1} ends before it starts`);
    return { start, end, text: words };
  });
}

// What never moves between themes: the safe area the build measures (content inside x 78–902 and
// above y 1380, the caption above y 1600), so every layout clears the Shorts interface.
export function sceneHtml(doc, cue, { fontCss = '', assetUrl = '' } = {}) {
  const scene = doc.scenes[cue.sceneIndex];
  const theme = themeOf(doc);
  const c = theme.colors;
  const rows = (scene.body ?? []).map((row, index) => theme.rows === 'numbered'
    ? `<div class="row numbered"><span class="n">${index + 1}</span><span>${esc(row)}</span></div>`
    : `<div class="row${theme.rows === 'compare' ? ` side-${index % 2 ? 'b' : 'a'}` : ''}">${esc(row)}</div>`).join('');
  return `<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><style>${fontCss}
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:${c.background};color:${c.text};font-family:'Noto Sans TC Variable',sans-serif}
.glow{position:absolute;${theme.glow};border-radius:50%;background:radial-gradient(circle,${c.glow},transparent 70%)}
.brand{position:absolute;top:90px;left:80px;font-size:27px;letter-spacing:4px;color:${c.muted}}.series{position:absolute;left:80px;top:174px;font-size:29px;letter-spacing:2px;color:${c.accent}}
.content{position:absolute;left:80px;top:258px;width:820px;height:1120px;display:flex;flex-direction:column;gap:34px;justify-content:center;padding-bottom:60px}
.content.with-asset{justify-content:flex-start;padding-bottom:0}
h1{font-size:88px;line-height:1.2;letter-spacing:-2px;margin:0;font-weight:850;word-break:normal;overflow-wrap:anywhere;white-space:pre-line}
.line{height:8px;width:${theme.rule};background:${c.highlight};border-radius:8px;flex-shrink:0}.body{display:flex;flex-direction:column;gap:18px}.row{font-size:47px;line-height:1.45;border-left:5px solid ${c.rowBorder};background:${c.row};padding:24px;border-radius:0 18px 18px 0;white-space:pre-wrap}
.row.numbered{display:flex;gap:22px;border-left:0;border-radius:18px}.row .n{color:${c.highlight};font-weight:850;flex-shrink:0}.row.side-b{border-left-color:${c.highlight}}
.big{font-size:168px;line-height:1.12;font-weight:850;color:${c.highlight};letter-spacing:-3px;padding:25px 0}.note{font-size:28px;line-height:1.5;color:${c.muted}}
.asset{max-height:835px;max-width:820px;object-fit:contain;align-self:center;border-radius:18px;border:2px solid ${c.rowBorder}}
.caption{position:absolute;left:80px;top:1430px;width:820px;height:165px;padding:14px 20px;background:${c.caption};border-radius:22px;font-size:49px;line-height:1.36;font-weight:650;display:flex;align-items:center;justify-content:center;text-align:center}
.count{position:absolute;top:1640px;left:80px;font-size:25px;color:${c.muted}}.progress{position:absolute;left:80px;top:1700px;width:820px;height:7px;background:${c.track}}.progress span{display:block;height:100%;background:${c.accent};width:${Math.round((cue.sceneIndex+1)/doc.scenes.length*100)}%}
</style><body data-theme="${esc(theme.id)}"><div class="glow"></div><div class="brand">${esc(theme.brand)}</div><div class="series">${esc(scene.kicker ?? theme.kicker)}</div><main class="content${assetUrl?' with-asset':''}"><h1>${esc(scene.headline)}</h1><div class="line"></div>${scene.big ? `<div class="big">${esc(scene.big)}</div>`:''}${assetUrl ? `<img class="asset" src="${esc(assetUrl)}">`:''}${rows ? `<div class="body">${rows}</div>`:''}${scene.note ? `<div class="note">${esc(scene.note)}</div>`:''}</main><div class="caption">${esc(cue.text)}</div><div class="count">${String(cue.sceneIndex+1).padStart(2,'0')} / ${String(doc.scenes.length).padStart(2,'0')} · ${esc(theme.footer)}</div><div class="progress"><span></span></div></body></html>`;
}
