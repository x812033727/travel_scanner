// The compilation of a binge series on the host (docs/videos/BINGE.md): once the site says every
// episode is cleared for upload, the worker starts one video that joins them all. Nothing is
// narrated or generated again. The worker's part is the document (core/compilation.mjs builds
// it), the upload fields the planner writes (title, description, tags, the thumbnail's picture
// and headline), the thumbnail's source keyframe copied from an episode, the five locales'
// title and description, and the commands in between (render, compile); the final cut, the
// upload package and the YouTube id then go the way of every video (flow.mjs).
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { sha256File } from "../core/approvals.mjs";
import { COMPILATION_HEADLINE_PLACEHOLDER, COMPILATION_TITLE_PLACEHOLDER, compilationDocument, THUMB_SHOT, THUMB_SOURCE } from "../core/compilation.mjs";
import { DESCRIPTION_MAX_BYTES, TAGS_MAX_CHARS, TITLE_MAX_CHARS } from "../core/metadata.mjs";
import { atomicWrite, docDir, readJson } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE } from "../core/schema.mjs";
import { ARTIFACTS, lintProject, loadProject } from "../core/state.mjs";
import { AutomationError, OUTPUT_INVALID } from "./client.mjs";
import { GENRE_SPECS } from "./prompts.mjs";

export const COMPILATION_FILE = "compilation.json";
// Keyframes from this many leading episodes are offered as the thumbnail's picture: the first
// episodes carry the premise, and the judge scored every keyframe when it was drawn.
export const THUMBNAIL_EPISODES = 3;
export const THUMBNAIL_CANDIDATES = 12;
export const HEADLINE_MAX_CHARS = 12;
export const TAG_MAX_CHARS = 6;
// What a chapter line of the description costs (a timestamp, 「第 N 集」 and a title of about
// twelve characters, some 60 bytes), and the room the tool's own lines take. The compile step
// falls back to bare 「第 N 集」 chapters if the titled description still passes 5,000 bytes.
const CHAPTER_LINE_BYTES = 64;
const DESCRIPTION_RESERVE_BYTES = 400;
const ANSWER_ATTEMPTS = 2;

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const bytes = (text) => Buffer.byteLength(String(text ?? ""), "utf8");

/** The compilation video's slug for a series. */
export const compilationSlug = (seriesSlug) => `${seriesSlug}-full`;

/** How many bytes the description body may take once the chapter lines are appended. */
export function descriptionBudget(episodeCount) {
  return Math.max(500, DESCRIPTION_MAX_BYTES - DESCRIPTION_RESERVE_BYTES - episodeCount * CHAPTER_LINE_BYTES);
}

/**
 * The keyframes the planner may pick the thumbnail from: the leading episodes' drawn keyframes
 * of shots with a character in frame (the face the viewer clicks on), best judged first. Each
 * candidate says where its file is, so the chosen one can be copied.
 */
export function thumbnailCandidates(workBase, root, episodes, limit = THUMBNAIL_CANDIDATES) {
  const found = [];
  for (const episode of episodes.slice(0, THUMBNAIL_EPISODES)) {
    const workdir = path.join(workBase, episode.slug);
    const manifest = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
    const video = readJson(path.join(docDir(episode.slug, root), "video.json"), null);
    if (!manifest?.shots || !video) continue;
    const scenes = new Map((video.scenes ?? []).map((scene) => [scene.id, scene]));
    for (const [shot, entry] of Object.entries(manifest.shots)) {
      const scene = scenes.get(shot);
      const characters = scene?.data?.characters ?? [];
      if (!entry?.file || entry.needs_review || !characters.length) continue;
      found.push({ episode: episode.slug, number: episode.number, shot, judge: entry.judge?.overall ?? null, characters, prompt: String(scene?.data?.prompt ?? "").slice(0, 300), file: path.join(workdir, entry.file), sha256: entry.sha256 ?? null });
    }
  }
  return found.sort((a, b) => (b.judge ?? 0) - (a.judge ?? 0)).slice(0, limit);
}

