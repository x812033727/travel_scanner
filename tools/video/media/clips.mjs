// `clips`: one motion clip per shot, generated from the shot's keyframe with the chosen sheets
// as references, checked by ffmpeg and the judge, retaken with another seed, and the judge's
// fixes in the prompt, when it fails (docs/videos/DRAMA.md). The most expensive stage, so it
// runs after the look, the narration, the keyframes and the storyboard have been approved, and
// every submission is checked against the per-video cap first. Writes clips/manifest.json (what
// assemble reads) and clips/<shot>-<seed>.mp4.
//
// A shot marked visual "still" (docs/videos/BINGE.md) buys no clip: assemble animates its
// keyframe instead. It still gets a manifest entry naming that keyframe and its hash, so the
// manifest covers every shot, its clips_hash moves when a keyframe is redrawn, and status and
// assemble read one file for the whole picture track. A shot cut from another shot's clip
// (data.source, docs/videos/DRAMA.md) buys nothing either: its entry names that clip and the
// frame the cut starts at, and the ledger records what the cut saved.
//
// `clips import` brings in a clip made outside the pipeline (a Hailuo web plan, Kling's MCP):
// the same gates and ffmpeg checks as a bought take, the judge when asked, a manifest entry
// that names its route, and a ledger entry with what the route charged.
import { execFile } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { approvalState, sha256File } from "../core/approvals.mjs";
import { clipKey, clipShotScenes, clipsHash, isDrama, isSourced, lookHash, resolveLook, shotAppearancePrompt, shotCast, shotScenes, sourcedShotScenes, stillShotScenes } from "../core/drama.mjs";
import { productionClipProblems, productionClipSizeProblem, productionShotProblems } from "../core/lint.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, keyframeProblems, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { FPS, speechHash, visualHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { chosenSheets, fixClauses, fixesBefore, retakePrompt } from "./keyframes.mjs";
import { bookImport, bookReuse, ledgerTotals, release, reserve } from "./ledger.mjs";
import { blackdetectArgs, clipVerdict, framePsnrArgs, freezedetectArgs, parseBlackdetect, parseFreezedetect, parseProbe, parsePsnr, parseSceneCuts, probeArgs, sceneCutArgs } from "./qc.mjs";
import { chosenModel, clipSecondPrice, JUDGE_USD_PER_CALL, mayWriteProject, retakeable, Stage, statusProblem } from "./stages.mjs";

const exec = promisify(execFile);

export const MAX_CLIP_TAKES = 2;
export const MIN_CLIP_SECONDS = 4;
export const MAX_CLIP_SECONDS = 10;
export const MAX_REFERENCES = 4;
// Where an imported clip was made: the Hailuo web plan, Kling's MCP, or anything else.
export const IMPORT_PROVIDERS = ["hailuo-web", "kling-mcp", "external"];

const ordinaryIdentityQuestion = (character) => `In the clip's last frame, is ${character.name} still the same person as in the reference sheet labelled "${character.name}": face, hair, clothing, build?`;
const sheetLabelNeedsId = (character) => `sheet ${character.name}`.length > 80;
const identityNeedsContext = (character) => Boolean(character.shot_look) || sheetLabelNeedsId(character) || ordinaryIdentityQuestion(character).length > 400;

/** What the judge scores a clip on: each character in its last frame, then the motion itself. */
export function clipRubric(characters) {
  return [
    ...characters.map((character) => ({
      key: `identity_${character.id.replace(/-/g, "_")}`,
      question: character.shot_look
        ? `Throughout the clip, does character ${character.id} keep the reference sheet's facial identity and recognizable bone structure while following the full requested appearance for look ${character.shot_look} in context? Its clothing, hair and age override the sheet's styling; no morphing back to the base outfit.`
        : identityNeedsContext(character)
          ? `In the clip's last frame, is character ${character.id} still the same person as in the reference sheet matched by the full name in context: face, hair, clothing, build?`
          : ordinaryIdentityQuestion(character),
      weight: 2,
    })),
    { key: "motion", question: "Is the motion natural and continuous: no morphing, no flicker, no limbs or objects drifting or changing shape?", weight: 2 },
    { key: "prompt", question: "Does the clip show the motion and the camera move that were asked for?", weight: 1 },
    { key: "clean", question: "Are hands, faces and bodies correct throughout, with nothing appearing or vanishing?", weight: 2 },
    { key: "no_text", question: "Is the clip free of text, letters, watermarks and logos?", weight: 1 },
  ];
}

/** Whole seconds to ask for: the lines' length rounded up, 4 to 10, at a duration the model offers. */
export function clipSeconds(neededFrames, durations = [], { model = "", resolution = null } = {}) {
  // Veo 3.1 offers 1080p only at eight seconds, including Lite. Do not submit a
  // rounded four/six-second request which the vendor must reject after queueing.
  if (/^veo-?3\.1/.test(model) && resolution === "1080p") return 8;
  const need = Math.max(MIN_CLIP_SECONDS, Math.min(MAX_CLIP_SECONDS, Math.ceil(neededFrames / FPS)));
  const allowed = [...durations].filter((each) => Number.isInteger(each)).sort((a, b) => a - b);
  if (!allowed.length) return need;
  return allowed.find((each) => each >= need) ?? allowed.at(-1);
}

