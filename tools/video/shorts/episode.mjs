// A long video's two Shorts, drafted with its script: an explainer episode's
// (docs/videos/so-thats-why/README.md §Shorts) or an illustrated slides video's
// (docs/videos/ILLUSTRATED.md). The scripts sit in docs/videos/<slug>/shorts.json, cuts of the
// video (schema 2, line "cut", docs/videos/SHORTS.md) whose pictures are the video's keyframes in
// its work directory, moving as they did in the long video.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { EXPLAINER_PRESET, hasPictures } from '../core/drama.mjs';
import { docDir, lexiconFile, readJson, resolveWorkdir, ROOT } from '../core/paths.mjs';
import { episodeShort, validate } from './core.mjs';

export const SHORTS_PER_EPISODE = 2;
// The series a long video's Shorts carry, which picks their theme (layouts.mjs): an explainer's
// and an illustrated slides video's.
export const EPISODE_SERIES = 'sothatswhy';
export const ILLUSTRATED_SERIES = 'illustrated';

/** The series of a long video's Shorts: an explainer's, else the illustrated slides'. */
export const episodeSeries = (video) => (video?.format === 'drama' && video?.look?.preset === EXPLAINER_PRESET ? EPISODE_SERIES : ILLUSTRATED_SERIES);

/** The fields the tool decides for the video's Short number `index` (0 or 1), over a draft. */
export const episodeShortFields = (slug, index, series = EPISODE_SERIES) => ({ schema_version: 2, slug: `${slug}-short-${index + 1}`, format: 'shorts', locale: 'zh-TW', line: 'cut', series, source: { slug } });
export const shortsFile = (slug, root = ROOT) => path.join(docDir(slug, root), 'shorts.json');

/**
 * What a shorts.json must be, beyond each Short's own schema: two Shorts of this episode, each
 * named after it, with every shot it shows among the long video's shots.
 */
export function episodeShortsProblems(shorts, video) {
  if (!Array.isArray(shorts) || shorts.length !== SHORTS_PER_EPISODE) return [`shorts.json must hold ${SHORTS_PER_EPISODE} Shorts`];
  const shots = new Set((video.scenes ?? []).filter((scene) => scene.template === 'shot').map((scene) => scene.id));
  const problems = [];
  for (const [index, doc] of shorts.entries()) {
    const where = `short ${index + 1}`;
    for (const error of validate(doc)) problems.push(`${where}: ${error}`);
    if (doc?.schema_version !== 2 || doc?.line !== 'cut') problems.push(`${where}: must be a cut (schema_version 2, line "cut")`);
    if (doc?.series !== episodeSeries(video)) problems.push(`${where}: series must be ${episodeSeries(video)}`);
    if (doc?.source?.slug !== video.slug) problems.push(`${where}: source.slug must be ${video.slug}`);
    if (doc?.slug !== `${video.slug}-short-${index + 1}`) problems.push(`${where}: slug must be ${video.slug}-short-${index + 1}`);
    const scenes = Array.isArray(doc?.scenes) ? doc.scenes : [];
    for (const [i, scene] of scenes.entries()) {
      if (scene?.shot !== undefined && !shots.has(scene.shot)) problems.push(`${where}, scene ${i}: "${scene.shot}" is not a shot of ${video.slug}`);
    }
  }
  return problems;
}

/**
 * The episode, its Shorts resolved against its keyframes, and where those keyframes are.
 * `workdir` is the episode's work directory (the same one `keyframes` wrote).
 */
export function loadEpisodeShorts({ slug, root = ROOT, env = process.env, home, workdirFlag }) {
  const dir = docDir(slug, root);
  const videoFile = path.join(dir, 'video.json');
  if (!existsSync(videoFile)) throw new Error(`no ${path.relative(root, videoFile)}`);
  const video = JSON.parse(readFileSync(videoFile, 'utf8'));
  if (!hasPictures(video)) throw new Error(`${slug} has no shots: its Shorts would have no pictures to reuse (an explainer or illustrated slides video does)`);
  const file = shortsFile(slug, root);
  if (!existsSync(file)) throw new Error(`no ${path.relative(root, file)}: the writer drafts it with the script`);
  const shorts = JSON.parse(readFileSync(file, 'utf8'));
  const problems = episodeShortsProblems(shorts, video);
  if (problems.length) throw new Error(problems.join('\n'));
  const workdir = resolveWorkdir({ flag: workdirFlag, env, slug, root, home });
  const keyframes = readJson(path.join(workdir, 'keyframes', 'manifest.json'), null);
  if (!keyframes) throw new Error(`no keyframes/manifest.json in ${workdir}: run keyframes for ${slug} first`);
  return {
    video,
    workdir,
    lexicon: readJson(lexiconFile(root), { schema_version: 1, terms: {} }),
    shorts: shorts.map((doc) => episodeShort(doc, keyframes, video)),
  };
}
