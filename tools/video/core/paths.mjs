// Where things live. Text sources are in the repository under docs/videos/<slug>/; everything
// generated (audio, frames, video, approvals) is in <VIDEO_WORKDIR>/<slug>/, a durable directory
// outside the repository: the repository is public and the files are large.
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = fileURLToPath(new URL("../../../", import.meta.url));
export const WORKDIR_ENV = "VIDEO_WORKDIR";

export const videosDir = (root = ROOT) => path.join(root, "docs", "videos");
export const docDir = (slug, root = ROOT) => path.join(videosDir(root), slug);
export const videoFile = (slug, root = ROOT) => path.join(docDir(slug, root), "video.json");
export const lexiconFile = (root = ROOT) => path.join(videosDir(root), "lexicon.json");
export const contentPackFile = (slug, root = ROOT) => path.join(root, "apps", "api", "app", "guides", "content", `${slug}.json`);

export class UsageError extends Error {}

/** Whether `child` is `parent` or inside it (case-insensitive on Windows). */
export function isInside(child, parent) {
  const fold = (value) => (process.platform === "win32" ? path.resolve(value).toLowerCase() : path.resolve(value));
  const relative = path.relative(fold(parent), fold(child));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

/** Where videos go when neither --workdir nor VIDEO_WORKDIR says otherwise. */
export function defaultWorkBase(home = os.homedir()) {
  return path.join(home, "mokaair-work", "videos");
}

/** The directory every video's work directory sits in. */
export function resolveWorkBase({ flag, env = process.env, root = ROOT, home } = {}) {
  const base = path.resolve(flag ?? env[WORKDIR_ENV] ?? defaultWorkBase(home));
  if (isInside(base, root)) throw new UsageError(`the work directory ${base} is inside the repository; generated media must stay out of git`);
  return base;
}

/** The video's own work directory, <base>/<slug>, refusing anything inside the repository. */
export function resolveWorkdir({ flag, env = process.env, slug, root = ROOT, home }) {
  const base = resolveWorkBase({ flag, env, root, home });
  const workdir = path.resolve(base, slug);
  if (isInside(workdir, root)) throw new UsageError(`the work directory ${workdir} is inside the repository; generated media must stay out of git`);
  return workdir;
}

/** Write through a temporary file and a rename, so an interrupted run never leaves half a file. */
export function atomicWrite(file, data) {
  mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${process.pid}.tmp`;
  writeFileSync(temporary, data);
  renameSync(temporary, file);
}

export function readJson(file, fallback = undefined) {
  if (!existsSync(file)) {
    if (fallback !== undefined) return fallback;
    throw new UsageError(`${file} does not exist`);
  }
  return JSON.parse(readFileSync(file, "utf8").replace(/^﻿/, ""));
}

export function readText(file) {
  return existsSync(file) ? readFileSync(file, "utf8") : null;
}

/**
 * A STOP file in the video's work directory, or in the base directory above it for every video,
 * asks long-running stages to finish the unit they are on and exit.
 */
export function stopRequested(workdir) {
  return existsSync(path.join(workdir, "STOP")) || existsSync(path.join(path.dirname(workdir), "STOP"));
}
