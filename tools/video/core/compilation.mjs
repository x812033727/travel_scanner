// A binge series' compilation, the 合集 (docs/videos/BINGE.md): one long video that plays every
// episode's finished cut in order, a chapter card before each and an outro after the last, with
// one YouTube chapter per episode. Nothing is narrated or generated again: the worker makes the
// project once every episode is cleared for upload, `render` draws the cards and the thumbnail,
// and `compile` joins the cuts. This module holds the document's rules, the layout on the 30 fps
// grid, the hash that says which cuts a compilation was made from, and the pieces the later
// stages share: the chapters, the merged captions and the description's byte budget.
//
// schema.mjs imports the validator from here, and this module reaches schema.mjs back through
// captions.mjs, metadata.mjs and timeline.mjs. The cycle is harmless: every binding that crosses
// it is a function declaration, used when called and never while the modules load.
import { createHash } from "node:crypto";

import { parseSrt } from "./captions.mjs";
import { SERIES_SLUG } from "./drama.mjs";
import { checkYoutubeFields, composeDescription, DESCRIPTION_MAX_BYTES } from "./metadata.mjs";
import { validateVideo } from "./schema.mjs";
import { visualHash } from "./timeline.mjs";
import { metadataStatus, namedWith } from "./translations.mjs";

// A compilation is a drama for every stage that asks (the disclosure, the steps), with a
// `compilation` block instead of a look, a cast and shots.
export const COMPILATION_FORMAT = "drama";
const FPS = 30;
const SAMPLE_RATE = 48_000;
// A chapter card stays two seconds and the outro four: long enough to read, short enough not
// to break the binge between two episodes.
export const CARD_FRAMES = 60;
export const OUTRO_FRAMES = 120;
export const TITLE_MAX_CHARS = 40;
// What the worker writes before the planner has named the compilation; status waits on them.
export const PLACEHOLDER_TITLE = "（合集標題待企劃）";
export const COMPILATION_TITLE_PLACEHOLDER = PLACEHOLDER_TITLE;
export const PLACEHOLDER_DESCRIPTION = "（合集說明待企劃）";
export const COMPILATION_HEADLINE_PLACEHOLDER = "（待企劃）";
/**
 * The compilation's pipeline steps, in order (core/state.mjs reports them). The worker copies
 * the thumbnail's source keyframe into the work directory during "metadata planned", so
 * "cards rendered" can draw the thumbnail on it.
 */
export const COMPILATION_STEPS = [
  "metadata planned",
  "cards rendered",
  "video compiled",
  "metadata translated",
  "final video approved",
  "upload package",
  "on YouTube",
];
// The thumbnail's background is an episode keyframe the worker copies into the work directory
// and lists in keyframes/manifest.json under this shot id, so render resolves it as a drama's.
export const THUMB_SHOT = "thumb";
export const THUMB_SOURCE = "keyframes/thumb-source.png";
export const OUTRO_ID = "outro";
export const DEFAULT_OUTRO = { title: "全集完", cta: "每一集都在頻道裡" };
// Lint and qa estimate the chapter timestamps before the cuts are joined: four minutes an episode.
export const ESTIMATED_EPISODE_FRAMES = 4 * 60 * FPS;
const COMPILATION_KEYS = new Set(["series", "episodes", "chapter_cards", "outro", "titles", "numbers"]);
const VIDEO_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
// The chapter label a locale falls back to when every title would not fit the description.
const EPISODE_LABELS = {
  "zh-TW": (n) => `第 ${n} 集`,
  "zh-CN": (n) => `第 ${n} 集`,
  ja: (n) => `第${n}話`,
  ko: (n) => `${n}화`,
  en: (n) => `Episode ${n}`,
};

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const hash16 = (...parts) => {
  const digest = createHash("sha256");
  for (const part of parts) digest.update(typeof part === "string" ? part : JSON.stringify(part));
  return digest.digest("hex").slice(0, 16);
};

