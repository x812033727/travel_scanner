import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { UsageError } from "./paths.mjs";
import { CURRENT_WATERMARK, pinWatermark, readWatermarkPin, resolveWatermark, selectWatermarkForRender, watermark, WATERMARK_DIR, WATERMARK_FILE, watermarkDataUri, watermarkRecord, watermarkRefusal, WATERMARKS } from "./watermark.mjs";

const doc = { format: "slides", youtube: { video_id: null } };
function box(t) {
  const workBase = mkdtempSync(path.join(os.tmpdir(), "video-watermark-"));
  const workdir = path.join(workBase, "one");
  mkdirSync(workdir);
  t.after(() => rmSync(workBase, { recursive: true, force: true }));
  return workdir;
}

/** A PNG's width and height, from its IHDR chunk. */
const pngSize = (bytes) => ({ width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) });

test("every registered picture is on disk with the bytes and the size the registry says", () => {
  assert.ok(Object.hasOwn(WATERMARKS, CURRENT_WATERMARK));
  for (const [id, shapes] of Object.entries(WATERMARKS)) {
    assert.deepEqual(Object.keys(shapes).sort(), ["long", "shorts"], `${id} has both frame shapes`);
    for (const [shape, entry] of Object.entries(shapes)) {
      const bytes = readFileSync(path.join(WATERMARK_DIR, id, entry.file));
      assert.equal(createHash("sha256").update(bytes).digest("hex"), entry.sha256, `${id}/${shape}: a version is never edited in place`);
      assert.deepEqual(pngSize(bytes), { width: entry.box.width, height: entry.box.height }, `${id}/${shape}: the box is the picture's size`);
      assert.equal(bytes.readUInt8(25), 6, `${id}/${shape}: RGBA, so the ground stays transparent`);
    }
  }
});

test("the boxes sit where nothing else is drawn, on even pixels", () => {
  for (const [id, shapes] of Object.entries(WATERMARKS)) {
    for (const [shape, { box: place }] of Object.entries(shapes)) {
      for (const [name, value] of Object.entries(place)) assert.equal(value % 2, 0, `${id}/${shape}.${name} is even: the mark goes over 4:2:0 video`);
    }
    const long = shapes.long.box;
    // theme.css: the progress bar ends at y 36, the content area starts at y 170, and the chrome
    // ends 96 px from the right edge; the PNG carries 6 px of padding around its letters.
    assert.ok(long.y >= 36 && long.y + long.height <= 170, `${id}: between the progress bar and the content`);
    assert.equal(long.x + long.width - 6, 1920 - 96, `${id}: the letters end where the slides' chrome ends`);
    // shorts/core.mjs: the header row, right of the brand line, above the kicker at y 174; the
    // safe area is x 78–902 (docs/videos/SHORTS.md).
    const shorts = shapes.shorts.box;
    assert.ok(shorts.x >= 620 && shorts.x + shorts.width <= 902, `${id}: right of the brand line, inside the safe area`);
    assert.ok(shorts.y >= 60 && shorts.y + shorts.height <= 174, `${id}: in the header row`);
  }
});

test("a mark is read by version and shape, and refuses what this checkout does not hold", () => {
  const long = watermark();
  assert.equal(long.id, CURRENT_WATERMARK);
  assert.equal(long.shape, "long");
  assert.ok(path.isAbsolute(long.file));
  assert.deepEqual(watermarkRecord(long), { id: long.id, sha256: long.sha256, box: long.box });
  assert.equal(watermarkRecord(null), null);
  assert.notEqual(watermark(CURRENT_WATERMARK, "shorts").sha256, long.sha256);
  assert.throws(() => watermark("v0"), UsageError);
  assert.throws(() => watermark(CURRENT_WATERMARK, "square"), UsageError);
  assert.throws(() => watermark("constructor"), UsageError, "an inherited property is not a version");
  const uri = watermarkDataUri(long);
  assert.match(uri, /^data:image\/png;base64,/);
  assert.deepEqual(Buffer.from(uri.split(",")[1], "base64"), readFileSync(long.file));
});

test("a record resolves to its own shape, and a record of other bytes is refused", () => {
  const record = watermarkRecord(watermark());
  assert.equal(resolveWatermark(null), null);
  assert.equal(resolveWatermark(undefined), null);
  assert.equal(resolveWatermark(record).shape, "long");
  assert.equal(resolveWatermark(record, "shorts").shape, "shorts");
  assert.throws(() => resolveWatermark({ ...record, sha256: "0".repeat(64) }), /run render again/);
  assert.throws(() => resolveWatermark({ ...record, id: "v0" }), UsageError);
  assert.throws(() => resolveWatermark({ id: 1 }), UsageError);
});

