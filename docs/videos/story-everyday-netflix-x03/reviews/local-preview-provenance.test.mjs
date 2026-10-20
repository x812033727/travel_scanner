import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { CHANGED_AUDIO_LINE_IDS, verifyPreviewReviewLineage } from "./local-preview-provenance.mjs";

const digest = (data) => createHash("sha256").update(data).digest("hex");
const text = (file) => readFileSync(file, "utf8");
const writeJson = (file, value) => writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const OLD = "a".repeat(64);
const CURRENT = "b".repeat(64);
const SERIES = "c".repeat(64);
const EVENT = "d".repeat(64);
const LEXICON = "e".repeat(64);
const SLUG = "story-everyday-netflix-x03";
const files = {
  original: ["source-review-release.md", "blind-a-release.md", "blind-b-release.md"],
  revised: ["source-review-audio-revision.md", "blind-a-audio-revision.md", "blind-b-audio-revision.md"],
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
    const bytes = `PASS: independent ${roles[index]} review of ${sha}\n`;
    writeFileSync(path.join(reviews, name), bytes);
    return { role: roles[index], file: `reviews/${name}`, sha256: digest(bytes) };
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
    video_json_sha256: CURRENT,
    previous_video_json_sha256: OLD,
    bootstrap_review_sha256: digest(text(bootstrapFile)),
    changed_line_ids: [...CHANGED_AUDIO_LINE_IDS],
    evidence: evidence("revised", CURRENT),
  };
  const revisionFile = path.join(reviews, "audio-revision-review.json");
  writeJson(revisionFile, revision);
  return { projectDir, reviews, bootstrap, bootstrapFile, sidecarFile, revision, revisionFile,
    verify: () => verifyPreviewReviewLineage({ projectDir, currentVideoSha: CURRENT, seriesSha: SERIES }) };
}

test("accepts a current script reviewed after a different immutable bootstrap script", (t) => {
  const f = fixture(t);
  const lineage = f.verify();
  assert.equal(lineage.historical_bootstrap.video_json_sha256, OLD);
  assert.equal(lineage.current_revision.video_json_sha256, CURRENT);
  assert.deepEqual(lineage.current_revision.changed_line_ids, CHANGED_AUDIO_LINE_IDS);
});

test("rejects current script or revised evidence drift", (t) => {
  const f = fixture(t);
  assert.throws(() => verifyPreviewReviewLineage({ projectDir: f.projectDir, currentVideoSha: "f".repeat(64), seriesSha: SERIES }), /current audio-revision script SHA drift/);
  writeFileSync(path.join(f.reviews, files.revised[0]), `PASS but changed ${CURRENT}\n`);
  assert.throws(f.verify, /review evidence SHA drift/);
});

test("rejects revisions detached from their historical bootstrap", (t) => {
  const f = fixture(t);
  f.revision.previous_video_json_sha256 = "f".repeat(64);
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /not based on the pinned script/);
  f.revision.previous_video_json_sha256 = OLD;
  writeJson(f.revisionFile, f.revision);
  f.bootstrap.reviewer = "new value changes historical receipt bytes";
  writeJson(f.bootstrapFile, f.bootstrap);
  assert.throws(f.verify, /immutable genesis review receipt SHA drift/);
});

test("rejects missing changed IDs and evidence that does not name the current script", (t) => {
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
  writeFileSync(outside, `PASS ${CURRENT}\n`);
  const file = path.join(f.reviews, files.revised[2]);
  rmSync(file);
  symlinkSync(outside, file);
  f.revision.evidence[2].sha256 = digest(text(outside));
  writeJson(f.revisionFile, f.revision);
  assert.throws(f.verify, /review evidence symlink escapes reviews/);
});
