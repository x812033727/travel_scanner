import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { presentationTimeline } from "./branding.mjs";
import { A01_COMPACT_BODY_SECONDS, C08_SHORT_MAX_PRESENTED_SECONDS, C08_SHORT_MIN_BODY_SECONDS, C08_SHORT_NARRATION_SHA256, C08_SHORT_SPOKEN_OVERRIDE_SHA256, C20_SHORT_MAX_PRESENTED_SECONDS, C20_SHORT_MIN_BODY_SECONDS, C20_SHORT_NARRATION_SHA256, C20_SHORT_SPOKEN_OVERRIDE_SHA256, animeBodyDurationProblems, animeDurationProblems, animeRuntimeProof, animeShotFitProblems, effectiveEpisodeMinutes, isA01CompactStory, isA01PilotStory, isC08ApprovedShortStory, isC08ShortStory, isC20ApprovedShortStory, isC20ShortStory, isKnowledgeLongform, knowledgeDurationProblems, KNOWLEDGE_MIN_SECONDS, KNOWLEDGE_TARGET_SECONDS } from "./duration.mjs";
import { LONG_ANIME_POLICY, runtimePolicyHash } from "./anime-policy.mjs";
import { fitPlan } from "../assemble/drama.mjs";
import { EXPLAINER_PRESETS } from "./drama.mjs";
import { dramaFixture, explainerFixture, fixture, storyFixture } from "./fixtures/load.mjs";

const doc = { format: "slides", category: "explainer", slug: "catalogue-example" };
function cut(frames = 14_400, branding = null) {
  const timeline = { fps: 30, total_frames: frames, speech_hash: "current-speech", scenes: [], lines: [], chapters: [] };
  const applied = branding ? { hash: "bookends", intro_frames: 150, outro_frames: 90, body_frames: frames, ...branding } : null;
  const presented = presentationTimeline(timeline, applied);
  return { doc, timeline, presented, timelineCurrent: true, checks: { ok: true, speech_hash: timeline.speech_hash, metrics: { frames: presented.total_frames }, ...(applied ? { branding: applied } : {}) } };
}

const a01 = {
  slug: "story-rolling-suitcase-v2", format: "drama", category: "story",
  series: { slug: "brand-stories-curio-pilot-v2", episode: 1 },
  look: { preset: "cute-mystery" }, target_minutes: [7, 8],
};
const c08Short = JSON.parse(readFileSync(new URL("../../../docs/videos/story-everyday-kikkoman-c08-short-v8/video.json", import.meta.url), "utf8"));
const c20Short = JSON.parse(readFileSync(new URL("../../../docs/videos/story-everyday-zippo-c20-short-v8/video.json", import.meta.url), "utf8"));

test("legacy explainer targets use ten minutes and explicit valid targets keep their length", () => {
  assert.deepEqual(EXPLAINER_PRESETS, ["flat-explainer", "cute-cartoon", "cute-mystery"]);
  for (const preset of EXPLAINER_PRESETS) {
    for (const legacy of [undefined, null, 0, 3, 7]) assert.equal(effectiveEpisodeMinutes(legacy, preset), 10, preset);
    for (const target of [8, 9, 10, 13, 20]) assert.equal(effectiveEpisodeMinutes(target, preset), target, preset);
  }
  assert.equal(effectiveEpisodeMinutes(3, "cinematic-3d"), 3, "ordinary drama keeps its target");
  assert.equal(effectiveEpisodeMinutes(13, "anime-2d"), 13, "brand stories keep thirteen minutes");
  assert.equal(effectiveEpisodeMinutes(undefined, "cinematic-3d"), undefined, "the caller retains its ordinary default");
});

test("malformed explainer targets fail instead of making a writer use a clipped duration", () => {
  for (const preset of EXPLAINER_PRESETS) {
    for (const invalid of [21, Infinity, NaN, 8.5, "10", false]) {
      assert.throws(() => effectiveEpisodeMinutes(invalid, preset), RangeError, preset);
    }
  }
});

