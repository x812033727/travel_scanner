// `assemble`: frames + narration → final.mp4, then the checks that prove it is what the timeline says.
import { existsSync, mkdirSync, readdirSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { atomicWrite, readJson, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "./ffmpeg.mjs";
import {
  checkLoudness,
  checkProbe,
  CLEAR_PSNR,
  concatList,
  ebur128Args,
  joinArgs,
  layoutScenes,
  measureLoudnessArgs,
  MIN_PSNR,
  muxArgs,
  normalizeArgs,
  parseEbur128,
  parseLoudnorm,
  parsePsnr,
  PlanError,
  probeArgs,
  psnrArgs,
  rivalImages,
  sampleProblem,
  segmentArgs,
  segmentKey,
  segmentSamples,
} from "./plan.mjs";

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, force: { type: "boolean" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("assemble needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  if (lintProject(project).errors.length) {
    ctx.stdout.write(`${project.doc.slug} has lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc, lexicon } = project;
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const speech = speechHash(doc, lexicon);
  if (!timeline || timeline.speech_hash !== speech) {
    ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first\n");
    return EXIT.usage;
  }
  const manifest = readJson(path.join(workdir, ARTIFACTS.frames), null);
  const visual = visualHash(doc);
  if (!manifest || manifest.visual_hash !== visual) {
    ctx.stderr.write("frames/manifest.json is missing or was rendered for an older script; run render first\n");
    return EXIT.usage;
  }
  let tools;
  try {
    tools = await locateFfmpeg(ctx.env);
  } catch (error) {
    if (!(error instanceof ToolMissing)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.missing;
  }

  let layout;
  try {
    layout = layoutScenes(timeline, manifest);
  } catch (error) {
    if (!(error instanceof PlanError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.usage;
  }
  const started = Date.now();
  const segmentsDir = path.join(workdir, "segments");
  const buildDir = path.join(workdir, "build");
  mkdirSync(segmentsDir, { recursive: true });
  mkdirSync(buildDir, { recursive: true });
  const resolve = (file) => path.join(workdir, file);
  const segmentFiles = [];
  let encoded = 0;
  for (const scene of layout) {
    if (stopRequested(workdir)) {
      ctx.stdout.write(`stopped by the STOP file after ${encoded} segments; rerun to continue\n`);
      return EXIT.ok;
    }
    const segment = path.join(segmentsDir, `${scene.id}-${segmentKey(scene)}.mp4`);
    segmentFiles.push(segment);
    if (existsSync(segment) && !values.force) continue;
    const list = path.join(segmentsDir, `${scene.id}.ffconcat`);
    writeFileSync(list, concatList(scene.entries, resolve));
    const partial = `${segment}.partial.mp4`;
    await runTool(tools.ffmpeg, segmentArgs(list, partial, scene.frames));
    renameSync(partial, segment);
    encoded += 1;
    ctx.stdout.write(`encoded ${scene.id} (${scene.frames} frames)\n`);
  }

  // Segments of scenes that have since changed are never used again.
  const kept = new Set(segmentFiles.map((file) => path.basename(file)));
  for (const name of readdirSync(segmentsDir)) {
    if (name.endsWith(".mp4") && !kept.has(name)) rmSync(path.join(segmentsDir, name), { force: true });
  }
  const joinList = path.join(buildDir, "segments.ffconcat");
  writeFileSync(joinList, `ffconcat version 1.0\n${segmentFiles.map((file) => `file '${file.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`).join("\n")}\n`);
  const video = path.join(buildDir, "video.mp4");
  await runTool(tools.ffmpeg, joinArgs(joinList, video));
  const narration = path.join(workdir, ARTIFACTS.narration);
  const measured = parseLoudnorm((await runTool(tools.ffmpeg, measureLoudnessArgs(narration))).stderr);
  const audio = path.join(buildDir, "audio.m4a");
  await runTool(tools.ffmpeg, normalizeArgs(narration, measured, audio));
  const final = path.join(workdir, ARTIFACTS.video);
  const partialFinal = path.join(buildDir, "final.partial.mp4");
  await runTool(tools.ffmpeg, muxArgs(video, audio, partialFinal));
  rmSync(final, { force: true });
  renameSync(partialFinal, final);

  const problems = [];
  const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(final))).stdout);
  problems.push(...checkProbe(probe, { frames: timeline.total_frames }));
  const loudness = parseEbur128((await runTool(tools.ffmpeg, ebur128Args(final))).stderr);
  problems.push(...checkLoudness(loudness));
  const psnr = [];
  layout.forEach((scene, index) =>
    psnr.push(...segmentSamples(scene).map((sample) => ({ scene: scene.id, segment: segmentFiles[index], rivalFiles: rivalImages(scene, sample.file), ...sample }))),
  );
  const measure = async (sample, file) => parsePsnr((await runTool(tools.ffmpeg, psnrArgs(sample.segment, sample.n, resolve(file)))).stderr);
  for (const sample of psnr) {
    const value = await measure(sample, sample.file);
    sample.psnr = Number.isFinite(value) ? Number(value.toFixed(2)) : "inf";
    // Only a frame in the grey zone is compared with the scene's other images.
    const rivals = {};
    if (value >= MIN_PSNR && value < CLEAR_PSNR) {
      for (const file of sample.rivalFiles) rivals[file] = await measure(sample, file);
      if (sample.rivalFiles.length) sample.rivals = Object.fromEntries(Object.entries(rivals).map(([file, score]) => [file, Number(score.toFixed(2))]));
    }
    const problem = sampleProblem(sample, value, rivals);
    if (problem) problems.push(problem);
    delete sample.segment;
    delete sample.rivalFiles;
  }
  const seconds = Math.round((Date.now() - started) / 1000);
  const checks = {
    ok: problems.length === 0,
    speech_hash: speech,
    visual_hash: visual,
    problems,
    metrics: { frames: timeline.total_frames, loudness, psnr, loudnorm_first_pass: measured.input_i },
    ffmpeg: tools.version,
    encoded_segments: encoded,
    seconds,
  };
  atomicWrite(path.join(workdir, ARTIFACTS.checks), `${JSON.stringify(checks, null, 2)}\n`);
  recordStage(workdir, "assemble", { ok: checks.ok, encoded_segments: encoded, seconds }, ctx.now());
  ctx.stdout.write(`${final}: ${timeline.total_frames} frames, ${loudness.integrated} LUFS, true peak ${loudness.truePeak} dBFS; ${encoded} of ${layout.length} segments encoded in ${seconds} s\n`);
  for (const problem of problems) ctx.stdout.write(`CHECK ${problem}\n`);
  if (!checks.ok) return EXIT.lint;
  ctx.stdout.write(`next: node tools/video/cli.mjs review --slug ${doc.slug}\n`);
  return EXIT.ok;
}
