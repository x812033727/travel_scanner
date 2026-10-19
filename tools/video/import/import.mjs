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
//
// `--languages` sends the same directory's other languages afterwards, as the languages gate the
// worker would (docs/videos/LANGUAGES.md): description.<l>.txt (title, a blank line, the
// description), <l>.srt and dub.<l>.m4a|mp3|wav, for the parts the owner ticked on the panel.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { ebur128Args, HEIGHT, LOUDNESS, LOUDNESS_TOLERANCE, parseEbur128, probeArgs, WIDTH } from "../assemble/plan.mjs";
import { sha256File } from "../core/approvals.mjs";
import { resolveWorkdir, UsageError } from "../core/paths.mjs";
import { LOCALES, NARRATION_LOCALE, VIDEO_CATEGORIES } from "../core/schema.mjs";
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
      // Another tool made it, not the worker: the owner decides at every gate (owner, 2026-10-17;
      // docs/videos/HANDS-OFF.md), whatever the site's switches say.
      hand_pushed: true,
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
  // A languages batch this command sent and the owner has not approved belongs to the old cut and
  // retains nothing: the new cut goes in, and `--languages` sends a batch that supersedes it.
  const ownBatch = (review) => review.gate === "languages" && review.status === "pending" && review.payload?.imported === true && review.payload?.hand_pushed === true;
  if (known?.reviews?.some((review) => review.payload?._final_renewal || (!ownBatch(review) && ["publish", "languages", "dubs"].includes(review.gate) && ["approved", "pending"].includes(review.status)))) {
    throw new UsageError(`${meta.slug} has downstream reviews or an owner renewal: stage a final-renewal candidate instead of importing over retained approvals`);
  }
  if (known?.reviews?.some(ownBatch)) log(`${meta.slug}: its pending languages batch belongs to the old cut; send --languages again after this import`);
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

// The audio types the review store takes for a dub track, as review-push sends them (review/sync.mjs DUB_TYPES).
const DUB_TYPES = { m4a: "audio/mp4", mp3: "audio/mpeg", wav: "audio/wav" };
const PART_NAMES = { metadata: "標題說明", captions: "CC", dub: "配音" };
// A dub is laid over the cut it was timed to: a track longer or shorter than that belongs to another cut.
const DUB_TOLERANCE = 0.5;

/** The language files a directory holds: { <locale>: { metadata?, captions?, dub? } }, each { file, role, content_type }. */
export function languageFiles(from) {
  const found = {};
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    const parts = {};
    const description = path.join(from, `description.${locale}.txt`);
    if (existsSync(description)) parts.metadata = { file: description, role: `description_${locale}`, content_type: "text/plain" };
    const captions = path.join(from, `${locale}.srt`);
    if (existsSync(captions)) parts.captions = { file: captions, role: `captions_${locale}`, content_type: "application/x-subrip" };
    const format = Object.keys(DUB_TYPES).find((ext) => existsSync(path.join(from, `dub.${locale}.${ext}`)));
    if (format) parts.dub = { file: path.join(from, `dub.${locale}.${format}`), role: `dub_${locale}`, content_type: DUB_TYPES[format], format };
    if (Object.keys(parts).length) found[locale] = parts;
  }
  return found;
}

/** What is wrong with one language file, or null: a title and description as YouTube takes them, captions that are an SRT. */
export function languageFileProblem(part, bytes) {
  if (part === "dub") return null;
  const content = bytes.toString("utf8");
  if (part === "captions") return content.includes("-->") ? null : "no caption cues";
  const [title = "", ...rest] = content.split(/\r?\n/);
  const description = rest.join("\n").trim();
  if (!text(title) || [...title.trim()].length > TITLE_MAX || /[<>]/.test(title)) return `first line is the title: 1–${TITLE_MAX} characters without angle brackets`;
  if (!description) return "the description follows the title after a blank line";
  if (Buffer.byteLength(description) > DESCRIPTION_BYTES) return `description is ${Buffer.byteLength(description)} bytes, YouTube takes ${DESCRIPTION_BYTES}`;
  return null;
}

/** The batch's summary line: each language with what it carries, and what the owner does. */
export function languagesSummary(locales) {
  const said = Object.entries(locales).map(([locale, entry]) => `${locale} ${Object.entries(PART_NAMES).filter(([part]) => entry[part] === "ready").map(([, name]) => name).join("、")}`);
  const dubbed = Object.values(locales).some((entry) => entry.dub === "ready");
  return `語言：${said.join("；")}（匯入）。${dubbed ? "配音到 Studio「語言」上傳後按「已在 Studio 上傳配音」" : "沒有要你上傳的配音"}`;
}

