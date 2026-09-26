// A long drama series on the host (docs/videos/SERIES.md): the worker plans the series' documents
// and starts its episodes in the order the site says. The site decides what is next
// (GET automation/series/next): the setting book, the whole-series outline, one chapter's
// detailed outline, or the next ready episode. A document is planned by the planner stage under a
// variant of its prompt and filed on the site as a new version that waits for the owner; sent
// back with a note, it is rewritten from that note while the site allows rewrites. An episode is
// started on the site under the video's slug, then drafted here from the chapter's beats: no
// outline options, the owner already approved the chapter.
import path from "node:path";

import { AutomationError, OUTPUT_INVALID } from "./client.mjs";

export const DOC_KINDS = ["setting", "outline", "chapter"];
const ANSWER_ATTEMPTS = 2;
const CHARACTER_KEYS = ["id", "name", "appearance"];
const BEAT_FIELDS = ["hook", "conflict", "turn", "cliffhanger"];

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;

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
  if (kind === "setting") {
    if (!Array.isArray(body.characters) || !body.characters.length) return "body_json.characters must list the cast";
    for (const character of body.characters) {
      if (!isObject(character) || !CHARACTER_KEYS.every((key) => isText(character[key]))) return "every character needs id, name and appearance";
      if (!/^[a-z][a-z0-9-]{1,23}$/.test(character.id)) return `character id "${character.id}" must be lowercase ascii, 2 to 24 characters`;
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
    if (episode.tension.at(-1) < 4) return `episode ${episode.number} must end tense (tension[4] >= 4)`;
    numbers.push(episode.number);
  }
  const expected = Array.from({ length: last - first + 1 }, (_, index) => first + index);
  if (JSON.stringify([...numbers].sort((a, b) => a - b)) !== JSON.stringify(expected)) return `chapter ${job.chapter_number} covers episodes ${first} to ${last}`;
  for (let index = 1; index < body.episodes.length; index++) {
    const before = body.episodes[index - 1].cliffhanger?.type;
    const now = body.episodes[index].cliffhanger?.type;
    if (before && now && before === now) return `episodes ${body.episodes[index - 1].number} and ${body.episodes[index].number} end on the same kind of cliffhanger (${now}); vary them`;
  }
  return null;
}

/** The cast as video.json wants it, from the setting book, by id. */
export function castFrom(setting) {
  const characters = Array.isArray(setting?.characters) ? setting.characters : [];
  return characters
    .filter((character) => isObject(character) && isText(character.id))
    .map((character) => {
      const entry = { id: character.id, name: String(character.name ?? character.id), appearance: String(character.appearance ?? "").slice(0, 800) };
      if (isObject(character.voice) && isText(character.voice.provider) && isText(character.voice.name)) {
        entry.voice = { provider: character.voice.provider, name: character.voice.name, ...(isText(character.voice.style) ? { style: character.voice.style.slice(0, 400) } : {}) };
      }
      if (isText(character.sheet_prompt)) entry.sheet_prompt = character.sheet_prompt.slice(0, 600);
      return entry;
    })
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

/**
 * An episode's brief.md, written from the chapter's row: the sections lint wants, and one outline
 * option, since the owner approved the chapter (no outline to pick).
 */
export function episodeBrief(series, episode, cast, beats) {
  const cliff = beats.cliffhanger && typeof beats.cliffhanger === "object" ? `${beats.cliffhanger.text ?? ""}（${beats.cliffhanger.type ?? ""}）` : String(beats.cliffhanger ?? "");
  const listed = (value) => (Array.isArray(value) && value.length ? value.join("、") : "無");
  const inFrame = Array.isArray(beats.characters) && beats.characters.length ? cast.filter((character) => beats.characters.includes(character.id)) : cast;
  return [
    `# ${series.title} 第 ${episode.number} 集：${episode.title}`,
    "",
    "## 故事前提",
    series.premise,
    "",
    `本集：${episode.logline || episode.title}`,
    "",
    "## 角色",
    ...(inFrame.length ? inFrame : cast).map((character) => `- ${character.id} ${character.name}：${character.appearance}`),
    "",
    "## 站主觀點",
    series.note || "依頻道立場與作品前提；沒有站主的親身經驗。",
    "",
    "## 幕",
    `- 開場鉤子：${beats.hook ?? ""}`,
    `- 主要衝突：${beats.conflict ?? ""}`,
    `- 轉折：${beats.turn ?? ""}`,
    `- 結尾懸念：${cliff}`,
    `- 埋下：${listed(beats.setups)}；回收：${listed(beats.payoffs)}`,
    `- 張力曲線：${Array.isArray(beats.tension) ? beats.tension.join("-") : "未定"}`,
    `- 場景：${listed(beats.locations)}`,
    ...(beats.theme ? [`- 主題句：${beats.theme}`] : []),
    "",
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
    },
    series_reference: refs.series,
    drama: refs.drama,
    drama_settings: automation.dramaPayload({ style_preset: series.style_preset }).drama_settings,
    ...(job.previous ? { previous: { body_md: job.previous.body_md, body_json: job.previous.body_json, owner_note: job.previous.note ?? "" } } : {}),
    ...(problem ? { previous_problem: problem } : {}),
  };
  if (job.kind === "setting") return base;
  const setting = context.setting ? { body_md: context.setting.body_md, body_json: context.setting.body_json } : null;
  if (job.kind === "outline") {
    return { ...base, setting, chapter_ranges: Array.from({ length: series.chapters }, (_, index) => chapterRange(series, index + 1)) };
  }
  const outline = context.outline?.body_json ?? {};
  const chapter = job.chapter_number;
  const chapters = Array.isArray(outline.chapters) ? outline.chapters : [];
  return {
    ...base,
    setting,
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

/** Plan one document with the planner and file it on the site; a line saying what happened. */
export async function planDocument(automation, job) {
  const { series } = job;
  const slug = `series-${series.slug}`;
  let problem = null;
  for (let attempt = 0; attempt < ANSWER_ATTEMPTS; attempt++) {
    let answer;
    try {
      answer = await automation.stage("planner", slug, documentPayload(automation, job, problem), 32_000, "drama", job.kind);
    } catch (error) {
      if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
      problem = error.message;
      continue;
    }
    problem = documentProblem(job.kind, answer, job);
    if (problem) continue;
    const doc = await automation.api.seriesDoc(series.slug, {
      kind: job.kind,
      chapter_number: job.kind === "chapter" ? job.chapter_number : 0,
      body_md: answer.body_md.endsWith("\n") ? answer.body_md : `${answer.body_md}\n`,
      body_json: answer.body_json,
    });
    const what = job.kind === "chapter" ? `chapter ${job.chapter_number}'s outline` : job.kind === "setting" ? "the setting book" : "the series outline";
    return `series ${series.slug}: ${what} ${job.previous ? "rewritten from the owner's note" : "planned"} (version ${doc.version}); it waits for the owner on /admin/videos`;
  }
  const kept = automation.keepAnswer(path.join(automation.workBase, "_series", series.slug), job.kind);
  return automation.later(`series ${series.slug}: the planner could not write ${job.kind === "chapter" ? `chapter ${job.chapter_number}` : `the ${job.kind}`} (${problem}${kept ? `; the answer is in ${kept}` : ""}); the next run tries again`);
}

/** Start the next episode on the site and draft it here from the chapter's beats. */
export async function startEpisode(automation, job) {
  const { series, episode } = job;
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
  if (!job) return null;
  if (job.kind === "episode") {
    if (!automation.room()) return null;
    return startEpisode(automation, job);
  }
  return planDocument(automation, job);
}
