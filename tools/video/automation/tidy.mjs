// The tidy (docs/videos/AUTOMATION.md §清理工作區): once a video is finished and has been for the
// retention, the large files the stages made for it go, so the worker's volume (video_work) does
// not fill. A brand story leaves 1.3 to 2 GB behind (docs/videos/STORY.md §上限與成本).
//
// Finished is what auto.json says: on YouTube (status "done" with the YouTube id recorded) or
// dropped by the owner. auto.json keeps a date only for a drop (dropped.at, the site's
// dropped_at); flow.mjs records the YouTube id without one. So a video on YouTube is timed the
// way the site times the review store's mp4 (apps/api/app/video_reviews/admin_service.py,
// prune_published_previews): from the later of the upload confirmation's approval (the publish
// entry of approvals.json here, publish_approved_at on the site's list) and the publish time the
// owner set (youtube_publish_at). A finished video with no such date keeps everything, and the
// round says so.
//
// This deletes files on the production host, so every step is written to delete too little:
// only the names in TARGETS and the review copies, only inside the video's own folder directly
// in the work base, never through a link (a link found on the way is removed as a link, never
// what it points at), never a name that begins with "_" (the shared _series/ and _music/), and a
// work base that is empty, relative, a drive's root or overlaps the repository is refused.
import { existsSync, lstatSync, readdirSync, readFileSync, realpathSync, rmdirSync, unlinkSync } from "node:fs";
import path from "node:path";

import { approvalsFile } from "../core/approvals.mjs";
import { atomicWrite, defaultWorkBase, isInside, ROOT, WORKDIR_ENV } from "../core/paths.mjs";
import { ARTIFACTS, dubArtifacts } from "../core/state.mjs";
import { DUB_FORMATS, DUB_LOCALES } from "../dubs/plan.mjs";

// flow.mjs writes this file and owns these two patterns; tidy.test.mjs holds the copies together.
export const STATE_FILE = "auto.json";
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?$/;
const YOUTUBE_ID = /^[A-Za-z0-9_-]{11}$/;

export const DAYS_ENV = "VIDEO_TIDY_DAYS";
// The site's PREVIEW_RETENTION: the review store lets a published video's mp4 go after as long.
export const DEFAULT_DAYS = 7;
export const MAX_DAYS = 3650;
const DAY_MS = 86_400_000;

/**
 * What goes from a finished video's work directory, relative to it: the media the stages made,
 * which nothing reads once the video is on YouTube or dropped. The review copies are added by
 * name (PREVIEW). Everything else stays: auto.json, state.json, checks.json, approvals.json,
 * timeline.json, captions/, i18n/, languages.json, media/ (the ledger, the cache, the jobs),
 * answers/, review/'s JSON and pages, upload/'s metadata, descriptions, captions and thumbnail,
 * characters/ and music/ (the owner's picks, and small), thumbnail.jpg and contact-sheet.png.
 */
export const TARGETS = [
  ARTIFACTS.video, // final.mp4: assemble's, or compile's for a compilation
  path.join("upload", "final.mp4"), // package's copy; a hard link for a compilation
  path.join("upload", "dubs"), // package's copies of the dub tracks
  "segments", // assemble and compile: one encoded segment per scene or card
  "build", // assemble and compile: the joined picture, the mixed sound, partial files
  ARTIFACTS.audio, // tts: one WAV per line
  ARTIFACTS.narration, // tts: the whole narration
  path.dirname(ARTIFACTS.frames), // render: every slide state, subtitle strip and card
  path.dirname(ARTIFACTS.keyframes), // keyframes: a picture per shot and the contact sheets
  path.dirname(ARTIFACTS.clips), // clips: a generated clip per shot
  // dub, per locale: a WAV per line, the whole track before loudness, and the upload track
  ...DUB_LOCALES.flatMap((locale) => {
    const files = dubArtifacts("", locale);
    return [files.audio, files.narration, ...DUB_FORMATS.map((format) => files.track(format))];
  }),
];
// The review copies review-push encodes once per source file (review/sync.mjs preview()).
export const PREVIEW = /^(?:narration-[0-9a-f]{16}\.m4a|preview-[0-9a-f]{16}\.mp4)$/;

const nodeFs = { existsSync, lstatSync, readdirSync, readFileSync, realpathSync, rmdirSync, unlinkSync };

