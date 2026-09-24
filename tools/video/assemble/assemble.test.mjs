import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "../core/fixtures/load.mjs";
import { estimateTimeline } from "../core/timeline.mjs";
import {
  checkLoudness,
  checkProbe,
  concatList,
  layoutScenes,
  measureLoudnessArgs,
  normalizeArgs,
  parseEbur128,
  parseLoudnorm,
  parsePsnr,
  PlanError,
  psnrArgs,
  segmentArgs,
  segmentKey,
  segmentSamples,
} from "./plan.mjs";

function manifestFor(timeline, transitions = 3) {
  return {
    scenes: timeline.scenes.map((scene) => ({
      id: scene.id,
      states: scene.states.map((_, index) => ({
        still: `frames/${scene.id}-${index}.png`,
        transition: Array.from({ length: transitions }, (__, frame) => `frames/${scene.id}-${index}-t${frame}.png`),
      })),
    })),
  };
}

test("each scene lays out transition frames one by one, then its still, adding up to the scene's frames", () => {
  const timeline = estimateTimeline(fixture());
  const layout = layoutScenes(timeline, manifestFor(timeline));
  for (const [index, scene] of layout.entries()) {
    assert.equal(scene.entries.reduce((sum, entry) => sum + entry.frames, 0), timeline.scenes[index].end_frame - timeline.scenes[index].start_frame);
  }
  const bullets = layout.find((scene) => scene.id === "questions");
  assert.deepEqual(bullets.entries.slice(0, 4).map((entry) => [entry.file, entry.frames]), [
    ["frames/questions-0-t0.png", 1],
    ["frames/questions-0-t1.png", 1],
    ["frames/questions-0-t2.png", 1],
    ["frames/questions-0.png", bullets.entries[3].frames],
  ]);
});

test("a state shorter than its transition keeps the transition's first frames only", () => {
  const timeline = { scenes: [{ id: "a", start_frame: 0, end_frame: 2, states: [{ start_frame: 0, end_frame: 2 }] }] };
  const layout = layoutScenes(timeline, manifestFor(timeline, 9));
  assert.deepEqual(layout[0].entries, [{ file: "frames/a-0-t0.png", frames: 1 }, { file: "frames/a-0.png", frames: 1 }]);
});

test("frames rendered for another script are refused", () => {
  const timeline = estimateTimeline(fixture());
  const manifest = manifestFor(timeline);
  manifest.scenes[1].states.pop();
  assert.throws(() => layoutScenes(timeline, manifest), PlanError);
  assert.throws(() => layoutScenes(timeline, { scenes: [] }), /run render again/);
});

test("concat lists open every image at 30 fps, round durations from the running total and repeat the last file", () => {
  const entries = [{ file: "a.png", frames: 1 }, { file: "b.png", frames: 1 }, { file: "c's.png", frames: 298 }];
  const text = concatList(entries, (file) => `C:\\work\\${file}`);
  const lines = text.trim().split("\n");
  assert.equal(lines[0], "ffconcat version 1.0");
  assert.equal(lines[1], "file 'C:/work/a.png'");
  assert.equal(lines[2], "option framerate 30");
  assert.equal(lines.at(-2), "file 'C:/work/c'\\''s.png'");
  assert.equal(lines.at(-1), "option framerate 30");
  const total = lines.filter((line) => line.startsWith("duration ")).reduce((sum, line) => sum + Number(line.slice(9)), 0);
  assert.ok(Math.abs(total - 10) < 1e-6, `durations add up to ${total}`);
});

test("segment keys change with the pictures and the encoder settings only", () => {
  const scene = { frames: 30, entries: [{ file: "a.png", frames: 30 }] };
  assert.equal(segmentKey(scene), segmentKey(structuredClone(scene)));
  assert.notEqual(segmentKey(scene), segmentKey({ ...scene, entries: [{ file: "b.png", frames: 30 }] }));
});

