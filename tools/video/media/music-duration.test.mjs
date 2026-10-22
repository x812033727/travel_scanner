import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { decodedMusicSeconds, decodedProgressSeconds } from "./music.mjs";

test("decoded progress accepts CRLF and older ffmpeg timestamp fields only at completion", () => {
  assert.equal(decodedProgressSeconds("out_time_us=174001633\r\nprogress=end\r\n"), 174.001633);
  assert.equal(decodedProgressSeconds("out_time_ms=174001633\r\nprogress=end\r\n"), 174.001633);
  assert.equal(decodedProgressSeconds("out_time=00:02:54.001633\r\nprogress=end\r\n"), 174.001633);
  assert.equal(decodedProgressSeconds("out_time_us=174001633\nprogress=continue\n"), null);
});

test("generated music duration comes from a full audio decode, including a repeated cache read", async () => {
  const dir = mkdtempSync(path.join(tmpdir(), "music-duration-"));
  try {
    const file = path.join(dir, "short.mp3");
    const { ffmpeg } = await locateFfmpeg();
    await runTool(ffmpeg, ["-nostdin", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=220:duration=2", "-c:a", "libmp3lame", file]);
    const first = await decodedMusicSeconds(file);
    const reused = await decodedMusicSeconds(file);
    assert.ok(first >= 1.99 && first <= 2.05, `decoded ${first} s`);
    assert.equal(reused, first);

    const corrupt = path.join(dir, "corrupt.mp3");
    writeFileSync(corrupt, "ID3music is not decodable audio");
    await assert.rejects(decodedMusicSeconds(corrupt), /ffmpeg failed|could not measure/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
