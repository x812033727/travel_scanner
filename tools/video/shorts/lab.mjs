// An experiment Short made by the host worker (docs/videos/SHORTS.md §三條內容線、§自動品管、§工具端):
// the topic's spec frozen with its answer key, the tested model run once under each condition in a
// fresh conversation, the answers scored, a script written from the evidence alone, checked against
// it in another conversation, then built, heard, checked, packaged and pushed like any other Short.
//
// Everything lives in <work base>/_shorts/<slug>/ (the leading "_" keeps the tidy and the tutorial
// loop away from it): lab.json is where the Short stands, lab/ is the source base the build reads
// (protocol.json, subject-a.json, subject-b.json, scores.json, an HTML answer, script.json,
// verify.json), and every build is a directory of its own beside them.
//
// The rules of the experiments line, kept here in code:
// - protocol.json is written once, before any run, and its hash recorded; every later step checks
//   the hash and stops if the file changed.
// - Every request to the tested model is recorded, a failed one too; a technical failure is tried
//   once more, and both are kept. A wrong answer is a result, not a failure.
// - Numbers and times are scored by a program against the frozen key; the checker only reads off
//   which passage of an answer is its answer, and judges the items that are not a number or a time.
// - The writer sees the spec, the evidence and the scores, nothing else, and a lint refuses a digit
//   the evidence does not have.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

import { AutomationError, OUTPUT_INVALID } from '../automation/client.mjs';
import { parseAnswer } from '../automation/prompts.mjs';
import { atomicWrite, readJson, stopRequested } from '../core/paths.mjs';
import { SPEECH_UNCERTAIN } from '../tts/client.mjs';
import { LAB_SERIES, SCRIPT_FILE, USAGE_FILE, saveJson, sha256, validate } from './core.mjs';
import { shortsInstructions } from './prompts.mjs';
import { VERIFY_FILE, scriptGrammarProblems } from './qa.mjs';

export const LAB_FILE = 'lab.json';
export const LAB_DIR = 'lab';
export const PROTOCOL_FILE = 'protocol.json';
export const SCORES_FILE = 'scores.json';
export const VARIANTS = Object.freeze(['a', 'b']);
export const answerFile = (variant) => `subject-${variant}.json`;
export const htmlFile = (variant) => `subject-${variant}.html`;
// What the tested model is asked under a condition, and how often a technical failure is retried.
export const MAX_SUBJECT_ATTEMPTS = 2;
// A stage that gave nothing usable twice in a row blocks the Short (flow.mjs keeps the same rule).
export const MAX_STAGE_FAILURES = 2;
// Each kind of automatic fix (docs/videos/SHORTS.md §自動品管) is tried this many rounds.
export const MAX_FIX_ROUNDS = 2;
// The writer is asked again at once with the lint's problems this many times in a round.
export const MAX_WRITER_TRIES = 2;
export const DEFAULT_VERIFY_ROUNDS = 3;
// A bound on one round of one Short, so a phase that "succeeds" without moving cannot spin.
const MAX_PHASES_PER_ROUND = 40;
// What an experiment needs beyond text that the worker cannot give yet (the server's requirements).
export const UNSUPPORTED = Object.freeze({
  vision: '受測模型要看圖，訂閱帳號的執行環境只收文字',
  image_edit: '受測模型要修圖，訂閱帳號的執行環境只收文字',
  sandbox: '要真的執行模型寫的程式，還沒有隔離的執行環境',
  image_generation: '要生圖，工人還不會做要花錢的實測',
});
// A request the tested model never received: the owner's setting, budget or account is in the way.
const NOTHING_RAN = new Set(['video_ai_subscription_paused', 'video_ai_subject_not_chosen', 'video_ai_budget_exhausted', 'video_ai_provider_not_configured', 'video_tool_token_invalid']);
// The automatic fixes in the order they are tried when the quality check fails.
// The quality check's items the writer can fix (grammar: a first card too long for a thumbnail,
// a call to action; its picture half, the loop tail, is the build's and never fails on its own).
const QA_FIXES = ['facts', 'layout', 'metadata', 'narration', 'grammar'];
const SCENE_FIELDS = ['beat', 'headline', 'kicker', 'narration', 'body', 'big', 'note', 'asset'];
const SCRIPT_FIELDS = ['titles', 'description', 'experiment_summary', 'limitations', 'hashtags', 'tags'];

const iso = (date) => date.toISOString();
const fullWidth = (text) => String(text).replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0)).replace(/．/g, '.').replace(/，(?=\d{3})/g, ',');

/** Why the worker cannot make this topic yet; null when it can. */
export function labRefusal(topic) {
  if (topic?.line !== 'lab') return `「${topic?.slug}」不是實測線的題目`;
  const missing = (topic.brief?.requires ?? []).filter((need) => UNSUPPORTED[need]);
  return missing.length ? `「${topic.slug}」${missing.map((need) => UNSUPPORTED[need]).join('；')}` : null;
}

// --- numbers ------------------------------------------------------------------------------------

/** One number as compared: no grouping commas, no leading zeros, no trailing decimal zeros. */
export function normalNumber(text) {
  const plain = String(text).replace(/,/g, '');
  if (!/^\d+(?:\.\d+)?$/.test(plain)) return null;
  const [whole, fraction = ''] = plain.split('.');
  const integer = whole.replace(/^0+(?=\d)/, '');
  const decimals = fraction.replace(/0+$/, '');
  return decimals ? `${integer}.${decimals}` : integer;
}

/** Every number written in a text, normalized: 1,234 is one number, 09:45 is two. */
export function numbersIn(text) {
  return [...fullWidth(text).matchAll(/\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?/g)].map((match) => normalNumber(match[0]));
}

