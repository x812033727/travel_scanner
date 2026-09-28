// The discussion threads (docs/videos/DRAMA-FLOW.md, section 3): the owner writes a line on a
// series document or an episode's screenplay on /admin/videos, and the worker's next round has
// the planner (a document) or the writer (a screenplay) answer it, one line per round, before any
// series work. A question gets a reply; a request for a change gets a new version too: a document
// is filed on the site as a version that waits for the owner, a screenplay is written back into
// video.json here (every line id kept, only what the owner asked changed), checked and heard
// again on the following rounds and sent to the script gate anew. A model that gives nothing
// usable is answered for: a reply says so and the thread waits for the owner; nothing is retried.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

import { docDir } from "../core/paths.mjs";
import { AutomationError, OUTPUT_INVALID } from "./client.mjs";
import { documentProblem } from "./series.mjs";

export const REPLY_MAX_CHARS = 8_000;
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;

/** The subject as its kind and number: chapter:3 → ["chapter", 3], script:2 → ["script", 2], bible → ["bible", 0]. */
export function parseSubject(subject) {
  const match = /^(setting|outline|bible|chapter:(\d+)|script:(\d+))$/.exec(String(subject));
  if (!match) throw new Error(`not a thread subject: ${subject}`);
  if (match[2] !== undefined) return ["chapter", Number(match[2])];
  if (match[3] !== undefined) return ["script", Number(match[3])];
  return [match[1], 0];
}

const threadOf = (job) => (job.thread ?? []).map(({ author, body_md: body, refers_to: refersTo, created_at: at }) => ({ author, body_md: body, refers_to: refersTo, created_at: at }));
const clip = (text) => String(text).trim().slice(0, REPLY_MAX_CHARS);
const discussionDoc = (doc) => doc ? ({ kind: doc.kind, version: doc.version, status: doc.status, needs_reconciliation: doc.needs_reconciliation ?? false, body_md: doc.body_md, body_json: doc.body_json }) : null;

/** The reply the owner reads when the model gave nothing usable: what went wrong, in zh-TW. */
export const unusableReply = (why) => `模型這一輪沒有給出可用的回覆（${why}）。這條討論串先停在這裡；請換個說法再問一次，或直接改文件。`;

/** What the planner gets to answer a line on a document. */
export function documentDiscussionPayload(automation, job) {
  const refs = automation.reference();
  const context = job.context ?? {};
  const series = job.series;
  const [kind, number] = parseSubject(job.subject);
  return {
    subject: job.subject,
    kind,
    message: job.message.body_md,
    thread: threadOf(job),
    document: discussionDoc(job.doc),
    series: {
      slug: series.slug,
      kind: series.kind ?? "series",
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
    // Discussion reads the latest parents, including drafts. Their status is explicit and
    // missing parents stay null; a conversation never grants production approval.
    ...(kind !== "setting" && kind !== "bible" ? { setting: discussionDoc(context.setting) } : {}),
    ...(kind === "chapter" ? { outline: discussionDoc(context.outline), chapter_number: number, chapter_range: context.chapter_range ?? null } : {}),
    context_instruction: "Parent documents are context only. Respect their status/version; review or rejected parents are provisional, and null parents are missing. Do not invent missing facts or approve parents. A revised document must contain matching complete body_md and body_json, including when the current document needs_reconciliation.",
  };
}

/** A revised document as the model returned it, or why it cannot be filed. */
export function revisedDocumentProblem(revised, job) {
  if (revised === null || revised === undefined) return null;
  const [kind, number] = parseSubject(job.subject);
  return documentProblem(kind, revised, { series: job.series, chapter_number: number });
}

/** The model's answer as {reply, revised}, or a problem string when it has no usable reply. */
export function answerProblem(answer) {
  if (!isObject(answer)) return "the answer is not an object";
  if (!isText(answer.reply)) return "the answer has no reply text";
  if (answer.revised !== null && answer.revised !== undefined && !isObject(answer.revised)) return "revised must be null or an object";
  return null;
}

/** Answer the owner's line on a document: a reply, and a new version when they asked for a change. */
export async function answerDocument(automation, job) {
  const { series } = job;
  const slug = `series-${series.slug}`;
  let answer;
  try {
    answer = await automation.stage("planner", slug, documentDiscussionPayload(automation, job), 32_000, "drama", "discuss");
  } catch (error) {
    if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
    automation.keepAnswer(path.join(automation.workBase, "_series", series.slug), "discuss");
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(error.message), revised: null });
    return `series ${series.slug}: the planner gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`;
  }
  const problem = answerProblem(answer);
  if (problem) {
    automation.keepAnswer(path.join(automation.workBase, "_series", series.slug), "discuss");
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(problem), revised: null });
    return `series ${series.slug}: the planner gave no usable answer on ${job.subject} (${problem}); the owner is told and the thread waits`;
  }
  let reply = clip(answer.reply);
  let revised = null;
  if (answer.revised) {
    const refused = revisedDocumentProblem(answer.revised, job);
    if (refused) reply = clip(`${reply}\n\n（新版本沒有存下來：${refused}）`);
    else revised = { body_md: answer.revised.body_md.endsWith("\n") ? answer.revised.body_md : `${answer.revised.body_md}\n`, body_json: answer.revised.body_json };
  }
  const result = await automation.api.messageAnswer(job.message.id, { reply_md: reply, revised, ...(revised && job.revision_context ? { revision_context: job.revision_context } : {}) });
  const filed = result?.revision ? ` with version ${result.revision.version} for the owner` : result?.revision_refused ? ` (only the reply was kept: ${result.revision_refused})` : revised ? " (the document changed meanwhile; only the reply was kept)" : "";
  return `series ${series.slug}: the planner answered the owner on ${job.subject}${filed}`;
}

