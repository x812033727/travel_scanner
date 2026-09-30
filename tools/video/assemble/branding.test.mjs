import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { brandingHash } from "../core/branding.mjs";
import { brandingJoinArgs, brandingSegmentArgs, commitBrandedVideo, verifyBrandingAssets } from "./branding.mjs";

const selected = { schema_version: 1, id: "mokaair", intro: { file: "intro.mp4", sha256: "a".repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } };

test("the wrapper copies normalized pictures but trims decoded audio to exact samples at both seams", () => {
  const args = brandingJoinArgs({ bodyFile: "body.mp4", bodyFrames: 301, branding: selected, outFile: "final.mp4", videoList: "join.ffconcat" });
  const filter = args[args.indexOf("-filter_complex") + 1];
  for (const count of [240000, 481600, 144000]) assert.match(filter, new RegExp(`atrim=end_sample=${count},apad=whole_len=${count},atrim=end_sample=${count}`));
  assert.match(filter, /^\[1:a:0\]aresample=48000/);
  assert.match(filter, /asetpts=PTS-STARTPTS/);
  assert.match(args.join(" "), /-map 0:v:0 -c:v copy/);
  assert.match(args.join(" "), /-c:a aac -b:a 384k -ar 48000 -ac 2/);
  assert.doesNotMatch(filter, /loudnorm/, "the selected audio stays at its approved volume");
});

test("dub wrappers support WAV and MP3 without extra input numbering or MP4-only flags", () => {
  const args = brandingJoinArgs({ bodyFile: "body.wav", bodyFrames: 30, branding: selected, outFile: "dub.wav", outputCodec: ["-c:a", "pcm_s16le"] });
  assert.match(args[args.indexOf("-filter_complex") + 1], /^\[0:a:0\]/);
  assert.ok(args.includes("pcm_s16le") && args.includes("-vn"));
  assert.ok(!args.includes("-movflags"));
  const picture = brandingSegmentArgs("intro.mp4", "normalized.mp4", 150).join(" ");
  assert.match(picture, /-i intro.mp4/);
  assert.match(picture, /-frames:v 150/);
  assert.match(picture, /-profile:v high/);
  assert.match(picture, /colorprim=bt709/);
});

test("installed assets must match their pinned bytes, frame count and audio presence", async (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "branding-assets-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const bytes = Buffer.from("fixture media");
  const sha256 = createHash("sha256").update(bytes).digest("hex");
  const branding = { ...selected };
  for (const role of ["intro", "outro"]) {
    const file = path.join(directory, `${role}.mp4`);
    writeFileSync(file, bytes);
    branding[role] = { ...selected[role], file, sha256 };
  }
  let wrongFrames = false;
  let audio = true;
  const exec = async (_tool, args) => {
    const frames = args.at(-1).endsWith("intro.mp4") ? 150 : 90;
    return { stdout: JSON.stringify({ streams: [{ codec_type: "video", width: 1920, height: 1080, r_frame_rate: "30/1", nb_read_packets: wrongFrames ? 1 : frames }, ...(audio ? [{ codec_type: "audio", duration: frames / 30 }] : [])] }) };
  };
  const tools = { ffprobe: "fake" };
  assert.equal((await verifyBrandingAssets(branding, { tools, exec })).id, "mokaair");
  wrongFrames = true;
  await assert.rejects(verifyBrandingAssets(branding, { tools, exec }), /exactly 150 frames/);
  wrongFrames = false;
  audio = false;
  await assert.rejects(verifyBrandingAssets(branding, { tools, exec }), /sound track/);
  writeFileSync(branding.intro.file, "different bytes");
  await assert.rejects(verifyBrandingAssets(branding, { tools, exec }), /SHA-256 changed/);
});

