// Everything that can be checked about a video before any audio or picture exists.
//
// Errors block the pipeline (the CLI exits 1); warnings are for the writer and reviewer to judge.
// The written-language list is the one the recorded route's video_kit.py uses, so a script that
// passes one route's check does not fail the other's.
import { cadenceProblems, HOOK_SECONDS as ILLUSTRATED_HOOK_SECONDS } from "./cadence.mjs";
import { craftProblems } from "./craft.mjs";
import { cueCoverageProblems, emotionProblems, EXPLAINER_PRESET, hasCast, illustrated, isDrama, isShot, isSourced, needsMinimumLength, shotProblems, shotVisual, visualTierProblems } from "./drama.mjs";
import { unknownTermsFor, validateLexicon } from "./lexicon.mjs";
import { articleUrl, checkYoutubeFields, composeDescription, youtubeWarnings } from "./metadata.mjs";
import { DEFAULT_TARGET_MINUTES, LOCALES, MIN_EPISODE_MINUTES, minEpisodeMinutes, eachLine, narrationLocale, spokenText, textHash, validateVideo } from "./schema.mjs";
import { isStory, storyProblems } from "./story.mjs";
import { DEFAULT_CPM, FPS, chapterList, checkChapters, estimateTimeline, formatClock, frameToSeconds, spokenUnits } from "./timeline.mjs";
import { metadataStatus, namedWith } from "./translations.mjs";
import { TEMPLATE_SPECS } from "../templates/templates.mjs";
import { isScreencast, screencastSceneProblems } from "../screencast/steps.mjs";
import { ANIME_BODY_TOLERANCE_SECONDS, hasAnimePolicy, isLongAnime, runtimePolicyHash, validateAnimePolicy } from "./anime-policy.mjs";

// Phrases that only work on a page. Same list as video_kit.py's WRITTEN_ONLY.
export const WRITTEN_ONLY = ["本文", "這篇文章", "如上表", "如下表", "上表", "下表", "綜上所述", "值得注意的是", "筆者", "如圖所示"];
// Narrating how the facts were checked belongs in claims.md, not in the viewer's ear.
export const PROCESS_TALK = ["本影片", "經查證", "根據官方文件", "查核後", "截至查證"];
// The same two lists for an English narration (`narration_locale: "en"`), matched without case.
export const WRITTEN_ONLY_EN = ["as shown above", "as shown below", "in this article", "the table below", "the table above", "as mentioned above"];
export const PROCESS_TALK_EN = ["we verified", "according to the official documentation", "as of our check", "we checked"];
// The two brief sections the monetization policy makes mandatory (docs/videos/DESIGN.md).
export const BRIEF_SECTIONS = ["站主觀點", "觀眾看完能做到的事"];
// A drama's brief is a story bible instead (docs/videos/DRAMA.md); the owner's stance stays.
export const BRIEF_SECTIONS_DRAMA = ["故事前提", "角色", "站主觀點"];
// An explainer (docs/videos/so-thats-why/) answers one question with no cast: the question, the
// one-sentence answer, and the owner's stance.
export const BRIEF_SECTIONS_EXPLAINER = ["問題", "一句答案", "站主觀點"];
// The hedges the channel review (docs/videos/channel-review-20261007/README.md §2.1 D04) found
// standing in for the numbers the title promised, counted as one family across the narration:
// the disclaimer lives in the description, and the number is said. A warning, never an error:
// an error would only teach the writer's lint_errors loop a synonym.
export const HEDGE_FAMILY = ["以官網為準", "以官方為準", "公告沒寫", "公告沒有寫", "不代表", "我不唸", "不在這裡唸", "不替你填"];
export const HEDGE_MAX = 1;
// How far into the narration (at the estimate's 250 characters a minute) a spoken table of
// contents still counts as the opening (D07), and the sentence shapes it takes.
export const OPENING_SECONDS = 40;
const OPENING_TOC = [
  /接下來(?:我們)?(?:會|要|就)?(?:分|分成|有|講|說|看|用)[一二三四五六七八九十兩\d]+(?:段|個|部分|點|件|步)/,
  /看完(?:這支|這部|這集|影片)?(?:之後|以後)?(?:你|大家)?(?:就|會|能)?(?:知道|學會|搞懂)/,
];
const ORDINAL_RUN = [/第一[，、]/, /第二[，、]/, /(?:第三|最後)[，、]/];
// The close (D03): three sentences, the last of them an invitation to subscribe with a reason.
export const OUTRO_SENTENCES = 3;
export const SUBSCRIBE_WORD = "訂閱";
export const SENTENCE_WARN = 40;
// An English word counts two units, so 40 is twenty words; spoken English runs to about 25 before it needs a breath.
export const SENTENCE_WARN_EN = 50;
export const HOOK_SECONDS = 30;
export const SIMILARITY_WARN = 0.8;
// SSML markup Azure also bills for, per line (a <break/> and the sentence wrapper); an estimate.
const MARKUP_PER_LINE = 30;

