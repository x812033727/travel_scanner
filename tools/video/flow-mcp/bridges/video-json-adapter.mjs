/**
 * Bidirectional bridge between Mokaair's `video.json` drama/shorts/explainer
 * scripts and Google Flow MCP (`flow-shot-list.json`, `cast.json`, and
 * `flow-clips/import-bridge.json`).
 *
 * Implements:
 *   - Reading `characters[]` and `scenes[]` (`camera`, `prompt`, `motion`,
 *     `characters`, `end_frame`, `data.source`, `visual: "still"`, `edit_from`,
 *     `continue_from`)
 *   - Stripping H3-specific `<Picture N>` tokens into natural Flow wording
 *     (shorts-PRODUCTION-ROUTES.md §3)
 *   - Auto-appending silent-comedy audio guard for zero-dialogue shorts
 *   - Emitting ready-to-run `clips import` commands and `edit/plan.json` cues
 */

import path from "node:path";
import {
  DEFAULT_VIDEO_DURATION_SEC,
  DEFAULT_VIDEO_MODEL,
  SILENT_COMEDY_AUDIO_GUARD,
  getSeriesPreset,
} from "../config.mjs";

const H3_PICTURE_TAG_RE = /(?:shown\s+in\s+)?<Picture\s*\d+>/gi;

export function sanitizeH3TagsForFlow(text) {
  if (!text || typeof text !== "string") return "";
  return text.replace(H3_PICTURE_TAG_RE, "from the starting frame").replace(/\s{2,}/g, " ").trim();
}

export function applySilentAudioGuard(prompt, { enabled = false } = {}) {
  const clean = sanitizeH3TagsForFlow(prompt);
  if (!enabled || !clean) return clean;
  if (/zero spoken dialogue|no spoken dialogue/i.test(clean)) return clean;
  return `${clean} ${SILENT_COMEDY_AUDIO_GUARD}`;
}

function inferSeriesFromVideoJson(videoJson, explicitSeries = null) {
  if (explicitSeries) return explicitSeries;
  const slug = String(videoJson?.slug || "").toLowerCase();
  const kind = String(videoJson?.kind || "").toLowerCase();
  const aspect = String(videoJson?.aspect || videoJson?.aspect_ratio || "").trim();

  if (slug.startsWith("sothatswhy-")) return "sothatswhy";
  if (slug.startsWith("curio-")) return "curio";
  if (kind === "short" || kind === "shorts" || slug.startsWith("shorts-")) return "shorts";
  if (aspect === "9:16") return "drama-9x16";
  if (kind === "drama" || kind === "anime" || kind === "animation") return "drama-16x9";
  return "drama-16x9";
}

/**
 * Converts a Mokaair `video.json` into a normalized `{ shotList, cast }` pair
 * ready for `flow_preflight_shotlist` -> `flow_generate_stills` -> `flow_generate_clips`.
 */
