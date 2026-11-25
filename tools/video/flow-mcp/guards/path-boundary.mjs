/**
 * Route B anti-leak path guard (2026-11-25).
 *
 * Ensures all episode drafts, generated Flow stills, video clips, manifests,
 * and ledgers are written ONLY inside gitignored `work/video-episodes/<slug>/`
 * (never into tracked repo trees like `docs/videos/`).
 */

import path from "node:path";
import { REPO_ROOT, resolveWorkEpisodesRoot } from "../config.mjs";

const SLUG_RE = /^[a-z0-9][a-z0-9._-]{1,120}$/i;

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
    reviewDir,
    preflightFile: path.join(reviewDir, "flow-preflight.json"),
  };
}
