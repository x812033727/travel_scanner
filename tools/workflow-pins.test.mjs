/**
 * Every GitHub Action this repository runs is pinned to a commit SHA.
 *
 * A tag is a pointer its owner can move, so `@v4` is whatever `v4` resolved to on the
 * morning a job happened to run — with the repository checked out and, in the two live
 * validation workflows, with provider API keys in the environment. The CI runner is also on
 * the path to production: `deployment_agent/executor.py` will not deploy unless CI is green,
 * and `.github/BRANCH_PROTECTION.md` makes those same jobs required to merge.
 *
 * This is a test rather than a convention because the failure is silent. An unpinned action
 * looks exactly like a pinned one in review, and nothing about it goes wrong until the day
 * it does.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const WORKFLOWS = fileURLToPath(new URL("../.github/workflows/", import.meta.url));
const USES = /^\s*-?\s*uses:\s*(\S+)/gm;

function actionReferences() {
  return readdirSync(WORKFLOWS)
    .filter((name) => name.endsWith(".yml") || name.endsWith(".yaml"))
    .flatMap((name) => {
      const source = readFileSync(join(WORKFLOWS, name), "utf8");
      return [...source.matchAll(USES)].map((match) => ({ workflow: name, reference: match[1] }));
    });
}

test("every action is pinned to a full commit SHA", () => {
  const references = actionReferences();
  // A guard that finds nothing passes forever. Workflows exist; if this is zero the pattern
  // above stopped matching, not the repository stopped using actions.
  assert.ok(references.length > 0, "no `uses:` found — the scan itself is broken");
  const floating = references.filter(({ reference }) => !/@[0-9a-f]{40}$/.test(reference));
  assert.deepEqual(
    floating.map(({ workflow, reference }) => `${workflow}: ${reference}`),
    [],
    "pin these to a commit SHA, with the version as a trailing comment",
  );
});

test("each pin records which version it is, so a reader is not left with a bare SHA", () => {
  const missing = [];
  for (const name of readdirSync(WORKFLOWS).filter((file) => file.endsWith(".yml"))) {
    const source = readFileSync(join(WORKFLOWS, name), "utf8");
    for (const line of source.split("\n")) {
      if (!/^\s*-?\s*uses:/.test(line)) continue;
      // Dependabot rewrites the SHA and this comment together, which is what keeps the two
      // from drifting apart.
      if (!/#\s*v?\d+\.\d+/.test(line)) missing.push(`${name}: ${line.trim()}`);
    }
  }
  assert.deepEqual(missing, []);
});

test("the same action is the same SHA everywhere", () => {
  const byAction = new Map();
  for (const { workflow, reference } of actionReferences()) {
    const [action, sha] = reference.split("@");
    if (!byAction.has(action)) byAction.set(action, new Map());
    byAction.get(action).set(sha, [...(byAction.get(action).get(sha) ?? []), workflow]);
  }
  const split = [...byAction.entries()]
    .filter(([, shas]) => shas.size > 1)
    .map(([action, shas]) => `${action}: ${[...shas.keys()].join(", ")}`);
  // Two versions of one action across workflows is how a bump gets half-applied and the
  // half nobody looked at keeps running the old code.
  assert.deepEqual(split, []);
});
