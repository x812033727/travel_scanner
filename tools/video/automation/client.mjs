// Calls to the automation endpoints (apps/web/app/api/video/automation → apps/api/app/video_automation):
// the owner's settings, one writing stage run with the model the settings name, and topic
// candidates. The same token as tts and review-push; on the host the worker sets MOKAAIR_SITE to
// the web container, so these never leave the compose network.
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";
import { stopRequested } from "../core/paths.mjs";
import { normalizeRun, policyHeld, POLICY_HOLD_CODE, RunReceiptError, runReceiptStore } from "./run-receipts.mjs";
import path from "node:path";

// A stage answered something that is not the JSON it was asked for; flow.mjs retries it later.
export const OUTPUT_INVALID = "video_ai_output_invalid";
// A stage run was sent and no answer came back: the connection dropped, or a deadline passed (the
// web route's 504 under this same code, a gateway's 5xx). The model may still have run, and been
// paid for, on the server, which keeps no answer to fetch again: on 2026-09-29 a translation
// finished after 302 s, past the web route's 295 s, and was recorded as ok. The run is not sent
// again here; flow.mjs stops the video for a person instead of paying twice. A Jev judgement whose
// answer was lost throws it too, and its callers (review/sync.mjs, qa/cli.mjs) leave it for a
// later round instead of asking Jev again at once.
export const RUN_UNCERTAIN = "video_ai_run_uncertain";
// A durable run still has a recoverable server receipt. The worker ends this round and polls
// that same operation next round instead of holding a gateway open for several minutes.
export const RUN_PENDING = "video_ai_run_pending";
export const POLICY_HOLD = POLICY_HOLD_CODE;

