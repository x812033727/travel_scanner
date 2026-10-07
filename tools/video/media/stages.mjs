// What the media stages share (docs/videos/DRAMA.md): one generation (an image, a clip or a
// music track) with the cache, the resumable job list, the cost ledger, the per-video cap and
// the STOP file; a judge call that is booked like a generation; and the two best-effort extras,
// a contact sheet drawn by the slide renderer and the dHash of each picture through ffmpeg.
import { execFile } from "node:child_process";
import { writeFileSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";

import { locateFfmpeg } from "../assemble/ffmpeg.mjs";
import { keyframeKey } from "../core/drama.mjs";
import { stopRequested } from "../core/paths.mjs";
import { PROJECT_LEASED, ProjectLeaseError, requireProjectLease } from "../core/project-lease.mjs";
import { contactSheetHtml, SHEET_WIDTH } from "../render/contact.mjs";
import { cached, forgetJob, mediaKey, pendingJob, remember, rememberJob } from "./cache.mjs";
import { MediaError, RETAKE_CODES, TERMINAL, downloadFile, judge as askJudge, putFile, submitClip, submitImage, submitMusic, waitForJob } from "./client.mjs";
import { appendLedger, bookJob, capProblem, release, reserve } from "./ledger.mjs";
import { dHash, dhashArgs } from "./qc.mjs";

const exec = promisify(execFile);

export const IMAGE_SIZE = { width: 1920, height: 1080 };
// What a picture is asked at: the vendors' 1K default (which every cache key so far was written
// for), or 2K for a still that fills the frame under a camera move, where a 1K picture upscaled
// 1.25× reads as soft (docs/videos/ILLUSTRATED.md §畫面不像 AI). The server prices a 2K picture
// with the choice's `usd_per_image_2k`; a model without one draws at 1K.
export const IMAGE_SIZES = { "1K": IMAGE_SIZE, "2K": { width: 2048, height: 1152 } };
// Mirrors JUDGE_USD_PER_CALL in apps/api/app/video_media/catalog.py.
export const JUDGE_USD_PER_CALL = 0.01;
const EXTENSIONS = { "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "video/mp4": ".mp4", "audio/mpeg": ".mp3", "audio/mp4": ".m4a", "audio/wav": ".wav", "audio/x-wav": ".wav" };
const DEFAULT_EXTENSION = { image: ".png", clip: ".mp4", music: ".mp3" };
// A clip takes a vendor minutes; a job is given this long before the run gives up on it.
const WAIT_MS = { image: 10 * 60_000, clip: 30 * 60_000, music: 15 * 60_000 };

// Illustrated slides (docs/videos/ILLUSTRATED.md) may draw with their own switch, image model and
// per-video cap on the server (`slides_enabled`, `slides_image`, `slides_max_usd_per_video`, once
// the site has them); until then they draw as a drama does.
export const SLIDES_FORMAT = "slides";

/**
 * The server's choice of model for a kind, for a video of `format`: slides have their own image
 * choice while their switch is on. With the slides switch off the server draws a slides video
 * under the drama's switch and with the drama's model (jobs.py `slides_on`), so the tool sizes
 * and prices with that choice too, or the first picture comes back as `video_media_model_changed`.
 */
export function choiceFor(status, kind, format = null) {
  if (kind === "image" && format === SLIDES_FORMAT && status.slides_image && status.slides_enabled) return status.slides_image;
  return status[kind];
}

/** The catalog entry of the server's chosen model for a kind (image, clip, music). */
export function chosenModel(status, kind, format = null) {
  const choice = choiceFor(status, kind, format);
  const group = { image: "images", clip: "clips", music: "music" }[kind];
  return (status.models?.[group]?.[choice?.provider] ?? []).find((each) => each.value === choice?.model) ?? null;
}

/** Match the server's per-series image selection without changing clip/music choices. */
export function imageStatus(status, series) {
  const model = series?.image_model;
  if (!model) return status;
  const images = status.models?.images ?? {};
  // The server tries the configured image vendor first, then the catalog's vendor order.
  const providers = [status.image?.provider, ...Object.keys(images)].filter((value, index, all) => value && all.indexOf(value) === index);
  for (const provider of providers) {
    const entry = (images[provider] ?? []).find((each) => each.value === model && each.status !== "retired");
    if (!entry) continue;
    if (typeof entry.usd_per_image !== "number" || !Number.isFinite(entry.usd_per_image) || entry.usd_per_image <= 0) {
      throw new MediaError(`the series image model ${model} has no usable image price; refresh the site's media catalog before generating`, { code: "video_media_price_unavailable", who: "owner" });
    }
    // Status reports credentials only for its three selected vendors. A different vendor
    // can be unknown; let the server check it before submitting to the paid provider.
    const known = [status.image, status.clip, status.music].find((choice) => choice?.provider === provider && typeof choice.configured === "boolean");
    // The 2K price on the settings' choice belongs to the settings' model, and the catalog rows
    // carry none: an overridden model is drawn and priced at 1K rather than asked for a 2K
    // picture it may not sell (the server answers that with 422).
    const own2k = status.image && Object.hasOwn(status.image, "usd_per_image_2k") ? { usd_per_image_2k: null } : {};
    return { ...status, image: { ...status.image, provider, model, configured: known?.configured ?? null, ...own2k } };
  }
  throw new MediaError(`the series image model ${model} is unavailable or retired; change the series model or clear its override`, { code: "video_media_model_not_allowed", who: "owner" });
}

export const sameImage = (left, right) => left?.provider === right?.provider && left?.model === right?.model;

/**
 * Whether the server's image choice for `format` reads a style reference (a style plate, the
 * owner's style frames; role "style"): the catalog's `style_references` on the chosen model
 * (apps/api/app/video_media/catalog.py), and on a server from before it said, the vendor: only
 * the Gemini adapter forwards a style reference, the MiniMax one sends a character reference
 * alone. A model that takes none is not drawn a plate it would never see (keyframes.mjs); its
 * style is judged from the look's text.
 */
export function takesStyleReference(status, format = null) {
  const entry = chosenModel(status, "image", format);
  if (typeof entry?.style_references === "number") return entry.style_references > 0;
  return choiceFor(status, "image", format)?.provider === "gemini";
}

// Old story artifacts could be labeled with the settings model instead of the series model.
// Keep this boundary even after an override is cleared (the stored field is then null).
export const imageSelectionVersion = (series) => Object.hasOwn(series ?? {}, "image_model") ? 1 : 0;

/** The list price of one image with the server's chosen image model, at 1K or, when asked, at 2K. */
export function imagePrice(status, format = null, size = null) {
  if (size === "2K") return Number(choiceFor(status, "image", format)?.usd_per_image_2k ?? 0);
  return Number(chosenModel(status, "image", format)?.usd_per_image ?? 0);
}

/** "2K" when the server's image choice for `format` is priced at 2K, else null (draw at 1K). */
export function imageSizeFor(status, format = null) {
  const price = choiceFor(status, "image", format)?.usd_per_image_2k;
  return typeof price === "number" && Number.isFinite(price) && price > 0 ? "2K" : null;
}

/** The owner's per-video cap for a video of `format`: slides may have their own. */
export function capFor(status, format = null) {
  return format === SLIDES_FORMAT && status.slides_max_usd_per_video !== undefined && status.slides_max_usd_per_video !== null ? status.slides_max_usd_per_video : status.max_usd_per_video;
}

/** The list price of one second of clip with the server's chosen clip model. */
export function clipSecondPrice(status) {
  return Number(chosenModel(status, "clip")?.usd_per_second ?? 0);
}

/** The list price of one track with the server's chosen music model. */
export function trackPrice(status) {
  return Number(chosenModel(status, "music")?.usd_per_track ?? 0);
}

/** Why the server will not generate this kind now, or null. `format` is the video's: slides may draw under their own switch. */
export function statusProblem(status, kind = "image", format = null) {
  const slides = format === SLIDES_FORMAT;
  if (!status.enabled && !(slides && status.slides_enabled)) {
    return slides
      ? "pictures for slides videos are off: turn on the drama route or the slides illustrations in the settings tab of /admin/videos"
      : "the drama route is off: turn it on in the settings tab of /admin/videos";
  }
  if (kind === "music" && !status.music_enabled) return "music generation is off: turn it on in the settings tab of /admin/videos";
  const choice = choiceFor(status, kind, format);
  // A series' own image vendor may be unknown to status (configured null): the server checks it on submit.
  if (choice?.configured !== null && !choice?.configured) return `the site has no ${choice?.provider} key for ${kind} generation (admin: API 與供應商設定)`;
  return null;
}

/** Failed jobs a new seed might fix. */
export const retakeable = (error) => error instanceof MediaError && RETAKE_CODES.has(error.code);

export const stoppedError = () => new MediaError("stopped by the STOP file; rerun to continue", { code: "stopped" });

/**
 * Whether a media command may write the project's files at all: not under the project's STOP
 * file (false, said on stdout), and only while this process holds the project's lease
 * (core/project-lease.mjs; another producer's is the owner's to sort out, and nothing is written).
 * Each command calls it once, right before its first write, and exits incomplete (6) when it says
 * false, so a STOP removed before the worker reads the exit cannot pass for a stage done. Once a run is under way, a STOP that
 * arrives keeps what was already paid for and asks for nothing more (Stage.generate, judge).
 */
export function mayWriteProject(ctx, workdir, owner) {
  if (stopRequested(workdir)) {
    ctx.stdout.write("stopped by the STOP file before anything was drawn or written; remove it to continue\n");
    return false;
  }
  try {
    requireProjectLease(workdir, { owner, now: ctx.now });
  } catch (error) {
    if (error instanceof ProjectLeaseError) throw new MediaError(error.message, { code: PROJECT_LEASED, who: "owner" });
    throw error;
  }
  return true;
}

/** One stage's connection to the media server and the work directory's books. */
export class Stage {
  constructor({ slug, workdir, options, status, stage, imageVersion = 0, format = null, now = () => new Date() }) {
    this.slug = slug;
    this.workdir = workdir;
    this.options = options;
    this.status = status;
    this.stage = stage;
    this.imageVersion = imageVersion;
    this.format = format;
    this.now = now;
  }

  stop() {
    return stopRequested(this.workdir);
  }

  /**
   * The project's lease (core/project-lease.mjs), before anything is reserved, sent or booked:
   * the worker's unit holds it and a command it runs joins it; a command run by hand takes it for
   * the rest of its process. Another producer holding it (or possibly holding it) is the owner's
   * to sort out, and nothing is spent meanwhile.
   */
  hold() {
    try {
      requireProjectLease(this.workdir, { owner: this.stage, now: this.now });
    } catch (error) {
      if (error instanceof ProjectLeaseError) throw new MediaError(error.message, { code: PROJECT_LEASED, who: "owner" });
      throw error;
    }
  }

  /**
   * Refuse spending `usd` on `what` (a generation, a judge call, an import) when it would pass
   * the owner's per-video cap, counting what the ledger has charged and still holds reserved.
   */
  spend(usd, what = "generation") {
    const problem = capProblem(this.workdir, usd, capFor(this.status, this.format), what);
    if (problem) throw new MediaError(problem, { code: "video_media_cap", who: "owner" });
  }

  /**
   * One generation of any kind, or the file this exact request produced before. A job left
   * running by an earlier run is picked up by its id; the STOP file ends the wait with code
   * "stopped" and keeps the id. A failed job throws with the server's code, which `retakeable`
   * says a new seed may fix. Returns `{ file, sha256, key, cost_usd, job_id, reused }`.
   *
   * Money is held before it is spent: the list price goes into the ledger as a `reserved` row
   * under the request key before the submission, and `bookJob` replaces that row with the
   * server's charge once the job is seen. A refusal from the server releases the hold, since no
   * job exists; a run that dies or stops after submitting leaves it, beside the pending job id,
   * for the next run to reconcile.
   */
  async generate({ kind, key, submit, request, id, target, usd, seconds = 0 }) {
    const expected = choiceFor(this.status, kind, this.format);
    const hit = cached(this.workdir, key);
    if (hit) return { ...hit, key, reused: true };
    this.hold();
    let job;
    const pending = pendingJob(this.workdir, key);
    if (pending) {
      job = await waitForJob({ jobId: pending.job_id, stop: () => this.stop(), timeoutMs: WAIT_MS[kind], ...this.options });
    } else {
      if (this.stop()) throw stoppedError();
      this.spend(usd);
      reserve(this.workdir, { stage: this.stage, kind, id, provider: expected.provider, model: expected.model, key, seconds, cost_usd: usd }, this.now());
      let submitted;
      try {
        submitted = await submit({ request, ...this.options });
      } catch (error) {
        // The server answered and took nothing (a spent budget, an exhausted request, a bad
        // reference): nothing is held. A lost connection may have left a job behind, so its
        // hold stays until a rerun submits the same key again and books what it finds.
        if (error instanceof MediaError && error.status > 0) release(this.workdir, key);
        throw error;
      }
      if (TERMINAL.has(submitted.status)) job = submitted;
      else {
        rememberJob(this.workdir, key, { job_id: submitted.id, kind, target }, this.now());
        job = await waitForJob({ jobId: submitted.id, stop: () => this.stop(), timeoutMs: WAIT_MS[kind], ...this.options });
      }
    }
    const provider = job.provider ?? expected.provider;
    const model = job.model ?? expected.model;
    if (kind === "image" && !sameImage({ provider, model }, expected)) {
      // The series may have changed on the site since series.json was written. Preserve
      // the actual charge and job id, but never label/cache its result as the old model.
      rememberJob(this.workdir, key, { job_id: job.id, kind, target }, this.now());
      bookJob(this.workdir, { stage: this.stage, kind, id, provider, model, key, job_id: job.id, seconds, cost_usd: job.status === "failed" ? 0 : Number(job.usd_estimate || 0), status: "failed", error: "video_media_model_changed" }, this.now());
      throw new MediaError(`${id}: the server used ${provider}/${model}, expected ${expected.provider}/${expected.model}; reconcile the series model and saved job before continuing`, { code: "video_media_model_changed", who: "owner", job });
    }
    rememberJob(this.workdir, key, { job_id: job.id, kind, target }, this.now());
    if (job.status !== "ready" || !job.file?.sha256) {
      const code = job.error?.code || `video_media_job_${job.status}`;
      bookJob(this.workdir, { stage: this.stage, kind, id, provider, model, key, job_id: job.id, seconds, cost_usd: job.status === "failed" ? 0 : Number(job.usd_estimate || 0), status: "failed", error: code }, this.now());
      forgetJob(this.workdir, key, job.id);
      throw new MediaError(`${id}: ${job.error?.detail || code}`, { code, job });
    }
    bookJob(this.workdir, { stage: this.stage, kind, id, provider, model, key, job_id: job.id, seconds, cost_usd: Number(job.usd_estimate || 0), status: "ready" }, this.now());
    const file = `${target}${EXTENSIONS[job.file.content_type] ?? DEFAULT_EXTENSION[kind]}`;
    const got = await downloadFile({ slug: this.slug, sha256: job.file.sha256, file: path.join(this.workdir, file), ...this.options });
    const entry = remember(this.workdir, key, { file, sha256: got.sha256, bytes: got.bytes, job_id: job.id, provider, model, seconds, cost_usd: Number(job.usd_estimate || 0) }, this.now());
    forgetJob(this.workdir, key, job.id);
    return { ...entry, key, reused: false };
  }

  /** The cache key of one image request: what `image` would draw it under, without asking for it. */
  imageKey({ prompt, negative = "", references = [], seed = null, size = null }) {
    const { provider, model } = choiceFor(this.status, "image", this.format);
    const dimensions = IMAGE_SIZES[size ?? "1K"] ?? IMAGE_SIZE;
    const baseKey = keyframeKey({ provider, model, prompt, negative, width: dimensions.width, height: dimensions.height, seed, references: references.map((reference) => reference.sha256) });
    return this.imageVersion ? mediaKey("series-image", { version: this.imageVersion, key: baseKey }) : baseKey;
  }

  /** Generate one image: a character sheet, a keyframe, an end frame; `size` "2K" asks for a larger picture (IMAGE_SIZES). */
  async image({ id, purpose, prompt, negative = "", aspect = "16:9", references = [], seed = null, shotId = null, size = null, target }) {
    const key = this.imageKey({ prompt, negative, references, seed, size });
    const request = {
      slug: this.slug,
      purpose,
      prompt,
      ...(negative ? { negative_prompt: negative } : {}),
      aspect,
      references,
      ...(seed !== null ? { seed } : {}),
      ...(shotId ? { shot_id: shotId } : {}),
      ...(size ? { size } : {}),
    };
    return this.generate({ kind: "image", key, submit: submitImage, request, id, target, usd: imagePrice(this.status, this.format, size) });
  }

  /** Generate one clip from its first frame (`request` is the server's ClipJobIn without the slug). */
  async clip({ id, key, request, target }) {
    return this.generate({ kind: "clip", key, submit: submitClip, request: { slug: this.slug, ...request }, id, target, usd: clipSecondPrice(this.status) * request.seconds, seconds: request.seconds });
  }

  /** Generate one music track. */
  async music({ id, key, prompt, seconds, target }) {
    return this.generate({ kind: "music", key, submit: submitMusic, request: { slug: this.slug, prompt, seconds }, id, target, usd: trackPrice(this.status), seconds });
  }

  /**
   * Ask the judge about some files and book the call; returns `{ overall, passed, scores, problems, notes }`.
   * A call is money too (JUDGE_USD_PER_CALL): it passes the per-video cap first, and is booked
   * once it has answered.
   */
  async judge({ id, kind, files, rubric, context = {} }) {
    if (this.stop()) throw stoppedError();
    this.hold();
    this.spend(JUDGE_USD_PER_CALL, "judge call");
    const verdict = await askJudge({ request: { slug: this.slug, kind, files, rubric, context }, ...this.options });
    appendLedger(this.workdir, { stage: this.stage, kind: "judge", id, provider: "gemini", model: verdict.model ?? "", key: null, cost_usd: JUDGE_USD_PER_CALL, status: "judged" }, this.now());
    return { overall: verdict.overall, passed: Boolean(verdict.passed), scores: verdict.scores ?? {}, problems: verdict.problems ?? [], notes: verdict.notes ?? "" };
  }

  /** Put a local file in the media store (an owner's style frame, a chosen sheet, a proxy) and return its SHA-256. */
  async upload(file) {
    return (await putFile({ slug: this.slug, file, ...this.options })).sha256;
  }
}

/**
 * A contact sheet of pictures, drawn by the slide renderer; `{ file: null, note }` when no
 * browser can start, since the review page shows the pictures one by one anyway.
 */
export async function drawContactSheet(ctx, { workdir, channel, title, tiles, file }) {
  const open = ctx.openRenderer ?? (await import("../render/browser.mjs")).openRenderer;
  let renderer;
  try {
    renderer = await open({ root: ctx.root, workdir, channel });
  } catch (error) {
    return { file: null, note: `no contact sheet: ${String(error.message).split("\n")[0]}` };
  }
  try {
    writeFileSync(path.join(workdir, file), await renderer.sheet(contactSheetHtml(title, tiles), SHEET_WIDTH));
    return { file, note: null };
  } finally {
    await renderer.close();
  }
}

/**
 * The dHash of each picture (`[{ id, hash }]`) through ffmpeg, or null when ffmpeg is missing;
 * `ctx.hashImage(file)` replaces ffmpeg in tests.
 */
export async function pictureHashes(ctx, workdir, pictures) {
  if (ctx.hashImage) return Promise.all(pictures.map(async (picture) => ({ id: picture.id, hash: await ctx.hashImage(path.join(workdir, picture.file)) })));
  let tools;
  try {
    tools = await locateFfmpeg(ctx.env);
  } catch {
    return null;
  }
  const hashes = [];
  for (const picture of pictures) {
    const { stdout } = await exec(tools.ffmpeg, dhashArgs(path.join(workdir, picture.file)), { encoding: "buffer", maxBuffer: 1 << 20, windowsHide: true });
    hashes.push({ id: picture.id, hash: dHash(stdout) });
  }
  return hashes;
}
