// Bring a video the host cleared back from Google Drive (docs/videos/BACKUP.md §還原).
//
// The owner's rule of 2026-11-03: once a video is on YouTube and Drive holds all of it, the host
// keeps nothing of it but a few records (tidy.mjs purge); a later language, a dub asked for again or
// a Short cut from it starts by restoring it. `node tools/video/automation/cli.mjs restore <slug>`
// reads the video's backup.json (the one the purge kept, or Drive's own), copies its folder from
// Drive into a staging folder beside the work directories, checks every file against backup.json's
// SHA-256 and size, and lays each back where the backup took it from (workPathOf, the reverse of
// backup.mjs planFiles). It writes `restored_at` where the tidy reads it, so the next rounds keep the
// files for RESTORE_HOLD_DAYS while the late work is done, and then clear them again the usual way.
// Nothing in Drive is changed. Runs where the backup runs: the video-worker container, with its
// rclone file.
import { createHash } from "node:crypto";
import { createReadStream, existsSync, linkSync, mkdirSync, readFileSync, renameSync, rmSync, statSync } from "node:fs";
import path from "node:path";

import { atomicWrite, isInside, readJson } from "../core/paths.mjs";
import { RESTORE_HOLD_DAYS } from "./tidy.mjs";
import { backupClient, DEFAULT_REMOTE, MANIFEST_FILE, OLD_VERSIONS, rcloneEnvironment, rcloneRunner, REMOTE_ENV, UNPACKAGED_CAPTIONS, UNPACKAGED_DUBS, videoDir } from "./backup.mjs";

export const RESTORE_STAGE = "_restore-stage";
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const SHA256 = /^[0-9a-f]{64}$/;
// Drive keeps these as the work directory had them (backup.mjs FULL_DIRS and FULL_FILES).
const SAME_DIRS = ["clips", "keyframes", "characters", "recordings", "audio", "i18n"];
const SAME_FILES = ["timeline.json", "narration.wav", "approvals.json", "languages.json"];

/**
 * Where a file of the backup goes back in the work directory, relative to it: the reverse of
 * backup.mjs planFiles. Null for a path that is not a file of a backup (backup.json, an old
 * version, anything climbing out).
 */
export function workPathOf(drivePath) {
  const p = String(drivePath);
  if (!p || p.startsWith("/") || p.split("/").some((part) => part === ".." || part === "." || part === "") || p === MANIFEST_FILE || p.startsWith(`${OLD_VERSIONS}/`)) return null;
  const description = /^descriptions\/([A-Za-z0-9-]+)\.txt$/.exec(p);
  if (description) return `upload/description.${description[1]}.txt`;
  const line = /^dub-lines\/([A-Za-z0-9-]+)\/(.+)$/.exec(p);
  if (line) return `dubs/${line[1]}/audio/${line[2]}`;
  if (p.startsWith(`${UNPACKAGED_DUBS}/`)) return `dubs/${p.slice(UNPACKAGED_DUBS.length + 1)}`;
  if (p.startsWith(`${UNPACKAGED_CAPTIONS}/`)) return `captions/${p.slice(UNPACKAGED_CAPTIONS.length + 1)}`;
  if (SAME_DIRS.some((dir) => p.startsWith(`${dir}/`)) || SAME_FILES.includes(p)) return p;
  // The rest is the upload package as package laid it out (final.mp4, metadata.json, captions/,
  // dubs/<locale>.<ext>, thumbnails, a Short's zh-TW.srt, cover.png and titles.json).
  return `upload/${p}`;
}

function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    createReadStream(file).on("error", reject).on("data", (chunk) => hash.update(chunk)).on("end", () => resolve(hash.digest("hex")));
  });
}

async function holds(file, entry) {
  try {
    return statSync(file).size === entry.size && (await sha256File(file)) === entry.sha256;
  } catch {
    return false;
  }
}

const why = (result) => (result.stderr || result.stdout || `exit ${result.code}`).trim().split("\n").slice(-1)[0];

/**
 * Restore `slug` into its work directory. Returns { lines, ok }. `dryRun` reads backup.json and
 * says what would come back, copying nothing. `ctx.backupClient`, `ctx.backupRclone` stand in for
 * the site and rclone in tests.
 */
