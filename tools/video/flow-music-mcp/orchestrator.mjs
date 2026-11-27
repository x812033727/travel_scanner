/**
 * High-level orchestrator backing all 17 `mokaair-flow-music` MCP tools.
 *
 * Supports the full Google Flow Music (Lyria 3.5) production lifecycle:
 *   - Multi-profile Chrome CDP auth & clip listing (`music_status`, `music_profiles`, `music_list_remote`)
 *   - Collection init or import of existing Drive libraries (`music_init_collection`)
 *   - Mixing & copyright prompt preflight (`music_preflight_plan`)
 *   - Async track generation & batch download (`music_generate`, `music_download`, `music_wait`, `music_cancel`)
 *   - Local FFmpeg EBU R128 loudness measurement, silence slicing, and cutting (`music_measure`, `music_detect_slices`, `music_cut`)
 *   - Interactive HTML audition gallery & owner sign-off (`music_qa_gallery`, `music_approve`)
 *   - Pipeline export to `_sfx/<set>/` (v2 manifest + sfx-measure), `_music/` staging, and SHA-256 0-diff Drive sync
 */

import fs from "node:fs";
import path from "node:path";
import {
  cutAudioSlice,
  detectAudioSlices,
  measureAudioFile,
} from "./audio/ffmpeg-audio.mjs";
import {
  DEFAULT_DOWNLOAD_FORMAT,
  DEFAULT_MUSIC_MODEL,
  FLOW_MUSIC_ORIGIN,
  REPO_ROOT,
  getSeriesPreset,
  resolveChromeBinary,
  resolveRuntimeHome,
} from "./config.mjs";
import { ChromeCdpMusicDriver } from "./drivers/chrome-cdp-driver.mjs";
import {
  allocateTrackFilename,
  atomicWriteJson,
  buildCueName,
  preflightMusicPlan,
  readJsonSafe,
  resolveCollectionPaths,
  sanitizeCueBaseName,
  sha256File,
} from "./guards/music-guards.mjs";
import { JobQueue } from "./jobs/job-queue.mjs";
import {
  exportSfxV2Set,
  stageTrackForEpisode,
  syncCollectionToDrive,
} from "./pipeline/export-and-sync.mjs";
import { writeMusicQaGallery } from "./qa/audition-gallery.mjs";

const AUDIO_EXT_RE = /\.(?:m4a|mp3|wav|flac|ogg)$/i;

function inferKindFromFilename(filename) {
  const lower = String(filename || "").toLowerCase();
  if (lower.includes("-sfx-") || lower.startsWith("sfx-")) return "sfx";
  if (lower.includes("-cue-") || lower.startsWith("cue-")) return "cue";
  return "bed";
}

export class FlowMusicOrchestrator {
  constructor({
    driver = null,
    queue = null,
    repoRoot = REPO_ROOT,
    runtimeHome = null,
    measureFn = measureAudioFile,
    detectSlicesFn = detectAudioSlices,
    cutFn = cutAudioSlice,
    exportSfxFn = exportSfxV2Set,
    stageTrackFn = stageTrackForEpisode,
    syncDriveFn = syncCollectionToDrive,
  } = {}) {
    this.repoRoot = repoRoot;
    this.runtimeHome = runtimeHome || resolveRuntimeHome();
    this.driver = driver || new ChromeCdpMusicDriver({ runtimeHome: this.runtimeHome });
    this.queue = queue || new JobQueue({ runtimeHome: this.runtimeHome });
    this.measureFn = measureFn;
    this.detectSlicesFn = detectSlicesFn;
    this.cutFn = cutFn;
    this.exportSfxFn = exportSfxFn;
    this.stageTrackFn = stageTrackFn;
    this.syncDriveFn = syncDriveFn;
  }