/** The length of a dub track in seconds, read with ffprobe. */
export async function probeSeconds(file, env = process.env) {
  const { ffprobe } = await locateFfmpeg(env);
  const probe = JSON.parse((await runTool(ffprobe, probeArgs(file))).stdout);
  const audio = probe.streams?.find((stream) => stream.codec_type === "audio");
  return Number(audio?.duration ?? probe.format?.duration) || 0;
}

/**
 * Send a directory's other languages as one languages batch (`import --languages`), for a video
 * this command imported. The batch belongs to the site's newest final cut, which must be the
 * directory's final.mp4: a dub is timed to one cut. Only the parts the owner ticked go; a part
 * ticked and not in the directory stays "working" on the page. The batch is hand-pushed, so it
 * waits for the owner, who fetches the tracks from its card for Studio and approves.
 * Returns { slug, status, locales, unticked, missing }.
 */
export async function importLanguages({ from, workdir, env = process.env, home, client = null, probe = probeSeconds, log = () => {} }) {
  const final = path.join(from, "final.mp4");
  const metaFile = path.join(from, "meta.json");
  for (const file of [final, metaFile]) if (!existsSync(file)) throw new UsageError(`${from} has no ${path.basename(file)}`);
  const meta = readMeta(JSON.parse(readFileSync(metaFile, "utf8")));
  const site = client ?? siteClient({ env, home });
  const known = await site.project(meta.slug);
  if (!known || !(known.checklist ?? []).some((item) => item.key === IMPORTED)) throw new UsageError(`${meta.slug} was not imported by this command; import its cut first`);
  const current = (known.reviews ?? []).find((review) => review.gate === "final" && !review.subject);
  const sha256 = await sha256File(final);
  if (!current || current.content_sha256 !== sha256 || !["pending", "approved"].includes(current.status)) {
    throw new UsageError(`${meta.slug}: the site's newest final cut is not this directory's final.mp4${current ? ` (it is ${current.content_sha256.slice(0, 12)}…, ${current.status})` : ""}; import the cut first`);
  }
  const chosen = known.locales ?? {};
  const found = languageFiles(from);
  const unticked = [];
  const missing = [];
  const send = [];
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    for (const part of Object.keys(PART_NAMES)) {
      const file = found[locale]?.[part];
      if (!chosen[locale]?.[part]) {
        if (file) unticked.push(`${locale} ${part}`);
        continue;
      }
      if (!file) missing.push(`${locale} ${part}`);
      else send.push({ locale, part, ...file });
    }
  }
  if (!send.length) throw new UsageError(`${meta.slug}: nothing to send: ${missing.length ? `the owner ticked ${missing.join(", ")} and ${from} has none of them` : "the owner ticked no language part on the panel"}`);
  const problems = [];
  const seconds = Number(current.payload?.duration_seconds) || 0;
  for (const item of send) {
    const problem = item.part === "dub"
      ? await (async () => {
        const length = await probe(item.file, env);
        return seconds && Math.abs(length - seconds) > DUB_TOLERANCE ? `lasts ${length.toFixed(2)} s, the cut ${seconds.toFixed(2)} s` : null;
      })()
      : languageFileProblem(item.part, readFileSync(item.file));
    if (problem) problems.push(`${path.basename(item.file)}: ${problem}`);
  }
  if (problems.length) throw new UsageError(`${meta.slug}: language files cannot be sent:\n  ${problems.join("\n  ")}`);

  const files = [];
  const locales = {};
  for (const item of send) {
    const sent = { ...(await upload(site, meta.slug, item.file, item.role)), content_type: item.content_type };
    files.push(sent);
    const entry = (locales[item.locale] ??= {});
    entry[item.part] = "ready";
    if (item.part === "dub") Object.assign(entry, { file: path.basename(item.file), format: item.format, file_role: item.role, sha256: sent.sha256 });
  }
  const source = { final: { review_id: current.id, content_sha256: current.content_sha256 } };
  // The batch is bound to the bytes of what it names: the cut and every file sent.
  const manifest = path.join(resolveWorkdir({ flag: workdir, env, slug: meta.slug, home }), "review", `languages-import-${sha256.slice(0, 16)}.json`);
  mkdirSync(path.dirname(manifest), { recursive: true });
  writeFileSync(manifest, `${JSON.stringify({ source, locales, files: files.map(({ role, sha256: sha }) => ({ role, sha256: sha })) }, null, 2)}\n`);
  const review = await site.submit(meta.slug, {
    gate: "languages",
    content_sha256: await sha256File(manifest),
    summary: languagesSummary(locales),
    payload: { locales, source, imported: true, hand_pushed: true },
    files,
  });
  log(`${meta.slug}: languages batch ${review.status} (${Object.keys(locales).join(", ")})`);
  return { slug: meta.slug, status: review.status, locales, unticked, missing };
}
