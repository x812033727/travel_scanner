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
// The replies to a line on a document whose request failed (answerDocument): there is no video to
// block for the owner's retry, so the thread is answered once instead of the request ending, or
// being paid for, every round; and to a line on a blocked video's screenplay (answerScript).
export const lostReply = (why) => `這句話的回答在途中遺失了（${why}），模型可能已經跑完並計費。為了不重複付費，這裡不會自動再問；要再問一次，請重新送出這句話。`;
export const refusedReply = (why) => `回答這句話的請求被拒絕了（${why}），同樣的請求再送也會被拒。這條討論串先停在這裡；請縮短或拆開這句話再送，若是模型服務的設定（例如金鑰）出了問題，請先到 AI 設定確認；也可以直接改文件。`;
export const failingReply = (why, rounds) => `回答這句話的請求連續 ${rounds} 輪都沒能完成（${why}）。這條討論串先停在這裡，好讓後面的討論繼續；請稍後再送一次這句話，或直接改文件。`;
export const blockedReply = (why) => `這支影片目前停住了（${why}），它的劇本要等你在影片頁按「重試這支影片」之後才會處理。重試後請再送一次這句話。`;

/**
 * What a document's thread decided about a line across rounds (answerDocument), under
 * _series/<slug>/threads.json: `waits`, how many rounds its request could not finish, and `lost`,
 * a lost answer whose reply is still to reach the site. Saved before the reply goes up, so a
 * reply the site did not take is posted next round instead of the request being bought again.
 */