  #paths(collection, workdir = null) {
    return resolveCollectionPaths(collection, { repoRoot: this.repoRoot, workdir });
  }

  #loadManifest(paths, { series = "curio" } = {}) {
    return (
      readJsonSafe(paths.manifestFile, null) || {
        collection: paths.collection,
        series,
        made: new Date().toISOString().slice(0, 10),
        tool: "Google Flow Music (Lyria 3.5)",
        ai_generated: true,
        account: null,
        files: [],
        cuts: [],
      }
    );
  }

  #saveManifest(paths, manifest) {
    manifest.updated_at = new Date().toISOString();
    atomicWriteJson(paths.manifestFile, manifest);
    return manifest;
  }

  #resolveEntryFilePath(paths, entry) {
    if (entry.filePath && fs.existsSync(entry.filePath)) return entry.filePath;
    const candidates = [
      path.join(paths.collectionDir, entry.file || ""),
      path.join(paths.rawDir, entry.file || ""),
      path.join(paths.cutsDir, entry.file || ""),
    ];
    for (const c of candidates) {
      if (entry.file && fs.existsSync(c)) return c;
    }
    return path.join(paths.collectionDir, entry.file || "");
  }

  // ---------------------------------------------------------------------------
  // Tool 1: music_status
  // ---------------------------------------------------------------------------
  async musicStatus({ profile = null, probeRemote = true } = {}) {
    const chromeBin = resolveChromeBinary();
    const lock = this.queue.inspectLock(profile);
    let auth = null;
    let error = null;

    if (probeRemote) {
      try {
        auth = await this.driver.checkAuth({ profile });
      } catch (err) {
        error = err?.toJSON ? err.toJSON() : { message: err.message };
      }
    }

    return {
      ok: Boolean(auth?.authenticated) && !error,
      driver: this.driver.name,
      origin: FLOW_MUSIC_ORIGIN,
      chromeBin,
      runtimeHome: this.runtimeHome,
      lock,
      auth,
      error,
      nextStep: auth?.authenticated
        ? "Flow Music session is ready. Run music_preflight_plan, music_list_remote, or music_init_collection."
        : "Run `npm run flow-music -- login` (or `--profile <name>`) to sign into www.flowmusic.app in isolated Chrome.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 2: music_profiles
  // ---------------------------------------------------------------------------
  async musicProfiles() {
    const raw = await this.driver.listProfiles();
    const profiles = raw.map((p) => ({
      ...p,
      lock: this.queue.inspectLock(p.profile),
    }));
    return {
      ok: true,
      count: profiles.length,
      profiles,
      tip: 'Run `npm run flow-music -- login --profile <name>` to add another Flow Music account without overwriting existing profiles.',
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 3: music_init_collection (creates or imports existing Drive folder)
  // ---------------------------------------------------------------------------
  async musicInitCollection({
    collection,
    series = "curio",
    workdir = null,
    importFromDir = null,
    copyImportedFiles = false,
  } = {}) {
    const preset = getSeriesPreset(series);
    const paths = this.#paths(collection, workdir);
    fs.mkdirSync(paths.collectionDir, { recursive: true });
    fs.mkdirSync(paths.cutsDir, { recursive: true });

    let manifest = this.#loadManifest(paths, { series: preset.id });
    manifest.series = preset.id;
    let importedCount = 0;

    if (importFromDir) {
      const srcDir = path.resolve(importFromDir);
      if (!fs.existsSync(srcDir)) {
        return { ok: false, reason: "import_dir_missing", message: `Import directory not found: ${srcDir}` };
      }
      const existingManifest = readJsonSafe(path.join(srcDir, "manifest.json"), null);
      if (existingManifest && Array.isArray(existingManifest.files)) {
        manifest.account = existingManifest.account || manifest.account;
        manifest.made = existingManifest.made || manifest.made;
        manifest.source_dir = srcDir;
        const existingNames = new Set((manifest.files || []).map((f) => f.file));
        for (const item of existingManifest.files) {
          if (!item?.file || existingNames.has(item.file)) continue;
          const srcFile = path.join(srcDir, item.file);
          let filePath = srcFile;
          if (copyImportedFiles && fs.existsSync(srcFile)) {
            const dst = path.join(paths.collectionDir, item.file);
            fs.copyFileSync(srcFile, dst);
            filePath = dst;
          }
          manifest.files.push({
            ...item,
            filePath,
            qa_status: item.qa_status || "pending",
          });
          existingNames.add(item.file);
          importedCount += 1;
        }
      } else {
        // Scan raw audio files in importFromDir
        const existingNames = new Set((manifest.files || []).map((f) => f.file));
        for (const name of fs.readdirSync(srcDir)) {
          if (!AUDIO_EXT_RE.test(name) || existingNames.has(name)) continue;
          const srcFile = path.join(srcDir, name);
          let filePath = srcFile;
          if (copyImportedFiles) {
            const dst = path.join(paths.collectionDir, name);
            fs.copyFileSync(srcFile, dst);
            filePath = dst;
          }
          manifest.files.push({
            file: name,
            filePath,
            kind: inferKindFromFilename(name),
            cue: sanitizeCueBaseName(name.replace(/-take\d+(?=\.[^.]+$)/i, "")),
            format: path.extname(name).slice(1).toLowerCase(),
            sha256: sha256File(filePath),
            qa_status: "pending",
          });
          existingNames.add(name);
          importedCount += 1;
        }
      }
    }

    this.#saveManifest(paths, manifest);
    return {
      ok: true,
      collection: paths.collection,
      series: preset.id,
      collectionDir: paths.collectionDir,
      manifestFile: paths.manifestFile,
      importedCount,
      totalTracks: manifest.files.length,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 4: music_preflight_plan
  // ---------------------------------------------------------------------------
  async musicPreflightPlan({
    collection = null,
    series = "curio",
    tracks = [],
    allowVocals = false,
    autoEnforceBedGuard = true,
    workdir = null,
  } = {}) {
    const result = preflightMusicPlan(tracks, { series, allowVocals, autoEnforceBedGuard });
    if (collection && result.ok) {
      const paths = this.#paths(collection, workdir);
      fs.mkdirSync(paths.collectionDir, { recursive: true });
      atomicWriteJson(paths.planFile, {
        collection: paths.collection,
        series: result.series,
        preflightedAt: new Date().toISOString(),
        tracks: result.normalizedTracks,
      });
      result.planFile = paths.planFile;
    }
    return result;
  }

  // ---------------------------------------------------------------------------
  // Tool 5: music_generate (async job queue -> Chrome CDP Lyria 3.5)
  // ---------------------------------------------------------------------------
  async musicGenerate({
    collection,
    series = "curio",
    tracks = null,
    format = DEFAULT_DOWNLOAD_FORMAT,
    model = DEFAULT_MUSIC_MODEL,
    profile = null,
    downloadImmediately = true,
    measureAfterDownload = true,
    allowVocals = false,
    waitMs = 15_000,
    workdir = null,
  } = {}) {
    const preset = getSeriesPreset(series);
    const paths = this.#paths(collection, workdir);
    fs.mkdirSync(paths.collectionDir, { recursive: true });

    let inputTracks = tracks;
    if (!inputTracks && fs.existsSync(paths.planFile)) {
      inputTracks = readJsonSafe(paths.planFile, {})?.tracks || [];
    }
    const preflight = preflightMusicPlan(inputTracks || [], { series: preset.id, allowVocals });
    if (!preflight.ok) {
      return {
        ok: false,
        reason: "preflight_blocked",
        blockers: preflight.blockers,
        warnings: preflight.warnings,
      };
    }

    const job = this.queue.enqueue({
      kind: "music_generate",
      collection: paths.collection,
      profile,
      items: preflight.normalizedTracks,
      worker: async (track, { signal }) => {
        const genRes = await this.driver.generateTrack({
          prompt: track.prompt,
          lyrics: track.lyrics || "",
          title: track.title,
          instrumental: track.instrumental,
          model,
          profile,
          signal,
        });

        const manifest = this.#loadManifest(paths, { series: preset.id });
        const savedEntries = [];
        for (const clip of genRes.clips || []) {
          let localFile = null;
          let metrics = null;
          let allocated = null;
          if (downloadImmediately && clip.id) {
            allocated = allocateTrackFilename({
              dir: paths.collectionDir,
              cue: track.cue,
              format,
            });
            localFile = path.join(paths.collectionDir, allocated.filename);
            await this.driver.downloadClip({
              clipId: clip.id,
              format: allocated.format,
              outFile: localFile,
              profile,
              signal,
            });
            if (measureAfterDownload) {
              metrics = await this.measureFn(localFile);
            }
          }
          const entry = {
            file: allocated?.filename || null,
            filePath: localFile,
            kind: track.kind,
            cue: track.cue,
            take: allocated?.take ?? 1,
            format: allocated?.format || format,
            sha256: metrics?.sha256 || (localFile && fs.existsSync(localFile) ? sha256File(localFile) : null),
            seconds: metrics?.seconds ?? clip.duration ?? null,
            lufs_i: metrics?.lufs_i ?? null,
            lufs_m: metrics?.lufs_m ?? null,
            peak_dbtp: metrics?.peak_dbtp ?? null,
            silences: metrics?.silences ?? null,
            flow_music_id: clip.id,
            title: clip.title || track.title,
            flow_music_seconds: clip.duration ?? null,
            created_at: clip.created_at || new Date().toISOString(),
            sound_prompt: clip.sound_prompt || track.prompt,
            conversation_id: clip.conversation_id || null,
            ai_generated: true,
            qa_status: "pending",
          };
          manifest.files.push(entry);
          savedEntries.push(entry);
        }
        this.#saveManifest(paths, manifest);
        return { cue: track.cue, generatedCount: savedEntries.length, entries: savedEntries };
      },
    });

    const waited = await this.queue.waitForJob(job.jobId, { timeoutMs: waitMs });
    return {
      ok: true,
      jobId: job.jobId,
      done: waited.done,
      job: waited.job,
      manifestFile: paths.manifestFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 6: music_list_remote
  // ---------------------------------------------------------------------------
  async musicListRemote({ profile = null, userId = null, limit = 100, filterTitle = null } = {}) {
    const res = await this.driver.listRemoteClips({ profile, userId, limit });
    let clips = res.clips || [];
    if (filterTitle) {
      const needle = String(filterTitle).toLowerCase();
      clips = clips.filter((c) => String(c.title || "").toLowerCase().includes(needle));
    }
    return {
      ok: true,
      profile: res.profile,
      userId: res.userId,
      count: clips.length,
      clips,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 7: music_download (async batch download with -takeN anti-collision)
  // ---------------------------------------------------------------------------
  async musicDownload({
    collection,
    series = "curio",
    clips = [],
    format = DEFAULT_DOWNLOAD_FORMAT,
    profile = null,
    measureAfterDownload = true,
    waitMs = 15_000,
    workdir = null,
  } = {}) {
    const preset = getSeriesPreset(series);
    const paths = this.#paths(collection, workdir);
    fs.mkdirSync(paths.collectionDir, { recursive: true });

    if (!Array.isArray(clips) || clips.length === 0) {
      return { ok: false, reason: "empty_clip_list", message: "Provide at least one clip { clipId, title?, kind?, cue? } to download." };
    }

    const job = this.queue.enqueue({
      kind: "music_download",
      collection: paths.collection,
      profile,
      items: clips,
      worker: async (item, { signal }) => {
        const clipId = item.clipId || item.id;
        if (!clipId) throw new Error("Each download item requires clipId.");
        const kind = item.kind || inferKindFromFilename(item.cue || item.title || "");
        const cue = item.cue || buildCueName({ series: preset.id, kind, name: item.title || clipId });
        const allocated = allocateTrackFilename({
          dir: paths.collectionDir,
          cue,
          format: item.format || format,
        });
        const outFile = path.join(paths.collectionDir, allocated.filename);
        const dl = await this.driver.downloadClip({
          clipId,
          format: allocated.format,
          outFile,
          profile,
          signal,
        });
        const metrics = measureAfterDownload ? await this.measureFn(outFile) : null;

        const manifest = this.#loadManifest(paths, { series: preset.id });
        const entry = {
          file: allocated.filename,
          filePath: outFile,
          kind,
          cue,
          take: allocated.take,
          format: allocated.format,
          sha256: metrics?.sha256 || dl.sha256,
          seconds: metrics?.seconds ?? item.duration ?? null,
          lufs_i: metrics?.lufs_i ?? null,
          lufs_m: metrics?.lufs_m ?? null,
          peak_dbtp: metrics?.peak_dbtp ?? null,
          silences: metrics?.silences ?? null,
          flow_music_id: clipId,
          title: item.title || cue,
          sound_prompt: item.sound_prompt || "",
          conversation_id: item.conversation_id || null,
          ai_generated: true,
          qa_status: "pending",
        };
        manifest.files.push(entry);
        this.#saveManifest(paths, manifest);
        return entry;
      },
    });

    const waited = await this.queue.waitForJob(job.jobId, { timeoutMs: waitMs });
    return {
      ok: true,
      jobId: job.jobId,
      done: waited.done,
      job: waited.job,
      manifestFile: paths.manifestFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 8: music_measure
  // ---------------------------------------------------------------------------
  async musicMeasure({ collection, series = "curio", files = null, workdir = null } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    const targetNames = files ? new Set(files) : null;

    const measured = [];
    const warnings = [];
    for (const entry of manifest.files || []) {
      if (targetNames && !targetNames.has(entry.file)) continue;
      const fp = this.#resolveEntryFilePath(paths, entry);
      if (!fs.existsSync(fp)) {
        warnings.push({ file: entry.file, reason: "file_missing", filePath: fp });
        continue;
      }
      const m = await this.measureFn(fp);
      entry.sha256 = m.sha256;
      entry.seconds = m.seconds;
      entry.lufs_i = m.lufs_i;
      entry.lufs_m = m.lufs_m;
      entry.peak_dbtp = m.peak_dbtp;
      entry.silences = m.silences;
      entry.near_silent = m.nearSilent;
      entry.clipping = m.clipping;
      measured.push({
        file: entry.file,
        kind: entry.kind,
        seconds: m.seconds,
        lufs_i: m.lufs_i,
        peak_dbtp: m.peak_dbtp,
        silences: m.silences,
        nearSilent: m.nearSilent,
        clipping: m.clipping,
      });
      if (m.nearSilent) {
        warnings.push({ file: entry.file, reason: "near_silent", lufs_i: m.lufs_i });
      }
      if (m.clipping) {
        warnings.push({ file: entry.file, reason: "clipping", peak_dbtp: m.peak_dbtp });
      }
    }

    this.#saveManifest(paths, manifest);
    return {
      ok: true,
      collection: paths.collection,
      measuredCount: measured.length,
      warnings,
      measured,
      manifestFile: paths.manifestFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 9: music_detect_slices
  // ---------------------------------------------------------------------------
  async musicDetectSlices({
    collection,
    series = "curio",
    files = null,
    kinds = ["cue", "sfx"],
    noiseDb = -40,
    minSilenceSec = 0.35,
    minSliceSec = 0.2,
    workdir = null,
  } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    const targetFiles = files ? new Set(files) : null;
    const targetKinds = new Set(kinds || ["cue", "sfx"]);

    const results = [];
    for (const entry of manifest.files || []) {
      if (targetFiles) {
        if (!targetFiles.has(entry.file)) continue;
      } else if (!targetKinds.has(entry.kind)) {
        continue;
      }
      const fp = this.#resolveEntryFilePath(paths, entry);
      if (!fs.existsSync(fp)) continue;
      const detected = await this.detectSlicesFn(fp, { noiseDb, minSilenceSec, minSliceSec });
      entry.slices = detected.slices;
      results.push(detected);
    }

    this.#saveManifest(paths, manifest);
    atomicWriteJson(paths.slicesFile, {
      collection: paths.collection,
      detectedAt: new Date().toISOString(),
      noiseDb,
      minSilenceSec,
      results,
    });

    return {
      ok: true,
      collection: paths.collection,
      analyzedCount: results.length,
      slicesFile: paths.slicesFile,
      results,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 10: music_cut
  // ---------------------------------------------------------------------------
  async musicCut({
    collection,
    series = "curio",
    cuts = [],
    format = DEFAULT_DOWNLOAD_FORMAT,
    workdir = null,
  } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    manifest.cuts = Array.isArray(manifest.cuts) ? manifest.cuts : [];
    fs.mkdirSync(paths.cutsDir, { recursive: true });

    const created = [];
    for (const spec of cuts || []) {
      const sourceEntry = (manifest.files || []).find((f) => f.file === spec.file || f.cue === spec.file);
      const inputPath = spec.inputPath || (sourceEntry ? this.#resolveEntryFilePath(paths, sourceEntry) : null);
      if (!inputPath || !fs.existsSync(inputPath)) {
        return {
          ok: false,
          reason: "cut_source_missing",
          message: `Source track "${spec.file || spec.inputPath}" not found in collection "${paths.collection}".`,
        };
      }
      const baseName = sanitizeCueBaseName(spec.outputName || `${(sourceEntry?.cue || path.basename(inputPath, path.extname(inputPath)))}-cut`);
      const ext = String(spec.format || format || "m4a").replace(/^\./, "").toLowerCase();
      const outFilename = baseName.endsWith(`.${ext}`) ? baseName : `${baseName}.${ext}`;
      const outputPath = path.join(paths.cutsDir, outFilename);

      const cutRes = await this.cutFn({
        inputPath,
        outputPath,
        startSec: spec.startSec,
        endSec: spec.endSec,
        fadeInSec: spec.fadeInSec ?? 0.01,
        fadeOutSec: spec.fadeOutSec ?? 0.08,
      });

      const cutRecord = {
        file: outFilename,
        filePath: outputPath,
        source_file: sourceEntry?.file || path.basename(inputPath),
        flow_music_id: sourceEntry?.flow_music_id || null,
        kind: spec.kind || sourceEntry?.kind || "cue",
        sound_name: spec.soundName || null,
        cut: cutRes.cut,
        sha256: cutRes.sha256,
        seconds: cutRes.seconds,
        lufs_i: cutRes.lufs_i,
        lufs_m: cutRes.lufs_m,
        peak_dbtp: cutRes.peak_dbtp,
        near_silent: cutRes.nearSilent,
        qa_status: "pending",
        created_at: new Date().toISOString(),
      };
      manifest.cuts = manifest.cuts.filter((c) => c.file !== outFilename);
      manifest.cuts.push(cutRecord);
      created.push(cutRecord);
    }

    this.#saveManifest(paths, manifest);
    return {
      ok: true,
      collection: paths.collection,
      createdCount: created.length,
      cutsDir: paths.cutsDir,
      cuts: created,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 11: music_qa_gallery
  // ---------------------------------------------------------------------------
  async musicQaGallery({ collection, series = "curio", includeCuts = true, workdir = null } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    const items = (manifest.files || []).map((f) => ({
      ...f,
      filePath: this.#resolveEntryFilePath(paths, f),
    }));
    if (includeCuts && Array.isArray(manifest.cuts)) {
      for (const c of manifest.cuts) {
        items.push({
          ...c,
          filePath: this.#resolveEntryFilePath(paths, c),
        });
      }
    }
    const galleryFile = writeMusicQaGallery({
      galleryFile: paths.galleryFile,
      collection: paths.collection,
      series: manifest.series || series,
      files: items,
    });
    return {
      ok: true,
      collection: paths.collection,
      trackCount: items.length,
      galleryFile,
      nextStep: "Double-click qa-gallery.html in your browser to audition tracks, mark approved/rejected + reasons, then paste the copied JSON into music_approve.",
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 12: music_approve
  // ---------------------------------------------------------------------------
  async musicApprove({
    collection,
    series = "curio",
    approved = [],
    rejected = [],
    reasons = {},
    workdir = null,
  } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    const approvedSet = new Set(approved || []);
    const rejectedSet = new Set(rejected || []);
    const now = new Date().toISOString();

    let updated = 0;
    const apply = (list) => {
      for (const item of list || []) {
        const key = item.file;
        if (approvedSet.has(key)) {
          item.qa_status = "approved";
          item.qa_reviewed_at = now;
          if (reasons?.[key]) item.qa_reason = reasons[key];
          updated += 1;
        } else if (rejectedSet.has(key)) {
          item.qa_status = "rejected";
          item.qa_reviewed_at = now;
          item.qa_reason = reasons?.[key] || item.qa_reason || "rejected";
          updated += 1;
        }
      }
    };
    apply(manifest.files);
    apply(manifest.cuts);
    this.#saveManifest(paths, manifest);

    const all = [...(manifest.files || []), ...(manifest.cuts || [])];
    return {
      ok: true,
      collection: paths.collection,
      updated,
      summary: {
        approved: all.filter((x) => x.qa_status === "approved").length,
        rejected: all.filter((x) => x.qa_status === "rejected").length,
        pending: all.filter((x) => !x.qa_status || x.qa_status === "pending").length,
      },
      manifestFile: paths.manifestFile,
    };
  }

  // ---------------------------------------------------------------------------
  // Tool 13: music_export_sfx_set
  // ---------------------------------------------------------------------------
  async musicExportSfxSet({
    collection,
    series = "curio",
    setName = null,
    soundMapping = {},
    workBase = null,
    account = null,
    runSfxMeasure = false,
    workdir = null,
  } = {}) {
    const preset = getSeriesPreset(series);
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series: preset.id });
    const allEntries = [...(manifest.cuts || []), ...(manifest.files || [])];

    const soundsMap = {};
    for (const [soundName, fileRef] of Object.entries(soundMapping || {})) {
      const found = allEntries.find((e) => e.file === fileRef || e.cue === fileRef || e.sound_name === fileRef);
      const filePath = found ? this.#resolveEntryFilePath(paths, found) : fileRef;
      soundsMap[soundName] = {
        filePath,
        seconds: found?.seconds,
        lufs_i: found?.lufs_i,
        lufs_m: found?.lufs_m,
        peak_dbtp: found?.peak_dbtp,
        flow_music_id: found?.flow_music_id,
      };
    }

    const acct = account || manifest.account || "owner";
    return this.exportSfxFn({
      setName: setName || preset.sfxSetName,
      soundsMap,
      ...(workBase ? { workBase } : {}),
      source: `Google Flow Music (Lyria 3.5)，帳號 ${acct}`,
      runSfxMeasure,
      repoRoot: this.repoRoot,
    });
  }

  // ---------------------------------------------------------------------------
  // Tool 14: music_stage_for_episode
  // ---------------------------------------------------------------------------
  async musicStageForEpisode({
    collection,
    series = "curio",
    file,
    targetFilename = null,
    workBase = null,
    allowUnapproved = false,
    allowOverwrite = false,
    workdir = null,
  } = {}) {
    const paths = this.#paths(collection, workdir);
    const manifest = this.#loadManifest(paths, { series });
    const allEntries = [...(manifest.cuts || []), ...(manifest.files || [])];
    const entry = allEntries.find((e) => e.file === file || e.cue === file);
    if (!entry) {
      return { ok: false, reason: "track_not_found", message: `Track "${file}" not found in collection "${paths.collection}".` };
    }
    if (!allowUnapproved && entry.qa_status !== "approved") {
      return {
        ok: false,
        reason: "track_not_approved",
        message: `Track "${entry.file}" has qa_status="${entry.qa_status || "pending"}". Audition and approve it via music_approve first (or pass allowUnapproved: true).`,
      };
    }

    const sourceFile = this.#resolveEntryFilePath(paths, entry);
    return this.stageTrackFn({
      sourceFile,
      targetFilename: targetFilename || entry.file,
      ...(workBase ? { workBase } : {}),
      allowOverwrite,
    });
  }

  // ---------------------------------------------------------------------------
  // Tool 15: music_push_drive
  // ---------------------------------------------------------------------------
  async musicPushDrive({
    collection,
    series = "curio",
    driveSubdir = null,
    driveRoot = null,
    dryRun = false,
    workdir = null,
  } = {}) {
    const paths = this.#paths(collection, workdir);
    return this.syncDriveFn({
      collectionDir: paths.collectionDir,
      series,
      driveSubdir,
      driveRoot,
      dryRun,
    });
  }

  // ---------------------------------------------------------------------------
  // Tool 16 & 17: music_wait / music_cancel
  // ---------------------------------------------------------------------------
  async musicWait({ job_id, timeoutMs = 25_000 } = {}) {
    return this.queue.waitForJob(job_id, { timeoutMs });
  }

  async musicCancel({ job_id } = {}) {
    return this.queue.cancelJob(job_id);
  }
}
