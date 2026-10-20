// Apply human-checked picture substitutions to the unapproved local concept only.
// Keep the generated takes and their judge verdicts intact for the official gate.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { contactSheetPages } from "../../../../tools/video/media/keyframes.mjs";
import { drawContactSheet, pictureHashes } from "../../../../tools/video/media/stages.mjs";
import { duplicates } from "../../../../tools/video/media/qc.mjs";
import { acquireProjectLease } from "../../../../tools/video/core/project-lease.mjs";
import { lookHash } from "../../../../tools/video/core/drama.mjs";
import { visualHash } from "../../../../tools/video/core/timeline.mjs";

const ROOT = path.resolve(import.meta.dirname, "../../../..");
const SLUG = "story-everyday-netflix-x03";
const docFile = path.join(ROOT, "docs/videos", SLUG, "video.json");
const read = (file) => JSON.parse(readFileSync(file, "utf8"));
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const hex = /^[a-f0-9]{64}$/;
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");

function inside(workdir, candidate) {
  const file = path.resolve(workdir, candidate);
  assert.ok(file.startsWith(`${path.resolve(workdir)}${path.sep}`), `picture escapes workdir: ${candidate}`);
  return file;
}

function dimensions(file) {
  const result = spawnSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", file], { encoding: "utf8" });
  assert.equal(result.status, 0, `ffprobe failed: ${file}: ${result.stderr}`);
  const stream = JSON.parse(result.stdout).streams?.[0];
  assert.ok(stream?.width > 0 && stream?.height > 0 && stream.width * 9 === stream.height * 16, `picture must be 16:9: ${file}`);
  return { width: stream.width, height: stream.height };
}

function existingInside(workdir, candidate) {
  const file = inside(workdir, candidate);
  assert.ok(realpathSync(file).startsWith(`${realpathSync(workdir)}${path.sep}`), `picture symlink escapes workdir: ${candidate}`);
  return file;
}

function validate(workdir, mapFile) {
  const doc = read(docFile);
  const manifestFile = inside(workdir, "keyframes/manifest.json");
  const manifest = read(manifestFile);
  const map = read(mapFile);
  assert.equal(map.video_json_sha256, sha(docFile), "donor map must bind the current script");
  assert.equal(manifest.look_hash, lookHash(doc), "keyframe look hash drift");
  assert.equal(manifest.visual_hash, visualHash(doc), "keyframe visual hash drift");
  assert.ok(Array.isArray(map.replacements) && map.replacements.length > 0, "no substitutions proposed");
  const ids = new Set(doc.scenes.filter((scene) => scene.template === "shot" && !scene.data?.source).map((scene) => scene.id));
  assert.equal(ids.size, 65, "unexpected scene count");
  assert.equal(Object.keys(manifest.shots).length, ids.size, "incomplete keyframe batch");
  assert.equal(readdirSync(inside(workdir, "review")).filter((name) => /^manual-keyframe-selections-[a-f0-9]{12}\.json$/.test(name)).length, 0, "a manual selection receipt already exists");
  for (const id of ids) {
    const shot = manifest.shots[id];
    assert.ok(shot?.file && !shot.incomplete && hex.test(shot.sha256 ?? "") && !shot.manual_selection, `incomplete or already substituted shot: ${id}`);
    assert.equal(sha(existingInside(workdir, shot.file)), shot.sha256, `selected image drift: ${id}`);
  }
  if (map.manifest_before_sha256 !== undefined) assert.equal(map.manifest_before_sha256, sha(manifestFile), "donor map belongs to another keyframe manifest");
  const seen = new Set();
  const validated = map.replacements.map((item) => {
    assert.ok(ids.has(item.target_id) && !seen.has(item.target_id), `unknown or repeated target: ${item.target_id}`);
    seen.add(item.target_id);
    assert.ok(typeof item.reason === "string" && item.reason.trim().length >= 8, `reason missing: ${item.target_id}`);
    assert.match(item.donor_sha256, hex, `donor SHA missing: ${item.target_id}`);
    const previous = manifest.shots[item.target_id];
    assert.ok(previous?.file && previous.sha256 && !previous.incomplete && !previous.manual_selection, `target is incomplete or already manually substituted: ${item.target_id}`);
    if (item.previous_sha256 !== undefined) assert.equal(item.previous_sha256, previous.sha256, `donor map was reviewed against another selected take: ${item.target_id}`);
    const donor = existingInside(workdir, item.donor_file);
    assert.ok(existsSync(donor), `donor missing: ${item.donor_file}`);
    assert.equal(sha(donor), item.donor_sha256, `donor SHA drift: ${item.target_id}`);
    const shape = dimensions(donor);
    const ext = path.extname(donor).toLowerCase();
    assert.ok([".jpg", ".jpeg", ".png"].includes(ext), `unsupported donor format: ${donor}`);
    return { item, previous, donor, shape, ext };
  });
  return { doc, map, manifest, manifestFile, validated, mapSha: sha(mapFile), manifestSha: sha(manifestFile) };
}

