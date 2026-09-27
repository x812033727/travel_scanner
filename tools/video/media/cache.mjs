// What the media stages already paid for, and what they are still waiting on.
//
// media/cache.json maps a request key (everything that changes the picture: provider, model,
// prompt, references, seed, size) to the file it produced, so a rerun after an edit regenerates
// only the shots whose keys changed. media/jobs.json holds the server job ids of requests that
// were submitted but not finished when the run stopped (STOP file, a crash, a timeout), so the
// next run polls them instead of paying for the same generation twice.
import { createHash } from "node:crypto";
import { existsSync, rmSync } from "node:fs";
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";
import { ARTIFACTS } from "../core/state.mjs";

export const CACHE_VERSION = 1;

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  return value;
}

/** A short key for one request: the kind and every field that changes the result, order-insensitive. */
export function mediaKey(kind, fields) {
  return createHash("sha256").update(JSON.stringify([CACHE_VERSION, kind, canonical(fields)])).digest("hex").slice(0, 16);
}

export const cacheFile = (workdir) => path.join(workdir, ARTIFACTS.mediaCache);
export const jobsFile = (workdir) => path.join(workdir, ARTIFACTS.mediaJobs);

export function readCache(workdir) {
  return readJson(cacheFile(workdir), { version: CACHE_VERSION, entries: {} });
}

export function writeCache(workdir, cache) {
  atomicWrite(cacheFile(workdir), `${JSON.stringify(cache, null, 2)}\n`);
}

/** The cached file for a key when it is still on disk; null otherwise (and the entry is dropped). */
export function cached(workdir, key) {
  const cache = readCache(workdir);
  const entry = cache.entries[key];
  if (!entry) return null;
  if (!existsSync(path.join(workdir, entry.file))) {
    delete cache.entries[key];
    writeCache(workdir, cache);
    return null;
  }
  return entry;
}

/** Record what a key produced: `{ file (relative to the work directory), sha256, bytes, job_id, provider, model, cost_usd }`. */
export function remember(workdir, key, entry, now = new Date()) {
  const cache = readCache(workdir);
  cache.entries[key] = { ...entry, created_at: now.toISOString() };
  writeCache(workdir, cache);
  return cache.entries[key];
}

/** Drop the entries (and their files) a stage no longer references, e.g. after a retake won. */
export function forget(workdir, keys) {
  const cache = readCache(workdir);
  const removed = [];
  for (const key of keys) {
    const entry = cache.entries[key];
    if (!entry) continue;
    rmSync(path.join(workdir, entry.file), { force: true });
    delete cache.entries[key];
    removed.push(key);
  }
  if (removed.length) writeCache(workdir, cache);
  return removed;
}

export function readJobs(workdir) {
  return readJson(jobsFile(workdir), { jobs: {} });
}

export function writeJobs(workdir, jobs) {
  atomicWrite(jobsFile(workdir), `${JSON.stringify(jobs, null, 2)}\n`);
}

/** The server job id a key is waiting on, or null. */
export function pendingJob(workdir, key) {
  return readJobs(workdir).jobs[key] ?? null;
}

export function rememberJob(workdir, key, { job_id: jobId, kind, target }, now = new Date()) {
  const jobs = readJobs(workdir);
  jobs.jobs[key] = { job_id: jobId, kind, target, submitted_at: now.toISOString() };
  writeJobs(workdir, jobs);
}

export function forgetJob(workdir, key) {
  const jobs = readJobs(workdir);
  if (!(key in jobs.jobs)) return;
  delete jobs.jobs[key];
  writeJobs(workdir, jobs);
}
