import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { CHANGED_AUDIO_LINE_IDS, CHANGED_VISUAL_SCENE_IDS, displayedNarrationSha256, nonPromptDocumentSha256, verifyPreviewReviewLineage } from "./local-preview-provenance.mjs";

const digest = (data) => createHash("sha256").update(data).digest("hex");
const text = (file) => readFileSync(file, "utf8");
const writeJson = (file, value) => writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const OLD = "a".repeat(64);
const AUDIO = "b".repeat(64);
const SPEECH = "1".repeat(16);
const SERIES = "c".repeat(64);
const EVENT = "d".repeat(64);
const LEXICON = "e".repeat(64);
const SLUG = "story-everyday-netflix-x03";
const files = {
  original: ["source-review-release.md", "blind-a-release.md", "blind-b-release.md"],
  revised: ["source-review-audio-revision.md", "blind-a-audio-revision.md", "blind-b-audio-revision.md"],
  visual: ["source-review-visual-revision.md", "visual-prompt-review.md"],
  style: ["source-review-style-amendment.md", "visual-prompt-style-amendment.md"],
};
const roles = ["source", "narrative_a", "narrative_b"];

function fixture(t) {
  const projectDir = mkdtempSync(path.join(os.tmpdir(), "netflix-x03-review-lineage-"));
  t.after(() => rmSync(projectDir, { recursive: true, force: true }));
  const reviews = path.join(projectDir, "reviews");
  const lexicon = path.join(projectDir, "story-lexicon");
  const sidecars = path.join(lexicon, "manual-bootstraps");
  mkdirSync(reviews);
  mkdirSync(sidecars, { recursive: true });
  const evidence = (set, sha) => files[set].map((name, index) => {
    const role = set === "visual" || set === "style" ? ["source", "visual"][index] : roles[index];
    const bytes = `PASS: independent ${role} review of ${sha}\n`;
    writeFileSync(path.join(reviews, name), bytes);
    return { role, file: `reviews/${name}`, sha256: digest(bytes) };
  });
  const bootstrap = {
    schema_version: 1,
    kind: "manual_story_lexicon_bootstrap_review",
    slug: SLUG,
    decision: "pin_unspoken_manual_draft",
    video_json_sha256: OLD,
    series_json_sha256: SERIES,
    evidence: evidence("original", OLD),
  };
  const bootstrapFile = path.join(reviews, "lexicon-bootstrap.json");
  writeJson(bootstrapFile, bootstrap);
  writeJson(path.join(lexicon, "current.json"), { slug: SLUG, head_event_sha256: EVENT, lexicon_sha256: LEXICON });
  const sidecarFile = path.join(sidecars, `${EVENT}.json`);
  writeJson(sidecarFile, {
    event_sha256: EVENT,
    lexicon_sha256: LEXICON,
    video_json_sha256: OLD,
    series_json_sha256: SERIES,
    review_receipt_sha256: digest(text(bootstrapFile)),
    evidence: bootstrap.evidence,
  });
  const revision = {
    schema_version: 1,
    kind: "story_audio_revision_review",
    slug: SLUG,
    decision: "reviewed_script_revision_pass",
    scope: "text_only",
    video_json_sha256: AUDIO,
    previous_video_json_sha256: OLD,
    bootstrap_review_sha256: digest(text(bootstrapFile)),
    changed_line_ids: [...CHANGED_AUDIO_LINE_IDS],
    evidence: evidence("revised", AUDIO),
  };
  const revisionFile = path.join(reviews, "audio-revision-review.json");
  writeJson(revisionFile, revision);
  const beforeStyle = { slug: SLUG, look: { preset: "cute-mystery" }, voice: { name: "synthetic" }, scenes: CHANGED_VISUAL_SCENE_IDS.map((id) => ({
    id, template: "shot", data: { prompt: `object-only shot for ${id}`, camera: "static" },
    lines: [{ id: id.slice(6), text: `spoken words for ${id}` }],
  })) };
  const visualSha = digest(`${JSON.stringify(beforeStyle, null, 2)}\n`);
  const currentDoc = structuredClone(beforeStyle);
  currentDoc.look.style = "objects have no faces or mascot features";
  const currentSha = digest(`${JSON.stringify(currentDoc, null, 2)}\n`);
  const visual = {
    schema_version: 1,
    kind: "story_visual_prompt_revision_review",
    slug: SLUG,
    decision: "reviewed_visual_prompt_revision_pass",
    scope: "visual_prompts_only",
    previous_video_json_sha256: AUDIO,
    video_json_sha256: visualSha,
    audio_revision_review_sha256: digest(text(revisionFile)),
    speech_hash: SPEECH,
    displayed_narration_sha256: displayedNarrationSha256(beforeStyle),
    non_prompt_document_sha256: nonPromptDocumentSha256(beforeStyle),
    changed_visual_scene_ids: [...CHANGED_VISUAL_SCENE_IDS],
    evidence: evidence("visual", visualSha),
  };
  const visualFile = path.join(reviews, "visual-prompt-revision.json");
  writeJson(visualFile, visual);
  const style = {
    schema_version: 1,
    kind: "story_visual_style_amendment_review",
    slug: SLUG,
    decision: "reviewed_visual_style_amendment_pass",
    scope: "look_style_only",
    previous_video_json_sha256: visualSha,
    video_json_sha256: currentSha,
    previous_visual_review_sha256: digest(text(visualFile)),
    changed_json_pointers: ["/look/style"],
    speech_hash: SPEECH,
    displayed_narration_sha256: displayedNarrationSha256(currentDoc),
    non_prompt_document_sha256: nonPromptDocumentSha256(currentDoc),
    evidence: evidence("style", currentSha),
  };
  const styleFile = path.join(reviews, "visual-style-amendment.json");
  writeJson(styleFile, style);
  return { projectDir, reviews, bootstrap, bootstrapFile, sidecarFile, revision, revisionFile, currentDoc, visual, visualFile, style, styleFile, visualSha, currentSha,
    verify: () => verifyPreviewReviewLineage({ projectDir, currentVideoSha: currentSha, seriesSha: SERIES, currentDoc, currentSpeechHash: SPEECH }) };
}

