/**
 * Three CI fixes that stop working without anyone noticing if a later edit undoes them.
 *
 * Container images. `docker run` pulls a missing image once, and a single 502, 504 or
 * connection reset from quay.io or auth.docker.io failed a required job seven times in four
 * jobs. Each job now pulls its images with tools/ci/pull-images.sh, which retries transient
 * failures, and then runs them with `--pull=never` from one env var. A new `docker run` that
 * names its image inline, or a pull list that forgets one, would put the single unretried pull
 * back, and it would look fine in review.
 *
 * Keep-alive. The web start script carries `--keepAliveTimeout`, the same value production
 * sets as KEEP_ALIVE_TIMEOUT. Without it, Next closes an idle connection after about 6 s, and
 * Playwright's request context reuses that socket and gets `read ECONNRESET`.
 *
 * Browser results. Uploading apps/web/test-results on every run filled the repository's
 * artifact storage until a passing job failed to finalize its upload (403). They upload only
 * when something failed.
 */
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { delimiter, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const WORKFLOWS = join(ROOT, ".github", "workflows");
const PULL_SCRIPT = join(ROOT, "tools", "ci", "pull-images.sh");

function workflows() {
  return readdirSync(WORKFLOWS)
    .filter((name) => name.endsWith(".yml") || name.endsWith(".yaml"))
    .map((name) => ({ name, source: readFileSync(join(WORKFLOWS, name), "utf8") }));
}

/** The text before `jobs:` (workflow-level env lives there) and each job's own text. */
function splitJobs(source) {
  const start = source.search(/^jobs:\s*$/m);
  if (start < 0) return { preamble: source, jobs: [] };
  const body = source.slice(start).replace(/^jobs:\s*\n/, "");
  const jobs = body
    .split(/^(?=  [A-Za-z0-9_-]+:\s*$)/m)
    .filter((text) => text.trim())
    .map((text) => ({ job: text.trim().split(":")[0], text }));
  return { preamble: source.slice(0, start), jobs };
}

/** Script lines with shell continuations joined, so a `docker run` spread over lines is one. */
function commandLines(text) {
  return text
    .replace(/\\\r?\n\s*/g, " ")
    .split("\n")
    .filter((line) => !line.trim().startsWith("#"));
}

function dockerRuns() {
  return workflows().flatMap(({ name, source }) => {
    const { preamble, jobs } = splitJobs(source);
    return jobs.flatMap(({ job, text }) => {
      const lines = commandLines(text);
      return lines.flatMap((line, index) =>
        /\bdocker run\b/.test(line) ? [{ workflow: name, job, text, preamble, lines, index, line: line.trim() }] : [],
      );
    });
  });
}

const IMAGE_VAR = /"\$\{?([A-Z][A-Z0-9_]*_IMAGE)\}?"/;

test("every docker run uses a pre-pulled image named by an env var", () => {
  const runs = dockerRuns();
  // A guard that finds nothing passes forever. CI does start containers; zero here means the
  // scan broke, not that the workflows stopped using docker.
  assert.ok(runs.length > 0, "no `docker run` found — the scan itself is broken");
  const problems = [];
  for (const { workflow, job, line } of runs) {
    if (!/\s--pull=never\b/.test(line)) problems.push(`${workflow} ${job}: missing --pull=never: ${line}`);
    if (!IMAGE_VAR.test(line)) problems.push(`${workflow} ${job}: image is not a quoted *_IMAGE env var: ${line}`);
  }
  assert.deepEqual(problems, [], "pull the image with tools/ci/pull-images.sh and run it with --pull=never");
});

test("each image a job runs is declared and passed to pull-images.sh earlier in that job", () => {
  const problems = [];
  for (const { workflow, job, text, preamble, lines, index, line } of dockerRuns()) {
    const name = IMAGE_VAR.exec(line)?.[1];
    if (!name) continue; // reported by the test above
    const declared = new RegExp(`^\\s+${name}:\\s*\\S`, "m");
    if (!declared.test(text) && !declared.test(preamble)) {
      problems.push(`${workflow} ${job}: ${name} is not set in the job or workflow env`);
    }
    const pulledBefore = lines
      .slice(0, index)
      .some((earlier) => earlier.includes("tools/ci/pull-images.sh") && new RegExp(`\\$\\{?${name}\\b`).test(earlier));
    // With --pull=never a missing pull fails loudly, but only on the run that needs it; this
    // says so before anything is pushed.
    if (!pulledBefore) problems.push(`${workflow} ${job}: ${name} is not passed to tools/ci/pull-images.sh before it runs`);
  }
  assert.deepEqual(problems, []);
});

test("an image env var names the same image in every workflow", () => {
  const values = new Map();
  for (const { name, source } of workflows()) {
    for (const match of source.matchAll(/^\s+([A-Z][A-Z0-9_]*_IMAGE):\s*(\S+)\s*$/gm)) {
      if (!values.has(match[1])) values.set(match[1], new Map());
      const byValue = values.get(match[1]);
      byValue.set(match[2], [...(byValue.get(match[2]) ?? []), name]);
    }
  }
  assert.ok(values.size > 0, "no *_IMAGE env var found — the scan itself is broken");
  const split = [...values.entries()]
    .filter(([, byValue]) => byValue.size > 1)
    .map(([variable, byValue]) => `${variable}: ${[...byValue.keys()].join(", ")}`);
  // One tag in ci.yml and another in travel-discovery.yml is how an image bump gets
  // half-applied.
  assert.deepEqual(split, []);
});

test("the web start script keeps connections open as long as production does", () => {
  const { scripts } = JSON.parse(readFileSync(join(ROOT, "apps", "web", "package.json"), "utf8"));
  const flag = /--keepAliveTimeout\s+(\d+)/.exec(scripts.start);
  assert.ok(flag, `apps/web start script lost --keepAliveTimeout: ${scripts.start}`);
  const compose = readFileSync(join(ROOT, "docker-compose.prod.yml"), "utf8");
  const production = /^\s+KEEP_ALIVE_TIMEOUT:\s*"?(\d+)"?\s*$/m.exec(compose);
  assert.ok(production, "KEEP_ALIVE_TIMEOUT not found in docker-compose.prod.yml");
  // The workflow comments promise these match; this is what keeps that true.
  assert.equal(flag[1], production[1]);
});

test("browser results upload only when something failed", () => {
  const uploads = workflows().flatMap(({ name, source }) =>
    source
      .split(/^\s*- /m)
      .filter((step) => step.includes("actions/upload-artifact@") && /^\s*path:\s*apps\/web\/test-results\s*$/m.test(step))
      .map((step) => ({
        workflow: name,
        artifact: /^\s*name:\s*(\S+)/m.exec(step)?.[1],
        condition: /^\s*if:\s*(.+)$/m.exec(step)?.[1]?.trim() ?? "(none)",
      })),
  );
  const names = uploads.map(({ workflow, artifact }) => `${workflow}: ${artifact}`);
  const suiteUploads = [
    "ci.yml: site-experience-browser-results",
    "ci.yml: community-browser-results",
    "travel-discovery.yml: discovery-browser-results",
    "planner-premium.yml: planner-premium-browser-results",
    "food-map-reservations.yml: food-map-reservations-browser-results",
  ];
  for (const expected of suiteUploads) {
    assert.ok(names.includes(expected), `upload not found — the scan itself is broken: ${expected}`);
  }
  const unconditional = uploads
    .filter(({ condition }) => !condition.includes("failure()") || condition.includes("always()"))
    .map(({ workflow, artifact, condition }) => `${workflow}: ${artifact} (if: ${condition})`);
  assert.deepEqual(unconditional, [], "upload apps/web/test-results with `if: failure()`");
  // A job that hits timeout-minutes ends cancelled, not failed, and a hung browser run is exactly
  // when its traces get read, so the whole-suite uploads keep that case too.
  const missingTimeout = uploads
    .filter(({ workflow, artifact }) => suiteUploads.includes(`${workflow}: ${artifact}`))
    .filter(({ condition }) => condition !== "failure() || cancelled()")
    .map(({ workflow, artifact, condition }) => `${workflow}: ${artifact} (if: ${condition})`);
  assert.deepEqual(missingTimeout, [], "suite result uploads use `if: failure() || cancelled()`");
});

/** Returns false when bash can run the script here, or the reason it cannot. */
function bashUnavailable() {
  const probe = mkdtempSync(join(tmpdir(), "pull-images-probe-"));
  try {
    // On Windows the first `bash` on PATH can be the WSL launcher, which cannot see this path.
    const result = spawnSync("bash", ["-c", 'test -d "$1"', "probe", probe.replaceAll("\\", "/")], { encoding: "utf8" });
    if (result.error) return `bash is not available (${result.error.code})`;
    return result.status === 0 ? false : "bash cannot see the temp directory";
  } finally {
    rmSync(probe, { recursive: true, force: true });
  }
}

const PATH_KEY = Object.keys(process.env).find((key) => key.toUpperCase() === "PATH") ?? "PATH";

/**
 * Runs pull-images.sh with a fake `docker` first on PATH. `behaviour` is shell run on every
 * call after the call is recorded; `$calls` is how many calls there have been so far.
 */
function pull({ behaviour, images = ["quay.io/minio/minio:RELEASE.2025-09-07T16-13-09Z"], env = {} }) {
  const bin = mkdtempSync(join(tmpdir(), "pull-images-"));
  try {
    const script = (body) => `#!/usr/bin/env bash\n${body}\n`;
    writeFileSync(
      join(bin, "docker"),
      script(`log="$(dirname "$0")/calls"\necho "$*" >> "$log"\ncalls=$(( $(wc -l < "$log") ))\n${behaviour}`),
      { mode: 0o755 },
    );
    // Stands in for coreutils `timeout`, so the Windows timeout.exe on PATH cannot answer.
    writeFileSync(join(bin, "timeout"), script(`test "$1" -gt 0\nshift\nexec "$@"`), { mode: 0o755 });
    const result = spawnSync("bash", [PULL_SCRIPT.replaceAll("\\", "/"), ...images], {
      encoding: "utf8",
      env: { ...process.env, PULL_RETRY_DELAY: "0", ...env, [PATH_KEY]: `${bin}${delimiter}${process.env[PATH_KEY]}` },
    });
    let calls = [];
    try {
      calls = readFileSync(join(bin, "calls"), "utf8").split("\n").filter(Boolean);
    } catch {
      // docker was never called
    }
    return { status: result.status, output: `${result.stdout}${result.stderr}`, calls };
  } finally {
    rmSync(bin, { recursive: true, force: true });
  }
}

const RESET = `echo 'Error response from daemon: Get "https://quay.io/v2/": read tcp 10.1.0.253:39838->3.14.204.72:443: read: connection reset by peer' >&2; exit 1`;

test("pull-images.sh", { skip: bashUnavailable() }, async (t) => {
  await t.test("pulls each image once when the registry answers", () => {
    const result = pull({ behaviour: 'echo "$3"', images: ["nginx:1.28-alpine", "axllent/mailpit:latest"] });
    assert.equal(result.status, 0, result.output);
    assert.deepEqual(result.calls, ["pull --quiet nginx:1.28-alpine", "pull --quiet axllent/mailpit:latest"]);
    assert.doesNotMatch(result.output, /::(warning|error)::/);
  });

  await t.test("retries a transient failure and succeeds", () => {
    const result = pull({
      behaviour: `if [ "$calls" -eq 1 ]; then echo 'docker: received unexpected HTTP status: 502 Bad Gateway' >&2; exit 1; fi\necho "$3"`,
    });
    assert.equal(result.status, 0, result.output);
    assert.equal(result.calls.length, 2);
    assert.match(result.output, /502 Bad Gateway/, "docker's own output is printed");
    assert.match(result.output, /::warning::docker pull quay\.io\/minio\/minio:\S+ failed \(attempt 1\/5/);
    assert.doesNotMatch(result.output, /::error::/);
  });

  await t.test("does not retry a refusal", () => {
    const result = pull({
      behaviour: `echo "Error response from daemon: pull access denied for minio/minio, repository does not exist or may require 'docker login': denied: requested access to the resource is denied" >&2; exit 1`,
    });
    assert.equal(result.status, 1, result.output);
    assert.equal(result.calls.length, 1);
    assert.match(result.output, /::error::docker pull quay\.io\/minio\/minio:\S+ was refused/);
    assert.doesNotMatch(result.output, /::warning::/);
  });

  await t.test("gives up after PULL_ATTEMPTS transient failures", () => {
    const result = pull({ behaviour: RESET, env: { PULL_ATTEMPTS: "2" } });
    assert.equal(result.status, 1, result.output);
    assert.equal(result.calls.length, 2);
    assert.match(result.output, /::warning::.*attempt 1\/2/);
    assert.match(result.output, /::error::docker pull \S+ failed 2 times/);
  });

  await t.test("rejects an attempt count that would never pull", () => {
    for (const attempts of ["0", "abc", "-1"]) {
      const result = pull({ behaviour: RESET, env: { PULL_ATTEMPTS: attempts } });
      assert.equal(result.status, 2, `${attempts}: ${result.output}`);
      assert.deepEqual(result.calls, []);
      assert.match(result.output, /::error::PULL_ATTEMPTS/);
    }
  });
});
