// Build an unreviewed local preview from real TTS, keyframes, cards and music, with
// visibly labelled concept bookends. This never counts as installed channel branding
// or writes clips/assemble manifests, approvals, checks.json or final.mp4.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { sha256File } from "../../../tools/video/core/approvals.mjs";
import { audioEvidenceProblems } from "../../../tools/video/core/audio-evidence.mjs";
import { buildCues, checkCues, toSrt, toVtt } from "../../../tools/video/core/captions.mjs";
import { drawnShotScenes, lookHash, mixHash, resolveMusic } from "../../../tools/video/core/drama.mjs";
import { isInside, resolveWorkdir, ROOT } from "../../../tools/video/core/paths.mjs";
import { ARTIFACTS, keyframeProblems, lintProject, loadProject } from "../../../tools/video/core/state.mjs";
import { frameToMs, speechHash, visualHash } from "../../../tools/video/core/timeline.mjs";
import { resolveWatermark } from "../../../tools/video/core/watermark.mjs";
import { lastFrameArgs, layoutDrama, measureMixArgs, mixArgs, motionSegmentArgs, motionSegmentKey } from "../../../tools/video/assemble/drama.mjs";
import { locateFfmpeg, runTool } from "../../../tools/video/assemble/ffmpeg.mjs";
import { checkProbe, concatList, joinArgs, muxArgs, parseLoudnorm, probeArgs, segmentArgs, segmentKey } from "../../../tools/video/assemble/plan.mjs";
import { themeHash } from "../../../tools/video/render/plan.mjs";
import { INTRO_FRAMES, OUTRO_FRAMES, assertConceptBookendFont, conceptBookendArgs, bookendedAudioArgs } from "./local-preview-bookends.mjs";

const SLUG = "story-everyday-netflix-x03";
const usage = "Usage: node docs/videos/story-everyday-netflix-x03/local-preview.mjs --workdir <media-base-outside-repo> [--dry-run] [--force] [--allow-review-needed]";
const fileAt = (workdir, name) => {
  const file = path.resolve(workdir, name);
  if (!isInside(file, workdir)) throw new Error(`media path escapes the work directory: ${name}`);
  return file;
};
const ffconcatFile = (file) => `file '${file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`;
const readBoundJson = (file) => {
  if (!existsSync(file)) return { value: null, sha256: null };
  const bytes = readFileSync(file);
  return { value: JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, "")), sha256: createHash("sha256").update(bytes).digest("hex") };
};

const reviewNeededShot = (shot) => Boolean(shot?.needs_review || (shot?.judge?.passed === false && !Array.isArray(shot?.accepted_with_problems)));

/** A local concept may show a complete rejected still, but never waive its file/hash evidence. */
export async function assessPreviewKeyframes({ doc, manifest, workdir, allowReviewNeeded = false }) {
  const reviewNeeded = drawnShotScenes(doc).flatMap((scene) => {
    const shot = manifest.shots?.[scene.id];
    if (!reviewNeededShot(shot)) return [];
    return [{
      id: scene.id,
      needs_review: Boolean(shot.needs_review),
      file: shot.file ?? null,
      sha256: shot.sha256 ?? null,
      judge_overall: shot.judge?.overall ?? null,
      judge_passed: shot.judge?.passed ?? null,
      problems: [...new Set([...(Array.isArray(shot.problems) ? shot.problems : []), ...(Array.isArray(shot.judge?.problems) ? shot.judge.problems : [])])],
      takes_count: shot.takes?.length ?? 0,
    }];
  });
  const issues = await keyframeProblems({ doc, manifest, workdir, allowNeedsReview: allowReviewNeeded });
  // layoutDrama rejects needs_review. Only the local layout receives these shallow copies;
  // keyframes/manifest.json and its review verdict remain exactly as generated.
  const layoutKeyframes = allowReviewNeeded && reviewNeeded.length && !issues.length
    ? { ...manifest, shots: { ...manifest.shots, ...Object.fromEntries(reviewNeeded.map(({ id }) => [id, { ...manifest.shots[id], needs_review: false }])) } }
    : manifest;
  return { issues, reviewNeeded, layoutKeyframes };
}

export const previewStem = (allowReviewNeeded, reviewNeeded) => allowReviewNeeded && reviewNeeded.length ? "preview-review-needed" : "preview";

