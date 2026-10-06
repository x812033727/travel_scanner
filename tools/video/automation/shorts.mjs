// The worker's Shorts (docs/videos/SHORTS.md §排片與時段、§成效與每週報告、§工具端): once a round of
// `auto`, `shortsStep` asks the site for the next Shorts job and does it — the weekly report, the
// week's calendar, new topics for the pool, or one Short to make — governed by the Shorts settings
// alone, whatever the tutorials' switch says. The knock that lets the site do what is due on the
// calendar is not here: the worker's loop script runs `shorts/cli.mjs tick` on its own clock.
//
// The order within a round (cli.mjs): while the library holds fewer days of Shorts than the
// settings' stock_days, the Shorts go before the dramas and the tutorials; otherwise after them.
//
// The worker's rules hold here too: a model that gives nothing usable has its answer kept and the
// round ends; the same job failing twice in a row stops asking (a Short is blocked and the site
// says why; a plan is recorded empty so it is not asked again at once; a report is saved saying it
// could not be written, with the raw values; new topics wait half a day); a service that is down
// does not count; a STOP file is read between units. A planner job sent whose answer never came
// back (client.mjs RUN_UNCERTAIN) may have run and been paid for: its slug, one day's plan or brief
// or one week's report, is recorded under `lost` and that call is not asked again (`unanswered`).
import { mkdirSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite, lexiconFile, readJson, resolveWorkBase, ROOT, stopRequested } from "../core/paths.mjs";
import { LAB_SERIES } from "../shorts/core.mjs";
import { CutShort } from "../shorts/cut.mjs";
import { defaultTools, LAB_FILE, LabShort, labRefusal, numbersIn } from "../shorts/lab.mjs";
import { shortsInstructions } from "../shorts/prompts.mjs";
import { siteClient } from "../shorts/site.mjs";
import { AutomationError, automationClient, OUTPUT_INVALID, RUN_UNCERTAIN } from "./client.mjs";
import { parseAnswer } from "./prompts.mjs";

export const SHORTS_DIR = "_shorts";
export const SHORTS_STATE = "shorts-state.json";
// The content lines this worker makes so far: the experiments (lab.mjs) and the highlights of the
// published tutorials (cut.mjs). The vertical dramas come with their own ticket, so the plan
// leaves their topics to it.
export const MAKES = Object.freeze(["lab", "cut"]);
const MAX_PLANNER_TRIES = 2;
const MAX_JOB_FAILURES = 2;
// New topics that failed twice wait as long as the server waits between two briefs.
const BRIEF_HOLD_MS = 12 * 3600_000;
// A lost planner answer is remembered this long: its slug names a day or a week long gone by then.
const LOST_KEEP_MS = 14 * 86_400_000;
const TOPIC_SLUG = /^[a-z][a-z0-9-]{1,78}[a-z0-9]$/;
const SERIES = /^[a-z0-9][a-z0-9-]{0,39}$/;
const PERIODS = { d1: "第 1 天", d3: "第 3 天", d7: "第 7 天", now: "最新" };
const SOURCES = { data_api: "YouTube Data API", analytics_api: "YouTube Analytics API", studio_export: "Studio 匯出" };
const LINES = { lab: "實測", cut: "長片精華", drama: "漫劇直式短篇" };
const METRICS = [["views", "觀看"], ["engaged_views", "engaged views"], ["likes", "喜歡"], ["comments", "留言"], ["shares", "分享"], ["subscribers_gained", "新增訂閱"], ["avg_view_seconds", "平均觀看秒數"], ["avg_view_percent", "平均觀看百分比"], ["stayed_percent", "選擇觀看比例"]];
// What a report computes for itself, by name: the check refuses these words besides the numbers.
const DERIVED = /中位數|排名|名次|分數|成長率|達成率|加權/;
const REPORT_MAX = 40_000;

// --- the calendar ---------------------------------------------------------------------------------

