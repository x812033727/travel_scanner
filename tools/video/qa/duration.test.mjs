import assert from "node:assert/strict";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { runtimePolicyHash } from "../core/anime-policy.mjs";
import { sha256File } from "../core/approvals.mjs";
import { presentationTimeline } from "../core/branding.mjs";
import { lookHash, mixHash, subtitlesHash } from "../core/drama.mjs";
import { dramaFixture, fixture, fixtureLexicon, sandbox, writeAudioFixture } from "../core/fixtures/load.mjs";
import { eachLine } from "../core/schema.mjs";
import { buildTimeline, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";
import { assembleItem, ITEM_IDS } from "./checks.mjs";

// These short script fixtures exercise the actual timeline floor, not narration estimates.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

function longAnimeDoc() {
  const doc = dramaFixture();
  Object.assign(doc, {
    category: "anime", production_policy: "long-anime-v1", target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "fantasy", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false },
  });
  doc.look.preset = "anime-2d";
  delete doc.music;
  for (const scene of doc.scenes) delete scene.data.fit;
  return doc;
}

// Synthetic WAV sample counts exercise measured timing arithmetic; no generated media is claimed.
function measuredAnimeTimeline(doc, frames) {
  const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const last = [...eachLine(doc)].at(-1).line.id;
  samples[last] += (frames - buildTimeline(doc, samples).total_frames) * SAMPLES_PER_FRAME;
  return { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, fixtureLexicon()) };
}

function animeChecks(doc, timeline, finalSha256) {
  const shots = doc.scenes.filter((scene) => scene.template === "shot").map((scene) => {
    const timing = timeline.scenes.find((placed) => placed.id === scene.id);
    const frames = timing.end_frame - timing.start_frame;
    return { shot: scene.id, kind: "clip", fit: { available: frames, mode: "auto", speed: 1, source_frames: frames, stretched: frames, pad: 0, trim: 0 } };
  });
  return {
    ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(doc),
    runtime_policy_hash: runtimePolicyHash(doc), final_sha256: finalSha256,
    look_hash: lookHash(doc), subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc), clips_hash: "fixture-clips",
    metrics: { fps: 30, frames: timeline.total_frames, shots },
  };
}

test("anime QA rechecks inclusive measured body bounds and rejects stale duration receipts", () => {
  const doc = longAnimeDoc();
  const finalSha256 = "f".repeat(64);
  const timeline = measuredAnimeTimeline(doc, 39_600);
  const checks = animeChecks(doc, timeline, finalSha256);
  const input = { doc, timeline, checks, timelineCurrent: true, current: true, finalExists: true, finalSha256 };
  assert.equal(assembleItem(input).ok, true);
  for (const frames of [37_800, 41_400]) {
    const boundary = measuredAnimeTimeline(doc, frames);
    assert.equal(assembleItem({ ...input, timeline: boundary, checks: animeChecks(doc, boundary, finalSha256) }).ok, true, `${frames} is included`);
  }
  for (const frames of [3_600, 37_799, 41_401]) {
    const short = measuredAnimeTimeline(doc, frames);
    const verdict = assembleItem({ ...input, timeline: short, checks: animeChecks(doc, short, finalSha256) });
    assert.equal(verdict.ok, false);
    assert.match(verdict.detail, /long-anime body is/);
  }
  for (const [name, change, expected] of [
    ["missing timeline", { timeline: null }, /current actual body timeline/],
    ["stale body", { timelineCurrent: false }, /current actual body timeline/],
    ["estimate", { timeline: { ...timeline, timing_basis: "estimated" } }, /measured/],
    ["stale body policy", { timeline: { ...timeline, runtime_policy_hash: "old" } }, /another runtime policy/],
    ["stale checks policy", { checks: { ...checks, runtime_policy_hash: "old" } }, /another runtime policy/],
    ["stale speech", { checks: { ...checks, speech_hash: "old" } }, /same speech hash/],
    ["different final frames", { checks: { ...checks, metrics: { ...checks.metrics, frames: 39_601 } } }, /checked final frames/],
    ["missing final SHA", { finalSha256: null }, /current final.mp4 SHA-256/],
    ["replaced final", { finalSha256: "e".repeat(64) }, /current final.mp4 SHA-256/],
  ]) {
    const verdict = assembleItem({ ...input, ...change });
    assert.equal(verdict.ok, false, name);
    assert.match(verdict.detail, expected, name);
  }
  const partial = { ...doc };
  delete partial.runtime_spec;
  assert.equal(assembleItem({ ...input, doc: partial }).ok, false, "a partial marker cannot fall back to ordinary drama");
});

