/**
 * The tests kept beside the plans and runners in docs/videos, and the two ways they could stop
 * running again without anyone noticing.
 *
 * `npm run test:tools` globs tools/** only, so docs/videos/imported-long-languages/runner.test.mjs
 * ran in no job, and two of its cases stayed red for two days after #1342. They run as
 * `npm run test:docs-videos`, in ci.yml's video-tests job, which installs ffmpeg and Chromium and
 * is one of the jobs the required `web` gate waits for. The same job runs every tools test again:
 * web-checks has neither tool, so the tools tests that need one skip there, and a skip here that
 * still names ffmpeg or Chromium fails the job.
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
  // A Claude Code mod kept beside the video that teaches it (docs/videos/<slug>/mods/<mod>/tests/)
  // has tests that import claude-code/testing and run under `claude plugin test`. node --test
  // cannot load them and CI has no Claude Code, so they are run where the video's run log says.
  const modTests = found.filter((file) => file.endsWith(".test.ts") && file.split("/").includes("mods"));
  assert.ok(found.length > props.length + modTests.length, "no test found under docs/videos — the scan itself is broken");
  const runs = selected();
  assert.deepEqual(
    found.filter((file) => !props.includes(file) && !modTests.includes(file) && !runs.has(file)),
    [],
    `${SCRIPT} does not run these: name them *.test.mjs, or widen its glob`,
  );
  assert.deepEqual(props.filter((file) => runs.has(file)), [], "a demo folder's tests fail on purpose and must not run");
  assert.deepEqual(modTests.filter((file) => runs.has(file)), [], "a mod's tests run under claude plugin test and must not be selected");
});

/** The positional arguments of a `node --test` command: its globs, quotes taken off. */
const globsOf = (command) => command.replace(/\\\r?\n\s*/g, " ").split(/\s+/).slice(2).filter((word) => word && !word.startsWith("--")).map((word) => word.replace(/^"(.*)"$/, "$1"));

test("the video-tests job installs ffmpeg and Chromium, runs both suites, fails on a skip that names either, and the web gate waits for it", () => {
  const ci = readFileSync(join(ROOT, ".github", "workflows", "ci.yml"), "utf8");
  const job = /^ {2}video-tests:\r?\n((?: {4}.*\r?\n|[ \t]*\r?\n)+)/m.exec(ci)?.[1];
  assert.ok(job, "ci.yml has no video-tests job");
  // Without ffmpeg six of the runner's native speech cases fail with ToolMissing.
  assert.match(job, /\bapt-get\b[^\n]*\binstall\b[^\n]*\bffmpeg\b/, "the video-tests job no longer installs ffmpeg");
  assert.match(job, /^\s+- run: npx playwright install --with-deps chromium\s*$/m, "the video-tests job no longer installs Chromium");
  assert.match(job, /^\s+- run: npm run test:docs-videos\s*$/m, `the video-tests job no longer runs npm run ${SCRIPT}`);
  // The tools tests again, on test:tools' own globs, with a TAP copy the skip check reads.
  const tools = /^ {10}(node --test (?:[^\n]*\\\r?\n {12})*[^\n]*)$/m.exec(job)?.[1];
  assert.ok(tools, "the video-tests job no longer runs the tools tests");
  const scripts = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8")).scripts;
  assert.deepEqual(globsOf(tools), globsOf(scripts["test:tools"]), "the video-tests job must run the tools tests test:tools runs");
  // Nothing narrows the run: a --test-name-pattern or --test-skip-pattern leaves the tests it drops
  // out of the TAP copy altogether, so the skip check below would not see them.
  const flags = tools.replace(/\\\r?\n\s*/g, " ").split(/\s+/).filter((word) => word.startsWith("--"));
  assert.deepEqual(flags, ["--test", "--test-reporter=spec", "--test-reporter-destination=stdout", "--test-reporter=tap", '--test-reporter-destination="$RUNNER_TEMP/tools-tests.tap"'], "the tools step takes the reporters and nothing else");
  assert.doesNotMatch(job, /continue-on-error/, "a step of the video-tests job that may fail would let a red test through");
  assert.match(tools, /--test-reporter=tap --test-reporter-destination="\$RUNNER_TEMP\/tools-tests\.tap"/);
  assert.match(job, /^ {8}env:\r?\n {10}VIDEO_RENDER_BROWSER_TESTS: "1"\r?\n {8}run: \|\r?\n {10}node --test /m, "the browser regressions run where Chromium is installed");
  assert.match(job, /if grep -E '# SKIP \.\*\(ffmpeg\|Chromium\)' "\$RUNNER_TEMP\/tools-tests\.tap"; then\s+echo "::error::[^"]*"\s+exit 1/, "a skip that names ffmpeg or Chromium must fail the job");
  const needs = /^ {2}web:\r?\n {4}needs: \[([^\]]*)\]/m.exec(ci)?.[1]?.split(",").map((name) => name.trim());
  assert.ok(needs, "the web gate's needs list was not found — the scan itself is broken");
  assert.ok(needs.includes("video-tests"), "the required web gate must wait for video-tests");
});