const fold = (value) => (process.platform === "win32" ? path.resolve(value).toLowerCase() : path.resolve(value));
const samePath = (left, right) => fold(left) === fold(right);
const strictlyInside = (child, parent) => isInside(child, parent) && !samePath(child, parent);
const isRoot = (dir) => path.parse(path.resolve(dir)).root === path.resolve(dir);
const slash = (relative) => relative.split(path.sep).join("/");
const day = (ms) => new Date(ms).toISOString().slice(0, 10);
const readState = (file, fs = nodeFs) => JSON.parse(fs.readFileSync(file, "utf8").replace(/^﻿/, ""));

/** How long a finished video keeps its files: { days }, { off: true }, or { problem }. */
export function retentionFrom(env = process.env) {
  const text = String(env[DAYS_ENV] ?? "").trim();
  if (text === "") return { days: DEFAULT_DAYS };
  if (text.toLowerCase() === "off") return { off: true };
  const days = Number(text);
  if (/^\d+$/.test(text) && days >= 1 && days <= MAX_DAYS) return { days };
  return { problem: `${DAYS_ENV}=${text} is neither a number of days from 1 to ${MAX_DAYS} nor "off"` };
}

function realOr(file, fs) {
  try {
    return fs.realpathSync(file);
  } catch {
    return file;
  }
}

function baseProblem(base, repos) {
  if (isRoot(base)) return `the work base ${base} is a drive's root`;
  for (const repo of repos) {
    if (isInside(base, repo)) return `the work base ${base} is inside the repository ${repo}`;
    if (isInside(repo, base)) return `the work base ${base} holds the repository ${repo}`;
  }
  return null;
}

/** The repositories no work base may overlap: the one the docs are read from, and this tool's own. */
export const repositories = (root) => [...new Set([root, ROOT].filter(Boolean).map((repo) => path.resolve(repo)))];

/**
 * The work base the tidy may clear in, as its real path: { base }; { missing } when there is
 * none yet; { refused } when it is empty, relative, a drive's root, or overlaps a repository.
 * `flag` is --workdir; otherwise VIDEO_WORKDIR, otherwise the default under the home directory.
 */
export function tidyBase({ flag, env = process.env, root = ROOT, home, fs = nodeFs } = {}) {
  const raw = flag ?? env[WORKDIR_ENV];
  if (raw !== undefined && raw !== null) {
    if (String(raw).trim() === "") return { refused: "the work base is empty" };
    if (!path.isAbsolute(String(raw))) return { refused: `the work base "${raw}" is a relative path` };
  }
  const base = path.resolve(raw ?? defaultWorkBase(home));
  const repos = repositories(root);
  const problem = baseProblem(base, repos);
  if (problem) return { refused: problem };
  if (!fs.existsSync(base)) return { missing: base };
  let real;
  try {
    real = fs.realpathSync(base);
  } catch (error) {
    return { refused: `the work base ${base} cannot be resolved (${error.code ?? error.message})` };
  }
  const realProblem = baseProblem(real, repos.map((repo) => realOr(repo, fs)));
  return realProblem ? { refused: realProblem } : { base: real };
}

/**
 * Why nothing may be removed from `workdir` at all, or null: the work base is not a root and
 * overlaps no repository, and the video's work directory sits directly in it under a video's
 * name (never "_…").
 */
function placeRefusal({ base, workdir, repos }) {
  const problem = baseProblem(base, repos);
  if (problem) return problem;
  if (!samePath(path.dirname(workdir), base) || !SLUG.test(path.basename(workdir))) return `${workdir} is not a video's folder directly in the work base ${base}`;
  for (const repo of repos) if (isInside(workdir, repo) || isInside(repo, workdir)) return `${workdir} is in the repository ${repo}`;
  return null;
}

/**
 * Why the tidy may not remove `target`, or null, from the paths alone: the place is sound
 * (placeRefusal), and the target is below the video's work directory, not that directory
 * itself, not the work base, and in no repository. What is on the disk (links) is checked by
 * the walk.
 */
export function targetRefusal(target, { base, workdir, repos = [ROOT] }) {
  if (samePath(target, base)) return `${target} is the work base itself`;
  const problem = placeRefusal({ base, workdir, repos });
  if (problem) return problem;
  if (samePath(target, workdir)) return `${target} is the video's whole work directory`;
  if (!strictlyInside(target, workdir)) return `${target} is outside the video's work directory ${workdir}`;
  for (const repo of repos) if (isInside(target, repo) || isInside(repo, target)) return `${target} is in the repository ${repo}`;
  return null;
}