test("accepts an immutable bootstrap, audio and visual revisions, then a style-only amendment", (t) => {
  const f = fixture(t);
  const lineage = f.verify();
  assert.equal(lineage.historical_bootstrap.video_json_sha256, OLD);
  assert.equal(lineage.audio_revision.video_json_sha256, AUDIO);
  assert.equal(lineage.visual_revision.video_json_sha256, f.visualSha);
  assert.equal(lineage.visual_style_amendment.video_json_sha256, f.currentSha);
  assert.deepEqual(lineage.audio_revision.changed_line_ids, CHANGED_AUDIO_LINE_IDS);
  assert.deepEqual(lineage.visual_revision.changed_visual_scene_ids, CHANGED_VISUAL_SCENE_IDS);
  assert.deepEqual(lineage.visual_style_amendment.changed_json_pointers, ["/look/style"]);
});

test("rejects current visual script or prior audio evidence drift", (t) => {
  const f = fixture(t);
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: "9".repeat(64), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /current script is not canonical JSON or has drifted/);
  writeFileSync(path.join(f.reviews, files.revised[0]), `PASS but changed ${AUDIO}\n`);
  assert.throws(f.verify, /review evidence SHA drift/);
});

test("rejects revisions detached from their historical bootstrap", (t) => {
  const f = fixture(t);
  f.revision.previous_video_json_sha256 = "9".repeat(64);
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /not based on the pinned script/);
  f.revision.previous_video_json_sha256 = OLD;
  writeJson(f.revisionFile, f.revision);
  f.bootstrap.reviewer = "new value changes historical receipt bytes";
  writeJson(f.bootstrapFile, f.bootstrap);
  assert.throws(f.verify, /immutable genesis review receipt SHA drift/);
});

test("rejects missing audio changed IDs and evidence that does not name its script", (t) => {
  const f = fixture(t);
  f.revision.changed_line_ids.pop();
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /changed-line set/);
  f.revision.changed_line_ids = [...CHANGED_AUDIO_LINE_IDS];
  const file = path.join(f.reviews, files.revised[1]);
  writeFileSync(file, "PASS: a review that does not bind the script\n");
  f.revision.evidence[1].sha256 = digest(text(file));
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /does not mention its script SHA/);
});

