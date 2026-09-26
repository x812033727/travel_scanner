// `look`: a few candidate character sheets per character, scored by the judge, for the owner to
// pick from on /admin/videos (docs/videos/DRAMA.md). The chosen sheet is the reference every
// keyframe of that character is generated from, which is what keeps a character the same from
// shot to shot. Writes characters/manifest.json (the look gate binds to it), one PNG per
// candidate under characters/<id>/, and a contact sheet.
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { isDrama, lookHash, resolveLook } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { drawContactSheet, imagePrice, JUDGE_USD_PER_CALL, retakeable, Stage, statusProblem } from "./stages.mjs";

export const MAX_LOOK_ROUNDS = 2;
export const DEFAULT_SHEET_PROMPT = "character design sheet: front view, three-quarter view and full body side by side, neutral standing pose, plain light grey background, even studio lighting, no text";
// What the judge scores a sheet on; keys are what the manifest and the review page show.
export const SHEET_RUBRIC = [
  { key: "recognizable", question: "Is the character distinctive, with a face and silhouette that could be kept the same across many shots?", weight: 2 },
  { key: "appearance", question: "Does the character match the written appearance: age, build, hair, clothing, colours, props?", weight: 2 },
  { key: "style", question: "Is the picture in the requested visual style?", weight: 1 },
  { key: "clean", question: "Are anatomy and clothing free of faults: correct hands and fingers, no warped face, nothing floating or duplicated?", weight: 2 },
  { key: "no_text", question: "Is the picture free of text, letters, watermarks and logos?", weight: 1 },
];

/** The option letter of candidate n on the review page: 1 → A. */
export const optionKey = (n) => String.fromCharCode(64 + n);

export function sheetPrompt(character, look) {
  return `${character.sheet_prompt ?? DEFAULT_SHEET_PROMPT}. Character: ${character.name}, ${character.appearance}. Style: ${look.style}`.slice(0, 4000);
}

/** The owner's picks from `--choose jingwei=2,yandi=1`, checked against the manifest. */
export function parseChoice(text, manifest) {
  const chosen = {};
  for (const pair of String(text).split(",").map((each) => each.trim()).filter(Boolean)) {
    const [id, number] = pair.split("=");
    const n = Number(number);
    const character = manifest.characters?.[id];
    if (!character) throw new UsageError(`--choose: ${id} is not a character in characters/manifest.json`);
    if (!Number.isInteger(n) || !character.candidates.some((candidate) => candidate.n === n)) throw new UsageError(`--choose: ${id} has no candidate ${number}; it has ${character.candidates.map((candidate) => candidate.n).join(", ")}`);
    chosen[id] = n;
  }
  return chosen;
}

