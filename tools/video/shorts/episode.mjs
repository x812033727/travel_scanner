// An explainer episode's two Shorts (docs/videos/so-thats-why/README.md §Shorts): the scripts in
// docs/videos/<slug>/shorts.json, their pictures the episode's keyframes in its work directory.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { docDir, lexiconFile, readJson, resolveWorkdir, ROOT } from '../core/paths.mjs';
import { EPISODE_SERIES, episodeShort, validate } from './core.mjs';

export const SHORTS_PER_EPISODE = 2;
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
    if (doc?.series !== EPISODE_SERIES) problems.push(`${where}: series must be ${EPISODE_SERIES}`);
    if (doc?.episode !== video.slug) problems.push(`${where}: episode must be ${video.slug}`);
    if (doc?.slug !== `${video.slug}-short-${index + 1}`) problems.push(`${where}: slug must be ${video.slug}-short-${index + 1}`);
    for (const [i, scene] of (doc?.scenes ?? []).entries()) {
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
  const file = shortsFile(slug, root);
  if (!existsSync(file)) throw new Error(`no ${path.relative(root, file)}: the explainer writer drafts it with the script`);
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
    shorts: shorts.map((doc) => episodeShort(doc, keyframes)),
  };
}
