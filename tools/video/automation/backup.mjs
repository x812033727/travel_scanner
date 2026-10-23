// The backup (docs/videos/BACKUP.md): every video on YouTube is copied to the owner's Google
// Drive, under AI/備份/<series>/<episode>/, with rclone, and the tidy keeps a video's files on the
// host until Drive has them. The site holds the settings and each video's folder and tier
// (apps/api/app/video_backup); this file does the copying, once a round, before the tidy.
//
// What goes: the tier's files (planFiles), hashed into backup.json beside the work directory's
// other records. A round copies at most VIDEO_BACKUP_PER_ROUND videos, oldest first, with
// `rclone copy --checksum` into a staging folder's layout, moves any file it would overwrite to
// <episode>/_舊版/<time>/ instead, and never deletes in Drive (copy, never sync). Only once
// `rclone check` finds every staged file in Drive with the same hash is backup.json uploaded and
// the video reported done; the site counts the report against the owner's language choice and
// may answer partial. A file added later (a dub approved after the upload) queues the video again.
//
// Each video's own record is backup-state.json, not auto.json: a lane that saves an older copy of
// auto.json can then never erase it. The tidy reads the round's verdicts (backupGate), so a
// video whose backup is not done, not confirmed by the site, or has new files keeps its files.
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, createReadStream, existsSync, linkSync, lstatSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite, isInside, readJson, resolveWorkBase, stopRequested } from "../core/paths.mjs";
import { USER_AGENT } from "../tts/client.mjs";
import { readCredentials } from "../tts/credentials.mjs";

export const PER_ROUND_ENV = "VIDEO_BACKUP_PER_ROUND";
export const DEFAULT_PER_ROUND = 2;
export const REMOTE_ENV = "VIDEO_BACKUP_REMOTE";
export const DEFAULT_REMOTE = "videobackup";
// The Drive folder the remote's root_folder_id points at, as the site should know it.
export const LOCK_ENV = "VIDEO_BACKUP_LOCK_PATH";
// The host's rclone file, mounted read-only; rclone runs on a private copy in /tmp so a
// refreshed access token can be written back without touching the host's file.
export const CONFIG_ENV = "VIDEO_BACKUP_RCLONE_CONFIG";
export const STATE_FILE = "backup-state.json";
export const MANIFEST_FILE = "backup.json";
// Under the work base, so the tidy (which skips names beginning with "_") never reads it.
export const STAGE_DIR = "_backup-stage";
export const OLD_VERSIONS = "_舊版";
export const QUOTA_MARGIN_BYTES = 2 * 1024 ** 3;
export const MAX_FAILURES = 3;
export const FAILED_RETRY_MS = 6 * 60 * 60 * 1000;
// Reports that only say "queued" or repeat a done the site missed; the token's window is 120 a minute.
export const REPORTS_PER_ROUND = 10;
// The full tier's extra files, beside upload/ (docs/videos/BACKUP.md §每一層備份哪些檔).
export const FULL_DIRS = ["clips", "keyframes", "characters"];
export const FULL_FILES = ["timeline.json", "narration.wav"];
const SERIES_DIR = "_series";
const UPLOAD = "upload";
const DESCRIPTION = /^description\.([A-Za-z0-9-]+)\.txt$/;
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;

export class BackupError extends Error {
  constructor(message, { status = 0, code = "" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

const posix = (relative) => relative.split(path.sep).join("/");
const remoteJoin = (...parts) => parts.filter((part) => part !== null && part !== undefined && part !== "").join("/");

/** Every regular file under `dir`, as [absolute, relative] pairs; links are never followed. */
function walk(dir, fs) {
  const found = [];
  const visit = (current) => {
    let entries;
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0))) {
      const file = path.join(current, entry.name);
      if (entry.isDirectory()) visit(file);
      else if (entry.isFile()) found.push([file, posix(path.relative(dir, file))]);
    }
  };
  visit(dir);
  return found;
}

