// The branch mirror (docs/videos/BACKUP.md §AI 劇的分支鏡像): the AI dramas made in cloud sessions
// are backed up to GitHub as `transfer/*` branches (docs/videos/drama/BACKUP-BRANCHES.md), and the
// owner asked on 2026-11-08 that Drive hold the same: 「備份到雲端的內容應該也要跟備份到分支的一樣」.
// The review store cannot carry them (120 clips, 40 build files, no sub-paths, 20 GB in all), so
// the worker mirrors the branches themselves, once a round after the backup (cli.mjs).
//
// For each remote branch under the configured prefixes whose head is not the commit last mirrored
// (branch-mirror.json in <work base>/_branch-mirror/): a shallow fetch of that one commit into a
// throwaway bare repository, its tree written out to a staging folder (links as plain files), the
// repository removed again, every `X.part00`, `X.part01`… joined back into `X` (checked against the
// sha256 in an `X.SPLIT` note when the branch has one), then `rclone sync --checksum` into
// AI/備份/drama/<series>/_分支/<branch>/ with `--backup-dir` <that folder>/_舊版/<time>/, so a file
// the new commit changed or deleted is moved there, never deleted, and `rclone check` both ways.
// Only a check with no differences records the commit as mirrored; anything else is tried again
// next round (after MAX_FAILURES failures, once every FAILED_RETRY_MS).
//
// Bounded: one branch at a time, the staging folder cleared after each, at most PER_ROUND_ENV
// branches and MAX_GB_ENV gigabytes a round, and none while the work base has less than
// MIN_FREE_GB_ENV free, so the first run over every existing branch is spread over many rounds.
// On when SWITCH_ENV is "on", as the production compose file sets it. The repository is public, so
// git fetches anonymously over HTTPS and the host needs nothing (a token, TOKEN_ENV or
// TOKEN_FILE_ENV, is only a fallback). The site has no row for a branch yet, so the result is in
// the state file and the worker's log (task 2026-11-08-backup-card-shows-branch-mirror).
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { createReadStream, createWriteStream, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statfsSync, statSync } from "node:fs";
import path from "node:path";
import { pipeline } from "node:stream/promises";

import { atomicWrite, resolveWorkBase, stopRequested } from "../core/paths.mjs";
import { backupClient, DEFAULT_REMOTE, OLD_VERSIONS, rcloneEnvironment, rcloneRunner, REMOTE_ENV } from "./backup.mjs";

export const SWITCH_ENV = "VIDEO_BRANCH_MIRROR";
export const PREFIXES_ENV = "VIDEO_BRANCH_MIRROR_PREFIXES";
export const DEFAULT_PREFIXES = ["transfer/zt-", "transfer/tn-"];
export const REPO_ENV = "VIDEO_BRANCH_MIRROR_REPO";
export const DEFAULT_REPO = "x812033727/travel_scanner";
// The repository is public: no key and no token. A token is only a fallback, as a value or a file.
export const TOKEN_ENV = "VIDEO_BRANCH_MIRROR_TOKEN";
export const TOKEN_FILE_ENV = "VIDEO_BRANCH_MIRROR_TOKEN_FILE";
export const PER_ROUND_ENV = "VIDEO_BRANCH_MIRROR_PER_ROUND";
export const DEFAULT_PER_ROUND = 1;
export const MAX_GB_ENV = "VIDEO_BRANCH_MIRROR_MAX_GB";
export const DEFAULT_MAX_GB = 2;
export const MIN_FREE_GB_ENV = "VIDEO_BRANCH_MIRROR_MIN_FREE_GB";
// The largest branch is about 1.8 GB; while one is written out its pack and its tree are both on disk.
export const DEFAULT_MIN_FREE_GB = 5;
// Under the work base, beginning with "_" so the tidy never reads it.
export const MIRROR_DIR = "_branch-mirror";
export const STATE_FILE = "branch-mirror.json";
export const BRANCHES_DIR = "_分支";
export const SERIES_DIRS = { zt: "zhong-tian-qu-qi", tn: "tai-nainai" };
export const OTHER_SERIES = "_其他";
export const MAX_FAILURES = 3;
export const FAILED_RETRY_MS = 6 * 60 * 60 * 1000;
const PART = /^(.+)\.part(\d{2,})$/;
const SPLIT_NOTE = ".SPLIT";
const SHA256 = /\b[0-9a-f]{64}\b/i;
const BRANCH = /^[A-Za-z0-9][A-Za-z0-9._-]*(?:\/[A-Za-z0-9][A-Za-z0-9._-]*)*$/;
const SHORT = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
const COMMIT = /^[0-9a-f]{40}(?:[0-9a-f]{24})?$/;
const GB = 1024 ** 3;