/**
 * Every folder in the work base that is a video the worker made: a real folder (a link is never
 * followed), named as a video, holding an auto.json that names the same slug. Names that begin
 * with "_" are the shared folders and are not even read.
 */
function workVideos(base, fs) {
  let entries;
  try {
    entries = fs.readdirSync(base, { withFileTypes: true });
  } catch {
    return [];
  }
  const videos = [];
  for (const entry of entries) {
    if (entry.name.startsWith("_") || !entry.isDirectory() || !SLUG.test(entry.name)) continue;
    const workdir = path.join(base, entry.name);
    let state;
    try {
      state = readState(path.join(workdir, STATE_FILE), fs);
    } catch {
      continue;
    }
    if (state && typeof state === "object" && state.slug === entry.name) videos.push({ slug: entry.name, workdir, state });
  }
  return videos;
}

/** When the upload confirmation was last recorded here (approvals.json, gate "publish"), or NaN. */
function publishApproval(workdir, fs) {
  try {
    const record = readState(approvalsFile(workdir), fs);
    const dates = (record.approvals ?? []).filter((entry) => entry?.gate === "publish").map((entry) => Date.parse(String(entry.approved_at ?? "")));
    return Math.max(...dates.filter(Number.isFinite));
  } catch {
    return Number.NaN;
  }
}

/**
 * An episode of a binge series (docs/videos/BINGE.md) keeps its files until the series'
 * compilation is on YouTube: compile joins the episodes' approved final.mp4 and captions, and
 * the planner draws the thumbnail from the first episodes' keyframes.
 */
function compilationHold(state, states) {
  const series = state.series;
  if (!series || series.compilation !== true || state.compilation) return null;
  const whole = states.find((other) => other?.compilation?.series === series.slug);
  if (whole && whole.status === "done" && YOUTUBE_ID.test(String(whole.youtube_video_id ?? ""))) return null;
  return `an episode of ${series.slug}, whose compilation ${whole ? "is not on YouTube yet" : "has not started"}`;
}

/**
 * Whether a video is finished and since when: null when it is not (being made, blocked, waiting
 * for the owner, or already tidied); { held } when it is finished but something still needs its
 * files; { problem } when it is finished but has no usable date; else { at, how }.
 */
function judge({ slug, workdir, state }, { states, listed, fs }) {
  if (state.tidied_at) return null;
  const dropped = state.status === "dropped";
  const onYouTube = state.status === "done" && YOUTUBE_ID.test(String(state.youtube_video_id ?? ""));
  if (!dropped && !onYouTube) return null;
  if (fs.existsSync(path.join(workdir, "STOP"))) return { held: "a STOP file is in its work directory" };
  if (dropped) {
    const at = Date.parse(String(state.dropped?.at ?? ""));
    return Number.isFinite(at) ? { at, how: "dropped" } : { problem: "dropped, but auto.json has no date in dropped.at" };
  }
  const compilation = compilationHold(state, states);
  if (compilation) return { held: compilation };
  if (!listed) return { held: "the site's video list was not read, so its publish time and languages are unknown" };
  // A video that fell off the site's list (the newest 200) has no publish time or languages to
  // check there any more; its own approvals still date it.
  const site = listed.get(slug) ?? null;
  if (site && !site.locales_decided_at) return { held: "its languages are not decided on /admin/videos yet" };
  const working = Object.entries(site?.languages ?? {}).flatMap(([locale, parts]) =>
    Object.entries(parts ?? {})
      .filter(([, part]) => part?.state === "working")
      .map(([part]) => `${locale} ${part}`),
  );
  if (working.length) return { held: `the site still shows ${working.join(", ")} in the making` };
  const confirmed = [publishApproval(workdir, fs), Date.parse(String(site?.publish_approved_at ?? ""))].filter(Number.isFinite);
  if (!confirmed.length) return { problem: "on YouTube, but its upload confirmation has no date (no publish approval in approvals.json, none on the site)" };
  let at = Math.max(...confirmed);
  if (site?.youtube_publish_at !== null && site?.youtube_publish_at !== undefined) {
    const publish = Date.parse(String(site.youtube_publish_at));
    if (!Number.isFinite(publish)) return { problem: `the site's publish time "${site.youtube_publish_at}" is not a date` };
    at = Math.max(at, publish);
  }
  return { at, how: "on YouTube" };
}