/** A day in a time zone as YYYY-MM-DD; UTC when the zone is unknown. */
export function localDay(now, timezone) {
  try {
    return new Intl.DateTimeFormat("en-CA", { timeZone: timezone, year: "numeric", month: "2-digit", day: "2-digit" }).format(now);
  } catch {
    return now.toISOString().slice(0, 10);
  }
}

/** A moment in a time zone as "YYYY-MM-DD HH:MM". */
export function localTime(value, timezone) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value ?? "");
  try {
    const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", { timeZone: timezone, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(date).map((part) => [part.type, part.value]));
    return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}`;
  } catch {
    return date.toISOString().slice(0, 16).replace("T", " ");
  }
}

/**
 * How many slots the run's pattern has from `today` for `days` days (apps/api/app/video_shorts/rules.py
 * build_slots: each segment publishes its counts in turn, never more than there are slot times).
 * 0 before the run has a first day.
 */
export function slotsAhead(settings, today, days) {
  if (!settings?.campaign_start || !Array.isArray(settings.daily_pattern)) return 0;
  const times = Array.isArray(settings.slot_times) ? settings.slot_times.length : 1;
  const offset = Math.round((Date.parse(`${today}T00:00:00Z`) - Date.parse(`${settings.campaign_start}T00:00:00Z`)) / 86_400_000);
  let total = 0;
  for (let day = offset; day < offset + days; day++) {
    if (day < 0) continue;
    let index = day;
    for (const segment of settings.daily_pattern) {
      if (index < segment.days) {
        total += Math.min(segment.counts[index % segment.counts.length] ?? 0, times);
        break;
      }
      index -= segment.days;
    }
  }
  return total;
}

// --- what the planner wrote ------------------------------------------------------------------------

/** The plan's items the server can take from this worker, and why the others were left out. */
export function planItems(answer, job) {
  if (!Array.isArray(answer?.items)) return { items: [], dropped: [], problem: "the answer has no items list" };
  const slots = new Set((job.open_slots ?? []).map((slot) => slot.id));
  const topics = new Map((job.topics ?? []).map((topic) => [topic.slug, topic]));
  const items = [];
  const dropped = [];
  const usedSlots = new Set();
  const usedTopics = new Set();
  for (const item of answer.items) {
    const topic = topics.get(item?.topic_slug);
    if (!slots.has(item?.slot_id)) dropped.push(`${item?.slot_id}: not an open slot`);
    else if (!topic) dropped.push(`${item?.topic_slug}: not a topic of the pool`);
    else if (!MAKES.includes(topic.line)) dropped.push(`${topic.slug}: the worker does not make ${topic.line} yet`);
    else if (topic.line === "lab" && topic.paid) dropped.push(`${topic.slug}: needs a generated picture`);
    else if (usedSlots.has(item.slot_id) || usedTopics.has(topic.slug)) dropped.push(`${topic.slug}: twice in the plan`);
    else {
      usedSlots.add(item.slot_id);
      usedTopics.add(topic.slug);
      items.push({ slot_id: item.slot_id, topic_slug: topic.slug });
    }
  }
  return { items, dropped, problem: null };
}

const text = (value, max) => (typeof value === "string" && value.trim() ? value.trim().slice(0, max) : null);
const texts = (value, max, count) => (Array.isArray(value) ? value.map((each) => text(each, max)).filter(Boolean).slice(0, count) : []);

/** One topic as the server takes it (TopicIn, which refuses any other field), or the reason it cannot be. */
export function topicIn(raw, { ideas, taken }) {
  const slug = raw?.slug;
  const idea = ideas.get(slug);
  if (typeof slug !== "string" || !TOPIC_SLUG.test(slug)) return { problem: `${slug}: not a topic slug` };
  if (!idea && taken.has(slug)) return { problem: `${slug}: a topic or a video has that slug already` };
  const line = idea?.line ?? raw.line;
  if (line !== "lab") return { problem: `${slug}: the worker writes experiment topics only` };
  const series = idea?.series ?? raw.series;
  if (!LAB_SERIES.includes(series)) return { problem: `${slug}: the series must be ${LAB_SERIES.join(", ")}` };
  const title = text(raw.title, 200);
  if (!title) return { problem: `${slug}: no title` };
  const brief = raw.brief ?? {};
  const protocol = brief.test_protocol ?? {};
  const clean = {
    test_protocol: Object.fromEntries(["setup", "input", "condition_a", "condition_b", "runs", "scoring", "failure_path"].map((field) => [field, text(protocol[field], 2000)])),
    truth_check: texts(brief.truth_check, 600, 20),
    acceptance: texts(brief.acceptance, 600, 20),
    narration_outline: (Array.isArray(brief.narration_outline) ? brief.narration_outline : []).slice(0, 20).map((beat) => ({ seconds: text(beat?.seconds, 20), voice: text(beat?.voice, 400), visual: text(beat?.visual, 400) })),
    titles: texts(brief.titles, 600, 6),
    source_material: texts(brief.source_material, 600, 20),
    ...(Number.isInteger(brief.estimated_seconds) && brief.estimated_seconds >= 10 && brief.estimated_seconds <= 180 ? { estimated_seconds: brief.estimated_seconds } : {}),
    ...(text(brief.notes, 4000) ? { notes: text(brief.notes, 4000) } : {}),
  };
  const hook = text(raw.hook, 300);
  return { topic: { slug, line, series, title, ...(hook ? { hook } : {}), brief: clean } };
}

/** The topics of a brief answer the server can take, and the reasons for the rest. */
export function briefTopics(answer, job) {
  if (!Array.isArray(answer?.topics)) return { topics: [], dropped: ["the answer has no topics list"] };
  const ideas = new Map((job.ideas ?? []).map((idea) => [idea.slug, idea]));
  const taken = new Set((job.existing ?? []).map((topic) => topic.slug));
  const topics = [];
  const dropped = [];
  for (const raw of answer.topics.slice(0, 30)) {
    const { topic, problem } = topicIn(raw, { ideas, taken });
    if (problem) dropped.push(problem);
    else {
      taken.add(topic.slug);
      topics.push(topic);
    }
  }
  return { topics, dropped };
}

// --- the weekly report ---------------------------------------------------------------------------

const shown = (value) => (value === null || value === undefined || value === "" ? "—" : String(value));

/**
 * The table of raw values the report ends with, printed by the program, never by the model: every
 * snapshot as YouTube reported it with its source and the time it was read, the missed slots, the
 * week's ledger and the budget as the server gave them, next week's calendar.
 */
export function rawTable(job) {
  const zone = job.timezone;
  const lines = [`## 原值表（照抄伺服器存的數字，不是本站算的）`, "", `週：${job.week_start} 到 ${job.week_end}（${zone}）`, ""];
  const used = METRICS.filter(([field]) => (job.published ?? []).some((short) => short.snapshots.some((snapshot) => snapshot[field] !== null && snapshot[field] !== undefined)));
  const metrics = used.length ? used : METRICS.slice(0, 3);
  lines.push("### 上週公開的 Shorts", "");
  if (!(job.published ?? []).length) lines.push("上週沒有公開的 Shorts。", "");
  else {
    lines.push(`| Short | 內容線 | 系列 | 公開時間 | 時間窗 | 來源 | 讀取時間 | ${metrics.map(([, label]) => label).join(" | ")} |`);
    lines.push(`| ${["---", "---", "---", "---", "---", "---", "---", ...metrics.map(() => "---")].join(" | ")} |`);
    for (const short of job.published) {
      const head = [`${short.title}（${short.slug}，${short.youtube_video_id}）`, LINES[short.line] ?? shown(short.line), shown(short.series), localTime(short.published_at, zone)];
      if (!short.snapshots.length) lines.push(`| ${[...head, "還沒有讀到", "—", "—", ...metrics.map(() => "—")].join(" | ")} |`);
      for (const snapshot of short.snapshots) {
        lines.push(`| ${[...head, PERIODS[snapshot.period] ?? snapshot.period, SOURCES[snapshot.source] ?? snapshot.source, localTime(snapshot.captured_at, zone), ...metrics.map(([field]) => shown(snapshot[field]))].join(" | ")} |`);
      }
    }
    lines.push("");
  }
  lines.push("### 錯過的時段", "");
  if (!(job.missed ?? []).length) lines.push("沒有。", "");
  else lines.push(...job.missed.map((slot) => `- ${slot.local_date} ${slot.local_time}：${shown(slot.topic_slug)}（${LINES[slot.line] ?? "未定內容線"}）`), "");
  lines.push("### 花費", "");
  if (!(job.costs ?? []).length) lines.push("這一週沒有帳。", "");
  else {
    lines.push("| 時間 | 項目 | Short | 金額 | 幣別 | 新台幣 | 狀態 | 備註 |", "| --- | --- | --- | --- | --- | --- | --- | --- |");
    for (const cost of job.costs) lines.push(`| ${[localTime(cost.occurred_at, zone), cost.category, shown(cost.project_slug), shown(cost.amount), cost.currency, shown(cost.amount_ntd), cost.status, shown(cost.note)].join(" | ")} |`);
    lines.push("");
  }
  const budget = job.budget ?? {};
  lines.push(`預算：這一期（${localTime(budget.period_start, zone)} 起）已花 NT$${shown(budget.spent_ntd)}、預留 NT$${shown(budget.reserved_ntd)}、金額未知 ${shown(budget.unknown)} 筆；上限 NT$${shown(budget.limit_ntd)}，到 NT$${shown(budget.soft_ntd)} 停開新的付費工作；全程已花 NT$${shown(budget.total_spent_ntd)}，上限 NT$${shown(budget.total_limit_ntd)}。${budget.reason ? `（${budget.reason}）` : ""}`, "");
  lines.push("### 下週的時段", "");
  if (!(job.next_week ?? []).length) lines.push("還沒有時段。");
  else lines.push(...job.next_week.map((slot) => `- ${slot.local_date} ${slot.local_time}：${shown(slot.topic_slug)}（${LINES[slot.line] ?? "未定內容線"}，${slot.status}）`));
  return lines.join("\n");
}

