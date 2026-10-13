import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { adoptionRefusal, appliedBranding, brandingCurrent, brandingHash, currentBrandingFile, defaultIntroAt, INTRO_AFTER_FIRST_CHAPTER, INTRO_AT_START, introAtFrame, linesAcrossIntro, narratedLong, pinBranding, pinRecord, placeBranding, presentationTimeline, readBranding, replacementRefusal, selectBrandingForBuild, shiftBrandingCues, validateBranding } from "./branding.mjs";

const preset = (n = "a") => ({ schema_version: 1, id: `mokaair-${n}`, intro: { file: "intro.mp4", sha256: n.repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } });
const doc = { format: "slides", youtube: { video_id: null } };
function box(t) {
  const workBase = mkdtempSync(path.join(os.tmpdir(), "video-branding-"));
  const workdir = path.join(workBase, "one");
  mkdirSync(workdir);
  mkdirSync(path.join(workBase, "_branding"));
  t.after(() => rmSync(workBase, { recursive: true, force: true }));
  const current = (value, series = null) => {
    const file = path.join(workBase, currentBrandingFile(series));
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, JSON.stringify(value));
  };
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

const explainer = { format: "drama", look: { preset: "flat-explainer" } };
const seriesPreset = () => ({ ...preset("c"), intro: { ...preset("c").intro, frames: 357 } });

test("only new explainers use the series default; absent, disabled and invalid registries differ", async (t) => {
  const b = box(t);
  b.current(preset());
  assert.equal((await selectBrandingForBuild({ ...b, doc: explainer })).intro.frames, 150);
  b.current(seriesPreset(), "sothatswhy");
  assert.equal((await selectBrandingForBuild({ ...b, doc: explainer })).intro.frames, 357);
  assert.equal((await selectBrandingForBuild({ ...b, doc: explainer, adoptCurrent: true })).intro.frames, 357);
  // cute-cartoon is So That's Why redrawn, so it keeps the series' bookends; cute-mystery is
  // another series' explainer and wears the channel's until it has bookends of its own.
  assert.equal((await selectBrandingForBuild({ ...b, doc: { format: "drama", look: { preset: "cute-cartoon" } } })).intro.frames, 357);
  for (const other of [doc, { format: "screencast" }, { format: "drama", look: { preset: "anime" } }, { format: "drama", look: { preset: "cute-mystery" } }, { ...doc, title: "原來如此", look: { preset: "flat-explainer" } }]) {
    assert.equal((await selectBrandingForBuild({ ...b, doc: other })).intro.frames, 150);
  }
  assert.equal(await selectBrandingForBuild({ ...b, doc: { format: "shorts", look: explainer.look } }), null);
  b.current({ enabled: false }, "sothatswhy");
  assert.equal(await selectBrandingForBuild({ ...b, doc: explainer }), null);
  await assert.rejects(selectBrandingForBuild({ ...b, doc: explainer, adoptCurrent: true }), /no current branding/);
  b.current({ invalid: true }, "sothatswhy");
  await assert.rejects(selectBrandingForBuild({ ...b, doc: explainer }), /schema_version/);
  assert.equal((await selectBrandingForBuild({ ...b, doc })).intro.frames, 150);
});

test("series defaults cannot alter existing pins or protected and legacy explainers", async (t) => {
  const b = box(t);
  b.current(preset());
  const pinned = await selectBrandingForBuild({ ...b, doc: explainer });
  pinBranding(b.workdir, pinned);
  b.current({ invalid: true }, "sothatswhy");
  b.current({ invalid: true });
  assert.equal((await selectBrandingForBuild({ ...b, doc: explainer })).hash, pinned.hash);
  for (const proof of ["final", "publish", "youtube", "auto", "package", "history", "checks"]) {
    const c = box(t);
    c.current({ invalid: true }, "sothatswhy");
    let source = explainer;
    if (["final", "publish"].includes(proof)) writeFileSync(path.join(c.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: proof, sha256: "old" }] }));
    if (proof === "youtube") source = { ...explainer, youtube: { video_id: "abcdefghijk" } };
    if (proof === "auto") writeFileSync(path.join(c.workdir, "auto.json"), JSON.stringify({ status: "done" }));
    if (proof === "package") { mkdirSync(path.join(c.workdir, "upload")); writeFileSync(path.join(c.workdir, "upload", "metadata.json"), "{}"); }
    if (proof === "history") writeFileSync(path.join(c.workdir, "state.json"), JSON.stringify({ runs: [{ stage: "assemble" }] }));
    if (proof === "checks") writeFileSync(path.join(c.workdir, "checks.json"), "{}");
    assert.equal(await selectBrandingForBuild({ ...c, doc: source }), null, proof);
    if (!["history", "checks"].includes(proof)) await assert.rejects(selectBrandingForBuild({ ...c, doc: source, adoptCurrent: true }), /unchanged/);
  }
});

