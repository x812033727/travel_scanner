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
import { contactSheetHtml, SHEET_WIDTH } from "../render/contact.mjs";
import { cached, forgetJob, pendingJob, remember, rememberJob } from "./cache.mjs";
import { MediaError, RETAKE_CODES, TERMINAL, downloadFile, judge as askJudge, putFile, submitClip, submitImage, submitMusic, waitForJob } from "./client.mjs";
import { appendLedger, capProblem } from "./ledger.mjs";
import { dHash, dhashArgs } from "./qc.mjs";

const exec = promisify(execFile);

export const IMAGE_SIZE = { width: 1920, height: 1080 };
// Mirrors JUDGE_USD_PER_CALL in apps/api/app/video_media/catalog.py.
export const JUDGE_USD_PER_CALL = 0.01;
const EXTENSIONS = { "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "video/mp4": ".mp4", "audio/mpeg": ".mp3", "audio/mp4": ".m4a", "audio/wav": ".wav", "audio/x-wav": ".wav" };
const DEFAULT_EXTENSION = { image: ".png", clip: ".mp4", music: ".mp3" };
// A clip takes a vendor minutes; a job is given this long before the run gives up on it.
const WAIT_MS = { image: 10 * 60_000, clip: 30 * 60_000, music: 15 * 60_000 };

/** The catalog entry of the server's chosen model for a kind (image, clip, music). */
export function chosenModel(status, kind) {
  const choice = status[kind];
  const group = { image: "images", clip: "clips", music: "music" }[kind];
  return (status.models?.[group]?.[choice?.provider] ?? []).find((each) => each.value === choice?.model) ?? null;
}

/** The list price of one image with the server's chosen image model. */
export function imagePrice(status) {
  return Number(chosenModel(status, "image")?.usd_per_image ?? 0);
}

/** The list price of one second of clip with the server's chosen clip model. */
export function clipSecondPrice(status) {
  return Number(chosenModel(status, "clip")?.usd_per_second ?? 0);
}

/** The list price of one track with the server's chosen music model. */
export function trackPrice(status) {
  return Number(chosenModel(status, "music")?.usd_per_track ?? 0);
}

/** Why the server will not generate this kind now, or null. */
export function statusProblem(status, kind = "image") {
  if (!status.enabled) return "the drama route is off: turn it on in the settings tab of /admin/videos";
  if (kind === "music" && !status.music_enabled) return "music generation is off: turn it on in the settings tab of /admin/videos";
  if (!status[kind]?.configured) return `the site has no ${status[kind]?.provider} key for ${kind} generation (admin: API 與供應商設定)`;
  return null;
}

/** Failed jobs a new seed might fix. */
export const retakeable = (error) => error instanceof MediaError && RETAKE_CODES.has(error.code);

export const stoppedError = () => new MediaError("stopped by the STOP file; rerun to continue", { code: "stopped" });

/** One stage's connection to the media server and the work directory's books. */
export class Stage {
  constructor({ slug, workdir, options, status, stage, now = () => new Date() }) {
    this.slug = slug;
    this.workdir = workdir;
    this.options = options;
    this.status = status;
    this.stage = stage;
    this.now = now;
  }

  stop() {
    return stopRequested(this.workdir);
  }

  /** Refuse a generation that would pass the owner's per-video cap. */
  spend(usd) {
    const problem = capProblem(this.workdir, usd, this.status.max_usd_per_video);
    if (problem) throw new MediaError(problem, { code: "video_media_cap", who: "owner" });
  }

  /**
   * One generation of any kind, or the file this exact request produced before. A job left
   * running by an earlier run is picked up by its id; the STOP file ends the wait with code
   * "stopped" and keeps the id. A failed job throws with the server's code, which `retakeable`
   * says a new seed may fix. Returns `{ file, sha256, key, cost_usd, job_id, reused }`.
   */
  async generate({ kind, key, submit, request, id, target, usd, seconds = 0 }) {
    const { provider, model } = this.status[kind];
    const hit = cached(this.workdir, key);
    if (hit) return { ...hit, key, reused: true };
    let job;
    const pending = pendingJob(this.workdir, key);
    if (pending) {
      job = await waitForJob({ jobId: pending.job_id, stop: () => this.stop(), timeoutMs: WAIT_MS[kind], ...this.options });
    } else {
      if (this.stop()) throw stoppedError();
      this.spend(usd);
      const submitted = await submit({ request, ...this.options });
      if (TERMINAL.has(submitted.status)) job = submitted;
      else {
        rememberJob(this.workdir, key, { job_id: submitted.id, kind, target }, this.now());
        job = await waitForJob({ jobId: submitted.id, stop: () => this.stop(), timeoutMs: WAIT_MS[kind], ...this.options });
      }
    }
    forgetJob(this.workdir, key);
    if (job.status !== "ready" || !job.file?.sha256) {
      const code = job.error?.code || `video_media_job_${job.status}`;
      appendLedger(this.workdir, { stage: this.stage, kind, id, provider, model, key, job_id: job.id, seconds, cost_usd: job.status === "failed" ? 0 : Number(job.usd_estimate || 0), status: "failed", error: code }, this.now());
      throw new MediaError(`${id}: ${job.error?.detail || code}`, { code, job });
    }
    const file = `${target}${EXTENSIONS[job.file.content_type] ?? DEFAULT_EXTENSION[kind]}`;
    const got = await downloadFile({ slug: this.slug, sha256: job.file.sha256, file: path.join(this.workdir, file), ...this.options });
    const entry = remember(this.workdir, key, { file, sha256: got.sha256, bytes: got.bytes, job_id: job.id, provider, model, seconds, cost_usd: Number(job.usd_estimate || 0) }, this.now());
    appendLedger(this.workdir, { stage: this.stage, kind, id, provider, model, key, job_id: job.id, seconds, cost_usd: entry.cost_usd, status: "ready" }, this.now());
    return { ...entry, key, reused: false };
  }

  /** Generate one image: a character sheet, a keyframe, an end frame. */
  async image({ id, purpose, prompt, negative = "", aspect = "16:9", references = [], seed = null, shotId = null, target }) {
    const { provider, model } = this.status.image;
    const key = keyframeKey({ provider, model, prompt, negative, width: IMAGE_SIZE.width, height: IMAGE_SIZE.height, seed, references: references.map((reference) => reference.sha256) });
    const request = {
      slug: this.slug,
      purpose,
      prompt,
      ...(negative ? { negative_prompt: negative } : {}),
      aspect,
      references,
      ...(seed !== null ? { seed } : {}),
      ...(shotId ? { shot_id: shotId } : {}),
    };
    return this.generate({ kind: "image", key, submit: submitImage, request, id, target, usd: imagePrice(this.status) });
  }

  /** Generate one clip from its first frame (`request` is the server's ClipJobIn without the slug). */
  async clip({ id, key, request, target }) {
    return this.generate({ kind: "clip", key, submit: submitClip, request: { slug: this.slug, ...request }, id, target, usd: clipSecondPrice(this.status) * request.seconds, seconds: request.seconds });
  }

  /** Generate one music track. */
  async music({ id, key, prompt, seconds, target }) {
    return this.generate({ kind: "music", key, submit: submitMusic, request: { slug: this.slug, prompt, seconds }, id, target, usd: trackPrice(this.status), seconds });
  }

  /** Ask the judge about some files and book the call; returns `{ overall, passed, scores, problems, notes }`. */
  async judge({ id, kind, files, rubric, context = {} }) {
    if (this.stop()) throw stoppedError();
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
