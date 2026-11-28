/**
 * Route B anti-leak path guard (2026-11-25).
 *
 * Ensures all episode drafts, generated Flow stills, video clips, manifests,
 * and ledgers are written ONLY inside gitignored `work/video-episodes/<slug>/`
 * (never into tracked repo trees like `docs/videos/`).
 */

import fs from "node:fs";
import path from "node:path";
import { REPO_ROOT, resolveWorkEpisodesRoot } from "../config.mjs";

const SLUG_RE = /^[a-z0-9][a-z0-9._-]{1,120}$/i;

export const MAX_TRANSFER_CHUNK_BYTES = 512 * 1024; // 512 KiB decoded -> ~683 KiB base64 (< 1 MiB RPC cap)
export const MAX_EPISODE_FILE_BYTES = 128 * 1024 * 1024; // 128 MiB per episode asset

export const EPISODE_TRANSFER_ALLOWED_EXTS = Object.freeze(
  new Set([
    ".json",
    ".txt",
    ".md",
    ".html",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".mp4",
    ".wav",
    ".m4a",
    ".mp3",
    ".srt",
    ".vtt",
    ".csv",
  ]),
);

const FORBIDDEN_REPO_PREFIXES = [
  "docs/videos",
  "docs",
  "apps",
  "tools",
  "ops",
  "tasks",
  ".git",
  ".agents",
  ".claude",
];

function normalizeForCompare(p) {
  const resolved = path.resolve(p).replace(/\\/g, "/").replace(/\/+$/, "");
  return process.platform === "win32" ? resolved.toLowerCase() : resolved;
}

function isInside(child, parent) {
  const c = normalizeForCompare(child);
  const p = normalizeForCompare(parent);
  return c === p || c.startsWith(`${p}/`);
}

function assertNoSymlinkChain(rootDir, segments) {
  let cursor = path.resolve(rootDir);
  if (fs.existsSync(cursor) && fs.lstatSync(cursor).isSymbolicLink()) {
    throw new Error(`Refusing symlinked episode root "${cursor}".`);
  }
  for (const seg of segments) {
    cursor = path.join(cursor, seg);
    if (!fs.existsSync(cursor)) break;
    if (fs.lstatSync(cursor).isSymbolicLink()) {
      throw new Error(`Refusing symlink path component "${seg}" inside episode directory.`);
    }
  }
}

function sanitizeRelativeSegments(rawPath, { allowEmpty = false } = {}) {
  const text = String(rawPath ?? "").trim();
  if (!text) {
    if (allowEmpty) return [];
    throw new Error("Relative episode path must be non-empty.");
  }
  if (text.includes("\0")) {
    throw new Error("Relative episode path must not contain null bytes.");
  }
  const normalized = text.replace(/\\/g, "/");
  if (normalized.startsWith("/") || /^[A-Za-z]:/.test(normalized)) {
    throw new Error(`Episode path "${rawPath}" must be relative (no leading slash or drive letter).`);
  }
  const rawSegments = normalized.split("/").filter((s) => s.length > 0);
  if (rawSegments.length === 0) {
    if (allowEmpty) return [];
    throw new Error("Relative episode path must be non-empty.");
  }
  for (const seg of rawSegments) {
    if (seg === "." || seg === ".." || seg.startsWith(".")) {
      throw new Error(`Forbidden path segment "${seg}" in episode path "${rawPath}".`);
    }
  }
  return rawSegments;
}

export function validateEpisodeSlug(slug) {
  const value = String(slug || "").trim();
  if (!SLUG_RE.test(value) || value.includes("..")) {
    throw new Error(
      `Invalid episode slug "${slug}". Use only letters, digits, dots, hyphens, or underscores (no path separators or "..").`,
    );
  }
  return value;
}

/**
 * Verifies that `targetDir` is a safe Route B episode workdir and cannot leak
 * scripts or binary media into tracked GitHub paths.
 */
export function assertEpisodeWorkdirSafe(
  targetDir,
  { repoRoot = REPO_ROOT, allowExternal = false } = {},
) {
  if (!targetDir || typeof targetDir !== "string") {
    throw new Error("Episode workdir must be a non-empty path.");
  }

  const resolvedTarget = path.resolve(targetDir);
  const workRoot = path.resolve(resolveWorkEpisodesRoot(repoRoot));

  for (const rel of FORBIDDEN_REPO_PREFIXES) {
    const forbidden = path.resolve(repoRoot, rel);
    if (isInside(resolvedTarget, forbidden)) {
      throw new Error(
        `Route B boundary violation: refusing to write episode assets inside tracked repo directory "${rel}" (${resolvedTarget}). Use work/video-episodes/<slug>/ instead.`,
      );
    }
  }

  if (!isInside(resolvedTarget, workRoot)) {
    if (!allowExternal) {
      throw new Error(
        `Route B boundary violation: episode workdir "${resolvedTarget}" must live under "${workRoot}". Set allowExternal only for isolated temp test runs.`,
      );
    }
  }

  return resolvedTarget;
}