export function clipPrompt(scene, look, characters = []) {
  const variants = characters.filter((character) => character.shot_look);
  return [scene.data?.motion, scene.data?.camera, look.motion, variants.length ? shotAppearancePrompt(variants) : null].filter(Boolean).join(". ").slice(0, 4000);
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

/** What a character's sheet is called when it goes to the judge: its name, or its id when the name is too long for a label. */
const sheetLabel = (character) => `sheet ${sheetLabelNeedsId(character) ? character.id : character.name}`;

/** The judge's verdict on a clip in the media store; one too large to send inline is judged from a 720p proxy. */
async function judgeClip({ ctx, tools, stage, workdir, scene, look, characters, sheetFiles, clip, proxy, upload }) {
  const ask = (sha256) => stage.judge({ id: scene.id, kind: "clip", files: [{ sha256, label: "clip" }, ...sheetFiles].slice(0, 6), rubric: clipRubric(characters), context: { shot: { id: scene.id, prompt: scene.data.prompt, motion: scene.data.motion ?? null, camera: scene.data.camera ?? null }, characters: characters.map((character) => ({ ...(identityNeedsContext(character) ? { id: character.id } : {}), ...(character.shot_look ? { shot_look: character.shot_look } : {}), name: character.name, description: character.appearance })), style: look.style } });
  try {
    return await ask(clip.sha256);
  } catch (error) {
    if (error.code !== "video_media_judge_too_large") throw error;
    if (ctx.makeProxy) await ctx.makeProxy(path.join(workdir, clip.file), path.join(workdir, proxy));
    else await runTool(tools.ffmpeg, proxyArgs(path.join(workdir, clip.file), path.join(workdir, proxy)));
    return ask(await upload(proxy));
  }
}

/** The manifest entry of a shot cut from `origin`, another shot's clip; `problems` say why it cannot be cut there. */
function cutRecord(origin, { shot, from_s }, neededFrames) {
  const fromFrame = Math.round(from_s * FPS);
  const have = origin.frames ?? Math.round((origin.seconds ?? 0) * FPS);
  const problems = [];
  if (origin.still || origin.source || origin.needs_review) problems.push(`${shot}'s clip did not pass its checks; fix ${shot} and run clips again`);
  else if (fromFrame + neededFrames > have) problems.push(`${shot}'s clip runs ${(have / FPS).toFixed(1)} s; a cut starting at ${from_s} s needs ${(neededFrames / FPS).toFixed(1)} s: start earlier or shorten the lines`);
  const record = { source: { shot, from_s, from_frame: fromFrame }, file: origin.file, sha256: origin.sha256, seconds: origin.seconds ?? null, frames: origin.frames ?? null, needed_s: Number((neededFrames / FPS).toFixed(3)), needs_review: problems.length > 0 };
  if (problems.length) record.problems = problems;
  return record;
}

/** "hailuo-web, pro, 96 credits": where an imported clip came from and what it was charged. */
const importedFrom = (shot) => [shot.provider, shot.plan, shot.credits === null || shot.credits === undefined ? null : `${shot.credits} credits`].filter(Boolean).join(", ");

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.clips);

function writeManifest(workdir, doc, manifest) {
  const order = shotScenes(doc).filter((scene) => manifest.shots[scene.id]?.sha256).map((scene) => ({ id: scene.id, sha256: manifest.shots[scene.id].sha256 }));
  manifest.clips_hash = clipsHash(order);
  atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);
}

// What keyframeProblems says about a selected file's bytes or presence (not its review state).
const PICTURE_PROBLEM = /selected picture (has changed|is missing)|has no selected picture/;

/**
 * The selected start (and end) pictures of these scenes whose bytes are not the ones the keyframes
 * manifest recorded, or that are missing: core/state.mjs keyframeProblems on those scenes alone,
 * and any end frame the manifest records, which a clip is sent with whether or not the script
 * still asks for one.
 */
