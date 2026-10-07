// The compilation of a binge series on the host (docs/videos/BINGE.md): once the site says every
// episode is cleared for upload, the worker starts one video that joins them all. Nothing is
// narrated or generated again. The worker's part is the document (core/compilation.mjs builds
// it), the upload fields the planner writes (title, description, tags, the thumbnail's picture
// and headline), the thumbnail's source keyframe copied from an episode, the five locales'
// title and description, and the commands in between (render, compile); the final cut, the
// upload package and the YouTube id then go the way of every video (flow.mjs).
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";

import { sha256File } from "../core/approvals.mjs";
import { appliedBranding, presentationTimeline } from "../core/branding.mjs";
import { COMPILATION_HEADLINE_PLACEHOLDER, COMPILATION_TITLE_PLACEHOLDER, compilationDocument, compilationScenes, episodeNumbers, THUMB_SHOT, THUMB_SOURCE, TITLE_MAX_CHARS as CHAPTER_TITLE_MAX } from "../core/compilation.mjs";
import { COMPILATION_REVIEW_FILE, contextFromSeries, publicTexts, reviewCurrent, reviewHash, reviewProblem } from "../core/compilation-review.mjs";
import { DESCRIPTION_MAX_BYTES, TAGS_MAX_CHARS, TITLE_MAX_CHARS } from "../core/metadata.mjs";
import { atomicWrite, docDir, readJson } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE } from "../core/schema.mjs";
import { ARTIFACTS, lintProject, loadProject } from "../core/state.mjs";
import { chosenLocales, readLanguages } from "../core/stages.mjs";
import { composeMetadata } from "../package/metadata.mjs";
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

const writeJson = (file, value) => atomicWrite(file, `${JSON.stringify(value, null, 2)}\n`);
const chaptersOf = (video) => Object.fromEntries(video.compilation.episodes.map((slug, index) => [slug, video.compilation.titles?.[slug] ?? `第 ${episodeNumbers(video.compilation)[index]} 集`]));

/** Restore a legacy compilation's missing context; an absent schedule never means no mysteries. */
async function compilationInfo(automation, state) {
  const file = path.join(docDir(state.slug, automation.ctx.root), COMPILATION_FILE);
  const info = readJson(file, {});
  if (!Array.isArray(info.spoiler_context?.mysteries)) {
    const series = state.compilation?.series ?? state.series?.slug;
    const context = contextFromSeries(await automation.api.seriesContext(series));
    if (!context) return { info, problem: "the series has no usable mystery context; restore its setting and reveal schedule before reviewing public text" };
    info.spoiler_context = context;
    writeJson(file, info);
  }
  return { info, problem: null };
}

function reviewInputs(automation, state, video, translations = {}, plan = null) {
  const workdir = automation.workdir(state.slug);
  const body = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const timeline = body ? presentationTimeline(body, appliedBranding(readJson(path.join(workdir, ARTIFACTS.checks), null))) : null;
  const pack = video.source_guide ? loadProject({ slug: state.slug, root: automation.ctx.root }).pack ?? null : null;
  return publicTexts({ doc: video, translations, timeline, plan, pack });
}

function receiptsFor(automation, state) {
  return readJson(path.join(docDir(state.slug, automation.ctx.root), COMPILATION_REVIEW_FILE), { schema_version: 1, locales: {} });
}

function saveReview(automation, state, context, locale, fields) {
  const receipts = receiptsFor(automation, state);
  writeJson(path.join(docDir(state.slug, automation.ctx.root), COMPILATION_REVIEW_FILE), {
    schema_version: 1,
    locales: { ...(receipts.schema_version === 1 ? receipts.locales : {}), [locale]: { passed: true, input_sha256: reviewHash(context, locale, fields), reviewed_at: automation.ctx.now().toISOString() } },
  });
  automation.cleared(state, "verifier");
  automation.cleared(state, locale === NARRATION_LOCALE ? "planner" : "translator");
  automation.saveState(automation.workdir(state.slug), state);
}

async function publicTextProblem(automation, state, context, locale, fields) {
  if (!context.mysteries.length) return null;
  try {
    const verdict = await automation.stage("verifier", state.slug, { locale, spoiler_context: context, public_text: fields }, 16_000, "drama", "compilation", state.series);
    return reviewProblem(verdict);
  } catch (error) {
    if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
    return error.message;
  }
}

