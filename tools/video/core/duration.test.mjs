import assert from "node:assert/strict";
import test from "node:test";

import { presentationTimeline } from "./branding.mjs";
import { effectiveEpisodeMinutes, isKnowledgeLongform, knowledgeDurationProblems, KNOWLEDGE_MIN_SECONDS, KNOWLEDGE_TARGET_SECONDS } from "./duration.mjs";
import { dramaFixture, explainerFixture, fixture, storyFixture } from "./fixtures/load.mjs";

const doc = { format: "slides", category: "explainer", slug: "catalogue-example" };
function cut(frames = 14_400, branding = null) {
  const timeline = { fps: 30, total_frames: frames, speech_hash: "current-speech", scenes: [], lines: [], chapters: [] };
  const applied = branding ? { hash: "bookends", intro_frames: 150, outro_frames: 90, body_frames: frames, ...branding } : null;
  const presented = presentationTimeline(timeline, applied);
  return { doc, timeline, presented, timelineCurrent: true, checks: { ok: true, speech_hash: timeline.speech_hash, metrics: { frames: presented.total_frames }, ...(applied ? { branding: applied } : {}) } };
}

test("legacy explainer targets use ten minutes and explicit valid targets keep their length", () => {
  for (const legacy of [undefined, null, 0, 3, 7]) assert.equal(effectiveEpisodeMinutes(legacy, "flat-explainer"), 10);
  for (const target of [8, 9, 10, 13, 20]) assert.equal(effectiveEpisodeMinutes(target, "flat-explainer"), target);
  assert.equal(effectiveEpisodeMinutes(3, "cinematic-3d"), 3, "ordinary drama keeps its target");
  assert.equal(effectiveEpisodeMinutes(13, "anime-2d"), 13, "brand stories keep thirteen minutes");
  assert.equal(effectiveEpisodeMinutes(undefined, "cinematic-3d"), undefined, "the caller retains its ordinary default");
});

test("malformed explainer targets fail instead of making a writer use a clipped duration", () => {
  for (const invalid of [21, Infinity, NaN, 8.5, "10", false]) {
    assert.throws(() => effectiveEpisodeMinutes(invalid, "flat-explainer"), RangeError);
  }
});

test("knowledge catalogues are covered without changing ordinary drama, compilations or Shorts", () => {
  assert.equal(KNOWLEDGE_MIN_SECONDS, 480);
  assert.equal(KNOWLEDGE_TARGET_SECONDS, 600);
  for (const category of ["ai-terms", "explainer", "story"]) assert.equal(isKnowledgeLongform({ ...doc, category }), true);
  for (const slug of ["sothatswhy-s01", "ai-term-token", "story-umbrella"]) assert.equal(isKnowledgeLongform({ format: "slides", slug }), true);
  assert.equal(isKnowledgeLongform(explainerFixture()), true, "flat-explainer pilot lacks a category");
  assert.equal(isKnowledgeLongform({ ...storyFixture(), category: "story" }), true, "the story worker marks brand stories with category story");
  for (const other of [undefined, fixture(), dramaFixture(), { ...doc, format: "shorts" }, { ...doc, compilation: { episodes: [] } }]) {
    assert.equal(isKnowledgeLongform(other), false);
    assert.deepEqual(knowledgeDurationProblems({ doc: other }), [], "other formats need no new timeline proof");
  }
});

test("eight minutes passes exactly; one frame short fails without rounding or trusting planned minutes", () => {
  assert.deepEqual(knowledgeDurationProblems(cut()), []);
  const short = cut(14_399);
  short.doc = { ...doc, target_minutes: [10, 12] };
  const problems = knowledgeDurationProblems(short);
  assert.equal(problems.length, 2, "both body and final cut are below the floor");
  assert.match(problems[0], /14399 frames \(479\.966666/);
  assert.match(problems[1], /final cut is 14399 frames/);
});

test("bookends cannot make a short body pass, while a qualifying body may keep its bookends", () => {
  const padded = cut(14_399, {});
  assert.equal(padded.presented.total_frames, 14_639);
  assert.match(knowledgeDurationProblems(padded).join("; "), /body is 14399 frames.*excluding intro and outro/);
  assert.deepEqual(knowledgeDurationProblems(cut(14_400, {})), []);
  const wrappedBody = cut();
  wrappedBody.timeline = { ...wrappedBody.timeline, branding_hash: "already-wrapped", body_total_frames: 14_160 };
  assert.match(knowledgeDurationProblems(wrappedBody).join("; "), /unwrapped narration timeline/);
});

test("missing, stale and malformed timelines cannot borrow an estimate or old passing checks", () => {
  for (const change of [
    { timeline: null },
    { timelineCurrent: false },
    { timeline: { ...cut().timeline, total_frames: 14_400.5 } },
    { timeline: { ...cut().timeline, fps: 60 } },
    { timeline: { ...cut().timeline, total_frames: Infinity } },
    { timeline: { ...cut().timeline, speech_hash: "old-speech" } },
  ]) assert.ok(knowledgeDurationProblems({ ...cut(), ...change }).length > 0);
});

test("checked final frames and FPS must match the actual presentation and narration", () => {
  const current = cut();
  for (const metrics of [{ frames: 14_399 }, { frames: 14_401 }, { frames: 14_400, fps: 24 }, { frames: "14400" }, {}]) {
    assert.match(knowledgeDurationProblems({ ...current, checks: { ...current.checks, metrics } }).join("; "), /checked final frame count/);
  }
  for (const presented of [{ ...current.presented, speech_hash: "old" }, { ...current.presented, fps: 60 }, { ...current.presented, total_frames: 14_401 }]) {
    assert.ok(knowledgeDurationProblems({ ...current, presented }).length > 0);
  }
  const branded = cut(14_400, {});
  branded.checks.branding.body_frames -= 1;
  assert.match(knowledgeDurationProblems(branded).join("; "), /current body and selected bookends/);
  assert.deepEqual(knowledgeDurationProblems({ ...current, checks: { ...current.checks, metrics: { frames: 14_400, fps: 30 } } }), []);
});
