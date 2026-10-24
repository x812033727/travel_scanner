---
id: 2026-10-11-qa-facts-matches-row-numbers-as
title: QA facts: a verify report's row numbers are matched against claim ids
status: done
priority: P3
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:22:26Z
created_at: 2026-10-11T04:04:00Z
completed_at: 2026-10-24T13:22:49Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/qa/facts.mjs
  - tools/video/qa/facts.test.mjs
---

# QA facts: a verify report's row numbers are matched against claim ids

## Why

The QA `facts` item (`tools/video/qa/facts.mjs`) reads the fact-checker's
`docs/videos/<slug>/verify-<round>.md`, takes every table row whose verdict is NOT FOUND, and
fails if a scene still cites that claim. It takes the row's **first cell** as the claim id
(`notFoundClaims`: `normalizeClaimId(cells[0])`, which strips a leading `c`), and compares it
with the ids the scenes list in `claims` (the c-numbers of `claims.md`). But a verify report
numbers its rows 1, 2, 3 in the order the checker went through the script; they are not claim
ids. On 2026-10-10 row 19 of `docs/videos/sothatswhy-b26/verify-1.md` (a detail in a card's
source line, NOT FOUND and already removed) was read as claim `c19`, an unrelated and confirmed
claim, and the item reported five scenes still citing a dropped claim. It was worked around by
rewording that row's verdict cell in the report.

## Definition of done

- [x] The check matches a report's rows against claim ids only when the rows are claim ids
      (for example the first cell is `c<number>`, or the table's header names a claim column),
      and otherwise does not treat a bare row number as one; **or** the verifier prompt tells
      the checker to number rows by claim id and to put a row with no claim under a non-numeric
      label, and the check refuses a report that does not.
- [x] A test with a report shaped like `sothatswhy-b26/verify-1.md`: row 19 NOT FOUND, scenes
      citing `c19`, no failure; and the existing true positive (a NOT FOUND claim id still
      cited) still fails.
- [x] Reports already in the repository give the same verdict as before, except the false one.

## Steps

- [x] Read how the three report shapes in `docs/videos/*/verify-*.md` label their first column
      before choosing.
- [ ] If the prompt route is chosen, widen the scope to the prompt file and its test.

## How to verify

`node --test tools/video/qa/facts.test.mjs`; `node tools/video/cli.mjs qa --slug sothatswhy-b26`
with the original wording of row 19 restored in a copy passes `facts`.

## Notes

- 2026-10-24: Only a self-identifying c-number or an explicit claim-id column is matched
  to scene claims. Generic `#` row ordinals are ignored. Explicit ids and numeric ids
  in labelled columns still refuse a scene citing NOT FOUND; column mappings reset
  between tables and data cells named `result` are not mistaken for headers.
- Added B26-shaped false-positive/true-positive and nonfirst claim-column regressions;
  both failed on the old implementation. Complete facts and QA tests passed 23/23,
  zero skips, using bundled Node 24.19.0 and fake services.
- Compared all 190 tracked verify reports against their video projects. Every latest
  report kept the same pass/fail verdict. Two historical, nonlatest reports also had
  demonstrably false ordinal matches: `always-on-agent-explained/verify-1.md` row 6
  checks a description claim explicitly labelled c3, while old QA matched c6 in the
  price-result scene; `openai-devday-2026-recap/verify-1.md` explicitly numbers 399
  video/Shorts strings, and its rows 3/18/19 concern quote marks and source-page dates,
  not the unrelated c3/c18/c19 cited by scenes. Their old false failures now pass.
  All report bytes are retained. This is parser reconciliation, not new fact approval.
- Full per-report comparison is retained outside Git as
  `qa-facts-repository-comparison-20261024.json` in the operator's temporary directory;
  focused red/green logs are `qa-facts-red-20261024.log` and `qa-facts-green-20261024.log`.

- 2026-10-11 filed from ticket `2026-10-10-sothatswhy-minimax-images` (its Notes, item 3 of
  what B26 taught).


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- - [ ] The check matches a report's rows against claim ids only when the rows are claim ids
- - [ ] A test with a report shaped like `sothatswhy-b26/verify-1.md`: row 19 NOT FOUND, scenes
- 2026-10-24 execution: Bare ordinal rows no longer treated as claim IDs;23 QA tests and190 historical report comparisons,latest verdicts unchanged. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
