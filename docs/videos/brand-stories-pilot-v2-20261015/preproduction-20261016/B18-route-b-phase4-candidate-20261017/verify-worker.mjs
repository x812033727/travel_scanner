import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readChapterAnswer, composeStory, cuteStoryVisualProblems } from '../../../../../tools/video/automation/story.mjs';
import { validateVideo } from '../../../../../tools/video/core/schema.mjs';
import { estimateTimeline } from '../../../../../tools/video/core/timeline.mjs';
import { shotProblems } from '../../../../../tools/video/core/drama.mjs';

const dir = dirname(fileURLToPath(import.meta.url));
const root = resolve(dir, '../../../../..');
const base = resolve(dir, '..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const read = (file) => JSON.parse(readFileSync(file, 'utf8'));
const fail = (condition, why) => { if (!condition) throw new Error(why); };
const chapters = Object.fromEntries(keys.map((key) => [key, read(join(dir, 'remapped-chapters', `${key}.json`))]));
const row = read(join(base, 'B18-route-b-row10b-candidate-20261017', 'B18.json'));
const issued = new Map();
for (const chapter of Object.values(chapters)) {
  for (const scene of chapter.scenes) {
    for (const line of scene.lines) issued.set(line.id, createHash('sha256').update(`worker-issued:${line.id}`).digest('hex').slice(0, 8));
  }
}
fail(issued.size === [...issued.values()].length && new Set(issued.values()).size === issued.size, 'simulated line ID collision');
const result = {};
for (const key of keys) {
  const old = chapters[key];
  const answer = {
    title: old.title,
    scenes: old.scenes.map((scene) => ({ ...scene, lines: scene.lines.map((line) => ({ ...line, id: issued.get(line.id) })) })),
    claims: old.claims,
    loops: old.loops.map((loop) => ({ ...loop, setup: issued.get(loop.setup), ...(loop.payoff ? { payoff: issued.get(loop.payoff) } : {}) })),
    ...(old.thumbnail_shot ? { thumbnail_shot: old.thumbnail_shot } : {}),
  };
  const accepted = readChapterAnswer(answer, {
    key,
    ids: answer.scenes.flatMap((scene) => scene.lines.map((line) => line.id)),
    sources: row.sources.length,
    facts: row.must_verify.length,
  });
  fail(!accepted.problem && !accepted.noMore, `worker rejected ${key}: ${accepted.problem ?? accepted.noMore}`);
  result[key] = { ...accepted.chapter, claims: accepted.chapter.claims.map((claim, index) => ({ ...claim, id: old.claims[index].id, verdict: 'UNCHECKED' })) };
}
const info = {
  slug: 'brand-stories', episode: 2, title: row.title,
  logline: row.logline, target_minutes: 10,
  look: { preset: 'cute-mystery' }, characters: [], plan: row,
};
const video = composeStory({ slug: 'story-conveyor-belt-sushi-v2', info, chapters: result, voice: { provider: 'gemini', name: 'Sulafat', style: '溫和、好奇的說書人語氣，台灣國語' }, root });
fail(video.scenes.length === 95 && video.scenes.at(-1).template === 'outro', 'merged scene/outro shape drift');
fail(video.loops?.length === 3, `only ${video.loops?.length ?? 0} cross-chapter loops survive`);
fail(new Set(video.loops.map((loop) => loop.setup)).size === 3, 'loop setup deduped');
fail(cuteStoryVisualProblems(video).length === 0, 'cute-mystery static visual gate failed');
const t18 = result.turn.claims.find((claim) => claim.id === 't18');
fail(t18?.scene === 'turn-s088' && t18.source === 2 && t18.fact === null && t18.verdict === 'UNCHECKED', 't18 source/fact route drifted');
const structural = validateVideo(video);
const estimatedAt300 = estimateTimeline(video, 300);
const shotsAt300 = shotProblems(video, estimatedAt300);
console.log(JSON.stringify({
  status: 'OFFLINE_WORKER_SHAPE_ONLY_HOLD',
  scenes: video.scenes.length,
  shots: video.scenes.filter((scene) => scene.template === 'shot').length,
  outro: video.scenes.at(-1).id,
  loops: video.loops.length,
  visual_problems: cuteStoryVisualProblems(video),
  schema_problems: structural,
  estimated_at_300_cpm_seconds: Number((estimatedAt300.total_frames / 30).toFixed(1)),
  estimated_shot_errors: shotsAt300.errors,
  estimated_shot_warnings: shotsAt300.warnings,
  t18,
}, null, 2));
fail(structural.length === 0, `video schema has ${structural.length} problem(s)`);
fail(shotsAt300.errors.length === 0, `estimated shot lint has ${shotsAt300.errors.length} error(s)`);