/** Why the report's own text cannot go: a number the table does not have, a derived metric by name. */
export function reportProblems(body, table) {
  if (typeof body !== "string" || !body.trim()) return ["body_md is empty"];
  const problems = [];
  const known = new Set(numbersIn(table));
  const strange = [...new Set(numbersIn(body).filter((number) => !known.has(number)))];
  if (strange.length) problems.push(`these numbers are not in raw_values: ${strange.join(", ")} (copy a number only as it stands there; write counts in words)`);
  const derived = DERIVED.exec(body);
  if (derived) problems.push(`「${derived[0]}」is a metric computed from YouTube's numbers; judge in words instead`);
  if (body.length + table.length + 2 > REPORT_MAX) problems.push(`the report is too long (at most ${REPORT_MAX - table.length - 2} characters above the table)`);
  return problems;
}

// --- the round -------------------------------------------------------------------------------------

export class ShortsWorker {
  /** `settings` are the tutorials' (the verifier's rounds); the Shorts settings are read here. */
  constructor(ctx, api, settings = {}) {
    this.ctx = ctx;
    this.api = api;
    this.settings = settings;
    this.shorts = undefined;
    this.lastAnswer = null;
  }

  get base() {
    return path.join(resolveWorkBase({ env: this.ctx.env, root: this.ctx.root, home: this.ctx.home }), SHORTS_DIR);
  }

