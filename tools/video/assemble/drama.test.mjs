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
  subtitleTrack,
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

test("the slides encoder version is untouched, so no published video's segments are redone", () => {
  assert.equal(ENCODER_VERSION, "x264-high-crf18-stillimage-g60-bf2-bt709-v2");
  assert.notEqual(CLIP_ENCODER_VERSION, ENCODER_VERSION);
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
  const list = uploadChecklist({ metadata: { title: "t", made_for_kids: false, category_id: 24 }, captions: [], thumbnail: false, drama: true });
  assert.match(list, /合成內容揭露.*一律勾「是」/);
  assert.match(list, /每集劇情獨立/);
  assert.match(list, /音樂授權/);
  assert.match(list, /站主看過並核准了每一個關卡/);
  const plain = uploadChecklist({ metadata: { title: "t", made_for_kids: false, category_id: 28 }, captions: [], thumbnail: true });
  assert.match(plain, /AI 使用揭露/);
  assert.doesNotMatch(plain, /音樂授權/);
});
