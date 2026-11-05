// How `check-audio` and `dub` send their paid speech requests several at a time.
//
// A day of the daily podcast is ~250 lines in 8 locales, each transcribed by check-audio and
// synthesized by dub; one request at a time that took about ten hours on 2026-11-04. The owner
// approved sending up to VIDEO_SPEECH_CONCURRENCY at once (default 4) the same day. What a run
// leaves behind must not depend on which answer comes back first, so the callers here start the
// work in script order, save each answer as it arrives, and report in script order.
import { UsageError } from "../core/paths.mjs";

export const SPEECH_CONCURRENCY_ENV = "VIDEO_SPEECH_CONCURRENCY";
export const DEFAULT_SPEECH_CONCURRENCY = 4;

/** How many speech requests a run may have out at once: VIDEO_SPEECH_CONCURRENCY, default 4. */
export function speechConcurrency(env = {}) {
  const value = env[SPEECH_CONCURRENCY_ENV];
  if (value === undefined || value === "") return DEFAULT_SPEECH_CONCURRENCY;
  const text = String(value).trim();
  if (!/^[0-9]+$/.test(text) || Number(text) < 1) {
    throw new UsageError(`${SPEECH_CONCURRENCY_ENV} must be a whole number of requests, at least 1 (1 sends one at a time): got ${JSON.stringify(value)}`);
  }
  return Number(text);
}

/**
 * Work through `items` in order, at most `limit()` jobs at once. Before each item, `halt()` may
 * name a reason to launch nothing more (a STOP file, a service that keeps failing); then
 * `prepare(item, index)` runs at once, in order, and gives `{ keys, run }`. `run()` is the job.
 *
 * Two jobs that share a key never run together: the later waits for the earlier to finish
 * completely, which is what a sequential run does. A job only ever waits for jobs already
 * running, and those wait for nothing, so this cannot deadlock.
 *
 * A job that throws, or a `prepare` that does, stops the launching; the jobs already out still
 * finish (their answers are paid for and get saved), then the first error is thrown. Resolves
 * to `{ halted }`: the reason `halt()` gave, or null when every item was launched.
 *
 * `limit()` is read before every launch, so a caller can drop to one at a time mid-run. With a
 * limit of 1 each job finishes before the next item is looked at: the loop a run had before.
 */
export async function sendInOrder(items, { limit, halt = () => null, prepare }) {
  const running = new Map();
  let failure = null;
  let halted = null;
  const settleOne = () => Promise.race(running.keys());
  const conflicts = (keys) => keys.length > 0 && [...running.values()].some((held) => keys.some((key) => held.has(key)));
  for (let index = 0; index < items.length; index++) {
    while (running.size >= Math.max(1, limit())) await settleOne();
    if (failure) break;
    halted = halt() || null;
    if (halted) break;
    let job;
    try {
      job = prepare(items[index], index);
    } catch (error) {
      failure = { error };
      break;
    }
    const keys = [...new Set(job.keys ?? [])];
    if (conflicts(keys)) {
      while (conflicts(keys)) await settleOne();
      if (failure) break;
      halted = halt() || null;
      if (halted) break;
    }
    const task = (async () => job.run())()
      .catch((error) => {
        failure ??= { error };
      })
      .finally(() => running.delete(task));
    running.set(task, new Set(keys));
  }
  while (running.size) await settleOne();
  if (failure) throw failure.error;
  return { halted };
}

// The answers that say the service wants fewer requests: the routes' own rate limit, a provider
// that is busy (client.mjs retries both after a wait). A spent budget is a 429 too, but asking
// more slowly does not help it; client.mjs gives it up at once.
const BUSY_CODES = new Set(["rate_limit_exceeded", "video_speech_upstream_busy"]);
const busyAnswer = (status, code) => BUSY_CODES.has(code) || (status === 429 && !code.endsWith("_budget_exhausted"));

/**
 * Client options (tts/client.mjs) whose fetch calls `onBusy({ status, code })` on each busy or
 * 429 answer, before the client sees it; everything else passes through untouched. The client
 * still retries such an answer as it always did: this only tells the caller to send fewer.
 */
export function watchBusy(options, onBusy) {
  const inner = options.fetchImpl;
  return {
    ...options,
    fetchImpl: async (url, init) => {
      const response = await (inner ?? globalThis.fetch)(url, init);
      if (response && !response.ok && (response.status === 429 || response.status >= 500)) {
        let code = "";
        try {
          code = String((await response.clone().json())?.code ?? "");
        } catch {
          // No JSON code: the status alone decides.
        }
        if (busyAnswer(response.status, code)) onBusy({ status: response.status, code });
      }
      return response;
    },
  };
}

/**
 * `record` with its keys in a sequential run's order: the keys it had when the run began, where
 * they were, then the others in `order` (the script's ids). A run that saves answers as they
 * arrive inserts new keys in completion order; this writes the same file whichever came first.
 */
export function inRunOrder(record, initial, order) {
  const rank = new Map();
  for (const id of [...initial, ...order]) if (!rank.has(id)) rank.set(id, rank.size);
  const last = rank.size;
  return Object.fromEntries(Object.entries(record).sort(([a], [b]) => (rank.get(a) ?? last) - (rank.get(b) ?? last)));
}