function applyChapterTitles(video, titles) {
  video.compilation.titles = titles;
  const numbers = episodeNumbers(video.compilation);
  video.scenes = compilationScenes({
    episodes: video.compilation.episodes.map((slug, index) => ({ slug, number: numbers[index], title: titles[slug] })),
    chapterCards: video.compilation.chapter_cards ?? true,
    outro: video.compilation.outro ?? true,
    outroData: video.scenes.find((scene) => scene.template === "outro")?.data,
  });
}

/** The compilation video's slug for a series. */
export const compilationSlug = (seriesSlug) => `${seriesSlug}-full`;

/** How many bytes the description body may take once the chapter lines are appended. */
export function descriptionBudget(episodeCount) {
  return Math.max(500, DESCRIPTION_MAX_BYTES - DESCRIPTION_RESERVE_BYTES - episodeCount * CHAPTER_LINE_BYTES);
}

/** Whether `file` is there and holds the bytes the episode's manifest approved (`sha256`). */
function approvedBytes(file, sha256) {
  if (!/^[0-9a-f]{64}$/.test(sha256 ?? "") || !existsSync(file)) return false;
  return createHash("sha256").update(readFileSync(file)).digest("hex") === sha256;
}

/**
 * The keyframes the planner may pick the thumbnail from: the leading episodes' drawn keyframes
 * of shots with a character in frame (the face the viewer clicks on), best judged first. Each
 * candidate says where its file is, so the chosen one can be copied. A keyframe file is reused
 * by a later take of the same seed, so one whose bytes are not the ones its manifest approved
 * (or that is missing, or has no recorded hash) is never offered: hashed best first, until
 * `limit` are found.
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
  const offered = [];
  for (const candidate of found.sort((a, b) => (b.judge ?? 0) - (a.judge ?? 0))) {
    if (offered.length >= limit) break;
    if (approvedBytes(candidate.file, candidate.sha256)) offered.push(candidate);
  }
  return offered;
}

/**
 * Copy the chosen episode keyframe to the compilation's THUMB_SOURCE and record it in the
 * compilation's keyframes manifest under the episode's approved hash. False, with any earlier
 * copy left as it was, when the file is gone or no longer holds those bytes: it is copied to a
 * temporary file and compared before it takes the place of the old one.
 */
