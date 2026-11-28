/**
 * Full-axis prompt safety scanner, dual-project isolation verifier, AI drama
 * continuity/cast checks, and retention redline preflight checker.
 *
 * Implements:
 *   - FLOW-PRODUCTION-RULES.md §4 & §5 (explainers)
 *   - CURIO-FLOW-CHECKLIST.md §2 (full-axis minor/violence scan across W/H/G/F)
 *   - shorts-PRODUCTION-ROUTES.md §3.8 (multi-character accessory anti-bleed)
 *   - animation-production (`data.source` 0-credit cuts, 3-shot Pilot mode, drama combat nuance)
 */

import { DEFAULT_PILOT_MAX_SHOTS, estimateClipCredits, getSeriesPreset } from "../config.mjs";

const MINOR_TERMS_RE =
  /\b(?:8-year-old|\d{1,2}-year-old\s+(?:boy|girl|child|kid)|elementary\s+school\s+(?:child|student|boy|girl)|high\s+school\s+student|schoolgirl|schoolboy|schoolchild|schoolchildren|toddler|toddlers|infant|infants|baby|babies|child|children|kid|kids|boy|boys|girl|girls|minor|minors|teenager|teenagers|teen|teens|little\s+(?:boy|girl))\b/gi;

const SOTHATSWHY_FILTER_TERMS_RE = /\b(?:bare\s+face|thrusts?)\b/gi;

const EXTREME_GORE_TERMS_RE =
  /\b(?:gore|gory|corpse|corpses|dead\s+bod(?:y|ies)|cadaver|decapitat\w*|dismember\w*|gunshot\s+wound|severed\s+\w+|mutilat\w*|bleeding\s+out|blood\s+splatter|murder\s+scene|tortur\w*|slaughter\w*)\b/gi;

// Action/conflict terms that are hard blockers on explainers (Flow safety filter)
// but reviewable warnings on historical/martial AI dramas
const DRAMA_ACTION_TERMS_RE = /\b(?:bloody|stabbing|stabbed)\b/gi;

const COPYRIGHT_IP_RE =
  /\b(?:pikachu|doraemon|mickey\s+mouse|minnie\s+mouse|hello\s+kitty|super\s+mario|spongebob|donald\s+duck|spider-?man|batman|iron\s+man)\b/gi;

const CHARACTER_REF_NAME_RE = /(?:canon|ada|chief|kid|character|cast)/i;

const REPEATED_STYLE_RE = /(?:theatrical\s+gouache|thick\s+gouache\s+painting)/gi;

const ACCESSORY_EXCLUSION_RE = /\b(?:no\s+glasses|without\s+glasses|unbespectacled|no\s+hat|without\s+\w+|wearing\s+.+while\s+.+wearing)\b/i;

function findRegexMatches(text, regex) {
  const results = [];
  if (!text || typeof text !== "string") return results;
  regex.lastIndex = 0;
  let match;
  while ((match = regex.exec(text)) !== null) {
    results.push({ match: match[0], index: match.index });
    if (match.index === regex.lastIndex) regex.lastIndex += 1;
  }
  return results;
}

/**
 * Scans a single prompt string for Google Flow safety-filter triggers,
 * copyright IP leaks, and series-specific redlines.
 */
