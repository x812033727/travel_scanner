#!/usr/bin/env node
/**
 * Self-test before a push: run on this machine the checks the changed files call for,
 * instead of finding out from a GitHub Actions run.
 *
 *   npm run selftest                 # plan from the diff against origin/main, then run it
 *   npm run selftest -- --dry-run    # print the plan only
 *   npm run selftest -- --all        # every check, whatever changed
 *   npm run selftest -- --mark       # also post a `selftest` commit status on HEAD
 *   npm run selftest -- --base <ref> # diff against another ref
 *
 * The same `isDocsOnly` rule decides, in ci.yml's `changes` job, whether a pull request
 * may skip the browser, container and full-stack jobs. Keep this file free of
 * dependencies: that job runs it straight after a checkout, with no `npm ci`.
 *
 * What it cannot run here: the container builds and the full-stack smoke (they need
 * Docker, PostgreSQL, Redis and MinIO), the Playwright suites and Lighthouse. CI keeps
 * those; the plan says so instead of pretending they passed.
 */
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

/**
 * Paths that only change prose, plans and scripts for people: `docs/`, `tasks/` and a
 * Markdown file at the repository root. `.dockerignore` keeps `docs` out of every image
 * and no Playwright spec reads these files, so a change limited to them cannot move the
 * browser, container or full-stack results. Unit tests do read `docs/videos` (api tests,
 * vitest, the tools and docs-videos suites), which is why CI still runs those.
 */
