import assert from "node:assert/strict";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { checkVerdict, commands, ineligible, main, manuallyDisabled, plan, REQUIRED } from "./ci/auto-update-branches.mjs";

const run = (name, status, conclusion = "", startedAt = "2026-09-26T10:00:00Z", workflowName = "CI") => ({
  __typename: "CheckRun", name, status, conclusion, startedAt, workflowName,
});
const allGreen = () => REQUIRED.map((name) => run(name, "COMPLETED", "SUCCESS"));
const head = (number) => `${String(number).padStart(4, "0")}${"a".repeat(36)}`;
const pr = (number, overrides = {}) => ({
  id: `PR_${number}`,
  number,
  isDraft: false,
  isCrossRepository: false,
  author: { login: "owner", is_bot: false },
  labels: [],
  baseRefName: "main",
  headRefOid: head(number),
  mergeStateStatus: "BEHIND",
  autoMergeRequest: { enabledAt: "2026-09-26T00:00:00Z" },
  statusCheckRollup: allGreen(),
  ...overrides,
});
const opts = { authors: ["owner"], maxInflight: 3 };
const numbers = (list) => list.map((item) => item.number);

test("checkVerdict reads the latest CI row per name, the way branch protection does", () => {
  const older = run("api", "COMPLETED", "SUCCESS", "2026-09-26T09:00:00Z");
  const newer = run("api", "COMPLETED", "FAILURE", "2026-09-26T09:30:00Z");
  assert.equal(checkVerdict([older, newer], "api"), "failed", "a newer failure is not hidden by an older success");
  assert.equal(checkVerdict([run("api", "COMPLETED", "SKIPPED")], "api"), "success");
  assert.equal(checkVerdict([run("api", "COMPLETED", "NEUTRAL")], "api"), "success");
  assert.equal(checkVerdict([run("api", "COMPLETED", "TIMED_OUT")], "api"), "failed");
  for (const status of ["QUEUED", "IN_PROGRESS", "WAITING", "PENDING", "REQUESTED"]) {
    assert.equal(checkVerdict([run("web", status)], "web"), "running", status);
  }
  assert.equal(checkVerdict([run("web", "COMPLETED", "CANCELLED")], "web"), "missing", "nothing is coming after a cancel");
  assert.equal(checkVerdict([], "web"), "missing");
});

test("checkVerdict ignores commit statuses and other workflows' checks with the same name", () => {
  const ciFailed = run("api", "COMPLETED", "FAILURE");
  const status = { __typename: "StatusContext", context: "api", state: "SUCCESS" };
  const other = run("api", "COMPLETED", "SUCCESS", "2026-09-26T11:00:00Z", "Other");
  assert.equal(checkVerdict([ciFailed, status, other], "api"), "failed");
});

test("only branches of this repository, targeting main, opened by an allowed person, are eligible", () => {
  const cases = [
    [pr(1, { isCrossRepository: true }), "fork"],
    [pr(2, { baseRefName: "claude/feature" }), "base claude/feature"],
    [pr(3, { author: { login: "app/dependabot", is_bot: true } }), "dependabot"],
    [pr(4, { author: { login: "app/renovate", is_bot: true } }), "bot app/renovate"],
    [pr(5, { author: { login: "app/github-actions", is_bot: true } }), "bot app/github-actions"],
    [pr(6, { author: { login: "someone", is_bot: false } }), "author someone"],
    [pr(7, { isDraft: true }), "draft"],
    [pr(8, { labels: [{ name: "no-auto-merge" }] }), "label no-auto-merge"],
    [pr(9, { autoMergeManuallyDisabled: true }), "auto-merge turned off by hand"],
    [pr(10), null],
  ];
  for (const [item, reason] of cases) assert.equal(ineligible(item, opts), reason, `#${item.number}`);
  // Ineligible and otherwise ready to merge: nothing happens to any of them.
  const ready = cases.slice(0, -1).map(([item]) => ({ ...item, mergeStateStatus: "CLEAN", autoMergeRequest: null }));
  const actions = plan(ready, opts);
  assert.deepEqual([actions.merge, actions.enableAuto, actions.update, actions.disableAuto], [[], [], [], []]);
});

