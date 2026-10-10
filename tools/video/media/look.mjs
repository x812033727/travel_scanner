// `look`: a few candidate character sheets per character, scored by the judge, for the owner to
// pick from on /admin/videos (docs/videos/DRAMA.md); each candidate after the first is asked
// with the judge's fixes for the ones before it, the second round with the first round's. The
// chosen sheet is the reference every keyframe of that character is generated from, which is
// what keeps a character the same from shot to shot. Writes characters/manifest.json (the look
// gate binds to it), one PNG per candidate under characters/<id>/, and a contact sheet.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, realpathSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { inflateSync } from "node:zlib";

import { approve } from "../core/approvals.mjs";
import { isDrama, lookHash, resolveLook } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { fixClauses, fixesBefore, retakePrompt } from "./keyframes.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { externalCandidateProblem, externalSourcesCurrent, reuseSheets, sheetKey } from "./series-store.mjs";
import { drawContactSheet, imagePrice, imageSelectionVersion, imageStatus, JUDGE_USD_PER_CALL, mayWriteProject, retakeable, sameImage, Stage, statusProblem } from "./stages.mjs";

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
    const candidate = character.candidates.find((each) => each.n === n);
    if (candidate.external_import && !candidate.judge) throw new UsageError(`--choose: ${id} candidate ${number} has not been judged; rerun look import with --judge before choosing`);
    chosen[id] = n;
  }
  return chosen;
}

/** The candidate to suggest: the best-scoring one that passed the judge, or null. */
export function suggestedOf(candidates) {
  const passed = candidates.filter((candidate) => candidate.judge?.passed && !candidate.superseded_by);
  if (!passed.length) return null;
  return passed.reduce((best, candidate) => (candidate.judge.overall > best.judge.overall ? candidate : best)).n;
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.characters);
const choiceFile = (workdir) => path.join(workdir, ARTIFACTS.characterChoice);
const writeManifest = (workdir, manifest) => atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const HASH = /^[a-f0-9]{64}$/;
const PNG_SIGNATURE = Buffer.from("89504e470d0a1a0a", "hex");
const MAX_IMPORT_BYTES = 32 * 1024 * 1024;

