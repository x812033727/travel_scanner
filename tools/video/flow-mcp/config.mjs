/**
 * Configuration, series presets (explainers + AI dramas + vertical shorts),
 * credit estimation table, and cross-platform path resolvers for Mokaair's
 * local Google Flow MCP server (`tools/video/flow-mcp`).
 *
 * Aligns with Google Drive SSOT rules:
 *   - FLOW-PRODUCTION-RULES.md & CURIO-FLOW-CHECKLIST.md (explainers)
 *   - shorts-PRODUCTION-ROUTES.md & AI-DRAMA-DRIVE.md (AI dramas & shorts)
 */

import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const REPO_ROOT = path.resolve(fileURLToPath(new URL("../../../", import.meta.url)));

export const MCP_SERVER_NAME = "mokaair-flow";
export const MCP_SERVER_VERSION = "2.0.0";

export const DEFAULT_IMAGE_MODEL = "nano2.1";
export const DEFAULT_VIDEO_MODEL = "omni-1.2-flash";
export const DEFAULT_VIDEO_DURATION_SEC = 4;
export const DEFAULT_VIDEO_RESOLUTION = "720p";
export const DEFAULT_CLIP_CREDITS = 12;
export const DEFAULT_MAX_CREDITS_PER_CLIP = 25;
export const DEFAULT_MAX_CLIP_TAKES = 2;
export const DEFAULT_PILOT_MAX_SHOTS = 3;

export const SILENT_COMEDY_AUDIO_GUARD =
  "Silent film visual comedy: zero spoken dialogue, no voices, no gibberish speech, no background music; only subtle natural foley sounds.";

