/**
 * Core orchestrator implementing all 16 Mokaair Google Flow MCP tools across
 * explainers (`sothatswhy`, `curio`), AI dramas (`drama-16x9`, `drama-9x16`),
 * and zero-dialogue vertical Shorts (`shorts`).
 *
 * Enforces every guard from `FLOW-PRODUCTION-RULES.md`, `CURIO-FLOW-CHECKLIST.md`,
 * `shorts-PRODUCTION-ROUTES.md`, `AI-DRAMA-DRIVE.md`, and `animation-production`:
 *   1. Route B `work/video-episodes/<slug>/` path boundary (0 GitHub commits)
 *   2. Dual-project isolation (`character` vs `scenery`) + multi-character Cast (`cast.json`)
 *   3. Full-axis safety prompt scan + drama multi-character anti-bleed + 0-credit `cut` shots
 *   4. 0-credit `Nano Banana 2.1` stills + same-camera `edit_from` chain + 16:9 / 9:16 binary check
 *   5. Explicit QA sign-off (`flow_approve_stills`) before unlocking paid clips
 *   6. Variable per-shot model/duration budgets + 3-shot Pilot + single-use `confirm_token`
 *   7. Multi-take archival (`takes/`), `MAX_CLIP_TAKES=2` hard stop, `flow_select_take`
 *   8. Exact-Join `continue_from` last-frame extraction, `flow_extend_clip`, `flow_reconcile`
 *   9. Local FFmpeg 1080p30/bt709/tv/-an + optional raw-audio WAV + PSNR/hard-cut QC + import bridge
 */

import fs from "node:fs";
import path from "node:path";
import {
  buildDrivePushCommand,
  buildImportBridge,
  convertVideoJsonToFlowSpec,
  applySilentAudioGuard,
} from "./bridges/video-json-adapter.mjs";
import {
  DEFAULT_CLIP_CREDITS,
  DEFAULT_IMAGE_MODEL,
  DEFAULT_MAX_CREDITS_PER_CLIP,
  DEFAULT_PILOT_MAX_SHOTS,
  DEFAULT_VIDEO_DURATION_SEC,
  DEFAULT_VIDEO_MODEL,
  DEFAULT_VIDEO_RESOLUTION,
  REPO_ROOT,
  estimateClipCredits,
  getSeriesPreset,
  resolveRulesCacheRoot,
  resolveRuntimeHome,
} from "./config.mjs";
import { GflowCliDriver } from "./drivers/gflow-cli-driver.mjs";
import { verifyStillDimensions } from "./guards/aspect-verify.mjs";
import {
  atomicWriteJson,
  loadCreditLedger,
  planClipBudget,
  readJsonSafe,
  recalculateLedgerTotals,
  recordCreditEvent,
  verifyAndConsumeConfirmToken,
} from "./guards/budget-guard.mjs";
import { resolveEpisodePaths } from "./guards/path-boundary.mjs";
import { normalizeShots, preflightShotList, scanPromptText } from "./guards/prompt-safety.mjs";
import { JobQueue } from "./jobs/job-queue.mjs";
import {
  saveClipsManifest,
  writeClipsQaGallery,
  writeStillsQaGallery,
} from "./postprocess/qa-contact-sheet.mjs";
import { extractLastFrame, sha256File, upscaleClipTo1080p30 } from "./postprocess/upscale-1080p30.mjs";

function sanitizeFilename(id) {
  return String(id || "shot")
    .trim()
    .replace(/[^a-zA-Z0-9._-]+/g, "_")
    .replace(/^_+|_+$/g, "") || "shot";
}

function findCanonFiles(series, rulesCacheRoot) {
  const preset = getSeriesPreset(series);
  const found = [];
  const missing = [];
  for (const rel of preset.canonRuleFiles) {
    const abs = path.join(rulesCacheRoot, rel);
    if (fs.existsSync(abs)) {
      found.push({ rel, path: abs });
    } else {
      missing.push({ rel, path: abs });
    }
  }
  return { found, missing };
}

function getShotMode(shot) {
  return String(
    shot.mode || (shot.source ? "cut" : shot.video_prompt || shot.motion_prompt ? "clip" : "still"),
  ).toLowerCase();
}

function getShotTrack(shot) {
  const hasChars =
    shot.has_character === true ||
    (Array.isArray(shot.characters) && shot.characters.length > 0) ||
    (Array.isArray(shot.character_refs) && shot.character_refs.length > 0);
  return String(shot.track || (hasChars ? "character" : "scenery")).toLowerCase();
}

export class FlowOrchestrator {
  constructor({
    driver = null,
    queue = null,
    repoRoot = REPO_ROOT,
    runtimeHome = resolveRuntimeHome(),
    rulesCacheRoot = null,
    allowExternalWorkdir = false,
    upscaleFn = upscaleClipTo1080p30,
    extractLastFrameFn = extractLastFrame,
  } = {}) {
    this.repoRoot = repoRoot;
    this.runtimeHome = runtimeHome;
    this.rulesCacheRoot = rulesCacheRoot || resolveRulesCacheRoot(repoRoot);
    this.allowExternalWorkdir = allowExternalWorkdir;
    this.driver = driver || new GflowCliDriver({ runtimeHome });
    this.queue = queue || new JobQueue({ runtimeHome });
    this.upscaleFn = upscaleFn;
    this.extractLastFrameFn = extractLastFrameFn;
  }