const URL = /https?:\/\/|www\.|\b[a-z0-9-]+\.(?:com|io|ai|dev|org|net|tw)\b/i;
const CJK = /[㐀-鿿豈-﫿]/gu;

// Before a myriad unit, the Japanese and Korean dub voices have read a number with a zero inside
// it as if the zero were not there: 4050億 and 4050억 both came out as 450. Writing the thousands
// with 千 or 천 (4千50億, 4천50억) was read right.
const MYRIAD_NUMBER = /(\d{1,3}(?:,\d{3})+|\d{4,})(?=\s*[億万억만])/g;
const THOUSANDS = { ja: "千", ko: "천" };

/** Numbers in a ja or ko line that have an inner zero and stand before 億, 万, 억 or 만. */
export function innerZeroNumbers(text) {
  return [...text.matchAll(MYRIAD_NUMBER)].map((match) => match[1]).filter((number) => /0+[1-9]/.test(number.replace(/,/g, "")));
}

/**
 * The body of each `## heading` in brief.md, comments removed. A heading is keyed by its name
 * alone: the planner prompt spells each one out as 「## 站主觀點 — what goes here」, and a brief
 * that copied the dash and the description still has the section.
 */
export function briefSections(markdown) {
  const sections = {};
  let current = null;
  for (const line of markdown.replace(/\r\n/g, "\n").replace(/<!--[\s\S]*?-->/g, "").split("\n")) {
    const heading = /^##\s+(.+?)\s*$/.exec(line);
    if (heading) {
      current = heading[1].split(/\s+[—–]\s+/)[0];
      sections[current] = "";
    } else if (current) {
      sections[current] += `${line}\n`;
    }
  }
  return sections;
}

/** The brief sections a video must fill: `preset` is a drama's look preset. */
export function briefSectionsFor(format = "slides", preset = null) {
  if (format !== "drama") return BRIEF_SECTIONS;
  return preset === EXPLAINER_PRESET ? BRIEF_SECTIONS_EXPLAINER : BRIEF_SECTIONS_DRAMA;
}

export function checkBrief(markdown, format = "slides", preset = null) {
  if (markdown === null || markdown === undefined) return ["brief.md is missing: the planner writes it before the script"];
  const sections = briefSections(markdown);
  return briefSectionsFor(format, preset).filter((name) => {
    const body = (sections[name] ?? "").replace(/待填|TODO|TBD/gi, "").replace(/[\s\p{P}\p{S}]/gu, "");
    return body.length === 0;
  }).map((name) => `brief.md needs a non-empty "## ${name}" section`);
}

// The channel's stance (docs/videos/HANDS-OFF.md §頻道立場): the owner's numbered points, one
// per line, and the brief's 站主觀點 opens by naming the ones this video applies.
export const STANCE_SECTION = "站主觀點";
export const STANCE_LINE = "套用立場";
const STANCE_POINT = /^\s*([0-9０-９]+)\s*[.．、)）]\s*(\S.*)$/;
const FULL_WIDTH_ZERO = "０".charCodeAt(0);

const asciiDigits = (text) => text.replace(/[０-９]/g, (digit) => String(digit.charCodeAt(0) - FULL_WIDTH_ZERO));

/** The stance's numbered points, `1. …` one per line: { number: text }. Empty for a blank stance. */
export function stancePoints(stance) {
  const points = {};
  if (typeof stance !== "string") return points;
  for (const line of stance.replace(/\r\n/g, "\n").split("\n")) {
    const match = STANCE_POINT.exec(line);
    if (match) points[Number(asciiDigits(match[1]))] = match[2].trim();
  }
  return points;
}

