// The Whisper second opinion reads the tool's clips itself (PyAV 19 broke faster-whisper's
// decoder on 2026-10-10) and prints UTF-8 whatever the console's code page. These run the
// script's standard-library half; faster-whisper itself is not needed.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const python = ["python3", "python"].find((name) => spawnSync(name, ["--version"]).status === 0);

function pcmWav(samples, rate, channels = 1) {
  const data = Buffer.alloc(samples.length * 2);
  samples.forEach((value, index) => data.writeInt16LE(value, index * 2));
  const header = Buffer.alloc(44);
  header.write("RIFF", 0); header.writeUInt32LE(36 + data.length, 4); header.write("WAVE", 8);
  header.write("fmt ", 12); header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20); header.writeUInt16LE(channels, 22);
  header.writeUInt32LE(rate, 24); header.writeUInt32LE(rate * channels * 2, 28); header.writeUInt16LE(channels * 2, 32); header.writeUInt16LE(16, 34);
  header.write("data", 36); header.writeUInt32LE(data.length, 40);
  return Buffer.concat([header, data]);
}

function run(code, env = {}) {
  const result = spawnSync(python, ["-I", "-c", `import sys; sys.path.insert(0, ${JSON.stringify(here)}); import whisper_second_opinion as w\n${code}`], { env: { ...process.env, ...env }, encoding: "buffer" });
  assert.equal(result.status, 0, result.stderr.toString());
  return result.stdout;
}

test("a 48 kHz clip is read without PyAV and resampled to Whisper's 16 kHz", { skip: !python && "no python" }, () => {
  const dir = mkdtempSync(path.join(tmpdir(), "whisper-"));
  const file = path.join(dir, "9ey5.wav");
  const samples = Array.from({ length: 4800 }, (_, index) => Math.round(16384 * Math.sin(index / 10)));
  writeFileSync(file, pcmWav(samples, 48_000));
  const out = JSON.parse(run(`s, r = w.read_wav(${JSON.stringify(file)}); x = w.resample(s, r); print(__import__("json").dumps([r, len(s), len(x), round(max(x), 2)]))`).toString());
  assert.deepEqual(out, [48_000, 4800, 1600, 0.5]);
});

test("a stereo clip is averaged to one channel; a clip that is not 16-bit PCM is refused", { skip: !python && "no python" }, () => {
  const dir = mkdtempSync(path.join(tmpdir(), "whisper-"));
  const stereo = path.join(dir, "st.wav");
  writeFileSync(stereo, pcmWav([1000, 3000, -2000, 0], 16_000, 2));
  assert.equal(run(`s, r = w.read_wav(${JSON.stringify(stereo)}); print([round(v * 32768) for v in s], r)`).toString().trim(), "[2000, -1000] 16000");
  const odd = path.join(dir, "odd.wav");
  const bytes = pcmWav([0, 0], 16_000);
  bytes.writeUInt16LE(8, 34);
  writeFileSync(odd, bytes);
  const result = spawnSync(python, ["-I", "-c", `import sys; sys.path.insert(0, ${JSON.stringify(here)}); import whisper_second_opinion as w; w.read_wav(${JSON.stringify(odd)})`]);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr.toString(), /16-bit PCM/);
});

test("transcripts are written as UTF-8 even when the console is cp1252", { skip: !python && "no python" }, () => {
  const out = run(`w.emit("kirn.wav", "pixiv·niconico 停止 ไม่ต้องล็อกอิน")`, { PYTHONIOENCODING: "cp1252" });
  assert.equal(out.toString("utf8"), "kirn.wav pixiv·niconico 停止 ไม่ต้องล็อกอิน\n");
});