export const SERIES_PRESETS = Object.freeze({
  sothatswhy: Object.freeze({
    id: "sothatswhy",
    label: "原來如此事務所",
    kind: "explainer",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 500,
    budgetHardCap: 500,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.45,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    safetyProfile: "explainer",
    audioPolicy: "strip", // -an
    safeZoneOverlay: false,
    canonRuleFiles: Object.freeze([
      "原來如此事務所/chief-canon-v2.png",
      "原來如此事務所/kid-canon-v2.png",
    ]),
    childReplacement: "the cute 2D cartoon mascot character in a navy coat with yellow hood",
    drivePathTemplate: "<分類>/<代碼>/製作檔/<slug>",
  }),
  curio: Object.freeze({
    id: "curio",
    label: "奇聞檔案局",
    kind: "explainer",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 550,
    budgetHardCap: 600,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.4,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    safetyProfile: "explainer",
    audioPolicy: "strip",
    safeZoneOverlay: false,
    canonRuleFiles: Object.freeze([
      "奇聞檔案局/ada-canon-v2.png",
    ]),
    childReplacement: "a young adult observer in period-appropriate attire",
    drivePathTemplate: "<分類>/<代碼>/製作檔/<slug>",
  }),
  "drama-16x9": Object.freeze({
    id: "drama-16x9",
    label: "AI 劇（橫式 16:9 長篇漫劇／真人劇）",
    kind: "drama",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 800,
    budgetHardCap: 1200,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.65,
    maxConsecutiveStills: 2,
    maxStillDurationSec: 6,
    safetyProfile: "drama",
    audioPolicy: "extract_sidecar", // clean -an master + raw-audio/*.wav sidecar
    safeZoneOverlay: false,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a young adult villager in period attire",
    drivePathTemplate: "第0XX集/製作檔/<slug>",
  }),
  "drama-9x16": Object.freeze({
    id: "drama-9x16",
    label: "AI 劇（直式 9:16 短劇／漫劇／真人短劇）",
    kind: "drama",
    aspect: "9:16",
    targetStillWidth: 768,
    targetStillHeight: 1376,
    budgetSoftCap: 300,
    budgetHardCap: 500,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.75,
    maxConsecutiveStills: 2,
    maxStillDurationSec: 5,
    safetyProfile: "drama",
    audioPolicy: "extract_sidecar",
    safeZoneOverlay: true,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a young adult character in modern casual attire",
    drivePathTemplate: "第0XX集/製作檔/<slug>",
  }),
  shorts: Object.freeze({
    id: "shorts",
    label: "零台詞 Shorts 短劇（9:16）",
    kind: "shorts",
    aspect: "9:16",
    targetStillWidth: 768,
    targetStillHeight: 1376,
    budgetSoftCap: 120,
    budgetHardCap: 240,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.7,
    maxConsecutiveStills: 2,
    maxStillDurationSec: 5,
    safetyProfile: "drama",
    audioPolicy: "silent_with_guard",
    safeZoneOverlay: true,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a stylized 2D cartoon mascot character",
    drivePathTemplate: "<系列>/<slug>",
  }),
  custom: Object.freeze({
    id: "custom",
    label: "自訂系列",
    kind: "custom",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 500,
    budgetHardCap: 1000,
    clipCredits: DEFAULT_CLIP_CREDITS,
    maxClipTakes: DEFAULT_MAX_CLIP_TAKES,
    minDynamicRatio: 0.4,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    safetyProfile: "drama",
    audioPolicy: "extract_sidecar",
    safeZoneOverlay: false,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a stylized adult character",
    drivePathTemplate: "<分類>/<slug>",
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
 * Estimates Flow credits for a single clip or extend operation by model + duration.
 * Omni 1.2 Flash bills 12 credits at 4s (3 credits/sec across 3-15s).
 * Veo models bill per-tier (lite=10, fast=20, quality=100).
 */
export function estimateClipCredits({
  model = DEFAULT_VIDEO_MODEL,
  durationSec = DEFAULT_VIDEO_DURATION_SEC,
  creditsOverride = null,
} = {}) {
  if (creditsOverride != null && Number.isFinite(Number(creditsOverride))) {
    return Math.max(0, Math.round(Number(creditsOverride)));
  }
  const m = String(model || DEFAULT_VIDEO_MODEL).trim().toLowerCase();
  const sec = Math.max(3, Math.min(15, Number(durationSec) || DEFAULT_VIDEO_DURATION_SEC));

  if (m === "omni-1.2-flash" || m === "omni-1.2" || m === "omni-flash") {
    return Math.round(sec * 3);
  }
  if (m === "veo-lite" || m === "veo-lite-lp") {
    return 10;
  }
  if (m === "veo-fast") {
    return 20;
  }
  if (m === "veo-quality") {
    return 100;
  }
  return DEFAULT_CLIP_CREDITS;
}

/**
 * Resolves the dedicated local runtime directory for Chrome profile metadata,
 * job snapshots, and per-profile `runtime-<profile>.lock` files.
 */
export function resolveRuntimeHome({ env = process.env, platform = process.platform, homedir = os.homedir() } = {}) {
  if (env.MOKAAIR_FLOW_HOME && env.MOKAAIR_FLOW_HOME.trim()) {
    return env.MOKAAIR_FLOW_HOME.trim();
  }
  if (platform === "win32") {
    const localAppData = env.LOCALAPPDATA || path.win32.join(env.USERPROFILE || homedir, "AppData", "Local");
    return path.win32.join(localAppData, "mokaair-flow");
  }
  return path.join(homedir, ".mokaair-flow");
}

export function resolveProfileLockPath(runtimeHome, profile = null) {
  const safeProfile = String(profile || "default")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "_") || "default";
  return path.join(runtimeHome, safeProfile === "default" ? "runtime.lock" : `runtime-${safeProfile}.lock`);
}

export function resolveWorkEpisodesRoot(repoRoot = REPO_ROOT) {
  return path.join(repoRoot, "work", "video-episodes");
}

export function resolveRulesCacheRoot(repoRoot = REPO_ROOT) {
  return path.join(repoRoot, ".cache", "video-drive", "rules", "_規則");
}

/**
 * Detects whether a path sits inside OneDrive (Windows) or TCC-protected
 * Desktop/Documents/Downloads (macOS).
 */
export function detectSyncFolderHazard(targetPath, platform = process.platform) {
  const normalized = String(targetPath || "").replace(/\\/g, "/").toLowerCase();
  if (platform === "win32" && normalized.includes("/onedrive")) {
    return "Path is inside a OneDrive-synced folder; move it to a local folder such as C:\\dev\\travel_scanner or %LOCALAPPDATA%\\mokaair-flow.";
  }
  if (platform === "darwin" && /\/(desktop|documents|downloads)(\/|$)/.test(normalized)) {
    return "Path is inside a macOS protected folder (Desktop/Documents/Downloads); move it under your home directory.";
  }
  return null;
}
