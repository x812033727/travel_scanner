/**
 * Mokaair pipeline integration & Route B Google Drive sync for Flow Music:
 *   1. Export approved SFX cuts into a validated v2 `_sfx/<set>/manifest.json`
 *      using Mokaair's own `sfxSetProblems()` from `tools/video/assemble/sfx.mjs`,
 *      and optionally run `node tools/video/cli.mjs assemble sfx-measure --set <set>`.
 *   2. Stage approved bed/cue tracks into `<workBase>/_music/` with strict
 *      `MUSIC_TRACK` naming + SHA-256 verification and emit the exact `video.json`
 *      `"music"` snippet.
 *   3. SHA-256 0-diff sync of a collection folder to Google Drive (local mount
 *      `G:\我的雲端硬碟\AI\備份\AI劇\...` or `rclone` fallback, 0 GitHub commits).
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { SFX_TARGET_LUFS, sfxSetProblems } from "../../assemble/sfx.mjs";
import {
  MUSIC_TRACK_RE,
  REPO_ROOT,
  getSeriesPreset,
  resolveLocalDriveAiDramaRoot,
  resolveVideoWorkBase,
} from "../config.mjs";
import { atomicWriteJson, sanitizeCueBaseName, sha256File } from "../guards/music-guards.mjs";

const AUDIO_EXT_RE = /\.(?:m4a|mp3|wav|flac|ogg)$/i;

/**
 * Exports approved SFX audio files into `<workBase>/_sfx/<set>/` with a v2
 * manifest validated directly by Mokaair's `sfxSetProblems()`.
 */
export function exportSfxV2Set({
  setName,
  soundsMap,
  workBase = resolveVideoWorkBase(),
  source = "Google Flow Music (Lyria 3.5)",
  license = "Flow Music paid subscription (owner-verified commercial rights; AI-generated)",
  runSfxMeasure = false,
  repoRoot = REPO_ROOT,
  spawnFn = spawnSync,
} = {}) {
  const safeSet = sanitizeCueBaseName(setName);
  const setDir = path.join(workBase, "_sfx", safeSet);
  fs.mkdirSync(setDir, { recursive: true });

  const manifestSounds = {};
  for (const [soundName, spec] of Object.entries(soundsMap || {})) {
    if (!spec?.filePath || !fs.existsSync(spec.filePath)) {
      throw new Error(`SFX sound "${soundName}" source file not found: ${spec?.filePath}`);
    }
    const ext = path.extname(spec.filePath).toLowerCase() || ".m4a";
    const destName = `${sanitizeCueBaseName(soundName)}${ext}`;
    const destPath = path.join(setDir, destName);
    if (path.resolve(spec.filePath) !== path.resolve(destPath)) {
      fs.copyFileSync(spec.filePath, destPath);
    }
    const entry = {
      file: destName,
      sha256: sha256File(destPath),
      target_lufs: spec.target_lufs ?? SFX_TARGET_LUFS[soundName] ?? -16,
      source: spec.source || source,
      license: spec.license || license,
      ai_generated: true,
    };
    if (Number.isFinite(spec.seconds) && spec.seconds > 0) entry.seconds = Number(spec.seconds.toFixed(3));
    if (Number.isFinite(spec.lufs_i)) entry.lufs_i = Number(spec.lufs_i.toFixed(1));
    if (Number.isFinite(spec.lufs_m)) entry.lufs_m = Number(spec.lufs_m.toFixed(1));
    if (Number.isFinite(spec.peak_dbtp)) entry.peak_dbtp = Number(spec.peak_dbtp.toFixed(1));
    if (spec.flow_music_id) entry.flow_music_id = spec.flow_music_id;
    manifestSounds[soundName] = entry;
  }

  const manifest = {
    manifest_version: 2,
    set: safeSet,
    created_at: new Date().toISOString(),
    source,
    license,
    ai_generated: true,
    sounds: manifestSounds,
  };

  const preMeasureProblems = sfxSetProblems(manifest, { measured: false });
  if (preMeasureProblems.length > 0) {
    return {
      ok: false,
      reason: "invalid_sfx_manifest",
      setDir,
      problems: preMeasureProblems,
    };
  }

  const manifestFile = path.join(setDir, "manifest.json");
  atomicWriteJson(manifestFile, manifest);

  let measureResult = null;
  if (runSfxMeasure) {
    const cliPath = path.join(repoRoot, "tools", "video", "cli.mjs");
    const res = spawnFn(process.execPath, [cliPath, "assemble", "sfx-measure", "--set", safeSet], {
      cwd: repoRoot,
      env: { ...process.env, MOKAAIR_VIDEO_WORK_BASE: workBase },
      encoding: "utf8",
      windowsHide: true,
    });
    measureResult = {
      exitCode: res.status ?? 1,
      stdout: (res.stdout || "").trim(),
      stderr: (res.stderr || "").trim(),
    };
  }

  const finalManifest = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
  const measuredProblems = sfxSetProblems(finalManifest, { measured: true });

  return {
    ok: measuredProblems.length === 0 || (!runSfxMeasure && preMeasureProblems.length === 0),
    set: safeSet,
    setDir,
    manifestFile,
    manifestSha256: sha256File(manifestFile),
    soundCount: Object.keys(manifestSounds).length,
    measuredProblems,
    measureResult,
    videoJsonSnippet: {
      sfx: {
        set: safeSet,
        sha256: sha256File(manifestFile),
      },
    },
  };
}

