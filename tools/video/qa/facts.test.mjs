import assert from "node:assert/strict";
import test from "node:test";

import { citedClaims, factsChecks, lastVerifyReport, normalizeClaimId, notFoundClaims } from "./facts.mjs";

const ASCII = `# verify-2: slug

## Claim table

| # | claim | where | URL | HTTP | verdict | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | The price is NT$270 | hook k7p2 | https://openai.com/a | 200 | CONFIRMED | - |
| c7 | Launched in May | event-two 4bzz | https://openai.com/b | 200 | NOT FOUND | dropped the month |
| 12 | Three companies | event-two imav | - | - | NOT FOUND（已改寫） | 「三家」→「幾家」 |
| 13 | Not found on the page but true | outro | - | - | CHANGED | - |

## Summary

- Claims checked: 4. Confirmed: 1. Changed: 1. Not found: 2 (NOT FOUND rows above).
`;

const FULL_WIDTH = `＃ ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after
c3 ｜ 每月 100 次 ｜ limits x9fe ｜ https://x ｜ NOT FOUND ｜ 刪掉數字
c4 ｜ 每月 100 次 ｜ limits x9fe ｜ https://x ｜ CONFIRMED ｜ -
`;

test("the last round is the highest-numbered verify file", () => {
  assert.deepEqual(lastVerifyReport(["verify-1.md", "brief.md", "verify-10.md", "verify-2.md"]), { name: "verify-10.md", round: 10 });
  assert.equal(lastVerifyReport(["brief.md", "verify.md"]), null);
});

test("NOT FOUND rows are read from ASCII and full-width tables, ids compared without their prefix", () => {
  assert.deepEqual(notFoundClaims(ASCII).map((row) => row.id), ["7", "12"]);
  assert.deepEqual(notFoundClaims(FULL_WIDTH).map((row) => row.id), ["3"]);
  assert.deepEqual(["c12", "#12", "12", "C12", "`c12`", "c2b"].map(normalizeClaimId), ["12", "12", "12", "12", "12", "2b"]);
  assert.deepEqual(notFoundClaims("Not found: 0. | nothing | here |"), [], "a line with bars but no NOT FOUND cell is not a row");
});

test("the facts item passes when no scene cites a dropped claim, and names the scene when one does", () => {
  const doc = { scenes: [{ id: "hook", claims: ["c1"] }, { id: "event-two", claims: ["c7", "c8"] }, { id: "outro" }] };
  assert.deepEqual([...citedClaims(doc).keys()], ["1", "7", "8"]);
  const still = factsChecks({ report: { name: "verify-2.md", markdown: ASCII }, doc });
  assert.equal(still.ok, false);
  assert.equal(still.detail, "claim 7 was NOT FOUND in verify-2.md but event-two still cites it");
  const clean = factsChecks({ report: { name: "verify-2.md", markdown: ASCII }, doc: { scenes: [{ id: "hook", claims: ["c1"] }] } });
  assert.equal(clean.ok, true);
  assert.equal(clean.detail, "verify-2.md marks 2 claims NOT FOUND (7, 12); no scene cites them");
  const none = factsChecks({ report: { name: "verify-1.md", markdown: "| 1 | x | y | z | CONFIRMED |" }, doc });
  assert.deepEqual(none, { ok: true, detail: "verify-1.md marks no claim NOT FOUND" });
  assert.match(factsChecks({ report: null, doc }).detail, /has not been fact-checked/);
});
