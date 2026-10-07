/**
 * The tests kept beside the plans and runners in docs/videos, and the two ways they could stop
 * running again without anyone noticing.
 *
 * `npm run test:tools` globs tools/** only, so docs/videos/imported-long-languages/runner.test.mjs
 * ran in no job, and two of its cases stayed red for two days after #1342. They run as
 * `npm run test:docs-videos`, in ci.yml's docs-videos job, which installs ffmpeg and is one of
 * the jobs the required `web` gate waits for.
 *
 * A folder named demo holds a video's prop: its acceptance test fails on purpose, because the
 * video shows it failing (docs/videos/ai-bug-fix-pr-review/demo/README.md). The script's glob
 * leaves out every test file whose own folder is named demo and selects every other one at any
 * depth, so a new folder needs no edit anywhere. A narrower glob, a test named outside
 * *.test.mjs, or a gate that stops waiting for the job would each look fine in review.
 */
import assert from "node:assert/strict";
import { globSync, readFileSync } from "node:fs";
import { join, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const SCRIPT = "test:docs-videos";
const posix = (file) => file.split(sep).join("/");

/** The files the script's quoted globs select, resolved by the glob node --test itself uses. */
function selected() {
  const command = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8")).scripts?.[SCRIPT];
  assert.ok(command, `package.json lost the ${SCRIPT} script`);
  // Quoted globs, expanded by node rather than a shell, are what make the command the same on
  // Windows (cmd.exe), Linux and macOS.
  assert.match(command, /^node --test( "[^"]+")+$/, `${SCRIPT} should stay node --test over quoted globs: ${command}`);
  const patterns = [...command.matchAll(/"([^"]+)"/g)].map((match) => match[1]);
  return new Set(globSync(patterns, { cwd: ROOT }).map(posix));
}

test("every test under docs/videos runs, except a demo folder's, which never does", () => {
  const found = globSync("docs/videos/**/*.test.{mjs,js,cjs,ts,mts,cts}", { cwd: ROOT }).map(posix);
  const props = found.filter((file) => file.split("/").at(-2) === "demo");
  assert.ok(found.length > props.length, "no test found under docs/videos — the scan itself is broken");
  const runs = selected();
  assert.deepEqual(
    found.filter((file) => !props.includes(file) && !runs.has(file)),
    [],
    `${SCRIPT} does not run these: name them *.test.mjs, or widen its glob`,
  );
  assert.deepEqual(props.filter((file) => runs.has(file)), [], "a demo folder's tests fail on purpose and must not run");
});

test("the docs-videos job installs ffmpeg, runs the script, and the web gate waits for it", () => {
  const ci = readFileSync(join(ROOT, ".github", "workflows", "ci.yml"), "utf8");
  const job = /^ {2}docs-videos:\r?\n((?: {4}.*\r?\n|[ \t]*\r?\n)+)/m.exec(ci)?.[1];
  assert.ok(job, "ci.yml has no docs-videos job");
  // Without ffmpeg six of the runner's native speech cases fail with ToolMissing.
  assert.match(job, /\bapt-get\b[^\n]*\binstall\b[^\n]*\bffmpeg\b/, "the docs-videos job no longer installs ffmpeg");
  assert.match(job, /^\s+- run: npm run test:docs-videos\s*$/m, `the docs-videos job no longer runs npm run ${SCRIPT}`);
  const needs = /^ {2}web:\r?\n {4}needs: \[([^\]]*)\]/m.exec(ci)?.[1]?.split(",").map((name) => name.trim());
  assert.ok(needs, "the web gate's needs list was not found — the scan itself is broken");
  assert.ok(needs.includes("docs-videos"), "the required web gate must wait for docs-videos");
});