/** A clock time as HH:MM, or null. */
export function normalTime(text) {
  const match = /(\d{1,2})\s*[:：]\s*(\d{2})/.exec(fullWidth(text ?? ''));
  if (!match || Number(match[1]) > 23 || Number(match[2]) > 59) return null;
  return `${match[1].padStart(2, '0')}:${match[2]}`;
}

const squeeze = (text) => fullWidth(text).replace(/\s+/g, ' ').trim();

// --- freezing -----------------------------------------------------------------------------------

/** The spec as the server gave it, in the shape protocol.json keeps. */
export function specOf(topic) {
  const brief = topic.brief ?? {};
  const protocol = brief.test_protocol ?? {};
  return {
    title: topic.title,
    hook: topic.hook ?? null,
    setup: protocol.setup ?? '',
    input: protocol.input ?? '',
    condition_a: protocol.condition_a ?? '',
    condition_b: protocol.condition_b ?? '',
    runs: protocol.runs ?? '',
    scoring: protocol.scoring ?? '',
    failure_path: protocol.failure_path ?? '',
    truth_check: [...(brief.truth_check ?? [])],
    acceptance: [...(brief.acceptance ?? [])],
    source_material: [...(brief.source_material ?? [])],
  };
}

/**
 * Whether condition b continues a's conversation ("in the same context, add…"): b is then a's
 * request, a's answer and b's question, sent as one fresh request, since a stage call has no memory.
 */
export const followsUp = (spec) => /同一(?:個)?\s*(?:context|對話|會話|脈絡)|追加/i.test(spec.condition_b ?? '');

/** What the tested model is sent under a condition, before any answer exists. */
export function subjectPrompt(spec, variant) {
  const question = variant === 'a' || followsUp(spec) ? spec.condition_a : spec.condition_b;
  return [spec.input.trim(), question.trim()].filter(Boolean).join('\n\n');
}

/** Condition b's request when it follows a's answer. */
export function followUpPrompt(protocol, answerA) {
  return `${protocol.subject.a.instructions}\n\n---\n你剛才的回答：\n${answerA ?? '（沒有回答）'}\n---\n\n${protocol.spec.condition_b.trim()}`;
}

/** Why an answer key is not the spec's; empty when every item comes from it. */
export function keyProblems(items, spec) {
  if (!Array.isArray(items) || !items.length || items.length > 12) return ['the key must list 1 to 12 items'];
  const text = squeeze([...spec.truth_check, spec.scoring, spec.input, spec.condition_a, spec.condition_b].join('\n'));
  const problems = [];
  const ids = new Set();
  for (const [index, item] of items.entries()) {
    const label = item?.id ?? `item ${index + 1}`;
    if (typeof item?.id !== 'string' || !/^q\d{1,2}$/.test(item.id) || ids.has(item.id)) problems.push(`${label}: the id must be q1, q2… once each`);
    ids.add(item?.id);
    if (!['number', 'time', 'text'].includes(item?.kind)) problems.push(`${label}: kind must be number, time or text`);
    if (typeof item?.question !== 'string' || !item.question.trim()) problems.push(`${label}: the question is missing`);
    if (typeof item?.expected !== 'string' || !item.expected.trim()) problems.push(`${label}: expected is missing`);
    if (typeof item?.source !== 'string' || !item.source.trim() || !text.includes(squeeze(item.source))) problems.push(`${label}: source must be copied word for word from truth_check or scoring`);
    else if (item.kind === 'number' && (normalNumber(fullWidth(item.expected)) === null || !numbersIn(item.source).includes(normalNumber(fullWidth(item.expected))))) problems.push(`${label}: the expected number ${item.expected} is not in its source`);
    else if (item.kind === 'time' && (normalTime(item.expected) === null || !numbersIn(item.source).length || !squeeze(item.source).replace(/：/g, ':').includes(normalTime(item.expected).replace(/^0/, '')))) problems.push(`${label}: the expected time ${item.expected} is not in its source`);
  }
  return problems;
}

/** protocol.json: the spec, the key and the requests, frozen before the tested model is asked. */
export function freezeProtocol({ topic, slug, key, now }) {
  const spec = specOf(topic);
  const follows = followsUp(spec);
  return {
    version: 1,
    slug,
    topic: topic.slug,
    line: 'lab',
    series: topic.series ?? null,
    spec,
    answer_key: key.map(({ id, question, kind, expected, source }) => ({ id, question, kind, expected: kind === 'number' ? normalNumber(fullWidth(expected)) : kind === 'time' ? normalTime(expected) : expected.trim(), source })),
    subject: {
      a: { instructions: subjectPrompt(spec, 'a'), payload: {} },
      b: follows ? { follows: 'a', question: spec.condition_b.trim(), payload: {} } : { instructions: subjectPrompt(spec, 'b'), payload: {} },
    },
    rules: { conversation: 'fresh', attempts: MAX_SUBJECT_ATTEMPTS, retry: 'one more request after a technical failure; a wrong answer is a result' },
    frozen_at: iso(now),
  };
}

// --- the tested model's answers -------------------------------------------------------------------

