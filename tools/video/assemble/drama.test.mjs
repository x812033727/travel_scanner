import assert from "node:assert/strict";
import test from "node:test";

import { dramaFixture, fixture } from "../core/fixtures/load.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import { checksCurrent } from "../package/cli.mjs";
import { uploadChecklist } from "../package/metadata.mjs";
import {
  bedLevel,
  bedLoudnessArgs,
  checkBed,
  CLIP_ENCODER_VERSION,
  clipFrames,
  clipSegmentArgs,
  clipSegmentKey,
  DISSOLVE_FRAMES,
  duckRatio,
  fitPlan,
  freezeProblem,
  keyframeProblem,
  lastFrameArgs,
  layoutDrama,
  MAX_FREEZE_FRAMES,
  measureMixArgs,
  mixArgs,
  mixFilter,
  MOTION_DRIFT_ZOOM,
  MOTION_ENCODER_VERSION,
  MOTION_PAN_ZOOM,
  MOTION_SOURCE_SCALE,
  MOTION_ZOOM,
  motionFramePsnrArgs,
  motionMove,
  motionSegmentArgs,
  motionSegmentKey,
  subtitleTrack,
  zoompanExpr,
} from "./drama.mjs";
import { ENCODER_VERSION, PlanError } from "./plan.mjs";
import { clipSeconds, LONG_BY_SECONDS, SHORT_BY_SECONDS } from "./synthetic.mjs";

const MUSIC = { gain_db: -20, duck_db: -10, fade_in_ms: 1500, fade_out_ms: 3000 };

function framesManifestFor(doc, timeline) {
  return {
    scenes: timeline.scenes.map((scene) => {
      const source = doc.scenes.find((each) => each.id === scene.id);
      const clip = source.template === "shot";
      return { id: scene.id, kind: clip ? "clip" : "stills", states: clip ? [] : scene.states.map((_, index) => ({ still: `frames/${scene.id}-${index}.png`, transition: [] })) };
    }),
  };
}

function clipsManifestFor(doc) {
  const shots = {};
  for (const scene of doc.scenes.filter((each) => each.template === "shot")) shots[scene.id] = { file: `clips/${scene.id}.mp4`, sha256: "a".repeat(64) };
  return { clips_hash: "c1", shots };
}

test("the slides and clip encoder versions are untouched, so no published video's segments are redone", () => {
  assert.equal(ENCODER_VERSION, "x264-high-crf18-stillimage-g60-bf2-bt709-v2");
  assert.equal(CLIP_ENCODER_VERSION, "x264-high-crf18-film-g60-bf2-bt709-clip-v1");
  assert.equal(MOTION_ENCODER_VERSION, "x264-high-crf18-film-g60-bf2-bt709-motion-v3");
  assert.equal(new Set([ENCODER_VERSION, CLIP_ENCODER_VERSION, MOTION_ENCODER_VERSION]).size, 3);
});

test("a clip is cut when long, slowed then held when short, as far as its fit mode allows", () => {
  assert.deepEqual(fitPlan(300, 240, "auto"), { mode: "auto", speed: 1, source_frames: 240, stretched: 240, pad: 0, trim: 60 });
  // 10% short: slowed to 0.9x and nothing held.
  assert.deepEqual(fitPlan(216, 240, "auto"), { mode: "auto", speed: 0.9, source_frames: 216, stretched: 240, pad: 0, trim: 0 });
  // 25% short: slowed to the floor of 0.85x, the rest held.
  const held = fitPlan(180, 240, "auto");
  assert.equal(held.speed, 0.85);
  assert.equal(held.stretched, Math.floor(180 / 0.85));
  assert.equal(held.stretched + held.pad, 240);
  assert.deepEqual(fitPlan(180, 240, "freeze"), { mode: "freeze", speed: 1, source_frames: 180, stretched: 180, pad: 60, trim: 0 });
  assert.deepEqual(fitPlan(180, 240, "trim"), { mode: "trim", speed: 1, source_frames: 180, stretched: 180, pad: 60, trim: 0 });
  const slow = fitPlan(120, 300, "slow");
  assert.equal(slow.speed, 0.5);
  assert.equal(slow.stretched + slow.pad, 300);
  assert.throws(() => fitPlan(0, 30), PlanError);
  assert.throws(() => fitPlan(30, 0), PlanError);
});

test("a long hold is a problem unless the shot says freeze", () => {
  const scene = { id: "storm" };
  assert.equal(freezeProblem(scene, fitPlan(240, 240)), null);
  assert.equal(freezeProblem(scene, { mode: "auto", pad: MAX_FREEZE_FRAMES }), null);
  assert.match(freezeProblem(scene, { mode: "auto", pad: MAX_FREEZE_FRAMES + 1 }), /shot storm holds its last frame for 61 frames \(2\.0 s\)/);
  assert.match(freezeProblem(scene, { mode: "trim", pad: 90 }), /fit "freeze"/);
  assert.equal(freezeProblem(scene, { mode: "freeze", pad: 900 }), null);
});

