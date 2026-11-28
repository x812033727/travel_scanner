/**
 * Central configuration, series presets, and cross-platform path resolvers for
 * Mokaair's local Google Flow Music MCP server (`mokaair-flow-music`).
 *
 * Drives https://www.flowmusic.app (Google Flow Music / Lyria 3.5) using the
 * owner's own subscription account via an isolated Chrome profile (zero
 * passwords touched, zero credential export, 0 GitHub commits per Route B).
 */

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const MCP_SERVER_NAME = "mokaair-flow-music";
export const MCP_SERVER_VERSION = "1.0.0";
export const FLOW_MUSIC_ORIGIN = "https://www.flowmusic.app";
export const DEFAULT_MUSIC_MODEL = "lyria-3.5";
export const DEFAULT_DOWNLOAD_FORMAT = "m4a";
export const SUPPORTED_DOWNLOAD_FORMATS = Object.freeze(["m4a", "mp3", "wav"]);

/** Standard `MUSIC_TRACK` filename contract used by Mokaair's video pipeline. */
export const MUSIC_TRACK_RE = /^[a-z0-9][a-z0-9._-]{0,63}\.(?:m4a|mp3|wav|flac|ogg)$/;
export const TRACK_KINDS = Object.freeze(["bed", "cue", "sfx"]);

const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(MODULE_DIR, "../../..");

/** Mixing guardrail appended to narration background beds (`kind: "bed"`). */
export const BED_MIXING_SUFFIX =
  "instrumental only, no vocals, no solo lead melody competing with narration, steady understated arrangement, no big drops, clean ending";

/**
 * Series presets aligned with docs/videos/explainer-series/music-library/README.md
 * and Google Drive SSOT layout (`AI/備份/AI劇/`).
 */
export const SERIES_PRESETS = Object.freeze({
  curio: Object.freeze({
    id: "curio",
    label: "奇聞檔案局",
    driveLibraryPath: "奇聞檔案局/_共用/製作檔/curio-music-library",
    sfxSetName: "curio-flow",
    bedMix: Object.freeze({ gainDb: -20, duckDb: -10, maxBedLufs: -24, targetMinSec: 120 }),
    styleGuide: "light, curious, slightly mysterious, understated acoustic/chamber textures, no vocals",
  }),
  sothatswhy: Object.freeze({
    id: "sothatswhy",
    label: "原來如此事務所",
    driveLibraryPath: "原來如此事務所/_共用/製作檔/sothatswhy-music-library",
    sfxSetName: "sothatswhy-flow",
    bedMix: Object.freeze({ gainDb: -20, duckDb: -10, maxBedLufs: -24, targetMinSec: 120 }),
    styleGuide: "bright, playful, curious, warm pizzicato/ukulele/marimba/light percussion, no vocals",
  }),
  "drama-16x9": Object.freeze({
    id: "drama-16x9",
    label: "橫式 AI 劇（16:9）",
    driveLibraryPath: "_共用素材/music/drama-16x9",
    sfxSetName: "drama-flow",
    bedMix: Object.freeze({ gainDb: -18, duckDb: -10, maxBedLufs: -24, targetMinSec: 120 }),
    styleGuide: "cinematic underscore tailored to scene mood, clean stems/no competing lead vocal",
  }),
  "drama-9x16": Object.freeze({
    id: "drama-9x16",
    label: "直式 AI 短劇（9:16）",
    driveLibraryPath: "_共用素材/music/drama-9x16",
    sfxSetName: "drama-vertical-flow",
    bedMix: Object.freeze({ gainDb: -18, duckDb: -10, maxBedLufs: -24, targetMinSec: 90 }),
    styleGuide: "punchy short-form cinematic underscore, fast hook in first 3 seconds, no vocals",
  }),
  shorts: Object.freeze({
    id: "shorts",
    label: "零台詞 Shorts 短劇（9:16）",
    driveLibraryPath: "Shorts/_共用/製作檔/shorts-music-library",
    sfxSetName: "shorts-flow",
    bedMix: Object.freeze({ gainDb: -16, duckDb: -6, maxBedLufs: -22, targetMinSec: 30 }),
    styleGuide: "expressive playful silent-comedy underscore, crisp rhythmic beats, zero spoken vocals",
  }),
  shared: Object.freeze({
    id: "shared",
    label: "跨節目共用素材",
    driveLibraryPath: "_共用素材/music",
    sfxSetName: "shared-flow",
    bedMix: Object.freeze({ gainDb: -20, duckDb: -10, maxBedLufs: -24, targetMinSec: 120 }),
    styleGuide: "versatile instrumental background bed, no vocals, steady tempo, no big drops",
  }),
  custom: Object.freeze({
    id: "custom",
    label: "自訂系列",
    driveLibraryPath: "_共用素材/music/custom",
    sfxSetName: "custom-flow",
    bedMix: Object.freeze({ gainDb: -20, duckDb: -10, maxBedLufs: -24, targetMinSec: 60 }),
    styleGuide: "clean instrumental background music",
  }),
});

export function getSeriesPreset(series = "curio") {
  const key = String(series || "curio").trim().toLowerCase();
  const preset = SERIES_PRESETS[key];
  if (!preset) {
    throw new Error(
      `Unknown series "${series}". Expected one of: ${Object.keys(SERIES_PRESETS).join(", ")}.`,
    );
  }
  return preset;
}

