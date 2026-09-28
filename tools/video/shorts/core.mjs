import { createHash } from 'node:crypto';
import { readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';
import { isInside } from '../core/paths.mjs';

export const PROFILE = Object.freeze({ width: 1080, height: 1920, fps: 30, minSeconds: 25, maxSeconds: 55 });
export const sha256 = (value) => createHash('sha256').update(value).digest('hex');
// The AI-experiment campaign's three series (docs/videos/ai-shorts/), and the explainer's Shorts cut
// from a long episode (docs/videos/so-thats-why/), which rest on its keyframes instead of evidence.
export const EXPERIMENT_SERIES = ['daily', 'blind', 'prompts'];
export const EPISODE_SERIES = 'sothatswhy';
export const SERIES_BRAND = Object.freeze({
  daily: { brand: 'MOKAAIR / AI 真的可以？', kicker: '實測紀錄', count: '原創實測' },
  blind: { brand: 'MOKAAIR / AI 真的可以？', kicker: '實測紀錄', count: '原創實測' },
  prompts: { brand: 'MOKAAIR / AI 真的可以？', kicker: '實測紀錄', count: '原創實測' },
  [EPISODE_SERIES]: { brand: '原來如此事務所', kicker: '為什麼？', count: '原來如此', more: '完整版在長片 ▶' },
});
const EPISODE_SLUG = /^[a-z0-9][a-z0-9-]{1,79}$/;
export const esc = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function validate(doc) {
  const errors = [];
  if (doc?.schema_version !== 1) errors.push('schema_version must be 1');
  if (!/^[a-z][a-z0-9-]{2,79}$/.test(doc?.slug ?? '')) errors.push('invalid slug');
  if (doc?.format !== 'shorts') errors.push('format must be shorts');
  if (doc?.locale !== 'zh-TW') errors.push('locale must be zh-TW');
  const episode = doc?.series === EPISODE_SERIES;
  if (![...EXPERIMENT_SERIES, EPISODE_SERIES].includes(doc?.series)) errors.push('invalid series');
  if (!Array.isArray(doc?.titles) || doc.titles.length !== 2 || doc.titles.some(t => typeof t !== 'string' || !t.trim() || t.length > 100)) errors.push('two titles of 1–100 characters required');
  // An episode's Short is a cut of a video already checked; its pictures are the episode's
  // keyframes, bound by hash when the Short is built, so it has no experiment to report.
  for (const field of episode ? ['description'] : ['description', 'experiment_summary', 'limitations']) if (typeof doc?.[field] !== 'string' || !doc[field].trim()) errors.push(`${field} required`);
  if (episode && !EPISODE_SLUG.test(doc?.episode ?? '')) errors.push('episode must be the long video\'s slug');
  const evidence = Array.isArray(doc?.evidence) ? doc.evidence : [];
  if (doc?.evidence !== undefined && !Array.isArray(doc.evidence)) errors.push('evidence must be an array');
  if (!episode && !evidence.length) errors.push('evidence required');
  for (const item of evidence) if (!item || typeof item.path !== 'string' || !item.path || !/^[a-f0-9]{64}$/.test(item.sha256 ?? '')) errors.push('evidence requires path and sha256');
  const scenes = Array.isArray(doc?.scenes) ? doc.scenes : [];
  if (scenes.length < 3 || scenes.length > 12) errors.push('3–12 scenes required');
  for (const [i, scene] of scenes.entries()) {
    if (!scene || typeof scene !== 'object' || Array.isArray(scene)) {
      errors.push(`scene ${i}: an object is required`);
      continue;
    }
    if (typeof scene.headline !== 'string' || !scene.headline.trim() || scene.headline.length > 36) errors.push(`scene ${i}: headline 1–36 characters`);
    if (!Array.isArray(scene.narration) || !scene.narration.length || scene.narration.some(t => typeof t !== 'string' || !t.trim() || [...t].length > 38)) errors.push(`scene ${i}: narration phrases 1–38 characters`);
    if (scene.body && (!Array.isArray(scene.body) || scene.body.length > 5 || scene.body.some(t => typeof t !== 'string' || t.length > 85))) errors.push(`scene ${i}: up to five body rows of 85 characters`);
    if (scene.asset && !evidence.some(e => e?.path === scene.asset)) errors.push(`scene ${i}: asset must be evidence-bound`);
    if (scene.shot !== undefined && (!episode || typeof scene.shot !== 'string' || !scene.shot.trim())) errors.push(`scene ${i}: shot names a keyframe of the long episode (series ${EPISODE_SERIES} only)`);
    if (scene.shot !== undefined && scene.asset) errors.push(`scene ${i}: a scene shows a shot or an asset, not both`);
  }
  return errors;
}

/**
 * An episode's Short with its shots resolved: each scene's `shot` becomes the asset of that shot's
 * keyframe (`keyframes/manifest.json` in the episode's work directory), listed as evidence with
 * its hash, so verifyEvidence binds the Short to the very pictures the long video used.
 */
export function episodeShort(doc, keyframes) {
  const shots = keyframes?.shots ?? {};
  const evidence = new Map();
  const scenes = doc.scenes.map((scene, i) => {
    if (scene.shot === undefined) return scene;
    const frame = shots[scene.shot];
    if (!frame?.file || !/^[a-f0-9]{64}$/.test(frame.sha256 ?? '')) throw new Error(`scene ${i}: shot "${scene.shot}" has no keyframe in keyframes/manifest.json`);
    if (frame.needs_review) throw new Error(`scene ${i}: shot "${scene.shot}" still needs a prompt fix (needs_review)`);
    evidence.set(frame.file, { path: frame.file, sha256: frame.sha256 });
    const { shot: _shot, ...rest } = scene;
    return { ...rest, asset: frame.file };
  });
  return { ...doc, scenes, evidence: [...(doc.evidence ?? []), ...evidence.values()] };
}

// Resolve real paths too: a symlink must not allow an artifact to read outside its source tree.
export function sourcePath(base, relative) {
  if (typeof relative !== 'string' || path.isAbsolute(relative)) throw new Error('source path must be relative');
  const file = realpathSync(path.resolve(base, relative));
  if (!isInside(file, realpathSync(base))) throw new Error(`source outside campaign: ${relative}`);
  return file;
}

export function verifyEvidence(doc, sourceBase) {
  return doc.evidence.map(item => {
    const file = sourcePath(sourceBase, item.path);
    const bytes = readFileSync(file);
    if (sha256(bytes) !== item.sha256) throw new Error(`evidence changed: ${item.path}`);
    return { ...item, file, bytes };
  });
}

export function buildTimeline(doc, durations) {
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
  if (seconds < PROFILE.minSeconds || seconds > PROFILE.maxSeconds) throw new Error(`narration is ${seconds.toFixed(2)}s; edit script to fit ${PROFILE.minSeconds}–${PROFILE.maxSeconds}s (never truncate speech)`);
  return { fps: PROFILE.fps, frames: frame, seconds, cues };
}

const stamp = (frame) => {
  const ms = Math.round(frame * 1000 / PROFILE.fps);
  return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')},${String(ms%1000).padStart(3,'0')}`;
};
export function srt(timeline) { return timeline.cues.map((c,i) => `${i+1}\n${stamp(c.startFrame)} --> ${stamp(c.endFrame)}\n${c.text}\n`).join('\n'); }

export function sceneHtml(doc, cue, { fontCss = '', assetUrl = '' } = {}) {
  const scene = doc.scenes[cue.sceneIndex];
  const brand = SERIES_BRAND[doc.series] ?? SERIES_BRAND.daily;
  const last = cue.sceneIndex === doc.scenes.length - 1;
  return `<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><style>${fontCss}
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0b2026;color:#f6f4e8;font-family:'Noto Sans TC Variable',sans-serif}
.glow{position:absolute;left:500px;top:-220px;width:850px;height:850px;border-radius:50%;background:radial-gradient(circle,#1f635960,transparent 70%)}
.brand{position:absolute;top:90px;left:80px;font-size:27px;letter-spacing:4px;color:#8fc8bd}.series{position:absolute;left:80px;top:174px;font-size:29px;letter-spacing:2px;color:#50d2b7}
.content{position:absolute;left:80px;top:258px;width:820px;height:1120px;display:flex;flex-direction:column;gap:34px;justify-content:center;padding-bottom:60px}
.content.with-asset{justify-content:flex-start;padding-bottom:0}
h1{font-size:88px;line-height:1.2;letter-spacing:-2px;margin:0;font-weight:850;word-break:normal;overflow-wrap:anywhere;white-space:pre-line}
.line{height:8px;width:114px;background:#ffb36a;border-radius:8px;flex-shrink:0}.body{display:flex;flex-direction:column;gap:18px}.row{font-size:47px;line-height:1.45;border-left:5px solid #397b73;background:#16353a;padding:24px;border-radius:0 18px 18px 0;white-space:pre-wrap}
.big{font-size:168px;line-height:1.12;font-weight:850;color:#ffb36a;letter-spacing:-3px;padding:25px 0}.note{font-size:28px;line-height:1.5;color:#aad0c6}
.more{font-size:40px;font-weight:750;color:#ffb36a}
.asset{max-height:835px;max-width:820px;object-fit:contain;align-self:center;border-radius:18px;border:2px solid #568c82}
.caption{position:absolute;left:80px;top:1430px;width:820px;height:165px;padding:14px 20px;background:#071a20eb;border-radius:22px;font-size:49px;line-height:1.36;font-weight:650;display:flex;align-items:center;justify-content:center;text-align:center}
.count{position:absolute;top:1640px;left:80px;font-size:25px;color:#84aea7}.progress{position:absolute;left:80px;top:1700px;width:820px;height:7px;background:#244348}.progress span{display:block;height:100%;background:#50d2b7;width:${Math.round((cue.sceneIndex+1)/doc.scenes.length*100)}%}
</style><body><div class="glow"></div><div class="brand">${esc(brand.brand)}</div><div class="series">${esc(scene.kicker ?? brand.kicker)}</div><main class="content${assetUrl?' with-asset':''}"><h1>${esc(scene.headline)}</h1><div class="line"></div>${scene.big ? `<div class="big">${esc(scene.big)}</div>`:''}${assetUrl ? `<img class="asset" src="${esc(assetUrl)}">`:''}${scene.body?.length ? `<div class="body">${scene.body.map(t=>`<div class="row">${esc(t)}</div>`).join('')}</div>`:''}${scene.note ? `<div class="note">${esc(scene.note)}</div>`:''}${last && brand.more ? `<div class="more">${esc(brand.more)}</div>`:''}</main><div class="caption">${esc(cue.text)}</div><div class="count">${String(cue.sceneIndex+1).padStart(2,'0')} / ${String(doc.scenes.length).padStart(2,'0')} · ${esc(brand.count)}</div><div class="progress"><span></span></div></body></html>`;
}
