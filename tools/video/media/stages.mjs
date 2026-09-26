// What the look and keyframes stages share (docs/videos/DRAMA.md): one image generation with the
// cache, the resumable job list, the cost ledger, the per-video cap and the STOP file; a judge
// call that is booked like a generation; and the two best-effort extras, a contact sheet drawn
// by the slide renderer and the dHash of each picture through ffmpeg.
import { execFile } from "node:child_process";
import { writeFileSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";

import { locateFfmpeg } from "../assemble/ffmpeg.mjs";
import { keyframeKey } from "../core/drama.mjs";
import { stopRequested } from "../core/paths.mjs";
import { contactSheetHtml, SHEET_WIDTH } from "../render/contact.mjs";
import { cached, forgetJob, pendingJob, remember, rememberJob } from "./cache.mjs";
import { MediaError, RETAKE_CODES, TERMINAL, downloadFile, judge as askJudge, putFile, runJob, submitImage, waitForJob } from "./client.mjs";
import { appendLedger, capProblem } from "./ledger.mjs";
import { dHash, dhashArgs } from "./qc.mjs";

const exec = promisify(execFile);

export const IMAGE_SIZE = { width: 1920, height: 1080 };
// Mirrors JUDGE_USD_PER_CALL in apps/api/app/video_media/catalog.py.
export const JUDGE_USD_PER_CALL = 0.01;
const EXTENSIONS = { "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp" };

/** The list price of one image with the server's chosen image model. */
export function imagePrice(status) {
  const { provider, model } = status.image;
  const option = (status.models?.images?.[provider] ?? []).find((each) => each.value === model);
  return Number(option?.usd_per_image ?? 0);
}

/** Why the server will not generate images now, or null. */
export function statusProblem(status) {
  if (!status.enabled) return "the drama route is off: turn it on in the settings tab of /admin/videos";
  if (!status.image?.configured) return `the site has no ${status.image?.provider} key for image generation (admin: API 與供應商設定)`;
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
   * Generate one image, or reuse the one this exact request produced before. Returns
   * `{ file (relative to the work directory), sha256, key, cost_usd, job_id, reused }`.
   * A job left running by an earlier run is picked up by its id; the STOP file ends the wait
   * with code "stopped" and keeps the id. A failed job throws with the server's code, which
   * `retakeable` says a new seed may fix.
   */
  async image({ id, purpose, prompt, negative = "", aspect = "16:9", references = [], seed = null, shotId = null, target }) {
    const { provider, model } = this.status.image;
    const key = keyframeKey({ provider, model, prompt, negative, width: IMAGE_SIZE.width, height: IMAGE_SIZE.height, seed, references: references.map((reference) => reference.sha256) });
    const hit = cached(this.workdir, key);
    if (hit) return { ...hit, key, reused: true };
    let job;
    const pending = pendingJob(this.workdir, key);
    if (pending) {
      job = await waitForJob({ jobId: pending.job_id, stop: () => this.stop(), ...this.options });
    } else {
      if (this.stop()) throw stoppedError();
      this.spend(imagePrice(this.status));
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
      const submitted = await submitImage({ request, ...this.options });
      if (TERMINAL.has(submitted.status)) job = submitted;
      else {
        rememberJob(this.workdir, key, { job_id: submitted.id, kind: "image", target }, this.now());
        job = await waitForJob({ jobId: submitted.id, stop: () => this.stop(), ...this.options });
      }
    }
    forgetJob(this.workdir, key);
    if (job.status !== "ready" || !job.file?.sha256) {
      const code = job.error?.code || `video_media_job_${job.status}`;
      appendLedger(this.workdir, { stage: this.stage, kind: "image", id, provider, model, key, job_id: job.id, cost_usd: job.status === "failed" ? 0 : Number(job.usd_estimate || 0), status: "failed", error: code }, this.now());
      throw new MediaError(`${id}: ${job.error?.detail || code}`, { code, job });
    }
    const file = `${target}${EXTENSIONS[job.file.content_type] ?? ".png"}`;
    const got = await downloadFile({ slug: this.slug, sha256: job.file.sha256, file: path.join(this.workdir, file), ...this.options });
    const entry = remember(this.workdir, key, { file, sha256: got.sha256, bytes: got.bytes, job_id: job.id, provider, model, cost_usd: Number(job.usd_estimate || 0) }, this.now());
    appendLedger(this.workdir, { stage: this.stage, kind: "image", id, provider, model, key, job_id: job.id, cost_usd: entry.cost_usd, status: "ready" }, this.now());
    return { ...entry, key, reused: false };
  }

  /** Ask the judge about some pictures and book the call; returns `{ overall, passed, scores, problems, notes }`. */
  async judge({ id, kind, files, rubric, context = {} }) {
    if (this.stop()) throw stoppedError();
    const verdict = await askJudge({ request: { slug: this.slug, kind, files, rubric, context }, ...this.options });
    appendLedger(this.workdir, { stage: this.stage, kind: "judge", id, provider: "gemini", model: verdict.model ?? "", key: null, cost_usd: JUDGE_USD_PER_CALL, status: "judged" }, this.now());
    return { overall: verdict.overall, passed: Boolean(verdict.passed), scores: verdict.scores ?? {}, problems: verdict.problems ?? [], notes: verdict.notes ?? "" };
  }

  /** Put a local picture in the media store (an owner's style frame, a chosen sheet) and return its SHA-256. */
  async upload(file) {
    return (await putFile({ slug: this.slug, file, ...this.options })).sha256;
  }
}

/** Keep `runJob` reachable for the clips stage, which submits differently. */
export { runJob };

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
