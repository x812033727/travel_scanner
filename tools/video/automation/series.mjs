// A long drama series on the host (docs/videos/SERIES.md): the worker plans the series' documents
// and starts its episodes in the order the site says. The site decides what is next
// (GET automation/series/next): the setting book, the whole-series outline, one chapter's
// detailed outline, or the next ready episode. A document is planned by the planner stage under a
// variant of its prompt and filed on the site as a new version that waits for the owner; sent
// back with a note, it is rewritten from that note while the site allows rewrites. An episode is
// started on the site under the video's slug, then drafted here from the chapter's beats: no
// outline options, the owner already approved the chapter. A one-off drama is a series of one
// episode whose only document is its story bible (docs/videos/DRAMA-FLOW.md, section 2).
import path from "node:path";

import { hasAnimePolicy, isLongAnime, isClosedAnimeFinale, validateAnimePolicy } from "../core/anime-policy.mjs";
import { EXPLAINER_PRESET, shotLooksProblem } from "../core/drama.mjs";
import { eachLine } from "../core/schema.mjs";
import { estimateTimeline, framesFor, frameToSeconds } from "../core/timeline.mjs";
import { AutomationError, OUTPUT_INVALID } from "./client.mjs";
import { BEATS, GENRE_SPECS, HOOK_TYPES, LEAD_ARCS, MIN_SATISFACTION } from "./prompts.mjs";
import { startStory } from "./story.mjs";

export const DOC_KINDS = ["setting", "outline", "chapter", "bible"];
const BIBLE_LISTS = ["acts"];
const ANSWER_ATTEMPTS = 2;
const CHARACTER_KEYS = ["id", "name", "appearance"];
const BEAT_FIELDS = ["hook", "conflict", "turn", "cliffhanger"];
// The hands-off rules of a binge series (docs/videos/BINGE.md), the same the site applies
// (apps/api/app/video_automation/judge.py): a planned document's verdicts by kind, and the
// screenplay's coverage and measured timing. Checked here first so a failing document is
// rewritten and a failing screenplay fixed before anything is filed or sent.
export const REQUIRED_VERDICTS = {
  setting: ["originality", "conflict_engine", "genre_fit", "cast_playable"],
  outline: ["originality", "escalation", "midpoint_reveal", "chapter_turns", "satisfaction_schedule"],
  chapter: ["originality", "tension_rules", "hooks", "satisfaction", "alternation", "escalation"],
};
export const VERDICT_VALUES = ["有", "弱", "無"];
export const COVERAGE_BEATS = ["hook", "conflict", "turn", "cliffhanger"];
export const MAX_WEAK_VERDICTS = 1;
export const HOOK_MAX_SECONDS = 8;
export const FIRST_SATISFACTION_MAX_SECONDS = 30;

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;

/** Whether a series is a one-off drama: one episode, one story bible (docs/videos/DRAMA-FLOW.md, section 2). */
export const isOneOff = (series) => series?.kind === "one-off";
/**
 * Whether a one-off is an illustrated explainer (docs/videos/so-thats-why/): the owner picked the
 * flat-explainer preset, so its bible is a question's, with no cast.
 */
export const isExplainerOneOff = (series) => isOneOff(series) && series?.style_preset === EXPLAINER_PRESET;
/** The planner prompt of a document: its kind, or the explainer's bible. */
export const documentVariant = (kind, series) => (kind === "bible" && isExplainerOneOff(series) ? "bible-explainer" : kind);
/** Whether a series' genre carries the retention rules (the classic xianxia series does not). */
export const retentionRequired = (series) => !hasAnimePolicy(series) && Boolean(GENRE_SPECS[series?.genre]?.retention);

/** The video slug of an episode: the series' slug and the number, zero-padded (xianxia-e001). */
export const episodeSlug = (seriesSlug, number) => `${seriesSlug}-e${String(number).padStart(3, "0")}`;

/** The chapter's first and last episode numbers, as the site cuts them. */
export function chapterRange(series, chapter) {
  const size = series.episodes_per_chapter;
  return [(chapter - 1) * size + 1, Math.min(chapter * size, series.planned_episodes)];
}

/**
 * Why a planner's answer cannot be filed as this document, or null. The same shapes the site
 * checks (apps/api/app/video_automation/series.py doc_problem), checked here first so a bad
 * answer costs one more model call, not a refused upload.
 */