  log(line) {
    this.ctx.stdout.write(`${line}\n`);
  }

  state() {
    return readJson(path.join(this.base, SHORTS_STATE), { failures: {}, holds: {} });
  }

  saveState(state) {
    atomicWrite(path.join(this.base, SHORTS_STATE), `${JSON.stringify(state, null, 2)}\n`);
  }

  /** The Shorts settings, read once a round; null on a site without Shorts. */
  async settingsNow() {
    if (this.shorts === undefined) this.shorts = await this.api.shortsSettings();
    return this.shorts;
  }

  /** Whether the library holds fewer days of Shorts than stock_days: then the Shorts go first. */
  async low() {
    const shorts = await this.settingsNow();
    if (!shorts?.enabled || !shorts.campaign_start || !(shorts.stock_days > 0)) return false;
    const wanted = slotsAhead(shorts, localDay(this.ctx.now(), shorts.timezone), shorts.stock_days);
    if (!wanted) return false;
    const library = await this.api.videos({ shorts: "only", state: "library", limit: "200" });
    return Array.isArray(library) && library.length < wanted;
  }

  /** The site's client for the Shorts tool, on the same token and fetch. */
  site() {
    this.siteClient ??= siteClient({ env: this.ctx.env, home: this.ctx.home, ...(this.ctx.fetch ? { fetch: this.ctx.fetch } : {}), ...(this.ctx.sleep ? { sleep: this.ctx.sleep } : {}) });
    return this.siteClient;
  }

