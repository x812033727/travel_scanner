import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { adoptionRefusal, appliedBranding, brandingCurrent, brandingHash, pinBranding, presentationTimeline, readBranding, selectBrandingForBuild, shiftBrandingCues, validateBranding } from "./branding.mjs";

const preset = (n = "a") => ({ schema_version: 1, id: `mokaair-${n}`, intro: { file: "intro.mp4", sha256: n.repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } });
const doc = { format: "slides", youtube: { video_id: null } };
function box(t) {
  const workBase = mkdtempSync(path.join(os.tmpdir(), "video-branding-"));
  const workdir = path.join(workBase, "one");
  mkdirSync(workdir);
  mkdirSync(path.join(workBase, "_branding"));
  t.after(() => rmSync(workBase, { recursive: true, force: true }));
  const current = (value) => writeFileSync(path.join(workBase, "_branding", "current.json"), JSON.stringify(value));
  return { workdir, workBase, current };
}

test("only first builds adopt the current package; an unapproved old cut needs explicit adoption", async (t) => {
  const b = box(t);
  b.current(preset());
  const selected = await selectBrandingForBuild({ ...b, doc });
  assert.equal(selected.intro.frames, 150);
  assert.equal(readBranding(b.workdir), null, "a failed build must not pin a new selection over an old cut");
  writeFileSync(path.join(b.workdir, "checks.json"), JSON.stringify({ ok: true }));
  assert.equal(await selectBrandingForBuild({ ...b, doc }), null);
  assert.equal((await selectBrandingForBuild({ ...b, doc, adoptCurrent: true })).hash, selected.hash);
});

test("a first candidate that failed QA still adopts branding on retry; historical completed builds stay legacy", async (t) => {
  const b = box(t);
  b.current(preset());
  const history = path.join(b.workdir, "state.json");
  writeFileSync(history, JSON.stringify({ runs: [{ stage: "assemble", ok: false }, { stage: "compile", ok: false }] }));
  assert.equal((await selectBrandingForBuild({ ...b, doc })).hash, brandingHash(preset()));
  writeFileSync(history, JSON.stringify({ runs: [{ stage: "assemble" }, { stage: "assemble", ok: false }] }));
  assert.equal(await selectBrandingForBuild({ ...b, doc }), null, "old stage records without an ok field still prove a prior build");
});

test("published, approved, packaged and Short videos refuse adoption; completed source files may have been tidied", async (t) => {
  for (const proof of ["final", "publish", "youtube", "auto", "package", "history", "shorts"]) {
    const b = box(t);
    b.current(preset());
    let source = doc;
    if (["final", "publish"].includes(proof)) writeFileSync(path.join(b.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: proof, sha256: "old" }] }));
    if (proof === "youtube") source = { ...doc, youtube: { video_id: "abcdefghijk" } };
    if (proof === "auto") writeFileSync(path.join(b.workdir, "auto.json"), JSON.stringify({ status: "done", youtube_video_id: "abcdefghijk" }));
    if (proof === "package") {
      mkdirSync(path.join(b.workdir, "upload"));
      writeFileSync(path.join(b.workdir, "upload", "metadata.json"), "{}");
    }
    if (proof === "history") writeFileSync(path.join(b.workdir, "state.json"), JSON.stringify({ runs: [{ stage: "assemble" }] }));
    if (proof === "shorts") source = { format: "shorts" };
    assert.equal(await selectBrandingForBuild({ ...b, doc: source }), null, proof);
    if (proof !== "history") {
      assert.ok(adoptionRefusal({ doc: source, workdir: b.workdir }), proof);
      await assert.rejects(selectBrandingForBuild({ ...b, doc: source, adoptCurrent: true }), /unchanged|long videos/, proof);
    }
  }
});

test("a local pin wins over every later channel default, even an invalid one; legacy artifacts remain current", async (t) => {
  const b = box(t);
  b.current(preset());
  const chosen = await selectBrandingForBuild({ ...b, doc });
  pinBranding(b.workdir, chosen, new Date("2026-09-30T00:00:00Z"));
  const bytes = readFileSync(path.join(b.workdir, "branding.json"), "utf8");
  b.current({ invalid: true });
  assert.equal((await selectBrandingForBuild({ ...b, doc })).hash, chosen.hash);
  assert.equal(readFileSync(path.join(b.workdir, "branding.json"), "utf8"), bytes);
  assert.equal(brandingCurrent({ branding: { hash: chosen.hash } }, readBranding(b.workdir)), true);
  assert.equal(brandingCurrent({ ok: true }, null), true);
  assert.equal(brandingCurrent({ ok: true }, chosen), false);
  assert.equal(appliedBranding({ ok: true }), null);
});

test("branding is bound to source bytes and duration, not locations, labels or dates", () => {
  const original = preset();
  assert.equal(brandingHash(original), brandingHash({ ...original, id: "renamed", intro: { ...original.intro, file: "elsewhere.mp4" } }));
  assert.notEqual(brandingHash(original), brandingHash(preset("c")));
  assert.notEqual(brandingHash(original), brandingHash({ ...original, intro: { ...original.intro, frames: 149 } }));
  assert.throws(() => validateBranding({ ...original, hash: "wrong" }), /hash/);
  assert.throws(() => validateBranding({ ...original, outro: { ...original.outro, frames: -1 } }), /frames/);
});

test("presentation shifts content once, keeps chapter zero and does not change the approved narration", () => {
  const body = { fps: 30, total_frames: 900, lines: [{ id: "line", start_frame: 0, end_frame: 120 }], scenes: [{ id: "scene", start_frame: 0, end_frame: 900, states: [{ start_frame: 0, end_frame: 900 }] }], chapters: [{ title: "First", start_frame: 0 }, { title: "Second", start_frame: 600 }] };
  const original = structuredClone(body);
  const applied = { hash: brandingHash(preset()), intro_frames: 150, outro_frames: 90, body_frames: 900 };
  const full = presentationTimeline(body, applied);
  assert.deepEqual(body, original);
  assert.equal(full.total_frames, 1140);
  assert.equal(full.body_total_frames, 900);
  assert.equal(full.content_end_frame, 1050);
  assert.deepEqual(full.chapters.map((each) => each.start_frame), [0, 750]);
  assert.deepEqual([full.lines[0].start_frame, full.lines[0].end_frame], [150, 270]);
  assert.deepEqual(full.scenes[0].states, [{ start_frame: 150, end_frame: 1050 }]);
  assert.equal(presentationTimeline(full, applied), full, "a dubbed presentation timeline is not offset twice");
  assert.equal(presentationTimeline(body, null), body);
  const cues = [{ start_ms: 350, end_ms: 1350, text: "hello" }];
  assert.deepEqual(shiftBrandingCues(shiftBrandingCues(cues, applied), applied, -1), cues);
});
