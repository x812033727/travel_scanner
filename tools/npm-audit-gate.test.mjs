import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { allowProblems, findings, verdict } from "./npm-audit-gate.mjs";

const read = (file) => readFileSync(new URL(`../${file}`, import.meta.url), "utf8");
const via = (ghsa, severity = "high") => ({ source: 1, title: "a flaw", url: `https://github.com/advisories/${ghsa}`, severity });
// The shape npm reports for one advisory carried up a chain: only `braces` names the advisory.
const report = (extra = {}) => ({
  vulnerabilities: {
    braces: { severity: "high", via: [via("GHSA-vfj7-8cjw-p6xm")] },
    micromatch: { severity: "high", via: ["braces"] },
    "fast-glob": { severity: "high", via: ["micromatch"] },
    ...extra,
  },
});
const allow = (review_by = "2026-11-04") => [{ advisory: "GHSA-vfj7-8cjw-p6xm", package: "braces", reason: "no patched release exists and the chain is lint-time only", review_by }];

test("a chain of dependents is one finding, the advisory itself", () => {
  assert.deepEqual(findings(report()).map((finding) => `${finding.package} ${finding.advisory}`), ["braces GHSA-vfj7-8cjw-p6xm"]);
  assert.equal(findings(report({ lodash: { severity: "moderate", via: [via("GHSA-2222-3333-4444", "moderate")] } })).length, 1, "below high does not block");
});

test("an exempted advisory passes until its review date, and nothing else rides along", () => {
  assert.equal(verdict(report(), allow(), "2026-10-04").ok, true);
  assert.equal(verdict(report(), allow(), "2026-11-04").ok, true, "the review date itself still counts");
  const late = verdict(report(), allow(), "2026-11-05");
  assert.equal(late.ok, false);
  assert.equal(late.expired.length, 1);
  const other = verdict(report({ tar: { severity: "critical", via: [via("GHSA-2222-3333-4444", "critical")] } }), allow(), "2026-10-04");
  assert.equal(other.ok, false);
  assert.deepEqual(other.blocking.map((finding) => finding.package), ["tar"]);
  // The same advisory in another package is a different finding.
  assert.equal(verdict({ vulnerabilities: { other: { via: [via("GHSA-vfj7-8cjw-p6xm")] } } }, allow(), "2026-10-04").ok, false);
});

test("an exemption nothing needs is reported, not fatal; a report that is not one is fatal", () => {
  const clean = verdict({ vulnerabilities: {} }, allow(), "2026-10-04");
  assert.equal(clean.ok, true);
  assert.equal(clean.unused.length, 1);
  assert.throws(() => verdict({ error: { code: "ENOTFOUND", summary: "registry down" } }, allow(), "2026-10-04"), /no report: registry down/);
});

test("an exemption has to say which advisory, which package, why, and until when", () => {
  assert.deepEqual(allowProblems(allow()), []);
  assert.equal(allowProblems([{ advisory: "braces", package: "", reason: "because", review_by: "soon" }]).length, 4);
  assert.equal(verdict(report(), [{}], "2026-10-04").ok, false);
});

test("the shipped allow list is well formed and the daily workflow runs the gate", () => {
  assert.deepEqual(allowProblems(JSON.parse(read("tools/npm-audit-allow.json"))), []);
  const workflow = read(".github/workflows/npm-audit.yml");
  assert.match(workflow, /npm audit --omit=dev --audit-level=high/, "what ships to production takes no exemption");
  assert.match(workflow, /node tools\/npm-audit-gate\.mjs/);
});