  async tools() {
    this.shortTools ??= this.ctx.shortsTools ?? (await defaultTools());
    return this.shortTools;
  }

  /** The Short a make job is for: an experiment, or a highlight of a tutorial (`line` cut). */
  async lab(job, slug, line = "lab") {
    const Short = line === "cut" ? CutShort : LabShort;
    return new Short({
      ctx: this.ctx,
      root: this.ctx.root ?? ROOT,
      api: this.api,
      // Every request to the tested model is one the evidence records: the client never repeats one.
      subjectApi: this.ctx.subjectApi ?? automationClient(this.ctx, { attempts: 1 }),
      site: this.site(),
      job,
      slug,
      base: this.base,
      settings: this.settings,
      shortsSettings: this.shorts ?? {},
      tools: await this.tools(),
      lexicon: readJson(lexiconFile(this.ctx.root ?? ROOT), null),
    });
  }

  /** One Shorts unit: the lines it prints, empty when there was nothing to do. */
  async step() {
    if (stopRequested(this.base)) return [];
    const shorts = await this.settingsNow();
    if (!shorts?.enabled) return [];
    const lines = await this.follow();
    if (stopRequested(this.base)) return lines;
    const next = await this.api.shortsNext();
    if (!next?.kind) return lines;
    const job = next[next.kind];
    if (!job) return [...lines, `shorts: the site named a ${next.kind} job without its contents`];
    const done = await this[next.kind](job);
    return [...lines, ...done];
  }

  /** The Shorts whose cut waited for the owner: the approved ones go on to their upload package. */
  async follow() {
    const lines = [];
    let names = [];
    try {
      names = readdirSync(this.base, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => entry.name);
    } catch {
      return lines;
    }
    for (const name of names.sort()) {
      const state = readJson(path.join(this.base, name, LAB_FILE), null);
      if (state?.status !== "awaiting") continue;
      const lab = await this.lab({ topic: { slug: state.topic, title: state.title }, channel_stance: "" }, name, state.line ?? "lab");
      const line = await lab.follow();
      if (line) lines.push(line);
    }
    return lines;
  }

  /** A planner stage of the Shorts: its answer as JSON; an unusable answer is an AutomationError. */
  async ask(variant, slug, payload, maxOutputTokens = 16_000) {
    const stance = typeof this.settings.channel_stance === "string" ? this.settings.channel_stance : "";
    const answer = await this.api.run("planner", slug, shortsInstructions("planner", variant, stance), payload, maxOutputTokens, "shorts", variant);
    this.lastAnswer = answer.text;
    try {
      return { value: parseAnswer(answer.text), answer };
    } catch (error) {
      throw new AutomationError(`planner (${variant}) answered something that is not JSON: ${error.message}`, { code: OUTPUT_INVALID });
    }
  }

  /** Keep the last answer as it came, under _shorts/answers/. */
  keepAnswer(what) {
    if (typeof this.lastAnswer !== "string") return null;
    const name = `${what}-${this.ctx.now().toISOString().replace(/[:.]/g, "-")}.txt`;
    mkdirSync(path.join(this.base, "answers"), { recursive: true });
    writeFileSync(path.join(this.base, "answers", name), this.lastAnswer);
    this.lastAnswer = null;
    return `${SHORTS_DIR}/answers/${name}`;
  }