export function scanPromptText(
  text,
  { series = "curio", shotId = null, field = "prompt" } = {},
) {
  const preset = getSeriesPreset(series);
  const findings = [];

  for (const hit of findRegexMatches(text, MINOR_TERMS_RE)) {
    findings.push({
      severity: "blocker",
      category: "minor_term",
      shotId,
      field,
      match: hit.match,
      index: hit.index,
      suggestion: `Replace "${hit.match}" with neutral wording such as "${preset.childReplacement}" (avoid triggering Flow's minor safety filter across all axes).`,
    });
  }

  for (const hit of findRegexMatches(text, SOTHATSWHY_FILTER_TERMS_RE)) {
    findings.push({
      severity: "blocker",
      category: "flow_filter_term",
      shotId,
      field,
      match: hit.match,
      index: hit.index,
      suggestion: `Avoid "${hit.match}" in Flow prompts; describe the character's expression or camera motion neutrally instead.`,
    });
  }

  for (const hit of findRegexMatches(text, EXTREME_GORE_TERMS_RE)) {
    findings.push({
      severity: "blocker",
      category: "violence_gore_term",
      shotId,
      field,
      match: hit.match,
      index: hit.index,
      suggestion: `Replace "${hit.match}" with suspenseful candlelight/silhouette/evidence close-up or narrator reaction framing.`,
    });
  }

  for (const hit of findRegexMatches(text, DRAMA_ACTION_TERMS_RE)) {
    const isDrama = preset.safetyProfile === "drama";
    findings.push({
      severity: isDrama ? "warning" : "blocker",
      category: isDrama ? "drama_action_caution" : "violence_gore_term",
      shotId,
      field,
      match: hit.match,
      index: hit.index,
      suggestion: isDrama
        ? `"${hit.match}" may trigger Flow's violence filter in AI drama shots; consider stylized impact sparks, silhouette, or weapon clash wording.`
        : `Replace "${hit.match}" with suspenseful candlelight/silhouette/evidence close-up or reaction framing.`,
    });
  }

  for (const hit of findRegexMatches(text, COPYRIGHT_IP_RE)) {
    findings.push({
      severity: "blocker",
      category: "copyright_ip",
      shotId,
      field,
      match: hit.match,
      index: hit.index,
      suggestion: `Remove third-party trademarked IP "${hit.match}" and describe an original generic object/character.`,
    });
  }

  const styleHits = findRegexMatches(text, REPEATED_STYLE_RE);
  if (styleHits.length > 1) {
    findings.push({
      severity: "warning",
      category: "duplicate_style_declaration",
      shotId,
      field,
      match: styleHits[1].match,
      index: styleHits[1].index,
      suggestion: "Style phrase appears more than once in the same prompt; keep one concise style cue.",
    });
  }

  const blockerCount = findings.filter((f) => f.severity === "blocker").length;
  const warningCount = findings.filter((f) => f.severity === "warning").length;

  return {
    ok: blockerCount === 0,
    blockerCount,
    warningCount,
    findings,
  };
}

/**
 * Normalizes a shot list JSON (supports `{ series, shots: [...] }` or
 * `{ scenes: [...] }` or plain array of shots).
 */
export function normalizeShots(shotList) {
  if (Array.isArray(shotList)) return shotList;
  if (shotList && Array.isArray(shotList.shots)) return shotList.shots;
  if (shotList && Array.isArray(shotList.scenes)) return shotList.scenes;
  return [];
}

/**
 * Runs a complete 0-credit preflight check over an episode's `flow-shot-list.json`:
 *   1. Full-axis safety term scan across top-level + per-shot still/video prompts.
 *   2. Dual-project isolation (`scenery` track cannot carry character refs).
 *   3. AI drama continuity links (`edit_from`, `continue_from`, `mode: "cut"` + `source`)
 *      and multi-character accessory anti-bleed check.
 *   4. Retention redlines & 3-shot Pilot mode check.
 *   5. Per-shot model/duration Flow credit budget check against series caps.
 */