/** The candidate to suggest: the best-scoring one that passed the judge, or null. */
export function suggestedOf(candidates) {
  const passed = candidates.filter((candidate) => candidate.judge?.passed);
  if (!passed.length) return null;
  return passed.reduce((best, candidate) => (candidate.judge.overall > best.judge.overall ? candidate : best)).n;
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.characters);
const choiceFile = (workdir) => path.join(workdir, ARTIFACTS.characterChoice);
const writeManifest = (workdir, manifest) => atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: {
      slug: { type: "string" },
      file: { type: "string" },
      workdir: { type: "string" },
      candidates: { type: "string" },
      character: { type: "string" },
      choose: { type: "string" },
      "dry-run": { type: "boolean" },
      channel: { type: "string" },
    },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("look needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc) || !doc.characters?.length) throw new UsageError("look is for a drama with characters (format \"drama\", characters: [...])");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const hash = lookHash(doc);
  const characters = values.character ? doc.characters.filter((character) => character.id === values.character) : doc.characters;
  if (!characters.length) throw new UsageError(`--character ${values.character} is not a character of ${doc.slug}`);

  if (values.choose) {
    const manifest = readJson(manifestFile(workdir), null);
    if (!manifest || manifest.look_hash !== hash) throw new UsageError("characters/manifest.json is missing or was made for an older look; run look first");
    const chosen = { ...(readJson(choiceFile(workdir), null)?.look_hash === hash ? readJson(choiceFile(workdir)).chosen : {}), ...parseChoice(values.choose, manifest) };
    atomicWrite(choiceFile(workdir), `${JSON.stringify({ look_hash: hash, chosen, chosen_at: ctx.now().toISOString() }, null, 2)}\n`);
    ctx.stdout.write(`chosen: ${Object.entries(chosen).map(([id, n]) => `${id} = ${n} (${optionKey(n)})`).join(", ")}\nnext: node tools/video/cli.mjs approve --slug ${doc.slug} --gate look (or let the owner choose on /admin/videos)\n`);
    return EXIT.ok;
  }

  const count = values.candidates ? Number(values.candidates) : look.candidates;
  if (!Number.isInteger(count) || count < 1 || count > 6) throw new UsageError("--candidates must be 1 to 6");
  if (values["dry-run"]) {
    ctx.stdout.write(`look ${hash}: ${characters.length} characters × ${count} candidates = ${characters.length * count} images (up to ${MAX_LOOK_ROUNDS} rounds), plus a judge call each\n`);
    for (const character of characters) ctx.stdout.write(`${character.id} (${character.name}): ${sheetPrompt(character, look)}\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = await mediaStatus(clientOptions(ctx, credentials));
      const problem = statusProblem(status);
      const usd = characters.length * count * (imagePrice(status) + JUDGE_USD_PER_CALL);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.image.provider} ${status.image.model} ready`}; about US$${usd.toFixed(2)} for one round; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
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
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "look", now: ctx.now });
  mkdirSync(path.join(workdir, "characters"), { recursive: true });
  // The owner's style frames go to the media store once, and every sheet is generated with them.
  const references = [];
  for (const frame of look.style_frames) {
    const file = path.join(project.dir, frame);
    if (!existsSync(file)) throw new UsageError(`look.style_frames: ${frame} is not in ${project.dir}`);
    references.push({ sha256: await stage.upload(file), role: "style" });
  }
  const existing = readJson(manifestFile(workdir), null);
  const manifest = existing?.look_hash === hash ? existing : { look_hash: hash, look, image: { provider: status.image.provider, model: status.image.model }, characters: {} };
  manifest.image = { provider: status.image.provider, model: status.image.model };
  const started = Date.now();
  let generated = 0;
  let stopped = false;

  for (const character of characters) {
    const entry = manifest.characters[character.id] ?? { name: character.name, candidates: [], suggested: null, needs_review: false };
    entry.name = character.name;
    entry.prompt = sheetPrompt(character, look);
    manifest.characters[character.id] = entry;
    for (let round = 1; round <= MAX_LOOK_ROUNDS && !stopped; round++) {
      if (round > 1 && suggestedOf(entry.candidates) !== null) break;
      for (let index = 1; index <= count; index++) {
        const seed = (round - 1) * 100 + index;
        if (entry.candidates.some((candidate) => candidate.seed === seed && candidate.judge)) continue;
        let picture;
        try {
          picture = await stage.image({
            id: character.id,
            purpose: "character_sheet",
            prompt: entry.prompt,
            negative: look.negative,
            references,
            seed,
            target: `characters/${character.id}/${String(seed).padStart(3, "0")}`,
          });
        } catch (error) {
          if (error.code === "stopped") {
            stopped = true;
            break;
          }
          if (retakeable(error)) {
            ctx.stdout.write(`${character.id} seed ${seed}: ${error.message}; trying another seed\n`);
            continue;
          }
          throw error;
        }
        if (!picture.reused) generated += 1;
        let judge;
        try {
          judge = await stage.judge({
            id: character.id,
            kind: "look",
            files: [{ sha256: picture.sha256, label: `candidate ${optionKey(entry.candidates.length + 1)}` }],
            rubric: SHEET_RUBRIC,
            context: { character: { name: character.name, description: character.appearance }, style: look.style },
          });
        } catch (error) {
          if (error.code !== "stopped") throw error;
          stopped = true;
          break;
        }
        entry.candidates.push({ n: entry.candidates.length + 1, seed, file: picture.file, sha256: picture.sha256, key: picture.key, judge });
        entry.suggested = suggestedOf(entry.candidates);
        entry.needs_review = entry.suggested === null;
        writeManifest(workdir, manifest);
        ctx.stdout.write(`${character.id} ${optionKey(entry.candidates.length)}: judge ${judge.overall}/10${judge.passed ? "" : ` NOT passed: ${judge.problems.join("; ") || "below the bar"}`}${picture.reused ? " (reused)" : ""}\n`);
      }
    }
    if (stopped) break;
  }
  writeManifest(workdir, manifest);
  if (stopped) {
    ctx.stdout.write(`stopped by the STOP file after ${generated} new sheets; rerun to continue\n`);
    return EXIT.ok;
  }

  const tiles = Object.entries(manifest.characters).flatMap(([id, entry]) =>
    entry.candidates.map((candidate) => ({ file: candidate.file, label: `${entry.name} · ${optionKey(candidate.n)} · ${candidate.judge?.overall ?? "?"}/10${entry.suggested === candidate.n ? " · 建議" : ""}` })),
  );
  const sheet = await drawContactSheet(ctx, { workdir, channel: values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL, title: `${doc.slug}：角色設定圖`, tiles, file: "characters/contact-sheet.png" });
  if (sheet.note) ctx.stdout.write(`${sheet.note}\n`);
  manifest.contact_sheet = sheet.file;
  manifest.generated_at = ctx.now().toISOString();
  writeManifest(workdir, manifest);
  const seconds = Math.round((Date.now() - started) / 1000);
  const waiting = Object.entries(manifest.characters).filter(([, entry]) => entry.needs_review);
  recordStage(workdir, "look", { characters: Object.keys(manifest.characters).length, generated, needs_review: waiting.map(([id]) => id), usd: ledgerTotals(workdir).usd, seconds }, ctx.now());
  for (const [id, entry] of Object.entries(manifest.characters)) {
    ctx.stdout.write(`${id}: ${entry.candidates.length} candidates, suggested ${entry.suggested === null ? "none" : optionKey(entry.suggested)}\n`);
  }
  ctx.stdout.write(`${generated} sheets generated in ${seconds} s; this video has spent US$${ledgerTotals(workdir).usd.toFixed(2)}\n`);
  if (waiting.length) {
    for (const [id, entry] of waiting) ctx.stdout.write(`ERROR ${id}: no candidate passed the judge: ${[...new Set(entry.candidates.flatMap((candidate) => candidate.judge?.problems ?? []))].join("; ")}\n`);
    ctx.stdout.write(`rewrite the appearance or sheet_prompt of ${waiting.map(([id]) => id).join(", ")} and run look again\n`);
    return EXIT.lint;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs review-push --slug ${doc.slug} --gate look\n`);
  return EXIT.ok;
}