export function reviewSidecar({ doc, stem, scriptSha, timelineSha, manifestSha, framesSha, musicSha, cardFiles, reviewNeeded, outputSha, srtSha, vttSha }) {
  if (!["preview", "preview-review-needed"].includes(stem)) throw new Error(`invalid local preview stem: ${stem}`);
  return {
    kind: "unapproved-local-concept-preview",
    approved: false,
    official_branding: false,
    slug: SLUG,
    video_json_sha256: scriptSha,
    timeline_sha256: timelineSha,
    keyframes_manifest_sha256: manifestSha,
    frames_manifest_sha256: framesSha,
    music_manifest_sha256: musicSha,
    rendered_card_files: cardFiles,
    look_hash: lookHash(doc),
    visual_hash: visualHash(doc),
    review_needed: reviewNeeded,
    outputs: {
      mp4: { file: `${stem}.mp4`, sha256: outputSha },
      srt: { file: `${stem}.zh-TW.srt`, sha256: srtSha },
      vtt: { file: `${stem}.zh-TW.vtt`, sha256: vttSha },
    },
  };
}

/** The spoken body and condensed first chapter are separate requirements from bookends. */
export function previewDurationProblems(timeline) {
  if (!timeline) return [];
  const issues = [];
  if (timeline.fps !== 30) issues.push("preview requires a measured 30 fps timeline");
  if (!Number.isSafeInteger(timeline.total_frames) || timeline.total_frames < 8 * 60 * 30) {
    issues.push("spoken body must be at least eight minutes before concept bookends");
  }
  const hookFrames = timeline.chapters?.[1]?.start_frame;
  if (!Number.isSafeInteger(hookFrames) || hookFrames < 30 * 30 || hookFrames > 60 * 30) {
    issues.push("the condensed first chapter must last 30–60 seconds before the concept intro");
  }
  return issues;
}

/** Bind each rendered card's path and actual bytes, independent of manifest order or repeated uses. */
export async function renderedCardEvidence(frames, workdir) {
  const names = [];
  const issues = [];
  for (const scene of frames.scenes ?? []) for (const state of scene.states ?? []) {
    for (const name of [state.still, ...(state.transition ?? [])]) {
      if (typeof name !== "string" || !name) issues.push("rendered card frame is missing: (unnamed)");
      else names.push(name);
    }
  }
  const files = [];
  for (const name of [...new Set(names)].sort()) {
    const file = fileAt(workdir, name);
    if (!existsSync(file) || !statSync(file).isFile()) issues.push(`rendered card frame is missing: ${name}`);
    else files.push({ file: name, sha256: await sha256File(file) });
  }
  return { files, issues };
}

/** All media inputs that may change during a long local encode must match at publication. */
export function previewSourcesChanged(before, after) {
  return ["scriptSha", "timelineSha", "manifestSha", "framesSha", "musicSha"].some((key) => before[key] !== after[key])
    || JSON.stringify(before.cardFiles) !== JSON.stringify(after.cardFiles)
    || JSON.stringify(before.reviewNeeded) !== JSON.stringify(after.reviewNeeded);
}

/** Place captions from the line's exact timeline frame, avoiding rounded-ms boundary drift. */
export function shiftPreviewCues(cues, timeline, introAtFrame) {
  if (!Number.isSafeInteger(introAtFrame) || introAtFrame <= 0) throw new Error("concept intro needs a positive chapter boundary");
  const starts = new Map(timeline.lines.map((line) => [line.id, line.start_frame]));
  const offset = frameToMs(INTRO_FRAMES);
  return cues.map((cue) => {
    const startFrame = starts.get(cue.line);
    if (!Number.isSafeInteger(startFrame)) throw new Error(`preview caption has no timeline line: ${cue.line}`);
    const by = startFrame >= introAtFrame ? offset : 0;
    return { ...cue, start_ms: Math.round(cue.start_ms + by), end_ms: Math.round(cue.end_ms + by) };
  });
}

/** The MP4 is the completion marker: publish it only after captions and review evidence. */
export function publishPreviewFiles({ partial, output, srtPartial, srt, vttPartial, vtt, sidecarPartial = null, sidecar = null, force = false }) {
  if (Boolean(sidecarPartial) !== Boolean(sidecar)) throw new Error("preview review evidence needs both a partial and final path");
  if (existsSync(output)) {
    if (!force) throw new Error(`${output} already exists; pass --force to replace this local preview`);
    // A forced replacement must not leave an old MP4 paired with new review evidence
    // if the process stops between the following renames.
    rmSync(output);
  }
  renameSync(srtPartial, srt);
  renameSync(vttPartial, vtt);
  if (sidecar) renameSync(sidecarPartial, sidecar);
  renameSync(partial, output);
}