/**
 * How a target is reached from the work directory: { stat } (lstat, not followed) when every
 * folder on the way is a real folder; { absent } when something on the way is not there;
 * { problem } when a link or a file stands where a folder should, so nothing is removed through it.
 */
function reach(workdir, target, fs) {
  const parts = path.relative(workdir, target).split(path.sep);
  let current = workdir;
  for (const [index, part] of parts.entries()) {
    current = path.join(current, part);
    let stat;
    try {
      stat = fs.lstatSync(current);
    } catch (error) {
      if (error.code === "ENOENT" || error.code === "ENOTDIR") return { absent: true };
      return { problem: `${slash(path.relative(workdir, current))} cannot be read (${error.code ?? error.message})` };
    }
    if (index === parts.length - 1) return { stat };
    if (!stat.isDirectory()) return { problem: `${slash(path.relative(workdir, current))} is a link or a file, not a folder; nothing is removed through it` };
  }
  return { absent: true };
}

/** The targets present in a work directory: TARGETS, then the review copies by name. */
function targetsIn(workdir, fs) {
  const names = [...TARGETS];
  const review = path.join(workdir, "review");
  try {
    if (fs.lstatSync(review).isDirectory()) for (const name of fs.readdirSync(review).sort()) if (PREVIEW.test(name)) names.push(path.join("review", name));
  } catch {
    // No review folder: nothing to add.
  }
  return names;
}

/**
 * Remove one file, link or folder tree, never following a link: a folder is emptied and removed
 * only when it is a real folder where it stands; a link of any kind (a symbolic link, a Windows
 * junction) is unlinked as a name. A dry run walks the same way and removes nothing. A file
 * frees its bytes once every name it has went (a compilation's upload/final.mp4 is a hard link).
 */
function removeTree(file, job) {
  let stat;
  try {
    stat = job.fs.lstatSync(file, { bigint: true });
  } catch (error) {
    job.missed(file, error);
    return;
  }
  if (stat.isDirectory()) {
    let real;
    try {
      real = job.fs.realpathSync(file);
    } catch (error) {
      job.failure(file, error.code ?? error.message);
      return;
    }
    if (!samePath(real, file)) {
      job.failure(file, `resolves to ${real}, so it is not followed`);
      return;
    }
    let names;
    try {
      names = job.fs.readdirSync(file);
    } catch (error) {
      job.failure(file, error.code ?? error.message);
      return;
    }
    const failedBefore = job.failed.length;
    for (const name of names) removeTree(path.join(file, name), job);
    // A folder whose content could not all go stays with it; its own removal would only repeat that.
    if (job.dryRun || job.failed.length > failedBefore) return;
    try {
      job.fs.rmdirSync(file);
    } catch (error) {
      job.missed(file, error);
    }
    return;
  }
  if (!job.dryRun) {
    try {
      job.fs.unlinkSync(file);
    } catch (error) {
      job.missed(file, error);
      return;
    }
  }
  job.files += 1;
  if (stat.isFile()) job.count(stat);
}

function newJob({ workdir, dryRun, fs }) {
  const inodes = new Map();
  const job = {
    fs,
    dryRun,
    files: 0,
    bytes: 0,
    failed: [],
    gone: [],
    failure(file, error) {
      job.failed.push({ path: slash(path.relative(workdir, file)), error: String(error) });
    },
    // A name that is already gone was removed by someone else; anything else is a failure.
    missed(file, error) {
      if (error.code === "ENOENT") job.gone.push(slash(path.relative(workdir, file)));
      else job.failure(file, error.code ?? error.message);
    },
    count(stat) {
      const key = `${stat.dev}:${stat.ino}`;
      const entry = inodes.get(key) ?? { size: stat.size, links: stat.nlink, seen: 0n };
      entry.seen += 1n;
      inodes.set(key, entry);
      if (entry.seen === entry.links) job.bytes += Number(entry.size);
    },
  };
  return job;
}

