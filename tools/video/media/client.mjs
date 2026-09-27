// Calls to the media server (apps/web/app/api/video/media → apps/api/app/video_media).
//
// The same shape as tts/client.mjs: failures are sorted by who can fix them, which is what the
// CLI's exit code reports: the owner (a revoked token, the drama switched off, no vendor key, a
// model the settings tab must change, a spent budget), the service (a vendor down or over
// quota, retried with the server's Retry-After), or the tool's own bug. A generation is a job:
// submitted, then polled until it is ready, then its file fetched by SHA-256; the server moves
// the job one step per poll, so polling is the work, not a wait.
import { createHash } from "node:crypto";
import { closeSync, createWriteStream, mkdirSync, openSync, readSync, renameSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { Readable, Transform } from "node:stream";
import { pipeline } from "node:stream/promises";

import { sha256File } from "../core/approvals.mjs";

export const USER_AGENT = "Mokaair-video-cli/1.0 (https://mokaair.com; support@mokaair.com)";
// Mirrors PART_BYTES in apps/api/app/video_reviews/storage.py: under nginx's 6 MB request cap.
export const PART_BYTES = 4 * 1024 * 1024;
export const TERMINAL = new Set(["ready", "failed", "expired"]);
const MIN_POLL_MS = 3000;
const MAX_POLL_MS = 60_000;

export class MediaError extends Error {
  constructor(message, { status = 0, code = "", who = "service", job = null } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    // "owner": needs the site owner (exit 3); "service": external service or quota (exit 4); "tool": our bug (exit 2).
    this.who = who;
    this.job = job;
  }
}

const OWNER_CODES = new Set([
  "video_tool_token_invalid",
  "video_media_disabled",
  "video_media_not_configured",
  "video_media_model_not_allowed",
  "video_media_budget_exhausted",
  "video_media_judge_unavailable",
]);
const TOOL_CODES = new Set(["video_media_reference_missing", "video_media_reference_too_large", "video_media_route_unknown", "video_media_bad_part", "video_media_hash_mismatch"]);
const RETRYABLE_CODES = new Set(["video_media_upstream_busy", "video_media_job_busy", "rate_limit_exceeded", "upstream_unavailable", "video_media_judge_failed"]);
// Codes of a failed job that a new seed may fix; the stages retake on these, not on the owner's.
export const RETAKE_CODES = new Set(["video_media_rejected", "video_media_upstream_failed", "video_media_upstream_expired", "video_media_unsupported_type", "video_media_upstream_invalid"]);

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

async function call({ site, token, path: route, init, fetchImpl, sleep, attempts }) {
  let last;
  for (let attempt = 0; attempt < attempts; attempt++) {
    let response;
    try {
      response = await fetchImpl(`${site}/api/video/media/${route}`, {
        ...init,
        headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW", ...(init?.headers ?? {}) },
      });
    } catch (error) {
      last = new MediaError(`cannot reach ${site}: ${error.message}`, { code: "network" });
      await sleep(retryDelayMs(null, attempt));
      continue;
    }
    if (response.ok) return response;
    const problem = await problemOf(response);
    const message = problem.detail || `HTTP ${response.status}`;
    if (response.status === 401 || OWNER_CODES.has(problem.code)) throw new MediaError(message, { status: response.status, code: problem.code, who: "owner" });
    if (TOOL_CODES.has(problem.code)) throw new MediaError(message, { status: response.status, code: problem.code, who: "tool" });
    last = new MediaError(message, { status: response.status, code: problem.code });
    if (!(RETRYABLE_CODES.has(problem.code) || response.status === 429 || response.status >= 500)) throw last;
    await sleep(retryDelayMs(response, attempt));
  }
  throw last;
}

const defaults = (options) => ({ fetchImpl: globalThis.fetch, sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)), attempts: 5, ...options });

const postJson = (options, route, body) =>
  call({ ...defaults(options), path: route, init: { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } });

/** What the server offers and allows right now: providers, models, budgets, the store, limits. */
export async function mediaStatus(options) {
  const response = await call({ ...defaults(options), path: "status", init: { method: "GET" } });
  return response.json();
}

/** Submit an image job: `{ slug, purpose, prompt, negative_prompt?, aspect?, references?, seed?, shot_id?, idempotency_key? }`. */
export async function submitImage({ request, ...options }) {
  return (await postJson(options, "images", request)).json();
}

/** Submit a clip job: `{ slug, shot_id, prompt, first_frame, last_frame?, references?, seconds, resolution?, native_audio?, seed?, ... }`. */
export async function submitClip({ request, ...options }) {
  return (await postJson(options, "clips", request)).json();
}

/** Submit a music job: `{ slug, prompt, seconds, idempotency_key? }`. */
export async function submitMusic({ request, ...options }) {
  return (await postJson(options, "music", request)).json();
}