export function preflightShotList(shotList, { series, pilot = false, cast = null } = {}) {
  const effectiveSeries = series || shotList?.series || "curio";
  const preset = getSeriesPreset(effectiveSeries);
  const shots = normalizeShots(shotList);

  const findings = [];
  const seenIds = new Set();
  const shotIndexById = new Map();
  const shotModeById = new Map();

  if (shots.length === 0) {
    findings.push({
      severity: "blocker",
      category: "empty_shotlist",
      shotId: null,
      field: "shots",
      match: "",
      suggestion: "Shot list contains 0 shots. Populate `shots` before running Flow generation.",
    });
  }

  if (pilot && shots.length > DEFAULT_PILOT_MAX_SHOTS) {
    findings.push({
      severity: "warning",
      category: "pilot_shot_count",
      shotId: null,
      field: "shots",
      match: `${shots.length} shots`,
      suggestion: `Pilot mode recommends <= ${DEFAULT_PILOT_MAX_SHOTS} consecutive shots first; pass shotIds to flow_plan_clips / flow_generate_stills for the 3-shot pilot.`,
    });
  }

  if (typeof shotList?.prompt === "string" && shotList.prompt.trim()) {
    findings.push(
      ...scanPromptText(shotList.prompt, {
        series: effectiveSeries,
        shotId: null,
        field: "prompt",
      }).findings,
    );
  }

  let clipCount = 0;
  let stillCount = 0;
  let cutCount = 0;
  let sceneryCount = 0;
  let characterCount = 0;
  let estimatedCredits = 0;

  let currentChapter = "__default__";
  let consecutiveStills = 0;

  for (let i = 0; i < shots.length; i += 1) {
    const shot = shots[i] || {};
    const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);

    if (seenIds.has(shotId)) {
      findings.push({
        severity: "blocker",
        category: "duplicate_shot_id",
        shotId,
        field: "id",
        match: shotId,
        suggestion: `Shot id "${shotId}" is duplicated. Every shot must have a unique id.`,
      });
    }
    seenIds.add(shotId);
    shotIndexById.set(shotId, i);

    const hasChars =
      shot.has_character === true ||
      (Array.isArray(shot.characters) && shot.characters.length > 0) ||
      (Array.isArray(shot.character_refs) && shot.character_refs.length > 0);
    const track = String(shot.track || (hasChars ? "character" : "scenery")).toLowerCase();
    if (track !== "character" && track !== "scenery") {
      findings.push({
        severity: "blocker",
        category: "invalid_track",
        shotId,
        field: "track",
        match: track,
        suggestion: `Shot "${shotId}" has invalid track "${track}". Must be "character" or "scenery".`,
      });
    } else if (track === "scenery") {
      sceneryCount += 1;
    } else {
      characterCount += 1;
    }

    const mode = String(
      shot.mode || (shot.source ? "cut" : shot.video_prompt || shot.motion_prompt ? "clip" : "still"),
    ).toLowerCase();
    shotModeById.set(shotId, mode);

    if (!["still", "clip", "cut"].includes(mode)) {
      findings.push({
        severity: "blocker",
        category: "invalid_mode",
        shotId,
        field: "mode",
        match: mode,
        suggestion: `Shot "${shotId}" has invalid mode "${mode}". Must be "still", "clip", or "cut".`,
      });
    }

    // Cut shot (`data.source`) validation — 0 Flow credits
    if (mode === "cut") {
      cutCount += 1;
      const src = String(shot.source || "").trim();
      if (!src || !shotIndexById.has(src)) {
        findings.push({
          severity: "blocker",
          category: "invalid_cut_source",
          shotId,
          field: "source",
          match: src,
          suggestion: `Cut shot "${shotId}" must reference an earlier shot id in \`source\` (got "${src}").`,
        });
      } else if (shotModeById.get(src) !== "clip") {
        findings.push({
          severity: "blocker",
          category: "cut_source_not_clip",
          shotId,
          field: "source",
          match: src,
          suggestion: `Cut shot "${shotId}" references "${src}", which is mode="${shotModeById.get(src)}" instead of "clip".`,
        });
      }
      consecutiveStills = 0;
      continue;
    }

    // Dual-project isolation guard
    const refs = [
      ...(Array.isArray(shot.refs) ? shot.refs : []),
      ...(Array.isArray(shot.character_refs) ? shot.character_refs : []),
    ];
    if (
      track === "scenery" &&
      (refs.some((r) => CHARACTER_REF_NAME_RE.test(String(r))) ||
        (Array.isArray(shot.character_refs) && shot.character_refs.length > 0))
    ) {
      findings.push({
        severity: "blocker",
        category: "dual_project_leak",
        shotId,
        field: "character_refs",
        match: refs.join(", "),
        suggestion: `Scenery shot "${shotId}" cannot include character references (dual-project isolation rule). Remove character refs or set track: "character".`,
      });
    }

    // Same-camera `edit_from` chain check
    if (shot.edit_from) {
      const parent = String(shot.edit_from);
      if (parent === shotId || !shotIndexById.has(parent)) {
        findings.push({
          severity: "blocker",
          category: "invalid_edit_from",
          shotId,
          field: "edit_from",
          match: parent,
          suggestion: `Shot "${shotId}" edit_from="${parent}" must reference an earlier shot in the same shot list so its approved still exists first.`,
        });
      }
    }

    // Exact-Join `continue_from` chain check
    if (shot.continue_from) {
      const prev = String(shot.continue_from);
      if (prev === shotId || !shotIndexById.has(prev) || shotModeById.get(prev) !== "clip") {
        findings.push({
          severity: "blocker",
          category: "invalid_continue_from",
          shotId,
          field: "continue_from",
          match: prev,
          suggestion: `Shot "${shotId}" continue_from="${prev}" must reference an earlier clip shot so its last frame can be extracted cleanly.`,
        });
      }
    }

    // Multi-character accessory anti-bleed check (shorts-PRODUCTION-ROUTES.md §3.8)
    const charNames = Array.isArray(shot.characters) ? shot.characters : [];
    const combinedPromptText = [shot.still_prompt, shot.video_prompt, shot.prompt].filter(Boolean).join(" ");
    if (charNames.length >= 2 && !ACCESSORY_EXCLUSION_RE.test(combinedPromptText)) {
      const castHasNoAccessoryHint =
        cast?.characters &&
        charNames.some((c) => Array.isArray(cast.characters[c]?.noAccessories) && cast.characters[c].noAccessories.length > 0);
      findings.push({
        severity: "warning",
        category: "multi_character_accessory_bleed",
        shotId,
        field: "still_prompt",
        match: charNames.join(", "),
        suggestion: castHasNoAccessoryHint
          ? `Shot "${shotId}" includes multiple characters (${charNames.join(", ")}); specify distinguishing traits/no-accessory cues (cast.json notes will be appended automatically if configured).`
          : `Shot "${shotId}" includes multiple characters (${charNames.join(", ")}); explicitly state who does NOT wear glasses/hats/props so Flow does not bleed accessories across faces.`,
      });
    }

    // Scan all prompt fields (including scenes[].data.prompt)
    const promptFields = [
      ["prompt", shot.prompt],
      ["still_prompt", shot.still_prompt],
      ["end_still_prompt", shot.end_still_prompt],
      ["video_prompt", shot.video_prompt],
      ["motion_prompt", shot.motion_prompt],
      ["data.prompt", shot.data?.prompt],
    ];
    let hasAnyPrompt = false;
    for (const [fieldName, value] of promptFields) {
      if (typeof value === "string" && value.trim()) {
        hasAnyPrompt = true;
        findings.push(
          ...scanPromptText(value, {
            series: effectiveSeries,
            shotId,
            field: fieldName,
          }).findings,
        );
      }
    }

    if (!hasAnyPrompt) {
      findings.push({
        severity: "blocker",
        category: "missing_prompt",
        shotId,
        field: "still_prompt",
        match: "",
        suggestion: `Shot "${shotId}" has no prompt text. Provide still_prompt (and video_prompt for clips).`,
      });
    }

    // Retention & per-shot credit calculation
    const chapter = String(shot.chapter ?? "__default__");
    if (chapter !== currentChapter) {
      currentChapter = chapter;
      consecutiveStills = 0;
    }

    if (mode === "clip") {
      clipCount += 1;
      consecutiveStills = 0;
      const dur = Number(shot.clip_duration_sec ?? 4);
      if (shot.end_still_prompt && dur > 10) {
        findings.push({
          severity: "blocker",
          category: "end_frame_duration_limit",
          shotId,
          field: "clip_duration_sec",
          match: `${dur}s`,
          suggestion: `Shot "${shotId}" uses end_still_prompt with duration ${dur}s; Omni 1.2 Flash supports at most 10s when --end-frame is passed.`,
        });
      }
      estimatedCredits += estimateClipCredits({
        model: shot.model,
        durationSec: dur,
        creditsOverride: shot.credits_override,
      });
    } else if (mode === "still") {
      stillCount += 1;
      consecutiveStills += 1;
      if (consecutiveStills > preset.maxConsecutiveStills) {
        findings.push({
          severity: "warning",
          category: "retention_consecutive_stills",
          shotId,
          field: "mode",
          match: `${consecutiveStills} consecutive stills`,
          suggestion: `Chapter "${chapter}" has ${consecutiveStills} consecutive stills (redline <= ${preset.maxConsecutiveStills}). Promote one shot to a Flow clip.`,
        });
      }
      const durationSec = Number(shot.duration_sec ?? shot.durationSec ?? 0);
      if (Number.isFinite(durationSec) && durationSec > preset.maxStillDurationSec) {
        findings.push({
          severity: "warning",
          category: "retention_still_duration",
          shotId,
          field: "duration_sec",
          match: `${durationSec}s`,
          suggestion: `Still "${shotId}" is ${durationSec}s (redline <= ${preset.maxStillDurationSec}s). Split into 2 shots or convert to a Flow clip.`,
        });
      }
    }
  }

  const totalShots = shots.length;
  const dynamicShots = clipCount + cutCount;
  const dynamicRatio = totalShots > 0 ? dynamicShots / totalShots : 0;
  const sceneryRatio = totalShots > 0 ? sceneryCount / totalShots : 0;

  if (totalShots > 0 && dynamicRatio < preset.minDynamicRatio) {
    findings.push({
      severity: "warning",
      category: "low_dynamic_ratio",
      shotId: null,
      field: "shots",
      match: `${(dynamicRatio * 100).toFixed(1)}%`,
      suggestion: `Dynamic shot share is ${(dynamicRatio * 100).toFixed(1)}% (${dynamicShots}/${totalShots}); ${preset.label} targets >= ${(preset.minDynamicRatio * 100).toFixed(0)}%.`,
    });
  }

  if (estimatedCredits > preset.budgetHardCap) {
    findings.push({
      severity: "blocker",
      category: "budget_exceeds_hard_cap",
      shotId: null,
      field: "shots",
      match: `${estimatedCredits} credits`,
      suggestion: `Estimated Flow spend is ${estimatedCredits} credits (${clipCount} clips, ${cutCount} zero-credit cuts), exceeding ${preset.label} hard cap of ${preset.budgetHardCap} credits.`,
    });
  } else if (estimatedCredits > preset.budgetSoftCap) {
    findings.push({
      severity: "warning",
      category: "budget_exceeds_soft_cap",
      shotId: null,
      field: "shots",
      match: `${estimatedCredits} credits`,
      suggestion: `Estimated Flow spend is ${estimatedCredits} credits, above the recommended ${preset.budgetSoftCap} soft cap (hard cap ${preset.budgetHardCap}).`,
    });
  }

  const blockers = findings.filter((f) => f.severity === "blocker");
  const warnings = findings.filter((f) => f.severity === "warning");

  return {
    ok: blockers.length === 0,
    series: preset.id,
    seriesLabel: preset.label,
    pilot: Boolean(pilot),
    summary: {
      totalShots,
      clipCount,
      stillCount,
      cutCount,
      characterCount,
      sceneryCount,
      dynamicRatio: Number(dynamicRatio.toFixed(4)),
      sceneryRatio: Number(sceneryRatio.toFixed(4)),
      estimatedCredits,
      budgetSoftCap: preset.budgetSoftCap,
      budgetHardCap: preset.budgetHardCap,
    },
    blockerCount: blockers.length,
    warningCount: warnings.length,
    unsafe_prompts: blockers.filter((b) =>
      ["minor_term", "flow_filter_term", "violence_gore_term", "copyright_ip"].includes(b.category),
    ),
    findings,
  };
}