async function inspect(workdir, { allowReviewNeeded = false } = {}) {
  const project = loadProject({ slug: SLUG, root: ROOT });
  const { doc, lexicon } = project;
  const scriptSha = await sha256File(path.join(ROOT, "docs", "videos", SLUG, "video.json"));
  const issues = lintProject(project).errors.map(({ path: where, message }) => `${where}: ${message}`);
  const notStill = doc.scenes.filter((scene) => scene.template === "shot" && scene.data?.visual !== "still");
  if (notStill.length) issues.push(`preview only supports still shots: ${notStill.map((scene) => scene.id).join(", ")}`);

  const { value: timeline, sha256: timelineSha } = readBoundJson(fileAt(workdir, ARTIFACTS.timeline));
  if (!timeline) issues.push("timeline.json is missing; run TTS first");
  else {
    issues.push(...previewDurationProblems(timeline));
    if (timeline.speech_hash !== speechHash(doc, lexicon)) issues.push("timeline.json belongs to an older script or voice");
    else issues.push(...audioEvidenceProblems(timeline, workdir));
  }

  const { value: keyframes, sha256: manifestSha } = readBoundJson(fileAt(workdir, ARTIFACTS.keyframes));
  let reviewNeeded = [];
  let layoutKeyframes = keyframes;
  if (!keyframes) issues.push("keyframes/manifest.json is missing; generate the full keyframe batch first");
  else if (keyframes.look_hash !== lookHash(doc) || keyframes.visual_hash !== visualHash(doc)) issues.push("keyframes/manifest.json belongs to an older script or look");
  else {
    const assessed = await assessPreviewKeyframes({ doc, manifest: keyframes, workdir, allowReviewNeeded });
    issues.push(...assessed.issues);
    reviewNeeded = assessed.reviewNeeded;
    layoutKeyframes = assessed.layoutKeyframes;
  }

  const { value: frames, sha256: framesSha } = readBoundJson(fileAt(workdir, ARTIFACTS.frames));
  let cardFiles = [];
  if (!frames) issues.push("frames/manifest.json is missing; run render after keyframes");
  else if (frames.visual_hash !== visualHash(doc) || frames.theme_hash !== themeHash()) issues.push("frames/manifest.json belongs to an older script or render theme");
  else {
    const cards = await renderedCardEvidence(frames, workdir);
    cardFiles = cards.files;
    issues.push(...cards.issues);
  }

  const { value: music, sha256: musicSha } = readBoundJson(fileAt(workdir, ARTIFACTS.music));
  let musicFile = null;
  if (!music || music.mix_hash !== mixHash(doc) || !music.file || !music.sha256) issues.push("music/manifest.json is missing or stale; run music first");
  else {
    musicFile = fileAt(workdir, music.file);
    if (!existsSync(musicFile) || await sha256File(musicFile) !== music.sha256) issues.push(`music track is missing or changed: ${music.file}`);
  }

  let layout = null;
  if (timeline && keyframes && frames && !issues.length) {
    try { layout = layoutDrama(doc, timeline, frames, null, layoutKeyframes); }
    catch (error) { issues.push(error.message); }
  }
  if (timeline && layout && !layout.some((scene) => scene.start_frame === timeline.chapters?.[1]?.start_frame)) {
    issues.push("the first chapter has no exact scene boundary for the concept intro");
  }
  return { doc, timeline, frames, musicFile, layout, issues, scriptSha, timelineSha, manifestSha, framesSha, musicSha, cardFiles, reviewNeeded };
}

