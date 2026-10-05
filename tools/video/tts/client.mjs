// Calls to the narration server (apps/web/app/api/video/speech → apps/api/app/video_speech).
//
// Failures are sorted by who can fix them, which is what the CLI's exit code reports: the owner
// (a revoked token, the card not filled in, a voice not on the allowlist), the service (budget
// spent, Azure down), or nobody right now (throttling, retried with the server's Retry-After).
// A paid request (speech, speech/transcribe, speech/judge) is sent again only when it never reached
// the API or the API settled it; one that went out and lost its answer stops (SPEECH_UNCERTAIN).
import { createHash } from "node:crypto";
import { NARRATION_LOCALE } from "../core/schema.mjs";
import { toNarrationRate } from "./wav.mjs";

export const USER_AGENT = "Mokaair-video-cli/1.0 (https://mokaair.com; support@mokaair.com)";

// A paid request was sent and no answer came back: the connection dropped after it went out, a
// gateway or the web route answered instead of the API, or the answer broke off on the way. The
// server may have synthesized, transcribed or judged it, and been charged; it keeps no answer to
// fetch again and takes no idempotency key, so the request is not sent again. The error names the
// request (`path`, `requestSha256` of the body sent) and is the owner's (exit 3); its one-line
// message ends with this code, which the worker (automation/flow.mjs) reads to block the video
// rather than give a dub up.
export const SPEECH_UNCERTAIN = "video_speech_uncertain";

export class SpeechError extends Error {
  constructor(message, { status = 0, code = "", who = "service" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    // "owner": needs the site owner (exit 3); "service": external service or quota (exit 4).
    this.who = who;
  }
}

const OWNER_CODES = new Set(["video_tool_token_invalid", "video_speech_not_configured", "video_speech_voice_not_allowed"]);
const RETRYABLE_CODES = new Set(["video_speech_upstream_busy", "rate_limit_exceeded", "video_speech_upstream_failed", "upstream_unavailable"]);
// A paid request's 5xx the API answers itself (apps/api/app/video_speech/admin_api.py; synthesis
// gives the reserved characters back first), retried as before. Settled only when the API reached
// the provider's answer or never connected: `video_speech_upstream_failed` and
// `video_judge_upstream_failed` also cover a provider read timeout or dropped answer after the
// request went out (any httpx.HTTPError), which may have been billed, and are still resent until
// 2026-10-05-speech-api-tells-a-provider-answer gives that case its own code.
const SETTLED_CODES = new Set(["video_speech_upstream_busy", "video_speech_upstream_failed", "video_speech_upstream_rejected_key", "video_judge_upstream_failed"]);
// The speech routes' own 502 `upstream_unavailable` (apps/web/app/api/video/speech/forward.ts) is
// an API they never reached, so nothing ran and it is retried as well. Since #1272 they answer a
// request the API took and whose answer was lost with 504 `video_speech_answer_lost` (SPEECH_LOST,
// uncertain here like any 5xx not listed). A host from before that answers this 502 for both, so
// this client needs a host that serves #1272 (production does since c12e159d0, deployed
// 2026-10-05). Only the 502: no speech route answers the code with another status, so a 503
// `upstream_unavailable` came from something else and stays uncertain.
const NEVER_REACHED = { status: 502, code: "upstream_unavailable" };
const settled = (status, code) => SETTLED_CODES.has(code) || (status === NEVER_REACHED.status && code === NEVER_REACHED.code);
// Connection errors that mean the request never reached a server, so nothing it asks has started.
const NEVER_SENT = new Set(["ECONNREFUSED", "ENOTFOUND", "EAI_AGAIN", "EHOSTUNREACH", "ENETUNREACH", "UND_ERR_CONNECT_TIMEOUT"]);

const neverSent = (error) => NEVER_SENT.has(error?.cause?.code ?? error?.code);

function uncertain(path, body, cause, status = 0) {
  const requestSha256 = createHash("sha256").update(body ?? "").digest("hex");
  // One line, so the code stays in the last line the CLIs print.
  const why = String(cause).replace(/\s+/g, " ").trim();
  const message = `POST /api/video/${path} was sent and no usable answer came back (${why}); it may have run and been charged, so it is not sent again (${SPEECH_UNCERTAIN}, request sha256 ${requestSha256})`;
  return Object.assign(new SpeechError(message, { status, code: SPEECH_UNCERTAIN, who: "owner" }), { path, requestSha256, why });
}

async function problemOf(response) {
  try {
    const body = await response.json();
    return { code: body.code ?? "", detail: body.detail ?? body.title ?? "" };
  } catch {
    return { code: "", detail: "" };
  }
}

function retryDelayMs(response, attempt) {
  const header = Number(response?.headers.get("retry-after"));
  if (Number.isFinite(header) && header > 0) return Math.min(header, 60) * 1000;
  return Math.min(2 ** attempt, 30) * 1000;
}

async function call({ site, token, path, init, fetchImpl, sleep, attempts, paid = false }) {
  let last;
  for (let attempt = 0; attempt < attempts; attempt++) {
    let response;
    try {
      response = await fetchImpl(`${site}/api/video/${path}`, {
        ...init,
        headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW", ...(init?.headers ?? {}) },
      });
    } catch (error) {
      if (paid && !neverSent(error)) throw uncertain(path, init.body, error.cause?.message ?? error.message);
      last = new SpeechError(`cannot reach ${site}: ${error.message}`, { code: "network" });
      await sleep(retryDelayMs(null, attempt));
      continue;
    }
    if (response.ok) return response;
    const problem = await problemOf(response);
    const message = problem.detail || `HTTP ${response.status}`;
    if (response.status === 401 || OWNER_CODES.has(problem.code)) throw new SpeechError(message, { status: response.status, code: problem.code, who: "owner" });
    // A spent budget stays spent for the rest of the month (speech) or day (Jev): do not retry.
    if (problem.code === "video_speech_budget_exhausted" || problem.code === "jev_budget_exhausted") {
      throw new SpeechError(message, { status: response.status, code: problem.code });
    }
    if (paid && response.status >= 500 && !settled(response.status, problem.code)) {
      throw uncertain(path, init.body, `HTTP ${response.status}${problem.code ? ` ${problem.code}` : ""}${problem.detail ? `: ${problem.detail}` : ""}`, response.status);
    }
    last = new SpeechError(message, { status: response.status, code: problem.code });
    if (!(RETRYABLE_CODES.has(problem.code) || response.status === 429 || response.status >= 500)) throw last;
    await sleep(retryDelayMs(response, attempt));
  }
  throw last;
}

const defaults = (options) => ({ fetchImpl: globalThis.fetch, sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)), attempts: 5, ...options });

