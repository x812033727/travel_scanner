// ff2manifest.mjs and clips2manifest.mjs: gen-dh.mjs's lists become the manifests the
// minimax-h3-colab skill runs, with the work-dir naming assemble-v4.mjs reads back.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FF2 = path.join(HERE, "ff2manifest.mjs");
const CLIPS2 = path.join(HERE, "clips2manifest.mjs");
const { pickRefs, rewritePrompt, describeRef } = await import(FF2);
const { latestFrame, nextClipTake } = await import(CLIPS2);

const HAILUO_PROMPT = "At the county yamen gate at dawn, stone steps: medium shot of Xu Yan and A-ling, 16:9 frame. Style: 3D Chinese donghua. Camera: locked. Characters: Xu Yan: tall; A-ling: cold beauty. Reference images: Xu Yan and A-ling must be the same characters as in their reference portraits (same faces); the location matches the set reference picture. Not a photograph, not live action. No text, no letters, no watermark, no UI.";

function workdir() {
  const root = mkdtempSync(path.join(tmpdir(), "zt-colab-"));
  const refs = path.join(root, "_series", "zhong-tian-qu-qi", "refs-dh");
  mkdirSync(refs, { recursive: true });
  for (const name of ["xuyan-portrait-t1.png", "aling-portrait-t1.png", "tangxiaotang-portrait-t2.png", "set-xianya-t1.png"]) writeFileSync(path.join(refs, name), "png");
  const work = path.join(root, "zhong-tian-qu-qi-e031-dh");
  mkdirSync(path.join(work, "first-frames"), { recursive: true });
  mkdirSync(path.join(work, "clips"));
  return { root, refs, work, env: { ...process.env, VIDEO_WORKDIR: root } };
}

const run = (script, args, env) => spawnSync("node", [script, ...args], { env, encoding: "utf8" });

test("ff2manifest: three pictures at most, the set always kept, and the prompt names each image", () => {
  assert.deepEqual(describeRef("dh-set-xianya-t1.png"), { file: "set-xianya-t1.png", kind: "set", id: "xianya" });
  assert.deepEqual(describeRef("dh-tangxiaotang-portrait-t2.png"), { file: "tangxiaotang-portrait-t2.png", kind: "portrait", id: "tangxiaotang" });
  const { kept, dropped } = pickRefs(["dh-xuyan-portrait-t1.png", "dh-aling-portrait-t1.png", "dh-tangxiaotang-portrait-t2.png", "dh-set-xianya-t1.png"]);
  assert.deepEqual(kept.map((r) => r.file), ["xuyan-portrait-t1.png", "aling-portrait-t1.png", "set-xianya-t1.png"]);
  assert.deepEqual(dropped.map((r) => r.id), ["tangxiaotang"]);
  const prompt = rewritePrompt(HAILUO_PROMPT, kept);
  assert.ok(!prompt.includes("must be the same characters as in their reference portraits"), "Hailuo's sentence is gone");
  assert.match(prompt, /Reference images: image 1 is the character sheet of Xu Yan: keep his face, hair, costume and the same 3D donghua art style exactly; image 2 is the character sheet of A-ling: keep her face[^.]*; image 3 is the location: keep its layout[^.]*\. Not a photograph, not live action\./);
  assert.ok(prompt.startsWith("At the county yamen gate at dawn"));
});

