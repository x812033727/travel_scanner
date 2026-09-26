// Everything that can be checked about a video before any audio or picture exists.
//
// Errors block the pipeline (the CLI exits 1); warnings are for the writer and reviewer to judge.
// The written-language list is the one the recorded route's video_kit.py uses, so a script that
// passes one route's check does not fail the other's.
import { emotionProblems, isDrama, shotProblems } from "./drama.mjs";
import { unknownTerms, validateLexicon } from "./lexicon.mjs";
import { articleUrl, checkYoutubeFields, composeDescription } from "./metadata.mjs";
import { DEFAULT_TARGET_MINUTES, LOCALES, NARRATION_LOCALE, eachLine, spokenText, textHash, validateVideo } from "./schema.mjs";
import { DEFAULT_CPM, chapterList, checkChapters, estimateTimeline, formatClock, frameToSeconds, spokenUnits } from "./timeline.mjs";
import { metadataStatus, namedWith } from "./translations.mjs";

// Phrases that only work on a page. Same list as video_kit.py's WRITTEN_ONLY.
export const WRITTEN_ONLY = ["本文", "這篇文章", "如上表", "如下表", "上表", "下表", "綜上所述", "值得注意的是", "筆者", "如圖所示"];
// Narrating how the facts were checked belongs in claims.md, not in the viewer's ear.
export const PROCESS_TALK = ["本影片", "經查證", "根據官方文件", "查核後", "截至查證"];
// The two brief sections the monetization policy makes mandatory (docs/videos/DESIGN.md).
export const BRIEF_SECTIONS = ["站主觀點", "觀眾看完能做到的事"];
// A drama's brief is a story bible instead (docs/videos/DRAMA.md); the owner's stance stays.
export const BRIEF_SECTIONS_DRAMA = ["故事前提", "角色", "站主觀點"];
export const SENTENCE_WARN = 40;
export const HOOK_SECONDS = 30;
export const SIMILARITY_WARN = 0.8;
// SSML markup Azure also bills for, per line (a <break/> and the sentence wrapper); an estimate.
const MARKUP_PER_LINE = 30;

const URL = /https?:\/\/|www\.|\b[a-z0-9-]+\.(?:com|io|ai|dev|org|net|tw)\b/i;
const CJK = /[㐀-鿿豈-﫿]/gu;

/** The body of each `## heading` in brief.md, comments removed. */
export function briefSections(markdown) {
  const sections = {};
  let current = null;
  for (const line of markdown.replace(/\r\n/g, "\n").replace(/<!--[\s\S]*?-->/g, "").split("\n")) {
    const heading = /^##\s+(.+?)\s*$/.exec(line);
    if (heading) {
      current = heading[1];
      sections[current] = "";
    } else if (current) {
      sections[current] += `${line}\n`;
    }
  }
  return sections;
}

