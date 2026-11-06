// A drama series' shared assets (refs-dh, refs, sfx) copied into its Drive backup folder.
import assert from "node:assert/strict";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { backupSeries, SUMS } from "./series-backup.mjs";

function box(t) {
  const dir = mkdtempSync(path.join(os.tmpdir(), "series-backup-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const source = path.join(dir, "_series", "zhong-tian-qu-qi");
  for (const [relative, text] of [["refs-dh/tangxiaotang-portrait-t2.png", "collar"], ["refs/court.png", "court"], ["sfx/rain-48k.wav", "rain"], [".DS_Store", "skip"]]) {
    mkdirSync(path.dirname(path.join(source, relative)), { recursive: true });
    writeFileSync(path.join(source, relative), text);
  }
  return { source, target: path.join(dir, "drive", "_series") };
}

test("a series' references and sound library reach the backup folder once, with SHA256SUMS", (t) => {
  const { source, target } = box(t);
  const first = backupSeries(source, target);
  assert.deepEqual([first.files, first.copied, first.unchanged], [3, 3, 0]);
  assert.equal(readFileSync(path.join(target, "refs-dh", "tangxiaotang-portrait-t2.png"), "utf8"), "collar");
  assert.ok(!existsSync(path.join(target, ".DS_Store")), "hidden files stay behind");
  const sums = readFileSync(path.join(target, SUMS), "utf8").trim().split("\n");
  assert.deepEqual(sums.map((line) => line.split("  ")[1]), ["refs/court.png", "refs-dh/tangxiaotang-portrait-t2.png", "sfx/rain-48k.wav"]);
  assert.match(sums[1], /^[0-9a-f]{64} {2}refs-dh\//);

  // Run again after one reference changed: only it is copied, and nothing at the target is deleted.
  writeFileSync(path.join(source, "refs", "court.png"), "court, redrawn");
  rmSync(path.join(source, "sfx", "rain-48k.wav"));
  const second = backupSeries(source, target);
  assert.deepEqual([second.files, second.copied, second.unchanged], [2, 1, 1]);
  assert.equal(readFileSync(path.join(target, "refs", "court.png"), "utf8"), "court, redrawn");
  assert.ok(existsSync(path.join(target, "sfx", "rain-48k.wav")), "a file the source dropped keeps its Drive copy");
});

test("a missing or empty source, or the target being the source, is refused", (t) => {
  const { source, target } = box(t);
  assert.throws(() => backupSeries(path.join(source, "nope"), target), /is not a folder/);
  assert.throws(() => backupSeries(source, source), /same folder/);
  const empty = path.join(path.dirname(source), "empty");
  mkdirSync(empty);
  assert.throws(() => backupSeries(empty, target), /holds no files/);
});
