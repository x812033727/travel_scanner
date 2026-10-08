// A brand story on the host (docs/videos/STORY.md): a 12 to 15 minute non-fiction documentary told
// by a narrator alone over about 90 cartoon stills, written, fact-checked and heard one chapter at
// a time from a plan that was fact-checked before it was imported.
//
// The site hands a story over as an episode of a series of kind "story" (GET automation/series/next,
// then episodes/{n}/start under the video slug the plan fixed), with the whole plan as the
// episode's beats. The worker writes brief.md and series.json from it and approves the outline
// here, as it does for an episode of an approved chapter: the owner approved the list of stories.
// Then every step makes at most one model call, so each fits the site's 295-second relay and its
// output limit: the writer writes a chapter a call (writer:story) and the worker keeps the six in
// <workdir>/story/chapters/, merges them into video.json and claims.md and lints; a lint error is
// sent back for the chapter it is in. A fresh checker takes a chapter a call (verifier:story) and
// answers a patch and the chapter's rows of the claims table; the listener takes a chapter a call
// (listener:story) and answers a patch. A story has no script gate: the step every drama has is
// approved here, with a note that says why. After tts the measured narration must be within a
// band around the target; else the writer adds to or cuts from one chapter, twice at most, and a
// story whose passages hold no more is left for the owner, never padded. A keyframe that failed
// its check goes back to the writer (writer:story-fix) for the named shots alone.
//
// The fact check differs most from a drama's. The plan's facts are established (a second reader
// confirmed each against its sources before the import): the checker holds the script to the
// plan and looks in the pages only for what the writer added. The pages are read whole and the
// passages around a chapter's figures, years and names are cut out of them, since a quarter of
// the plan's long pages hold the sentence past the 40,000 characters the reader keeps; a page the
// reader cannot turn into text (a PDF, a page over 3 MB) is handed over as the plan's `supports`
// line for it, marked as read by the plan's reviewer; a fact whose sources are all like that
// (`reviewer_only`) is held to the plan's wording and no page is looked for.
//
// This module works through the automation's methods, as compilation.mjs does, and imports
// nothing from flow.mjs or series.mjs, which call into it.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { approve } from "../core/approvals.mjs";
import { emptyLexicon } from "../core/lexicon.mjs";
import { lintVideo } from "../core/lint.mjs";
import { atomicWrite, contentPackFile, docDir, lexiconFile, readJson, readText } from "../core/paths.mjs";
import { writeScreenplay } from "../core/screenplay.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { namePattern, STORY_KIND, STORY_RULES } from "../core/story.mjs";
import { DEFAULT_CPM, formatClock, FPS, spokenUnits } from "../core/timeline.mjs";
import { clipHeadline } from "../story-plans/plan.mjs";
import { AutomationError } from "./client.mjs";
import { pageReader } from "./fetch.mjs";
import { rewriteProblems } from "./rewrite.mjs";
import { STORY_FIX_VARIANT, STORY_VARIANT } from "./story-prompts.mjs";

// --- the numbers -------------------------------------------------------------------------------

/** The six chapters of every plan, in order, with the letter their claim ids start with. */
export const STORY_CHAPTERS = [
  { key: "hook", label: "開場的問題", prefix: "h" },
  { key: "origin", label: "起點與人物", prefix: "o" },
  { key: "idea", label: "關鍵點子", prefix: "i" },
  { key: "engine", label: "生意怎麼運作", prefix: "e" },
  { key: "turn", label: "代價或轉折", prefix: "t" },
  { key: "now", label: "現在與一句觀察", prefix: "n" },
];
export const CHAPTER_KEYS = STORY_CHAPTERS.map((chapter) => chapter.key);
const CHAPTER_OF = new Map(STORY_CHAPTERS.map((chapter, index) => [chapter.key, { ...chapter, index }]));

// How a story's length is shared (docs/videos/STORY.md §一支故事影片的規格): the narration is read
// at 250 characters a minute (the tool's estimate), the hook is said within 30 seconds, and the
// other five chapters share the rest in these weights, engine the longest. A shot holds 6 to 12
// seconds; the budgets are cut to SHOT_SECONDS a shot, so a 13-minute story is 3,250 characters
// over about 90 shots. chapterBudgets() is the one place these become a chapter's share.
export const STORY_CPM = DEFAULT_CPM;
export const HOOK_SECONDS = 30;
export const CHAPTER_WEIGHTS = { origin: 5, idea: 4.5, engine: 7, turn: 5, now: 3.5 };
export const SHOT_SECONDS = 8.7;
// video.json's target_minutes around the series' target: lint warns outside it (12 to 15 for 13).
export const TARGET_SPREAD = { below: 1, above: 2 };
// The measured narration after tts: within this far of the target (11:30 to 15:30 for 13
// minutes), else the writer adds to or cuts from ONE chapter, LENGTH_FIX_ROUNDS times at most.
export const LENGTH_BAND_SECONDS = { below: 90, above: 150 };
export const LENGTH_FIX_ROUNDS = 2;
// A cut asks at most this share of the chapter it is asked of, an addition at most this much of
// it again (a chapter that ran half its share may double).
const RESIZE_SHARE = { cut: 0.45, add: 1 };

// The rounds this flow allows, the same as the drama's (flow.mjs MAX_LINT_FIXES,
// MAX_PROMPT_FIX_ROUNDS); a checker that changes more than CHANGED_FACTS_RECHECK facts in a
// chapter has the chapter checked again by a fresh session (STORY.md §產線與關卡), up to the
// drama's rounds on the settings tab.
export const STORY_LINT_FIXES = 3;
export const STORY_PROMPT_FIX_ROUNDS = 2;
export const CHANGED_FACTS_RECHECK = 3;

// What a model call may carry of the pages (docs/videos/STORY.md §查核與來源規則): a page this short
// goes whole; a longer one gives the passages around the chapter's figures, years and names, this
// many characters either side, at most PER_SOURCE of one page and PER_CALL of all of them.
export const PASSAGES = { radius: 500, wholePage: 4_000, perSource: 8_000, perCall: 40_000, hitsPerAnchor: 8 };
// A page that answers with less text than this is drawn by a script the reader does not run: the
// plan's own check counts it as unreadable (tools/video/story-plans/validate.mjs MIN_PAGE_CHARS).
export const MIN_READABLE_CHARS = 400;

// The output each call may take: a chapter is about 25 shots at most, some 5,000 tokens.
const WRITER_TOKENS = 16_000;
const CHECKER_TOKENS = 16_000;
// The listener runs on Opus 5.5 by default, which always thinks; thinking counts toward the cap.
const LISTENER_TOKENS = 16_000;
const FIX_TOKENS = 16_000;

// What a story keeps in its work directory, relative to it: the chapters as written and checked
// (small, and what a person reads when a story goes wrong), and the pages its sources gave, whole
// (megabytes; the tidy removes them with the other media once the video is finished, tidy.mjs).
export const STORY_DIR = "story";
export const STORY_CHAPTERS_DIR = path.join(STORY_DIR, "chapters");
export const STORY_PAGES_DIR = path.join(STORY_DIR, "pages");

export const OUTLINE_NOTE = "品牌故事：題目是站主核准過的企劃清單（docs/videos/STORY.md），大綱不再問 Jev";
export const SCRIPT_NOTE = "品牌故事沒有劇本關卡：企劃查核過、逐章查核與聽眾審稿已完成，依故事流程在本機核准";
export const STORY_MUSIC = "light documentary underscore: soft piano, pizzicato strings and marimba, curious and warm, steady mid tempo, no vocals";
const CATEGORY_TAGS = { everyday: "日常用品", "asia-brand": "亞洲品牌", tech: "科技" };
const PLAN_UNREAD = (source, why) => `工人這次讀不到這一頁（${why}）；supports 是企劃查核時（${source.checked ?? "?"}）讀到的內容，不是這次讀的`;

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const clip = (text, max) => String(text).trim().slice(0, max);
const hash16 = (text) => createHash("sha256").update(String(text)).digest("hex").slice(0, 16);
const chars = (text) => [...String(text)].length;

/** Each chapter's share of a story of `targetMinutes`: { key, seconds, chars, shots }, summing to the target. */
export function chapterBudgets(targetMinutes) {
  const total = Math.round(targetMinutes * 60);
  const rest = Math.max(0, total - HOOK_SECONDS);
  const weight = Object.values(CHAPTER_WEIGHTS).reduce((sum, each) => sum + each, 0);
  const budgets = CHAPTER_KEYS.map((key) => {
    const seconds = key === "hook" ? Math.min(HOOK_SECONDS, total) : (rest * CHAPTER_WEIGHTS[key]) / weight;
    return { key, seconds: Math.round(seconds), chars: Math.round((seconds * STORY_CPM) / 60), shots: Math.max(2, Math.round(seconds / SHOT_SECONDS)) };
  });
  // Rounding lands on the longest chapter, so the shares add up to the target exactly.
  const engine = budgets.find((budget) => budget.key === "engine");
  engine.seconds += total - budgets.reduce((sum, budget) => sum + budget.seconds, 0);
  engine.chars += Math.round((total * STORY_CPM) / 60) - budgets.reduce((sum, budget) => sum + budget.chars, 0);
  return budgets;
}

/** The measured narration a story of `targetMinutes` may run, in seconds: [low, high]. */
export const lengthBand = (targetMinutes) => [targetMinutes * 60 - LENGTH_BAND_SECONDS.below, targetMinutes * 60 + LENGTH_BAND_SECONDS.above];

// --- the plan ----------------------------------------------------------------------------------

/** Why a story's plan (the episode's beats) cannot be written from, or null. */
export function planShapeProblem(plan) {
  if (!isObject(plan)) return "the episode has no plan (beats)";
  const chapters = Array.isArray(plan.chapters) ? plan.chapters : [];
  if (chapters.length !== CHAPTER_KEYS.length || chapters.some((chapter, index) => chapter?.key !== CHAPTER_KEYS[index] || !isText(chapter?.point))) return `the plan's chapters must be the six ${CHAPTER_KEYS.join(", ")}, each with its point`;
  if (!Array.isArray(plan.sources) || !plan.sources.length || plan.sources.some((source) => !isText(source?.url))) return "the plan has no sources";
  if (!Array.isArray(plan.must_verify)) return "the plan has no must_verify";
  if (!Array.isArray(plan.names)) return "the plan has no names";
  if (!isText(plan.question)) return "the plan has no question";
  return null;
}

