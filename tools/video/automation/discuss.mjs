// The discussion threads (docs/videos/DRAMA-FLOW.md, section 3): the owner writes a line on a
// series document or an episode's screenplay on /admin/videos, and the worker's next round has
// the planner (a document) or the writer (a screenplay) answer it, one line per round, before any
// series work. A question gets a reply; a request for a change gets a new version too: a document
// is filed on the site as a version that waits for the owner, a screenplay is written back into
// video.json here (every line id kept, only what the owner asked changed), checked and heard
// again on the following rounds and sent to the script gate anew. A model that gives nothing
// usable is answered for: a reply says so and the thread waits for the owner; nothing is retried.
import { existsSync, readFileSync, rmSync } from "node:fs";
import path from "node:path";

import { hasAnimePolicy, isLongAnime } from "../core/anime-policy.mjs";
import { atomicWrite, docDir, readJson } from "../core/paths.mjs";
import { AutomationError, OUTPUT_INVALID, RUN_UNCERTAIN } from "./client.mjs";
import { JOB_GONE_KIND } from "./run-receipts.mjs";
import { documentProblem } from "./series.mjs";

export const REPLY_MAX_CHARS = 8_000;
// The writer's variants that answer a line on a screenplay (answerScript). Both are durable jobs
// (client.mjs run), so one may still be running on the server when its unit ends; flow.mjs reads
// a video's saved runs by these to take the discussion up before the video's own stages.
export const SCRIPT_DISCUSSION_VARIANTS = Object.freeze(["discuss", "anime-discuss-plan"]);
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

/**
 * The reply to a line on a document whose planner request was sent and its answer lost
 * (client.mjs RUN_UNCERTAIN): the planner may have run, and been paid for, and the server keeps
 * no answer to fetch again, so the worker does not ask again on its own; the owner does.
 */
export const lostReply = (why) => `模型的請求送出後沒有收到回答（${why}），可能已經在伺服器上跑過並計費；為了不重複付費，工人不會自己再問一次。要再問，請在這裡再寫一次。`;

/** The reply to a line on a document whose planner request the site refused: the same request would be refused again. */
export const refusedReply = (why) => `網站拒絕了這次的模型請求（${why}），同樣的請求再送一次也會被拒絕。這條討論串先停在這裡；請換個說法再問一次，或直接改文件。`;

/**
 * The reply to a line on the screenplay of a video blocked for a reason that is not this line's
 * (answerScript): its screenplay is not changed while the owner has the video to look at, and the
 * site hands over one line at a time, so holding this one would hold every line behind it.
 */
export const blockedReply = (why) => `這支影片目前停住了（${why}），劇本先不動。請先在影片頁處理（重試或放棄），再在這裡問一次。`;

// Where a reply the site did not take is kept (postAnswer), beside the video's auto.json or a
// series' planner answers: the line is handed over again, and the paid answer is posted, not bought again.
const UNPOSTED_FILE = "discussion-answer.json";

/**
 * Post the answer to the owner's line, keeping it first in `dir`: a site that does not take it
 * hands the same line over on a later round, and takeUnposted posts this answer then, with no
 * second model request (the answer was paid for, and a screenplay it rewrote is already saved).
 */
async function postAnswer(automation, dir, id, body) {
  const file = path.join(dir, UNPOSTED_FILE);
  atomicWrite(file, `${JSON.stringify({ message_id: id, body }, null, 2)}\n`);
  const result = await automation.api.messageAnswer(id, body);
  rmSync(file, { force: true });
  return result;
}

/**
 * The answer kept for this line when the site did not take it (postAnswer), posted now, or
 * undefined when none is kept. A kept answer of another line (answered or withdrawn since) is
 * set aside.
 */
async function takeUnposted(automation, dir, id) {
  const file = path.join(dir, UNPOSTED_FILE);
  const kept = readJson(file, null);
  if (!kept) return undefined;
  if (kept.message_id !== id) {
    rmSync(file, { force: true });
    return undefined;
  }
  const result = await automation.api.messageAnswer(id, kept.body);
  rmSync(file, { force: true });
  return result ?? null;
}