export function convertVideoJsonToFlowSpec(
  videoJson,
  {
    series = null,
    defaultModel = DEFAULT_VIDEO_MODEL,
    defaultDurationSec = DEFAULT_VIDEO_DURATION_SEC,
    silentAudioGuard = null,
  } = {},
) {
  if (!videoJson || typeof videoJson !== "object") {
    throw new Error("videoJson must be a valid JSON object.");
  }

  const effectiveSeries = inferSeriesFromVideoJson(videoJson, series);
  const preset = getSeriesPreset(effectiveSeries);
  const useSilentGuard =
    silentAudioGuard != null
      ? Boolean(silentAudioGuard)
      : preset.audioPolicy === "silent_with_guard" || videoJson.silent === true;

  // Build Cast map from videoJson.characters (supports array or object map)
  const castCharacters = {};
  const rawChars = Array.isArray(videoJson.characters)
    ? videoJson.characters
    : videoJson.characters && typeof videoJson.characters === "object"
      ? Object.entries(videoJson.characters).map(([id, val]) => ({ id, ...(val || {}) }))
      : [];

  for (const ch of rawChars) {
    const id = String(ch.id || ch.name || "").trim();
    if (!id) continue;
    castCharacters[id] = {
      id,
      name: ch.name || id,
      appearance: ch.appearance || ch.sheet_prompt || "",
      refs: Array.isArray(ch.refs) ? ch.refs : ch.sheet ? [ch.sheet] : [],
      looks: ch.looks && typeof ch.looks === "object" ? ch.looks : {},
      noAccessories: Array.isArray(ch.no_accessories) ? ch.no_accessories : [],
      voice: ch.voice || null,
      flowEntityId: ch.flow_entity_id || null,
      flowEntityName: ch.flow_entity_name || null,
    };
  }

  const scenes = Array.isArray(videoJson.scenes) ? videoJson.scenes : [];
  const shots = [];

  for (let i = 0; i < scenes.length; i += 1) {
    const scene = scenes[i] || {};
    const data = scene.data && typeof scene.data === "object" ? scene.data : {};
    const shotId = String(scene.id || data.id || `s${String(i + 1).padStart(2, "0")}`);
    const chapter = String(scene.chapter || data.chapter || "main");

    const sceneChars = Array.isArray(data.characters)
      ? data.characters.map(String)
      : Array.isArray(scene.characters)
        ? scene.characters.map(String)
        : [];
    const track = sceneChars.length > 0 ? "character" : String(data.track || "scenery").toLowerCase();

    // Cut shot (`data.source`) reuses a previously bought clip for 0 Flow credits
    if (data.source) {
      shots.push({
        id: shotId,
        chapter,
        track,
        mode: "cut",
        source: String(data.source),
        characters: sceneChars,
        duration_sec: Number(data.duration_sec ?? scene.duration_sec ?? 2),
        note: `Cut from ${data.source} (0 Flow credits)`,
      });
      continue;
    }

    const isStill =
      scene.visual === "still" ||
      data.visual === "still" ||
      data.still === true ||
      scene.still === true;

    const camera = sanitizeH3TagsForFlow(data.camera || scene.camera || "");
    const basePrompt = sanitizeH3TagsForFlow(data.prompt || scene.prompt || "");
    const motion = sanitizeH3TagsForFlow(data.motion || scene.motion || "");
    const stillPrompt = [camera, basePrompt].filter(Boolean).join(". ");
    const rawVideoPrompt = [motion || basePrompt, camera].filter(Boolean).join(". ");
    const videoPrompt = isStill
      ? undefined
      : applySilentAudioGuard(rawVideoPrompt || stillPrompt, { enabled: useSilentGuard });

    const shot = {
      id: shotId,
      chapter,
      track,
      mode: isStill ? "still" : "clip",
      characters: sceneChars,
      character_looks: data.character_looks || scene.character_looks || undefined,
      still_prompt: stillPrompt,
      ...(data.end_frame || data.end_still_prompt
        ? { end_still_prompt: sanitizeH3TagsForFlow(data.end_frame || data.end_still_prompt) }
        : {}),
      ...(videoPrompt ? { video_prompt: videoPrompt } : {}),
      ...(data.edit_from ? { edit_from: String(data.edit_from) } : {}),
      ...(data.continue_from ? { continue_from: String(data.continue_from) } : {}),
      ...(data.flow_model ? { model: String(data.flow_model) } : !isStill ? { model: defaultModel } : {}),
      ...(data.clip_duration_sec || data.buy_s
        ? { clip_duration_sec: Number(data.clip_duration_sec ?? data.buy_s) }
        : !isStill
          ? { clip_duration_sec: defaultDurationSec }
          : {}),
      ...(data.duration_sec || scene.duration_sec
        ? { duration_sec: Number(data.duration_sec ?? scene.duration_sec) }
        : {}),
      ...(Array.isArray(data.refs) ? { refs: data.refs } : {}),
      ...(data.r2v === true ? { video_mode: "r2v" } : {}),
    };

    shots.push(shot);
  }

  return {
    series: preset.id,
    shotList: {
      schemaVersion: 2,
      series: preset.id,
      slug: videoJson.slug || null,
      sourceFormat: "video.json",
      silentAudioGuard: useSilentGuard,
      shots,
    },
    cast: {
      schemaVersion: 1,
      series: preset.id,
      characters: castCharacters,
    },
    stats: {
      totalShots: shots.length,
      clips: shots.filter((s) => s.mode === "clip").length,
      stills: shots.filter((s) => s.mode === "still").length,
      cuts: shots.filter((s) => s.mode === "cut").length,
      charactersCount: Object.keys(castCharacters).length,
    },
  };
}