/**
 * What is wrong with the brief's 站主觀點 against the stance, as strings; nothing when the stance
 * is blank (the owner has not written one, so the old rule holds). With a stance, the section's
 * first non-blank line must read 「套用立場：N、M」 and every number must be one of its points.
 */
export function stanceProblems(brief, stance) {
  const points = stancePoints(stance);
  if (!Object.keys(points).length) return [];
  if (typeof brief !== "string") return ["brief.md is missing: the planner writes it before the script"];
  const section = briefSections(brief)[STANCE_SECTION];
  if (section === undefined) return [`brief.md needs a "## ${STANCE_SECTION}" section`];
  const first = section.split("\n").map((line) => line.trim()).find((line) => line.length > 0) ?? "";
  const match = new RegExp(`^${STANCE_LINE}\\s*[：:]\\s*(.*)$`).exec(first);
  if (!match) return [`the first line of "## ${STANCE_SECTION}" must read 「${STANCE_LINE}：N、M」, the numbers of the stance points it applies (found 「${first.slice(0, 40)}」)`];
  const numbers = asciiDigits(match[1]).split(/[、,，\s;；/]+/).filter(Boolean);
  if (!numbers.length) return [`「${STANCE_LINE}：」 names no stance point; the stance has ${Object.keys(points).join(", ")}`];
  const problems = [];
  for (const number of numbers) {
    if (!/^\d+$/.test(number)) problems.push(`「${STANCE_LINE}」 lists "${number}", which is not a point number`);
    else if (!(Number(number) in points)) problems.push(`「${STANCE_LINE}」 names point ${number}, but the stance has only ${Object.keys(points).join(", ")}`);
  }
  return problems;
}

function lcsLength(a, b) {
  const row = new Array(b.length + 1).fill(0);
  for (const x of a) {
    let previous = 0;
    for (let j = 1; j <= b.length; j++) {
      const saved = row[j];
      row[j] = x === b[j - 1] ? previous + 1 : Math.max(row[j], row[j - 1]);
      previous = saved;
    }
  }
  return row[b.length];
}

/**
 * How alike two videos' scene template sequences are, 0 to 1. Only the cards count: two
 * illustrated videos share "shot, shot, shot" whatever they show, and shotProblems compares the
 * pictures' prompts instead.
 */
export function templateSimilarity(a, b) {
  const x = a.scenes.filter((scene) => !isShot(scene)).map((scene) => scene.template);
  const y = b.scenes.filter((scene) => !isShot(scene)).map((scene) => scene.template);
  if (!x.length || !y.length) return 0;
  return lcsLength(x, y) / Math.max(x.length, y.length);
}

function revealCapacity(data) {
  for (const key of ["items", "rows", "steps", "points", "output"]) if (Array.isArray(data?.[key])) return data[key].length;
  return null;
}

/** Billable characters Azure would count: each Chinese character twice, markup included. */
export function billableEstimate(doc) {
  let total = 0;
  for (const { line } of eachLine(doc)) {
    const text = spokenText(line);
    total += [...text].length + (text.match(CJK)?.length ?? 0) + MARKUP_PER_LINE;
  }
  return total;
}

/**
 * Lint one video.
 * context: { lexicon, brief (markdown or null), others: [{ slug, doc }], translations: { locale: json },
 *            pack (the source_guide content pack or null), series (series.json or null), cpm }
 */
/**
 * An episode of a series uses the cast as the setting book has it, word for word, so the
 * character sheets are reused across episodes (docs/videos/SERIES.md). series.json beside
 * video.json is that cast, written by the worker when it starts the episode.
 */