const nodeFs = { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statfsSync, statSync };

// docker-compose.prod.yml sets it "on" for the video worker (owner, 2026-11-08: the mirror runs once
// deployed, nobody opens a shell on the host); anything else, or unset (a hand run, the tests), is off.
export const mirrorOn = (env = {}) => String(env[SWITCH_ENV] ?? "").trim().toLowerCase() === "on";

/** The configured prefixes: a comma-separated list, each under refs/heads/; the default without one. */
export function prefixesFrom(env = {}) {
  const given = String(env[PREFIXES_ENV] ?? "").split(",").map((value) => value.trim()).filter(Boolean);
  return given.length ? given : DEFAULT_PREFIXES;
}

/** Where a branch goes under the remote's root: drama/<series>/_分支/<name without transfer/>, or null for a name it will not use. */
export function branchFolder(branch) {
  if (!BRANCH.test(branch) || branch.split("/").includes("..")) return null;
  const short = branch.replace(/^transfer\//, "");
  if (!SHORT.test(short) || short === "." || short === "..") return null;
  const code = short.match(/^([a-z0-9]+)-/)?.[1];
  const series = (code && Object.hasOwn(SERIES_DIRS, code) && SERIES_DIRS[code]) || OTHER_SERIES;
  return ["drama", series, BRANCHES_DIR, short].join("/");
}

const intFrom = (value, fallback) => {
  const read = Number.parseFloat(value ?? "");
  return Number.isFinite(read) && read >= 0 ? read : fallback;
};

/** A child process as { code, stdout, stderr }, never a throw. Output is capped. */
export function processRunner(command, env, cwd) {
  const cap = 256 * 1024;
  return (args, options = {}) =>
    new Promise((resolve) => {
      let stdout = "";
      let stderr = "";
      let child;
      try {
        child = spawn(command, args, { env: options.env ?? env, cwd: options.cwd ?? cwd, stdio: ["ignore", "pipe", "pipe"] });
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

const why = (result) => (result.stderr || result.stdout).trim().split("\n").filter(Boolean).slice(-1)[0]?.slice(0, 300) || `exit ${result.code}`;

/**
 * How git reaches the repository: { url, env }. The repository is public, so by default anonymously
 * over HTTPS with nothing on the host; a token (TOKEN_ENV or TOKEN_FILE_ENV, contents:read) is only a
 * fallback should it ever turn private, sent as an HTTP header in git's environment, never on a
 * command line. { problem } when a named token file cannot be read.
 */
export function gitAccess(env, fs = nodeFs) {
  const repo = String(env[REPO_ENV] || DEFAULT_REPO).trim();
  const named = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repo) ? repo.replace(/\.git$/, "") : null;
  const url = named ? `https://github.com/${named}.git` : repo;
  const base = { ...env, GIT_TERMINAL_PROMPT: "0", GIT_ASKPASS: "true", GIT_CONFIG_NOSYSTEM: "1", GIT_CONFIG_GLOBAL: "/dev/null" };
  let token = String(env[TOKEN_ENV] ?? "").trim();
  const tokenFile = String(env[TOKEN_FILE_ENV] ?? "").trim();
  if (!token && tokenFile) {
    try {
      token = fs.readFileSync(tokenFile, "utf8").trim();
    } catch (error) {
      return { problem: `the token file ${tokenFile} cannot be read (${error.code ?? error.message})` };
    }
  }
  if (!token) return { url, env: base, how: "anonymous" };
  const header = `Authorization: Basic ${Buffer.from(`x-access-token:${token}`).toString("base64")}`;
  return { url, env: { ...base, GIT_CONFIG_COUNT: "1", GIT_CONFIG_KEY_0: "http.https://github.com/.extraheader", GIT_CONFIG_VALUE_0: header }, how: "token" };
}

/** The remote's branches under the prefixes, as [{ branch, commit }], from `git ls-remote --heads`. */
export function parseHeads(stdout, prefixes) {
  const heads = [];
  for (const line of String(stdout).split("\n")) {
    const [commit, ref] = line.trim().split(/\s+/);
    if (!COMMIT.test(commit ?? "") || !ref?.startsWith("refs/heads/")) continue;
    const branch = ref.slice("refs/heads/".length);
    if (prefixes.some((prefix) => branch.startsWith(prefix))) heads.push({ branch, commit });
  }
  return heads.sort((a, b) => (a.branch < b.branch ? -1 : a.branch > b.branch ? 1 : 0));
}

/** Every regular file under `dir`, relative with "/", links never followed. */
function walk(dir, fs) {
  const found = [];
  const visit = (current, prefix) => {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      if (entry.isDirectory()) visit(path.join(current, entry.name), `${prefix}${entry.name}/`);
      else if (entry.isFile()) found.push(`${prefix}${entry.name}`);
    }
  };
  visit(dir, "");
  return found.sort();
}

/**
 * Every `X.part00`, `X.part01`… under `stage` joined back into `X`, the parts removed. Parts must
 * run from 00 without a gap; an `X.SPLIT` note with a sha256 must match the joined file. A branch
 * that has both `X` and its parts keeps them as they are. Returns { joined: [X], kept: [X], problem }.
 */
export async function rejoinParts(stage, fs = nodeFs) {
  const groups = new Map();
  for (const relative of walk(stage, fs)) {
    const match = relative.match(PART);
    if (!match) continue;
    const [, whole, index] = match;
    if (!groups.has(whole)) groups.set(whole, []);
    groups.get(whole).push({ relative, index: Number.parseInt(index, 10) });
  }
  const joined = [];
  const kept = [];
  for (const [whole, parts] of [...groups.entries()].sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))) {
    const target = path.join(stage, ...whole.split("/"));
    if (fs.existsSync(target)) {
      kept.push(whole);
      continue;
    }
    parts.sort((a, b) => a.index - b.index);
    if (parts.some((part, position) => part.index !== position)) return { joined, kept, problem: `${whole}: its parts do not run from part00 without a gap (${parts.map((part) => part.relative.split(".part").pop()).join(", ")})` };
    const hash = createHash("sha256");
    const out = createWriteStream(target);
    try {
      for (const part of parts) {
        const source = createReadStream(path.join(stage, ...part.relative.split("/")));
        source.on("data", (chunk) => hash.update(chunk));
        await pipeline(source, out, { end: false });
      }
    } finally {
      await new Promise((resolve) => out.end(resolve));
    }
    const digest = hash.digest("hex");
    const note = `${target}${SPLIT_NOTE}`;
    if (fs.existsSync(note)) {
      const wanted = fs.readFileSync(note, "utf8").match(SHA256)?.[0]?.toLowerCase();
      if (wanted && wanted !== digest) return { joined, kept, problem: `${whole}: joined parts hash ${digest}, its ${SPLIT_NOTE} note says ${wanted}` };
    }
    for (const part of parts) fs.rmSync(path.join(stage, ...part.relative.split("/")), { force: true });
    joined.push(whole);
  }
  return { joined, kept, problem: null };
}

const stamp = (date) => date.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");

export const readMirrorState = (base, fs = nodeFs) => {
  try {
    const read = JSON.parse(fs.readFileSync(path.join(base, MIRROR_DIR, STATE_FILE), "utf8"));
    return read && typeof read === "object" && read.branches && typeof read.branches === "object" ? read : { branches: {} };
  } catch {
    return { branches: {} };
  }
};

const saveState = (base, state) => atomicWrite(path.join(base, MIRROR_DIR, STATE_FILE), `${JSON.stringify(state, null, 2)}\n`);

function isDue(record, now) {
  if (!record?.failures || record.failures < MAX_FAILURES) return true;
  const last = Date.parse(record.failed_at ?? "");
  return !Number.isFinite(last) || now.getTime() - last >= FAILED_RETRY_MS;
}

function freeBytes(dir, fs) {
  try {
    const stats = fs.statfsSync(dir);
    return Number(stats.bavail) * Number(stats.bsize);
  } catch {
    return null;
  }
}

/** One branch: fetched, written out, rejoined, synced, checked. { ok, commit, files, bytes, joined } or { ok: false, error }. */
async function mirrorBranch(job, { branch, commit }) {
  const work = path.join(job.dir, "work");
  const repo = path.join(work, "repo.git");
  const stage = path.join(work, "tree");
  const { fs } = job;
  fs.rmSync(work, { recursive: true, force: true });
  fs.mkdirSync(stage, { recursive: true });
  try {
    const git = (args) => job.git(args, { env: job.access.env, cwd: work });
    let ran = await git(["init", "--bare", "--quiet", repo]);
    if (ran.code !== 0) return { ok: false, error: `git init: ${why(ran)}` };
    ran = await git(["--git-dir", repo, "fetch", "--quiet", "--no-tags", "--depth", "1", job.access.url, `+refs/heads/${branch}:refs/mirror/head`]);
    if (ran.code !== 0) return { ok: false, error: `git fetch: ${why(ran)}` };
    ran = await git(["--git-dir", repo, "rev-parse", "refs/mirror/head^{commit}"]);
    const fetched = ran.stdout.trim();
    if (ran.code !== 0 || !COMMIT.test(fetched)) return { ok: false, error: `git rev-parse: ${why(ran)}` };
    // The tree as plain files: a link is written as a file holding its target, as git stores it.
    const index = ["-c", "core.symlinks=false", "-c", "core.autocrlf=false", "--git-dir", repo, "--work-tree", stage];
    const indexEnv = { ...job.access.env, GIT_INDEX_FILE: path.join(work, "index") };
    ran = await job.git([...index, "read-tree", fetched], { env: indexEnv, cwd: work });
    if (ran.code === 0) ran = await job.git([...index, "checkout-index", "--all", "--force"], { env: indexEnv, cwd: work });
    if (ran.code !== 0) return { ok: false, error: `git checkout-index: ${why(ran)}`, commit: fetched };
    // The pack is not needed once the tree is out: only one copy of the branch on disk.
    fs.rmSync(repo, { recursive: true, force: true });
    fs.rmSync(path.join(work, "index"), { force: true });
    const rejoined = await rejoinParts(stage, fs);
    if (rejoined.problem) return { ok: false, error: rejoined.problem, commit: fetched };
    const files = walk(stage, fs);
    if (!files.length) return { ok: false, error: "the branch has no files; nothing is synced over the Drive folder", commit: fetched };
    const bytes = files.reduce((sum, relative) => sum + fs.statSync(path.join(stage, ...relative.split("/"))).size, 0);
    const folder = branchFolder(branch);
    const remote = `${job.remote}:${[job.prefix, folder].filter(Boolean).join("/")}`;
    const filters = ["--exclude", `/${OLD_VERSIONS}/**`];
    // sync, not copy, only so a file the branch deleted leaves the folder too: --backup-dir moves
    // it (and every file replaced) to _舊版/<time>/; nothing in Drive is deleted.
    const synced = await job.rclone(["sync", stage, remote, "--checksum", "--drive-chunk-size", "64M", "--tpslimit", "5", "--retries", "5", "--backup-dir", `${remote}/${OLD_VERSIONS}/${stamp(job.now)}`, ...filters]);
    if (synced.code !== 0) return { ok: false, error: `rclone sync: ${why(synced)}`, commit: fetched, folder };
    // Both ways: Drive's folder (bar _舊版) holds exactly the branch's files with the same hashes.
    const checked = await job.rclone(["check", stage, remote, ...filters]);
    if (checked.code !== 0) return { ok: false, error: `rclone check: ${why(checked)}`, commit: fetched, folder };
    return { ok: true, commit: fetched, folder, files: files.length, bytes, joined: rejoined.joined, kept: rejoined.kept };
  } catch (error) {
    return { ok: false, error: error.message };
  } finally {
    fs.rmSync(work, { recursive: true, force: true });
  }
}

/**
 * One round of the mirror: { lines, mirrored, state }. Never throws. `prefix` is the folder under
 * the remote's root the site's backup uses (its remote_prefix); without it the site's own config
 * is read. `rclone` and `git` are injectable runners (tests).
 */
export async function branchMirrorRound(ctx, { prefix, client: given, rclone: rcloneGiven, git: gitGiven } = {}) {
  const lines = [];
  const say = (line) => lines.push(`branch mirror: ${line}`);
  if (!mirrorOn(ctx.env)) return { lines, mirrored: [] };
  const fs = ctx.branchMirrorFs ?? nodeFs;
  let base;
  try {
    base = resolveWorkBase({ env: ctx.env, root: ctx.root, home: ctx.home });
  } catch (error) {
    say(`not run: ${error.message}`);
    return { lines, mirrored: [] };
  }
  if (stopRequested(base)) {
    say("STOP found; nothing is mirrored");
    return { lines, mirrored: [] };
  }
  if (prefix === undefined) {
    try {
      const config = await (given ?? backupClient(ctx)).config();
      prefix = config?.enabled ? config.remote_prefix : null;
    } catch (error) {
      say(`not run: the site's backup settings could not be read (${error.message})`);
      return { lines, mirrored: [] };
    }
  }
  if (prefix === null || prefix === undefined) {
    say("not run: the backup is off on /admin/videos or has no Drive folder; the mirror writes beside it");
    return { lines, mirrored: [] };
  }
  const rcloneEnv = rcloneEnvironment(ctx, fs);
  if (rcloneEnv.problem && !rcloneGiven) {
    say(`not run: ${rcloneEnv.problem}`);
    return { lines, mirrored: [] };
  }
  const dir = path.join(base, MIRROR_DIR);
  fs.mkdirSync(dir, { recursive: true });
  const access = gitAccess(ctx.env, fs);
  if (access.problem) {
    say(`not run: ${access.problem}; see docs/videos/BACKUP.md §AI 劇的分支鏡像`);
    return { lines, mirrored: [] };
  }
  const gitRun = gitGiven ?? processRunner("git", access.env, dir);
  const listed = await gitRun(["ls-remote", "--heads", access.url], { env: access.env, cwd: dir });
  if (listed.code !== 0) {
    say(`the branches could not be listed (${why(listed)})`);
    return { lines, mirrored: [] };
  }
  const now = ctx.now();
  const heads = parseHeads(listed.stdout, prefixesFrom(ctx.env));
  const state = readMirrorState(base, fs);
  const due = heads
    .filter(({ branch, commit }) => state.branches[branch]?.commit !== commit && isDue(state.branches[branch], now))
    .filter(({ branch }) => {
      if (branchFolder(branch)) return true;
      say(`${branch}: not mirrored, its name cannot be a Drive folder`);
      return false;
    })
    // Never tried first, then the one tried longest ago: a branch that keeps failing does not hold the others.
    .sort((a, b) => String(state.branches[a.branch]?.attempted_at ?? "").localeCompare(String(state.branches[b.branch]?.attempted_at ?? "")));
  const perRound = Math.floor(intFrom(ctx.env[PER_ROUND_ENV], DEFAULT_PER_ROUND));
  const maxBytes = intFrom(ctx.env[MAX_GB_ENV], DEFAULT_MAX_GB) * GB;
  const minFree = intFrom(ctx.env[MIN_FREE_GB_ENV], DEFAULT_MIN_FREE_GB) * GB;
  const job = {
    dir, fs, now, access, prefix,
    remote: String(ctx.env[REMOTE_ENV] || DEFAULT_REMOTE),
    git: gitRun,
    rclone: rcloneGiven ?? rcloneRunner(rcloneEnv.env),
  };
  const mirrored = [];
  let copied = 0;
  let done = 0;
  for (const head of due) {
    if (done >= perRound || copied >= maxBytes) break;
    if (stopRequested(base)) {
      say("STOP found; the rest wait");
      break;
    }
    const free = (ctx.branchMirrorFree ?? ((where) => freeBytes(where, fs)))(base);
    if (free !== null && free < minFree) {
      say(`waiting: ${(free / GB).toFixed(1)} GB free on the work disk, ${MIN_FREE_GB_ENV} wants ${minFree / GB}`);
      break;
    }
    done += 1;
    const previous = state.branches[head.branch] ?? {};
    const result = await mirrorBranch(job, head);
    const attempted = now.toISOString();
    if (result.ok) {
      copied += result.bytes;
      state.branches[head.branch] = {
        commit: result.commit, mirrored_at: attempted, attempted_at: attempted, folder: result.folder, check: "ok",
        files: result.files, bytes: result.bytes, joined: result.joined, ...(result.kept.length ? { kept_parts: result.kept } : {}), failures: 0, error: null,
      };
      mirrored.push({ branch: head.branch, commit: result.commit });
      say(`${head.branch} ${result.commit.slice(0, 12)} → ${[prefix, result.folder].filter(Boolean).join("/")}: ${result.files} files, ${(result.bytes / 1e6).toFixed(0)} MB, ${result.joined.length} joined from parts, rclone check 0 differences`);
    } else {
      state.branches[head.branch] = {
        ...previous, attempted_at: attempted, failed_at: attempted, failures: (previous.failures ?? 0) + 1, error: result.error,
        check: result.error.startsWith("rclone check") ? "differences" : previous.check ?? null, pending_commit: result.commit ?? head.commit,
      };
      say(`${head.branch} ${head.commit.slice(0, 12)}: not mirrored (${result.error}); tried again ${state.branches[head.branch].failures >= MAX_FAILURES ? "in 6 hours" : "next round"}`);
    }
    state.updated_at = attempted;
    saveState(base, state);
  }
  const waiting = due.length - done;
  if (waiting > 0) say(`${waiting} more branch${waiting === 1 ? "" : "es"} wait for a later round`);
  return { lines, mirrored, state };
}
