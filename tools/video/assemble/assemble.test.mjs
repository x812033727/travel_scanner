import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT } from "../cli.mjs";
import { runtimePolicyHash } from "../core/anime-policy.mjs";
import { lookHash } from "../core/drama.mjs";
import { writeAudioFixture, dramaFixture, fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { eachLine } from "../core/schema.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { buildTimeline, estimateTimeline, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";
import { run } from "./cli.mjs";
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
  rivalImages,
  sampleProblem,
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

test("direct anime assembly rejects a two-minute measured body and estimated or stale timing before media or ffmpeg", async (t) => {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  Object.assign(doc, {
    category: "anime", production_policy: "long-anime-v1", target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "fantasy", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false },
  });
  doc.look.preset = "anime-2d";
  delete doc.music;
  for (const scene of doc.scenes) delete scene.data.fit;
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ ...doc.series, category: doc.category, production_policy: doc.production_policy, runtime_spec: doc.runtime_spec, target_minutes: 22, style_preset: "anime-2d", characters: doc.characters }));
  const lint = lintProject(loadProject({ slug: doc.slug, root: box.root }));
  assert.deepEqual(lint.errors, [], "the approved policy and trusted series projection pass script preflight");
  mkdirSync(box.workdir, { recursive: true });
  const actual = (frames) => {
    // Synthetic WAV sample counts: this test verifies timing, without generating a film or voice.
    const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
    const last = [...eachLine(doc)].at(-1).line.id;
    samples[last] += (frames - buildTimeline(doc, samples).total_frames) * SAMPLES_PER_FRAME;
    return { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, fixtureLexicon()) };
  };
  let ffmpegReached = 0;
  let stderr = "";
  const ctx = {
    root: box.root, home: box.base, EXIT,
    env: { VIDEO_WORKDIR: box.work, get FFMPEG_PATH() { ffmpegReached += 1; throw new Error("ffmpeg sentinel"); } },
    stdout: { write() {} }, stderr: { write(value) { stderr += value; } },
  };
  for (const [name, timeline, expected] of [
    ["two-minute body", actual(3_600), /body is 3600 frames/],
    ["estimated body", { ...actual(39_600), timing_basis: "estimated" }, /measured/],
    ["stale policy", { ...actual(39_600), runtime_policy_hash: "old" }, /another runtime policy/],
    ["missing policy receipt", { ...actual(39_600), runtime_policy_hash: undefined }, /another runtime policy/],
  ]) {
    writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
    stderr = "";
    assert.equal(await run("assemble", ["--slug", doc.slug], ctx), EXIT.lint, name);
    assert.match(stderr, expected, name);
    assert.equal(ffmpegReached, 0);
    assert.ok(!existsSync(path.join(box.workdir, "segments")));
    assert.ok(!existsSync(path.join(box.workdir, "final.mp4")));
  }
  for (const frames of [37_800, 41_400]) {
    const timeline = actual(frames);
    assert.equal(timeline.runtime_policy_hash, runtimePolicyHash(doc));
    writeAudioFixture(timeline, box.workdir);
    stderr = "";
    assert.equal(await run("assemble", ["--slug", doc.slug], ctx), EXIT.usage);
    assert.match(stderr, /run render first/, "valid boundary body advances to the existing media gate");
  }
  assert.equal(ffmpegReached, 0);
});