test("the drama layout keeps the cards as stills and gives each shot its clip, fit and transition", () => {
  const doc = dramaFixture();
  const timeline = estimateTimeline(doc);
  const frames = framesManifestFor(doc, timeline);
  const clips = clipsManifestFor(doc);
  const keyframes = { shots: { "sea-storm": { file: "keyframes/sea-storm.png" } } };
  const layout = layoutDrama(doc, timeline, frames, clips, keyframes);
  assert.deepEqual(layout.map((scene) => [scene.id, scene.kind]), [["opening", "clip"], ["farewell", "clip"], ["sea-storm", "clip"], ["bird", "clip"], ["wrap", "stills"]]);
  const storm = layout[2];
  assert.equal(storm.fit, "freeze");
  assert.equal(storm.clip.file, "clips/sea-storm.mp4");
  assert.equal(storm.keyframe, "keyframes/sea-storm.png");
  assert.equal(storm.frames, timeline.scenes[2].end_frame - timeline.scenes[2].start_frame);
  assert.equal(layout[3].transition, "dissolve");
  assert.equal(layout[3].keyframe, null);
  assert.equal(layout[0].transition, "cut");
  assert.equal(layout[4].entries.length, 1, "the outro card is one held still");
  assert.equal(layout.reduce((sum, scene) => sum + scene.frames, 0), timeline.total_frames);
  // Without a clip for a shot, or with one that failed its checks, assemble says what to run.
  const missing = clipsManifestFor(doc);
  delete missing.shots.bird;
  assert.throws(() => layoutDrama(doc, timeline, frames, missing), /shot bird has no clip; run clips first/);
  const flagged = clipsManifestFor(doc);
  flagged.shots.bird.needs_review = true;
  assert.throws(() => layoutDrama(doc, timeline, frames, flagged), /needs_review/);
  assert.throws(() => layoutDrama(doc, timeline, { scenes: [] }, clips), /run render again/);
});

test("a still shot is laid out as a motion scene carrying its keyframe and its camera move", () => {
  const doc = dramaFixture();
  doc.scenes[0].data.visual = "still";
  doc.scenes[3].data.visual = "still";
  const timeline = estimateTimeline(doc);
  const frames = framesManifestFor(doc, timeline);
  const clips = clipsManifestFor(doc);
  clips.shots.opening = { still: true, file: "keyframes/opening-1.png", sha256: "b".repeat(64) };
  clips.shots.bird = { still: true, file: "keyframes/bird-1.png", sha256: "c".repeat(64) };
  const keyframes = { shots: { opening: { file: "keyframes/opening-1.png", sha256: "b".repeat(64) }, "sea-storm": { file: "keyframes/sea-storm-1.png" } } };
  const layout = layoutDrama(doc, timeline, frames, clips, keyframes);
  assert.deepEqual(layout.map((scene) => [scene.id, scene.kind]), [["opening", "motion"], ["farewell", "clip"], ["sea-storm", "clip"], ["bird", "motion"], ["wrap", "stills"]]);
  const opening = layout[0];
  assert.deepEqual(opening.keyframe, { file: "keyframes/opening-1.png", sha256: "b".repeat(64) });
  assert.deepEqual(opening.move, { name: "push-in", startsAtIdentity: true }, "camera \"slow push in\"");
  assert.equal(opening.fit, null);
  assert.equal(opening.transition, "cut");
  assert.equal(opening.clip, undefined);
  assert.equal(opening.frames, timeline.scenes[0].end_frame - timeline.scenes[0].start_frame);
  const bird = layout[3];
  assert.deepEqual(bird.keyframe, { file: "keyframes/bird-1.png", sha256: "c".repeat(64) }, "without the keyframes manifest, the clips manifest's still entry serves");
  assert.equal(bird.transition, "dissolve");
  assert.equal(bird.move.name, "drift", "\"slow orbit\" and ruffling feathers name no move");
  assert.equal(layout.reduce((sum, scene) => sum + scene.frames, 0), timeline.total_frames);
  // A still needs a passed keyframe from one manifest or the other.
  assert.throws(() => layoutDrama(doc, timeline, frames, clipsManifestFor(doc), { shots: {} }), /shot opening is a still with no keyframe; run keyframes first/);
  const flagged = { shots: { ...keyframes.shots, opening: { ...keyframes.shots.opening, needs_review: true } } };
  assert.throws(() => layoutDrama(doc, timeline, frames, clips, flagged), /shot opening is a still whose keyframe failed its checks/);
  // And a clip shot whose manifest entry is a still has no clip to play.
  const swapped = clipsManifestFor(doc);
  swapped.shots.farewell = { still: true, file: "keyframes/farewell-1.png", sha256: "d".repeat(64) };
  assert.throws(() => layoutDrama(doc, timeline, frames, swapped, keyframes), /shot farewell has no clip; run clips first/);
});