/** Why the planner's upload fields cannot be used, or null. */
export function metadataProblem(answer, candidates) {
  if (!isObject(answer)) return "the answer is not an object";
  if (!isText(answer.title) || answer.title.length > TITLE_MAX_CHARS || /[<>]/.test(answer.title)) return `title must be 1 to ${TITLE_MAX_CHARS} characters without angle brackets`;
  if (answer.title === COMPILATION_TITLE_PLACEHOLDER) return "title is still the placeholder";
  if (!isText(answer.description)) return "description is missing";
  if (!Array.isArray(answer.tags) || !answer.tags.length || !answer.tags.every(isText)) return "tags must be a list of at least one word";
  if (answer.tags.join(",").length > TAGS_MAX_CHARS) return `tags must be at most ${TAGS_MAX_CHARS} characters in all`;
  const thumbnail = answer.thumbnail;
  if (!isObject(thumbnail) || !isText(thumbnail.headline) || thumbnail.headline.length > HEADLINE_MAX_CHARS) return `thumbnail.headline must be 1 to ${HEADLINE_MAX_CHARS} characters`;
  if (thumbnail.headline === COMPILATION_HEADLINE_PLACEHOLDER) return "thumbnail.headline is still the placeholder";
  if (thumbnail.tag !== undefined && thumbnail.tag !== null && (!isText(thumbnail.tag) || thumbnail.tag.length > TAG_MAX_CHARS)) return `thumbnail.tag must be at most ${TAG_MAX_CHARS} characters or null`;
  if (candidates.length && !candidates.some((candidate) => matchesCandidate(candidate, thumbnail))) return "thumbnail.episode and thumbnail.shot must name one of thumbnail_candidates";
  return null;
}

/** The planner names the candidate by the episode's slug as asked, or by its number: both are unambiguous. */
export const matchesCandidate = (candidate, thumbnail) => (candidate.episode === thumbnail?.episode || candidate.number === thumbnail?.episode) && candidate.shot === thumbnail?.shot;

/** Why a locale's translation of the upload fields cannot be used, or null. */
export function translationProblem(answer, chapters) {
  if (!isObject(answer)) return "the answer is not an object";
  if (!isText(answer.title) || answer.title.length > TITLE_MAX_CHARS || /[<>]/.test(answer.title)) return `title must be 1 to ${TITLE_MAX_CHARS} characters without angle brackets`;
  if (!isText(answer.description) || bytes(answer.description) > DESCRIPTION_MAX_BYTES) return "description is missing or too long";
  // An empty list would read as "not translated" in lint, which qa counts against the captions.
  if (!Array.isArray(answer.tags) || !answer.tags.length || !answer.tags.every(isText) || answer.tags.join(",").length > TAGS_MAX_CHARS) return "tags must be a short list of at least one word";
  if (!isObject(answer.chapters)) return "chapters must map each episode slug to its title";
  const missing = Object.keys(chapters).filter((key) => !isText(answer.chapters[key]));
  if (missing.length) return `chapters lack ${missing.join(", ")}`;
  return null;
}

/**
 * Start the compilation the site asked for: claim the video's slug on the site, write its
 * document beside the episodes' and its state in the work directory, and report it.
 */
export async function startCompilation(automation, job) {
  const { series } = job;
  const slug = compilationSlug(series.slug);
  let started;
  try {
    started = await automation.api.compilationStart(series.slug, slug);
  } catch (error) {
    // The site refuses a compilation it cannot start (the slug is another video's, the series
    // is no longer finished): nothing on this side changes that, so say so instead of failing
    // every round with the same request.
    if (error instanceof AutomationError && error.status === 409) return automation.later(`series ${series.slug}: the site refused to start the compilation ${slug}: ${error.message}`);
    throw error;
  }
  const episodes = (started.episodes ?? []).map((episode) => ({ slug: episode.slug, number: episode.number, title: episode.title, logline: episode.logline ?? "", recap: episode.recap ?? null }));
  if (!episodes.length) return automation.later(`series ${series.slug}: the site started a compilation with no finished episodes; nothing to join`);
  const dir = docDir(slug, automation.ctx.root);
  mkdirSync(dir, { recursive: true });
  // The settings' voice as lint accepts it, not as the site serialises it (settle does the same).
  const video = compilationDocument({ slug, series: series.slug, episodes, voice: automation.voice() });
  writeFileSync(path.join(dir, "video.json"), `${JSON.stringify(video, null, 2)}\n`);
  // What the planner and the translators read later: the series as the site summarises it,
  // the episodes in order with their recaps, and the genre.
  const context = started.context ?? {};
  atomicWrite(path.join(dir, COMPILATION_FILE), `${JSON.stringify({
    series: started.series ?? series,
    episodes,
    all_recaps: context.all_recaps ?? [],
    setting_md: context.setting?.body_md ?? "",
    genre: series.genre ?? "xianxia-bonds",
  }, null, 2)}\n`);
  const state = {
    slug,
    title: `${series.title}（合集）`.slice(0, 200),
    status: "active",
    created_at: automation.ctx.now().toISOString(),
    format: "drama",
    compilation: { series: series.slug, episodes: episodes.map((episode) => episode.slug) },
    series: { slug: series.slug, genre: series.genre ?? "xianxia-bonds", lead: series.lead ?? "dual-male", visual_tier: series.visual_tier ?? "clips", compilation: true, hands_off: Boolean(series.hands_off) },
    replans: 0,
    verify_rounds: 0,
    verified: true,
    listener_done: true,
    retakes: 0,
    rewrites: 0,
    prompt_fixes: {},
    notes: [],
  };
  automation.saveState(automation.workdir(slug), state);
  await automation.report(state, "compilation started");
  return `series ${series.slug}: compilation ${slug} started from ${episodes.length} episodes`;
}

