/**
 * Single-worker sequential job queue with cross-client file lock (`runtime.lock`),
 * randomized pacing between Flow submissions, persistent job snapshots, and
 * bounded async waiting (`waitForJob`) so MCP clients (Claude/Codex/Antigravity)
 * never hit 60s tool timeouts.
 */

import { randomBytes } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { resolveProfileLockPath, resolveRuntimeHome } from "../config.mjs";
import { atomicWriteJson, readJsonSafe } from "../guards/budget-guard.mjs";

function isPidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (err) {
    // EPERM means process exists under another privilege level
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
          // race with another waiter
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
    this.lock = new RuntimeLock(resolveProfileLockPath(runtimeHome, null));
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

  lockForProfile(profile = null) {
    if (!profile || profile === "default") return this.lock;
    return new RuntimeLock(resolveProfileLockPath(this.runtimeHome, profile));
  }

  jobFile(jobId) {
    return path.join(this.jobsDir, `${jobId}.json`);
  }

  persistJob(job) {
    atomicWriteJson(this.jobFile(job.jobId), job);
  }

  notifyWaiters(jobId) {
    const set = this.waiters.get(jobId);
    if (!set) return;
    for (const resolve of set) resolve();
    set.clear();
  }

  getLockStatus(profile = null) {
    return this.lockForProfile(profile).inspect();
  }

  getJob(jobId) {
    if (this.jobs.has(jobId)) {
      return structuredClone(this.jobs.get(jobId));
    }
    const persisted = readJsonSafe(this.jobFile(jobId), null);
    return persisted ? structuredClone(persisted) : null;
  }

  /**
   * Enqueues a multi-item sequential Flow job. Returns immediately with the
   * initial job snapshot (non-blocking).
   */
  enqueue({ kind, slug, profile = null, items, worker, onComplete = null }) {
    const jobId = `job_${Date.now().toString(36)}_${randomBytes(4).toString("hex")}`;
    const job = {
      jobId,
      kind,
      slug,
      profile: profile || "default",
      status: "queued",
      createdAt: new Date().toISOString(),
      startedAt: null,
      finishedAt: null,
      total: items.length,
      completed: 0,
      failed: 0,
      skipped: 0,
      cancelled: false,
      currentItem: null,
      results: [],
      errors: [],
      summary: null,
    };

    this.jobs.set(jobId, job);
    this.persistJob(job);
    this.pendingQueue.push({ jobId, profile, items, worker, onComplete });

    // Kick the single-worker background pump
    void this.#pump();
    return structuredClone(job);
  }

  async #pump() {
    if (this.runningLoop) return;
    this.runningLoop = true;

    try {
      while (this.pendingQueue.length > 0) {
        const entry = this.pendingQueue.shift();
        const job = this.jobs.get(entry.jobId);
        if (!job || job.cancelled) continue;

        const activeLock = this.lockForProfile(entry.profile);
        const lockResult = activeLock.acquire({ jobId: job.jobId, kind: job.kind, slug: job.slug, profile: entry.profile || "default" });
        if (!lockResult.acquired) {
          job.status = "failed";
          job.finishedAt = new Date().toISOString();
          job.errors.push({
            shotId: null,
            code: "profile_locked",
            retryable: false,
            charged: "no",
            message: `Another Flow client (PID ${lockResult.holder?.pid ?? "unknown"}) is currently using Chrome profile "${entry.profile || "default"}". Wait for it to finish before starting a new job.`,
          });
          this.persistJob(job);
          this.notifyWaiters(job.jobId);
          continue;
        }

        const ac = new AbortController();
        this.activeJobId = job.jobId;
        this.activeAbortController = ac;
        job.status = "running";
        job.startedAt = new Date().toISOString();
        this.persistJob(job);

        try {
          for (let i = 0; i < entry.items.length; i += 1) {
            if (job.cancelled || ac.signal.aborted) {
              job.skipped += entry.items.length - i;
              break;
            }

            if (i > 0) {
              const pauseMs = computeJitteredPauseMs({
                minPauseMs: this.minPauseMs,
                maxPauseMs: this.maxPauseMs,
                random: this.random,
              });
              await sleepWithAbort(pauseMs, ac.signal);
            }

            const item = entry.items[i];
            job.currentItem = item.shotId || item.id || `item_${i + 1}`;
            this.persistJob(job);

            try {
              const res = await entry.worker(item, { signal: ac.signal, index: i, total: entry.items.length });
              job.results.push(res);
              job.completed += 1;
            } catch (err) {
              const errInfo = {
                shotId: item.shotId || item.id || null,
                code: err.code || "worker_error",
                message: err.message,
                retryable: Boolean(err.retryable),
                charged: err.charged || "no",
                nextAction: err.nextAction || "none",
                remediation: err.remediation || null,
              };
              job.errors.push(errInfo);
              job.failed += 1;

              // Fail-Fast on fatal account/session/budget/UI drift errors
              const fatal =
                errInfo.nextAction === "reauth" ||
                errInfo.code === "profile_locked" ||
                errInfo.code === "gflow_not_installed" ||
                [3, 22, 23, 28, 36, 37, 45].includes(err.exitCode);

              if (fatal) {
                job.skipped += entry.items.length - i - 1;
                job.currentItem = null;
                break;
              }
            }

            this.persistJob(job);
          }

          job.currentItem = null;
          if (entry.onComplete) {
            job.summary = await entry.onComplete(job);
          }

          if (job.cancelled) {
            job.status = "cancelled";
          } else if (job.failed > 0 && job.completed === 0) {
            job.status = "failed";
          } else if (job.failed > 0) {
            job.status = "completed_with_errors";
          } else {
            job.status = "completed";
          }
          job.finishedAt = new Date().toISOString();
          this.persistJob(job);
        } catch (err) {
          job.currentItem = null;
          job.status = job.cancelled ? "cancelled" : "failed";
          job.finishedAt = new Date().toISOString();
          job.errors.push({
            shotId: null,
            code: err.code || "queue_error",
            message: err.message,
            retryable: false,
            charged: err.charged || "maybe",
          });
          this.persistJob(job);
        } finally {
          this.activeJobId = null;
          this.activeAbortController = null;
          activeLock.release();
          this.notifyWaiters(job.jobId);
        }
      }
    } finally {
      this.runningLoop = false;
    }
  }

  async waitForJob(jobId, { timeoutMs = 25_000 } = {}) {
    const terminal = new Set(["completed", "completed_with_errors", "failed", "cancelled"]);
    const current = this.getJob(jobId);
    if (!current) {
      return { found: false, jobId, message: `Job "${jobId}" not found.` };
    }
    if (terminal.has(current.status)) {
      return { found: true, timedOut: false, job: current };
    }

    await new Promise((resolve) => {
      let set = this.waiters.get(jobId);
      if (!set) {
        set = new Set();
        this.waiters.set(jobId, set);
      }
      let settled = false;
      const done = () => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        set.delete(done);
        resolve();
      };
      const timer = setTimeout(done, Math.max(50, Number(timeoutMs) || 25_000));
      set.add(done);
    });

    const latest = this.getJob(jobId);
    return {
      found: true,
      timedOut: !terminal.has(latest.status),
      job: latest,
    };
  }

  cancelJob(jobId) {
    const job = this.jobs.get(jobId);
    if (!job) {
      return { ok: false, reason: "not_found", message: `Job "${jobId}" is not active in this process.` };
    }
    if (["completed", "completed_with_errors", "failed", "cancelled"].includes(job.status)) {
      return { ok: false, reason: "already_terminal", status: job.status, job: structuredClone(job) };
    }

    job.cancelled = true;
    // If still queued, remove from pendingQueue immediately
    const idx = this.pendingQueue.findIndex((item) => item.jobId === jobId);
    if (idx >= 0) {
      const [removed] = this.pendingQueue.splice(idx, 1);
      job.skipped = removed.items.length;
      job.status = "cancelled";
      job.finishedAt = new Date().toISOString();
      this.persistJob(job);
      this.notifyWaiters(jobId);
      return { ok: true, status: "cancelled", job: structuredClone(job) };
    }

    if (this.activeJobId === jobId && this.activeAbortController) {
      this.activeAbortController.abort();
    }
    this.persistJob(job);
    return { ok: true, status: "cancelling", job: structuredClone(job) };
  }
}
