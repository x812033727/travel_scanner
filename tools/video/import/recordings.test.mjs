import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";

import { fittedDirs, packRecordings, recordingDirs, unpackRecordings, wavFile, wavParts } from "./recordings.mjs";

const FMT = Buffer.from([1, 0, 1, 0, 0x80, 0xbb, 0, 0, 0, 0x77, 1, 0, 2, 0, 16, 0]); // PCM, mono, 48 kHz, 16-bit
const wav = (samples, fmt = FMT) => wavFile(fmt, Buffer.from(samples));

function box(t) {
  const dir = mkdtempSync(path.join(os.tmpdir(), "recordings-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const work = path.join(dir, "zhong-tian-qu-qi-e035-dh");
  mkdirSync(path.join(work, "audio"), { recursive: true });
  mkdirSync(path.join(work, "audio-en"), { recursive: true });
  mkdirSync(path.join(work, "clips"), { recursive: true });
  writeFileSync(path.join(work, "audio", "zq35a01.wav"), wav([1, 2, 3, 4]));
  writeFileSync(path.join(work, "audio", "zq35a02.wav"), wav([5, 6]));
  writeFileSync(path.join(work, "audio-en", "zq35a01.wav"), wav([7, 8, 9, 10]));
  writeFileSync(path.join(work, "audio-en", "zq35a01.json"), '{"text":"Ducks."}\n');
  writeFileSync(path.join(work, "audio-en", "notes.txt"), "not a recording");
  return { dir, work, out: path.join(dir, "packed") };
}

test("wavParts finds the format and the samples; wavFile writes them back", () => {
  const bytes = wav([1, 2, 3, 4]);
  const parts = wavParts(bytes);
  assert.deepEqual(parts.fmt, FMT);
  assert.deepEqual(bytes.subarray(parts.dataStart, parts.dataStart + parts.dataLength), Buffer.from([1, 2, 3, 4]));
  assert.equal(wavParts(Buffer.from("not a wav")).problem, "not a RIFF WAVE file");
});

test("recordingDirs: audio/ is zh-TW, audio-<locale>/ each dub, nothing else", (t) => {
  const { work } = box(t);
  assert.deepEqual(recordingDirs(work).map(({ locale, dir }) => [locale, path.basename(dir)]), [["zh-TW", "audio"], ["en", "audio-en"]]);
  assert.deepEqual(recordingDirs(path.join(work, "nope")), []);
});

test("pack writes one playable wav a locale and a manifest; unpack gives back every line and sidecar byte for byte", (t) => {
  const { dir, work, out } = box(t);
  const { files, problems } = packRecordings(work, out);
  assert.deepEqual(problems, []);
  assert.deepEqual(files.map((file) => [path.basename(file.file), file.role, file.content_type]), [
    ["manifest.json", "recordings_manifest", "application/json"],
    ["zh-TW.wav", "recording_zh-TW", "audio/wav"],
    ["en.wav", "recording_en", "audio/wav"],
  ]);
  const joined = readFileSync(path.join(out, "zh-TW.wav"));
  const parts = wavParts(joined);
  assert.deepEqual(joined.subarray(parts.dataStart, parts.dataStart + parts.dataLength), Buffer.from([1, 2, 3, 4, 5, 6]));

  const back = path.join(dir, "back");
  assert.equal(unpackRecordings(out, back), 4);
  for (const folder of ["audio", "audio-en"]) {
    const names = readdirSync(path.join(back, folder)).sort();
    assert.deepEqual(names, readdirSync(path.join(work, folder)).filter((name) => name !== "notes.txt").sort());
    for (const name of names) assert.deepEqual(readFileSync(path.join(back, folder, name)), readFileSync(path.join(work, folder, name)), `${folder}/${name}`);
  }
});

test("pack refuses a line in another format or a file that is not a wav, and writes nothing", (t) => {
  const { work, out } = box(t);
  writeFileSync(path.join(work, "audio", "zq35a03.wav"), wav([1, 2], Buffer.from([1, 0, 2, 0, 0x80, 0xbb, 0, 0, 0, 0xee, 2, 0, 4, 0, 16, 0])));
  writeFileSync(path.join(work, "audio-en", "zq35a09.wav"), "not a wav");
  const { files, problems } = packRecordings(work, out);
  assert.deepEqual(files, []);
  assert.deepEqual(problems, ["audio/zq35a03.wav: its format differs from the folder's other lines", "audio-en/zq35a09.wav: not a RIFF WAVE file"]);
  assert.throws(() => readdirSync(out), /ENOENT/);
});

test("pack with no recordings writes nothing; unpack refuses a wav that is not the manifest's", (t) => {
  const { dir, work, out } = box(t);
  assert.deepEqual(packRecordings(path.join(work, "clips"), out), { files: [], manifest: null, problems: [] });
  packRecordings(work, out);
  writeFileSync(path.join(out, "en.wav"), wav([0, 0, 0, 0]));
  assert.throws(() => unpackRecordings(out, path.join(dir, "back")), /en\.wav is not the one the manifest names/);
});

const STEREO = Buffer.from([1, 0, 2, 0, 0x80, 0xbb, 0, 0, 0, 0xee, 2, 0, 4, 0, 16, 0]);

function fitted(work) {
  for (const folder of ["segments/dub-en", "segments-v4/lines", "segments-v4/dub-en", "segments-v4/dub-ja"]) mkdirSync(path.join(work, folder), { recursive: true });
  writeFileSync(path.join(work, "segments", "dub-en", "old.wav"), wav([9, 9], STEREO));
  writeFileSync(path.join(work, "segments-v4", "lines", "_s01.wav"), wav([0, 0, 0, 0], STEREO));
  writeFileSync(path.join(work, "segments-v4", "lines", "zq35a01.wav"), wav([1, 1, 2, 2], STEREO));
  writeFileSync(path.join(work, "segments-v4", "dub-en", "zq35a01.raw.wav"), wav([3, 3, 4, 4], STEREO));
  writeFileSync(path.join(work, "segments-v4", "dub-en", "zq35a01.wav"), wav([3, 4, 3, 4], STEREO));
  writeFileSync(path.join(work, "segments-v4", "dub-en", "dialogue.wav"), wav([0, 0, 3, 4, 3, 4, 0, 0], STEREO));
  writeFileSync(path.join(work, "segments-v4", "dub-en", "fit.json"), '[{"id":"zq35a01","start":0.12,"tempo":1}]\n');
  writeFileSync(path.join(work, "segments-v4", "dub-ja", "fit.json"), "[]\n");
  writeFileSync(path.join(work, "segments-v4", "mix-graph.txt"), "not packed");
}

test("fittedDirs: the newest segments folder's lines/ and dub-<locale>/", (t) => {
  const { work } = box(t);
  fitted(work);
  assert.deepEqual(fittedDirs(work).map(({ key, folder }) => [key, folder]), [["fit-lines", "segments-v4/lines"], ["fit-en", "segments-v4/dub-en"], ["fit-ja", "segments-v4/dub-ja"]]);
  assert.deepEqual(fittedDirs(path.join(work, "clips")), []);
});

test("pack carries the fitted takes, dialogue.wav and fit.json too; unpack gives them back byte for byte", (t) => {
  const { dir, work, out } = box(t);
  fitted(work);
  const { files, manifest, problems } = packRecordings(work, out);
  assert.deepEqual(problems, []);
  assert.deepEqual(files.map((file) => [path.basename(file.file), file.role]), [
    ["manifest.json", "recordings_manifest"],
    ["zh-TW.wav", "recording_zh-TW"],
    ["en.wav", "recording_en"],
    ["fit-lines.wav", "recording_fit-lines"],
    ["fit-en.wav", "recording_fit-en"],
  ]);
  assert.equal(manifest.schema_version, 2);
  assert.equal(manifest.fitted["fit-en"].folder, "segments-v4/dub-en");
  assert.equal(manifest.fitted["fit-en"].texts["fit.json"], '[{"id":"zq35a01","start":0.12,"tempo":1}]\n');

  const back = path.join(dir, "back");
  assert.equal(unpackRecordings(out, back), 4 + 2 + 4);
  for (const folder of ["segments-v4/lines", "segments-v4/dub-en"]) {
    const names = readdirSync(path.join(back, folder)).sort();
    assert.deepEqual(names, readdirSync(path.join(work, folder)).sort());
    for (const name of names) assert.deepEqual(readFileSync(path.join(back, folder, name)), readFileSync(path.join(work, folder, name)), `${folder}/${name}`);
  }
});

test("unpack refuses a fitted folder outside segments*/", (t) => {
  const { dir, work, out } = box(t);
  fitted(work);
  packRecordings(work, out);
  const file = path.join(out, "manifest.json");
  const manifest = JSON.parse(readFileSync(file, "utf8"));
  manifest.fitted["fit-en"].folder = "../escape";
  writeFileSync(file, JSON.stringify(manifest));
  assert.throws(() => unpackRecordings(out, path.join(dir, "back")), /bad folder \.\.\/escape/);
});