/**
 * The planner writes the upload fields and picks the thumbnail's picture; the chosen keyframe
 * is copied into the work directory as the "thumb" shot so render draws the thumbnail on it.
 */
export async function planMetadata(automation, state) {
  const { ctx } = automation;
  const dir = docDir(state.slug, ctx.root);
  const info = readJson(path.join(dir, COMPILATION_FILE), {});
  const episodes = info.episodes ?? [];
  const candidates = thumbnailCandidates(automation.workBase, ctx.root, episodes);
  const payload = {
    series: info.series ?? {},
    genre_spec: GENRE_SPECS[state.series?.genre] ?? null,
    series_reference: automation.reference().series,
    episodes: episodes.map(({ slug, number, title, logline, recap }) => ({ slug, number, title, logline, recap })),
    all_recaps: info.all_recaps ?? [],
    description_budget_bytes: descriptionBudget(episodes.length),
    thumbnail_headline_max: HEADLINE_MAX_CHARS,
    thumbnail_candidates: candidates.map(({ episode, number, shot, judge, characters, prompt }) => ({ episode, number, shot, judge, characters, prompt })),
  };
  let problem = null;
  let answer = null;
  for (let attempt = 0; attempt < ANSWER_ATTEMPTS && !answer; attempt++) {
    let candidate;
    try {
      candidate = await automation.stage("planner", state.slug, problem ? { ...payload, previous_problem: problem } : payload, 16_000, "drama", "compilation", state.series);
    } catch (error) {
      if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
      problem = error.message;
      continue;
    }
    problem = metadataProblem(candidate, candidates);
    if (!problem) answer = candidate;
  }
  if (!answer) return automation.retryLater(state, "planner", `the compilation's upload fields were not usable (${problem})`);
  const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
  const description = bytes(answer.description) > descriptionBudget(episodes.length) ? answer.description.slice(0, Math.floor(descriptionBudget(episodes.length) / 3)) : answer.description;
  video.youtube = { ...video.youtube, title: answer.title.trim(), description: description.trim(), tags: answer.tags.map((tag) => tag.trim()), video_id: null };
  video.thumbnail = { template: "thumb", data: { headline: answer.thumbnail.headline.trim(), ...(isText(answer.thumbnail.tag) ? { tag: answer.thumbnail.tag.trim() } : {}), shot: THUMB_SHOT } };
  const chosen = candidates.find((candidate) => matchesCandidate(candidate, answer.thumbnail)) ?? candidates[0] ?? null;
  const workdir = automation.workdir(state.slug);
  if (chosen && existsSync(chosen.file)) {
    mkdirSync(path.join(workdir, "keyframes"), { recursive: true });
    copyFileSync(chosen.file, path.join(workdir, THUMB_SOURCE));
    atomicWrite(path.join(workdir, ARTIFACTS.keyframes), `${JSON.stringify({ shots: { [THUMB_SHOT]: { file: THUMB_SOURCE, sha256: await sha256File(path.join(workdir, THUMB_SOURCE)), source: { episode: chosen.episode, shot: chosen.shot } } } }, null, 2)}\n`);
  } else {
    // No episode keyframe to draw on: the thumb template still draws its text on the theme.
    delete video.thumbnail.data.shot;
  }
  writeFileSync(path.join(dir, "video.json"), `${JSON.stringify(video, null, 2)}\n`);
  atomicWrite(path.join(dir, "metadata-plan.json"), `${JSON.stringify({ titles: [answer.title, ...(Array.isArray(answer.titles) ? answer.titles : [])], thumbnail: answer.thumbnail, planned_at: ctx.now().toISOString() }, null, 2)}\n`);
  const errors = lintProject(loadProject({ slug: state.slug, root: ctx.root })).errors;
  if (errors.length) return automation.retryLater(state, "planner", `the compilation's document fails lint after the upload fields: ${errors.slice(0, 3).map((error) => `${error.path}: ${error.message}`).join("; ")}`);
  automation.cleared(state, "planner");
  automation.saveState(workdir, state);
  await automation.report(state, "metadata planned");
  return `${state.slug}: title, description, tags and thumbnail planned (${answer.title})`;
}

