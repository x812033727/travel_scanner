import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { layoutDrama } from "../../../tools/video/assemble/drama.mjs";
import { assessPreviewKeyframes, previewSourcesChanged, previewStem, publishPreviewFiles, renderedCardEvidence, reviewSidecar, shiftPreviewCues } from "./local-preview.mjs";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

function fixture(t) {
  const workdir = mkdtempSync(path.join(tmpdir(), "dominos-local-preview-"));
  t.after(() => rmSync(workdir, { recursive: true, force: true }));
  mkdirSync(path.join(workdir, "keyframes"));
  const bytes = "selected concept still";
  const file = "keyframes/shot-one.png";
  writeFileSync(path.join(workdir, file), bytes);
  const doc = { scenes: [{ id: "shot-one", template: "shot", data: { visual: "still", camera: "locked" }, lines: [] }] };
  const shot = {
    file, sha256: sha(bytes), needs_review: true,
    judge: { overall: 6, passed: false, problems: ["wrong pizza box"] },
    problems: ["wrong pizza box", "text artifact"],
    takes: [{ seed: 1 }, { seed: 2 }, { seed: 3 }],
  };
  const manifest = { shots: { "shot-one": shot } };
  const timeline = { scenes: [{ id: "shot-one", start_frame: 0, end_frame: 90 }] };
  const frames = { scenes: [{ id: "shot-one", states: [] }] };
  return { workdir, doc, shot, manifest, timeline, frames, file };
}

test("review-needed concept requires an explicit flag and changes only the local layout copy", async (t) => {
  const box = fixture(t);
  const strict = await assessPreviewKeyframes(box);
  assert.deepEqual(strict.issues, ["shot-one keyframe needs review"]);
  assert.equal(strict.layoutKeyframes, box.manifest);
  assert.throws(() => layoutDrama(box.doc, box.timeline, box.frames, null, strict.layoutKeyframes), /needs_review/);
  assert.equal(previewStem(false, strict.reviewNeeded), "preview");

  const concept = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.deepEqual(concept.issues, []);
  assert.notEqual(concept.layoutKeyframes, box.manifest);
  assert.equal(concept.layoutKeyframes.shots["shot-one"].needs_review, false);
  assert.equal(box.manifest.shots["shot-one"].needs_review, true);
  assert.equal(concept.layoutKeyframes.shots["shot-one"].sha256, box.shot.sha256);
  assert.equal(layoutDrama(box.doc, box.timeline, box.frames, null, concept.layoutKeyframes)[0].keyframe.file, box.file);
  assert.equal(previewStem(true, concept.reviewNeeded), "preview-review-needed");
  assert.deepEqual(concept.reviewNeeded, [{
    id: "shot-one", needs_review: true, file: box.file, sha256: box.shot.sha256,
    judge_overall: 6, judge_passed: false, problems: ["wrong pizza box", "text artifact"], takes_count: 3,
  }]);
});

test("explicit review mode still rejects missing, incomplete and changed picture evidence", async (t) => {
  const box = fixture(t);
  box.shot.incomplete = true;
  let result = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(result.issues.join("; "), /keyframe is incomplete/);
  assert.equal(result.layoutKeyframes, box.manifest);

  delete box.shot.incomplete;
  box.shot.sha256 = "bad";
  result = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(result.issues.join("; "), /has no selected picture hash/);
  assert.equal(result.layoutKeyframes, box.manifest);

  box.shot.sha256 = "f".repeat(64);
  result = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(result.issues.join("; "), /selected picture has changed/);
  assert.equal(result.layoutKeyframes, box.manifest);

  box.shot.file = "keyframes/missing.png";
  result = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(result.issues.join("; "), /selected picture is missing/);
  assert.equal(result.layoutKeyframes, box.manifest);

  box.shot.file = "../escape.png";
  result = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(result.issues.join("; "), /selected picture is missing/);
  assert.equal(result.layoutKeyframes, box.manifest);
});

test("end-frame evidence remains mandatory and the unapproved sidecar binds source and output hashes", async (t) => {
  const box = fixture(t);
  box.doc.scenes[0].data.end_frame = { prompt: "Empty delivery table" };
  const blocked = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(blocked.issues.join("; "), /end frame has no selected picture/);
  assert.equal(blocked.layoutKeyframes, box.manifest);

  const reviewNeeded = blocked.reviewNeeded;
  const sidecar = reviewSidecar({
    doc: box.doc, scriptSha: "a".repeat(64), timelineSha: "f".repeat(64), manifestSha: "b".repeat(64),
    framesSha: "1".repeat(64), musicSha: "2".repeat(64), cardFiles: [{ file: "frames/card.png", sha256: "3".repeat(64) }], reviewNeeded,
    outputSha: "c".repeat(64), srtSha: "d".repeat(64), vttSha: "e".repeat(64),
  });
  assert.equal(sidecar.approved, false);
  assert.equal(sidecar.kind, "unapproved-local-concept-preview");
  assert.equal(sidecar.video_json_sha256, "a".repeat(64));
  assert.equal(sidecar.timeline_sha256, "f".repeat(64));
  assert.equal(sidecar.keyframes_manifest_sha256, "b".repeat(64));
  assert.equal(sidecar.frames_manifest_sha256, "1".repeat(64));
  assert.equal(sidecar.music_manifest_sha256, "2".repeat(64));
  assert.deepEqual(sidecar.rendered_card_files, [{ file: "frames/card.png", sha256: "3".repeat(64) }]);
  assert.equal(sidecar.review_needed[0].file, box.file);
  assert.equal(sidecar.review_needed[0].sha256, box.shot.sha256);
  assert.deepEqual(Object.values(sidecar.outputs).map(({ file }) => file), [
    "preview-review-needed.mp4", "preview-review-needed.zh-TW.srt", "preview-review-needed.zh-TW.vtt",
  ]);
  assert.equal(sidecar.outputs.mp4.sha256, "c".repeat(64));
});