function isFile(file, fs) {
  try {
    return fs.lstatSync(file).isFile();
  } catch {
    return false;
  }
}

const nodeFs = { copyFileSync, existsSync, linkSync, lstatSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync };

/**
 * The files a tier copies from a work directory, as { source, path } with `path` where it goes
 * under the episode's folder: the whole upload package (description.<locale>.txt into
 * descriptions/<locale>.txt), the work directory's thumbnail.jpg when the package has none, and
 * for the full tier clips/, keyframes/, characters/, timeline.json and narration.wav.
 */
export function planFiles(workdir, tier, fs = nodeFs) {
  const planned = new Map();
  for (const [source, relative] of walk(path.join(workdir, UPLOAD), fs)) {
    const description = relative.match(DESCRIPTION);
    planned.set(description ? `descriptions/${description[1]}.txt` : relative, source);
  }
  const thumbnail = path.join(workdir, "thumbnail.jpg");
  if (!planned.has("thumbnail.jpg") && isFile(thumbnail, fs)) planned.set("thumbnail.jpg", thumbnail);
  if (tier === "full") {
    for (const dir of FULL_DIRS) for (const [source, relative] of walk(path.join(workdir, dir), fs)) planned.set(`${dir}/${relative}`, source);
    for (const name of FULL_FILES) if (isFile(path.join(workdir, name), fs)) planned.set(name, path.join(workdir, name));
  }
  return [...planned.entries()].sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)).map(([where, source]) => ({ source, path: where }));
}

/** A file's sha256, streamed: a final.mp4 is gigabytes. */
export function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    createReadStream(file).on("error", reject).on("data", (chunk) => hash.update(chunk)).on("end", () => resolve(hash.digest("hex")));
  });
}

/**
 * The plan with each file's size and sha256. A file whose size and modification time match the
 * last backup's entry keeps that hash, so a round over many finished videos reads only what
 * changed.
 */
export async function hashPlan(plan, previous, { fs = nodeFs, hash = sha256File } = {}) {
  const known = new Map((previous?.files ?? []).map((entry) => [entry.path, entry]));
  const entries = [];
  for (const item of plan) {
    const stat = fs.statSync(item.source);
    const before = known.get(item.path);
    const mtime = Math.round(stat.mtimeMs);
    const sha256 = before && before.size === stat.size && before.mtime_ms === mtime && before.sha256 ? before.sha256 : await hash(item.source);
    entries.push({ ...item, size: stat.size, mtime_ms: mtime, sha256 });
  }
  return entries;
}

/** What Drive holds after copying `entries`: the last backup's files, those here replacing theirs. */
export function mergedFiles(entries, previous) {
  const merged = new Map((previous?.files ?? []).map((entry) => [entry.path, { path: entry.path, size: entry.size, mtime_ms: entry.mtime_ms, sha256: entry.sha256 }]));
  for (const entry of entries) merged.set(entry.path, { path: entry.path, size: entry.size, mtime_ms: entry.mtime_ms, sha256: entry.sha256 });
  return [...merged.values()].sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
}

/** The files here that Drive does not have as they are: new ones, or changed since the last backup. */
export function changedFiles(entries, previous) {
  const known = new Map((previous?.files ?? []).map((entry) => [entry.path, entry.sha256]));
  return entries.filter((entry) => known.get(entry.path) !== entry.sha256);
}

/** One hash for a backup's whole file list, the one the site keeps. */
export function filesHash(files) {
  const hash = createHash("sha256");
  for (const file of [...files].sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0))) hash.update(`${file.path}\t${file.sha256}\n`);
  return hash.digest("hex");
}

const LOCALE = /^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$/;
const localesBy = (paths, pattern) => [...new Set(paths.map((item) => item.match(pattern)?.[1]).filter((locale) => locale && LOCALE.test(locale)))].sort();
const keysOf = (value) => (value && typeof value === "object" && !Array.isArray(value) ? Object.keys(value).filter((locale) => LOCALE.test(locale)).sort() : []);