export function documentProblem(kind, answer, job) {
  if (!isObject(answer)) return "the answer is not an object";
  if (!isText(answer.body_md)) return "body_md (the document as the owner reads it) is missing";
  if (!isObject(answer.body_json)) return "body_json (the structured document) is missing";
  const body = answer.body_json;
  const series = job.series;
  if (hasAnimePolicy(series)) {
    const problems = validateAnimePolicy(series);
    if (problems.length) return problems.join("; ");
  }
  if (kind === "bible" && isExplainerOneOff(series)) {
    // An explainer's bible (apps/api/app/video_automation/series.py doc_problem): no cast, the
    // question, its answer and reasons, and the one outline the episode is written from.
    if (!Array.isArray(body.characters) || body.characters.length) return "body_json.characters must be empty: an explainer has no cast";
    for (const key of BIBLE_LISTS) if (!Array.isArray(body[key]) || !body[key].length) return `body_json.${key} must list the ${key}`;
    const outline = body.outline;
    if (!isObject(outline)) return "body_json.outline must be the one outline (an object)";
    for (const key of ["question", "answer", "hook"]) if (!isText(outline[key])) return `body_json.outline.${key} is missing`;
    if (!Array.isArray(outline.reasons) || outline.reasons.length < 2 || !outline.reasons.every(isText)) return "body_json.outline.reasons must list the reasons";
    if (!Array.isArray(outline.sources) || !outline.sources.length || !outline.sources.every((url) => /^https:\/\//.test(url))) return "body_json.outline.sources must list the https pages the facts rest on";
    return null;
  }
  if (kind === "setting" || kind === "bible") {
    if (!Array.isArray(body.characters) || !body.characters.length) return "body_json.characters must list the cast";
    for (const character of body.characters) {
      if (!isObject(character) || !CHARACTER_KEYS.every((key) => isText(character[key]))) return "every character needs id, name and appearance";
      if (!/^[a-z][a-z0-9-]{1,23}$/.test(character.id)) return `character id "${character.id}" must be lowercase ascii, 2 to 24 characters`;
      const looks = looksProblem(character, series);
      if (looks) return looks;
      const shotLooks = shotLooksProblem(character);
      if (shotLooks) return `character ${character.id}: ${shotLooks}`;
    }
    if (kind === "bible") {
      // The one-off's story bible (apps/api/app/video_automation/series.py doc_problem): the
      // acts, and the one outline the episode is written from.
      for (const key of BIBLE_LISTS) if (!Array.isArray(body[key]) || !body[key].length) return `body_json.${key} must list the ${key}`;
      if (!isObject(body.outline)) return "body_json.outline must be the one outline (an object)";
      return null;
    }
    if (!Array.isArray(body.mysteries) || !body.mysteries.length) return "body_json.mysteries must list the long-running mysteries";
    return null;
  }
  if (kind === "outline") {
    if (!Array.isArray(body.chapters) || body.chapters.length !== series.chapters) return `body_json.chapters must list exactly ${series.chapters} chapters`;
    const numbers = [];
    for (const chapter of body.chapters) {
      if (!isObject(chapter) || !isText(chapter.title) || !Array.isArray(chapter.episodes)) return "every chapter needs a title and an episodes list";
      for (const episode of chapter.episodes) {
        if (!isObject(episode) || !Number.isInteger(episode.number) || !isText(episode.title) || !isText(episode.logline)) return "every episode needs a number, a title and a logline";
        numbers.push(episode.number);
      }
    }
    const expected = Array.from({ length: series.planned_episodes }, (_, index) => index + 1);
    if (JSON.stringify([...numbers].sort((a, b) => a - b)) !== JSON.stringify(expected)) return `the episodes must be numbered 1 to ${series.planned_episodes}, each once`;
    return null;
  }
  const [first, last] = chapterRange(series, job.chapter_number);
  if (!Array.isArray(body.episodes)) return "body_json.episodes must list the chapter's episodes";
  const numbers = [];
  for (const episode of body.episodes) {
    if (!isObject(episode) || !Number.isInteger(episode.number)) return "every episode needs a number";
    const missing = BEAT_FIELDS.filter((key) => !(isText(episode[key]) || (key === "cliffhanger" && isObject(episode[key]) && isText(episode[key].text))));
    if (missing.length) return `episode ${episode.number} lacks ${missing.join(", ")}`;
    if (!Array.isArray(episode.tension) || episode.tension.length !== 5 || episode.tension.some((value) => !Number.isInteger(value) || value < 1 || value > 5)) return `episode ${episode.number} needs tension: five scores from 1 to 5`;
    if (episode.tension.at(-1) < 4 && !isClosedAnimeFinale(series, episode.number, episode)) return `episode ${episode.number} must end tense (tension[4] >= 4)`;
    numbers.push(episode.number);
  }
  const expected = Array.from({ length: last - first + 1 }, (_, index) => first + index);
  if (JSON.stringify([...numbers].sort((a, b) => a - b)) !== JSON.stringify(expected)) return `chapter ${job.chapter_number} covers episodes ${first} to ${last}`;
  for (let index = 1; index < body.episodes.length; index++) {
    const before = body.episodes[index - 1].cliffhanger?.type;
    const now = body.episodes[index].cliffhanger?.type;
    if (before && now && before === now) return `episodes ${body.episodes[index - 1].number} and ${body.episodes[index].number} end on the same kind of cliffhanger (${now}); vary them`;
  }
  if (isLongAnime(series)) return animeNarrativeProblem(series, body.episodes, job.context?.episodes ?? []);
  if (retentionRequired(series)) return retentionProblem(series, body.episodes);
  return null;
}

/** Source-native tension and consequences; these do not substitute wins for an ensemble's losses. */
export function animeNarrativeProblem(series, episodes, previous = []) {
  for (const episode of episodes) {
    const who = `episode ${episode.number}`;
    if (typeof episode.closed_ending !== "boolean") return `${who}: closed_ending must be boolean`;
    if (!Number.isInteger(episode.number) || episode.number < 1 || episode.number > series.planned_episodes) return `${who} is outside the series`;
    for (const key of ["title", "logline", "hook", "conflict", "turn", "theme"]) if (!isText(episode[key])) return `${who} needs ${key}`;
    if (!Array.isArray(episode.tension) || episode.tension.length !== 5 || episode.tension.some((score) => !Number.isInteger(score) || score < 1 || score > 5)) return `${who} needs five integer tension scores from 1 to 5`;
    if (!isObject(episode.cliffhanger) || !isText(episode.cliffhanger.text) || !["danger", "reveal", "choice", "reversal", "emotion"].includes(episode.cliffhanger.type)) return `${who} needs a valid ending`;
    const finale = isClosedAnimeFinale(series, episode.number, episode);
    if (series.open_ended === false && episode.number === series.planned_episodes && !finale) return `${who}: the closed series must declare its final resolution`;
    if (finale && (episode.tension.at(-1) > 3 || episode.cliffhanger.type !== "emotion")) return `${who}: quiet final resolution ends with emotion and tension 1 to 3`;
    if (!finale && episode.tension.at(-1) < 4) return `${who} must end tense`;
    if (episode.closed_ending === true && !isClosedAnimeFinale(series, episode.number, episode)) return `${who}: only the planned closed finale may declare closed_ending`;
    if (!Array.isArray(episode.high_tension) || episode.high_tension.length !== 2) return `${who} needs two high_tension events`;
    for (const [index, beat] of episode.high_tension.entries()) {
      if (!isObject(beat) || beat.beat !== ["first_half", "second_half"][index] || !["event", "stakes", "consequence"].every((key) => isText(beat[key]))) return `${who}: high_tension needs beat, event, stakes and consequence`;
    }
    if (new Set(episode.high_tension.map((beat) => beat.beat)).size !== 2 || new Set(episode.high_tension.map((beat) => beat.event.trim())).size !== 2) return `${who}: high_tension events must be distinct and span both halves`;
    if (!isText(episode.consequence)) return `${who} needs a lasting consequence`;
    if (!isObject(episode.state) || !["time", "knowledge", "character_state", "evidence", "carry_forward"].every((key) => isText(episode.state[key]))) return `${who} needs complete source state`;
    for (const key of ["setups", "payoffs", "general_payoffs", "characters", "locations"]) {
      if (!Array.isArray(episode[key]) || (["characters", "locations"].includes(key) && !episode[key].length) || !episode[key].every(isText) || new Set(episode[key]).size !== episode[key].length) return `${who}: ${key} must contain unique nonempty text`;
    }
  }
  const earlier = previous.filter((row) => Number.isInteger(row?.number) && row.number < episodes[0]?.number).sort((a, b) => a.number - b.number).slice(-3);
  for (const row of earlier) {
    if (animeNarrativeProblem(series, [{ ...(row.beats ?? row), number: row.number }])) return "previous chapter has invalid long-anime continuity data";
  }
  const rows = new Map(earlier.map((row) => [row.number, { ...(row.beats ?? row), number: row.number }]));
  for (const episode of episodes) rows.set(episode.number, episode);
  const ordered = [...rows.entries()].sort(([a], [b]) => a - b);
  for (let index = 1; index < ordered.length; index++) {
    if (ordered[index][0] - ordered[index - 1][0] === 1 && ordered[index][1].cliffhanger?.type === ordered[index - 1][1].cliffhanger?.type) return `episodes ${ordered[index - 1][0]} and ${ordered[index][0]} must vary their ending types`;
  }
  for (let start = 0; start + 4 <= ordered.length; start++) {
    const window = ordered.slice(start, start + 4);
    if (window.at(-1)[0] - window[0][0] !== 3) continue;
    if (!window.some(([, row]) => (row.payoffs?.length ?? 0) + (row.general_payoffs?.length ?? 0) > 0)) return `episodes ${window[0][0]} to ${window.at(-1)[0]} need a meaningful local payoff`;
  }
  return null;
}

export const ANIME_REQUIRED_VERDICTS = {
  setting: REQUIRED_VERDICTS.setting,
  outline: ["originality", "escalation", "midpoint_reveal", "chapter_turns", "payoff_schedule"],
  chapter: ["originality", "tension_rules", "hooks", "high_tension", "consequences", "escalation"],
};
const verdictKeys = (kind, series) => (isLongAnime(series) ? ANIME_REQUIRED_VERDICTS : REQUIRED_VERDICTS)[kind] ?? [];

/**
 * Why a chapter outline breaks the retention rules (docs/videos/BINGE.md), or null: every
 * episode names its hook type, the lead's arc and at least MIN_SATISFACTION satisfaction beats
 * of the genre's types, the first inside the first half; two episodes in a row never leave the
 * lead only suffering; any four in a row pay something off. The site refuses the same.
 */
export function retentionProblem(series, episodes) {
  const allowed = new Set(GENRE_SPECS[series?.genre]?.satisfactions ?? []);
  const ordered = [...episodes].filter((episode) => Number.isInteger(episode?.number)).sort((a, b) => a.number - b.number);
  for (const episode of ordered) {
    if (!HOOK_TYPES.includes(episode.hook_type)) return `episode ${episode.number} needs hook_type: one of ${HOOK_TYPES.join(", ")}`;
    if (!LEAD_ARCS.includes(episode.lead_arc)) return `episode ${episode.number} needs lead_arc: one of ${LEAD_ARCS.join(", ")}`;
    const beats = episode.satisfaction;
    if (!Array.isArray(beats) || beats.length < MIN_SATISFACTION) return `episode ${episode.number} needs at least ${MIN_SATISFACTION} satisfaction beats`;
    for (const beat of beats) {
      if (!isObject(beat) || !BEATS.includes(beat.beat) || !allowed.has(beat.type)) return `episode ${episode.number}: every satisfaction beat is {beat: one of ${BEATS.join(", ")}, type: one of the genre's types}`;
    }
    if (!["opening", "first_half"].includes(beats[0].beat)) return `episode ${episode.number}: the first satisfaction beat must land in the first half`;
  }
  for (let index = 1; index < ordered.length; index++) {
    if (ordered[index - 1].lead_arc === "suffers" && ordered[index].lead_arc === "suffers") return `episodes ${ordered[index - 1].number} and ${ordered[index].number} both leave the lead suffering; give one of them a win`;
  }
  for (let start = 0; start + 4 <= ordered.length; start++) {
    const window = ordered.slice(start, start + 4);
    if (!window.some((episode) => Array.isArray(episode.payoffs) && episode.payoffs.length)) return `episodes ${window[0].number} to ${window[3].number} pay nothing off; every four in a row must pay off at least one thread`;
  }
  return null;
}

/** Why a checker's verdict on a document cannot be filed as one, or null. */
export function verdictProblem(verdict, kind, series = null) {
  if (!isObject(verdict) || !isObject(verdict.verdicts)) return "the verdict has no verdicts object";
  const required = verdictKeys(kind, series);
  const missing = required.filter((key) => !VERDICT_VALUES.includes(verdict.verdicts[key]));
  if (missing.length) return `the verdict lacks ${missing.join(", ")} (each 有, 弱 or 無)`;
  if (!Array.isArray(verdict.problems) || !Array.isArray(verdict.similar_works)) return "the verdict needs problems and similar_works lists";
  return null;
}

/** The verdict as the site reads it: the required keys, the lists, one line of notes. */
export function verdictFor(verdict, kind, series = null) {
  const keys = verdictKeys(kind, series);
  return {
    verdicts: Object.fromEntries(keys.map((key) => [key, verdict.verdicts[key]])),
    problems: verdict.problems.map((item) => String(item)).filter((item) => item.trim()),
    similar_works: verdict.similar_works.map((item) => String(item)).filter((item) => item.trim()),
    notes: typeof verdict.notes === "string" ? verdict.notes.slice(0, 400) : "",
  };
}

/** Whether a verdict passes the site's rule (mirrored here so the report line can say so). */
export function verdictPasses(verdict, kind, series = null) {
  const keys = verdictKeys(kind, series);
  const values = keys.map((key) => verdict.verdicts?.[key]);
  if (values.some((value) => value !== "有" && value !== "弱")) return false;
  if (values.filter((value) => value === "弱").length > MAX_WEAK_VERDICTS) return false;
  return verdict.problems.length === 0 && verdict.similar_works.length === 0;
}

/**
 * The retention numbers of a screenplay, measured on its estimated timeline (250 characters a
 * minute) from the lines the checker named, never taken from the model: how many seconds in
 * the hook ends, when each satisfaction line starts, and whether the cliffhanger line is the
 * last thing said. Null when the checker named none.
 */
export function retentionNumbers(video, retention) {
  if (!isObject(retention)) return null;
  const timeline = estimateTimeline(video);
  const lines = new Map(timeline.lines.map((line) => [line.id, line]));
  const ids = [...eachLine(video)].map(({ line }) => line.id);
  const hook = lines.get(retention.hook_line);
  const satisfaction = (Array.isArray(retention.satisfaction_lines) ? retention.satisfaction_lines : []).map((id) => lines.get(id)).filter(Boolean);
  const positions = satisfaction.map((line) => Number(frameToSeconds(line.start_frame).toFixed(1)));
  return {
    // The hook lands when its words end: the pause after the line and the gap to the next shot
    // are not part of it (a line's end_frame includes both).
    hook_seconds: hook ? Number(frameToSeconds(hook.start_frame + framesFor(hook.audio_samples)).toFixed(1)) : null,
    satisfaction: { count: satisfaction.length, first_seconds: positions.length ? Math.min(...positions) : null, positions },
    cliffhanger_last: Boolean(retention.cliffhanger_line) && ids.at(-1) === retention.cliffhanger_line,
  };
}

/**
 * Whether a screenplay's check passes the site's script rule (docs/videos/BINGE.md), and why
 * not, so a hands-off episode is fixed before it is sent rather than sent to be refused.
 */
export function scriptVerdict(check, series) {
  const problems = [];
  const coverage = isObject(check?.coverage) ? check.coverage : {};
  const required = isLongAnime(series) && isClosedAnimeFinale(series) ? ["hook", "conflict", "turn", "closure"] : COVERAGE_BEATS;
  for (const beat of required) {
    if (!VERDICT_VALUES.includes(coverage[beat])) problems.push(`the checker gave no verdict on the ${beat}`);
    else if (coverage[beat] === "無") problems.push(`the ${beat} is missing from the script`);
  }
  if (required.filter((beat) => coverage[beat] === "弱").length > MAX_WEAK_VERDICTS) problems.push("more than one beat is only weakly delivered");
  for (const problem of check?.problems ?? []) problems.push(String(problem));
  for (const work of check?.similar_works ?? []) problems.push(`resembles an existing work: ${work}`);
  if (isLongAnime(series)) {
    if (!Array.isArray(coverage.high_tension) || coverage.high_tension.length !== 2 || coverage.high_tension.some((value) => value !== "有")) problems.push("both high_tension events must be fully played");
    if (coverage.consequences !== "有") problems.push("lasting consequences must be played");
    if (isClosedAnimeFinale(series) && coverage.closure !== "有") problems.push("the closed finale needs positive closure");
    if (!Array.isArray(check?.continuity_problems)) problems.push("the checker needs continuity_problems");
    else problems.push(...check.continuity_problems.map(String));
  }
  if (retentionRequired(series)) {
    if (!["有", "弱"].includes(coverage.satisfaction)) problems.push("the satisfaction beats are not played");
    const retention = check?.retention;
    if (!isObject(retention)) problems.push("the checker named no hook, satisfaction or cliffhanger lines");
    else {
      // The site reads these as numbers and refuses a null (a hook_line that is not in the
      // script measures as null), so a missing number is a problem here too, not a pass.
      const hook = retention.hook_seconds;
      const count = retention.satisfaction?.count;
      const first = retention.satisfaction?.first_seconds;
      if (typeof hook !== "number") problems.push("the checker's hook_line is not a line of the script: name the first line's id");
      else if (hook > HOOK_MAX_SECONDS) problems.push(`the hook line ends at ${hook} s; shorten it (or move what follows into the next line) so its words end inside ${HOOK_MAX_SECONDS} s`);
      if (typeof count !== "number" || count < MIN_SATISFACTION) problems.push(`only ${typeof count === "number" ? count : 0} satisfaction beats are played; at least ${MIN_SATISFACTION}`);
      if (typeof first !== "number") problems.push("the checker's satisfaction_lines are not lines of the script: name their ids");
      else if (first > FIRST_SATISFACTION_MAX_SECONDS) problems.push(`the first satisfaction beat starts at ${first} s; it must land inside ${FIRST_SATISFACTION_MAX_SECONDS} s`);
      if (retention.cliffhanger_last !== true) problems.push("the cliffhanger is not the last line: cut everything after it");
    }
  }
  return { passed: problems.length === 0, problems };
}

/**
 * A character's looks (docs/videos/SERIES.md, 換裝與變化): `looks: [{ id, from, to?, appearance,
 * sheet_prompt?, voice_style? }]` on the character in the setting book. A look covers episodes
 * `from` to `to` (to the series' end without `to`) and, in those episodes, stands in for the
 * book's appearance (and sheet prompt and voice style, when it has its own): the image prompts
 * take it word for word, so it is the whole look, not a change to the base one.
 */
const LOOK_ID = /^[a-z][a-z0-9-]{1,23}$/;
const lastEpisodeOf = (look) => (look.to === undefined || look.to === null ? Infinity : look.to);
const usableLook = (look) => isObject(look) && isText(look.appearance) && Number.isInteger(look.from) && (look.to === undefined || look.to === null || Number.isInteger(look.to));

/** Why a character's looks cannot be filed, or null. A character without looks has nothing to check. */
export function looksProblem(character, series = null) {
  if (character.looks === undefined) return null;
  const who = `character ${character.id}`;
  if (!Array.isArray(character.looks)) return `${who}: looks must be a list`;
  const seen = new Set();
  for (const look of character.looks) {
    if (!isObject(look) || !isText(look.id) || !isText(look.appearance)) return `${who}: every look needs an id and an appearance`;
    const where = `${who}, look ${look.id}`;
    if (!LOOK_ID.test(look.id)) return `${where}: the id must be lowercase ascii, 2 to 24 characters`;
    if (seen.has(look.id)) return `${who}: two looks are called ${look.id}`;
    seen.add(look.id);
    if (!Number.isInteger(look.from) || look.from < 1) return `${where}: from must be the number of the first episode it covers`;
    if (look.to !== undefined && look.to !== null && (!Number.isInteger(look.to) || look.to < look.from)) return `${where}: to must be the number of the last episode it covers, not before from (leave it out to cover the rest of the series)`;
    if (Number.isInteger(series?.planned_episodes) && look.from > series.planned_episodes) return `${where}: from ${look.from} is after the last episode (${series.planned_episodes})`;
    for (const key of ["sheet_prompt", "voice_style"]) if (look[key] !== undefined && !isText(look[key])) return `${where}: ${key} must be text when it is given`;
    if (look.voice_style !== undefined && character.voice?.provider !== "gemini") return `${where}: voice_style needs the character's own Gemini voice`;
  }
  const ordered = [...character.looks].sort((a, b) => a.from - b.from);
  for (let index = 1; index < ordered.length; index++) {
    if (ordered[index].from <= lastEpisodeOf(ordered[index - 1])) return `${who}: looks ${ordered[index - 1].id} and ${ordered[index].id} both cover episode ${ordered[index].from}; one look per episode`;
  }
  return null;
}

/** The look a character wears in an episode, or null for the setting book's own appearance. */
export function lookFor(character, episode) {
  if (!Number.isInteger(episode) || !Array.isArray(character?.looks)) return null;
  return character.looks.find((look) => usableLook(look) && look.from <= episode && episode <= lastEpisodeOf(look)) ?? null;
}

/**
 * The cast as video.json wants it, from the setting book, by id. Given the episode, a character
 * with a look covering it takes the look's appearance, sheet prompt and voice style; everything
 * downstream (the sheet and shot prompts, the series' sheet store, the narration) reads these.
 */
export function castFrom(setting, episode = null) {
  const characters = Array.isArray(setting?.characters) ? setting.characters : [];
  return characters
    .filter((character) => isObject(character) && isText(character.id))
    .map((character) => {
      const look = lookFor(character, episode);
      const entry = { id: character.id, name: String(character.name ?? character.id), appearance: String(look?.appearance ?? character.appearance ?? "").slice(0, 800) };
      if (Array.isArray(character.shot_looks)) entry.shot_looks = character.shot_looks.map(({ id, appearance }) => ({ id, appearance }));
      if (isObject(character.voice) && isText(character.voice.provider) && isText(character.voice.name)) {
        const style = isText(look?.voice_style) && character.voice.provider === "gemini" ? look.voice_style : character.voice.style;
        entry.voice = { provider: character.voice.provider, name: character.voice.name, ...(isText(style) ? { style: style.slice(0, 400) } : {}) };
      }
      const sheetPrompt = isText(look?.sheet_prompt) ? look.sheet_prompt : character.sheet_prompt;
      if (isText(sheetPrompt)) entry.sheet_prompt = sheetPrompt.slice(0, 600);
      return entry;
    })
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

/**
 * An episode's brief.md, written from the chapter's row: the sections lint wants, and one outline
 * option, since the owner approved the chapter (no outline to pick).
 */
/**
 * An explainer's brief (docs/videos/so-thats-why/), from its approved bible's outline: the
 * sections lint wants for the flat-explainer preset, and the one outline as option A.
 */
function explainerBrief(series, episode, beats) {
  const reasons = Array.isArray(beats.reasons) ? beats.reasons : [];
  return [
    `# ${beats.question || episode.title || series.title}`,
    "",
    "## 問題",
    beats.question || series.premise,
    "",
    "## 一句答案",
    beats.answer || episode.logline || "",
    "",
    "## 站主觀點",
    series.note || "依頻道立場；沒有站主的親身經驗。",
    "",
    "## 原因",
    ...reasons.map((reason) => `- ${reason}`),
    "",
    "## 大綱",
    "",
    `### 選項 A：${episode.title || beats.question || series.title}`,
    `一行說明：${beats.answer || episode.logline || ""}`,
    `開場鉤子：「${beats.hook ?? ""}」`,
    ...(beats.closing ? [`結尾：${beats.closing}`] : []),
    "",
    "## 素材",
    ...(Array.isArray(beats.sources) ? beats.sources.map((url) => `- ${url}`) : []),
    "",
  ].join("\n");
}

export function episodeBrief(series, episode, cast, beats) {
  if (isExplainerOneOff(series)) return explainerBrief(series, episode, beats);
  const cliff = beats.cliffhanger && typeof beats.cliffhanger === "object" ? `${beats.cliffhanger.text ?? ""}（${beats.cliffhanger.type ?? ""}）` : String(beats.cliffhanger ?? "");
  const listed = (value) => (Array.isArray(value) && value.length ? value.join("、") : "無");
  const inFrame = Array.isArray(beats.characters) && beats.characters.length ? cast.filter((character) => beats.characters.includes(character.id)) : cast;
  // A one-off is its own one-episode series: the brief is the story's, not "episode 1 of".
  const oneOff = isOneOff(series);
  return [
    oneOff ? `# ${episode.title || series.title}` : `# ${series.title} 第 ${episode.number} 集：${episode.title}`,
    "",
    "## 故事前提",
    series.premise,
    "",
    `${oneOff ? "一句話" : "本集"}：${episode.logline || episode.title}`,
    "",
    "## 角色",
    ...(inFrame.length ? inFrame : cast).map((character) => `- ${character.id} ${character.name}：${character.appearance}`),
    "",
    "## 站主觀點",
    series.note || "依頻道立場與作品前提；沒有站主的親身經驗。",
    "",
    "## 幕",
    ...(series.compilation ? ["- 冷開場：第一句就是鉤子，沒有片頭卡；最後一句是懸念，之後沒有任何總結"] : []),
    `- 開場鉤子：${beats.hook ?? ""}${beats.hook_type ? `（${beats.hook_type}）` : ""}`,
    `- 主要衝突：${beats.conflict ?? ""}`,
    `- 轉折：${beats.turn ?? ""}`,
    `- ${isClosedAnimeFinale(series, episode.number, beats) ? "終局收束" : "結尾懸念"}：${cliff}`,
    ...(Array.isArray(beats.satisfaction) && beats.satisfaction.length ? [`- 爽點：${beats.satisfaction.map((beat) => `${beat.beat}｜${beat.type}`).join("、")}`] : []),
    ...(beats.lead_arc ? [`- 主角走向：${beats.lead_arc}`] : []),
    `- 埋下：${listed(beats.setups)}；回收：${listed(beats.payoffs)}`,
    `- 張力曲線：${Array.isArray(beats.tension) ? beats.tension.join("-") : "未定"}`,
    `- 場景：${listed(beats.locations)}`,
    ...(beats.theme ? [`- 主題句：${beats.theme}`] : []),
    "",
    ...(isLongAnime(series) ? ["", "## 原作事件與製作預算", JSON.stringify({ production_policy: series.production_policy, runtime_spec: series.runtime_spec, beats }, null, 2)] : []),
    "## 大綱",
    "",
    `### 選項 A：${episode.title}`,
    `一行說明：${episode.logline || episode.title}`,
    `開場鉤子：「${beats.hook ?? ""}」`,
    "",
  ].join("\n");
}

/** What the planner gets for a document, on top of the drama references. */
export function documentPayload(automation, job, problem = null) {
  const refs = automation.reference();
  const context = job.context ?? {};
  const series = job.series;
  const base = {
    kind: job.kind,
    series: {
      slug: series.slug,
      kind: series.kind ?? "series",
      ...(hasAnimePolicy(series) ? { category: series.category, production_policy: series.production_policy, runtime_spec: series.runtime_spec } : {}),
      title: series.title,
      premise: series.premise,
      aspects: series.aspects,
      tone: series.tone,
      style_preset: series.style_preset,
      target_minutes: series.target_minutes,
      planned_episodes: series.planned_episodes,
      episodes_per_chapter: series.episodes_per_chapter,
      chapters: series.chapters,
      open_ended: series.open_ended,
      note: series.note,
      genre: series.genre ?? "xianxia-bonds",
      lead: series.lead ?? "dual-male",
      visual_tier: series.visual_tier ?? "clips",
      compilation: Boolean(series.compilation),
      hands_off: Boolean(series.hands_off),
      total_minutes: series.total_minutes ?? null,
    },
    genre_spec: isLongAnime(series) ? null : GENRE_SPECS[series.genre] ?? null,
    series_reference: refs.series,
    drama: refs.drama,
    drama_settings: automation.dramaPayload({ style_preset: series.style_preset }).drama_settings,
    ...(job.previous ? { previous: { body_md: job.previous.body_md, body_json: job.previous.body_json, owner_note: job.previous.note ?? "" } } : {}),
    ...(problem ? { previous_problem: problem } : {}),
  };
  if (job.kind === "setting" || job.kind === "bible") return base;
  const setting = context.setting ? { body_md: context.setting.body_md, body_json: context.setting.body_json } : null;
  // Keep the authors' answers and schedule units intact. The API's live mystery state is
  // not a replacement for the approved setting, and missing evidence is not an empty list.
  const publicTextContext = {
    mystery_answers: setting?.body_json?.mysteries ?? null,
    reveal_schedule: context.outline?.body_json?.reveal_schedule ?? null,
  };
  if (job.kind === "outline") {
    return { ...base, setting, ...publicTextContext, chapter_ranges: Array.from({ length: series.chapters }, (_, index) => chapterRange(series, index + 1)) };
  }
  const outline = context.outline?.body_json ?? {};
  const chapter = job.chapter_number;
  const chapters = Array.isArray(outline.chapters) ? outline.chapters : [];
  return {
    ...base,
    setting,
    ...publicTextContext,
    outline: { body_md: context.outline?.body_md ?? "", body_json: outline },
    chapter_number: chapter,
    chapter_range: chapterRange(series, chapter),
    chapter_outline: chapters.find((each) => each?.number === chapter) ?? null,
    previous_chapters: chapters.filter((each) => each?.number < chapter).map(({ number, title, theme, end_state }) => ({ number, title, theme, end_state })),
    recaps: context.recaps ?? [],
    episodes_so_far: (context.episodes ?? []).filter((episode) => episode.number < chapterRange(series, chapter)[0]).map(({ number, title, logline, status }) => ({ number, title, logline, status })),
    mysteries: context.mysteries ?? [],
  };
}

/**
 * The checker's verdict on a planned document (docs/videos/BINGE.md), for a hands-off series:
 * a fresh session reads the document against the series and the approved documents before it.
 * Null when the checker answered nothing usable twice; the document then waits for the owner.
 */
export async function judgeDocument(automation, job, answer) {
  const { series } = job;
  const context = job.context ?? {};
  const payload = {
    kind: job.kind,
    series: documentPayload(automation, job).series,
    genre_spec: isLongAnime(series) ? null : GENRE_SPECS[series.genre] ?? null,
    series_reference: automation.reference().series,
    document: { body_md: answer.body_md, body_json: answer.body_json },
    setting: job.kind !== "setting" && context.setting ? { body_md: context.setting.body_md, body_json: context.setting.body_json } : null,
    outline: job.kind === "chapter" && context.outline ? { body_md: context.outline.body_md, body_json: context.outline.body_json } : null,
    chapter_number: job.kind === "chapter" ? job.chapter_number : null,
  };
  let problem = null;
  for (let attempt = 0; attempt < ANSWER_ATTEMPTS; attempt++) {
    let verdict;
    try {
      verdict = await automation.stage("verifier", `series-${series.slug}`, problem ? { ...payload, previous_problem: problem } : payload, 16_000, "drama", "series-doc", series);
    } catch (error) {
      if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
      problem = error.message;
      continue;
    }
    problem = verdictProblem(verdict, job.kind, series);
    if (!problem) return verdictFor(verdict, job.kind, series);
  }
  automation.log(`  the checker gave no usable verdict on ${job.kind} (${problem}); the document waits for the owner`);
  return null;
}

/** Plan one document with the planner and file it on the site; a line saying what happened. */
export async function planDocument(automation, job) {
  const { series } = job;
  const slug = `series-${series.slug}`;
  let problem = null;
  for (let attempt = 0; attempt < ANSWER_ATTEMPTS; attempt++) {
    let answer;
    try {
      answer = await automation.stage("planner", slug, documentPayload(automation, job, problem), 32_000, "drama", documentVariant(job.kind, series), series);
    } catch (error) {
      if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
      problem = error.message;
      continue;
    }
    problem = documentProblem(job.kind, answer, job);
    if (problem) continue;
    // A hands-off series (docs/videos/BINGE.md): the checker's verdict travels with the
    // document, and the site decides on arrival; a verdict the checker could not give leaves
    // the document for the owner, as on a classic series.
    const judge = series.hands_off ? await judgeDocument(automation, job, answer) : null;
    const doc = await automation.api.seriesDoc(series.slug, {
      kind: job.kind,
      chapter_number: job.kind === "chapter" ? job.chapter_number : 0,
      body_md: answer.body_md.endsWith("\n") ? answer.body_md : `${answer.body_md}\n`,
      body_json: answer.body_json,
      ...(judge ? { judge } : {}),
    });
    const what = documentName(job);
    const made = job.previous ? `rewritten from ${String(job.previous.note ?? "").startsWith("[auto]") ? "the checker's" : "the owner's"} note` : "planned";
    if (doc.status === "approved") return `series ${series.slug}: ${what} ${made} (version ${doc.version}) and approved on the checker's verdict`;
    if (doc.status === "rejected") return `series ${series.slug}: ${what} ${made} (version ${doc.version}); the checker sent it back for a rewrite (${doc.note ?? ""})`;
    if (judge && !verdictPasses(judge, job.kind, series)) return `series ${series.slug}: ${what} ${made} (version ${doc.version}); the rewrites are spent, so it waits for the owner with the checker's problems`;
    return `series ${series.slug}: ${what} ${made} (version ${doc.version}); it waits for the owner on /admin/videos`;
  }
  const kept = automation.keepAnswer(path.join(automation.workBase, "_series", series.slug), job.kind);
  return automation.later(`series ${series.slug}: the planner could not write ${documentName(job)} (${problem}${kept ? `; the answer is in ${kept}` : ""}); the next run tries again`);
}

/** How a document is named in the worker's lines. */
export function documentName({ kind, chapter_number: chapter }) {
  if (kind === "chapter") return `chapter ${chapter}'s outline`;
  if (kind === "setting") return "the setting book";
  if (kind === "bible") return "the story bible";
  return "the series outline";
}

/** Start the next episode on the site and draft it here from the chapter's beats. */
export async function startEpisode(automation, job) {
  const { series, episode } = job;
  if (series.planning_only) throw new AutomationError("planning-only series cannot start production", { code: OUTPUT_INVALID });
  // A brand story (docs/videos/STORY.md) starts under the slug its plan fixed, drafted by story.mjs.
  if (series.kind === "story") return startStory(automation, job);
  const started = await automation.api.episodeStart(series.slug, episode.number, episodeSlug(series.slug, episode.number));
  return automation.draftEpisode(started.request, started.context, started.episode);
}

/**
 * One unit of series work, or null: asked before any one-off request and any scheduled draft,
 * so a series in the making is never starved by them.
 */
export async function seriesStep(automation) {
  if (!automation.settings.drama?.drama_enabled) return null;
  let job;
  try {
    job = await automation.api.seriesNext();
  } catch (error) {
    // A site from before the series route has no such endpoint: there is nothing to do here.
    if (error instanceof AutomationError && error.status === 404) return null;
    throw error;
  }
  if (!job || job.series?.planning_only) return null;
  if (job.kind === "episode") {
    if (!automation.room()) return null;
    return startEpisode(automation, job);
  }
  if (job.kind === "compilation") {
    if (!automation.room()) return null;
    return automation.startCompilation(job);
  }
  return planDocument(automation, job);
}
