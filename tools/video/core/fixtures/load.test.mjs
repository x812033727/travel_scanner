// The sandboxes the video tests make go when the test process exits, so a run of the tool tests
// leaves nothing behind in the system's temporary directory (they once piled up by the tens of
// thousands). Each case runs a child node process, because the removal happens on its exit.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import path from "node:path";
import test from "node:test";

const LOAD = new URL("./load.mjs", import.meta.url).href;

/** Runs `body` as an ES module in a child node process and returns what it printed, one line per entry. */
function child(body, { keep = false, env: extra = {} } = {}) {
  const env = { ...process.env, ...extra };
  delete env.VIDEO_KEEP_SANDBOX;
  if (keep) env.VIDEO_KEEP_SANDBOX = "1";
  const result = spawnSync(process.execPath, ["--input-type=module", "-e", body], { env, encoding: "utf8" });
  return { status: result.status, stderr: result.stderr, lines: result.stdout.split(/\r?\n/).filter(Boolean) };
}

test("a sandbox is removed when the process that made it exits", () => {
  const run = child(`
    const { sandbox, tempDir } = await import(${JSON.stringify(LOAD)});
    const box = sandbox();
    const drama = sandbox("fixture-drama", "drama");
    console.log(box.base);
    console.log(drama.base);
    console.log(tempDir("video-core-test-"));
  `);
  assert.equal(run.status, 0, run.stderr);
  assert.equal(run.lines.length, 3);
  for (const dir of run.lines) assert.ok(!existsSync(dir), `${dir} is gone`);
});

test("VIDEO_KEEP_SANDBOX=1 keeps the sandbox for a look", (t) => {
  const run = child(`
    const { sandbox } = await import(${JSON.stringify(LOAD)});
    console.log(sandbox().base);
  `, { keep: true });
  assert.equal(run.status, 0, run.stderr);
  const [base] = run.lines;
  t.after(() => base && rmSync(base, { recursive: true, force: true }));
  assert.ok(path.basename(base).startsWith("video-core-"));
  assert.ok(existsSync(path.join(base, "repo", "docs", "videos", "fixture-minimal", "video.json")), "the kept sandbox still holds its fixture");
});

test("a sandbox that cannot be removed neither fails the exit nor keeps the others", (t) => {
  // rmSync throws for the first sandbox, as a file still open on Windows would make it.
  const run = child(`
    import fs from "node:fs";
    import { syncBuiltinESMExports } from "node:module";
    const rmSync = fs.rmSync;
    let first;
    fs.rmSync = (dir, options) => {
      if (dir === first) throw Object.assign(new Error("resource busy or locked"), { code: "EBUSY" });
      return rmSync(dir, options);
    };
    syncBuiltinESMExports();
    const { sandbox } = await import(${JSON.stringify(LOAD)});
    first = sandbox().base;
    console.log(first);
    console.log(sandbox().base);
  `);
  const [locked, other] = run.lines;
  t.after(() => locked && rmSync(locked, { recursive: true, force: true }));
  assert.equal(run.status, 0, run.stderr);
  assert.equal(run.stderr, "");
  assert.ok(existsSync(locked), "the one that failed is left behind");
  assert.ok(!existsSync(other), "the next one still went");
});

