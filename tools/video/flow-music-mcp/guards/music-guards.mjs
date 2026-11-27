/**
 * Mokaair production guards for Flow Music:
 *   1. Route B path boundary (`work/music-library/<collection>/` only; blocks tracked repo dirs).
 *   2. `MUSIC_TRACK` filename sanitizer + automatic `-takeN` collision protection.
 *   3. Prompt mixing & copyright preflight (`preflightMusicPlan`) enforcing instrumental
 *      bed discipline, vocal-conflict warnings, and Lyria 3.5 duration reminders.
 *   4. Atomic JSON + SHA-256 helpers.
 */

import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {
  BED_MIXING_SUFFIX,
  DEFAULT_DOWNLOAD_FORMAT,
  MUSIC_TRACK_RE,
  REPO_ROOT,
  SUPPORTED_DOWNLOAD_FORMATS,
  TRACK_KINDS,
  getSeriesPreset,
  resolveWorkLibraryRoot,
} from "../config.mjs";

const COLLECTION_RE = /^[a-z0-9][a-z0-9._-]{1,79}$/;

const FORBIDDEN_REPO_PREFIXES = [
  "docs/videos",
  "docs/",
  "apps/",
  "tools/",
  "ops/",
  "tasks/",
  ".github/",
  ".agents/",
  ".claude/",
];

const VOCAL_CONFLICT_PATTERNS = [
  /\b(vocals?|singing|singer|vocalist|lyrics?|rap|rapper|choir|choral|opera singer|spoken word|chanting)\b/i,
  /(人聲|歌詞|演唱|合唱|主唱|饒舌|rap)/i,
];

const DROP_CONFLICT_PATTERNS = [
  /\b(massive drop|bass drop|edm drop|dubstep drop|jump scare|loud explosion|screaming)\b/i,
  /(大爆點|重低音炸裂|驚嚇音效)/i,
];

const COPYRIGHT_ARTIST_PATTERNS = [
  /\b(taylor swift|billie eilish|hans zimmer|john williams|joe hisaishi|ludovico einaudi|studio ghibli|disney|marvel|star wars|harry potter|pokemon|nintendo|final fantasy|zelda|attack on titan|demon slayer|jay chou)\b/i,
  /(周杰倫|久石讓|迪士尼|宮崎駿|吉卜力|漫威|星際大戰|哈利波特|寶可夢|任天堂)/i,
];

export function atomicWriteJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tmpPath = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  fs.writeFileSync(tmpPath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.renameSync(tmpPath, filePath);
}