test("native auto-fit probes every directed clip and refuses a short action before encoding any segment", async (t) => {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  Object.assign(doc, { category: "anime", production_policy: "long-anime-v1", target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "fantasy", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false } });
  doc.look.preset = "anime-2d";
  delete doc.music;
  doc.subtitles = { burn_in: false };
  for (const scene of doc.scenes) delete scene.data.fit;
  doc.scenes.push({ id: "bridge-action", template: "shot", action_seconds: 8, data: { prompt: "The girl leaps between collapsing bridge stones", motion: "stones crack and fall into the river", characters: ["jingwei"] }, lines: [] });
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ ...doc.series, category: doc.category, production_policy: doc.production_policy, runtime_spec: doc.runtime_spec, target_minutes: 22, style_preset: "anime-2d", characters: doc.characters }));
  assert.deepEqual(lintProject(loadProject({ slug: doc.slug, root: box.root })).errors, []);
  // These frame counts and probe binaries are synthetic. No real 22-minute media is produced.
  const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const last = [...eachLine(doc)].at(-1).line.id;
  samples[last] += (39_600 - buildTimeline(doc, samples).total_frames) * SAMPLES_PER_FRAME;
  const timeline = { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, fixtureLexicon()) };
  const visual = visualHash(doc);
  mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
  mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
  writeAudioFixture(timeline, box.workdir);
  writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visual, ...manifestFor(timeline, 0) }));
  const shots = Object.fromEntries(timeline.scenes.map((scene) => {
    const file = `clips/${scene.id}.mp4`;
    writeFileSync(path.join(box.workdir, file), JSON.stringify({ frames: scene.id === "bridge-action" ? 180 : scene.end_frame - scene.start_frame }));
    return [scene.id, { file, sha256: "a".repeat(64) }];
  }));
  writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ speech_hash: timeline.speech_hash, visual_hash: visual, look_hash: lookHash(doc), shots }));
  const bin = path.join(box.base, "bin");
  const marker = path.join(box.base, "encoding-started");
  mkdirSync(bin);
  writeFileSync(path.join(bin, "ffmpeg"), '#!/usr/bin/env node\nimport { writeFileSync } from "node:fs";\nimport path from "node:path";\nconst args=process.argv.slice(2);\nif(args.includes("-encoders")) process.stdout.write(" libx264 "); else if(args.includes("-version")) process.stdout.write("ffmpeg synthetic test\\n"); else { writeFileSync(path.join(path.dirname(process.argv[1]),"..","encoding-started"),"unexpected encode"); process.exit(9); }\n', { mode: 0o755 });
  writeFileSync(path.join(bin, "ffprobe"), '#!/usr/bin/env node\nimport { readFileSync } from "node:fs";\nconst frames=JSON.parse(readFileSync(process.argv.at(-1),"utf8")).frames;\nprocess.stdout.write(JSON.stringify({streams:[{codec_type:"video",r_frame_rate:"30/1",nb_read_packets:String(frames)}]}));\n', { mode: 0o755 });
  let stderr = "";
  const ctx = { root: box.root, home: box.base, EXIT, env: { VIDEO_WORKDIR: box.work, FFMPEG_PATH: bin }, stdout: { write() {} }, stderr: { write(value) { stderr += value; } } };
  assert.equal(await run("assemble", ["--slug", doc.slug], ctx), EXIT.lint, stderr);
  assert.match(stderr, /bridge-action must cover its 240 frames at natural speed with no frozen tail/);
  assert.equal(existsSync(marker), false, "no clip, motion, subtitle or final encoding starts");
  assert.equal(existsSync(path.join(box.workdir, "segments")), false, "even earlier valid shots are not encoded before the last shot is checked");
});

test("direct assembly refuses wrong-model, short or non-native-1080p production clips before reaching ffmpeg", async () => {
  const expected = { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p", aspect: "16:9" };
  for (const fault of ["model", "duration", "dimensions", "missing dimensions"]) {
    const box = sandbox("fixture-drama", "drama");
    const doc = dramaFixture();
    delete doc.music;
    delete doc.sfx;
    doc.subtitles = { burn_in: false };
    for (const scene of doc.scenes) {
      delete scene.data.fit;
      for (const line of scene.lines) {
        line.text = "走。";
        delete line.say;
        delete line.say_for;
      }
    }
    writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
    const seriesFile = path.join(box.dir, "series.json");
    writeFileSync(seriesFile, JSON.stringify({ production: { profile: { video: expected } } }));
    const speech = speechHash(doc, fixtureLexicon());
    const visual = visualHash(doc);
    const timeline = { ...estimateTimeline(doc), speech_hash: speech };
    mkdirSync(box.workdir, { recursive: true });
    writeAudioFixture(timeline, box.workdir);
    mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
    writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visual }));
    const clips = {
      speech_hash: speech, visual_hash: visual, look_hash: lookHash(doc), clip: { ...expected },
      shots: Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `clips/${scene.id}.mp4`, sha256: "a".repeat(64), qc: { ok: true, metrics: { duration: 8, width: 1920, height: 1080 } } }])),
    };
    if (fault === "model") clips.clip.model = "gemini-omni-1.1-flash";
    else if (fault === "duration") clips.shots[doc.scenes[0].id].qc.metrics.duration = 0.1;
    else if (fault === "dimensions") Object.assign(clips.shots[doc.scenes[0].id].qc.metrics, { width: 1280, height: 720 });
    else delete clips.shots[doc.scenes[0].id].qc.metrics.width;
    mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
    writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify(clips));
    let ffmpegReached = 0;
    let stderr = "";
    const ctx = {
      root: box.root, home: box.base, EXIT,
      env: { VIDEO_WORKDIR: box.work, get FFMPEG_PATH() { ffmpegReached += 1; throw new Error("ffmpeg sentinel"); } },
      stdout: { write() {} }, stderr: { write(value) { stderr += value; } },
    };
    assert.equal(await run("assemble", ["--slug", doc.slug], ctx), EXIT.usage, stderr);
    assert.match(stderr, /production clips need review before assembly/);
    assert.match(stderr, fault === "model" ? /approved production model/ : fault === "duration" ? /whole dialogue/ : /native 1920x1080/);
    assert.equal(ffmpegReached, 0, "neither ffmpeg discovery nor any encoding is started");
    assert.ok(!existsSync(path.join(box.workdir, "segments")));
    // The same older manifest remains valid for the legacy assembly path; stop
    // at tool discovery so this control never runs a native command either.
    writeFileSync(seriesFile, JSON.stringify({}));
    await assert.rejects(run("assemble", ["--slug", doc.slug], ctx), /ffmpeg sentinel/);
    assert.equal(ffmpegReached, 1);
  }
});