test("failed media QA and interrupted promotion preserve the complete previous cut and records", (t) => {
  const workdir = mkdtempSync(path.join(os.tmpdir(), "branding-commit-"));
  t.after(() => rmSync(workdir, { recursive: true, force: true }));
  mkdirSync(path.join(workdir, "build"));
  const old = { "final.mp4": "old final", "build/body.mp4": "old body", "branding.json": "old pin", "checks.json": "old checks" };
  for (const [file, value] of Object.entries(old)) writeFileSync(path.join(workdir, file), value);
  const finalPartial = path.join(workdir, "build", "final.partial.mp4");
  const bodyPartial = path.join(workdir, "build", "body.partial.mp4");
  writeFileSync(finalPartial, "new final");
  writeFileSync(bodyPartial, "new body");
  const checks = { ok: true, branding: { hash: brandingHash(selected), body_file: "build/body.mp4" } };
  const options = { workdir, branding: selected, finalPartial, bodyPartial, checks };
  assert.throws(() => commitBrandedVideo({ ...options, checks: { ...checks, ok: false } }), /failed branded cut/);
  const assertOld = () => { for (const [file, value] of Object.entries(old)) assert.equal(readFileSync(path.join(workdir, file), "utf8"), value, file); };
  assertOld();
  const rename = (from, to) => {
    if (to === path.join(workdir, "checks.json")) throw new Error("injected filesystem failure");
    renameSync(from, to);
  };
  assert.throws(() => commitBrandedVideo({ ...options, rename }), /injected filesystem failure/);
  assertOld();
  assert.equal(readFileSync(finalPartial, "utf8"), "new final", "the partial is available for diagnosis or retry");
  commitBrandedVideo(options);
  assert.equal(readFileSync(path.join(workdir, "final.mp4"), "utf8"), "new final");
  assert.equal(readFileSync(path.join(workdir, "build", "body.mp4"), "utf8"), "new body");
  assert.equal(JSON.parse(readFileSync(path.join(workdir, "checks.json"), "utf8")).branding.hash, brandingHash(selected));
});

test("compilation captions and timeline commit with the video, including whole-directory rollback", (t) => {
  const workdir = mkdtempSync(path.join(os.tmpdir(), "branding-artifacts-"));
  t.after(() => rmSync(workdir, { recursive: true, force: true }));
  for (const directory of ["build", "captions", "staging/captions"]) mkdirSync(path.join(workdir, directory), { recursive: true });
  for (const [file, text] of Object.entries({ "final.mp4": "old final", "captions/old.srt": "old captions", "timeline.json": "old timeline", "staging/captions/new.srt": "new captions", "staging/timeline.json": "new timeline", "build/final.partial.mp4": "new final" })) writeFileSync(path.join(workdir, file), text);
  const artifacts = [{ source: "staging/captions", target: "captions" }, { source: "staging/timeline.json", target: "timeline.json" }];
  const options = { workdir, branding: selected, finalPartial: path.join(workdir, "build", "final.partial.mp4"), checks: { ok: true, branding: { hash: brandingHash(selected), body_file: "build/body.mp4" } }, artifacts };
  const rename = (from, to) => {
    if (to === path.join(workdir, "checks.json")) throw new Error("failed after derived artifacts moved");
    renameSync(from, to);
  };
  assert.throws(() => commitBrandedVideo({ ...options, rename }), /derived artifacts/);
  assert.equal(readFileSync(path.join(workdir, "final.mp4"), "utf8"), "old final");
  assert.equal(readFileSync(path.join(workdir, "captions", "old.srt"), "utf8"), "old captions");
  assert.equal(readFileSync(path.join(workdir, "timeline.json"), "utf8"), "old timeline");
  assert.equal(readFileSync(path.join(workdir, "staging", "captions", "new.srt"), "utf8"), "new captions");
  commitBrandedVideo(options);
  assert.equal(readFileSync(path.join(workdir, "captions", "new.srt"), "utf8"), "new captions");
  assert.equal(readFileSync(path.join(workdir, "timeline.json"), "utf8"), "new timeline");
  assert.throws(() => readFileSync(path.join(workdir, "captions", "old.srt")), /ENOENT/, "replacing a directory also removes previously exported, now absent caption locales");
});

test("derived artifact destinations cannot escape the video or overlap the core commit files", (t) => {
  const workdir = mkdtempSync(path.join(os.tmpdir(), "branding-artifact-paths-"));
  t.after(() => rmSync(workdir, { recursive: true, force: true }));
  const options = { workdir, branding: selected, finalPartial: path.join(workdir, "new.mp4"), checks: { ok: true, branding: { hash: brandingHash(selected), body_file: "build/body.mp4" } } };
  for (const target of ["..", "../outside.json", ".", "checks.json", "build", "final.mp4"]) assert.throws(() => commitBrandedVideo({ ...options, artifacts: [{ source: "staging/data", target }] }), /inside|overlap/, target);
  assert.throws(() => commitBrandedVideo({ ...options, artifacts: [{ source: "staging/one", target: "captions" }, { source: "staging/two", target: "captions/en.srt" }] }), /overlap/);
});