function seriesProblems(doc, series, error, warn) {
  if (!series) {
    const report = hasAnimePolicy(doc) ? error : warn;
    report("series", "no series.json beside video.json: the worker writes it when it starts an episode (docs/videos/SERIES.md)");
    return;
  }
  if (series.slug !== doc.series.slug || series.episode !== doc.series.episode) {
    error("series", `series.json is for ${series.slug} episode ${series.episode}, not ${doc.series.slug} episode ${doc.series.episode}`);
  }
  if (hasAnimePolicy(doc)) {
    const problems = validateAnimePolicy(series);
    if (!isLongAnime(series) || problems.length) error("series", "the series snapshot must carry the complete approved long-anime production policy");
    else if (runtimePolicyHash(doc) !== runtimePolicyHash(series)) error("runtime_spec", "differs from the approved series production policy; restore its body and broadcast budgets");
    for (const key of ["kind", "genre", "lead", "planned_episodes", "open_ended", "closed_ending"]) {
      if (series[key] !== doc.series[key]) error(`series.${key}`, "differs from the trusted series episode context");
    }
  } else if (hasAnimePolicy(series)) error("production_policy", "the episode lost its series' long-anime production policy");
  const cast = new Map((series.characters ?? []).map((character) => [character.id, character]));
  (doc.characters ?? []).forEach((character, index) => {
    const known = cast.get(character.id);
    if (!known) {
      error(`characters[${index}]`, `"${character.id}" is not in the series' setting book; an episode uses the cast as written there`);
      return;
    }
    for (const key of ["appearance", "sheet_prompt"]) {
      if ((character[key] ?? null) !== (known[key] ?? null)) error(`characters[${index}].${key}`, "differs from the series' setting book; copy it as written so the character sheets are reused");
    }
    if (JSON.stringify(character.voice ?? null) !== JSON.stringify(known.voice ?? null)) error(`characters[${index}].voice`, "differs from the series' setting book; copy it as written");
    if (JSON.stringify(character.shot_looks ?? []) !== JSON.stringify(known.shot_looks ?? [])) error(`characters[${index}].shot_looks`, "differs from the series' approved look catalog; copy it as written");
  });
  // A binge series (docs/videos/BINGE.md) buys clips by tier: the worker copies the series'
  // visual_tier into series.json, and a script over its cap is caught here, before the clips
  // stage spends anything. An episode headed for a compilation opens cold, on the hook itself:
  // the episodes are stitched back to back, and a title card at every seam breaks the binge.
  if (series.visual_tier !== undefined && series.visual_tier !== null) {
    const tier = visualTierProblems(doc, series.visual_tier);
    for (const problem of tier.errors) error(problem.path, problem.message);
    for (const problem of tier.warnings) warn(problem.path, problem.message);
  }
  if (series.compilation === true) {
    if (doc.scenes[0]?.template === "title") error("scenes[0]", "a binge episode opens cold: the first line is the hook; drop the title card");
    // The compilation puts its own chapter card between episodes and one outro after the last;
    // an episode's outro card would play at every seam.
    doc.scenes.forEach((scene, index) => {
      if (scene.template === "outro") error(`scenes[${index}]`, "a binge episode ends on its cliffhanger: the compilation adds the cards; drop the outro");
    });
  }
}

/**
 * The shape of a narrated episode's script (script-writing.md §開場, §句子, §結尾), as warnings:
 * the hedge family said more than once in the narration, an opening that reads a table of
 * contents, and an outro that asks for no subscription or has not its three sentences.
 * `timeline` is the estimate; the opening is its first OPENING_SECONDS seconds.
 */
export function episodeScriptProblems(doc, timeline) {
  const problems = [];
  const warn = (path, message) => problems.push({ path, message });
  const counts = new Map();
  for (const { line } of eachLine(doc)) {
    for (const phrase of HEDGE_FAMILY) {
      const hits = line.text.split(phrase).length - 1;
      if (hits) counts.set(phrase, (counts.get(phrase) ?? 0) + hits);
    }
  }
  const hedges = [...counts.values()].reduce((sum, hits) => sum + hits, 0);
  if (hedges > HEDGE_MAX) {
    const found = [...counts].map(([phrase, hits]) => `「${phrase}」×${hits}`).join(", ");
    warn("scenes", `the narration hedges ${hedges} times (${found}); the family (${HEDGE_FAMILY.join("／")}) is said at most ${HEDGE_MAX} time a video: say the number from the official page or the site's checked article, and leave the disclaimer to the description`);
  }
  const starts = new Map((timeline?.lines ?? []).map((line) => [line.id, line.start_frame]));
  const opening = [...eachLine(doc)].filter(({ line }) => (starts.get(line.id) ?? Infinity) < OPENING_SECONDS * FPS).map(({ line }) => line.text).join("");
  if (OPENING_TOC.some((pattern) => pattern.test(opening)) || ORDINAL_RUN.every((pattern) => pattern.test(opening))) {
    warn("scenes[0]", `the first ${OPENING_SECONDS} s read a table of contents (「接下來分三段」「第一，…第二，…最後」「看完你會知道」); open on the question or the claim and a concrete number, date or name, and let the chapters announce themselves`);
  }
  doc.scenes.forEach((scene, index) => {
    if (scene.template !== "outro") return;
    const where = `scenes[${index}] (${scene.id})`;
    const said = (scene.lines ?? []).map((line) => line.text);
    if (!said.some((text) => text.includes(SUBSCRIBE_WORD))) warn(where, `the outro asks for no subscription: its ${OUTRO_SENTENCES} sentences answer the opening question with its number, ask one question the viewer can answer in a comment, and give one reason to subscribe (script-writing.md §結尾)`);
    if (said.length < OUTRO_SENTENCES) warn(where, `the outro has ${said.length} sentence${said.length === 1 ? "" : "s"}; the close is ${OUTRO_SENTENCES}: the answer with its number, a comment question, a subscribe invitation with a reason`);
  });
  return problems;
}