test("11.9-second series presentation offsets captions, windows and chapters once", () => {
  const body = { total_frames: 900, lines: [{ start_frame: 0, end_frame: 120 }], windows: [{ start_frame: 0, end_frame: 900 }], chapters: [{ start_frame: 0 }, { start_frame: 600 }] };
  const original = structuredClone(body);
  const applied = { hash: brandingHash(seriesPreset()), intro_frames: 357, outro_frames: 90 };
  const full = presentationTimeline(body, applied);
  assert.deepEqual(body, original);
  assert.equal(full.total_frames, 1347);
  assert.equal(full.content_end_frame, 1257);
  assert.deepEqual(full.lines, [{ start_frame: 357, end_frame: 477 }]);
  assert.deepEqual(full.windows, [{ start_frame: 357, end_frame: 1257 }]);
  assert.deepEqual(full.chapters.map(chapter => chapter.start_frame), [0, 957]);
  assert.equal(presentationTimeline(full, applied), full);
  const cues = [{ start_ms: 0, end_ms: 4000, text: "正文" }];
  assert.deepEqual(shiftBrandingCues(cues, applied), [{ start_ms: 11900, end_ms: 15900, text: "正文" }]);
  assert.deepEqual(shiftBrandingCues(shiftBrandingCues(cues, applied), applied, -1), cues);
});