export async function restoreVideo(ctx, { slug, base, dryRun = false }) {
  const lines = [];
  const say = (line) => lines.push(line);
  if (!SLUG.test(String(slug))) return { lines: [`restore: ${slug} is not a video's name`], ok: false };
  const client = ctx.backupClient ?? backupClient(ctx);
  const config = await client.config();
  if (config.remote_prefix === null || config.remote_prefix === undefined) return { lines: [`restore: the site gives no Drive folder to read from (${config.problem ?? "backups are off"})`], ok: false };
  const workdir = videoDir(base, slug);
  const local = readJson(path.join(workdir, MANIFEST_FILE), null);
  const listed = (config.videos ?? []).find((video) => video?.slug === slug);
  const folder = listed?.folder ?? local?.folder;
  if (typeof folder !== "string" || !folder || folder.split("/").includes("..")) return { lines: [`restore: ${slug} has no Drive folder on the site's list or in its backup.json`], ok: false };
  let rclone = ctx.backupRclone;
  if (!rclone) {
    const environment = rcloneEnvironment(ctx);
    if (environment.problem) return { lines: [`restore: ${environment.problem}`], ok: false };
    rclone = rcloneRunner(environment.env);
  }
  const remote = `${String(ctx.env[REMOTE_ENV] || DEFAULT_REMOTE)}:${[config.remote_prefix, folder].filter(Boolean).join("/")}`;
  const stageRoot = path.join(base, RESTORE_STAGE);
  const stage = path.join(stageRoot, slug);
  if (!isInside(stage, stageRoot) || path.dirname(stage) !== stageRoot) return { lines: [`restore: ${stage} is not a staging folder`], ok: false };
  rmSync(stage, { recursive: true, force: true });
  mkdirSync(stage, { recursive: true });
  try {
    // Drive's backup.json is the list of what it holds; the one kept here may be older.
    const fetched = await rclone(["copyto", `${remote}/${MANIFEST_FILE}`, path.join(stage, MANIFEST_FILE)]);
    const manifest = fetched.code === 0 ? readJson(path.join(stage, MANIFEST_FILE), null) : local;
    if (!manifest?.files?.length) return { lines: [`restore: ${slug}: no backup.json in Drive under ${folder} or here (${why(fetched)})`], ok: false };
    const files = manifest.files.filter((entry) => workPathOf(entry?.path) && SHA256.test(String(entry.sha256)) && Number(entry.size) >= 0);
    const bytes = files.reduce((sum, entry) => sum + Number(entry.size), 0);
    if (dryRun) {
      say(`restore --dry-run: ${slug}: ${files.length} files, ${Math.round(bytes / 1024 ** 2)} MB would come back from Drive (${folder}) into ${workdir}`);
      return { lines, ok: true };
    }
    const copied = await rclone(["copy", remote, path.join(stage, "files"), "--checksum", "--exclude", `/${OLD_VERSIONS}/**`, "--exclude", `/${MANIFEST_FILE}`, "--retries", "5"]);
    if (copied.code !== 0) return { lines: [`restore: ${slug}: rclone copy: ${why(copied)}; nothing was placed`], ok: false };
    const problems = [];
    let placed = 0;
    for (const entry of files) {
      const source = path.join(stage, "files", ...entry.path.split("/"));
      const target = path.join(workdir, ...workPathOf(entry.path).split("/"));
      if (!isInside(target, workdir)) continue;
      if (await holds(target, entry)) continue;
      if (!(await holds(source, entry))) {
        problems.push(entry.path);
        continue;
      }
      mkdirSync(path.dirname(target), { recursive: true });
      rmSync(target, { force: true });
      renameSync(source, target);
      placed += 1;
    }
    // The worker's own video reads its cut at the root too (ARTIFACTS.video).
    const state = path.join(workdir, "auto.json");
    const cut = path.join(workdir, "upload", "final.mp4");
    if (existsSync(state) && existsSync(cut) && !existsSync(path.join(workdir, "final.mp4"))) {
      try {
        linkSync(cut, path.join(workdir, "final.mp4"));
      } catch {
        // A cut that cannot be linked is still in upload/.
      }
    }
    const at = (ctx.now?.() ?? new Date()).toISOString();
    markRestored(workdir, at);
    say(`restore: ${slug}: ${placed} file(s) back from Drive (${folder}), ${files.length - placed - problems.length} already here; kept ${RESTORE_HOLD_DAYS} days before the tidy may clear it again`);
    if (problems.length) say(`restore: ${slug}: ${problems.length} file(s) did not match backup.json and were not placed: ${problems.slice(0, 5).join(", ")}${problems.length > 5 ? ", …" : ""}`);
    return { lines, ok: problems.length === 0 };
  } finally {
    rmSync(stage, { recursive: true, force: true });
  }
}

/**
 * Record the restore where the tidy reads it: auto.json for the worker's own video (its tidy
 * record goes, so the stages see a video with its files), tidied.json for a folder made by hand.
 */
export function markRestored(workdir, at) {
  const auto = path.join(workdir, "auto.json");
  if (existsSync(auto)) {
    const state = JSON.parse(readFileSync(auto, "utf8"));
    const { tidied_at: _at, tidied: _tidied, ...rest } = state;
    atomicWrite(auto, `${JSON.stringify({ ...rest, restored_at: at }, null, 2)}\n`);
    return;
  }
  atomicWrite(path.join(workdir, "tidied.json"), `${JSON.stringify({ restored_at: at }, null, 2)}\n`);
}