test("ff2manifest CLI: writes part manifests with absolute pictures, prompt files and the next take; a missing picture stops it with 1", () => {
  const { refs, work, env } = workdir();
  const ff = [
    { id: "s01", kind: "clip", refs: ["dh-xuyan-portrait-t1.png", "dh-set-xianya-t1.png"], want: "1 22 創建", prompt: HAILUO_PROMPT },
    { id: "s02", kind: "clip", refs: ["dh-aling-portrait-t1.png"], want: "1 21 創建", prompt: HAILUO_PROMPT },
    { id: "s03", kind: "clip", refs: ["dh-xuyan-portrait-t1.png", "dh-aling-portrait-t1.png", "dh-tangxiaotang-portrait-t2.png", "dh-set-xianya-t1.png"], want: "1 24 創建", prompt: HAILUO_PROMPT },
  ];
  const list = path.join(work, "ff-dh-e031.json");
  writeFileSync(list, JSON.stringify(ff));
  writeFileSync(path.join(work, "first-frames", "s02-t1.png"), "old take");
  const out = path.join(work, "colab");
  const result = run(FF2, [list, "31", out, "--chunk", "2"], env);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /s03: dropped tangxiaotang-portrait-t2\.png/);
  assert.match(result.stdout, /3 first-frame jobs -> 2 manifest\(s\)/);
  const part1 = JSON.parse(readFileSync(path.join(out, "ff-e031-part1.json"), "utf8"));
  const part2 = JSON.parse(readFileSync(path.join(out, "ff-e031-part2.json"), "utf8"));
  assert.deepEqual(part1.jobs.map((j) => j.id), ["s01", "s02"]);
  assert.deepEqual(part2.jobs.map((j) => j.id), ["s03"]);
  assert.deepEqual(part1.jobs[0].reference_images, [path.join(refs, "xuyan-portrait-t1.png"), path.join(refs, "set-xianya-t1.png")]);
  assert.deepEqual([part1.jobs[0].width, part1.jobs[0].height, part1.jobs[0].output_name], [1312, 736, "s01-t1.png"]);
  assert.equal(part1.jobs[1].output_name, "s02-t2.png", "s02 already has a take, so this is t2");
  assert.ok(readFileSync(path.join(out, part1.jobs[0].prompt_file), "utf8").includes("image 2 is the location"));
  // --only and --take; a reference the fetch never saved is named and exits 1 after writing.
  const only = run(FF2, [list, "31", out, "--only", "s01", "--take", "5"], env);
  assert.equal(only.status, 0, only.stderr);
  assert.equal(JSON.parse(readFileSync(path.join(out, "ff-e031-part1.json"), "utf8")).jobs[0].output_name, "s01-t5.png");
  writeFileSync(list, JSON.stringify([{ id: "s09", kind: "clip", refs: ["dh-laisan-portrait-t1.png"], want: "1 21 創建", prompt: HAILUO_PROMPT }]));
  const missing = run(FF2, [list, "31", out], env);
  assert.equal(missing.status, 1);
  assert.match(missing.stderr, /1 reference picture\(s\) missing[\s\S]*laisan-portrait-t1\.png/);
});

test("clips2manifest: latest first frame, byte-exact prompt with its full hash, 20 per part, and a shot without a frame stops it", () => {
  const { work, env } = workdir();
  const frames = path.join(work, "first-frames");
  for (const name of ["s01-t1.png", "s01-t2.png", "s02-t1.png", "s03-t1.png"]) writeFileSync(path.join(frames, name), "png");
  writeFileSync(path.join(work, "clips", "s02-t1.mp4"), "mp4");
  assert.equal(latestFrame(frames, "s01"), path.join(frames, "s01-t2.png"));
  assert.equal(latestFrame(frames, "s01", 1), path.join(frames, "s01-t1.png"));
  assert.equal(latestFrame(frames, "s07"), null);
  assert.equal(nextClipTake(path.join(work, "clips"), "s02"), 2);
  assert.equal(nextClipTake(path.join(work, "clips"), "s01"), 1);
  const text = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] 3D CG. Xu Yan shown in <Picture 1> keeps the same face. The camera holds a static shot. One continuous shot.\noverall_soundscape: N/A\nnon_diegetic_music: N/A";
  const clips = { "a31-s01": [text, "abcd", 5], "a31-s02": [text, "abcd", 6], "a31-s03": [text, "abcd", 6], "a31-s04": [text, "abcd", 5], "a30-s01": [text, "abcd", 5] };
  const list = path.join(work, "clips-dh-e031.json");
  writeFileSync(list, JSON.stringify(clips));
  const out = path.join(work, "colab");
  const stopped = run(CLIPS2, [list, "31", out, "--chunk", "2"], env);
  assert.equal(stopped.status, 1);
  assert.match(stopped.stderr, /1 shot\(s\) have no first frame[^\n]*: s04/);
  const result = run(CLIPS2, [list, "31", out, "--chunk", "2", "--skip-missing"], env);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /3 clip jobs \(1 × 5 s, 2 × 6 s\) -> 2 manifest\(s\)/);
  const part1 = JSON.parse(readFileSync(path.join(out, "clips-e031-part1.json"), "utf8"));
  assert.deepEqual(part1.jobs.map((j) => j.id), ["s01", "s02"]);
  assert.ok(existsSync(path.join(out, "clips-e031-part2.json")));
  const s01 = part1.jobs[0];
  assert.deepEqual([s01.inference_mode, s01.reference_images, s01.duration_seconds, s01.width, s01.height, s01.output_name], ["first_frame", [path.join(frames, "s01-t2.png")], 5, 1312, 736, "s01-t1.mp4"]);
  assert.equal(part1.jobs[1].output_name, "s02-t2.mp4", "s02 already has a clip, so this is t2");
  assert.equal(readFileSync(path.join(out, s01.prompt_file), "utf8"), text);
  assert.equal(s01.prompt_sha256, createHash("sha256").update(text).digest("hex"));
  assert.ok(!JSON.stringify(part1).includes("a30-"), "another episode's shots are ignored");
});
