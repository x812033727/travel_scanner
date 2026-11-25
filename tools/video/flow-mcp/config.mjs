/**
 * Configuration, series presets, and cross-platform path resolvers for
 * Mokaair's local Google Flow MCP server (`tools/video/flow-mcp`).
 *
 * Aligns with Google Drive SSOT rules (`FLOW-PRODUCTION-RULES.md` and
 * `CURIO-FLOW-CHECKLIST.md`, 2026-11-25 Route B).
 */

import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const REPO_ROOT = path.resolve(fileURLToPath(new URL("../../../", import.meta.url)));

export const MCP_SERVER_NAME = "mokaair-flow";
export const MCP_SERVER_VERSION = "1.0.0";

export const DEFAULT_IMAGE_MODEL = "nano2.1";
export const DEFAULT_VIDEO_MODEL = "omni-1.2-flash";
export const DEFAULT_VIDEO_DURATION_SEC = 4;
export const DEFAULT_VIDEO_RESOLUTION = "720p";
export const DEFAULT_CLIP_CREDITS = 12;
export const DEFAULT_MAX_CREDITS_PER_CLIP = 15;

export const SERIES_PRESETS = Object.freeze({
  sothatswhy: Object.freeze({
    id: "sothatswhy",
    label: "原來如此事務所",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 500,
    budgetHardCap: 500,
    clipCredits: DEFAULT_CLIP_CREDITS,
    minDynamicRatio: 0.45,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    canonRuleFiles: Object.freeze([
      "原來如此事務所/chief-canon-v2.png",
      "原來如此事務所/kid-canon-v2.png",
    ]),
    childReplacement: "the cute 2D cartoon mascot character in a navy coat with yellow hood",
  }),
  curio: Object.freeze({
    id: "curio",
    label: "奇聞檔案局",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 550,
    budgetHardCap: 600,
    clipCredits: DEFAULT_CLIP_CREDITS,
    minDynamicRatio: 0.4,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    canonRuleFiles: Object.freeze([
      "奇聞檔案局/ada-canon-v2.png",
    ]),
    childReplacement: "a young adult observer in period-appropriate attire",
  }),
  shorts: Object.freeze({
    id: "shorts",
    label: "零台詞 Shorts 短劇",
    aspect: "9:16",
    targetStillWidth: 768,
    targetStillHeight: 1376,
    budgetSoftCap: 200,
    budgetHardCap: 240,
    clipCredits: DEFAULT_CLIP_CREDITS,
    minDynamicRatio: 0.7,
    maxConsecutiveStills: 2,
    maxStillDurationSec: 6,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a stylized 2D cartoon mascot character",
  }),
  custom: Object.freeze({
    id: "custom",
    label: "自訂系列",
    aspect: "16:9",
    targetStillWidth: 1376,
    targetStillHeight: 768,
    budgetSoftCap: 400,
    budgetHardCap: 600,
    clipCredits: DEFAULT_CLIP_CREDITS,
    minDynamicRatio: 0.4,
    maxConsecutiveStills: 3,
    maxStillDurationSec: 8,
    canonRuleFiles: Object.freeze([]),
    childReplacement: "a stylized adult character",
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
 * Resolves the dedicated local runtime directory for Chrome profile metadata,
 * job snapshots, and the cross-client `runtime.lock` file.
 * Kept outside OneDrive-synced folders (Desktop/Documents) on Windows.
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

export function resolveWorkEpisodesRoot(repoRoot = REPO_ROOT) {
  return path.join(repoRoot, "work", "video-episodes");
}

export function resolveRulesCacheRoot(repoRoot = REPO_ROOT) {
  return path.join(repoRoot, ".cache", "video-drive", "rules", "_規則");
}

/**
 * Detects whether a Windows path sits inside OneDrive, Desktop, or Documents
 * where cloud placeholders or macOS TCC permissions can break Chrome profiles
 * or MCP launches.
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