export function readJsonSafe(filePath, fallback = null) {
  if (!fs.existsSync(filePath)) return fallback;
  try {
    const raw = fs.readFileSync(filePath, "utf8").trim();
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function sha256File(filePath) {
  const hash = createHash("sha256");
  hash.update(fs.readFileSync(filePath));
  return hash.digest("hex");
}

export function sanitizeCollectionSlug(collection) {
  const clean = String(collection || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  if (!COLLECTION_RE.test(clean)) {
    throw new Error(
      `Invalid collection slug "${collection}". Must match ${COLLECTION_RE} (lowercase letters, digits, ., _, -).`,
    );
  }
  return clean;
}

export function sanitizeCueBaseName(name) {
  const clean = String(name || "")
    .trim()
    .toLowerCase()
    .replace(/\.(?:m4a|mp3|wav|flac|ogg)$/i, "")
    .replace(/\(take\s*\d+\)/gi, "")
    .replace(/[^a-z0-9._-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^[-._]+|[-._]+$/g, "");
  return clean || "track";
}

/**
 * Builds a Mokaair-compliant `<series>-<kind>-<slug>` cue identifier.
 */
export function buildCueName({ series = "curio", kind = "bed", name }) {
  const s = sanitizeCueBaseName(series);
  const k = TRACK_KINDS.includes(String(kind || "").toLowerCase()) ? String(kind).toLowerCase() : "bed";
  const raw = sanitizeCueBaseName(name);
  const prefix = `${s}-${k}-`;
  if (raw.startsWith(prefix)) return raw.slice(0, 48);
  const strippedSeries = raw.startsWith(`${s}-`) ? raw.slice(s.length + 1) : raw;
  const strippedKind = strippedSeries.startsWith(`${k}-`) ? strippedSeries.slice(k.length + 1) : strippedSeries;
  return `${prefix}${strippedKind || "untitled"}`.slice(0, 48);
}

/**
 * Picks the next non-colliding `<cue>-take<N>.<ext>` filename inside a directory
 * (preventing the Flow Music duplicate-title overwrite bug).
 */
export function allocateTrackFilename({
  dir,
  cue,
  format = DEFAULT_DOWNLOAD_FORMAT,
  existingFiles = null,
} = {}) {
  const ext = SUPPORTED_DOWNLOAD_FORMATS.includes(String(format).toLowerCase())
    ? String(format).toLowerCase()
    : DEFAULT_DOWNLOAD_FORMAT;
  const taken = new Set(
    (existingFiles || (dir && fs.existsSync(dir) ? fs.readdirSync(dir) : [])).map((f) => f.toLowerCase()),
  );
  const baseCue = sanitizeCueBaseName(cue).slice(0, 50);

  for (let take = 1; take <= 99; take += 1) {
    const candidate = `${baseCue}-take${take}.${ext}`;
    if (!taken.has(candidate.toLowerCase())) {
      if (!MUSIC_TRACK_RE.test(candidate)) {
        throw new Error(`Allocated filename "${candidate}" violates MUSIC_TRACK_RE.`);
      }
      return { filename: candidate, take, format: ext };
    }
  }
  throw new Error(`Too many takes (>=99) already exist for cue "${baseCue}".`);
}

/**
 * Enforces Route B: collection outputs MUST live under gitignored
 * `work/music-library/<collection>/` (never inside tracked repo folders).
 */
export function resolveCollectionPaths(collection, { repoRoot = REPO_ROOT, workdir = null } = {}) {
  const slug = sanitizeCollectionSlug(collection);
  const resolvedRepo = path.resolve(repoRoot);
  const libraryRoot = path.resolve(resolveWorkLibraryRoot(resolvedRepo));
  const targetDir = workdir ? path.resolve(workdir) : path.join(libraryRoot, slug);

  const relFromRepo = path.relative(resolvedRepo, targetDir).replace(/\\/g, "/");
  const insideRepo = relFromRepo && !relFromRepo.startsWith("..") && !path.isAbsolute(relFromRepo);

  if (insideRepo) {
    for (const forbidden of FORBIDDEN_REPO_PREFIXES) {
      if (relFromRepo === forbidden.replace(/\/$/, "") || relFromRepo.startsWith(forbidden)) {
        throw new Error(
          `Route B boundary violation: refusing to write music collection inside tracked repo path "${relFromRepo}". Use work/music-library/<collection>/ instead.`,
        );
      }
    }
    if (!relFromRepo.startsWith("work/music-library/") && !relFromRepo.startsWith("work/video-episodes/")) {
      throw new Error(
        `Route B boundary violation: path "${relFromRepo}" is inside the git repo outside gitignored work/music-library/ or work/video-episodes/.`,
      );
    }
  }

  return {
    collection: slug,
    collectionDir: targetDir,
    rawDir: path.join(targetDir, "raw"),
    cutsDir: path.join(targetDir, "cuts"),
    manifestFile: path.join(targetDir, "manifest.json"),
    planFile: path.join(targetDir, "music-plan.json"),
    galleryFile: path.join(targetDir, "qa-gallery.html"),
    slicesFile: path.join(targetDir, "slices.json"),
  };
}

/**
 * Preflights a batch of Flow Music track prompts against Mokaair mixing rules,
 * vocal-conflict checks, copyright guardrails, and Lyria 3.5 quirks.
 */
export function preflightMusicPlan(plan, { series = "curio", allowVocals = false, autoEnforceBedGuard = true } = {}) {
  const preset = getSeriesPreset(series);
  const tracks = Array.isArray(plan) ? plan : Array.isArray(plan?.tracks) ? plan.tracks : [];
  const blockers = [];
  const warnings = [];
  const normalizedTracks = [];
  const seenCues = new Map();

  if (tracks.length === 0) {
    blockers.push({ code: "empty_plan", message: "Music plan contains 0 tracks." });
  }

  for (let i = 0; i < tracks.length; i += 1) {
    const raw = tracks[i] || {};
    const kind = String(raw.kind || "bed").trim().toLowerCase();
    if (!TRACK_KINDS.includes(kind)) {
      blockers.push({
        index: i,
        code: "invalid_kind",
        message: `Track #${i + 1} has invalid kind "${raw.kind}". Expected one of: ${TRACK_KINDS.join(", ")}.`,
      });
      continue;
    }

    const baseName = raw.cue || raw.name || raw.title || `track-${i + 1}`;
    const cue = buildCueName({ series: preset.id, kind, name: baseName });
    const dupCount = (seenCues.get(cue) || 0) + 1;
    seenCues.set(cue, dupCount);
    if (dupCount > 1) {
      warnings.push({
        index: i,
        cue,
        code: "duplicate_cue_name",
        message: `Cue "${cue}" appears ${dupCount} times; downloads will auto-suffix -take1/-take2/-take3 to avoid overwriting.`,
      });
    }

    let prompt = String(raw.prompt || raw.sound_prompt || "").trim();
    if (!prompt) {
      blockers.push({ index: i, cue, code: "empty_prompt", message: `Track "${cue}" has an empty prompt.` });
      continue;
    }

    // Copyright check (hard blocker)
    for (const pattern of COPYRIGHT_ARTIST_PATTERNS) {
      const m = prompt.match(pattern);
      if (m) {
        blockers.push({
          index: i,
          cue,
          code: "copyright_reference",
          term: m[0],
          message: `Track "${cue}" references copyrighted artist/IP "${m[0]}". Replace with generic musical style descriptors.`,
        });
      }
    }

    const trackAllowVocals = Boolean(raw.allowVocals ?? allowVocals);

    // Bed-specific narration mixing rules
    if (kind === "bed") {
      if (!trackAllowVocals) {
        for (const pattern of VOCAL_CONFLICT_PATTERNS) {
          const m = prompt.match(pattern);
          if (m && !/\bno\s+vocals?\b/i.test(prompt.slice(Math.max(0, m.index - 4), m.index + m[0].length))) {
            blockers.push({
              index: i,
              cue,
              code: "bed_vocal_conflict",
              term: m[0],
              message: `Background bed "${cue}" mentions "${m[0]}". Narration beds must be instrumental (or pass allowVocals: true explicitly).`,
            });
          }
        }
      }

      for (const pattern of DROP_CONFLICT_PATTERNS) {
        const m = prompt.match(pattern);
        if (m && !/\bno\s+(?:big\s+)?drops?\b/i.test(prompt.slice(Math.max(0, m.index - 6), m.index + m[0].length))) {
          warnings.push({
            index: i,
            cue,
            code: "bed_drop_warning",
            term: m[0],
            message: `Background bed "${cue}" contains "${m[0]}", which may disrupt narration ducking (gain_db ${preset.bedMix.gainDb}, duck_db ${preset.bedMix.duckDb}).`,
          });
        }
      }

      const hasInstrumentalMarker = /\b(instrumental|no vocals?|without vocals?)\b/i.test(prompt);
      if (!hasInstrumentalMarker && !trackAllowVocals) {
        if (autoEnforceBedGuard) {
          prompt = `${prompt.replace(/[.,;\s]+$/, "")}, ${BED_MIXING_SUFFIX}`;
        } else {
          warnings.push({
            index: i,
            cue,
            code: "missing_instrumental_guard",
            message: `Background bed "${cue}" omits "instrumental / no vocals" guardrail.`,
          });
        }
      }
    }

    if (kind === "cue") {
      warnings.push({
        index: i,
        cue,
        code: "lyria_cue_trim_reminder",
        message: `Lyria 3.5 typically generates ~40–65s for short cues; run music_detect_slices + music_cut to trim "${cue}" to your target 3–20s window.`,
      });
    }

    if (kind === "sfx") {
      warnings.push({
        index: i,
        cue,
        code: "lyria_sfx_slice_reminder",
        message: `Lyria 3.5 typically outputs multi-hit ~60s audio with silences for SFX; run music_detect_slices + music_cut + music_export_sfx_set after downloading "${cue}".`,
      });
    }

    normalizedTracks.push({
      cue,
      kind,
      title: String(raw.title || cue).trim(),
      prompt,
      lyrics: String(raw.lyrics || "").trim(),
      targetSeconds: raw.targetSeconds ?? (kind === "bed" ? 160 : kind === "cue" ? 8 : 2),
      takesRequested: Math.max(1, Math.min(4, Number(raw.takes || raw.takesRequested || 1))),
      instrumental: !trackAllowVocals,
      purpose: raw.purpose || "",
    });
  }

  return {
    ok: blockers.length === 0,
    series: preset.id,
    seriesLabel: preset.label,
    summary: {
      total: normalizedTracks.length,
      beds: normalizedTracks.filter((t) => t.kind === "bed").length,
      cues: normalizedTracks.filter((t) => t.kind === "cue").length,
      sfx: normalizedTracks.filter((t) => t.kind === "sfx").length,
      blockers: blockers.length,
      warnings: warnings.length,
    },
    aiDisclosureReminder:
      "All Flow Music (Lyria 3.5) tracks are AI-generated. Record ai_generated: true in manifest.json and check YouTube's altered/synthetic content rule before uploading.",
    blockers,
    warnings,
    normalizedTracks,
  };
}