// A deliberately narrow PNG contract, without a native image library or a server: validate
// every chunk, then decompress every scanline. No resizing or pixel rewriting takes place.
export function inspectLookPng(bytes) {
  const bad = (why) => { throw new UsageError(`--image: invalid PNG (${why})`); };
  if (bytes.length > MAX_IMPORT_BYTES || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) bad("expected PNG, at most 32 MiB");
  let width, height, channels, ended = false, dataEnded = false;
  const compressed = [];
  for (let offset = 8; offset < bytes.length;) {
    if (offset + 12 > bytes.length) bad("truncated chunk");
    const length = bytes.readUInt32BE(offset);
    const end = offset + 12 + length;
    if (end > bytes.length) bad("truncated chunk data");
    const type = bytes.toString("ascii", offset + 4, offset + 8);
    if (!/^[A-Za-z]{4}$/.test(type)) bad("chunk type");
    let crc = 0xffffffff;
    for (const byte of bytes.subarray(offset + 4, end - 4)) {
      crc ^= byte;
      for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
    if (((crc ^ 0xffffffff) >>> 0) !== bytes.readUInt32BE(end - 4)) bad(`${type} checksum`);
    const data = bytes.subarray(offset + 8, end - 4);
    if (offset === 8 && type !== "IHDR") bad("IHDR must be first");
    if (type === "IHDR") {
      if (width || length !== 13) bad("IHDR");
      width = data.readUInt32BE(0); height = data.readUInt32BE(4);
      if (width < 512 || height < 512 || width > 8192 || height > 8192 || width * height > 16 * 1024 * 1024) bad("each side must be 512–8192 pixels, at most 16 megapixels");
      if (data[8] !== 8 || ![2, 6].includes(data[9]) || data[10] || data[11] || data[12]) bad("requires 8-bit, non-interlaced RGB or RGBA");
      channels = data[9] === 6 ? 4 : 3;
    } else if (type === "IDAT") {
      if (dataEnded) bad("non-consecutive IDAT");
      compressed.push(data);
    } else if (type === "IEND") {
      if (length || end !== bytes.length || !compressed.length) bad("IEND or missing pixels");
      ended = true;
    } else {
      if (compressed.length) dataEnded = true;
      if (type === "acTL" || type === "fcTL" || type === "fdAT") bad("animated PNG is not a character sheet");
      if (type === "PLTE") {
        if (compressed.length || !length || length % 3 || length > 768) bad("PLTE");
      } else if (type[0] === type[0].toUpperCase()) bad(`unsupported critical chunk ${type}`);
    }
    offset = end;
  }
  if (!ended) bad("missing IEND");
  const row = 1 + width * channels;
  let pixels;
  try { pixels = inflateSync(Buffer.concat(compressed), { maxOutputLength: row * height }); }
  catch { bad("pixel decompression"); }
  if (pixels.length !== row * height) bad("pixel length");
  for (let offset = 0; offset < pixels.length; offset += row) if (pixels[offset] > 4) bad("scanline filter");
  return { width, height, format: "png" };
}

function importFile(file, label, limit = MAX_IMPORT_BYTES) {
  try {
    const stat = statSync(file);
    if (!stat.isFile() || stat.size > limit) throw new Error("not a regular file or too large");
    return readFileSync(file);
  } catch (error) { throw new UsageError(`${label}: ${error.message}`); }
}

function importSource(bytes, { character, hash, mediaHash, root }) {
  let source;
  try { source = JSON.parse(bytes.toString("utf8")); }
  catch { throw new UsageError("--source must be a JSON provenance receipt"); }
  if (source?.schema_version !== 1 || source.character_id !== character.id || source.look_hash !== hash || source.image_sha256 !== mediaHash) throw new UsageError("--source: schema_version, character_id, look_hash or image_sha256 does not match the current import");
  if (!Array.isArray(source.source_files) || !source.source_files.length) throw new UsageError("--source: source_files must bind at least one repository source file");
  const seen = new Set();
  for (const entry of source.source_files) {
    if (!entry || typeof entry.path !== "string" || !entry.path || entry.path.includes("\\") || path.posix.isAbsolute(entry.path) || entry.path.split("/").some((part) => !part || part === "." || part === "..") || entry.path.includes(":") || !HASH.test(entry.sha256 ?? "") || seen.has(entry.path)) throw new UsageError("--source: source_files requires unique repository-relative POSIX paths and SHA-256 hashes");
    seen.add(entry.path);
    // Resolve links as well as lexical paths; a receipt cannot read outside the source tree.
    let relative;
    try { relative = path.relative(realpathSync(root), realpathSync(path.join(root, entry.path))); }
    catch { throw new UsageError(`--source: missing source file ${entry.path}`); }
    if (relative.startsWith(`..${path.sep}`) || relative === ".." || path.isAbsolute(relative)) throw new UsageError(`--source: source outside the repository: ${entry.path}`);
  }
  if (!externalSourcesCurrent({ source_files: source.source_files }, root)) throw new UsageError("--source: source file SHA-256 changed; refresh the receipt and review the affected artwork");
  for (const field of ["prompt_sha256", "reference_sha256"]) if (source[field] !== undefined && !HASH.test(source[field])) throw new UsageError(`--source: ${field} must be a SHA-256 hash`);
  return source;
}

function preserveFile(file, bytes) {
  if (existsSync(file)) {
    if (sha(readFileSync(file)) !== sha(bytes)) throw new UsageError(`existing content-addressed import was changed: ${file}`);
    return;
  }
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, bytes, { flag: "wx" });
}

function invalidateImportedLook(workdir, key) {
  // Preserve paid work and prior decisions. The regular look/storyboard/hash gates will
  // refuse these manifests until the owner reviews and the affected stages are rebuilt.
  for (const artifact of [ARTIFACTS.keyframes, ARTIFACTS.clips]) {
    const file = path.join(workdir, artifact);
    if (!existsSync(file)) continue;
    const bytes = readFileSync(file);
    const previous = JSON.parse(bytes.toString("utf8"));
    preserveFile(path.join(workdir, "characters", "history", `${sha(bytes)}.json`), bytes);
    atomicWrite(file, `${JSON.stringify({ ...previous, look_hash: null, external_look_invalidated_by: key }, null, 2)}\n`);
  }
}

