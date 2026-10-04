import assert from "node:assert/strict";
import { existsSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { tempDir } from "./fixtures/load.mjs";
import { atomicWrite } from "./paths.mjs";

const OLD = '{"version":"old"}';
const NEXT = '{"version":"new","complete":true}';
function target() {
  const file = path.join(tempDir("video-atomic-"), "state.json");
  writeFileSync(file, OLD);
  return file;
}
const failure = (code) => Object.assign(new Error(`synthetic ${code}`), { code });

for (const code of ["EPERM", "EACCES", "EBUSY"]) {
  test(`atomicWrite survives a temporary Windows ${code} without exposing partial data`, () => {
    const file = target();
    let attempts = 0;
    const waits = [];
    atomicWrite(file, NEXT, {
      platform: "win32",
      rename(source, destination) {
        attempts++;
        assert.equal(destination, file);
        assert.equal(readFileSync(file, "utf8"), OLD, "old destination survives until the rename succeeds");
        assert.equal(readFileSync(source, "utf8"), NEXT, "the temporary file is already complete");
        if (attempts <= 2) throw failure(code);
        renameSync(source, destination);
      },
      wait(ms) {
        waits.push(ms);
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
      },
    });
    assert.ok(attempts >= 3, "both injected locks must be retried");
    assert.ok(waits.length >= 2);
    assert.ok(waits.reduce((sum, ms) => sum + ms, 0) <= 1000, "waiting is bounded");
    assert.equal(readFileSync(file, "utf8"), NEXT);
    assert.equal(existsSync(`${file}.${process.pid}.tmp`), false);
  });
}

test("atomicWrite gives up on a persistent lock and retains the old complete destination", () => {
  const file = target();
  const error = failure("EPERM");
  let attempts = 0;
  const waits = [];
  assert.throws(() => atomicWrite(file, NEXT, {
    platform: "win32",
    rename() { attempts++; throw error; },
    wait(ms) { waits.push(ms); },
  }), (caught) => caught === error);
  assert.ok(attempts > 1 && attempts < 30, "bounded attempts even with a non-advancing test clock");
  assert.ok(waits.every(ms => ms > 0));
  assert.ok(waits.reduce((sum, ms) => sum + ms, 0) <= 1000);
  assert.equal(readFileSync(file, "utf8"), OLD);
  assert.equal(readFileSync(`${file}.${process.pid}.tmp`, "utf8"), NEXT);
});

for (const [platform, code] of [["linux", "EPERM"], ["darwin", "EBUSY"], ["win32", "ENOENT"], ["win32", "ENOSPC"]]) {
  test(`atomicWrite preserves immediate ${code} failure on ${platform}`, () => {
    const file = target();
    const error = failure(code);
    let attempts = 0;
    assert.throws(() => atomicWrite(file, NEXT, {
      platform,
      rename() { attempts++; throw error; },
      wait() { assert.fail("this failure must not wait"); },
    }), (caught) => caught === error);
    assert.equal(attempts, 1);
    assert.equal(readFileSync(file, "utf8"), OLD);
  });
}
