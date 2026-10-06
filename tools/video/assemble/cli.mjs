// `assemble`: frames + narration → final.mp4, then the checks that prove it is what the timeline says.
// A drama (docs/videos/DRAMA.md) also brings its clips, its subtitle strips and its music: each
// shot is fitted to its lines and captioned in its own segment, the music is ducked under the voice.
// A shot marked visual "still" (docs/videos/BINGE.md) has no clip: its keyframe is animated with a
// slow camera move in a motion segment that encodes exactly like a clip segment.
// `assemble sfx-measure` is the one step beside the assembly: it measures a sound-effect set's
// files and writes their loudness into the set's manifest (docs/videos/ILLUSTRATED.md §配樂與音效).
import { existsSync, mkdirSync, readdirSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { burnIn, hasPictures, illustrated, isDrama, keyframesHash, lookHash, mixHash, picturesHash, resolveSfx, sfxHash, shotScenes, subtitlesHash } from "../core/drama.mjs";
import { hasAnimePolicy, runtimePolicyHash } from "../core/anime-policy.mjs";
import { sha256File } from "../core/approvals.mjs";
import { animeBodyDurationProblems, animeDurationProblems, animeRuntimeProof, animeShotFitProblems } from "../core/duration.mjs";
import { presentationTimeline, selectBrandingForBuild } from "../core/branding.mjs";
import { productionClipProblems } from "../core/lint.mjs";
import { audioEvidenceProblems } from "../core/audio-evidence.mjs";
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
  frameArgs,
  freezeProblem,
  illustratedTransition,
  keyframeProblem,
  lastFrameArgs,
  layoutDrama,
  measureMixArgs,
  mixArgs,
  motionFramePsnrArgs,
  motionSegmentArgs,
  motionSegmentKey,
  sourceFrameProblem,
  subtitleTrack,
} from "./drama.mjs";
import { locateFfmpeg as defaultLocateFfmpeg, runTool as defaultRunTool, ToolMissing } from "./ffmpeg.mjs";
import {
  checkLoudness,
  checkProbe,
  CLEAR_PSNR,
  concatList,
  ebur128Args,
  joinArgs,
  layoutScenes,
  LOUDNESS,
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
import {
  duckedBedArgs,
  mixWindowsArgs,
  parseEbur128Windows,
  sfxAudibility,
  sfxDir,
  sfxGains,
  sfxMeasureArgs,
  sfxPlan,
  sfxSetHash,
  sfxSetProblems,
  sfxTargetLufs,
  sfxTrackArgs,
  sfxTrackGainDb,
  soundMeasurement,
  underMixArgs,
} from "./sfx.mjs";
import { musicInputs, sfxInputs, sfxManifestFile } from "./sound.mjs";
import { commitBrandedVideo, verifyBrandingAssets, wrapVideo } from "./branding.mjs";

export const SFX_MEASURE = "sfx-measure";

/** The length of the first audio stream ffprobe reports, in seconds, or null. */
function audioSeconds(probe) {
  const value = Number(probe?.streams?.find((stream) => stream.codec_type === "audio")?.duration);
  return Number.isFinite(value) && value > 0 ? Number(value.toFixed(3)) : null;
}

/** How long each sound the cut uses lasts: the manifest's word (a measured set), else ffprobe's. */
async function soundSeconds(sfx, events, tools, runTool) {
  const seconds = {};
  for (const name of new Set(events.map((event) => event.sound))) {
    seconds[name] = sfx.sounds[name].seconds ?? audioSeconds(JSON.parse((await runTool(tools.ffprobe, probeArgs(sfx.files[name]))).stdout)) ?? 0;
  }
  return seconds;
}

/**
 * `assemble sfx-measure`: measure every sound of a set with ebur128 (integrated and loudest
 * momentary loudness, true peak) and ffprobe (its length), write them with each file's hash into
 * the set's manifest as version 2, and print the manifest's hash for the script's sfx.sha256. The
 * set is --set NAME under <work base>/_sfx/, or the one the script of --slug/--file names.
 */
async function measureSfxSet(values, ctx, { locateFfmpeg, runTool }) {
  const { EXIT } = ctx;
  let set = values.set ?? null;
  if (!set) {
    if (!values.slug && !values.file) throw new UsageError(`assemble ${SFX_MEASURE} needs --set NAME (a set under <work base>/_sfx/) or --slug/--file of a script that names one`);
    const { doc } = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
    set = resolveSfx(doc)?.set ?? null;
    if (!set) {
      ctx.stderr.write(`${doc.slug} names no sound-effect set (video.json sfx.set)\n`);
      return EXIT.usage;
    }
  }
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  const dir = sfxDir(workBase, set);
  const manifestFile = sfxManifestFile(workBase, set);
  const manifest = readJson(manifestFile, null);
  if (!manifest) {
    ctx.stderr.write(`set ${set} has no manifest.json in ${dir}: write one naming the licensed sounds first (docs/videos/ILLUSTRATED.md §配樂與音效)\n`);
    return EXIT.usage;
  }
  const problems = sfxSetProblems(manifest, { measured: false });
  if (problems.length) {
    ctx.stderr.write(`the sound-effect set ${set} is not usable: ${problems.join("; ")}\n`);
    return EXIT.usage;
  }
  for (const [name, sound] of Object.entries(manifest.sounds)) {
    if (!existsSync(path.join(dir, sound.file))) {
      ctx.stderr.write(`sound ${name} of set ${set} is missing: ${path.join(dir, sound.file)}\n`);
      return EXIT.usage;
    }
  }
  let tools;
  try {
    tools = await locateFfmpeg(ctx.env);
  } catch (error) {
    if (!(error instanceof ToolMissing)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.missing;
  }
  for (const [name, sound] of Object.entries(manifest.sounds)) {
    const file = path.join(dir, sound.file);
    const seconds = audioSeconds(JSON.parse((await runTool(tools.ffprobe, probeArgs(file))).stdout));
    let measured;
    try {
      measured = soundMeasurement((await runTool(tools.ffmpeg, sfxMeasureArgs(file))).stderr);
    } catch (error) {
      if (!(error instanceof PlanError)) throw error;
      ctx.stderr.write(`${sound.file}: ${error.message}\n`);
      return EXIT.usage;
    }
    Object.assign(sound, { sha256: await sha256File(file) }, measured);
    if (seconds) sound.seconds = seconds;
    ctx.stdout.write(`${name}: ${sound.file} ${measured.lufs_i} LUFS (loudest window ${measured.lufs_m}), true peak ${measured.peak_dbtp} dBTP${seconds ? `, ${seconds} s` : ""}; target ${sfxTargetLufs(name, sound)} LUFS\n`);
  }
  manifest.manifest_version = 2;
  atomicWrite(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
  ctx.stdout.write(`${manifestFile}: version 2, ${Object.keys(manifest.sounds).length} sounds measured\n`);
  ctx.stdout.write(`manifest sha256 ${await sha256File(manifestFile)}: write it as sfx.sha256 in video.json to bind the cut to this set\n`);
  return EXIT.ok;
}

/**
 * What a video needs beyond the frames and narration, each checked against the script it was
 * made for. A drama: the clips manifest (which names the keyframe of every still shot too) and
 * current subtitle strips when they are burned in. Illustrated slides: the keyframes manifest
 * bound to this look and these shots, every shot drawn and none waiting for a prompt fix. Any
 * format: the music and the sound effects it names. Returns { problem } with what to run first
 * when something is missing, else the inputs (null when the video needs nothing extra).
 */
async function mediaInputs(doc, workdir, workBase, manifest, speech, visual) {
  const drama = isDrama(doc);
  const pictures = illustrated(doc);
  const sound = await musicInputs(doc, workdir, workBase);
  if (sound.problem) return sound;
  const effects = await sfxInputs(doc, workBase);
  if (effects.problem) return effects;
  if (!drama && !pictures && !sound.track && !effects.sfx) return null;
  const look = hasPictures(doc) ? lookHash(doc) : null;
  let subtitles = false;
  let clips = null;
  let keyframes = null;
  if (drama) {
    subtitles = burnIn(doc);
    if (subtitles && (manifest.speech_hash !== speech || manifest.subtitles_hash !== subtitlesHash(doc) || !manifest.subtitles)) {
      return { problem: "frames/manifest.json has no subtitle strips for this script; run render again" };
    }
    clips = readJson(path.join(workdir, ARTIFACTS.clips), null);
    if (!clips || clips.speech_hash !== speech || clips.visual_hash !== visual || clips.look_hash !== look) {
      return { problem: "clips/manifest.json is missing or was made for an older script or look; run clips first" };
    }
    keyframes = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
  } else if (pictures) {
    keyframes = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
    if (!keyframes || keyframes.look_hash !== look || keyframes.pictures_hash !== picturesHash(doc)) {
      return { problem: "keyframes/manifest.json is missing or was drawn for another look or other shots; run keyframes first" };
    }
    const missing = shotScenes(doc).filter((scene) => !keyframes.shots?.[scene.id]?.file).map((scene) => scene.id);
    if (missing.length) return { problem: `keyframes/manifest.json has no picture for ${missing.join(", ")}; run keyframes first` };
    const waiting = shotScenes(doc).filter((scene) => keyframes.shots[scene.id].needs_review).map((scene) => scene.id);
    if (waiting.length) return { problem: `${waiting.join(", ")} failed the judge (needs_review in keyframes/manifest.json); fix the prompts and run keyframes again` };
  }
  return { look, subtitles, clips, keyframes, music: sound.music, track: sound.track, sfx: effects.sfx };
}

export async function run(command, args, ctx, { locateFfmpeg = defaultLocateFfmpeg, runTool = defaultRunTool } = {}) {
  const { EXIT } = ctx;
  const { values, positionals } = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, set: { type: "string" }, force: { type: "boolean" }, "adopt-branding": { type: "boolean" } },
    strict: true,
    allowPositionals: true,
  });
  if (positionals[0] === SFX_MEASURE) return measureSfxSet(values, ctx, { locateFfmpeg, runTool });
  if (positionals.length) throw new UsageError(`assemble has no step "${positionals[0]}"; its one step is: assemble ${SFX_MEASURE} [--set NAME | --slug S] [--workdir D]`);
  if (values.set) throw new UsageError(`--set belongs to assemble ${SFX_MEASURE}`);
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
  const bodyProblems = animeBodyDurationProblems({ doc, timeline, timelineCurrent: true });
  if (bodyProblems.length) {
    ctx.stderr.write(`${bodyProblems.join("; ")}\n`);
    return EXIT.lint;
  }
  const audioProblems = audioEvidenceProblems(timeline, workdir);
  if (audioProblems.length) {
    ctx.stderr.write(`narration needs current audio evidence before assembly: ${audioProblems.join("; ")}\n`);
    return EXIT.usage;
  }
  const manifest = readJson(path.join(workdir, ARTIFACTS.frames), null);
  const visual = visualHash(doc);
  if (!manifest || manifest.visual_hash !== visual) {
    ctx.stderr.write("frames/manifest.json is missing or was rendered for an older script; run render first\n");
    return EXIT.usage;
  }
  const drama = isDrama(doc);
  const pictures = illustrated(doc);
  const inputs = await mediaInputs(doc, workdir, workBase, manifest, speech, visual);
  if (inputs?.problem) {
    ctx.stderr.write(`${inputs.problem}\n`);
    return EXIT.usage;
  }
  const productionProblems = productionClipProblems(doc, project.series, timeline, inputs?.clips);
  if (productionProblems.length) {
    ctx.stderr.write(`production clips need review before assembly: ${productionProblems.map((problem) => `${problem.path}: ${problem.message}`).join("; ")}\n`);
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
  const branding = await selectBrandingForBuild({ doc, workdir, workBase, adoptCurrent: values["adopt-branding"] });
  if (branding) await verifyBrandingAssets(branding, { tools });

  let layout;
  try {
    // Illustrated slides (docs/videos/ILLUSTRATED.md) take the drama's mixed layout: the shots
    // under their camera moves, single-state cards drifting, dissolves between pictures and a
    // hard cut into every chapter card.
    layout = drama
      ? layoutDrama(doc, timeline, manifest, inputs.clips, inputs.keyframes)
      : pictures
        ? layoutDrama(doc, timeline, manifest, null, inputs.keyframes, { transitionRule: illustratedTransition, cardMotion: true })
        : layoutScenes(timeline, manifest);
  } catch (error) {
    if (!(error instanceof PlanError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.usage;
  }
  /** The frames a clip offers a shot: all of them, or those after the frame a cut from another shot starts at. */
  const offered = (frames, scene) => frames - (scene.from_frame ?? 0);
  const pastTheEnd = (scene) => `shot ${scene.id} is cut from ${scene.source.shot}'s clip at ${scene.source.from_s} s, past that clip's end; start earlier and run clips again\n`;
  const fits = {};
  if (hasAnimePolicy(doc)) {
    const shotEvidence = [];
    for (const scene of layout) {
      if (scene.kind === "motion") {
        shotEvidence.push({ shot: scene.id, kind: "motion", move: scene.move.name });
        continue;
      }
      if (scene.kind !== "clip") continue;
      const source = path.join(workdir, scene.clip.file);
      if (!existsSync(source)) {
        ctx.stderr.write(`${scene.clip.file} for shot ${scene.id} is missing; run clips again\n`);
        return EXIT.usage;
      }
      const available = offered(clipFrames(JSON.parse((await runTool(tools.ffprobe, probeArgs(source))).stdout)), scene);
      if (available <= 0) {
        ctx.stderr.write(pastTheEnd(scene));
        return EXIT.usage;
      }
      fits[scene.id] = { available, ...fitPlan(available, scene.frames, scene.fit) };
      shotEvidence.push({ shot: scene.id, kind: "clip", fit: fits[scene.id] });
    }
    const fitProblems = animeShotFitProblems({ doc, timeline, shots: shotEvidence });
    if (fitProblems.length) {
      ctx.stderr.write(`${fitProblems.join("; ")}\n`);
      return EXIT.lint;
    }
  }
  // The sound effects (docs/videos/ILLUSTRATED.md §配樂與音效): the cut's beats and the script's
  // own cues, planned before any segment is encoded so a cue past the video stops the run first.
  let effects = [];
  if (inputs?.sfx) {
    try {
      effects = sfxPlan(layout, timeline, doc);
    } catch (error) {
      if (!(error instanceof PlanError)) throw error;
      ctx.stderr.write(`${error.message}\n`);
      return EXIT.usage;
    }
  }
  const started = Date.now();
  const segmentsDir = path.join(workdir, "segments");
  const buildDir = path.join(workdir, "build");
  mkdirSync(segmentsDir, { recursive: true });
  mkdirSync(buildDir, { recursive: true });
  const resolve = (file) => path.join(workdir, file);
  const segmentFiles = [];
  const keys = [];
  let encoded = 0;
  for (const [index, scene] of layout.entries()) {
    if (stopRequested(workdir)) {
      ctx.stdout.write(`stopped by the STOP file after ${encoded} segments; rerun to continue\n`);
      return EXIT.ok;
    }
    if (scene.kind === "clip" || scene.kind === "motion") {
      const motion = scene.kind === "motion";
      const source = resolve(motion ? scene.keyframe.file : scene.clip.file);
      if (!existsSync(source)) {
        ctx.stderr.write(`${motion ? scene.keyframe.file : scene.clip.file} for shot ${scene.id} is missing; run ${motion ? "keyframes" : "clips"} again\n`);
        return EXIT.usage;
      }
      let fit = null;
      let available = null;
      if (!motion) {
        if (fits[scene.id]) {
          available = fits[scene.id].available;
          const { available: ignored, ...planned } = fits[scene.id];
          fit = planned;
        } else {
          const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(source))).stdout);
          available = offered(clipFrames(probe), scene);
          if (available <= 0) {
            ctx.stderr.write(pastTheEnd(scene));
            return EXIT.usage;
          }
          fit = fitPlan(available, scene.frames, scene.fit);
          fits[scene.id] = { available, ...fit };
        }
      }
      const strips = inputs?.subtitles ? subtitleTrack(scene, manifest.subtitles.cues, manifest.subtitles.blank) : null;
      // A dissolve overlays the previous scene's last frame, so its segment is keyed on that too.
      const previousKey = scene.transition === "dissolve" && index > 0 ? keys[index - 1] : null;
      const key = motion ? motionSegmentKey(scene, scene.move, strips, previousKey) : clipSegmentKey(scene, fit, strips, previousKey);
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
      const args = motion
        ? motionSegmentArgs({ keyframe: source, frames: scene.frames, move: scene.move, subtitlesList, dissolveFrom, outFile: partial })
        : clipSegmentArgs({ clip: source, frames: scene.frames, fit, fromFrame: scene.from_frame ?? 0, subtitlesList, dissolveFrom, outFile: partial });
      await runTool(tools.ffmpeg, args);
      renameSync(partial, segment);
      encoded += 1;
      if (motion) {
        ctx.stdout.write(`encoded ${scene.id} (${scene.frames} frames, ${scene.card ? "card " : ""}motion ${scene.move.name}${scene.transition === "dissolve" ? ", dissolve" : ""})\n`);
      } else {
        const how = fit.speed === 1 && fit.pad === 0 ? "" : ` at ${fit.speed}x${fit.pad ? `, last frame held ${fit.pad} frames` : ""}`;
        ctx.stdout.write(`encoded ${scene.id} (${scene.frames} frames from a ${available}-frame clip${how})\n`);
      }
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
  // The effects on one track, mixed over the voice and the bed; a script with a set but a cut
  // with no beat has no track. The mix under the effects is measured first: its integrated
  // loudness is what the final normalization will move, so a sound's target in the finished mix
  // becomes a gain on the track (a version 2 set; a version 1 set keeps its one gain_db), and its
  // windows are what each cue must be heard over.
  const musicFile = inputs?.track?.file ?? null;
  const music = inputs?.music ?? null;
  let sfxFile = null;
  let under = null;
  let audibility = null;
  if (effects.length) {
    under = parseEbur128Windows((await runTool(tools.ffmpeg, underMixArgs(narration, musicFile, music, totalSeconds))).stderr);
    effects = sfxGains(effects, inputs.sfx, LOUDNESS.integrated - under.integrated);
    sfxFile = path.join(buildDir, "sfx.wav");
    await runTool(tools.ffmpeg, sfxTrackArgs(effects, inputs.sfx.files, timeline.total_frames, sfxTrackGainDb(inputs.sfx), sfxFile));
  }
  if (musicFile || sfxFile) {
    measured = parseLoudnorm((await runTool(tools.ffmpeg, measureMixArgs(narration, musicFile, music, totalSeconds, sfxFile))).stderr);
    await runTool(tools.ffmpeg, mixArgs(narration, musicFile, music, totalSeconds, measured, audio, sfxFile));
    if (musicFile) {
      const bedLoudness = parseEbur128((await runTool(tools.ffmpeg, bedLoudnessArgs(narration, musicFile, music, totalSeconds))).stderr);
      bed = bedLevel(bedLoudness.integrated, measured);
    }
  } else {
    measured = parseLoudnorm((await runTool(tools.ffmpeg, measureLoudnessArgs(narration))).stderr);
    await runTool(tools.ffmpeg, normalizeArgs(narration, measured, audio));
  }
  const final = path.join(workdir, ARTIFACTS.video);
  const partialFinal = path.join(buildDir, "final.partial.mp4");
  const bodyPartial = branding ? path.join(buildDir, "body.partial.mp4") : null;
  let applied = null;
  if (branding) {
    await runTool(tools.ffmpeg, muxArgs(video, audio, bodyPartial));
    applied = await wrapVideo({ tools, workdir, bodyFile: bodyPartial, bodyFrames: timeline.total_frames, branding, outFile: partialFinal });
    applied.body_file = "build/body.mp4";
  } else {
    await runTool(tools.ffmpeg, muxArgs(video, audio, partialFinal));
    rmSync(final, { force: true });
    renameSync(partialFinal, final);
  }
  const presented = presentationTimeline(timeline, applied);
  const candidate = branding ? partialFinal : final;

  const problems = [];
  const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(candidate))).stdout);
  problems.push(...checkProbe(probe, { frames: presented.total_frames }));
  const loudness = parseEbur128((await runTool(tools.ffmpeg, ebur128Args(candidate))).stderr);
  problems.push(...checkLoudness(loudness));
  if (bed !== null) problems.push(...checkBed(bed));
  // Every cue measured where it sounds: the effects track, the mix under it, the ducked bed and
  // the whole mix through ebur128 on the same clock; a cue masked by the bed or one that would
  // push the mix past the normalization's ceiling fails the cut.
  if (sfxFile) {
    const finalGain = LOUDNESS.integrated - Number(measured.input_i);
    const effect = parseEbur128Windows((await runTool(tools.ffmpeg, ebur128Args(sfxFile))).stderr);
    const mix = parseEbur128Windows((await runTool(tools.ffmpeg, mixWindowsArgs(narration, musicFile, music, totalSeconds, sfxFile))).stderr);
    const ducked = musicFile ? parseEbur128Windows((await runTool(tools.ffmpeg, duckedBedArgs(narration, musicFile, music, totalSeconds))).stderr) : null;
    const seconds = await soundSeconds(inputs.sfx, effects, tools, runTool);
    audibility = sfxAudibility(effects, { effect: effect.windows, under: under.windows, bed: ducked?.windows ?? null, mix: mix.windows }, { seconds, finalGain });
    problems.push(...audibility.problems);
  }
  const psnr = [];
  layout.forEach((scene, index) => {
    if (scene.kind !== "stills") return;
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
  // is laid over it) and must not sit frozen on its last frame. A motion shot cannot freeze, and
  // opens on its keyframe only when its move starts at zoom 1.0 (a pull-out or a pan starts
  // inside the picture), so the picture chain's first frame is measured then and null is
  // recorded otherwise.
  const shots = [];
  for (const [index, scene] of layout.entries()) {
    if (scene.kind === "motion") {
      const record = { shot: scene.id, kind: "motion", move: scene.move.name, keyframe_psnr: null, ...(scene.card ? { card: true } : {}), ...(scene.transition === "dissolve" ? { transition: "dissolve" } : {}) };
      if (scene.move.startsAtIdentity && existsSync(resolve(scene.keyframe.file))) {
        const value = parsePsnr((await runTool(tools.ffmpeg, motionFramePsnrArgs(resolve(scene.keyframe.file), scene.move, scene.frames))).stderr);
        record.keyframe_psnr = Number.isFinite(value) ? Number(value.toFixed(2)) : "inf";
        const problem = keyframeProblem(scene, value);
        if (problem) problems.push(problem);
      }
      shots.push(record);
      continue;
    }
    if (scene.kind !== "clip") continue;
    const fit = fits[scene.id];
    const record = { shot: scene.id, kind: "clip", fit };
    const freeze = freezeProblem(scene, fit);
    if (freeze) problems.push(freeze);
    if (scene.keyframe && existsSync(resolve(scene.keyframe))) {
      const value = parsePsnr((await runTool(tools.ffmpeg, psnrArgs(resolve(scene.clip.file), 0, resolve(scene.keyframe)))).stderr);
      record.keyframe_psnr = Number.isFinite(value) ? Number(value.toFixed(2)) : "inf";
      const problem = keyframeProblem(scene, value);
      if (problem) problems.push(problem);
    } else if (scene.source) {
      // A cut from another shot's clip has no keyframe: its segment must open on that clip's
      // frame at from_s, which is pulled out by number and compared with the segment's frame 0.
      const frame = path.join(buildDir, `source-${scene.id}-${keys[index]}.png`);
      if (!existsSync(frame)) await runTool(tools.ffmpeg, frameArgs(resolve(scene.clip.file), scene.from_frame, frame));
      const value = parsePsnr((await runTool(tools.ffmpeg, psnrArgs(segmentFiles[index], 0, frame))).stderr);
      record.source = scene.source;
      record.source_frame_psnr = Number.isFinite(value) ? Number(value.toFixed(2)) : "inf";
      const problem = sourceFrameProblem(scene, value);
      if (problem) problems.push(problem);
    }
    shots.push(record);
  }
  const seconds = Math.round((Date.now() - started) / 1000);
  const finalSha256 = hasAnimePolicy(doc) ? await sha256File(candidate) : null;
  const checks = {
    ok: problems.length === 0,
    speech_hash: speech,
    narration_sha256: timeline.audio_evidence.narration_sha256,
    visual_hash: visual,
    ...(hasAnimePolicy(doc) ? { runtime_policy_hash: runtimePolicyHash(doc), final_sha256: finalSha256 } : {}),
    ...(drama ? { look_hash: inputs.look, clips_hash: inputs.clips.clips_hash, subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc) } : {}),
    // Illustrated slides bind the cut to the pictures it was made from; any video with music or
    // effects binds it to those too (core/state.mjs and package read them back).
    ...(pictures ? { look_hash: inputs.look, pictures_hash: keyframesHash(doc, inputs.keyframes) } : {}),
    ...(!drama && doc.music ? { mix_hash: mixHash(doc) } : {}),
    // sfx_hash is what status, package and dub compare with the script; sfx_set_hash adds the
    // very files of the set and a measured set's targets, for a reader of this file.
    ...(inputs?.sfx ? { sfx_hash: sfxHash(doc), sfx_set_hash: sfxSetHash(doc, inputs.sfx.manifest) } : {}),
    ...(applied ? { branding: applied } : {}),
    problems,
    metrics: {
      frames: presented.total_frames,
      ...(hasAnimePolicy(doc) ? { fps: FPS } : {}),
      loudness,
      psnr,
      loudnorm_first_pass: measured.input_i,
      ...(drama || pictures ? { shots, music_bed_lufs: bed, music: inputs.track ? path.basename(inputs.track.file) : null } : {}),
      ...(!drama && !pictures && inputs?.track ? { music_bed_lufs: bed, music: path.basename(inputs.track.file) } : {}),
      ...(inputs?.sfx ? {
        sfx: {
          set: inputs.sfx.set,
          version: inputs.sfx.version,
          events: effects.length,
          sounds: Object.fromEntries(Object.keys(inputs.sfx.files).map((name) => [name, effects.filter((event) => event.sound === name).length])),
          ...(audibility ? { cues: audibility.cues, min_bed_margin_db: audibility.min_bed_margin_db } : {}),
        },
      } : {}),
    },
    ffmpeg: tools.version,
    encoded_segments: encoded,
    seconds,
  };
  const durationInput = { doc, timeline, presented, timelineCurrent: true, checks, finalSha256 };
  problems.push(...animeDurationProblems(durationInput));
  checks.ok = problems.length === 0;
  if (checks.ok && hasAnimePolicy(doc)) checks.runtime_proof = animeRuntimeProof(durationInput);
  if (branding && checks.ok) commitBrandedVideo({ workdir, branding, finalPartial: partialFinal, bodyPartial, checks, now: ctx.now() });
  else atomicWrite(path.join(branding ? buildDir : workdir, branding ? "branding-failed-checks.json" : ARTIFACTS.checks), `${JSON.stringify(checks, null, 2)}\n`);
  recordStage(workdir, "assemble", { ok: checks.ok, encoded_segments: encoded, seconds, ...(drama || pictures ? { shots: shots.length, stills: shots.filter((shot) => shot.kind === "motion").length, music: bed !== null, sfx: effects.length } : {}) }, ctx.now());
  const marginText = audibility?.min_bed_margin_db === null || audibility?.min_bed_margin_db === undefined ? "" : ` (lowest ${audibility.min_bed_margin_db} dB above the bed)`;
  const bedText = `${bed === null ? "" : `, music bed ${bed} LUFS`}${effects.length ? `, ${effects.length} sound effects${marginText}` : ""}`;
  ctx.stdout.write(`${branding && !checks.ok ? candidate : final}: ${presented.total_frames} frames, ${loudness.integrated} LUFS, true peak ${loudness.truePeak} dBFS${bedText}; ${encoded} of ${layout.length} segments encoded in ${seconds} s\n`);
  for (const problem of problems) ctx.stdout.write(`CHECK ${problem}\n`);
  if (!checks.ok) return EXIT.lint;
  ctx.stdout.write(`next: node tools/video/cli.mjs review --slug ${doc.slug}\n`);
  return EXIT.ok;
}