/** Clear one due video (or, in a dry run, say what would go) and record it in its auto.json. */
function clearVideo(video, { base, repos, now, dryRun, fs }) {
  const { slug, workdir } = video;
  const outcome = { slug, at: video.at, how: video.how, dryRun, removed: [], failed: [], gone: [], bytes: 0, refused: null, recorded: null };
  outcome.refused = placeRefusal({ base, workdir, repos });
  if (outcome.refused) return outcome;
  let real = null;
  try {
    real = fs.lstatSync(workdir).isDirectory() ? fs.realpathSync(workdir) : null;
  } catch {
    real = null;
  }
  if (!real || !samePath(real, workdir)) {
    outcome.refused = `${workdir} is not a real folder where it stands`;
    return outcome;
  }
  const job = newJob({ workdir, dryRun, fs });
  for (const relative of targetsIn(workdir, fs)) {
    const target = path.join(workdir, relative);
    const refusal = targetRefusal(target, { base, workdir, repos });
    if (refusal) {
      job.failure(target, refusal);
      continue;
    }
    const way = reach(workdir, target, fs);
    if (way.absent) continue;
    if (way.problem) {
      job.failure(target, way.problem);
      continue;
    }
    const before = { files: job.files, bytes: job.bytes, failed: job.failed.length, gone: job.gone.length };
    removeTree(target, job);
    const whole = job.failed.length === before.failed && job.gone.length === before.gone;
    if (job.files > before.files || whole) outcome.removed.push({ path: slash(relative), folder: way.stat.isDirectory(), files: job.files - before.files, bytes: job.bytes - before.bytes });
  }
  Object.assign(outcome, { failed: job.failed, gone: job.gone, bytes: job.bytes });
  if (dryRun) return outcome;
  const file = path.join(workdir, STATE_FILE);
  try {
    const state = readState(file, fs);
    if (state.tidied_at) {
      outcome.recorded = `another run recorded its tidy at ${state.tidied_at} first`;
      return outcome;
    }
    const tidied = { bytes: outcome.bytes, removed: outcome.removed.map((entry) => entry.path), failed: outcome.failed, ...(outcome.gone.length ? { gone: outcome.gone } : {}) };
    atomicWrite(file, `${JSON.stringify({ ...state, tidied_at: now.toISOString(), tidied }, null, 2)}\n`);
    outcome.recorded = true;
  } catch (error) {
    outcome.recorded = `auto.json could not record the tidy (${error.message})`;
  }
  return outcome;
}

/**
 * One round of the tidy: every finished video in the work base sorted into due, waiting, held
 * and undated, then the oldest due one cleared (or, with dryRun, what would go listed). `base`
 * is tidyBase's real path; `site` is the round's video list from the site (ProjectSummary[]),
 * null when it was not read; `repos` are the repositories nothing may touch.
 */
export function tidyRound({ base: given, repos: named = [ROOT], site = null, now = new Date(), days = DEFAULT_DAYS, dryRun = false, fs = nodeFs }) {
  // Every path below is compared with real paths: a link in the work base's own path is the
  // operator's choice, a link below it is never followed.
  const base = realOr(given, fs);
  const repos = named.map((repo) => realOr(repo, fs));
  const cutoff = now.getTime() - days * DAY_MS;
  const videos = workVideos(base, fs);
  const states = videos.map((video) => video.state);
  const listed = Array.isArray(site) ? new Map(site.filter((video) => typeof video?.slug === "string").map((video) => [video.slug, video])) : null;
  const round = { base, days, dryRun, due: [], waiting: [], held: [], undated: [], refused: [], cleared: null };
  for (const video of videos) {
    const verdict = judge(video, { states, listed, fs });
    if (!verdict) continue;
    if (verdict.held) round.held.push({ slug: video.slug, why: verdict.held });
    else if (verdict.problem) round.undated.push({ slug: video.slug, why: verdict.problem });
    else if (verdict.at <= cutoff) round.due.push({ ...video, ...verdict });
    else round.waiting.push({ slug: video.slug, how: verdict.how, at: verdict.at, until: verdict.at + days * DAY_MS });
  }
  const order = (a, b) => a.at - b.at || (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0);
  round.due.sort(order);
  round.waiting.sort((a, b) => a.until - b.until || order(a, b));
  // One video a round, the oldest first. A folder refused before anything was touched does not
  // hold the others back: the next one is tried, and the refusal is reported every round.
  for (const video of round.due) {
    const outcome = clearVideo(video, { base, repos, now, dryRun, fs });
    if (outcome.refused) {
      round.refused.push(outcome);
      continue;
    }
    round.cleared = outcome;
    break;
  }
  return round;
}

