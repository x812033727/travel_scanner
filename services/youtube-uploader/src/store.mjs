import { DatabaseSync } from "node:sqlite";
import { mkdirSync, statSync, openSync, closeSync, writeSync, fsyncSync, unlinkSync, createReadStream } from "node:fs";
import { createHash } from "node:crypto";
import path from "node:path";
import { ACTIVE, CHUNK, HASH, Refused, hash, jobSteps } from "./contract.mjs";

export async function fileHash(file) {
  const digest = createHash("sha256");
  for await (const bytes of createReadStream(file)) digest.update(bytes);
  return digest.digest("hex");
}
/** One SQLite lock lives on a separate connection for the lifetime of the service. */
export class Store {
  constructor(directory) {
    this.directory = path.resolve(directory);
    mkdirSync(this.directory, { recursive: true, mode: 0o700 });
    this.lock = new DatabaseSync(path.join(this.directory, "service-lock.db"));
    try { this.lock.exec("BEGIN EXCLUSIVE"); } catch { this.lock.close(); throw new Refused("service_already_running"); }
    this.db = new DatabaseSync(path.join(this.directory, "jobs.db"));
    this.db.exec("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, slug TEXT NOT NULL, created TEXT NOT NULL, document TEXT NOT NULL)");
    this.uploads = new Set();
    for (const job of this.all()) {
      if (job.state === "running") this.patch(job.id, { state: "needs_action", code: "interrupted" });
    }
  }
  close() { this.db.close(); this.lock.close(); }
  all() { return this.db.prepare("SELECT document FROM jobs ORDER BY created, id").all().map((r) => JSON.parse(r.document)); }
  get(id) {
    if (!HASH.test(id)) throw new Refused("job_not_found", 404);
    const row = this.db.prepare("SELECT document FROM jobs WHERE id = ?").get(id);
    if (!row) throw new Refused("job_not_found", 404);
    return JSON.parse(row.document);
  }
  latest(slug) { return this.all().filter((j) => j.manifest.slug === slug).at(-1) ?? null; }
  save(job) {
    this.db.prepare("INSERT INTO jobs VALUES (?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET document=excluded.document")
      .run(job.id, job.manifest.slug, job.created_at, JSON.stringify(job));
    return job;
  }
  patch(id, fields) { return this.save({ ...this.get(id), ...fields, updated_at: new Date().toISOString() }); }
  create(id, manifest) {
    if (!HASH.test(id)) throw new Refused("invalid_job", 422);
    const same = this.all().find((j) => j.id === id);
    if (same) {
      if (same.fingerprint !== hash(JSON.stringify(manifest))) throw new Refused("request_changed");
      return same;
    }
    const previous = this.latest(manifest.slug);
    if (previous && ACTIVE.has(previous.state)) throw new Refused("project_busy");
    if (previous?.video_id && manifest.video_id !== previous.video_id) throw new Refused("existing_video_required");
    const now = new Date().toISOString();
    mkdirSync(path.join(this.directory, id), { mode: 0o700 });
    return this.save({ id, manifest, fingerprint: hash(JSON.stringify(manifest)), state: "staging", code: null,
      video_id: manifest.video_id, upload_started: false, completed: [], steps: jobSteps(manifest), created_at: now, updated_at: now });
  }
  file(job, sha) {
    const file = job.manifest.files.find((f) => f.sha256 === sha);
    if (!HASH.test(sha) || !file) throw new Refused("file_not_found", 404);
    return path.join(this.directory, job.id, sha);
  }
  received(job, sha) {
    try { return statSync(this.file(job, sha)).size; } catch (e) { if (e.code === "ENOENT") return 0; throw e; }
  }
  view(job) {
    return { id: job.id, slug: job.manifest.slug, channel_id: job.manifest.channel_id, review_sha256: job.manifest.review_sha256,
      state: job.state, code: job.code, video_id: job.video_id, upload_started: job.upload_started,
      steps: job.steps.map((id) => ({ id, done: job.completed.includes(id) })), updated_at: job.updated_at,
      files: job.manifest.files.map((f) => ({ ...f, received: this.received(job, f.sha256) })) };
  }
  async put(id, sha, offset, bytes) {
    const key = id + sha;
    if (this.uploads.has(key) || this.uploads.has(id)) throw new Refused("file_busy");
    this.uploads.add(key);
    try {
      const job = this.get(id);
      if (job.state !== "staging") throw new Refused("not_staging");
      const file = job.manifest.files.find((f) => f.sha256 === sha);
      const target = this.file(job, sha);
      if (!Number.isSafeInteger(offset) || offset !== this.received(job, sha)) throw new Refused("offset_changed");
      if (!bytes.length || bytes.length > CHUNK || offset + bytes.length > file.size) throw new Refused("invalid_chunk", 422);
      const fd = openSync(target, "a", 0o600);
      try { let written = 0; while (written < bytes.length) written += writeSync(fd, bytes, written); fsyncSync(fd); }
      finally { closeSync(fd); }
      if (offset + bytes.length === file.size && await fileHash(target) !== sha) {
        unlinkSync(target);
        throw new Refused("file_hash_mismatch", 422);
      }
      return this.view(job);
    } finally { this.uploads.delete(key); }
  }
  async queue(id) {
    if ([...this.uploads].some((key) => key.startsWith(id))) throw new Refused("file_busy");
    this.uploads.add(id);
    try {
    const job = this.get(id);
    if (job.state !== "staging") return this.view(job);
    for (const f of job.manifest.files) {
      if (this.received(job, f.sha256) !== f.size || await fileHash(this.file(job, f.sha256)) !== f.sha256) throw new Refused("files_incomplete");
    }
    return this.view(this.patch(id, { state: "queued", code: null }));
    } finally { this.uploads.delete(id); }
  }
  resume(id, videoId) {
    const job = this.get(id);
    if (!["needs_action", "cancelled"].includes(job.state)) throw new Refused("not_paused");
    if (job.video_id && videoId && videoId !== job.video_id) throw new Refused("video_changed");
    if (job.upload_started && !job.video_id && !videoId) throw new Refused("video_id_required");
    return this.view(this.patch(id, { state: job.state === "cancelled" ? "staging" : "queued", code: null, video_id: job.video_id || videoId || null }));
  }
  cancel(id) {
    if ([...this.uploads].some((key) => key.startsWith(id))) throw new Refused("file_busy");
    const job = this.get(id);
    if (!["staging", "queued", "needs_action"].includes(job.state)) throw new Refused("cannot_cancel");
    // Preserve uncertain uploads: cancelling never grants permission to upload another copy.
    if (job.upload_started && !job.video_id) throw new Refused("video_id_required");
    return this.view(this.patch(id, { state: "cancelled", code: null }));
  }
}