test("anime QA counts actual bookends separately and never uses the slot reserve to fill the body", () => {
  const doc = longAnimeDoc();
  const finalSha256 = "f".repeat(64);
  const timeline = measuredAnimeTimeline(doc, 39_600);
  const branding = { hash: "brand", intro_frames: 2_700, outro_frames: 2_700, body_frames: timeline.total_frames };
  const presented = presentationTimeline(timeline, branding);
  const bodyChecks = animeChecks(doc, timeline, finalSha256);
  const checks = { ...bodyChecks, branding, metrics: { ...bodyChecks.metrics, frames: presented.total_frames } };
  const input = { doc, timeline, presented, checks, finalSha256, timelineCurrent: true, current: true, finalExists: true };
  assert.equal(assembleItem(input).ok, true, "actual OP/ED may use its 180-second budget");
  const short = measuredAnimeTimeline(doc, 3_600);
  assert.match(assembleItem({ ...input, timeline: short }).detail, /body is 3600 frames/, "bookends cannot supply missing story time");
  const overBudget = { ...branding, outro_frames: 2_701 };
  const overPresented = presentationTimeline(timeline, overBudget);
  const overChecks = { ...checks, branding: overBudget, metrics: { ...checks.metrics, frames: overPresented.total_frames } };
  assert.match(assembleItem({ ...input, presented: overPresented, checks: overChecks }).detail, /actual OP\/ED exceeds/);
  const upperBody = measuredAnimeTimeline(doc, 41_400);
  const reserved = presentationTimeline(upperBody, { ...branding, body_frames: upperBody.total_frames });
  const upperChecks = animeChecks(doc, upperBody, finalSha256);
  const reservedChecks = { ...upperChecks, branding: { ...branding, body_frames: upperBody.total_frames }, metrics: { ...upperChecks.metrics, frames: reserved.total_frames } };
  assert.match(assembleItem({ ...input, timeline: upperBody, presented: reserved, checks: reservedChecks }).detail, /reserve must never be rendered/);
});

test("anime QA rejects missing, stale or stretched shot evidence while allowing a longer clip to be trimmed", () => {
  const doc = longAnimeDoc();
  const timeline = measuredAnimeTimeline(doc, 39_600);
  const finalSha256 = "f".repeat(64);
  const checks = animeChecks(doc, timeline, finalSha256);
  const input = { doc, timeline, checks, finalSha256, timelineCurrent: true, current: true, finalExists: true };
  const first = checks.metrics.shots[0];
  const replaceFirst = (shot) => ({ ...checks, metrics: { ...checks.metrics, shots: [shot, ...checks.metrics.shots.slice(1)] } });
  for (const [name, changed] of [
    ["missing shots", { ...checks, metrics: { ...checks.metrics, shots: undefined } }],
    ["missing required shot", { ...checks, metrics: { ...checks.metrics, shots: checks.metrics.shots.slice(1) } }],
    ["missing fit", replaceFirst({ ...first, fit: undefined })],
    ["slowed clip", replaceFirst({ ...first, fit: { ...first.fit, speed: 0.85 } })],
    ["held tail", replaceFirst({ ...first, fit: { ...first.fit, pad: 1 } })],
    ["stale scene span", replaceFirst({ ...first, fit: { ...first.fit, available: first.fit.available + 1, source_frames: first.fit.source_frames + 1, stretched: first.fit.stretched + 1 } })],
  ]) {
    const verdict = assembleItem({ ...input, checks: changed });
    assert.equal(verdict.ok, false, name);
    assert.match(verdict.detail, /shot|clip|fit|speed|pad|frame/i, name);
  }
  const trimmed = replaceFirst({ ...first, fit: { ...first.fit, available: first.fit.available + 30, trim: 30 } });
  assert.equal(assembleItem({ ...input, checks: trimmed }).ok, true, "trim retains native speed and the measured scene span");
});