export function lintVideo(doc, context = {}) {
  const errors = [];
  const warnings = [];
  const error = (path, message) => errors.push({ path, message });
  const warn = (path, message) => warnings.push({ path, message });

  for (const problem of validateVideo(doc)) error(problem.path, problem.message);
  if (errors.length) return { errors, warnings, summary: null };

  const lexicon = context.lexicon ?? { schema_version: 1, terms: {} };
  for (const problem of validateLexicon(lexicon)) error(`lexicon.${problem.path}`, problem.message);
  for (const problem of checkBrief(context.brief, doc.format, doc.look?.preset ?? null)) error("brief.md", problem);
  const drama = isDrama(doc);
  const narration = narrationLocale(doc);
  const english = narration === "en";
  const pictures = illustrated(doc);
  if (doc.source_guide && context.pack === null) error("source_guide", `no content pack named ${doc.source_guide}`);
  if (drama && doc.series) seriesProblems(doc, context.series, error, warn);

  for (const { line, label } of eachLine(doc)) {
    const spoken = spokenText(line);
    for (const term of unknownTermsFor(spoken, lexicon, narration)) {
      error(label, `"${term}" is not in docs/videos/lexicon.json: add how to say it, or null once it sounds right`);
    }
    if (line.say !== undefined && line.say_for !== textHash(line.text)) {
      error(label, `"say" was written for an older "text"; update it, then set say_for to ${textHash(line.text)}`);
    }
    if (URL.test(line.text) || URL.test(spoken)) error(label, "never read a URL aloud: say it is in the description");
    for (const phrase of WRITTEN_ONLY) if (line.text.includes(phrase)) error(label, `"${phrase}" is written language; say it the way you would out loud`);
    for (const phrase of PROCESS_TALK) if (line.text.includes(phrase)) warn(label, `"${phrase}" narrates the process; facts and their sources go in claims.md and the description`);
    if (english) {
      const lower = line.text.toLowerCase();
      for (const phrase of WRITTEN_ONLY_EN) if (lower.includes(phrase)) error(label, `"${phrase}" is written language; say it the way you would out loud`);
      for (const phrase of PROCESS_TALK_EN) if (lower.includes(phrase)) warn(label, `"${phrase}" narrates the process; facts and their sources go in claims.md and the description`);
    }
    const longest = english ? SENTENCE_WARN_EN : SENTENCE_WARN;
    if (spokenUnits(line.text) > longest) warn(label, `${spokenUnits(line.text)} spoken units; split sentences longer than ${longest}`);
    if (/[()（）]/.test(line.text)) warn(label, "parentheses do not survive being read aloud; make it its own sentence");
  }

  doc.scenes.forEach((scene, index) => {
    // What the renderer refuses (templates.mjs), found here so the writer fixes it before any
    // audio is paid for, instead of the render blocking the video after the narration gate.
    const spec = !isShot(scene) && TEMPLATE_SPECS[scene.template];
    if (spec) for (const problem of spec.check(scene.data ?? {}).filter(Boolean)) error(`scenes[${index}] (${scene.id}).data`, problem);
    // A screencast's steps: safe to run (no secret typed, public pages only) and one capture per state.
    if (isScreencast(scene)) for (const problem of screencastSceneProblems(scene)) error(`scenes[${index}] (${scene.id}).data`, problem);
    const capacity = revealCapacity(scene.data);
    const reveals = scene.lines.reduce((sum, line) => sum + (line.reveal ?? 0), 0);
    if (capacity !== null && reveals > capacity) error(`scenes[${index}]`, `reveals ${reveals} elements but the ${scene.template} slide has ${capacity}`);
  });

  const timeline = estimateTimeline(doc, context.cpm ?? DEFAULT_CPM);
  for (const problem of productionShotProblems(doc, context.series, timeline)) error(problem.path, problem.message);
  if (drama || pictures) {
    const shots = shotProblems(doc, timeline);
    for (const problem of shots.errors) error(problem.path, problem.message);
    for (const problem of shots.warnings) warn(problem.path, problem.message);
  }
  // A drama with a cast is also read against the craft spec (craft.mjs, the rows the skill's
  // drama_craft_check.mjs prints): the rows it misses are warnings the writer fixes or answers.
  // A long anime keeps to its own production policy instead.
  if (hasCast(doc) && !isLongAnime(doc)) for (const problem of craftProblems(doc, timeline)) warn(problem.path, problem.message);
  // The performance contract (docs/videos/ILLUSTRATED.md §聲音表演): a plan on the narration's voice
  // and a cue on any format's line reach a Gemini style; one an Azure voice cannot take, and
  // lines that leave the plan to be read flat, are warnings for the writer.
  for (const problem of [...emotionProblems(doc), ...cueCoverageProblems(doc)]) warn(problem.path, problem.message);
  // The cadence of an illustrated video (docs/videos/ILLUSTRATED.md) is estimated here and
  // measured at the final gate; warnings, so the writer's draft is never blocked on an estimate.
  for (const problem of cadenceProblems(doc, timeline)) warn(problem.path, `${problem.message} (estimated; the final gate measures the synthesized timeline)`);
  // A brand story (docs/videos/STORY.md) is known by its series.json, which the worker writes
  // when it starts the episode; its rules come on top of the drama's.
  if (isStory(context.series)) {
    const story = storyProblems(doc, context.series, timeline);
    for (const problem of story.errors) error(problem.path, problem.message);
    for (const problem of story.warnings) warn(problem.path, problem.message);
  }
  const chapters = chapterList(timeline);
  for (const problem of checkChapters(timeline)) {
    if (problem.includes("at least")) error("scenes", problem);
    else warn("scenes", `${problem} (estimated; the real check runs on the synthesized timeline)`);
  }
  const hookSeconds = pictures ? ILLUSTRATED_HOOK_SECONDS : HOOK_SECONDS;
  if (chapters[0] && chapters[0].seconds > hookSeconds) {
    warn("scenes[0]", `the opening chapter runs about ${Math.round(chapters[0].seconds)} s; the hook should land within ${hookSeconds} s`);
  }
  const minutes = frameToSeconds(timeline.total_frames) / 60;
  const [low, high] = doc.target_minutes ?? DEFAULT_TARGET_MINUTES;
  // Every episode but a drama's runs at least eight minutes. The estimate reads 250 characters a
  // minute and the voice speaks about 300, so a script that clears it here can still come out
  // short: qa's assemble item measures the cut.
  const floor = needsMinimumLength(doc) ? minEpisodeMinutes() : 0;
  if (low < floor) error("target_minutes", `starts at ${low} minutes; every episode but a drama's runs at least ${floor}`);
  if (minutes < floor) error("scenes", `about ${minutes.toFixed(1)} minutes; every episode but a drama's runs at least ${floor}: write more narration`);
  // Where the floor holds it is the only length rule (owner, 2026-10-04): the upper end of
  // target_minutes is what the writer aims at, not a limit, so running over it is not warned. A
  // drama, a brand story and a long anime keep their own lengths on both sides.
  else if (minutes < low || (minutes > high && !needsMinimumLength(doc))) warn("scenes", `about ${minutes.toFixed(1)} minutes; the target is ${low}-${high}`);
  // The script's shape (episodeScriptProblems) is read on an episode: a narrated zh-TW video of
  // MIN_EPISODE_MINUTES or more, the constant and not the floor a fixture runner relaxes (the
  // examples run seconds and show the templates' shape, not a script's). A draft under the floor
  // is already sent back to be written longer; a drama keeps its own craft; the phrases are zh-TW.
  if (!drama && !english && minutes >= MIN_EPISODE_MINUTES) for (const problem of episodeScriptProblems(doc, timeline)) warn(problem.path, problem.message);
  if (isLongAnime(doc)) {
    const target = doc.runtime_spec.body_target_seconds;
    const seconds = frameToSeconds(timeline.total_frames);
    if (Math.abs(seconds - target) > ANIME_BODY_TOLERANCE_SECONDS) warn("runtime_spec", `estimated story body is ${seconds.toFixed(1)} seconds; measured acceptance is ${target - ANIME_BODY_TOLERANCE_SECONDS}–${target + ANIME_BODY_TOLERANCE_SECONDS} seconds, excluding OP/ED and broadcast reserve; write and pace the story before final QA`);
  }

  const article = context.pack ? articleUrl(context.pack, narration, doc.slug) : null;
  const description = composeDescription({ body: doc.youtube.description, timeline, article, sources: doc.sources ?? [], locale: narration, tags: doc.youtube.tags });
  for (const problem of checkYoutubeFields({ title: doc.youtube.title, description, tags: doc.youtube.tags })) error("youtube", problem);
  for (const problem of youtubeWarnings({ title: doc.youtube.title, tags: doc.youtube.tags }, "youtube", { numbered: drama })) warn("youtube", problem);
  if (!doc.youtube.tags.length) warn("youtube.tags", "no tags: add the product names and their common misspellings");
  if (!doc.sources?.length) warn("sources", "no sources: every fact in claims.md needs one, and they go in the description");

  for (const locale of LOCALES.filter((each) => each !== narration)) {
    const translation = context.translations?.[locale];
    if (!translation) continue;
    const stale = [];
    const missing = [];
    for (const { line } of eachLine(doc)) {
      const entry = translation.lines?.[line.id];
      if (!entry) missing.push(line.id);
      else if (entry.source_hash !== textHash(line.text)) stale.push(line.id);
    }
    if (missing.length) warn(`i18n/${locale}.json`, `${missing.length} lines not translated: ${missing.join(", ")}`);
    if (stale.length) warn(`i18n/${locale}.json`, `${stale.length} translations older than the ${narration} line: ${stale.join(", ")}`);
    const state = metadataStatus(doc, translation);
    const [absent, older, unknown] = ["missing", "stale", "unknown"].map((wanted) => namedWith(state, wanted));
    if (absent.length) warn(`i18n/${locale}.json`, `not translated: ${absent.join(", ")}`);
    if (older.length) warn(`i18n/${locale}.json`, `translations older than the ${narration} text: ${older.join(", ")}`);
    if (unknown.length) warn(`i18n/${locale}.json`, `translations merged before i18n-merge hashed their ${narration} text, so possibly stale: ${unknown.join(", ")}; i18n-sheet marks them todo`);
    if (state.orphans.length) warn(`i18n/${locale}.json`, `chapter titles for scenes that no longer open a chapter: ${state.orphans.join(", ")}; i18n-merge drops them`);
    // The description `package` uploads carries the link, chapters, sources and hashtags too, and
    // Hangul and kana take 3 bytes each, so a body that looks short can pass YouTube's 5,000 bytes.
    if (translation.title && translation.description) {
      const localeArticle = context.pack ? articleUrl(context.pack, context.pack.locales?.[locale] ? locale : narration, doc.slug) : null;
      const tags = translation.tags?.length ? translation.tags : doc.youtube.tags;
      const composed = composeDescription({ body: translation.description, timeline, chapterTitles: translation.chapters ?? {}, article: localeArticle, sources: doc.sources ?? [], locale, tags });
      for (const problem of checkYoutubeFields({ title: translation.title, description: composed, tags: [] }, locale)) warn(`i18n/${locale}.json`, `${problem} (package refuses it)`);
      for (const problem of youtubeWarnings({ title: translation.title, tags: [] }, locale, { numbered: drama })) warn(`i18n/${locale}.json`, problem);
    }
    const thousands = THOUSANDS[locale];
    if (thousands) {
      const risky = Object.entries(translation.lines ?? {}).flatMap(([id, entry]) => innerZeroNumbers(entry.text ?? "").map((number) => `${id} (${number})`));
      if (risky.length) warn(`i18n/${locale}.json`, `numbers with a zero inside, before a myriad unit, which the ${locale} dub voice has read without the zero (4050 as 450): ${risky.join(", ")}; write the thousands out, like 4${thousands}50`);
    }
  }

  // Every drama scene is a shot, so template sequences say nothing there; shotProblems compares prompts instead.
  for (const other of drama ? [] : context.others ?? []) {
    if (isDrama(other.doc)) continue;
    const similarity = templateSimilarity(doc, other.doc);
    if (similarity >= SIMILARITY_WARN && doc.scenes.length >= 5) {
      warn("scenes", `the slide sequence is ${Math.round(similarity * 100)}% the same as ${other.slug}; templated look-alikes are what YouTube's inauthentic-content policy demonetizes`);
    }
  }

  const summary = {
    minutes,
    lines: timeline.lines.length,
    spoken_units: [...eachLine(doc)].reduce((sum, { line }) => sum + spokenUnits(spokenText(line)), 0),
    billable_characters: billableEstimate(doc),
    chapters: chapters.map((chapter) => `${formatClock(chapter.start)} ${chapter.title}`),
  };
  return { errors, warnings, summary };
}