function threadNotes(automation, series) {
  const file = automation.workBase ? path.join(automation.workBase, "_series", series.slug, "threads.json") : null;
  const saved = file ? readJson(file, null) : null;
  const notes = { waits: { ...(saved?.waits ?? {}) }, lost: { ...(saved?.lost ?? {}) } };
  const save = () => file && atomicWrite(file, `${JSON.stringify(notes, null, 2)}\n`);
  return { notes, save };
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

/** Answer the owner's line on a document: a reply, and a new version when they asked for a change. */
export async function answerDocument(automation, job) {
  const { series } = job;
  const slug = `series-${series.slug}`;
  const id = job.message.id;
  // A line whose planner could not be asked in this run (a busy service) waits for the next round.
  if (automation.heldLines?.has(id)) return null;
  const { notes, save } = threadNotes(automation, series);
  const toldLost = async (why) => {
    await automation.api.messageAnswer(id, { reply_md: lostReply(why), revised: null });
    delete notes.lost[id];
    save();
    return `series ${series.slug}: the planner's answer on ${job.subject} was lost (${why}); the owner is told it may have run, and it is asked again only when they send the line again`;
  };
  // Lost in an earlier round, and the reply did not reach the site then: told now, not asked again.
  if (notes.lost[id]) return toldLost(notes.lost[id]);
  const told = async (reply, line) => {
    await automation.api.messageAnswer(id, { reply_md: reply, revised: null });
    if (notes.waits[id] !== undefined) {
      delete notes.waits[id];
      save();
    }
    return line;
  };
  let answer;
  try {
    answer = await automation.stage("planner", slug, documentDiscussionPayload(automation, job), 32_000, "drama", "discuss", series);
  } catch (error) {
    if (error instanceof AutomationError && error.code === OUTPUT_INVALID) {
      automation.keepAnswer(path.join(automation.workBase, "_series", series.slug), "discuss");
      return told(unusableReply(error.message), `series ${series.slug}: the planner gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`);
    }
    // A document's thread has no video to block for the owner's retry (answerScript has one): a
    // lost answer or a refusal is answered for once, so it neither ends nor is paid for every
    // round, and a request that could not finish waits for the next round, until the owner is
    // told after deferLimit rounds (the site hands over the oldest line first: one held for ever
    // holds every thread after it).
    const scope = automation.threadScope(error);
    const code = error.code || `HTTP ${error.status}`;
    if (scope === "lost") {
      notes.lost[id] = error.why ?? error.message;
      delete notes.waits[id];
      save();
      return toldLost(notes.lost[id]);
    }
    if (scope === "run") throw error;
    // The model service's own settled 502 is a request it turns down, as the site's 4xx is: asking again changes nothing.
    if (scope === "video" || error.code === "video_ai_upstream_failed") {
      return told(refusedReply(`${code}: ${error.message}`), `series ${series.slug}: the planner request on ${job.subject} was refused (${code}: ${error.message}); the owner is told and the thread waits`);
    }
    const rounds = (notes.waits[id] ?? 0) + 1;
    if (rounds >= (automation.deferLimit ?? 6)) {
      return told(failingReply(`${code}: ${error.message}`, rounds), `series ${series.slug}: the planner request on ${job.subject} could not finish in ${rounds} rounds (${code}: ${error.message}); the owner is told and the threads after it move on`);
    }
    notes.waits[id] = rounds;
    save();
    automation.heldLines.add(id);
    automation.log(`series ${series.slug}: the owner's line on ${job.subject} waits; the planner request could not finish (${code}: ${error.message}), and it is asked again next round`);
    return null;
  }
  if (notes.waits[id] !== undefined) {
    delete notes.waits[id];
    save();
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
 * Every other failure of the discussion's request is its video's, sorted as its own writer's
 * would be (Automation.sortFailure): a saved job the server no longer has (client.mjs `gone`,
 * after the worker was paired again) blocks the video as `job_gone:writer`, its journal kept until
 * the owner's retry sets it aside; an answer that may have run without reaching the worker blocks
 * it as `uncertain:writer`, and the run ends once; a refusal of the request blocks it with the
 * reason; a busy service makes it wait (defer). Until 2026-10-06 every one of them, and until
 * 2026-10-07 all but the gone job, left this step as an exception every round: the run ended
 * here, before any series work or draft, a lost answer could be paid for again each round, and no
 * retry could reach the journal because no video was blocked for it. A lint repair of the rewrite
 * (Automation.saveAndLint) whose answer was lost is the discussion's request too: the last good
 * script goes back, and the video is blocked as `uncertain:writer` the same way.
 *
 * The line whose request blocked its video (recorded as `blocked_line`), and any line while the
 * video's writer job is gone, stays unanswered until the owner's retry and is sent once after it.
 * A video blocked for anything else does not hold the line: the site hands over the oldest
 * unanswered line of every series (apps/api/app/video_automation/messages.py next_message), so
 * one held line holds every thread behind it until that retry. The owner is told the video is
 * blocked and to send the line again after the retry; before 2026-10-07 they were told there was
 * no screenplay here.
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
    if (blocked?.blocked_kind === `${JOB_GONE_KIND}writer`) return held(blocked.slug, "its video is blocked until the owner's retry sets the saved writer job aside, and the line is answered after it");
    if (blocked?.blocked_line === job.message.id) return held(blocked.slug, "its video is blocked until the owner's retry, and the line is answered after it");
    if (blocked) {
      await automation.api.messageAnswer(job.message.id, { reply_md: blockedReply(blocked.blocked ?? "原因見影片頁"), revised: null });
      return `${blocked.slug}: blocked, so the owner is told the line on ${job.subject} waits for the retry and the thread moves on`;
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

/** answerScript once the video is at rest and held: the reply, and the rewrite when one was asked for. */
async function answerHeld(automation, job, state) {
  const { series } = job;
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
    if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) {
      // Nothing of the video's is settled with this unit: a long anime's plan, paid for before its
      // act request failed, is taken again from its saved run on the next attempt, not bought again.
      automation.runSlugs?.delete(state.slug);
      return automation.sortFailure(state, error, { sends: `answers the owner's line on ${job.subject} once more`, line: job.message.id });
    }
    automation.keepAnswer(automation.workdir(state.slug), "discuss");
    await automation.api.messageAnswer(job.message.id, { reply_md: unusableReply(error.message), revised: null });
    return `${state.slug}: the writer gave no usable answer on ${job.subject} (${error.message}); the owner is told and the thread waits`;
  }
  if (state.discussion_waits) {
    delete state.discussion_waits;
    automation.saveState(automation.workdir(state.slug), state);
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
      let refused;
      try {
        refused = await automation.saveAndLint(state, { video: revisedVideo });
      } catch (error) {
        // A STOP or a lost lease during the lint repairs (flow.mjs PROJECT_HELD, not imported here:
        // flow.mjs imports this module): the last good script goes back before the video is set
        // aside, unless another producer holds the project now, whose files are its own. A lint
        // repair whose answer was lost (RUN_UNCERTAIN: the writer may have run, and been paid for)
        // puts it back too, and is the discussion's own request: the video is blocked as
        // `uncertain:writer` with the line held, and the owner's retry sends the line once more.
        // Until 2026-10-07 it left the step every round, the revision stayed in video.json, and
        // the video's own unit sent the same paid repair again.
        const lost = error instanceof AutomationError && error.code === RUN_UNCERTAIN;
        if (lost || error?.code === "video_project_held") {
          try {
            automation.restoreVideo(state, before);
          } catch (restoreError) {
            if (restoreError?.code !== "video_project_held") throw restoreError;
          }
        }
        if (!lost) throw error;
        // Its paid answer is not settled with this unit either: on a durable run the retry takes it again from its saved run.
        automation.runSlugs?.delete(state.slug);
        return automation.sortFailure(state, error, { sends: `answers the owner's line on ${job.subject} once more`, line: job.message.id });
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