/**
 * Stages an approved music track into `<workBase>/_music/<trackName>` and
 * verifies SHA-256 so `video.json` can bind it directly.
 */
export function stageTrackForEpisode({
  sourceFile,
  targetFilename = null,
  workBase = resolveVideoWorkBase(),
  allowOverwrite = false,
} = {}) {
  if (!sourceFile || !fs.existsSync(sourceFile)) {
    throw new Error(`Track source file not found: ${sourceFile}`);
  }
  const ext = path.extname(sourceFile).toLowerCase() || ".m4a";
  const rawName = targetFilename || path.basename(sourceFile);
  const safeBase = sanitizeCueBaseName(rawName.replace(AUDIO_EXT_RE, ""));
  const finalName = `${safeBase}${ext}`;

  if (!MUSIC_TRACK_RE.test(finalName)) {
    throw new Error(`Target track filename "${finalName}" violates MUSIC_TRACK_RE.`);
  }

  const musicDir = path.join(workBase, "_music");
  fs.mkdirSync(musicDir, { recursive: true });
  const destPath = path.join(musicDir, finalName);

  if (fs.existsSync(destPath) && !allowOverwrite) {
    const srcHash = sha256File(sourceFile);
    const dstHash = sha256File(destPath);
    if (srcHash !== dstHash) {
      throw new Error(
        `Destination "${destPath}" already exists with a different SHA-256. Pass allowOverwrite: true or pick a distinct filename.`,
      );
    }
  } else {
    fs.copyFileSync(sourceFile, destPath);
  }

  const sha256 = sha256File(destPath);
  return {
    ok: true,
    track: finalName,
    destPath,
    sha256,
    videoJsonSnippet: {
      music: {
        track: finalName,
        sha256,
      },
    },
    aiDisclosureReminder:
      "This track was generated by Google Flow Music (Lyria 3.5). Check YouTube's altered/synthetic content disclosure rule before publishing.",
  };
}

/**
 * Syncs a local music collection directory to Google Drive with SHA-256 0-diff
 * verification (Route B: 0 GitHub commits).
 */
export function syncCollectionToDrive({
  collectionDir,
  series = "curio",
  driveSubdir = null,
  driveRoot = null,
  dryRun = false,
} = {}) {
  if (!collectionDir || !fs.existsSync(collectionDir)) {
    return { ok: false, reason: "missing_collection_dir", message: `Collection dir not found: ${collectionDir}` };
  }

  const preset = getSeriesPreset(series);
  const resolvedDriveRoot = driveRoot || resolveLocalDriveAiDramaRoot();
  const relDest = driveSubdir
    ? path.join(preset.driveLibraryPath, driveSubdir)
    : path.join(preset.driveLibraryPath, path.basename(collectionDir));

  if (!resolvedDriveRoot) {
    return {
      ok: false,
      reason: "drive_mount_not_found",
      message: "Local Google Drive mount (G:\\我的雲端硬碟\\AI\\備份\\AI劇) was not found. Set VDRIVE_ROOT or pass driveRoot explicitly.",
      suggestedRelDest: relDest.replace(/\\/g, "/"),
    };
  }

  const destDir = path.join(resolvedDriveRoot, relDest);
  const filesToCopy = [];

  const walk = (dir, prefix = "") => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.endsWith(".tmp")) continue;
      const full = path.join(dir, entry.name);
      const rel = prefix ? path.join(prefix, entry.name) : entry.name;
      if (entry.isDirectory()) {
        walk(full, rel);
      } else {
        filesToCopy.push({ rel: rel.replace(/\\/g, "/"), src: full, dst: path.join(destDir, rel) });
      }
    }
  };
  walk(collectionDir);

  if (dryRun) {
    return {
      ok: true,
      dryRun: true,
      destDir,
      fileCount: filesToCopy.length,
      files: filesToCopy.map((f) => f.rel),
    };
  }

  let copied = 0;
  let unchanged = 0;
  const mismatches = [];

  for (const item of filesToCopy) {
    fs.mkdirSync(path.dirname(item.dst), { recursive: true });
    const srcHash = sha256File(item.src);
    if (fs.existsSync(item.dst) && sha256File(item.dst) === srcHash) {
      unchanged += 1;
      continue;
    }
    fs.copyFileSync(item.src, item.dst);
    const dstHash = sha256File(item.dst);
    if (dstHash !== srcHash) {
      mismatches.push({ file: item.rel, srcHash, dstHash });
    } else {
      copied += 1;
    }
  }

  return {
    ok: mismatches.length === 0,
    destDir,
    totalFiles: filesToCopy.length,
    copied,
    unchanged,
    mismatches,
  };
}
