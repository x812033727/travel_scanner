// `keyframes`: one 1920x1080 picture per shot, generated from the shot's prompt with the chosen
// character sheets as references, scored by the judge and retaken with another seed when it
// fails (docs/videos/DRAMA.md). Needs the look gate approved: the sheets are what keep every
// character the same from shot to shot. Writes keyframes/manifest.json (the storyboard gate
// binds to it), keyframes/<shot>-<seed>.png and a contact sheet.
import { mkdirSync, existsSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { approvalState } from "../core/approvals.mjs";
import { isDrama, lookHash, resolveLook, shotScenes } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { duplicates } from "./qc.mjs";
import { drawContactSheet, imagePrice, JUDGE_USD_PER_CALL, pictureHashes, retakeable, Stage, statusProblem } from "./stages.mjs";

export const MAX_KEYFRAME_TAKES = 3;
// The server takes at most four reference pictures per image.
export const MAX_REFERENCES = 4;

/** What the judge scores a keyframe on: one identity question per character in the shot, then the picture itself. */
export function keyframeRubric(characters) {
  return [
    ...characters.map((character) => ({
      key: `identity_${character.id.replace(/-/g, "_")}`,
      question: `Is ${character.name} in the keyframe the same person as in the reference sheet labelled "${character.name}": face, hair, clothing, build?`,
      weight: 2,
    })),
    { key: "prompt", question: "Does the picture show what the shot prompt describes: subjects, setting, action, framing?", weight: 2 },
    { key: "style", question: "Is the picture in the requested visual style, consistent with the reference sheets?", weight: 1 },
    { key: "clean", question: "Is it free of faults: correct hands and fingers, no warped faces, no floating or duplicated parts, no smeared background?", weight: 2 },
    { key: "no_text", question: "Is it free of text, letters, watermarks and logos?", weight: 1 },
    { key: "subtitle_band", question: "Is the main subject clear of the bottom 14% of the frame, where subtitles will be burned in?", weight: 1 },
  ];
}

export function shotPrompt(scene, look, characters) {
  const cast = characters.map((character) => `${character.name}: ${character.appearance}`).join("; ");
  return `${scene.data.prompt}. Style: ${look.style}${scene.data.camera ? `. Camera: ${scene.data.camera}` : ""}${cast ? `. Characters: ${cast}` : ""}`.slice(0, 4000);
}

/** The chosen sheet of each character: `{ <id>: { file, sha256 } }`, from the look manifest and the owner's choice. */
export function chosenSheets(manifest, chosen) {
  const sheets = {};
  for (const [id, n] of Object.entries(chosen ?? {})) {
    const candidate = manifest?.characters?.[id]?.candidates?.find((each) => each.n === n);
    if (candidate) sheets[id] = { file: candidate.file, sha256: candidate.sha256 };
  }
  return sheets;
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.keyframes);
const writeManifest = (workdir, manifest) => atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: {
      slug: { type: "string" },
      file: { type: "string" },
      workdir: { type: "string" },
      shot: { type: "string" },
      force: { type: "boolean" },
      "dry-run": { type: "boolean" },
      takes: { type: "string" },
      channel: { type: "string" },
    },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("keyframes needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc)) throw new UsageError("keyframes is for a drama (format \"drama\")");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const hash = lookHash(doc);
  const visual = visualHash(doc);
  const wanted = values.shot ? new Set(values.shot.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  const shots = shotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  if (!shots.length) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug}`);
  const takes = values.takes ? Number(values.takes) : MAX_KEYFRAME_TAKES;
  if (!Number.isInteger(takes) || takes < 1 || takes > 6) throw new UsageError("--takes must be 1 to 6");
  const byId = new Map((doc.characters ?? []).map((character) => [character.id, character]));
  const cast = (scene) => (scene.data.characters ?? []).map((id) => byId.get(id)).filter(Boolean);

  // The look must be approved as it stands, with a sheet chosen (or suggested) for every character.
  const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
  const chosen = lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash);
  const approval = await approvalState({ gate: "look", docDir: project.dir, workdir });
  if (approval.status !== "approved" || chosen === null) {
    const why = approval.status === "stale" ? "changed since it was approved" : approval.status === "absent" ? "not generated yet (run look)" : chosen === null ? "approved but a character has no chosen sheet" : "not approved yet";
    throw new MediaError(`the look is ${why}: run review-push --gate look and wait for the owner on /admin/videos, then review-pull`, { who: "owner" });
  }
  const sheets = chosenSheets(lookManifest, chosen);
  const endFrames = shots.filter((scene) => scene.data.end_frame?.prompt).length;

  if (values["dry-run"]) {
    ctx.stdout.write(`keyframes for ${shots.length} shots (${endFrames} end frames), up to ${takes} takes each\n`);
    for (const scene of shots) ctx.stdout.write(`${scene.id}: ${shotPrompt(scene, look, cast(scene))}\n  references: ${(scene.data.characters ?? []).map((id) => `${id}=${sheets[id] ? optionOf(chosen[id]) : "?"}`).join(", ") || "none"}\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = await mediaStatus(clientOptions(ctx, credentials));
      const problem = statusProblem(status);
      const usd = (shots.length + endFrames) * (imagePrice(status) + JUDGE_USD_PER_CALL);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.image.provider} ${status.image.model} ready`}; about US$${usd.toFixed(2)} for one take of everything; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await mediaStatus(options);
  const problem = statusProblem(status);
  if (problem) throw new MediaError(problem, { who: "owner" });
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "keyframes", now: ctx.now });
  mkdirSync(path.join(workdir, "keyframes"), { recursive: true });
  // The chosen sheets and the style frames go to the media store (the server may have pruned
  // them), once per run, and every keyframe is generated with them as references.
  const uploaded = {};
  for (const [id, sheet] of Object.entries(sheets)) uploaded[id] = await stage.upload(path.join(workdir, sheet.file));
  const styleReferences = [];
  for (const frame of look.style_frames) {
    const file = path.join(project.dir, frame);
    if (!existsSync(file)) throw new UsageError(`look.style_frames: ${frame} is not in ${project.dir}`);
    styleReferences.push({ sha256: await stage.upload(file), role: "style" });
  }
  const existing = readJson(manifestFile(workdir), null);
  const manifest = existing?.look_hash === hash && existing.visual_hash === visual && !values.force ? existing : { look_hash: hash, visual_hash: visual, shots: {} };
  manifest.image = { provider: status.image.provider, model: status.image.model };
  const started = Date.now();
  let generated = 0;
  let stopped = false;

  for (const scene of shots) {
    const characters = cast(scene);
    const current = manifest.shots[scene.id];
    if (current && !current.needs_review && !values.force && existsSync(path.join(workdir, current.file))) {
      ctx.stdout.write(`${scene.id}: kept (judge ${current.judge?.overall ?? "?"}/10)\n`);
      continue;
    }
    const references = [...characters.map((character) => ({ sha256: uploaded[character.id], role: "character" })).filter((reference) => reference.sha256), ...styleReferences].slice(0, MAX_REFERENCES);
    const prompt = shotPrompt(scene, look, characters);
    const entry = current?.takes && !values.force ? current : { takes: [] };
    for (let take = 1; take <= takes; take++) {
      const seed = take;
      if (entry.takes.some((each) => each.seed === seed && each.judge)) continue;
      let picture;
      try {
        picture = await stage.image({ id: scene.id, purpose: "keyframe", prompt, negative: look.negative, references, seed, shotId: scene.id, target: `keyframes/${scene.id}-${seed}` });
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
      if (!picture.reused) generated += 1;
      let judge;
      try {
        judge = await stage.judge({
          id: scene.id,
          kind: "keyframe",
          files: [{ sha256: picture.sha256, label: "keyframe" }, ...characters.filter((character) => uploaded[character.id]).map((character) => ({ sha256: uploaded[character.id], label: `sheet ${character.name}` }))].slice(0, 6),
          rubric: keyframeRubric(characters),
          context: { shot: { id: scene.id, prompt: scene.data.prompt, camera: scene.data.camera ?? null }, characters: characters.map((character) => ({ name: character.name, description: character.appearance })), style: look.style },
        });
      } catch (error) {
        if (error.code !== "stopped") throw error;
        stopped = true;
        break;
      }
      entry.takes.push({ seed, file: picture.file, sha256: picture.sha256, key: picture.key, judge });
      ctx.stdout.write(`${scene.id} take ${take}: judge ${judge.overall}/10${judge.passed ? "" : ` NOT passed: ${judge.problems.join("; ") || "below the bar"}`}${picture.reused ? " (reused)" : ""}\n`);
      if (judge.passed) break;
    }
    if (stopped) {
      // Judged takes are kept for the rerun; a shot with none is simply not drawn yet.
      if (entry.takes.length) manifest.shots[scene.id] = { ...entry, needs_review: true, incomplete: true };
      writeManifest(workdir, manifest);
      break;
    }
    const best = [...entry.takes].reverse().find((each) => each.judge?.passed) ?? entry.takes.at(-1) ?? null;
    if (!best) {
      manifest.shots[scene.id] = { ...entry, needs_review: true, problems: ["no take could be generated"] };
      writeManifest(workdir, manifest);
      continue;
    }
    const record = { file: best.file, sha256: best.sha256, key: best.key, seed: best.seed, judge: best.judge, takes: entry.takes, needs_review: !best.judge?.passed };
    if (record.needs_review) record.problems = [...new Set(entry.takes.flatMap((each) => each.judge?.problems ?? []))];
    // An end frame guides the clip's last picture; it is not judged, only drawn.
    if (scene.data.end_frame?.prompt) {
      try {
        const end = await stage.image({ id: `${scene.id}/end`, purpose: "keyframe", prompt: `${scene.data.end_frame.prompt}. Style: ${look.style}`.slice(0, 4000), negative: look.negative, references, seed: 1, shotId: scene.id, target: `keyframes/${scene.id}-end` });
        if (!end.reused) generated += 1;
        record.end_frame = { file: end.file, sha256: end.sha256, key: end.key };
      } catch (error) {
        if (error.code === "stopped") {
          stopped = true;
          manifest.shots[scene.id] = { ...record, needs_review: true, incomplete: true };
          writeManifest(workdir, manifest);
          break;
        }
        throw error;
      }
    }
    manifest.shots[scene.id] = record;
    writeManifest(workdir, manifest);
  }
  if (stopped) {
    ctx.stdout.write(`stopped by the STOP file after ${generated} new keyframes; rerun to continue\n`);
    return EXIT.ok;
  }

  // Two neighbouring shots that look the same read as a video that stalled; the writer fixes the prompt.
  const drawn = shotScenes(doc).map((scene) => manifest.shots[scene.id] && { id: scene.id, file: manifest.shots[scene.id].file }).filter(Boolean);
  const hashes = await pictureHashes(ctx, workdir, drawn);
  manifest.duplicates = hashes ? duplicates(hashes) : [];
  for (const pair of manifest.duplicates) ctx.stdout.write(`WARN shots ${pair.a} and ${pair.b} look alike (dHash distance ${pair.distance}); vary the prompt or the camera\n`);
  const thumbnailShot = doc.thumbnail?.data?.shot;
  manifest.thumbnail_source = thumbnailShot && manifest.shots[thumbnailShot] ? manifest.shots[thumbnailShot].file : null;
  const tiles = drawn.map((shot) => ({ file: shot.file, label: `${shot.id} · ${manifest.shots[shot.id].judge?.overall ?? "?"}/10${manifest.shots[shot.id].needs_review ? " · 待修" : ""}` }));
  const sheet = await drawContactSheet(ctx, { workdir, channel: values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL, title: `${doc.slug}：分鏡 ${drawn.length} 鏡`, tiles, file: "keyframes/contact-sheet.png" });
  if (sheet.note) ctx.stdout.write(`${sheet.note}\n`);
  manifest.contact_sheet = sheet.file;
  manifest.generated_at = ctx.now().toISOString();
  writeManifest(workdir, manifest);
  const seconds = Math.round((Date.now() - started) / 1000);
  const waiting = Object.entries(manifest.shots).filter(([, shot]) => shot.needs_review);
  recordStage(workdir, "keyframes", { shots: Object.keys(manifest.shots).length, generated, needs_review: waiting.map(([id]) => id), duplicates: manifest.duplicates.length, usd: ledgerTotals(workdir).usd, seconds }, ctx.now());
  ctx.stdout.write(`${generated} keyframes generated in ${seconds} s; ${Object.keys(manifest.shots).length} shots drawn; this video has spent US$${ledgerTotals(workdir).usd.toFixed(2)}\n`);
  if (waiting.length) {
    for (const [id, shot] of waiting) ctx.stdout.write(`ERROR ${id}: no take passed the judge: ${(shot.problems ?? []).join("; ")}\n`);
    ctx.stdout.write(`fix the prompts of ${waiting.map(([id]) => id).join(", ")} and run keyframes again (needs_review in keyframes/manifest.json)\n`);
    return EXIT.lint;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs review-push --slug ${doc.slug} --gate storyboard\n`);
  return EXIT.ok;
}

const optionOf = (n) => String.fromCharCode(64 + n);
