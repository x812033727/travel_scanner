// The brand story's own lint rules (docs/videos/STORY.md).
//
// A story is a drama told by the narrator alone over still pictures under slow camera moves,
// about a real brand, object or standard and written from checked sources. What makes it a
// story is its series, not its video.json: lint.mjs applies these rules when series.json beside
// video.json says kind "story". The worker writes that file when it starts the episode, with the
// story's names (the brands, products and real people it is about), which the narration may say
// and no picture may show. The length stays target_minutes' business, as for any video, and the
// longest shot stays drama.mjs's MAX_SHOT_SECONDS; these rules only add what a story needs.
import { isDrama, isShot, NARRATOR, shotVisual } from "./drama.mjs";
import { FPS } from "./timeline.mjs";

export const STORY_KIND = "story";
export const MIN_STORY_SOURCES = 3;
export const STORY_CHAPTERS = { min: 5, max: 7 };
// The reference channel changes the picture about every nine seconds; a story's mean shot is
// held to a band around that, since one shot per sentence reads as a slideshow and a picture
// held for most of a minute reads as a stall.
export const MEAN_SHOT_SECONDS = { min: 5, max: 11 };
// The words that reach the image model: a shot's own fields, and the fields of a character the
// keyframe prompt and the character sheet carry for every shot the character is in.
const SHOT_TEXT = ["prompt", "camera", "negative"];
const CAST_TEXT = ["name", "appearance", "sheet_prompt"];

/**
 * The story's rules, one sentence each, as the worker quotes them to the writer: `id` is what a
 * problem below is about, `level` whether breaking it stops the pipeline (error) or is for the
 * writer to judge (warning).
 */
export const STORY_RULES = [
  { id: "stills", level: "error", rule: 'Every shot scene sets data.visual "still": a story is still pictures under slow camera moves and buys no clip.' },
  { id: "narrator", level: "error", rule: `Every line is the narrator's: no speaker other than "${NARRATOR}". The people in a story are seen, never heard.` },
  { id: "sources", level: "error", rule: `sources lists at least ${MIN_STORY_SOURCES} pages, each an https URL.` },
  { id: "chapters", level: "error", rule: `${STORY_CHAPTERS.min} to ${STORY_CHAPTERS.max} chapters: the hook, the origin, the idea, how the business works, the cost or the turn, where it stands now.` },
  {
    id: "names",
    level: "error",
    rule: "No shot's prompt, camera or negative, and no character's name, appearance or sheet_prompt, contains a name from series.json names (the whole phrase, in any case): the narration may name a brand, a picture may not show one.",
  },
  { id: "pace", level: "warning", rule: `The mean shot on the estimated timeline runs ${MEAN_SHOT_SECONDS.min} to ${MEAN_SHOT_SECONDS.max} s.` },
];

/** Whether series.json (loadProject's `series`) makes this video a brand story. */
export const isStory = (series) => series?.kind === STORY_KIND;

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const escapeRegExp = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const ASCII_WORD = /[A-Za-z0-9]/;

/**
 * A name as a pattern for the whole phrase: any case, any run of white space between its words,
 * and a Latin name never inside a longer word ("Marsh" is not in "marshmallow"); a name in
 * Chinese or Japanese has no spaces to stop at, so it matches wherever it stands.
 */
export function namePattern(name) {
  const phrase = name.trim().split(/\s+/).map(escapeRegExp).join("\\s+");
  const edges = [...name.trim()];
  const before = ASCII_WORD.test(edges[0]) ? "(?<![A-Za-z0-9])" : "";
  const after = ASCII_WORD.test(edges.at(-1)) ? "(?![A-Za-z0-9])" : "";
  return new RegExp(`${before}${phrase}${after}`, "iu");
}

function httpsUrl(value) {
  try {
    return new URL(value).protocol === "https:";
  } catch {
    return false;
  }
}

