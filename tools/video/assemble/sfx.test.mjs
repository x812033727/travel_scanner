import assert from "node:assert/strict";
import test from "node:test";

import { illustratedFixture } from "../core/fixtures/load.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { illustratedTransition, layoutDrama } from "./drama.mjs";
import { MIN_GAP_FRAMES, POP_WINDOW_FRAMES, SFX_NAMES, sfxPlan, sfxSetHash, sfxSetProblems, sfxTrackArgs, WHOOSH_LEAD_FRAMES } from "./sfx.mjs";

function framesManifestFor(doc, timeline) {
  return { scenes: timeline.scenes.map((scene) => ({ id: scene.id, states: doc.scenes.find((each) => each.id === scene.id).template === "shot" ? [] : scene.states.map((_, index) => ({ still: `frames/${scene.id}-${index}.png`, transition: [] })) })) };
}

const MANIFEST = { sounds: { stamp: { file: "stamp.wav", sha256: "a".repeat(64) }, whoosh: { file: "whoosh.wav" }, pop: { file: "pop.wav" } } };

test("a set names the three sounds, each a file in its directory", () => {
  assert.deepEqual(SFX_NAMES, ["stamp", "whoosh", "pop"]);
  assert.deepEqual(sfxSetProblems(MANIFEST), []);
  assert.match(sfxSetProblems(null)[0], /manifest\.json must hold an object/);
  assert.match(sfxSetProblems({ sounds: { stamp: { file: "stamp.wav" } } }).join(";"), /sounds\.whoosh is missing.*sounds\.pop is missing/);
  assert.match(sfxSetProblems({ sounds: { ...MANIFEST.sounds, pop: { file: "../pop.wav" } } })[0], /sounds\.pop\.file/);
  assert.match(sfxSetProblems({ sounds: { ...MANIFEST.sounds, pop: { file: "pop.wav", sha256: "zz" } } })[0], /sha256/);
  assert.notEqual(sfxSetHash(illustratedFixture(), MANIFEST), sfxSetHash(illustratedFixture(), { sounds: { ...MANIFEST.sounds, stamp: { file: "other.wav" } } }));
});

test("effects fall on chapter cards, dissolves and reveals, thinned so they never crowd", () => {
  const doc = illustratedFixture();
  const timeline = estimateTimeline(doc);
  const keyframes = { shots: Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `keyframes/${scene.id}.png`, sha256: "e".repeat(64) }])) };
  const layout = layoutDrama(doc, timeline, framesManifestFor(doc, timeline), null, keyframes, { transitionRule: illustratedTransition, cardMotion: true });
  const events = sfxPlan(layout, timeline, doc);
  const at = (id) => timeline.scenes.find((scene) => scene.id === id).start_frame;
  // The first scene opens a chapter but nothing sounds on frame 0; the later chapter openers stamp.
  assert.deepEqual(events.filter((event) => event.sound === "stamp").map((event) => event.scene), ["desk", "numbers", "door"]);
  assert.equal(events.find((event) => event.scene === "desk").frame, at("desk"));
  // A whoosh leads the dissolve into a picture by a few frames.
  const whoosh = events.find((event) => event.sound === "whoosh" && event.scene === "podium");
  assert.equal(whoosh.frame, at("podium") - WHOOSH_LEAD_FRAMES);
  // The stats card reveals twice: pops, no closer than the window allows.
  const pops = events.filter((event) => event.sound === "pop");
  assert.ok(pops.length >= 1 && pops.length <= 2, `${pops.length} pops`);
  assert.ok(pops.every((event) => event.scene === "numbers"));
  // Nothing within the minimum gap of the beat before it, and everything in frame order.
  events.forEach((event, index) => {
    if (index) assert.ok(event.frame - events[index - 1].frame >= MIN_GAP_FRAMES, `${event.sound} at ${event.frame} crowds ${events[index - 1].sound} at ${events[index - 1].frame}`);
  });
  for (const [index, event] of pops.entries()) if (index) assert.ok(event.frame - pops[index - 1].frame >= POP_WINDOW_FRAMES);
  assert.ok(events.every((event) => event.frame > 0));
});

test("the effects track opens each sound once, delays every beat to its frame and is cut to the video", () => {
  const files = { stamp: "/sfx/stamp.wav", whoosh: "/sfx/whoosh.wav", pop: "/sfx/pop.wav" };
  assert.equal(sfxTrackArgs([], files, 300, -12, "fx.wav"), null);
  const events = [{ frame: 30, sound: "whoosh" }, { frame: 90, sound: "stamp" }, { frame: 150, sound: "whoosh" }];
  const args = sfxTrackArgs(events, files, 300, -12, "fx.wav");
  assert.deepEqual(args.slice(4, 8), ["-i", "/sfx/whoosh.wav", "-i", "/sfx/stamp.wav"], "each sound opened once, in first use order");
  const graph = args[args.indexOf("-filter_complex") + 1];
  assert.match(graph, /^\[0:a\]aformat=sample_rates=48000:channel_layouts=stereo,adelay=1000\|1000\[e0\];\[1:a\]aformat=[^;]*adelay=3000\|3000\[e1\];\[0:a\][^;]*adelay=5000\|5000\[e2\];/);
  assert.match(graph, /\[e0\]\[e1\]\[e2\]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0\[all\];\[all\]volume=-12dB,apad=whole_dur=10\.000000,atrim=0:10\.000000,asetpts=PTS-STARTPTS\[out\]$/);
  assert.deepEqual(args.slice(-7), ["-map", "[out]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "fx.wav"].slice(-7));
  const one = sfxTrackArgs([{ frame: 45, sound: "pop" }], files, 60, -6, "fx.wav");
  assert.match(one[one.indexOf("-filter_complex") + 1], /\[e0\]acopy\[all\]/);
});
