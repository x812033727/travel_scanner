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
function child(body, { keep = false } = {}) {
  const env = { ...process.env };
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