  /** A job gave nothing usable: counted; the second time in a row `giveUp` says what happens instead. */
  async failedJob(kind, why, giveUp) {
    const state = this.state();
    state.failures[kind] = (state.failures[kind] ?? 0) + 1;
    const kept = this.keepAnswer(kind);
    const detail = `${why}${kept ? `; the answer is in ${kept}` : ""}`;
    if (state.failures[kind] < MAX_JOB_FAILURES) {
      this.saveState(state);
      return [`shorts: the ${kind} gave nothing usable (${detail}); the next round tries once more`];
    }
    delete state.failures[kind];
    this.saveState(state);
    const instead = await giveUp(detail);
    return [`shorts: the ${kind} failed ${MAX_JOB_FAILURES} times in a row (${detail}); ${instead}`];
  }

  cleared(kind) {
    const state = this.state();
    if (!state.failures[kind]) return;
    delete state.failures[kind];
    this.saveState(state);
  }

  /**
   * A planner job was sent and its answer never came back (client.mjs RUN_UNCERTAIN): the model
   * may have run, and been paid for, on the server, which keeps no answer to fetch again. Its slug
   * is kept under `lost` in the state, so the same call is not asked again on its own; the slug
   * names one day's plan or brief or one week's report, so the next one is a new call.
   */
  unanswered(kind, variant, slug, error) {
    this.lastAnswer = null;
    const state = this.state();
    const now = this.ctx.now();
    const kept = Object.entries(state.lost ?? {}).filter(([, entry]) => now.getTime() - Date.parse(entry?.at) < LOST_KEEP_MS);
    const entry = { kind, variant, at: now.toISOString(), why: error.why ?? error.message };
    state.lost = { ...Object.fromEntries(kept), [slug]: entry };
    this.saveState(state);
    return entry;
  }

  /** The planner job under `slug` whose answer was lost, if it was: then it is not asked again. */
  lostBefore(slug) {
    return this.state().lost?.[slug] ?? null;
  }

  /** What the owner reads in the log about a lost planner answer, and what happens instead. */
  lostLine(kind, slug, entry, before, instead) {
    if (before) return `shorts: the ${kind} ${slug} is not asked again: its answer was lost at ${entry.at} (${entry.why}) and the model may have run; ${instead}`;
    return `shorts: the ${kind} ${slug} may have run on the server without its answer reaching the worker (${entry.why}); it is not asked again; ${instead}`;
  }

  /** Try a planner job twice within the unit, the second time told why the first could not be used. */
  async attempt(kind, variant, slug, payload, use) {
    let problem = null;
    for (let attempt = 0; attempt < MAX_PLANNER_TRIES; attempt++) {
      let asked;
      try {
        asked = await this.ask(variant, slug, problem ? { ...payload, previous_problem: problem } : payload);
      } catch (error) {
        if (error instanceof AutomationError && error.code === RUN_UNCERTAIN) return { lost: this.unanswered(kind, variant, slug, error) };
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        problem = error.message;
        continue;
      }
      const used = await use(asked);
      if (used.line) {
        this.cleared(kind);
        return { line: used.line };
      }
      problem = used.problem;
    }
    return { problem };
  }

  /** A refusal of what the worker sent (422) is the answer's problem; anything else goes up. */
  async send(call) {
    try {
      return { out: await call() };
    } catch (error) {
      if (error instanceof AutomationError && error.status === 422) return { problem: `the site refused it: ${error.message}` };
      throw error;
    }
  }

