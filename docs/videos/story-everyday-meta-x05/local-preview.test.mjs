import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { layoutDrama } from "../../../tools/video/assemble/drama.mjs";
import { assessPreviewKeyframes, generatedPictureProblems, previewDurationProblems, previewDurations, previewSourcesChanged, previewStem, publishPreviewFiles, renderedCardEvidence, reviewSidecar, shiftPreviewCues, unsafeSelectedPicture } from "./local-preview.mjs";
import { INTRO_FRAMES, OUTRO_FRAMES, bookendedAudioArgs, conceptBookendArgs } from "./local-preview-bookends.mjs";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

function fixture(t) {
  const workdir = mkdtempSync(path.join(tmpdir(), "meta-local-preview-"));
  t.after(() => rmSync(workdir, { recursive: true, force: true }));
  mkdirSync(path.join(workdir, "keyframes"));
  const bytes = "selected concept still";
  const file = "keyframes/shot-one.png";
  writeFileSync(path.join(workdir, file), bytes);
  const doc = { scenes: [{ id: "shot-one", template: "shot", data: { visual: "still", camera: "locked" }, lines: [] }] };
  const shot = {
    file, sha256: sha(bytes), needs_review: true,
    judge: { overall: 6, passed: false, problems: ["unreadable movie card"] },
    problems: ["unreadable movie card", "text artifact"],
    takes: [{ seed: 1 }, { seed: 2 }, { seed: 3 }],
  };
  const manifest = { shots: { "shot-one": shot } };
  const timeline = { scenes: [{ id: "shot-one", start_frame: 0, end_frame: 90 }] };
  const frames = { scenes: [{ id: "shot-one", states: [] }] };
  return { workdir, doc, shot, manifest, timeline, frames, file };
}