/**
 * The reply to a line on a brand story's screenplay (docs/videos/STORY.md): a story is written and
 * checked a chapter at a time from its checked plan (story.mjs), and a whole-script rewrite here
 * would be undone by the next merge of the chapters, and never checked.
 */
export const STORY_THREAD_REPLY = "品牌故事的稿子是照查核過的企劃逐章寫、逐章查核的，這裡不直接改稿。要改旁白，請在影片頁退回旁白並寫下要改什麼：工人會逐章照你的話修；題目本身不對，就放棄這支影片。";

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
      ...(hasAnimePolicy(series) ? { category: series.category, production_policy: series.production_policy, runtime_spec: series.runtime_spec, genre: series.genre, lead: series.lead, compilation: series.compilation, hands_off: series.hands_off } : {}),
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

/**
 * Answer the owner's line on a document: a reply, and a new version when they asked for a change.
 *
 * An error of the planner's request is sorted as a video's would be (flow.mjs errorScope), with
 * no video to block: an answer lost after the request went out (RUN_UNCERTAIN) and a refusal the
 * same request would meet again are told to the owner, and the thread waits for them; a busy
 * service or a rate limit leaves the line for the next run, and this one goes on with the series
 * work; trouble that is everyone's ends the run. Until 2026-10-07 every one of them ended the
 * run, every round: a lost answer was asked, and paid for, again on each, and a refusal met again.
 * An answer the site did not take is kept and posted on a later round (postAnswer), not bought again.
 */