/** The job as the server sees it now; asking is what moves it on. */
export async function pollOnce({ jobId, ...options }) {
  const response = await call({ ...defaults(options), path: `jobs/${jobId}`, init: { method: "GET" } });
  return response.json();
}

/**
 * Poll a job until it is terminal. `stop()` is checked between polls (the STOP file); when it
 * says so, a MediaError with code "stopped" carries the last job state so the caller can keep
 * its id and resume next time. `timeoutMs` bounds one job's total wait.
 */
export async function waitForJob({ jobId, stop = () => false, timeoutMs = 20 * 60_000, onPoll = () => {}, ...options }) {
  const { sleep, now = () => Date.now() } = defaults(options);
  const started = now();
  let job = await pollOnce({ jobId, ...options });
  while (!TERMINAL.has(job.status)) {
    onPoll(job);
    if (stop()) throw new MediaError(`stopped while job ${jobId} was ${job.status}`, { code: "stopped", job });
    if (now() - started > timeoutMs) throw new MediaError(`job ${jobId} is still ${job.status} after ${Math.round(timeoutMs / 60_000)} minutes`, { code: "timeout", job });
    const wait = Math.min(Math.max((job.retry_after_seconds || 5) * 1000, MIN_POLL_MS), MAX_POLL_MS);
    await sleep(wait);
    job = await pollOnce({ jobId, ...options });
  }
  return job;
}

/** Submit then wait; returns the terminal job. `submit` is one of the submit* functions. */
export async function runJob({ submit, request, ...options }) {
  const job = await submit({ request, ...options });
  if (TERMINAL.has(job.status)) return job;
  return waitForJob({ jobId: job.id, ...options });
}

/**
 * Fetch a file from the store by its SHA-256 into `file`, streaming through `.partial` and
 * verifying the hash as it arrives, so a torn download never carries the name of a good one.
 */
export async function downloadFile({ slug, sha256, file, maxBytes = 200 * 1024 * 1024, ...options }) {
  const response = await call({ ...defaults(options), path: `files/${slug}/${sha256}`, init: { method: "GET", headers: { Accept: "*/*" } } });
  const declared = Number(response.headers.get("content-length"));
  if (Number.isFinite(declared) && declared > maxBytes) throw new MediaError(`${sha256.slice(0, 12)} is ${declared} bytes, over the ${maxBytes} limit`, { code: "too_large", who: "tool" });
  mkdirSync(path.dirname(file), { recursive: true });
  const partial = `${file}.partial`;
  const hash = createHash("sha256");
  let size = 0;
  const source = response.body ? Readable.fromWeb(response.body) : Readable.from([Buffer.from(await response.arrayBuffer())]);
  const counted = new Transform({
    transform(chunk, _encoding, done) {
      size += chunk.length;
      if (size > maxBytes) return done(new MediaError(`${sha256.slice(0, 12)} grew past ${maxBytes} bytes`, { code: "too_large", who: "tool" }));
      hash.update(chunk);
      done(null, chunk);
    },
  });
  try {
    await pipeline(source, counted, createWriteStream(partial));
    const digest = hash.digest("hex");
    if (digest !== sha256) throw new MediaError(`downloaded ${sha256.slice(0, 12)} but the bytes hash to ${digest.slice(0, 12)}`, { code: "hash_mismatch" });
    rmSync(file, { force: true });
    renameSync(partial, file);
  } finally {
    rmSync(partial, { force: true });
  }
  return { file, sha256, bytes: size, content_type: response.headers.get("content-type") ?? "" };
}

/** Upload a local file to the store in parts unless the server has it; returns its SHA-256. */
export async function putFile({ slug, file, ...options }) {
  const sha256 = await sha256File(file);
  const size = statSync(file).size;
  const parts = Math.max(1, Math.ceil(size / PART_BYTES));
  const handle = openSync(file, "r");
  try {
    for (let part = 0; part < parts; part++) {
      const length = Math.min(PART_BYTES, size - part * PART_BYTES);
      const bytes = Buffer.alloc(length);
      readSync(handle, bytes, 0, length, part * PART_BYTES);
      const response = await call({
        ...defaults(options),
        path: `files/${slug}/${sha256}?part=${part}&parts=${parts}&size=${size}`,
        init: { method: "PUT", headers: { "Content-Type": "application/octet-stream" }, body: bytes },
      });
      const result = await response.json();
      if (result.complete) break;
    }
  } finally {
    closeSync(handle);
  }
  return { sha256, size };
}

/**
 * Ask the judge: `{ slug, kind, files: [{ sha256, label }], rubric: [{ key, question, weight? }], context?, min_score? }`
 * → `{ scores, overall, passed, problems, notes, model }`.
 */
export async function judge({ request, ...options }) {
  return (await postJson(options, "judge", request)).json();
}