const DOCS_ONLY = [/^docs\//, /^tasks\//, /^[^/]+\.md$/];

export function isDocsOnly(paths) {
  const list = paths.map((p) => p.trim()).filter(Boolean);
  return list.length > 0 && list.every((p) => DOCS_ONLY.some((re) => re.test(p)));
}

/** Every check this script knows, in the order it runs them. */
export const CHECKS = {
  tasks: { label: "task board", cmd: "npm run check:tasks" },
  "web-lint": { label: "web lint", cmd: "npm run lint:web" },
  i18n: { label: "i18n messages", cmd: "npm run check:i18n" },
  "web-types": { label: "web typecheck", cmd: "npm run typecheck:web" },
  "web-unit": { label: "web unit tests (vitest)", cmd: "npm run test:web" },
  "api-ruff": { label: "api ruff", cmd: "uv run ruff check .", cwd: "apps/api" },
  "api-mypy": { label: "api mypy", cmd: "uv run mypy app && uv run mypy tests", cwd: "apps/api" },
  "api-pytest": { label: "api pytest", cmd: "uv run pytest -q", cwd: "apps/api" },
  tools: { label: "tools tests", cmd: "npm run test:tools" },
  "docs-videos": { label: "docs/videos tests (needs ffmpeg)", cmd: "npm run test:docs-videos" },
};

const RULES = [
  { match: /^(apps\/web\/|package(-lock)?\.json$)/, checks: ["web-lint", "i18n", "web-types", "web-unit"] },
  { match: /^apps\/api\//, checks: ["api-ruff", "api-mypy", "api-pytest"] },
  // The tools tests read the skills, the workflows, AGENTS.md and parts of docs/.
  { match: /^(tools\/|\.agents\/|\.claude\/|\.github\/|docs\/|[^/]+\.md$|package\.json$)/, checks: ["tools"] },
  { match: /^docs\/videos\//, checks: ["docs-videos"] },
];

/** What only CI can show for these paths. */
const CI_ONLY = [
  { match: /^(apps\/|ops\/|docker-compose|\.env\.example$|nginx\/)/, note: "containers and full-stack-smoke run on CI only" },
  { match: /^apps\/web\//, note: "Playwright suites (web-e2e, Planner UX, Food map, Travel discovery) and the SEO audit run on CI only" },
];

/** Pure: which checks the changed paths call for, plus what is left to CI. */
export function planChecks(paths, { all = false } = {}) {
  const list = paths.map((p) => p.trim()).filter(Boolean);
  const wanted = new Set(all ? Object.keys(CHECKS) : ["tasks"]);
  const ciOnly = new Set(all ? CI_ONLY.map((rule) => rule.note) : []);
  for (const p of list) {
    for (const rule of RULES) if (rule.match.test(p)) rule.checks.forEach((c) => wanted.add(c));
    for (const rule of CI_ONLY) if (rule.match.test(p)) ciOnly.add(rule.note);
  }
  return {
    docsOnly: isDocsOnly(list),
    checks: Object.keys(CHECKS).filter((id) => wanted.has(id)),
    ciOnly: [...ciOnly],
  };
}

function git(args) {
  const res = spawnSync("git", args, { encoding: "utf8" });
  if (res.status !== 0) throw new Error(`git ${args.join(" ")} failed: ${res.stderr.trim()}`);
  return res.stdout;
}

function changedPaths(base) {
  const mergeBase = git(["merge-base", base, "HEAD"]).trim();
  const committed = git(["diff", "--name-only", `${mergeBase}...HEAD`]);
  const working = git(["diff", "--name-only", "HEAD"]);
  const untracked = git(["ls-files", "--others", "--exclude-standard"]);
  return [...new Set(`${committed}\n${working}\n${untracked}`.split("\n").map((p) => p.trim()).filter(Boolean))];
}

function parseArgs(argv) {
  const opts = { base: "origin/main", all: false, dryRun: false, mark: false, docsOnly: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--all") opts.all = true;
    else if (a === "--dry-run") opts.dryRun = true;
    else if (a === "--mark") opts.mark = true;
    else if (a === "--base") opts.base = argv[++i];
    else if (a === "--docs-only") opts.docsOnly = true;
    else throw new Error(`unknown option ${a}`);
  }
  return opts;
}

function markStatus(state, description) {
  const sha = git(["rev-parse", "HEAD"]).trim();
  const res = spawnSync(
    "gh",
    ["api", `repos/{owner}/{repo}/statuses/${sha}`, "-f", `state=${state}`, "-f", "context=selftest", "-f", `description=${description.slice(0, 140)}`],
    { encoding: "utf8" },
  );
  if (res.status !== 0) console.error(`could not post the selftest status: ${res.stderr.trim()}`);
  else console.log(`posted selftest=${state} on ${sha.slice(0, 9)}`);
}

function main() {
  const opts = parseArgs(process.argv.slice(2));

  // ci.yml's `changes` job: paths on stdin, prints true or false.
  if (opts.docsOnly) {
    console.log(isDocsOnly(readFileSync(0, "utf8").split("\n")) ? "true" : "false");
    return;
  }

  if (opts.mark && git(["status", "--porcelain"]).trim()) {
    throw new Error("--mark needs a clean working tree: the status is posted on HEAD, so commit first");
  }
  const paths = changedPaths(opts.base);
  const plan = planChecks(paths, { all: opts.all });
  console.log(`${paths.length} changed file(s) against ${opts.base}${plan.docsOnly ? " (docs only)" : ""}`);
  console.log(`checks: ${plan.checks.join(", ")}`);
  for (const note of plan.ciOnly) console.log(`left to CI: ${note}`);
  if (opts.dryRun) return;

  const results = [];
  for (const id of plan.checks) {
    const check = CHECKS[id];
    console.log(`\n=== ${check.label}: ${check.cmd}${check.cwd ? ` (in ${check.cwd})` : ""}`);
    const started = Date.now();
    const res = spawnSync(check.cmd, { shell: true, stdio: "inherit", cwd: check.cwd ?? process.cwd() });
    results.push({ id, ok: res.status === 0, seconds: Math.round((Date.now() - started) / 1000) });
  }

  console.log("\n=== selftest summary");
  for (const r of results) console.log(`${r.ok ? "PASS" : "FAIL"}  ${CHECKS[r.id].label}  ${r.seconds}s`);
  const failed = results.filter((r) => !r.ok).map((r) => r.id);
  if (opts.mark) {
    markStatus(failed.length ? "failure" : "success", failed.length ? `failed: ${failed.join(", ")}` : `passed: ${plan.checks.join(", ")}`);
  }
  if (failed.length) process.exitCode = 1;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  try {
    main();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
