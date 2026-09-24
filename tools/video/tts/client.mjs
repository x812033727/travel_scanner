// Calls to the narration server (apps/web/app/api/video/speech → apps/api/app/video_speech).
//
// Failures are sorted by who can fix them, which is what the CLI's exit code reports: the owner
// (a revoked token, the card not filled in, a voice not on the allowlist), the service (budget
// spent, Azure down), or nobody right now (throttling, retried with the server's Retry-After).
import { toNarrationRate } from "./wav.mjs";

export const USER_AGENT = "Mokaair-video-cli/1.0 (https://mokaair.com; support@mokaair.com)";

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

async function call({ site, token, path, init, fetchImpl, sleep, attempts }) {
  let last;
  for (let attempt = 0; attempt < attempts; attempt++) {
    let response;
    try {
      response = await fetchImpl(`${site}/api/video/${path}`, {
        ...init,
        headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW", ...(init?.headers ?? {}) },
      });
    } catch (error) {
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

const postJson = (options, path, body) =>
  call({ ...defaults(options), path, init: { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } });

/** The words in one clip, as the server's transcriber hears them. */
export async function transcribeClip({ wav, ...options }) {
  const response = await postJson(options, "speech/transcribe", { audio: Buffer.from(wav).toString("base64") });
  const body = await response.json();
  return typeof body.text === "string" ? body.text : "";
}

/** Jev's probability, per line id, that each transcript says its intended words; one Jev call. */
export async function judgeLines({ lines, ...options }) {
  const response = await postJson(options, "speech/judge", { lines });
  const body = await response.json();
  return new Map((body.results ?? []).map((result) => [result.id, Number(result.noul)]));
}

/** Synthesize one request body; resolves to the WAV bytes and the billable characters charged. */
export async function synthesize({ body, ...options }) {
  const response = await call({
    ...defaults(options),
    path: "speech",
    init: { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) },
  });
  // Gemini voices come back at 24 kHz; everything downstream works on the 48 kHz grid.
  return { wav: toNarrationRate(Buffer.from(await response.arrayBuffer())), billable: Number(response.headers.get("x-billable-characters") || 0) };
}
