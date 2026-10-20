// Build an unreviewed body-only preview from the episode's real TTS, keyframes,
// rendered cards and music. This deliberately does not run clips/assemble or write
// their manifests, approvals, checks.json or final.mp4.
import { existsSync, mkdirSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../../../tools/video/core/approvals.mjs";
import { audioEvidenceProblems } from "../../../tools/video/core/audio-evidence.mjs";
import { lookHash, mixHash, resolveMusic } from "../../../tools/video/core/drama.mjs";
import { isInside, readJson, resolveWorkdir, ROOT } from "../../../tools/video/core/paths.mjs";
import { ARTIFACTS, keyframeProblems, lintProject, loadProject } from "../../../tools/video/core/state.mjs";
import { speechHash, visualHash } from "../../../tools/video/core/timeline.mjs";
import { resolveWatermark } from "../../../tools/video/core/watermark.mjs";
import { lastFrameArgs, layoutDrama, measureMixArgs, mixArgs, motionSegmentArgs, motionSegmentKey } from "../../../tools/video/assemble/drama.mjs";
import { locateFfmpeg, runTool } from "../../../tools/video/assemble/ffmpeg.mjs";
import { checkProbe, concatList, joinArgs, muxArgs, parseLoudnorm, probeArgs, segmentArgs, segmentKey } from "../../../tools/video/assemble/plan.mjs";
import { themeHash } from "../../../tools/video/render/plan.mjs";

const SLUG = "story-everyday-crocs-c01";
const usage = "Usage: node docs/videos/story-everyday-crocs-c01/local-preview.mjs --workdir <media-base-outside-repo> [--dry-run] [--force]";
const fileAt = (workdir, name) => {
  const file = path.resolve(workdir, name);
  if (!isInside(file, workdir)) throw new Error(`media path escapes the work directory: ${name}`);
  return file;
};
const ffconcatFile = (file) => `file '${file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`;

async function inspect(workdir) {
  const project = loadProject({ slug: SLUG, root: ROOT });
  const { doc, lexicon } = project;
  const issues = lintProject(project).errors.map(({ path: where, message }) => `${where}: ${message}`);
  const notStill = doc.scenes.filter((scene) => scene.template === "shot" && scene.data?.visual !== "still");
  if (notStill.length) issues.push(`preview only supports still shots: ${notStill.map((scene) => scene.id).join(", ")}`);

  const timeline = readJson(fileAt(workdir, ARTIFACTS.timeline), null);
  if (!timeline) issues.push("timeline.json is missing; run TTS first");
  else {
    if (timeline.speech_hash !== speechHash(doc, lexicon)) issues.push("timeline.json belongs to an older script or voice");
    else issues.push(...audioEvidenceProblems(timeline, workdir));
  }

  const keyframes = readJson(fileAt(workdir, ARTIFACTS.keyframes), null);
  if (!keyframes) issues.push("keyframes/manifest.json is missing; generate the full keyframe batch first");
  else if (keyframes.look_hash !== lookHash(doc) || keyframes.visual_hash !== visualHash(doc)) issues.push("keyframes/manifest.json belongs to an older script or look");
  else issues.push(...await keyframeProblems({ doc, manifest: keyframes, workdir }));

  const frames = readJson(fileAt(workdir, ARTIFACTS.frames), null);
  if (!frames) issues.push("frames/manifest.json is missing; run render after keyframes");
  else if (frames.visual_hash !== visualHash(doc) || frames.theme_hash !== themeHash()) issues.push("frames/manifest.json belongs to an older script or render theme");
  else for (const scene of frames.scenes ?? []) for (const state of scene.states ?? []) {
    for (const name of [state.still, ...(state.transition ?? [])]) {
      if (!name || !existsSync(fileAt(workdir, name))) issues.push(`rendered card frame is missing: ${name ?? "(unnamed)"}`);
    }
  }

  const music = readJson(fileAt(workdir, ARTIFACTS.music), null);
  let musicFile = null;
  if (!music || music.mix_hash !== mixHash(doc) || !music.file || !music.sha256) issues.push("music/manifest.json is missing or stale; run music first");
  else {
    musicFile = fileAt(workdir, music.file);
    if (!existsSync(musicFile) || await sha256File(musicFile) !== music.sha256) issues.push(`music track is missing or changed: ${music.file}`);
  }

  let layout = null;
  if (timeline && keyframes && frames && !issues.length) {
    try { layout = layoutDrama(doc, timeline, frames, null, keyframes); }
    catch (error) { issues.push(error.message); }
  }
  return { doc, timeline, frames, musicFile, layout, issues };
}

async function encode({ doc, timeline, frames, musicFile, layout, workdir, previewDir, force }) {
  const output = path.join(previewDir, "preview.mp4");
  if (existsSync(output) && !force) throw new Error(`${output} already exists; pass --force to replace this local preview`);
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
    const segment = path.join(segmentsDir, `${scene.id}-${key}.mp4`);
    segments.push(segment);
    if (existsSync(segment)) continue;
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
  }

  const joinedList = path.join(previewDir, "segments.ffconcat");
  writeFileSync(joinedList, `ffconcat version 1.0\n${segments.map(ffconcatFile).join("\n")}\n`);
  const video = path.join(previewDir, "body.mp4");
  await runTool(ffmpeg, joinArgs(joinedList, video));

  const audio = path.join(previewDir, "audio.m4a");
  const narration = fileAt(workdir, ARTIFACTS.narration);
  const seconds = timeline.total_frames / 30;
  const settings = resolveMusic(doc);
  const measured = parseLoudnorm((await runTool(ffmpeg, measureMixArgs(narration, musicFile, settings, seconds))).stderr);
  await runTool(ffmpeg, mixArgs(narration, musicFile, settings, seconds, measured, audio));

  const partial = path.join(previewDir, "preview.partial.mp4");
  await runTool(ffmpeg, muxArgs(video, audio, partial));
  const probe = JSON.parse((await runTool(ffprobe, probeArgs(partial))).stdout);
  const problems = checkProbe(probe, { frames: timeline.total_frames });
  if (problems.length) throw new Error(`preview encoding check failed: ${problems.join("; ")}; inspect ${partial}`);
  renameSync(partial, output);
  process.stdout.write(`${output}: ${timeline.total_frames} frames, ${seconds.toFixed(2)} s, 1920×1080/30 fps; body-only local preview, unreviewed\n`);
}

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: { workdir: { type: "string" }, "dry-run": { type: "boolean" }, force: { type: "boolean" }, help: { type: "boolean" } },
    strict: true,
  });
  if (values.help) { process.stdout.write(`${usage}\n`); return; }
  if (!values.workdir) throw new Error(usage);
  const workdir = resolveWorkdir({ flag: values.workdir, slug: SLUG, root: ROOT });
  const previewDir = path.join(workdir, "review", "local-preview");
  const ready = await inspect(workdir);
  process.stdout.write(`${SLUG}: ${ready.doc.scenes.filter((scene) => scene.template === "shot").length} still shots, ${ready.doc.scenes.filter((scene) => scene.template !== "shot").length} cards\n`);
  if (ready.issues.length) for (const issue of ready.issues) process.stdout.write(`NEEDS ${issue}\n`);
  if (values["dry-run"]) {
    process.stdout.write(`local preview: ${ready.issues.length ? "not ready" : "ready"}; output ${path.join(previewDir, "preview.mp4")}\n`);
    return;
  }
  if (ready.issues.length) throw new Error("local preview needs the current generated media listed above");
  await encode({ ...ready, workdir, previewDir, force: values.force });
}

main().catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