/**
 * Generates an `import-bridge.json` artifact mapping every completed Flow clip
 * (and cut/still) to both `tools/video/cli.mjs clips import` commands and
 * `edit/plan.json` cues (with recommended trim windows from hard-cut QC).
 */
export function buildImportBridge({ slug, series, clipsManifest = {}, shots = [] }) {
  const clipsMap = clipsManifest.clips || {};
  const entries = [];

  for (let i = 0; i < shots.length; i += 1) {
    const shot = shots[i];
    const shotId = String(shot.id || shot.shot_id || `s${String(i + 1).padStart(2, "0")}`);
    const mode = String(shot.mode || "still").toLowerCase();
    const clip = clipsMap[shotId];

    if (mode === "cut") {
      entries.push({
        shotId,
        mode: "cut",
        sourceShotId: shot.source || null,
        credits: 0,
        importCommand: null,
      });
      continue;
    }

    if (mode === "still" || !clip) {
      entries.push({
        shotId,
        mode,
        ready: Boolean(clip),
        filePath: clip?.upscaledPath || null,
        importCommand: null,
      });
      continue;
    }

    const activePath = clip.upscaledPath || clip.rawPath;
    const credits = clip.credits ?? 12;
    const durationSec = clip.durationSec ?? 4;
    const model = clip.model || DEFAULT_VIDEO_MODEL;
    const importCommand = `node tools/video/cli.mjs clips import --slug ${slug} --shot ${shotId} --file "${activePath}" --provider external --note "route=google-flow-mcp model=${model} credits=${credits} dur=${durationSec}s"`;

    entries.push({
      shotId,
      mode: "clip",
      ready: true,
      selectedTake: clip.selectedTake ?? clip.takes?.length ?? 1,
      filePath: activePath,
      rawPath: clip.rawPath || null,
      rawAudioPath: clip.rawAudioPath || null,
      sha256: clip.upscaledSha256 || clip.rawSha256 || null,
      model,
      credits,
      durationSec,
      qc: clip.qc || null,
      recommendedEdit: clip.qc?.recommendedTrim || { inSec: 0, durSec: durationSec, keepCuts: false },
      importCommand,
    });
  }

  return {
    schemaVersion: 1,
    slug,
    series,
    generatedAt: new Date().toISOString(),
    readyClips: entries.filter((e) => e.mode === "clip" && e.ready).length,
    cutShots: entries.filter((e) => e.mode === "cut").length,
    entries,
  };
}

/**
 * Formats the exact Google Drive `vdrive push-episode` command for both
 * explainers (`<分類>/<代碼>`) and AI dramas (`第0XX集` / `Shorts/<系列>`).
 */
export function buildDrivePushCommand({ slug, series, workdir, dramaName = null, episodeLabel = null }) {
  const preset = getSeriesPreset(series);
  const safeWorkdir = path.resolve(workdir);
  if (preset.id === "shorts") {
    return `npm run vdrive -- push-episode --series shorts --path "${dramaName || "<系列名>"}/${slug}" --from "${safeWorkdir}"`;
  }
  if (preset.kind === "drama") {
    const targetSeries = dramaName || "<劇名代碼如 zhong-tian-qu-qi / tai-nainai>";
    const ep = episodeLabel || "第0XX集";
    return `npm run vdrive -- push-episode --series ${targetSeries} --path "${ep}/製作檔/${slug}" --from "${safeWorkdir}"`;
  }
  return `npm run vdrive -- push-episode --series ${preset.id} --path "<分類>/<代碼>/製作檔/${slug}" --from "${safeWorkdir}"`;
}
