// `import`: a long video finished by another tool goes to /admin/videos for the owner to review.
//
// review-push needs a docs/videos/<slug>/video.json project and the work directory the slides or
// drama pipeline leaves; a cut made elsewhere (PR #880's season, built by its own script) has
// neither, so it never reached the site. This takes a directory holding final.mp4 and meta.json,
// and optionally zh-TW.srt and a thumbnail, reports the video as a tutorial and submits its final
// cut: a 720p copy, the thumbnail, the captions, the titles, the chapters and what the cut
// measures against the pipeline's profile. Nothing the other tool measured is taken over. The
// Shorts twin is tools/video/shorts/import.mjs.
//
// meta.json: { slug, title | titles: [a, b], description, chapters?: [{ time, title }],
//              source_guide?, category?, note? }
// Chapters left out are read from the description's "00:00 title" lines.
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { ebur128Args, HEIGHT, LOUDNESS, LOUDNESS_TOLERANCE, parseEbur128, probeArgs, WIDTH } from "../assemble/plan.mjs";
import { sha256File } from "../core/approvals.mjs";
import { resolveWorkdir, UsageError } from "../core/paths.mjs";
import { VIDEO_CATEGORIES } from "../core/schema.mjs";
import { FPS, formatClock } from "../core/timeline.mjs";
import { previewArgs } from "../review/sync.mjs";
import { upload } from "../shorts/push.mjs";
import { siteClient } from "../shorts/site.mjs";

// The site's video slug (apps/api/app/video_reviews/storage.py) and article slug (schemas.py).
export const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
const CLOCK = /^(?:\d{1,2}:)?\d{1,2}:\d{2}$/;
// YouTube's limits: a title of 100 characters, a description of 5,000 bytes.
const TITLE_MAX = 100;
const DESCRIPTION_BYTES = 5000;
const NOTE_MAX = 200;
// The checklist key that marks a video on the site as one this command put there.
export const IMPORTED = "imported";
const THUMBNAILS = ["thumbnail.png", "thumbnail.jpg", "thumbnail.jpeg"];
const CAPTIONS = "zh-TW.srt";
const text = (value) => typeof value === "string" && value.trim().length > 0;

