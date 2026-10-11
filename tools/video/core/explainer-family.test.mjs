// The explainer family (docs/videos/DRAMA.md `look`): which presets are narrator-only
// explainers, which series' identity each wears, and the bytes of the first of them.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { composeShotPrompt } from "../media/prompt-budget.mjs";
import { IMAGE_SIZES } from "../media/stages.mjs";
import { keyframeKey, lookHash, PRESETS, resolveLook } from "./drama.mjs";
import { explainerFixture } from "./fixtures/load.mjs";
import { visualHash } from "./timeline.mjs";

const sha256 = (text) => createHash("sha256").update(text, "utf8").digest("hex");

// Recorded on main before the family existed. A change to any of these moves the look hash of
// every flat-explainer video already drawn, so its pictures would be asked for (and paid for)
// again, and the image cache key of every picture it still has to draw.
test("flat-explainer is what it was: preset bytes, look hash, visual hash, composed prompt and image keys", () => {
  assert.equal(sha256(JSON.stringify(PRESETS["flat-explainer"])), "0646ae3434271709496daa3d9e83f1d5c19bfe0e6760c1d6c2860e6a3afb6881");
  const fixture = explainerFixture();
  assert.equal(lookHash(fixture), "bd2b3b49af8e9623");
  assert.equal(lookHash({ format: "drama", look: { preset: "flat-explainer" }, characters: [] }), "bd2b3b49af8e9623");
  assert.equal(visualHash(fixture), "1ee426698cc02ed3");

  const shot = fixture.scenes.find((scene) => scene.id === "flash");
  const look = resolveLook(fixture.look);
  const { prompt } = composeShotPrompt({ prompt: shot.data.prompt, look, camera: shot.data.camera, cast: "", limit: 4000 });
  assert.equal(sha256(prompt), "ea312665764d5a793065d1fd6ef3a76cc70c31be1232315c03896c59d11147e3");
  const key = (size) => keyframeKey({ provider: "gemini", model: "gemini-3-pro-image", prompt, negative: look.negative, ...IMAGE_SIZES[size], seed: 1, references: [] });
  assert.equal(key("2K"), "5169040efab27447");
  assert.equal(key("1K"), "7c56c03a202a1cc8");
});
