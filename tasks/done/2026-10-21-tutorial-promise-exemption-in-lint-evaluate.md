---
id: 2026-10-21-tutorial-promise-exemption-in-lint-evaluate
title: Tutorial promise exemption in lint: evaluate TOC patterns on the opening minus the promise sentence; anchor PROMISE_VERB
status: done
priority: P3
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:24:26Z
created_at: 2026-10-21T14:40:00Z
completed_at: 2026-10-24T13:24:50Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Tutorial promise exemption in lint: evaluate TOC patterns on the opening minus the promise sentence; anchor PROMISE_VERB

## Why

PR #1643 let a tutorial's opening carry one promise sentence (teaching-flow.md §一) by skipping
the table-of-contents warning in `episodeScriptProblems` when `doc.category === "tutorial"`, a
`PROMISE_VERB` matches anywhere in the first 60 s, there is no ordinal run and no `SECTION_WORD`.
A code review of the PR (2026-10-21) found two leaks:

1. The flag suppresses the whole check, so a tutorial opening 「這集講 A、B，還有 C。看完你會學會
   四件事」 raises no warning although the list announcement is not the promise sentence.
2. `PROMISE_VERB`'s `能(?:用|做|寫|自己)` matches inside 可能用／不能用／可能做, so an opening with no
   promise can still be exempted.

Both files are bound by the duration receipt (`docs/videos/long-form/review.json`), so the fix
needs its own independent increment; that is why it was not folded into the review's other fixes
(`core/narrative.mjs`, unbound).

## Definition of done

- [x] The TOC patterns (`OPENING_TOC`, `announcesList`, the ordinal runs) are evaluated on the opening
      with the one promise sentence removed (the first sentence matching `PROMISE_VERB`), so a list
      announcement beside the promise still warns.
- [x] `PROMISE_VERB` does not match 可能用／不能用／可能做 (`(?<![可不])能…` or a deliverable noun).
- [x] `lint.test.mjs` covers both: the two tutorial promises still pass, the mixed opening warns,
      the 可能用 opening warns.

## Steps

- [x] Split the opening on sentence ends, find the promise sentence, lint the rest.
- [x] Anchor the verb.
- [ ] Tests; then an independent reviewer records the increment in review.md / review.json.

## How to verify

`node --test tools/video/core/lint.test.mjs`; `node tools/video/long-form/cli.mjs check` after the
re-binding.

## Notes

- 2026-10-24: Only one eligible promise sentence is omitted from a tutorial's TOC
  warning input. Section labels and complete ordinal runs retain their warnings;
  another list announcement is still checked. The ability verb excludes a preceding
  可 or 不, so 可能用／不能用／可能做 do not exempt the surrounding list.
- The new mixed-opening regression failed on old source. Complete lint tests
  passed 52/52, zero skips, on bundled Node 24.19.0, including both original
  accepted promises and all existing non-tutorial opening checks.
  The independent duration-receipt increment is left to the coordinator/reviewer.

Found by the review that gated the merge of PR #1643; the other three findings (global panel hash
invalidating saved story verdicts, PROGRESS_CARRIER accepting a bare question mark, no test on the
tutorial question keys) were fixed in that PR.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- - [ ] The TOC patterns (`OPENING_TOC`, `announcesList`, the ordinal runs) are evaluated on the opening
- - [ ] `PROMISE_VERB` does not match 可能用／不能用／可能做 (`(?<![可不])能…` or a deliverable noun).
- 2026-10-24 execution: TOC exception subtracts exactly one real promised-result sentence, negative modal cannot match;52 lint tests passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
