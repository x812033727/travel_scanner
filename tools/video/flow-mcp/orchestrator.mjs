/**
 * Core orchestrator implementing Mokaair's 10 Google Flow MCP tools.
 *
 * Enforces every guard from `FLOW-PRODUCTION-RULES.md` & `CURIO-FLOW-CHECKLIST.md`:
 *   1. Route B `work/video-episodes/<slug>/` path boundary (0 GitHub commits)
 *   2. Dual-project strict isolation (`character` vs `scenery`)
 *   3. Full-axis safety prompt preflight scanner
 *   4. Zero-credit `Nano Banana 2.1` stills-first + 1376x768 binary aspect check
 *   5. Explicit QA sign-off (`flow_approve_stills`) before unlocking paid clips
 *   6. Series credit budget hard caps + single-use `confirm_token` gate
 *   7. Free 720p download -> local `ffmpeg` 1080p30/bt709/tv/-an + 4-frame QA + SHA-256 manifest
 */

import fs from "node:fs";
import path from "node:path";
import {
  DEFAULT_CLIP_CREDITS,
  DEFAULT_IMAGE_MODEL,
  DEFAULT_MAX_CREDITS_PER_CLIP,
  DEFAULT_VIDEO_DURATION_SEC,
  DEFAULT_VIDEO_MODEL,
  DEFAULT_VIDEO_RESOLUTION,
  REPO_ROOT,
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
import { sha256File, upscaleClipTo1080p30 } from "./postprocess/upscale-1080p30.mjs";

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

export class FlowOrchestrator {
  constructor({
    driver = null,
    queue = null,
    repoRoot = REPO_ROOT,
    runtimeHome = resolveRuntimeHome(),
    rulesCacheRoot = null,
    allowExternalWorkdir = false,
    upscaleFn = upscaleClipTo1080p30,
  } = {}) {
    this.repoRoot = repoRoot;
    this.runtimeHome = runtimeHome;
    this.rulesCacheRoot = rulesCacheRoot || resolveRulesCacheRoot(repoRoot);
    this.allowExternalWorkdir = allowExternalWorkdir;
    this.driver = driver || new GflowCliDriver({ runtimeHome });
    this.queue = queue || new JobQueue({ runtimeHome });
    this.upscaleFn = upscaleFn;
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
        `Missing flow-shot-list.json at "${paths.shotListFile}". Place your episode shot list under work/video-episodes/<slug>/flow-shot-list.json first.`,
      );
    }
    return JSON.parse(fs.readFileSync(paths.shotListFile, "utf8"));
  }

  #loadWorkspace(paths) {
    return readJsonSafe(paths.workspaceFile, null);
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

  // ---------------------------------------------------------------------------
  // Tool 1: flow_status (0 credits)
  // ---------------------------------------------------------------------------
  async flowStatus({ profile = null, refreshCredits = false } = {}) {
    const lock = this.queue.getLockStatus();
    let auth = null;
    let credits = null;
    let driverError = null;

    try {
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
      runtimeHome: this.runtimeHome,
      lock,
      auth,
      credits,
      error: driverError,
      nextStep: auth?.authenticated
        ? "Session is ready. Run flow_preflight_shotlist or flow_init_episode."
        : "Run `npm run flow -- login` on your local desktop to sign into Google Flow via Chrome.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 2: flow_init_episode (0 credits)
  // ---------------------------------------------------------------------------
  async flowInitEpisode({
    slug,
    series = "curio",
    workdir = null,
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
      schemaVersion: 1,
      slug: paths.slug,
      series: preset.id,
      seriesLabel: preset.label,
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
          ? "Some canon character sheets were not found in `.cache/video-drive/rules/`. Run `npm run vdrive -- pull-rules explainer` first."
          : null,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 3: flow_preflight_shotlist (0 credits)
  // ---------------------------------------------------------------------------
  async flowPreflightShotlist({ slug, series = null, workdir = null, shotList = null }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = shotList || this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";

    const report = preflightShotList(rawList, { series: effectiveSeries });
    const enriched = {
      ...report,
      slug: paths.slug,
      checkedAt: new Date().toISOString(),
      dualProjectsConfigured: Boolean(
        workspace?.characterProjectId &&
          workspace?.sceneryProjectId &&
          workspace.characterProjectId !== workspace.sceneryProjectId,
      ),
    };

    atomicWriteJson(paths.preflightFile, enriched);
    return {
      ...enriched,
      preflightFile: paths.preflightFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 4: flow_generate_stills (0 credits — Nano Banana 2.1 + 1376x768 check)
  // ---------------------------------------------------------------------------
  async flowGenerateStills({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
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

    // Mandatory preflight safety & isolation gate before opening Chrome
    const preflight = preflightShotList(rawList, { series: effectiveSeries });
    if (!preflight.ok) {
      return {
        ok: false,
        reason: "preflight_failed",
        message: `Blocked before Chrome launch: shot list has ${preflight.blockerCount} blocker(s). Fix them and re-run flow_preflight_shotlist.`,
        preflight,
      };
    }

    const shots = normalizeShots(rawList);
    const filterSet = Array.isArray(shotIds) && shotIds.length > 0 ? new Set(shotIds.map(String)) : null;
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });

    const items = [];
    for (let i = 0; i < shots.length; i += 1) {
      const shot = shots[i];
      const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);
      if (filterSet && !filterSet.has(shotId)) continue;

      const existingQa = qaStore.stills?.[shotId];
      if (existingQa?.qaStatus === "approved" && !overwriteApproved) {
        continue;
      }

      const track = String(shot.track || (shot.has_character ? "character" : "scenery")).toLowerCase();
      const projectId =
        track === "character" ? workspace?.characterProjectId || null : workspace?.sceneryProjectId || null;

      if (workspace?.characterProjectId && workspace?.sceneryProjectId && !projectId) {
        throw new Error(`Shot "${shotId}" track "${track}" has no bound Flow project.`);
      }

      // Enforce dual-project ref isolation at execution time too
      const refs =
        track === "character"
          ? [
              ...(Array.isArray(shot.character_refs) ? shot.character_refs : []),
              ...(Array.isArray(shot.refs) ? shot.refs : []),
              ...(!shot.character_refs && !shot.refs ? workspace?.localCanonPaths || [] : []),
            ]
          : [];

      const stillPrompt = shot.still_prompt || shot.prompt || shot.data?.prompt;
      const safety = scanPromptText(stillPrompt, { series: preset.id, shotId, field: "still_prompt" });
      if (!safety.ok) {
        return {
          ok: false,
          reason: "unsafe_prompt",
          shotId,
          findings: safety.findings,
        };
      }

      const outFile = path.join(paths.stillsDir, `${sanitizeFilename(shotId)}.png`);
      items.push({
        shotId,
        track,
        projectId,
        prompt: stillPrompt,
        refs,
        outFile,
        model,
        aspect: preset.aspect,
        expectedWidth: preset.targetStillWidth,
        expectedHeight: preset.targetStillHeight,
        profile,
      });

      // Also generate end-frame still if a clip shot defines `end_still_prompt`
      if (shot.end_still_prompt && String(shot.end_still_prompt).trim()) {
        const endId = `${shotId}__end`;
        items.push({
          shotId: endId,
          parentShotId: shotId,
          isEndFrame: true,
          track,
          projectId,
          prompt: String(shot.end_still_prompt).trim(),
          refs,
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
      items,
      worker: async (item, { signal }) => {
        const gen = await this.driver.generateImage({
          prompt: item.prompt,
          refs: item.refs,
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
          // Move aspect-drifted (e.g. silent 1:1) still into `_rejected/` so it cannot enter production
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
      nextStep: "Poll progress with flow_wait(job_id), inspect stills/qa-gallery.html, then call flow_approve_stills.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 5: flow_approve_stills (0 credits — unlocks clip generation)
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
  // Tool 6: flow_plan_clips (0 credits — Dry-Run budget & confirm_token)
  // ---------------------------------------------------------------------------
  async flowPlanClips({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
    model = DEFAULT_VIDEO_MODEL,
    creditsPerClip = DEFAULT_CLIP_CREDITS,
    budgetHardCapOverride = null,
    checkLiveBalance = false,
    profile = null,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);

    const preflight = preflightShotList(rawList, { series: effectiveSeries });
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
    const filterSet = Array.isArray(shotIds) && shotIds.length > 0 ? new Set(shotIds.map(String)) : null;

    const eligibleShotIds = [];
    const unapprovedStills = [];

    for (let i = 0; i < shots.length; i += 1) {
      const shot = shots[i];
      const shotId = String(shot.id || shot.shot_id || `shot_${String(i + 1).padStart(3, "0")}`);
      const mode = String(shot.mode || (shot.video_prompt || shot.motion_prompt ? "clip" : "still")).toLowerCase();
      if (mode !== "clip") continue;
      if (filterSet && !filterSet.has(shotId)) continue;

      const stillRecord = qaStore.stills?.[shotId];
      if (!stillRecord || stillRecord.qaStatus !== "approved" || !stillRecord.aspectOk) {
        unapprovedStills.push({
          shotId,
          qaStatus: stillRecord?.qaStatus || "missing",
          aspectOk: stillRecord?.aspectOk ?? false,
        });
        continue;
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

      eligibleShotIds.push(shotId);
    }

    if (unapprovedStills.length > 0) {
      return {
        ok: false,
        reason: "stills_not_approved",
        message: `Blocked by Stills-First Gate: ${unapprovedStills.length} clip shot(s) do not have approved 16:9 stills yet. Complete 0-credit QA and call flow_approve_stills first.`,
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
      model,
      creditsPerClip,
      accountCredits,
      budgetHardCapOverride,
    });
  }

  // ---------------------------------------------------------------------------
  // Tool 7: flow_generate_clips (PAID — requires confirm_token + 1080p30 upscale)
  // ---------------------------------------------------------------------------
  async flowGenerateClips({
    slug,
    series = null,
    workdir = null,
    shotIds = null,
    confirm_token,
    model = DEFAULT_VIDEO_MODEL,
    durationSec = DEFAULT_VIDEO_DURATION_SEC,
    creditsPerClip = DEFAULT_CLIP_CREDITS,
    maxCreditsPerClip = DEFAULT_MAX_CREDITS_PER_CLIP,
    skipPostprocess = false,
    profile = null,
    waitMs = 0,
  }) {
    const paths = this.#paths(slug, workdir);
    const workspace = this.#loadWorkspace(paths);
    const rawList = this.#loadShotList(paths);
    const effectiveSeries = series || rawList.series || workspace?.series || "curio";
    const preset = getSeriesPreset(effectiveSeries);
    const shots = normalizeShots(rawList);
    const qaStore = this.#loadStillsQa(paths, { slug: paths.slug, series: preset.id });

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
            .filter(([, s]) => String(s.mode || (s.video_prompt || s.motion_prompt ? "clip" : "still")).toLowerCase() === "clip")
            .map(([id]) => id);

    // 1. Validate every shot's Stills-First QA (start + optional end frame) & safety BEFORE consuming token
    const items = [];
    for (const shotId of requestedIds) {
      const shot = shotMap.get(shotId);
      if (!shot) {
        return { ok: false, reason: "unknown_shot_id", message: `Shot "${shotId}" not found in flow-shot-list.json.` };
      }

      const stillRec = qaStore.stills?.[shotId];
      if (!stillRec || stillRec.qaStatus !== "approved" || !stillRec.filePath || !fs.existsSync(stillRec.filePath)) {
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

      const track = String(shot.track || (shot.has_character ? "character" : "scenery")).toLowerCase();
      const projectId =
        track === "character" ? workspace?.characterProjectId || null : workspace?.sceneryProjectId || null;

      const videoPrompt = shot.video_prompt || shot.motion_prompt || shot.still_prompt || shot.prompt;
      const safety = scanPromptText(videoPrompt, { series: preset.id, shotId, field: "video_prompt" });
      if (!safety.ok) {
        return { ok: false, reason: "unsafe_prompt", shotId, findings: safety.findings };
      }

      const safeName = sanitizeFilename(shotId);
      items.push({
        shotId,
        track,
        projectId,
        prompt: videoPrompt,
        initialFrame: stillRec.filePath,
        endFrame: endRec?.filePath || null,
        model,
        aspect: preset.aspect,
        durationSec: Number(shot.clip_duration_sec ?? durationSec),
        resolution: DEFAULT_VIDEO_RESOLUTION, // Always free 720p download; upscale locally
        maxCredits: maxCreditsPerClip,
        creditsPerClip,
        rawPath: path.join(paths.clipsRawDir, `${safeName}-720p.mp4`),
        upscaledPath: path.join(paths.clipsDir, `${safeName}-1080p30.mp4`),
        qa4Path: path.join(paths.clipsQaDir, `${safeName}-qa4.jpg`),
        skipPostprocess,
        profile,
      });
    }

    // 2. Verify and atomically consume the single-use confirm_token only after all prechecks pass
    const tokenCheck = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: confirm_token,
      shotIds: requestedIds,
      model,
      creditsPerClip,
    });
    if (!tokenCheck.ok) {
      return {
        ok: false,
        reason: tokenCheck.reason,
        message: tokenCheck.message,
      };
    }

    fs.mkdirSync(paths.clipsRawDir, { recursive: true });
    fs.mkdirSync(paths.clipsQaDir, { recursive: true });

    const job = this.queue.enqueue({
      kind: "generate_clips",
      slug: paths.slug,
      items,
      worker: async (item, { signal }) => {
        let gen;
        try {
          gen = await this.driver.generateVideo({
            prompt: item.prompt,
            initialFrame: item.initialFrame,
            endFrame: item.endFrame,
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
          // Record `maybe` / `yes` spend accurately even on failure so budget caps stay honest
          if (err.charged === "yes" || err.charged === "maybe") {
            recordCreditEvent(paths.ledgerFile, {
              slug: paths.slug,
              series: preset.id,
              shotId: item.shotId,
              model: item.model,
              credits: item.creditsPerClip,
              charged: err.charged,
              mediaId: err.operationId || null,
              note: `Failure (${err.code}): ${err.message}`,
            });
          }
          throw err;
        }

        const actualCredits = gen.creditsSpent ?? item.creditsPerClip;
        recordCreditEvent(paths.ledgerFile, {
          slug: paths.slug,
          series: preset.id,
          shotId: item.shotId,
          model: item.model,
          credits: actualCredits,
          charged: gen.charged || "yes",
          mediaId: gen.mediaId,
          note: "720p raw clip generated",
        });

        const rawPath = gen.outFile || item.rawPath;
        let post = null;
        if (!item.skipPostprocess) {
          const targetW = preset.aspect === "9:16" ? 1080 : 1920;
          const targetH = preset.aspect === "9:16" ? 1920 : 1080;
          post = await this.upscaleFn({
            inputPath: rawPath,
            outputPath: item.upscaledPath,
            qa4OutputPath: item.qa4Path,
            width: targetW,
            height: targetH,
            fps: 30,
          });
        }

        const clipEntry = {
          shotId: item.shotId,
          track: item.track,
          projectId: gen.projectId || item.projectId,
          mediaId: gen.mediaId,
          model: item.model,
          credits: actualCredits,
          prompt: item.prompt,
          initialFrame: item.initialFrame,
          endFrame: item.endFrame,
          rawPath,
          rawSha256: post?.rawSha256 || (fs.existsSync(rawPath) ? sha256File(rawPath) : null),
          upscaledPath: post ? item.upscaledPath : null,
          upscaledSha256: post?.upscaledSha256 || null,
          qa4Path: post?.qa4Path || null,
          spec: post?.spec || null,
          generatedAt: new Date().toISOString(),
        };

        // Incremental manifest save so partial progress survives crashes
        const existingManifest = readJsonSafe(paths.clipsManifestFile, {
          slug: paths.slug,
          series: preset.id,
          clips: {},
        });
        existingManifest.clips = existingManifest.clips || {};
        existingManifest.clips[item.shotId] = clipEntry;
        saveClipsManifest(paths.clipsManifestFile, existingManifest);

        return clipEntry;
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
        const ledger = loadCreditLedger(paths.ledgerFile, { slug: paths.slug, series: preset.id });
        return {
          clipsManifestFile: paths.clipsManifestFile,
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
      nextStep: "Poll progress with flow_wait(job_id). When done, inspect flow-clips/qa-gallery.html and run flow_episode_ledger.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 8: flow_wait (0 credits)
  // ---------------------------------------------------------------------------
  async flowWait({ job_id, timeout_ms = 25_000 }) {
    const capped = Math.min(45_000, Math.max(100, Number(timeout_ms) || 25_000));
    return this.queue.waitForJob(job_id, { timeoutMs: capped });
  }

  // ---------------------------------------------------------------------------
  // Tool 9: flow_cancel (0 credits)
  // ---------------------------------------------------------------------------
  async flowCancel({ job_id }) {
    return this.queue.cancelJob(job_id);
  }

  // ---------------------------------------------------------------------------
  // Tool 10: flow_episode_ledger (0 credits)
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
      .filter((s) => String(s.mode || (s.video_prompt || s.motion_prompt ? "clip" : "still")).toLowerCase() === "clip")
      .map((s, idx) => String(s.id || s.shot_id || `shot_${String(idx + 1).padStart(3, "0")}`));

    const completedClips = Object.keys(clipsManifest.clips || {});
    const missingClips = expectedClipIds.filter((id) => !clipsManifest.clips?.[id]);

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
      ledger.totalSpentCredits + ledger.totalMaybeCredits <= preset.budgetHardCap;

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
        missing: missingClips,
      },
      readyForDrivePush,
      drivePushCommand: `npm run vdrive -- push-episode --series ${preset.id} --path "<分類>/<代碼>/製作檔/${paths.slug}" --from "${paths.root}"`,
    };
  }
}
