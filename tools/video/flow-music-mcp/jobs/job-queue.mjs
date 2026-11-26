/**
 * Single-worker sequential job queue + per-profile file lock (`RuntimeLock`)
 * with randomized anti-bot pacing, persistent job snapshots, bounded async
 * waiting (`waitForJob`), and mid-batch cancellation (`cancelJob`).
 */

import { randomBytes } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { resolveProfileLockPath, resolveRuntimeHome } from "../config.mjs";
import { atomicWriteJson, readJsonSafe } from "../guards/music-guards.mjs";

function isPidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (err) {
    return err.code === "EPERM";
  }
}

export function computeJitteredPauseMs({ minPauseMs = 1500, maxPauseMs = 4000, random = Math.random } = {}) {
  const low = Math.max(0, Number(minPauseMs) || 0);
  const high = Math.max(low, Number(maxPauseMs) || low);
  return Math.round(low + random() * (high - low));
}

function sleepWithAbort(ms, signal) {
  if (ms <= 0) return Promise.resolve();
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new Error("Job cancelled during pacing pause."));
      return;
    }
    const timer = setTimeout(() => {
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      clearTimeout(timer);
      reject(new Error("Job cancelled during pacing pause."));
    };
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
}

export class RuntimeLock {
  constructor(lockFile, { staleAgeMs = 30 * 60 * 1000 } = {}) {
    this.lockFile = lockFile;
    this.staleAgeMs = staleAgeMs;
  }

  inspect() {
    if (!fs.existsSync(this.lockFile)) {
      return { locked: false, owner: null };
    }
    const payload = readJsonSafe(this.lockFile, null);
    if (!payload) {
      return { locked: true, stale: true, owner: null };
    }
    const ageMs = payload.acquiredAt ? Date.now() - Date.parse(payload.acquiredAt) : Infinity;
    const alive = isPidAlive(payload.pid);
    const stale = !alive || ageMs > this.staleAgeMs;
    return { locked: !stale, stale, owner: payload };
  }

  acquire(meta = {}) {
    fs.mkdirSync(path.dirname(this.lockFile), { recursive: true });
    const tryCreate = () => {
      const fd = fs.openSync(this.lockFile, "wx");
      const record = {
        pid: process.pid,
        acquiredAt: new Date().toISOString(),
        ...meta,
      };
      try {
        fs.writeFileSync(fd, `${JSON.stringify(record, null, 2)}\n`, "utf8");
      } finally {
        fs.closeSync(fd);
      }
      return record;
    };

    try {
      return { acquired: true, record: tryCreate() };
    } catch (err) {
      if (err.code !== "EEXIST") throw err;
      const state = this.inspect();
      if (state.stale) {
        try {
          fs.unlinkSync(this.lockFile);
        } catch {
          // ignore race
        }
        try {
          return { acquired: true, recoveredStale: true, record: tryCreate() };
        } catch (retryErr) {
          if (retryErr.code !== "EEXIST") throw retryErr;
        }
      }
      return { acquired: false, holder: state.owner };
    }
  }

  release() {
    try {
      const existing = readJsonSafe(this.lockFile, null);
      if (!existing || existing.pid === process.pid) {
        fs.unlinkSync(this.lockFile);
      }
    } catch (err) {
      if (err.code !== "ENOENT") throw err;
    }
  }
}

export class JobQueue {
  constructor({
    runtimeHome = resolveRuntimeHome(),
    minPauseMs = 1500,
    maxPauseMs = 4000,
    random = Math.random,
  } = {}) {
    this.runtimeHome = runtimeHome;
    this.jobsDir = path.join(runtimeHome, "jobs");
    this.minPauseMs = minPauseMs;
    this.maxPauseMs = maxPauseMs;
    this.random = random;

    this.jobs = new Map();
    this.pendingQueue = [];
    this.activeJobId = null;
    this.activeAbortController = null;
    this.waiters = new Map();
    this.runningLoop = false;
  }

  inspectLock(profile = null) {
    return new RuntimeLock(resolveProfileLockPath(this.runtimeHome, profile)).inspect();
  }

