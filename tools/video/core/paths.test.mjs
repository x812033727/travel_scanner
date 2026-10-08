import assert from "node:assert/strict";
import { spawn } from "node:child_process";
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
    assert.ok(waits.reduce((sum, ms) => sum + ms, 0) <= 3000, "waiting is bounded");
    assert.equal(readFileSync(file, "utf8"), NEXT);
    assert.equal(existsSync(`${file}.${process.pid}.tmp`), false);
  });
}

test("atomicWrite survives a Windows sharing conflict that outlasts seven rename attempts", () => {
  const file = target();
  let attempts = 0;
  let waited = 0;
  atomicWrite(file, NEXT, {
    platform: "win32",
    rename(source, destination) {
      attempts++;
      assert.equal(readFileSync(destination, "utf8"), OLD);
      assert.equal(readFileSync(source, "utf8"), NEXT);
      if (waited < 1000) throw failure("EPERM");
      renameSync(source, destination);
    },
    wait(ms) { waited += ms; },
  });
  assert.ok(attempts >= 8, "all seven attempts before the one-second release must be retried");
  assert.ok(waited >= 1000 && waited <= 3000, "a longer transient lock gets a bounded retry");
  assert.equal(readFileSync(file, "utf8"), NEXT);
  assert.equal(existsSync(`${file}.${process.pid}.tmp`), false);
});

test("atomicWrite survives a real Windows reader that denies delete sharing for one second", { skip: process.platform !== "win32", timeout: 20_000 }, async (t) => {
  const file = target();
  const release = path.join(path.dirname(file), "start-release-delay");
  // A separate process must release the handle: atomicWrite's synchronous wait blocks
  // this process's timers. Start its one-second delay only after a real rename fails.
  const script = `
    $ErrorActionPreference = 'Stop'
    $taskStream = [System.IO.File]::Open($env:ATOMIC_TEST_TARGET, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
      [Console]::Out.WriteLine('locked')
      [Console]::Out.Flush()
      $taskClock = [System.Diagnostics.Stopwatch]::StartNew()
      while (-not [System.IO.File]::Exists($env:ATOMIC_TEST_RELEASE)) {
        if ($taskClock.ElapsedMilliseconds -gt 5000) { throw 'release signal did not arrive' }
        Start-Sleep -Milliseconds 10
      }
      Start-Sleep -Milliseconds 1000
    } finally { $taskStream.Dispose() }
  `;
  const child = spawn("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", script], {
    windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, ATOMIC_TEST_TARGET: file, ATOMIC_TEST_RELEASE: release },
  });
  let stdout = "";
  let stderr = "";
  let failure;
  let finished = false;
  child.on("error", (error) => { failure = error; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const closed = new Promise((resolve) => child.on("close", (code, signal) => {
    finished = true;
    resolve({ code, signal });
  }));
  const ready = new Promise((resolve) => child.stdout.on("data", (chunk) => {
    stdout += chunk;
    if (stdout.includes("locked")) resolve();
  }));
  const bounded = async (promise, message, ms = 5000) => {
    let timer;
    try {
      return await Promise.race([promise, new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Error(`${message}: ${failure?.message ?? stderr}`)), ms);
      })]);
    } finally { clearTimeout(timer); }
  };
  t.after(async () => {
    try {
      if (!finished) child.kill("SIGKILL");
      await bounded(closed, "sharing holder did not close during cleanup");
    } finally {
      child.stdout.destroy();
      child.stderr.destroy();
      if (!finished) child.unref();
    }
  });
  await bounded(Promise.race([ready, closed.then(({ code, signal }) => {
    throw new Error(`sharing holder closed before ready (${code}, ${signal}): ${failure?.message ?? stderr}`);
  })]), "sharing holder did not become ready", 10_000);
  const denied = [];
  try {
    atomicWrite(file, NEXT, {
      rename(source, destination) {
        assert.equal(readFileSync(destination, "utf8"), OLD);
        assert.equal(readFileSync(source, "utf8"), NEXT);
        try { renameSync(source, destination); }
        catch (error) {
          denied.push(error.code);
          if (denied.length === 1) writeFileSync(release, "start");
          throw error;
        }
      },
    });
  } catch (error) {
    assert.equal(readFileSync(file, "utf8"), OLD, "a failed rename preserves the old complete target");
    assert.equal(readFileSync(`${file}.${process.pid}.tmp`, "utf8"), NEXT, "the new complete bytes remain recoverable");
    throw error;
  }
  assert.ok(denied.length > 0 && denied.every((code) => ["EPERM", "EACCES", "EBUSY"].includes(code)), "a real sharing conflict was encountered");
  assert.equal(readFileSync(file, "utf8"), NEXT);
  assert.equal(existsSync(`${file}.${process.pid}.tmp`), false);
  assert.deepEqual(await bounded(closed, "sharing holder did not finish"), { code: 0, signal: null });
});

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
  assert.equal(waits.reduce((sum, ms) => sum + ms, 0), 2550, "persistent failures exhaust the fixed wait budget");
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