test("a camera word names the move, from the camera direction first, then the motion prompt; nothing named drifts", async () => {
  const table = [
    ["slow push in", "push-in", true],
    ["Dolly in on her face", "push-in", true],
    ["zoom in", "push-in", true],
    ["the camera moves closer", "push-in", true],
    ["move in slowly", "push-in", true],
    ["slow pull back", "pull-out", false],
    ["zoom out to the valley", "pull-out", false],
    ["widen to the whole hall", "pull-out", false],
    ["back away from the door", "pull-out", false],
    ["pan left along the wall", "pan-right", false],
    ["pan to the left", "pan-right", false],
    ["sweep left to right", "pan-right", false],
    ["pan right", "pan-left", false],
    ["pan to the right", "pan-left", false],
    ["right to left across the ranks", "pan-left", false],
    ["tilt up to the moon", "tilt-up", false],
    ["crane up", "tilt-up", false],
    ["a slow rise", "tilt-up", false],
    ["tilt down to the water", "tilt-down", false],
    ["crane down", "tilt-down", false],
    ["descend into the valley", "tilt-down", false],
    ["static, slight handheld drift", "drift", true],
    ["", "drift", true],
  ];
  for (const [camera, name, startsAtIdentity] of table) {
    assert.deepEqual(motionMove({ camera }), name === "drift" ? { name, startsAtIdentity, direction: "right" } : { name, startsAtIdentity }, camera);
  }
  assert.deepEqual(motionMove({}), { name: "drift", startsAtIdentity: true, direction: "right" });
  assert.deepEqual(motionMove(undefined), { name: "drift", startsAtIdentity: true, direction: "right" });
  assert.equal(motionMove({ motion: "the camera pushes in on the pebble" }).name, "push-in", "the motion prompt is read when the camera names nothing");
  assert.equal(motionMove({ camera: "pan left", motion: "zoom in" }).name, "pan-right", "the camera direction wins over the motion prompt");
  assert.equal(motionMove({ camera: "handheld", motion: "waves crashing" }).name, "drift");
  // A drift goes the way its shot id says, so a run of drifting pictures does not all go one way.
  const { driftDirection, DRIFT_DIRECTIONS } = await import("./drama.mjs");
  assert.deepEqual(DRIFT_DIRECTIONS, ["right", "left"]);
  assert.equal(driftDirection("podium"), "right");
  assert.equal(driftDirection("desk"), "left");
  assert.equal(motionMove({ camera: "drift" }, "desk").direction, "left");
  assert.equal(motionMove({ camera: "push in" }, "desk").direction, undefined, "only a drift has a direction");
});

test("zoompan expressions end the move on the last frame, and only push-in and drift open on the whole keyframe", async () => {
  assert.equal(MOTION_ZOOM, 0.1);
  assert.equal(MOTION_PAN_ZOOM, 1.08);
  assert.equal(MOTION_DRIFT_ZOOM, 0.04);
  assert.equal(MOTION_SOURCE_SCALE, 1.25);
  assert.deepEqual(zoompanExpr({ name: "push-in" }, 180), { z: "1+0.1*on/179", x: "iw/2-(iw/zoom/2)", y: "ih/2-(ih/zoom/2)" });
  assert.deepEqual(zoompanExpr("pull-out", 180), { z: "1.1-0.1*on/179", x: "iw/2-(iw/zoom/2)", y: "ih/2-(ih/zoom/2)" });
  // The crop window slides left for pan-right (the picture travels right) and right for pan-left.
  assert.deepEqual(zoompanExpr("pan-right", 180), { z: "1.08", x: "(iw-iw/zoom)*(1-on/179)", y: "(ih-ih/zoom)/2" });
  assert.deepEqual(zoompanExpr("pan-left", 180), { z: "1.08", x: "(iw-iw/zoom)*on/179", y: "(ih-ih/zoom)/2" });
  // The camera tilting up climbs the keyframe: the window slides from the bottom to the top.
  assert.deepEqual(zoompanExpr("tilt-up", 180), { z: "1.08", x: "(iw-iw/zoom)/2", y: "(ih-ih/zoom)*(1-on/179)" });
  assert.deepEqual(zoompanExpr("tilt-down", 180), { z: "1.08", x: "(iw-iw/zoom)/2", y: "(ih-ih/zoom)*on/179" });
  assert.deepEqual(zoompanExpr("drift", 180), { z: "1+0.04*on/179", x: "(iw-iw/zoom)/2+(iw-iw/zoom)*0.15*on/179", y: "ih/2-(ih/zoom/2)" });
  assert.equal(zoompanExpr("push-in", 1).z, "1+0.1*on/1", "a one-frame shot divides by one, not zero");
  assert.equal(zoompanExpr("push-in", 0).z, "1+0.1*on/1");
  // The long video eases its stills (smoothstep) and scales the travel to the shot; a Short keeps the linear forms above.
  const { motionTravel, MOTION_TRAVEL_SECONDS, MOTION_TRAVEL_MIN } = await import("./drama.mjs");
  assert.equal(MOTION_TRAVEL_SECONDS, 6);
  assert.equal(MOTION_TRAVEL_MIN, 0.5);
  assert.equal(motionTravel(180), 1);
  assert.equal(motionTravel(120), 120 / 180);
  assert.equal(motionTravel(90), 0.5);
  assert.equal(motionTravel(30), 0.5, "a short shot keeps half the travel rather than standing still");
  assert.equal(zoompanExpr("push-in", 180, { eased: true }).z, "1+0.1*((on/179)*(on/179)*(3-2*(on/179)))");
  assert.equal(zoompanExpr("pull-out", 90, { travel: 0.5 }).z, "1.05-0.05*on/89");
  assert.equal(zoompanExpr("pan-left", 90, { travel: 0.5 }).x, "(iw-iw/zoom)*0.5*on/89");
  assert.equal(zoompanExpr("tilt-up", 90, { eased: true, travel: 0.5 }).y, "(ih-ih/zoom)*(1-0.5*((on/89)*(on/89)*(3-2*(on/89))))");
  assert.equal(zoompanExpr({ name: "drift", direction: "left" }, 180).x, "(iw-iw/zoom)/2-(iw-iw/zoom)*0.15*on/179");
  assert.equal(zoompanExpr({ name: "drift", direction: "right" }, 180).x, zoompanExpr("drift", 180).x, "no direction drifts right, as before");
  assert.equal(zoompanExpr("drift", 180, { eased: true, travel: 0.5 }).z, "1+0.02*((on/179)*(on/179)*(3-2*(on/179)))");
});