test("rejects evidence symlinks that escape the project reviews directory", (t) => {
  const f = fixture(t);
  const outside = path.join(f.projectDir, "outside.md");
  writeFileSync(outside, `PASS ${AUDIO}\n`);
  const file = path.join(f.reviews, files.revised[2]);
  rmSync(file);
  symlinkSync(outside, file);
  f.revision.evidence[2].sha256 = digest(text(outside));
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /review evidence symlink escapes reviews/);
});

test("rejects visual receipts disconnected from the audio receipt or speech timeline", (t) => {
  const f = fixture(t);
  f.visual.audio_revision_review_sha256 = "9".repeat(64);
  writeJson(f.visualFile, f.visual);
  assert.throws(f.verify, /references a different audio receipt/);
  f.visual.audio_revision_review_sha256 = digest(text(f.revisionFile));
  f.visual.speech_hash = "2".repeat(16);
  writeJson(f.visualFile, f.visual);
  assert.throws(f.verify, /changed the measured speech hash/);
});

test("rejects changes beyond look.style and a changed historical visual-scene set", (t) => {
  const f = fixture(t);
  f.currentDoc.scenes[0].data.camera = "tracking";
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: digest(`${JSON.stringify(f.currentDoc, null, 2)}\n`), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /style-free script does not reconstruct/);
  f.currentDoc.scenes[0].data.camera = "static";
  f.currentDoc.scenes[0].lines[0].text = "different displayed text";
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: digest(`${JSON.stringify(f.currentDoc, null, 2)}\n`), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /style-free script does not reconstruct/);
  f.currentDoc.scenes[0].lines[0].text = `spoken words for ${CHANGED_VISUAL_SCENE_IDS[0]}`;
  f.visual.changed_visual_scene_ids.pop();
  writeJson(f.visualFile, f.visual);
  assert.throws(f.verify, /changed-scene list/);
});

test("rejects changes to shot prompts after the visual receipt is frozen", (t) => {
  const f = fixture(t);
  f.currentDoc.scenes[0].data.prompt = "revised object-only prompt";
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: digest(`${JSON.stringify(f.currentDoc, null, 2)}\n`), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /style-free script does not reconstruct/);
  f.currentDoc.scenes[0].data.prompt = `object-only shot for ${CHANGED_VISUAL_SCENE_IDS[0]}`;
  const visualFile = path.join(f.reviews, files.visual[1]);
  writeFileSync(visualFile, `PASS: but no bound script SHA\n`);
  f.visual.evidence[1].sha256 = digest(text(visualFile));
  writeJson(f.visualFile, f.visual);
  assert.throws(f.verify, /does not mention its script SHA/);
});

test("rejects style receipt and style evidence drift independently", (t) => {
  const f = fixture(t);
  f.style.previous_visual_review_sha256 = "9".repeat(64);
  writeJson(f.styleFile, f.style);
  assert.throws(f.verify, /references a different visual receipt/);
  f.style.previous_visual_review_sha256 = digest(text(f.visualFile));
  f.style.changed_json_pointers = ["/look/style", "/scenes/0/data/prompt"];
  writeJson(f.styleFile, f.style);
  assert.throws(f.verify, /changed-field list/);
  f.style.changed_json_pointers = ["/look/style"];
  writeJson(f.styleFile, f.style);
  const file = path.join(f.reviews, files.style[0]);
  writeFileSync(file, "PASS but no current script hash\n");
  f.style.evidence[0].sha256 = digest(text(file));
  writeJson(f.styleFile, f.style);
  assert.throws(f.verify, /does not mention its script SHA/);
});

test("the only accepted style edit is an added look.style field", (t) => {
  const f = fixture(t);
  f.currentDoc.look.style = "a different style";
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: digest(`${JSON.stringify(f.currentDoc, null, 2)}\n`), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /current style-amendment script SHA drift/);
  delete f.currentDoc.look.style;
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: digest(`${JSON.stringify(f.currentDoc, null, 2)}\n`), seriesSha: SERIES, currentDoc: f.currentDoc, currentSpeechHash: SPEECH }), /style amendment is missing look.style/);
});