function unknownKeys(value, allowed, where, errors) {
  for (const key of Object.keys(value)) {
    if (!allowed.has(key)) errors.push({ path: `${where}.${key}`, message: `unknown field "${key}"` });
  }
}

export const isCompilation = (doc) => isObject(doc?.compilation);
export const cardId = (number) => `card-${number}`;
export const cardLineId = (number) => `c${String(number).padStart(3, "0")}`;
/** 「第 N 集 <title>」, or 「第 N 集」 alone when the episode has no title yet. */
export const chapterTitle = (number, title = "") => (isText(title) ? `第 ${number} 集 ${title.trim()}` : `第 ${number} 集`);
export const episodeLabel = (number, locale = "zh-TW") => (EPISODE_LABELS[locale] ?? EPISODE_LABELS.en)(number);

/**
 * Each episode's number in the series, in play order: `compilation.numbers` when the block has
 * it (a chapter's compilation starts past 1, and a skipped episode leaves a gap), else the
 * position. The cards and the chapters say 「第 N 集」 with this N.
 */
export function episodeNumbers(spec) {
  return (spec.episodes ?? []).map((slug, index) => (Number.isInteger(spec.numbers?.[slug]) ? spec.numbers[slug] : index + 1));
}

/** The card scenes a compilation document holds: one chapter card per episode ({ slug, number, title }), then the outro. */
export function compilationScenes({ episodes, chapterCards = true, outro = true, outroData = DEFAULT_OUTRO }) {
  const scenes = [];
  if (chapterCards) {
    for (const episode of episodes) {
      const title = chapterTitle(episode.number, episode.title);
      scenes.push({ id: cardId(episode.number), chapter: title, template: "chapter", data: { title: isText(episode.title) ? episode.title.trim() : chapterTitle(episode.number) }, lines: [{ id: cardLineId(episode.number), text: title }] });
    }
  }
  if (outro) scenes.push({ id: OUTRO_ID, template: "outro", data: { ...outroData }, lines: [{ id: OUTRO_ID, text: outroData.title }] });
  return scenes;
}

/**
 * A compilation's video.json as the worker creates it, complete enough to pass validateVideo
 * and lint: the `compilation` block, the placeholder title, description and thumbnail headline
 * the planner replaces, and the card scenes that follow from the block, with line ids fixed by
 * the episode numbers so a rebuild gives the same document. `episodes` is [{ slug, number,
 * title }] in play order; `voice` is the settings' voice object. The thumbnail's `shot` is the
 * keyframe the worker copies into keyframes/manifest.json under `thumb`.
 */
export function compilationDocument({ slug, series, episodes, voice, chapterCards = true, outro = true, outroData = DEFAULT_OUTRO }) {
  const titles = Object.fromEntries(episodes.filter((episode) => isText(episode.title)).map((episode) => [episode.slug, episode.title.trim()]));
  const numbered = episodes.map((episode, index) => ({ ...episode, number: Number.isInteger(episode.number) ? episode.number : index + 1 }));
  const numbers = Object.fromEntries(numbered.map((episode) => [episode.slug, episode.number]));
  const positional = numbered.every((episode, index) => episode.number === index + 1);
  return {
    schema_version: 1,
    slug: slug ?? `${series}-full`,
    format: COMPILATION_FORMAT,
    ...(voice ? { voice } : {}),
    compilation: {
      series,
      episodes: numbered.map((episode) => episode.slug),
      chapter_cards: chapterCards,
      outro,
      ...(Object.keys(titles).length ? { titles } : {}),
      ...(positional ? {} : { numbers }),
    },
    youtube: { category_id: 24, made_for_kids: false, default_language: "zh-TW", title: PLACEHOLDER_TITLE, description: PLACEHOLDER_DESCRIPTION, tags: [], video_id: null },
    thumbnail: { template: "thumb", data: { headline: COMPILATION_HEADLINE_PLACEHOLDER, shot: THUMB_SHOT } },
    scenes: compilationScenes({ episodes: numbered, chapterCards, outro, outroData }),
  };
}