/** The video of the episode a screenplay thread is about, as this worker holds it, or null. */
export function scriptStateFor(automation, job) {
  const slug = job.episode?.slug;
  if (!slug) return null;
  return automation.states().find((state) => state.slug === slug && state.status === "active") ?? null;
}

/** What the writer gets to answer a line on a screenplay. */
export function scriptDiscussionPayload(automation, job, state, video) {
  const dir = docDir(state.slug, automation.ctx.root);
  const screenplay = path.join(dir, "script.md");
  const brief = path.join(dir, "brief.md");
  return automation.scriptPayload(state, {
    subject: job.subject,
    message: job.message.body_md,
    thread: threadOf(job),
    video,
    screenplay: existsSync(screenplay) ? readFileSync(screenplay, "utf8") : "",
    brief: existsSync(brief) ? readFileSync(brief, "utf8") : "",
    line_ids: automation.freshIds(state, video, 40),
  });
}

/**
 * Answer the owner's line on a screenplay: a reply, and when they asked for a change the
 * corrected video.json written here, to be checked, heard and sent to the script gate again.
 */
export async function answerScript(automation, job) {
  const { series } = job;
  const state = scriptStateFor(automation, job);
  if (!state) {
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(`這台工人沒有 ${job.episode?.slug ?? job.subject} 的劇本`), revised: null });
    return `series ${series.slug}: no video for ${job.subject} here; the owner is told and the thread waits`;
  }
  const dir = docDir(state.slug, automation.ctx.root);
  const file = path.join(dir, "video.json");
  if (!existsSync(file)) {
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply("劇本還沒寫出來"), revised: null });
    return `series ${series.slug}: ${state.slug} has no video.json yet; the owner is told and the thread waits`;
  }
  const video = JSON.parse(readFileSync(file, "utf8"));
  let answer;
  try {
    answer = await automation.stage("writer", state.slug, scriptDiscussionPayload(automation, job, state, video), 32_000, "drama", "discuss");
  } catch (error) {
    if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
    automation.keepAnswer(automation.workdir(state.slug), "discuss");
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(error.message), revised: null });
    return `${state.slug}: the writer gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`;
  }
  const problem = answerProblem(answer);
  if (problem) {
    automation.keepAnswer(automation.workdir(state.slug), "discuss");
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(problem), revised: null });
    return `${state.slug}: the writer gave no usable answer on ${job.subject} (${problem}); the owner is told and the thread waits`;
  }
  let reply = clip(answer.reply);
  let rewritten = false;
  // The writer answers {"revised": {"video": …}}; a whole video.json in "revised" itself is taken too.
  const revisedVideo = answer.revised ? (isObject(answer.revised.video) ? answer.revised.video : Array.isArray(answer.revised.scenes) ? answer.revised : null) : null;
  if (answer.revised) {
    if (!isObject(revisedVideo)) reply = clip(`${reply}\n\n（新版本沒有存下來：revised.video 不是完整的 video.json）`);
    else {
      const before = readFileSync(file, "utf8");
      const refused = await automation.saveAndLint(state, { video: revisedVideo });
      if (refused) {
        // The script goes back as it was: a discussion never leaves a broken script behind.
        automation.restoreVideo(state, before);
        reply = clip(`${reply}\n\n（新版本沒有存下來：${refused}）`);
      } else {
        rewritten = true;
        state.verified = false;
        state.listener_done = false;
        state.notes.push(`script discussed: ${job.message.body_md.slice(0, 200)}`);
        automation.persist(state);
      }
    }
  }
  await automation.api.messageAnswer(job.message.id, { reply_md: reply, revised: null });
  return `${state.slug}: the writer answered the owner on ${job.subject}${rewritten ? "; the screenplay is rewritten and will be checked, heard and sent again" : ""}`;
}

/** One line answered, or null: asked before any series work, so the owner is never kept waiting. */
export async function discussStep(automation) {
  if (!automation.settings.drama?.drama_enabled) return null;
  let job;
  try {
    job = await automation.api.messageNext();
  } catch (error) {
    // A site from before the threads has no such endpoint: there is nothing to answer.
    if (error instanceof AutomationError && error.status === 404) return null;
    throw error;
  }
  if (!job) return null;
  return job.target === "script" ? answerScript(automation, job) : answerDocument(automation, job);
}