test("a motion segment animates the looped keyframe with zoompan and then encodes exactly like a clip segment", () => {
  const move = motionMove({ camera: "slow push in" });
  const plain = motionSegmentArgs({ keyframe: "keyframes/a.png", frames: 180, move, outFile: "seg.mp4" });
  const inputs = plain.slice(0, plain.indexOf("-filter_complex"));
  assert.deepEqual(inputs, ["-hide_banner", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", "6.000000", "-i", "keyframes/a.png"]);
  const graph = plain[plain.indexOf("-filter_complex") + 1];
  // The RGB keyframe is converted to YUV with the BT.709 matrix before the overlays, as the slides path does; COLOUR's format is then a no-op.
  // A six-second still travels the full move, eased.
  assert.match(graph, /^\[0:v\]scale=2400:1350:flags=lanczos,zoompan=z='1\+0\.1\*\(\(on\/179\)\*\(on\/179\)\*\(3-2\*\(on\/179\)\)\)':x='iw\/2-\(iw\/zoom\/2\)':y='ih\/2-\(ih\/zoom\/2\)':d=1:s=1920x1080:fps=30,scale=1920:1080:out_color_matrix=bt709:out_range=tv,format=yuv420p,trim=end_frame=180,setpts=PTS-STARTPTS\[pic\];\[pic\]format=yuv420p,setparams=/);
  const brief = motionSegmentArgs({ keyframe: "keyframes/a.png", frames: 90, move, outFile: "seg.mp4" });
  assert.match(brief[brief.indexOf("-filter_complex") + 1], /zoompan=z='1\+0\.05\*\(\(on\/89\)/, "a three-second still travels half as far, at the same speed");
  for (const expected of ["zoompan=", "s=1920x1080", "fps=30", "trim=end_frame=180"]) assert.ok(graph.includes(expected), expected);
  assert.equal(plain[plain.indexOf("-frames:v") + 1], "180");
  assert.doesNotMatch(graph, /overlay|tpad|setpts=PTS\//);
  // Everything from -c:v on is the clip segment's, so joinArgs still copies the streams.
  const clip = clipSegmentArgs({ clip: "clips/a.mp4", frames: 180, fit: fitPlan(180, 180), outFile: "seg.mp4" });
  assert.deepEqual(plain.slice(plain.indexOf("-c:v")), clip.slice(clip.indexOf("-c:v")));
  assert.deepEqual(plain.slice(plain.indexOf("-map"), plain.indexOf("-c:v")), clip.slice(clip.indexOf("-map"), clip.indexOf("-c:v")));

  const full = motionSegmentArgs({ keyframe: "keyframes/a.png", frames: 180, move: { name: "pan-left" }, subtitlesList: "segments/a-subtitles.ffconcat", dissolveFrom: "build/last-prev.png", outFile: "seg.mp4" });
  const fullInputs = full.filter((_, index) => full[index - 1] === "-i");
  assert.deepEqual(fullInputs, ["keyframes/a.png", "segments/a-subtitles.ffconcat", "build/last-prev.png"]);
  const chain = full[full.indexOf("-filter_complex") + 1];
  const clipFull = clipSegmentArgs({ clip: "clips/a.mp4", frames: 180, fit: fitPlan(180, 180), subtitlesList: "segments/a-subtitles.ffconcat", dissolveFrom: "build/last-prev.png", outFile: "seg.mp4" });
  const tail = (args) => args[args.indexOf("-filter_complex") + 1].slice(args[args.indexOf("-filter_complex") + 1].indexOf("[pic];"));
  assert.equal(tail(full), tail(clipFull), "the dissolve, strips and colour chain is the clip segment's");
  assert.match(chain, /zoompan=z='1\.08':x='\(iw-iw\/zoom\)\*\(\(on\/179\)\*\(on\/179\)\*\(3-2\*\(on\/179\)\)\)'/);
  assert.match(chain, /\[2:v\]scale=1920:1080,format=yuva420p,fade=t=out.*\[prev\];\[pic\]\[prev\]overlay=0:0:eof_action=pass\[dissolved\];\[1:v\]format=rgba\[strips\];\[dissolved\]\[strips\]overlay=0:main_h-overlay_h:eof_action=pass\[captioned\];\[captioned\]format=yuv420p/);
  assert.deepEqual(full.slice(full.indexOf("-c:v")), clipFull.slice(clipFull.indexOf("-c:v")));

  // The keyframe check runs the picture chain alone, so strips and dissolves never count against it.
  const psnr = motionFramePsnrArgs("keyframes/a.png", move, 180);
  assert.deepEqual(psnr.slice(0, 6), ["-hide_banner", "-nostats", "-i", "keyframes/a.png", "-i", "keyframes/a.png"]);
  const lavfi = psnr[psnr.indexOf("-lavfi") + 1];
  assert.match(lavfi, /^\[0:v\]scale=2400:1350:flags=lanczos,zoompan=z='1\+0\.1\*\(\(on\/179\)\*\(on\/179\)\*\(3-2\*\(on\/179\)\)\)'.*:d=1:s=1920x1080:fps=30,select=eq\(n\\,0\),format=rgb24\[a\];\[1:v\]scale=1920:1080,format=rgb24\[b\];\[a\]\[b\]psnr$/);
  assert.deepEqual(psnr.slice(-5), ["-frames:v", "1", "-f", "null", "-"]);
});

test("motion segment keys change with the keyframe, the move, the strips, the dissolve source and the encoder", () => {
  const scene = { id: "a", frames: 180, keyframe: { file: "keyframes/a.png", sha256: "1".repeat(64) }, transition: "cut" };
  const move = motionMove({ camera: "push in" });
  const base = motionSegmentKey(scene, move);
  assert.match(base, /^[0-9a-f]{16}$/);
  assert.equal(motionSegmentKey({ ...scene }, { ...move }), base);
  assert.notEqual(motionSegmentKey({ ...scene, keyframe: { file: "keyframes/a.png", sha256: "2".repeat(64) } }, move), base);
  assert.notEqual(motionSegmentKey({ ...scene, keyframe: { file: "keyframes/a-2.png", sha256: "1".repeat(64) } }, move), base);
  assert.notEqual(motionSegmentKey({ ...scene, frames: 181 }, move), base);
  assert.notEqual(motionSegmentKey(scene, motionMove({ camera: "pull back" })), base);
  assert.notEqual(motionSegmentKey(scene, { name: "drift", direction: "left" }), motionSegmentKey(scene, { name: "drift", direction: "right" }), "a drift's direction is part of its key");
  assert.notEqual(motionSegmentKey(scene, move, [{ file: "frames/sub-x.png", frames: 180 }]), base);
  assert.notEqual(motionSegmentKey({ ...scene, transition: "dissolve" }, move, null, "prevkey"), base);
  assert.notEqual(motionSegmentKey({ ...scene, transition: "dissolve" }, move, null, "otherkey"), motionSegmentKey({ ...scene, transition: "dissolve" }, move, null, "prevkey"));
  const clipScene = { ...scene, clip: { file: "keyframes/a.png", sha256: "1".repeat(64) } };
  assert.notEqual(clipSegmentKey(clipScene, fitPlan(180, 180)), base, "a clip and a motion segment of the same file never share a key");
});

test("a scene's subtitle track covers exactly its frames, blank where nobody speaks", () => {
  const scene = { id: "s", start_frame: 100, frames: 90 };
  const cues = [
    { line: "a", start_frame: 40, end_frame: 110, file: "frames/sub-a.png" },
    { line: "b", start_frame: 120, end_frame: 150, file: "frames/sub-b.png" },
    { line: "c", start_frame: 150, end_frame: 170, file: "frames/sub-c.png" },
    { line: "d", start_frame: 185, end_frame: 240, file: "frames/sub-d.png" },
    { line: "z", start_frame: 300, end_frame: 330, file: "frames/sub-z.png" },
  ];
  const track = subtitleTrack(scene, cues, "frames/sub-blank.png");
  assert.deepEqual(track, [
    { file: "frames/sub-a.png", frames: 10 },
    { file: "frames/sub-blank.png", frames: 10 },
    { file: "frames/sub-b.png", frames: 30 },
    { file: "frames/sub-c.png", frames: 20 },
    { file: "frames/sub-blank.png", frames: 15 },
    { file: "frames/sub-d.png", frames: 5 },
  ]);
  assert.equal(track.reduce((sum, entry) => sum + entry.frames, 0), scene.frames);
  assert.deepEqual(subtitleTrack(scene, [], "frames/sub-blank.png"), [{ file: "frames/sub-blank.png", frames: 90 }]);
  // Two cues sharing a strip and touching each other are one entry.
  const same = subtitleTrack({ id: "s", start_frame: 0, frames: 20 }, [{ start_frame: 0, end_frame: 10, file: "x" }, { start_frame: 10, end_frame: 20, file: "x" }], "blank");
  assert.deepEqual(same, [{ file: "x", frames: 20 }]);
});

test("a probed clip's frames come from its packet count at 30 fps, else from its duration", () => {
  assert.equal(clipFrames({ streams: [{ codec_type: "video", r_frame_rate: "30/1", nb_read_packets: "241", duration: "8.03" }] }), 241);
  assert.equal(clipFrames({ streams: [{ codec_type: "video", r_frame_rate: "24/1", nb_read_packets: "192", duration: "8.000000" }] }), 240);
  assert.throws(() => clipFrames({ streams: [{ codec_type: "audio" }] }), PlanError);
});

test("a clip segment scales, slows, holds, cuts, dissolves and captions in one graph, tuned for film", () => {
  const fit = fitPlan(180, 240, "auto");
  const plain = clipSegmentArgs({ clip: "clips/a.mp4", frames: 240, fit, outFile: "seg.mp4" });
  const graph = plain[plain.indexOf("-filter_complex") + 1];
  assert.match(graph, /^\[0:v\]scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,pad=1920:1080:\(ow-iw\)\/2:\(oh-ih\)\/2,setpts=PTS\/0\.85,fps=30,tpad=stop_mode=clone:stop_duration=\d+\.\d+,trim=end_frame=240,setpts=PTS-STARTPTS\[pic\];\[pic\]format=yuv420p,setparams=/);
  assert.doesNotMatch(graph, /overlay/);
  assert.ok(plain.includes("-tune") && plain[plain.indexOf("-tune") + 1] === "film");
  assert.ok(!plain.includes("stillimage"));
  assert.equal(plain[plain.indexOf("-frames:v") + 1], "240");
  assert.deepEqual(plain.slice(-2), ["-an", "seg.mp4"]);

  const exact = clipSegmentArgs({ clip: "clips/a.mp4", frames: 240, fit: fitPlan(300, 240), outFile: "seg.mp4" });
  assert.doesNotMatch(exact[exact.indexOf("-filter_complex") + 1], /setpts=PTS\/|tpad/);

  const full = clipSegmentArgs({ clip: "clips/a.mp4", frames: 240, fit, subtitlesList: "segments/a-subtitles.ffconcat", dissolveFrom: "build/last-prev.png", outFile: "seg.mp4" });
  const inputs = full.filter((_, index) => full[index - 1] === "-i");
  assert.deepEqual(inputs, ["clips/a.mp4", "segments/a-subtitles.ffconcat", "build/last-prev.png"]);
  const chain = full[full.indexOf("-filter_complex") + 1];
  assert.match(chain, new RegExp(`\\[2:v\\]scale=1920:1080,format=yuva420p,fade=t=out:st=0:d=${(DISSOLVE_FRAMES / 30).toFixed(6)}:alpha=1\\[prev\\];\\[pic\\]\\[prev\\]overlay=0:0:eof_action=pass\\[dissolved\\]`));
  assert.match(chain, /\[1:v\]format=rgba\[strips\];\[dissolved\]\[strips\]overlay=0:main_h-overlay_h:eof_action=pass\[captioned\];\[captioned\]format=yuv420p/);
  assert.ok(full.includes("-loop"), "the dissolve frame is a looped image input");
  assert.deepEqual(lastFrameArgs("seg.mp4", 240, "last.png").slice(-7), ["-vf", "select=eq(n\\,239)", "-fps_mode", "passthrough", "-frames:v", "1", "last.png"]);
});

test("clip segment keys change with the clip, the fit, the strips, the dissolve source and the encoder", () => {
  const scene = { id: "a", frames: 240, clip: { file: "clips/a.mp4", sha256: "1".repeat(64) }, transition: "cut" };
  const fit = fitPlan(240, 240);
  const base = clipSegmentKey(scene, fit);
  assert.match(base, /^[0-9a-f]{16}$/);
  assert.equal(clipSegmentKey({ ...scene }, { ...fit }), base);
  assert.notEqual(clipSegmentKey({ ...scene, clip: { file: "clips/a.mp4", sha256: "2".repeat(64) } }, fit), base);
  assert.notEqual(clipSegmentKey(scene, fitPlan(200, 240)), base);
  assert.notEqual(clipSegmentKey(scene, fit, [{ file: "frames/sub-x.png", frames: 240 }]), base);
  assert.notEqual(clipSegmentKey({ ...scene, transition: "dissolve" }, fit, null, "prevkey"), base);
  assert.notEqual(clipSegmentKey({ ...scene, transition: "dissolve" }, fit, null, "otherkey"), clipSegmentKey({ ...scene, transition: "dissolve" }, fit, null, "prevkey"));
});

test("the mix ducks the music under the voice, keeps the voice's length and normalizes after", () => {
  assert.equal(duckRatio(-10), 2);
  assert.equal(duckRatio(0), 1);
  assert.equal(duckRatio(-40), 20, "capped");
  const filter = mixFilter(MUSIC, 120);
  assert.match(filter, /^\[1:a\]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:120\.000000,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1\.500,afade=t=out:st=117\.000000:d=3\.000,volume=-20dB\[bed\];/);
  assert.match(filter, /\[0:a\]aformat=sample_rates=48000:channel_layouts=mono,pan=stereo\|c0=c0\|c1=c0,asplit=2\[voice\]\[side\];/);
  assert.match(filter, /\[bed\]\[side\]sidechaincompress=threshold=0\.03:ratio=2:attack=30:release=500:makeup=1:level_sc=1\[ducked\];/);
  assert.match(filter, /\[voice\]\[ducked\]amix=inputs=2:duration=first:dropout_transition=0:normalize=0\[mix\]$/);
  const measure = measureMixArgs("narration.wav", "music/x.wav", MUSIC, 120);
  assert.deepEqual(measure.slice(0, 10), ["-hide_banner", "-nostats", "-i", "narration.wav", "-stream_loop", "-1", "-t", "120.000000", "-i", "music/x.wav"]);
  assert.match(measure[measure.indexOf("-filter_complex") + 1], /\[mix\]loudnorm=I=-14:TP=-1:LRA=11:print_format=json\[out\]$/);
  assert.deepEqual(measure.slice(-4), ["-map", "[out]", "-f", "null", "-"].slice(1));
  const measured = { input_i: "-23.1", input_tp: "-5.0", input_lra: "6.0", input_thresh: "-33.5", target_offset: "0.1" };
  const mix = mixArgs("narration.wav", "music/x.wav", MUSIC, 120, measured, "audio.m4a");
  assert.match(mix[mix.indexOf("-filter_complex") + 1], /measured_I=-23\.1:measured_TP=-5\.0:measured_LRA=6\.0:measured_thresh=-33\.5:offset=0\.1:linear=true,aresample=48000\[out\]$/);
  assert.deepEqual(mix.slice(-7), ["-c:a", "aac", "-b:a", "384k", "-ar", "48000", "audio.m4a"]);
  const bed = bedLoudnessArgs("narration.wav", "music/x.wav", MUSIC, 120);
  assert.match(bed[bed.indexOf("-filter_complex") + 1], /volume=-20dB\[bed\];\[bed\]ebur128=peak=true\[out\]$/);
  // The bed measured at -33 LUFS in a mix that loudnorm lifts by 9.1 dB ends near -24: just fine.
  assert.equal(bedLevel(-33.2, measured), -24.1);
  assert.deepEqual(checkBed(-24.1), []);
  assert.match(checkBed(-20)[0], /music bed at -20 LUFS in the mix, above -24/);
});

test("a shot's first frame must look like its keyframe", () => {
  assert.equal(keyframeProblem({ id: "a" }, 40), null);
  assert.equal(keyframeProblem({ id: "a" }, Infinity), null);
  assert.match(keyframeProblem({ id: "a" }, 18.4), /shot a frame 0 does not look like its keyframe \(PSNR 18\.4 dB/);
});

test("the stand-in clips ask for whole seconds between 4 and 10, one short and one long", () => {
  assert.equal(clipSeconds(30), 4);
  assert.equal(clipSeconds(170), 6);
  assert.equal(clipSeconds(900), 10);
  assert.ok(SHORT_BY_SECONDS > 0 && LONG_BY_SECONDS > 0);
});

test("package trusts checks.json only for the very same script, and a drama's look, clips, subtitles and music too", () => {
  const slides = fixture();
  const lexicon = { terms: {} };
  const { speechHash, visualHash } = { speechHash: (doc) => doc, visualHash: (doc) => doc };
  assert.ok(speechHash && visualHash);
  const drama = dramaFixture();
  const good = (doc) => ({ ok: true, speech_hash: undefined, visual_hash: undefined, look_hash: undefined, subtitles_hash: undefined, mix_hash: undefined, clips_hash: "c1", doc });
  assert.equal(checksCurrent(slides, lexicon, { ok: false }), false);
  assert.equal(checksCurrent(drama, lexicon, good(drama), { clips_hash: "c1" }), false, "hashes of another script are refused");
  // UPLOAD.md keeps only the Studio steps: a drama's disclosure is ticked as metadata.json says
  // (the self-check list moved into the automatic checks, docs/videos/HANDS-OFF.md).
  const list = uploadChecklist({ metadata: { title: "t", made_for_kids: false, category_id: 24 }, captions: [], thumbnail: false, drama: true });
  assert.match(list, /「變造或合成內容」：勾「是」。`metadata\.json` 的 `contains_synthetic_media` 是 `true`/);
  assert.doesNotMatch(list, /- \[ \]/);
  const plain = uploadChecklist({ metadata: { title: "t", made_for_kids: false, category_id: 28 }, captions: [], thumbnail: true });
  assert.match(plain, /「變造或合成內容」：不用勾。`metadata\.json` 的 `contains_synthetic_media` 是 `false`/);
  assert.doesNotMatch(plain, /音樂授權/);
});

test("illustrated slides lay out as shots under moves, single-state cards drifting in turn, cuts between pictures except after a pause beat, and cuts into chapters", async () => {
  const { illustratedFixture } = await import("../core/fixtures/load.mjs");
  const { illustratedTransition, CARD_MOVES, MOTION_CARD_VERSION, DISSOLVE_BEAT_MS, effectsFilter, soundGraph } = await import("./drama.mjs");
  const doc = illustratedFixture();
  const timeline = estimateTimeline(doc);
  const frames = framesManifestFor(doc, timeline);
  const keyframes = { shots: Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `keyframes/${scene.id}-1.png`, sha256: "e".repeat(64) }])) };
  const layout = layoutDrama(doc, timeline, frames, null, keyframes, { transitionRule: illustratedTransition, cardMotion: true });
  // The title's line ends on a 600 ms beat, so the first picture dissolves in; the clock says
  // "dissolve" itself; every other change is a cut.
  assert.deepEqual(
    layout.map((scene) => [scene.id, scene.kind, scene.card ?? false, scene.transition ?? null, scene.move?.name ?? null]),
    [
      ["hook", "motion", true, "cut", "drift"],
      ["podium", "motion", false, "dissolve", "push-in"],
      ["desk", "motion", false, "cut", "drift"],
      ["clock", "motion", false, "dissolve", "tilt-down"],
      ["numbers", "stills", false, null, null],
      ["race", "motion", false, "cut", "pan-left"],
      ["rule", "motion", true, "cut", "push-in"],
      ["door", "motion", false, "cut", "push-in"],
      ["wrap", "motion", true, "cut", "drift"],
    ],
  );
  assert.equal(DISSOLVE_BEAT_MS, 600);
  const shot = { template: "shot", data: {}, lines: [] };
  assert.equal(illustratedTransition(shot, 3, { lines: [{ text: "。", pause_after_ms: 600 }] }), "dissolve");
  assert.equal(illustratedTransition(shot, 3, { lines: [{ text: "。", pause_after_ms: 300 }] }), "cut");
  assert.equal(illustratedTransition(shot, 3, { lines: [{ text: "。" }] }), "cut");
  assert.equal(illustratedTransition(shot, 3, null), "cut");
  assert.equal(illustratedTransition({ ...shot, chapter: "下一章" }, 3, { lines: [{ text: "。", pause_after_ms: 1200 }] }), "cut", "a chapter opener is the beat itself");
  assert.equal(illustratedTransition({ ...shot, data: { transition: "dissolve" } }, 3, null), "dissolve", "the writer's word wins");
  assert.equal(illustratedTransition({ ...shot, data: { transition: "cut" } }, 3, { lines: [{ text: "。", pause_after_ms: 900 }] }), "cut");
  assert.equal(illustratedTransition(shot, 0, null), "cut");
  // Drifting cards take turns going right and left; the shots' drifts go where their ids say.
  assert.equal(layout[0].move.direction, "right");
  assert.equal(layout[8].move.direction, "left");
  assert.equal(layout[2].move.direction, "left", "desk drifts left (its id's sum is odd)");
  assert.equal(layout[6].move.direction, undefined, "a push-in has no direction");
  assert.deepEqual(CARD_MOVES, ["drift", "push-in"]);
  assert.deepEqual(layout[0].keyframe, { file: "frames/hook-0.png", sha256: null }, "a card's picture is its rendered still");
  assert.equal(layout.reduce((sum, scene) => sum + scene.frames, 0), timeline.total_frames);
  // A card's segment key carries the card version, so no drama's motion key moves.
  const card = { ...layout[0], frames: 90, keyframe: { file: "frames/x.png", sha256: null } };
  const still = { ...card, card: undefined };
  assert.notEqual(motionSegmentKey(card, card.move), motionSegmentKey(still, still.move));
  assert.equal(MOTION_CARD_VERSION, "card-motion-v1");
  // Without the options, the same document lays out as a drama would: cards held as stills, shots cut in.
  const plain = layoutDrama(doc, timeline, frames, null, keyframes);
  assert.deepEqual(plain.map((scene) => scene.kind), ["stills", "motion", "motion", "motion", "stills", "motion", "stills", "motion", "stills"]);
  assert.equal(plain[1].transition, "cut");
  assert.equal(plain[3].transition, "dissolve", "the shot's own word still counts");
  // The effects join the mix as a third input; without music they sit over the voice alone.
  assert.match(mixFilter(MUSIC, 120, 2), /\[2:a\]aformat=sample_rates=48000:channel_layouts=stereo\[effects\];\[voice\]\[ducked\]\[effects\]amix=inputs=3:duration=first:dropout_transition=0:normalize=0\[mix\]$/);
  assert.equal(mixFilter(MUSIC, 120), mixFilter(MUSIC, 120, null), "no effects: the drama's mix, unchanged");
  assert.match(effectsFilter(), /^\[0:a\]aformat=sample_rates=48000:channel_layouts=mono,pan=stereo\|c0=c0\|c1=c0\[voice\];\[1:a\]aformat=sample_rates=48000:channel_layouts=stereo\[effects\];\[voice\]\[effects\]amix=inputs=2/);
  assert.deepEqual(soundGraph("n.wav", { musicFile: "m.mp3", music: MUSIC, sfxFile: "fx.wav" }, 120).inputs, ["-i", "n.wav", "-stream_loop", "-1", "-t", "120.000000", "-i", "m.mp3", "-i", "fx.wav"]);
  assert.deepEqual(soundGraph("n.wav", { sfxFile: "fx.wav" }, 120).inputs, ["-i", "n.wav", "-i", "fx.wav"]);
  assert.throws(() => soundGraph("n.wav", {}, 120), PlanError);
  const measured = { input_i: "-23.1", input_tp: "-5.0", input_lra: "6.0", input_thresh: "-33.5", target_offset: "0.1" };
  assert.deepEqual(mixArgs("n.wav", "m.mp3", MUSIC, 120, measured, "a.m4a"), mixArgs("n.wav", "m.mp3", MUSIC, 120, measured, "a.m4a", null), "the drama's arguments are unchanged");
  assert.equal(measureMixArgs("n.wav", null, null, 120, "fx.wav").indexOf("-stream_loop"), -1);
});

test("package trusts an illustrated cut only with its very pictures, music and effects", async () => {
  const { illustratedFixture, fixtureLexicon } = await import("../core/fixtures/load.mjs");
  const { keyframesHash, lookHash, mixHash, sfxHash } = await import("../core/drama.mjs");
  const { speechHash, visualHash } = await import("../core/timeline.mjs");
  const doc = illustratedFixture();
  const lexicon = fixtureLexicon();
  const keyframes = { shots: Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: "k.png", sha256: "f".repeat(64) }])) };
  const checks = { ok: true, speech_hash: speechHash(doc, lexicon), visual_hash: visualHash(doc), look_hash: lookHash(doc), pictures_hash: keyframesHash(doc, keyframes), mix_hash: mixHash(doc), sfx_hash: sfxHash(doc) };
  assert.equal(checksCurrent(doc, lexicon, checks, null, keyframes), true);
  assert.equal(checksCurrent(doc, lexicon, checks, null, null), false, "the pictures must be there to compare");
  assert.equal(checksCurrent(doc, lexicon, checks, null, { shots: { ...keyframes.shots, podium: { file: "k.png", sha256: "0".repeat(64) } } }), false, "a redrawn picture");
  assert.equal(checksCurrent(doc, lexicon, { ...checks, mix_hash: "x" }, null, keyframes), false, "other music");
  assert.equal(checksCurrent(doc, lexicon, { ...checks, sfx_hash: "x" }, null, keyframes), false, "other effects");
  const plain = fixture();
  assert.equal(checksCurrent(plain, lexicon, { ok: true, speech_hash: speechHash(plain, lexicon), visual_hash: visualHash(plain) }), true, "plain slides as before");
});