test("a video drawn for the first time takes the current mark; one cut before it had a pin stays unmarked", (t) => {
  const workdir = box(t);
  assert.equal(selectWatermarkForRender({ doc, workdir }).id, CURRENT_WATERMARK);
  assert.equal(readWatermarkPin(workdir), null, "selecting pins nothing: render pins beside its manifest");
  for (const file of ["final.mp4", "checks.json"]) {
    const old = box(t);
    writeFileSync(path.join(old, file), "{}");
    assert.equal(selectWatermarkForRender({ doc, workdir: old }), null, `${file} means the cut exists`);
    assert.equal(selectWatermarkForRender({ doc, workdir: old, adopt: true }).id, CURRENT_WATERMARK, "an unapproved cut may adopt it");
  }
  const ran = box(t);
  writeFileSync(path.join(ran, "state.json"), JSON.stringify({ runs: [{ stage: "render", ok: true }, { stage: "assemble", ok: true }] }));
  assert.equal(selectWatermarkForRender({ doc, workdir: ran }), null);
  const failed = box(t);
  writeFileSync(path.join(failed, "state.json"), JSON.stringify({ runs: [{ stage: "render", ok: true }, { stage: "assemble", ok: false }] }));
  assert.equal(selectWatermarkForRender({ doc, workdir: failed }).id, CURRENT_WATERMARK, "a render before any cut is still a first drawing");
});

test("a pin outlives every later state of the video, and is written once", (t) => {
  const workdir = box(t);
  const mark = selectWatermarkForRender({ doc, workdir });
  pinWatermark(workdir, mark, new Date("2026-10-12T00:00:00Z"));
  const pin = JSON.parse(readFileSync(path.join(workdir, WATERMARK_FILE), "utf8"));
  assert.deepEqual(pin, { schema_version: 1, id: mark.id, sha256: mark.sha256, adopted_at: "2026-10-12T00:00:00.000Z" });
  pinWatermark(workdir, mark, new Date("2027-01-01T00:00:00Z"));
  assert.equal(JSON.parse(readFileSync(path.join(workdir, WATERMARK_FILE), "utf8")).adopted_at, "2026-10-12T00:00:00.000Z");
  writeFileSync(path.join(workdir, "final.mp4"), "cut");
  writeFileSync(path.join(workdir, "checks.json"), "{}");
  writeFileSync(path.join(workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final" }] }));
  assert.equal(selectWatermarkForRender({ doc, workdir }).id, mark.id, "an approved, pinned video is redrawn with its own mark");
  pinWatermark(box(t), null);
});

test("a pin that is malformed or names a version this checkout lacks stops the render", (t) => {
  const workdir = box(t);
  writeFileSync(path.join(workdir, WATERMARK_FILE), JSON.stringify({ id: CURRENT_WATERMARK }));
  assert.throws(() => selectWatermarkForRender({ doc, workdir }), /schema_version 1/);
  writeFileSync(path.join(workdir, WATERMARK_FILE), JSON.stringify({ schema_version: 1, id: "v0", sha256: "0".repeat(64) }));
  assert.throws(() => selectWatermarkForRender({ doc, workdir }), UsageError);
});

test("an approved, packaged or uploaded cut is never given a mark, even when asked", (t) => {
  const approved = box(t);
  writeFileSync(path.join(approved, "approvals.json"), JSON.stringify({ approvals: [{ gate: "audio" }, { gate: "final" }] }));
  const packaged = box(t);
  mkdirSync(path.join(packaged, "upload"));
  writeFileSync(path.join(packaged, "upload", "metadata.json"), "{}");
  const finished = box(t);
  writeFileSync(path.join(finished, "auto.json"), JSON.stringify({ status: "done" }));
  for (const workdir of [approved, packaged, finished]) {
    assert.ok(watermarkRefusal({ doc, workdir }));
    assert.equal(selectWatermarkForRender({ doc, workdir }), null);
    assert.throws(() => selectWatermarkForRender({ doc, workdir, adopt: true }), /stay as they are/);
  }
  const uploaded = box(t);
  assert.throws(() => selectWatermarkForRender({ doc: { ...doc, youtube: { video_id: "abc" } }, workdir: uploaded, adopt: true }), /already uploaded/);
  const audioOnly = box(t);
  writeFileSync(path.join(audioOnly, "approvals.json"), JSON.stringify({ approvals: [{ gate: "audio" }] }));
  assert.equal(watermarkRefusal({ doc, workdir: audioOnly }), null, "an audio approval is given before any picture exists");
  assert.equal(selectWatermarkForRender({ doc, workdir: audioOnly }).id, CURRENT_WATERMARK);
});
