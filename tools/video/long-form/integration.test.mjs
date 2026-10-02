import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { needsMinimumLength } from "../core/drama.mjs";
import { minEpisodeMinutes } from "../core/schema.mjs";
import { assembleItem } from "../qa/checks.mjs";

test("an ordinary CLI process cannot disable the general floor even with an inherited test marker", () => {
  const schemaUrl = new URL("../core/schema.mjs", import.meta.url).href;
  const checksUrl = new URL("../qa/checks.mjs", import.meta.url).href;
  const code = `import { minEpisodeMinutes } from ${JSON.stringify(schemaUrl)};
    import { assembleItem } from ${JSON.stringify(checksUrl)};
    const floor = minEpisodeMinutes();
    const result = assembleItem({ finalExists: true, current: true, minMinutes: floor,
      checks: { ok: true, metrics: { frames: 14399 } } });
    console.log(JSON.stringify({ floor, ok: result.ok }));`;
  const env = { ...process.env, VIDEO_MIN_EPISODE_MINUTES: "0" };
  delete env.NODE_TEST_CONTEXT;
  for (const marker of [undefined, "child-v8", "arbitrary-marker"]) {
    if (marker === undefined) delete env.NODE_TEST_CONTEXT;
    else env.NODE_TEST_CONTEXT = marker;
    const result = spawnSync(process.execPath, ["--input-type=module", "-e", code], { env, encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), { floor: 8, ok: false });
  }
  const cli = fileURLToPath(new URL("../cli.mjs", import.meta.url));
  assert.equal(minEpisodeMinutes({ NODE_TEST_CONTEXT: "child-v8", VIDEO_MIN_EPISODE_MINUTES: "0" }, cli), 8);
});

test("fixture exemptions cannot pad a knowledge or brand-story body with bookends", () => {
  const smoke = fileURLToPath(new URL("../assemble/smoke.mjs", import.meta.url));
  assert.equal(minEpisodeMinutes({ VIDEO_MIN_EPISODE_MINUTES: "0" }, smoke), 0);
  const timeline = { fps: 30, total_frames: 14399, speech_hash: "speech" };
  const presented = { ...timeline, body_total_frames: 14399, branding_hash: "brand", total_frames: 15000 };
  const checks = { ok: true, speech_hash: "speech", metrics: { frames: 15000 },
    branding: { hash: "brand", body_frames: 14399, intro_frames: 300, outro_frames: 301 } };
  for (const doc of [{ format: "drama", look: { preset: "flat-explainer" } }, { format: "drama", category: "story" }]) {
    const result = assembleItem({ doc, timeline, presented, checks, finalExists: true, current: true, timelineCurrent: true, minMinutes: 0 });
    assert.equal(result.ok, false);
    assert.match(result.detail, /body is 14399 frames/);
  }
});

test("both duration rules coexist while ordinary dramas and compilations retain their format", () => {
  const doc = { format: "drama", look: { preset: "flat-explainer" } };
  const timeline = { fps: 30, total_frames: 14400, speech_hash: "speech" };
  const checks = { ok: true, speech_hash: "speech", metrics: { frames: 14400 } };
  assert.equal(assembleItem({ doc, timeline, checks, finalExists: true, current: true, timelineCurrent: true, minMinutes: 8 }).ok, true);
  const drama = { format: "drama", category: "drama" };
  assert.equal(needsMinimumLength(drama), false);
  assert.equal(assembleItem({ doc: drama, checks: { ok: true, metrics: { frames: 30 } }, finalExists: true, current: true, minMinutes: 0 }).ok, true);
  assert.equal(needsMinimumLength({ ...doc, compilation: {} }), false);
});
