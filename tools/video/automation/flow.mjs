// The automated pipeline, one unit of work at a time (docs/videos/AUTOMATION.md).
//
// `pipelineStatus` already knows the next step of a video from the hashes in its files. This
// adds what it cannot see (whether the fact-check rounds and the listener edit are done, how
// many retakes were tried, what the owner wrote when sending something back) in
// <workdir>/<slug>/auto.json, and does that step: a writing stage through the server's model
// runner, or one of the existing commands. The gates stop the video until the site decides: the
// owner on /admin/videos, or the site itself on arrival when the owner let it (docs/videos/
// HANDS-OFF.md) — Jev picks the outline against the channel stance, the quality check approves
// the final cut, the package check approves the upload, Jev's line check approves the narration.
// What still waits for a person: a check that did not pass, an outline Jev could not pick after
// the rewrites, a blocked video, and the upload itself, whose YouTube id comes back from the site.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { approvalState, approve, sha256File } from "../core/approvals.mjs";
import { EXPLAINER_PRESET } from "../core/drama.mjs";
import { emptyLexicon } from "../core/lexicon.mjs";
import { stanceProblems } from "../core/lint.mjs";
import { articlePath, SITE } from "../core/metadata.mjs";
import { atomicWrite, contentPackFile, docDir, lexiconFile, readJson, resolveWorkBase, resolveWorkdir, ROOT } from "../core/paths.mjs";
import { eachLine, LINE_ID, spokenText } from "../core/schema.mjs";
import { writeScreenplay } from "../core/screenplay.mjs";
import { LOCALE_PARTS, readLanguages, writeLanguages } from "../core/stages.mjs";
import { ARTIFACTS, dubArtifacts, dubsStatus, lintProject, loadProject, pipelineStatus } from "../core/state.mjs";
import { speechHash } from "../core/timeline.mjs";
import { MAX_TEMPO } from "../dubs/plan.mjs";
import { checklistFrom, guideSlugs, judgeOutline, outlineOptions, outlineReview, sourceGuideOf } from "../review/sync.mjs";
import { AutomationError, OUTPUT_INVALID } from "./client.mjs";
import { discussStep } from "./discuss.mjs";
import { pageReader, urlsIn } from "./fetch.mjs";
import { instructionsFor, parseAnswer, references } from "./prompts.mjs";
import { rewriteProblems } from "./rewrite.mjs";
import { advanceCompilation, startCompilation } from "./compilation.mjs";
import { castFrom, episodeBrief, isExplainerOneOff, isOneOff, retentionNumbers, scriptVerdict, seriesStep } from "./series.mjs";
import { episodeShortFields, episodeShortsProblems, shortsFile } from "../shorts/episode.mjs";

export const STATE_FILE = "auto.json";
const GLOBAL_FILE = "auto-state.json";
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?$/;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
export const MAX_LINT_FIXES = 3;
export const MAX_REPLANS = 2;
export const MAX_STAGE_FAILURES = 2;
// A drama's failed sheets, keyframes or clips are handed to the writer to fix the prompts, this
// many times per kind, before the video is blocked for a person (docs/videos/DRAMA.md).
export const MAX_PROMPT_FIX_ROUNDS = 2;
// Once the retakes are spent, the lines Jev still hears wrong are reworded by the listener and
// retaken, this many rounds in all, before the narration waits for the owner (docs/videos/HANDS-OFF.md §旁白).
export const MAX_REWRITE_ROUNDS = 2;
// A dub track (docs/videos/DUBS.md): a window that does not fit even sped up has its lines
// shortened by the translator this many rounds, and the lines Jev hears wrong are retaken this
// many rounds, before the worker gives the locale up with the reason and the video goes on
// without that track (docs/videos/LANGUAGES.md).
export const MAX_DUB_SHORTEN_ROUNDS = 2;
export const MAX_DUB_RETAKE_ROUNDS = 2;
const MAX_SOURCE_PAGES = 25;
const MAX_SOURCE_CHARS = 350_000;
const REQUIRED_SECTIONS = ["## 觀眾看完能做到的事", "## 站主觀點", "## 大綱"];
const DRAMA_SECTIONS = ["## 故事前提", "## 角色", "## 站主觀點", "## 大綱"];
// An explainer's brief (docs/videos/so-thats-why/) answers a question and has no cast.
const EXPLAINER_SECTIONS = ["## 問題", "## 一句答案", "## 站主觀點", "## 大綱"];
const YOUTUBE_ID = /^[A-Za-z0-9_-]{11}$/;
// Which manifest a drama stage's failures are read from, and what its entries are called.
const FIX_SOURCES = {
  look: { manifest: ARTIFACTS.characters, entries: "characters", what: "character" },
  keyframes: { manifest: ARTIFACTS.keyframes, entries: "shots", what: "shot" },
  clips: { manifest: ARTIFACTS.clips, entries: "shots", what: "shot" },
};

const today = (ctx) => ctx.now().toISOString().slice(0, 10);
/**
 * The prompt variant of an episode's writer and checker: "episode" for an episode of a long
 * series (the beats, the recaps, the next episode's promise); a one-off drama, though it is an
 * episode of its own one-episode series (docs/videos/DRAMA-FLOW.md, section 2), is written with
 * the drama prompts, since its story ends.
 */
const episodeVariant = (state) => (state.series && state.series.kind !== "one-off" ? "episode" : null);

/** Every video the automation started, oldest first. */
export function automatedVideos(workBase) {
  if (!existsSync(workBase)) return [];
  return readdirSync(workBase, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(path.join(workBase, entry.name, STATE_FILE)))
    .map((entry) => readJson(path.join(workBase, entry.name, STATE_FILE)))
    .filter((state) => state && SLUG.test(state.slug ?? ""))
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));
}

function saveState(workdir, state) {
  mkdirSync(workdir, { recursive: true });
  atomicWrite(path.join(workdir, STATE_FILE), `${JSON.stringify(state, null, 2)}\n`);
}

/** Whether a translation worksheet has nothing left to fill, for the parts it holds (i18n-sheet --parts). */
export function sheetDone(sheet) {
  const filled = (entry) => typeof entry?.text === "string" && entry.text.trim() !== "";
  const parts = Array.isArray(sheet.parts) && sheet.parts.length ? sheet.parts : ["metadata", "captions"];
  const captions = !parts.includes("captions") || !(sheet.lines ?? []).some((line) => line.todo);
  const metadata = !parts.includes("metadata") || (filled(sheet.title) && filled(sheet.description) && (sheet.chapters ?? []).every(filled) && Array.isArray(sheet.tags?.text) && sheet.tags.text.length > 0);
  return captions && metadata;
}