  async plan(job) {
    const day = localDay(this.ctx.now(), job.timezone);
    const slug = `shorts-plan-${day}`;
    const payload = { ...job, today: day };
    const before = this.lostBefore(slug);
    const result = before ? { lost: before } : await this.attempt("plan", "shorts-plan", slug, payload, async ({ value }) => {
      const { items, dropped, problem } = planItems(value, job);
      if (problem) return { problem };
      const sent = await this.send(() => this.api.shortsPlan(items));
      if (sent.problem) return { problem: sent.problem };
      this.keepPlan(day, value, dropped);
      return { line: `shorts: planned ${sent.out.planned.length} of ${job.open_slots.length} open slots until ${localTime(job.window_end, job.timezone)}${dropped.length ? ` (left out: ${dropped.join("; ")})` : ""}` };
    });
    if (result.line) return [result.line];
    if (result.lost) {
      // Recorded empty too, so the server names no plan for half a day and the other jobs go on.
      await this.api.shortsPlan([]);
      return [this.lostLine("plan", slug, result.lost, before, "an empty plan was recorded, so no plan is asked for half a day, and the next day's plan is a new call")];
    }
    // An empty plan is recorded, so the server does not ask again for half a day.
    return this.failedJob("plan", result.problem, async () => {
      await this.api.shortsPlan([]);
      return "an empty plan was recorded, so the planner is not asked again for half a day";
    });
  }

  /** The planner's reasons, which the server does not keep, beside the calendar it wrote. */
  keepPlan(day, answer, dropped) {
    mkdirSync(path.join(this.base, "plans"), { recursive: true });
    writeFileSync(path.join(this.base, "plans", `${day}.json`), `${JSON.stringify({ answer, dropped }, null, 2)}\n`);
  }

  async brief(job) {
    const state = this.state();
    const hold = Date.parse(state.holds?.brief ?? "");
    if (Number.isFinite(hold) && hold > this.ctx.now().getTime()) return [];
    const day = localDay(this.ctx.now(), this.shorts?.timezone ?? "Asia/Taipei");
    const slug = `shorts-brief-${day}`;
    const before = this.lostBefore(slug);
    const result = before ? { lost: before } : await this.attempt("brief", "shorts-brief", slug, { ...job, today: day }, async ({ value }) => {
      const { topics, dropped } = briefTopics(value, job);
      if (!topics.length) return { problem: `no topic the server can take: ${dropped.join("; ") || "the list is empty"}` };
      const sent = await this.send(() => this.api.shortsTopics(topics));
      if (sent.problem) return { problem: sent.problem };
      return { line: `shorts: ${sent.out.created} new topics, ${sent.out.updated} ideas completed${dropped.length ? ` (left out: ${dropped.join("; ")})` : ""}` };
    });
    if (result.line) return [result.line];
    // The server keeps no empty brief (it takes one topic at least): the wait is the worker's own.
    if (result.lost) {
      this.holdBrief();
      return [this.lostLine("brief", slug, result.lost, before, "new topics wait half a day, and the next day's brief is a new call")];
    }
    return this.failedJob("brief", result.problem, async () => {
      this.holdBrief();
      return "new topics wait half a day";
    });
  }

  holdBrief() {
    const state = this.state();
    state.holds = { ...(state.holds ?? {}), brief: new Date(this.ctx.now().getTime() + BRIEF_HOLD_MS).toISOString() };
    this.saveState(state);
  }