/**
 * Every compilation-only rule, appended to `errors`. Runs after the shared structure checks
 * (schema.mjs validates the scenes and lines as objects with ids first). A compilation refuses
 * what an episode has (shots, a cast, a look, music, `series`) and pins its scenes to the cards
 * its `compilation` block implies, so the document has one source of truth.
 */
export function validateCompilation(doc, errors) {
  const spec = doc.compilation;
  if (doc.format !== COMPILATION_FORMAT) errors.push({ path: "format", message: `a compilation has format "${COMPILATION_FORMAT}": it joins a drama series' episodes` });
  if (!isObject(spec)) {
    errors.push({ path: "compilation", message: "must be an object { series, episodes, chapter_cards?, outro?, titles? }" });
    return;
  }
  unknownKeys(spec, COMPILATION_KEYS, "compilation", errors);
  if (typeof spec.series !== "string" || !SERIES_SLUG.test(spec.series)) {
    errors.push({ path: "compilation.series", message: "must be the series' slug: lowercase letters, digits and hyphens" });
  }
  const episodes = Array.isArray(spec.episodes) && spec.episodes.length ? spec.episodes : null;
  if (!episodes) errors.push({ path: "compilation.episodes", message: "must list at least one episode's video slug, in play order" });
  else {
    episodes.forEach((slug, index) => {
      const where = `compilation.episodes[${index}]`;
      if (typeof slug !== "string" || !VIDEO_SLUG.test(slug)) errors.push({ path: where, message: "must be an episode's video slug" });
      else if (episodes.indexOf(slug) !== index) errors.push({ path: where, message: `duplicates compilation.episodes[${episodes.indexOf(slug)}]` });
      else if (slug === doc.slug) errors.push({ path: where, message: "a compilation cannot contain itself" });
    });
  }
  for (const key of ["chapter_cards", "outro"]) {
    if (spec[key] !== undefined && typeof spec[key] !== "boolean") errors.push({ path: `compilation.${key}`, message: "must be true or false" });
  }
  if (spec.titles !== undefined) {
    if (!isObject(spec.titles)) errors.push({ path: "compilation.titles", message: "must map an episode slug to its chapter title" });
    else {
      for (const [slug, title] of Object.entries(spec.titles)) {
        if (!episodes?.includes(slug)) errors.push({ path: `compilation.titles.${slug}`, message: "names an episode that is not in compilation.episodes" });
        if (!isText(title) || [...title.trim()].length > TITLE_MAX_CHARS) errors.push({ path: `compilation.titles.${slug}`, message: `must be a chapter title of at most ${TITLE_MAX_CHARS} characters` });
      }
    }
  }
  if (spec.numbers !== undefined) {
    if (!isObject(spec.numbers)) errors.push({ path: "compilation.numbers", message: "must map an episode slug to its number in the series" });
    else {
      for (const [slug, number] of Object.entries(spec.numbers)) {
        if (!episodes?.includes(slug)) errors.push({ path: `compilation.numbers.${slug}`, message: "names an episode that is not in compilation.episodes" });
        if (!Number.isInteger(number) || number < 1) errors.push({ path: `compilation.numbers.${slug}`, message: "must be a positive integer" });
      }
      const numbers = episodeNumbers(spec);
      if (numbers.some((number, index) => index > 0 && number <= numbers[index - 1])) errors.push({ path: "compilation.numbers", message: "a compilation plays its episodes in order: the numbers must increase" });
    }
  }
  for (const key of ["characters", "look", "music"]) {
    if (doc[key] !== undefined) errors.push({ path: key, message: `a compilation has no ${key}: the episodes were made with theirs` });
  }
  if (doc.series !== undefined) errors.push({ path: "series", message: "only an episode has series; a compilation names its series in compilation.series" });
  if (doc.subtitles !== undefined && (!isObject(doc.subtitles) || doc.subtitles.burn_in === true)) {
    errors.push({ path: "subtitles", message: "a compilation burns no subtitles: the episodes' cuts already carry theirs; omit subtitles or set burn_in false" });
  }
  if (isObject(doc.thumbnail?.data) && doc.thumbnail.data.shot !== undefined && doc.thumbnail.data.shot !== THUMB_SHOT) {
    errors.push({ path: "thumbnail.data.shot", message: `must be "${THUMB_SHOT}": keyframes/manifest.json lists the chosen episode keyframe under that id` });
  }
  if (!Array.isArray(doc.scenes) || !episodes) return;
  const cards = spec.chapter_cards ?? true;
  const outro = spec.outro ?? true;
  const numbers = episodeNumbers(spec);
  const expected = [
    ...(cards ? episodes.map((slug, index) => ({ id: cardId(numbers[index]), template: "chapter", n: numbers[index] })) : []),
    ...(outro ? [{ id: OUTRO_ID, template: "outro" }] : []),
  ];
  if (doc.scenes.length !== expected.length) {
    const wanted = [cards ? `one "chapter" card per episode (${episodes.length})` : "no chapter cards", outro ? "one outro" : "no outro"].join(" and ");
    errors.push({ path: "scenes", message: `a compilation's scenes are ${wanted}; found ${doc.scenes.length} scenes` });
  }
  doc.scenes.forEach((scene, index) => {
    if (!isObject(scene)) return;
    const where = `scenes[${index}]`;
    if (scene.template === "shot") {
      errors.push({ path: `${where}.template`, message: '"shot" scenes belong to an episode; a compilation joins the episodes\' finished cuts' });
      return;
    }
    const want = expected[index];
    if (!want) return;
    if (scene.id !== want.id) errors.push({ path: `${where}.id`, message: `must be "${want.id}"` });
    if (scene.template !== want.template) errors.push({ path: `${where}.template`, message: `must be "${want.template}"` });
    if (want.n) {
      const prefix = chapterTitle(want.n);
      if (typeof scene.chapter !== "string" || !(scene.chapter === prefix || scene.chapter.startsWith(`${prefix} `))) {
        errors.push({ path: `${where}.chapter`, message: `must open the chapter 「${prefix}」, followed by the episode's title` });
      }
    } else if (scene.chapter !== undefined) {
      errors.push({ path: `${where}.chapter`, message: "the outro opens no chapter: a compilation has one chapter per episode" });
    }
    for (const [lineIndex, line] of (Array.isArray(scene.lines) ? scene.lines : []).entries()) {
      if (!isObject(line)) continue;
      for (const key of ["speaker", "emotion", "reveal"]) {
        if (line[key] !== undefined) errors.push({ path: `${where}.lines[${lineIndex}].${key}`, message: "a card of a compilation has no speaker, emotion or reveal: nothing is narrated" });
      }
    }
  });
}

