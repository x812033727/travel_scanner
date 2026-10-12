import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { validateBranding } from "../core/branding.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { packageSelection } from "./cli.mjs";
import { audioFilter, BASE_FRAMES, buildOutro, layerPlan, measureArgs, OUTRO_FRAMES, outroArgs, PACKAGES, slotDistance, SLOTS, videoFilter } from "./outro.mjs";

test("the outro is 21 seconds: a held pause, the like/share/bell clip, then the end-screen canvas", () => {
  assert.equal(OUTRO_FRAMES, 630);
  const filter = videoFilter();
  assert.match(filter, /\[0:v\]trim=end_frame=90,setpts=N\/\(30\*TB\),tpad=start=30:start_mode=clone,/);
  assert.match(filter, /color=c=0xF6F0E4:s=1920x1080:r=30:d=17,/);
  assert.match(filter, /\[base\]\[canvas\]concat=n=2:v=1:a=0\[v\]$/);
  // The base clip's icons fade out first, and the outlines only start fading in after them.
  assert.match(filter, /fade=out:d=0\.5:alpha=1\[icons\]/);
  assert.match(filter, /fade=in:st=0\.5:d=0\.5:alpha=1\[stroke\]/);
});

test("the slot outlines are a distance field over both videos and the subscribe circle", () => {
  const distance = slotDistance();
  assert.equal(distance.match(/hypot/g).length, 3);
  assert.match(distance, /hypot\(X-960,Y-550\)-148/);
  // One row, as saved in Studio: video | subscribe | video, symmetric about the centre, inside
  // Studio's safe area, and clear of the wordmark above.
  const [left, right] = SLOTS.videos;
  const { cx, cy, r } = SLOTS.subscribe;
  for (const video of SLOTS.videos) assert.ok(Math.abs(video.w / video.h - 16 / 9) < 0.01);
  // Dragged in Studio's quarter-size preview, so symmetric to within a few pixels.
  assert.ok(Math.abs(left.x + left.w / 2 + right.x + right.w / 2 - 2 * cx) <= 4);
  assert.ok(left.x + left.w < cx - r && cx + r < right.x);
  for (const top of [left.y, cy - r]) assert.ok(top > 335 && top >= 140);
  for (const bottom of [left.y + left.h, cy + r]) assert.ok(bottom <= 912);
});

test("the music plays under the sound effects, rises after them and fades out at the end", () => {
  const measure = audioFilter({ musicStart: 106.5 });
  assert.match(measure, /\[2:a:0\]atrim=start=106\.5:duration=21,/);
  assert.match(measure, /volume='0\.4\+0\.6\*clip\(\(t-3\.5\)\/1,0,1\)':eval=frame/);
  assert.match(measure, /afade=t=out:st=19\.5:d=1\.5/);
  assert.match(measure, /adelay=1000:all=1,/);
  assert.match(measure, /afade=t=in:d=1,/);
  assert.match(measure, /atrim=end_sample=1008000,loudnorm=I=-16:TP=-1:LRA=11:print_format=json/);
  const measured = { input_i: "-12.1", input_tp: "-0.4", input_lra: "2.5", input_thresh: "-22.3", target_offset: "0.1" };
  assert.match(audioFilter({ musicStart: 0, measured }), /measured_I=-12\.1:.*offset=0\.1:linear=true/);
  assert.throws(() => audioFilter({ musicStart: -1 }), /--music-start/);
  assert.throws(() => audioFilter({ musicStart: Number.NaN }), /--music-start/);
});

test("both passes read the same inputs; the second maps picture and sound into one 630-frame file", () => {
  const layers = layerPlan("L");
  const common = { base: "outro.mp4", last: "last.png", music: "m.mp3", layers, musicStart: 3 };
  const first = measureArgs(common);
  assert.deepEqual(first.slice(first.indexOf("-i"), first.indexOf("-filter_complex")), outroArgs({ ...common, measured: {}, outFile: "o.mp4" }).filter((arg, index, all) => index >= all.indexOf("-i") && index < all.indexOf("-filter_complex")));
  const second = outroArgs({ ...common, measured: { input_i: -12 }, outFile: "o.mp4" });
  assert.equal(second[second.indexOf("-frames:v") + 1], "630");
  assert.deepEqual(second.slice(second.indexOf("-map"), second.indexOf("-map") + 4), ["-map", "[v]", "-map", "[a]"]);
  assert.equal(second.at(-1), "o.mp4");
  assert.equal(layers.stroke.at(-1), path.join("L", "stroke.png"));
});

// A fake ffmpeg/ffprobe: writes each output file and reports the frame counts real media would.
function fakeTools(frames) {
  const calls = [];
  const exec = async (tool, args) => {
    calls.push({ tool, args });
    if (tool === "probe") return { stdout: JSON.stringify({ streams: [{ codec_type: "video", nb_read_packets: String(frames[path.basename(args.at(-1))] ?? 0) }] }), stderr: "" };
    if (args.includes("-f") && args.at(-1) === "-") return { stdout: "", stderr: '{ "input_i" : "-12.0", "input_tp" : "-0.5", "input_lra" : "2.0", "input_thresh" : "-22.0", "target_offset" : "0.2" }' };
    writeFileSync(args.at(-1), `made by ${args.at(-1)}`);
    return { stdout: "", stderr: "" };
  };
  return { tools: { ffmpeg: "encode", ffprobe: "probe" }, exec, calls };
}

test("buildOutro writes an installable package per intro", async () => {
  const box = sandbox();
  const src = path.join(box.base, "src");
  mkdirSync(src);
  for (const file of ["base.mp4", "intro.mp4", "series.mp4", "track.mp3"]) writeFileSync(path.join(src, file), file);
  const { tools, exec, calls } = fakeTools({ "base.mp4": BASE_FRAMES, "intro.mp4": 150, "series.mp4": 357, "outro.mp4": OUTRO_FRAMES });
  const out = path.join(box.base, "out");
  const result = await buildOutro({ base: path.join(src, "base.mp4"), music: path.join(src, "track.mp3"), musicStart: 106.5, intros: { channel: path.join(src, "intro.mp4"), sothatswhy: path.join(src, "series.mp4") }, out, tools, exec });
  assert.equal(result.measured.input_i, "-12.0");
  const second = calls.find((call) => call.args.includes("[v]"));
  assert.match(second.args.join(" "), /measured_I=-12\.0/);
  for (const [name, introFrames] of [["channel", 150], ["sothatswhy", 357]]) {
    const manifest = JSON.parse(readFileSync(path.join(out, name, "manifest.json"), "utf8"));
    assert.equal(manifest.package_id, PACKAGES[name].id);
    assert.equal(manifest.outro_source.music_start_seconds, 106.5);
    const selection = packageSelection(path.join(out, name));
    assert.equal(selection.intro.frames, introFrames);
    assert.equal(selection.outro.frames, OUTRO_FRAMES);
    assert.ok(validateBranding(selection).hash);
  }
});

test("buildOutro refuses a base that is not the 90-frame like/share/bell clip", async () => {
  const box = sandbox();
  for (const file of ["outro.mp4", "intro.mp4", "track.mp3"]) writeFileSync(path.join(box.base, file), file);
  const { tools, exec } = fakeTools({ "outro.mp4": 600, "intro.mp4": 150 });
  await assert.rejects(buildOutro({ base: path.join(box.base, "outro.mp4"), music: path.join(box.base, "track.mp3"), musicStart: 0, intros: { channel: path.join(box.base, "intro.mp4") }, out: path.join(box.base, "out"), tools, exec }), /90-frame/);
});