/**
 * What a backup holds, by kind, for the site's count (apps/api/app/video_backup/target.py
 * missing_files): the package's own files, each language's description, captions and dub track,
 * and the parts the package skipped with a reason (metadata.json's skipped_*_locales).
 */
export function contentsOf(paths, metadata = null) {
  const captions = localesBy(paths, /^captions\/([^/]+)\.srt$/);
  // A Short's package keeps its one caption file beside the cut: zh-TW.srt.
  for (const locale of localesBy(paths, /^([^/]+)\.srt$/)) if (!captions.includes(locale)) captions.push(locale);
  return {
    final: paths.includes("final.mp4"),
    metadata: paths.includes("metadata.json"),
    thumbnail: paths.includes("thumbnail.jpg"),
    descriptions: localesBy(paths, /^descriptions\/([^/]+)\.txt$/),
    captions: captions.sort(),
    dubs: localesBy(paths, /^dubs\/([^/.]+)\.[A-Za-z0-9]+$/),
    skipped: { descriptions: [], captions: keysOf(metadata?.skipped_caption_locales), dubs: keysOf(metadata?.skipped_dub_locales) },
    clips: paths.filter((item) => item.startsWith("clips/") && item !== "clips/manifest.json").length,
    keyframes: paths.filter((item) => item.startsWith("keyframes/") && item !== "keyframes/manifest.json").length,
  };
}

export const readBackupState = (workdir) => readJson(path.join(workdir, STATE_FILE), null);
const saveBackupState = (workdir, state) => atomicWrite(path.join(workdir, STATE_FILE), `${JSON.stringify(state, null, 2)}\n`);

/** The site's backup routes, through the web container like the other automation calls. */
export function backupClient(ctx) {
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) throw new BackupError("no video tool token yet: run `node tools/video/cli.mjs login`", { code: "video_tool_token_invalid" });
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  async function call(method, route, json) {
    let response;
    try {
      response = await fetchImpl(`${site}/api/video/automation/backup/${route}`, {
        method,
        headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW", ...(json ? { "Content-Type": "application/json" } : {}) },
        body: json ? JSON.stringify(json) : undefined,
      });
    } catch (error) {
      throw new BackupError(`cannot reach ${site}: ${error.message}`, { code: "network" });
    }
    if (response.ok) return response.json();
    let problem = {};
    try {
      problem = await response.json();
    } catch {
      problem = {};
    }
    throw new BackupError(problem.detail || `HTTP ${response.status}`, { status: response.status, code: problem.code ?? "" });
  }
  return {
    config: () => call("GET", "config"),
    lock: (body) => call("POST", "lock", body),
    answer: (id, body) => call("POST", `test/${id}`, body),
    report: (slug, body) => call("POST", `${slug}/report`, body),
  };
}

/** rclone as a child process: { code, stdout, stderr }, never a throw. Output is capped. */
export function rcloneRunner(env) {
  const cap = 64 * 1024;
  return (args) =>
    new Promise((resolve) => {
      let stdout = "";
      let stderr = "";
      let child;
      try {
        child = spawn("rclone", args, { env, stdio: ["ignore", "pipe", "pipe"] });
      } catch (error) {
        resolve({ code: -1, stdout: "", stderr: error.message });
        return;
      }
      child.stdout.on("data", (chunk) => {
        if (stdout.length < cap) stdout += chunk;
      });
      child.stderr.on("data", (chunk) => {
        if (stderr.length < cap) stderr += chunk;
      });
      child.on("error", (error) => resolve({ code: -1, stdout, stderr: `${stderr}${error.message}` }));
      child.on("close", (code) => resolve({ code: code ?? -1, stdout, stderr }));
    });
}