test("the encoder arguments pin the frame count, H.264 High, BT.709 and no audio", () => {
  const args = segmentArgs("list.ffconcat", "out.mp4", 428).join(" ");
  for (const expected of ["-frames:v 428", "-profile:v high", "-bf 2", "-tune stillimage", "colorprim=bt709", "setparams=range=tv:color_primaries=bt709", "out_color_matrix=bt709", "-fps_mode cfr", "-an"]) {
    assert.ok(args.includes(expected), expected);
  }
});

test("loudness is measured and normalized after going stereo, linearly, to AAC-LC 384k", () => {
  assert.match(measureLoudnessArgs("n.wav").join(" "), /pan=stereo\|c0=c0\|c1=c0,loudnorm=I=-14:TP=-1:LRA=11:print_format=json/);
  const measured = parseLoudnorm('[Parsed_loudnorm_1 @ 0x1]\n{\n"input_i" : "-20.10",\n"input_tp" : "-6.00",\n"input_lra" : "3.10",\n"input_thresh" : "-30.50",\n"target_offset" : "0.20"\n}\n');
  const args = normalizeArgs("n.wav", measured, "a.m4a").join(" ");
  assert.match(args, /pan=stereo.*measured_I=-20\.10:measured_TP=-6\.00:measured_LRA=3\.10:measured_thresh=-30\.50:offset=0\.20:linear=true/);
  assert.match(args, /-c:a aac -b:a 384k -ar 48000/);
  assert.throws(() => parseLoudnorm("nothing"), PlanError);
});

test("ebur128 and psnr summaries are read from ffmpeg's stderr", () => {
  const ebur = "... Summary:\n\n  Integrated loudness:\n    I:         -13.9 LUFS\n    Threshold: -24.1 LUFS\n\n  True peak:\n    Peak:      -12.8 dBFS\n";
  assert.deepEqual(parseEbur128(ebur), { integrated: -13.9, truePeak: -12.8 });
  assert.equal(parsePsnr("[Parsed_psnr_2 @ 0x] PSNR r:47.1 g:48.2 b:47.9 average:47.72 min:47.1 max:48.2"), 47.72);
  assert.equal(parsePsnr("PSNR r:inf g:inf b:inf average:inf min:inf max:inf"), Infinity);
  assert.deepEqual(checkLoudness({ integrated: -13.9, truePeak: -12.8 }), []);
  assert.equal(checkLoudness({ integrated: -10.9, truePeak: -0.2 }).length, 2);
});

test("frames are compared by number: first, second and last of each segment", () => {
  const scene = { entries: [{ file: "t0", frames: 1 }, { file: "t1", frames: 1 }, { file: "still", frames: 100 }] };
  assert.deepEqual(segmentSamples(scene), [{ n: 0, file: "t0" }, { n: 1, file: "t1" }, { n: 101, file: "still" }]);
  assert.deepEqual(segmentSamples({ entries: [{ file: "only", frames: 1 }] }), [{ n: 0, file: "only" }]);
  assert.match(psnrArgs("s.mp4", 101, "still.png").join(" "), /select=eq\(n\\,101\)/);
});

test("the probe check wants exactly the timeline's frames and YouTube's recommended streams", () => {
  const good = {
    streams: [
      { codec_type: "video", codec_name: "h264", profile: "High", width: 1920, height: 1080, r_frame_rate: "30/1", pix_fmt: "yuv420p", color_space: "bt709", color_primaries: "bt709", color_transfer: "bt709", nb_read_packets: "1247" },
      { codec_type: "audio", codec_name: "aac", sample_rate: "48000", channels: 2, duration: "41.566667" },
    ],
  };
  assert.deepEqual(checkProbe(good, { frames: 1247 }), []);
  const bad = structuredClone(good);
  bad.streams[0].color_primaries = "unknown";
  bad.streams[0].nb_read_packets = "1246";
  bad.streams[1].channels = 1;
  bad.streams[1].duration = "43.0";
  assert.equal(checkProbe(bad, { frames: 1247 }).length, 4);
});