test("rendered card evidence binds sorted unique paths and actual bytes", async (t) => {
  const dir = mkdtempSync(path.join(tmpdir(), "dominos-preview-cards-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  mkdirSync(path.join(dir, "frames"));
  writeFileSync(path.join(dir, "frames", "a.png"), "first frame");
  writeFileSync(path.join(dir, "frames", "b.png"), "second frame");
  const frames = { scenes: [{ states: [{ still: "frames/b.png", transition: ["frames/a.png", "frames/b.png"] }] }] };
  const before = await renderedCardEvidence(frames, dir);
  assert.deepEqual(before, { issues: [], files: [
    { file: "frames/a.png", sha256: sha("first frame") },
    { file: "frames/b.png", sha256: sha("second frame") },
  ] });
  writeFileSync(path.join(dir, "frames", "a.png"), "changed frame");
  const after = await renderedCardEvidence(frames, dir);
  assert.equal(after.files[0].sha256, sha("changed frame"));
  assert.equal(previewSourcesChanged({ cardFiles: before.files }, { cardFiles: after.files }), true);
  rmSync(path.join(dir, "frames", "a.png"));
  assert.match((await renderedCardEvidence(frames, dir)).issues.join("; "), /rendered card frame is missing: frames\/a\.png/);
});

test("publication rejects changes to every bound media manifest", () => {
  const before = {
    scriptSha: "a", timelineSha: "b", manifestSha: "c", framesSha: "d", musicSha: "e",
    cardFiles: [{ file: "frames/card.png", sha256: "f" }], reviewNeeded: [{ id: "shot-one" }],
  };
  assert.equal(previewSourcesChanged(before, { ...before }), false);
  for (const key of ["scriptSha", "timelineSha", "manifestSha", "framesSha", "musicSha"]) {
    assert.equal(previewSourcesChanged(before, { ...before, [key]: "changed" }), true, key);
  }
  assert.equal(previewSourcesChanged(before, { ...before, reviewNeeded: [] }), true);
});

test("the rounded first cue of chapter two moves after the 5 s intro while the hook stays put", () => {
  const timeline = { lines: [
    { id: "hook-last", start_frame: 1358 },
    { id: "chapter-two-first", start_frame: 1516 },
    { id: "chapter-two-next", start_frame: 1726 },
  ] };
  const cues = [
    { line: "hook-last", start_ms: 45267, end_ms: 49907, text: "hook" },
    { line: "chapter-two-first", start_ms: 50533, end_ms: 56923, text: "first" },
    { line: "chapter-two-next", start_ms: 57533, end_ms: 61423, text: "next" },
  ];
  const placed = shiftPreviewCues(cues, timeline, 1516);
  assert.deepEqual(placed.map(({ start_ms, end_ms }) => [start_ms, end_ms]), [
    [45267, 49907], [55533, 61923], [62533, 66423],
  ]);
  assert.equal(cues[1].start_ms, 50533, "source cues are unchanged");
  assert.throws(() => shiftPreviewCues([{ line: "missing", start_ms: 0, end_ms: 10 }], timeline, 1516), /no timeline line/);
});

test("review evidence and captions publish before the MP4 completion marker", (t) => {
  const dir = mkdtempSync(path.join(tmpdir(), "dominos-preview-publish-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const output = path.join(dir, "preview-review-needed.mp4");
  const srt = path.join(dir, "preview-review-needed.zh-TW.srt");
  const vtt = path.join(dir, "preview-review-needed.zh-TW.vtt");
  const sidecar = path.join(dir, "preview-review-needed.json");
  const partial = `${output}.partial.mp4`;
  const srtPartial = `${srt}.partial`;
  const vttPartial = `${vtt}.partial`;
  const sidecarPartial = `${sidecar}.partial`;
  const files = { partial, output, srtPartial, srt, vttPartial, vtt, sidecarPartial, sidecar, force: true };

  writeFileSync(output, "old video");
  writeFileSync(sidecar, "old evidence");
  writeFileSync(srtPartial, "new captions");
  writeFileSync(vttPartial, "new VTT");
  writeFileSync(sidecarPartial, "new evidence");
  assert.throws(() => publishPreviewFiles(files), { code: "ENOENT" }, "a failed video publish cannot leave the old MP4 with new evidence");
  assert.equal(existsSync(output), false);
  assert.equal(readFileSync(sidecar, "utf8"), "new evidence");

  writeFileSync(partial, "new video");
  writeFileSync(srtPartial, "new captions");
  writeFileSync(vttPartial, "new VTT");
  writeFileSync(sidecarPartial, "new evidence");
  publishPreviewFiles(files);
  assert.equal(readFileSync(output, "utf8"), "new video");
  assert.equal(readFileSync(srt, "utf8"), "new captions");
  assert.equal(readFileSync(vtt, "utf8"), "new VTT");
  assert.equal(readFileSync(sidecar, "utf8"), "new evidence");
  assert.equal(existsSync(partial), false);
});