test("a first candidate that failed QA still adopts branding on retry; historical completed builds stay legacy", async (t) => {
  const b = box(t);
  b.current(preset());
  const history = path.join(b.workdir, "state.json");
  writeFileSync(history, JSON.stringify({ runs: [{ stage: "assemble", ok: false }, { stage: "compile", ok: false }] }));
  assert.equal((await selectBrandingForBuild({ ...b, doc })).hash, brandingHash({ ...preset(), intro_at: "after_first_chapter" }), "a new narrated build plays its intro after the condensation");
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

test("an approved cut whose script, narration or storyboard was approved again is being remade and may take the current bookends", async (t) => {
  const b = box(t);
  b.current(preset());
  const approvals = (entries) => writeFileSync(path.join(b.workdir, "approvals.json"), JSON.stringify({ approvals: entries }));
  mkdirSync(path.join(b.workdir, "upload"));
  writeFileSync(path.join(b.workdir, "upload", "metadata.json"), "{}");
  const final = { gate: "final", sha256: "old", approved_at: "2026-10-13T09:00:00Z" };
  approvals([{ gate: "storyboard", sha256: "a", approved_at: "2026-10-12T09:00:00Z" }, final]);
  assert.match(adoptionRefusal({ doc, workdir: b.workdir }), /final or publish approval/, "content approved before the cut: the cut stands");
  approvals([final, { gate: "script", sha256: "b", approved_at: "2026-10-13T12:00:00Z" }]);
  assert.equal(adoptionRefusal({ doc, workdir: b.workdir }), null, "a script approved after the cut: the cut is being remade, package and all");
  approvals([final, { gate: "publish", sha256: "c", approved_at: "2026-10-13T13:00:00Z" }, { gate: "audio", sha256: "d", approved_at: "2026-10-13T12:00:00Z" }]);
  assert.match(adoptionRefusal({ doc, workdir: b.workdir }), /final or publish approval/, "a publish approval newer than the content: the cut stands");
  approvals([{ gate: "script", sha256: "e", approved_at: "2026-10-13T12:00:00Z" }, { gate: "final", sha256: "f" }]);
  assert.match(adoptionRefusal({ doc, workdir: b.workdir }), /final or publish approval/, "a final with no time is never taken for an older one");
  approvals([final, { gate: "storyboard", sha256: "g", approved_at: "2026-10-13T14:00:00Z" }]);
  writeFileSync(path.join(b.workdir, "auto.json"), JSON.stringify({ status: "done" }));
  assert.match(adoptionRefusal({ doc, workdir: b.workdir }), /uploaded or finished/, "a finished video stays as it is, remade or not");
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
  const body = { fps: 30, total_frames: 900, lines: [{ id: "line", start_frame: 0, end_frame: 120 }], actions: [{ scene: "action", start_frame: 120, end_frame: 210 }], scenes: [{ id: "scene", start_frame: 0, end_frame: 900, states: [{ start_frame: 0, end_frame: 900 }] }], chapters: [{ title: "First", start_frame: 0 }, { title: "Second", start_frame: 600 }] };
  const original = structuredClone(body);
  const applied = { hash: brandingHash(preset()), intro_frames: 150, outro_frames: 90, body_frames: 900 };
  const full = presentationTimeline(body, applied);
  assert.deepEqual(body, original);
  assert.equal(full.total_frames, 1140);
  assert.equal(full.body_total_frames, 900);
  assert.equal(full.content_end_frame, 1050);
  assert.deepEqual(full.chapters.map((each) => each.start_frame), [0, 750]);
  assert.deepEqual([full.lines[0].start_frame, full.lines[0].end_frame], [150, 270]);
  assert.deepEqual(full.actions, [{ scene: "action", start_frame: 270, end_frame: 360 }]);
  assert.deepEqual(full.scenes[0].states, [{ start_frame: 150, end_frame: 1050 }]);
  assert.equal(presentationTimeline(full, applied), full, "a dubbed presentation timeline is not offset twice");
  assert.equal(presentationTimeline(body, null), body);
  const cues = [{ start_ms: 350, end_ms: 1350, text: "hello" }];
  assert.deepEqual(shiftBrandingCues(shiftBrandingCues(cues, applied), applied, -1), cues);
});

// docs/videos/BRANDING.md §片頭位置: a narrated long video plays the intro after its condensation.
const story = { kind: "story" };
const cast = { format: "drama", look: { preset: "anime" }, characters: [{ id: "hero" }] };

test("only narrated long videos move the intro behind the condensation; casts, compilations and Shorts keep it first", async (t) => {
  for (const narrated of [doc, { format: "screencast" }, explainer, { ...explainer, characters: [{ id: "host" }] }, { format: "drama", look: { preset: "anime" } }]) {
    assert.equal(narratedLong(narrated), true, JSON.stringify(narrated));
    assert.equal(defaultIntroAt(narrated), INTRO_AFTER_FIRST_CHAPTER);
  }
  assert.equal(narratedLong(cast, story), true, "a brand story is narrated even when its pictures have a cast");
  for (const kept of [cast, { format: "drama", compilation: { episodes: ["a"] } }, { format: "slides", compilation: { episodes: ["a"] } }, { format: "shorts" }]) {
    assert.equal(defaultIntroAt(kept), INTRO_AT_START, JSON.stringify(kept));
  }
  const b = box(t);
  b.current(preset());
  assert.equal((await selectBrandingForBuild({ ...b, doc })).intro_at, INTRO_AFTER_FIRST_CHAPTER);
  assert.equal((await selectBrandingForBuild({ ...b, doc: cast })).intro_at, undefined);
  assert.equal((await selectBrandingForBuild({ ...b, doc: cast, series: story })).intro_at, INTRO_AFTER_FIRST_CHAPTER);
  assert.equal((await selectBrandingForBuild({ ...b, doc: cast })).hash, brandingHash(preset()), "a drama with a cast keeps the original hash");
  b.current(seriesPreset(), "sothatswhy");
  const series = await selectBrandingForBuild({ ...b, doc: explainer });
  assert.deepEqual([series.intro.frames, series.intro_at], [357, INTRO_AFTER_FIRST_CHAPTER], "the series' 357-frame intro moves too");
});

test("old pins have no placement field and rebuild unchanged; new pins record it explicitly", async (t) => {
  const b = box(t);
  b.current(preset("c"));
  const legacy = { ...preset(), hash: brandingHash(preset()), adopted_at: "2026-10-01T00:00:00.000Z" };
  writeFileSync(path.join(b.workdir, "branding.json"), JSON.stringify(legacy));
  const pinned = await selectBrandingForBuild({ ...b, doc });
  assert.equal(pinned.hash, legacy.hash, "a pin from before the placement keeps its intro at the start and its hash");
  assert.equal(pinned.intro_at, undefined);
  assert.equal(introAtFrame(pinned, { chapters: [{ start_frame: 0 }, { start_frame: 900 }] }), 0);
  pinBranding(b.workdir, pinned, new Date("2026-10-13T00:00:00Z"));
  const rewritten = JSON.parse(readFileSync(path.join(b.workdir, "branding.json"), "utf8"));
  assert.equal(rewritten.intro_at, INTRO_AT_START, "the placement is written down even when it is the original one");
  assert.equal(validateBranding(rewritten, { base: b.workdir }).hash, legacy.hash);
  const placed = placeBranding(pinned, INTRO_AFTER_FIRST_CHAPTER);
  assert.notEqual(placed.hash, legacy.hash, "nothing timed for the start is reused after the condensation");
  assert.equal(validateBranding(pinRecord(placed), { base: b.workdir }).hash, placed.hash);
  assert.throws(() => validateBranding({ ...preset(), intro_at: "middle" }), /intro_at/);
  assert.throws(() => validateBranding({ ...preset(), intro_at: INTRO_AFTER_FIRST_CHAPTER, hash: legacy.hash }), /hash/);
});

test("--intro-after-condensation re-places a not-uploaded narrated cut, approved or not, and nothing else", async (t) => {
  const b = box(t);
  b.current(preset("c"));
  writeFileSync(path.join(b.workdir, "branding.json"), JSON.stringify({ ...preset(), adopted_at: "2026-10-01T00:00:00.000Z" }));
  writeFileSync(path.join(b.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", sha256: "old" }, { gate: "publish", sha256: "old" }] }));
  mkdirSync(path.join(b.workdir, "upload"));
  writeFileSync(path.join(b.workdir, "upload", "metadata.json"), "{}");
  const moved = await selectBrandingForBuild({ ...b, doc, introAfterCondensation: true });
  assert.equal(moved.intro_at, INTRO_AFTER_FIRST_CHAPTER);
  assert.equal(moved.intro.sha256, "a".repeat(64), "the pinned assets stay; only their place changes");
  assert.equal(moved.hash, brandingHash({ ...preset(), intro_at: INTRO_AFTER_FIRST_CHAPTER }));
  assert.equal(readBranding(b.workdir).intro_at, undefined, "the pin is rewritten only by a successful build");
  await assert.rejects(selectBrandingForBuild({ ...b, doc: cast, introAfterCondensation: true }), /narrated long video/);
  await assert.rejects(selectBrandingForBuild({ ...b, doc: { ...doc, youtube: { video_id: "abcdefghijk" } }, introAfterCondensation: true }), /already uploaded/);
  writeFileSync(path.join(b.workdir, "auto.json"), JSON.stringify({ status: "done" }));
  await assert.rejects(selectBrandingForBuild({ ...b, doc, introAfterCondensation: true }), /already uploaded/);
  assert.notEqual(replacementRefusal({ doc: { format: "drama", compilation: { episodes: ["a"] } }, workdir: b.workdir }), null);
});

test("the intro after chapter 1 moves only what follows it: lines, scenes, windows, chapters and cues", () => {
  const body = {
    fps: 30, total_frames: 2400,
    lines: [{ id: "hook", start_frame: 0, end_frame: 1100 }, { id: "c2", start_frame: 1200, end_frame: 1500 }],
    scenes: [{ id: "hook", start_frame: 0, end_frame: 1200, states: [{ start_frame: 0, end_frame: 1200 }] }, { id: "two", start_frame: 1200, end_frame: 2400 }],
    windows: [{ start_frame: 0, end_frame: 2400 }],
    chapters: [{ title: "開場", scene: "hook", start_frame: 0 }, { title: "第二章", scene: "two", start_frame: 1200 }, { title: "第三章", scene: "three", start_frame: 1800 }],
  };
  const applied = { hash: brandingHash({ ...seriesPreset(), intro_at: INTRO_AFTER_FIRST_CHAPTER }), intro_frames: 357, outro_frames: 630, body_frames: 2400, intro_at_frame: 1200 };
  const full = presentationTimeline(body, applied);
  assert.equal(full.total_frames, 2400 + 357 + 630);
  assert.equal(full.content_end_frame, 2757);
  assert.deepEqual([full.intro_at_frame, full.intro_end_frame], [1200, 1557]);
  assert.deepEqual(full.lines.map((line) => [line.start_frame, line.end_frame]), [[0, 1100], [1557, 1857]], "the hook is spoken from 0:00; chapter 2 after the intro");
  assert.deepEqual(full.scenes.map((scene) => [scene.start_frame, scene.end_frame]), [[0, 1200], [1557, 2757]], "a scene ending at the intro stays before it");
  assert.deepEqual(full.windows, [{ start_frame: 0, end_frame: 2757 }], "a window spanning the intro covers it");
  assert.deepEqual(full.chapters.map((chapter) => chapter.start_frame), [0, 1557, 2157]);
  // The pin form (no frame recorded yet) finds the same boundary from the timeline's chapters.
  assert.equal(introAtFrame({ intro_at: INTRO_AFTER_FIRST_CHAPTER }, body), 1200);
  assert.throws(() => introAtFrame({ intro_at: INTRO_AFTER_FIRST_CHAPTER }, { total_frames: 10, chapters: [{ start_frame: 0 }] }), /second chapter/);
  const cues = [{ start_ms: 1000, end_ms: 36000, text: "hook" }, { start_ms: 40000, end_ms: 45000, text: "two" }];
  const shown = shiftBrandingCues(cues, applied);
  assert.deepEqual(shown.map((cue) => [cue.start_ms, cue.end_ms]), [[1000, 36000], [51900, 56900]]);
  assert.deepEqual(shiftBrandingCues(shown, applied, -1), cues);
  assert.deepEqual(linesAcrossIntro([{ id: "a", start_frame: 1000, end_frame: 1201 }, { id: "b", start_frame: 1000, end_frame: 1200 }], 1200), ["a"]);
  assert.deepEqual(linesAcrossIntro([{ id: "a", start_frame: 0, end_frame: 5 }], 0), []);
});