test("direct assembly refuses missing or changed audio evidence before any ffmpeg work", async () => {
  for (const fault of ["legacy", "take", "narration"]) {
    const box = sandbox("fixture-drama", "drama");
    const doc = dramaFixture();
    const timeline = writeAudioFixture({ ...estimateTimeline(doc), speech_hash: speechHash(doc, fixtureLexicon()) }, box.workdir);
    if (fault === "legacy") {
      delete timeline.audio_evidence;
      writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
    } else {
      const file = path.join(box.workdir, fault === "take" ? `audio/${timeline.lines[0].id}.wav` : "narration.wav");
      const bytes = readFileSync(file); bytes[48] ^= 1; writeFileSync(file, bytes);
    }
    let ffmpegReached = 0, stderr = "";
    const ctx = { root: box.root, home: box.base, EXIT, env: { VIDEO_WORKDIR: box.work, get FFMPEG_PATH() { ffmpegReached += 1; throw new Error("ffmpeg sentinel"); } }, stdout: { write() {} }, stderr: { write(value) { stderr += value; } } };
    assert.equal(await run("assemble", ["--slug", box.slug], ctx), EXIT.usage);
    assert.match(stderr, /current audio evidence before assembly/);
    assert.equal(ffmpegReached, 0);
  }
});

test("each scene lays out transition frames one by one, then its still, adding up to the scene's frames", () => {
  const timeline = estimateTimeline(fixture());
  const layout = layoutScenes(timeline, manifestFor(timeline));
  for (const [index, scene] of layout.entries()) {
    // assemble samples only "stills" scenes by PSNR; a plain slides video must not lose its frame checks.
    assert.equal(scene.kind, "stills");
    assert.ok(segmentSamples(scene).length > 0);
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

test("a dense slide near 40 dB passes when it looks most like its own image, and fails when a rival is as close", () => {
  const scene = { entries: [{ file: "t0", frames: 1 }, { file: "first", frames: 40 }, { file: "t1", frames: 1 }, { file: "second", frames: 60 }] };
  assert.deepEqual(rivalImages(scene, "second"), ["first"]);
  const sample = { scene: "myth-compare", n: 101, file: "second" };
  // Numbers from the pilot on 2026-09-25: the right frame of a two-card comparison scored 39.97 dB.
  assert.equal(sampleProblem(sample, 47.2), null);
  assert.equal(sampleProblem(sample, 39.97, { first: 27.4 }), null);
  assert.match(sampleProblem(sample, 39.97, { first: 38.1 }), /looks as much like first/);
  assert.match(sampleProblem(sample, 33.5), /does not show second/);
  assert.equal(sampleProblem({ ...sample, file: "only" }, 42.9, {}), null, "a scene with one image has no rival");
});

test("the probe check wants exactly the timeline's frames and YouTube's recommended streams", () => {
  const good = {
    streams: [
      { codec_type: "video", codec_name: "h264", profile: "High", width: 1920, height: 1080, r_frame_rate: "30/1", pix_fmt: "yuv420p", color_space: "bt709", color_primaries: "bt709", color_transfer: "bt709", nb_read_packets: "1247" },
      { codec_type: "audio", codec_name: "aac", sample_rate: "48000", channels: 2, duration: "41.566667" },
    ],
  };
  assert.deepEqual(checkProbe(good, { frames: 1247 }), []);
  // AAC pads to whole 1,024-sample frames: the pilot's 17,995 frames came back 0.067 s longer.
  const padded = structuredClone(good);
  padded.streams[1].duration = String(1247 / 30 + 0.067);
  assert.deepEqual(checkProbe(padded, { frames: 1247 }), []);
  const short = structuredClone(good);
  short.streams[1].duration = String(1247 / 30 - 0.05);
  assert.match(checkProbe(short, { frames: 1247 })[0], /audio lasts/);
  const bad = structuredClone(good);
  bad.streams[0].color_primaries = "unknown";
  bad.streams[0].nb_read_packets = "1246";
  bad.streams[1].channels = 1;
  bad.streams[1].duration = "43.0";
  assert.equal(checkProbe(bad, { frames: 1247 }).length, 4);
});