async function changedPictures(doc, keyframes, workdir, scenes) {
  const ids = new Set(scenes.map((scene) => scene.id));
  const problems = (await keyframeProblems({ doc: { ...doc, scenes: doc.scenes.filter((scene) => ids.has(scene.id)) }, manifest: keyframes, workdir, allowNeedsReview: true }))
    .filter((problem) => PICTURE_PROBLEM.test(problem));
  for (const scene of scenes) {
    const end = keyframes.shots?.[scene.id]?.end_frame;
    if (!end?.file || scene.data?.end_frame?.prompt) continue;
    const file = path.resolve(workdir, end.file);
    if (!existsSync(file) || await sha256File(file) !== end.sha256) problems.push(`${scene.id} end frame selected picture has changed: ${end.file}`);
  }
  return problems;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  if (args[0] === "import") return importClip(args.slice(1), ctx);
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
  const productionTiming = productionShotProblems(doc, project.series, timeline);
  if (productionTiming.length) throw new MediaError(`measured production timeline needs a script revision: ${productionTiming.map((problem) => `${problem.path}: ${problem.message}`).join("; ")}`, { who: "owner" });
  const keyframes = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
  if (!keyframes || keyframes.look_hash !== hash || keyframes.visual_hash !== visual) {
    ctx.stderr.write("keyframes/manifest.json is missing or was drawn for an older script or look; run keyframes first\n");
    return EXIT.usage;
  }
  const wanted = values.shot ? new Set(values.shot.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  const shots = clipShotScenes(doc).filter((scene) => !isSourced(scene) && (!wanted || wanted.has(scene.id)));
  const stills = stillShotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  // Cuts from another shot's clip: nothing to draw or buy, recorded once the source clip is done.
  const cuts = sourcedShotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  if (!shots.length && !stills.length && !cuts.length) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug}`);
  // A still is its keyframe, so it needs a passed one as much as a clip does.
  const undrawn = [...shots, ...stills].filter((scene) => !keyframes.shots?.[scene.id]?.file || keyframes.shots[scene.id].needs_review);
  if (undrawn.length) {
    ctx.stderr.write(`shots ${undrawn.map((scene) => scene.id).join(", ")} have no passed keyframe; run keyframes first\n`);
    return EXIT.usage;
  }
  const storyboard = await approvalState({ gate: "storyboard", docDir: project.dir, workdir });
  if (storyboard.status !== "approved") {
    const why = storyboard.status === "stale" ? "changed since it was approved" : "not approved yet";
    throw new MediaError(`the storyboard is ${why}: run review-push --gate storyboard, let the owner (or the auto-approve setting) decide on /admin/videos, then review-pull`, { who: "owner" });
  }
  // The approval is of the manifest; a later keyframes run may have drawn over a selected file
  // name since. The start and end pictures this run uses are checked byte for byte before
  // anything is asked of the site.
  const changed = await changedPictures(doc, keyframes, workdir, [...shots, ...stills]);
  if (changed.length) {
    ctx.stderr.write(`${changed.join("; ")}; run keyframes again or restore the approved pictures\n`);
    return EXIT.usage;
  }
  const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
  const sheets = chosenSheets(lookManifest, lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash) ?? {});
  const cast = (scene) => shotCast(doc, scene);
  const framesOf = new Map(timeline.scenes.map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const takes = values.takes ? Number(values.takes) : MAX_CLIP_TAKES;
  if (!Number.isInteger(takes) || takes < 1 || takes > 5) throw new UsageError("--takes must be 1 to 5");

  if (values["dry-run"]) {
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    const status = credentials.token ? await mediaStatus(clientOptions(ctx, credentials)) : null;
    const durations = status ? (chosenModel(status, "clip")?.durations ?? []) : [];
    const price = status ? clipSecondPrice(status) : 0;
    // A clip brought in by `clips import` stays (unless --force buys the shot again), so it is not priced.
    const existing = readJson(manifestFile(workdir), null);
    const kept = !values.force && existing?.speech_hash === speech && existing.visual_hash === visual && existing.look_hash === hash ? existing.shots ?? {} : {};
    const imported = shots.filter((scene) => kept[scene.id]?.imported_at && !kept[scene.id].needs_review);
    const priced = shots.length - imported.length;
    let total = 0;
    let saved = 0;
    for (const scene of shotScenes(doc)) {
      if (!shots.includes(scene) && !stills.includes(scene) && !cuts.includes(scene)) continue;
      const lines = ((framesOf.get(scene.id) ?? 0) / FPS).toFixed(1);
      if (stills.includes(scene)) {
        ctx.stdout.write(`${scene.id}: ${lines} s of lines → still, its keyframe under a camera move (no clip to buy)\n`);
        continue;
      }
      if (imported.includes(scene)) {
        ctx.stdout.write(`${scene.id}: ${lines} s of lines → imported (${importedFrom(kept[scene.id])}; no clip to buy)\n`);
        continue;
      }
      const seconds = clipSeconds(framesOf.get(scene.id) ?? 0, durations, status?.clip);
      if (cuts.includes(scene)) {
        saved += seconds;
        ctx.stdout.write(`${scene.id}: ${lines} s of lines → cut from ${scene.data.source.shot}'s clip at ${scene.data.source.from_s} s (no clip to buy; ${seconds} clip seconds not bought)\n`);
        continue;
      }
      total += seconds;
      ctx.stdout.write(`${scene.id}: ${lines} s of lines → ${seconds} s clip${status ? ` ≈ US$${(seconds * price).toFixed(2)}` : ""}; ${clipPrompt(scene, look, cast(scene))}\n`);
    }
    ctx.stdout.write(`${shots.length + stills.length + cuts.length} shots: ${stills.length} stills (animated keyframes, nothing to buy)${cuts.length ? `, ${cuts.length} cuts from another shot's clip (nothing to buy, ${saved} clip seconds saved)` : ""}${imported.length ? `, ${imported.length} imported from outside the pipeline (nothing to buy)` : ""} and ${priced} clips priced, ${total} clip seconds for one take each\n`);
    if (status) {
      const problem = statusProblem(status, "clip");
      const budget = status.budgets?.clip_seconds;
      const totals = ledgerTotals(workdir);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.clip.provider} ${status.clip.model} ${status.clip.resolution} ready`}; about US$${(total * price + priced * JUDGE_USD_PER_CALL).toFixed(2)}${budget ? `; ${budget.remaining} of ${budget.limit} clip seconds left this month` : ""}; this video so far US$${totals.usd.toFixed(2)}${totals.reserved > 0 ? ` (US$${totals.reserved.toFixed(2)} of it reserved for ${totals.reservations} request${totals.reservations === 1 ? "" : "s"} not yet reconciled)` : ""} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  const production = project.series?.production;
  if (production?.profile?.video?.model === "veo-3.1-lite-generate-preview") {
    const sceneConstraint = production.episode?.video_constraints;
    if (sceneConstraint?.veo_lite_i2v === "unverified-minor-on-screen") {
      throw new MediaError(`Veo Lite image-to-video only supports allow_adult; this episode includes an unverified minor on screen: ${sceneConstraint.reason || "see the approved production direction"}. Ask the owner to choose a supported animation route before generating; preserve the approved ages`, { who: "owner" });
    }
    const underage = new Map((production.characters ?? [])
      .filter((character) => Number.isFinite(character.video_constraints?.min_visual_age_years)
        && character.video_constraints.min_visual_age_years < 18)
      .map((character) => [character.id, character.video_constraints.min_visual_age_years]));
    const blocked = shotScenes(doc).flatMap((scene) => (scene.data?.characters ?? [])
      .filter((id) => underage.has(id)).map((id) => `${scene.id}/${id} (${underage.get(id)})`));
    if (blocked.length) {
      throw new MediaError(`Veo Lite image-to-video only supports allow_adult; these visual characters are not verified for this provider: ${blocked.join(", ")}. Ask the owner to choose a supported animation route before generating; preserve the approved ages`, { who: "owner" });
    }
  }

  if (!mayWriteProject(ctx, workdir, "clips")) return EXIT.incomplete;
  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await mediaStatus(options);
  const problem = statusProblem(status, "clip");
  if (problem) throw new MediaError(problem, { who: "owner" });
  const requiredVideo = project.series?.production?.profile?.video;
  if (requiredVideo && (status.clip.model !== requiredVideo.model || status.clip.resolution !== requiredVideo.resolution || (requiredVideo.provider && status.clip.provider !== requiredVideo.provider))) {
    throw new MediaError(`the approved production profile requires ${requiredVideo.provider ?? ""} ${requiredVideo.model} at ${requiredVideo.resolution}; the server selects ${status.clip.provider} ${status.clip.model} at ${status.clip.resolution}. Ask the owner to align the media settings before generating clips`, { who: "owner" });
  }
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
  const modelCurrent = !project.series?.production?.profile || ["provider", "model", "resolution"].every((key) => (existing?.clip?.[key] ?? null) === (status.clip[key] ?? null));
  const current = existing?.speech_hash === speech && existing.visual_hash === visual && existing.look_hash === hash && modelCurrent && !values.force;
  const manifest = current ? existing : { speech_hash: speech, visual_hash: visual, look_hash: hash, shots: {} };
  manifest.clip = { provider: status.clip.provider, model: status.clip.model, resolution };
  // The keyframes and the chosen sheets go back to the media store once per run (the server may
  // have pruned them); the store keys them by hash, so nothing is stored twice.
  const uploads = new Map();
  const upload = async (file) => {
    if (!uploads.has(file)) uploads.set(file, await stage.upload(path.join(workdir, file)));
    return uploads.get(file);
  };
  // A picture a clip request carries (its start and end keyframes, the still it continues from)
  // is hashed right before it goes to the store, against the record that names it: a shot outside
  // --shot, or a file drawn over since the early check, cannot slip into a paid request.
  const uploadApproved = async (file, sha256, label) => {
    const local = path.join(workdir, file);
    if (!existsSync(local)) throw new UsageError(`${label} selected picture is missing: ${file}; run keyframes again or restore the approved picture`);
    const changed = () => new UsageError(`${label} selected picture has changed: ${file}; run keyframes again or restore the approved picture`);
    if (typeof sha256 !== "string" || await sha256File(local) !== sha256) throw changed();
    // The store answers with the hash of what it took: a file drawn over between the two reads is caught too.
    if (await upload(file) !== sha256) throw changed();
    return sha256;
  };
  const started = Date.now();
  let generated = 0;
  let stopped = false;

  // The stills first: they cost nothing, and a clip continuing from one (start_frame) reads its
  // entry below. Each names the keyframe assemble will animate, so a redrawn keyframe changes
  // the clips_hash and the video is assembled again.
  for (const scene of stills) {
    const keyframe = keyframes.shots[scene.id];
    manifest.shots[scene.id] = { still: true, file: keyframe.file, sha256: keyframe.sha256 };
  }
  if (stills.length) writeManifest(workdir, doc, manifest);

  for (const scene of shots) {
    const present = manifest.shots[scene.id];
    const cachedProblem = present && !present.needs_review
      ? productionClipProblems(doc, project.series, timeline, manifest).find((problem) => problem.path === `clips.${scene.id}`)
      : null;
    if (cachedProblem) {
      throw new MediaError(`cached clip ${scene.id}: ${cachedProblem.message}; revise or explicitly regenerate it before production can continue`, { who: "owner" });
    }
    if (present && !present.needs_review && !values.force && existsSync(path.join(workdir, present.file))) {
      ctx.stdout.write(`${scene.id}: kept (${present.imported_at ? `imported from ${present.provider}, ` : ""}${present.seconds} s, judge ${present.judge?.overall ?? "?"}/10)\n`);
      continue;
    }
    const characters = cast(scene);
    const neededFrames = framesOf.get(scene.id) ?? 0;
    const seconds = clipSeconds(neededFrames, durations, status.clip);
    const keyframe = keyframes.shots[scene.id];
    const firstFrame = await uploadApproved(keyframe.file, keyframe.sha256, scene.id);
    const endFrame = keyframe.end_frame?.file ? await uploadApproved(keyframe.end_frame.file, keyframe.end_frame.sha256, `${scene.id} end frame`) : null;
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
      if (previous.still) {
        // A still ends on its keyframe under a slight camera move, so the keyframe itself is
        // the picture this clip continues from; there is no clip to take a last frame of. Its
        // record here may be from an earlier run (a still outside --shot), and the approval is of
        // the keyframes manifest, which a later keyframes run may have pointed at another picture.
        const label = `${scene.data.start_frame.shot} (the still ${scene.id} continues from)`;
        const approved = keyframes.shots?.[scene.data.start_frame.shot];
        if (approved?.file !== previous.file || approved?.sha256 !== previous.sha256) {
          throw new UsageError(`${label} is ${previous.file} in clips/manifest.json, but the approved keyframes select ${approved?.file ?? "no picture"}; run clips --shot ${scene.data.start_frame.shot} first`);
        }
        continues = { shot: scene.data.start_frame.shot, file: previous.file, sha256: await uploadApproved(previous.file, previous.sha256, label) };
      } else {
        const frame = `clips/${scene.data.start_frame.shot}-last.png`;
        if (ctx.extractFrame) await ctx.extractFrame(path.join(workdir, previous.file), path.join(workdir, frame));
        else await runTool(tools.ffmpeg, lastFrameArgs(path.join(workdir, previous.file), previous.frames ?? Math.round(previous.seconds * FPS), path.join(workdir, frame)));
        continues = { shot: scene.data.start_frame.shot, file: frame, sha256: await upload(frame) };
      }
      references.push({ sha256: continues.sha256, role: "previous_frame" });
    }
    // A model the catalog gives 0 reference images (Lite; H3, none beside a first frame) gets none: the server
    // refuses them. Keep the sheets for judging below; the approved first frame already carries the face.
    const refs = model?.reference_images === 0 || /^veo-?3\.1-lite/.test(status.clip.model) ? [] : references.slice(0, MAX_REFERENCES);
    const prompt = clipPrompt(scene, look, characters);
    const neighbours = shotScenes(doc);
    const at = neighbours.findIndex((each) => each.id === scene.id);
    const rivals = [neighbours[at - 1], neighbours[at + 1]].filter(Boolean).map((each) => keyframes.shots[each.id]?.file).filter(Boolean).map((file) => path.join(workdir, file));
    const entry = present?.takes && !values.force ? present : { takes: [] };
    // What the provider said each time it refused a seed: when it refuses them all, that is the
    // problem the prompt fix starts from (a prompt too long for the model, say).
    const refusals = [];
    for (let take = 1; take <= takes; take++) {
      const seed = take;
      if (entry.takes.some((each) => each.seed === seed && each.qc)) continue;
      // The judge's fixes for the takes before this one go into its prompt.
      const fixes = fixesBefore(entry.takes, seed);
      if (fixes.length) ctx.stdout.write(`${scene.id} take ${take}: asked with the corrections of the takes before: ${fixes.join("; ")}\n`);
      const asked = retakePrompt(prompt, fixes);
      const key = clipKey({ provider: status.clip.provider, model: status.clip.model, prompt: asked, negative: look.negative, seconds, resolution, seed, startFrame: firstFrame, endFrame, references: refs.map((reference) => reference.sha256) });
      const request = {
        shot_id: scene.id,
        prompt: asked,
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
          refusals.push(error.message.startsWith(`${scene.id}: `) ? error.message.slice(scene.id.length + 2) : error.message);
          continue;
        }
        throw error;
      }
      if (!clip.reused) generated += 1;
      const inspected = await inspect(ctx, tools, path.join(workdir, clip.file), { keyframe: path.join(workdir, keyframe.file), rivals, requested: seconds, needed: neededFrames / FPS });
      let judge;
      try {
        const sheetFiles = characters.filter((character) => sheets[character.id]).map((character) => ({ sha256: uploads.get(sheets[character.id].file), label: sheetLabel(character) }));
        judge = await judgeClip({ ctx, tools, stage, workdir, scene, look, characters, sheetFiles, clip, proxy: `clips/${scene.id}-${seed}-proxy.mp4`, upload });
      } catch (error) {
        if (error.code !== "stopped") throw error;
        stopped = true;
        break;
      }
      const verdict = clipVerdict({ ...inspected, requested_s: seconds, needed_s: neededFrames / FPS, judge });
      const sizeProblem = productionClipSizeProblem(project.series, inspected.probe);
      if (sizeProblem) {
        verdict.ok = false;
        verdict.problems.push(sizeProblem);
      }
      if (project.series?.production?.profile && Math.round((inspected.probe?.duration ?? 0) * FPS) < neededFrames) {
        verdict.ok = false;
        verdict.problems.push("the production profile requires motion for the whole shot; this take would need padding or slowing to cover its dialogue");
      }
      entry.takes.push({ seed, file: clip.file, sha256: clip.sha256, key, seconds, frames: inspected.probe?.frames ?? null, ...(fixes.length ? { fixes } : {}), qc: verdict, judge });
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
      // Every seed was refused. The entry has no clip: nothing of an earlier record is carried
      // over, or the clips hash, a cut or a shot continuing from this one would read its file.
      const why = [...new Set(refusals)].map((reason) => `no take could be generated: ${reason}`);
      manifest.shots[scene.id] = { takes: [], needs_review: true, problems: why.length ? why : ["no take could be generated"] };
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
    if (record.needs_review) {
      // Every check and judge problem of every take, and the judge's fixes among them.
      record.problems = [...new Set(entry.takes.flatMap((each) => each.qc?.problems ?? []))];
      const fixes = fixClauses(entry.takes.flatMap((each) => each.judge?.problems ?? []));
      if (fixes.length) record.fixes = fixes;
    }
    manifest.shots[scene.id] = record;
    writeManifest(workdir, doc, manifest);
  }
  if (stopped) {
    ctx.stdout.write(`stopped by the STOP file after ${generated} new clips; rerun to continue\n`);
    return EXIT.ok;
  }

  // Cuts from another shot's clip: nothing is bought. The source clip is done by now (a shot
  // may only cut from an earlier one); its entry is copied with the frame the cut starts at,
  // once it has passed and runs long enough, and the ledger records what the cut saved.
  let savedSeconds = 0;
  for (const scene of cuts) {
    const { shot, from_s } = scene.data.source;
    const origin = manifest.shots[shot];
    if (!origin?.file) {
      ctx.stderr.write(`${scene.id} is cut from ${shot}, which has no clip yet; run clips for it first\n`);
      return EXIT.usage;
    }
    const neededFrames = framesOf.get(scene.id) ?? 0;
    const record = cutRecord(origin, scene.data.source, neededFrames);
    if (!record.needs_review) {
      const notBought = clipSeconds(neededFrames, durations, status.clip);
      savedSeconds += notBought;
      bookReuse(workdir, { stage: "clips", id: scene.id, provider: status.clip.provider, model: status.clip.model, source: { shot, from_s }, saved_seconds: notBought, saved_usd: Number((notBought * clipSecondPrice(status)).toFixed(4)) }, ctx.now());
      ctx.stdout.write(`${scene.id}: cut from ${shot}'s clip at ${from_s} s (${notBought} clip seconds not bought)\n`);
    }
    manifest.shots[scene.id] = record;
  }

  manifest.generated_at = ctx.now().toISOString();
  writeManifest(workdir, doc, manifest);
  const seconds = Math.round((Date.now() - started) / 1000);
  const totals = ledgerTotals(workdir);
  const waiting = Object.entries(manifest.shots).filter(([, shot]) => shot.needs_review);
  const stillCount = Object.values(manifest.shots).filter((shot) => shot.still).length;
  const cutCount = Object.values(manifest.shots).filter((shot) => shot.source).length;
  const importCount = Object.values(manifest.shots).filter((shot) => shot.imported_at).length;
  recordStage(workdir, "clips", { shots: Object.keys(manifest.shots).length, stills: stillCount, ...(cutCount ? { cuts: cutCount, saved_clip_seconds: savedSeconds } : {}), ...(importCount ? { imported: importCount } : {}), generated, needs_review: waiting.map(([id]) => id), clip_seconds: totals.clip_seconds, usd: totals.usd, seconds }, ctx.now());
  ctx.stdout.write(`${generated} clips generated in ${seconds} s; ${Object.keys(manifest.shots).length} shots in the manifest (${stillCount} stills${cutCount ? `, ${cutCount} cuts from another shot's clip, ${savedSeconds} clip seconds not bought` : ""}${importCount ? `, ${importCount} imported from outside the pipeline` : ""}); this video has spent US$${totals.usd.toFixed(2)} (${totals.clip_seconds} clip seconds)\n`);
  if (waiting.length) {
    // A shot with neither a clip nor a take was refused outright: its problems say so themselves.
    for (const [id, shot] of waiting) {
      ctx.stdout.write(`ERROR ${id}: ${shot.file || shot.takes?.length ? "no take passed: " : ""}${(shot.problems ?? []).join("; ")}\n`);
      if (shot.fixes?.length) ctx.stdout.write(`  fixes for ${id}: ${shot.fixes.join("; ")}\n`);
    }
    ctx.stdout.write(`fix the prompts of ${waiting.map(([id]) => id).join(", ")} and run clips again (needs_review in clips/manifest.json)\n`);
    return EXIT.lint;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs ${doc.music ? "music" : "assemble"} --slug ${doc.slug}\n`);
  return EXIT.ok;
}

/**
 * `clips import --slug S --shot ID --file MP4 --provider hailuo-web|kling-mcp|external`: a clip
 * made outside the pipeline becomes the shot's clip. The shot passes the gates a bought clip
 * does (a current timeline, a passed keyframe, an approved storyboard); the file is copied to
 * clips/<shot>-import-<n>.mp4 and checked like a bought take, by ffmpeg and, with --judge, by
 * the judge. A clip that fails is left needs_review like a failed take, unless --force keeps it.
 */
async function importClip(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, workdir: { type: "string" }, shot: { type: "string" }, file: { type: "string" }, provider: { type: "string" }, plan: { type: "string" }, credits: { type: "string" }, usd: { type: "string" }, note: { type: "string" }, judge: { type: "boolean" }, force: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug || !values.shot || !values.file) throw new UsageError("clips import needs --slug, --shot and --file (the mp4 to bring in)");
  if (!IMPORT_PROVIDERS.includes(values.provider)) throw new UsageError(`--provider must be one of ${IMPORT_PROVIDERS.join(", ")}: where the clip was made`);
  const amount = (flag) => {
    if (values[flag] === undefined) return null;
    const value = Number(values[flag]);
    if (!Number.isFinite(value) || value < 0) throw new UsageError(`--${flag} must be a number, zero or more`);
    return value;
  };
  const credits = amount("credits");
  const usd = amount("usd") ?? 0;
  const origin = path.resolve(values.file);
  if (!existsSync(origin)) throw new UsageError(`${values.file} does not exist`);
  const project = loadProject({ slug: values.slug, root: ctx.root });
  const { doc, lexicon } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc)) throw new UsageError("clips is for a drama (format \"drama\")");
  // A production profile names the one model its clips are bought with, and status and assemble
  // hold the manifest to it (productionClipProblems): another route is the owner's to allow.
  if (project.series?.production?.profile) throw new MediaError(`${doc.slug} has an approved production profile, which accepts only clips bought with its own model; a clip made elsewhere needs the owner to allow that route in the profile first`, { who: "owner" });
  const scene = shotScenes(doc).find((each) => each.id === values.shot);
  if (!scene) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug}`);
  if (isSourced(scene)) throw new UsageError(`${scene.id} is cut from ${scene.data.source.shot}'s clip; import a clip for ${scene.data.source.shot} instead`);
  if (!clipShotScenes(doc).includes(scene)) throw new UsageError(`${scene.id} is a still: assemble animates its keyframe, so there is no clip to import`);
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
  const keyframe = keyframes.shots?.[scene.id];
  if (!keyframe?.file || keyframe.needs_review) {
    ctx.stderr.write(`shot ${scene.id} has no passed keyframe; run keyframes first (the clip must start on it)\n`);
    return EXIT.usage;
  }
  const storyboard = await approvalState({ gate: "storyboard", docDir: project.dir, workdir });
  if (storyboard.status !== "approved") {
    const why = storyboard.status === "stale" ? "changed since it was approved" : "not approved yet";
    throw new MediaError(`the storyboard is ${why}: run review-push --gate storyboard, let the owner (or the auto-approve setting) decide on /admin/videos, then review-pull`, { who: "owner" });
  }
  // Money first, as for a bought take: the dollars --usd prices the credits at, and with --judge
  // the judge's own call, count against the per-video cap. Both need the site's cap, so an import
  // that costs nothing and asks no judge never calls the site. The dollars are held in the ledger
  // under the import's key while the clip is checked, and the booking replaces the hold; an
  // import that ends without booking (a missing ffmpeg, the STOP file, a failed check) lets it go.
  const changed = await changedPictures(doc, keyframes, workdir, [scene]);
  if (changed.length) {
    ctx.stderr.write(`${changed.join("; ")}; run keyframes again or restore the approved picture (the clip must start on it)\n`);
    return EXIT.usage;
  }
  if (!mayWriteProject(ctx, workdir, "clips import")) return EXIT.incomplete;
  const sha256 = await sha256File(origin);
  const reservation = usd > 0 ? `import:${scene.id}:${sha256}` : null;
  let stage = null;
  if (reservation || values.judge) {
    const options = clientOptions(ctx, requireCredentials(ctx));
    stage = new Stage({ slug: doc.slug, workdir, options, status: await mediaStatus(options), stage: "clips", now: ctx.now });
  }
  if (reservation) {
    stage.spend(usd, "import");
    reserve(workdir, { stage: "clips", kind: "clip", id: scene.id, provider: values.provider, plan: values.plan ?? null, credits, key: reservation, seconds: 0, cost_usd: usd }, ctx.now());
  }
  let booked = false;
  try {
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
    const started = Date.now();
    const existing = readJson(manifestFile(workdir), null);
    const current = existing?.speech_hash === speech && existing.visual_hash === visual && existing.look_hash === hash;
    const manifest = current ? existing : { speech_hash: speech, visual_hash: visual, look_hash: hash, shots: {} };
    mkdirSync(path.join(workdir, "clips"), { recursive: true });
    // The next free clips/<shot>-import-<n>.mp4; the same bytes brought in again keep their name.
    let n = 1;
    let file = `clips/${scene.id}-import-${n}.mp4`;
    while (existsSync(path.join(workdir, file)) && (await sha256File(path.join(workdir, file))) !== sha256) file = `clips/${scene.id}-import-${++n}.mp4`;
    if (!existsSync(path.join(workdir, file))) copyFileSync(origin, path.join(workdir, file));

    const framesOf = new Map(timeline.scenes.map((each) => [each.id, each.end_frame - each.start_frame]));
    const neededFrames = framesOf.get(scene.id) ?? 0;
    const neighbours = shotScenes(doc);
    const at = neighbours.findIndex((each) => each.id === scene.id);
    const rivals = [neighbours[at - 1], neighbours[at + 1]].filter(Boolean).map((each) => keyframes.shots[each.id]?.file).filter(Boolean).map((each) => path.join(workdir, each));
    // Nothing was asked of a server, so there is no requested length to hold the clip to.
    const inspected = await inspect(ctx, tools, path.join(workdir, file), { keyframe: path.join(workdir, keyframe.file), rivals, requested: null, needed: neededFrames / FPS });
    let judge = null;
    if (values.judge) {
      const upload = (each) => stage.upload(path.join(workdir, each));
      const characters = shotCast(doc, scene);
      const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
      const sheets = chosenSheets(lookManifest, lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash) ?? {});
      try {
        const sheetFiles = [];
        for (const character of characters) if (sheets[character.id]) sheetFiles.push({ sha256: await upload(sheets[character.id].file), label: sheetLabel(character) });
        judge = await judgeClip({ ctx, tools, stage, workdir, scene, look, characters, sheetFiles, clip: { file, sha256: await upload(file) }, proxy: `clips/${scene.id}-import-${n}-proxy.mp4`, upload });
      } catch (error) {
        if (error.code !== "stopped") throw error;
        ctx.stdout.write(`stopped by the STOP file before ${scene.id} was judged; nothing was recorded, rerun to continue\n`);
        return EXIT.ok;
      }
    }
    const verdict = clipVerdict({ ...inspected, requested_s: null, needed_s: neededFrames / FPS, judge });
    const forced = !verdict.ok && Boolean(values.force);
    const seconds = Math.max(1, Math.round(inspected.probe?.duration ?? 0));
    const imported = { provider: values.provider, plan: values.plan ?? null, credits, imported_at: ctx.now().toISOString(), ...(values.note ? { note: values.note } : {}), ...(forced ? { forced: true } : {}) };
    const take = { import: n, file, sha256, seconds, frames: inspected.probe?.frames ?? null, qc: verdict, judge, ...imported };
    const previous = manifest.shots[scene.id];
    const record = {
      file,
      sha256,
      seconds,
      frames: take.frames,
      needed_s: Number((neededFrames / FPS).toFixed(3)),
      first_frame: { file: keyframe.file, sha256: keyframe.sha256 },
      qc: verdict,
      judge,
      takes: [...(previous?.takes ?? []).filter((each) => each.sha256 !== sha256), take],
      needs_review: !verdict.ok && !forced,
      ...imported,
    };
    if (record.needs_review) {
      record.problems = verdict.problems;
      const fixes = fixClauses(judge?.problems ?? []);
      if (fixes.length) record.fixes = fixes;
    }
    manifest.shots[scene.id] = record;
    // Shots cut from this shot's clip play the new file from now on.
    const recut = sourcedShotScenes(doc).filter((each) => each.data.source.shot === scene.id && manifest.shots[each.id]);
    for (const each of recut) manifest.shots[each.id] = cutRecord(record, each.data.source, framesOf.get(each.id) ?? 0);
    writeManifest(workdir, doc, manifest);
    const totals = bookImport(workdir, { stage: "clips", id: scene.id, provider: values.provider, plan: values.plan ?? null, credits, seconds, cost_usd: usd, file, sha256, ...(reservation ? { key: reservation } : {}) }, ctx.now());
    booked = true;
    const waiting = Object.entries(manifest.shots).filter(([, shot]) => shot.needs_review).map(([id]) => id);
    recordStage(workdir, "clips", { shots: Object.keys(manifest.shots).length, imported: Object.values(manifest.shots).filter((shot) => shot.imported_at).length, generated: 0, needs_review: waiting, clip_seconds: totals.clip_seconds, usd: totals.usd, seconds: Math.round((Date.now() - started) / 1000) }, ctx.now());

    const probe = inspected.probe ?? {};
    ctx.stdout.write(`${scene.id}: ${file} from ${importedFrom(imported)}${usd ? `, US$${usd.toFixed(2)}` : ""}: ${Number(probe.duration ?? 0).toFixed(1)} s for ${(neededFrames / FPS).toFixed(1)} s of lines, ${probe.width}x${probe.height}, ${judge ? `judge ${judge.overall}/10` : "not judged (--judge asks)"}${previous?.file && previous.file !== file ? `; replaces ${previous.file}` : ""}\n`);
    if (Math.round((probe.duration ?? 0) * FPS) < neededFrames) ctx.stdout.write(`${scene.id}: the clip is shorter than its lines; assemble slows it and holds its last frame for the rest, and refuses a long hold unless the shot's fit says "freeze"\n`);
    if (record.needs_review) {
      ctx.stdout.write(`ERROR ${scene.id}: ${verdict.problems.join("; ")}\n`);
      if (record.fixes) ctx.stdout.write(`  fixes for ${scene.id}: ${record.fixes.join("; ")}\n`);
      ctx.stdout.write(`make ${scene.id} again from its keyframe (${keyframe.file}) and import that, or keep this one with --force (needs_review in clips/manifest.json)\n`);
      return EXIT.lint;
    }
    if (forced) ctx.stdout.write(`${scene.id}: kept by --force although ${verdict.problems.join("; ")}\n`);
    if (recut.length) ctx.stdout.write(`${recut.map((each) => each.id).join(", ")}: cut from ${scene.id}'s clip, now from the imported one\n`);
    // A cut the imported clip is too short for is left for a fix, as `clips` leaves it.
    const short = recut.filter((each) => manifest.shots[each.id].needs_review);
    for (const each of short) ctx.stdout.write(`ERROR ${each.id}: ${manifest.shots[each.id].problems.join("; ")}\n`);
    if (short.length) return EXIT.lint;
    ctx.stdout.write(`next: node tools/video/cli.mjs status --slug ${doc.slug}\n`);
    return EXIT.ok;
  } finally {
    // Nothing booked means nothing to count: the hold goes, whatever ended the import.
    if (reservation && !booked) release(workdir, reservation);
  }
}