/** Starts `body` in a child node process, waits for its first line, then sends `signal`. */
async function interrupted(body, signal, env = {}) {
  const { spawn } = await import("node:child_process");
  const childEnv = { ...process.env, ...env };
  delete childEnv.VIDEO_KEEP_SANDBOX;
  const proc = spawn(process.execPath, ["--input-type=module", "-e", body], { env: childEnv, stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "", stderr = "";
  proc.stderr.on("data", (chunk) => (stderr += chunk));
  const first = await new Promise((resolve, reject) => {
    proc.stdout.on("data", (chunk) => {
      stdout += chunk;
      if (stdout.includes("\n")) resolve(stdout.split(/\r?\n/)[0]);
    });
    proc.on("exit", () => reject(new Error(`exited before it printed: ${stderr}`)));
  });
  const ended = new Promise((resolve) => proc.on("exit", (code, sig) => resolve({ code, signal: sig })));
  proc.kill(signal);
  return { dir: first, ...(await ended), stderr };
}

// Made, then waits to be stopped, as a test file stopped partway through a run does.
const WAITS = `
  const { sandbox } = await import(${JSON.stringify(LOAD)});
  console.log(sandbox().base);
  setInterval(() => {}, 1000);
`;

for (const signal of ["SIGINT", "SIGTERM"]) {
  test(`a sandbox is removed when the process that made it is stopped with ${signal}, and the process still ends by ${signal}`, { skip: process.platform === "win32" && "no POSIX signals" }, async () => {
    const run = await interrupted(WAITS, signal);
    assert.ok(run.dir.includes("video-core-"), run.stderr);
    assert.ok(!existsSync(run.dir), `${run.dir} is gone`);
    assert.equal(run.signal, signal, "the signal still ends the process");
  });
}

test("what a SIGKILL leaves is swept by a later process once it is old, and a young one is kept", { skip: process.platform === "win32" && "no POSIX signals" }, async (t) => {
  const { mkdtempSync, mkdirSync, utimesSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const parent = mkdtempSync(path.join(tmpdir(), "load-sweep-"));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const env = { TMPDIR: parent, TEMP: parent, TMP: parent };
  const killed = await interrupted(WAITS, "SIGKILL", env);
  assert.ok(existsSync(killed.dir), "a SIGKILL cannot be caught: the sandbox stays");
  // Seven hours old now, past STALE_SANDBOX_MS; another one made a minute ago stays.
  const old = new Date(Date.now() - 7 * 60 * 60 * 1000);
  utimesSync(killed.dir, old, old);
  const young = path.join(parent, "video-core-young");
  mkdirSync(young);
  const run = child(`
    const { sandbox } = await import(${JSON.stringify(LOAD)});
    console.log(sandbox().base);
  `, { env });
  assert.equal(run.status, 0, run.stderr);
  assert.ok(!existsSync(killed.dir), "the next process's first sandbox swept the old one");
  assert.ok(existsSync(young), "a sandbox of a run still going is left alone");
});

test("the sweep removes only old directories with the prefix, follows no link, and VIDEO_KEEP_SANDBOX=1 turns it off", async (t) => {
  const { mkdtempSync, mkdirSync, symlinkSync, utimesSync, writeFileSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const { sweepStaleSandboxes, STALE_SANDBOX_MS } = await import(LOAD);
  const parent = mkdtempSync(path.join(tmpdir(), "load-sweep-"));
  const outside = mkdtempSync(path.join(tmpdir(), "load-outside-"));
  t.after(() => {
    rmSync(parent, { recursive: true, force: true });
    rmSync(outside, { recursive: true, force: true });
  });
  const now = Date.now();
  const age = (dir, ms) => utimesSync(dir, new Date(now - ms), new Date(now - ms));
  const stale = path.join(parent, "video-core-stale");
  mkdirSync(path.join(stale, "repo"), { recursive: true });
  age(stale, STALE_SANDBOX_MS + 60_000);
  const fresh = path.join(parent, "video-core-fresh");
  mkdirSync(fresh);
  const other = path.join(parent, "something-else");
  mkdirSync(other);
  age(other, STALE_SANDBOX_MS * 2);
  const file = path.join(parent, "video-core-file");
  writeFileSync(file, "x");
  writeFileSync(path.join(outside, "keep.txt"), "kept");
  const link = path.join(parent, "video-core-link");
  let linked = true;
  try {
    symlinkSync(outside, link, "dir");
  } catch {
    linked = false; // Windows without the symlink privilege.
  }
  assert.deepEqual(sweepStaleSandboxes("video-core-", { parent, now }), [stale]);
  assert.ok(!existsSync(stale));
  for (const kept of [fresh, other, file]) assert.ok(existsSync(kept), `${kept} is kept`);
  if (linked) assert.ok(existsSync(path.join(outside, "keep.txt")), "the link's target is untouched");

  // With VIDEO_KEEP_SANDBOX=1 a new sandbox sweeps nothing.
  const kept = path.join(parent, "video-core-kept");
  mkdirSync(kept);
  age(kept, STALE_SANDBOX_MS * 2);
  const run = child(`
    const { sandbox } = await import(${JSON.stringify(LOAD)});
    console.log(sandbox().base);
  `, { keep: true, env: { TMPDIR: parent, TEMP: parent, TMP: parent } });
  assert.equal(run.status, 0, run.stderr);
  assert.ok(existsSync(kept), "kept sandboxes are not swept");
});
