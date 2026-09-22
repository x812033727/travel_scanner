#!/usr/bin/env node
/**
 * Who is on what: the read-only survey to run before claiming a ticket or opening a PR.
 *
 *   node .agents/skills/task-board/scripts/who-is-on-it.mjs [--scope <path>] [--json]
 *
 * The board alone cannot answer it: `claim` only writes to the task file on your own branch,
 * so the checks that catch a collision are the branches. This prints, from the repository root:
 *   - active claims (in-progress / review) with their age, whether they are stale (24 h),
 *     and where their branch is visible: `+` (checked out in another local worktree), remote,
 *     an open PR;
 *   - the open tasks each active claim locks (shared scope), so a stale claim's cost is visible;
 *   - local worktrees, `+` branches and remote heads that no task's `branch` field names
 *     (work that is not on the board);
 *   - with --scope, every active task and open PR that touches that path.
 * Nothing here writes. `gh` is optional; without it the PR columns are skipped.
 */
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import {
  STALE_CLAIM_HOURS,
  isStale,
  loadTasks,
  scopesOverlap,
  sharedScope,
} from "../../../../tools/tasks.mjs";

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const ACTIVE = new Set(["in-progress", "review"]);
const args = process.argv.slice(2);
const scopeArg = args.includes("--scope") ? args[args.indexOf("--scope") + 1] : null;
const asJson = args.includes("--json");

function run(file, fileArgs, { optional = false } = {}) {
  try {
    return execFileSync(file, fileArgs, { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch (error) {
    if (optional) return null;
    throw error;
  }
}

function hoursSince(stamp, now) {
  const then = Date.parse(stamp);
  return Number.isNaN(then) ? null : Math.round((now - then) / 36e5);
}

const now = Date.now();
const tasks = loadTasks(ROOT);
const open = tasks.filter((task) => task.status !== "done");
const active = open.filter((task) => ACTIVE.has(task.status));

// Branches: `+` means checked out in another worktree (pushed or not), `*` is this one.
const localBranches = new Map();
for (const line of run("git", ["branch", "--list"]).split(/\r?\n/)) {
  const match = /^([+* ]) (.+)$/.exec(line);
  if (match) localBranches.set(match[2].trim(), match[1]);
}
const remoteHeads = new Set(
  run("git", ["ls-remote", "--heads", "origin"], { optional: true })
    ?.split(/\r?\n/)
    .map((line) => line.split(/\s+/)[1]?.replace(/^refs\/heads\//, ""))
    .filter((name) => name && name !== "main") ?? [],
);
const worktrees = [];
{
  let current = null;
  for (const line of run("git", ["worktree", "list", "--porcelain"]).split(/\r?\n/)) {
    if (line.startsWith("worktree ")) current = { path: line.slice(9), branch: null, detached: false };
    else if (line.startsWith("branch ")) current.branch = line.slice(7).replace(/^refs\/heads\//, "");
    else if (line === "detached") current.detached = true;
    else if (line === "" && current) {
      worktrees.push(current);
      current = null;
    }
  }
  if (current) worktrees.push(current);
}

// Open pull requests, when gh is available.
const prsRaw = run("gh", ["pr", "list", "--state", "open", "--limit", "100", "--json", "number,title,headRefName,files"], { optional: true });
const prs = prsRaw ? JSON.parse(prsRaw) : null;
const prByBranch = new Map((prs ?? []).map((pr) => [pr.headRefName, pr]));

function whereIsBranch(name) {
  if (!name) return "no branch recorded";
  const marks = [];
  if (localBranches.get(name) === "+") marks.push("checked out in another worktree");
  if (localBranches.get(name) === "*") marks.push("checked out here");
  if (remoteHeads.has(name)) marks.push("on remote");
  if (prByBranch.has(name)) marks.push(`PR #${prByBranch.get(name).number}`);
  if (marks.length === 0) marks.push(localBranches.has(name) ? "local only, not pushed" : "not found anywhere");
  return marks.join(", ");
}

const report = { staleHours: STALE_CLAIM_HOURS, activeClaims: [], unlistedWork: [], scope: null };

for (const task of active) {
  const age = hoursSince(task.claimed_at, now);
  const locks = open
    .filter((other) => other.id !== task.id && !ACTIVE.has(other.status) && sharedScope(other, task).length > 0)
    .map((other) => other.id);
  report.activeClaims.push({
    id: task.id,
    status: task.status,
    owner: task.owner,
    ageHours: age,
    stale: isStale(task, new Date(now)),
    branch: task.branch || null,
    branchSeen: whereIsBranch(task.branch),
    locks,
  });
}

const namedBranches = new Set(tasks.map((task) => task.branch).filter(Boolean));
for (const [name, mark] of localBranches) {
  if (name === "main" || namedBranches.has(name) || mark !== "+") continue;
  report.unlistedWork.push({ kind: "worktree branch (+)", name, pr: prByBranch.get(name)?.number ?? null });
}
for (const name of remoteHeads) {
  if (namedBranches.has(name) || localBranches.get(name) === "+") continue;
  report.unlistedWork.push({ kind: "remote branch", name, pr: prByBranch.get(name)?.number ?? null });
}
for (const worktree of worktrees) {
  if (worktree.detached) report.unlistedWork.push({ kind: "DETACHED worktree (commits on no branch)", name: worktree.path, pr: null });
}

if (scopeArg) {
  const probe = { scope: [scopeArg] };
  report.scope = {
    path: scopeArg,
    activeTasks: active.filter((task) => sharedScope(task, probe).length > 0).map((task) => `${task.id} (${task.owner}, ${task.status})`),
    openPRs: (prs ?? [])
      .filter((pr) => (pr.files ?? []).some((file) => scopesOverlap(file.path, scopeArg)))
      .map((pr) => `#${pr.number} ${pr.headRefName}: ${pr.title}`),
    landedOnMain: run("git", ["log", "--oneline", "-5", "origin/main", "--", scopeArg], { optional: true }) || "",
  };
}

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`Active claims (${report.activeClaims.length}); stale after ${STALE_CLAIM_HOURS} h${prs ? "" : "; gh unavailable, PR columns skipped"}`);
  for (const claim of report.activeClaims) {
    const age = claim.ageHours === null ? "?" : `${claim.ageHours} h`;
    console.log(`  ${claim.stale ? "STALE " : "      "}${claim.id}  ${claim.status}  ${claim.owner}  ${age}  [${claim.branchSeen}]`);
    if (claim.locks.length) console.log(`        locks: ${claim.locks.join(", ")}`);
  }
  console.log(`Work not on the board (${report.unlistedWork.length})`);
  for (const item of report.unlistedWork) {
    console.log(`  ${item.kind}: ${item.name}${item.pr ? `  (PR #${item.pr})` : ""}`);
  }
  if (report.scope) {
    console.log(`Scope ${report.scope.path}`);
    console.log(`  active tasks: ${report.scope.activeTasks.join("; ") || "none"}`);
    console.log(`  open PRs touching it: ${report.scope.openPRs.join("; ") || "none"}`);
    console.log(`  last commits on origin/main:\n${report.scope.landedOnMain.replace(/^/gm, "    ") || "    none"}`);
  }
}
