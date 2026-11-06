import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { CHECKS, isDocsOnly, planChecks } from "./selftest.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SCRIPT = join(ROOT, "tools", "selftest.mjs");

test("a change to scripts, plans and tasks only is docs only", () => {
  assert.equal(isDocsOnly(["docs/videos/series-plans/a/e001.md", "tasks/open/x.md", "README.md"]), true);
});

test("any code, workflow, skill or nested Markdown outside docs is not docs only", () => {
  for (const path of ["apps/web/app/page.tsx", "apps/api/README.md", ".github/workflows/ci.yml", ".agents/skills/x/SKILL.md", "tools/x.mjs", "package.json"]) {
    assert.equal(isDocsOnly(["docs/a.md", path]), false, path);
  }
});

test("an empty change is not docs only, so CI runs everything", () => {
  assert.equal(isDocsOnly([]), false);
  assert.equal(isDocsOnly(["", "  "]), false);
});

test("a script under docs/videos runs the tools and docs-videos tests, nothing for web or api", () => {
  const plan = planChecks(["docs/videos/zhong-tian-qu-qi-e040/script.md"]);
  assert.deepEqual(plan.checks, ["tasks", "tools", "docs-videos"]);
  assert.equal(plan.docsOnly, true);
  assert.deepEqual(plan.ciOnly, []);
});

test("a web change runs the web gate locally and names what is left to CI", () => {
  const plan = planChecks(["apps/web/components/a.tsx"]);
  assert.deepEqual(plan.checks, ["tasks", "web-lint", "i18n", "web-types", "web-unit"]);
  assert.ok(plan.ciOnly.some((note) => note.includes("Playwright")));
  assert.ok(plan.ciOnly.some((note) => note.includes("full-stack-smoke")));
});

test("an api change runs ruff, mypy and pytest", () => {
  assert.deepEqual(planChecks(["apps/api/app/main.py"]).checks, ["tasks", "api-ruff", "api-mypy", "api-pytest"]);
});

test("--all plans every check", () => {
  assert.deepEqual(planChecks([], { all: true }).checks, Object.keys(CHECKS));
});

test("--docs-only reads paths on stdin, as ci.yml's changes job calls it", () => {
  const run = (input) => spawnSync(process.execPath, [SCRIPT, "--docs-only"], { input, encoding: "utf8" }).stdout.trim();
  assert.equal(run("docs/a.md\ntasks/open/b.md\n"), "true");
  assert.equal(run("docs/a.md\napps/web/a.ts\n"), "false");
  assert.equal(run(""), "false");
});

test("ci.yml lets a gate pass a skipped job only on a docs-only change", () => {
  const ci = readFileSync(join(ROOT, ".github", "workflows", "ci.yml"), "utf8");
  assert.match(ci, /node tools\/selftest\.mjs --docs-only/);
  for (const job of ["web-e2e", "containers", "full-stack-smoke"]) {
    const block = ci.split(new RegExp(`^  ${job}:\\n`, "m"))[1]?.split(/^  [a-z0-9-]+:\n/m)[0] ?? "";
    assert.match(block, /needs\.changes\.outputs\.docs_only != 'true'/, `${job} must skip on docs only`);
    // A failed `changes` job must make the job run, not skip it into a pass.
    assert.match(block, /!cancelled\(\)/, `${job} must not inherit a skip from a failed changes job`);
  }
});