/** The last useful line rclone printed, for a report a person reads. */
const why = (result) => (result.stderr || result.stdout).trim().split("\n").filter(Boolean).slice(-1)[0]?.slice(0, 300) || `exit ${result.code}`;

/**
 * The host's rclone file copied to a private one rclone may write (a refreshed token), and the
 * environment rclone runs with: { env } or { problem } when the host has none.
 */
export function rcloneEnvironment(ctx, fs = nodeFs) {
  const mounted = ctx.env[CONFIG_ENV];
  if (!mounted || !fs.existsSync(mounted)) return { problem: `主機沒有影片備份用的 rclone 設定（${mounted || CONFIG_ENV} 未設定）` };
  const lock = String(ctx.env[LOCK_ENV] ?? "").trim();
  if (!lock) return { problem: `video-worker 沒有設定 ${LOCK_ENV}（rclone root_folder_id 對應的雲端路徑）` };
  const copy = path.join(ctx.env.TMPDIR || "/tmp", "rclone-videos.conf");
  try {
    fs.copyFileSync(mounted, copy);
  } catch (error) {
    return { problem: `讀不到 ${mounted}（${error.code ?? error.message}）；檔案要讓容器的 pwuser 讀得到` };
  }
  return { env: { ...ctx.env, RCLONE_CONFIG: copy }, lock: drivePath(lock) };
}

/**
 * A Drive path as the site stores it (apps/api/app/video_backup/target.py normalise_path): no
 * drive letter, no 我的雲端硬碟 or My Drive, slashes, none at either end.
 */
export function drivePath(value) {
  const parts = String(value ?? "").normalize("NFC").trim().replace(/\\/g, "/").replace(/^[A-Za-z]:/, "").split("/").filter(Boolean);
  if (parts.length && ["我的雲端硬碟", "my drive"].includes(parts[0].toLowerCase())) parts.shift();
  return parts.join("/");
}

/** `path` under the remote's root, which is the lock; null outside it (the site's remote_prefix rule). */
export function prefixUnder(wantedPath, lock) {
  const wanted = drivePath(wantedPath);
  const root = drivePath(lock);
  if (!root) return null;
  if (wanted === root) return "";
  return wanted.startsWith(`${root}/`) ? wanted.slice(root.length + 1) : null;
}

/**
 * The staging folder: the episode's layout as hard links to the work files (a copy where a link
 * cannot be made), so one `rclone copy` puts every file where it goes. Removed after the copy.
 */
function buildStage(base, slug, plan, fs) {
  const root = path.join(base, STAGE_DIR);
  const stage = path.join(root, slug);
  if (!isInside(stage, root) || path.dirname(stage) !== root) throw new BackupError(`${stage} is not a staging folder`);
  fs.rmSync(stage, { recursive: true, force: true });
  fs.mkdirSync(stage, { recursive: true });
  for (const item of plan) {
    const target = path.join(stage, ...item.path.split("/"));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    try {
      fs.linkSync(item.source, target);
    } catch {
      fs.copyFileSync(item.source, target);
    }
  }
  return stage;
}

function removeStage(base, slug, fs) {
  const root = path.join(base, STAGE_DIR);
  fs.rmSync(path.join(root, slug), { recursive: true, force: true });
}

const stamp = (date) => date.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");

/** The copy, then the check, of one local folder into one Drive folder; null, or why it failed. */
async function copyChecked(job, local, remote, ts) {
  const filters = ["--exclude", `/${OLD_VERSIONS}/**`, "--exclude", `/${MANIFEST_FILE}`];
  const copy = await job.rclone(["copy", local, remote, "--checksum", "--drive-chunk-size", "64M", "--tpslimit", "5", "--retries", "5", "--backup-dir", `${remote}/${OLD_VERSIONS}/${ts}`, ...filters]);
  if (copy.code !== 0) return `rclone copy: ${why(copy)}`;
  // Hashes on both sides (Drive keeps an md5 of every file), so nothing is downloaded.
  const check = await job.rclone(["check", local, remote, "--one-way", ...filters]);
  if (check.code !== 0) return `rclone check: ${why(check)}`;
  return null;
}