/**
 * Resolves all standardized directories and artifact files for an episode.
 */
export function resolveEpisodePaths(
  slug,
  { repoRoot = REPO_ROOT, workdir, allowExternal = false } = {},
) {
  const cleanSlug = validateEpisodeSlug(slug);
  const root = workdir
    ? assertEpisodeWorkdirSafe(workdir, { repoRoot, allowExternal })
    : assertEpisodeWorkdirSafe(path.join(resolveWorkEpisodesRoot(repoRoot), cleanSlug), {
        repoRoot,
        allowExternal,
      });

  const stillsDir = path.join(root, "stills");
  const clipsDir = path.join(root, "flow-clips");
  const reviewDir = path.join(root, "review");

  return {
    slug: cleanSlug,
    root,
    workspaceFile: path.join(root, "flow-workspace.json"),
    castFile: path.join(root, "cast.json"),
    videoJsonFile: path.join(root, "video.json"),
    shotListFile: path.join(root, "flow-shot-list.json"),
    stillsDir,
    rejectedStillsDir: path.join(stillsDir, "_rejected"),
    stillsQaFile: path.join(stillsDir, "qa-manifest.json"),
    stillsGalleryFile: path.join(stillsDir, "qa-gallery.html"),
    clipsDir,
    clipsRawDir: path.join(clipsDir, "raw-720p"),
    clipsTakesDir: path.join(clipsDir, "takes"),
    clipsAudioDir: path.join(clipsDir, "raw-audio"),
    clipsQaDir: path.join(clipsDir, "qa4"),
    clipsManifestFile: path.join(clipsDir, "manifest.json"),
    clipsImportBridgeFile: path.join(clipsDir, "import-bridge.json"),
    clipsGalleryFile: path.join(clipsDir, "qa-gallery.html"),
    ledgerFile: path.join(clipsDir, "credit-ledger.json"),
    pendingApprovalsFile: path.join(clipsDir, ".pending-approvals.json"),
    transfersDir: path.join(root, ".transfers"),
    reviewDir,
    preflightFile: path.join(reviewDir, "flow-preflight.json"),
  };
}

/**
 * Resolves an optional relative subdirectory jailed inside `paths.root`.
 */
export function resolveEpisodeSubdir(paths, subdir = "") {
  const segments = sanitizeRelativeSegments(subdir, { allowEmpty: true });
  const absDir = segments.length > 0 ? path.resolve(paths.root, ...segments) : path.resolve(paths.root);
  if (!isInside(absDir, paths.root)) {
    throw new Error(`Episode subdir "${subdir}" escapes "${paths.root}".`);
  }
  assertNoSymlinkChain(paths.root, segments);
  return {
    relDir: segments.join("/"),
    absDir,
  };
}

/**
 * Resolves and validates a relative file path jailed inside `paths.root` for
 * remote MCP file transfer (blocks traversal, dotfiles, symlinks, and
 * non-allowlisted extensions).
 */
export function resolveEpisodeRelPath(paths, relPath) {
  const segments = sanitizeRelativeSegments(relPath, { allowEmpty: false });
  const cleanRel = segments.join("/");
  const ext = path.posix.extname(cleanRel).toLowerCase();
  if (!EPISODE_TRANSFER_ALLOWED_EXTS.has(ext)) {
    throw new Error(
      `Unsupported episode file extension "${ext || "(none)"}" for "${cleanRel}". Allowed: ${[...EPISODE_TRANSFER_ALLOWED_EXTS].join(", ")}.`,
    );
  }
  const absPath = path.resolve(paths.root, ...segments);
  if (!isInside(absPath, paths.root) || normalizeForCompare(absPath) === normalizeForCompare(paths.root)) {
    throw new Error(`Episode file path "${relPath}" escapes "${paths.root}".`);
  }
  assertNoSymlinkChain(paths.root, segments);
  return {
    relPath: cleanRel,
    absPath,
    ext,
  };
}

/**
 * Resolves the gitignored shared series Cast file for multi-episode AI dramas
 * (`work/video-episodes/_series/<dramaName>/cast.json`).
 */
export function resolveSeriesCastPath(dramaName, { repoRoot = REPO_ROOT } = {}) {
  const cleanName = String(dramaName || "")
    .trim()
    .replace(/[^a-zA-Z0-9._\u4e00-\u9fff-]+/g, "_")
    .replace(/^_+|_+$/g, "");
  if (!cleanName || cleanName.includes("..")) {
    throw new Error(`Invalid dramaName "${dramaName}" for shared series cast.`);
  }
  const seriesDir = assertEpisodeWorkdirSafe(
    path.join(resolveWorkEpisodesRoot(repoRoot), "_series", cleanName),
    { repoRoot },
  );
  return path.join(seriesDir, "cast.json");
}