/** The animation profile's rules apply to both estimated and measured voice timelines. */
export function productionShotProblems(doc, series, timeline) {
  if (!isDrama(doc) || !series?.production?.profile) return [];
  const errors = [];
  const timed = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene]));
  doc.scenes.forEach((scene, index) => {
    if (!isShot(scene)) return;
    const where = `scenes[${index}] (${scene.id})`;
    if (shotVisual(scene) !== "clip") errors.push({ path: `${where}.data.visual`, message: "the production profile requires animated clips, not stills; put checked text graphics over an animated shot" });
    if (scene.data?.fit === "freeze") errors.push({ path: `${where}.data.fit`, message: "the production profile does not allow freeze-frame padding; split the shot or shorten its dialogue" });
    const duration = timed.get(scene.id);
    if (duration && duration.end_frame - duration.start_frame > 8 * FPS) errors.push({ path: where, message: "the production profile limits a shot to 8 seconds including pauses; split the shot or shorten its dialogue instead of holding the last frame" });
    // The profile's clips run exactly 8 seconds, so a cut from one must end inside them.
    if (isSourced(scene) && duration && scene.data.source.from_s * FPS + (duration.end_frame - duration.start_frame) > 8 * FPS) errors.push({ path: `${where}.data.source`, message: "the production profile's clips run 8 seconds; a cut from another shot's clip must end inside them: start earlier or shorten its dialogue" });
  });
  return errors;
}