export async function copyThumbSource(workdir, chosen) {
  const target = path.join(workdir, THUMB_SOURCE);
  const temporary = `${target}.${process.pid}.tmp`;
  if (!existsSync(chosen.file)) return false;
  mkdirSync(path.dirname(target), { recursive: true });
  copyFileSync(chosen.file, temporary);
  if ((await sha256File(temporary)) !== chosen.sha256) {
    rmSync(temporary, { force: true });
    return false;
  }
  renameSync(temporary, target);
  atomicWrite(path.join(workdir, ARTIFACTS.keyframes), `${JSON.stringify({ shots: { [THUMB_SHOT]: { file: THUMB_SOURCE, sha256: chosen.sha256, source: { episode: chosen.episode, shot: chosen.shot } } } }, null, 2)}\n`);
  return true;
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
    spoiler_context: contextFromSeries(context),
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
export async function planMetadata(automation, state, previousProblem = null) {
  const { ctx } = automation;
  const dir = docDir(state.slug, ctx.root);
  const loaded = await compilationInfo(automation, state);
  if (loaded.problem) return automation.block(state, loaded.problem);
  const { info } = loaded;
  const context = info.spoiler_context;
  const file = path.join(dir, "video.json");
  const original = readFileSync(file, "utf8");
  const before = JSON.parse(original);
  const episodes = info.episodes ?? [];
  const candidates = thumbnailCandidates(automation.workBase, ctx.root, episodes);
  const payload = {
    series: info.series ?? {},
    genre_spec: GENRE_SPECS[state.series?.genre] ?? null,
    series_reference: automation.reference().series,
    episodes: episodes.map(({ slug, number, title, logline, recap }) => ({ slug, number, title, logline, recap })),
    all_recaps: info.all_recaps ?? [],
    spoiler_context: context,
    chapters: chaptersOf(before),
    description_budget_bytes: descriptionBudget(episodes.length),
    thumbnail_headline_max: HEADLINE_MAX_CHARS,
    thumbnail_candidates: candidates.map(({ episode, number, shot, judge, characters, prompt }) => ({ episode, number, shot, judge, characters, prompt })),
  };
  let problem = previousProblem;
  let answer = null;
  let video;
  let plan;
  let fields;
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
    if (problem) continue;
    if (context.mysteries.length || candidate.chapters !== undefined) {
      const chapters = candidate.chapters;
      if (!isObject(chapters) || Object.keys(chapters).length !== before.compilation.episodes.length || before.compilation.episodes.some((slug) => !isText(chapters[slug]) || [...chapters[slug].trim()].length > CHAPTER_TITLE_MAX)) {
        problem = `chapters must give every episode slug a public title of 1 to ${CHAPTER_TITLE_MAX} characters`;
        continue;
      }
    }
    video = structuredClone(before);
    const description = bytes(candidate.description) > descriptionBudget(episodes.length) ? candidate.description.slice(0, Math.floor(descriptionBudget(episodes.length) / 3)) : candidate.description;
    video.youtube = { ...video.youtube, title: candidate.title.trim(), description: description.trim(), tags: candidate.tags.map((tag) => tag.trim()) };
    video.thumbnail = { template: "thumb", data: { headline: candidate.thumbnail.headline.trim(), ...(isText(candidate.thumbnail.tag) ? { tag: candidate.thumbnail.tag.trim() } : {}), shot: THUMB_SHOT } };
    if (candidate.chapters) applyChapterTitles(video, Object.fromEntries(video.compilation.episodes.map((slug) => [slug, candidate.chapters[slug].trim()])));
    plan = { titles: [candidate.title, ...(Array.isArray(candidate.titles) ? candidate.titles : [])], thumbnail: candidate.thumbnail, ...(isText(candidate.pinned_comment) ? { pinned_comment: candidate.pinned_comment } : {}), planned_at: ctx.now().toISOString() };
    const errors = lintProject({ ...loadProject({ slug: state.slug, root: ctx.root }), doc: video }).errors;
    if (errors.length) {
      problem = `the candidate fails lint: ${errors.slice(0, 3).map((error) => `${error.path}: ${error.message}`).join("; ")}`;
      continue;
    }
    fields = reviewInputs(automation, state, video, {}, plan)[NARRATION_LOCALE];
    problem = await publicTextProblem(automation, state, context, NARRATION_LOCALE, fields);
    if (!problem) answer = candidate;
  }
  if (!answer) return automation.retryLater(state, "planner", `the compilation's upload fields were not usable (${problem})`);
  if (readFileSync(file, "utf8") !== original) return automation.retryLater(state, "planner", "the compilation changed while its public text was reviewed; retry without overwriting the newer document");
  const chosen = candidates.find((candidate) => matchesCandidate(candidate, answer.thumbnail)) ?? candidates[0] ?? null;
  const workdir = automation.workdir(state.slug);
  if (chosen) {
    // Drawn over or removed since it was offered: plan again rather than draw on bytes nobody
    // approved, or drop the picture the planner chose its headline for.
    if (!(await copyThumbSource(workdir, chosen))) return automation.retryLater(state, "planner", `the thumbnail's keyframe ${chosen.episode}/${chosen.shot} changed since it was offered`);
  } else {
    // No episode keyframe to draw on: the thumb template still draws its text on the theme.
    delete video.thumbnail.data.shot;
  }
  writeJson(file, video);
  writeJson(path.join(dir, "metadata-plan.json"), plan);
  if (context.mysteries.length) saveReview(automation, state, context, NARRATION_LOCALE, fields);
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
  const original = readFileSync(path.join(dir, "video.json"), "utf8");
  const video = JSON.parse(original);
  const loaded = await compilationInfo(automation, state);
  if (loaded.problem) return automation.block(state, loaded.problem);
  const { info } = loaded;
  const context = info.spoiler_context;
  const chapters = chaptersOf(video);
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    const file = path.join(dir, "i18n", `${locale}.json`);
    const existing = readJson(file, null);
    let problem = null;
    let fields;
    if (existing && !translationProblem(existing, chapters)) {
      if (!context.mysteries.length) continue;
      fields = reviewInputs(automation, state, video, { [locale]: existing })[locale];
      if (reviewCurrent(receiptsFor(automation, state), context, locale, fields)) continue;
      problem = await publicTextProblem(automation, state, context, locale, fields);
      if (!problem) {
        saveReview(automation, state, context, locale, fields);
        return `${state.slug}: ${locale} public text reviewed`;
      }
    }
    const payload = { locale, youtube: { title: video.youtube.title, description: video.youtube.description, tags: video.youtube.tags }, chapters, series: info.series ?? {}, spoiler_context: context };
    let translated = null;
    for (let attempt = 0; attempt < ANSWER_ATTEMPTS && !translated; attempt++) {
      let answer;
      try {
        answer = await automation.stage("translator", state.slug, problem ? { ...payload, previous_problem: problem } : payload, 16_000, "drama", "compilation");
      } catch (error) {
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        problem = error.message;
        continue;
      }
      problem = translationProblem(answer, chapters);
      if (problem) continue;
      const candidate = { title: answer.title.trim(), description: answer.description.trim(), tags: answer.tags.map((tag) => tag.trim()), chapters: Object.fromEntries(Object.keys(chapters).map((key) => [key, answer.chapters[key].trim()])), lines: {} };
      fields = reviewInputs(automation, state, video, { [locale]: candidate })[locale];
      problem = await publicTextProblem(automation, state, context, locale, fields);
      if (!problem) translated = candidate;
    }
    if (!translated) return automation.retryLater(state, "translator", `the ${locale} upload fields were not usable (${problem})`);
    if (readFileSync(path.join(dir, "video.json"), "utf8") !== original || JSON.stringify(readJson(file, null)) !== JSON.stringify(existing)) {
      return automation.retryLater(state, "translator", "the compilation or translation changed during review; retry without overwriting newer text");
    }
    mkdirSync(path.join(dir, "i18n"), { recursive: true });
    writeJson(file, translated);
    if (context.mysteries.length) saveReview(automation, state, context, locale, fields);
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
  const loaded = await compilationInfo(automation, state);
  if (loaded.problem) return automation.block(state, loaded.problem);
  const context = loaded.info.spoiler_context;
  if (context.mysteries.length) {
    const dir = docDir(state.slug, ctx.root);
    const project = loadProject({ slug: state.slug, root: ctx.root });
    const plan = readJson(path.join(dir, "metadata-plan.json"), null);
    const fields = reviewInputs(automation, state, project.doc, project.translations, plan);
    const receipts = receiptsFor(automation, state);
    if (!reviewCurrent(receipts, context, NARRATION_LOCALE, fields[NARRATION_LOCALE])) {
      const problem = await publicTextProblem(automation, state, context, NARRATION_LOCALE, fields[NARRATION_LOCALE]);
      if (problem) return planMetadata(automation, state, problem);
      saveReview(automation, state, context, NARRATION_LOCALE, fields[NARRATION_LOCALE]);
      return `${state.slug}: source public text reviewed`;
    }
    const later = ["metadata translated", "final video approved", "upload package", "on YouTube"].includes(next) || !next;
    const needsTranslationReview = LOCALES.filter((locale) => locale !== NARRATION_LOCALE).some((locale) => {
      const translation = project.translations[locale];
      return translation ? translationProblem(translation, chaptersOf(project.doc)) || !reviewCurrent(receipts, context, locale, fields[locale]) : later;
    });
    if (needsTranslationReview) return translateMetadata(automation, state);
    // Status historically binds a package only to final.mp4. A resumed worker must replace
    // its old public fields before handing that package to the shared publish step.
    if (next === "on YouTube" || !next) {
      const workdir = automation.workdir(state.slug);
      const packaged = readJson(path.join(workdir, "upload", "metadata.json"), null);
      const body = readJson(path.join(workdir, ARTIFACTS.timeline), null);
      const timeline = body ? presentationTimeline(body, appliedBranding(readJson(path.join(workdir, ARTIFACTS.checks), null))) : null;
      if (!timeline) return automation.block(state, "the compilation has no timeline for its public chapter list; run compile first");
      const expected = composeMetadata({ doc: project.doc, timeline, translations: project.translations, pack: project.pack ?? null, locales: chosenLocales(readLanguages(workdir), "metadata") }).metadata;
      const keys = ["title", "description", "tags", "localizations", "chapters", "default_language"];
      if (!packaged || keys.some((key) => JSON.stringify(packaged[key]) !== JSON.stringify(expected[key]))) {
        const result = await automation.run(["package", "--slug", state.slug]);
        if (result.code !== 0) return automation.block(state, `package failed after public-text review: ${automation.lastLine(result.out)}`);
        return `${state.slug}: reviewed upload metadata rebuilt`;
      }
    }
  }
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
