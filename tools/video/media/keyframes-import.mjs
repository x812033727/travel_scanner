// `keyframes import --slug S --shot ID --file PNG|JPG --provider colab|hailuo-web|external [--judge]
// [--credits N] [--usd N] [--note "…"] [--force]`: a picture drawn outside the pipeline (a Colab
// GPU, a web tool) becomes the shot's keyframe (ticket 2026-10-28-keyframes-import-keyframes-manifest-judge).
// The shot passes the gates a drawn keyframe does (lint, the approved look with a sheet chosen
// for every character); the file is copied to keyframes/<shot>-import-<n>.<ext> and written into
// keyframes/manifest.json bound to the current look and script, exactly as `keyframes` binds
// it, so `clips import` takes the clip whose first frame is this picture and the storyboard
// gate goes stale until the owner looks again. Without --judge the picture is the owner's
// choice and is not left needs_review; with --judge the site's judge scores it on the rubric
// `keyframes` uses (one identity question per character, against the chosen sheets) and the
// verdict decides, as for a drawn take. Money (`--usd`) and credits go to the ledger like a
// clip import's (docs/videos/DRAMA.md 外面畫的首格).
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { approvalState, sha256File } from "../core/approvals.mjs";
import { burnIn, drawnShotScenes, hasCast, hasPictures, illustrated, lookHash, picturesHash, resolveLook, shotCast } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, recordStage } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { chosenSheets, fixClauses, keyframeRubric } from "./keyframes.mjs";
import { bookImport, ledgerTotals, release, reserve } from "./ledger.mjs";
import { pictureVerdict } from "./qc.mjs";
import { choiceFor, imageSelectionVersion, imageStatus, mayWriteProject, Stage } from "./stages.mjs";

/** Where an imported keyframe may come from: the Colab GPU route (minimax-h3-colab), a web image tool, anything else. */
export const KEYFRAME_IMPORT_PROVIDERS = ["colab", "hailuo-web", "external"];
/** The smallest picture a keyframe may be: the clip models' first frame and qc.mjs's floor. */
export const MIN_KEYFRAME_WIDTH = 1280;
export const MIN_KEYFRAME_HEIGHT = 720;

/**
 * The pixel size of a PNG or JPEG from its bytes, `{ width, height, ext }`, or null for anything
 * else. PNG: the IHDR chunk right after the signature. JPEG: the first SOF marker's frame header.
 */
export function pictureSize(bytes) {
  if (bytes.length >= 24 && bytes.subarray(0, 8).equals(Buffer.from("\x89PNG\r\n\x1a\n", "binary")) && bytes.subarray(12, 16).toString("latin1") === "IHDR") {
    return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20), ext: "png" };
  }
  if (bytes.length >= 4 && bytes[0] === 0xff && bytes[1] === 0xd8) {
    let at = 2;
    while (at + 9 < bytes.length) {
      if (bytes[at] !== 0xff) return null;
      const marker = bytes[at + 1];
      if (marker === 0xd8 || (marker >= 0xd0 && marker <= 0xd7) || marker === 0x01 || marker === 0xff) { at += marker === 0xff ? 1 : 2; continue; }
      const length = bytes.readUInt16BE(at + 2);
      // SOF0–SOF15 carry the frame size, except the Huffman (C4), arithmetic (C8) and DAC (CC) tables.
      if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
        return { width: bytes.readUInt16BE(at + 7), height: bytes.readUInt16BE(at + 5), ext: "jpg" };
      }
      if (marker === 0xda) return null; // scan data before any frame header: not a picture we can size
      at += 2 + length;
    }
  }
  return null;
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.keyframes);
const writeManifest = (workdir, manifest) => atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);
const importedFrom = (imported) => `${imported.provider}${imported.credits !== null && imported.credits !== undefined ? ` (${imported.credits} credits)` : ""}`;

