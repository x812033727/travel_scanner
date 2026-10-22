---
id: 2026-10-22-repair-c12-pyrex-blind-narration-a
title: Repair C12 Pyrex blind narration A findings
status: review
priority: P1
area: docs
owner: codex-c12-script-repair
claimed_at: 2026-10-22T15:36:13Z
created_at: 2026-10-22T15:36:03Z
completed_at:
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/script.md
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.md
  - docs/videos/story-everyday-pyrex-c12-script/author-blind-a-repair.md
  - docs/videos/story-everyday-pyrex-c12-script/reviews/blind-narration-v2-a-b-holds.md
---

# Repair C12 Pyrex blind narration A findings

## Why

Independent blind narration read A placed the 80-line C12 draft at HOLD (script SHA-256 `491AEE730835B0FFC6AC034E544AF25BB257C0CAD354BF0FC845DB8376411036`). It found an early final-chapter reveal, repeated obstacles, a weak run of modern examples, process language, and a next-video mention. The source and visual receipts covered the old bytes, so the author needs a narrow revision with a new hash and an explicit handoff.

## Definition of done

- [x] Revise only the needed script and visual-plan rows, keeping 80 ordered IDs and 67 illustration / 13 card direction with a maximum run of 2 cards.
- [x] Leave an author-only SHA and changed-ID receipt that routes the new bytes to independent review without self-approval.
- [x] Run local structure and repository checks; push this narrow revision to draft PR #1692. The full repository checks have external/long-running limits recorded below.

## Steps

- [x] Read AGENTS, brand-story, youtube-video story and script-writing rules, the source matrix, and the blind A HOLD.
- [x] Reopen applicable primary pages and revise the repeated beats, final comparison, oral clarity, and ending.
- [x] Adjust only visual rows whose scene or card meaning moved.
- [x] Verify hashes, IDs, scene types, and diff; run task format and video-doc checks, recording the limits below.
- [x] Commit and push only `script.md`, `visual-plan.md`, `author-blind-a-repair.md`, and this task file (`4255699c0`); this follow-up only marks the task ready for review.

## How to verify

Compare `git show HEAD:<file>` with working files by ID; compute `Get-FileHash` SHA-256 for both; parse 80 unique ordered IDs and visual `I`/`C` types; run `git diff --check`, `npm run check:tasks`, and `npm run test:docs-videos`. Confirm the draft PR's new head after push. Old review receipts may be used as routing evidence only.

## Notes

Author revision changes 34 narration IDs and 8 visual IDs, listed in `docs/videos/story-everyday-pyrex-c12-script/author-blind-a-repair.md`. S3 live FAQ timed out in this pass; N01 did not expand the historical claim. Independent source/visual recheck, two new-hash blind reads, pronunciation, owner script review, measured audio duration, images, cost, and publication stay as separate gates. Other agents' untracked review-task files in this shared worktree are outside this task and must not be staged. `npm run check:tasks` currently fails because those two open copies duplicate tracked done tasks; the coordinator was notified, and this task must not delete them. `git diff --cached --check` and the targeted parser passed: 80 ordered unique IDs, 67 I / 13 C, max card run 2, and the receipt hashes match. `npm run test:docs-videos` ran for several minutes through unrelated language/caption tests, all output seen was passing; it was stopped while still running on coordinator instruction, so this is not a full-suite PASS. No paid calls were made.

2026-10-23 follow-up under this already claimed author task: independent source/visual v2 receipt at `99ea2632c` kept the unchanged 34 narration differences at PASS and held visual O09 only. Repair scope is one O09 visual row plus the SHA-bound author receipt and this task note; `script.md` remains byte-identical. New visual SHA-256 `EA563A3EFFF9182EC73C3844E3DB7A413143879A6A13E7A6708D77C5CBCC7CAA`. Independent review of the new visual bytes remains pending; no author self-approval. Other agents' untracked ghost tickets remain untouched. Targeted comparison PASS: script bytes unchanged; 80 ordered unique IDs; only visual O09 changed; 67 I / 13 C, max card run 2; both SHA values match the author receipt. `git diff --check` passed. The known `npm run check:tasks` duplicate-ID failure and incomplete broad docs-video suite are not represented as passing.

## 2026-10-23 fresh blind A/B follow-up

- [x] Record both independent narration-only HOLDs under their exact reviewer aliases in `reviews/blind-narration-v2-a-b-holds.md`, bound to old `script.md` SHA-256 `87D9B4BB3E09890C526F291DBAFB1F491201E372FDB2C0826F2418829555DF2B` and verified 80-line extract SHA-256 `49B85085F6B740B100B2E3977E452A605A0BE5D2DBB0B59826E76C421C904277`.
- [x] Repair only 18 narration IDs and 9 matching visual IDs; record new `script.md` SHA-256 `C030DC97CFF150D222828F56847F3D26FE63E88C97535F1755EE086BFD2CC0CF` and `visual-plan.md` SHA-256 `A90DCE6626EF7A13816E47AE9A2D4BD90A2846948F0A052C4A6B18F526546582` in the author receipt. S1/S2 official museum pages were reopened for 1920, named experts, 1929 and 1931. This author task does not approve its own source delta or narration.
- [x] Targeted parser PASS: 80 unique ordered IDs, exact 18/9 changed-ID sets, 67 I / 13 C, maximum consecutive cards 2, 2,513 narration characters and maximum checkpoint gap 164 **characters**, both file hashes and review-extract hash match receipts. `git diff --check` passed. No paid generation or full docs-video suite was run.

`npm run check:tasks` exit 1 still reports only the two existing unrelated open/done duplicate IDs `2026-10-22-blind-narration-review-a-for-c12` and `2026-10-22-independently-audit-c12-pyrex-script-and` as errors; its other notices are warnings. Their untracked open copies are another agent's files and stay untouched. This revision awaits independent new-SHA source/visual delta and two new-SHA narration-only blind reads, then pronunciation, owner script, measured audio and production gates.

## 2026-10-23 independent source v4 HOLD follow-up

This already claimed author task covers the narrow repair after `reviews/independent-source-visual-delta-v4.md` held E10, T09 and T11 on script SHA-256 `C030DC97CFF150D222828F56847F3D26FE63E88C97535F1755EE086BFD2CC0CF`. The original Corning Museum and Corning Incorporated pages were reopened. Narration changed **only E10, T05, T09, T10, T11** to separate premarket expert prototypes, the later consumer question, the kitchen's existence by 1931, initial sales training and later product tests. Visual rows changed **only E10, E11, T05, T09, T10, T11** for matching chronology and concept scenes. S8/S9 are defined in the script, not added to the locked treatment source matrix.

New author input hashes: script `06CB92F117686781DCAA116D32DB021A7DE45AB70BD49D19ECDA6935BF25837A`; visual `D3231901C3DEF3444F016939A0E41A298953612AA6AD5502D35450C7F3490D2F`. Targeted parser: 80 ordered unique IDs in each file, 67 illustration / 13 card rows, max card run 2, 2,503 narration characters, max checkpoint gap 164 **characters**. The SHA-bound author receipt is `author-blind-a-repair.md`; independent new-hash source/visual and narration reads remain pending. No paid generation or author self-approval. Preserve the two unrelated untracked open task copies, which continue to make `npm run check:tasks` fail.

Verification: `git diff --check` found no whitespace error; `npm run check:tasks` exit 1 identified only those two existing unrelated open/done duplicate IDs as errors, plus board-wide warnings. The full docs-video suite was not rerun for this narrow wording/visual-note revision.