/**
 * Every story rule the script breaks, on the estimated timeline lint builds:
 * { errors: [{ path, message }], warnings: [...] }, like drama.mjs's shotProblems.
 */
export function storyProblems(doc, series, timeline) {
  const errors = [];
  const warnings = [];
  const error = (path, message) => errors.push({ path, message });
  if (!isDrama(doc)) {
    error("format", 'series.json makes this a story, and a story is a drama: set format "drama"');
    return { errors, warnings };
  }

  const names = [];
  if (series.names !== undefined && !Array.isArray(series.names)) error("series.json", "names must be a list of the story's brand, product and people names");
  for (const name of Array.isArray(series.names) ? series.names : []) {
    if (isText(name) && !names.some((each) => each.name === name.trim())) names.push({ name: name.trim(), pattern: namePattern(name) });
  }
  const named = (text) => (isText(text) ? names.filter((each) => each.pattern.test(text)).map((each) => `"${each.name}"`) : []);
  const noName = (path, text) => {
    const found = named(text);
    if (found.length) error(path, `names ${found.join(", ")}, which series.json lists among the story's names: the narration may say it, a picture may not show it; describe it generically`);
  };

  const shots = [];
  doc.scenes.forEach((scene, index) => {
    const where = `scenes[${index}]`;
    if (isShot(scene)) {
      shots.push(scene);
      if (scene.data?.visual !== "still") error(`${where}.data.visual`, `a story is still pictures only: set visual "still" (a ${shotVisual(scene)} is bought by the second)`);
      for (const key of SHOT_TEXT) noName(`${where}.data.${key}`, scene.data?.[key]);
    }
    scene.lines.forEach((line, lineIndex) => {
      if (line.speaker !== undefined && line.speaker !== NARRATOR) {
        error(`${where}.lines[${lineIndex}] (${line.id}).speaker`, `a story is narrated: every line is the narrator's, and "${line.speaker}" speaks this one`);
      }
    });
  });
  (doc.characters ?? []).forEach((character, index) => {
    for (const key of CAST_TEXT) noName(`characters[${index}].${key}`, character?.[key]);
  });

  const sources = Array.isArray(doc.sources) ? doc.sources : [];
  if (sources.length < MIN_STORY_SOURCES) error("sources", `a story needs at least ${MIN_STORY_SOURCES} sources for its facts; it has ${sources.length}`);
  sources.forEach((source, index) => {
    if (!httpsUrl(source?.url)) error(`sources[${index}].url`, "a story's source is an https URL the checker can open");
  });

  const chapters = doc.scenes.filter((scene) => isText(scene.chapter)).length;
  if (chapters < STORY_CHAPTERS.min || chapters > STORY_CHAPTERS.max) {
    error("scenes", `a story has ${STORY_CHAPTERS.min} to ${STORY_CHAPTERS.max} chapters (the hook, the origin, the idea, the business, the turn, where it stands now); this one has ${chapters}`);
  }

  const seconds = shots
    .map((scene) => timeline.scenes.find((each) => each.id === scene.id))
    .filter(Boolean)
    .map((placed) => (placed.end_frame - placed.start_frame) / FPS);
  if (seconds.length) {
    const mean = seconds.reduce((sum, each) => sum + each, 0) / seconds.length;
    if (mean < MEAN_SHOT_SECONDS.min) warnings.push({ path: "scenes", message: `the mean shot runs about ${mean.toFixed(1)} s; a story holds a picture ${MEAN_SHOT_SECONDS.min} to ${MEAN_SHOT_SECONDS.max} s, so merge some shots` });
    else if (mean > MEAN_SHOT_SECONDS.max) warnings.push({ path: "scenes", message: `the mean shot runs about ${mean.toFixed(1)} s; a story holds a picture ${MEAN_SHOT_SECONDS.min} to ${MEAN_SHOT_SECONDS.max} s, so split some shots` });
  }
  return { errors, warnings };
}