test("QA reads the current anime policy, measured body and final file instead of trusting old passing checks", async (t) => {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = longAnimeDoc();
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ ...doc.series, category: doc.category, production_policy: doc.production_policy, runtime_spec: doc.runtime_spec, target_minutes: 22, style_preset: "anime-2d", characters: doc.characters }));
  mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
  writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ clips_hash: "fixture-clips" }));
  const finalFile = path.join(box.workdir, "final.mp4");
  writeFileSync(finalFile, "local fixture, not real media");
  const finalSha256 = await sha256File(finalFile);
  let timeline = measuredAnimeTimeline(doc, 3_600);
  let checks = animeChecks(doc, timeline, finalSha256);
  const save = () => {
    // Silent takes of the measured lengths bind the timeline's audio evidence, and the cut's
    // receipt names that narration, so QA judges the duration rather than missing evidence.
    writeAudioFixture(timeline, box.workdir);
    checks.narration_sha256 = timeline.audio_evidence.narration_sha256;
    writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify(checks));
  };
  const ctx = {
    root: box.root, home: box.base,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: `mkv_${"q".repeat(43)}`, MOKAAIR_SITE: "https://site.test" },
    stdout: { write() {} }, stderr: { write() {} }, sleep: async () => {},
    fetch: async (url) => url.endsWith("/judge/policy") ? Response.json({ passed: true }) : new Response("", { status: 200 }),
  };
  const qa = async () => {
    save();
    assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint, "unbuilt unrelated QA stages still fail");
    const report = JSON.parse(readFileSync(path.join(box.workdir, "review", "qa.json"), "utf8"));
    assert.equal(report.policy_hash, runtimePolicyHash(doc));
    assert.deepEqual(report.runtime_spec, doc.runtime_spec);
    assert.deepEqual(report.items.map((entry) => entry.id), ITEM_IDS);
    return report.items[0];
  };
  assert.match((await qa()).detail, /body is 3600 frames/);
  timeline = measuredAnimeTimeline(doc, 39_600);
  checks = animeChecks(doc, timeline, finalSha256);
  assert.equal((await qa()).ok, true);
  writeFileSync(finalFile, "replacement local fixture, not real media");
  assert.match((await qa()).detail, /current final.mp4 SHA-256/);
  checks.final_sha256 = await sha256File(finalFile);
  timeline.timing_basis = "estimated";
  assert.match((await qa()).detail, /measured/);
});

test("an old passing assemble item is rechecked against the current long-video floor", () => {
  const doc = { format: "slides", category: "ai-terms", slug: "ai-term-token" };
  const timeline = { fps: 30, total_frames: 14_399, speech_hash: "speech" };
  const checks = { ok: true, speech_hash: "speech", metrics: { frames: timeline.total_frames } };
  const input = { doc, timeline, timelineCurrent: true, checks, current: true, finalExists: true };
  assert.equal(assembleItem(input).ok, false);
  assert.match(assembleItem(input).detail, /body is 14399 frames/);
  timeline.total_frames = 14_400;
  checks.metrics.frames = 14_400;
  assert.equal(assembleItem(input).ok, true);
  assert.equal(assembleItem({ ...input, timeline: null }).ok, false);
  assert.equal(assembleItem({ ...input, doc: { format: "slides", slug: "unrelated-video" }, timeline: null }).ok, true);
});

test("QA forwards actual body and presentation timelines to its existing assemble item", async (t) => {
  const box = sandbox();
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = { ...fixture(), category: "explainer", target_minutes: [10, 12] };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "final.mp4"), "local fixture, not real media");
  const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const last = [...eachLine(doc)].at(-1).line.id;
  const initial = buildTimeline(doc, samples);
  samples[last] += (14_399 - initial.total_frames) * SAMPLES_PER_FRAME;
  const timeline = { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, fixtureLexicon()) };
  const checks = { ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(doc), metrics: { frames: timeline.total_frames } };
  const save = () => {
    writeAudioFixture(timeline, box.workdir);
    checks.narration_sha256 = timeline.audio_evidence.narration_sha256;
    writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify(checks));
  };
  save();
  const ctx = {
    root: box.root, home: box.base,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: `mkv_${"q".repeat(43)}`, MOKAAIR_SITE: "https://site.test" },
    stdout: { write() {} }, stderr: { write() {} }, sleep: async () => {},
    fetch: async (url) => url.endsWith("/judge/policy") ? Response.json({ passed: true }) : new Response("", { status: 200 }),
  };
  const assemble = async () => {
    assert.equal(await main(["qa", "--slug", box.slug], ctx), EXIT.lint, "unbuilt unrelated QA items still fail");
    const report = JSON.parse(readFileSync(path.join(box.workdir, "review", "qa.json"), "utf8"));
    assert.deepEqual(report.items.map((entry) => entry.id), ITEM_IDS, "the server still receives exactly eleven items");
    return report.items[0];
  };
  assert.match((await assemble()).detail, /body is 14399 frames/);
  samples[last] += SAMPLES_PER_FRAME;
  Object.assign(timeline, buildTimeline(doc, samples));
  checks.metrics.frames = timeline.total_frames;
  save();
  assert.equal((await assemble()).ok, true, "exactly eight minutes passes the assemble item");
  checks.metrics.frames -= 1;
  save();
  assert.match((await assemble()).detail, /checked final frame count/, "an unbranded final must match the actual timeline too");
});