export async function importKeyframe(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, workdir: { type: "string" }, shot: { type: "string" }, file: { type: "string" }, provider: { type: "string" }, credits: { type: "string" }, usd: { type: "string" }, note: { type: "string" }, judge: { type: "boolean" }, force: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug || !values.shot || !values.file) throw new UsageError("keyframes import needs --slug, --shot and --file (the png or jpg to bring in)");
  if (!KEYFRAME_IMPORT_PROVIDERS.includes(values.provider)) throw new UsageError(`--provider must be one of ${KEYFRAME_IMPORT_PROVIDERS.join(", ")}: where the picture was made`);
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
  const size = pictureSize(readFileSync(origin));
  if (!size) throw new UsageError(`${values.file} is not a PNG or JPEG`);

  const project = loadProject({ slug: values.slug, root: ctx.root });
  const { doc } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!hasPictures(doc)) throw new UsageError("keyframes import is for a drama (format \"drama\") or illustrated slides");
  const scene = drawnShotScenes(doc).find((each) => each.id === values.shot);
  if (!scene) throw new UsageError(`--shot ${values.shot} names no shot of ${doc.slug} with a keyframe of its own`);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const hash = lookHash(doc);
  const slides = illustrated(doc);
  const binding = slides ? { pictures_hash: picturesHash(doc) } : { visual_hash: visualHash(doc) };
  const bound = (manifest) => Boolean(manifest) && Object.entries(binding).every(([key, value]) => manifest[key] === value);

  // The look gate, as `keyframes` wants it: approved as it stands, a sheet chosen for every character.
  let sheets = {};
  if (hasCast(doc)) {
    const lookManifest = readJson(path.join(workdir, ARTIFACTS.characters), null);
    const chosen = lookChosen(lookManifest, readJson(path.join(workdir, ARTIFACTS.characterChoice), null), hash);
    const approval = await approvalState({ gate: "look", docDir: project.dir, workdir });
    if (approval.status !== "approved" || chosen === null) {
      const why = approval.status === "stale" ? "changed since it was approved" : approval.status === "absent" ? "not generated yet (run look)" : chosen === null ? "approved but a character has no chosen sheet" : "not approved yet";
      throw new MediaError(`the look is ${why}: run review-push --gate look and wait for the owner on /admin/videos, then review-pull`, { who: "owner" });
    }
    sheets = chosenSheets(lookManifest, chosen);
  }
  if (!mayWriteProject(ctx, workdir, "keyframes import")) return EXIT.incomplete;

  const sha256 = await sha256File(origin);
  const reservation = usd > 0 ? `import:${scene.id}:${sha256}` : null;
  let stage = null;
  if (reservation || values.judge) {
    const options = clientOptions(ctx, requireCredentials(ctx));
    stage = new Stage({ slug: doc.slug, workdir, options, status: imageStatus(await mediaStatus(options), project.series), stage: "keyframes", imageVersion: imageSelectionVersion(project.series), now: ctx.now });
  }
  if (reservation) {
    stage.spend(usd, "import");
    reserve(workdir, { stage: "keyframes", kind: "image", id: scene.id, provider: values.provider, model: null, key: reservation, seconds: 0, cost_usd: usd }, ctx.now());
  }

  let booked = false;
  try {
  const existing = readJson(manifestFile(workdir), null);
  const current = existing?.look_hash === hash && bound(existing);
  // A fresh manifest carries the fields `keyframes` binds its own to (image_selection_version;
  // the image model when the site was asked), so a later `keyframes` run reads it as its own
  // setup; and `keyframes` keeps imported entries whatever its generator selection.
  const manifest = current ? existing : { look_hash: hash, ...binding, image_selection_version: 1, shots: {} };
  if (stage && !manifest.image) {
    const choice = choiceFor(stage.status, "image", slides ? doc.format : null);
    if (choice) manifest.image = { provider: choice.provider, model: choice.model };
  }
  mkdirSync(path.join(workdir, "keyframes"), { recursive: true });
  // The next free keyframes/<shot>-import-<n>.<ext>, numbered across both extensions; the same
  // bytes brought in again keep their name.
  const taken = async (number) => {
    for (const ext of ["png", "jpg"]) {
      const candidate = path.join(workdir, `keyframes/${scene.id}-import-${number}.${ext}`);
      if (existsSync(candidate)) return (await sha256File(candidate)) === sha256 ? "same" : "other";
    }
    return null;
  };
  let n = 1;
  while ((await taken(n)) === "other") n += 1;
  const file = `keyframes/${scene.id}-import-${n}.${size.ext}`;
  if (!existsSync(path.join(workdir, file))) copyFileSync(origin, path.join(workdir, file));

  const characters = shotCast(doc, scene);
  let judge = null;
  if (values.judge) {
    try {
      const files = [{ sha256: await stage.upload(path.join(workdir, file)), label: "keyframe" }];
      for (const character of characters) if (sheets[character.id]) files.push({ sha256: await stage.upload(path.join(workdir, sheets[character.id].file)), label: `sheet ${character.name}` });
      judge = await stage.judge({
        id: scene.id,
        kind: "keyframe",
        files,
        rubric: keyframeRubric(characters, { subtitleBand: burnIn(doc), craft: slides, plate: false }),
        context: { shot: { id: scene.id, prompt: scene.data.prompt, camera: scene.data.camera ?? null }, characters: characters.map((character) => ({ name: character.name, description: character.appearance })), style: look.style },
      });
    } catch (error) {
      if (error.code !== "stopped") throw error;
      ctx.stdout.write(`stopped by the STOP file before ${scene.id} was judged; nothing was recorded, rerun to continue\n`);
      return EXIT.ok;
    }
  }
  const verdict = pictureVerdict({ width: size.width, height: size.height, judge, min_width: MIN_KEYFRAME_WIDTH, min_height: MIN_KEYFRAME_HEIGHT });
  const forced = !verdict.ok && Boolean(values.force);
  // A picture kept by --force over a failed verdict is recorded as `keyframes --accept-best`
  // records one (accepted_with_problems): what keyframeProblems and pipelineStatus read as the owner's call.
  const imported = { provider: values.provider, credits, imported_at: ctx.now().toISOString(), ...(values.note ? { note: values.note } : {}), ...(forced ? { forced: true, accepted_with_problems: [...verdict.problems] } : {}) };
  const take = { import: n, file, sha256, width: size.width, height: size.height, qc: verdict, judge, ...imported };
  const previous = manifest.shots[scene.id];
  const record = {
    file,
    sha256,
    key: null,
    seed: null,
    width: size.width,
    height: size.height,
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
  writeManifest(workdir, manifest);
  bookImport(workdir, { stage: "keyframes", kind: "image", id: scene.id, provider: values.provider, credits, seconds: 0, cost_usd: usd, file, sha256, ...(reservation ? { key: reservation } : {}) }, ctx.now());
  booked = true;
  const waiting = Object.entries(manifest.shots).filter(([, shot]) => shot.needs_review).map(([id]) => id);
  recordStage(workdir, "keyframes", { shots: Object.keys(manifest.shots).length, imported: Object.values(manifest.shots).filter((shot) => shot.imported_at).length, generated: 0, needs_review: waiting, usd: ledgerTotals(workdir).usd, seconds: 0 }, ctx.now());

  ctx.stdout.write(`${scene.id}: ${file} from ${importedFrom(imported)}${usd ? `, US$${usd.toFixed(2)}` : ""}: ${size.width}x${size.height}, ${judge ? `judge ${judge.overall}/10` : "not judged (--judge asks)"}${previous?.file && previous.file !== file ? `; replaces ${previous.file}` : ""}\n`);
  if (record.needs_review) {
    ctx.stdout.write(`ERROR ${scene.id}: ${verdict.problems.join("; ")}\n`);
    if (record.fixes) ctx.stdout.write(`  fixes for ${scene.id}: ${record.fixes.join("; ")}\n`);
    ctx.stdout.write(`draw ${scene.id} again and import that, or keep this one with --force (needs_review in keyframes/manifest.json)\n`);
    return EXIT.lint;
  }
  if (forced) ctx.stdout.write(`${scene.id}: kept by --force although ${verdict.problems.join("; ")}\n`);
  ctx.stdout.write(`next: node tools/video/cli.mjs review-push --slug ${doc.slug} --gate storyboard (the storyboard changed) or node tools/video/cli.mjs keyframes import for the next shot\n`);
  return EXIT.ok;
  } finally {
    // An import that ends without booking (the STOP file, an upload or judge failure) lets its hold go.
    if (reservation && !booked) release(workdir, reservation);
  }
}
