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
import { burnIn, drawnShotScenes, hasCast, hasPictures, illustrated, isExplainer, lookHash, picturesHash, resolveLook, shotAppearancePrompt, shotCast, shotScenes } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { mediaKey } from "./cache.mjs";
import { duplicates } from "./qc.mjs";
import { capFor, choiceFor, drawContactSheet, imagePrice, imageSelectionVersion, imageSizeFor, imageStatus, JUDGE_USD_PER_CALL, pictureHashes, retakeable, sameImage, Stage, statusProblem } from "./stages.mjs";
import { trimMargins } from "./trim.mjs";

export const MAX_KEYFRAME_TAKES = 3;
// The server takes at most four reference pictures per image.
export const MAX_REFERENCES = 4;
// Illustrated slides draw one style plate per video first (docs/videos/ILLUSTRATED.md §第二輪):
// a neutral scene in the look, judged like a shot, then sent with every shot as a style
// reference so the pictures read as one illustrator's set rather than as sixty separate rolls of
// the same dice. The plate is bound to the look alone (keyframes/plate.json carries look_hash),
// so a prompt edit redraws that shot and nothing else; a new look draws a new plate, and with
// it every picture. The scene is chosen to show the hand on what the videos ask for most: a
// place, two people doing something, a few materials, daylight.
export const STYLE_PLATE_PROMPT = "Medium shot of a quiet street corner in a small town in the late afternoon, a woman in a raincoat locking a bicycle to a lamp post beside a greengrocer's crates of oranges and leeks, an old man on the doorstep feeding a tabby cat, a delivery scooter passing behind, brick, glass, wet pavement and a plain canvas awning with no lettering, warm low sun from the left, the picture running past all four edges of the frame";
export const STYLE_PLATE_ID = "style-plate";
export const PLATE_FILE = path.join("keyframes", "plate.json");
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
 * picture itself. With no cast the style is judged against the look's description alone, and a
 * video whose subtitles are CC only (illustrated slides) has no subtitle band to keep clear.
 * `craft` adds the question illustrated slides are held to (does it read as drawn by a hand, not
 * rendered by a machine: docs/videos/ILLUSTRATED.md §畫面不像 AI). It is the caller's word about
 * the video, never inferred from a shot having no characters: an empty establishing shot of a
 * 3D drama must not be judged as a print illustration, and the explainer's look allows the
 * faceless figures this question marks down. `plate` says the judge was also sent the video's
 * style plate (labelled "style plate"), and the style is then judged against it, as a drama's
 * is against its sheets. `clean` also refuses a picture that does not fill the frame: a tall
 * subject sometimes comes back as a vertical picture between blurred bars.
 */
export function keyframeRubric(characters, { subtitleBand = true, craft = false, plate = false } = {}) {
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
      question: characters.length
        ? "Is the picture in the requested visual style, consistent with the reference sheets?"
        : plate
          ? "Is the picture in the same technique, line, palette, texture and finish as the picture labelled \"style plate\", as if by the same hand on the same paper, and in the style the context describes?"
          : "Is the picture in the requested visual style, as the style description in the context puts it: technique, palette, line, mood?",
      weight: 1,
    },
    ...(!craft ? [] : [{ key: "craft", question: "Does it read as made by a person for print, not generated: marks of the medium (grain, brush, ink or print texture) and small irregularities, no even outline traced around everything, no uniform fine detail everywhere, an asymmetric composition with one focal point and depth, people with simple faces or turned away, and no glossy, airbrushed, glowing or rendered finish?", weight: 1 }]),
    { key: "clean", question: "Is it free of faults: correct hands and fingers, no warped faces, no floating or duplicated parts, no smeared background, and one picture filling the whole frame with no bars, borders, margins or blurred side panels?", weight: 2 },
    { key: "no_text", question: "Is it free of text, letters, watermarks and logos?", weight: 1 },
    ...(subtitleBand ? [{ key: "subtitle_band", question: "Is the main subject clear of the bottom 14% of the frame, where subtitles will be burned in?", weight: 1 }] : []),
  ];
}