export async function speechStatus(options) {
  const response = await call({ ...defaults(options), path: "speech/status", init: { method: "GET" } });
  return response.json();
}

/**
 * One paid POST and `read` of its answer. An answer that breaks off or cannot be read was still
 * paid for, so it is SPEECH_UNCERTAIN like a lost one, never sent again.
 */
async function postPaid(options, path, body, read) {
  const init = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const response = await call({ ...defaults(options), path, init, paid: true });
  try {
    return await read(response);
  } catch (error) {
    throw uncertain(path, init.body, `the answer could not be read: ${error.message}`, response.status);
  }
}

// The server's default language for a clip and for Jev's state; a dub names its own.
const trackLanguage = (language) => (language === NARRATION_LOCALE ? {} : { language });

/**
 * The words in one clip, as the server's transcriber hears them. `terms` are the English words
 * the line says and `language` the locale the clip is read in; a server from before either
 * existed refuses the field, so each goes only when it says something the default does not.
 */
export async function transcribeClip({ wav, terms = [], language = NARRATION_LOCALE, ...options }) {
  const request = { audio: Buffer.from(wav).toString("base64"), ...(terms.length ? { terms } : {}), ...trackLanguage(language) };
  return postPaid(options, "speech/transcribe", request, async (response) => {
    const body = await response.json();
    return typeof body.text === "string" ? body.text : "";
  });
}

/**
 * Jev's probability, per line id, that each transcript says its intended words; one Jev call.
 * `language` is what the lines are written in, sent the same way as for a clip.
 */
export async function judgeLines({ lines, language = NARRATION_LOCALE, ...options }) {
  return postPaid(options, "speech/judge", { lines, ...trackLanguage(language) }, async (response) => {
    const body = await response.json();
    return new Map((body.results ?? []).map((result) => [result.id, Number(result.noul)]));
  });
}

/** Synthesize one request body; resolves to the WAV bytes and the billable characters charged. */
export async function synthesize({ body, ...options }) {
  // Gemini voices come back at 24 kHz; everything downstream works on the 48 kHz grid.
  return postPaid(options, "speech", body, async (response) => ({
    wav: toNarrationRate(Buffer.from(await response.arrayBuffer())),
    billable: Number(response.headers.get("x-billable-characters") || 0),
  }));
}
