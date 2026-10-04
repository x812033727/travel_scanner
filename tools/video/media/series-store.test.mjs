import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { dramaFixture, tempDir } from "../core/fixtures/load.mjs";
import { keepSheets, readStore, reuseSheets, sheetKey, storeDir } from "./series-store.mjs";

const PRO = { provider: "gemini", model: "gemini-3-pro-image" };
const FLASH = { provider: "gemini", model: "gemini-3.1-flash-image" };
const NOW = new Date("2026-09-29T00:00:00Z");
const SHA = (bytes) => createHash("sha256").update(bytes).digest("hex");

// Only byte copies and JSON are involved: no renderer, media server or model calls.
function fixture() {
  const workBase = tempDir("video-series-image-store-");
  const workdir = path.join(workBase, "episode-one");
  const doc = dramaFixture();
  doc.slug = "episode-one";
  doc.characters = [doc.characters[0]];
  const character = doc.characters[0];
  const file = path.join("characters", character.id, "approved.png");
  const bytes = Buffer.from("synthetic approved character sheet");
  mkdirSync(path.dirname(path.join(workdir, file)), { recursive: true });
  writeFileSync(path.join(workdir, file), bytes);
  const candidate = {
    n: 1, seed: 1, file, sha256: SHA(bytes),
    judge: { overall: 9, passed: true, scores: {}, problems: [], notes: "fixture approval" },
  };
  return { workBase, workdir, doc, character, candidate, bytes, seriesSlug: "fixture-series" };
}

function keep(box, image) {
  return keepSheets({
    ...box,
    manifest: { image_selection_version: 1, ...(image ? { image } : {}), characters: { [box.character.id]: { candidates: [box.candidate] } } },
    chosen: { [box.character.id]: 1 },
    now: NOW,
  });
}

function reuse(box, image, episode = "episode-two") {
  const workdir = path.join(box.workBase, episode);
  const result = reuseSheets({
    workBase: box.workBase, workdir, seriesSlug: box.seriesSlug,
    characters: box.doc.characters, look: box.doc.look, ...(image ? { image } : {}),
  });
  return { ...result, workdir };
}

function saved(box) {
  return readStore(box.workBase, box.seriesSlug).sheets[sheetKey(box.character, box.doc.look)];
}

test("approved series sheets preserve their generating provider/model and copied bytes", () => {
  const box = fixture();
  assert.equal(keep(box, FLASH), 1);
  const entry = saved(box);
  assert.deepEqual(entry.image, FLASH);
  assert.equal(entry.from, box.doc.slug);
  assert.equal(entry.sha256, SHA(box.bytes));
  assert.deepEqual(readFileSync(path.join(storeDir(box.workBase, box.seriesSlug), entry.file)), box.bytes);

  const again = reuse(box, FLASH);
  assert.deepEqual(again.missing, []);
  assert.deepEqual(Object.keys(again.reused), [box.character.id]);
  const candidate = again.reused[box.character.id];
  assert.deepEqual(candidate.image, FLASH);
  assert.equal(candidate.reused_from, box.doc.slug);
  assert.equal(candidate.sha256, SHA(box.bytes));
  assert.deepEqual(readFileSync(path.join(again.workdir, candidate.file)), box.bytes);
});

test("an explicit image selection refuses a stored model or provider mismatch", () => {
  for (const image of [PRO, { provider: "other-vendor", model: FLASH.model }]) {
    const box = fixture();
    keep(box, image);
    const result = reuse(box, FLASH);
    assert.deepEqual(result.reused, {});
    assert.deepEqual(result.missing, box.doc.characters);
    assert.equal(existsSync(path.join(result.workdir, "characters")), false);
    assert.deepEqual(saved(box).image, image, "a refusal must not relabel the stored sheet");
  }
});

test("an explicit image selection treats legacy sheets without provenance as missing", () => {
  const box = fixture();
  keep(box);
  assert.equal(Object.hasOwn(saved(box), "image"), false);
  const result = reuse(box, FLASH);
  assert.deepEqual(result.reused, {});
  assert.deepEqual(result.missing, box.doc.characters);
  assert.equal(existsSync(path.join(result.workdir, "characters")), false);
});

test("saving a pre-fix manifest cannot certify its possibly mislabeled image model", () => {
  const box = fixture();
  keepSheets({
    ...box,
    manifest: { image: PRO, characters: { [box.character.id]: { candidates: [box.candidate] } } },
    chosen: { [box.character.id]: 1 }, now: NOW,
  });
  assert.equal(Object.hasOwn(saved(box), "image"), false);
  assert.deepEqual(reuse(box, PRO).missing, box.doc.characters);
});

test("omitting the image selection preserves legacy reuse, including known old-model sheets", () => {
  for (const image of [undefined, PRO]) {
    const box = fixture();
    keep(box, image);
    const result = reuse(box);
    assert.deepEqual(result.missing, []);
    assert.deepEqual(Object.keys(result.reused), [box.character.id]);
    const candidate = result.reused[box.character.id];
    assert.deepEqual(candidate.image, image);
    assert.deepEqual(readFileSync(path.join(result.workdir, candidate.file)), box.bytes);
  }
});

test("keeping a reused sheet preserves its actual model instead of the enclosing manifest model", () => {
  const box = fixture();
  keep(box, PRO);
  const result = reuse(box);
  const reused = result.reused[box.character.id];
  assert.deepEqual(reused.image, PRO);

  const later = {
    ...box, workdir: result.workdir, doc: { ...box.doc, slug: "episode-two" },
    candidate: reused,
  };
  assert.equal(keep(later, FLASH), 1);
  assert.deepEqual(saved(box).image, PRO);
  assert.equal(saved(box).from, "episode-two");
  assert.equal(saved(box).sha256, SHA(box.bytes));
  assert.deepEqual(reuse(box, FLASH, "episode-three").missing, box.doc.characters);
  const matching = reuse(box, PRO, "episode-four");
  assert.deepEqual(matching.missing, []);
  assert.deepEqual(matching.reused[box.character.id].image, PRO);
});

test("resaving a legacy reused sheet cannot turn unknown provenance into the manifest model", () => {
  const box = fixture();
  keep(box);
  const result = reuse(box);
  const reused = result.reused[box.character.id];
  assert.equal(Object.hasOwn(reused, "image"), false);
  assert.equal(reused.reused_from, "episode-one");

  const later = {
    ...box, workdir: result.workdir, doc: { ...box.doc, slug: "episode-two" },
    candidate: reused,
  };
  assert.equal(keep(later, FLASH), 1);
  assert.equal(Object.hasOwn(saved(box), "image"), false, "unknown old bytes must stay unknown");
  assert.deepEqual(reuse(box, FLASH, "episode-three").missing, box.doc.characters);
  assert.deepEqual(reuse(box, undefined, "episode-four").missing, [], "legacy unscoped reuse still works");
});