async function apply(workdir, mapFile) {
  const lease = acquireProjectLease(workdir, { owner: "manual-keyframe-concept-substitution" });
  try { await applyWithLease(workdir, mapFile, lease); }
  finally { lease.release(); }
}

async function applyWithLease(workdir, mapFile, lease) {
  const data = validate(workdir, mapFile);
  const namespace = `manual-${data.mapSha.slice(0, 12)}`;
  const outputDir = inside(workdir, `keyframes/${namespace}`);
  const receiptFile = inside(workdir, `review/manual-keyframe-selections-${data.mapSha.slice(0, 12)}.json`);
  const mapRelative = `review/manual-keyframe-map-${data.mapSha.slice(0, 12)}.json`;
  const mapSnapshot = inside(workdir, mapRelative);
  const backupRelative = `review/keyframe-manifest-before-${namespace}.json`;
  const backup = inside(workdir, backupRelative);
  const manifestTemp = `${data.manifestFile}.manual-${process.pid}.tmp`;
  const receiptTemp = `${receiptFile}.tmp`;
  assert.ok(!existsSync(outputDir) && !existsSync(receiptFile), "manual selection was already applied");
  const lock = inside(workdir, "review/manual-keyframes.lock");
  mkdirSync(path.dirname(lock), { recursive: true });
  writeFileSync(lock, `${process.pid}\n`, { flag: "wx" });
  const manifestBefore = readFileSync(data.manifestFile);
  let manifestCommitted = false;
  try {
    lease.verify();
    assert.equal(sha(data.manifestFile), data.manifestSha, "keyframe manifest changed during manual review");
    mkdirSync(outputDir);
    copyFileSync(mapFile, mapSnapshot);
    assert.equal(sha(mapSnapshot), data.mapSha, "donor map changed during manual review");
    const changes = [];
    for (const { item, previous, donor, shape, ext } of data.validated) {
      const relative = `keyframes/${namespace}/${item.target_id}${ext}`;
      const destination = inside(workdir, relative);
      copyFileSync(donor, destination);
      assert.equal(sha(destination), item.donor_sha256, `donor copy failed: ${item.target_id}`);
      const old = { file: previous.file, sha256: previous.sha256, seed: previous.seed, judge_passed: previous.judge?.passed ?? null };
      const manual = { kind: "human_safe_donor_for_unapproved_preview", donor_file: item.donor_file, donor_sha256: item.donor_sha256, previous: old, reason: item.reason, severity: item.severity ?? "hold", dimensions: shape };
      const shot = data.manifest.shots[item.target_id];
      shot.file = relative;
      shot.sha256 = item.donor_sha256;
      shot.needs_review = true;
      shot.manual_selection = manual;
      shot.problems = [...new Set([...(Array.isArray(shot.problems) ? shot.problems : []), `human visual hold; concept-only donor: ${item.reason}`])];
      changes.push({ target_id: item.target_id, ...manual, selected_file: relative });
    }
    const drawn = data.doc.scenes.filter((scene) => scene.template === "shot" && !scene.data?.source).map((scene) => ({ id: scene.id, file: data.manifest.shots[scene.id].file }));
    const hashes = await pictureHashes({ env: process.env }, workdir, drawn);
    data.manifest.duplicates = hashes ? duplicates(hashes) : [];
    const thumbnailId = data.doc.thumbnail?.data?.shot;
    data.manifest.thumbnail_source = thumbnailId ? data.manifest.shots[thumbnailId]?.file ?? null : null;
    const pages = contactSheetPages(drawn.map(({ id, file }) => ({ file, label: `${id} · ${data.manifest.shots[id].judge?.overall ?? "?"}/10${data.manifest.shots[id].needs_review ? " · 待審" : ""}` })));
    const contactSheets = [];
    for (const [index, page] of pages.entries()) {
      const title = `${SLUG}：本機概念分鏡 ${drawn.length} 鏡（第 ${index + 1}／${pages.length} 頁）`;
      // Keep the generated contact sheets intact until the new manifest is committed.
      const file = `keyframes/${namespace}/${path.basename(page.file)}`;
      const sheet = await drawContactSheet({ root: ROOT, env: process.env }, { workdir, title, tiles: page.tiles, file });
      assert.ok(sheet.file, sheet.note ?? "contact sheet rendering failed");
      contactSheets.push(sheet.file);
    }
    data.manifest.contact_sheet = contactSheets[0];
    data.manifest.contact_sheets = contactSheets;
    data.manifest.generated_at = new Date().toISOString();
    copyFileSync(data.manifestFile, backup);
    const manifestBytes = json(data.manifest);
    const receipt = { schema_version: 1, kind: "manual_keyframe_substitutions", approval: "UNAPPROVED_CONCEPT", official_branding: false, video_json_sha256: data.map.video_json_sha256, donor_map_file: mapRelative, donor_map_sha256: data.mapSha, manifest_before_sha256: data.manifestSha, manifest_after_sha256: digest(manifestBytes), backup: backupRelative, contact_sheets: contactSheets.map((file) => ({ file, sha256: sha(inside(workdir, file)) })), changes };
    writeFileSync(manifestTemp, manifestBytes, { flag: "wx" });
    writeFileSync(receiptTemp, json(receipt), { flag: "wx" });
    lease.verify();
    renameSync(manifestTemp, data.manifestFile);
    manifestCommitted = true;
    renameSync(receiptTemp, receiptFile);
    process.stdout.write(json({ status: "SUBSTITUTED_FOR_CONCEPT_REVIEW", receipt: receiptFile, changes: changes.length, manifest_sha256: receipt.manifest_after_sha256, contact_sheets: contactSheets }));
  } catch (error) {
    if (manifestCommitted) {
      try {
        writeFileSync(manifestTemp, manifestBefore);
        renameSync(manifestTemp, data.manifestFile);
      } catch (rollbackError) {
        throw new AggregateError([error, rollbackError], "manual substitution failed and its keyframe manifest could not be restored");
      }
    }
    rmSync(outputDir, { recursive: true, force: true });
    for (const file of [receiptFile, receiptTemp, manifestTemp, backup, mapSnapshot]) rmSync(file, { force: true });
    throw error;
  } finally {
    rmSync(lock, { force: true });
  }
}

const { values } = parseArgs({ args: process.argv.slice(2), options: { workdir: { type: "string" }, map: { type: "string" }, apply: { type: "boolean" } }, strict: true });
assert.ok(values.workdir && values.map, "usage: node apply-manual-keyframes.mjs --workdir <episode-workdir> --map <donor-map.json> [--apply]");
const workdir = path.resolve(values.workdir);
const mapFile = path.resolve(values.map);
if (values.apply) await apply(workdir, mapFile);
else {
  const data = validate(workdir, mapFile);
  process.stdout.write(json({ status: "READY_FOR_MANUAL_SUBSTITUTION", map_sha256: data.mapSha, manifest_sha256: data.manifestSha, replacements: data.validated.map(({ item, shape }) => ({ target_id: item.target_id, donor_sha256: item.donor_sha256, dimensions: shape })) }));
}