export async function answerDocument(automation, job) {
  const { series } = job;
  const slug = `series-${series.slug}`;
  const dir = path.join(automation.workBase, "_series", series.slug);
  if (automation.waitingLines?.has(job.message.id)) return null;
  if (await takeUnposted(automation, dir, job.message.id) !== undefined) return `series ${series.slug}: the planner's answer on ${job.subject}, kept when the site did not take it, is posted`;
  let answer;
  try {
    answer = await automation.stage("planner", slug, documentDiscussionPayload(automation, job), 32_000, "drama", "discuss", series);
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    if (error.code === OUTPUT_INVALID) {
      automation.keepAnswer(dir, "discuss");
      await postAnswer(automation, dir, job.message.id, { reply_md: unusableReply(error.message), revised: null });
      return `series ${series.slug}: the planner gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`;
    }
    const why = error.why ?? error.message;
    if (error.code === RUN_UNCERTAIN) {
      await postAnswer(automation, dir, job.message.id, { reply_md: lostReply(why), revised: null });
      return `series ${series.slug}: the planner's answer on ${job.subject} was lost on the way (${why}); the owner is told, and it is not asked again on its own`;
    }
    const scope = automation.errorScope(error);
    if (scope === "video") {
      await automation.api.messageAnswer(job.message.id, { reply_md: refusedReply(`${error.code || `HTTP ${error.status}`}: ${error.message}`), revised: null });
      return `series ${series.slug}: the site refused the planner request on ${job.subject} (${error.code || `HTTP ${error.status}`}: ${error.message}); the owner is told and the thread waits`;
    }
    if (scope === "wait") {
      automation.waitingLines.add(job.message.id);
      return `series ${series.slug}: the planner request on ${job.subject} could not finish (${error.code || `HTTP ${error.status}`}: ${error.message}); the line waits for the next run`;
    }
    throw error;
  }
  const problem = answerProblem(answer);
  if (problem) {
    automation.keepAnswer(dir, "discuss");
    await postAnswer(automation, dir, job.message.id, { reply_md: unusableReply(problem), revised: null });
    return `series ${series.slug}: the planner gave no usable answer on ${job.subject} (${problem}); the owner is told and the thread waits`;
  }
  let reply = clip(answer.reply);
  let revised = null;
  if (answer.revised) {
    const refused = revisedDocumentProblem(answer.revised, job);
    if (refused) reply = clip(`${reply}\n\n（新版本沒有存下來：${refused}）`);
    else revised = { body_md: answer.revised.body_md.endsWith("\n") ? answer.revised.body_md : `${answer.revised.body_md}\n`, body_json: answer.revised.body_json };
  }
  const result = await postAnswer(automation, dir, job.message.id, { reply_md: reply, revised, ...(revised && job.revision_context ? { revision_context: job.revision_context } : {}) });
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
 *
 * Null, with nothing sent and the line left unanswered, while the video is not at rest
 * (Automation.resting): another lane is moving it, a lane set it aside in this run, its writer is
 * still running on the server, or it waits on its own from an earlier round (a deferral: this
 * run never looked at it, so a job sent before may still be running). The line is taken up on a
 * later unit or round: a deferral ends in a visit without trouble or in a block. Since
 * 2026-10-06 a pending writer no longer ends the run, so this step runs right after it: a
 * discussion sent then was a second writer request for the same video while the first was in
 * flight, and a rewrite it saved left the first job's paid answer matching no request (or, with
 * the first draft still pending, told the owner there was no screenplay yet). The site hands
 * over one line at a time, so the lines behind a held one wait with it.
 *
 * The mirror image holds too: from the resting check to the end the discussion holds its video
 * in the lanes' shared `busy` set, as a lane's own unit does, so no lane sends the video's own
 * writer or verifier request while the discussion's is in flight; a job still running when the
 * unit ends keeps the video set aside (flow.mjs step, stepUnit).
 *
 * An error of the writer's request is the video's, sorted as its own stages' are (flow.mjs
 * requestFailed): an answer lost after the request went out (RUN_UNCERTAIN) blocks the video as
 * `uncertain:writer`, a saved job the server no longer has (client.mjs `gone`, after the worker
 * was paired again) as `job_gone:writer`, a refusal the same request would meet again with the
 * reason, and a policy hold parks it; a busy service or a rate limit defers it, and the line
 * waits with it (resting). The video keeps the line's id (`blocked_line`) while it is blocked by
 * it, and the line stays unanswered until the owner's retry, after which it is sent once more:
 * any saved journal stays until that retry sets it aside. Until 2026-10-07 only a job gone did
 * this; every other error left this step as an exception, every round, before any series work
 * or draft, and a lost answer with no durable journal was asked, and paid for, again on each.
 *
 * A line on the screenplay of a video blocked for another reason is answered with the block
 * (blockedReply), not held: the site hands over one line at a time, and a block the owner may
 * never retry would hold every line behind it. An answer the site did not take is kept and
 * posted on a later visit (postAnswer), not bought again.
 */
export async function answerScript(automation, job) {
  const { series } = job;
  const state = scriptStateFor(automation, job);
  // Said once a run: the site hands the same line over on every unit until it is answered.
  const held = (slug, why) => {
    if (!automation.heldLines.has(job.message.id)) {
      automation.heldLines.add(job.message.id);
      automation.log(`${slug}: the owner's line on ${job.subject} waits; ${why}`);
    }
    return null;
  };
  if (!state) {
    const blocked = automation.states().find((each) => each.slug === job.episode?.slug && each.status === "blocked");
    const waits = blocked ? heldBy(blocked, job) : null;
    if (waits) return held(blocked.slug, waits);
    if (blocked) {
      await automation.api.messageAnswer(job.message.id, { reply_md: blockedReply(clip(blocked.blocked ?? "").slice(0, 200)), revised: null });
      return `${blocked.slug}: the owner's line on ${job.subject} is answered with the video's block; the thread waits`;
    }
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(`這台工人沒有 ${job.episode?.slug ?? job.subject} 的劇本`), revised: null });
    return `series ${series.slug}: no video for ${job.subject} here; the owner is told and the thread waits`;
  }
  if (!automation.resting(state)) return held(state.slug, "the video is being worked on or waits on its own, and the line is answered once it is at rest");
  // Nothing is awaited between the read of the state, the check and this hold.
  automation.busy.add(state.slug);
  try {
    return await answerHeld(automation, job, state);
  } finally {
    automation.busy.delete(state.slug);
  }
}