async function importLook(args, ctx) {
  const values = parseArgs({ args, strict: true, options: {
    slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" },
    character: { type: "string" }, image: { type: "string" }, source: { type: "string" },
    judge: { type: "boolean" }, "dry-run": { type: "boolean" },
  } }).values;
  if ((!values.slug && !values.file) || !values.character || !values.image || !values.source) throw new UsageError("look import needs --slug (or --file video.json), --character ID, --image PNG and --source receipt.json");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc } = project;
  if (lintProject(project).errors.length) { ctx.stdout.write(`${doc.slug} has lint errors; run lint first\n`); return ctx.EXIT.lint; }
  if (!isDrama(doc)) throw new UsageError("look import is for a drama's base character sheet");
  const character = doc.characters?.find((each) => each.id === values.character);
  if (!character) throw new UsageError(`--character ${values.character} is not a character of ${doc.slug}`);
  const bytes = importFile(values.image, "--image");
  const dimensions = inspectLookPng(bytes);
  const mediaHash = sha(bytes), hash = lookHash(doc), look = resolveLook(doc.look);
  const sourceBytes = importFile(values.source, "--source", 1024 * 1024);
  const source = importSource(sourceBytes, { character, hash, mediaHash, root: ctx.root });
  const sourceHash = sha(sourceBytes);
  const key = sha(JSON.stringify(["external-look-v1", sheetKey(character, look), mediaHash, sourceHash]));
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  if (values["dry-run"]) {
    ctx.stdout.write(`look import ${character.id}: ${dimensions.width}x${dimensions.height}, PNG ${mediaHash}, source ${sourceHash}\n${values.judge ? "explicit --judge would call the normal paid look judge" : "offline pending candidate only"}; dry-run writes nothing and makes no requests\n`);
    return ctx.EXIT.ok;
  }
  if (!mayWriteProject(ctx, workdir, "look-import")) return ctx.EXIT.incomplete;
  const existing = readJson(manifestFile(workdir), null);
  const manifest = existing?.look_hash === hash ? existing : { look_hash: hash, look, characters: {} };
  for (const each of doc.characters) manifest.characters[each.id] ??= { name: each.name, prompt: sheetPrompt(each, look), candidates: [], suggested: null, needs_review: true };
  const entry = manifest.characters[character.id];
  let candidate = entry.candidates.find((each) => each.key === key && each.external_import);
  if (!candidate) {
    if (existing) preserveFile(path.join(workdir, "characters", "history", `${sha(readFileSync(manifestFile(workdir)))}.json`), readFileSync(manifestFile(workdir)));
    const file = `characters/${character.id}/import-${key}.png`;
    const receipt = `characters/${character.id}/import-${key}.source.json`;
    preserveFile(path.join(workdir, file), bytes);
    preserveFile(path.join(workdir, receipt), sourceBytes);
    for (const previous of entry.candidates) {
      if (previous.external_import && !externalSourcesCurrent(previous.external_import, ctx.root)) previous.superseded_by = key;
    }
    candidate = { n: Math.max(0, ...entry.candidates.map((each) => each.n)) + 1, seed: null, file, sha256: mediaHash, key, judge: null,
      external_import: { schema_version: 1, source_sha256: sourceHash, source_file: receipt, source_files: source.source_files,
        character_key: sheetKey(character, look), dimensions, original_name: path.basename(values.image), imported_at: ctx.now().toISOString(),
        ...(source.prompt_sha256 ? { prompt_sha256: source.prompt_sha256 } : {}), ...(source.reference_sha256 ? { reference_sha256: source.reference_sha256 } : {}) } };
    entry.candidates.push(candidate);
    entry.suggested = null; entry.needs_review = true; delete entry.reused;
    manifest.external_imports = true;
    manifest.contact_sheet = null; // Any earlier composite omits this new candidate; keep its bytes, drop the stale link.
    // An old choice must not silently select this revision (or its prior version).
    const choice = readJson(choiceFile(workdir), null);
    if (choice) {
      const chosen = choice.look_hash === hash ? { ...choice.chosen } : {};
      delete chosen[character.id];
      atomicWrite(choiceFile(workdir), `${JSON.stringify({ ...choice, look_hash: hash, chosen }, null, 2)}\n`);
    }
    invalidateImportedLook(workdir, key);
    writeManifest(workdir, manifest);
  } else {
    preserveFile(path.join(workdir, candidate.file), bytes);
    preserveFile(path.join(workdir, candidate.external_import.source_file), sourceBytes);
  }
  if (values.judge && !candidate.judge) {
    if (candidate.judge_state === "submitted") throw new MediaError("the previous judge request has an unknown outcome; reconcile it before any retry", { who: "owner" });
    const options = { ...clientOptions(ctx, requireCredentials(ctx)), attempts: 1 };
    const status = await mediaStatus(options);
    if (!status.enabled) throw new MediaError("the drama route is off; enable it before judging", { who: "owner" });
    const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "look", now: ctx.now });
    stage.spend(JUDGE_USD_PER_CALL, "judge call");
    const uploaded = await stage.upload(path.join(workdir, candidate.file));
    if (uploaded !== mediaHash) throw new MediaError("uploaded character PNG SHA-256 does not match the imported bytes", { who: "owner" });
    // Persist before the paid POST. A timeout/crash cannot turn the next run into a duplicate call.
    candidate.judge_state = "submitted";
    writeManifest(workdir, manifest);
    candidate.judge = await stage.judge({ id: character.id, kind: "look", files: [{ sha256: mediaHash, label: `candidate ${optionKey(candidate.n)}` }], rubric: SHEET_RUBRIC, context: { character: { name: character.name, description: character.appearance }, style: look.style } });
    candidate.judge_state = "judged";
    entry.suggested = suggestedOf(entry.candidates); entry.needs_review = entry.suggested === null;
    writeManifest(workdir, manifest);
  }
  ctx.stdout.write(`${character.id} ${optionKey(candidate.n)} imported: ${candidate.judge ? `judge ${candidate.judge.overall}/10${candidate.judge.passed ? "" : " NOT passed"}` : "pending judge"}; no choice or approval was recorded\nnext: ${candidate.judge ? `node tools/video/cli.mjs review-push --slug ${doc.slug} --gate look` : "rerun the same look import arguments with --judge when authorized"}\n`);
  return candidate.judge && !candidate.judge.passed ? ctx.EXIT.lint : ctx.EXIT.ok;
}

