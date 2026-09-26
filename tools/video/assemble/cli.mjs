// `assemble`: frames + narration → final.mp4, then the checks that prove it is what the timeline says.
// A drama (docs/videos/DRAMA.md) also brings its clips, its subtitle strips and its music: each
// shot is fitted to its lines and captioned in its own segment, the music is ducked under the voice.
import { existsSync, mkdirSync, readdirSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../core/approvals.mjs";
import { burnIn, isDrama, lookHash, mixHash, resolveMusic, subtitlesHash } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { FPS, speechHash, visualHash } from "../core/timeline.mjs";
import {
  bedLevel,
  bedLoudnessArgs,
  checkBed,
  clipFrames,
  clipSegmentArgs,
  clipSegmentKey,
  fitPlan,
  freezeProblem,
  keyframeProblem,
  lastFrameArgs,
  layoutDrama,
  measureMixArgs,
  mixArgs,
  subtitleTrack,
} from "./drama.mjs";
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

/**
 * What a drama needs beyond the frames and narration, each checked against the script it was
 * made for: the clips, current subtitle strips when they are burned in, and the music, either
 * generated into the work directory or the owner's own file under <work base>/_music/.
 * Returns { problem } with what to run first when something is missing.
 */
async function dramaInputs(doc, workdir, workBase, manifest, speech, visual) {
  const look = lookHash(doc);
  const subtitles = burnIn(doc);
  if (subtitles && (manifest.speech_hash !== speech || manifest.subtitles_hash !== subtitlesHash(doc) || !manifest.subtitles)) {
    return { problem: "frames/manifest.json has no subtitle strips for this script; run render again" };
  }
  const clips = readJson(path.join(workdir, ARTIFACTS.clips), null);
  if (!clips || clips.speech_hash !== speech || clips.visual_hash !== visual || clips.look_hash !== look) {
    return { problem: "clips/manifest.json is missing or was made for an older script or look; run clips first" };
  }
  const keyframes = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
  const music = resolveMusic(doc);
  let track = null;
  if (music?.track) {
    const file = path.join(workBase, "_music", music.track);
    if (!existsSync(file)) return { problem: `music.track ${music.track} is not in ${path.join(workBase, "_music")}` };
    if (music.sha256 && (await sha256File(file)) !== music.sha256) return { problem: `${music.track} does not match music.sha256; check the file or update video.json` };
    track = { file, sha256: music.sha256 ?? (await sha256File(file)) };
  } else if (music) {
    const generated = readJson(path.join(workdir, ARTIFACTS.music), null);
    if (!generated?.file || generated.mix_hash !== mixHash(doc)) return { problem: "music/manifest.json is missing or was made for older music settings; run music first" };
    track = { file: path.join(workdir, generated.file), sha256: generated.sha256 ?? null };
  }
  return { look, subtitles, clips, keyframes, music, track };
}

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
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
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
  const drama = isDrama(doc);
  const inputs = drama ? await dramaInputs(doc, workdir, workBase, manifest, speech, visual) : null;
  if (inputs?.problem) {
    ctx.stderr.write(`${inputs.problem}\n`);
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
    layout = drama ? layoutDrama(doc, timeline, manifest, inputs.clips, inputs.keyframes) : layoutScenes(timeline, manifest);
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
  const keys = [];
  const fits = {};
  let encoded = 0;
  for (const [index, scene] of layout.entries()) {
    if (stopRequested(workdir)) {
      ctx.stdout.write(`stopped by the STOP file after ${encoded} segments; rerun to continue\n`);
      return EXIT.ok;
    }
    if (scene.kind === "clip") {
      const clipFile = resolve(scene.clip.file);
      if (!existsSync(clipFile)) {
        ctx.stderr.write(`${scene.clip.file} for shot ${scene.id} is missing; run clips again\n`);
        return EXIT.usage;
      }
      const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(clipFile))).stdout);
      const available = clipFrames(probe);
      const fit = fitPlan(available, scene.frames, scene.fit);
      fits[scene.id] = { available, ...fit };
      const strips = inputs.subtitles ? subtitleTrack(scene, manifest.subtitles.cues, manifest.subtitles.blank) : null;
      // A dissolve overlays the previous scene's last frame, so its segment is keyed on that too.
      const previousKey = scene.transition === "dissolve" && index > 0 ? keys[index - 1] : null;
      const key = clipSegmentKey(scene, fit, strips, previousKey);
      keys[index] = key;
      const segment = path.join(segmentsDir, `${scene.id}-${key}.mp4`);
      segmentFiles.push(segment);
      if (existsSync(segment) && !values.force) continue;
      let subtitlesList = null;
      if (strips) {
        subtitlesList = path.join(segmentsDir, `${scene.id}-subtitles.ffconcat`);
        writeFileSync(subtitlesList, concatList(strips, resolve));
      }
      let dissolveFrom = null;
      if (previousKey) {
        const previous = layout[index - 1];
        dissolveFrom = path.join(buildDir, `last-${previous.id}-${previousKey}.png`);
        if (!existsSync(dissolveFrom)) await runTool(tools.ffmpeg, lastFrameArgs(segmentFiles[index - 1], previous.frames, dissolveFrom));
      }
      const partial = `${segment}.partial.mp4`;
      await runTool(tools.ffmpeg, clipSegmentArgs({ clip: clipFile, frames: scene.frames, fit, subtitlesList, dissolveFrom, outFile: partial }));
      renameSync(partial, segment);
      encoded += 1;
      const how = fit.speed === 1 && fit.pad === 0 ? "" : ` at ${fit.speed}x${fit.pad ? `, last frame held ${fit.pad} frames` : ""}`;
      ctx.stdout.write(`encoded ${scene.id} (${scene.frames} frames from a ${available}-frame clip${how})\n`);
      continue;
    }
    const key = segmentKey(scene);
    keys[index] = key;
    const segment = path.join(segmentsDir, `${scene.id}-${key}.mp4`);
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
  const audio = path.join(buildDir, "audio.m4a");
  const totalSeconds = timeline.total_frames / FPS;
  let measured;
  let bed = null;
  if (inputs?.track) {
    const { file, music } = { file: inputs.track.file, music: inputs.music };
    measured = parseLoudnorm((await runTool(tools.ffmpeg, measureMixArgs(narration, file, music, totalSeconds))).stderr);
    await runTool(tools.ffmpeg, mixArgs(narration, file, music, totalSeconds, measured, audio));
    const bedLoudness = parseEbur128((await runTool(tools.ffmpeg, bedLoudnessArgs(narration, file, music, totalSeconds))).stderr);
    bed = bedLevel(bedLoudness.integrated, measured);
  } else {
    measured = parseLoudnorm((await runTool(tools.ffmpeg, measureLoudnessArgs(narration))).stderr);
    await runTool(tools.ffmpeg, normalizeArgs(narration, measured, audio));
  }
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
  if (bed !== null) problems.push(...checkBed(bed));
  const psnr = [];
  layout.forEach((scene, index) => {
    if (scene.kind === "clip") return;
    psnr.push(...segmentSamples(scene).map((sample) => ({ scene: scene.id, segment: segmentFiles[index], rivalFiles: rivalImages(scene, sample.file), ...sample })));
  });
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
  // A shot's clip must open on its keyframe (measured on the clip itself, before any dissolve
  // is laid over it) and must not sit frozen on its last frame.
  const shots = [];
  for (const scene of layout) {
    if (scene.kind !== "clip") continue;
    const fit = fits[scene.id];
    const record = { shot: scene.id, fit };
    const freeze = freezeProblem(scene, fit);
    if (freeze) problems.push(freeze);
    if (scene.keyframe && existsSync(resolve(scene.keyframe))) {
      const value = parsePsnr((await runTool(tools.ffmpeg, psnrArgs(resolve(scene.clip.file), 0, resolve(scene.keyframe)))).stderr);
      record.keyframe_psnr = Number.isFinite(value) ? Number(value.toFixed(2)) : "inf";
      const problem = keyframeProblem(scene, value);
      if (problem) problems.push(problem);
    }
    shots.push(record);
  }
  const seconds = Math.round((Date.now() - started) / 1000);
  const checks = {
    ok: problems.length === 0,
    speech_hash: speech,
    visual_hash: visual,
    ...(drama ? { look_hash: inputs.look, clips_hash: inputs.clips.clips_hash, subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc) } : {}),
    problems,
    metrics: {
      frames: timeline.total_frames,
      loudness,
      psnr,
      loudnorm_first_pass: measured.input_i,
      ...(drama ? { shots, music_bed_lufs: bed, music: inputs.track ? path.basename(inputs.track.file) : null } : {}),
    },
    ffmpeg: tools.version,
    encoded_segments: encoded,
    seconds,
  };
  atomicWrite(path.join(workdir, ARTIFACTS.checks), `${JSON.stringify(checks, null, 2)}\n`);
  recordStage(workdir, "assemble", { ok: checks.ok, encoded_segments: encoded, seconds, ...(drama ? { shots: shots.length, music: bed !== null } : {}) }, ctx.now());
  const bedText = bed === null ? "" : `, music bed ${bed} LUFS`;
  ctx.stdout.write(`${final}: ${timeline.total_frames} frames, ${loudness.integrated} LUFS, true peak ${loudness.truePeak} dBFS${bedText}; ${encoded} of ${layout.length} segments encoded in ${seconds} s\n`);
  for (const problem of problems) ctx.stdout.write(`CHECK ${problem}\n`);
  if (!checks.ok) return EXIT.lint;
  ctx.stdout.write(`next: node tools/video/cli.mjs review --slug ${doc.slug}\n`);
  return EXIT.ok;
}