/** Bytes as people read them. */
export function sizeText(bytes) {
  if (bytes >= 1024 ** 3) return `${(bytes / 1024 ** 3).toFixed(2)} GB`;
  if (bytes >= 1024 ** 2) return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
  if (bytes >= 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${bytes} bytes`;
}

const firstFew = (items, text, limit = 3) => `${items.slice(0, limit).map(text).join(", ")}${items.length > limit ? ` and ${items.length - limit} more` : ""}`;
// When the retention started: the drop, or the later of the upload confirmation and the publish time.
const finished = ({ how, at }) => (how === "dropped" ? `dropped on ${day(at)}` : `on YouTube, counted from ${day(at)}`);

/** The line naming the video, what was removed (or would be) and how many bytes were freed. */
export function clearedLine(outcome) {
  const since = finished(outcome);
  if (outcome.refused) return `tidy: ${outcome.slug} (${since}) not cleared: ${outcome.refused}`;
  const list = outcome.removed.map((entry) => (entry.folder ? `${entry.path}/ (${entry.files} file${entry.files === 1 ? "" : "s"})` : entry.path)).join(", ");
  const size = outcome.bytes >= 1024 ? `${sizeText(outcome.bytes)} (${outcome.bytes} bytes)` : sizeText(outcome.bytes);
  const notes = [
    outcome.failed.length ? `could not remove ${outcome.failed.length}: ${firstFew(outcome.failed, (entry) => `${entry.path} (${entry.error})`)}` : "",
    outcome.gone.length ? `already gone: ${firstFew(outcome.gone, (name) => name)}` : "",
    typeof outcome.recorded === "string" ? outcome.recorded : "",
  ].filter(Boolean);
  const tail = notes.length ? `; ${notes.join("; ")}` : "";
  if (outcome.dryRun) return `tidy --dry-run: ${outcome.slug} (${since}) would lose ${list || "nothing"}; ${size} would be freed${tail}`;
  return `tidy: ${outcome.slug} (${since}): ${list ? `removed ${list}` : "nothing was left to remove"}; ${size} freed${tail}`;
}

/**
 * What a round prints. `auto` prints only what happened and what needs a person (the cleared
 * video, a refusal, a finished video with no usable date); the hand-run command (verbose) also
 * says what waits and why.
 */
export function roundLines(round, { verbose = false } = {}) {
  const lines = [];
  for (const outcome of round.refused) lines.push(clearedLine(outcome));
  if (round.cleared) lines.push(clearedLine(round.cleared));
  if (round.undated.length) lines.push(`tidy: finished but kept, no usable date: ${round.undated.map((entry) => `${entry.slug} (${entry.why})`).join("; ")}`);
  if (!verbose) return lines;
  if (!round.cleared) lines.push(`tidy: nothing is due${round.refused.length ? " that can be cleared" : ""}`);
  const later = round.due.filter((video) => video.slug !== round.cleared?.slug && !round.refused.some((outcome) => outcome.slug === video.slug));
  if (later.length) lines.push(`tidy: also due, one a round: ${later.map((video) => `${video.slug} (${finished(video)})`).join(", ")}`);
  if (round.held.length) lines.push(`tidy: finished but kept while something needs the files: ${round.held.map((entry) => `${entry.slug} (${entry.why})`).join("; ")}`);
  if (round.waiting.length) lines.push(`tidy: ${round.waiting.length} finished ${round.waiting.length === 1 ? "video keeps" : "videos keep"} its files for ${round.days} days; the next, ${round.waiting[0].slug}, is due on ${day(round.waiting[0].until)}`);
  return lines;
}

/**
 * What `status` says instead of the next step once a video's work files were cleared: the steps
 * that read them show as not done, and nothing makes them again. Null for a video not tidied.
 */
export function tidiedNote(workdir, fs = nodeFs) {
  let state;
  try {
    state = readState(path.join(workdir, STATE_FILE), fs);
  } catch {
    return null;
  }
  if (!state?.tidied_at) return null;
  const cleared = `the work files were cleared on ${String(state.tidied_at).slice(0, 10)}${Number.isFinite(state.tidied?.bytes) ? ` (${sizeText(state.tidied.bytes)} freed)` : ""}`;
  const failed = state.tidied?.failed?.length ? `; ${state.tidied.failed.length} could not be removed (auto.json, tidied.failed)` : "";
  const lead = state.status === "dropped" ? `Dropped by the owner${state.dropped?.at ? ` on ${String(state.dropped.at).slice(0, 10)}` : ""}` : `On YouTube${state.youtube_video_id ? ` as ${state.youtube_video_id}` : ""}`;
  return `${lead}; ${cleared}${failed}. The steps above that read those files show as not done; nothing makes them again.`;
}