/**
 * What the judge is asked about an illustrated-slides picture when the server takes fault checks
 * (`limits.judge_checks`): one concrete fault a question, answered yes or no, and the server
 * computes the scores. Asked for a score from 0 to 10 the judge gives a picture it has no remark
 * on a 7 and never goes higher, wherever the scale is explained to it, so the owner's bar of 7
 * passed only the takes it said nothing about and the same picture flipped when asked twice
 * (docs/videos/ILLUSTRATED.md §judge 的刻度與判定沿用). `cost` is what a fault takes off its
 * criterion's 10. The first six cost all of it: the criterion falls under the server's floor of
 * 4 and the picture is redrawn whatever the rest scores; their small weight only keeps the
 * overall of such a take from reading as good. The last three are flaws a viewer may notice on
 * a second look, and they carry the overall: at a bar of 7 a picture passes with one of them
 * beside a missed detail and fails when it is both awkward and generated-looking; at 8 an
 * awkward body fails, at 9 only a missed detail is let through, at 10 nothing is. `plate` says
 * the judge is also shown the video's style plate. The questions are the ones measured on the
 * 163 recorded takes; a reworded one has to be measured again.
 */
export function keyframeChecks({ plate = false } = {}) {
  const redraw = { weight: 0.25, cost: 10 };
  return [
    { key: "text", question: "Can you read any letter, word or number anywhere in the picture, or see a logo or a watermark? Marks that only suggest writing without forming letters do not count.", ...redraw },
    { key: "anatomy", question: "Count the digits of every hand drawn large, thumb included. Does any hand show more than five, or does any person or animal have an extra hand, arm or leg, or a face or body warped out of shape? A finger that is hidden or left out by the style does not count.", ...redraw },
    { key: "detached", question: "Is any part floating, cut off from what should hold it or duplicated, or is there a stray figure or object that does not belong to the scene (a tiny person, a hand with no arm, eyes in the dark)?", ...redraw },
    { key: "subject", question: "Is the main subject of the shot prompt, or the main thing it is doing, missing or clearly wrong? Secondary props, bystanders, which hand and the exact framing do not count here.", ...redraw },
    { key: "frame", question: "Does the picture fail to fill the frame as one upright picture: bars or blurred panels at the sides, the scene tilted, blank paper or a table showing past its corners, or the scene drawn as a photograph of a print? A thin plain margin does not count.", ...redraw },
    { key: "style", question: plate ? "Is the technique clearly unlike the picture labelled \"style plate\": another medium, another palette or another finish?" : "Is the technique clearly unlike the style the context describes: another medium, another palette or another finish?", ...redraw },
    { key: "details", question: "Is a secondary thing the shot prompt asks for missing or different: a prop, a bystander, a gesture, the shot size?", weight: 2, cost: 3 },
    { key: "awkward", question: "Is a hand, a face or a body awkward enough that a viewer would notice it on a second look, beyond the way the style simplifies everything?", weight: 3, cost: 6 },
    { key: "generated", question: "Does it read as generated rather than printed by hand: an even outline traced around everything, the same fine detail everywhere, a glossy, airbrushed or glowing finish?", weight: 2, cost: 6 },
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

/**
 * The take a shot keeps: the latest that passed, else the one the judge scored highest (the
 * earlier seed on a tie), so a shot waiting for a prompt fix shows its best picture on the
 * contact sheet and to whoever rewrites the prompt, not whichever seed happened to come last.
 */
export function bestTake(takes) {
  return [...takes].reverse().find((each) => each.judge?.passed) ?? takes.reduce((best, each) => ((each.judge?.overall ?? -1) > (best?.judge?.overall ?? -1) ? each : best), null);
}

/**
 * Whether a shot's entry from a manifest bound to other pictures still stands: every take was
 * asked for exactly as it would be asked for now (`keys.take(seed)`, the image cache key: prompt,
 * camera, style, cast, references, model, size), its end frame too, and judged on the question
 * the judge would be asked now (`stamp`: rubric, context, the owner's bar). A verdict from before
 * takes carried a stamp stands only on a shot that passed.
 */
export function entryStands(entry, { keys, stamp }) {
  const takes = entry?.takes ?? [];
  if (!takes.length || !takes.every((take) => take.judge && take.key === keys.take(take.seed))) return false;
  if ((entry.end_frame?.key ?? null) !== keys.end) return false;
  return takes.every((take) => take.judged === stamp || (take.judged === undefined && !entry.needs_review));
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.keyframes);
const writeManifest = (workdir, manifest) => atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);

/** The style plate of a video whose look is `hash`, as keyframes/plate.json records it, or null. */
export function readStylePlate(workdir, hash) {
  const plate = readJson(path.join(workdir, PLATE_FILE), null);
  return plate?.look_hash === hash && plate.file && existsSync(path.join(workdir, plate.file)) ? plate : null;
}

/**
 * Draw the video's style plate, or keep the one its look already has: STYLE_PLATE_PROMPT in the
 * look, up to `takes` seeds until the judge passes one, the best take kept either way (a plate
 * that fails on a detail still shows the hand, and no shot can be drawn without one). Returns
 * the plate record, or null when the STOP file ended the run.
 */
/**
 * A still that fills the frame (illustrated slides, the explainer) with its paper margin cut
 * off (trim.mjs): the trimmed copy's file and sha stand in for the picture's in the manifest,
 * the judge having seen the picture as it came. Returns the picture, trimmed or not.
 */
async function trimmed(ctx, workdir, picture, id) {
  const cut = await trimMargins(ctx, workdir, picture.file);
  if (!cut) return picture;
  const widest = Math.max(...Object.values(cut.margins));
  ctx.stdout.write(`${id}: trimmed a ${widest}% paper margin\n`);
  return { ...picture, file: cut.file, sha256: cut.sha256, margins: cut.margins };
}

async function stylePlate({ stage, workdir, look, hash, takes, size, rubric, force, trim, ctx }) {
  const kept = force ? null : readStylePlate(workdir, hash);
  if (kept) {
    ctx.stdout.write(`style plate: kept (judge ${kept.judge?.overall ?? "?"}/10)\n`);
    return kept;
  }
  const prompt = `${STYLE_PLATE_PROMPT}. Style: ${look.style}`.slice(0, 4000);
  const taken = [];
  let generated = 0;
  for (let take = 1; take <= takes; take++) {
    let picture;
    try {
      picture = await stage.image({ id: STYLE_PLATE_ID, purpose: "style_frame", prompt, negative: look.negative, references: [], seed: take, shotId: STYLE_PLATE_ID, size, target: `keyframes/plate-${take}` });
      if (!picture.reused) generated += 1;
    } catch (error) {
      if (error.code === "stopped") return null;
      if (retakeable(error)) {
        ctx.stdout.write(`style plate seed ${take}: ${error.message}; trying another seed\n`);
        continue;
      }
      throw error;
    }
    let judge;
    try {
      judge = await stage.judge({ id: STYLE_PLATE_ID, kind: "keyframe", files: [{ sha256: picture.sha256, label: "keyframe" }], rubric, context: { shot: { id: STYLE_PLATE_ID, prompt: STYLE_PLATE_PROMPT, camera: null }, characters: [], style: look.style } });
    } catch (error) {
      if (error.code === "stopped") return null;
      throw error;
    }
    // The plate goes to every shot as its reference, so a margin on it would be copied: cut it off.
    if (trim) picture = await trimmed(ctx, workdir, picture, STYLE_PLATE_ID);
    taken.push({ seed: take, file: picture.file, sha256: picture.sha256, key: picture.key, judge, ...(picture.margins ? { margins: picture.margins } : {}) });
    ctx.stdout.write(`style plate take ${take}: judge ${judge.overall}/10${judge.passed ? "" : ` NOT passed: ${judge.problems.join("; ") || "below the bar"}`}${picture.reused ? " (reused)" : ""}\n`);
    if (judge.passed) break;
  }
  if (!taken.length) throw new MediaError("the style plate could not be drawn; every seed was refused", { code: "video_media_rejected" });
  const best = bestTake(taken);
  const record = { look_hash: hash, file: best.file, sha256: best.sha256, key: best.key, seed: best.seed, judge: best.judge, takes: taken, drawn_at: ctx.now().toISOString() };
  atomicWrite(path.join(workdir, PLATE_FILE), `${JSON.stringify(record, null, 2)}\n`);
  return { ...record, generated };
}

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
  const rubricOptions = { subtitleBand: burnIn(doc), craft: slides };
  const wanted = values.shot ? new Set(values.shot.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  // A shot cut from another shot's clip (data.source) shows that clip, so it has no keyframe to draw.
  const shots = drawnShotScenes(doc).filter((scene) => !wanted || wanted.has(scene.id));
  if (!shots.length) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug} with a keyframe of its own`);
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
  // Illustrated slides draw from a style plate unless the owner gave the look its own frames.
  const plated = slides && !look.style_frames.length;

  if (values["dry-run"]) {
    ctx.stdout.write(`keyframes for ${shots.length} shots (${endFrames} end frames), up to ${takes} takes each${plated ? `, after one style plate${readStylePlate(workdir, hash) ? " (already drawn)" : ""}` : ""}\n`);
    for (const scene of shots) ctx.stdout.write(`${scene.id}: ${shotPrompt(scene, look, cast(scene))}\n  references: ${[...(scene.data.characters ?? []).map((id) => `${id}=${sheets[id] ? optionOf(chosen[id]) : "?"}`), ...(plated ? ["style plate"] : [])].join(", ") || "none"}\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = imageStatus(await mediaStatus(clientOptions(ctx, credentials)), project.series);
      const problem = statusProblem(status, "image", format);
      const choice = choiceFor(status, "image", format);
      const size = sizeFor(status);
      const plates = plated && !readStylePlate(workdir, hash) ? 1 : 0;
      const usd = (shots.length + plates) * (imagePrice(status, format, size) + JUDGE_USD_PER_CALL) + endFrames * (imagePrice(status, format) + JUDGE_USD_PER_CALL);
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
  // Illustrated slides are judged by yes/no fault checks once the server takes them; a drama's
  // pictures, and any picture on an older server, are scored on the rubric as before.
  const checks = slides && Boolean(status.limits?.judge_checks);
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
  const started = Date.now();
  let generated = 0;
  let stopped = false;
  // The style plate comes first and goes last in every shot's references (the server tells the
  // model the last reference is the plate); it is put in the store again in case it was pruned.
  let plate = null;
  if (plated) {
    plate = await stylePlate({ stage, workdir, look, hash, takes, size, rubric: checks ? keyframeChecks() : keyframeRubric([], rubricOptions), force: values.force, trim: stillPictures, ctx });
    if (!plate) {
      ctx.stdout.write("stopped by the STOP file before the style plate; rerun to continue\n");
      return EXIT.ok;
    }
    generated += plate.generated ?? 0;
    await stage.upload(path.join(workdir, plate.file));
    styleReferences.push({ sha256: plate.sha256, role: "style" });
  }
  const existing = readJson(manifestFile(workdir), null);
  const chosenImage = choiceFor(status, "image", format);
  const sameSetup = existing?.look_hash === hash && sameImage(existing.image, chosenImage) && (!imageVersion || existing.image_selection_version === imageVersion) && !values.force;
  const manifest = sameSetup && bound(existing) ? existing : { look_hash: hash, ...binding, image_selection_version: 1, shots: {} };
  manifest.image = { provider: chosenImage.provider, model: chosenImage.model };
  if (plate) manifest.plate = { file: plate.file, sha256: plate.sha256, seed: plate.seed, judge: plate.judge };
  else delete manifest.plate;

  // What a shot is drawn from and what the judge is asked about it, as they stand now.
  const referencesOf = (characters) => [...characters.map((character) => ({ sha256: uploaded[character.id], role: "character" })).filter((reference) => reference.sha256), ...styleReferences].slice(-MAX_REFERENCES);
  const endPrompt = (scene, characters) => shotPrompt({ ...scene, data: { ...scene.data, prompt: scene.data.end_frame.prompt } }, look, characters);
  const question = (scene, characters) => ({
    rubric: checks ? keyframeChecks({ plate: Boolean(plate) }) : keyframeRubric(characters, { ...rubricOptions, plate: Boolean(plate) }),
    context: { shot: { id: scene.id, prompt: scene.data.prompt, camera: scene.data.camera ?? null }, characters: characters.map((character) => ({ name: character.name, description: character.appearance })), style: look.style },
  });
  // A verdict answers one question at the owner's bar of the day; a take judged on another has no verdict yet.
  const stampOf = (asked) => mediaKey("keyframe-judge", { ...asked, bar: status.judge_min_score ?? null });
  // Only the binding moved (another shot's prompt or camera; on a drama, a card): a shot whose own
  // requests are what they were keeps its takes and their verdicts. Judging the same picture again
  // costs a call a take and, worse, flips verdicts: on 2026-10-04 one prompt edit sent 74 cached
  // pictures back to the judge and five that had passed failed with nothing changed.
  if (sameSetup && !bound(existing)) {
    for (const scene of drawnShotScenes(doc)) {
      const characters = cast(scene);
      const references = referencesOf(characters);
      const prompt = shotPrompt(scene, look, characters);
      const keys = {
        take: (seed) => stage.imageKey({ prompt, negative: look.negative, references, seed, size }),
        end: scene.data.end_frame?.prompt ? stage.imageKey({ prompt: endPrompt(scene, characters), negative: look.negative, references, seed: 1 }) : null,
      };
      if (entryStands(existing.shots?.[scene.id], { keys, stamp: stampOf(question(scene, characters)) })) manifest.shots[scene.id] = existing.shots[scene.id];
    }
    ctx.stdout.write(`${Object.keys(manifest.shots).length} of ${Object.keys(existing.shots ?? {}).length} drawn shots are unchanged and keep their verdicts\n`);
  }

  for (const scene of shots) {
    const characters = cast(scene);
    const current = manifest.shots[scene.id];
    if (current && !current.needs_review && !values.force && existsSync(path.join(workdir, current.file))) {
      ctx.stdout.write(`${scene.id}: kept (judge ${current.judge?.overall ?? "?"}/10)\n`);
      continue;
    }
    const references = referencesOf(characters);
    const prompt = shotPrompt(scene, look, characters);
    const asked = question(scene, characters);
    const judged = stampOf(asked);
    const entry = current?.takes && !values.force ? current : { takes: [] };
    for (let take = 1; take <= takes; take++) {
      const seed = take;
      // A take judged on this question is not asked about again. One judged on another question
      // is, from its cached picture; a take from before verdicts were stamped is of another
      // question only where the question is now the checks.
      if (entry.takes.some((each) => each.seed === seed && each.judge && (each.judged === judged || (each.judged === undefined && !checks)))) continue;
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
          files: [{ sha256: picture.sha256, label: "keyframe" }, ...characters.filter((character) => uploaded[character.id]).map((character) => ({ sha256: uploaded[character.id], label: `sheet ${character.name}` })), ...(plate ? [{ sha256: plate.sha256, label: "style plate" }] : [])].slice(0, 6),
          ...asked,
        });
      } catch (error) {
        if (error.code !== "stopped") throw error;
        stopped = true;
        break;
      }
      // A still under a camera move is used without its paper margin; the judge saw it whole.
      if (stillPictures) picture = await trimmed(ctx, workdir, picture, scene.id);
      entry.takes = [...entry.takes.filter((each) => each.seed !== seed), { seed, file: picture.file, sha256: picture.sha256, key: picture.key, judge, judged, ...(picture.margins ? { margins: picture.margins } : {}) }].sort((a, b) => a.seed - b.seed);
      ctx.stdout.write(`${scene.id} take ${take}: judge ${judge.overall}/10${judge.passed ? "" : ` NOT passed: ${judge.problems.join("; ") || "below the bar"}`}${picture.reused ? " (reused)" : ""}\n`);
      if (judge.passed) break;
    }
    if (stopped) {
      // Judged takes are kept for the rerun; a shot with none is simply not drawn yet.
      if (entry.takes.length) manifest.shots[scene.id] = { ...entry, needs_review: true, incomplete: true };
      writeManifest(workdir, manifest);
      break;
    }
    const best = bestTake(entry.takes);
    if (!best) {
      manifest.shots[scene.id] = { ...entry, needs_review: true, problems: ["no take could be generated"] };
      writeManifest(workdir, manifest);
      continue;
    }
    const record = { file: best.file, sha256: best.sha256, key: best.key, seed: best.seed, judge: best.judge, takes: entry.takes, needs_review: !best.judge?.passed, ...(best.margins ? { margins: best.margins } : {}) };
    if (record.needs_review) record.problems = [...new Set(entry.takes.flatMap((each) => each.judge?.problems ?? []))];
    // An end frame guides the clip's last picture; it is not judged, only drawn.
    if (scene.data.end_frame?.prompt) {
      try {
        const end = await stage.image({ id: `${scene.id}/end`, purpose: "keyframe", prompt: endPrompt(scene, characters), negative: look.negative, references, seed: 1, shotId: scene.id, target: `keyframes/${scene.id}-end` });
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