export function checkBrief(markdown, format = "slides") {
  if (markdown === null || markdown === undefined) return ["brief.md is missing: the planner writes it before the script"];
  const sections = briefSections(markdown);
  return (format === "drama" ? BRIEF_SECTIONS_DRAMA : BRIEF_SECTIONS).filter((name) => {
    const body = (sections[name] ?? "").replace(/待填|TODO|TBD/gi, "").replace(/[\s\p{P}\p{S}]/gu, "");
    return body.length === 0;
  }).map((name) => `brief.md needs a non-empty "## ${name}" section`);
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

/** How alike two videos' scene template sequences are, 0 to 1. */
export function templateSimilarity(a, b) {
  const x = a.scenes.map((scene) => scene.template);
  const y = b.scenes.map((scene) => scene.template);
  if (!x.length || !y.length) return 0;
  return lcsLength(x, y) / Math.max(x.length, y.length);
}

function revealCapacity(data) {
  for (const key of ["items", "rows", "steps", "points"]) if (Array.isArray(data?.[key])) return data[key].length;
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
 *            pack (the source_guide content pack or null), cpm }
 */
export function lintVideo(doc, context = {}) {
  const errors = [];
  const warnings = [];
  const error = (path, message) => errors.push({ path, message });
  const warn = (path, message) => warnings.push({ path, message });

  for (const problem of validateVideo(doc)) error(problem.path, problem.message);
  if (errors.length) return { errors, warnings, summary: null };

  const lexicon = context.lexicon ?? { schema_version: 1, terms: {} };
  for (const problem of validateLexicon(lexicon)) error(`lexicon.${problem.path}`, problem.message);
  for (const problem of checkBrief(context.brief, doc.format)) error("brief.md", problem);
  const drama = isDrama(doc);
  if (!drama && doc.music) warn("music", "the channel spec puts no music under slides videos (docs/videos/README.md); a drama may");
  if (doc.source_guide && context.pack === null) error("source_guide", `no content pack named ${doc.source_guide}`);

  for (const { line, label } of eachLine(doc)) {
    const spoken = spokenText(line);
    for (const term of unknownTerms(spoken, lexicon)) {
      error(label, `"${term}" is not in docs/videos/lexicon.json: add how to say it, or null once it sounds right`);
    }
    if (line.say !== undefined && line.say_for !== textHash(line.text)) {
      error(label, `"say" was written for an older "text"; update it, then set say_for to ${textHash(line.text)}`);
    }
    if (URL.test(line.text) || URL.test(spoken)) error(label, "never read a URL aloud: say it is in the description");
    for (const phrase of WRITTEN_ONLY) if (line.text.includes(phrase)) error(label, `"${phrase}" is written language; say it the way you would out loud`);
    for (const phrase of PROCESS_TALK) if (line.text.includes(phrase)) warn(label, `"${phrase}" narrates the process; facts and their sources go in claims.md and the description`);
    if (spokenUnits(line.text) > SENTENCE_WARN) warn(label, `${spokenUnits(line.text)} spoken units; split sentences longer than ${SENTENCE_WARN}`);
    if (/[()（）]/.test(line.text)) warn(label, "parentheses do not survive being read aloud; make it its own sentence");
  }

  doc.scenes.forEach((scene, index) => {
    const capacity = revealCapacity(scene.data);
    const reveals = scene.lines.reduce((sum, line) => sum + (line.reveal ?? 0), 0);
    if (capacity !== null && reveals > capacity) error(`scenes[${index}]`, `reveals ${reveals} elements but the ${scene.template} slide has ${capacity}`);
  });

  const timeline = estimateTimeline(doc, context.cpm ?? DEFAULT_CPM);
  if (drama) {
    const shots = shotProblems(doc, timeline);
    for (const problem of shots.errors) error(problem.path, problem.message);
    for (const problem of shots.warnings) warn(problem.path, problem.message);
    for (const problem of emotionProblems(doc)) warn(problem.path, problem.message);
  }
  const chapters = chapterList(timeline);
  for (const problem of checkChapters(timeline)) {
    if (problem.includes("at least")) error("scenes", problem);
    else warn("scenes", `${problem} (estimated; the real check runs on the synthesized timeline)`);
  }
  if (chapters[0] && chapters[0].seconds > HOOK_SECONDS) {
    warn("scenes[0]", `the opening chapter runs about ${Math.round(chapters[0].seconds)} s; the hook should land within ${HOOK_SECONDS} s`);
  }
  const minutes = frameToSeconds(timeline.total_frames) / 60;
  const [low, high] = doc.target_minutes ?? DEFAULT_TARGET_MINUTES;
  if (minutes < low || minutes > high) warn("scenes", `about ${minutes.toFixed(1)} minutes; the target is ${low}-${high}`);

  const article = context.pack ? articleUrl(context.pack, NARRATION_LOCALE, doc.slug) : null;
  const description = composeDescription({ body: doc.youtube.description, timeline, article, sources: doc.sources ?? [], locale: NARRATION_LOCALE });
  for (const problem of checkYoutubeFields({ title: doc.youtube.title, description, tags: doc.youtube.tags })) error("youtube", problem);
  if (!doc.youtube.tags.length) warn("youtube.tags", "no tags: add the product names and their common misspellings");
  if (!doc.sources?.length) warn("sources", "no sources: every fact in claims.md needs one, and they go in the description");

  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
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
    if (stale.length) warn(`i18n/${locale}.json`, `${stale.length} translations older than the zh-TW line: ${stale.join(", ")}`);
    const state = metadataStatus(doc, translation);
    const [absent, older, unknown] = ["missing", "stale", "unknown"].map((wanted) => namedWith(state, wanted));
    if (absent.length) warn(`i18n/${locale}.json`, `not translated: ${absent.join(", ")}`);
    if (older.length) warn(`i18n/${locale}.json`, `translations older than the zh-TW text: ${older.join(", ")}`);
    if (unknown.length) warn(`i18n/${locale}.json`, `translations merged before i18n-merge hashed their zh-TW text, so possibly stale: ${unknown.join(", ")}; i18n-sheet marks them todo`);
    if (state.orphans.length) warn(`i18n/${locale}.json`, `chapter titles for scenes that no longer open a chapter: ${state.orphans.join(", ")}; i18n-merge drops them`);
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