export async function run(command, args, ctx) {
  if (args[0] === "import") return importLook(args.slice(1), ctx);
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
  const imageVersion = imageSelectionVersion(project.series);
  const { doc } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc) || !doc.characters?.length) throw new UsageError("look is for a drama with characters (format \"drama\", characters: [...]); a drama with none has no look stage: run keyframes");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const look = resolveLook(doc.look);
  const hash = lookHash(doc);
  const characters = values.character ? doc.characters.filter((character) => character.id === values.character) : doc.characters;
  if (!characters.length) throw new UsageError(`--character ${values.character} is not a character of ${doc.slug}`);

  if (values.choose) {
    if (!mayWriteProject(ctx, workdir, "look")) return EXIT.incomplete;
    const manifest = readJson(manifestFile(workdir), null);
    if (!manifest || manifest.look_hash !== hash) throw new UsageError("characters/manifest.json is missing or was made for an older look; run look first");
    const chosen = { ...(readJson(choiceFile(workdir), null)?.look_hash === hash ? readJson(choiceFile(workdir)).chosen : {}), ...parseChoice(values.choose, manifest) };
    for (const [id, n] of Object.entries(chosen)) {
      const candidate = manifest.characters[id]?.candidates.find((each) => each.n === n);
      const problem = externalCandidateProblem(candidate, { workdir, sourceRoot: ctx.root, character: doc.characters.find((each) => each.id === id), look });
      if (problem) throw new UsageError(`${id}: ${problem}`);
    }
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
      const status = imageStatus(await mediaStatus(clientOptions(ctx, credentials)), project.series);
      const problem = statusProblem(status);
      const usd = characters.length * count * (imagePrice(status) + JUDGE_USD_PER_CALL);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.image.provider} ${status.image.model} ${status.image.configured === null ? "(provider key checked on submit)" : "ready"}`}; about US$${usd.toFixed(2)} for one round; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  if (!mayWriteProject(ctx, workdir, "look")) return EXIT.incomplete;
  const prior = readJson(manifestFile(workdir), null);
  if (characters.some((character) => prior?.characters?.[character.id]?.candidates?.some((candidate) => candidate.external_import))) throw new MediaError("external character candidates already exist; use look import to add/judge them, or --choose after judging; generation will not replace imported artwork", { who: "owner" });
  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = imageStatus(await mediaStatus(options), project.series);
  const problem = statusProblem(status);
  if (problem) throw new MediaError(problem, { who: "owner" });
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "look", imageVersion, now: ctx.now });
  mkdirSync(path.join(workdir, "characters"), { recursive: true });
  // The owner's style frames go to the media store once, and every sheet is generated with them.
  const references = [];
  for (const frame of look.style_frames) {
    const file = path.join(project.dir, frame);
    if (!existsSync(file)) throw new UsageError(`look.style_frames: ${frame} is not in ${project.dir}`);
    references.push({ sha256: await stage.upload(file), role: "style" });
  }
  const existing = readJson(manifestFile(workdir), null);
  const manifest = existing?.look_hash === hash && (existing.external_imports || (sameImage(existing.image, status.image) && (!imageVersion || existing.image_selection_version === imageVersion))) ? existing : { look_hash: hash, look, image: { provider: status.image.provider, model: status.image.model }, image_selection_version: 1, characters: {} };
  manifest.image = { provider: status.image.provider, model: status.image.model };
  manifest.image_selection_version = 1;
  const started = Date.now();
  let generated = 0;
  let stopped = false;
  // An episode of a series reuses the sheets the owner approved for the same characters
  // (docs/videos/SERIES.md); only a new or changed character is drawn.
  const store = doc.series
    ? reuseSheets({ workBase: resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home }), workdir, sourceRoot: ctx.root, seriesSlug: doc.series.slug, characters, look, ...(imageVersion ? { image: status.image } : {}) })
    : { reused: {}, missing: characters };
  for (const [id, candidate] of Object.entries(store.reused)) {
    const character = characters.find((each) => each.id === id);
    manifest.characters[id] = { name: character.name, prompt: sheetPrompt(character, look), candidates: [candidate], suggested: 1, needs_review: false, reused: true };
    if (candidate.external_import) manifest.external_imports = true;
    ctx.stdout.write(`${id}: reusing the sheet approved for ${candidate.reused_from}\n`);
  }

  for (const character of store.missing) {
    const entry = manifest.characters[character.id] ?? { name: character.name, candidates: [], suggested: null, needs_review: false };
    entry.name = character.name;
    entry.prompt = sheetPrompt(character, look);
    manifest.characters[character.id] = entry;
    for (let round = 1; round <= MAX_LOOK_ROUNDS && !stopped; round++) {
      if (round > 1 && suggestedOf(entry.candidates) !== null) break;
      for (let index = 1; index <= count; index++) {
        const seed = (round - 1) * 100 + index;
        if (entry.candidates.some((candidate) => candidate.seed === seed && candidate.judge)) continue;
        // The judge's fixes for the candidates before this one go into its prompt.
        const fixes = fixesBefore(entry.candidates, seed);
        if (fixes.length) ctx.stdout.write(`${character.id} seed ${seed}: asked with the corrections of the candidates before: ${fixes.join("; ")}\n`);
        let picture;
        try {
          picture = await stage.image({
            id: character.id,
            purpose: "character_sheet",
            prompt: retakePrompt(entry.prompt, fixes),
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
        entry.candidates.push({ n: entry.candidates.length + 1, seed, file: picture.file, sha256: picture.sha256, key: picture.key, judge, ...(fixes.length ? { fixes } : {}) });
        entry.suggested = suggestedOf(entry.candidates);
        entry.needs_review = entry.suggested === null;
        writeManifest(workdir, manifest);
        ctx.stdout.write(`${character.id} ${optionKey(entry.candidates.length)}: judge ${judge.overall}/10${judge.passed ? "" : ` NOT passed: ${judge.problems.join("; ") || "below the bar"}`}${picture.reused ? " (reused)" : ""}\n`);
      }
    }
    // The judge's fixes across every candidate: what a rewrite of the appearance starts from.
    const fixes = fixClauses(entry.candidates.flatMap((candidate) => candidate.judge?.problems ?? []));
    if (entry.needs_review && fixes.length) entry.fixes = fixes;
    else delete entry.fixes;
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
    for (const [id, entry] of waiting) {
      ctx.stdout.write(`ERROR ${id}: no candidate passed the judge: ${[...new Set(entry.candidates.flatMap((candidate) => candidate.judge?.problems ?? []))].join("; ")}\n`);
      if (entry.fixes?.length) ctx.stdout.write(`  fixes for ${id}: ${entry.fixes.join("; ")}\n`);
    }
    ctx.stdout.write(`rewrite the appearance or sheet_prompt of ${waiting.map(([id]) => id).join(", ")} and run look again\n`);
    return EXIT.lint;
  }
  if (doc.series && !store.missing.length) {
    // Nothing new to choose: the owner's earlier picks stand, and the look is approved as such.
    atomicWrite(path.join(workdir, "characters", "choice.json"), `${JSON.stringify({ look_hash: hash, chosen: Object.fromEntries(Object.keys(store.reused).map((id) => [id, 1])), chosen_at: ctx.now().toISOString() }, null, 2)}\n`);
    await approve({ gate: "look", docDir: project.dir, workdir, now: ctx.now(), note: "reused the sheets approved earlier for this series" });
    ctx.stdout.write(`every sheet reused from the series; the look is approved\nnext: node tools/video/cli.mjs tts --slug ${doc.slug}\n`);
    return EXIT.ok;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs review-push --slug ${doc.slug} --gate look\n`);
  return EXIT.ok;
}
