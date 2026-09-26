// `clips`: one motion clip per shot, generated from the shot's keyframe with the chosen sheets
// as references, checked by ffmpeg and the judge, retaken with another seed when it fails
// (docs/videos/DRAMA.md). The most expensive stage, so it runs after the look, the narration,
// the keyframes and the storyboard have been approved, and every submission is checked against
// the per-video cap first. Writes clips/manifest.json (what assemble reads) and clips/<shot>-<seed>.mp4.
import { execFile } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { approvalState } from "../core/approvals.mjs";
import { clipKey, clipsHash, isDrama, lookHash, resolveLook, shotScenes } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { FPS, speechHash, visualHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { chosenSheets } from "./keyframes.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { blackdetectArgs, clipVerdict, framePsnrArgs, freezedetectArgs, parseBlackdetect, parseFreezedetect, parseProbe, parsePsnr, parseSceneCuts, probeArgs, sceneCutArgs } from "./qc.mjs";
import { chosenModel, clipSecondPrice, JUDGE_USD_PER_CALL, retakeable, Stage, statusProblem } from "./stages.mjs";

const exec = promisify(execFile);

export const MAX_CLIP_TAKES = 2;
export const MIN_CLIP_SECONDS = 4;
export const MAX_CLIP_SECONDS = 10;
export const MAX_REFERENCES = 4;

/** What the judge scores a clip on: each character in its last frame, then the motion itself. */
export function clipRubric(characters) {
  return [
    ...characters.map((character) => ({
      key: `identity_${character.id.replace(/-/g, "_")}`,
      question: `In the clip's last frame, is ${character.name} still the same person as in the reference sheet labelled "${character.name}": face, hair, clothing, build?`,
      weight: 2,
    })),
    { key: "motion", question: "Is the motion natural and continuous: no morphing, no flicker, no limbs or objects drifting or changing shape?", weight: 2 },
    { key: "prompt", question: "Does the clip show the motion and the camera move that were asked for?", weight: 1 },
    { key: "clean", question: "Are hands, faces and bodies correct throughout, with nothing appearing or vanishing?", weight: 2 },
    { key: "no_text", question: "Is the clip free of text, letters, watermarks and logos?", weight: 1 },
  ];
}

/** Whole seconds to ask for: the lines' length rounded up, 4 to 10, at a duration the model offers. */
export function clipSeconds(neededFrames, durations = []) {
  const need = Math.max(MIN_CLIP_SECONDS, Math.min(MAX_CLIP_SECONDS, Math.ceil(neededFrames / FPS)));
  const allowed = [...durations].filter((each) => Number.isInteger(each)).sort((a, b) => a - b);
  if (!allowed.length) return need;
  return allowed.find((each) => each >= need) ?? allowed.at(-1);
}

export function clipPrompt(scene, look) {
  return [scene.data?.motion, scene.data?.camera, look.motion].filter(Boolean).join(". ").slice(0, 4000);
}

/** A 720p copy for the judge, whose inline limit a 1080p clip may pass. */
export function proxyArgs(clip, out) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", clip, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", out];
}

/** The last frame of a clip as a PNG: what the next shot continues from. */
export function lastFrameArgs(clip, frames, out) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", clip, "-vf", `select=eq(n\\,${Math.max(0, frames - 1)})`, "-fps_mode", "passthrough", "-frames:v", "1", out];
}

/** Everything ffmpeg can say about a clip, for `clipVerdict`; `ctx.clipQc(file, wanted)` replaces ffmpeg in tests. */
async function inspect(ctx, tools, file, wanted) {
  if (ctx.clipQc) return ctx.clipQc(file, wanted);
  const probe = parseProbe((await runTool(tools.ffprobe, probeArgs(file))).stdout);
  const black = parseBlackdetect((await runTool(tools.ffmpeg, blackdetectArgs(file))).stderr);
  const freezes = parseFreezedetect((await runTool(tools.ffmpeg, freezedetectArgs(file))).stderr, probe.duration);
  const cuts = parseSceneCuts((await runTool(tools.ffmpeg, sceneCutArgs(file))).stderr);
  const psnr = async (image) => parsePsnr((await runTool(tools.ffmpeg, framePsnrArgs(file, 0, image, probe.width, probe.height))).stderr);
  const keyframePsnr = wanted.keyframe ? await psnr(wanted.keyframe) : null;
  let rival = null;
  for (const image of wanted.rivals ?? []) {
    const score = await psnr(image);
    if (score !== null && (rival === null || score > rival)) rival = score;
  }
  return { probe, black, freezes, cuts, keyframe_psnr: keyframePsnr, rival_psnr: rival };
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.clips);

