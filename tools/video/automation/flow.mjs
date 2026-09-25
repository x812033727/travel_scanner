// The automated pipeline, one unit of work at a time (docs/videos/AUTOMATION.md).
//
// `pipelineStatus` already knows the next step of a video from the hashes in its files. This
// adds what it cannot see (whether the fact-check rounds and the listener edit are done, how
// many retakes were tried, what the owner wrote when sending something back) in
// <workdir>/<slug>/auto.json, and does that step: a writing stage through the server's model
// runner, or one of the existing commands. The three gates the owner keeps — outline, final cut,
// publishing — stop the video until they decide on /admin/videos; narration waits too unless
// Jev passed every line and the owner left automatic approval on.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { sha256File } from "../core/approvals.mjs";
import { atomicWrite, contentPackFile, docDir, lexiconFile, readJson, resolveWorkBase, resolveWorkdir, ROOT } from "../core/paths.mjs";
import { eachLine, LINE_ID } from "../core/schema.mjs";
import { lintProject, loadProject, pipelineStatus } from "../core/state.mjs";
import { checklistFrom, guideSlugs, outlineOptions, sourceGuideOf } from "../review/sync.mjs";
import { AutomationError } from "./client.mjs";
import { pageReader, urlsIn } from "./fetch.mjs";
import { INSTRUCTIONS, parseAnswer, references } from "./prompts.mjs";

export const STATE_FILE = "auto.json";
const GLOBAL_FILE = "auto-state.json";
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?$/;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
export const MAX_LINT_FIXES = 3;
export const MAX_REPLANS = 2;
export const MAX_STAGE_FAILURES = 2;
const OUTPUT_INVALID = "video_ai_output_invalid";
const MAX_SOURCE_PAGES = 25;
const MAX_SOURCE_CHARS = 350_000;
const REQUIRED_SECTIONS = ["## 觀眾看完能做到的事", "## 站主觀點", "## 大綱"];

const today = (ctx) => ctx.now().toISOString().slice(0, 10);

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

/** Whether a translation worksheet has nothing left to fill. */
export function sheetDone(sheet) {
  const filled = (entry) => typeof entry?.text === "string" && entry.text.trim() !== "";
  return !sheet.lines.some((line) => line.todo) && filled(sheet.title) && filled(sheet.description) && sheet.chapters.every(filled) && Array.isArray(sheet.tags?.text) && sheet.tags.text.length > 0;
}