function titleOf(brief) {
  return (/^#\s+(.+)$/m.exec(brief)?.[1] ?? "").trim().slice(0, 200);
}

/** The site article a video retells: its source_guide, or else the first site article it rests on. */
export function mainGuide({ source_guide: guide, source_urls: urls }) {
  return (GUIDE_SLUG.test(guide ?? "") ? guide : null) ?? guideSlugs(urls)[0] ?? null;
}

// Until 2026-09-27 drafts read their article at /<locale>/guides/<slug>, a kind's list page the
// site answers with 404 for an article; the writer of gpt-6-sol-luna-where-to-use refused twice
// for want of a source. Addresses saved that way are read where the article is served.
const STALE_ARTICLE_URL = /^https:\/\/(?:www\.)?mokaair\.com\/([A-Za-z-]+)\/guides\/([a-z0-9][a-z0-9-]{0,118}[a-z0-9])\/?(?:[?#].*)?$/;

/**
 * Where a stage reads a site article: the path its content pack's kind gives (core/metadata.mjs
 * articlePath). A slug with no pack here is read as a life article, the section the drafts'
 * topics come from (apps/api/app/video_automation/topics.py).
 */
export function siteArticleUrl(slug, root = ROOT, locale = "zh-TW") {
  const kind = readJson(contentPackFile(slug, root), null)?.kind ?? "life";
  return `${SITE}/${locale}${articlePath({ slug, kind })}`;
}

/**
 * The pages a stage reads for a video: its site article first, then the rest, each stale
 * /<locale>/guides/<slug> address moved to where the article is served. A kind's list page has
 * no content pack, so it stays as it is.
 */
export function siteSources(sourceGuide, urls = [], root = ROOT) {
  const moved = (urls ?? []).map((url) => {
    const stale = STALE_ARTICLE_URL.exec(String(url));
    if (!stale) return url;
    if (stale[2] === sourceGuide || existsSync(contentPackFile(stale[2], root))) return siteArticleUrl(stale[2], root, stale[1]);
    return url;
  });
  return [...new Set([...(sourceGuide ? [siteArticleUrl(sourceGuide, root)] : []), ...moved])];
}

/**
 * What makes a planner's answer unusable, or null. `usedGuides` are earlier videos' main
 * articles; a drama's brief has the story bible's sections instead of a tutorial's, and an
 * explainer's (`preset` "flat-explainer") the question's. With a
 * channel stance, 站主觀點 must open by naming the stance points it applies (core/lint.mjs
 * stanceProblems); the local `lint` has no stance and does not check this.
 */
export function planProblem(plan, taken, usedGuides = new Set(), format = "slides", stance = "", preset = null) {
  if (!plan || typeof plan !== "object") return "the answer is not an object";
  if (!SLUG.test(plan.slug ?? "")) return `slug "${plan.slug}" is not lowercase kebab-case of at most 60 characters`;
  if (taken.has(plan.slug)) return `slug "${plan.slug}" is already used by an earlier video`;
  if (typeof plan.brief !== "string") return "brief is missing";
  const sections = format !== "drama" ? REQUIRED_SECTIONS : preset === EXPLAINER_PRESET ? EXPLAINER_SECTIONS : DRAMA_SECTIONS;
  const missing = sections.filter((heading) => !plan.brief.includes(heading));
  if (missing.length) return `brief lacks ${missing.join(", ")}`;
  const stanceIssues = stanceProblems(plan.brief, stance);
  if (stanceIssues.length) return `站主觀點 does not apply the channel stance: ${stanceIssues.join("; ")}`;
  if (outlineOptions(plan.brief).length < 2) return "brief needs 2 or 3 options written as 「### 選項 A：…」 with 一行說明 and 開場鉤子 lines";
  if (!Array.isArray(plan.source_urls) || !plan.source_urls.every((url) => /^https:\/\//.test(url))) return "source_urls must be https URLs";
  const guide = mainGuide(plan);
  if (guide && usedGuides.has(guide)) return `the site article "${guide}" is what an earlier video retells (see used_guides); pick another topic`;
  return null;
}

/** The pages a stage rests on, read now, within the payload's size budget. */
async function readSources(read, urls) {
  const pages = [];
  let chars = 0;
  for (const url of [...new Set(urls)].slice(0, MAX_SOURCE_PAGES)) {
    const page = await read(url);
    if (page.ok && chars + page.text.length > MAX_SOURCE_CHARS) {
      pages.push({ url, ok: false, error: "not read: the payload is full" });
      continue;
    }
    chars += page.ok ? page.text.length : 0;
    pages.push(page);
  }
  return pages;
}

function writeVideo(dir, video) {
  writeFileSync(path.join(dir, "video.json"), `${JSON.stringify(video, null, 2)}\n`);
}

function mergeLexicon(root, additions) {
  if (!additions || typeof additions !== "object") return [];
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

/**
 * The settings a video reads by its format (docs/videos/DRAMA-FLOW.md, section 1). A drama has
 * its own standing instructions, narrator voice, fact-check and retake rounds and topic scope on
 * drama tab's settings; a null voice, and a site from before the split that sends none
 * of them, mean the tutorial's. The languages a video is made in are not here at all: the owner
 * chooses them per video after the final cut (docs/videos/LANGUAGES.md), and `caption_locales`
 * only pre-ticks that panel.
 */
export function settingsFor(settings, format = "slides") {
  const tutorial = {
    voice: settings.voice,
    instructions: settings.stage_instructions ?? {},
    verifyRounds: settings.max_verify_rounds,
    retakeRounds: settings.max_retake_rounds,
    topicScope: settings.topic_scope ?? [],
  };
  if (format !== "drama") return tutorial;
  const drama = settings.drama ?? {};
  return {
    voice: drama.drama_voice ?? tutorial.voice,
    instructions: drama.drama_stage_instructions ?? tutorial.instructions,
    verifyRounds: drama.drama_max_verify_rounds ?? tutorial.verifyRounds,
    retakeRounds: drama.drama_max_retake_rounds ?? tutorial.retakeRounds,
    topicScope: drama.drama_topic_scope ?? tutorial.topicScope,
  };
}

/**
 * The settings tab's voice as video.json may carry it: the site serialises every field (a null
 * model, a "+0%" rate), and lint refuses the ones the provider does not use. Gemini takes its
 * pace from the style and has no rate; Azure has a rate and no style or model.
 */
export function settledVoice(voice) {
  const unused = voice.provider === "gemini" ? ["rate"] : ["style", "model"];
  return Object.fromEntries(Object.entries(voice).filter(([key, value]) => value !== null && value !== "" && !unused.includes(key)));
}

/**
 * video.json as the owner's settings say it must be, whatever the model returned. A drama
 * (docs/videos/DRAMA.md) also takes the settings tab's style preset, subtitle burn-in and
 * whether music is made at all, and its narrator voice is the drama part's when the owner chose
 * one; the writer's own look fields stay. The owner's request's preset (`stylePreset`) wins over
 * the settings tab's; an explainer's preset is not the writer's to change, and it has no characters.
 */
export function settle(video, { slug, settings, sourceGuide, root, format = "slides", series = null, cast = null, stylePreset = null }) {
  const settled = { ...video, slug, voice: settledVoice(settingsFor(settings, format).voice) };
  // The description links the article through its content pack. An article the news automation
  // published lives only in the database, so without a pack the script names it in sources instead.
  if (sourceGuide && existsSync(contentPackFile(sourceGuide, root))) settled.source_guide = sourceGuide;
  else delete settled.source_guide;
  settled.assets = [];
  if (settled.youtube) settled.youtube = { ...settled.youtube, video_id: null };
  if (format === "drama") {
    const drama = settings.drama ?? {};
    settled.format = "drama";
    const preset = stylePreset ?? drama.style_preset ?? "cinematic-3d";
    settled.look = { preset, ...(video.look ?? {}) };
    if (preset === EXPLAINER_PRESET) {
      settled.look.preset = EXPLAINER_PRESET;
      settled.characters = [];
    }
    settled.subtitles = { burn_in: drama.subtitle_burn_in ?? true, ...(video.subtitles ?? {}) };
    if (drama.music_enabled === false) delete settled.music;
  }
  if (format === "drama" && series) {
    // An episode of a series (docs/videos/SERIES.md): the cast is the setting book's, word for
    // word, listed by id; a character the book does not have stays for lint to refuse.
    settled.series = { slug: series.slug, episode: series.episode, chapter: series.chapter };
    const book = new Map((cast ?? []).map((character) => [character.id, character]));
    settled.characters = (video.characters ?? []).map((character) => book.get(character?.id) ?? character).sort((a, b) => (a?.id < b?.id ? -1 : a?.id > b?.id ? 1 : 0));
  }
  return settled;
}

function lintErrors(ctx, slug) {
  const result = lintProject(loadProject({ slug, root: ctx.root }));
  return result.errors.map((error) => `${error.path}: ${error.message}`);
}

async function run(ctx, command) {
  // Tests hand in a runner that plays the media stages without any vendor.
  if (ctx.runCommand) return ctx.runCommand(command, ctx);
  const { main } = await import("../cli.mjs");
  let out = "";
  const sink = { write: (text) => (out += text) };
  const code = await main(command, { ...ctx, stdout: sink, stderr: sink });
  return { code, out };
}

const lastLine = (out, lines = 1) => out.trim().split("\n").slice(-lines).join(" ");
/** The digits of a line, in order: a shortened translation must keep every one of them. */
const digitsOf = (text) => (String(text).match(/\d+(?:[.,]\d+)*/g) ?? []).join(" ");
/** A unit's report line names its video once: a phrase gets the slug, a line that has it stays. */
const lineFor = (slug, text) => (text.startsWith(`${slug}: `) ? text : `${slug}: ${text}`);

/** The YouTube id the script records, or null: a report without it would clear the site's. */
function recordedVideoId(state, root) {
  const video = readJson(path.join(docDir(state.slug, root), "video.json"), null);
  const id = video?.youtube?.video_id;
  return YOUTUBE_ID.test(id ?? "") ? id : null;
}

/** Hand everything the automation knows to /admin/videos: title, stage, checklist, article, format, YouTube id. */
async function report(ctx, api, state, stage) {
  const workdir = resolveWorkdir({ env: ctx.env, slug: state.slug, root: ctx.root, home: ctx.home });
  const status = await pipelineStatus({ slug: state.slug, root: ctx.root, workdir });
  const guide = mainGuide(state);
  // The page has no field for why a video stopped; the checklist is what the owner reads.
  const blocked = state.status === "blocked" && state.blocked ? [{ key: "blocked", label: `卡住，需要人處理：${state.blocked}`.slice(0, 120), done: false }] : [];
  await api.report(state.slug, {
    title: state.title || state.slug,
    stage: stage.slice(0, 40),
    checklist: [...blocked, ...checklistFrom(status.steps)],
    format: state.format ?? "slides",
    youtube_video_id: recordedVideoId(state, ctx.root),
    ...(guide ? { source_guide: guide } : {}),
    ...(state.series ? { series_slug: state.series.slug, ...(Number.isInteger(state.series.episode) ? { episode_number: state.series.episode } : {}) } : {}),
    ...(state.retry_request_id ? { retry_acknowledged_id: state.retry_request_id } : {}),
  });
}

export class Automation {
  constructor(ctx, api, settings) {
    this.ctx = ctx;
    this.api = api;
    this.settings = settings;
    this.read = pageReader({ fetchImpl: ctx.fetch ?? globalThis.fetch, sleep: ctx.sleep, now: () => ctx.now().getTime() });
    this.refs = null;
    this.log = (text) => ctx.stdout.write(`${text}\n`);
    // Set when a unit could not move and trying again at once would only repeat it: `auto`
    // ends the run, and the worker tries again on its next round.
    this.halted = false;
    this.lastAnswer = null;
  }

  get workBase() {
    return resolveWorkBase({ env: this.ctx.env, root: this.ctx.root, home: this.ctx.home });
  }

  workdir(slug) {
    return resolveWorkdir({ env: this.ctx.env, slug, root: this.ctx.root, home: this.ctx.home });
  }

  /** Every video this worker started, oldest first (auto.json), for the modules beside this one. */
  states() {
    return automatedVideos(this.workBase);
  }

  /** Write a video's auto.json as it stands. */
  persist(state) {
    saveState(this.workdir(state.slug), state);
  }

  /** Put video.json back as it was before a revision that lint refused. */
  restoreVideo(state, source) {
    writeFileSync(path.join(docDir(state.slug, this.ctx.root), "video.json"), source);
  }

  /** The skill's reference texts, from the tool's own repository whatever root the docs are under. */
  reference() {
    this.refs ??= references(ROOT);
    return this.refs;
  }

  // The module's helpers as methods, for the compilation module (compilation.mjs) that works
  // on this automation without reaching into the file's private functions.
  saveState(workdir, state) {
    saveState(workdir, state);
  }

  report(state, stage) {
    return report(this.ctx, this.api, state, stage);
  }

  run(command) {
    return run(this.ctx, command);
  }

  lastLine(out, lines = 1) {
    return lastLine(out, lines);
  }

  /** The channel's stance from the settings tab (docs/videos/HANDS-OFF.md §頻道立場); "" while the owner has not written one. */
  get stance() {
    return typeof this.settings.channel_stance === "string" ? this.settings.channel_stance.trim() : "";
  }

  /**
   * The prompt variant of a drama's planner, writer and checker: an episode of a long series has
   * its own (episodeVariant); an explainer (the flat-explainer preset), a one-off or a legacy
   * request, has the question's; any other drama none.
   */
  variantOf(state) {
    const episode = episodeVariant(state);
    if (episode) return episode;
    return state.format === "drama" && state.style_preset === EXPLAINER_PRESET ? "explainer" : null;
  }

  async stage(stage, slug, payload, maxOutputTokens, format = "slides", variant = null, series = null) {
    // The channel's stance (the planner and the writer read it), a binge series' genre section
    // (docs/videos/BINGE.md) and the owner's standing instructions for the stage end the prompt:
    // the tutorial part's for a slides video, the drama part's for a drama
    // (docs/videos/DRAMA-FLOW.md, section 1). The server keeps what was sent, per stage, format
    // and variant, for the owner to read.
    const standing = settingsFor(this.settings, format).instructions?.[stage] ?? "";
    const answer = await this.api.run(stage, slug, instructionsFor(stage, format, standing, variant, this.stance, series), payload, maxOutputTokens, format, variant);
    this.log(`  ${stage}: ${answer.model}, ${answer.input_tokens + answer.output_tokens} tokens; month ${answer.usage.tokens}/${answer.usage.token_budget}`);
    this.lastAnswer = answer.text;
    try {
      return parseAnswer(answer.text);
    } catch (error) {
      const invalid = new AutomationError(`${stage} answered something that is not JSON: ${error.message}`, { code: OUTPUT_INVALID });
      invalid.stage = stage;
      throw invalid;
    }
  }

  /** Save the last stage's answer as it came, so a person can see why it was unusable. */
  keepAnswer(dir, what) {
    if (typeof this.lastAnswer !== "string") return null;
    const name = `${what.replace(/[^a-z0-9-]+/gi, "-")}-${this.ctx.now().toISOString().replace(/[:.]/g, "-")}.txt`;
    mkdirSync(path.join(dir, "answers"), { recursive: true });
    writeFileSync(path.join(dir, "answers", name), this.lastAnswer);
    this.lastAnswer = null;
    return path.join("answers", name);
  }

  /** The voice a document of this format may carry (settledVoice); a compilation is a drama. */
  voice(format = "drama") {
    return settledVoice(settingsFor(this.settings, format).voice);
  }

  /** Nothing moved and nothing was wrong with the video (a service was down): end this run. */
  later(line) {
    this.halted = true;
    return line;
  }

  /**
   * A stage gave nothing usable. Keep what it said and end this run; after the second time in a
   * row the video is blocked, since a third try of the same payload would most likely fail the
   * same way. On 2026-09-25 a writer that kept answering without a script was asked six times
   * in two minutes, about 106,000 subscription tokens, before the worker was stopped by hand.
   */
  async retryLater(state, what, why) {
    const workdir = this.workdir(state.slug);
    state.failures = { ...(state.failures ?? {}), [what]: (state.failures?.[what] ?? 0) + 1 };
    const kept = this.keepAnswer(workdir, what);
    saveState(workdir, state);
    this.halted = true;
    const detail = `${why}${kept ? `; the answer is in ${kept}` : ""}`;
    if (state.failures[what] >= MAX_STAGE_FAILURES) return this.block(state, `${what} failed ${state.failures[what]} times in a row: ${detail}`);
    return `${state.slug}: ${what} gave nothing usable (${detail}); the next run tries once more`;
  }

  /** A stage worked: its count of failures in a row starts again. */
  cleared(state, what) {
    if (state.failures?.[what]) delete state.failures[what];
  }

  /** One unit of work; returns a line saying what was done, or null when nothing could be. */
  async step() {
    if (!this.settings.enabled) return null;
    // Every video on /admin/videos, the ones this worker did not make included, read afresh
    // each unit: the owner may drop one at any time.
    this.site = await this.api.videos();
    const dropped = new Map(this.site.filter((video) => video.dropped_at).map((video) => [video.slug, video]));
    for (const state of automatedVideos(this.workBase)) {
      if (state.status !== "dropped" && dropped.has(state.slug)) return this.drop(state, dropped.get(state.slug));
    }
    // A retry belongs to one site request and one local state transition. Remember the request
    // before doing any paid stage so a stale list response or a failed report cannot replay it.
    const siteBySlug = new Map(this.site.map((video) => [video.slug, video]));
    for (const state of automatedVideos(this.workBase)) {
      const siteVideo = siteBySlug.get(state.slug);
      const request = siteVideo?.retry_request_id;
      if (state.status !== "blocked" || !request || request === siteVideo.retry_acknowledged_id || request === state.retry_request_id) continue;
      state.retry_request_id = request;
      // A language batch can fail after the finished video reached YouTube. Resume
      // only its languages, rather than revisiting the production stages.
      state.status = state.blocked_from_status === "done" ? "done" : "active";
      delete state.blocked_from_status;
      const failedStage = /^([a-z_]+) failed \d+ times in a row:/.exec(state.blocked ?? "")?.[1];
      if (failedStage && state.failures) delete state.failures[failedStage];
      delete state.blocked;
      saveState(this.workdir(state.slug), state);
      try {
        await report(this.ctx, this.api, state, "retrying");
        siteVideo.retry_acknowledged_id = request;
      } catch (error) {
        return this.later(`${state.slug}: retry saved; could not report it yet (${error.message})`);
      }
      break;
    }
    // The owner uploaded a finished video and pasted its address on /admin/videos: the id goes
    // into the script, and the video reads as complete (docs/videos/HANDS-OFF.md).
    const uploaded = new Map(this.site.filter((video) => YOUTUBE_ID.test(video.youtube_video_id ?? "")).map((video) => [video.slug, video.youtube_video_id]));
    for (const state of automatedVideos(this.workBase)) {
      if (!["active", "done"].includes(state.status) || !uploaded.has(state.slug)) continue;
      const recorded = await this.recordVideoId(state, uploaded.get(state.slug));
      if (recorded) return recorded;
    }
    // A finished compilation the site has not heard about yet (the call failed on the round
    // that finished it): tell it now, or the series stays 合集正在做.
    for (const state of automatedVideos(this.workBase)) {
      if (state.status === "done" && state.compilation && !state.compilation_told && (await this.tellCompilationDone(state))) {
        return `${state.slug}: the site now knows the compilation of ${state.compilation.series} is done`;
      }
    }
    for (const state of automatedVideos(this.workBase)) {
      if (!["active", "done"].includes(state.status)) continue;
      // If the first acknowledgement of a retry could not reach the site, send it before another stage.
      if (state.retry_request_id && siteBySlug.get(state.slug)?.retry_acknowledged_id !== state.retry_request_id) {
        try {
          await report(this.ctx, this.api, state, "retrying");
        } catch (error) {
          return this.later(`${state.slug}: retry saved; could not report it yet (${error.message})`);
        }
      }
      let done = null;
      try {
        if (state.status === "active") done = await this.advance(state);
        // The languages the owner chose after the final cut (docs/videos/LANGUAGES.md), for a
        // video still on its way to YouTube or already there; nothing while a step of its own is due.
        done ??= await this.languages(state);
      } catch (error) {
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        return this.retryLater(state, error.stage, error.message);
      }
      if (done) return done;
    }
    // The owner's lines on a document or a screenplay are answered first, one per round
    // (docs/videos/DRAMA-FLOW.md, section 3): the owner is waiting, and nothing is paid for.
    const discussed = await discussStep(this);
    if (discussed) return discussed;
    // A series in the making comes next (docs/videos/SERIES.md), then the owner's one-off
    // requests from before one-offs became series, then a scheduled draft, all within the same
    // waiting cap.
    const series = await seriesStep(this);
    if (series) return series;
    // The owner's drama requests come before any scheduled draft, within the same waiting cap.
    if (this.settings.drama?.drama_enabled && this.room()) {
      const request = await this.api.dramaNext();
      if (request) return this.draftDrama(request);
    }
    if (this.due()) return this.draft();
    return null;
  }

  /** Whether another video may start without passing the owner's cap on drafts waiting on them. */
  room() {
    const active = automatedVideos(this.workBase).filter((state) => state.status === "active").length;
    return active < this.settings.max_waiting_drafts;
  }

  /**
   * Write the YouTube id the site reports into docs/videos/<slug>/video.json (youtube.video_id),
   * the file the worker's docs volume holds, once: a script that already names a video keeps it.
   * `status` then reads the video as on YouTube, and /admin/videos gets the finished checklist.
   */
  async recordVideoId(state, videoId) {
    const file = path.join(docDir(state.slug, this.ctx.root), "video.json");
    if (!existsSync(file)) return null;
    const video = JSON.parse(readFileSync(file, "utf8"));
    if (video.youtube?.video_id) return null;
    atomicWrite(file, `${JSON.stringify({ ...video, youtube: { ...(video.youtube ?? {}), video_id: videoId } }, null, 2)}\n`);
    state.status = "done";
    state.youtube_video_id = videoId;
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "on YouTube");
    // The owner may paste the address before the worker read the publish approval: the series
    // still has to hear that its compilation is done.
    if (state.compilation) await this.tellCompilationDone(state);
    return `${state.slug}: on YouTube as ${videoId}; video.json records it and the video is complete`;
  }

  /**
   * Tell the site the compilation is done (docs/videos/BINGE.md), once: until it hears, the
   * series page says 合集正在做 and refuses another. A call that fails is made again on a later
   * round (step), so a site that was down for a minute does not leave the series waiting forever.
   */
  async tellCompilationDone(state) {
    if (!state.compilation || state.compilation_told) return false;
    try {
      await this.api.compilationDone(state.compilation.series);
    } catch (error) {
      this.log(`  could not mark the compilation of ${state.compilation.series} done: ${error.message}`);
      return false;
    }
    state.compilation_told = true;
    saveState(this.workdir(state.slug), state);
    return true;
  }

  /** The owner dropped this video on /admin/videos: leave it, files and all. */
  drop(state, video) {
    state.status = "dropped";
    state.dropped = { at: video.dropped_at, note: video.dropped_note ?? "" };
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: the owner dropped it (${state.dropped.note}); the worker leaves it`;
  }

  /** Whether a new draft may start: on, interval passed, not too many waiting on the owner. */
  due() {
    if (!this.room()) return false;
    const last = readJson(path.join(this.workBase, GLOBAL_FILE), {}).last_draft_at;
    return !last || this.ctx.now().getTime() - Date.parse(last) >= this.settings.draft_interval_hours * 3600_000;
  }

  /**
   * Every video made or started: the ones in docs/videos, the worker's own drafts, and every video
   * on /admin/videos (the owner's branches and dropped ones too), with the article each retells.
   */
  earlierVideos() {
    const found = new Map();
    const videos = path.join(this.ctx.root, "docs", "videos");
    const dirs = existsSync(videos) ? readdirSync(videos, { withFileTypes: true }).filter((entry) => entry.isDirectory()) : [];
    for (const entry of dirs) {
      const brief = path.join(videos, entry.name, "brief.md");
      const video = readJson(path.join(videos, entry.name, "video.json"), null);
      found.set(entry.name, {
        slug: entry.name,
        title: video?.youtube?.title ?? (existsSync(brief) ? titleOf(readFileSync(brief, "utf8")) : ""),
        source_guide: video ? sourceGuideOf(video) : null,
        templates: (video?.scenes ?? []).map((scene) => scene.template),
      });
    }
    for (const state of automatedVideos(this.workBase)) {
      const known = found.get(state.slug);
      const entry = known ?? { slug: state.slug, title: state.title ?? "", source_guide: null, templates: [] };
      entry.source_guide ??= mainGuide(state);
      if (state.status === "dropped") entry.dropped = true;
      found.set(state.slug, entry);
    }
    for (const video of this.site ?? []) {
      const entry = found.get(video.slug) ?? { slug: video.slug, title: video.title ?? "", source_guide: null, templates: [] };
      entry.source_guide ??= video.source_guide ?? null;
      if (video.dropped_at) entry.dropped = true;
      found.set(video.slug, entry);
    }
    return [...found.values()];
  }

  planPayload(extra, earlier = this.earlierVideos(), format = "slides") {
    const refs = this.reference();
    return {
      today: today(this.ctx),
      // A drama's own topic scope (the drama part's), the topics to avoid shared by both.
      scope: settingsFor(this.settings, format).topicScope,
      avoid: this.settings.topic_avoid,
      target_minutes: [this.settings.target_minutes_min, this.settings.target_minutes_max],
      channel: refs.channel,
      formats: refs.formats,
      script_writing: refs.script_writing,
      earlier_videos: earlier,
      used_guides: [...new Set(earlier.map((video) => video.source_guide).filter(Boolean))],
      ...extra,
    };
  }

  /** Pick a topic and write a brief; the owner chooses an outline next. */
  async draft() {
    const { topics, notes } = await this.api.topics();
    const draftSlug = `draft-${this.ctx.now().toISOString().slice(0, 16).replace(/[-:T]/g, "")}`;
    const earlier = this.earlierVideos();
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    let plan = null;
    let problem = null;
    for (let attempt = 0; attempt < 2 && !plan; attempt++) {
      let answer;
      try {
        answer = await this.stage("planner", draftSlug, this.planPayload({ topics, topic_notes: notes, ...(problem ? { previous_problem: problem } : {}) }, earlier));
      } catch (error) {
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        problem = error.message;
        continue;
      }
      problem = planProblem(answer, taken, usedGuides, "slides", this.stance);
      if (!problem) plan = answer;
    }
    // Written whatever came of it: a failed draft waits for the next interval like a good one.
    atomicWrite(path.join(this.workBase, GLOBAL_FILE), `${JSON.stringify({ last_draft_at: this.ctx.now().toISOString() }, null, 2)}\n`);
    if (!plan) {
      const kept = this.keepAnswer(this.workBase, "planner");
      return this.later(`draft: the planner's brief was not usable (${problem}${kept ? `; the answer is in ${kept}` : ""}); trying again after the next interval`);
    }
    const dir = docDir(plan.slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    const state = {
      slug: plan.slug,
      title: String(plan.title || titleOf(plan.brief)).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      source_guide: plan.source_guide || null,
      source_urls: plan.source_urls.slice(0, 12),
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      notes: [],
    };
    saveState(this.workdir(plan.slug), state);
    return `draft: ${plan.slug} planned from ${topics.length} topics; ${await this.submitOutline(state)}`;
  }

  /**
   * Send the outline for review, and say what became of it. With the channel stance written and
   * the switch on, Jev picks first (docs/videos/HANDS-OFF.md §Jev 挑大綱): a pick that clears the
   * thresholds goes up with the review and the site approves it on arrival; one that does not is
   * the planner's note for a rewrite, MAX_REPLANS times in all, after which the outline waits for
   * the owner with the last pick attached, so the review card shows Jev's table. A site whose
   * judge is off (409) means the owner chooses as before; Jev or the site being down ends this
   * run, and the next one asks again.
   */
  async submitOutline(state) {
    const file = path.join(docDir(state.slug, this.ctx.root), "brief.md");
    const brief = readFileSync(file, "utf8");
    const options = outlineOptions(brief);
    const verdict = await judgeOutline(this.api, state.slug, brief, options);
    if (verdict.status === "later") return this.later(`Jev could not judge the outline (${verdict.reason}); the next run asks again`);
    if (verdict.pick) {
      state.last_pick = verdict.pick;
      saveState(this.workdir(state.slug), state);
    }
    if (verdict.status === "failed" && state.replans < MAX_REPLANS) return this.replan(state, verdict.pick.note, "Jev");
    await report(this.ctx, this.api, state, "outline approved");
    const { payload, summary } = outlineReview(brief, options, verdict, "（自動產生）");
    await this.api.submit(state.slug, { gate: "outline", content_sha256: await sha256File(file), summary, payload, files: [] });
    if (verdict.status === "passed") return `Jev picked outline ${verdict.pick.choice}; outline sent to /admin/videos`;
    if (verdict.status === "failed") return `Jev found no outline that passes after ${state.replans} rewrites (${verdict.pick.note}); outline sent to /admin/videos for the owner, pick attached`;
    return `outline sent to /admin/videos for the owner (${verdict.reason})`;
  }

  /** What the drama planner and writer get beyond a tutorial's payload. */
  dramaPayload(state) {
    const refs = this.reference();
    const drama = this.settings.drama ?? {};
    return {
      drama: refs.drama,
      drama_example: refs.drama_example,
      drama_brief: refs.drama_brief,
      drama_settings: { style_preset: state.style_preset ?? drama.style_preset ?? "cinematic-3d", voices: drama.character_voice_pool ?? [], subtitle_burn_in: drama.subtitle_burn_in ?? true, music_enabled: drama.music_enabled !== false },
    };
  }

  /**
   * An episode the owner asked for on /admin/videos: plan it from the premise, claim the request
   * under the video's slug, and send the outline. A planner that fails twice leaves a blocked
   * video behind, so the owner sees why on the page instead of a request that never starts.
   */
  async draftDrama(request) {
    const earlier = this.earlierVideos();
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const minutes = Number(request.target_minutes) || 3;
    const stateBase = { format: "drama", request_id: request.id, premise: request.premise, style_preset: request.style_preset ?? null, target_minutes: minutes, source_guide: request.source_guide ?? null };
    const sources = request.source_guide ? await readSources(this.read, [siteArticleUrl(request.source_guide, this.ctx.root)]) : [];
    let plan = null;
    let problem = null;
    for (let attempt = 0; attempt < 2 && !plan; attempt++) {
      let answer;
      try {
        answer = await this.stage(
          "planner",
          `drama-${String(request.id).slice(0, 8)}`,
          this.planPayload({ premise: request.premise, title: request.title ?? null, note: request.note ?? null, source_guide: request.source_guide ?? null, sources, target_minutes: [minutes, minutes], ...this.dramaPayload(stateBase), ...(problem ? { previous_problem: problem } : {}) }, earlier, "drama"),
          16_000,
          "drama",
          this.variantOf(stateBase),
        );
      } catch (error) {
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        problem = error.message;
        continue;
      }
      problem = planProblem(answer, taken, request.source_guide ? new Set() : usedGuides, "drama", this.stance, stateBase.style_preset);
      if (!problem) plan = answer;
    }
    const slug = plan?.slug ?? `drama-${String(request.id).slice(0, 8)}`;
    const state = {
      slug,
      title: String(plan?.title || request.title || titleOf(plan?.brief ?? "") || slug).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      ...stateBase,
      source_urls: (plan?.source_urls ?? []).slice(0, 12),
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      prompt_fixes: {},
      notes: request.note ? [`owner request: ${request.note}`] : [],
    };
    await this.api.dramaStart(request.id, slug);
    if (!plan) {
      const kept = this.keepAnswer(this.workdir(slug), "planner");
      saveState(this.workdir(slug), state);
      return this.block(state, `the planner could not write a usable brief for the owner's request (${problem}${kept ? `; the answer is in ${kept}` : ""})`);
    }
    const dir = docDir(slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    saveState(this.workdir(slug), state);
    return `drama: ${slug} planned from the owner's request; ${await this.submitOutline(state)}`;
  }

  /**
   * An episode of a series (docs/videos/SERIES.md), started on the site from the chapter's
   * approved outline: the brief is written from the episode's beats and approved here, since
   * the owner already chose the chapter; series.json beside it carries the cast and the context
   * the writer, the checker and lint read.
   */
  async draftEpisode(request, context, episode) {
    const series = context.series;
    const slug = request.slug;
    // A one-off's story bible stands where the setting book does (docs/videos/DRAMA-FLOW.md,
    // section 2): the site hands it over as "setting", and its one outline is the episode's beats.
    const oneOff = isOneOff(series);
    const cast = castFrom(context.setting?.body_json);
    const beats = episode.beats ?? {};
    const state = {
      slug,
      title: String(request.title || (oneOff ? episode.title || series.title : `${series.title} 第 ${episode.number} 集 ${episode.title}`)).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      format: "drama",
      request_id: request.id,
      premise: request.premise,
      style_preset: series.style_preset ?? null,
      target_minutes: Number(request.target_minutes) || series.target_minutes || 3,
      source_guide: request.source_guide ?? null,
      // The binge fields (docs/videos/BINGE.md) travel with a series' episode: the genre section
      // of every prompt, the visual tier lint holds the script to, whether the gates are
      // hands-off. A one-off is no binge series and carries none of them.
      series: {
        slug: series.slug,
        episode: episode.number,
        chapter: episode.chapter_number,
        ...(oneOff
          ? { kind: "one-off" }
          : {
              genre: series.genre ?? "xianxia-bonds",
              lead: series.lead ?? "dual-male",
              visual_tier: series.visual_tier ?? "clips",
              compilation: Boolean(series.compilation),
              hands_off: Boolean(series.hands_off),
            }),
      },
      // An explainer's facts rest on the pages its bible names; the checker reads them.
      source_urls: isExplainerOneOff(series) && Array.isArray(beats.sources) ? beats.sources.filter((url) => /^https:\/\//.test(url)).slice(0, 12) : [],
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      prompt_fixes: {},
      chosen: "A",
      notes: series.note ? [`series note: ${series.note}`] : [],
    };
    const dir = docDir(slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    const episodes = context.episodes ?? [];
    const following = episodes.find((each) => each.number === episode.number + 1);
    writeFileSync(path.join(dir, "series.json"), `${JSON.stringify({
      slug: series.slug,
      episode: episode.number,
      chapter: episode.chapter_number,
      title: episode.title,
      logline: episode.logline,
      characters: cast,
      beats,
      recaps: context.recaps ?? [],
      earlier: episodes.filter((each) => each.number < episode.number).map(({ number, title, logline }) => ({ number, title, logline })),
      next_logline: following?.logline ?? null,
      mysteries: context.mysteries ?? [],
      setting_md: context.setting?.body_md ?? "",
      chapter_md: context.chapter?.body_md ?? "",
      series: { title: series.title, premise: series.premise, tone: series.tone, aspects: series.aspects, note: series.note, style_preset: series.style_preset, open_ended: series.open_ended, genre: series.genre ?? "xianxia-bonds", lead: series.lead ?? "dual-male", visual_tier: series.visual_tier ?? "clips", compilation: Boolean(series.compilation), hands_off: Boolean(series.hands_off), total_minutes: series.total_minutes ?? null },
      visual_tier: series.visual_tier ?? "clips",
      compilation: Boolean(series.compilation),
    }, null, 2)}\n`);
    writeFileSync(path.join(dir, "brief.md"), episodeBrief(series, episode, cast, beats));
    const workdir = this.workdir(slug);
    saveState(workdir, state);
    await approve({ gate: "outline", docDir: dir, workdir, now: this.ctx.now(), note: oneOff ? "依故事聖經" : `planned by chapter ${episode.chapter_number}'s approved outline` });
    await report(this.ctx, this.api, state, "outline approved");
    if (oneOff) return `one-off ${series.slug}: ${slug} started from the approved story bible`;
    return `series ${series.slug}: episode ${episode.number} (${slug}) started from the chapter outline`;
  }

  /**
   * The script gate (docs/videos/DRAMA-FLOW.md, section 2): every drama's screenplay is read by
   * the owner, who may discuss it, before any image or clip is paid for. With 「劇本先給我看」
   * (series_script_gate) switched off on the settings tab, the screenplay is approved here. On a
   * hands-off series (docs/videos/BINGE.md) the checker's coverage and the measured timing stand
   * in for the owner: a script that fails the site's rule is fixed by the writer here,
   * MAX_PROMPT_FIX_ROUNDS times, before anything is sent; then it goes up, and the site approves
   * it on arrival when it passes, or leaves it for the owner with the problems on the card when
   * the rounds are spent.
   */
  async scriptGate(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const file = writeScreenplay(dir, JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8")));
    if (this.settings.drama?.series_script_gate === false) {
      await approve({ gate: "script", docDir: dir, workdir: this.workdir(state.slug), now: this.ctx.now(), note: "「劇本先給我看」關著，依設定自動核准" });
      return `${state.slug}: screenplay approved by the settings (劇本先給我看 is off)`;
    }
    const review = await this.decision(state, "script", file);
    if (!review) {
      if (state.series?.hands_off) {
        const check = readJson(path.join(this.workdir(state.slug), "review", "script-check.json"), null);
        const verdict = scriptVerdict(check, state.series);
        const rounds = state.prompt_fixes?.script ?? 0;
        if (!verdict.passed && rounds < MAX_PROMPT_FIX_ROUNDS) return this.fixScript(state, verdict.problems.join("；"), "the checker");
      }
      const result = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "script"]);
      if (result.code !== 0) return this.block(state, `review-push failed: ${lastLine(result.out)}`);
      return `${state.slug}: screenplay sent to /admin/videos`;
    }
    if (review.status === "approved") {
      await this.pull(state.slug);
      if (review.note) state.notes.push(`script: ${review.note}`);
      saveState(this.workdir(state.slug), state);
      const checker = review.note && /依作品設定自動核准/.test(review.note);
      return `${state.slug}: ${checker ? "the site" : "the owner"} approved the screenplay`;
    }
    if (review.status === "rejected") return this.fixScript(state, review.note ?? "");
    return null;
  }

  /** The screenplay was sent back (by the owner, or the checker on a hands-off series): the writer rewrites from the note, then it is checked again. */
  async fixScript(state, note, by = "the owner") {
    const rounds = state.prompt_fixes?.script ?? 0;
    if (rounds >= MAX_PROMPT_FIX_ROUNDS) return this.block(state, `${by} sent the screenplay back ${rounds + 1} times: ${note}`);
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const answer = await this.stage("writer", state.slug, this.scriptPayload(state, { video, fix: { kind: "script", targets: [], problems: [note], owner_note: note }, line_ids: this.freshIds(state, video, 40) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    const problem = await this.saveAndLint(state, answer);
    state.prompt_fixes = { ...(state.prompt_fixes ?? {}), script: rounds + 1 };
    state.notes.push(`script sent back by ${by}: ${note}`);
    state.verified = false;
    state.listener_done = false;
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "writer", `the rewritten screenplay ${problem}`);
    return `${state.slug}: screenplay rewritten after ${by === "the owner" ? "the owner's" : "the checker's"} note (round ${rounds + 1}); it is checked again`;
  }

  /** The compilation of a binge series (docs/videos/BINGE.md): started from the site's job. */
  startCompilation(job) {
    return startCompilation(this, job);
  }

  /** The finished episode's recap, kept on the site for the next episode's writer and checker. */
  async recap(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const info = readJson(path.join(dir, "series.json"), {});
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    try {
      const answer = await this.stage("verifier", state.slug, { video, beats: info.beats ?? {}, previous_recaps: info.recaps ?? [], episode: state.series.episode }, 16_000, state.format, "recap");
      if (typeof answer.recap !== "string" || !answer.recap.trim()) throw new AutomationError("the recap answer has no recap text", { code: OUTPUT_INVALID });
      await this.api.episodeRecap(state.series.slug, state.series.episode, { recap: answer.recap.trim().slice(0, 4000), state: answer.state && typeof answer.state === "object" ? answer.state : {} });
      state.recap_sent = true;
      saveState(this.workdir(state.slug), state);
      return true;
    } catch (error) {
      if (error instanceof AutomationError) {
        this.log(`  recap of episode ${state.series.episode} not kept yet: ${error.message}`);
        return false;
      }
      throw error;
    }
  }

  /** The newest decision on a gate for the current file: {status, choice, note} or null. */
  async decision(state, gate, file) {
    const project = await this.api.reviews(state.slug);
    const sha = existsSync(file) ? await sha256File(file) : null;
    return project?.reviews?.find((review) => review.gate === gate && review.content_sha256 === sha) ?? null;
  }

  async pull(slug) {
    return run(this.ctx, ["review-pull", "--slug", slug]);
  }

  /** Stop working on a video and say why on /admin/videos; the owner or a person takes over. */
  async block(state, why) {
    state.blocked_from_status = state.status;
    state.status = "blocked";
    state.blocked = why;
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "blocked");
    return `${state.slug}: blocked — ${why}`;
  }

  /** Move one video on by one step; null when it waits on the owner or cannot move. */
  async advance(state) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const dir = docDir(state.slug, ctx.root);
    const status = await pipelineStatus({ slug: state.slug, root: ctx.root, workdir });
    const next = status.next?.id;

    // A compilation (docs/videos/BINGE.md) has its own first steps; the final cut, the upload
    // package and the YouTube id go the same way as any video.
    if (state.compilation) {
      const moved = await advanceCompilation(this, state, next);
      if (moved !== undefined) return moved;
    }

    if (next === "outline approved") {
      const review = await this.decision(state, "outline", path.join(dir, "brief.md"));
      if (!review) return lineFor(state.slug, await this.submitOutline(state));
      if (review.status === "approved") {
        await this.pull(state.slug);
        state.chosen = review.choice;
        state.notes.push(...(review.note ? [`outline: ${review.note}`] : []));
        saveState(workdir, state);
        // The site approves on arrival when Jev's pick passed; otherwise the owner chose.
        const jev = review.payload?.pick?.passed === true && review.payload.pick.choice === review.choice;
        return `${state.slug}: ${jev ? "Jev" : "the owner"} chose outline ${review.choice}${review.note ? ` (${review.note})` : ""}`;
      }
      if (review.status === "rejected") {
        if (state.replans >= MAX_REPLANS) return this.block(state,`the outline was sent back ${state.replans + 1} times (Jev and the owner together): ${review.note}`);
        return lineFor(state.slug, await this.replan(state, review.note ?? ""));
      }
      return null;
    }

    if (next === "brief") return this.block(state,"brief.md is gone");
    if (next === "script passes lint") return this.write(state);
    // status only knows that verify-1.md exists; the rounds and the listener edit are ours.
    if (!state.verified) return this.verify(state);
    if (!state.listener_done) return this.listen(state);
    // An episode of a series: the owner reads the screenplay before any image or clip is paid for.
    if (next === "script approved") return this.scriptGate(state);

    // The drama's own steps (docs/videos/DRAMA.md): each media stage runs as a command, a failed
    // check goes back to the writer as a prompt fix, and two gates wait on the owner.
    if (next === "look generated") return this.media(state, "look");
    if (next === "look approved") return this.lookGate(state);
    if (next === "keyframes drawn") return this.media(state, "keyframes");
    if (next === "storyboard approved") return this.storyboardGate(state);
    if (next === "clips generated") return this.media(state, "clips");
    if (next === "music generated") return this.media(state, "music");

    if (next === "narration synthesized") {
      const result = await run(ctx, ["tts", "--slug", state.slug]);
      if (result.code !== 0) return this.block(state,`tts failed: ${result.out.trim().split("\n").at(-1)}`);
      await report(ctx, this.api, state, "narration synthesized");
      return `${state.slug}: narration synthesized`;
    }
    if (next === "narration approved") return this.narration(state);
    if (next === "frames rendered") {
      const channel = ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", ctx.env.VIDEO_BROWSER_CHANNEL] : [];
      const result = await run(ctx, ["render", "--slug", state.slug, ...channel]);
      if (result.code !== 0) return this.block(state,`render failed: ${result.out.trim().split("\n").at(-1)}`);
      return `${state.slug}: frames rendered`;
    }
    if (next === "video assembled") {
      const result = await run(ctx, ["assemble", "--slug", state.slug]);
      if (result.code !== 0) return this.block(state,`assemble failed: ${result.out.trim().split("\n").slice(-3).join(" ")}`);
      await report(ctx, this.api, state, "video assembled");
      // The script is final now: the episode's recap goes to the site for the next episode.
      if (episodeVariant(state) && !state.recap_sent) await this.recap(state);
      return `${state.slug}: video assembled`;
    }
    if (next === "captions written") return this.captions(state);
    if (next === "final video approved") return this.gate(state, "final", path.join(workdir, "final.mp4"));
    if (next === "upload package") {
      const result = await run(ctx, ["package", "--slug", state.slug]);
      if (result.code !== 0) return this.block(state,`package failed: ${result.out.trim().split("\n").at(-1)}`);
      return `${state.slug}: upload package written`;
    }
    if (next === "on YouTube") {
      const upload = path.join(workdir, "upload", "metadata.json");
      const review = await this.decision(state, "publish", upload);
      if (!review) {
        await run(ctx, ["review-push", "--slug", state.slug, "--gate", "publish"]);
        return `${state.slug}: publish confirmation sent to /admin/videos`;
      }
      if (review.status === "approved") {
        await this.pull(state.slug);
        state.status = "done";
        state.notes.push(...(review.note ? [`publish: ${review.note}`] : []));
        saveState(workdir, state);
        if (state.compilation) {
          await this.tellCompilationDone(state);
        } else if (state.series) {
          try {
            if (episodeVariant(state) && !state.recap_sent) await this.recap(state);
            await this.api.episodeDone(state.series.slug, state.series.episode);
          } catch (error) {
            // The next round of the series waits until this is reported; the log says why.
            this.log(`  could not mark episode ${state.series.episode} done: ${error.message}`);
          }
        } else if (state.request_id) {
          try {
            await this.api.dramaDone(state.request_id);
          } catch (error) {
            // The request reads as done once the video is on YouTube anyway.
            this.log(`  could not mark the drama request done: ${error.message}`);
          }
        }
        return `${state.slug}: the upload is confirmed${review.note ? ` (${review.note})` : ""}; the owner uploads it in YouTube Studio and pastes the address on /admin/videos`;
      }
      if (review.status === "rejected") return this.block(state,`the owner sent the upload back: ${review.note}`);
      return null;
    }
    if (!next) {
      state.status = "done";
      saveState(workdir, state);
      return `${state.slug}: done`;
    }
    return null;
  }

  /**
   * Rewrite the brief from a note — the owner's when they sent the outline back, Jev's when no
   * option passed (`by`) — then send it again; both count toward MAX_REPLANS.
   */
  async replan(state, note, by = "the owner") {
    const dir = docDir(state.slug, this.ctx.root);
    const previous = readFileSync(path.join(dir, "brief.md"), "utf8");
    const earlier = this.earlierVideos().filter((video) => video.slug !== state.slug);
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const drama = state.format === "drama";
    const { topics } = drama ? { topics: [] } : await this.api.topics();
    const extra = drama ? { premise: state.premise, target_minutes: [state.target_minutes ?? 3, state.target_minutes ?? 3], source_guide: state.source_guide, ...this.dramaPayload(state) } : { topics };
    const answer = await this.stage("planner", state.slug, this.planPayload({ ...extra, owner_note: note, sent_back_by: by === "Jev" ? "jev" : "owner", previous_brief: previous, slug: state.slug }, earlier, state.format), 16_000, state.format, drama ? this.variantOf(state) : null);
    const problem = planProblem({ ...answer, slug: state.slug }, taken, drama && state.source_guide ? new Set() : usedGuides, state.format, this.stance, state.style_preset ?? null);
    state.replans += 1;
    state.notes.push(`outline sent back by ${by}: ${note}`);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "planner", `the re-planned brief was not usable (${problem})`);
    this.cleared(state, "planner");
    writeFileSync(path.join(dir, "brief.md"), answer.brief.endsWith("\n") ? answer.brief : `${answer.brief}\n`);
    state.source_urls = (answer.source_urls ?? state.source_urls).slice(0, 12);
    state.source_guide = answer.source_guide ?? state.source_guide;
    saveState(this.workdir(state.slug), state);
    return `brief rewritten after ${by === "Jev" ? "Jev's" : "the owner's"} note (round ${state.replans}); ${await this.submitOutline(state)}`;
  }

  scriptPayload(state, extra) {
    const refs = this.reference();
    const lexicon = readJson(lexiconFile(this.ctx.root), { terms: {} });
    const drama = state.format === "drama";
    return {
      today: today(this.ctx),
      slug: state.slug,
      voice: settingsFor(this.settings, state.format).voice,
      source_guide: state.source_guide,
      target_minutes: drama ? [state.target_minutes ?? 3, state.target_minutes ?? 3] : [this.settings.target_minutes_min, this.settings.target_minutes_max],
      lexicon: Object.keys(lexicon.terms),
      script_writing: refs.script_writing,
      channel: refs.channel,
      minimal: refs.minimal,
      showcase: refs.showcase,
      owner_notes: state.notes,
      ...(drama ? this.dramaPayload(state) : {}),
      ...(state.series ? this.seriesPayload(state) : {}),
      ...extra,
    };
  }

  /** What an episode of a series adds for the writer and the checker: series.json's context. */
  seriesPayload(state) {
    const info = readJson(path.join(docDir(state.slug, this.ctx.root), "series.json"), null);
    if (!info) return {};
    return {
      series: { ...(info.series ?? {}), slug: state.series.slug, episode: state.series.episode, chapter: state.series.chapter, title_of_episode: info.title, logline: info.logline },
      series_reference: this.reference().series,
      cast: info.characters ?? [],
      setting_md: info.setting_md ?? "",
      chapter_md: info.chapter_md ?? "",
      beats: info.beats ?? {},
      recaps: info.recaps ?? [],
      earlier_episodes: info.earlier ?? [],
      next_logline: info.next_logline ?? null,
      mysteries: info.mysteries ?? [],
    };
  }

  /** Save a stage's video.json and lexicon terms, then fix lint errors with the writer, up to 3 times. */
  async saveAndLint(state, answer) {
    const dir = docDir(state.slug, this.ctx.root);
    let current = answer;
    for (let fix = 0; ; fix++) {
      if (!current?.video || typeof current.video !== "object") return "the answer has no video object";
      const cast = state.series ? readJson(path.join(dir, "series.json"), {}).characters ?? [] : null;
      writeVideo(dir, settle(current.video, { slug: state.slug, settings: this.settings, sourceGuide: state.source_guide, root: this.ctx.root, format: state.format, series: state.series ?? null, cast, stylePreset: state.style_preset ?? null }));
      const added = mergeLexicon(this.ctx.root, current.lexicon_additions);
      if (added.length) state.lexicon_added = [...new Set([...(state.lexicon_added ?? []), ...added])];
      const errors = lintErrors(this.ctx, state.slug);
      if (!errors.length) return null;
      if (fix >= MAX_LINT_FIXES) return `lint still fails after ${MAX_LINT_FIXES} fixes: ${errors.slice(0, 3).join("; ")}`;
      const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
      current = await this.stage("writer", state.slug, this.scriptPayload(state, { video, lint_errors: errors, line_ids: this.freshIds(state, video, 40) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    }
  }

  /**
   * Run one of the drama's media stages. Exit 1 means the checks failed some sheets, keyframes or
   * clips: the writer fixes their prompts and the stage runs again next round. Exit 3 needs the
   * owner (the cap, a setting, a key) and blocks the video with the reason on /admin/videos; exit
   * 4 is a vendor or the budget server-side, tried again next round; anything else blocks.
   */
  async media(state, command) {
    const { ctx } = this;
    const channel = ["look", "keyframes"].includes(command) && ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", ctx.env.VIDEO_BROWSER_CHANNEL] : [];
    const result = await run(ctx, [command, "--slug", state.slug, ...channel]);
    if (result.code === 0) {
      this.cleared(state, command);
      delete state.prompt_fixes?.[command];
      saveState(this.workdir(state.slug), state);
      await report(ctx, this.api, state, `${command} done`);
      return `${state.slug}: ${command} done`;
    }
    if (result.code === 1 && FIX_SOURCES[command]) return this.fixPrompts(state, command, {});
    if (result.code === 3) return this.block(state, `${command} needs the owner: ${lastLine(result.out)}`);
    if (result.code === 4) return this.later(`${state.slug}: ${command} could not finish (${lastLine(result.out)}); the next run tries again`);
    return this.block(state, `${command} failed: ${lastLine(result.out, 2)}`);
  }

  /** The ids a stage left for a prompt fix, with what the judge or the checks said about each. */
  failedTargets(state, kind) {
    const source = FIX_SOURCES[kind];
    const manifest = readJson(path.join(this.workdir(state.slug), source.manifest), null);
    const targets = [];
    for (const [id, entry] of Object.entries(manifest?.[source.entries] ?? {})) {
      if (!entry?.needs_review) continue;
      const problems = entry.problems ?? [...new Set((entry.candidates ?? entry.takes ?? []).flatMap((take) => take.judge?.problems ?? take.qc?.problems ?? []))];
      targets.push({ id, problems });
    }
    return targets;
  }

  /**
   * Hand failed sheets, keyframes or clips (or a gate the owner sent back) to the writer as a
   * prompt fix, at most MAX_PROMPT_FIX_ROUNDS times per kind; then the video waits for a person.
   */
  async fixPrompts(state, kind, { targets = null, ownerNote = null }) {
    const workdir = this.workdir(state.slug);
    const found = targets ?? this.failedTargets(state, kind);
    const what = FIX_SOURCES[kind]?.what ?? "shot";
    const summary = found.map((target) => `${target.id}: ${(target.problems ?? []).join("; ") || "failed"}`).join(" | ") || ownerNote || "no detail";
    const rounds = state.prompt_fixes?.[kind] ?? 0;
    if (rounds >= MAX_PROMPT_FIX_ROUNDS) return this.block(state, `${kind} still fails after ${rounds} prompt fixes (${summary})`);
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const answer = await this.stage("writer", state.slug, this.scriptPayload(state, { video, fix: { kind, targets: found, problems: found.flatMap((target) => target.problems ?? []), owner_note: ownerNote }, line_ids: this.freshIds(state, video, 40) }), 32_000, "drama", this.variantOf(state), state.series ?? null);
    const problem = await this.saveAndLint(state, answer);
    if (problem) return this.retryLater(state, "writer", `the ${kind} fix ${problem}`);
    this.cleared(state, "writer");
    state.prompt_fixes = { ...(state.prompt_fixes ?? {}), [kind]: rounds + 1 };
    if (ownerNote) state.notes.push(`${kind} sent back: ${ownerNote}`);
    saveState(workdir, state);
    return `${state.slug}: ${kind} prompts fixed (round ${rounds + 1}) for ${found.map((target) => target.id).join(", ") || what}; ${kind} runs again next`;
  }

  /**
   * The look gate: one review per character. Nothing sent yet for these sheets: send them. Every
   * character approved: record the choice and the approval. One sent back: the writer rewrites
   * that character and the sheets are drawn again.
   */
  async lookGate(state) {
    const workdir = this.workdir(state.slug);
    const file = path.join(workdir, ARTIFACTS.characters);
    const manifest = readJson(file, null);
    if (!manifest?.characters) return this.block(state, "characters/manifest.json is gone; run look again");
    const project = await this.api.reviews(state.slug);
    const sha = await sha256File(file);
    const reviews = (project?.reviews ?? []).filter((review) => review.gate === "look" && review.content_sha256 === sha);
    if (!reviews.length) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "look"]);
      if (pushed.code !== 0) return this.later(`${state.slug}: could not send the look for review: ${lastLine(pushed.out)}`);
      return `${state.slug}: character sheets sent to /admin/videos`;
    }
    const rejected = reviews.filter((review) => review.status === "rejected");
    if (rejected.length) {
      const targets = rejected.map((review) => ({ id: review.subject, problems: review.note ? [review.note] : [] }));
      return this.fixPrompts(state, "look", { targets, ownerNote: rejected.map((review) => `${review.subject}: ${review.note ?? ""}`).join("; ") });
    }
    const approved = new Set(reviews.filter((review) => review.status === "approved").map((review) => review.subject));
    if (Object.keys(manifest.characters).every((id) => approved.has(id))) {
      await this.pull(state.slug);
      return `${state.slug}: the owner chose the character sheets`;
    }
    return null;
  }

  /** The storyboard gate: sent when nothing is pending for these keyframes; sent back means a prompt fix. */
  async storyboardGate(state) {
    const workdir = this.workdir(state.slug);
    const review = await this.decision(state, "storyboard", path.join(workdir, ARTIFACTS.keyframes));
    if (!review) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "storyboard"]);
      if (pushed.code !== 0) return this.later(`${state.slug}: could not send the storyboard for review: ${lastLine(pushed.out)}`);
      return `${state.slug}: storyboard sent to /admin/videos`;
    }
    if (review.status === "approved") {
      await this.pull(state.slug);
      return `${state.slug}: the owner approved the storyboard${review.note ? ` (${review.note})` : ""}`;
    }
    if (review.status === "rejected") {
      const shots = (review.payload?.shots ?? []).filter((shot) => shot.needs_review).map((shot) => ({ id: shot.id, problems: shot.judge?.problems ?? [] }));
      return this.fixPrompts(state, "keyframes", { targets: shots, ownerNote: review.note ?? "" });
    }
    return null;
  }

  /** Line ids for the model to use, none already in the script (the same alphabet as `ids`). */
  freshIds(state, video, count) {
    const taken = new Set(video ? [...eachLine(video)].map(({ line }) => line.id) : []);
    const ids = [];
    const alphabet = "abcdefghijkmnpqrstuvwxyz23456789";
    while (ids.length < count) {
      let id = "";
      for (let index = 0; index < 4; index++) id += alphabet[Math.floor(Math.random() * alphabet.length)];
      if (LINE_ID.test(id) && !taken.has(id) && !ids.includes(id)) ids.push(id);
    }
    return ids;
  }

  async write(state) {
    const dir = docDir(state.slug, this.ctx.root);
    if (existsSync(path.join(dir, "video.json"))) {
      // A draft exists and only fails lint: fix it rather than write a new one.
      const problem = await this.saveAndLint(state, { video: JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8")) });
      saveState(this.workdir(state.slug), state);
      return problem ? await this.block(state, problem) : `${state.slug}: script fixed and passes lint`;
    }
    const brief = readFileSync(path.join(dir, "brief.md"), "utf8");
    const option = outlineOptions(brief).find((each) => each.key === state.chosen) ?? null;
    const sources = await readSources(this.read, siteSources(state.source_guide, state.source_urls, this.ctx.root));
    const answer = await this.stage("writer", state.slug, this.scriptPayload(state, { brief, chosen_option: option, sources, line_ids: this.freshIds(state, null, 140) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    const problem = await this.saveAndLint(state, answer);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "writer", `the script ${problem}`);
    this.cleared(state, "writer");
    const shorts = this.variantOf(state) === "explainer" ? this.saveShorts(state, answer.shorts) : null;
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "fact-checked");
    return `${state.slug}: script drafted and passes lint${shorts ? `; ${shorts}` : ""}`;
  }

  /**
   * An explainer's two Shorts (docs/videos/so-thats-why/), drafted with its script: the fields the
   * tool decides are set here, and shorts.json is written only when both Shorts fit this video.
   * A bad draft is noted and never holds the long video back; the Shorts can be written later.
   */
  saveShorts(state, drafted) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const shorts = Array.isArray(drafted)
      ? drafted.map((doc, index) => ({ ...doc, ...episodeShortFields(state.slug, index) }))
      : drafted;
    const problems = episodeShortsProblems(shorts, video);
    if (problems.length) {
      state.notes.push(`the drafted Shorts were not saved: ${problems.slice(0, 3).join("; ")}`);
      return "Shorts not saved (see notes)";
    }
    writeFileSync(shortsFile(state.slug, this.ctx.root), `${JSON.stringify(shorts, null, 2)}\n`);
    return "2 Shorts drafted";
  }

  async verify(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const claims = existsSync(path.join(dir, "claims.md")) ? readFileSync(path.join(dir, "claims.md"), "utf8") : "";
    const round = state.verify_rounds + 1;
    const urls = siteSources(null, [...urlsIn(claims), ...(video.sources ?? []).map((source) => source.url), ...(state.source_urls ?? [])], this.ctx.root);
    const sources = await readSources(this.read, urls);
    const answer = await this.stage("verifier", state.slug, { today: today(this.ctx), round, video, claims, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), sources, ...(state.series ? this.seriesPayload(state) : {}) }, 32_000, state.format, this.variantOf(state), state.series ?? null);
    if (typeof answer.report !== "string") return this.retryLater(state, "verifier", `fact-check round ${round} returned no report`);
    writeFileSync(path.join(dir, `verify-${round}.md`), answer.report.endsWith("\n") ? answer.report : `${answer.report}\n`);
    if (state.series) {
      // What the script gate shows the owner: whether each beat is delivered, and what jars;
      // the retention numbers are measured on the checked script from the lines the checker
      // named (docs/videos/BINGE.md), never taken from the model.
      const reviewDir = path.join(this.workdir(state.slug), "review");
      mkdirSync(reviewDir, { recursive: true });
      const checked = answer.video && typeof answer.video === "object" ? answer.video : video;
      atomicWrite(path.join(reviewDir, "script-check.json"), `${JSON.stringify({ round, coverage: answer.coverage ?? null, problems: Array.isArray(answer.problems) ? answer.problems : [], similar_works: Array.isArray(answer.similar_works) ? answer.similar_works : [], retention: retentionNumbers(checked, answer.retention) }, null, 2)}\n`);
    }
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    state.verify_rounds = round;
    const changed = Number(answer.changed_facts) || 0;
    if (answer.video) {
      const problem = await this.saveAndLint(state, { video: answer.video });
      if (problem) return this.retryLater(state, "verifier", `fact-check round ${round} changed ${changed} facts but ${problem}`);
    }
    state.verified = changed <= 3 || round >= settingsFor(this.settings, state.format).verifyRounds;
    this.cleared(state, "verifier");
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: fact-check round ${round}, ${changed} facts changed${state.verified ? "" : "; another round follows"}`;
  }

  async listen(state, note = null) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const answer = await this.stage("listener", state.slug, { video, script_writing: this.reference().script_writing, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), ...(note ? { owner_note: note } : {}) }, 32_000, state.format);
    const problem = await this.saveAndLint(state, answer);
    state.listener_done = !problem;
    if (problem) return this.retryLater(state, "listener", `the listener edit ${problem}`);
    this.cleared(state, "listener");
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: listener edit, ${(answer.edits ?? []).length} changes`;
  }

  async narration(state) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const timeline = path.join(workdir, "timeline.json");
    const review = await this.decision(state, "audio", timeline);
    if (review?.status === "approved") {
      await this.pull(state.slug);
      return `${state.slug}: narration approved${review.note ? ` (${review.note})` : ""}`;
    }
    if (review?.status === "rejected") {
      state.notes.push(`narration sent back: ${review.note}`);
      state.listener_done = false;
      saveState(workdir, state);
      return this.listen(state, review.note);
    }
    if (review?.status === "pending") return null;
    let check = await run(ctx, ["check-audio", "--slug", state.slug]);
    const retakeRounds = settingsFor(this.settings, state.format).retakeRounds;
    while (check.code === 1 && state.retakes < retakeRounds) {
      state.retakes += 1;
      saveState(workdir, state);
      const redo = await run(ctx, ["tts", "--slug", state.slug, "--redo", path.join(workdir, "review", "check-flags.json")]);
      if (redo.code !== 0) return this.block(state,`retake failed: ${redo.out.trim().split("\n").at(-1)}`);
      check = await run(ctx, ["check-audio", "--slug", state.slug]);
    }
    // The retakes are spent and Jev still hears some lines wrong: the listener rewords those
    // lines, they are retaken and checked again, MAX_REWRITE_ROUNDS rounds in all
    // (docs/videos/HANDS-OFF.md §旁白). What is still flagged after that waits for the owner.
    let rounds = 0;
    let rewritten = 0;
    let problems = [];
    while (check.code === 1 && (state.rewrites ?? 0) < MAX_REWRITE_ROUNDS) {
      const round = await this.rewriteNarration(state, problems);
      if (round.stopped) return round.stopped;
      rounds += 1;
      rewritten += round.ids.length;
      problems = round.problems;
      // Nothing changed: the same clips would only be flagged again; the next round, if any,
      // is told why the rewrites were refused.
      if (!round.ids.length) continue;
      const redo = await run(ctx, ["tts", "--slug", state.slug, "--redo", round.flagsFile]);
      if (redo.code !== 0) return this.block(state, `retake after the rewrite failed: ${lastLine(redo.out)}`);
      check = await run(ctx, ["check-audio", "--slug", state.slug]);
    }
    if (check.code === 4) return this.later(`${state.slug}: narration check could not finish (${check.out.trim().split("\n").at(-1)}); the next run tries again`);
    const pushed = await run(ctx, ["review-push", "--slug", state.slug, "--gate", "audio"]);
    if (pushed.code !== 0) return this.later(`${state.slug}: could not send the narration for review: ${pushed.out.trim()}`);
    await this.pull(state.slug);
    const rewriting = rounds ? `; ${rewritten} lines rewritten in ${rounds} rewrite round${rounds === 1 ? "" : "s"}` : "";
    return `${state.slug}: narration checked (${check.code === 0 ? "Jev passed every line" : "some lines flagged"}${rewriting}) and sent for review`;
  }

  /**
   * One rewrite round (docs/videos/HANDS-OFF.md §旁白): the lines check-audio still flags, with
   * what the transcriber heard, go to the listener's rewrite pass. A rewrite that keeps every
   * number, Latin word and dictionary term (rewrite.mjs) replaces the line in video.json, the
   * rest are dropped with the reason in the notes; a script the rewrites make fail lint is put
   * back as it was. The accepted rewrites go to review/rewrites.json for the review card and
   * their ids to a flags file for `tts --redo`. `previousProblems` are the refusals of the round
   * before, so the listener does not repeat them. Answers { ids, flagsFile, problems }, or
   * { stopped } with this run's line when the answer was unusable.
   */
  async rewriteNarration(state, previousProblems = []) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const dir = docDir(state.slug, ctx.root);
    const reviewDir = path.join(workdir, "review");
    const check = readJson(path.join(reviewDir, "check.json"), { lines: {} });
    const flags = readJson(path.join(reviewDir, "check-flags.json"), { flags: [], notes: {} });
    const file = path.join(dir, "video.json");
    const source = readFileSync(file, "utf8");
    const video = JSON.parse(source);
    const lines = new Map([...eachLine(video)].map(({ line }) => [line.id, line]));
    const flagged = (flags.flags ?? [])
      .filter((id) => lines.has(id))
      .map((id) => ({ id, text: spokenText(lines.get(id)), heard: check.lines?.[id]?.heard ?? "", jev: typeof check.lines?.[id]?.noul === "number" ? check.lines[id].noul : null }));
    const round = (state.rewrites ?? 0) + 1;
    const lexicon = readJson(lexiconFile(ctx.root), emptyLexicon());
    const payload = { lines: flagged, lexicon: Object.keys(lexicon.terms), round, ...(previousProblems.length ? { previous_problems: previousProblems } : {}) };
    const answer = await this.stage("listener", state.slug, payload, 16_000, state.format, "rewrite");
    if (!Array.isArray(answer?.lines)) return { stopped: await this.retryLater(state, "listener", `rewrite round ${round} answered without a lines array`) };
    this.cleared(state, "listener");
    const accepted = [];
    const problems = [];
    const seen = new Set();
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const before = flagged.find((each) => each.id === id);
      if (!before) {
        problems.push(`${id || "?"}: not one of the flagged lines`);
        continue;
      }
      if (seen.has(id)) continue;
      seen.add(id);
      const after = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!after) {
        problems.push(`${id}: the rewrite is empty`);
        continue;
      }
      if (after === before.text) continue;
      const found = rewriteProblems(before.text, after, { lexicon });
      if (found.length) {
        problems.push(`${id}: ${found.join("; ")}`);
        continue;
      }
      accepted.push({ id, before: before.text, after, heard: before.heard });
    }
    if (accepted.length) {
      for (const { id, after } of accepted) {
        const line = lines.get(id);
        line.text = after;
        // The rewrite is what the voice says now; a spoken form written for the old text would fail lint.
        delete line.say;
        delete line.say_for;
      }
      writeVideo(dir, video);
      const errors = lintErrors(ctx, state.slug);
      if (errors.length) {
        writeFileSync(file, source);
        problems.push(`${accepted.map((each) => each.id).join(", ")}: lint refuses the rewritten script: ${errors.slice(0, 3).join("; ")}`);
        accepted.length = 0;
      }
    }
    state.rewrites = round;
    for (const each of accepted) state.notes.push(`narration rewritten: ${each.id} 「${each.before}」 → 「${each.after}」`);
    for (const problem of problems) state.notes.push(`narration rewrite dropped: ${problem}`);
    // Every round's accepted rewrites, in order: review/sync.mjs sends them as the audio review's payload.rewrites.
    atomicWrite(path.join(reviewDir, "rewrites.json"), `${JSON.stringify([...readJson(path.join(reviewDir, "rewrites.json"), []), ...accepted], null, 2)}\n`);
    const flagsFile = path.join(reviewDir, "rewrite-flags.json");
    if (accepted.length) atomicWrite(flagsFile, `${JSON.stringify({ slug: state.slug, flags: accepted.map((each) => each.id) }, null, 2)}\n`);
    saveState(workdir, state);
    this.log(`  rewrite round ${round}: ${accepted.length} of ${flagged.length} flagged lines rewritten${problems.length ? `, ${problems.length} dropped` : ""}`);
    return { ids: accepted.map((each) => each.id), flagsFile, problems };
  }

  /**
   * The zh-TW captions, cut from the approved narration. The other languages are no longer made
   * here: the owner chooses them per video once the final cut is approved, and `languages` makes
   * exactly those (docs/videos/LANGUAGES.md), so the final gate never waits on a translation.
   */
  async captions(state) {
    const result = await run(this.ctx, ["captions", "--slug", state.slug]);
    if (result.code !== 0) return this.block(state, `captions failed: ${result.out.trim()}`);
    return `${state.slug}: captions written`;
  }

  /**
   * One unit of the languages work (docs/videos/LANGUAGES.md). Once the final cut is approved
   * and the owner has chosen the video's languages on /admin/videos, the choice is copied into
   * the work directory (captions, package, qa and review-push read it there); then a round
   * translates one locale's chosen parts, or makes one locale's dub track (shortening and
   * retaking within the round), and once every chosen part the site still reports as in the
   * making is made, the captions and the package are written again and the batch goes up as a
   * languages review. Null when there is nothing to do: no choice yet, nothing pending, or the
   * final cut not approved. A video the owner already uploaded takes the same round for the
   * languages ticked after the fact.
   */
  async languages(state) {
    const { ctx } = this;
    const slug = state.slug;
    const video = (this.site ?? []).find((each) => each.slug === slug);
    if (!video || video.dropped_at || !video.locales_decided_at) return null;
    const dir = docDir(slug, ctx.root);
    const workdir = this.workdir(slug);
    if (!existsSync(path.join(dir, "video.json"))) return null;
    if ((await approvalState({ gate: "final", docDir: dir, workdir })).status !== "approved") return null;
    writeLanguages(workdir, { locales: video.locales ?? {}, decided_at: video.locales_decided_at, synced_at: ctx.now().toISOString() });
    const choice = readLanguages(workdir);
    const pending = this.pendingLanguages(video, choice);
    if (!pending.length) return null;
    const project = loadProject({ slug, root: ctx.root });
    const doc = project.doc;
    for (const { locale, parts } of pending) {
      const sheetParts = parts.filter((part) => part !== "dub");
      if (!sheetParts.length) continue;
      const translated = await this.translateLocale(state, locale, sheetParts, doc);
      if (translated) return translated;
    }
    const dubs = dubsStatus(project, workdir, speechHash(doc, project.lexicon));
    for (const { locale, parts } of pending) {
      if (!parts.includes("dub") || ["current", "skipped"].includes(dubs[locale]?.status)) continue;
      return this.makeDub(state, locale);
    }
    // Every chosen part is made: cut the captions on the dubs, write the package with the chosen
    // locales, and send the batch; the site marks the parts ready (or waits for the owner's
    // "uploaded" when a dub track is among them).
    const captions = await run(ctx, ["captions", "--slug", slug]);
    if (captions.code !== 0) return this.block(state, `captions failed: ${lastLine(captions.out)}`);
    const packaged = await run(ctx, ["package", "--slug", slug]);
    if (packaged.code !== 0) return this.block(state, `package failed: ${lastLine(packaged.out)}`);
    const pushed = await run(ctx, ["review-push", "--slug", slug, "--gate", "languages"]);
    // A rejected payload will not recover next round. Park only this video so later
    // videos can run; the existing one-shot retry resumes it after the payload is fixed.
    if (pushed.code === ctx.EXIT.lint) return this.block(state, `language submission rejected: ${lastLine(pushed.out, 2)}`);
    if (pushed.code !== 0) return this.later(`${slug}: could not send the language batch: ${lastLine(pushed.out, 2)}`);
    await this.pull(slug);
    await report(ctx, this.api, state, "languages sent");
    return `${slug}: language batch sent to /admin/videos (${pending.map(({ locale, parts }) => `${locale} ${parts.join("+")}`).join(", ")})`;
  }

  /** The chosen parts the site still reports as in the making, by locale in the page's order. */
  pendingLanguages(video, choice) {
    const pending = [];
    for (const [locale, chosen] of Object.entries(choice?.locales ?? {})) {
      const states = video.languages?.[locale] ?? {};
      const working = LOCALE_PARTS.filter((part) => chosen[part] && (states[part]?.state ?? "working") === "working");
      if (working.length) pending.push({ locale, parts: working });
    }
    return pending;
  }

  /**
   * One locale's translation of the parts the owner chose (docs/videos/LANGUAGES.md): the sheet
   * `i18n-sheet --parts` writes (with each line's dub budget when a dub is chosen), filled by the
   * translator and read by the caption reviewer, then merged. Null when the sheet has nothing
   * left to translate; else this run's line.
   */
  async translateLocale(state, locale, parts, video) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const sheetResult = await run(ctx, ["i18n-sheet", "--slug", state.slug, "--locale", locale, "--parts", parts.join(",")]);
    if (sheetResult.code !== 0) return this.block(state, `i18n-sheet ${locale} failed: ${sheetResult.out.trim()}`);
    const sheetFile = path.join(workdir, "i18n", `${locale}.todo.json`);
    const sheet = readJson(sheetFile, null);
    if (!sheet) return this.block(state, `no ${locale} worksheet was written`);
    if (sheetDone(sheet)) return null;
    // The sheet's identity travels with it, whatever the model leaves out.
    const keep = (worksheet) => ({ ...worksheet, locale, slug: sheet.slug, parts: sheet.parts });
    const translated = await this.stage("translator", state.slug, { locale, parts, worksheet: sheet, video }, 32_000, state.format);
    if (!Array.isArray(translated.worksheet?.lines)) return this.retryLater(state, "translator", `the ${locale} translation returned no worksheet`);
    writeFileSync(sheetFile, `${JSON.stringify(keep(translated.worksheet), null, 2)}\n`);
    const reviewed = await this.stage("caption_reviewer", state.slug, { locale, parts, worksheet: keep(translated.worksheet), video }, 32_000, state.format);
    if (Array.isArray(reviewed.worksheet?.lines)) writeFileSync(sheetFile, `${JSON.stringify(keep(reviewed.worksheet), null, 2)}\n`);
    const merged = await run(ctx, ["i18n-merge", "--slug", state.slug, "--locale", locale]);
    if (merged.code !== 0) return this.retryLater(state, "translator", `the ${locale} translation does not merge: ${lastLine(merged.out, 2)}`);
    this.cleared(state, "translator");
    saveState(workdir, state);
    await report(ctx, this.api, state, "languages");
    return `${state.slug}: ${locale} ${parts.join(" and ")} translated and reviewed`;
  }

  /**
   * One locale's dub track (docs/videos/DUBS.md): `dub`, and when a window does not fit even at
   * MAX_TEMPO, the translator shortens those lines and `dub` runs again, MAX_DUB_SHORTEN_ROUNDS
   * times; then Jev listens (`check-audio --locale`) and the flagged lines are retaken,
   * MAX_DUB_RETAKE_ROUNDS times. What still fails after that, and what needs the owner (a voice
   * that speaks one language, a missing key), gives the locale up with the reason instead of
   * blocking the video; a service that is down ends this run and the next one tries again.
   */
  async makeDub(state, locale) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    const rounds = { shorten: 0, retakes: 0, ...(state.languages?.[locale] ?? {}) };
    const remember = () => {
      state.languages = { ...(state.languages ?? {}), [locale]: rounds };
      saveState(workdir, state);
    };
    const dubArgs = ["dub", "--slug", slug, "--locale", locale];
    let made = await run(ctx, dubArgs);
    while (made.code === 1 && rounds.shorten < MAX_DUB_SHORTEN_ROUNDS) {
      const over = readJson(dubArtifacts(workdir, locale).fit, null)?.over;
      if (!Array.isArray(over) || !over.length) break;
      rounds.shorten += 1;
      remember();
      const shortened = await this.shortenDub(state, locale, over);
      if (shortened.stopped) return shortened.stopped;
      // Nothing usable came back: the same windows would only be over again.
      if (!shortened.ids.length) break;
      made = await run(ctx, dubArgs);
    }
    if (made.code === 1) {
      const over = readJson(dubArtifacts(workdir, locale).fit, null)?.over ?? [];
      const why = over.length ? `${over.length} lines (${over.map((line) => line.id).join(", ")}) do not fit even at ${MAX_TEMPO}x after ${rounds.shorten} shortening round${rounds.shorten === 1 ? "" : "s"}` : lastLine(made.out);
      return this.giveUpDub(state, locale, why);
    }
    if (made.code === 3) return this.giveUpDub(state, locale, `dub needs the owner: ${lastLine(made.out)}`);
    if (made.code === 4) return this.later(`${slug}: ${locale} dub could not finish (${lastLine(made.out)}); the next run tries again`);
    if (made.code !== 0) return this.block(state, `dub ${locale} failed: ${lastLine(made.out, 2)}`);
    const flags = path.join(workdir, "review", `check-flags.${locale}.json`);
    const checkArgs = ["check-audio", "--slug", slug, "--locale", locale];
    let check = await run(ctx, checkArgs);
    while (check.code === 1 && rounds.retakes < MAX_DUB_RETAKE_ROUNDS) {
      rounds.retakes += 1;
      remember();
      const redo = await run(ctx, [...dubArgs, "--redo", flags]);
      if (redo.code === 4) return this.later(`${slug}: ${locale} dub retake could not finish (${lastLine(redo.out)}); the next run tries again`);
      if (redo.code === 1 || redo.code === 3) return this.giveUpDub(state, locale, `the retake failed: ${lastLine(redo.out)}`);
      if (redo.code !== 0) return this.block(state, `dub ${locale} retake failed: ${lastLine(redo.out, 2)}`);
      check = await run(ctx, checkArgs);
    }
    if (check.code === 4) return this.later(`${slug}: ${locale} dub check could not finish (${lastLine(check.out)}); the next run tries again`);
    if (check.code === 1) return this.giveUpDub(state, locale, `Jev still hears lines wrong after ${rounds.retakes} retake${rounds.retakes === 1 ? "" : "s"}: ${lastLine(check.out)}`);
    if (check.code === 3) return this.giveUpDub(state, locale, `the dub check needs the owner: ${lastLine(check.out)}`);
    if (check.code !== 0) return this.block(state, `check-audio ${locale} failed: ${lastLine(check.out, 2)}`);
    if (state.languages) delete state.languages[locale];
    saveState(workdir, state);
    await report(ctx, this.api, state, "languages");
    const rounding = [rounds.shorten ? `${rounds.shorten} shortening round${rounds.shorten === 1 ? "" : "s"}` : "", rounds.retakes ? `${rounds.retakes} retake${rounds.retakes === 1 ? "" : "s"}` : ""].filter(Boolean).join(", ");
    return `${slug}: ${locale} dub made${rounding ? ` after ${rounding}` : ""}; Jev passed every line`;
  }

  /** Give a locale's dub up with the reason (dubs/<locale>/skipped.json); the batch reports it, the video goes on. */
  giveUpDub(state, locale, reason) {
    const workdir = this.workdir(state.slug);
    const files = dubArtifacts(workdir, locale);
    mkdirSync(files.dir, { recursive: true });
    atomicWrite(files.skipped, `${JSON.stringify({ reason, at: this.ctx.now().toISOString() }, null, 2)}\n`);
    state.notes.push(`${locale} dub skipped: ${reason}`);
    if (state.languages) delete state.languages[locale];
    saveState(workdir, state);
    this.log(`  ${locale} dub given up: ${reason}`);
    return `${state.slug}: ${locale} dub given up (${reason}); the video goes on without it`;
  }

  /**
   * The translator's shortening pass (docs/videos/DUBS.md): the lines of the windows that do not
   * fit even sped up, with their budgets from fit.json, go to the translator (variant "shorten").
   * A shortened line that is shorter and keeps every digit replaces the translation through a
   * captions-only sheet and i18n-merge, so the captions and the dub read the same words and the
   * hashes are the tool's; the rest are dropped with the reason in the notes. Answers { ids,
   * problems }, or { stopped } with this run's line when the answer was unusable.
   */
  async shortenDub(state, locale, over) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    const dir = docDir(slug, ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const translation = readJson(path.join(dir, "i18n", `${locale}.json`), { lines: {} });
    const sources = new Map([...eachLine(video)].map(({ line }) => [line.id, line.text]));
    const lines = over
      .filter((entry) => sources.has(entry.id) && typeof translation.lines?.[entry.id]?.text === "string")
      .map((entry) => ({ id: entry.id, source: sources.get(entry.id), text: translation.lines[entry.id].text, chars: entry.chars, max_chars: entry.max_chars, ...(entry.seconds === undefined ? {} : { seconds: entry.seconds }), window_over_seconds: entry.window_over_seconds }));
    if (!lines.length) return { ids: [], problems: ["no line to shorten has a current translation"] };
    const answer = await this.stage("translator", slug, { locale, lines, video }, 16_000, state.format, "shorten");
    if (!Array.isArray(answer?.lines)) return { stopped: await this.retryLater(state, "translator", `the ${locale} shortening pass answered without a lines array`) };
    this.cleared(state, "translator");
    const accepted = new Map();
    const problems = [];
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const before = lines.find((each) => each.id === id);
      if (!before) {
        problems.push(`${id || "?"}: not one of the lines to shorten`);
        continue;
      }
      if (accepted.has(id)) continue;
      const after = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!after) {
        problems.push(`${id}: the shortened line is empty`);
        continue;
      }
      if ([...after].length >= [...before.text].length) {
        problems.push(`${id}: not shorter (${[...after].length} characters, was ${[...before.text].length})`);
        continue;
      }
      if (digitsOf(after) !== digitsOf(before.text)) {
        problems.push(`${id}: the numbers changed`);
        continue;
      }
      accepted.set(id, after);
    }
    if (accepted.size) {
      const sheetResult = await run(ctx, ["i18n-sheet", "--slug", slug, "--locale", locale, "--parts", "captions"]);
      if (sheetResult.code !== 0) return { stopped: await this.block(state, `i18n-sheet ${locale} failed: ${lastLine(sheetResult.out)}`) };
      const sheetFile = path.join(workdir, "i18n", `${locale}.todo.json`);
      const sheet = readJson(sheetFile);
      sheet.lines = sheet.lines.map((line) => (accepted.has(line.id) ? { ...line, text: accepted.get(line.id) } : line));
      writeFileSync(sheetFile, `${JSON.stringify(sheet, null, 2)}\n`);
      const merged = await run(ctx, ["i18n-merge", "--slug", slug, "--locale", locale]);
      if (merged.code !== 0) return { stopped: await this.retryLater(state, "translator", `the shortened ${locale} lines do not merge: ${lastLine(merged.out, 2)}`) };
    }
    for (const [id, text] of accepted) state.notes.push(`${locale} dub line shortened: ${id} → 「${text}」`);
    for (const problem of problems) state.notes.push(`${locale} shortening dropped: ${problem}`);
    saveState(workdir, state);
    this.log(`  ${locale} shortening: ${accepted.size} of ${lines.length} lines shortened${problems.length ? `, ${problems.length} dropped` : ""}`);
    return { ids: [...accepted.keys()], problems };
  }

  /**
   * A gate the site decides: the final cut. `review-push --gate final` runs the quality check
   * and sends its report; the site approves on arrival when every item passed and the owner's
   * switch is on, else the owner decides. A push that could not finish (the check's service, the
   * site) ends this run and is tried again next round.
   */
  async gate(state, gate, file) {
    const review = await this.decision(state, gate, file);
    if (!review) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", gate]);
      if (pushed.code !== 0) return this.later(`${state.slug}: could not send the ${gate} for review: ${lastLine(pushed.out, 2)}`);
      return `${state.slug}: ${gate} sent to /admin/videos (${lastLine(pushed.out)})`;
    }
    if (review.status === "approved") {
      await this.pull(state.slug);
      if (review.note) state.notes.push(`${gate}: ${review.note}`);
      saveState(this.workdir(state.slug), state);
      // The site's checklist shows the step done at once: the language panel opens on it (docs/videos/LANGUAGES.md).
      await report(this.ctx, this.api, state, `${gate} approved`);
      return `${state.slug}: the ${gate} is approved${review.note ? ` (${review.note})` : ""}`;
    }
    if (review.status === "rejected") return this.block(state,`the owner sent the ${gate} back: ${review.note}`);
    return null;
  }
}