/**
 * Where everything sits on the 30 fps grid. `episodes` is [{ slug, frames, file?, sha256? }] in
 * play order; the result is [{ kind: "card" | "episode" | "outro", id, slug?, episode?, start_frame,
 * frames, file?, sha256? }], a card before its episode and the outro last. `episode` is the
 * episode's number in the series.
 */
export function compilationLayout(doc, episodes) {
  const spec = doc.compilation;
  const order = episodes.map((episode) => episode.slug);
  if (JSON.stringify(order) !== JSON.stringify(spec.episodes)) throw new Error(`the episodes ${order.join(", ")} are not compilation.episodes in order`);
  const numbers = episodeNumbers(spec);
  const layout = [];
  let frame = 0;
  episodes.forEach((episode, index) => {
    const n = numbers[index];
    if (spec.chapter_cards ?? true) {
      layout.push({ kind: "card", id: cardId(n), slug: episode.slug, episode: n, start_frame: frame, frames: CARD_FRAMES });
      frame += CARD_FRAMES;
    }
    if (!Number.isInteger(episode.frames) || episode.frames <= 0) throw new Error(`episode ${episode.slug} has no frame count`);
    layout.push({ kind: "episode", id: episode.slug, slug: episode.slug, episode: n, start_frame: frame, frames: episode.frames, ...(episode.file ? { file: episode.file } : {}), ...(episode.sha256 ? { sha256: episode.sha256 } : {}) });
    frame += episode.frames;
  });
  if (spec.outro ?? true) layout.push({ kind: "outro", id: OUTRO_ID, start_frame: frame, frames: OUTRO_FRAMES });
  return layout;
}