/** Native source dimensions, before assembly can scale the picture. */
export function productionClipSizeProblem(series, metrics) {
  const video = series?.production?.profile?.video;
  if (video?.resolution !== "1080p" || (video.aspect ?? "16:9") !== "16:9") return null;
  if (metrics?.width === 1920 && metrics?.height === 1080) return null;
  return `the production profile requires a native 1920x1080 source; measured ${metrics?.width ?? "unknown"}x${metrics?.height ?? "unknown"} cannot be accepted by upscaling`;
}

/** Saved clip evidence must meet the current production profile on resume as well. */
export function productionClipProblems(doc, series, timeline, clips) {
  if (!isDrama(doc) || !series?.production?.profile) return [];
  const errors = productionShotProblems(doc, series, timeline);
  const expected = series.production.profile.video;
  if (expected && ["provider", "model", "resolution"].some((key) => expected[key] && clips?.clip?.[key] !== expected[key])) errors.push({ path: "clips", message: "saved clips do not match the approved production model and resolution" });
  const timed = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene]));
  doc.scenes.filter(isShot).forEach((scene) => {
    const entry = clips?.shots?.[scene.id];
    // A cut from another shot's clip is judged on that clip's evidence, from its start frame.
    const origin = entry?.source ? clips?.shots?.[entry.source.shot] : entry;
    const offset = entry?.source ? Math.round(entry.source.from_s * FPS) : 0;
    const duration = origin?.qc?.metrics?.duration;
    const time = timed.get(scene.id);
    if (origin?.still || origin?.qc?.ok !== true || !Number.isFinite(duration) || !time || Math.round(duration * FPS) < offset + time.end_frame - time.start_frame) errors.push({ path: `clips.${scene.id}`, message: "saved clip has no passing evidence of motion covering its whole dialogue; recheck the production clip" });
    const sizeProblem = productionClipSizeProblem(series, origin?.qc?.metrics);
    if (sizeProblem) errors.push({ path: `clips.${scene.id}`, message: sizeProblem });
  });
  return errors;
}