/**
 * Why a line on the screenplay of a blocked video waits for the owner's retry instead of being
 * answered, or null: the retry sets aside the writer's saved run that blocked it (a job gone, an
 * answer lost), or the block came from this line's own request (blocked_line).
 */
function heldBy(state, job) {
  if (state.blocked_kind === `${JOB_GONE_KIND}writer`) return "its video is blocked until the owner's retry sets the saved writer job aside, and the line is answered after it";
  if (state.blocked_kind === "uncertain:writer") return "its video is blocked until the owner's retry sets aside the writer run whose answer was lost, and the line is answered after it";
  if (state.blocked_line === job.message.id) return "its video is blocked by this line's own request until the owner's retry, and the line is answered after it";
  return null;
}

/** answerScript once the video is at rest and held: the reply, and the rewrite when one was asked for. */
async function answerHeld(automation, job, state) {
  const { series } = job;
  const workdir = automation.workdir(state.slug);
  if (await takeUnposted(automation, workdir, job.message.id) !== undefined) return `${state.slug}: the writer's answer on ${job.subject}, kept when the site did not take it, is posted`;
  if (state.story) {
    await automation.api.messageAnswer(job.message.id, { reply_md: STORY_THREAD_REPLY, revised: null });
    return `${state.slug}: a story's screenplay is not rewritten from a thread; the owner is told how to change it`;
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
    if (isLongAnime(state)) {
      const payload = scriptDiscussionPayload(automation, job, state, video);
      delete payload.line_ids;
      answer = await automation.stage("writer", state.slug, payload, 8_000, "drama", "anime-discuss-plan", state.series);
      if (typeof answer?.change_required !== "boolean" || answer.revised != null) throw new AutomationError("anime discussion must give a change decision, not a whole-script replacement", { code: OUTPUT_INVALID });
      if (answer.change_required) {
        const revision = await automation.animeRewrite(state, { message: job.message.body_md, thread: threadOf(job), subject: job.subject }, video, "writer", `discuss-${job.message.id}`);
        answer = { reply: answer.reply, revised: { video: revision.video } };
      } else answer = { reply: answer.reply, revised: null };
    } else answer = await automation.stage("writer", state.slug, scriptDiscussionPayload(automation, job, state, video), 32_000, "drama", "discuss");
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    if (error.code === OUTPUT_INVALID) {
      automation.keepAnswer(workdir, "discuss");
      await postAnswer(automation, workdir, job.message.id, { reply_md: unusableReply(error.message), revised: null });
      return `${state.slug}: the writer gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`;
    }
    // A STOP or another producer's lease (flow.mjs PROJECT_HELD, not imported here): step() sets
    // the video aside for the run, and the line waits with it.
    if (error.code === "video_project_held") throw error;
    error.unit ??= `the owner's line on ${job.subject}`;
    const line = await automation.requestFailed(state, error, { sends: `answers the owner's line on ${job.subject} once more`, request: `the writer request for the owner's line on ${job.subject}` });
    if (state.status === "blocked") {
      state.blocked_line = job.message.id;
      automation.persist(state);
    }
    return line;
  }
  const problem = answerProblem(answer);
  if (problem) {
    automation.keepAnswer(workdir, "discuss");
    await postAnswer(automation, workdir, job.message.id, { reply_md: unusableReply(problem), revised: null });
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
      let refused;
      try {
        refused = await automation.saveAndLint(state, { video: revisedVideo });
      } catch (error) {
        // A STOP or a lost lease during the lint repairs (flow.mjs PROJECT_HELD, not imported here:
        // flow.mjs imports this module): the last good script goes back before the video is set
        // aside, unless another producer holds the project now, whose files are its own.
        if (error?.code === "video_project_held") {
          try {
            automation.restoreVideo(state, before);
          } catch (restoreError) {
            if (restoreError?.code !== "video_project_held") throw restoreError;
          }
        }
        throw error;
      }
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
  await postAnswer(automation, workdir, job.message.id, { reply_md: reply, revised: null });
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
