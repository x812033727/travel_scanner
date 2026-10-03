import assert from "node:assert/strict";
import test from "node:test";

import { presentationTimeline } from "./branding.mjs";
import { animeBodyDurationProblems, animeDurationProblems, animeRuntimeProof, animeShotFitProblems, effectiveEpisodeMinutes, isKnowledgeLongform, knowledgeDurationProblems, KNOWLEDGE_MIN_SECONDS, KNOWLEDGE_TARGET_SECONDS } from "./duration.mjs";
import { LONG_ANIME_POLICY, runtimePolicyHash } from "./anime-policy.mjs";
import { fitPlan } from "../assemble/drama.mjs";
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

function animeCut(frames = 39_600, branding = null) {
  const anime = {
    production_policy: LONG_ANIME_POLICY, format: "drama", category: "anime", look: { preset: "anime-2d" }, target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { kind: "series", genre: "custom", lead: "ensemble" },
  };
  const current = cut(frames, branding);
  current.doc = anime;
  current.timeline.runtime_policy_hash = runtimePolicyHash(anime);
  current.timeline.timing_basis = "measured";
  current.timeline.speech_hash = "a".repeat(16);
  current.presented = presentationTimeline(current.timeline, current.checks.branding);
  current.checks.runtime_policy_hash = runtimePolicyHash(anime);
  current.checks.speech_hash = current.timeline.speech_hash;
  current.checks.metrics.fps = 30;
  current.finalSha256 = "f".repeat(64);
  current.checks.final_sha256 = current.finalSha256;
  return current;
}

test("long-anime measured bodies use inclusive 21-to-23-minute bounds with no rounding", () => {
  for (const frames of [37_800, 39_600, 41_400]) assert.deepEqual(animeDurationProblems(animeCut(frames)), []);
  for (const frames of [37_799, 41_401]) assert.match(animeDurationProblems(animeCut(frames)).join("; "), /needs 37800 to 41400 frames/);
  const proof = animeRuntimeProof(animeCut());
  assert.equal(proof.basis, "measured");
  assert.equal(proof.body_seconds, 1320);
  assert.equal(proof.op_ed_seconds, 0, "the OP/ED budget does not invent footage");
  assert.equal(proof.presentation_seconds, 1320);
});

test("OP/ED cannot make a short anime body pass or render the broadcast reserve", () => {
  assert.match(animeDurationProblems(animeCut(37_799, { intro_frames: 2700, outro_frames: 2700 })).join("; "), /excluding OP\/ED and slot reserve/);
  assert.deepEqual(animeDurationProblems(animeCut(39_600, { intro_frames: 2700, outro_frames: 2700 })), []);
  assert.match(animeDurationProblems(animeCut(39_600, { intro_frames: 2701, outro_frames: 2700 })).join("; "), /OP\/ED exceeds/);
  assert.match(animeDurationProblems(animeCut(41_400, { intro_frames: 2700, outro_frames: 2700 })).join("; "), /reserved broadcast-slot time/);
});

test("anime duration evidence fails closed for missing, stale or malformed proof and current final hashes", () => {
  for (const change of [
    { timeline: null }, { timelineCurrent: false }, { finalSha256: null }, { finalSha256: "e".repeat(64) },
    { timeline: { ...animeCut().timeline, timing_basis: "estimated" } }, { timeline: { ...animeCut().timeline, timing_basis: undefined } },
    { timeline: { ...animeCut().timeline, speech_hash: "malformed" } },
    { checks: { ...animeCut().checks, metrics: { frames: 39_600 } } },
    { timeline: { ...animeCut().timeline, fps: 60 } }, { timeline: { ...animeCut().timeline, total_frames: 39_600.5 } },
    { timeline: { ...animeCut().timeline, runtime_policy_hash: "old" } },
    { checks: { ...animeCut().checks, runtime_policy_hash: "old" } },
    { checks: { ...animeCut().checks, speech_hash: "old" } },
    { checks: { ...animeCut().checks, metrics: { frames: 39_599 } } },
  ]) assert.ok(animeDurationProblems({ ...animeCut(), ...change }).length, JSON.stringify(change));
  const halfPolicy = animeCut();
  delete halfPolicy.doc.production_policy;
  assert.match(animeDurationProblems(halfPolicy).join("; "), /production_policy/);
  assert.throws(() => animeRuntimeProof({ ...animeCut(), finalSha256: null }), RangeError);
  assert.deepEqual(animeBodyDurationProblems(animeCut()), [], "body validation can run before a final cut exists");
  assert.deepEqual(animeDurationProblems({ doc: { format: "drama", category: "anime" } }), [], "classification alone preserves ordinary drama rules");
});

test("a default auto fit cannot slow or freeze native anime to meet its measured target", () => {
  const doc = { ...animeCut().doc, scenes: [{ id: "bridge", template: "shot", action_seconds: 8, data: {}, lines: [] }] };
  const timeline = { scenes: [{ id: "bridge", start_frame: 0, end_frame: 240 }] };
  const short = { available: 180, ...fitPlan(180, 240) };
  assert.equal(short.speed, 0.85);
  assert.equal(short.pad, 29, "the previous ordinary default could hold its final frame for less than two seconds");
  assert.match(animeShotFitProblems({ doc, timeline, shots: [{ shot: "bridge", kind: "clip", fit: short }] }).join("; "), /natural speed with no frozen tail/);
  assert.deepEqual(animeShotFitProblems({ doc: { format: "drama" }, timeline, shots: [{ shot: "bridge", kind: "clip", fit: short }] }), [], "ordinary drama keeps its existing auto fit policy");
  assert.match(animeShotFitProblems({ doc, timeline, shots: null }).join("; "), /every directed shot/);
  assert.match(animeShotFitProblems({ doc, timeline, shots: [] }).join("; "), /current measured scene and fit evidence/);
  const natural = { available: 270, ...fitPlan(270, 240) };
  assert.equal(natural.trim, 30);
  assert.deepEqual(animeShotFitProblems({ doc, timeline, shots: [{ shot: "bridge", kind: "clip", fit: natural }] }), []);
});