  #paths(slug, workdir) {
    return resolveEpisodePaths(slug, {
      repoRoot: this.repoRoot,
      workdir,
      allowExternal: this.allowExternalWorkdir,
    });
  }

  #loadShotList(paths) {
    if (!fs.existsSync(paths.shotListFile)) {
      throw new Error(
        `Missing flow-shot-list.json at "${paths.shotListFile}". Place your episode shot list under work/video-episodes/<slug>/flow-shot-list.json (or call flow_import_video_json first).`,
      );
    }
    return JSON.parse(fs.readFileSync(paths.shotListFile, "utf8"));
  }

  #loadWorkspace(paths) {
    return readJsonSafe(paths.workspaceFile, null);
  }

  #loadCast(paths, { series = "curio" } = {}) {
    return (
      readJsonSafe(paths.castFile, null) || {
        schemaVersion: 1,
        series,
        characters: {},
      }
    );
  }

  #loadStillsQa(paths, { slug, series }) {
    return (
      readJsonSafe(paths.stillsQaFile, null) || {
        schemaVersion: 1,
        slug,
        series,
        updatedAt: null,
        stills: {},
      }
    );
  }

  /**
   * Resolves character reference image paths and anti-bleed accessory cues
   * from `cast.json` + `shot.characters` + `shot.character_looks` + workspace canon.
   */
  #resolveCharacterContext(shot, { cast, workspace }) {
    const refs = [];
    const antiBleedNotes = [];
    const charNames = Array.isArray(shot.characters) ? shot.characters.map(String) : [];
    const lookOverrides = shot.character_looks && typeof shot.character_looks === "object" ? shot.character_looks : {};

    for (const charId of charNames) {
      const entry = cast?.characters?.[charId];
      if (!entry) continue;
      const requestedLook = lookOverrides[charId];
      if (requestedLook && entry.looks?.[requestedLook]) {
        const lookVal = entry.looks[requestedLook];
        if (Array.isArray(lookVal)) refs.push(...lookVal);
        else refs.push(String(lookVal));
      } else if (Array.isArray(entry.refs) && entry.refs.length > 0) {
        refs.push(...entry.refs);
      }
      if (charNames.length >= 2 && Array.isArray(entry.noAccessories) && entry.noAccessories.length > 0) {
        antiBleedNotes.push(`${entry.name || charId} has NO ${entry.noAccessories.join(" and NO ")}`);
      }
    }

    if (Array.isArray(shot.character_refs)) refs.push(...shot.character_refs);
    if (Array.isArray(shot.refs)) refs.push(...shot.refs);

    if (refs.length === 0 && !shot.character_refs && !shot.refs) {
      refs.push(...(workspace?.localCanonPaths || []));
    }

    return {
      refs: [...new Set(refs.filter(Boolean))],
      antiBleedSuffix: antiBleedNotes.length > 0 ? ` (${antiBleedNotes.join("; ")})` : "",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 1: flow_status (0 credits)
  // ---------------------------------------------------------------------------
  async flowStatus({ profile = null, refreshCredits = false } = {}) {
    const lock = this.queue.getLockStatus(profile);
    let auth = null;
    let credits = null;
    let driverVersion = null;
    let driverError = null;

    try {
      driverVersion = await this.driver.getVersion();
      auth = await this.driver.checkAuth({ profile });
      if (auth.authenticated) {
        try {
          credits = await this.driver.getCredits({ profile, refresh: refreshCredits });
        } catch (err) {
          credits = { credits: null, error: err.message };
        }
      }
    } catch (err) {
      driverError = err.toJSON ? err.toJSON() : { message: err.message };
    }

    return {
      ok: Boolean(auth?.authenticated) && !driverError,
      driver: this.driver.name,
      driverVersion,
      runtimeHome: this.runtimeHome,
      lock,
      auth,
      credits,
      error: driverError,
      desktopReminder:
        "Keep the dedicated Chrome window visible (not minimized) and PC awake while Flow jobs are running.",
      nextStep: auth?.authenticated
        ? "Session is ready. Run flow_preflight_shotlist, flow_import_video_json, or flow_init_episode."
        : "Run `npm run flow -- login` on your local desktop to sign into Google Flow via Chrome.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 2: flow_profiles (0 credits — multi-account subscription overview)
  // ---------------------------------------------------------------------------
  async flowProfiles({ refreshCredits = false } = {}) {
    const profiles = await this.driver.listProfiles({ refreshCredits });
    const enriched = profiles.map((p) => ({
      ...p,
      lock: this.queue.getLockStatus(p.profile),
    }));
    const totalCredits = enriched.reduce((sum, p) => sum + (Number(p.credits) || 0), 0);
    return {
      ok: true,
      count: enriched.length,
      totalCredits,
      profiles: enriched,
      tip: "Pass `profile: \"<name>\"` to any Flow tool to run on a specific Google AI subscription account without colliding locks.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 3: flow_init_episode (0 credits)
  // ---------------------------------------------------------------------------
  async flowInitEpisode({
    slug,
    series = "curio",
    workdir = null,
    dramaName = null,
    episodeLabel = null,
    characterProjectId = null,
    sceneryProjectId = null,
    createProjects = false,
    uploadCanonRefs = false,
    extraCharacterRefs = [],
    profile = null,
  }) {
    const preset = getSeriesPreset(series);
    const paths = this.#paths(slug, workdir);
    fs.mkdirSync(paths.stillsDir, { recursive: true });
    fs.mkdirSync(paths.clipsDir, { recursive: true });
    fs.mkdirSync(paths.clipsTakesDir, { recursive: true });
    fs.mkdirSync(paths.reviewDir, { recursive: true });

    const existing = this.#loadWorkspace(paths) || {};
    let charProj = characterProjectId || existing.characterProjectId || null;
    let scenProj = sceneryProjectId || existing.sceneryProjectId || null;

    if (charProj && scenProj && charProj === scenProj) {
      throw new Error(
        `Dual-project isolation violation: characterProjectId and sceneryProjectId cannot be identical ("${charProj}"). Keep character references strictly separated from scenery shots.`,
      );
    }

    if (createProjects) {
      if (!charProj) {
        const created = await this.driver.createProject({
          name: `${paths.slug}-character`,
          profile,
        });
        charProj = created.projectId;
      }
      if (!scenProj) {
        const created = await this.driver.createProject({
          name: `${paths.slug}-scenery`,
          profile,
        });
        scenProj = created.projectId;
      }
    }

    const canonDiscovery = findCanonFiles(preset.id, this.rulesCacheRoot);
    const localCanonPaths = [
      ...canonDiscovery.found.map((f) => f.path),
      ...(extraCharacterRefs || []).filter((p) => fs.existsSync(p)),
    ];

    const uploadedCanonAssets = existing.uploadedCanonAssets || [];
    if (uploadCanonRefs && charProj) {
      for (const filePath of localCanonPaths) {
        const already = uploadedCanonAssets.find((a) => a.filePath === filePath && a.projectId === charProj);
        if (already) continue;
        const up = await this.driver.uploadAsset({
          filePath,
          projectId: charProj,
          profile,
        });
        uploadedCanonAssets.push({
          filePath,
          projectId: charProj,
          assetUuid: up.assetUuid,
          uploadedAt: new Date().toISOString(),
        });
      }
    }

    const workspace = {
      schemaVersion: 2,
      slug: paths.slug,
      series: preset.id,
      seriesLabel: preset.label,
      dramaName: dramaName || existing.dramaName || null,
      episodeLabel: episodeLabel || existing.episodeLabel || null,
      aspect: preset.aspect,
      targetStillWidth: preset.targetStillWidth,
      targetStillHeight: preset.targetStillHeight,
      characterProjectId: charProj,
      sceneryProjectId: scenProj,
      localCanonPaths,
      missingCanonRuleFiles: canonDiscovery.missing.map((m) => m.rel),
      uploadedCanonAssets,
      createdAt: existing.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    atomicWriteJson(paths.workspaceFile, workspace);

    return {
      ok: true,
      workspaceFile: paths.workspaceFile,
      workspace,
      dualProjectsReady: Boolean(charProj && scenProj && charProj !== scenProj),
      rulesHint:
        canonDiscovery.missing.length > 0
          ? "Some canon character sheets were not found in `.cache/video-drive/rules/`. Run `npm run vdrive -- pull-rules all` first."
          : null,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 4: flow_register_character (0 credits — Cast + optional @Name entity)
  // ---------------------------------------------------------------------------
  async flowRegisterCharacter({
    slug,
    series = null,
    workdir = null,
    id,
    name = null,
    appearance = "",
    refs = [],
    looks = {},
    noAccessories = [],
    voice = null,
    createFlowEntity = false,
    facePrompt = null,
    bodyPrompt = null,
    profile = null,
  }) {
    if (!id || !String(id).trim()) {
      throw new Error("Character `id` is required.");
    }
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "drama-16x9";
    const cast = this.#loadCast(paths, { series: effectiveSeries });

    const charId = String(id).trim();
    const displayName = String(name || charId).trim();
    const cleanRefs = (refs || []).filter(Boolean).map(String);

    let flowEntity = null;
    if (createFlowEntity) {
      const projectId = workspace?.characterProjectId;
      if (!projectId) {
        throw new Error(
          "Cannot create Flow Character entity without a bound `characterProjectId`. Run flow_init_episode first.",
        );
      }
      flowEntity = await this.driver.createCharacter({
        projectId,
        name: displayName,
        imagePath: cleanRefs[0] || null,
        bodyImagePath: cleanRefs[1] || null,
        facePrompt: facePrompt || null,
        bodyPrompt: bodyPrompt || null,
        voice: voice || null,
        profile,
      });
    }

    const existing = cast.characters[charId] || {};
    cast.characters[charId] = {
      id: charId,
      name: displayName,
      appearance: appearance || existing.appearance || "",
      refs: cleanRefs.length > 0 ? cleanRefs : existing.refs || [],
      looks: { ...(existing.looks || {}), ...(looks || {}) },
      noAccessories:
        Array.isArray(noAccessories) && noAccessories.length > 0
          ? noAccessories.map(String)
          : existing.noAccessories || [],
      voice: voice || existing.voice || null,
      flowEntityId: flowEntity?.entityId || existing.flowEntityId || null,
      flowEntityName: flowEntity?.name || existing.flowEntityName || null,
      updatedAt: new Date().toISOString(),
    };

    atomicWriteJson(paths.castFile, cast);
    return {
      ok: true,
      castFile: paths.castFile,
      character: cast.characters[charId],
      totalCharacters: Object.keys(cast.characters).length,
      mentionSyntax: flowEntity?.name ? `@${flowEntity.name}` : null,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 5: flow_import_video_json (0 credits — bridge Mokaair video.json)
  // ---------------------------------------------------------------------------
  async flowImportVideoJson({
    slug,
    series = null,
    workdir = null,
    videoJsonPath = null,
    defaultModel = DEFAULT_VIDEO_MODEL,
    defaultDurationSec = DEFAULT_VIDEO_DURATION_SEC,
    silentAudioGuard = null,
  }) {
    const paths = this.#paths(slug, workdir);
    const sourcePath = videoJsonPath ? path.resolve(videoJsonPath) : paths.videoJsonFile;
    if (!fs.existsSync(sourcePath)) {
      throw new Error(`video.json not found at "${sourcePath}".`);
    }
    const videoJson = JSON.parse(fs.readFileSync(sourcePath, "utf8"));
    const converted = convertVideoJsonToFlowSpec(videoJson, {
      series,
      defaultModel,
      defaultDurationSec,
      silentAudioGuard,
    });

    atomicWriteJson(paths.shotListFile, converted.shotList);

    // Merge cast characters without clobbering existing local ref paths
    const existingCast = this.#loadCast(paths, { series: converted.series });
    for (const [charId, ch] of Object.entries(converted.cast.characters)) {
      const prev = existingCast.characters[charId] || {};
      existingCast.characters[charId] = {
        ...ch,
        refs: ch.refs.length > 0 ? ch.refs : prev.refs || [],
        looks: { ...(prev.looks || {}), ...(ch.looks || {}) },
        noAccessories: ch.noAccessories.length > 0 ? ch.noAccessories : prev.noAccessories || [],
        flowEntityId: ch.flowEntityId || prev.flowEntityId || null,
        flowEntityName: ch.flowEntityName || prev.flowEntityName || null,
      };
    }
    atomicWriteJson(paths.castFile, existingCast);

    return {
      ok: true,
      slug: paths.slug,
      series: converted.series,
      sourcePath,
      shotListFile: paths.shotListFile,
      castFile: paths.castFile,
      stats: converted.stats,
      nextStep: "Run flow_preflight_shotlist to verify safety, continuity links, and credit budget.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 6: flow_preflight_shotlist (0 credits)
  // ---------------------------------------------------------------------------
  async flowPreflightShotlist({ slug, series = null, workdir = null, shotList = null, pilot = false }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = shotList || this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const cast = this.#loadCast(paths, { series: effectiveSeries });

    const report = preflightShotList(rawList, { series: effectiveSeries, pilot, cast });
    const enriched = {
      ...report,
      slug: paths.slug,
      checkedAt: new Date().toISOString(),
      dualProjectsConfigured: Boolean(
        workspace?.characterProjectId &&
          workspace?.sceneryProjectId &&
          workspace.characterProjectId !== workspace.sceneryProjectId,
      ),
      castCharactersCount: Object.keys(cast.characters || {}).length,
    };

    atomicWriteJson(paths.preflightFile, enriched);
    return {
      ...enriched,
      preflightFile: paths.preflightFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 7: flow_generate_stills (0 credits — Nano Banana 2.1 + edit_from chain)
  // ---------------------------------------------------------------------------
  async flowGenerateStills({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
    pilot = false,
    model = DEFAULT_IMAGE_MODEL,
    overwriteApproved = false,
    profile = null,
    waitMs = 0,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);
    const cast = this.#loadCast(paths, { series: preset.id });

    const preflight = preflightShotList(rawList, { series: effectiveSeries, pilot, cast });
    if (!preflight.ok) {
      return {
        ok: false,
        reason: "preflight_failed",
        message: `Blocked before Chrome launch: shot list has ${preflight.blockerCount} blocker(s). Fix them and re-run flow_preflight_shotlist.`,
        preflight,
      };
    }

    const shots = normalizeShots(rawList);
    let filterSet = Array.isArray(shotIds) && shotIds.length > 0 ? new Set(shotIds.map(String)) : null;
    if (pilot && !filterSet) {
      // Auto-pick first 3 non-cut shots for a 3-shot Pilot
      filterSet = new Set(
        shots
          .filter((s) => getShotMode(s) !== "cut")
          .slice(0, DEFAULT_PILOT_MAX_SHOTS)
          .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`)),
      );
    }

    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
    const items = [];

    for (let i = 0; i < shots.length; i += 1) {
      const shot = shots[i];
      const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);
      if (filterSet && !filterSet.has(shotId)) continue;
      if (getShotMode(shot) === "cut") continue; // 0-credit cut reuses source clip

      const existingQa = qaStore.stills?.[shotId];
      if (existingQa?.qaStatus === "approved" && !overwriteApproved) {
        continue;
      }

      const track = getShotTrack(shot);
      const projectId =
        track === "character" ? workspace?.characterProjectId || null : workspace?.sceneryProjectId || null;

      if (workspace?.characterProjectId && workspace?.sceneryProjectId && !projectId) {
        throw new Error(`Shot "${shotId}" track "${track}" has no bound Flow project.`);
      }

      const charCtx =
        track === "character" ? this.#resolveCharacterContext(shot, { cast, workspace }) : { refs: [], antiBleedSuffix: "" };

      const basePrompt = shot.still_prompt || shot.prompt || shot.data?.prompt;
      const stillPrompt = `${basePrompt}${charCtx.antiBleedSuffix}`;
      const safety = scanPromptText(stillPrompt, { series: preset.id, shotId, field: "still_prompt" });
      if (!safety.ok) {
        return { ok: false, reason: "unsafe_prompt", shotId, findings: safety.findings };
      }

      const outFile = path.join(paths.stillsDir, `${sanitizeFilename(shotId)}.png`);
      items.push({
        shotId,
        track,
        projectId,
        prompt: stillPrompt,
        refs: charCtx.refs,
        editFromShotId: shot.edit_from ? String(shot.edit_from) : null,
        outFile,
        model,
        aspect: preset.aspect,
        expectedWidth: preset.targetStillWidth,
        expectedHeight: preset.targetStillHeight,
        profile,
      });

      if (shot.end_still_prompt && String(shot.end_still_prompt).trim()) {
        const endId = `${shotId}__end`;
        items.push({
          shotId: endId,
          parentShotId: shotId,
          isEndFrame: true,
          track,
          projectId,
          prompt: `${String(shot.end_still_prompt).trim()}${charCtx.antiBleedSuffix}`,
          refs: charCtx.refs,
          editFromShotId: shot.edit_from ? String(shot.edit_from) : shotId,
          outFile: path.join(paths.stillsDir, `${sanitizeFilename(endId)}.png`),
          model,
          aspect: preset.aspect,
          expectedWidth: preset.targetStillWidth,
          expectedHeight: preset.targetStillHeight,
          profile,
        });
      }
    }

    if (items.length === 0) {
      return {
        ok: true,
        queued: 0,
        message: "All matching stills are already approved (pass overwriteApproved: true to regenerate).",
        stillsQaFile: paths.stillsQaFile,
        stillsGalleryFile: paths.stillsGalleryFile,
      };
    }

    fs.mkdirSync(paths.stillsDir, { recursive: true });
    fs.mkdirSync(paths.rejectedStillsDir, { recursive: true });

    const job = this.queue.enqueue({
      kind: "generate_stills",
      slug: paths.slug,
      profile,
      items,
      worker: async (item, { signal }) => {
        // Resolve same-camera `edit_from` parent still dynamically so sequential
        // shots in the same batch can chain off the parent's generated file!
        const runtimeRefs = [...item.refs];
        if (item.editFromShotId) {
          const liveQa = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
          const parentStill = liveQa.stills?.[item.editFromShotId];
          if (parentStill?.filePath && fs.existsSync(parentStill.filePath) && parentStill.aspectOk !== false) {
            runtimeRefs.unshift(parentStill.filePath);
          } else if (!item.isEndFrame) {
            const err = new Error(
              `Same-camera edit_from="${item.editFromShotId}" still is missing or rejected; generate/approve "${item.editFromShotId}" first.`,
            );
            err.code = "missing_edit_from_still";
            err.charged = "no";
            throw err;
          }
        }

        const gen = await this.driver.generateImage({
          prompt: item.prompt,
          refs: [...new Set(runtimeRefs)],
          model: item.model,
          aspect: item.aspect,
          projectId: item.projectId,
          outFile: item.outFile,
          profile: item.profile,
          signal,
        });

        const filePath = gen.outFile || item.outFile;
        const check = verifyStillDimensions(filePath, {
          expectedWidth: item.expectedWidth,
          expectedHeight: item.expectedHeight,
        });

        const currentQa = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });

        if (!check.ok) {
          const rejectedPath = path.join(
            paths.rejectedStillsDir,
            `${sanitizeFilename(item.shotId)}-${check.reason}-${Date.now()}.png`,
          );
          if (fs.existsSync(filePath)) {
            fs.renameSync(filePath, rejectedPath);
          }
          currentQa.stills[item.shotId] = {
            shotId: item.shotId,
            track: item.track,
            projectId: gen.projectId || item.projectId,
            mediaId: gen.mediaId,
            filePath: rejectedPath,
            aspectOk: false,
            aspectReason: check.reason,
            width: check.width,
            height: check.height,
            qaStatus: "rejected",
            note: check.message || `Failed dimension check (${check.reason})`,
            prompt: item.prompt,
            updatedAt: new Date().toISOString(),
          };
          currentQa.updatedAt = new Date().toISOString();
          atomicWriteJson(paths.stillsQaFile, currentQa);

          const err = new Error(check.message || `Still ${item.shotId} failed dimension verification (${check.reason}).`);
          err.code = check.reason;
          err.charged = "no";
          err.retryable = true;
          throw err;
        }

        const record = {
          shotId: item.shotId,
          track: item.track,
          editFromShotId: item.editFromShotId,
          projectId: gen.projectId || item.projectId,
          mediaId: gen.mediaId,
          filePath,
          sha256: fs.existsSync(filePath) ? sha256File(filePath) : null,
          aspectOk: true,
          aspectReason: check.reason,
          width: check.width,
          height: check.height,
          qaStatus: "pending",
          note: "",
          prompt: item.prompt,
          updatedAt: new Date().toISOString(),
        };
        currentQa.stills[item.shotId] = record;
        currentQa.updatedAt = new Date().toISOString();
        atomicWriteJson(paths.stillsQaFile, currentQa);
        return record;
      },
      onComplete: async () => {
        const finalQa = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
        const galleryItems = Object.values(finalQa.stills || {});
        writeStillsQaGallery({
          galleryFile: paths.stillsGalleryFile,
          slug: paths.slug,
          series: preset.id,
          items: galleryItems,
          safeZoneOverlay: preset.safeZoneOverlay,
        });
        return {
          stillsQaFile: paths.stillsQaFile,
          stillsGalleryFile: paths.stillsGalleryFile,
          totalRecorded: galleryItems.length,
        };
      },
    });

    if (waitMs > 0) {
      const waited = await this.queue.waitForJob(job.jobId, { timeoutMs: waitMs });
      return {
        ok: true,
        creditsSpent: 0,
        job_id: job.jobId,
        ...waited,
        stillsGalleryFile: paths.stillsGalleryFile,
      };
    }

    return {
      ok: true,
      creditsSpent: 0,
      job_id: job.jobId,
      queued: items.length,
      status: job.status,
      stillsGalleryFile: paths.stillsGalleryFile,
      nextStep: "Poll progress with flow_wait(job_id), double-click stills/qa-gallery.html to inspect & copy JSON, then call flow_approve_stills.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 8: flow_approve_stills (0 credits — unlocks clip generation)
  // ---------------------------------------------------------------------------
  async flowApproveStills({
    slug,
    series = null,
    workdir = null,
    approved = [],
    rejected = [],
    reviewer = "owner",
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });

    const updatedApproved = [];
    const blockedApprove = [];

    for (const entry of approved || []) {
      const shotId = typeof entry === "string" ? entry : entry.shotId;
      const note = typeof entry === "string" ? "" : entry.note || "";
      const record = qaStore.stills?.[shotId];
      if (!record || !record.filePath || !fs.existsSync(record.filePath)) {
        blockedApprove.push({ shotId, reason: "still_file_missing" });
        continue;
      }
      const check = verifyStillDimensions(record.filePath, {
        expectedWidth: preset.targetStillWidth,
        expectedHeight: preset.targetStillHeight,
      });
      if (!check.ok) {
        blockedApprove.push({ shotId, reason: check.reason, message: check.message });
        continue;
      }
      record.qaStatus = "approved";
      record.approvedBy = reviewer;
      record.approvedAt = new Date().toISOString();
      if (note) record.note = note;
      updatedApproved.push(shotId);
    }

    const updatedRejected = [];
    for (const entry of rejected || []) {
      const shotId = typeof entry === "string" ? entry : entry.shotId;
      const note = typeof entry === "string" ? "Rejected during visual QA" : entry.note || "Rejected during visual QA";
      if (!qaStore.stills[shotId]) {
        qaStore.stills[shotId] = { shotId, qaStatus: "rejected", note };
      } else {
        qaStore.stills[shotId].qaStatus = "rejected";
        qaStore.stills[shotId].note = note;
        qaStore.stills[shotId].rejectedBy = reviewer;
        qaStore.stills[shotId].rejectedAt = new Date().toISOString();
      }
      updatedRejected.push(shotId);
    }

    qaStore.updatedAt = new Date().toISOString();
    atomicWriteJson(paths.stillsQaFile, qaStore);
    writeStillsQaGallery({
      galleryFile: paths.stillsGalleryFile,
      slug: paths.slug,
      series: preset.id,
      items: Object.values(qaStore.stills || {}),
      safeZoneOverlay: preset.safeZoneOverlay,
    });

    const summary = {
      approvedCount: Object.values(qaStore.stills).filter((s) => s.qaStatus === "approved").length,
      pendingCount: Object.values(qaStore.stills).filter((s) => s.qaStatus === "pending").length,
      rejectedCount: Object.values(qaStore.stills).filter((s) => s.qaStatus === "rejected").length,
    };

    return {
      ok: blockedApprove.length === 0,
      updatedApproved,
      updatedRejected,
      blockedApprove,
      summary,
      stillsQaFile: paths.stillsQaFile,
      stillsGalleryFile: paths.stillsGalleryFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 9: flow_plan_clips (0 credits — Dry-Run, pilot, resumeMissingOnly, confirm_token)
  // ---------------------------------------------------------------------------
  async flowPlanClips({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
    pilot = false,
    resumeMissingOnly = false,
    forceRetake = false,
    model = DEFAULT_VIDEO_MODEL,
    creditsPerClip = null,
    budgetHardCapOverride = null,
    checkLiveBalance = false,
    profile = null,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);
    const cast = this.#loadCast(paths, { series: preset.id });

    const preflight = preflightShotList(rawList, { series: effectiveSeries, pilot, cast });
    if (!preflight.ok) {
      return {
        ok: false,
        reason: "preflight_failed",
        message: "Shot list failed safety/isolation preflight; fix blockers before planning paid clips.",
        preflight,
      };
    }

    const shots = normalizeShots(rawList);
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
    const existingManifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
    let filterSet = Array.isArray(shotIds) && shotIds.length > 0 ? new Set(shotIds.map(String)) : null;

    if (pilot && !filterSet) {
      filterSet = new Set(
        shots
          .filter((s) => getShotMode(s) === "clip")
          .slice(0, DEFAULT_PILOT_MAX_SHOTS)
          .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`)),
      );
    }

    const eligibleShotIds = [];
    const shotPlans = [];
    const unapprovedStills = [];
    const retakeLimitBlocked = [];

    for (let i = 0; i < shots.length; i += 1) {
      const shot = shots[i];
      const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);
      if (getShotMode(shot) !== "clip") continue;
      if (filterSet && !filterSet.has(shotId)) continue;

      const existingClip = existingManifest.clips?.[shotId];
      if (resumeMissingOnly && existingClip) continue;

      const priorTakes = Array.isArray(existingClip?.takes)
        ? existingClip.takes.length
        : existingClip
          ? 1
          : 0;
      if (!forceRetake && priorTakes >= preset.maxClipTakes) {
        retakeLimitBlocked.push({
          shotId,
          priorTakes,
          maxClipTakes: preset.maxClipTakes,
          message: `Shot "${shotId}" already reached MAX_CLIP_TAKES=${preset.maxClipTakes}. Redesign the prompt/motion before passing forceRetake: true.`,
        });
        continue;
      }

      // `continue_from` clips inherit their opening frame from the previous clip's
      // final frame rather than requiring a standalone still!
      if (!shot.continue_from) {
        const stillRecord = qaStore.stills?.[shotId];
        if (!stillRecord || stillRecord.qaStatus !== "approved" || !stillRecord.aspectOk) {
          unapprovedStills.push({
            shotId,
            qaStatus: stillRecord?.qaStatus || "missing",
            aspectOk: stillRecord?.aspectOk ?? false,
          });
          continue;
        }
      }

      if (shot.end_still_prompt) {
        const endRecord = qaStore.stills?.[`${shotId}__end`];
        if (!endRecord || endRecord.qaStatus !== "approved" || !endRecord.aspectOk) {
          unapprovedStills.push({
            shotId: `${shotId}__end`,
            qaStatus: endRecord?.qaStatus || "missing",
            aspectOk: endRecord?.aspectOk ?? false,
          });
          continue;
        }
      }

      const shotModel = shot.model || model;
      const shotDuration = Number(shot.clip_duration_sec ?? DEFAULT_VIDEO_DURATION_SEC);
      const shotCreditCost = estimateClipCredits({
        model: shotModel,
        durationSec: shotDuration,
        creditsOverride: shot.credits_override ?? creditsPerClip,
      });

      eligibleShotIds.push(shotId);
      shotPlans.push({
        shotId,
        model: shotModel,
        durationSec: shotDuration,
        credits: shotCreditCost,
        continueFrom: shot.continue_from || null,
        nextTake: priorTakes + 1,
      });
    }

    if (retakeLimitBlocked.length > 0) {
      return {
        ok: false,
        reason: "retake_limit_reached",
        message: `${retakeLimitBlocked.length} shot(s) already reached MAX_CLIP_TAKES=${preset.maxClipTakes}. Revise prompt/motion instead of blind retries, or pass forceRetake: true.`,
        retakeLimitBlocked,
      };
    }

    if (unapprovedStills.length > 0) {
      return {
        ok: false,
        reason: "stills_not_approved",
        message: `Blocked by Stills-First Gate: ${unapprovedStills.length} clip shot(s) do not have approved stills yet. Complete 0-credit QA and call flow_approve_stills first.`,
        unapprovedStills,
        eligibleShotIds,
      };
    }

    let accountCredits = null;
    if (checkLiveBalance) {
      try {
        const bal = await this.driver.getCredits({ profile });
        accountCredits = bal.credits;
      } catch {
        accountCredits = null;
      }
    }

    return planClipBudget({
      episodePaths: paths,
      series: preset.id,
      shotIds: eligibleShotIds,
      shotPlans,
      model,
      creditsPerClip: creditsPerClip ?? DEFAULT_CLIP_CREDITS,
      accountCredits,
      budgetHardCapOverride,
    });
  }

  // ---------------------------------------------------------------------------
  // Tool 10: flow_generate_clips (PAID — multi-take archival, continue_from, QC)
  // ---------------------------------------------------------------------------
  async flowGenerateClips({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
    confirm_token,
    model = DEFAULT_VIDEO_MODEL,
    durationSec = DEFAULT_VIDEO_DURATION_SEC,
    creditsPerClip = null,
    maxCreditsPerClip = DEFAULT_MAX_CREDITS_PER_CLIP,
    forceRetake = false,
    runQc = false,
    skipPostprocess = false,
    profile = null,
    waitMs = 0,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);
    const cast = this.#loadCast(paths, { series: preset.id });
    const shots = normalizeShots(rawList);
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
    const existingManifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });

    const shotMap = new Map();
    for (let i = 0; i < shots.length; i += 1) {
      const shot = shots[i];
      const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);
      shotMap.set(shotId, shot);
    }

    const requestedIds =
      Array.isArray(shotIds) && shotIds.length > 0
        ? shotIds.map(String)
        : [...shotMap.entries()]
            .filter(([, s]) => getShotMode(s) === "clip")
            .map(([id]) => id);

    // 1. Validate every shot BEFORE consuming the single-use confirm_token
    const items = [];
    let totalPlannedCredits = 0;

    for (const shotId of requestedIds) {
      const shot = shotMap.get(shotId);
      if (!shot) {
        return { ok: false, reason: "unknown_shot_id", message: `Shot "${shotId}" not found in flow-shot-list.json.` };
      }

      const existingClip = existingManifest.clips?.[shotId];
      const priorTakes = Array.isArray(existingClip?.takes)
        ? existingClip.takes.length
        : existingClip
          ? 1
          : 0;
      if (!forceRetake && priorTakes >= preset.maxClipTakes) {
        return {
          ok: false,
          reason: "retake_limit_reached",
          shotId,
          message: `Shot "${shotId}" already has ${priorTakes} take(s) (limit ${preset.maxClipTakes}). Redesign prompt/motion or pass forceRetake: true.`,
        };
      }

      const stillRec = qaStore.stills?.[shotId];
      if (!shot.continue_from && (!stillRec || stillRec.qaStatus !== "approved" || !stillRec.filePath || !fs.existsSync(stillRec.filePath))) {
        return {
          ok: false,
          reason: "stills_not_approved",
          message: `Shot "${shotId}" does not have an approved still on disk.`,
        };
      }

      let endRec = null;
      if (shot.end_still_prompt) {
        endRec = qaStore.stills?.[`${shotId}__end`];
        if (!endRec || endRec.qaStatus !== "approved" || !endRec.filePath || !fs.existsSync(endRec.filePath)) {
          return {
            ok: false,
            reason: "end_still_not_approved",
            message: `Shot "${shotId}" end frame ("${shotId}__end") is not approved on disk.`,
          };
        }
      }

      const track = getShotTrack(shot);
      const projectId =
        track === "character" ? workspace?.characterProjectId || null : workspace?.sceneryProjectId || null;

      const rawVideoPrompt = shot.video_prompt || shot.motion_prompt || shot.still_prompt || shot.prompt;
      const useSilentGuard = preset.audioPolicy === "silent_with_guard" && shot.preserve_dialogue !== true;
      const videoPrompt = applySilentAudioGuard(rawVideoPrompt, { enabled: useSilentGuard });
      const safety = scanPromptText(videoPrompt, { series: preset.id, shotId, field: "video_prompt" });
      if (!safety.ok) {
        return { ok: false, reason: "unsafe_prompt", shotId, findings: safety.findings };
      }

      const shotModel = shot.model || model;
      const shotDuration = Number(shot.clip_duration_sec ?? durationSec);
      const shotCredits = estimateClipCredits({
        model: shotModel,
        durationSec: shotDuration,
        creditsOverride: shot.credits_override ?? creditsPerClip,
      });
      totalPlannedCredits += shotCredits;

      const takeNum = priorTakes + 1;
      const safeName = sanitizeFilename(shotId);
      const charCtx =
        track === "character" && shot.video_mode === "r2v"
          ? this.#resolveCharacterContext(shot, { cast, workspace })
          : { refs: [] };

      items.push({
        shotId,
        takeNum,
        track,
        projectId,
        prompt: videoPrompt,
        videoMode: shot.video_mode || "i2v",
        initialFrame: stillRec?.filePath || null,
        continueFromShotId: shot.continue_from ? String(shot.continue_from) : null,
        endFrame: endRec?.filePath || null,
        r2vRefs: charCtx.refs,
        model: shotModel,
        aspect: preset.aspect,
        durationSec: shotDuration,
        resolution: DEFAULT_VIDEO_RESOLUTION,
        maxCredits: Math.max(maxCreditsPerClip, shotCredits + 3),
        creditsEstimate: shotCredits,
        rawPath: path.join(paths.clipsRawDir, `${safeName}-t${takeNum}-720p.mp4`),
        takeUpscaledPath: path.join(paths.clipsTakesDir, `${safeName}-t${takeNum}-1080p30.mp4`),
        activeUpscaledPath: path.join(paths.clipsDir, `${safeName}-1080p30.mp4`),
        rawAudioPath:
          preset.audioPolicy === "extract_sidecar"
            ? path.join(paths.clipsAudioDir, `${safeName}-t${takeNum}-raw.wav`)
            : null,
        qa4Path: path.join(paths.clipsQaDir, `${safeName}-t${takeNum}-qa4.jpg`),
        runQc: Boolean(runQc || preset.kind === "drama"),
        skipPostprocess,
        profile,
      });
    }

    // 2. Verify and atomically consume the single-use confirm_token
    const tokenCheck = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: confirm_token,
      shotIds: requestedIds,
      model,
      creditsPerClip: creditsPerClip ?? DEFAULT_CLIP_CREDITS,
      plannedCreditsOverride: totalPlannedCredits,
    });
    if (!tokenCheck.ok) {
      return {
        ok: false,
        reason: tokenCheck.reason,
        message: tokenCheck.message,
      };
    }

    fs.mkdirSync(paths.clipsRawDir, { recursive: true });
    fs.mkdirSync(paths.clipsTakesDir, { recursive: true });
    fs.mkdirSync(paths.clipsQaDir, { recursive: true });

    const job = this.queue.enqueue({
      kind: "generate_clips",
      slug: paths.slug,
      profile,
      items,
      worker: async (item, { signal }) => {
        // Resolve Exact-Join `continue_from` by extracting the real final frame of the previous clip
        let initialFrame = item.initialFrame;
        if (item.continueFromShotId) {
          const liveManifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
          const prevClip = liveManifest.clips?.[item.continueFromShotId];
          const prevVideo = prevClip?.upscaledPath || prevClip?.rawPath;
          if (!prevVideo || !fs.existsSync(prevVideo)) {
            const err = new Error(
              `continue_from="${item.continueFromShotId}" clip does not exist on disk yet. Generate "${item.continueFromShotId}" first.`,
            );
            err.code = "missing_continue_from_clip";
            err.charged = "no";
            throw err;
          }
          const extractedPath = path.join(
            paths.stillsDir,
            `${sanitizeFilename(item.shotId)}__from_${sanitizeFilename(item.continueFromShotId)}.png`,
          );
          await this.extractLastFrameFn({ inputPath: prevVideo, outputPngPath: extractedPath });
          initialFrame = extractedPath;
        }

        let gen;
        try {
          gen = await this.driver.generateVideo({
            prompt: item.prompt,
            initialFrame: item.videoMode === "r2v" ? null : initialFrame,
            endFrame: item.videoMode === "r2v" ? null : item.endFrame,
            refs: item.videoMode === "r2v" ? item.r2vRefs : [],
            model: item.model,
            aspect: item.aspect,
            durationSec: item.durationSec,
            resolution: item.resolution,
            maxCredits: item.maxCredits,
            projectId: item.projectId,
            outFile: item.rawPath,
            profile: item.profile,
            signal,
          });
        } catch (err) {
          if (err.charged === "yes" || err.charged === "maybe") {
            recordCreditEvent(paths.ledgerFile, {
              slug: paths.slug,
              series: preset.id,
              shotId: item.shotId,
              operation: "clip",
              take: item.takeNum,
              model: item.model,
              credits: item.creditsEstimate,
              charged: err.charged,
              mediaId: err.operationId || null,
              note: `Failure (${err.code}): ${err.message}`,
            });
          }
          throw err;
        }

        const actualCredits = gen.creditsSpent ?? item.creditsEstimate;
        recordCreditEvent(paths.ledgerFile, {
          slug: paths.slug,
          series: preset.id,
          shotId: item.shotId,
          operation: "clip",
          take: item.takeNum,
          model: item.model,
          credits: actualCredits,
          charged: gen.charged || "yes",
          mediaId: gen.mediaId,
          note: `Take ${item.takeNum} (${item.durationSec}s 720p raw)`,
        });

        const rawPath = gen.outFile || item.rawPath;
        let post = null;
        if (!item.skipPostprocess) {
          const targetW = preset.aspect === "9:16" ? 1080 : 1920;
          const targetH = preset.aspect === "9:16" ? 1920 : 1080;
          post = await this.upscaleFn({
            inputPath: rawPath,
            outputPath: item.takeUpscaledPath,
            qa4OutputPath: item.qa4Path,
            rawAudioOutputPath: item.rawAudioPath,
            keyframePath: initialFrame,
            durationSec: item.durationSec,
            runQc: item.runQc,
            width: targetW,
            height: targetH,
            fps: 30,
          });
          // Promote latest take to active `flow-clips/<shot>-1080p30.mp4` while keeping all takes intact
          if (fs.existsSync(item.takeUpscaledPath)) {
            fs.copyFileSync(item.takeUpscaledPath, item.activeUpscaledPath);
          }
        }

        const takeRecord = {
          take: item.takeNum,
          mediaId: gen.mediaId,
          model: item.model,
          durationSec: item.durationSec,
          credits: actualCredits,
          prompt: item.prompt,
          initialFrame,
          endFrame: item.endFrame,
          continueFrom: item.continueFromShotId,
          rawPath,
          rawSha256: post?.rawSha256 || (fs.existsSync(rawPath) ? sha256File(rawPath) : null),
          takeUpscaledPath: post ? item.takeUpscaledPath : null,
          upscaledSha256: post?.upscaledSha256 || null,
          rawAudioPath: post?.rawAudioPath || null,
          qa4Path: post?.qa4Path || null,
          qc: post?.qc || null,
          spec: post?.spec || null,
          generatedAt: new Date().toISOString(),
        };

        const liveManifest = readJsonSafe(paths.clipsManifestFile, {
          slug: paths.slug,
          series: preset.id,
          clips: {},
        });
        liveManifest.clips = liveManifest.clips || {};
        const prev = liveManifest.clips[item.shotId];
        const prevTakes = Array.isArray(prev?.takes) ? prev.takes : prev ? [{ ...prev, take: 1 }] : [];
        const takes = [...prevTakes, takeRecord];

        liveManifest.clips[item.shotId] = {
          shotId: item.shotId,
          track: item.track,
          projectId: gen.projectId || item.projectId,
          selectedTake: item.takeNum,
          mediaId: takeRecord.mediaId,
          model: takeRecord.model,
          durationSec: takeRecord.durationSec,
          credits: takeRecord.credits,
          prompt: takeRecord.prompt,
          initialFrame: takeRecord.initialFrame,
          endFrame: takeRecord.endFrame,
          rawPath: takeRecord.rawPath,
          rawSha256: takeRecord.rawSha256,
          upscaledPath: post ? item.activeUpscaledPath : null,
          upscaledSha256: takeRecord.upscaledSha256,
          rawAudioPath: takeRecord.rawAudioPath,
          qa4Path: takeRecord.qa4Path,
          qc: takeRecord.qc,
          spec: takeRecord.spec,
          takes,
          generatedAt: takeRecord.generatedAt,
        };
        saveClipsManifest(paths.clipsManifestFile, liveManifest);

        return liveManifest.clips[item.shotId];
      },
      onComplete: async () => {
        const manifest = readJsonSafe(paths.clipsManifestFile, {
          slug: paths.slug,
          series: preset.id,
          clips: {},
        });
        const list = Object.values(manifest.clips || {});
        writeClipsQaGallery({
          galleryFile: paths.clipsGalleryFile,
          slug: paths.slug,
          series: preset.id,
          clips: list,
        });
        const bridge = buildImportBridge({
          slug: paths.slug,
          series: preset.id,
          clipsManifest: manifest,
          shots,
        });
        atomicWriteJson(paths.clipsImportBridgeFile, bridge);
        const ledger = loadCreditLedger(paths.ledgerFile, { slug: paths.slug, series: preset.id });
        return {
          clipsManifestFile: paths.clipsManifestFile,
          clipsImportBridgeFile: paths.clipsImportBridgeFile,
          clipsGalleryFile: paths.clipsGalleryFile,
          totalClips: list.length,
          totalSpentCredits: ledger.totalSpentCredits,
          totalMaybeCredits: ledger.totalMaybeCredits,
        };
      },
    });

    if (waitMs > 0) {
      const waited = await this.queue.waitForJob(job.jobId, { timeoutMs: waitMs });
      return {
        ok: true,
        job_id: job.jobId,
        ...waited,
        clipsManifestFile: paths.clipsManifestFile,
        clipsImportBridgeFile: paths.clipsImportBridgeFile,
        clipsGalleryFile: paths.clipsGalleryFile,
      };
    }

    return {
      ok: true,
      job_id: job.jobId,
      queued: items.length,
      status: job.status,
      clipsManifestFile: paths.clipsManifestFile,
      clipsGalleryFile: paths.clipsGalleryFile,
      nextStep: "Poll progress with flow_wait(job_id). Inspect flow-clips/qa-gallery.html, select best takes with flow_select_take, and verify with flow_episode_ledger.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 11: flow_select_take (0 credits — promote chosen take, keep all takes)
  // ---------------------------------------------------------------------------
  async flowSelectTake({ slug, series = null, workdir = null, shotId, take }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "drama-16x9";
    const manifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
    const clip = manifest.clips?.[shotId];
    if (!clip) {
      return { ok: false, reason: "clip_not_found", message: `Shot "${shotId}" not found in clips manifest.` };
    }
    const takes = Array.isArray(clip.takes) ? clip.takes : [];
    const chosen = takes.find((t) => Number(t.take) === Number(take));
    if (!chosen) {
      return {
        ok: false,
        reason: "take_not_found",
        availableTakes: takes.map((t) => t.take),
        message: `Take ${take} not found for shot "${shotId}".`,
      };
    }

    const activePath = path.join(paths.clipsDir, `${sanitizeFilename(shotId)}-1080p30.mp4`);
    if (chosen.takeUpscaledPath && fs.existsSync(chosen.takeUpscaledPath)) {
      fs.copyFileSync(chosen.takeUpscaledPath, activePath);
    }

    clip.selectedTake = chosen.take;
    clip.mediaId = chosen.mediaId;
    clip.rawPath = chosen.rawPath;
    clip.rawSha256 = chosen.rawSha256;
    clip.upscaledPath = fs.existsSync(activePath) ? activePath : chosen.takeUpscaledPath;
    clip.upscaledSha256 = chosen.upscaledSha256;
    clip.rawAudioPath = chosen.rawAudioPath || null;
    clip.qa4Path = chosen.qa4Path;
    clip.qc = chosen.qc || null;
    clip.prompt = chosen.prompt;

    saveClipsManifest(paths.clipsManifestFile, manifest);
    writeClipsQaGallery({
      galleryFile: paths.clipsGalleryFile,
      slug: paths.slug,
      series: effectiveSeries,
      clips: Object.values(manifest.clips || {}),
    });

    const shots = fs.existsSync(paths.shotListFile)
      ? normalizeShots(JSON.parse(fs.readFileSync(paths.shotListFile, "utf8")))
      : [];
    const bridge = buildImportBridge({
      slug: paths.slug,
      series: effectiveSeries,
      clipsManifest: manifest,
      shots,
    });
    atomicWriteJson(paths.clipsImportBridgeFile, bridge);

    return {
      ok: true,
      shotId,
      selectedTake: chosen.take,
      totalPreservedTakes: takes.length,
      activePath: clip.upscaledPath,
      clipsImportBridgeFile: paths.clipsImportBridgeFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 12: flow_extend_clip (PAID — requires confirm_token; gflow video extend)
  // ---------------------------------------------------------------------------
  async flowExtendClip({
    slug,
    series = null,
    workdir = null,
    shotId,
    prompt,
    confirm_token,
    durationSec = 5,
    refs = [],
    creditsEstimate = null,
    maxCredits = DEFAULT_MAX_CREDITS_PER_CLIP,
    skipPostprocess = false,
    profile = null,
    waitMs = 0,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "drama-16x9";
    const preset = getSeriesPreset(effectiveSeries);

    const manifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
    const existing = manifest.clips?.[shotId];
    if (!existing) {
      return { ok: false, reason: "clip_not_found", message: `Shot "${shotId}" must exist in flow-clips/manifest.json before extending.` };
    }

    const safety = scanPromptText(prompt, { series: preset.id, shotId, field: "extend_prompt" });
    if (!safety.ok) {
      return { ok: false, reason: "unsafe_prompt", shotId, findings: safety.findings };
    }

    const estCredits = estimateClipCredits({
      model: existing.model || DEFAULT_VIDEO_MODEL,
      durationSec,
      creditsOverride: creditsEstimate,
    });

    const tokenCheck = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: confirm_token,
      shotIds: [shotId],
      model: "extend",
      plannedCreditsOverride: estCredits,
    });
    if (!tokenCheck.ok) {
      return { ok: false, reason: tokenCheck.reason, message: tokenCheck.message };
    }

    const prevTakes = Array.isArray(existing.takes) ? existing.takes : [{ ...existing, take: 1 }];
    const takeNum = prevTakes.length + 1;
    const safeName = sanitizeFilename(shotId);
    const source = existing.mediaId || existing.rawPath || existing.upscaledPath;
    const rawOut = path.join(paths.clipsRawDir, `${safeName}-ext-t${takeNum}-720p.mp4`);
    const takeUp = path.join(paths.clipsTakesDir, `${safeName}-ext-t${takeNum}-1080p30.mp4`);
    const activeUp = path.join(paths.clipsDir, `${safeName}-1080p30.mp4`);
    const qa4Out = path.join(paths.clipsQaDir, `${safeName}-ext-t${takeNum}-qa4.jpg`);

    const job = this.queue.enqueue({
      kind: "extend_clip",
      slug: paths.slug,
      profile,
      items: [{ shotId, takeNum, source, prompt, durationSec, refs, rawOut, takeUp, activeUp, qa4Out }],
      worker: async (item, { signal }) => {
        let gen;
        try {
          gen = await this.driver.extendVideo({
            source: item.source,
            prompt: item.prompt,
            projectId: existing.projectId || workspace?.characterProjectId || null,
            durationSec: item.durationSec,
            refs: item.refs,
            maxCredits: Math.max(maxCredits, estCredits + 5),
            outFile: item.rawOut,
            profile,
            signal,
          });
        } catch (err) {
          if (err.charged === "yes" || err.charged === "maybe") {
            recordCreditEvent(paths.ledgerFile, {
              slug: paths.slug,
              series: preset.id,
              shotId,
              operation: "extend",
              take: item.takeNum,
              model: "extend",
              credits: estCredits,
              charged: err.charged,
              mediaId: err.operationId || null,
              note: `Extend failure (${err.code}): ${err.message}`,
            });
          }
          throw err;
        }

        const actualCredits = gen.creditsSpent ?? estCredits;
        recordCreditEvent(paths.ledgerFile, {
          slug: paths.slug,
          series: preset.id,
          shotId,
          operation: "extend",
          take: item.takeNum,
          model: "extend",
          credits: actualCredits,
          charged: gen.charged || "yes",
          mediaId: gen.mediaId,
          note: `Extended clip take ${item.takeNum} (+${item.durationSec}s)`,
        });

        const rawPath = gen.outFile || item.rawOut;
        let post = null;
        if (!skipPostprocess) {
          const targetW = preset.aspect === "9:16" ? 1080 : 1920;
          const targetH = preset.aspect === "9:16" ? 1920 : 1080;
          post = await this.upscaleFn({
            inputPath: rawPath,
            outputPath: item.takeUp,
            qa4OutputPath: item.qa4Out,
            width: targetW,
            height: targetH,
            fps: 30,
          });
          if (fs.existsSync(item.takeUp)) {
            fs.copyFileSync(item.takeUp, item.activeUp);
          }
        }

        const takeRecord = {
          take: item.takeNum,
          extended: true,
          mediaId: gen.mediaId,
          model: "extend",
          durationSec: (existing.durationSec || 4) + item.durationSec,
          credits: actualCredits,
          prompt: item.prompt,
          rawPath,
          rawSha256: post?.rawSha256 || null,
          takeUpscaledPath: post ? item.takeUp : null,
          upscaledSha256: post?.upscaledSha256 || null,
          qa4Path: post?.qa4Path || null,
          generatedAt: new Date().toISOString(),
        };

        const liveManifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
        const target = liveManifest.clips[shotId];
        target.takes = [...(Array.isArray(target.takes) ? target.takes : []), takeRecord];
        target.selectedTake = item.takeNum;
        target.mediaId = takeRecord.mediaId || target.mediaId;
        target.upscaledPath = post ? item.activeUp : target.upscaledPath;
        target.upscaledSha256 = takeRecord.upscaledSha256 || target.upscaledSha256;
        target.qa4Path = takeRecord.qa4Path || target.qa4Path;
        saveClipsManifest(paths.clipsManifestFile, liveManifest);
        return takeRecord;
      },
    });

    if (waitMs > 0) {
      const waited = await this.queue.waitForJob(job.jobId, { timeoutMs: waitMs });
      return { ok: true, job_id: job.jobId, ...waited };
    }

    return { ok: true, job_id: job.jobId, status: job.status };
  }

  // ---------------------------------------------------------------------------
  // Tool 13: flow_reconcile (0 credits — recover `maybe` billed clips + resume list)
  // ---------------------------------------------------------------------------
  async flowReconcile({
    slug,
    series = null,
    workdir = null,
    downloadMissing = true,
    profile = null,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);

    const ledger = loadCreditLedger(paths.ledgerFile, { slug: paths.slug, series: preset.id });
    const maybeEntries = ledger.entries.filter((e) => e.charged === "maybe");

    let remoteVideos = [];
    try {
      remoteVideos = await this.driver.listRemoteVideos({ limit: 100, profile });
    } catch (err) {
      return {
        ok: false,
        reason: "remote_list_failed",
        message: err.message,
        maybeEntriesCount: maybeEntries.length,
      };
    }

    const remoteById = new Map();
    for (const v of remoteVideos) {
      const id = v?.media_id || v?.id;
      if (id) remoteById.set(String(id), v);
    }

    const recovered = [];
    const unresolved = [];

    for (const entry of maybeEntries) {
      const match = entry.mediaId ? remoteById.get(String(entry.mediaId)) : null;
      if (!match) {
        unresolved.push({ shotId: entry.shotId, mediaId: entry.mediaId, note: entry.note });
        continue;
      }

      let downloadedPath = null;
      if (downloadMissing) {
        fs.mkdirSync(paths.clipsRawDir, { recursive: true });
        const dl = await this.driver.downloadMedia({
          mediaId: entry.mediaId,
          outDir: paths.clipsRawDir,
          profile,
        });
        downloadedPath = dl.outFile;
      }

      // Settle `maybe` -> `yes` once confirmed in Flow catalog
      entry.charged = "yes";
      entry.note = `${entry.note} [reconciled ${new Date().toISOString()}]`;
      recovered.push({
        shotId: entry.shotId,
        mediaId: entry.mediaId,
        downloadedPath,
      });
    }

    if (recovered.length > 0) {
      recalculateLedgerTotals(ledger);
      atomicWriteJson(paths.ledgerFile, ledger);
    }

    const manifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
    const shots = fs.existsSync(paths.shotListFile)
      ? normalizeShots(JSON.parse(fs.readFileSync(paths.shotListFile, "utf8")))
      : [];
    const remainingMissingClips = shots
      .filter((s) => getShotMode(s) === "clip")
      .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`))
      .filter((id) => !manifest.clips?.[id]);

    return {
      ok: true,
      slug: paths.slug,
      checkedMaybeEntries: maybeEntries.length,
      recovered,
      unresolved,
      remainingMissingClips,
      resumeHint:
        remainingMissingClips.length > 0
          ? "Call flow_plan_clips({ slug, resumeMissingOnly: true }) to mint a confirm_token for only the remaining clips."
          : "All planned clips are present on disk.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 14: flow_wait (0 credits)
  // ---------------------------------------------------------------------------
  async flowWait({ job_id, timeout_ms = 25_000 }) {
    const capped = Math.min(45_000, Math.max(100, Number(timeout_ms) || 25_000));
    return this.queue.waitForJob(job_id, { timeoutMs: capped });
  }

  // ---------------------------------------------------------------------------
  // Tool 15: flow_cancel (0 credits)
  // ---------------------------------------------------------------------------
  async flowCancel({ job_id }) {
    return this.queue.cancelJob(job_id);
  }

  // ---------------------------------------------------------------------------
  // Tool 16: flow_episode_ledger (0 credits)
  // ---------------------------------------------------------------------------
  async flowEpisodeLedger({ slug, series = null, workdir = null }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const effectiveSeries = series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);

    const ledger = loadCreditLedger(paths.ledgerFile, { slug: paths.slug, series: preset.id });
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });
    const clipsManifest = readJsonSafe(paths.clipsManifestFile, { clips: {} });
    const shotList = fs.existsSync(paths.shotListFile) ? JSON.parse(fs.readFileSync(paths.shotListFile, "utf8")) : null;
    const shots = shotList ? normalizeShots(shotList) : [];

    const expectedClipIds = shots
      .filter((s) => getShotMode(s) === "clip")
      .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`));
    const cutShotIds = shots
      .filter((s) => getShotMode(s) === "cut")
      .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`));

    const completedClips = Object.keys(clipsManifest.clips || {});
    const missingClips = expectedClipIds.filter((id) => !clipsManifest.clips?.[id]);
    const totalTakes = Object.values(clipsManifest.clips || {}).reduce(
      (sum, c) => sum + (Array.isArray(c.takes) ? c.takes.length : 1),
      0,
    );

    const stillsEntries = Object.values(qaStore.stills || {});
    const stillsSummary = {
      total: stillsEntries.length,
      approved: stillsEntries.filter((s) => s.qaStatus === "approved").length,
      pending: stillsEntries.filter((s) => s.qaStatus === "pending").length,
      rejected: stillsEntries.filter((s) => s.qaStatus === "rejected").length,
    };

    const readyForDrivePush =
      missingClips.length === 0 &&
      stillsSummary.rejected === 0 &&
      ledger.totalMaybeCredits === 0 &&
      ledger.totalSpentCredits <= preset.budgetHardCap;

    return {
      ok: true,
      slug: paths.slug,
      series: preset.id,
      seriesLabel: preset.label,
      workdir: paths.root,
      dualProjects: {
        characterProjectId: workspace?.characterProjectId || null,
        sceneryProjectId: workspace?.sceneryProjectId || null,
      },
      credits: {
        spent: ledger.totalSpentCredits,
        maybe: ledger.totalMaybeCredits,
        budgetSoftCap: preset.budgetSoftCap,
        budgetHardCap: preset.budgetHardCap,
        remainingHardCap: preset.budgetHardCap - (ledger.totalSpentCredits + ledger.totalMaybeCredits),
        entriesCount: ledger.entries.length,
      },
      stills: stillsSummary,
      clips: {
        expected: expectedClipIds.length,
        completed: completedClips.length,
        totalTakes,
        zeroCreditCuts: cutShotIds.length,
        missing: missingClips,
      },
      importBridgeFile: fs.existsSync(paths.clipsImportBridgeFile) ? paths.clipsImportBridgeFile : null,
      readyForDrivePush,
      drivePushCommand: buildDrivePushCommand({
        slug: paths.slug,
        series: preset.id,
        workdir: paths.root,
        dramaName: workspace?.dramaName,
        episodeLabel: workspace?.episodeLabel,
      }),
    };
  }
}
