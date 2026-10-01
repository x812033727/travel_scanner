import assert from "node:assert/strict";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { eachLine } from "../core/schema.mjs";
import { buildTimeline, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";
import { assembleItem, ITEM_IDS } from "./checks.mjs";

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
    writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
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
