// `keyframes`: one 1920x1080 picture per shot, generated from the shot's prompt with the chosen
// character sheets as references, scored by the judge and retaken with another seed when it
// fails (docs/videos/DRAMA.md). Needs the look gate approved: the sheets are what keep every
// character the same from shot to shot. A drama with no characters (a narrator-only story,
// docs/videos/STORY.md) has no sheets and no look gate, and its keyframes take the look's style
// frames as their only references. Writes keyframes/manifest.json (the storyboard gate binds to
// it), keyframes/<shot>-<seed>.png and a contact sheet, in pages when there are many shots.
import { existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { approvalState } from "../core/approvals.mjs";
import { burnIn, hasCast, hasPictures, illustrated, isExplainer, lookHash, picturesHash, resolveLook, shotAppearancePrompt, shotCast, shotScenes } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { duplicates } from "./qc.mjs";
import { capFor, choiceFor, drawContactSheet, imagePrice, imageSelectionVersion, imageSizeFor, imageStatus, JUDGE_USD_PER_CALL, pictureHashes, retakeable, sameImage, Stage, statusProblem } from "./stages.mjs";

export const MAX_KEYFRAME_TAKES = 3;
// The server takes at most four reference pictures per image.
export const MAX_REFERENCES = 4;
// Shots per contact sheet page, six rows of four: the ninety shots of a story on one sheet would
// make an image over twenty rows tall, too long to look over and too heavy to send as one file.
export const CONTACT_SHEET_TILES = 24;
const CONTACT_SHEET = /^contact-sheet(?:-\d+)?\.png$/;

/**
 * How a storyboard's tiles are laid over contact sheets: one keyframes/contact-sheet.png while
 * they fit on a page, else pages of at most CONTACT_SHEET_TILES in shot order,
 * keyframes/contact-sheet-01.png, -02.png and so on. Returns [{ file, tiles }].
 */
export function contactSheetPages(tiles, perPage = CONTACT_SHEET_TILES) {
  if (tiles.length <= perPage) return [{ file: "keyframes/contact-sheet.png", tiles }];
  return Array.from({ length: Math.ceil(tiles.length / perPage) }, (_, index) => ({
    file: `keyframes/contact-sheet-${String(index + 1).padStart(2, "0")}.png`,
    tiles: tiles.slice(index * perPage, (index + 1) * perPage),
  }));
}

/**
 * What the judge scores a keyframe on: one identity question per character in the shot, then the
 * picture itself. With no cast the style is judged against the look's description alone and the
 * picture is also judged as craft (does it read as drawn by a hand, not rendered by a machine:
 * docs/videos/ILLUSTRATED.md §畫面不像 AI), and a video whose subtitles are CC only (illustrated
 * slides) has no subtitle band to keep clear.
 */
export function keyframeRubric(characters, { subtitleBand = true } = {}) {
  return [
    ...characters.map((character) => ({
      key: `identity_${character.id.replace(/-/g, "_")}`,
      question: character.shot_look
        ? `Is ${character.name} the same facial identity and recognizable bone structure as the reference sheet, while matching the requested look ${character.shot_look}: ${character.appearance}? The requested clothing, hair and age override the sheet's styling.`
        : `Is ${character.name} in the keyframe the same person as in the reference sheet labelled "${character.name}": face, hair, clothing, build?`,
      weight: 2,
    })),
    { key: "prompt", question: "Does the picture show what the shot prompt describes: subjects, setting, action, framing?", weight: 2 },
    {
      key: "style",
      question: characters.length ? "Is the picture in the requested visual style, consistent with the reference sheets?" : "Is the picture in the requested visual style, as the style description in the context puts it: technique, palette, line, mood?",
      weight: 1,
    },
    ...(characters.length ? [] : [{ key: "craft", question: "Does it read as drawn by a person for print: lines and colour with texture and small irregularities, an asymmetric composition with one focal point and depth, people with simple faces or turned away rather than featureless mannequins, and no glossy, glowing or computer-rendered finish?", weight: 1 }]),
    { key: "clean", question: "Is it free of faults: correct hands and fingers, no warped faces, no floating or duplicated parts, no smeared background?", weight: 2 },
    { key: "no_text", question: "Is it free of text, letters, watermarks and logos?", weight: 1 },
    ...(subtitleBand ? [{ key: "subtitle_band", question: "Is the main subject clear of the bottom 14% of the frame, where subtitles will be burned in?", weight: 1 }] : []),
  ];
}

export function shotPrompt(scene, look, characters) {
  const cast = shotAppearancePrompt(characters);
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
  const imageVersion = imageSelectionVersion(project.series);
  const { doc } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!hasPictures(doc)) throw new UsageError("keyframes is for a drama (format \"drama\") or illustrated slides (still \"shot\" scenes, docs/videos/ILLUSTRATED.md)");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const hash = lookHash(doc);
  // A drama's manifest is bound to the whole picture; illustrated slides bind theirs to the shots
  // alone (id, prompt, camera), so a card's text can change without every picture being judged again.
  const slides = illustrated(doc);
  const binding = slides ? { pictures_hash: picturesHash(doc) } : { visual_hash: visualHash(doc) };
  const bound = (manifest) => manifest && Object.entries(binding).every(([key, value]) => manifest[key] === value);
  const format = slides ? doc.format : null;
  const rubricOptions = { subtitleBand: burnIn(doc) };
  const wanted = values.shot ? new Set(values.shot.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  const shots = shotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  if (!shots.length) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug}`);
  const takes = values.takes ? Number(values.takes) : MAX_KEYFRAME_TAKES;
  if (!Number.isInteger(takes) || takes < 1 || takes > 6) throw new UsageError("--takes must be 1 to 6");
  const cast = (scene) => shotCast(doc, scene);

  // The look must be approved as it stands, with a sheet chosen (or suggested) for every
  // character. A narrator-only drama has no character, so no sheet to wait for.
  let chosen = {};
  let sheets = {};
  if (hasCast(doc)) {
    const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
    chosen = lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash);
    const approval = await approvalState({ gate: "look", docDir: project.dir, workdir });
    if (approval.status !== "approved" || chosen === null) {
      const why = approval.status === "stale" ? "changed since it was approved" : approval.status === "absent" ? "not generated yet (run look)" : chosen === null ? "approved but a character has no chosen sheet" : "not approved yet";
      throw new MediaError(`the look is ${why}: run review-push --gate look and wait for the owner on /admin/videos, then review-pull`, { who: "owner" });
    }
    sheets = chosenSheets(lookManifest, chosen);
  }
  const endFrames = shots.filter((scene) => scene.data.end_frame?.prompt).length;
  // A still that fills the frame under a camera move (illustrated slides, the explainer) is drawn
  // at 2K when the server prices the model at 2K; a drama's keyframes, which become a clip's
  // first frame, stay at the 1K the clip models take.
  const stillPictures = slides || isExplainer(doc);
  const sizeFor = (status) => (stillPictures ? imageSizeFor(status, format) : null);

  if (values["dry-run"]) {
    ctx.stdout.write(`keyframes for ${shots.length} shots (${endFrames} end frames), up to ${takes} takes each\n`);
    for (const scene of shots) ctx.stdout.write(`${scene.id}: ${shotPrompt(scene, look, cast(scene))}\n  references: ${(scene.data.characters ?? []).map((id) => `${id}=${sheets[id] ? optionOf(chosen[id]) : "?"}`).join(", ") || "none"}\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = imageStatus(await mediaStatus(clientOptions(ctx, credentials)), project.series);
      const problem = statusProblem(status, "image", format);
      const choice = choiceFor(status, "image", format);
      const size = sizeFor(status);
      const usd = shots.length * (imagePrice(status, format, size) + JUDGE_USD_PER_CALL) + endFrames * (imagePrice(status, format) + JUDGE_USD_PER_CALL);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${choice.provider} ${choice.model} ${choice.configured === null ? "(provider key checked on submit)" : "ready"}`}; pictures at ${size ?? "1K"}; about US$${usd.toFixed(2)} for one take of everything, up to US$${(usd * takes).toFixed(2)} at ${takes} takes; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${capFor(status, format)} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = imageStatus(await mediaStatus(options), project.series);
  const problem = statusProblem(status, "image", format);
  if (problem) throw new MediaError(problem, { who: "owner" });
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "keyframes", imageVersion, format, now: ctx.now });
  const size = sizeFor(status);
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
  const chosenImage = choiceFor(status, "image", format);
  const manifest = existing?.look_hash === hash && bound(existing) && sameImage(existing.image, chosenImage) && (!imageVersion || existing.image_selection_version === imageVersion) && !values.force ? existing : { look_hash: hash, ...binding, image_selection_version: 1, shots: {} };
  manifest.image = { provider: chosenImage.provider, model: chosenImage.model };
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
        picture = await stage.image({ id: scene.id, purpose: "keyframe", prompt, negative: look.negative, references, seed, shotId: scene.id, size, target: `keyframes/${scene.id}-${seed}` });
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
          rubric: keyframeRubric(characters, rubricOptions),
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
        const end = await stage.image({ id: `${scene.id}/end`, purpose: "keyframe", prompt: shotPrompt({ ...scene, data: { ...scene.data, prompt: scene.data.end_frame.prompt } }, look, characters), negative: look.negative, references, seed: 1, shotId: scene.id, target: `keyframes/${scene.id}-end` });
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
  // contact_sheets lists every page in order; contact_sheet stays the first, for the readers
  // written before there were pages.
  const pages = contactSheetPages(tiles);
  const contactSheets = [];
  for (const [index, page] of pages.entries()) {
    const title = `${doc.slug}：分鏡 ${drawn.length} 鏡${pages.length > 1 ? `（第 ${index + 1}／${pages.length} 頁）` : ""}`;
    const sheet = await drawContactSheet(ctx, { workdir, channel: values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL, title, tiles: page.tiles, file: page.file });
    if (sheet.note) {
      ctx.stdout.write(`${sheet.note}\n`);
      break;
    }
    contactSheets.push(sheet.file);
  }
  // A sheet left by an earlier run with another number of shots shows a storyboard that is gone.
  for (const name of readdirSync(path.join(workdir, "keyframes"))) {
    if (CONTACT_SHEET.test(name) && !contactSheets.includes(`keyframes/${name}`)) rmSync(path.join(workdir, "keyframes", name), { force: true });
  }
  manifest.contact_sheet = contactSheets[0] ?? null;
  manifest.contact_sheets = contactSheets;
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