test("a failed selected image remains blocked even in review-needed concept mode", async (t) => {
  const box = fixture(t);
  const strict = await assessPreviewKeyframes(box);
  assert.match(strict.issues.join("; "), /keyframe needs review/);
  assert.equal(strict.layoutKeyframes, box.manifest);
  assert.throws(() => layoutDrama(box.doc, box.timeline, box.frames, null, strict.layoutKeyframes), /needs_review/);
  assert.equal(previewStem(false, strict.reviewNeeded), "preview-review-needed");

  const concept = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(concept.issues.join("; "), /unpassed judge/);
  assert.equal(concept.layoutKeyframes, box.manifest);
  assert.equal(box.manifest.shots["shot-one"].needs_review, true);
  assert.equal(previewStem(true, concept.reviewNeeded), "preview-review-needed");
  assert.equal(previewStem(false, [], ["m050201"]), "preview-review-needed");
  assert.deepEqual(concept.reviewNeeded, [{
    id: "shot-one", needs_review: true, file: box.file, sha256: box.shot.sha256,
    judge_overall: 6, judge_passed: false, problems: ["unreadable movie card", "text artifact"], takes_count: 3,
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

test("review-needed concept cannot select an image with readable text or another hard redraw fault", async (t) => {
  const box = fixture(t);
  box.shot.judge = { overall: 9, passed: false, scores: { text: 0, subject: 0 }, problems: ["text: legible pseudo-English on a report"] };
  assert.deepEqual(unsafeSelectedPicture(box.shot), ["judge", "text", "subject"]);
  const assessed = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(assessed.issues.join("; "), /hard redraw fault \(judge, text, subject\)/);
  assert.equal(assessed.layoutKeyframes, box.manifest);
});

test("illustrated preview requires a passed MiniMax take, original cache bytes and paid receipt", async (t) => {
  const box = fixture(t);
  const original = "raw MiniMax image";
  const originalFile = "keyframes/shot-one-original.png";
  writeFileSync(path.join(box.workdir, originalFile), original);
  box.shot.key = "image-request-key";
  box.shot.judge = { passed: true, scores: { text: 10 } };
  box.shot.needs_review = false;
  box.shot.takes = [{ file: box.file, sha256: box.shot.sha256, key: box.shot.key, judge: box.shot.judge }];
  box.manifest.image = { provider: "minimax", model: "image-01" };
  const cache = { entries: { [box.shot.key]: { file: originalFile, sha256: sha(original), provider: "minimax", model: "image-01" } } };
  const receipt = { stage: "keyframes", kind: "image", id: "shot-one", key: box.shot.key, provider: "minimax", model: "image-01", status: "ready" };
  const ledger = { entries: [receipt] };
  assert.deepEqual(await generatedPictureProblems({ doc: box.doc, manifest: box.manifest, workdir: box.workdir, cache, ledger }), []);
  assert.match((await generatedPictureProblems({ doc: box.doc, manifest: box.manifest, workdir: box.workdir, cache, ledger: { entries: [] } })).join("; "), /absent from the paid-media image ledger/);
  box.shot.judge.passed = false;
  assert.match((await generatedPictureProblems({ doc: box.doc, manifest: box.manifest, workdir: box.workdir, cache, ledger })).join("; "), /not a passed generated take/);
});

test("end-frame evidence remains mandatory and the unapproved sidecar binds source and output hashes", async (t) => {
  const box = fixture(t);
  box.doc.scenes[0].data.end_frame = { prompt: "Empty return envelope" };
  const blocked = await assessPreviewKeyframes({ ...box, allowReviewNeeded: true });
  assert.match(blocked.issues.join("; "), /end frame has no selected picture/);
  assert.equal(blocked.layoutKeyframes, box.manifest);

  const reviewNeeded = blocked.reviewNeeded;
  const sidecar = reviewSidecar({
    doc: box.doc, stem: "preview-review-needed", scriptSha: "a".repeat(64), timelineSha: "f".repeat(64),
    audioCheckSha: "6".repeat(64), audioFlagsSha: "7".repeat(64), audioReviewNeeded: ["m050201"],
    narrationReview: { file: "narration-review.mp3", sha256: "8".repeat(64), spots: [{ id: "m050201", start_seconds: 50 }] },
    manifestSha: "b".repeat(64),
    framesSha: "1".repeat(64), musicSha: "2".repeat(64),
    musicProvenance: { source: "generated", slug: "story-everyday-netflix-x03", sha256: "4".repeat(64), original_manifest_sha256: "5".repeat(64) },
    cardFiles: [{ file: "frames/card.png", sha256: "3".repeat(64) }], reviewNeeded,
    outputSha: "c".repeat(64), srtSha: "d".repeat(64), vttSha: "e".repeat(64),
  });
  assert.equal(sidecar.approved, false);
  assert.equal(sidecar.official_branding, false);
  assert.equal(sidecar.kind, "unapproved-local-concept-preview");
  assert.equal(sidecar.video_json_sha256, "a".repeat(64));
  assert.equal(sidecar.timeline_sha256, "f".repeat(64));
  assert.equal(sidecar.audio_check_sha256, "6".repeat(64));
  assert.equal(sidecar.audio_flags_sha256, "7".repeat(64));
  assert.deepEqual(sidecar.audio_review_needed, ["m050201"]);
  assert.equal(sidecar.narration_review.spots[0].id, "m050201");
  assert.equal(sidecar.keyframes_manifest_sha256, "b".repeat(64));
  assert.equal(sidecar.frames_manifest_sha256, "1".repeat(64));
  assert.equal(sidecar.music_manifest_sha256, "2".repeat(64));
  assert.equal(sidecar.music_provenance.slug, "story-everyday-netflix-x03");
  assert.deepEqual(sidecar.rendered_card_files, [{ file: "frames/card.png", sha256: "3".repeat(64) }]);
  assert.equal(sidecar.review_needed[0].file, box.file);
  assert.equal(sidecar.review_needed[0].sha256, box.shot.sha256);
  assert.deepEqual(Object.values(sidecar.outputs).map(({ file }) => file), [
    "preview-review-needed.mp4", "preview-review-needed.zh-TW.srt", "preview-review-needed.zh-TW.vtt",
  ]);
  assert.equal(sidecar.outputs.mp4.sha256, "c".repeat(64));
});

test("clean stills still publish an unapproved concept sidecar with the clean stem", (t) => {
  const box = fixture(t);
  const sidecar = reviewSidecar({
    doc: box.doc, stem: "preview", scriptSha: "a".repeat(64), timelineSha: "b".repeat(64),
    manifestSha: "c".repeat(64), framesSha: "d".repeat(64), musicSha: "e".repeat(64),
    cardFiles: [], reviewNeeded: [], outputSha: "f".repeat(64), srtSha: "1".repeat(64), vttSha: "2".repeat(64),
  });
  assert.equal(sidecar.approved, false);
  assert.equal(sidecar.official_branding, false);
  assert.deepEqual(Object.values(sidecar.outputs).map(({ file }) => file), [
    "preview.mp4", "preview.zh-TW.srt", "preview.zh-TW.vtt",
  ]);
  assert.throws(() => reviewSidecar({ doc: box.doc, stem: "final", reviewNeeded: [] }), /invalid local preview stem/);
});

test("spoken body and hook timing are checked before the 5 s intro and 21 s end screen", () => {
  const doc = { scenes: [
    { id: "answer", template: "stats", lines: [{ id: "answer-line" }] },
    { id: "question", template: "shot", lines: [{ id: "question-line" }] },
    { id: "subscribe", template: "shot", lines: [{ id: "subscribe-line" }] },
  ] };
  const valid = { fps: 30, total_frames: 16_800, chapters: [{ start_frame: 0 }, { start_frame: 900 }],
    lines: [{ id: "answer-line", start_frame: 15_300 }, { id: "question-line", start_frame: 15_700 }, { id: "subscribe-line", start_frame: 16_000 }] };
  assert.deepEqual(previewDurationProblems(valid, doc), []);
  assert.deepEqual(previewDurations(valid, doc), { hookFrames: 900, afterHookFrames: 15_900, closingStartFrame: 15_300, substantiveBodyFrames: 14_400 });
  assert.match(previewDurationProblems({ ...valid, lines: [{ ...valid.lines[0], start_frame: 15_299 }, ...valid.lines.slice(1)] }, doc).join("; "), /at least eight minutes/,
    "the three narrated closing lines cannot rescue a body shorter than eight minutes");
  assert.match(previewDurationProblems({ ...valid, chapters: [{ start_frame: 0 }, { start_frame: 899 }] }, doc).join("; "), /30–60 seconds/);
  assert.match(previewDurationProblems({ ...valid, lines: [] }, doc).join("; "), /boundary is missing/);
  assert.equal(INTRO_FRAMES, 150);
  assert.equal(OUTRO_FRAMES, 630);
  const outroArgs = conceptBookendArgs("outro", "outro.mp4");
  assert.ok(outroArgs.includes("630"));
  assert.match(outroArgs.join(" "), /最符合觀眾喜好/);
  assert.match(outroArgs.join(" "), /最新上傳/);
  assert.match(outroArgs.join(" "), /訂閱/);
  assert.match(bookendedAudioArgs("body.m4a", "music.mp3", 14_400, 900, "full.m4a").join(" "), /concat=n=4/);
});

test("Meta native narrated outro card remains inside the body before the separate concept end screen", () => {
  const doc = { scenes: [
    { id: "shot-one", template: "shot", data: { visual: "still", camera: "locked" }, lines: [] },
    { id: "outro", template: "outro", data: { title: "兩條路", cta: "訂閱品牌故事" }, lines: [{ id: "m050619", text: "訂閱品牌故事。" }] },
  ] };
  const timeline = { scenes: [
    { id: "shot-one", start_frame: 0, end_frame: 90, states: [] },
    { id: "outro", start_frame: 90, end_frame: 150, states: [{ start_frame: 90, end_frame: 150 }] },
  ] };
  const frames = { scenes: [
    { id: "shot-one", states: [] },
    { id: "outro", states: [{ still: "frames/outro.png", transition: [] }] },
  ] };
  const keyframes = { shots: { "shot-one": { file: "keyframes/shot-one.png", sha256: "a".repeat(64) } } };
  const layout = layoutDrama(doc, timeline, frames, null, keyframes);
  assert.equal(layout[1].kind, "stills");
  assert.equal(layout[1].start_frame, 90);
  assert.deepEqual(layout[1].entries, [{ file: "frames/outro.png", frames: 60 }]);
});

test("rendered card evidence binds sorted unique paths and actual bytes", async (t) => {
  const dir = mkdtempSync(path.join(tmpdir(), "meta-preview-cards-"));
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
    scriptSha: "a", timelineSha: "b", audioCheckSha: "g", audioFlagsSha: "h", manifestSha: "c", framesSha: "d", musicSha: "e",
    cardFiles: [{ file: "frames/card.png", sha256: "f" }], reviewNeeded: [{ id: "shot-one" }],
  };
  assert.equal(previewSourcesChanged(before, { ...before }), false);
  for (const key of ["scriptSha", "timelineSha", "audioCheckSha", "audioFlagsSha", "manifestSha", "framesSha", "musicSha"]) {
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
  const dir = mkdtempSync(path.join(tmpdir(), "meta-preview-publish-"));
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
