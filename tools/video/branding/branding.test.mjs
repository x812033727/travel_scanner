import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sha256File } from "../core/approvals.mjs";
import { currentBrandingFile, readCurrentBranding } from "../core/branding.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { installPackage, packageSelection, run } from "./cli.mjs";

async function sourcePackage(box, introFrames = 150) {
  const directory = path.join(box.base, `selected-${introFrames}`);
  mkdirSync(directory);
  const assets = [];
  for (const [role, frames] of [["intro", introFrames], ["outro", 90]]) {
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

test("series installation and history stay isolated; tampering preserves both defaults", async () => {
  const box = sandbox();
  await installPackage({ directory: await sourcePackage(box), workBase: box.work, tools, exec });
  const globalFile = path.join(box.work, currentBrandingFile());
  const before = readFileSync(globalFile, "utf8");
  const directory = await sourcePackage(box, 357);
  const seriesExec = async (tool, args) => {
    const result = await exec(tool, args);
    const probe = JSON.parse(result.stdout);
    if (path.basename(args.at(-1)) === "intro.mp4") { probe.streams[0].nb_read_packets = "357"; probe.streams[1].duration = "11.9"; }
    return { ...result, stdout: JSON.stringify(probe) };
  };
  const options = { directory, workBase: box.work, series: "sothatswhy", tools, exec: seriesExec };
  await installPackage({ ...options, dryRun: true });
  assert.equal(readCurrentBranding(box.work, { series: "sothatswhy" }), null);
  await installPackage(options);
  const selected = readCurrentBranding(box.work, { series: "sothatswhy" });
  assert.equal(selected.intro.frames, 357);
  assert.equal(readFileSync(selected.intro.file, "utf8"), "intro");
  assert.equal(readFileSync(globalFile, "utf8"), before);
  await installPackage(options);
  assert.equal(existsSync(path.join(box.work, "_branding", "series", "sothatswhy", "history")), true);
  assert.equal(existsSync(path.join(box.work, "_branding", "history")), false);
  const seriesFile = path.join(box.work, currentBrandingFile("sothatswhy"));
  const seriesBefore = readFileSync(seriesFile, "utf8");
  writeFileSync(path.join(directory, "intro.mp4"), "tampered");
  await assert.rejects(installPackage(options), /SHA-256 changed/);
  assert.equal(readFileSync(seriesFile, "utf8"), seriesBefore);
  assert.equal(readFileSync(globalFile, "utf8"), before);
  const output = [];
  await run("branding", ["--series", "sothatswhy", "--json"], { env: { VIDEO_WORKDIR: box.work }, root: box.root, home: box.base, stdout: { write: value => output.push(value) }, EXIT: { ok: 0 } });
  assert.equal(JSON.parse(output.join("")).selection.intro.frames, 357);
});

test("unknown or escaping series identifiers are rejected before probing or creating files", async () => {
  const box = sandbox();
  for (const series of ["unknown", "../sothatswhy", "/sothatswhy", "sothatswhy/other", "sothatswhy\\other", ""]) {
    await assert.rejects(installPackage({ directory: "missing", workBase: box.work, series, tools, exec: () => { throw new Error("probe reached"); } }), /only sothatswhy/);
    await assert.rejects(run("branding", ["--series", series], {}), /only sothatswhy/);
  }
  assert.equal(existsSync(path.join(box.work, "_branding")), false);
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