test("a label or a draft turns auto-merge off again; a stacked or bot pull request is left as it is", () => {
  const actions = plan([
    pr(20, { labels: [{ name: "no-auto-merge" }] }),
    pr(21, { isDraft: true }),
    pr(22, { baseRefName: "claude/feature" }),
    pr(23, { author: { login: "app/renovate", is_bot: true } }),
  ], opts);
  assert.deepEqual(numbers(actions.disableAuto), [20, 21]);
});

test("the one up-to-date green pull request is merged at its head; updates wait for the next pass", () => {
  for (const state of ["CLEAN", "HAS_HOOKS", "UNSTABLE"]) {
    const actions = plan([pr(30, { mergeStateStatus: state }), pr(31, { mergeStateStatus: "CLEAN", autoMergeRequest: null }), pr(32)], opts);
    assert.deepEqual(actions.merge, [{ number: 30, id: "PR_30", head: head(30) }], state);
    assert.deepEqual(actions.update, []);
    assert.deepEqual(numbers(actions.enableAuto), [], "a mergeable #31 is neither merged twice nor given auto-merge");
  }
});

test("BEHIND pull requests are updated green first, and only up-to-date running ones hold a slot", () => {
  const runningUpToDate = (n) => pr(n, { mergeStateStatus: "BLOCKED", statusCheckRollup: [run("api", "IN_PROGRESS")] });
  const runningBehind = (n) => pr(n, { statusCheckRollup: [run("api", "IN_PROGRESS")] });
  const actions = plan([runningBehind(40), pr(45), runningUpToDate(50), pr(42), runningBehind(41)], opts);
  assert.deepEqual(numbers(actions.update), [42, 45], "two slots: the green ones go first");
  assert.ok(actions.notes.some((note) => note.includes("2 BEHIND pull request(s) wait: 1 up to date and running")));
});

test("pull requests with no CI result on their head take no slot and say so", () => {
  const stalled = (n) => pr(n, { mergeStateStatus: "BLOCKED", statusCheckRollup: [run("api", "COMPLETED", "CANCELLED")] });
  const actions = plan([stalled(60), stalled(61), stalled(62), pr(63)], opts);
  assert.deepEqual(numbers(actions.update), [63]);
  assert.ok(actions.notes.some((note) => note.startsWith("#60 has no CI result")));
});

test("nothing is updated while three up-to-date pull requests are running", () => {
  const running = (n) => pr(n, { mergeStateStatus: "BLOCKED", statusCheckRollup: [run("web", "QUEUED")] });
  assert.deepEqual(plan([running(1), running(2), running(3), pr(4)], opts).update, []);
});

test("a red or conflicting pull request is left alone and gets no auto-merge", () => {
  const red = pr(70, { autoMergeRequest: null, statusCheckRollup: [...allGreen().slice(1), run("api", "COMPLETED", "FAILURE")] });
  const redRunning = pr(71, { autoMergeRequest: null, mergeStateStatus: "BLOCKED", statusCheckRollup: [run("api", "COMPLETED", "FAILURE"), run("web", "IN_PROGRESS")] });
  const dirty = pr(72, { autoMergeRequest: null, mergeStateStatus: "DIRTY" });
  const actions = plan([red, redRunning, dirty, pr(73)], opts);
  assert.deepEqual([actions.merge, actions.enableAuto], [[], []]);
  assert.deepEqual(numbers(actions.update), [73], "a red pull request whose other jobs still run holds no slot");
  assert.ok(actions.notes.some((note) => note.startsWith("#70 red")));
  assert.ok(actions.notes.some((note) => note.startsWith("#72 conflicts")));
});

test("auto-merge is enabled on eligible pull requests that cannot merge yet", () => {
  const actions = plan([
    pr(80, { mergeStateStatus: "BLOCKED", autoMergeRequest: null, statusCheckRollup: [run("api", "IN_PROGRESS")] }),
    pr(81, { autoMergeRequest: null }),
    pr(82, { mergeStateStatus: "UNKNOWN", autoMergeRequest: null }),
  ], opts);
  assert.deepEqual(numbers(actions.enableAuto), [80, 81], "not while mergeability is unknown");
  assert.ok(actions.notes.some((note) => note.startsWith("#82 mergeability not computed")));
});