async function freeBytes(job) {
  const about = await job.rclone(["about", `${job.remote}:`, "--json"]);
  if (about.code !== 0) return { problem: `rclone about: ${why(about)}` };
  try {
    const read = JSON.parse(about.stdout);
    return { free: Number.isFinite(read.free) ? read.free : null, total: Number.isFinite(read.total) ? read.total : null };
  } catch {
    return { free: null, total: null };
  }
}

async function tellSite(job, slug, body) {
  try {
    return await job.client.report(slug, body);
  } catch (error) {
    job.lines.push(`backup: ${slug}: the site did not take the report (${error.message}); it is sent again next round`);
    return null;
  }
}

/** A failed attempt: pending again, or failed after MAX_FAILURES in a row, retried every six hours. */
async function failed(job, video, state, error) {
  const attempts = (state.attempts ?? 0) + 1;
  const next = { ...state, state: attempts >= MAX_FAILURES ? "failed" : "pending", attempts, error, last_attempt_at: job.now.toISOString() };
  saveBackupState(job.workdir(video.slug), next);
  await tellSite(job, video.slug, { state: next.state, folder: video.folder, tier: video.tier, attempts, error });
  job.lines.push(`backup: ${video.slug}: ${next.state === "failed" ? `failed ${attempts} times; tried again in six hours` : `attempt ${attempts} failed`}: ${error}`);
  return next;
}