  #persist(job) {
    fs.mkdirSync(this.jobsDir, { recursive: true });
    const snapshot = {
      jobId: job.jobId,
      kind: job.kind,
      collection: job.collection,
      profile: job.profile || "default",
      status: job.status,
      total: job.total,
      completed: job.completed,
      failed: job.failed,
      skipped: job.skipped,
      currentItem: job.currentItem,
      results: job.results,
      errors: job.errors,
      createdAt: job.createdAt,
      startedAt: job.startedAt,
      finishedAt: job.finishedAt,
    };
    atomicWriteJson(path.join(this.jobsDir, `${job.jobId}.json`), snapshot);
    return snapshot;
  }

  #notifyWaiters(jobId) {
    const set = this.waiters.get(jobId);
    if (!set) return;
    for (const resolve of set) resolve();
    set.clear();
  }

  enqueue({ kind, collection, profile = null, items, worker }) {
    const jobId = `mjob_${Date.now()}_${randomBytes(3).toString("hex")}`;
    const job = {
      jobId,
      kind,
      collection,
      profile: profile || "default",
      status: "queued",
      total: items.length,
      completed: 0,
      failed: 0,
      skipped: 0,
      currentItem: null,
      results: [],
      errors: [],
      createdAt: new Date().toISOString(),
      startedAt: null,
      finishedAt: null,
      items,
      worker,
      cancelled: false,
    };
    this.jobs.set(jobId, job);
    this.#persist(job);
    this.pendingQueue.push(jobId);
    void this.#drain();
    return this.getJob(jobId);
  }

  getJob(jobId) {
    const live = this.jobs.get(jobId);
    if (live) {
      return {
        jobId: live.jobId,
        kind: live.kind,
        collection: live.collection,
        profile: live.profile,
        status: live.status,
        total: live.total,
        completed: live.completed,
        failed: live.failed,
        skipped: live.skipped,
        currentItem: live.currentItem,
        results: live.results,
        errors: live.errors,
        createdAt: live.createdAt,
        startedAt: live.startedAt,
        finishedAt: live.finishedAt,
      };
    }
    return readJsonSafe(path.join(this.jobsDir, `${jobId}.json`), null);
  }

  cancelJob(jobId) {
    const job = this.jobs.get(jobId);
    if (!job) {
      return { ok: false, found: false, message: `Job "${jobId}" not found.` };
    }
    if (["completed", "failed", "cancelled"].includes(job.status)) {
      return { ok: true, alreadyFinished: true, job: this.getJob(jobId) };
    }
    job.cancelled = true;
    if (job.status === "queued") {
      job.status = "cancelled";
      job.skipped = job.total;
      job.finishedAt = new Date().toISOString();
      this.pendingQueue = this.pendingQueue.filter((id) => id !== jobId);
      this.#persist(job);
      this.#notifyWaiters(jobId);
      return { ok: true, job: this.getJob(jobId) };
    }
    if (this.activeJobId === jobId && this.activeAbortController) {
      this.activeAbortController.abort();
    }
    return { ok: true, cancelling: true, job: this.getJob(jobId) };
  }

  async waitForJob(jobId, { timeoutMs = 25_000 } = {}) {
    const deadline = Date.now() + Math.max(0, Number(timeoutMs) || 0);
    while (true) {
      const snapshot = this.getJob(jobId);
      if (!snapshot) {
        return { ok: false, found: false, message: `Job "${jobId}" not found.` };
      }
      if (["completed", "failed", "cancelled"].includes(snapshot.status)) {
        return { ok: true, done: true, job: snapshot };
      }
      const remaining = deadline - Date.now();
      if (remaining <= 0) {
        return { ok: true, done: false, job: snapshot };
      }
      await new Promise((resolve) => {
        if (!this.waiters.has(jobId)) this.waiters.set(jobId, new Set());
        const set = this.waiters.get(jobId);
        let done = false;
        const wake = () => {
          if (done) return;
          done = true;
          clearTimeout(timer);
          set.delete(wake);
          resolve();
        };
        const timer = setTimeout(wake, Math.min(remaining, 1000));
        set.add(wake);
      });
    }
  }

  async #drain() {
    if (this.runningLoop) return;
    this.runningLoop = true;
    try {
      while (this.pendingQueue.length > 0) {
        const jobId = this.pendingQueue.shift();
        const job = this.jobs.get(jobId);
        if (!job || job.cancelled) continue;

        const lock = new RuntimeLock(resolveProfileLockPath(this.runtimeHome, job.profile));
        const acquired = lock.acquire({ jobId, kind: job.kind, collection: job.collection, profile: job.profile });
        if (!acquired.acquired) {
          job.status = "failed";
          job.skipped = job.total;
          job.errors.push({
            code: "profile_locked",
            message: `Profile "${job.profile}" is already locked by PID ${acquired.holder?.pid ?? "unknown"}.`,
          });
          job.finishedAt = new Date().toISOString();
          this.#persist(job);
          this.#notifyWaiters(jobId);
          continue;
        }

        this.activeJobId = jobId;
        this.activeAbortController = new AbortController();
        job.status = "running";
        job.startedAt = new Date().toISOString();
        this.#persist(job);

        try {
          for (let i = 0; i < job.items.length; i += 1) {
            if (job.cancelled || this.activeAbortController.signal.aborted) {
              job.skipped = job.items.length - i;
              job.status = "cancelled";
              break;
            }
            const item = job.items[i];
            job.currentItem = item.cue || item.clipId || item.id || `item_${i + 1}`;
            this.#persist(job);

            try {
              const res = await job.worker(item, {
                index: i,
                signal: this.activeAbortController.signal,
              });
              job.results.push(res);
              job.completed += 1;
              this.#persist(job);
            } catch (err) {
              if (job.cancelled || this.activeAbortController.signal.aborted) {
                job.skipped = job.items.length - i;
                job.status = "cancelled";
                break;
              }
              job.failed += 1;
              const serialized = err?.toJSON
                ? err.toJSON()
                : { code: err?.code || "worker_error", message: err?.message || String(err), retryable: false };
              job.errors.push({ item: job.currentItem, ...serialized });

              // Fail-Fast on auth expiry, rate limit, or selector drift
              if (["auth_expired", "rate_limited", "selector_drift", "chrome_not_found"].includes(serialized.code)) {
                job.skipped = job.items.length - i - 1;
                job.status = "failed";
                this.#persist(job);
                break;
              }
              this.#persist(job);
            }

            if (i < job.items.length - 1 && !job.cancelled) {
              const pauseMs = computeJitteredPauseMs({
                minPauseMs: this.minPauseMs,
                maxPauseMs: this.maxPauseMs,
                random: this.random,
              });
              try {
                await sleepWithAbort(pauseMs, this.activeAbortController.signal);
              } catch {
                job.skipped = job.items.length - i - 1;
                job.status = "cancelled";
                break;
              }
            }
          }

          if (job.status === "running") {
            job.status = job.failed > 0 && job.completed === 0 ? "failed" : "completed";
          }
        } finally {
          job.currentItem = null;
          job.finishedAt = new Date().toISOString();
          this.#persist(job);
          this.#notifyWaiters(jobId);
          this.activeJobId = null;
          this.activeAbortController = null;
          lock.release();
        }
      }
    } finally {
      this.runningLoop = false;
    }
  }
}