/**
 * The plan's recurring figures as video.json's characters: generic cartoon people, never a
 * likeness. A figure's name reaches the image prompts (keyframes and sheets draw "<name>:
 * <appearance>"), so it is the figure's id in plain words with every name of the story taken out;
 * the voice is the narrator's, since nobody in a story speaks, and lint wants one.
 */
export function storyCast(plan, voice) {
  const names = (plan.names ?? []).filter(isText);
  return (plan.cast ?? [])
    .filter((figure) => isObject(figure) && isText(figure.id) && isText(figure.appearance))
    .map((figure, index) => {
      let name = figure.id.replace(/-/g, " ");
      for (const each of names) name = name.replace(new RegExp(namePattern(each).source, "giu"), " ");
      name = name.replace(/\s+/g, " ").trim();
      return { id: figure.id, name: name || `figure ${index + 1}`, appearance: clip(figure.appearance, 800), voice };
    })
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

/** docs/videos/<slug>/series.json for a story: what lint reads (kind, names, the cast) and what the stages read (the plan, the look). */
export function storySeriesFile({ series, episode, plan, cast }) {
  return {
    kind: STORY_KIND,
    slug: series.slug,
    episode: episode.number,
    chapter: 1,
    title: episode.title,
    logline: episode.logline,
    names: (plan.names ?? []).filter(isText),
    characters: cast,
    visual_tier: "stills",
    compilation: false,
    target_minutes: Number(series.target_minutes) || 13,
    image_model: series.image_model ?? null,
    look: isObject(series.look) ? { style: series.look.style ?? "", negative: series.look.negative ?? "", ...(isText(series.look.motion) ? { motion: series.look.motion } : {}) } : null,
    plan,
    series: { title: series.title, premise: series.premise ?? "", note: series.note ?? null, hands_off: Boolean(series.hands_off), episodes_per_day: series.episodes_per_day ?? null },
  };
}

/** brief.md for a story: the sections lint wants, the plan's six points, one outline (approved here). */
export function storyBrief({ episode, plan, cast }) {
  const lines = [
    `# ${episode.title}`,
    "",
    "## 故事前提",
    episode.logline || plan.subject || episode.title,
    "",
    `開場要回答的問題：${plan.question}`,
    "",
    `留給觀眾的觀察：${plan.takeaway ?? ""}`,
    "",
    "## 角色",
    ...(cast.length
      ? cast.map((figure) => `- ${figure.id}：${(plan.cast ?? []).find((each) => each.id === figure.id)?.role ?? figure.name}（一般化的卡通人物，不對應任何真人）`)
      : ["沒有反覆出場的角色：全片只有旁白，畫面裡的人物都是一般化的卡通人物，不對應任何真人。"]),
    "",
    "## 站主觀點",
    `${plan.takeaway ?? ""}只講查得到出處的事，傳說與事實分開講；不業配、不推薦購買。`,
    "",
    "## 章節",
    ...plan.chapters.map((chapter, index) => `${index + 1}. ${CHAPTER_OF.get(chapter.key)?.label ?? chapter.key}：${chapter.point}`),
    "",
    "## 大綱",
    "",
    `### 選項 A：${episode.title}`,
    `一行說明：${episode.logline || plan.subject || episode.title}`,
    `開場鉤子：「${plan.question}」`,
    "",
    "## 來源",
    ...plan.sources.map((source) => `- ${source.url}（${source.publisher ?? ""}）`),
    ...(isText(plan.caveats) ? ["", "## 查核者的注意事項", plan.caveats.trim()] : []),
    "",
  ];
  return lines.join("\n");
}

// --- facts, figures and passages ----------------------------------------------------------------

/** The figures of a text, as digit strings (thousands marks out, a decimal point kept); single digits are too common to find anything with. */
export function figuresIn(text) {
  const found = new Set();
  for (const match of String(text).normalize("NFKC").matchAll(/\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?/g)) {
    const figure = match[0].replace(/,/g, "");
    if (figure.replace(/\D/g, "").length >= 2) found.add(figure);
  }
  return found;
}

const escapeRegExp = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * A year as official pages write it besides the Western year: the Japanese eras and the Republic
 * of China's calendar (STORY.md: 660 of 773 measured facts were found literally, most of the rest
 * are a year in 昭和 or 民國).
 */
export function yearForms(year) {
  const forms = [];
  const era = (name, first, last) => {
    if (year < first || year > last) return;
    const n = year - first + 1;
    forms.push(`${name}${n}年`, ...(n === 1 ? [`${name}元年`] : []));
  };
  era("明治", 1868, 1912);
  era("大正", 1912, 1926);
  era("昭和", 1926, 1989);
  era("平成", 1989, 2019);
  era("令和", 2019, 2100);
  if (year >= 1912) forms.push(`民國${year - 1911}年`, `民國${year - 1911}`, `${year - 1911}年`);
  return forms;
}

/** A figure as a pattern: its digits with an optional thousands mark between any two, and a year in its other calendars. */
function figurePattern(figure) {
  const body = figure.includes(".") ? escapeRegExp(figure) : [...figure].join("[,，.'’ ]?");
  const year = /^\d{4}$/.test(figure) && Number(figure) >= 1868 && Number(figure) <= 2100 ? yearForms(Number(figure)).map((form) => `(?<!\\d)${escapeRegExp(form)}`) : [];
  return new RegExp([`(?<![\\d.,])${body}(?!\\d)`, ...year].join("|"), "gu");
}

/**
 * What to look for in a page: the figures, the story's names and the quoted phrases the texts
 * hold, each { label, pattern } with a global pattern. `names` is the plan's list.
 */
