import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { composeStory, cuteStoryVisualProblems, readChapterAnswer } from '../../../../../tools/video/automation/story.mjs';

const dir = dirname(fileURLToPath(import.meta.url));
const base = resolve(dir, '..');
const root = resolve(dir, '../../../../..');
const read = (path) => JSON.parse(readFileSync(path, 'utf8'));
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const chapters = Object.fromEntries(keys.map((key) => [key, read(join(dir, 'remapped-chapters', `${key}.json`))]));
const info = read(join(base, 'B18-attribution-flow-candidate-20261017', 'series-adoption.json'));
info.plan = read(join(base, 'B18-route-b-row10b-candidate-20261017', 'B18.json'));
const doc = composeStory({
  slug: 'story-conveyor-belt-sushi-v2', info, chapters,
  voice: info.characters[0].voice, root,
});
const visual = cuteStoryVisualProblems(doc);
const ids = chapters.origin.scenes.flatMap((scene) => scene.lines.map((line) => line.id));
const origin = readChapterAnswer(chapters.origin, {
  key: 'origin', ids, cast: info.characters,
  sources: info.plan.sources.length, facts: info.plan.must_verify.length,
});
if (visual.length) throw new Error(`cute-mystery visual gate failed: ${JSON.stringify(visual)}`);
if (!origin.problem?.includes('"title"')) throw new Error(`expected title-card worker rejection: ${JSON.stringify(origin)}`);
const result = {
  offline_visual_gate: 'PASS_73_OF_92_ILLUSTRATIONS_NO_CARD_RUN_OVER_3',
  writer_gate: 'HOLD',
  worker_origin_problem: origin.problem,
  worker_contract: 'readChapterAnswer accepts shot, plus last-chapter terminal outro; this draft has 19 title cards',
  worker_line_ids: 'offline deterministic IDs are not the issued writer IDs',
  final_scene: `${chapters.now.scenes.at(-1).id}/${chapters.now.scenes.at(-1).template}`,
  produced_media: false,
};
console.log(JSON.stringify(result, null, 2));