/**
 * Resolves the local runtime directory storing isolated Chrome profiles,
 * job snapshots, and per-profile lock files.
 */
export function resolveRuntimeHome({ env = process.env, platform = process.platform, homedir = os.homedir() } = {}) {
  if (env.MOKAAIR_FLOW_MUSIC_HOME && env.MOKAAIR_FLOW_MUSIC_HOME.trim()) {
    return env.MOKAAIR_FLOW_MUSIC_HOME.trim();
  }
  if (platform === "win32") {
    const localAppData = env.LOCALAPPDATA || path.win32.join(env.USERPROFILE || homedir, "AppData", "Local");
    return path.win32.join(localAppData, "mokaair-flow-music");
  }
  return path.join(homedir, ".mokaair-flow-music");
}

export function sanitizeProfileName(profile = null) {
  const safe = String(profile || "default")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "_");
  return safe || "default";
}

export function resolveChromeProfilesRoot(runtimeHome = resolveRuntimeHome()) {
  return path.join(runtimeHome, "chrome-profiles");
}

export function resolveChromeProfileDir(runtimeHome = resolveRuntimeHome(), profile = null) {
  return path.join(resolveChromeProfilesRoot(runtimeHome), `profile_${sanitizeProfileName(profile)}`);
}

export function resolveProfileLockPath(runtimeHome = resolveRuntimeHome(), profile = null) {
  const safe = sanitizeProfileName(profile);
  return path.join(runtimeHome, safe === "default" ? "runtime.lock" : `runtime-${safe}.lock`);
}

export function resolveWorkLibraryRoot(repoRoot = REPO_ROOT) {
  return path.join(repoRoot, "work", "music-library");
}

/**
 * Resolves default local work base (`~/mokaair-work/videos`) where `_music/`
 * and `_sfx/` live for the Mokaair video assembly pipeline.
 */
export function resolveVideoWorkBase({ env = process.env, homedir = os.homedir() } = {}) {
  if (env.MOKAAIR_VIDEO_WORK_BASE && env.MOKAAIR_VIDEO_WORK_BASE.trim()) {
    return env.MOKAAIR_VIDEO_WORK_BASE.trim();
  }
  return path.join(homedir, "mokaair-work", "videos");
}

/**
 * Locates Google Chrome (or Edge fallback on Windows) for CDP automation.
 */
export function resolveChromeBinary({
  env = process.env,
  platform = process.platform,
  existsSync = fs.existsSync,
} = {}) {
  if (env.MOKAAIR_CHROME_BIN && env.MOKAAIR_CHROME_BIN.trim()) {
    return env.MOKAAIR_CHROME_BIN.trim();
  }
  if (platform === "win32") {
    const candidates = [
      path.win32.join(env.PROGRAMFILES || "C:\\Program Files", "Google", "Chrome", "Application", "chrome.exe"),
      path.win32.join(env["PROGRAMFILES(X86)"] || "C:\\Program Files (x86)", "Google", "Chrome", "Application", "chrome.exe"),
      path.win32.join(env.LOCALAPPDATA || "", "Google", "Chrome", "Application", "chrome.exe"),
      path.win32.join(env["PROGRAMFILES(X86)"] || "C:\\Program Files (x86)", "Microsoft", "Edge", "Application", "msedge.exe"),
      path.win32.join(env.PROGRAMFILES || "C:\\Program Files", "Microsoft", "Edge", "Application", "msedge.exe"),
    ];
    for (const candidate of candidates) {
      if (candidate && existsSync(candidate)) return candidate;
    }
    return null;
  }
  if (platform === "darwin") {
    const macCandidates = [
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ];
    for (const candidate of macCandidates) {
      if (existsSync(candidate)) return candidate;
    }
    return null;
  }
  for (const bin of [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ]) {
    if (existsSync(bin)) return bin;
  }
  return null;
}

/**
 * Detects whether a local Drive mount (`G:\我的雲端硬碟\AI\備份\AI劇`) is available.
 */
export function resolveLocalDriveAiDramaRoot({ env = process.env, existsSync = fs.existsSync } = {}) {
  if (env.VDRIVE_ROOT && env.VDRIVE_ROOT.trim() && existsSync(env.VDRIVE_ROOT.trim())) {
    return env.VDRIVE_ROOT.trim();
  }
  const candidates = [
    "G:\\我的雲端硬碟\\AI\\備份\\AI劇",
    "G:\\My Drive\\AI\\備份\\AI劇",
    "/content/drive/MyDrive/AI/備份/AI劇",
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

/**
 * Detects whether a path sits inside OneDrive (Windows) or macOS TCC folders.
 */
export function detectSyncFolderHazard(targetPath, platform = process.platform) {
  const normalized = String(targetPath || "").replace(/\\/g, "/").toLowerCase();
  if (platform === "win32" && normalized.includes("/onedrive")) {
    return "Path is inside a OneDrive-synced folder; move it to a local folder such as C:\\dev\\travel_scanner or %LOCALAPPDATA%\\mokaair-flow-music.";
  }
  if (platform === "darwin" && /\/(desktop|documents|downloads)(\/|$)/.test(normalized)) {
    return "Path is inside a macOS protected folder (Desktop/Documents/Downloads); move it under your home directory.";
  }
  return null;
}