export function anchorsFor(texts, names = []) {
  const anchors = new Map();
  for (const text of texts.filter(isText)) {
    for (const figure of figuresIn(text)) if (!anchors.has(`#${figure}`)) anchors.set(`#${figure}`, { label: figure, pattern: figurePattern(figure) });
    for (const name of names.filter(isText)) {
      const pattern = namePattern(name);
      if (pattern.test(text) && !anchors.has(`@${name}`)) anchors.set(`@${name}`, { label: name, pattern: new RegExp(pattern.source, "giu") });
    }
    for (const match of String(text).matchAll(/[「“"『]([^」”"』]{4,40})[」”"』]/g)) {
      const phrase = match[1].trim();
      if (phrase.length >= 4 && !anchors.has(`"${phrase}`)) anchors.set(`"${phrase}`, { label: phrase, pattern: new RegExp(phrase.split(/\s+/).map(escapeRegExp).join("\\s+"), "giu") });
    }
  }
  return [...anchors.values()];
}

/**
 * The passages of a page's whole text around the anchors: windows of PASSAGES.radius characters
 * either side of each hit, merged where they touch, the windows holding the most anchors first,
 * within `limit` characters, then in page order. A short page goes whole; a page where nothing
 * is found gives its head, marked so the model converts calendars and units before it concludes.
 * Answers { passages: [{ at, text }], found: [labels], whole?, head? }.
 */
export function passagesOf(text, anchors, { radius = PASSAGES.radius, limit = PASSAGES.perSource, wholePage = PASSAGES.wholePage, hitsPerAnchor = PASSAGES.hitsPerAnchor } = {}) {
  const page = String(text);
  const hits = [];
  for (const anchor of anchors) {
    let count = 0;
    anchor.pattern.lastIndex = 0;
    for (const match of page.matchAll(anchor.pattern)) {
      hits.push({ start: match.index, end: match.index + match[0].length, label: anchor.label });
      if (++count >= hitsPerAnchor) break;
    }
  }
  const found = [...new Set(hits.map((hit) => hit.label))];
  if (page.length <= wholePage) return { passages: [{ at: 0, text: page }], found, whole: true };
  if (!hits.length) return { passages: [{ at: 0, text: `${page.slice(0, limit)}…` }], found, head: true };
  hits.sort((a, b) => a.start - b.start);
  const windows = [];
  for (const hit of hits) {
    const start = Math.max(0, hit.start - radius);
    const end = Math.min(page.length, hit.end + radius);
    const last = windows.at(-1);
    if (last && start <= last.end) {
      last.end = Math.max(last.end, end);
      last.labels.add(hit.label);
    } else windows.push({ start, end, labels: new Set([hit.label]) });
  }
  const chosen = [];
  let used = 0;
  for (const window of [...windows].sort((a, b) => b.labels.size - a.labels.size || a.start - b.start)) {
    const length = window.end - window.start;
    if (used + length <= limit) {
      chosen.push(window);
      used += length;
    } else if (!chosen.length) {
      chosen.push({ ...window, end: window.start + limit });
      used = limit;
    }
  }
  chosen.sort((a, b) => a.start - b.start);
  return { passages: chosen.map((window) => ({ at: window.start, text: `${window.start > 0 ? "…" : ""}${page.slice(window.start, window.end)}${window.end < page.length ? "…" : ""}` })), found };
}

/** Figures weigh more than names when a fact is matched to a chapter: a year is specific, a founder's name is everywhere. */
function anchorWeights(text, names) {
  const weights = new Map();
  for (const figure of figuresIn(text)) weights.set(`#${figure}`, 3);
  for (const name of names.filter(isText)) if (namePattern(name).test(text)) weights.set(`@${name}`, 1);
  return weights;
}

const overlap = (a, b) => [...a].reduce((sum, [key, weight]) => sum + (b.has(key) ? weight : 0), 0);

/**
 * The chapters each fact of the plan belongs to: the chapter(s) whose point shares the most of its
 * figures and names. A fact that shares nothing with any point belongs to none (the writer still
 * sees every fact; this only chooses which pages a chapter's passages come from).
 */
export function factChapters(plan) {
  const names = plan.names ?? [];
  const points = plan.chapters.map((chapter) => anchorWeights(chapter.point, names));
  return (plan.must_verify ?? []).map((fact) => {
    const mine = anchorWeights(fact?.claim ?? "", names);
    const scores = points.map((point) => overlap(mine, point));
    const best = Math.max(0, ...scores);
    return best > 0 ? CHAPTER_KEYS.filter((_, index) => scores[index] === best) : [];
  });
}

/** The plan's facts as the model reads them: index, claim, sources, flags, and the chapters they belong to. */
function factsPayload(plan, belongs = factChapters(plan)) {
  return (plan.must_verify ?? []).map((fact, index) => ({
    index,
    claim: fact.claim,
    sources: fact.sources ?? [],
    ...(fact.core ? { core: true } : {}),
    ...(fact.attributed ? { attributed: true } : {}),
    ...(fact.reviewer_only ? { reviewer_only: true, note: "工人讀不到這條的任何來源：照企劃的寫法核對，不去頁面裡找" } : {}),
    chapters: belongs[index],
  }));
}

// --- reading the pages ---------------------------------------------------------------------------

const readers = new WeakMap();

/** The story's reader: the worker's own (fetch.mjs), asked for the whole text. One per automation, so the per-host gap holds across a run. */
function storyReader(automation) {
  if (!readers.has(automation)) {
    const { ctx } = automation;
    readers.set(automation, pageReader({ fetchImpl: ctx.fetch ?? globalThis.fetch, ...(ctx.sleep ? { sleep: ctx.sleep } : {}), now: () => ctx.now().getTime(), whole: true }));
  }
  return readers.get(automation);
}

/**
 * One page as the stages of this video read it: { url, readable, text?, chars, error? }, kept in
 * <workdir>/story/pages/ so the six writers and six checkers read a page once. A failure that may
 * pass (no answer, 429, a server error) is not kept, so the next step asks again.
 */
export async function readStoryPage(automation, state, url) {
  const file = path.join(automation.workdir(state.slug), STORY_PAGES_DIR, `${hash16(url)}.json`);
  const kept = readJson(file, null);
  if (kept?.url === url) return kept;
  const page = await storyReader(automation)(url);
  const text = page.ok ? String(page.whole ?? page.text).normalize("NFKC") : "";
  const readable = page.ok && text.length >= MIN_READABLE_CHARS;
  const entry = { url, status: page.status ?? 0, readable, chars: text.length, ...(readable ? { title: page.title ?? "", text } : { error: page.ok ? `only ${text.length} characters of text` : page.error }), read_at: automation.ctx.now().toISOString() };
  const passing = !page.ok && (!page.status || page.status === 429 || page.status >= 500);
  if (!passing) atomicWrite(file, JSON.stringify(entry));
  return entry;
}

/**
 * The sources a call carries, most relevant first: a readable page as its passages around
 * `anchors`, within the call's budget; a page the reader cannot turn into text as the plan's
 * `supports` line, marked as read by the plan's reviewer and not now. Every source keeps its
 * `supports` line, which says what the page is evidence for.
 */
async function sourcesPayload(automation, state, plan, indexes, anchors) {
  const entries = [];
  let budget = PASSAGES.perCall;
  for (const index of indexes) {
    const source = plan.sources[index];
    if (!source) continue;
    const base = { index, url: source.url, publisher: source.publisher ?? "", kind: source.kind ?? "", supports: source.supports ?? "" };
    const page = await readStoryPage(automation, state, source.url);
    if (!page.readable) {
      entries.push({ ...base, read: "plan", note: PLAN_UNREAD(source, page.error ?? `HTTP ${page.status}`) });
      continue;
    }
    if (budget < 1_000) {
      entries.push({ ...base, read: "now", note: "這一頁讀得到，但這次呼叫的篇幅已滿，沒有附上段落" });
      continue;
    }
    const cut = passagesOf(page.text, anchors, { limit: Math.min(PASSAGES.perSource, budget) });
    budget -= cut.passages.reduce((sum, passage) => sum + passage.text.length, 0);
    entries.push({ ...base, read: "now", chars: page.chars, ...(cut.whole ? { whole: true } : {}), ...(cut.head ? { note: "頁面裡找不到這一章的數字、年份或名字的原樣：這是頁面開頭；先換算紀年與單位再下結論" } : {}), found: cut.found, passages: cut.passages });
  }
  return entries;
}

/** The pages a chapter's writer reads: those of the facts that belong to it and those whose supports line meets its point; every page when none does. */
function writerSourceOrder(plan, key, belongs) {
  const names = plan.names ?? [];
  const scores = new Map();
  const add = (index, score) => Number.isInteger(index) && plan.sources[index] && scores.set(index, (scores.get(index) ?? 0) + score);
  (plan.must_verify ?? []).forEach((fact, index) => {
    if (belongs[index].includes(key)) for (const source of fact.sources ?? []) add(source, 2);
  });
  const point = anchorWeights(plan.chapters[CHAPTER_OF.get(key).index].point, names);
  plan.sources.forEach((source, index) => {
    const score = overlap(anchorWeights(source.supports ?? "", names), point);
    if (score > 0) add(index, score);
  });
  if (!scores.size) plan.sources.forEach((_, index) => add(index, 0));
  return [...scores].sort((a, b) => b[1] - a[1] || a[0] - b[0]).map(([index]) => index);
}

/**
 * The pages a chapter's checker reads: those the writer's rows name, those of the facts the rows
 * tell and of the facts that belong to the chapter, but never for a fact marked reviewer_only,
 * whose pages the worker cannot read: that fact is held to the plan's wording instead.
 */
function checkerSourceOrder(plan, key, chapter, belongs) {
  const facts = plan.must_verify ?? [];
  const scores = new Map();
  const add = (index, score) => Number.isInteger(index) && plan.sources[index] && scores.set(index, (scores.get(index) ?? 0) + score);
  const factPages = (index, score) => {
    const fact = facts[index];
    if (fact && !fact.reviewer_only) for (const source of fact.sources ?? []) add(source, score);
  };
  for (const row of chapter.claims ?? []) {
    add(row.source, 3);
    if (Number.isInteger(row.fact)) factPages(row.fact, 2);
  }
  facts.forEach((_, index) => {
    if (belongs[index].includes(key)) factPages(index, 1);
  });
  // Rows that name no page and facts that meet no point: the pages the writer read, less those
  // only a reviewer_only fact cites.
  if (!scores.size) {
    const planOnly = new Set(facts.filter((fact) => fact?.reviewer_only).flatMap((fact) => fact.sources ?? []));
    const cited = new Set(facts.filter((fact) => fact && !fact.reviewer_only).flatMap((fact) => fact.sources ?? []));
    return writerSourceOrder(plan, key, belongs).filter((index) => !planOnly.has(index) || cited.has(index));
  }
  return [...scores].sort((a, b) => b[1] - a[1] || a[0] - b[0]).map(([index]) => index);
}

// --- the chapters on disk ------------------------------------------------------------------------

const chapterFile = (automation, state, key) => path.join(automation.workdir(state.slug), STORY_CHAPTERS_DIR, `${key}.json`);
export const readChapter = (automation, state, key) => readJson(chapterFile(automation, state, key), null);
const saveChapter = (automation, state, chapter) => atomicWrite(chapterFile(automation, state, chapter.key), `${JSON.stringify(chapter, null, 2)}\n`);

function readChapters(automation, state) {
  return Object.fromEntries(CHAPTER_KEYS.map((key) => [key, readChapter(automation, state, key)]).filter(([, chapter]) => chapter));
}

const linesOf = (chapter) => (chapter?.scenes ?? []).flatMap((scene) => scene.lines ?? []);
const chapterNarration = (chapter) => linesOf(chapter).map((line) => line.text);

function entryOf(state, key) {
  state.story.chapters ??= {};
  state.story.chapters[key] ??= { written: 0, lint: null, lint_fixes: 0, checked: false, check_rounds: 0, listened: false };
  return state.story.chapters[key];
}

function seriesInfo(automation, state) {
  return readJson(path.join(docDir(state.slug, automation.ctx.root), "series.json"));
}

// --- the writer's answer ---------------------------------------------------------------------------

/**
 * The scene ids of a chapter's answer: the writer's own where it is "<key>-…" and unique (so a
 * fix keeps the ids the claim rows and the keyframes know), else the next free "<key>-NN"; the
 * outro card is "now-outro".
 */
function chapterSceneIds(key, scenes) {
  const own = new RegExp(`^${key}-[a-z0-9]+(?:-[a-z0-9]+)*$`);
  const kept = new Set();
  const wanted = scenes.map((scene) => {
    const id = isObject(scene) && isText(scene.id) ? scene.id.trim() : "";
    if (!own.test(id) || kept.has(id)) return null;
    kept.add(id);
    return id;
  });
  let next = 0;
  const fresh = () => {
    let id;
    do id = `${key}-${String(++next).padStart(2, "0")}`;
    while (kept.has(id));
    kept.add(id);
    return id;
  };
  return scenes.map((scene, index) => {
    if (wanted[index]) return wanted[index];
    if (isObject(scene) && scene.template === "outro" && !kept.has(`${key}-outro`)) {
      kept.add(`${key}-outro`);
      return `${key}-outro`;
    }
    return fresh();
  });
}

/**
 * A chapter as the writer answered it, made the worker's: scene ids "<key>-…" (chapterSceneIds), every
 * shot a still, narrator lines only, line ids from the ones handed out (an id that is not, or
 * repeats, takes the next unused one), the claim rows pointing at the chapter's scenes. Answers
 * { chapter, lexicon }, { noMore: reason } or { problem }.
 */
export function readChapterAnswer(answer, { key, ids, cast = [], sources = 0, facts = 0 }) {
  if (!isObject(answer)) return { problem: "the answer is not an object" };
  if (answer.no_more === true) return { noMore: isText(answer.reason) ? answer.reason.trim() : "" };
  if (!isText(answer.title)) return { problem: "title (the chapter's name) is missing" };
  if (!Array.isArray(answer.scenes) || !answer.scenes.length) return { problem: "scenes is missing or empty" };
  const last = key === CHAPTER_KEYS.at(-1);
  const castIds = new Set(cast.map((figure) => figure.id));
  const unused = [...ids];
  const allowed = new Set(ids);
  const used = new Set();
  const renamed = new Map();
  const assigned = chapterSceneIds(key, answer.scenes);
  const scenes = [];
  let shots = 0;
  for (const [index, scene] of answer.scenes.entries()) {
    if (!isObject(scene)) return { problem: `scenes[${index}] is not an object` };
    const outro = scene.template === "outro";
    if (outro && !(last && index === answer.scenes.length - 1)) return { problem: "only the last chapter ends with an outro card, as its last scene" };
    if (!outro && scene.template !== "shot") return { problem: `scenes[${index}] is a "${scene.template}": a story's scene is a shot (the last chapter ends with an outro card)` };
    if (!Array.isArray(scene.lines) || !scene.lines.length) return { problem: `scenes[${index}] has no lines` };
    const lines = [];
    for (const line of scene.lines) {
      if (!isText(line?.text)) return { problem: `scenes[${index}] has a line without text` };
      let id = String(line.id ?? "");
      if (!allowed.has(id) || used.has(id)) {
        id = unused.find((each) => !used.has(each));
        if (!id) return { problem: "more lines than line_ids" };
      }
      used.add(id);
      const text = line.text.trim();
      lines.push({ id, text, ...(isText(line.say) ? { say: line.say.trim(), say_for: textHash(text) } : {}), ...(Number.isInteger(line.pause_after_ms) && line.pause_after_ms >= 0 && line.pause_after_ms <= 5000 ? { pause_after_ms: line.pause_after_ms } : {}) });
    }
    const id = assigned[index];
    if (!outro) shots += 1;
    if (isText(scene.id)) renamed.set(scene.id, id);
    if (outro) {
      const data = isObject(scene.data) ? scene.data : {};
      scenes.push({ id, template: "outro", data: { title: clip(isText(data.title) ? data.title : answer.title, 40), ...(isText(data.cta) ? { cta: clip(data.cta, 40) } : {}) }, lines });
      continue;
    }
    const data = isObject(scene.data) ? scene.data : {};
    if (!isText(data.prompt)) return { problem: `scenes[${index}] has no picture prompt` };
    const characters = Array.isArray(data.characters) ? [...new Set(data.characters.filter((each) => castIds.has(each)))].slice(0, 3) : [];
    scenes.push({
      id,
      template: "shot",
      data: {
        prompt: clip(data.prompt, 1000),
        camera: isText(data.camera) ? clip(data.camera, 120) : "slow drift",
        visual: "still",
        ...(characters.length ? { characters } : {}),
        ...(isText(data.negative) ? { negative: clip(data.negative, 400) } : {}),
        ...(data.transition === "dissolve" || data.transition === "cut" ? { transition: data.transition } : {}),
      },
      lines,
    });
  }
  if (!shots) return { problem: "the chapter has no shot" };
  const known = new Set(scenes.map((scene) => scene.id));
  const claims = (Array.isArray(answer.claims) ? answer.claims : [])
    .filter((row) => isObject(row) && isText(row.claim))
    .map((row) => {
      const scene = renamed.get(row.scene) ?? (known.has(row.scene) ? row.scene : scenes[0].id);
      return { claim: clip(row.claim, 300), scene, source: Number.isInteger(row.source) && row.source >= 0 && row.source < sources ? row.source : null, fact: Number.isInteger(row.fact) && row.fact >= 0 && row.fact < facts ? row.fact : null };
    });
  const thumbnail = renamed.get(answer.thumbnail_shot) ?? (known.has(answer.thumbnail_shot) ? answer.thumbnail_shot : null);
  const lexicon = isObject(answer.lexicon_additions) ? answer.lexicon_additions : {};
  return { chapter: { key, title: clip(answer.title, 30), scenes, claims, ...(thumbnail ? { thumbnail_shot: thumbnail } : {}) }, lexicon };
}

/** Claim ids per chapter: the chapter's letter and a number (h1, e12), kept across rewrites where a row keeps its id. */
function numberClaims(key, rows, previous = []) {
  const prefix = CHAPTER_OF.get(key).prefix;
  const own = (id) => isText(id) && id.startsWith(prefix) && /^\d+$/.test(id.slice(prefix.length));
  const numbers = [...previous, ...rows].filter((row) => own(row.id)).map((row) => Number(row.id.slice(prefix.length)));
  let next = Math.max(0, ...numbers) + 1;
  const seen = new Set();
  return rows.map((row) => {
    if (own(row.id) && !seen.has(row.id)) {
      seen.add(row.id);
      return row;
    }
    const id = `${prefix}${next++}`;
    seen.add(id);
    return { ...row, id };
  });
}

/** The writer's lexicon additions into the shared dictionary, by the rules flow.mjs's mergeLexicon keeps. */
function addTerms(root, additions) {
  if (!isObject(additions)) return [];
  const file = lexiconFile(root);
  const lexicon = readJson(file, { schema_version: 1, terms: {} });
  const added = [];
  for (const [term, spoken] of Object.entries(additions)) {
    if (!/^[A-Za-z0-9][A-Za-z0-9.+#'_-]{0,39}$/.test(term) || term in lexicon.terms) continue;
    if (spoken !== null && (typeof spoken !== "string" || !spoken.trim() || spoken.length > 80)) continue;
    lexicon.terms[term] = spoken === null ? null : spoken.trim();
    added.push(term);
  }
  if (added.length) atomicWrite(file, `${JSON.stringify(lexicon, null, 2)}\n`);
  return added;
}

// --- the merged script ---------------------------------------------------------------------------

/** The YouTube tags: the story, its subject and category, then its names, within YouTube's count. */
function storyTags(plan) {
  const tags = [];
  for (const tag of ["品牌故事", plan.subject, CATEGORY_TAGS[plan.category], ...(plan.names ?? [])]) {
    if (!isText(tag) || tags.includes(tag.trim()) || tags.length >= 12) continue;
    const next = [...tags, tag.trim()];
    if (next.reduce((sum, each) => sum + chars(each) + (/\s/.test(each) ? 2 : 0), 0) + next.length - 1 > 480) break;
    tags.push(tag.trim());
  }
  return tags;
}

/**
 * video.json from the chapters written so far: the worker's own fields from the plan and the
 * series (the voice, the shared look, the cast, the sources, the upload fields, the thumbnail on
 * the hook's chosen shot) and the chapters' scenes in order, each chapter's first scene carrying
 * its name and every scene the ids of the claims it rests on (a claim the checker found in no
 * page is cited by none, so the QA's facts item holds).
 */
export function composeStory({ slug, info, chapters, voice, drama = {}, root, videoId = null }) {
  const plan = info.plan;
  const target = Number(info.target_minutes) || 13;
  const scenes = [];
  for (const key of CHAPTER_KEYS) {
    const chapter = chapters[key];
    if (!chapter) continue;
    chapter.scenes.forEach((scene, index) => {
      const claims = (chapter.claims ?? []).filter((row) => row.scene === scene.id && row.verdict !== "NOT FOUND").map((row) => row.id);
      scenes.push({ id: scene.id, ...(index === 0 ? { chapter: chapter.title } : {}), template: scene.template, data: scene.data, ...(claims.length ? { claims } : {}), lines: scene.lines });
    });
  }
  const shots = scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id);
  const thumbnail = shots.includes(chapters.hook?.thumbnail_shot) ? chapters.hook.thumbnail_shot : shots[0];
  const guide = isText(plan.related_guide) && existsSync(contentPackFile(plan.related_guide, root)) ? plan.related_guide : null;
  const look = info.look ?? {};
  return {
    schema_version: 1,
    slug,
    format: "drama",
    // A brand story's place among the site's videos (/admin/videos filters by it).
    category: "story",
    ...(guide ? { source_guide: guide } : {}),
    target_minutes: [Math.max(1, target - TARGET_SPREAD.below), target + TARGET_SPREAD.above],
    voice,
    look: { preset: "custom", style: clip(look.style ?? "", 600), negative: clip(look.negative ?? "", 400), ...(isText(look.motion) ? { motion: clip(look.motion, 300) } : {}) },
    characters: info.characters ?? [],
    series: { slug: info.slug, episode: info.episode, chapter: 1 },
    ...(drama.music_enabled === false ? {} : { music: { prompt: STORY_MUSIC, gain_db: -20, duck_db: -10 } }),
    subtitles: { burn_in: true, style: "drama" },
    youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: clip(info.title ?? plan.subject, 100), description: `${info.logline || plan.subject}\n\n${plan.question}`, tags: storyTags(plan), video_id: videoId },
    ...(thumbnail ? { thumbnail: { template: "thumb", data: { headline: clipHeadline(plan.thumbnail?.headline ?? plan.subject), tag: "品牌故事", shot: thumbnail } } } : {}),
    sources: plan.sources.map((source) => ({ title: clip(source.publisher || source.url, 200), url: source.url, checked_on: source.checked })),
    assets: [],
    scenes,
  };
}

/** claims.md: every chapter's rows, "id｜claim｜URL｜checked｜scene｜verdict". */
function claimsMarkdown(info, chapters) {
  const out = [`# 主張表：${info.title}`, "", "企劃的必查事實在匯入前已由第二個人對過來源；這張表是逐章撰稿與查核的紀錄。", ""];
  for (const key of CHAPTER_KEYS) {
    const chapter = chapters[key];
    if (!chapter) continue;
    out.push(`## ${chapter.title}（${key}）`, "");
    for (const row of chapter.claims ?? []) {
      const source = Number.isInteger(row.source) ? info.plan.sources[row.source] : null;
      out.push([row.id, row.claim, source?.url ?? "", source?.checked ?? "", row.scene, row.verdict ?? "待查"].map((cell) => String(cell).replace(/[|｜\n]/g, "／")).join("｜"));
    }
    out.push("");
  }
  return out.join("\n");
}

/** verify-1.md: the six chapters' checks, one claim table each, as the QA's facts item reads it. */
function verifyMarkdown(info, chapters) {
  const out = [`# 查核：${info.title}（品牌故事，逐章查核）`, "", "企劃的必查事實在匯入前由第二個人對過來源；這一輪確認稿子說的跟企劃一樣，並在來源頁面的段落裡找撰稿模型自己加的數字、年份與人名。", ""];
  const counts = {};
  for (const key of CHAPTER_KEYS) {
    const chapter = chapters[key];
    if (!chapter) continue;
    out.push(`## ${chapter.title}（${key}）`, "", "| # | 主張 | 場景 | 來源 | 判定 | 說明 |", "| --- | --- | --- | --- | --- | --- |");
    for (const row of chapter.claims ?? []) {
      const verdict = row.verdict ?? "UNCHECKED";
      counts[verdict] = (counts[verdict] ?? 0) + 1;
      const source = Number.isInteger(row.source) ? info.plan.sources[row.source]?.url ?? "" : "";
      out.push(`| ${[row.id, row.claim, row.scene, source, verdict, row.note ?? ""].map((cell) => String(cell).replace(/[|｜\n]/g, "／")).join(" | ")} |`);
    }
    // The checker's own words, with no bar left in them: the QA's facts item reads every table
    // row of this file, and the rows above are the verdicts that count.
    out.push("", String(chapter.report ?? "").replace(/[|｜]/g, "／"), "");
  }
  out.push("## 統計", "", Object.entries(counts).map(([verdict, count]) => `${verdict} ${count}`).join("、") || "沒有主張", "");
  return out.join("\n");
}

/** The lint context of a draft that is not on disk yet: loadProject's, read from the video's directory. */
function draftContext(root, slug, doc) {
  const dir = docDir(slug, root);
  return {
    lexicon: readJson(lexiconFile(root), emptyLexicon()),
    brief: readText(path.join(dir, "brief.md")),
    series: readJson(path.join(dir, "series.json"), null),
    pack: doc.source_guide ? readJson(contentPackFile(doc.source_guide, root), null) : undefined,
    translations: {},
    others: [],
  };
}

const SCENE_PATH = /^scenes\[(\d+)\]/;

/**
 * Lint the chapters written so far, and when all six are there write video.json and claims.md
 * and lint them as `status` does. Every error inside a chapter's scenes is that chapter's (kept
 * in auto.json for the writer's next fix); an error outside them on the whole script is the
 * worker's (returned as `other`), and on a partial one it is only the missing chapters.
 */
async function relint(automation, state) {
  const { root } = automation.ctx;
  const info = seriesInfo(automation, state);
  const chapters = readChapters(automation, state);
  const complete = CHAPTER_KEYS.every((key) => chapters[key]);
  const dir = docDir(state.slug, root);
  const file = path.join(dir, "video.json");
  const recorded = readJson(file, null)?.youtube?.video_id ?? null;
  const doc = composeStory({ slug: state.slug, info, chapters, voice: automation.voice("drama"), drama: automation.settings.drama ?? {}, root, videoId: recorded });
  let errors;
  if (complete) {
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`);
    writeFileSync(path.join(dir, "claims.md"), claimsMarkdown(info, chapters));
    // script.md follows the lines at once: the local approval of the script gate is bound to it,
    // so a line changed after it (a length fix, the owner's note on the narration) voids it.
    writeScreenplay(dir, doc);
    errors = lintProject(loadProject({ slug: state.slug, root })).errors;
  } else {
    errors = lintVideo(doc, draftContext(root, state.slug, doc)).errors;
  }
  // Which chapter each scene index of the draft belongs to.
  const owner = [];
  for (const key of CHAPTER_KEYS) for (const _ of chapters[key]?.scenes ?? []) owner.push(key);
  const byChapter = {};
  const other = [];
  for (const error of errors) {
    const match = SCENE_PATH.exec(error.path);
    const key = match ? owner[Number(match[1])] : null;
    if (key) (byChapter[key] ??= []).push(`${error.path}: ${error.message}`);
    else other.push(`${error.path}: ${error.message}`);
  }
  for (const key of Object.keys(chapters)) entryOf(state, key).lint = byChapter[key] ?? null;
  return { complete, other: complete ? other : [], doc, chapters, info };
}

// --- the steps ------------------------------------------------------------------------------------

/**
 * Start the story the site says is next, under the video slug its plan fixed (the site refuses
 * any other with 409 video_series_story_slug), and draft it here.
 */
export async function startStory(automation, job) {
  const { series, episode } = job;
  const slug = episode?.slug;
  if (!isText(slug)) return automation.later(`story series ${series.slug}: story ${episode?.number ?? "?"} has no planned video slug; the import sets one`);
  let started;
  try {
    started = await automation.api.episodeStart(series.slug, episode.number, slug);
  } catch (error) {
    // A slug another video holds, a story that is no longer ready: nothing here changes that.
    if (error instanceof AutomationError && error.status === 409) return automation.later(`story series ${series.slug}: the site refused to start story ${episode.number} (${slug}): ${error.message}`);
    throw error;
  }
  return draftStory(automation, started, series);
}

/**
 * The story's files and state, from the episode the site started: series.json (what lint reads
 * for a story: kind, names, the cast, the tier; and the plan, the look, the image model), brief.md
 * (the sections lint wants and one outline), auto.json, and the outline approved here.
 */
export async function draftStory(automation, started, job = {}) {
  const { request = {}, episode = {} } = started;
  const series = { ...job, ...(started.context?.series ?? {}) };
  const plan = episode.beats ?? {};
  const slug = request.slug ?? episode.slug;
  const state = {
    slug,
    title: clip(episode.title || request.title || slug, 200),
    status: "active",
    created_at: automation.ctx.now().toISOString(),
    format: "drama",
    category: "story",
    request_id: request.id ?? null,
    premise: request.premise ?? plan.question ?? "",
    style_preset: "custom",
    target_minutes: Number(series.target_minutes) || 13,
    source_guide: isText(plan.related_guide) ? plan.related_guide : null,
    series: { slug: series.slug, episode: episode.number, chapter: 1, kind: STORY_KIND, visual_tier: "stills", compilation: false, hands_off: true },
    story: { id: plan.id ?? null, chapters: {}, resizes: 0, length: null, owner_note: null, audio_review: null },
    source_urls: [],
    replans: 0,
    verify_rounds: 0,
    verified: false,
    listener_done: false,
    retakes: 0,
    rewrites: 0,
    prompt_fixes: {},
    chosen: "A",
    notes: [],
  };
  const problem = planShapeProblem(plan) ?? (isText(series.look?.style) ? null : "the story series has no shared look (look.style); set it on /admin/videos");
  if (problem) {
    automation.persist(state);
    return automation.block(state, `the story cannot be written: ${problem}`);
  }
  const dir = docDir(slug, automation.ctx.root);
  mkdirSync(dir, { recursive: true });
  const cast = storyCast(plan, automation.voice("drama"));
  writeFileSync(path.join(dir, "series.json"), `${JSON.stringify(storySeriesFile({ series, episode, plan, cast }), null, 2)}\n`);
  writeFileSync(path.join(dir, "brief.md"), storyBrief({ episode, plan, cast }));
  const workdir = automation.workdir(slug);
  automation.persist(state);
  await approve({ gate: "outline", docDir: dir, workdir, now: automation.ctx.now(), note: OUTLINE_NOTE });
  await automation.report(state, "outline approved");
  return `story ${series.slug}: ${slug} (${plan.id ?? `story ${episode.number}`}) started from its plan; it is written, checked and heard one chapter at a time`;
}

/**
 * One step of a story, or undefined when the step is one every drama shares (look, tts, the
 * narration check, keyframes, the storyboard, render, clips, music, assemble, captions, the final
 * cut, the package, the upload), which flow.mjs takes.
 */
export async function advanceStory(automation, state, next) {
  if (!state.story) return undefined;
  if (next === "brief") return undefined;
  if (next === "outline approved") {
    await approve({ gate: "outline", docDir: docDir(state.slug, automation.ctx.root), workdir: automation.workdir(state.slug), now: automation.ctx.now(), note: OUTLINE_NOTE });
    return `${state.slug}: the story's outline approved again (${OUTLINE_NOTE})`;
  }
  // A chapter lint refuses is fixed before the next is written, so the next goes on from its final words.
  const failing = CHAPTER_KEYS.find((key) => entryOf(state, key).lint?.length && existsSync(chapterFile(automation, state, key)));
  if (failing) return fixChapterLint(automation, state, failing);
  const unwritten = CHAPTER_KEYS.find((key) => !entryOf(state, key).written || !existsSync(chapterFile(automation, state, key)));
  if (unwritten) return writeChapter(automation, state, unwritten);
  if (next === "script passes lint") {
    // Everything is written and no chapter is known to fail: the script on disk is behind (the
    // shared dictionary changed, a file was touched). Merge and lint it again.
    const result = await relint(automation, state);
    automation.persist(state);
    if (result.other.length) return automation.block(state, `the merged story fails lint outside its chapters: ${result.other.slice(0, 3).join("; ")}`);
    const again = CHAPTER_KEYS.filter((key) => entryOf(state, key).lint?.length);
    return again.length ? `${state.slug}: the merged story fails lint in ${again.join(", ")}; the writer fixes them chapter by chapter` : `${state.slug}: the story merged again and passes lint`;
  }
  const unchecked = CHAPTER_KEYS.find((key) => !entryOf(state, key).checked);
  if (unchecked) return checkChapter(automation, state, unchecked);
  const unheard = CHAPTER_KEYS.find((key) => !entryOf(state, key).listened);
  if (unheard) return listenChapter(automation, state, unheard);
  // Every chapter is checked and heard: flow.mjs must never fall back to its whole-script check.
  if (!state.verified || !state.listener_done) {
    Object.assign(state, { verified: true, listener_done: true });
    automation.persist(state);
  }
  if (next === "script approved") return approveScript(automation, state);
  if (next === "narration approved") {
    const length = await checkLength(automation, state);
    if (length !== undefined) return length;
    return narrationSentBack(automation, state);
  }
  return undefined;
}

/** What every writer call of a chapter carries (docs/videos/STORY.md §為什麼逐章寫稿). */
async function writerPayload(automation, state, key, extra = {}) {
  const info = seriesInfo(automation, state);
  const plan = info.plan;
  const index = CHAPTER_OF.get(key).index;
  const belongs = factChapters(plan);
  const budget = chapterBudgets(info.target_minutes)[index];
  const previous = index > 0 ? readChapter(automation, state, CHAPTER_KEYS[index - 1]) : null;
  const names = plan.names ?? [];
  const anchors = anchorsFor([plan.chapters[index].point, ...(plan.must_verify ?? []).filter((_, each) => belongs[each].includes(key)).map((fact) => fact.claim), ...(extra.current ? chapterNarration(extra.current) : [])], names);
  const lexicon = readJson(lexiconFile(automation.ctx.root), emptyLexicon());
  return {
    today: automation.ctx.now().toISOString().slice(0, 10),
    slug: state.slug,
    chapter: { key, number: index + 1, of: CHAPTER_KEYS.length, label: CHAPTER_OF.get(key).label, point: plan.chapters[index].point, budget: { seconds: budget.seconds, chars: budget.chars, shots: budget.shots } },
    plan: { id: plan.id, subject: plan.subject, category: plan.category, region: plan.region, title: info.title, logline: info.logline, question: plan.question, takeaway: plan.takeaway, chapters: plan.chapters, thumbnail: plan.thumbnail ?? null, image_notes: plan.image_notes ?? "", sensitivity: plan.sensitivity ?? "none", related_guide: plan.related_guide ?? null },
    facts: factsPayload(plan, belongs),
    caveats: plan.caveats ?? "",
    sources: await sourcesPayload(automation, state, plan, writerSourceOrder(plan, key, belongs), anchors),
    previous_lines: previous ? chapterNarration(previous).slice(-4) : [],
    look: info.look,
    cast: (plan.cast ?? []).map(({ id, role, appearance }) => ({ id, role, appearance })),
    names,
    story_rules: STORY_RULES,
    script_writing: automation.reference().script_writing,
    lexicon: Object.keys(lexicon.terms ?? {}),
    ...extra,
  };
}

/** Fresh line ids for a chapter: none that any chapter uses. */
function lineIds(automation, state, count) {
  const scenes = Object.values(readChapters(automation, state)).flatMap((chapter) => chapter.scenes ?? []);
  return automation.freshIds(state, { scenes }, count);
}

const idsFor = (budgetChars) => Math.ceil(budgetChars / 14) + 12;

/**
 * Keep a chapter the writer answered, merge its lexicon terms, and lint what is written so far.
 * A lint fix (`keepRows`) keeps the chapter's claim rows, verdicts and check report where their
 * scenes are still there; a rewrite takes the writer's new rows, to be checked again.
 */
async function keepChapter(automation, state, key, read, { previous = null, keepRows = false } = {}) {
  const before = previous?.claims ?? [];
  const exists = (row) => read.chapter.scenes.some((scene) => scene.id === row.scene);
  const rows = keepRows && before.length ? before.filter(exists) : read.chapter.claims.length ? read.chapter.claims : before.filter(exists);
  const chapter = { ...read.chapter, claims: numberClaims(key, rows, before), ...(keepRows && previous?.report ? { report: previous.report } : {}) };
  const added = addTerms(automation.ctx.root, read.lexicon);
  if (added.length) state.lexicon_added = [...new Set([...(state.lexicon_added ?? []), ...added])];
  saveChapter(automation, state, chapter);
  return { chapter, lint: await relint(automation, state) };
}

const describeChapter = (chapter) => `${chapter.scenes.filter((scene) => scene.template === "shot").length} shots, ${chapterNarration(chapter).reduce((sum, text) => sum + spokenUnits(text), 0)} characters`;

/** Write one chapter (writer:story), in order; when the sixth is there, the script is merged and linted. */
async function writeChapter(automation, state, key) {
  const info = seriesInfo(automation, state);
  const index = CHAPTER_OF.get(key).index;
  const budget = chapterBudgets(info.target_minutes)[index];
  const ids = lineIds(automation, state, idsFor(budget.chars));
  const payload = await writerPayload(automation, state, key, { line_ids: ids });
  const answer = await automation.stage("writer", state.slug, payload, WRITER_TOKENS, "drama", STORY_VARIANT);
  const read = readChapterAnswer(answer, { key, ids, cast: info.characters ?? [], sources: info.plan.sources.length, facts: (info.plan.must_verify ?? []).length });
  if (read.problem || read.noMore !== undefined) return automation.retryLater(state, "writer", `chapter ${key}: ${read.problem ?? "the writer answered no_more for a chapter not yet written"}`);
  automation.cleared(state, "writer");
  const entry = entryOf(state, key);
  const { chapter, lint } = await keepChapter(automation, state, key, read);
  Object.assign(entry, { written: entry.written + 1, checked: false, check_rounds: 0, listened: false });
  automation.persist(state);
  const line = `${state.slug}: chapter ${index + 1}/${CHAPTER_KEYS.length} (${key}) written: ${describeChapter(chapter)}`;
  if (lint.other.length) return automation.block(state, `the merged story fails lint outside its chapters: ${lint.other.slice(0, 3).join("; ")}`);
  if (entry.lint?.length) return `${line}; ${entry.lint.length} lint errors in it go back to the writer`;
  if (!lint.complete) return line;
  const failing = CHAPTER_KEYS.filter((each) => entryOf(state, each).lint?.length);
  if (failing.length) return `${line}; the six are merged, and lint sends ${failing.join(", ")} back to the writer`;
  await automation.report(state, "script passes lint");
  return `${line}; the six are merged into video.json and claims.md and the script passes lint`;
}

/** Send a chapter's lint errors back to the writer, STORY_LINT_FIXES times, then the video waits for a person. */
async function fixChapterLint(automation, state, key) {
  const entry = entryOf(state, key);
  if (entry.lint_fixes >= STORY_LINT_FIXES) return automation.block(state, `chapter ${key} still fails lint after ${entry.lint_fixes} fixes: ${entry.lint.slice(0, 3).join("; ")}`);
  const info = seriesInfo(automation, state);
  const current = readChapter(automation, state, key);
  const fresh = lineIds(automation, state, 30);
  const own = linesOf(current).map((line) => line.id);
  const answer = await automation.stage("writer", state.slug, await writerPayload(automation, state, key, { current, lint_errors: entry.lint, line_ids: fresh }), WRITER_TOKENS, "drama", STORY_VARIANT);
  const read = readChapterAnswer(answer, { key, ids: [...own, ...fresh], cast: info.characters ?? [], sources: info.plan.sources.length, facts: (info.plan.must_verify ?? []).length });
  if (read.problem || read.noMore !== undefined) return automation.retryLater(state, "writer", `chapter ${key}'s lint fix: ${read.problem ?? "no_more is not a fix"}`);
  automation.cleared(state, "writer");
  const errors = entry.lint.length;
  entry.lint_fixes += 1;
  const { lint } = await keepChapter(automation, state, key, read, { previous: current, keepRows: true });
  automation.persist(state);
  if (lint.other.length) return automation.block(state, `the merged story fails lint outside its chapters: ${lint.other.slice(0, 3).join("; ")}`);
  const left = entry.lint?.length ?? 0;
  return `${state.slug}: chapter ${key} fixed for ${errors} lint errors (round ${entry.lint_fixes})${left ? `; ${left} remain` : lint.complete ? "; the script passes lint" : ""}`;
}

/**
 * A patch to a chapter's lines: `patch` is line id to new text, `drop` the ids to take out. A
 * line of another chapter is refused; `guard(before, after)` may refuse a change (the listener
 * may not touch a figure), `mayDrop(line)` a drop. A shot left with no line goes; the chapter may
 * not lose every shot. Answers { chapter, changed, dropped, refused }.
 */
export function applyPatch(chapter, { patch = {}, drop = [] } = {}, { guard = () => [], mayDrop = () => true } = {}) {
  const next = structuredClone(chapter);
  const lines = new Map(next.scenes.flatMap((scene) => scene.lines.map((line) => [line.id, { line, scene }])));
  const changed = [];
  const dropped = [];
  const refused = [];
  for (const [id, text] of Object.entries(isObject(patch) ? patch : {})) {
    const found = lines.get(id);
    if (!found) {
      refused.push(`${id}: not a line of this chapter`);
      continue;
    }
    if (!isText(text)) {
      refused.push(`${id}: the new text is empty`);
      continue;
    }
    const after = text.trim();
    if (after === found.line.text) continue;
    const problems = guard(found.line.text, after);
    if (problems.length) {
      refused.push(`${id}: ${problems.join("; ")}`);
      continue;
    }
    found.line.text = after;
    // The say form was written for the old words.
    delete found.line.say;
    delete found.line.say_for;
    changed.push(id);
  }
  for (const id of Array.isArray(drop) ? drop.map(String) : []) {
    const found = lines.get(id);
    if (!found) {
      refused.push(`${id}: not a line of this chapter`);
      continue;
    }
    if (!mayDrop(found.line)) {
      refused.push(`${id}: may not be dropped (it holds a figure or a name)`);
      continue;
    }
    found.scene.lines = found.scene.lines.filter((line) => line.id !== id);
    dropped.push(id);
  }
  next.scenes = next.scenes.filter((scene) => scene.lines.length);
  if (!next.scenes.some((scene) => scene.template === "shot")) return { chapter, changed: [], dropped: [], refused: [...refused, "the patch would leave the chapter without a shot"] };
  return { chapter: next, changed, dropped, refused };
}

const VERDICTS = ["CONFIRMED", "PLAN", "CHANGED", "ATTRIBUTED", "NOT FOUND", "OUT OF SCOPE"];
const COUNTED = new Set(["CHANGED", "ATTRIBUTED", "NOT FOUND"]);

/** The checker's rows, each with a verdict it knows, pointing at scenes the chapter still has. */
function checkedRows(key, rows, chapter, previous, plan) {
  const scenes = new Set(chapter.scenes.map((scene) => scene.id));
  const known = new Map(previous.map((row) => [row.id, row]));
  const cleaned = rows
    .filter((row) => isObject(row) && isText(row.claim))
    .map((row) => {
      const verdict = String(row.verdict ?? "").toUpperCase().replace(/_/g, " ").trim();
      const before = known.get(row.id);
      return {
        ...(before ? { id: before.id } : {}),
        claim: clip(row.claim, 300),
        scene: scenes.has(row.scene) ? row.scene : before?.scene ?? chapter.scenes[0].id,
        source: Number.isInteger(row.source) && plan.sources[row.source] ? row.source : before?.source ?? null,
        fact: Number.isInteger(row.fact) && plan.must_verify?.[row.fact] ? row.fact : before?.fact ?? null,
        verdict: VERDICTS.includes(verdict) ? verdict : "UNCHECKED",
        ...(isText(row.note) ? { note: clip(row.note, 300) } : {}),
      };
    });
  return numberClaims(key, cleaned, previous);
}

/** Check one chapter (verifier:story, a fresh session): the patch and the chapter's rows of the claims table. */
async function checkChapter(automation, state, key) {
  const info = seriesInfo(automation, state);
  const plan = info.plan;
  const entry = entryOf(state, key);
  const index = CHAPTER_OF.get(key).index;
  const chapter = readChapter(automation, state, key);
  const belongs = factChapters(plan);
  const round = entry.check_rounds + 1;
  const anchors = anchorsFor([...chapterNarration(chapter), ...(chapter.claims ?? []).map((row) => row.claim), ...(plan.must_verify ?? []).filter((fact, each) => belongs[each].includes(key) && !fact.reviewer_only).map((fact) => fact.claim)], plan.names ?? []);
  const payload = {
    today: automation.ctx.now().toISOString().slice(0, 10),
    round,
    chapter: { key, number: index + 1, of: CHAPTER_KEYS.length, title: chapter.title, point: plan.chapters[index].point },
    plan: { title: info.title, question: plan.question, takeaway: plan.takeaway, chapters: plan.chapters },
    scenes: chapter.scenes.map((scene) => ({ id: scene.id, lines: scene.lines.map(({ id, text }) => ({ id, text })) })),
    claims: chapter.claims ?? [],
    facts: factsPayload(plan, belongs),
    caveats: plan.caveats ?? "",
    sources: await sourcesPayload(automation, state, plan, checkerSourceOrder(plan, key, chapter, belongs), anchors),
  };
  const answer = await automation.stage("verifier", state.slug, payload, CHECKER_TOKENS, "drama", STORY_VARIANT);
  if (!isObject(answer) || !Array.isArray(answer.claims)) return automation.retryLater(state, "verifier", `chapter ${key}: the check answered without its claims rows`);
  const patched = applyPatch(chapter, { patch: answer.patch ?? {}, drop: answer.drop ?? [] });
  if (!patched.changed.length && !patched.dropped.length && patched.refused.some((problem) => problem.includes("without a shot"))) return automation.retryLater(state, "verifier", `chapter ${key}: the check would drop the whole chapter`);
  automation.cleared(state, "verifier");
  const rows = checkedRows(key, answer.claims, patched.chapter, chapter.claims ?? [], plan);
  const changed = rows.filter((row) => COUNTED.has(row.verdict)).length;
  saveChapter(automation, state, { ...patched.chapter, claims: rows, report: `### 第 ${round} 輪\n\n${isText(answer.report) ? answer.report.trim() : "（查核模型沒有寫報告）"}${patched.refused.length ? `\n\n沒有套用的修改：${patched.refused.join("；")}` : ""}` });
  const rounds = automation.settings.drama?.drama_max_verify_rounds ?? automation.settings.max_verify_rounds ?? 3;
  Object.assign(entry, { check_rounds: round, checked: changed <= CHANGED_FACTS_RECHECK || round >= rounds, changed });
  for (const problem of patched.refused) state.notes.push(`check of ${key} not applied: ${problem}`);
  const lint = await relint(automation, state);
  let done = "";
  if (CHAPTER_KEYS.every((each) => entryOf(state, each).checked)) {
    writeFileSync(path.join(docDir(state.slug, automation.ctx.root), "verify-1.md"), verifyMarkdown(info, readChapters(automation, state)));
    state.verified = true;
    state.verify_rounds = Math.max(state.verify_rounds ?? 0, 1);
    done = "; every chapter is checked (verify-1.md)";
  }
  automation.persist(state);
  if (lint.other.length) return automation.block(state, `the merged story fails lint outside its chapters: ${lint.other.slice(0, 3).join("; ")}`);
  const tally = VERDICTS.map((verdict) => [verdict, rows.filter((row) => row.verdict === verdict).length]).filter(([, count]) => count).map(([verdict, count]) => `${count} ${verdict}`).join(", ");
  return `${state.slug}: chapter ${key} checked (round ${round}): ${patched.changed.length} lines changed, ${patched.dropped.length} dropped; ${tally || "no claims"}${entry.checked ? "" : `; ${changed} facts changed, so a fresh check follows`}${done}`;
}

/** A line the listener may drop: one that holds no figure and no Latin word. */
const holdsNoFact = (line) => !/[0-9０-９]/.test(line.text) && !/[A-Za-z]/.test(line.text);

/** Hear one chapter (listener:story): a patch, every figure, Latin word and dictionary term kept. */
async function listenChapter(automation, state, key) {
  const entry = entryOf(state, key);
  const index = CHAPTER_OF.get(key).index;
  const chapter = readChapter(automation, state, key);
  const previous = index > 0 ? readChapter(automation, state, CHAPTER_KEYS[index - 1]) : null;
  const following = index + 1 < CHAPTER_KEYS.length ? readChapter(automation, state, CHAPTER_KEYS[index + 1]) : null;
  const lexicon = readJson(lexiconFile(automation.ctx.root), emptyLexicon());
  const payload = {
    chapter: { key, number: index + 1, of: CHAPTER_KEYS.length, title: chapter.title },
    scenes: chapter.scenes.map((scene) => ({ id: scene.id, lines: scene.lines.map(({ id, text }) => ({ id, text })) })),
    previous_lines: previous ? chapterNarration(previous).slice(-3) : [],
    next_lines: following ? chapterNarration(following).slice(0, 2) : [],
    script_writing: automation.reference().script_writing,
    ...(isText(state.story.owner_note) ? { owner_note: state.story.owner_note } : {}),
  };
  const answer = await automation.stage("listener", state.slug, payload, LISTENER_TOKENS, "drama", STORY_VARIANT);
  if (!isObject(answer) || (answer.patch !== undefined && !isObject(answer.patch)) || (answer.drop !== undefined && !Array.isArray(answer.drop))) return automation.retryLater(state, "listener", `chapter ${key}: the edit is not a patch`);
  automation.cleared(state, "listener");
  const patched = applyPatch(chapter, { patch: answer.patch ?? {}, drop: answer.drop ?? [] }, { guard: (before, after) => rewriteProblems(before, after, { lexicon }), mayDrop: holdsNoFact });
  saveChapter(automation, state, patched.chapter);
  entry.listened = true;
  for (const problem of patched.refused) state.notes.push(`listener's edit of ${key} dropped: ${problem}`);
  const lint = await relint(automation, state);
  if (CHAPTER_KEYS.every((each) => entryOf(state, each).listened)) {
    state.listener_done = true;
    state.story.owner_note = null;
  }
  automation.persist(state);
  if (lint.other.length) return automation.block(state, `the merged story fails lint outside its chapters: ${lint.other.slice(0, 3).join("; ")}`);
  return `${state.slug}: chapter ${key} heard: ${patched.changed.length} lines reworded, ${patched.dropped.length} dropped${patched.refused.length ? `, ${patched.refused.length} edits refused` : ""}`;
}

/** The script gate every drama has (PR #870): a story has none, so it is approved here with the reason. */
async function approveScript(automation, state) {
  const dir = docDir(state.slug, automation.ctx.root);
  writeScreenplay(dir, JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8")));
  await approve({ gate: "script", docDir: dir, workdir: automation.workdir(state.slug), now: automation.ctx.now(), note: SCRIPT_NOTE });
  await automation.report(state, "script approved");
  return `${state.slug}: a story has no script gate; the screenplay is approved here (${SCRIPT_NOTE})`;
}

/** Each chapter's measured seconds on a timeline, from its scenes' ids ("<key>-NN"). */
export function chapterSeconds(timeline) {
  const seconds = Object.fromEntries(CHAPTER_KEYS.map((key) => [key, 0]));
  for (const scene of timeline.scenes ?? []) {
    const key = String(scene.id).split("-")[0];
    if (key in seconds) seconds[key] += (scene.end_frame - scene.start_frame) / FPS;
  }
  return seconds;
}

/**
 * The narration as synthesized, against the band around the target. Out of it, the writer cuts
 * from the longest chapter or adds to the thinnest (the least of its share), LENGTH_FIX_ROUNDS
 * times; after that, or when the passages hold nothing more, the video waits for the owner with
 * the measured length. Undefined when the length is fine (the narration check goes on).
 */
async function checkLength(automation, state) {
  const timeline = readJson(path.join(automation.workdir(state.slug), "timeline.json"), null);
  if (!timeline?.total_frames) return undefined;
  const info = seriesInfo(automation, state);
  const target = Number(info.target_minutes) || 13;
  const [low, high] = lengthBand(target);
  const seconds = timeline.total_frames / FPS;
  state.story.length = { seconds: Math.round(seconds), at: automation.ctx.now().toISOString() };
  if (seconds >= low && seconds <= high) {
    automation.persist(state);
    return undefined;
  }
  const long = seconds > high;
  const measured = `the narration measures ${formatClock(seconds)}, ${long ? "over" : "under"} ${formatClock(long ? high : low)}`;
  if ((state.story.resizes ?? 0) >= LENGTH_FIX_ROUNDS) return automation.block(state, `${measured} after ${state.story.resizes} length fixes; a story runs ${formatClock(low)} to ${formatClock(high)}: the owner decides`);
  const measuredBy = chapterSeconds(timeline);
  const budgets = Object.fromEntries(chapterBudgets(target).map((budget) => [budget.key, budget.seconds]));
  // The hook stays within its 30 seconds whatever the total does.
  const resizable = CHAPTER_KEYS.filter((each) => each !== "hook");
  const key = long
    ? resizable.reduce((best, each) => (measuredBy[each] > measuredBy[best] ? each : best))
    : resizable.reduce((best, each) => (measuredBy[each] / budgets[each] < measuredBy[best] / budgets[best] ? each : best));
  const wanted = target * 60 - seconds;
  const limit = measuredBy[key] * (long ? RESIZE_SHARE.cut : RESIZE_SHARE.add);
  const delta = Math.round(long ? Math.max(wanted, -limit) : Math.min(wanted, Math.max(limit, 20)));
  return resizeChapter(automation, state, key, delta, measured);
}

/** The writer adds to or cuts from one chapter (writer:story with "resize"); it is checked and heard again. */
async function resizeChapter(automation, state, key, delta, measured) {
  const info = seriesInfo(automation, state);
  const current = readChapter(automation, state, key);
  const fresh = lineIds(automation, state, delta > 0 ? idsFor((delta * STORY_CPM) / 60) : 20);
  const own = linesOf(current).map((line) => line.id);
  const round = (state.story.resizes ?? 0) + 1;
  const payload = await writerPayload(automation, state, key, { current, resize: { seconds: delta, why: measured, round }, line_ids: fresh });
  const answer = await automation.stage("writer", state.slug, payload, WRITER_TOKENS, "drama", STORY_VARIANT);
  const read = readChapterAnswer(answer, { key, ids: [...own, ...fresh], cast: info.characters ?? [], sources: info.plan.sources.length, facts: (info.plan.must_verify ?? []).length });
  if (read.noMore !== undefined) {
    if (delta > 0) {
      state.notes.push(`length: ${measured}; the writer found nothing more to tell in ${key}: ${read.noMore}`);
      return automation.block(state, `${measured}, and the passages hold nothing more to tell in ${key} (${read.noMore || "no reason given"}): the owner decides, a shorter video or another story`);
    }
    return automation.retryLater(state, "writer", `chapter ${key}: no_more is not a cut`);
  }
  if (read.problem) return automation.retryLater(state, "writer", `chapter ${key}'s length fix: ${read.problem}`);
  automation.cleared(state, "writer");
  state.story.resizes = round;
  const entry = entryOf(state, key);
  await keepChapter(automation, state, key, read, { previous: current });
  // Whatever the writer added is checked and heard like the rest; a rewritten chapter starts its
  // lint fixes afresh.
  Object.assign(entry, { checked: false, check_rounds: 0, listened: false, lint_fixes: 0 });
  state.verified = false;
  state.listener_done = false;
  state.notes.push(`length: ${measured}; the writer ${delta > 0 ? "added about" : "cut about"} ${Math.abs(delta)} s ${delta > 0 ? "to" : "from"} ${key} (round ${round})`);
  automation.persist(state);
  return `${state.slug}: ${measured}; the writer ${delta > 0 ? "added to" : "cut"} ${key} (about ${Math.abs(delta)} s, round ${round}); it is checked and heard again`;
}

/**
 * The owner sent the narration back (a hands-off story's narration waits for the owner only when
 * Jev still flags lines): the listener goes over the six chapters with the owner's note, a
 * chapter a call. A note the listener could not act on the first time leaves the video for a person.
 */
async function narrationSentBack(automation, state) {
  const review = await automation.decision(state, "audio", path.join(automation.workdir(state.slug), "timeline.json"));
  if (review?.status !== "rejected") return undefined;
  if (state.story.audio_review === review.id) return automation.block(state, `the owner sent the narration back (${review.note ?? ""}) and the listener's pass changed nothing`);
  state.story.audio_review = review.id;
  state.story.owner_note = review.note ?? "";
  for (const key of CHAPTER_KEYS) entryOf(state, key).listened = false;
  state.listener_done = false;
  state.notes.push(`narration sent back: ${review.note ?? ""}`);
  automation.persist(state);
  return `${state.slug}: the owner sent the narration back (${review.note ?? ""}); the listener goes over the six chapters with the note`;
}

/**
 * Keyframes (or clips) that failed their checks, or a storyboard the owner sent back, go to the
 * writer as a prompt fix for the named shots alone (writer:story-fix): the answer is a patch of
 * those shots' prompt, camera and figures, linted before it is kept, so a name of the story in a
 * prompt is refused before anything is drawn. A failed character sheet is a patch of that
 * figure's appearance in series.json. STORY_PROMPT_FIX_ROUNDS per kind, as the drama's; then a
 * person.
 */
export async function fixStoryPrompts(automation, state, kind, { targets = null, ownerNote = null } = {}) {
  const found = targets ?? automation.failedTargets(state, kind);
  const summary = found.map((target) => `${target.id}: ${(target.problems ?? []).join("; ") || "failed"}`).join(" | ") || ownerNote || "no detail";
  const rounds = state.prompt_fixes?.[kind] ?? 0;
  if (rounds >= STORY_PROMPT_FIX_ROUNDS) return automation.block(state, `${kind} still fails after ${rounds} prompt fixes (${summary})`);
  const info = seriesInfo(automation, state);
  const plan = info.plan;
  // The tightest budget among the targets that carry one (media/keyframes.mjs prompt_budget_chars,
  // as flow.mjs fixPrompts sends it); each target keeps its own.
  const budgets = found.map((target) => target.prompt_budget_chars).filter((value) => typeof value === "number");
  const common = { fix: { kind, targets: found, problems: found.flatMap((target) => target.problems ?? []), owner_note: ownerNote, ...(budgets.length ? { prompt_budget_chars: Math.min(...budgets) } : {}) }, look: info.look, names: plan.names ?? [], cast: (plan.cast ?? []).map(({ id, role, appearance }) => ({ id, role, appearance })), image_notes: plan.image_notes ?? "", sensitivity: plan.sensitivity ?? "none", story_rules: STORY_RULES };
  let line;
  if (kind === "look") {
    const wanted = new Set(found.map((target) => target.id));
    const answer = await automation.stage("writer", state.slug, { ...common, characters: (info.characters ?? []).filter((figure) => wanted.has(figure.id)) }, FIX_TOKENS, "drama", STORY_FIX_VARIANT);
    if (!Array.isArray(answer?.characters)) return automation.retryLater(state, "writer", "the look fix answered without characters");
    const file = path.join(docDir(state.slug, automation.ctx.root), "series.json");
    const before = readFileSync(file, "utf8");
    const patched = [];
    info.characters = (info.characters ?? []).map((figure) => {
      const fix = answer.characters.find((each) => each?.id === figure.id && wanted.has(each.id) && isText(each.appearance));
      if (!fix) return figure;
      patched.push(figure.id);
      return { ...figure, appearance: clip(fix.appearance, 800) };
    });
    if (!patched.length) return automation.retryLater(state, "writer", `the look fix changed none of ${[...wanted].join(", ")}`);
    writeFileSync(file, `${JSON.stringify(info, null, 2)}\n`);
    const lint = await relint(automation, state);
    if (lint.other.length) {
      // An appearance lint refuses (a name of the story in it) is not kept.
      writeFileSync(file, before);
      await relint(automation, state);
      automation.persist(state);
      return automation.retryLater(state, "writer", `the look fix fails lint: ${lint.other.slice(0, 3).join("; ")}`);
    }
    line = `${state.slug}: look prompts fixed (round ${rounds + 1}) for ${patched.join(", ")}; look runs again next`;
  } else {
    const chapters = readChapters(automation, state);
    const where = new Map();
    for (const chapter of Object.values(chapters)) for (const scene of chapter.scenes) if (scene.template === "shot") where.set(scene.id, chapter.key);
    // The shots the checks failed; or, when the owner sent the storyboard back with a note alone,
    // every shot, of which the writer patches only those the note is about.
    const named = found.filter((target) => where.has(target.id));
    const offered = named.length ? named : isText(ownerNote) ? [...where.keys()].map((id) => ({ id, problems: [] })) : [];
    if (!offered.length) return automation.block(state, `${kind} failed for shots the script does not have (${summary})`);
    const shots = offered.map((target) => {
      const scene = chapters[where.get(target.id)].scenes.find((each) => each.id === target.id);
      return { id: scene.id, prompt: scene.data.prompt, camera: scene.data.camera ?? "", characters: scene.data.characters ?? [], lines: scene.lines.map((each) => each.text), problems: target.problems ?? [] };
    });
    const answer = await automation.stage("writer", state.slug, { ...common, shots }, FIX_TOKENS, "drama", STORY_FIX_VARIANT);
    if (!Array.isArray(answer?.shots)) return automation.retryLater(state, "writer", `the ${kind} fix answered without shots`);
    const wanted = new Set(offered.map((target) => target.id));
    const castIds = new Set((info.characters ?? []).map((figure) => figure.id));
    const touched = new Set();
    const patched = [];
    for (const fix of answer.shots) {
      if (!isObject(fix) || !wanted.has(fix.id) || !isText(fix.prompt)) continue;
      const key = where.get(fix.id);
      const scene = chapters[key].scenes.find((each) => each.id === fix.id);
      scene.data = { ...scene.data, prompt: clip(fix.prompt, 1000), ...(isText(fix.camera) ? { camera: clip(fix.camera, 120) } : {}) };
      if (Array.isArray(fix.characters)) {
        const characters = [...new Set(fix.characters.filter((each) => castIds.has(each)))].slice(0, 3);
        if (characters.length) scene.data.characters = characters;
        else delete scene.data.characters;
      }
      touched.add(key);
      patched.push(fix.id);
    }
    if (!patched.length) return automation.retryLater(state, "writer", `the ${kind} fix changed none of ${[...wanted].join(", ")}`);
    const before = new Map([...touched].map((key) => [key, readChapter(automation, state, key)]));
    for (const key of touched) saveChapter(automation, state, chapters[key]);
    await relint(automation, state);
    const failing = [...touched].filter((key) => entryOf(state, key).lint?.length);
    if (failing.length) {
      // A patched prompt lint refuses (a name of the story, a field too long) is not kept.
      const errors = failing.flatMap((key) => entryOf(state, key).lint).slice(0, 3);
      for (const chapter of before.values()) saveChapter(automation, state, chapter);
      await relint(automation, state);
      automation.persist(state);
      return automation.retryLater(state, "writer", `the ${kind} fix fails lint: ${errors.join("; ")}`);
    }
    line = `${state.slug}: ${kind} prompts fixed (round ${rounds + 1}) for ${patched.join(", ")}; ${kind} runs again next`;
  }
  automation.cleared(state, "writer");
  state.prompt_fixes = { ...(state.prompt_fixes ?? {}), [kind]: rounds + 1 };
  if (ownerNote) state.notes.push(`${kind} sent back: ${ownerNote}`);
  automation.persist(state);
  return line;
}

/** Every line id of a story's chapters, for a check that ids never repeat across chapters. */
export function storyLineIds(chapters) {
  return [...eachLine({ scenes: Object.values(chapters).flatMap((chapter) => chapter.scenes ?? []) })].map(({ line }) => line.id);
}