/**
 * The other four locales' title, description, tags and chapter titles, one locale a unit. Every
 * locale the site captions in gets them (YouTube's localizations), whatever the caption
 * setting narrows the episodes to: the compilation's status waits on all four.
 */
export async function translateMetadata(automation, state) {
  const { ctx } = automation;
  const dir = docDir(state.slug, ctx.root);
  const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
  const info = readJson(path.join(dir, COMPILATION_FILE), {});
  const chapters = Object.fromEntries((info.episodes ?? []).map((episode) => [episode.slug, video.compilation?.titles?.[episode.slug] ?? `第 ${episode.number} 集`]));
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    const file = path.join(dir, "i18n", `${locale}.json`);
    const existing = readJson(file, null);
    if (existing && isText(existing.title) && isText(existing.description) && Array.isArray(existing.tags) && existing.tags.length && isObject(existing.chapters) && Object.keys(chapters).every((key) => isText(existing.chapters[key]))) continue;
    const answer = await automation.stage("translator", state.slug, { locale, youtube: { title: video.youtube.title, description: video.youtube.description, tags: video.youtube.tags }, chapters, series: info.series ?? {} }, 16_000, "drama", "compilation");
    const problem = translationProblem(answer, chapters);
    if (problem) return automation.retryLater(state, "translator", `the ${locale} upload fields ${problem}`);
    mkdirSync(path.join(dir, "i18n"), { recursive: true });
    atomicWrite(file, `${JSON.stringify({ title: answer.title.trim(), description: answer.description.trim(), tags: answer.tags.map((tag) => tag.trim()), chapters: Object.fromEntries(Object.keys(chapters).map((key) => [key, answer.chapters[key].trim()])), lines: {} }, null, 2)}\n`);
    automation.cleared(state, "translator");
    automation.saveState(automation.workdir(state.slug), state);
    return `${state.slug}: ${locale} title and description translated`;
  }
  return `${state.slug}: every locale's upload fields are translated`;
}

/**
 * One step of a compilation, or undefined when `next` is a step every video shares (the final
 * cut, the upload package, the YouTube id), which flow.mjs handles.
 */
export async function advanceCompilation(automation, state, next) {
  const { ctx } = automation;
  if (next === "metadata planned") return planMetadata(automation, state);
  if (next === "cards rendered") {
    const channel = ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", ctx.env.VIDEO_BROWSER_CHANNEL] : [];
    const result = await automation.run(["render", "--slug", state.slug, ...channel]);
    if (result.code !== 0) return automation.block(state, `render failed: ${automation.lastLine(result.out)}`);
    return `${state.slug}: chapter cards and thumbnail rendered`;
  }
  if (next === "video compiled") {
    const result = await automation.run(["compile", "--slug", state.slug]);
    if (result.code === 0) {
      automation.cleared(state, "compile");
      automation.saveState(automation.workdir(state.slug), state);
      await automation.report(state, "video compiled");
      return `${state.slug}: episodes joined into one cut`;
    }
    // Exit 2: an episode is not cleared for upload any more (re-cut after its approval); exit
    // 3: the owner (disk, a setting); exit 4: a tool or the STOP file, tried again next round.
    if (result.code === 4) return automation.later(`${state.slug}: compile could not finish (${automation.lastLine(result.out)}); the next run tries again`);
    return automation.block(state, `compile failed: ${automation.lastLine(result.out, 2)}`);
  }
  if (next === "metadata translated") return translateMetadata(automation, state);
  return undefined;
}