  async report(job) {
    const table = rawTable(job);
    const rows = [];
    for (const short of job.published ?? []) {
      for (const snapshot of short.snapshots) {
        const row = { youtube_video_id: short.youtube_video_id, period: snapshot.period, source: snapshot.source };
        if (!rows.some((each) => each.youtube_video_id === row.youtube_video_id && each.period === row.period && each.source === row.source)) rows.push(row);
      }
    }
    const plan = (notes = {}) => (job.next_week ?? []).slice(0, 60).map((slot) => {
      const note = slot.topic_slug && typeof notes[slot.topic_slug] === "string" ? notes[slot.topic_slug].trim().slice(0, 500) : "";
      return { starts_at: slot.starts_at, ...(slot.topic_slug ? { topic_slug: slot.topic_slug } : {}), ...(slot.line ? { line: slot.line } : {}), ...(note ? { note } : {}) };
    });
    const slug = `shorts-report-${job.week_start}`;
    const before = this.lostBefore(slug);
    const result = before ? { lost: before } : await this.attempt("report", "shorts-report", slug, { ...job, raw_values: table }, async ({ value, answer }) => {
      const problems = reportProblems(value?.body_md, table);
      if (problems.length) return { problem: problems.join("; ") };
      const sent = await this.send(() => this.api.shortsReport({ week_start: job.week_start, body_md: `${value.body_md.trim()}\n\n${table}`, rows: rows.slice(0, 400), plan: plan(value.notes ?? {}), provider: answer.provider ?? null, model: answer.model ?? null }));
      if (sent.problem) return { problem: sent.problem };
      return { line: `shorts: the report on the week of ${job.week_start} is on the site (${rows.length} snapshots cited)` };
    });
    if (result.line) return [result.line];
    // The week still gets a report: what went wrong, and the raw values, so later jobs are not held up.
    const unwritten = (why) => this.api.shortsReport({ week_start: job.week_start, body_md: `## 這一週的報告沒有寫成\n\n${why}下面是伺服器存的原值，照抄；判斷請站主自己看。\n\n${table}`, rows: rows.slice(0, 400), plan: plan() });
    if (result.lost) {
      // Saved whenever the server names the week again (the round that lost the answer may not have
      // saved it), never by asking the planner a second time.
      await unwritten(`企劃模型的回答在回傳途中遺失（${String(result.lost.why).slice(0, 1500)}）：它可能已經在伺服器上跑完並計費，所以不自動再問一次。`);
      return [this.lostLine("report", slug, result.lost, before, "a report saying so, with the raw values, is on the site instead")];
    }
    return this.failedJob("report", result.problem, async (detail) => {
      await unwritten(`企劃模型連續兩次交不出能用的報告（${detail.slice(0, 1500)}）。`);
      return "a report saying so, with the raw values, is on the site instead";
    });
  }

  async make(job) {
    const topic = job.topic;
    if (!MAKES.includes(job.line)) return [`shorts: ${topic.slug} is a ${job.line} topic; this worker makes the experiments and the highlights only so far`];
    // An experiment that needs what the worker lacks is not started. A highlight is started
    // whatever its source: one it cannot be cut from is blocked with the reason (cut.mjs), so its
    // slot goes to the next Short instead of asking for it every round.
    const refusal = job.line === "lab" ? labRefusal(topic) : null;
    if (refusal) return [`shorts: cannot make ${topic.slug}: ${refusal}`];
    let slug = job.resume ? job.project_slug : null;
    if (!slug) slug = (await this.api.shortsStart(topic.slug)).project_slug;
    const lab = await this.lab(job, slug, job.line);
    if (lab.state.status === "blocked" && !(await this.retried(lab))) return [];
    const line = await lab.run();
    return line ? [line] : [];
  }

  /**
   * A blocked Short the owner asked to try again (the retry on /admin/videos, the same request the
   * tutorials read): the failures of the step that stopped it start again, once per request.
   */
  async retried(lab) {
    const listed = await this.api.videos({ shorts: "only", state: "needs_you", limit: "200" });
    const video = (Array.isArray(listed) ? listed : []).find((each) => each.slug === lab.slug);
    const request = video?.retry_request_id;
    if (!request || request === video.retry_acknowledged_id || request === lab.state.retry_request_id) return false;
    lab.state.retry_request_id = request;
    lab.state.status = "active";
    const failed = /^([a-z-]+) failed \d+ times in a row:/.exec(lab.state.blocked ?? "")?.[1];
    if (failed) delete lab.state.failures[failed];
    delete lab.state.blocked;
    lab.save();
    await lab.tellSite("retrying", null, { retry_acknowledged_id: request });
    this.log(`${lab.slug}: the owner asked for another try; resuming at ${lab.state.phase}`);
    return true;
  }
}

/** The worker's Shorts unit for `auto`: the lines it printed. Never throws: a Shorts problem is a line. */
export async function shortsStep(worker) {
  try {
    const lines = await worker.step();
    for (const line of lines) worker.log(line);
    return lines;
  } catch (error) {
    const line = `shorts: stopped by ${error instanceof AutomationError || typeof error?.who === "string" ? "the site" : "an error"} (${error.message}); the round goes on`;
    worker.log(line);
    return [line];
  }
}
