#!/usr/bin/env node
// Keep open pull requests moving under strict branch protection, from GitHub Actions.
//
// `main` requires four checks and an up-to-date branch, so a green pull request that fell
// BEHIND waits until someone runs "update branch" and CI passes again. Merge queue would do
// this natively, but GitHub offers it only to organization-owned repositories, and this one
// belongs to a user account. Each pass of this script:
//
//   - merges the one pull request that is up to date with all four required checks green,
//     with --match-head-commit so a push that lands meanwhile is refused, not merged untested;
//   - enables GitHub auto-merge (squash) on every other eligible pull request that is not yet
//     mergeable, through the GraphQL mutation (never `gh pr merge --auto`, which merges a
//     pull request that happens to be mergeable at once);
//   - runs "update branch" on BEHIND pull requests, green ones first, while at most
//     MAX_INFLIGHT up-to-date pull requests have required checks running. A BEHIND pull
//     request's own run cannot lead to a merge, so it holds no slot;
//   - turns auto-merge off again on a pull request that became ineligible (label, draft).
//
// Eligible: targets the default branch; not a draft; a branch of this repository (never a
// fork: this repository is public, and a stranger's pull request must not merge on green
// CI); opened by an author in AUTO_MERGE_AUTHORS and not by a bot (Dependabot upgrades need a
// person: .agents/skills/dev-and-ci/references/dependabot.md); no `no-auto-merge` label; and
// auto-merge not switched off by hand on the pull request (someone decided to hold it).
// A red head or a conflict is left alone; GitHub shows it.
//
// The token must not be GITHUB_TOKEN: pull_request runs started by a GITHUB_TOKEN push wait
// for a maintainer to approve them, so an updated branch would sit without CI. See
// .github/BRANCH_PROTECTION.md, "Automatic updates and merges", for the token and settings.
//
// Usage: node tools/ci/auto-update-branches.mjs [--dry-run]
//   GH_TOKEN            the token gh uses; without it the script prints a notice and exits 0
//   GH_REPO             owner/name (set by the workflow)
//   MAX_INFLIGHT        up-to-date pull requests allowed to have required checks running (3)
//   AUTO_MERGE_AUTHORS  comma-separated logins whose pull requests are eligible (repo owner)
//   DEFAULT_BRANCH      the protected branch (main)
import { execFileSync } from "node:child_process";
import { appendFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

// Renaming a job in ci.yml renames its check: update this list and branch protection together.
export const REQUIRED = ["api", "web", "containers", "full-stack-smoke"];
export const REQUIRED_WORKFLOW = "CI";
export const OPT_OUT_LABEL = "no-auto-merge";
const MERGEABLE_STATES = new Set(["CLEAN", "HAS_HOOKS", "UNSTABLE"]);
const RUNNING_STATUSES = new Set(["QUEUED", "IN_PROGRESS", "WAITING", "PENDING", "REQUESTED"]);
const PASSING_CONCLUSIONS = new Set(["SUCCESS", "SKIPPED", "NEUTRAL"]);
const FIELDS = [
  "id", "number", "isDraft", "isCrossRepository", "author", "labels", "baseRefName",
  "headRefOid", "mergeStateStatus", "autoMergeRequest", "statusCheckRollup",
].join(",");

/**
 * The state of one required check on a pull request's head, the way branch protection sees
 * it: only CheckRun rows of the CI workflow, and per name the most recently started row.
 * Returns success | failed | running | missing (no row, or only a cancelled one: nothing is
 * coming unless the branch moves).
 */
export function checkVerdict(rollup, name, workflow = REQUIRED_WORKFLOW) {
  const rows = (rollup ?? []).filter(
    (row) => row.__typename === "CheckRun" && row.name === name && (row.workflowName ?? workflow) === workflow,
  );
  if (rows.length === 0) return "missing";
  const latest = rows.reduce((a, b) => (String(b.startedAt ?? "") > String(a.startedAt ?? "") ? b : a));
  const status = String(latest.status ?? "").toUpperCase();
  if (RUNNING_STATUSES.has(status)) return "running";
  const conclusion = String(latest.conclusion ?? "").toUpperCase();
  if (PASSING_CONCLUSIONS.has(conclusion)) return "success";
  if (conclusion === "CANCELLED" || conclusion === "" || conclusion === "STALE") return "missing";
  return "failed";
}

/** Why a pull request is not ours to touch, or null when it is eligible. */
export function ineligible(pr, { authors = [], defaultBranch = "main" } = {}) {
  if (pr.isCrossRepository) return "fork";
  if (pr.baseRefName && pr.baseRefName !== defaultBranch) return `base ${pr.baseRefName}`;
  const login = pr.author?.login ?? "";
  if (/dependabot/i.test(login)) return "dependabot";
  if (pr.author?.is_bot) return `bot ${login}`;
  if (authors.length && !authors.includes(login)) return `author ${login || "unknown"}`;
  if (pr.isDraft) return "draft";
  if ((pr.labels ?? []).some((label) => label.name === OPT_OUT_LABEL)) return `label ${OPT_OUT_LABEL}`;
  if (pr.autoMergeManuallyDisabled) return "auto-merge turned off by hand";
  return null;
}

/**
 * Decide one pass. Pure: the caller runs the actions.
 * Returns { merge: [..] (at most one), enableAuto, disableAuto, update, notes }, items being
 * { number, id, head }.
 */
export function plan(prs, { maxInflight = 3, required = REQUIRED, authors = [], defaultBranch = "main" } = {}) {
  const result = { merge: [], enableAuto: [], disableAuto: [], update: [], notes: [] };
  let inflight = 0;
  const greenBehind = [];
  const otherBehind = [];
  for (const pr of [...prs].sort((a, b) => a.number - b.number)) {
    const item = { number: pr.number, id: pr.id, head: pr.headRefOid };
    const reason = ineligible(pr, { authors, defaultBranch });
    if (reason) {
      // Only undo auto-merge where our own rules say "hold": a label or a draft. Forks, bots
      // and stacked pull requests are never given auto-merge by this script.
      if (pr.autoMergeRequest && (reason === "draft" || reason.startsWith("label "))) result.disableAuto.push(item);
      result.notes.push(`#${pr.number} skipped: ${reason}`);
      continue;
    }
    const verdicts = required.map((name) => checkVerdict(pr.statusCheckRollup, name));
    const failed = required.filter((_, i) => verdicts[i] === "failed");
    const running = verdicts.includes("running");
    const missing = required.filter((_, i) => verdicts[i] === "missing");
    const state = pr.mergeStateStatus;
    if (failed.length) {
      result.notes.push(`#${pr.number} red on ${String(pr.headRefOid).slice(0, 8)}: ${failed.join(", ")}`);
      continue;
    }
    if (state === "DIRTY") {
      result.notes.push(`#${pr.number} conflicts with ${defaultBranch}`);
      continue;
    }
    if (state === "BEHIND") {
      (running || missing.length ? otherBehind : greenBehind).push(item);
      if (!pr.autoMergeRequest) result.enableAuto.push(item);
      continue;
    }
    if (running) {
      inflight += 1;
      if (!pr.autoMergeRequest && !MERGEABLE_STATES.has(state)) result.enableAuto.push(item);
      continue;
    }
    if (missing.length) {
      result.notes.push(`#${pr.number} has no CI result for ${missing.join(", ")} on ${String(pr.headRefOid).slice(0, 8)}; push or re-run to get one`);
      continue;
    }
    if (MERGEABLE_STATES.has(state)) {
      if (result.merge.length === 0) result.merge.push(item);
      else result.notes.push(`#${pr.number} is ready too; it merges after main settles`);
      continue;
    }
    if (state === "UNKNOWN") result.notes.push(`#${pr.number} mergeability not computed yet`);
    if (!pr.autoMergeRequest && state === "BLOCKED") result.enableAuto.push(item);
  }
  // A merge moves main and makes every other branch BEHIND again: update on the next pass.
  if (result.merge.length === 0) {
    const slots = Math.max(0, maxInflight - inflight);
    const candidates = [...greenBehind, ...otherBehind];
    result.update = candidates.slice(0, slots);
    if (candidates.length > slots) {
      result.notes.push(`${candidates.length - slots} BEHIND pull request(s) wait: ${inflight} up to date and running, limit ${maxInflight}`);
    }
  }
  const merging = new Set(result.merge.map((m) => m.number));
  result.enableAuto = result.enableAuto.filter((item) => !merging.has(item.number));
  return result;
}

const ENABLE_AUTO_MERGE =
  "mutation($id: ID!, $oid: GitObjectID!) { enablePullRequestAutoMerge(input: {pullRequestId: $id, mergeMethod: SQUASH, expectedHeadOid: $oid}) { clientMutationId } }";

/** The gh argument lists a plan turns into, in the order they run. */
export function commands(actions) {
  const list = [];
  for (const { number, head } of actions.merge) {
    list.push({ label: `merged #${number} at ${String(head).slice(0, 8)}`, args: ["pr", "merge", String(number), "--squash", "--match-head-commit", head] });
  }
  for (const { number } of actions.disableAuto) {
    list.push({ label: `turned auto-merge off on #${number}`, args: ["pr", "merge", String(number), "--disable-auto"] });
  }
  for (const { number, id, head } of actions.enableAuto) {
    list.push({
      label: `enabled auto-merge on #${number}`,
      args: ["api", "graphql", "-f", `query=${ENABLE_AUTO_MERGE}`, "-f", `id=${id}`, "-f", `oid=${head}`],
    });
  }
  for (const { number, head } of actions.update) {
    list.push({ label: `updated #${number} from main (was ${String(head).slice(0, 8)})`, args: ["pr", "update-branch", String(number)] });
  }
  return list;
}

// When someone turned auto-merge off by hand, the last auto-merge event on the pull request is
// an AutoMergeDisabledEvent with reason code MANUALLY_DISABLED (older API: manually_disabled).
const OPT_OUT_QUERY = `query($owner: String!, $name: String!) { repository(owner: $owner, name: $name) {
  pullRequests(states: OPEN, first: 100) { nodes { number timelineItems(itemTypes: [AUTO_MERGE_ENABLED_EVENT, AUTO_MERGE_DISABLED_EVENT], last: 1) {
    nodes { __typename ... on AutoMergeDisabledEvent { reasonCode } } } } } } }`;

export function manuallyDisabled(graph) {
  const result = new Set();
  for (const node of graph?.data?.repository?.pullRequests?.nodes ?? []) {
    const last = node.timelineItems?.nodes?.at(-1);
    if (last?.__typename === "AutoMergeDisabledEvent" && /manual/i.test(String(last.reasonCode ?? ""))) result.add(node.number);
  }
  return result;
}

function report(line, env) {
  console.log(line);
  if (env.GITHUB_STEP_SUMMARY) appendFileSync(env.GITHUB_STEP_SUMMARY, `- ${line}\n`);
}

function defaultGh(args) {
  return execFileSync("gh", args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
}

export async function main(argv = process.argv.slice(2), { env = process.env, gh = defaultGh, sleep = (ms) => new Promise((r) => setTimeout(r, ms)) } = {}) {
  const dryRun = argv.includes("--dry-run");
  if (!env.GH_TOKEN) {
    report("AUTO_MERGE_TOKEN is not set; nothing to do (see .github/BRANCH_PROTECTION.md)", env);
    return 0;
  }
  const [owner, name] = String(env.GH_REPO ?? "").split("/");
  const parsed = Number.parseInt(env.MAX_INFLIGHT ?? "3", 10);
  const options = {
    maxInflight: Number.isFinite(parsed) && parsed >= 0 ? parsed : 3,
    authors: String(env.AUTO_MERGE_AUTHORS ?? owner ?? "").split(",").map((s) => s.trim()).filter(Boolean),
    defaultBranch: env.DEFAULT_BRANCH || "main",
  };
  let actions;
  for (let attempt = 0; ; attempt += 1) {
    const prs = JSON.parse(gh(["pr", "list", "--state", "open", "--limit", "100", "--json", FIELDS]));
    const held = owner && name ? manuallyDisabled(JSON.parse(gh(["api", "graphql", "-f", `query=${OPT_OUT_QUERY}`, "-f", `owner=${owner}`, "-f", `name=${name}`]))) : new Set();
    for (const pr of prs) pr.autoMergeManuallyDisabled = held.has(pr.number);
    actions = plan(prs, options);
    // Right after main moves GitHub has not recomputed mergeability yet: look again shortly
    // rather than let the pass that matters most do nothing.
    const unknown = prs.some((pr) => pr.mergeStateStatus === "UNKNOWN" && !ineligible(pr, options));
    if (!unknown || actions.merge.length || attempt >= 3) break;
    await sleep(10_000);
  }
  for (const note of actions.notes) report(note, env);
  const list = commands(actions);
  for (const { label, args } of list) {
    if (dryRun) {
      report(`[dry-run] ${label}: gh ${args.map((a) => (a.startsWith("query=") ? "query=<mutation>" : a)).join(" ")}`, env);
      continue;
    }
    try {
      gh(args);
      report(label, env);
    } catch (error) {
      report(`${label} refused: ${String(error.stderr || error.message).trim().split("\n")[0]}`, env);
    }
  }
  if (!list.length) report("nothing to merge or update this pass", env);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().then((code) => process.exit(code), (error) => {
    console.error(error);
    process.exit(1);
  });
}