export function totalFrames(layout) {
  const last = layout.at(-1);
  return last ? last.start_frame + last.frames : 0;
}

/**
 * What a compilation was made from: the cuts, by hash, and whether cards and an outro were
 * laid between them. The cards' pictures are the visual hash's business (frames/manifest.json,
 * and checks.json keeps both), so a title edit re-renders and re-joins, and an episode re-cut
 * after its approval voids the compilation.
 */
export function compilationHash(doc, episodes) {
  return hash16(["compilation", episodes.map((episode) => [episode.slug, episode.sha256]), doc.compilation.chapter_cards ?? true, doc.compilation.outro ?? true]);
}

/**
 * One chapter per episode, starting at its card when there is one (so the first chapter is at
 * 00:00 either way and the card belongs to the chapter a viewer clicks). `titles` maps an
 * episode slug to its title. `scene` is the episode's slug: a translation's `chapters` keys on
 * it, whether or not the cards are drawn; `card` names the card when there is one.
 */
export function chapterList(layout, titles = {}) {
  const chapters = [];
  const seen = new Set();
  for (const entry of layout) {
    if (entry.kind === "outro" || seen.has(entry.slug)) continue;
    seen.add(entry.slug);
    chapters.push({
      episode: entry.episode,
      slug: entry.slug,
      scene: entry.slug,
      card: entry.kind === "card" ? entry.id : null,
      start_frame: entry.start_frame,
      at: Math.floor(entry.start_frame / FPS),
      title: chapterTitle(entry.episode, titles[entry.slug]),
    });
  }
  return chapters;
}

/**
 * A timeline-shaped object for the stages that read one (chapterText, composeMetadata, the
 * review pages): the chapters and the length, no scenes or lines, no speech.
 */
export function compilationTimeline(layout, titles = {}) {
  return {
    fps: FPS,
    sample_rate: SAMPLE_RATE,
    total_frames: totalFrames(layout),
    scenes: [],
    lines: [],
    chapters: chapterList(layout, titles).map(({ title, scene, start_frame, episode }) => ({ title, scene, start_frame, episode })),
    speech_hash: null,
  };
}

/** The timeline lint and qa reason about before the cuts are measured: every episode ESTIMATED_EPISODE_FRAMES long. */
export function estimatedCompilationTimeline(doc) {
  return compilationTimeline(compilationLayout(doc, doc.compilation.episodes.map((slug) => ({ slug, frames: ESTIMATED_EPISODE_FRAMES }))), doc.compilation.titles ?? {});
}

/** Whether checks.json describes the join of these very cuts and these very cards. `episodes` is [{ slug, sha256 }]. */
export function compilationChecksCurrent(doc, checks, episodes) {
  if (!checks?.ok || !episodes.length || episodes.some((episode) => typeof episode.sha256 !== "string")) return false;
  return checks.compilation_hash === compilationHash(doc, episodes) && checks.visual_hash === visualHash(doc);
}

export function shiftCues(cues, offsetMs) {
  return cues.map((cue) => ({ ...cue, start_ms: Math.round(cue.start_ms + offsetMs), end_ms: Math.round(cue.end_ms + offsetMs) }));
}

/**
 * The episodes' caption files as one track: each file's cues moved to where its episode starts.
 * `perEpisode` is [{ srt, offsetMs }] in play order. An episode's cues end inside its own
 * length (captions never outlive their line), so the merged track never overlaps at a seam.
 */