/** Copy one video to Drive and report it; the new state. */
async function backUp(job, video, state) {
  const workdir = job.workdir(video.slug);
  const previous = readJson(path.join(workdir, MANIFEST_FILE), null);
  const plan = planFiles(workdir, video.tier, job.fs);
  if (!plan.length && !previous?.files?.length) return failed(job, video, state, `${workdir} has no upload package to back up`);
  let entries;
  try {
    entries = await hashPlan(plan, previous, { fs: job.fs, hash: job.hash });
  } catch (error) {
    return failed(job, video, state, `a file could not be read (${error.code ?? error.message})`);
  }
  const needed = changedFiles(entries, previous).reduce((sum, entry) => sum + entry.size, 0);
  const space = await freeBytes(job);
  if (space.problem) return failed(job, video, state, space.problem);
  if (space.free !== null && space.free < needed + QUOTA_MARGIN_BYTES) {
    const error = `雲端硬碟剩 ${Math.floor(space.free / 1024 ** 2)} MB，這次要傳 ${Math.ceil(needed / 1024 ** 2)} MB，另外要留 2 GB`;
    const next = { ...state, state: "blocked_quota", error, last_attempt_at: job.now.toISOString() };
    saveBackupState(workdir, next);
    await tellSite(job, video.slug, { state: "blocked_quota", folder: video.folder, tier: video.tier, error, free_bytes: space.free, ...(space.total !== null ? { total_bytes: space.total } : {}) });
    job.lines.push(`backup: ${video.slug}: waiting for space: ${error}`);
    return next;
  }
  const destination = `${job.remote}:${remoteJoin(job.prefix, video.folder)}`;
  const ts = stamp(job.now);
  let problem = null;
  try {
    const stage = buildStage(job.base, video.slug, entries, job.fs);
    problem = await copyChecked(job, stage, destination, ts);
    // A series' approved character sheets, once in its shared folder, for the full tier.
    const shared = video.series_slug ? path.join(job.base, SERIES_DIR, video.series_slug, "characters") : null;
    if (!problem && video.tier === "full" && shared && job.fs.existsSync(shared)) {
      problem = await copyChecked(job, shared, `${job.remote}:${remoteJoin(job.prefix, video.shared_folder, "characters")}`, ts);
    }
  } catch (error) {
    problem = `the staging folder could not be built (${error.code ?? error.message})`;
  } finally {
    try {
      removeStage(job.base, video.slug, job.fs);
    } catch {
      // A staging folder left behind is rebuilt from scratch next time.
    }
  }
  if (problem) return failed(job, video, state, problem);
  const files = mergedFiles(entries, previous);
  const hash = filesHash(files);
  const manifest = { slug: video.slug, youtube_video_id: video.youtube_video_id, series: video.series_key, folder: video.folder, tier: video.tier, files_hash: hash, files, backed_up_at: job.now.toISOString() };
  const manifestFile = path.join(workdir, MANIFEST_FILE);
  atomicWrite(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
  const uploaded = await job.rclone(["copyto", manifestFile, `${destination}/${MANIFEST_FILE}`, "--checksum"]);
  if (uploaded.code !== 0) return failed(job, video, state, `backup.json: rclone copyto: ${why(uploaded)}`);
  const bytes = files.reduce((sum, entry) => sum + entry.size, 0);
  const next = { ...state, state: "done", folder: video.folder, tier: video.tier, files_hash: hash, bytes, files: files.length, at: job.now.toISOString(), attempts: 0, error: null, site_state: null, missing: [] };
  saveBackupState(workdir, next);
  job.lines.push(`backup: ${video.slug}: ${files.length} files, ${Math.round(bytes / 1024 ** 2)} MB, checked in Drive under ${remoteJoin(job.prefix, video.folder)}`);
  return confirm(job, video, next);
}

/** Tell the site a backup is done; it may answer partial, with what is missing. */
async function confirm(job, video, state) {
  const metadata = readJson(path.join(job.workdir(video.slug), UPLOAD, "metadata.json"), null);
  const manifest = readJson(path.join(job.workdir(video.slug), MANIFEST_FILE), null);
  const paths = (manifest?.files ?? []).map((entry) => entry.path);
  const answer = await tellSite(job, video.slug, {
    state: "done", folder: video.folder, tier: state.tier, bytes: state.bytes, files: state.files, files_hash: state.files_hash, contents: contentsOf(paths, metadata),
  });
  if (!answer) return state;
  const next = { ...state, site_state: answer.state, missing: Array.isArray(answer.missing) ? answer.missing : [] };
  saveBackupState(job.workdir(video.slug), next);
  if (answer.state !== "done") job.lines.push(`backup: ${video.slug}: the site reads it ${answer.state}${next.missing.length ? `, missing ${next.missing.join(", ")}` : ""}; the tidy keeps its files`);
  return next;
}

/** Whether a done backup still covers the work files: the new or changed ones, by the cached hashes. */
async function stillCovered(job, video) {
  const workdir = job.workdir(video.slug);
  const previous = readJson(path.join(workdir, MANIFEST_FILE), null);
  if (!previous) return { covered: false, why: "no backup.json" };
  try {
    const entries = await hashPlan(planFiles(workdir, video.tier, job.fs), previous, { fs: job.fs, hash: job.hash });
    const changed = changedFiles(entries, previous);
    return changed.length ? { covered: false, why: `${changed.length} new or changed file${changed.length === 1 ? "" : "s"} (${changed.slice(0, 3).map((entry) => entry.path).join(", ")})` } : { covered: true };
  } catch (error) {
    return { covered: false, why: `a file could not be read (${error.code ?? error.message})` };
  }
}

function isDue(state, now) {
  if (state.state === "pending" || state.state === "blocked_quota") return true;
  if (state.state !== "failed") return false;
  const last = Date.parse(String(state.last_attempt_at ?? ""));
  return !Number.isFinite(last) || now.getTime() - last >= FAILED_RETRY_MS;
}

/** Answer the owner's test from the card: write and delete a probe file, and read the free space. */
async function answerTest(job, config, rclone) {
  const test = config.test;
  if (!test?.id) return;
  let answer;
  if (rclone.problem) answer = { ok: false, message: rclone.problem };
  else {
    const prefix = prefixUnder(config.path, rclone.lock);
    if (prefix === null) answer = { ok: false, message: `${config.path} 不在主機鎖定的 ${rclone.lock} 之內` };
    else {
      const name = `_probe-${stamp(job.now)}.txt`;
      const local = path.join(job.env.TMPDIR || "/tmp", name);
      job.fs.writeFileSync(local, `Mokaair video backup probe ${job.now.toISOString()}\n`);
      const target = `${job.remote}:${remoteJoin(prefix, name)}`;
      const wrote = await job.rclone(["copyto", local, target]);
      const removed = wrote.code === 0 ? await job.rclone(["deletefile", target]) : null;
      job.fs.rmSync(local, { force: true });
      const space = await freeBytes(job);
      const sizes = space.problem ? {} : { ...(space.free !== null ? { free_bytes: space.free } : {}), ...(space.total !== null ? { total_bytes: space.total } : {}) };
      if (wrote.code !== 0) answer = { ok: false, message: `寫入 ${remoteJoin(rclone.lock, prefix, name)} 失敗：${why(wrote)}`, ...sizes };
      else if (removed.code !== 0) answer = { ok: false, message: `寫入成功，刪除測試檔失敗：${why(removed)}`, ...sizes };
      else answer = { ok: true, message: `已在 ${remoteJoin(rclone.lock, prefix) || "/"} 寫入並刪除測試檔`, ...sizes };
    }
  }
  try {
    await job.client.answer(test.id, answer);
    job.lines.push(`backup: answered the owner's test: ${answer.ok ? "ok" : answer.message}`);
  } catch (error) {
    job.lines.push(`backup: the test could not be answered (${error.message})`);
  }
}

/**
 * One round of the backup, then what the tidy may do: { lines, gate }. `gate` is { enabled:
 * false } when backups are off (the tidy works as before), { unknown } when the round could not
 * tell (the tidy keeps every video on YouTube), or { enabled: true, verdicts } with each video's
 * { ok, why }. `copy: false` only judges, for the hand-run tidy. Never throws.
 */
export async function backupRound(ctx, { copy = true, client: given, rclone: runner, hash } = {}) {
  const lines = [];
  let base;
  try {
    base = resolveWorkBase({ env: ctx.env, root: ctx.root, home: ctx.home });
  } catch (error) {
    return { lines: [`backup: not run: ${error.message}`], gate: { unknown: error.message } };
  }
  if (stopRequested(base)) return { lines: copy ? ["backup: STOP found; nothing is copied"] : [], gate: { unknown: "a STOP file is in the work base" } };
  let client;
  let config;
  try {
    client = given ?? backupClient(ctx);
    config = await client.config();
  } catch (error) {
    // A site from before the backup (no such route) is a site with backups off: the tidy as before.
    if (error instanceof BackupError && error.status === 404 && !String(error.code).startsWith("video_backup")) return { lines: [], gate: { enabled: false } };
    return { lines: [`backup: the site's backup settings could not be read (${error.message})`], gate: { unknown: `the backup settings could not be read (${error.message})` } };
  }
  const fs = ctx.backupFs ?? nodeFs;
  const rclone = rcloneEnvironment(ctx, fs);
  const job = {
    base, client, fs, lines, hash, env: ctx.env,
    now: ctx.now(),
    remote: String(ctx.env[REMOTE_ENV] || DEFAULT_REMOTE),
    rclone: runner ?? (rclone.env ? rcloneRunner(rclone.env) : async () => ({ code: -1, stdout: "", stderr: rclone.problem })),
    workdir: (slug) => path.join(base, slug),
    prefix: null,
  };
  if (copy) {
    // The lock this worker runs with, whenever the site knows another (or none).
    const lock = rclone.problem ? null : rclone.lock;
    if (config.lock_path !== lock || lock === null) {
      try {
        await client.lock({ lock_path: lock, ...(rclone.problem ? { problem: rclone.problem } : {}) });
        config = await client.config();
      } catch (error) {
        lines.push(`backup: the lock path could not be reported (${error.message})`);
      }
    }
    await answerTest(job, config, rclone);
  }
  if (!config.enabled) return { lines, gate: { enabled: false } };
  if (config.remote_prefix === null || config.remote_prefix === undefined || rclone.problem) {
    const problem = rclone.problem ?? config.problem ?? "the site gave no folder to copy to";
    if (copy) lines.push(`backup: not copying: ${problem}; the tidy keeps every video on YouTube`);
    return { lines, gate: { unknown: problem } };
  }
  job.prefix = config.remote_prefix;
  const perRound = Number.parseInt(ctx.env[PER_ROUND_ENV] ?? "", 10);
  const limit = Number.isInteger(perRound) && perRound >= 0 ? perRound : DEFAULT_PER_ROUND;
  const verdicts = new Map();
  const queue = [];
  let reports = 0;
  for (const video of config.videos ?? []) {
    // The site's own slug pattern; anything else is never joined onto the work base.
    if (typeof video?.slug !== "string" || !SLUG.test(video.slug)) continue;
    const workdir = job.workdir(video.slug);
    if (!fs.existsSync(path.join(workdir, "auto.json"))) continue;
    if (video.tier === "off") {
      verdicts.set(video.slug, { ok: true, why: "its series is set not to be backed up" });
      continue;
    }
    let state = readBackupState(workdir);
    if (!state || typeof state !== "object") {
      state = { state: "pending", queued_at: job.now.toISOString(), attempts: 0 };
      if (copy) {
        saveBackupState(workdir, state);
        if (reports++ < REPORTS_PER_ROUND) await tellSite(job, video.slug, { state: "pending", folder: video.folder, tier: video.tier });
      }
    } else if (state.state === "done" || state.state === "partial") {
      const covered = await stillCovered(job, video);
      if (!covered.covered) {
        state = { ...state, state: "pending", queued_at: job.now.toISOString(), requeued: covered.why };
        if (copy) {
          saveBackupState(workdir, state);
          if (reports++ < REPORTS_PER_ROUND) await tellSite(job, video.slug, { state: "pending", folder: video.folder, tier: video.tier });
          lines.push(`backup: ${video.slug}: queued again: ${covered.why}`);
        }
      } else if (state.site_state === null || state.site_state === undefined) {
        if (copy && reports++ < REPORTS_PER_ROUND) state = await confirm(job, video, state);
      }
    }
    if (copy && isDue(state, job.now) && queue.length < limit) queue.push([video, state]);
    verdicts.set(video.slug, verdictOf(state));
  }
  for (const [video, state] of queue) {
    const next = await backUp(job, video, state);
    verdicts.set(video.slug, verdictOf(next));
  }
  return { lines, gate: { enabled: true, verdicts } };
}

/** Whether the tidy may clear a video, from its backup state. */
export function verdictOf(state) {
  if (state?.state === "done" && state.site_state === "done") return { ok: true, why: "in Drive" };
  if (state?.state === "partial" || (state?.state === "done" && state.site_state)) {
    return { ok: false, why: `backup ${state.site_state ?? "partial"}${state.missing?.length ? `: missing ${state.missing.slice(0, 3).join(", ")}` : ""}` };
  }
  if (state?.state === "done") return { ok: false, why: "backup done, not yet confirmed by the site" };
  if (state?.state === "blocked_quota") return { ok: false, why: "backup waiting for Drive space" };
  if (state?.state === "failed") return { ok: false, why: `backup failed: ${state.error ?? "see the log"}` };
  return { ok: false, why: "backup pending" };
}