async function encode({ doc, timeline, frames, musicFile, layout, workdir, previewDir, force, allowReviewNeeded, scriptSha, timelineSha, manifestSha, framesSha, musicSha, cardFiles, reviewNeeded }) {
  const stem = previewStem(allowReviewNeeded, reviewNeeded);
  const output = path.join(previewDir, `${stem}.mp4`);
  if (existsSync(output) && !force) throw new Error(`${output} already exists; pass --force to replace this local preview`);
  assertConceptBookendFont();
  const { ffmpeg, ffprobe } = await locateFfmpeg();
  const segmentsDir = path.join(previewDir, "segments");
  mkdirSync(segmentsDir, { recursive: true });
  const mark = resolveWatermark(frames.watermark);
  const segments = [];
  const keys = [];
  for (const [index, scene] of layout.entries()) {
    const previousKey = scene.transition === "dissolve" && index > 0 ? keys[index - 1] : null;
    const key = scene.kind === "motion"
      ? motionSegmentKey(scene, scene.move, null, previousKey, mark)
      : segmentKey(scene);
    keys.push(key);
    segments.push(path.join(segmentsDir, `${scene.id}-${key}.mp4`));
  }

  const completed = Array(layout.length);
  let nextScene = 0;
  const encodeScene = async (index) => {
    const scene = layout[index];
    const key = keys[index];
    const segment = segments[index];
    const previousKey = scene.transition === "dissolve" && index > 0 ? keys[index - 1] : null;
    // A dissolve reads the previous segment's last frame; cuts are independent.
    if (previousKey) await completed[index - 1];
    if (existsSync(segment)) return;
    const partial = `${segment}.partial.mp4`;
    if (scene.kind === "motion") {
      const picture = fileAt(workdir, scene.keyframe.file);
      let dissolveFrom = null;
      if (previousKey) {
        const previous = layout[index - 1];
        dissolveFrom = path.join(segmentsDir, `last-${previous.id}-${previousKey}.png`);
        if (!existsSync(dissolveFrom)) await runTool(ffmpeg, lastFrameArgs(segments[index - 1], previous.frames, dissolveFrom));
      }
      await runTool(ffmpeg, motionSegmentArgs({ keyframe: picture, frames: scene.frames, move: scene.move, dissolveFrom, mark, outFile: partial }));
    } else if (scene.kind === "stills") {
      const list = path.join(segmentsDir, `${scene.id}-${key}.ffconcat`);
      writeFileSync(list, concatList(scene.entries, (name) => fileAt(workdir, name)));
      await runTool(ffmpeg, segmentArgs(list, partial, scene.frames));
    } else throw new Error(`unsupported scene kind: ${scene.kind}`);
    renameSync(partial, segment);
    process.stdout.write(`encoded ${index + 1}/${layout.length}: ${scene.id}\n`);
  };
  const encodeWorker = async () => {
    while (nextScene < layout.length) {
      const index = nextScene++;
      completed[index] = encodeScene(index);
      await completed[index];
    }
  };
  const workers = await Promise.allSettled(Array.from({ length: Math.min(2, layout.length) }, () => encodeWorker()));
  const failed = workers.find((worker) => worker.status === "rejected");
  if (failed) throw failed.reason;

  const joinedList = path.join(previewDir, "segments.ffconcat");
  writeFileSync(joinedList, `ffconcat version 1.0\n${segments.map(ffconcatFile).join("\n")}\n`);
  await runTool(ffmpeg, joinArgs(joinedList, path.join(previewDir, "body.mp4")));

  const introAtFrame = timeline.chapters[1].start_frame;
  const insertAt = layout.findIndex((scene) => scene.start_frame === introAtFrame);
  if (insertAt < 1) throw new Error("the concept intro needs an opening chapter followed by a scene boundary");
  const intro = path.join(previewDir, "concept-intro.mp4");
  const outro = path.join(previewDir, "concept-outro.mp4");
  await runTool(ffmpeg, conceptBookendArgs("intro", intro));
  await runTool(ffmpeg, conceptBookendArgs("outro", outro));
  const playback = [...segments.slice(0, insertAt), intro, ...segments.slice(insertAt), outro];
  const playbackList = path.join(previewDir, "playback.ffconcat");
  writeFileSync(playbackList, `ffconcat version 1.0\n${playback.map(ffconcatFile).join("\n")}\n`);
  const video = path.join(previewDir, "playback.mp4");
  await runTool(ffmpeg, joinArgs(playbackList, video));

  const audio = path.join(previewDir, "audio.m4a");
  const narration = fileAt(workdir, ARTIFACTS.narration);
  const seconds = timeline.total_frames / 30;
  const settings = resolveMusic(doc);
  const measured = parseLoudnorm((await runTool(ffmpeg, measureMixArgs(narration, musicFile, settings, seconds))).stderr);
  await runTool(ffmpeg, mixArgs(narration, musicFile, settings, seconds, measured, audio));
  const playbackAudio = path.join(previewDir, "playback-audio.m4a");
  await runTool(ffmpeg, bookendedAudioArgs(audio, musicFile, timeline.total_frames, introAtFrame, playbackAudio));

  const partial = path.join(previewDir, `${stem}.partial.mp4`);
  await runTool(ffmpeg, muxArgs(video, playbackAudio, partial));
  const probe = JSON.parse((await runTool(ffprobe, probeArgs(partial))).stdout);
  const totalFrames = timeline.total_frames + INTRO_FRAMES + OUTRO_FRAMES;
  const problems = checkProbe(probe, { frames: totalFrames });
  if (problems.length) throw new Error(`preview encoding check failed: ${problems.join("; ")}; inspect ${partial}`);
  const texts = Object.fromEntries(doc.scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
  const { cues, missing } = buildCues(timeline, texts, "zh-TW");
  if (missing.length) throw new Error(`preview captions are missing ${missing.length} line(s): ${missing.join(", ")}`);
  const presentedCues = shiftPreviewCues(cues, timeline, introAtFrame);
  const srt = path.join(previewDir, `${stem}.zh-TW.srt`);
  const vtt = path.join(previewDir, `${stem}.zh-TW.vtt`);
  const srtPartial = `${srt}.partial`;
  const vttPartial = `${vtt}.partial`;
  writeFileSync(srtPartial, toSrt(presentedCues));
  writeFileSync(vttPartial, toVtt(presentedCues));
  // A long encode may overlap media generation. Reject any changed source bytes,
  // including rendered cards and the manifests that bind voice and music.
  const current = await inspect(workdir, { allowReviewNeeded });
  if (current.issues.length || previewSourcesChanged({ scriptSha, timelineSha, manifestSha, framesSha, musicSha, cardFiles, reviewNeeded }, current)) {
    throw new Error(`preview source changed during encoding; inspect the current script and media (${current.issues.join("; ") || "source hash changed"})`);
  }
  const sidecar = path.join(previewDir, `${stem}.json`);
  const sidecarPartial = `${sidecar}.partial`;
  const evidence = reviewSidecar({
    doc, stem, scriptSha, timelineSha, manifestSha, framesSha, musicSha, cardFiles, reviewNeeded,
    outputSha: await sha256File(partial),
    srtSha: await sha256File(srtPartial),
    vttSha: await sha256File(vttPartial),
  });
  writeFileSync(sidecarPartial, `${JSON.stringify(evidence, null, 2)}\n`);
  publishPreviewFiles({ partial, output, srtPartial, srt, vttPartial, vtt, sidecarPartial, sidecar, force });
  process.stdout.write(`UNAPPROVED CONCEPT: ${reviewNeeded.length} review-needed keyframe(s); evidence ${sidecar}\n`);
  const captionProblems = checkCues(presentedCues, "zh-TW");
  process.stdout.write(`${output}: ${totalFrames} frames, ${(totalFrames / 30).toFixed(2)} s, 1920×1080/30 fps; unreviewed local preview with concept bookends, not official branding\n`);
  process.stdout.write(`preview zh-TW captions: ${presentedCues.length} cues, ${captionProblems.length} timing or reading-speed warnings\n`);
}

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: { workdir: { type: "string" }, "dry-run": { type: "boolean" }, force: { type: "boolean" }, "allow-review-needed": { type: "boolean" }, help: { type: "boolean" } },
    strict: true,
  });
  if (values.help) { process.stdout.write(`${usage}\n`); return; }
  if (!values.workdir) throw new Error(usage);
  const workdir = resolveWorkdir({ flag: values.workdir, slug: SLUG, root: ROOT });
  const previewDir = path.join(workdir, "review", "local-preview");
  const allowReviewNeeded = Boolean(values["allow-review-needed"]);
  const ready = await inspect(workdir, { allowReviewNeeded });
  const stem = previewStem(allowReviewNeeded, ready.reviewNeeded);
  process.stdout.write(`${SLUG}: ${ready.doc.scenes.filter((scene) => scene.template === "shot").length} still shots, ${ready.doc.scenes.filter((scene) => scene.template !== "shot").length} cards\n`);
  process.stdout.write(`UNAPPROVED CONCEPT: ${ready.reviewNeeded.length} review-needed keyframe(s)${ready.reviewNeeded.length ? `: ${ready.reviewNeeded.map(({ id }) => id).join(", ")}; owner review required` : "; concept branding still requires owner review"}\n`);
  if (ready.issues.length) for (const issue of ready.issues) process.stdout.write(`NEEDS ${issue}\n`);
  if (values["dry-run"]) {
    process.stdout.write(`local preview: ${ready.issues.length ? "not ready" : "ready"}; output ${path.join(previewDir, `${stem}.mp4`)}\n`);
    return;
  }
  if (ready.issues.length) throw new Error("local preview needs the current generated media listed above");
  await encode({ ...ready, workdir, previewDir, force: values.force, allowReviewNeeded });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
}