/** The chapters a description lists, one "00:00 title" per line; empty when it lists none. */
export function chaptersFrom(description) {
  const chapters = [];
  for (const line of String(description ?? "").split(/\r?\n/)) {
    const match = /^\s*((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.+?)\s*$/.exec(line);
    if (match) chapters.push({ time: match[1], title: match[2] });
  }
  return chapters;
}

/** meta.json as the import uses it, or a UsageError listing everything wrong with it. */
export function readMeta(meta) {
  const problems = [];
  if (!SLUG.test(meta?.slug ?? "")) problems.push("slug: lower-case letters, digits and hyphens, at most 80");
  const titles = Array.isArray(meta?.titles) ? meta.titles : text(meta?.title) ? [meta.title] : [];
  if (titles.length < 1 || titles.length > 2 || titles.some((title) => !text(title) || [...title].length > TITLE_MAX || /[<>]/.test(title))) {
    problems.push(`title, or titles [a, b]: 1–${TITLE_MAX} characters without angle brackets`);
  }
  if (!text(meta?.description)) problems.push("description required");
  else if (Buffer.byteLength(meta.description) > DESCRIPTION_BYTES) problems.push(`description is ${Buffer.byteLength(meta.description)} bytes, YouTube takes ${DESCRIPTION_BYTES}`);
  const chapters = meta?.chapters === undefined ? chaptersFrom(meta?.description) : meta.chapters;
  if (!Array.isArray(chapters) || chapters.some((chapter) => !CLOCK.test(chapter?.time ?? "") || !text(chapter?.title))) problems.push('chapters: [{ time: "00:00", title }]');
  if (meta?.source_guide !== undefined && !GUIDE_SLUG.test(meta.source_guide)) problems.push("source_guide must be an article slug");
  if (meta?.category !== undefined && !VIDEO_CATEGORIES.includes(meta.category)) problems.push(`category must be one of ${VIDEO_CATEGORIES.join(", ")}`);
  if (meta?.note !== undefined && (!text(meta.note) || [...meta.note].length > NOTE_MAX)) problems.push(`note: 1–${NOTE_MAX} characters`);
  if (problems.length) throw new UsageError(`meta.json cannot be imported:\n  ${problems.join("\n  ")}`);
  return { slug: meta.slug, titles: titles.map((title) => title.trim()), description: meta.description, chapters, source_guide: meta.source_guide ?? null, category: meta.category ?? null, note: meta.note ?? null };
}

const rate = (value) => {
  const [top, bottom] = String(value ?? "").split("/").map(Number);
  return bottom ? top / bottom : top;
};

/**
 * Where the cut differs from what the pipeline makes (tools/video/assemble/plan.mjs): picture,
 * frame rate, sound and loudness. Each is said, none refuses the import: the owner decides.
 * Returns { seconds, problems }, the length from the picture.
 */
export function measureProblems(probe, loudness) {
  const problems = [];
  const video = probe.streams?.find((stream) => stream.codec_type === "video");
  const audio = probe.streams?.find((stream) => stream.codec_type === "audio");
  if (!video) return { seconds: 0, problems: ["no video stream"] };
  const fps = rate(video.r_frame_rate);
  const seconds = Number(video.duration) || Number(video.nb_read_packets) / fps || 0;
  if (video.codec_name !== "h264") problems.push(`video is ${video.codec_name}, the pipeline makes H.264`);
  if (video.width !== WIDTH || video.height !== HEIGHT) problems.push(`picture is ${video.width}×${video.height}, the pipeline makes ${WIDTH}×${HEIGHT}`);
  if (Math.abs(fps - FPS) > 0.01) problems.push(`${Number(fps.toFixed(3))} fps, the pipeline makes ${FPS}`);
  if (video.pix_fmt && video.pix_fmt !== "yuv420p") problems.push(`pixel format ${video.pix_fmt}`);
  if (!audio) problems.push("no audio stream");
  else {
    if (audio.codec_name !== "aac") problems.push(`audio is ${audio.codec_name}, the pipeline makes AAC`);
    if (Number(audio.sample_rate) !== 48000) problems.push(`audio at ${audio.sample_rate} Hz, the pipeline makes 48000`);
    if (audio.channels !== 2) problems.push(`${audio.channels} audio channel(s), the pipeline makes stereo`);
    // An AAC stream ends on its own block of 1,024 samples, a little past the last frame.
    if (Math.abs(Number(audio.duration) - seconds) > 0.1) problems.push(`sound lasts ${Number(audio.duration).toFixed(2)} s, picture ${seconds.toFixed(2)} s`);
  }
  if (loudness) {
    if (Math.abs(loudness.integrated - LOUDNESS.integrated) > LOUDNESS_TOLERANCE) problems.push(`loudness ${loudness.integrated} LUFS, the pipeline makes ${LOUDNESS.integrated} ± ${LOUDNESS_TOLERANCE}`);
    if (loudness.truePeak !== null && loudness.truePeak > LOUDNESS.truePeak + 0.5) problems.push(`true peak ${loudness.truePeak} dBFS, above ${LOUDNESS.truePeak}`);
  }
  return { seconds, problems };
}

/**
 * What the site is told about the video: a tutorial waiting at its final cut. The first
 * checklist item marks it as imported, so a later import may update it and nothing else.
 */
export function projectBody(meta) {
  return {
    title: meta.titles[0],
    stage: "final video approved",
    checklist: [
      { key: IMPORTED, label: "別的工具做好的成片", done: true },
      { key: "final_video_approved", label: "成片核准", done: false },
    ],
    format: "slides",
    ...(meta.source_guide ? { source_guide: meta.source_guide } : {}),
    // Filed on /admin/videos under it; left out, the owner files it on the page.
    ...(meta.category ? { category: meta.category } : {}),
  };
}

/** The final review, without its files: bound to the cut, carrying what the page shows. */
export function finalReview({ meta, sha256, seconds, problems, captions }) {
  const checks = problems.length ? `有 ${problems.length} 項跟產線規格不同` : "規格檢查全部通過";
  return {
    gate: "final",
    content_sha256: sha256,
    summary: `成片 ${formatClock(Math.round(seconds))}，別的工具做好後匯入；${checks}；沒有自動品管報告`,
    payload: {
      duration_seconds: seconds,
      ...(meta.titles.length > 1 ? { titles: meta.titles } : {}),
      checks: { ok: problems.length === 0, problems },
      chapters: meta.chapters,
      metadata: { "zh-TW": { title: meta.titles[0], description: meta.description } },
      imported: { note: meta.note, captions },
    },
  };
}

/** The cut's streams and loudness, measured with ffprobe and ffmpeg. */
export async function measureCut(file, env = process.env) {
  const { ffmpeg, ffprobe } = await locateFfmpeg(env);
  const probe = JSON.parse((await runTool(ffprobe, probeArgs(file))).stdout);
  const loudness = parseEbur128((await runTool(ffmpeg, ebur128Args(file))).stderr);
  return { probe, loudness };
}

/** The 720p copy the review page plays, as review-push makes it. */
export async function encodePreview(source, target, env = process.env) {
  const { ffmpeg } = await locateFfmpeg(env);
  await runTool(ffmpeg, previewArgs("preview", source, target));
}

/**
 * Send one directory. Refuses a slug the site knows as a video it did not import, unless `force`.
 * Returns { slug, status, seconds, problems }: the final review's status on the site.
 */
export async function importLong({ from, workdir, env = process.env, home, force = false, client = null, measure = measureCut, encode = encodePreview, log = () => {} }) {
  const final = path.join(from, "final.mp4");
  const metaFile = path.join(from, "meta.json");
  for (const file of [final, metaFile]) if (!existsSync(file)) throw new UsageError(`${from} has no ${path.basename(file)}`);
  const meta = readMeta(JSON.parse(readFileSync(metaFile, "utf8")));
  const site = client ?? siteClient({ env, home });
  const known = await site.project(meta.slug);
  if (known?.reviews?.some((review) => review.payload?._final_renewal || (["publish", "languages", "dubs"].includes(review.gate) && ["approved", "pending"].includes(review.status)))) {
    throw new UsageError(`${meta.slug} has downstream reviews or an owner renewal: stage a final-renewal candidate instead of importing over retained approvals`);
  }
  if (known && !force && !(known.checklist ?? []).some((item) => item.key === IMPORTED)) {
    throw new UsageError(`${meta.slug} is already on the site and was not imported: pick another slug, or pass --force to replace what it says`);
  }

  const { probe, loudness } = await measure(final, env);
  const { seconds, problems } = measureProblems(probe, loudness);
  const sha256 = await sha256File(final);
  const preview = path.join(resolveWorkdir({ flag: workdir, env, slug: meta.slug, home }), "review", `preview-${sha256.slice(0, 16)}.mp4`);
  if (!existsSync(preview)) {
    mkdirSync(path.dirname(preview), { recursive: true });
    log(`${meta.slug}: encode the 720p review copy`);
    await encode(final, preview, env);
  }

  await site.report(meta.slug, projectBody(meta));
  const files = [await upload(site, meta.slug, preview, "preview")];
  const thumbnail = THUMBNAILS.map((name) => path.join(from, name)).find((file) => existsSync(file));
  if (thumbnail) files.push(await upload(site, meta.slug, thumbnail, "thumbnail"));
  const captions = existsSync(path.join(from, CAPTIONS));
  if (captions) files.push(await upload(site, meta.slug, path.join(from, CAPTIONS), "captions_zh-TW"));
  const review = await site.submit(meta.slug, { ...finalReview({ meta, sha256, seconds, problems, captions }), files });
  log(`${meta.slug}: final review ${review.status}${problems.length ? `; ${problems.length} difference(s) from the pipeline's profile` : ""}`);
  return { slug: meta.slug, status: review.status, seconds, problems };
}