test("commands pin the head: merge and auto-merge refuse a newer push", () => {
  const list = commands({
    merge: [{ number: 1, id: "PR_1", head: "abc" }],
    disableAuto: [{ number: 2, id: "PR_2", head: "def" }],
    enableAuto: [{ number: 3, id: "PR_3", head: "123" }],
    update: [{ number: 4, id: "PR_4", head: "456" }],
  });
  assert.deepEqual(list[0].args, ["pr", "merge", "1", "--squash", "--match-head-commit", "abc"]);
  assert.deepEqual(list[1].args, ["pr", "merge", "2", "--disable-auto"]);
  assert.equal(list[2].args[0], "api");
  assert.ok(list[2].args.includes("id=PR_3") && list[2].args.includes("oid=123"));
  assert.match(list[2].args.find((a) => a.startsWith("query=")), /enablePullRequestAutoMerge.*mergeMethod: SQUASH.*expectedHeadOid/);
  assert.ok(!list.some(({ args }) => args.includes("--auto")), "never `gh pr merge --auto`: it merges a mergeable PR at once");
  assert.deepEqual(list[3].args, ["pr", "update-branch", "4"]);
});

test("a manual auto-merge switch-off is read from the timeline", () => {
  const graph = { data: { repository: { pullRequests: { nodes: [
    { number: 1, timelineItems: { nodes: [{ __typename: "AutoMergeDisabledEvent", reasonCode: "MANUALLY_DISABLED" }] } },
    { number: 2, timelineItems: { nodes: [{ __typename: "AutoMergeDisabledEvent", reasonCode: "BASE_BRANCH_CHANGED" }] } },
    { number: 3, timelineItems: { nodes: [{ __typename: "AutoMergeEnabledEvent" }] } },
    { number: 4, timelineItems: { nodes: [] } },
  ] } } } };
  assert.deepEqual([...manuallyDisabled(graph)], [1]);
});

test("without the token a pass does nothing, says why, and exits 0", async () => {
  const summary = join(mkdtempSync(join(tmpdir(), "auto-update-")), "summary.md");
  let called = false;
  const code = await main([], { env: { GITHUB_STEP_SUMMARY: summary }, gh: () => { called = true; return "[]"; } });
  assert.equal(code, 0);
  assert.equal(called, false);
  assert.match(readFileSync(summary, "utf8"), /AUTO_MERGE_TOKEN is not set/);
});

test("a dry run lists the commands without running any write", async () => {
  const calls = [];
  const gh = (args) => {
    calls.push(args);
    if (args[0] === "pr" && args[1] === "list") return JSON.stringify([pr(90, { mergeStateStatus: "CLEAN" })]);
    if (args[0] === "api") return JSON.stringify({ data: { repository: { pullRequests: { nodes: [] } } } });
    throw new Error(`unexpected write: ${args.join(" ")}`);
  };
  const code = await main(["--dry-run"], { env: { GH_TOKEN: "x", GH_REPO: "owner/repo" }, gh, sleep: async () => {} });
  assert.equal(code, 0);
  assert.deepEqual(calls.map((args) => args.slice(0, 2).join(" ")), ["pr list", "api graphql"]);
});

test("mergeability still unknown right after main moved is read again before deciding", async () => {
  let lists = 0;
  const gh = (args) => {
    if (args[0] === "pr" && args[1] === "list") {
      lists += 1;
      return JSON.stringify([pr(95, { mergeStateStatus: lists < 3 ? "UNKNOWN" : "CLEAN" })]);
    }
    if (args[0] === "api") return JSON.stringify({ data: { repository: { pullRequests: { nodes: [] } } } });
    return "";
  };
  const writes = [];
  await main([], { env: { GH_TOKEN: "x", GH_REPO: "owner/repo" }, gh: (args) => { if (args[1] === "merge") writes.push(args); return gh(args); }, sleep: async () => {} });
  assert.equal(lists, 3);
  assert.deepEqual(writes, [["pr", "merge", "95", "--squash", "--match-head-commit", head(95)]]);
});