function titleOf(brief) {
  return (/^#\s+(.+)$/m.exec(brief)?.[1] ?? "").trim().slice(0, 200);
}

/** The site article a video retells: its source_guide, or else the first site article it rests on. */
export function mainGuide({ source_guide: guide, source_urls: urls }) {
  return (GUIDE_SLUG.test(guide ?? "") ? guide : null) ?? guideSlugs(urls)[0] ?? null;
}

/** What makes a planner's answer unusable, or null. `usedGuides` are earlier videos' main articles. */
export function planProblem(plan, taken, usedGuides = new Set()) {
  if (!plan || typeof plan !== "object") return "the answer is not an object";
  if (!SLUG.test(plan.slug ?? "")) return `slug "${plan.slug}" is not lowercase kebab-case of at most 60 characters`;
  if (taken.has(plan.slug)) return `slug "${plan.slug}" is already used by an earlier video`;
  if (typeof plan.brief !== "string") return "brief is missing";
  const missing = REQUIRED_SECTIONS.filter((heading) => !plan.brief.includes(heading));
  if (missing.length) return `brief lacks ${missing.join(", ")}`;
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

/** video.json as the owner's settings say it must be, whatever the model returned. */
export function settle(video, { slug, settings, sourceGuide, root }) {
  // Gemini takes its pace from the style and has no rate; Azure has a rate and no style or model.
  const unused = settings.voice.provider === "gemini" ? ["rate"] : ["style", "model"];
  const voice = Object.fromEntries(Object.entries(settings.voice).filter(([key, value]) => value !== null && value !== "" && !unused.includes(key)));
  const settled = { ...video, slug, voice };
  // The description links the article through its content pack. An article the news automation
  // published lives only in the database, so without a pack the script names it in sources instead.
  if (sourceGuide && existsSync(contentPackFile(sourceGuide, root))) settled.source_guide = sourceGuide;
  else delete settled.source_guide;
  settled.assets = [];
  if (settled.youtube) settled.youtube = { ...settled.youtube, video_id: null };
  return settled;
}

function lintErrors(ctx, slug) {
  const result = lintProject(loadProject({ slug, root: ctx.root }));
  return result.errors.map((error) => `${error.path}: ${error.message}`);
}

async function run(ctx, command) {
  const { main } = await import("../cli.mjs");
  let out = "";
  const sink = { write: (text) => (out += text) };
  const code = await main(command, { ...ctx, stdout: sink, stderr: sink });
  return { code, out };
}

/** Hand everything the automation knows to /admin/videos: title, stage, checklist, article. */
async function report(ctx, api, state, stage) {
  const workdir = resolveWorkdir({ env: ctx.env, slug: state.slug, root: ctx.root, home: ctx.home });
  const status = await pipelineStatus({ slug: state.slug, root: ctx.root, workdir });
  const guide = mainGuide(state);
  // The page has no field for why a video stopped; the checklist is what the owner reads.
  const blocked = state.status === "blocked" && state.blocked ? [{ key: "blocked", label: `卡住，需要人處理：${state.blocked}`.slice(0, 120), done: false }] : [];
  await api.report(state.slug, { title: state.title || state.slug, stage: stage.slice(0, 40), checklist: [...blocked, ...checklistFrom(status.steps)], ...(guide ? { source_guide: guide } : {}) });
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

  /** The skill's reference texts, from the tool's own repository whatever root the docs are under. */
  reference() {
    this.refs ??= references(ROOT);
    return this.refs;
  }

  async stage(stage, slug, payload, maxOutputTokens) {
    const answer = await this.api.run(stage, slug, INSTRUCTIONS[stage], payload, maxOutputTokens);
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
    for (const state of automatedVideos(this.workBase)) {
      if (state.status !== "active") continue;
      let done;
      try {
        done = await this.advance(state);
      } catch (error) {
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        return this.retryLater(state, error.stage, error.message);
      }
      if (done) return done;
    }
    if (this.due()) return this.draft();
    return null;
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
    const active = automatedVideos(this.workBase).filter((state) => state.status === "active").length;
    if (active >= this.settings.max_waiting_drafts) return false;
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

  planPayload(extra, earlier = this.earlierVideos()) {
    const refs = this.reference();
    return {
      today: today(this.ctx),
      scope: this.settings.topic_scope,
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
      problem = planProblem(answer, taken, usedGuides);
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
      notes: [],
    };
    saveState(this.workdir(plan.slug), state);
    await this.submitOutline(state);
    return `draft: ${plan.slug} planned from ${topics.length} topics; outline sent to /admin/videos`;
  }

  async submitOutline(state) {
    const file = path.join(docDir(state.slug, this.ctx.root), "brief.md");
    const brief = readFileSync(file, "utf8");
    await report(this.ctx, this.api, state, "outline approved");
    const options = outlineOptions(brief);
    await this.api.submit(state.slug, { gate: "outline", content_sha256: await sha256File(file), summary: `企劃書與 ${options.length} 個大綱選項（自動產生）`, payload: { brief, options }, files: [] });
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

    if (next === "outline approved") {
      const review = await this.decision(state, "outline", path.join(dir, "brief.md"));
      if (!review) {
        await this.submitOutline(state);
        return `${state.slug}: outline re-sent to /admin/videos`;
      }
      if (review.status === "approved") {
        await this.pull(state.slug);
        state.chosen = review.choice;
        state.notes.push(...(review.note ? [`outline: ${review.note}`] : []));
        saveState(workdir, state);
        return `${state.slug}: the owner chose outline ${review.choice}`;
      }
      if (review.status === "rejected") {
        if (state.replans >= MAX_REPLANS) return this.block(state,`the owner sent the outline back ${state.replans + 1} times: ${review.note}`);
        return this.replan(state, review.note ?? "");
      }
      return null;
    }

    if (next === "brief") return this.block(state,"brief.md is gone");
    if (next === "script passes lint") return this.write(state);
    // status only knows that verify-1.md exists; the rounds and the listener edit are ours.
    if (!state.verified) return this.verify(state);
    if (!state.listener_done) return this.listen(state);

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
        saveState(workdir, state);
        return `${state.slug}: the owner confirmed the upload; they upload it in YouTube Studio`;
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

  async replan(state, note) {
    const dir = docDir(state.slug, this.ctx.root);
    const previous = readFileSync(path.join(dir, "brief.md"), "utf8");
    const earlier = this.earlierVideos().filter((video) => video.slug !== state.slug);
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const { topics } = await this.api.topics();
    const answer = await this.stage("planner", state.slug, this.planPayload({ topics, owner_note: note, previous_brief: previous, slug: state.slug }, earlier));
    const problem = planProblem({ ...answer, slug: state.slug }, taken, usedGuides);
    state.replans += 1;
    state.notes.push(`outline sent back: ${note}`);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "planner", `the re-planned brief was not usable (${problem})`);
    this.cleared(state, "planner");
    writeFileSync(path.join(dir, "brief.md"), answer.brief.endsWith("\n") ? answer.brief : `${answer.brief}\n`);
    state.source_urls = (answer.source_urls ?? state.source_urls).slice(0, 12);
    state.source_guide = answer.source_guide ?? state.source_guide;
    saveState(this.workdir(state.slug), state);
    await this.submitOutline(state);
    return `${state.slug}: brief rewritten after the owner's note; outline re-sent`;
  }

  scriptPayload(state, extra) {
    const refs = this.reference();
    const lexicon = readJson(lexiconFile(this.ctx.root), { terms: {} });
    return {
      today: today(this.ctx),
      slug: state.slug,
      voice: this.settings.voice,
      source_guide: state.source_guide,
      target_minutes: [this.settings.target_minutes_min, this.settings.target_minutes_max],
      lexicon: Object.keys(lexicon.terms),
      script_writing: refs.script_writing,
      channel: refs.channel,
      minimal: refs.minimal,
      showcase: refs.showcase,
      owner_notes: state.notes,
      ...extra,
    };
  }

  /** Save a stage's video.json and lexicon terms, then fix lint errors with the writer, up to 3 times. */
  async saveAndLint(state, answer) {
    const dir = docDir(state.slug, this.ctx.root);
    let current = answer;
    for (let fix = 0; ; fix++) {
      if (!current?.video || typeof current.video !== "object") return "the answer has no video object";
      writeVideo(dir, settle(current.video, { slug: state.slug, settings: this.settings, sourceGuide: state.source_guide, root: this.ctx.root }));
      const added = mergeLexicon(this.ctx.root, current.lexicon_additions);
      if (added.length) state.lexicon_added = [...new Set([...(state.lexicon_added ?? []), ...added])];
      const errors = lintErrors(this.ctx, state.slug);
      if (!errors.length) return null;
      if (fix >= MAX_LINT_FIXES) return `lint still fails after ${MAX_LINT_FIXES} fixes: ${errors.slice(0, 3).join("; ")}`;
      const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
      current = await this.stage("writer", state.slug, this.scriptPayload(state, { video, lint_errors: errors, line_ids: this.freshIds(state, video, 40) }), 32_000);
    }
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
    const siteUrl = state.source_guide ? [`https://mokaair.com/zh-TW/guides/${state.source_guide}`] : [];
    const sources = await readSources(this.read, [...siteUrl, ...(state.source_urls ?? [])]);
    const answer = await this.stage("writer", state.slug, this.scriptPayload(state, { brief, chosen_option: option, sources, line_ids: this.freshIds(state, null, 140) }), 32_000);
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    const problem = await this.saveAndLint(state, answer);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "writer", `the script ${problem}`);
    this.cleared(state, "writer");
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "fact-checked");
    return `${state.slug}: script drafted and passes lint`;
  }

  async verify(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const claims = existsSync(path.join(dir, "claims.md")) ? readFileSync(path.join(dir, "claims.md"), "utf8") : "";
    const round = state.verify_rounds + 1;
    const urls = [...urlsIn(claims), ...(video.sources ?? []).map((source) => source.url), ...(state.source_urls ?? [])];
    const sources = await readSources(this.read, urls);
    const answer = await this.stage("verifier", state.slug, { today: today(this.ctx), round, video, claims, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), sources }, 32_000);
    if (typeof answer.report !== "string") return this.retryLater(state, "verifier", `fact-check round ${round} returned no report`);
    writeFileSync(path.join(dir, `verify-${round}.md`), answer.report.endsWith("\n") ? answer.report : `${answer.report}\n`);
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    state.verify_rounds = round;
    const changed = Number(answer.changed_facts) || 0;
    if (answer.video) {
      const problem = await this.saveAndLint(state, { video: answer.video });
      if (problem) return this.retryLater(state, "verifier", `fact-check round ${round} changed ${changed} facts but ${problem}`);
    }
    state.verified = changed <= 3 || round >= this.settings.max_verify_rounds;
    this.cleared(state, "verifier");
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: fact-check round ${round}, ${changed} facts changed${state.verified ? "" : "; another round follows"}`;
  }

  async listen(state, note = null) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const answer = await this.stage("listener", state.slug, { video, script_writing: this.reference().script_writing, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), ...(note ? { owner_note: note } : {}) }, 32_000);
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
    while (check.code === 1 && state.retakes < this.settings.max_retake_rounds) {
      state.retakes += 1;
      saveState(workdir, state);
      const redo = await run(ctx, ["tts", "--slug", state.slug, "--redo", path.join(workdir, "review", "check-flags.json")]);
      if (redo.code !== 0) return this.block(state,`retake failed: ${redo.out.trim().split("\n").at(-1)}`);
      check = await run(ctx, ["check-audio", "--slug", state.slug]);
    }
    if (check.code === 4) return this.later(`${state.slug}: narration check could not finish (${check.out.trim().split("\n").at(-1)}); the next run tries again`);
    const pushed = await run(ctx, ["review-push", "--slug", state.slug, "--gate", "audio"]);
    if (pushed.code !== 0) return this.later(`${state.slug}: could not send the narration for review: ${pushed.out.trim()}`);
    await this.pull(state.slug);
    return `${state.slug}: narration checked (${check.code === 0 ? "Jev passed every line" : "some lines flagged"}) and sent for review`;
  }

  async captions(state) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const dir = docDir(state.slug, ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    for (const locale of this.settings.caption_locales) {
      const sheetResult = await run(ctx, ["i18n-sheet", "--slug", state.slug, "--locale", locale]);
      if (sheetResult.code !== 0) return this.block(state,`i18n-sheet ${locale} failed: ${sheetResult.out.trim()}`);
      const sheetFile = path.join(workdir, "i18n", `${locale}.todo.json`);
      const sheet = readJson(sheetFile, null);
      if (!sheet) return this.block(state, `no ${locale} worksheet was written`);
      if (sheetDone(sheet)) continue;
      const translated = await this.stage("translator", state.slug, { locale, worksheet: sheet, video }, 32_000);
      if (!translated.worksheet?.lines) return this.retryLater(state, "translator", `the ${locale} translation returned no worksheet`);
      writeFileSync(sheetFile, `${JSON.stringify(translated.worksheet, null, 2)}\n`);
      const reviewed = await this.stage("caption_reviewer", state.slug, { locale, worksheet: translated.worksheet, video }, 32_000);
      if (reviewed.worksheet?.lines) writeFileSync(sheetFile, `${JSON.stringify(reviewed.worksheet, null, 2)}\n`);
      const merged = await run(ctx, ["i18n-merge", "--slug", state.slug, "--locale", locale]);
      if (merged.code !== 0) return this.retryLater(state, "translator", `the ${locale} captions do not merge: ${merged.out.trim().split("\n").slice(-2).join(" ")}`);
      this.cleared(state, "translator");
      saveState(workdir, state);
      return `${state.slug}: ${locale} captions translated and reviewed`;
    }
    const result = await run(ctx, ["captions", "--slug", state.slug]);
    if (result.code !== 0) return this.block(state,`captions failed: ${result.out.trim()}`);
    return `${state.slug}: captions written`;
  }

  async gate(state, gate, file) {
    const review = await this.decision(state, gate, file);
    if (!review) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", gate]);
      if (pushed.code !== 0) return this.later(`${state.slug}: could not send the ${gate} for review: ${pushed.out.trim()}`);
      return `${state.slug}: ${gate} sent to /admin/videos`;
    }
    if (review.status === "approved") {
      await this.pull(state.slug);
      return `${state.slug}: the owner approved the ${gate}`;
    }
    if (review.status === "rejected") return this.block(state,`the owner sent the ${gate} back: ${review.note}`);
    return null;
  }
}
