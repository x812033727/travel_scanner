import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sha256File } from "../core/approvals.mjs";
import { readCurrentBranding } from "../core/branding.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { installPackage, packageSelection } from "./cli.mjs";

async function sourcePackage(box) {
  const directory = path.join(box.base, "selected");
  mkdirSync(directory);
  const assets = [];
  for (const [role, frames] of [["intro", 150], ["outro", 90]]) {
    const file = `${role}.mp4`;
    writeFileSync(path.join(directory, file), role);
    assets.push({ role, file, frames, sha256: (await sha256File(path.join(directory, file))).toUpperCase() });
  }
  writeFileSync(path.join(directory, "manifest.json"), JSON.stringify({ schema_version: 1, package_id: "selected-v1", assets }));
  return directory;
}

const tools = { ffprobe: "probe", ffmpeg: "encode" };
const exec = async (tool, args) => ({ stdout: JSON.stringify({ streams: [
  { codec_type: "video", width: 1920, height: 1080, r_frame_rate: "30/1", nb_read_packets: path.basename(args.at(-1)) === "intro.mp4" ? "150" : "90" },
  { codec_type: "audio", sample_rate: "48000", channels: 2, duration: path.basename(args.at(-1)) === "intro.mp4" ? "5" : "3" },
] }), stderr: "" });

test("install validates a package before writing and pins immutable copied assets", async () => {
  const box = sandbox();
  const directory = await sourcePackage(box);
  const options = { directory, workBase: box.work, tools, exec, now: new Date("2026-09-30T01:00:00Z") };
  const dry = await installPackage({ ...options, dryRun: true });
  assert.equal(dry.installed, false);
  assert.equal(existsSync(path.join(box.work, "_branding")), false);
  await installPackage(options);
  const selected = readCurrentBranding(box.work);
  assert.equal(selected.hash, dry.selection.hash);
  assert.notEqual(selected.intro.file, path.join(directory, "intro.mp4"));
  assert.equal(readFileSync(selected.intro.file, "utf8"), "intro");
  writeFileSync(path.join(directory, "intro.mp4"), "changed source");
  await assert.rejects(installPackage(options), /SHA-256 changed/);
  assert.equal(readCurrentBranding(box.work).hash, selected.hash, "failed validation leaves the current default intact");
  assert.equal(readFileSync(selected.intro.file, "utf8"), "intro", "source edits cannot alter an installed asset");
});

test("package paths cannot escape and falsely declared timing cannot become the default", async () => {
  const box = sandbox();
  const directory = await sourcePackage(box);
  const file = path.join(directory, "manifest.json");
  const manifest = JSON.parse(readFileSync(file, "utf8"));
  manifest.assets[0].frames = 149;
  writeFileSync(file, JSON.stringify(manifest));
  await assert.rejects(installPackage({ directory, workBase: box.work, tools, exec }), /exactly 149 frames/);
  assert.equal(readCurrentBranding(box.work), null);
  manifest.assets[0].file = "../outside.mp4";
  writeFileSync(file, JSON.stringify(manifest));
  assert.throws(() => packageSelection(directory), /inside the package/);
});