/** The HTML document in an answer, and whether a card may show it (no script, nothing fetched). */
export function htmlOf(raw) {
  const text = String(raw ?? '');
  const fenced = /```html\s*([\s\S]*?)```/i.exec(text);
  const bare = /<!doctype html[\s\S]*<\/html>|<html[\s\S]*<\/html>/i.exec(text);
  const html = (fenced?.[1] ?? bare?.[0] ?? '').trim();
  if (!html || !/<(?:html|body|div|section|main)\b/i.test(html)) return null;
  if (/<(?:script|iframe|object|embed)\b/i.test(html)) return { html, usable: false, reason: 'the HTML runs code; the cards show no active HTML' };
  if (/\b(?:src|href)\s*=\s*["']?\s*(?:https?:)?\/\//i.test(html) || /url\(\s*["']?\s*(?:https?:)?\/\//i.test(html)) return { html, usable: false, reason: 'the HTML loads something from the network; the cards render offline' };
  return { html, usable: true };
}

// --- scoring --------------------------------------------------------------------------------------

/**
 * scores.json from the key, the raw answers and what the checker read off them. Numbers and times
 * are compared here; a text item takes the checker's verdict. `problems` says why the reading
 * cannot be used (a quote that is not in the answer, a value that is not in its quote, an item
 * left out); a wrong answer is never a problem.
 */
export function scoreAnswers({ key, answers, read }) {
  const problems = [];
  const items = key.map((entry) => ({ id: entry.id, kind: entry.kind, question: entry.question, expected: entry.expected }));
  for (const variant of VARIANTS) {
    const raw = answers[variant];
    const given = Array.isArray(read?.[variant]) ? read[variant] : [];
    for (const [index, entry] of key.entries()) {
      const target = items[index];
      if (raw === null || raw === undefined) {
        target[variant] = { ok: false, quote: null, value: null, by: 'program', note: '這一組沒有回答' };
        continue;
      }
      const reading = given.find((each) => each?.id === entry.id);
      if (!reading) {
        problems.push(`${variant} ${entry.id}: no reading`);
        continue;
      }
      const quote = typeof reading.quote === 'string' ? reading.quote : '';
      if (quote && !squeeze(raw).includes(squeeze(quote))) problems.push(`${variant} ${entry.id}: the quote is not in the answer word for word`);
      if (entry.kind === 'text') {
        if (!['pass', 'fail'].includes(reading.verdict)) problems.push(`${variant} ${entry.id}: verdict must be pass or fail`);
        target[variant] = { ok: reading.verdict === 'pass', quote: quote || null, verdict: reading.verdict, reason: String(reading.reason ?? ''), by: 'verifier' };
        continue;
      }
      if (!quote || reading.value === null || reading.value === undefined || reading.value === '') {
        target[variant] = { ok: false, quote: quote || null, value: null, by: 'program', note: '回答裡沒有這一題的答案' };
        continue;
      }
      const value = entry.kind === 'time' ? normalTime(String(reading.value)) : normalNumber(fullWidth(String(reading.value)));
      const inQuote = entry.kind === 'time'
        ? normalTime(quote) !== null && [...fullWidth(quote).matchAll(/(\d{1,2})\s*[:：]\s*(\d{2})/g)].some((match) => normalTime(match[0]) === value)
        : numbersIn(quote).includes(value);
      if (value === null || !inQuote) problems.push(`${variant} ${entry.id}: the value ${reading.value} is not in its quote`);
      target[variant] = { ok: value !== null && value === entry.expected, quote, value, by: 'program' };
    }
  }
  const totals = Object.fromEntries(VARIANTS.map((variant) => [variant, items.filter((item) => item[variant]?.ok).length]));
  return { items, totals, of: key.length, tie: totals.a === totals.b, problems };
}

// --- the script -----------------------------------------------------------------------------------

/** The writer's answer as a script of the experiments line, the fields the worker owns set here. */
export function labScript(answer, { slug, series, evidence }) {
  const given = answer?.script && typeof answer.script === 'object' && !Array.isArray(answer.script) ? answer.script : {};
  const doc = { schema_version: 2, slug, format: 'shorts', locale: 'zh-TW', line: 'lab', series };
  for (const field of SCRIPT_FIELDS) if (given[field] !== undefined) doc[field] = given[field];
  doc.evidence = evidence;
  doc.scenes = Array.isArray(given.scenes)
    ? given.scenes.map((scene) => (scene && typeof scene === 'object' ? Object.fromEntries(SCENE_FIELDS.filter((field) => scene[field] !== undefined && scene[field] !== null).map((field) => [field, scene[field]])) : scene))
    : given.scenes;
  return doc;
}

/** Every text a viewer sees or hears, with where it is. */
function scriptTexts(doc) {
  const texts = [];
  (doc.titles ?? []).forEach((title, index) => texts.push([`titles[${index}]`, title]));
  for (const field of ['description', 'experiment_summary', 'limitations']) texts.push([field, doc[field]]);
  (Array.isArray(doc.scenes) ? doc.scenes : []).forEach((scene, index) => {
    for (const field of ['headline', 'kicker', 'big', 'note']) texts.push([`scene ${index} ${field}`, scene?.[field]]);
    for (const field of ['body', 'narration']) (Array.isArray(scene?.[field]) ? scene[field] : []).forEach((text) => texts.push([`scene ${index} ${field}`, text]));
  });
  return texts.filter(([, text]) => typeof text === 'string');
}

/**
 * Why a script cannot go to the checker: the format's own rules, a digit the evidence does not
 * have, an asset that is not a usable HTML answer. `evidenceText` is everything the evidence says.
 */
export function scriptProblems(doc, { evidenceText, htmlAssets = [] }) {
  const problems = validate(doc);
  const known = new Set(numbersIn(evidenceText));
  for (const [where, text] of scriptTexts(doc)) {
    const strange = [...new Set(numbersIn(text).filter((number) => !known.has(number)))];
    if (strange.length) problems.push(`${where}: ${strange.join('、')} is not in the protocol, the answers or the scores`);
  }
  (Array.isArray(doc.scenes) ? doc.scenes : []).forEach((scene, index) => {
    if (scene?.asset !== undefined && !htmlAssets.includes(scene.asset)) problems.push(`scene ${index}: asset may only be an HTML answer listed in evidence_files (${htmlAssets.join(', ') || 'none'})`);
  });
  // The grammar the quality check holds the cut to (qa.mjs): the first card reads at thumbnail
  // size, no call to action; refused here so the writer fixes it before anything is paid for.
  problems.push(...scriptGrammarProblems(doc));
  return problems;
}

/** verify.json from the checker's answer, bound to the script it checked. */
export function verifyRecord(answer, { documentSha256, model, round, now }) {
  const claims = Array.isArray(answer?.claims) ? answer.claims.filter((claim) => claim && typeof claim.text === 'string').map((claim) => ({ text: claim.text, ok: claim.ok === true, evidence: String(claim.evidence ?? ''), note: String(claim.note ?? '') })) : [];
  const problems = Array.isArray(answer?.problems) ? answer.problems.filter((problem) => typeof problem === 'string' && problem.trim()) : [];
  const ok = answer?.ok === true && claims.length > 0 && claims.every((claim) => claim.ok) && !problems.length;
  return { ok, document_sha256: documentSha256, checked_by: model, round, claims, problems, checked_at: iso(now) };
}

// --- making one Short -------------------------------------------------------------------------------

/** The tools a Short is made with; tests hand in their own. */
export async function defaultTools() {
  const [{ build }, { checkAudio }, { runQa }, { packageBuild }, { push }] = await Promise.all([
    import('./build.mjs'), import('./check.mjs'), import('./qa.mjs'), import('./package.mjs'), import('./push.mjs'),
  ]);
  return { build, checkAudio, runQa, packageBuild, push };
}

// A call to the site or a vendor carries `who`: the owner's to fix, or a service's. A service that
// is down or busy is tried again next round without counting against the Short; one that refused
// the request (a 4xx) refused what the worker sent, which counts like an unusable answer.
const owner = (error) => error?.who === 'owner';
const outside = (error) => typeof error?.who === 'string';
const transient = (error) => outside(error) && !owner(error) && (!error.status || error.status === 429 || error.status >= 500);
// Where a Short stands, in order, and the steps /admin/videos shows for it.
const ORDER = Object.freeze(['freeze', 'subject-a', 'subject-b', 'score', 'write', 'verify', 'build', 'audio', 'qa', 'package', 'push', 'awaiting', 'done']);
const CHECKLIST = Object.freeze([
  ['freeze', '凍結題目', ['freeze']],
  ['subject', '受測模型各跑一次', ['subject-a', 'subject-b']],
  ['score', '評分', ['score']],
  ['write', '撰稿與查核', ['write', 'verify']],
  ['build', '成片與旁白檢查', ['build', 'audio']],
  ['qa', '自動品管', ['qa']],
  ['push', '送審', ['package', 'push']],
]);

/**
 * One experiment Short, moved as far as it goes this round. `job` is the server's make job, `slug`
 * the video it is made under; `api` the automation client (and `subjectApi`, one that never
 * repeats a request on its own, for the tested model); `site` the Shorts tool's client; `base` the
 * Shorts work base (<work base>/_shorts). Returns the round's line.
 *
 * Another content line made the same way (cut.mjs, the highlights) extends this class with its own
 * `line`, `order` and `checklist`, its own phases before `build`, and its own `instructions` and
 * `protocol` (the frozen input the build checks); building, hearing, checking, packaging, pushing
 * and following the owner's decision stay the same.
 */
export class LabShort {
  static line = 'lab';
  static order = ORDER;
  static checklist = CHECKLIST;

  constructor({ ctx, api, subjectApi = api, site, job, slug, base, settings = {}, shortsSettings = {}, tools, lexicon = null }) {
    this.ctx = ctx;
    this.api = api;
    this.subjectApi = subjectApi;
    this.site = site;
    this.job = job;
    this.slug = slug;
    this.base = base;
    this.dir = path.join(base, slug);
    this.labDir = path.join(this.dir, LAB_DIR);
    this.settings = settings;
    this.shortsSettings = shortsSettings;
    this.tools = tools;
    this.lexicon = lexicon;
    this.lastAnswer = null;
    this.state = readJson(path.join(this.dir, LAB_FILE), null) ?? this.fresh();
  }

  fresh() {
    const topic = this.job.topic;
    return {
      slug: this.slug,
      topic: topic.slug,
      title: topic.title,
      series: LAB_SERIES.includes(topic.series) ? topic.series : 'prompts',
      status: 'active',
      phase: 'freeze',
      failures: {},
      fixes: {},
      verify_rounds: 0,
      problems: [],
      attempts: { a: [], b: [] },
      usage: {},
      created_at: iso(this.now()),
    };
  }

  now() {
    return this.ctx.now();
  }

  save() {
    this.state.updated_at = iso(this.now());
    atomicWrite(path.join(this.dir, LAB_FILE), `${JSON.stringify(this.state, null, 2)}\n`);
  }

  file(name) {
    return path.join(this.labDir, name);
  }

  writeLab(name, data) {
    mkdirSync(this.labDir, { recursive: true });
    const text = typeof data === 'string' ? data : `${JSON.stringify(data, null, 2)}\n`;
    writeFileSync(this.file(name), text);
    return sha256(Buffer.from(text));
  }

  /** The protocol as frozen; throws when the file is not the one whose hash was recorded. */
  protocol() {
    const file = this.file(PROTOCOL_FILE);
    if (!existsSync(file) || sha256(readFileSync(file)) !== this.state.protocol_sha256) throw new LabBlocked('protocol.json 在凍結之後被改過或不見了，這支的證據不能再用');
    return JSON.parse(readFileSync(file, 'utf8'));
  }

  /** What a stage of this Short is told. */
  instructions(stage, variant) {
    return shortsInstructions(stage, variant, this.job.channel_stance ?? '');
  }

  /** A writing or checking stage of the Short: its answer as JSON, its usage recorded. */
  async ask(stage, variant, payload, maxOutputTokens = 16_000) {
    const answer = await this.api.run(stage, this.slug, this.instructions(stage, variant), payload, maxOutputTokens, 'shorts', variant);
    this.count(`${stage}/${variant}`, answer);
    this.lastAnswer = answer.text;
    try {
      return { value: parseAnswer(answer.text), answer };
    } catch (error) {
      throw new AutomationError(`${stage} (${variant}) answered something that is not JSON: ${error.message}`, { code: OUTPUT_INVALID });
    }
  }

  count(key, answer) {
    const used = this.state.usage[key] ?? { calls: 0, input_tokens: 0, output_tokens: 0 };
    used.calls += 1;
    used.input_tokens += Number(answer.input_tokens) || 0;
    used.output_tokens += Number(answer.output_tokens) || 0;
    if (answer.provider) used.provider = answer.provider;
    if (answer.model) used.model = answer.model;
    this.state.usage[key] = used;
  }

  /** Keep the last stage's answer as it came, so a person can see why it was unusable. */
  keepAnswer(what) {
    if (typeof this.lastAnswer !== 'string') return null;
    const name = `${what.replace(/[^a-z0-9-]+/gi, '-')}-${iso(this.now()).replace(/[:.]/g, '-')}.txt`;
    mkdirSync(path.join(this.dir, 'answers'), { recursive: true });
    writeFileSync(path.join(this.dir, 'answers', name), this.lastAnswer);
    this.lastAnswer = null;
    return `answers/${name}`;
  }

  /** A phase gave nothing usable: end the round; the second time in a row the Short is blocked. */
  async failed(phase, why) {
    this.state.failures[phase] = (this.state.failures[phase] ?? 0) + 1;
    const kept = this.keepAnswer(phase);
    const detail = `${why}${kept ? `; the answer is in ${kept}` : ''}`;
    if (this.state.failures[phase] >= MAX_STAGE_FAILURES) return this.block(`${phase} failed ${this.state.failures[phase]} times in a row: ${detail}`);
    this.save();
    return `${this.slug}: ${phase} gave nothing usable (${detail}); the next round tries once more`;
  }

  /** Stop the Short for a person, and say why on /admin/videos (the tab lists it under 需要你). */
  async block(why) {
    this.state.status = 'blocked';
    this.state.blocked = why;
    this.save();
    await this.tellSite('blocked', `卡住，需要人處理：${why}`).catch((error) => this.ctx.stdout.write(`  could not report the block yet: ${error.message}\n`));
    return `${this.slug}: blocked — ${why}`;
  }

  /** Tell /admin/videos where the Short stands: its stage, why it stopped, the steps done. */
  async tellSite(stage, label = null, extra = {}) {
    const { order, checklist, line } = this.constructor;
    const at = order.indexOf(this.state.phase);
    await this.api.report(this.slug, {
      ...extra,
      title: String(this.state.title || this.slug).slice(0, 200),
      stage,
      checklist: [
        ...(label ? [{ key: 'blocked', label: label.slice(0, 120), done: false }] : []),
        ...checklist.map(([key, text, phases]) => ({ key, label: text, done: at > Math.max(...phases.map((phase) => order.indexOf(phase))) })),
      ],
      format: 'shorts',
      shorts_line: line,
      shorts_series: this.state.series,
    });
  }

  /** Move the Short until it waits, is done, fails or meets a STOP file. */
  async run() {
    if (this.state.status === 'blocked') return null;
    if (this.state.status === 'done' || this.state.status === 'returned') return null;
    const lines = [];
    const { order } = this.constructor;
    const moving = new Set(order.slice(0, order.indexOf('awaiting')));
    for (let step = 0; step < MAX_PHASES_PER_ROUND; step++) {
      if (['done', 'awaiting', 'blocked', 'returned'].includes(this.state.status)) break;
      if (stopRequested(this.base)) {
        lines.push('STOP found; stopping between units');
        break;
      }
      const phase = this.state.phase;
      // Only an answer of this phase is kept when it fails: never an earlier phase's good one.
      this.lastAnswer = null;
      let outcome;
      try {
        if (!moving.has(phase)) throw new LabBlocked(`lab.json names a step the worker does not know: ${phase}`);
        outcome = await this[phase]();
      } catch (error) {
        if (error instanceof LabBlocked) return [...lines, await this.block(error.message)].join('\n');
        // The model answered something unusable, here or on the server: counted like any failure.
        if (error?.code === OUTPUT_INVALID) return [...lines, await this.failed(phase, error.message)].join('\n');
        // A paid speech request whose answer was lost after it was sent, or one the speech journal
        // holds (tts/client.mjs SPEECH_UNCERTAIN): another round meets the same hold and paying
        // again may charge twice, so the Short is blocked where the owner sees it, the way
        // automation/flow.mjs blocks a video. The message names the request and how to release it.
        if (error?.code === SPEECH_UNCERTAIN) return [...lines, await this.block(error.message)].join('\n');
        if (owner(error)) {
          this.save();
          return [...lines, `${this.slug}: waits for the owner at ${phase}: ${error.message}`].join('\n');
        }
        if (transient(error)) {
          this.save();
          return [...lines, `${this.slug}: ${phase} is waiting on a service (${error.message}); the next round tries again`].join('\n');
        }
        // An unusable answer, a refused request or a step that broke: counted, blocked the second time.
        return [...lines, await this.failed(phase, error.message)].join('\n');
      }
      if (outcome.line) lines.push(`${this.slug}: ${outcome.line}`);
      if (outcome.failed) return [...lines, await this.failed(phase, outcome.failed)].join('\n');
      if (outcome.halt) {
        this.save();
        return [...lines, `${this.slug}: ${outcome.halt}`].join('\n');
      }
      if (this.state.failures[phase]) delete this.state.failures[phase];
      this.state.phase = outcome.next;
      this.save();
    }
    return lines.join('\n') || null;
  }

  // --- the phases ---------------------------------------------------------------------------------

  async freeze() {
    if (this.state.protocol_sha256 && existsSync(this.file(PROTOCOL_FILE))) {
      this.protocol();
      return { next: 'subject-a' };
    }
    const spec = specOf(this.job.topic);
    const { value } = await this.ask('verifier', 'shorts-lab-key', { spec, topic: { slug: this.job.topic.slug, title: this.job.topic.title } }, 4000);
    const problems = keyProblems(value?.items, spec);
    if (problems.length) return { failed: `the answer key does not come from the spec: ${problems.join('; ')}` };
    const protocol = freezeProtocol({ topic: this.job.topic, slug: this.slug, key: value.items, now: this.now() });
    this.state.protocol_sha256 = this.writeLab(PROTOCOL_FILE, protocol);
    return { next: 'subject-a', line: `protocol frozen (${protocol.answer_key.length} answers in the key, sha256 ${this.state.protocol_sha256.slice(0, 12)})` };
  }

  'subject-a'() {
    return this.subject('a');
  }

  'subject-b'() {
    return this.subject('b');
  }

  /** One request to the tested model under a condition, recorded whatever happens. */
  async subject(variant) {
    const protocol = this.protocol();
    const next = variant === 'a' ? 'subject-b' : 'score';
    if (existsSync(this.file(answerFile(variant)))) return { next };
    const attempts = this.state.attempts[variant] ?? [];
    const request = protocol.subject[variant].follows
      ? followUpPrompt(protocol, readJson(this.file(answerFile('a')), {}).raw ?? null)
      : protocol.subject[variant].instructions;
    const started = this.now();
    let answer;
    try {
      answer = await this.subjectApi.run('subject', this.slug, request, protocol.subject[variant].payload ?? {}, 16_000, 'shorts', variant);
    } catch (error) {
      if (!(error instanceof AutomationError)) throw error;
      // Nothing reached the tested model: the owner's setting, budget or a paused account.
      if (NOTHING_RAN.has(error.code)) throw error;
      attempts.push({ started_at: iso(started), ended_at: iso(this.now()), ok: false, status: error.status, code: error.code || null, error: error.message });
      this.state.attempts[variant] = attempts;
      if (attempts.length < MAX_SUBJECT_ATTEMPTS) return { halt: `the tested model (${variant}) failed technically (${error.message}); it is asked once more next round, and both requests are kept` };
      this.writeAnswer(variant, { protocol, request, attempts, answer: null });
      throw new LabBlocked(`受測模型（${variant}）兩次都技術失敗：照規格的失敗處理，沒有原始輸出就不做實測結論，等站主決定`);
    }
    attempts.push({ started_at: iso(started), ended_at: iso(this.now()), ok: true });
    this.state.attempts[variant] = attempts;
    this.count(`subject/${variant}`, answer);
    this.writeAnswer(variant, { protocol, request, attempts, answer });
    return { next, line: `the tested model answered under ${variant} (${answer.model || '未回傳'}, ${attempts.length} request${attempts.length > 1 ? 's' : ''})` };
  }

  /** subject-<v>.json, and the HTML document the answer holds when a card may show it. */
  writeAnswer(variant, { protocol, request, attempts, answer }) {
    const record = {
      variant,
      stage: 'subject',
      conversation: 'fresh',
      protocol_sha256: this.state.protocol_sha256,
      condition: variant === 'a' ? protocol.spec.condition_a : protocol.spec.condition_b,
      instructions: request,
      payload: protocol.subject[variant].payload ?? {},
      attempts,
      retries: Math.max(0, attempts.length - 1),
      provider: answer?.provider ?? null,
      model: answer?.model || '未回傳',
      answered_at: answer ? attempts.at(-1).ended_at : null,
      input_tokens: answer?.input_tokens ?? null,
      output_tokens: answer?.output_tokens ?? null,
      raw: answer ? String(answer.text) : null,
    };
    const html = answer ? htmlOf(answer.text) : null;
    if (html?.usable) record.html = { path: htmlFile(variant), sha256: this.writeLab(htmlFile(variant), `${html.html}\n`) };
    else if (html) record.html = { usable: false, reason: html.reason };
    this.writeLab(answerFile(variant), record);
  }

  answers() {
    return Object.fromEntries(VARIANTS.map((variant) => [variant, readJson(this.file(answerFile(variant)))]));
  }

  async score() {
    const protocol = this.protocol();
    const answers = this.answers();
    const { value, answer } = await this.ask('verifier', 'shorts-lab-score', { key: protocol.answer_key, answers: Object.fromEntries(VARIANTS.map((variant) => [variant, answers[variant].raw ?? ''])) }, 8000);
    const scores = scoreAnswers({ key: protocol.answer_key, answers: Object.fromEntries(VARIANTS.map((variant) => [variant, answers[variant].raw])), read: value });
    if (scores.problems.length) return { failed: `the reading of the answers cannot be used: ${scores.problems.join('; ')}` };
    const { problems: _none, ...kept } = scores;
    this.writeLab(SCORES_FILE, { protocol_sha256: this.state.protocol_sha256, read_by: answer.model, ...kept });
    return { next: 'write', line: `scored: a ${scores.totals.a}/${scores.of}, b ${scores.totals.b}/${scores.of}${scores.tie ? ' (a tie)' : ''}` };
  }

  /** The evidence files as the script lists them, and the HTML answers a card may show. */
  evidence() {
    const files = [PROTOCOL_FILE, answerFile('a'), answerFile('b'), SCORES_FILE];
    const answers = this.answers();
    const html = VARIANTS.map((variant) => answers[variant].html).filter((entry) => entry?.path);
    return {
      list: [...files, ...html.map((entry) => entry.path)].map((name) => ({ path: name, sha256: sha256(readFileSync(this.file(name))) })),
      html: html.map((entry) => entry.path),
      text: files.map((name) => readFileSync(this.file(name), 'utf8')).join('\n'),
    };
  }

  async write() {
    const protocol = this.protocol();
    const answers = this.answers();
    const scores = readJson(this.file(SCORES_FILE));
    const evidence = this.evidence();
    const previous = existsSync(this.file(SCRIPT_FILE)) ? readJson(this.file(SCRIPT_FILE)) : null;
    let problems = [...(this.state.problems ?? [])];
    for (let attempt = 0; attempt < MAX_WRITER_TRIES; attempt++) {
      const payload = {
        protocol: { spec: protocol.spec, answer_key: protocol.answer_key, subject: protocol.subject },
        evidence: Object.fromEntries(VARIANTS.map((variant) => [variant, { model: answers[variant].model, provider: answers[variant].provider, raw: answers[variant].raw, requests: answers[variant].attempts.length }])),
        scores,
        evidence_files: evidence.list.map((entry) => ({ ...entry, kind: entry.path.endsWith('.html') ? 'html' : 'json' })),
        seconds: { min: this.job.seconds_min, max: this.job.seconds_max },
        series: this.state.series,
        ...(previous && problems.length ? { previous_script: previous } : {}),
        ...(problems.length ? { problems } : {}),
      };
      const { value } = await this.ask('writer', 'shorts-lab', payload);
      const doc = labScript(value, { slug: this.slug, series: this.state.series, evidence: evidence.list });
      const found = scriptProblems(doc, { evidenceText: evidence.text, htmlAssets: evidence.html });
      if (!found.length) {
        this.writeLab(SCRIPT_FILE, doc);
        this.state.problems = [];
        return { next: 'verify', line: `script written (${doc.scenes.length} scenes)` };
      }
      problems = found;
    }
    return { failed: `the script does not pass the lint: ${problems.join('; ')}` };
  }

  async verify() {
    const protocol = this.protocol();
    const bytes = readFileSync(this.file(SCRIPT_FILE));
    const answers = this.answers();
    const { value, answer } = await this.ask('verifier', 'shorts-lab', {
      script: JSON.parse(bytes),
      protocol: { spec: protocol.spec, answer_key: protocol.answer_key },
      evidence: Object.fromEntries(VARIANTS.map((variant) => [variant, { model: answers[variant].model, raw: answers[variant].raw }])),
      scores: readJson(this.file(SCORES_FILE)),
    }, 8000);
    if (!Array.isArray(value?.claims) || !value.claims.length) return { failed: 'the check lists no claim' };
    this.state.verify_rounds += 1;
    const record = verifyRecord(value, { documentSha256: sha256(bytes), model: answer.model, round: this.state.verify_rounds, now: this.now() });
    this.writeLab(VERIFY_FILE, record);
    if (record.ok) return { next: 'build', line: `fact-checked: ${record.claims.length} claims backed by the evidence` };
    const most = Number(this.settings.max_verify_rounds) || DEFAULT_VERIFY_ROUNDS;
    if (this.state.verify_rounds >= most) return { next: 'build', line: `the check still finds problems after ${most} rounds; the quality check will show them to the owner` };
    this.state.problems = [...record.problems, ...record.claims.filter((claim) => !claim.ok).map((claim) => `${claim.text}：${claim.note || '證據不支持'}`)];
    return { next: 'write', line: `the check found ${this.state.problems.length} problems; back to the writer` };
  }

  /** A fix of one kind, while its rounds last: the writer gets the problems and the Short is made again. */
  fix(kind, problems, { block = false } = {}) {
    const done = this.state.fixes[kind] ?? 0;
    if (done >= MAX_FIX_ROUNDS) {
      if (block) throw new LabBlocked(`${kind} 自動修了 ${done} 輪仍然不行：${problems.join('；')}`.slice(0, 400));
      return null;
    }
    this.state.fixes[kind] = done + 1;
    this.state.problems = problems;
    return { next: 'write', line: `${kind}: back to the writer (fix round ${done + 1} of ${MAX_FIX_ROUNDS})` };
  }

  async build() {
    this.protocol();
    const redo = this.state.redo ? this.state.build : null;
    let result;
    try {
      result = await this.tools.build({ file: this.file(SCRIPT_FILE), sourceBase: this.labDir, workdir: this.base, speech: 'server', client: this.site, redo, lexicon: this.lexicon });
    } catch (error) {
      if (outside(error)) throw error;
      if (/edit script to fit/.test(error.message)) return this.fix('length', [`旁白長度不對：${error.message}；照 seconds 的範圍增刪句子`], { block: true });
      if (/^scene \d+, cue \d+:|text clipped|ancestor clips|asset image failed|active HTML|unsupported image/.test(error.message)) return this.fix('layout', [`字卡放不下或素材不能用：${error.message}；縮短那張字卡或拿掉那個素材`], { block: true });
      throw error;
    }
    delete this.state.redo;
    this.state.build = result.directory;
    // The checker's verdict travels with the build, where the quality check reads it.
    copyFileSync(this.file(VERIFY_FILE), path.join(result.directory, VERIFY_FILE));
    return { next: 'audio', line: `built ${result.seconds.toFixed(1)}s (${path.basename(result.directory)})` };
  }

  async audio() {
    const check = await this.tools.checkAudio({ directory: this.state.build, client: this.site, lexicon: this.lexicon });
    this.state.checks = { transcribe: (this.state.checks?.transcribe ?? 0) + (check.transcribe_calls ?? 0), judge: (this.state.checks?.judge ?? 0) + (check.judge_calls ?? 0) };
    if (check.ok) return { next: 'qa', line: `narration heard as written (${check.checked} phrases)` };
    return this.narrationFix(check.flagged_lines ?? []) ?? { next: 'qa', line: `${check.flagged} phrases still flagged after the fixes; the quality check will show them` };
  }

  /** The first round synthesizes the flagged phrases again; the second has the writer reword them. */
  narrationFix(flagged) {
    const done = this.state.fixes.narration ?? 0;
    if (done >= MAX_FIX_ROUNDS) return null;
    this.state.fixes.narration = done + 1;
    if (done === 0) {
      this.state.redo = true;
      return { next: 'build', line: `${flagged.length} phrases flagged; synthesized again (fix round 1 of ${MAX_FIX_ROUNDS})` };
    }
    this.state.problems = flagged.map((line) => `旁白「${line.text}」被聽成「${line.heard}」：改寫這一句，意思與數字不變`);
    return { next: 'write', line: `${flagged.length} phrases still flagged; back to the writer (fix round 2 of ${MAX_FIX_ROUNDS})` };
  }

  async qa() {
    const report = await this.tools.runQa({ directory: this.state.build, client: this.site });
    if (report.ok) return { next: 'package', line: `quality check: all ${report.items.length} items pass` };
    const failed = report.items.filter((item) => !item.ok);
    for (const kind of QA_FIXES) {
      const item = failed.find((each) => each.id === kind);
      if (!item) continue;
      const fixed = kind === 'narration' ? this.narrationFix(readJson(path.join(this.state.build, 'check.json'), {}).flagged_lines ?? []) : this.fix(kind, [`自動品管 ${kind} 沒過：${item.detail}`]);
      if (fixed) return fixed;
    }
    return { next: 'package', line: `quality check: ${failed.map((item) => item.id).join(', ')} still failing after the fixes; it goes to the owner` };
  }

  async package() {
    const { report } = this.tools.packageBuild({ directory: this.state.build, settings: this.shortsSettings });
    return { next: 'push', line: `packaged: ${report.ok ? 'complete' : report.items.filter((item) => !item.ok).map((item) => item.id).join(', ')}` };
  }

  /** usage.json: the narration the build counted and the stages this Short asked. */
  writeUsage() {
    const file = path.join(this.state.build, USAGE_FILE);
    const usage = readJson(file, {});
    saveJson(file, { ...usage, stages: this.state.usage, checks: this.state.checks ?? {} });
  }

  async push() {
    this.writeUsage();
    const result = await this.tools.push({ directory: this.state.build, client: this.site, log: (line) => this.ctx.stdout.write(`  ${line}\n`) });
    if (!result.final) return { failed: `push did not send the cut: ${result.waits}` };
    if (!this.state.told_done) {
      await this.api.shortsDone(this.state.topic, { outcome: 'made' });
      this.state.told_done = true;
    }
    if (result.publish) {
      this.state.status = 'done';
      return { next: 'done', line: `pushed: final ${result.final.status}, upload package ${result.publish.status}` };
    }
    if (result.final.status === 'rejected') {
      this.state.status = 'returned';
      this.state.returned = result.final.note ?? '';
      return { next: 'done', line: `the owner sent the cut back (${result.final.note ?? ''})` };
    }
    if (result.final.status === 'approved') return { failed: `the cut is approved but the package did not go: ${result.waits}` };
    this.state.status = 'awaiting';
    return { next: 'awaiting', line: `pushed; ${result.waits}` };
  }

  /**
   * A Short whose cut waited for the owner: once the site approved it, push again so the upload
   * package goes; sent back, it stays as it is. Null while it still waits.
   */
  async follow() {
    if (this.state.status !== 'awaiting') return null;
    const qa = readJson(path.join(this.state.build, 'qa.json'), null);
    const project = await this.site.project(this.slug);
    const final = (project?.reviews ?? []).find((review) => review.gate === 'final' && review.content_sha256 === qa?.final_sha256);
    if (!final || final.status === 'pending') return null;
    if (final.status === 'rejected' || final.status === 'superseded') {
      this.state.status = 'returned';
      this.state.returned = final.note ?? final.status;
      this.save();
      return `${this.slug}: the owner sent the cut back (${this.state.returned}); the worker leaves it`;
    }
    this.state.status = 'active';
    this.state.phase = 'push';
    this.save();
    return this.run();
  }
}

/** A Short that cannot go on without a person: the reason is reported to the site. */
export class LabBlocked extends Error {}