function writeManifest(workdir, doc, manifest) {
  const order = shotScenes(doc).filter((scene) => manifest.shots[scene.id]?.sha256).map((scene) => ({ id: scene.id, sha256: manifest.shots[scene.id].sha256 }));
  manifest.clips_hash = clipsHash(order);
  atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, shot: { type: "string" }, force: { type: "boolean" }, "dry-run": { type: "boolean" }, takes: { type: "string" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("clips needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc, lexicon } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc)) throw new UsageError("clips is for a drama (format \"drama\")");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const speech = speechHash(doc, lexicon);
  const visual = visualHash(doc);
  const hash = lookHash(doc);
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline || timeline.speech_hash !== speech) {
    ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first (a clip is as long as its lines)\n");
    return EXIT.usage;
  }
  const keyframes = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
  if (!keyframes || keyframes.look_hash !== hash || keyframes.visual_hash !== visual) {
    ctx.stderr.write("keyframes/manifest.json is missing or was drawn for an older script or look; run keyframes first\n");
    return EXIT.usage;
  }
  const wanted = values.shot ? new Set(values.shot.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  const shots = shotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  if (!shots.length) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug}`);
  const undrawn = shots.filter((scene) => !keyframes.shots?.[scene.id]?.file || keyframes.shots[scene.id].needs_review);
  if (undrawn.length) {
    ctx.stderr.write(`shots ${undrawn.map((scene) => scene.id).join(", ")} have no passed keyframe; run keyframes first\n`);
    return EXIT.usage;
  }
  const storyboard = await approvalState({ gate: "storyboard", docDir: project.dir, workdir });
  if (storyboard.status !== "approved") {
    const why = storyboard.status === "stale" ? "changed since it was approved" : "not approved yet";
    throw new MediaError(`the storyboard is ${why}: run review-push --gate storyboard, let the owner (or the auto-approve setting) decide on /admin/videos, then review-pull`, { who: "owner" });
  }
  const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
  const sheets = chosenSheets(lookManifest, lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash) ?? {});
  const byId = new Map((doc.characters ?? []).map((character) => [character.id, character]));
  const cast = (scene) => (scene.data.characters ?? []).map((id) => byId.get(id)).filter(Boolean);
  const framesOf = new Map(timeline.scenes.map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const takes = values.takes ? Number(values.takes) : MAX_CLIP_TAKES;
  if (!Number.isInteger(takes) || takes < 1 || takes > 5) throw new UsageError("--takes must be 1 to 5");

  if (values["dry-run"]) {
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    const status = credentials.token ? await mediaStatus(clientOptions(ctx, credentials)) : null;
    const durations = status ? (chosenModel(status, "clip")?.durations ?? []) : [];
    const price = status ? clipSecondPrice(status) : 0;
    let total = 0;
    for (const scene of shots) {
      const seconds = clipSeconds(framesOf.get(scene.id) ?? 0, durations);
      total += seconds;
      ctx.stdout.write(`${scene.id}: ${((framesOf.get(scene.id) ?? 0) / FPS).toFixed(1)} s of lines → ${seconds} s clip${status ? ` ≈ US$${(seconds * price).toFixed(2)}` : ""}; ${clipPrompt(scene, look)}\n`);
    }
    ctx.stdout.write(`${shots.length} shots, ${total} clip seconds for one take each\n`);
    if (status) {
      const problem = statusProblem(status, "clip");
      const budget = status.budgets?.clip_seconds;
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.clip.provider} ${status.clip.model} ${status.clip.resolution} ready`}; about US$${(total * price + shots.length * JUDGE_USD_PER_CALL).toFixed(2)}${budget ? `; ${budget.remaining} of ${budget.limit} clip seconds left this month` : ""}; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await mediaStatus(options);
  const problem = statusProblem(status, "clip");
  if (problem) throw new MediaError(problem, { who: "owner" });
  const model = chosenModel(status, "clip");
  const durations = model?.durations ?? [];
  const resolution = status.clip.resolution ?? null;
  let tools = null;
  if (!ctx.clipQc) {
    try {
      tools = await locateFfmpeg(ctx.env);
    } catch (error) {
      if (!(error instanceof ToolMissing)) throw error;
      ctx.stderr.write(`${error.message}\n`);
      return EXIT.missing;
    }
  }
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "clips", now: ctx.now });
  mkdirSync(path.join(workdir, "clips"), { recursive: true });
  const existing = readJson(manifestFile(workdir), null);
  const current = existing?.speech_hash === speech && existing.visual_hash === visual && existing.look_hash === hash && !values.force;
  const manifest = current ? existing : { speech_hash: speech, visual_hash: visual, look_hash: hash, shots: {} };
  manifest.clip = { provider: status.clip.provider, model: status.clip.model, resolution };
  // The keyframes and the chosen sheets go back to the media store once per run (the server may
  // have pruned them); the store keys them by hash, so nothing is stored twice.
  const uploads = new Map();
  const upload = async (file) => {
    if (!uploads.has(file)) uploads.set(file, await stage.upload(path.join(workdir, file)));
    return uploads.get(file);
  };
  const started = Date.now();
  let generated = 0;
  let stopped = false;

  for (const scene of shots) {
    const present = manifest.shots[scene.id];
    if (present && !present.needs_review && !values.force && existsSync(path.join(workdir, present.file))) {
      ctx.stdout.write(`${scene.id}: kept (${present.seconds} s, judge ${present.judge?.overall ?? "?"}/10)\n`);
      continue;
    }
    const characters = cast(scene);
    const neededFrames = framesOf.get(scene.id) ?? 0;
    const seconds = clipSeconds(neededFrames, durations);
    const keyframe = keyframes.shots[scene.id];
    const firstFrame = await upload(keyframe.file);
    const endFrame = keyframe.end_frame?.file ? await upload(keyframe.end_frame.file) : null;
    const references = [];
    for (const character of characters) if (sheets[character.id]) references.push({ sha256: await upload(sheets[character.id].file), role: "character" });
    let continues = null;
    if (scene.data.start_frame?.shot) {
      // The clip before this one is done by now (a shot may only continue an earlier one).
      const previous = manifest.shots[scene.data.start_frame.shot];
      if (!previous?.file) {
        ctx.stderr.write(`${scene.id} continues from ${scene.data.start_frame.shot}, which has no clip yet; run clips for it first\n`);
        return EXIT.usage;
      }
      const frame = `clips/${scene.data.start_frame.shot}-last.png`;
      if (ctx.extractFrame) await ctx.extractFrame(path.join(workdir, previous.file), path.join(workdir, frame));
      else await runTool(tools.ffmpeg, lastFrameArgs(path.join(workdir, previous.file), previous.frames ?? Math.round(previous.seconds * FPS), path.join(workdir, frame)));
      continues = { shot: scene.data.start_frame.shot, file: frame, sha256: await upload(frame) };
      references.push({ sha256: continues.sha256, role: "previous_frame" });
    }
    const refs = references.slice(0, MAX_REFERENCES);
    const prompt = clipPrompt(scene, look);
    const neighbours = shotScenes(doc);
    const at = neighbours.findIndex((each) => each.id === scene.id);
    const rivals = [neighbours[at - 1], neighbours[at + 1]].filter(Boolean).map((each) => keyframes.shots[each.id]?.file).filter(Boolean).map((file) => path.join(workdir, file));
    const entry = present?.takes && !values.force ? present : { takes: [] };
    for (let take = 1; take <= takes; take++) {
      const seed = take;
      if (entry.takes.some((each) => each.seed === seed && each.qc)) continue;
      const key = clipKey({ provider: status.clip.provider, model: status.clip.model, prompt, negative: look.negative, seconds, resolution, seed, startFrame: firstFrame, endFrame, references: refs.map((reference) => reference.sha256) });
      const request = {
        shot_id: scene.id,
        prompt,
        ...(look.negative ? { negative_prompt: look.negative } : {}),
        first_frame: firstFrame,
        ...(endFrame ? { last_frame: endFrame } : {}),
        references: refs,
        seconds,
        ...(resolution ? { resolution } : {}),
        native_audio: false,
        seed,
        idempotency_key: key,
      };
      let clip;
      try {
        clip = await stage.clip({ id: scene.id, key, request, target: `clips/${scene.id}-${seed}` });
      } catch (error) {
        if (error.code === "stopped") {
          stopped = true;
          break;
        }
        if (retakeable(error)) {
          ctx.stdout.write(`${scene.id} seed ${seed}: ${error.message}; trying another seed\n`);
          continue;
        }
        throw error;
      }
      if (!clip.reused) generated += 1;
      const inspected = await inspect(ctx, tools, path.join(workdir, clip.file), { keyframe: path.join(workdir, keyframe.file), rivals, requested: seconds, needed: neededFrames / FPS });
      let judge;
      try {
        const sheetFiles = characters.filter((character) => sheets[character.id]).map((character) => ({ sha256: uploads.get(sheets[character.id].file), label: `sheet ${character.name}` }));
        const ask = (sha256) => stage.judge({ id: scene.id, kind: "clip", files: [{ sha256, label: "clip" }, ...sheetFiles].slice(0, 6), rubric: clipRubric(characters), context: { shot: { id: scene.id, prompt: scene.data.prompt, motion: scene.data.motion ?? null, camera: scene.data.camera ?? null }, characters: characters.map((character) => ({ name: character.name, description: character.appearance })), style: look.style } });
        try {
          judge = await ask(clip.sha256);
        } catch (error) {
          if (error.code !== "video_media_judge_too_large") throw error;
          // Too big to send inline: a 720p proxy goes to the store and is judged instead.
          const proxy = `clips/${scene.id}-${seed}-proxy.mp4`;
          if (ctx.makeProxy) await ctx.makeProxy(path.join(workdir, clip.file), path.join(workdir, proxy));
          else await runTool(tools.ffmpeg, proxyArgs(path.join(workdir, clip.file), path.join(workdir, proxy)));
          judge = await ask(await upload(proxy));
        }
      } catch (error) {
        if (error.code !== "stopped") throw error;
        stopped = true;
        break;
      }
      const verdict = clipVerdict({ ...inspected, requested_s: seconds, needed_s: neededFrames / FPS, judge });
      entry.takes.push({ seed, file: clip.file, sha256: clip.sha256, key, seconds, frames: inspected.probe?.frames ?? null, qc: verdict, judge });
      ctx.stdout.write(`${scene.id} take ${take}: ${verdict.ok ? "passed" : `NOT passed: ${verdict.problems.join("; ")}`} (judge ${judge.overall}/10${clip.reused ? ", reused" : ""})\n`);
      if (verdict.ok) break;
    }
    if (stopped) {
      if (entry.takes.length) manifest.shots[scene.id] = { ...entry, needs_review: true, incomplete: true };
      writeManifest(workdir, doc, manifest);
      break;
    }
    const best = [...entry.takes].reverse().find((each) => each.qc?.ok) ?? entry.takes.at(-1) ?? null;
    if (!best) {
      manifest.shots[scene.id] = { ...entry, needs_review: true, problems: ["no take could be generated"] };
      writeManifest(workdir, doc, manifest);
      continue;
    }
    const record = {
      file: best.file,
      sha256: best.sha256,
      key: best.key,
      seed: best.seed,
      seconds: best.seconds,
      frames: best.frames,
      needed_s: Number((neededFrames / FPS).toFixed(3)),
      first_frame: { file: keyframe.file, sha256: firstFrame },
      ...(endFrame ? { end_frame: { file: keyframe.end_frame.file, sha256: endFrame } } : {}),
      ...(continues ? { continues } : {}),
      qc: best.qc,
      judge: best.judge,
      takes: entry.takes,
      needs_review: !best.qc?.ok,
    };
    if (record.needs_review) record.problems = [...new Set(entry.takes.flatMap((each) => each.qc?.problems ?? []))];
    manifest.shots[scene.id] = record;
    writeManifest(workdir, doc, manifest);
  }
  if (stopped) {
    ctx.stdout.write(`stopped by the STOP file after ${generated} new clips; rerun to continue\n`);
    return EXIT.ok;
  }
  manifest.generated_at = ctx.now().toISOString();
  writeManifest(workdir, doc, manifest);
  const seconds = Math.round((Date.now() - started) / 1000);
  const totals = ledgerTotals(workdir);
  const waiting = Object.entries(manifest.shots).filter(([, shot]) => shot.needs_review);
  recordStage(workdir, "clips", { shots: Object.keys(manifest.shots).length, generated, needs_review: waiting.map(([id]) => id), clip_seconds: totals.clip_seconds, usd: totals.usd, seconds }, ctx.now());
  ctx.stdout.write(`${generated} clips generated in ${seconds} s; ${Object.keys(manifest.shots).length} shots have clips; this video has spent US$${totals.usd.toFixed(2)} (${totals.clip_seconds} clip seconds)\n`);
  if (waiting.length) {
    for (const [id, shot] of waiting) ctx.stdout.write(`ERROR ${id}: no take passed: ${(shot.problems ?? []).join("; ")}\n`);
    ctx.stdout.write(`fix the prompts of ${waiting.map(([id]) => id).join(", ")} and run clips again (needs_review in clips/manifest.json)\n`);
    return EXIT.lint;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs ${doc.music ? "music" : "assemble"} --slug ${doc.slug}\n`);
  return EXIT.ok;
}
