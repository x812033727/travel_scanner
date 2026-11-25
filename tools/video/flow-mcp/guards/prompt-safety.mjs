/**
 * Full-axis prompt safety scanner, dual-project isolation verifier, and
 * retention redline preflight checker.
 *
 * Implements the rules documented in:
 *   - FLOW-PRODUCTION-RULES.md §4 (dual-project isolation, safety filters) & §5 (retention)
 *   - CURIO-FLOW-CHECKLIST.md §2 (full-axis minor/violence scan across W/H/G/F)
 */

import { getSeriesPreset } from "../config.mjs";

const MINOR_TERMS_RE =
  /\b(?:8-year-old|\d{1,2}-year-old\s+(?:boy|girl|child|kid)|elementary\s+school\s+(?:child|student|boy|girl)|high\s+school\s+student|schoolgirl|schoolboy|schoolchild|schoolchildren|toddler|toddlers|infant|infants|baby|babies|child|children|kid|kids|boy|boys|girl|girls|minor|minors|teenager|teenagers|teen|teens|little\s+(?:boy|girl))\b/gi;

const SOTHATSWHY_FILTER_TERMS_RE = /\b(?:bare\s+face|thrusts?)\b/gi;

const VIOLENCE_GORE_TERMS_RE =
  /\b(?:bloody|gore|gory|corpse|corpses|dead\s+bod(?:y|ies)|cadaver|decapitat\w*|dismember\w*|stabbing|stabbed|gunshot\s+wound|severed\s+\w+|mutilat\w*|bleeding\s+out|blood\s+splatter|murder\s+scene|tortur\w*|slaughter\w*)\b/gi;

const COPYRIGHT_IP_RE =
  /\b(?:pikachu|doraemon|mickey\s+mouse|minnie\s+mouse|hello\s+kitty|super\s+mario|spongebob|donald\s+duck|spider-?man|batman|iron\s+man)\b/gi;

const CHARACTER_REF_NAME_RE = /(?:canon|ada|chief|kid|character)/i;

const REPEATED_STYLE_RE = /(?:theatrical\s+gouache|thick\s+gouache\s+painting)/gi;

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

  for (const hit of findRegexMatches(text, VIOLENCE_GORE_TERMS_RE)) {
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
 *   3. Retention redlines (max consecutive stills <= 3, single still <= 8s, dynamic ratio).
 *   4. Series Flow credit budget check (500 for sothatswhy, 550 soft / 600 hard for curio).
 */
export function preflightShotList(shotList, { series } = {}) {
  const effectiveSeries = series || shotList?.series || "curio";
  const preset = getSeriesPreset(effectiveSeries);
  const shots = normalizeShots(shotList);

  const findings = [];
  const seenIds = new Set();

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

  // Scan optional top-level prompt field too (per CURIO-FLOW-CHECKLIST §2)
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
  let sceneryCount = 0;
  let characterCount = 0;

  // Track consecutive stills per chapter (or globally when chapter is omitted)
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

    const track = String(shot.track || (shot.has_character ? "character" : "scenery")).toLowerCase();
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

    const mode = String(shot.mode || (shot.video_prompt || shot.motion_prompt ? "clip" : "still")).toLowerCase();
    if (mode !== "still" && mode !== "clip") {
      findings.push({
        severity: "blocker",
        category: "invalid_mode",
        shotId,
        field: "mode",
        match: mode,
        suggestion: `Shot "${shotId}" has invalid mode "${mode}". Must be "still" or "clip".`,
      });
    }

    // Dual-project isolation guard
    const refs = [
      ...(Array.isArray(shot.refs) ? shot.refs : []),
      ...(Array.isArray(shot.character_refs) ? shot.character_refs : []),
    ];
    if (track === "scenery" && (refs.some((r) => CHARACTER_REF_NAME_RE.test(String(r))) || (Array.isArray(shot.character_refs) && shot.character_refs.length > 0))) {
      findings.push({
        severity: "blocker",
        category: "dual_project_leak",
        shotId,
        field: "character_refs",
        match: refs.join(", "),
        suggestion: `Scenery shot "${shotId}" cannot include character references (dual-project isolation rule). Remove character refs or set track: "character".`,
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

    // Retention checks
    const chapter = String(shot.chapter ?? "__default__");
    if (chapter !== currentChapter) {
      currentChapter = chapter;
      consecutiveStills = 0;
    }

    if (mode === "clip") {
      clipCount += 1;
      consecutiveStills = 0;
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
  const dynamicRatio = totalShots > 0 ? clipCount / totalShots : 0;
  const sceneryRatio = totalShots > 0 ? sceneryCount / totalShots : 0;
  const estimatedCredits = clipCount * preset.clipCredits;

  if (totalShots > 0 && dynamicRatio < preset.minDynamicRatio) {
    findings.push({
      severity: "warning",
      category: "low_dynamic_ratio",
      shotId: null,
      field: "shots",
      match: `${(dynamicRatio * 100).toFixed(1)}%`,
      suggestion: `Dynamic clip share is ${(dynamicRatio * 100).toFixed(1)}% (${clipCount}/${totalShots}); ${preset.label} targets >= ${(preset.minDynamicRatio * 100).toFixed(0)}%.`,
    });
  }

  if (estimatedCredits > preset.budgetHardCap) {
    findings.push({
      severity: "blocker",
      category: "budget_exceeds_hard_cap",
      shotId: null,
      field: "shots",
      match: `${estimatedCredits} credits`,
      suggestion: `Estimated Flow spend is ${estimatedCredits} credits (${clipCount} clips × ${preset.clipCredits}), exceeding ${preset.label} hard cap of ${preset.budgetHardCap} credits.`,
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
    summary: {
      totalShots,
      clipCount,
      stillCount,
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