export class AutomationError extends Error {
  constructor(message, { status = 0, code = "", who = "service" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    // "owner": needs the site owner (token, keys, a budget they set); "service": try again later.
    this.who = who;
  }
}

const OWNER_CODES = new Set([
  POLICY_HOLD,
  "video_tool_token_invalid",
  "video_ai_provider_not_configured",
  "video_ai_budget_exhausted",
  "video_ai_subscription_cli_outdated",
  "video_automation_settings_invalid",
  // The Shorts settings name no tested model yet (docs/videos/SHORTS.md §端點): nothing ran.
  "video_ai_subject_not_chosen",
]);
// What the tutorial and drama rounds ask the video list for: every video but the Shorts, so ninety
// days of Shorts do not push them past the list's cap of 200 (docs/videos/SHORTS.md §資料模型).
export const TUTORIAL_LIST = Object.freeze({ shorts: "exclude" });
const RETRYABLE_CODES = new Set(["video_ai_upstream_busy", "video_ai_upstream_unreachable", "rate_limit_exceeded", "upstream_unavailable"]);
// Every subscription account is at the owner's cap: nothing ran, and retrying within minutes will
// not help. This run of `auto` ends; the worker's loop tries again on its next round.
const PAUSE_CODES = new Set(["video_ai_subscription_paused"]);
// A stage run's 5xx that settles it: the API's own answer once the run is over (it is recorded as
// failed, no answer was lost), or the web route's 502 for an API it never reached. Any other 5xx
// after a stage run was sent leaves its outcome unknown (RUN_UNCERTAIN).
const SETTLED_RUN_CODES = new Set(["video_ai_upstream_busy", "video_ai_upstream_unreachable", "video_ai_upstream_failed", OUTPUT_INVALID, "upstream_unavailable"]);
// A Jev judgement (judge/policy, judge/outline) takes one call off the daily Jev budget before it
// asks Jev (apps/api/app/video_automation/judge.py `_ask`), so it is paid like a stage run. Its only
// settling 5xx is the API's own 502 once its Jev call failed: the API answered, and no verdict was
// lost on the way back. The judge routes name no lost answer of their own
// (apps/web/app/api/video/speech/forward.ts `lost`), so their 502 upstream_unavailable may follow a
// request the API received and answered too late: uncertain here, unlike a stage run's.
const SETTLED_JUDGE_CODES = new Set(["video_judge_upstream_failed"]);
const JUDGE = Object.freeze({ paid: true, settled: SETTLED_JUDGE_CODES, what: "Jev" });
// Connection errors that mean the request never reached a server, so nothing it asks has started.
const NEVER_SENT = new Set(["ECONNREFUSED", "ENOTFOUND", "EAI_AGAIN", "EHOSTUNREACH", "ENETUNREACH", "UND_ERR_CONNECT_TIMEOUT"]);

const neverSent = (error) => NEVER_SENT.has(error?.cause?.code ?? error?.code);

async function problemOf(response) {
  try {
    const body = await response.json();
    return { code: body.code ?? "", detail: body.detail ?? body.title ?? "" };
  } catch {
    return { code: "", detail: "" };
  }
}

function delayMs(response, attempt) {
  const header = Number(response?.headers.get("retry-after"));
  if (Number.isFinite(header) && header > 0) return Math.min(header, 120) * 1000;
  return Math.min(2 ** attempt * 5, 120) * 1000;
}

/**
 * A client bound to the stored site and token; `attempts` covers busy vendors and restarts. A
 * stage run or a Jev judgement (`paid`) is sent again only when nothing ran or the API settled it
 * (`settled`): never after a request that went out and lost its answer (RUN_UNCERTAIN).
 */
export function automationClient(ctx, { attempts = 4, durablePollMs = 25_000, durablePollIntervalMs = 1000 } = {}) {
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) throw new AutomationError("no video tool token yet: run `node tools/video/cli.mjs login`", { who: "owner" });
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  const sleep = ctx.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  const receipts = runReceiptStore(ctx, site);
  let durable = false;
  const uncertain = (route, why, status = 0, what = "the model") =>
    Object.assign(new AutomationError(`${route} was sent and no answer came back (${why}); ${what} may have run, so it is not sent again`, { status, code: RUN_UNCERTAIN }), { why });
  async function request(method, route, json, { paid = false, settled = SETTLED_RUN_CODES, what = "the model" } = {}) {
    let last;
    for (let attempt = 0; attempt < attempts; attempt++) {
      let response;
      try {
        response = await fetchImpl(`${site}/api/video/${route}`, {
          method,
          headers: {
            Authorization: `Bearer ${token}`,
            "User-Agent": USER_AGENT,
            "Accept-Language": "zh-TW",
            ...(json ? { "Content-Type": "application/json" } : {}),
          },
          body: json ? JSON.stringify(json) : undefined,
        });
      } catch (error) {
        if (paid && !neverSent(error)) throw uncertain(route, error.cause?.message ?? error.message, 0, what);
        last = new AutomationError(`cannot reach ${site}: ${error.message}`, { code: "network" });
        await sleep(delayMs(null, attempt));
        continue;
      }
      if (response.ok) {
        if (!paid) return response.json();
        try {
          return await response.json();
        } catch (error) {
          // The stage or judgement ran and its answer broke off on the way: it is not paid for again either.
          throw uncertain(route, `the answer could not be read: ${error.message}`, response.status, what);
        }
      }
      const problem = await problemOf(response);
      const message = problem.detail || `HTTP ${response.status}`;
      if (response.status === 401 || OWNER_CODES.has(problem.code)) throw new AutomationError(message, { status: response.status, code: problem.code, who: "owner" });
      if (PAUSE_CODES.has(problem.code)) throw new AutomationError(message, { status: response.status, code: problem.code });
      if (paid && response.status >= 500 && !settled.has(problem.code)) throw uncertain(route, `HTTP ${response.status}${problem.detail ? `: ${problem.detail}` : ""}`, response.status, what);
      last = new AutomationError(message, { status: response.status, code: problem.code });
      if (!(RETRYABLE_CODES.has(problem.code) || response.status === 429 || response.status >= 500)) throw last;
      await sleep(delayMs(response, attempt));
    }
    throw last;
  }
  const tagged = (error, body) => Object.assign(error, { slug: body.slug, stage: body.stage });
  async function durableRun(body, previous) {
    const entry = previous ?? receipts.prepare(body);
    const started = Date.now(), budget = Math.max(1, Math.min(durablePollMs, 25_000));
    const interval = Math.max(1, Math.min(durablePollIntervalMs, budget));
    let waited = 0, failures = 0;
    function completed() {
      const receipt = entry.record.receipt;
      if (policyHeld(entry.record)) {
        const refusal = receipt ?? entry.record.policy_rejection;
        throw tagged(Object.assign(new AutomationError(refusal.error_detail || "the video route is disabled; its original refusal is retained", {
          code: POLICY_HOLD, status: refusal.error_status ?? 409, who: "owner",
        }), { policy_hold: { format: entry.record.request.format, stage: entry.record.request.stage, receipt_id: receipt?.id ?? null } }), body);
      }
      if (receipt?.status === "succeeded") { receipts.consume(entry); return receipt.result; }
      if (receipt?.status === "uncertain") throw tagged(new AutomationError(receipt.error_detail || "the saved model run is uncertain; the owner must inspect it before retrying", { code: RUN_UNCERTAIN, status: receipt.error_status ?? 0, who: "owner" }), body);
      if (receipt?.status === "failed") {
        const error = tagged(new AutomationError(receipt.error_detail || "the saved model run failed", { code: receipt.error_code ?? "video_ai_upstream_failed", status: receipt.error_status ?? 502,
          who: OWNER_CODES.has(receipt.error_code) ? "owner" : "service" }), body);
        if (receipt.retry_after !== null && receipt.retry_after !== undefined) error.retry_after = receipt.retry_after;
        receipts.removeFailed(entry);
        throw error;
      }
      return null;
    }
    let lastProblem = "";
    for (;;) {
      const result = completed();
      if (result) return result;
      const remaining = budget - Math.max(waited, Date.now() - started);
      if (remaining <= 0 || stopRequested(path.dirname(path.dirname(entry.file)))) break;
      const known = entry.record.receipt;
      const route = known ? `automation/run/jobs/${known.id}?input_hash=${known.input_hash}` : "automation/run/jobs";
      try {
        const response = await fetchImpl(`${site}/api/video/${route}`, {
          method: known ? "GET" : "POST",
          headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW",
            ...(!known ? { "Content-Type": "application/json" } : {}) },
          ...(!known ? { body: JSON.stringify({ ...entry.record.request, request_key: entry.record.request_key }) } : {}),
          signal: AbortSignal.timeout(Math.max(1, Math.floor(remaining))),
        });
        if (!response.ok) {
          const problem = await problemOf(response);
          if (!known && response.status === 409 && problem.code === POLICY_HOLD) {
            receipts.hold(entry, { error_code: POLICY_HOLD, error_status: 409, error_detail: problem.detail || "the video route is disabled" });
            completed();
          }
          const error = new AutomationError(problem.detail || `HTTP ${response.status}`, { status: response.status, code: problem.code,
            who: response.status === 401 || OWNER_CODES.has(problem.code) || response.status === 409 ? "owner" : "service" });
          if (error.who === "owner" || response.status < 429 || PAUSE_CODES.has(problem.code)) throw tagged(error, body);
          lastProblem = error.message;
          failures++;
        } else {
          let receipt;
          try { receipt = await response.json(); }
          catch { // A partial body has the same safe recovery as a lost connection: reuse the key.
            lastProblem = "the receipt response ended before it could be read";
            failures++;
          }
          if (receipt !== undefined) { receipts.receive(entry, receipt); failures = 0; }
        }
      } catch (error) {
        if (error instanceof RunReceiptError || error instanceof AutomationError) throw error;
        // GET or same-key POST can reconnect safely. The persisted key survives process exit.
        lastProblem = error.message;
        failures++;
      }
      const resultAfter = completed();
      if (resultAfter) return resultAfter;
      if (failures >= attempts || stopRequested(path.dirname(path.dirname(entry.file)))) break;
      const wait = Math.min(interval, budget - Math.max(waited, Date.now() - started));
      if (wait <= 0) break;
      await sleep(wait);
      waited += wait;
    }
    throw tagged(new AutomationError(`the saved stage run is still pending${lastProblem ? ` (${lastProblem})` : ""}; its receipt will be recovered next round`, { code: RUN_PENDING }), body);
  }
  async function run(stage, slug, instructions, payload, maxOutputTokens = 16_000, format = "slides", variant = null) {
    const body = { stage, slug, instructions, payload, max_output_tokens: maxOutputTokens, format, ...(variant ? { variant } : {}) };
    // Anime acts and brand-story chapters already have their own bounded checkpoints.
    if (stage !== "writer" || ["anime-act", "story"].includes(variant)) return request("POST", "automation/run", body, { paid: true });
    try {
      const normalized = normalizeRun(body), previous = receipts.find(normalized);
      if (durable || previous) return await durableRun(normalized, previous);
      return await request("POST", "automation/run", body, { paid: true });
    } catch (error) {
      if (error instanceof RunReceiptError) throw tagged(Object.assign(new AutomationError(error.message, { code: RUN_UNCERTAIN, who: "owner" }), { why: error.message, receipt_code: error.code ?? "" }), body);
      throw error;
    }
  }
  async function retryRuns(slug, authorization = {}) {
    try {
      const confirmed = [];
      for (const entry of receipts.retryCandidates(slug, authorization)) {
        if (stopRequested(path.dirname(path.dirname(entry.file)))) throw new Error("STOP prevents this owner retry");
        const saved = entry.record.receipt;
        if (policyHeld(entry.record)) {
          const freshSettings = await request("GET", "automation/settings");
          const requestFormat = entry.record.request.format;
          const savedVideo = entry.record.request.payload.video;
          const correctedSlides = requestFormat === "drama" && savedVideo && typeof savedVideo === "object" && !Array.isArray(savedVideo)
            && (savedVideo.format ?? "slides") === "slides"
            && authorization.format === "slides";
          const dramaEnabled = freshSettings.drama?.drama_enabled ?? freshSettings.drama_enabled;
          if (freshSettings.enabled !== true || (!correctedSlides && (requestFormat !== "drama" || dramaEnabled !== true))) {
            throw Object.assign(new AutomationError("the saved policy still disables this video; its original receipt is retained", { code: POLICY_HOLD, status: 409, who: "owner" }),
              { slug, policy_hold: { format: requestFormat, stage: entry.record.request.stage, receipt_id: saved?.id ?? null } });
          }
          if (!saved) { confirmed.push({ entry, fresh: null, policyValidated: true }); continue; }
        }
        const response = await fetchImpl(`${site}/api/video/automation/run/jobs/${saved.id}?input_hash=${saved.input_hash}`, {
          method: "GET", headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW" },
          signal: AbortSignal.timeout(25_000),
        });
        if (!response.ok) {
          const problem = await problemOf(response);
          throw new Error(problem.detail || `HTTP ${response.status}`);
        }
        const fresh = receipts.receive(entry, await response.json());
        if (policyHeld(entry.record) && (fresh.status !== "failed" || fresh.error_code !== POLICY_HOLD || fresh.dispatched_at !== null)) {
          throw new Error("the saved policy refusal is no longer a verified undispatched failure");
        }
        confirmed.push({ entry, fresh, policyValidated: policyHeld(entry.record) });
      }
      // Verify every selected lookup before archiving any operation. A failed lookup leaves
      // all keys in place, even when another operation's current state was already readable.
      for (const { entry, fresh, policyValidated } of confirmed) {
        if (stopRequested(path.dirname(path.dirname(entry.file)))) throw new Error("STOP prevents this owner retry");
        // A late successful commit is recovered by the normal run path, before any budget
        // check. Only a freshly confirmed uncertain result permits this explicit new attempt.
        if (policyValidated || fresh.status === "uncertain" || fresh.status === "succeeded" && authorization.reason?.includes("inputs changed")) receipts.archive(entry, { ...authorization, policyValidated });
      }
    } catch (error) {
      if (error instanceof AutomationError && error.code === POLICY_HOLD) throw error;
      throw Object.assign(new AutomationError(`could not verify the saved run before owner retry: ${error.message}; its receipt is retained`, { code: RUN_UNCERTAIN, who: "owner" }), { slug, why: error.message });
    }
  }
  return {
    settings: async () => {
      const settings = await request("GET", "automation/settings");
      durable = settings.durable_stage_runs === true;
      return settings;
    },
    topics: () => request("GET", "automation/topics"),
    /**
     * Every video on /admin/videos, dropped ones too: slug, title, source_guide, dropped_at. With
     * no query the Shorts are left out (TUTORIAL_LIST); the Shorts round asks { shorts: "only" }.
     */
    videos: (query = TUTORIAL_LIST) => request("GET", `automation/videos?${new URLSearchParams(query)}`),
    /**
     * One stage: the server answers with the model the owner chose; returns { text, usage, … }.
     * An answer lost on the way throws RUN_UNCERTAIN instead of paying for the stage again.
     */
    run,
    /** After this returned output has been saved; later corrections may use new inputs. */
    adoptRuns: (slug, proof) => receipts.adopt(slug, proof),
    /** Only after this caller's completed unit has saved its artifacts and state. */
    settleRuns: (slugs) => receipts.settle(slugs),
    /** An explicit owner retry clears uncertain runs only; queued/running evidence stays. */
    retryRuns,
    /** Report the video's title, stage and checklist to /admin/videos. */
    report: (slug, project) => request("PUT", `reviews/${slug}`, project),
    /** Submit one review; the same content twice returns the review that exists. */
    submit: (slug, review) => request("POST", `reviews/${slug}/reviews`, review),
    /**
     * Jev's policy reading of a finished script for the QA's `policy` item (docs/videos/HANDS-OFF.md
     * §自動品管; tools/video/qa/policy.mjs shapes the body). Until the judge ticket ships the
     * endpoint, the site answers 404 and the caller reports it as not available. One Jev call:
     * an answer lost on the way throws RUN_UNCERTAIN instead of spending another (JUDGE).
     */
    judgePolicy: (body) => request("POST", "automation/judge/policy", body, JUDGE),
    /**
     * Jev's choice among a brief's outlines (docs/videos/HANDS-OFF.md §Jev 挑大綱): body
     * { slug, brief, options: [{ key, title, summary, hook }] }, 2 to 3 options, no other field.
     * Answers { choice, probabilities, options: { key: { stance, demo } }, advice, passed, note };
     * 409 video_judge_not_enabled while the stance is blank or the switch is off. One Jev call,
     * never asked again here once it was sent and its answer lost (RUN_UNCERTAIN, JUDGE).
     */
    judgeOutline: (body) => request("POST", "automation/judge/outline", body, JUDGE),
    /** The video's reviews as the owner left them, newest first. */
    reviews: async (slug) => {
      try {
        return await request("GET", `reviews/${slug}`);
      } catch (error) {
        if (error.status === 404) return null;
        throw error;
      }
    },
    // The owner's drama requests (docs/videos/DRAMA.md): filed on /admin/videos, made before any scheduled draft.
    /** The oldest request nobody has started, or null. */
    dramaNext: async () => (await request("GET", "automation/drama-requests/next")).request ?? null,
    /** Claim a request for the video about to be made under `slug`. */
    dramaStart: (id, slug) => request("POST", `automation/drama-requests/${id}/start`, { slug }),
    /** Report a request's video finished and confirmed for upload. */
    dramaDone: (id) => request("POST", `automation/drama-requests/${id}/done`),
    // A long series (docs/videos/SERIES.md): the site says what is next, the worker reports back.
    /** The next document to plan or episode to start, or null while every series waits. */
    seriesNext: async () => (await request("GET", "automation/series/next")).job ?? null,
    /** The prompts' context for a series, narrowed to one episode's chapter. */
    seriesContext: (slug, episode) => request("GET", `automation/series/${slug}/context${episode ? `?episode=${episode}` : ""}`),
    /** File a planned document as a new version that waits for the owner. */
    seriesDoc: (slug, doc) => request("POST", `automation/series/${slug}/docs`, doc),
    /** Start an episode under the video's slug; answers with the request row and the context. */
    episodeStart: (slug, number, videoSlug) => request("POST", `automation/series/${slug}/episodes/${number}/start`, { slug: videoSlug }),
    /** Keep the finished episode's recap and the characters' states for the next one. */
    episodeRecap: (slug, number, body) => request("POST", `automation/series/${slug}/episodes/${number}/recap`, body),
    /** Report the episode cleared for upload, so the next one may start. */
    episodeDone: (slug, number) => request("POST", `automation/series/${slug}/episodes/${number}/done`),
    // The discussion threads (docs/videos/DRAMA-FLOW.md, section 3): the owner's lines on a
    // document or a screenplay, answered one per round by the planner or the writer.
    /** The oldest line waiting for the model, with the thread and the context, or null. */
    messageNext: async () => (await request("GET", "automation/series/messages/next")).job ?? null,
    /** The model's reply, and for a document the revised version the owner reads next. */
    messageAnswer: (id, body) => request("POST", `automation/series/messages/${id}/answer`, body),
    // A binge series' compilation (docs/videos/BINGE.md): started under the video's slug once
    // every episode is cleared for upload, reported done when the compilation is.
    compilationStart: (slug, videoSlug) => request("POST", `automation/series/${slug}/compilation/start`, { slug: videoSlug }),
    compilationDone: (slug) => request("POST", `automation/series/${slug}/compilation/done`),
    // The Shorts worker (docs/videos/SHORTS.md §端點; apps/api/app/video_shorts/admin_automation_api.py
    // through apps/web/app/api/video/automation/shorts). A site from before Shorts answers 404.
    /** The Shorts settings the tools read (ToolSettingsView), or null on a site without Shorts. */
    shortsSettings: async () => {
      try {
        return await request("GET", "automation/shorts/settings");
      } catch (error) {
        if (error.status === 404) return null;
        throw error;
      }
    },
    /** The next job (NextOut): { kind: report|plan|brief|make|null, holds, report|plan|brief|make }; null without Shorts. */
    shortsNext: async () => {
      try {
        return await request("GET", "automation/shorts/next");
      } catch (error) {
        if (error.status === 404) return null;
        throw error;
      }
    },
    /** The planner's week (PlanIn): items [{ slot_id, topic_slug }]; an empty list says nothing fit. */
    shortsPlan: (items) => request("POST", "automation/shorts/plan", { items }),
    /** New topics and completed ideas (TopicsIn): every topic names its slug. */
    shortsTopics: (topics) => request("POST", "automation/shorts/topics", { topics }),
    /** The week's report (ReportIn): week_start, body_md, rows, plan, provider, model. */
    shortsReport: (body) => request("POST", "automation/shorts/report", body),
    /** Start a topic: answers { topic, project_slug, created }. */
    shortsStart: (topic) => request("POST", `automation/shorts/${topic}/start`),
    /** The topic is done (DoneIn): { outcome: "made" | "dropped", note? }. */
    shortsDone: (topic, body = { outcome: "made" }) => request("POST", `automation/shorts/${topic}/done`, body),
  };
}