export function mergeCaptions(perEpisode) {
  return perEpisode.flatMap(({ srt, offsetMs }) => shiftCues(parseSrt(srt), offsetMs));
}

/**
 * The chapter titles a description can afford. YouTube's description holds 5,000 bytes; eighty
 * chapters with full titles pass that, so when the composed description would, every chapter
 * falls back to 「第 N 集」 (in the locale's words). `titles` is the locale's own chapter titles
 * keyed by scene, as composeDescription takes them. Returns { titles, description, shortened }.
 */
export function descriptionWithinBudget(body, timeline, titles = {}, { locale = "zh-TW", sources = [], tags = [], article = null } = {}) {
  const compose = (chapterTitles) => composeDescription({ body, timeline, chapterTitles, article, sources, locale, tags });
  const overBudget = (description) => checkYoutubeFields({ title: "", description, tags: [] }).length > 0;
  const full = compose(titles);
  if (!overBudget(full)) return { titles, description: full, shortened: false };
  // The episode's number in the series, as its card says it, not its position: a skipped episode leaves a gap.
  const short = Object.fromEntries((timeline.chapters ?? []).map((chapter, index) => [chapter.scene, episodeLabel(chapter.episode ?? index + 1, locale)]));
  return { titles: short, description: compose(short), shortened: true };
}

/**
 * Lint for a compilation, in lintVideo's shape ({ errors, warnings, summary }). The narration
 * rules do not apply (no lexicon, no brief, no shot lengths); what remains is the structure, the
 * YouTube limits with the chapters estimated, and the translations' currency. The placeholder
 * title is allowed: the worker makes the project before the planner names it, and status waits.
 */
export function lintCompilation(doc, context = {}) {
  const errors = validateVideo(doc);
  const warnings = [];
  if (errors.length) return { errors, warnings, summary: null };
  const error = (path, message) => errors.push({ path, message });
  const warn = (path, message) => warnings.push({ path, message });
  const spec = doc.compilation;
  const timeline = estimatedCompilationTimeline(doc);
  const budget = descriptionWithinBudget(doc.youtube.description, timeline, {}, { sources: doc.sources ?? [], tags: doc.youtube.tags });
  for (const problem of checkYoutubeFields({ title: doc.youtube.title, description: budget.description, tags: doc.youtube.tags })) error("youtube", problem);
  if (budget.shortened) warn("youtube.description", `with every chapter titled the description would pass ${DESCRIPTION_MAX_BYTES} bytes, so the chapters fall back to 「第 N 集」`);
  if (doc.youtube.title === PLACEHOLDER_TITLE) warn("youtube.title", "still the placeholder; the worker plans the title, description and thumbnail first");
  if (!doc.thumbnail) warn("thumbnail", "no thumbnail yet: the worker adds one on an episode keyframe with the planned metadata");
  const untitled = spec.episodes.filter((slug) => !isText(spec.titles?.[slug]));
  if (untitled.length) warn("compilation.titles", `${untitled.length} episodes have no chapter title, so their chapters read 「第 N 集」: ${untitled.join(", ")}`);
  // A compilation's translated chapters key on the episode slugs, not on the card scenes, so
  // only the three fields go through metadataStatus.
  for (const [locale, translation] of Object.entries(context.translations ?? {})) {
    const state = { ...metadataStatus(doc, translation), chapters: {} };
    const absent = namedWith(state, "missing");
    const older = namedWith(state, "stale");
    const untranslatedChapters = spec.episodes.filter((slug) => !isText(translation?.chapters?.[slug]));
    if (absent.length) warn(`i18n/${locale}.json`, `not translated: ${absent.join(", ")}`);
    if (older.length) warn(`i18n/${locale}.json`, `translations older than the zh-TW text: ${older.join(", ")}`);
    if (untranslatedChapters.length) warn(`i18n/${locale}.json`, `${untranslatedChapters.length} chapters without a translated title (keyed by episode slug): ${untranslatedChapters.join(", ")}`);
  }
  return { errors, warnings, summary: null };
}