test("knowledge catalogues are covered without changing ordinary drama, compilations or Shorts", () => {
  assert.equal(KNOWLEDGE_MIN_SECONDS, 480);
  assert.equal(KNOWLEDGE_TARGET_SECONDS, 600);
  for (const category of ["ai-terms", "explainer", "story"]) assert.equal(isKnowledgeLongform({ ...doc, category }), true);
  for (const slug of ["sothatswhy-s01", "ai-term-token", "story-umbrella"]) assert.equal(isKnowledgeLongform({ format: "slides", slug }), true);
  assert.equal(isKnowledgeLongform(explainerFixture()), true, "flat-explainer pilot lacks a category");
  for (const preset of EXPLAINER_PRESETS) assert.equal(isKnowledgeLongform({ format: "drama", look: { preset } }), true, `${preset} is held to the floor by its preset alone`);
  assert.equal(isKnowledgeLongform({ format: "drama", look: { preset: "ink-wash" } }), false);
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

test("a cute explainer is held to the same 480 measured seconds as flat-explainer", () => {
  const mystery = { format: "drama", slug: "curio-example", look: { preset: "cute-mystery" }, characters: [] };
  assert.deepEqual(knowledgeDurationProblems({ ...cut(), doc: mystery }), []);
  const problems = knowledgeDurationProblems({ ...cut(14_399), doc: mystery });
  assert.ok(problems.length > 0, "one frame short of eight minutes is refused");
  assert.match(problems[0], /14399 frames/);
});

test("only the exact A01 pilot identity and per-video target use the compact band", () => {
  assert.deepEqual(A01_COMPACT_BODY_SECONDS, [420, 480]);
  assert.equal(isA01PilotStory(a01), true);
  assert.equal(isA01CompactStory(a01), true);
  for (const change of [
    { slug: "story-conveyor-belt-sushi-v2" }, { format: "slides" }, { category: "explainer" },
    { series: { slug: "brand-stories-curio-pilot-v2", episode: 2 } },
    { series: { slug: "brand-stories-five-v2", episode: 1 } },
    { look: { preset: "custom" } }, { look: { preset: "cute-mystery", style: "other" } },
    { compilation: { episodes: [] } },
  ]) {
    const other = { ...a01, ...change };
    assert.equal(isA01PilotStory(other), false, JSON.stringify(change));
    assert.equal(isA01CompactStory(other), false, JSON.stringify(change));
  }
  assert.equal(isA01PilotStory({ ...a01, target_minutes: [9, 11] }), true);
  assert.equal(isA01CompactStory({ ...a01, target_minutes: [9, 11] }), false,
    "an old A01 target cannot silently inherit the shorter QA floor");
  assert.equal(isA01CompactStory(null), false);
});

test("A01 accepts exactly 420 to 480 measured body seconds; bookends cannot buy time", () => {
  for (const frames of [420 * 30, 450 * 30, 480 * 30]) {
    assert.deepEqual(knowledgeDurationProblems({ ...cut(frames), doc: a01 }), []);
  }
  const under = knowledgeDurationProblems({ ...cut(420 * 30 - 1), doc: a01 });
  assert.equal(under.length, 2, "body and final cut are both below the inclusive floor");
  assert.match(under[0], /body is 12599 frames.*needs at least 12600 frames \(420 s\), excluding intro and outro/);
  const over = knowledgeDurationProblems({ ...cut(480 * 30 + 1), doc: a01 });
  assert.equal(over.length, 1);
  assert.match(over[0], /body is 14401 frames.*needs at most 14400 frames \(480 s\), excluding intro and outro/);
  const padded = cut(420 * 30 - 1, { intro_frames: 150, outro_frames: 630 });
  assert.ok(padded.presented.total_frames > 420 * 30);
  assert.match(knowledgeDurationProblems({ ...padded, doc: a01 }).join("; "), /body is 12599 frames.*excluding intro and outro/);
  assert.deepEqual(knowledgeDurationProblems({ ...cut(480 * 30, {}), doc: a01 }), [],
    "a valid 480-second body may have intro and outro outside the body maximum");
});

test("A01's shorter floor still needs current narration and checked matching cut; B18 keeps 480 seconds", () => {
  const valid = { ...cut(420 * 30), doc: a01 };
  assert.match(knowledgeDurationProblems({ ...valid, timelineCurrent: false }).join("; "), /current actual narration timeline/);
  assert.match(knowledgeDurationProblems({ ...valid, checks: { ...valid.checks, speech_hash: "stale" } }).join("; "), /same speech hash/);
  assert.match(knowledgeDurationProblems({ ...valid, checks: { ...valid.checks, metrics: { frames: 12_601 } } }).join("; "), /checked final frame count/);
  for (const other of [
    { ...a01, slug: "story-conveyor-belt-sushi-v2", series: { ...a01.series, episode: 2 }, target_minutes: [9, 11] },
    { ...a01, target_minutes: [9, 11] },
  ]) {
    assert.match(knowledgeDurationProblems({ ...cut(420 * 30), doc: other }).join("; "), /needs at least 14400 frames \(480 s\)/);
    assert.deepEqual(knowledgeDurationProblems({ ...cut(480 * 30), doc: other }), []);
  }
});

test("only C08 short-v8 gets a 240-second body floor and 300-second finished-cut cap", () => {
  assert.equal(C08_SHORT_MIN_BODY_SECONDS, 240);
  assert.equal(C08_SHORT_MAX_PRESENTED_SECONDS, 300);
  assert.equal(C08_SHORT_NARRATION_SHA256, "31041c60a61f7612878e07417aaf7b7b914a70e04ad49ab395de6e8918c6d7d9");
  assert.equal(C08_SHORT_SPOKEN_OVERRIDE_SHA256, "1f3d6939b2d5dcf8983bda60ffd5a48b9a753ca2a9f5e0f6ed55453e4ef7079c");
  assert.equal(isC08ShortStory(c08Short), true);
  assert.equal(isC08ApprovedShortStory(c08Short), true);
  for (const change of [
    { slug: "story-everyday-kikkoman-c08" }, { series: { slug: "brand-stories-everyday-reversals", episode: 9 } },
    { series: { slug: "another-series", episode: 8 } }, { format: "slides" },
    { category: "story" }, { look: { preset: "cute-mystery", style: "extra" } },
    { target_minutes: [9, 11] },
  ]) {
    const other = { ...c08Short, ...change };
    assert.equal(isC08ApprovedShortStory(other), false, JSON.stringify(change));
    assert.match(knowledgeDurationProblems({ ...cut(270 * 30), doc: other }).join("; "), /needs at least 14400 frames \(480 s\)/);
  }
  assert.equal(isC08ApprovedShortStory({ ...c08Short, compilation: { episodes: [] } }), false);
  const changedWords = structuredClone(c08Short);
  changedWords.scenes[0].lines[0].text += "改";
  assert.equal(isC08ApprovedShortStory(changedWords), false, "one changed character loses the short policy");
  assert.match(knowledgeDurationProblems({ ...cut(270 * 30), doc: changedWords }).join("; "), /needs at least 14400 frames \(480 s\)/);
  const changedSpeech = structuredClone(c08Short);
  changedSpeech.scenes[27].lines[0].say += "改";
  assert.equal(isC08ApprovedShortStory(changedSpeech), false, "a changed spoken override loses the short policy");
  assert.match(knowledgeDurationProblems({ ...cut(270 * 30), doc: changedSpeech }).join("; "), /needs at least 14400 frames \(480 s\)/);
  const changedPicture = structuredClone(c08Short);
  changedPicture.scenes[0].data.prompt += " A later media reference may change.";
  assert.equal(isC08ApprovedShortStory(changedPicture), true, "visual/media updates do not change approved narration");
  assert.deepEqual(knowledgeDurationProblems({ ...cut(270 * 30), doc: c08Short }), []);
  assert.match(knowledgeDurationProblems({ ...cut(240 * 30 - 1, { intro_frames: 150, outro_frames: 630 }), doc: c08Short }).join("; "), /body is 7199 frames.*needs at least 7200 frames \(240 s\), excluding intro and outro/);
  assert.deepEqual(knowledgeDurationProblems({ ...cut(274 * 30, { intro_frames: 150, outro_frames: 630 }), doc: c08Short }), []);
  assert.match(knowledgeDurationProblems({ ...cut(274 * 30 + 1, { intro_frames: 150, outro_frames: 630 }), doc: c08Short }).join("; "), /C08 short-v8 final cut.*needs at most 9000 frames \(300 s\)/);
  const stale = { ...cut(270 * 30), doc: c08Short, timelineCurrent: false };
  assert.match(knowledgeDurationProblems(stale).join("; "), /current actual narration timeline/);
});

test("only the frozen C20 short-v8 gets a 300-second body floor and 420-second finished-cut cap", () => {
  assert.equal(C20_SHORT_MIN_BODY_SECONDS, 300);
  assert.equal(C20_SHORT_MAX_PRESENTED_SECONDS, 420);
  assert.equal(C20_SHORT_NARRATION_SHA256, "57600d182ae57947e2426e8551b19bc9e660b8808616d7d44b72122a0b666632");
  assert.equal(C20_SHORT_SPOKEN_OVERRIDE_SHA256, "be30d595b6ab35f0d84a5afb56e24b6d20cb079c66536e95c8d85eb5d159faae");
  assert.equal(isC20ShortStory(c20Short), true);
  assert.equal(isC20ApprovedShortStory(c20Short), true);
  for (const change of [
    { slug: "story-everyday-zippo-c20" }, { series: { slug: "brand-stories-everyday-reversals", episode: 19 } },
    { series: { slug: "another-series", episode: 20 } }, { format: "slides" },
    { category: "story" }, { look: { preset: "cute-mystery", style: "extra" } },
    { target_minutes: [6, 7] },
  ]) {
    const other = { ...c20Short, ...change };
    assert.equal(isC20ApprovedShortStory(other), false, JSON.stringify(change));
    assert.match(knowledgeDurationProblems({ ...cut(333 * 30), doc: other }).join("; "), /needs at least 14400 frames \(480 s\)/);
  }
  assert.equal(isC20ApprovedShortStory({ ...c20Short, compilation: { episodes: [] } }), false);
  const changedWords = structuredClone(c20Short);
  changedWords.scenes[0].lines[0].text += "改";
  assert.equal(isC20ApprovedShortStory(changedWords), false, "one changed character loses the short policy");
  assert.match(knowledgeDurationProblems({ ...cut(333 * 30), doc: changedWords }).join("; "), /needs at least 14400 frames \(480 s\)/);
  const changedSpeech = structuredClone(c20Short);
  changedSpeech.scenes[1].lines[0].say += "改";
  assert.equal(isC20ApprovedShortStory(changedSpeech), false, "a changed TTS reading loses the short policy");
  assert.match(knowledgeDurationProblems({ ...cut(333 * 30), doc: changedSpeech }).join("; "), /needs at least 14400 frames \(480 s\)/);
  for (const [name, change] of [
    ["say_for binding", doc => { doc.scenes[1].lines[0].say_for += "0"; }],
    ["line ID", doc => { doc.scenes[0].lines[0].id += "x"; }],
  ]) {
    const other = structuredClone(c20Short);
    change(other);
    assert.equal(isC20ApprovedShortStory(other), false, `${name} change loses the short policy`);
    assert.match(knowledgeDurationProblems({ ...cut(333 * 30), doc: other }).join("; "), /needs at least 14400 frames \(480 s\)/);
  }
  const changedPicture = structuredClone(c20Short);
  changedPicture.scenes[0].data.prompt += " A later media reference may change.";
  assert.equal(isC20ApprovedShortStory(changedPicture), true, "visual/media updates do not change approved narration");
  assert.match(knowledgeDurationProblems({ ...cut(8_999, { intro_frames: 150, outro_frames: 630 }), doc: c20Short }).join("; "), /body is 8999 frames.*needs at least 9000 frames \(300 s\), excluding intro and outro/);
  assert.deepEqual(knowledgeDurationProblems({ ...cut(9_000, { intro_frames: 150, outro_frames: 630 }), doc: c20Short }), []);
  assert.deepEqual(knowledgeDurationProblems({ ...cut(11_820, { intro_frames: 150, outro_frames: 630 }), doc: c20Short }), []);
  assert.match(knowledgeDurationProblems({ ...cut(11_821, { intro_frames: 150, outro_frames: 630 }), doc: c20Short }).join("; "), /C20 short-v8 final cut.*needs at most 12600 frames \(420 s\)/);
  assert.match(knowledgeDurationProblems({ ...cut(333 * 30), doc: c20Short, timelineCurrent: false }).join("; "), /current actual narration timeline/);
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
