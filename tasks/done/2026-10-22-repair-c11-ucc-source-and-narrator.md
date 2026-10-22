---
id: 2026-10-22-repair-c11-ucc-source-and-narrator
title: Repair C11 UCC source and narrator wording
status: done
priority: P1
area: docs
owner: codex-c11-ucc-script
claimed_at: 2026-10-22T14:52:12Z
created_at: 2026-10-22T14:51:47Z
completed_at: 2026-10-22T14:53:55Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
---

# Repair C11 UCC source and narrator wording

## Why

The independent C11 script/source receipt on PR #1691 (head `37a41ec52`) found one elapsed-time error and two lines that speak about the editor's fact-checking instead of the story. The approved treatment still stands; repair only those lines and their author notes, then request a new SHA-bound delta review.

## Definition of done

- [x] c110208 states Mira preceded UCC without calling 1965-09-14 to 1969-04 a full four years.
- [x] c110210 and c110512 use natural narration while preserving the Mira versus milk-coffee scope and UCC-attributed Expo effects.
- [x] All 83 IDs remain matched to the unchanged visual plan; draft PR stays `no-auto-merge`, with the old HOLD receipt marked historical.

## Steps

- [x] Re-read the independent receipt and make the three narrow line edits.
- [x] Check source-note consistency, hashes, visual IDs, and commit/push the draft branch.

## How to verify

Compare all 83 script IDs against `visual-plan.json` in order; check the three revised sentences against H3/U1/U2/U3; `git diff --check`; do not repeat paid or broad test suites for this prose-only repair.

## Notes

- Prior review: `docs/videos/story-everyday-ucc-c11/reviews/independent-script-source-review.md`, bound to script SHA `553F5C14B5E4E7475875F2021F21AC86A3175BC024EA33B03DF3E60730C12438`, HOLD. H3 dates Mira sale 1965-09-14; U1 dates UCC launch only to April 1969, about three years seven months later.
- Task claim used `--force` solely because our own previous draft task `2026-10-22-draft-c11-ucc-story-script-and` was copied to `tasks/done/` but its original untracked `tasks/open/` copy remained after Windows file hold; the exact deletion was previously rejected by automatic approval review. Remote draft task is done. No other owner's scope was overridden, and no deletion workaround was attempted.
- Revised script SHA-256 `BF58A5C51F248806D56CBF37705737B1DAA7FEB4F7B43593CC702426E6D0C887`; author source notes SHA-256 `DB6CD95FE236D4265DD23116E942C4E05A457720CA2D52BF16885FECD145AB7F`; visual JSON unchanged SHA-256 `6B8FF62EE948B132C1E0B8B6942263D84628C96C42BA6E840B95E38CAB5DFEBA`. 83/83 IDs match in order; `git diff --check` PASS. New SHA independent delta review and two blind reads remain pending, no owner or paid gate crossed.
- `tasks done` wrote this completed copy but again left the original same-ID open file untracked in this Windows worktree. The earlier exact removal of the previous ticket was rejected by automatic approval review as `blocked by policy`; this continuation did not attempt a deletion workaround. Both untracked open copies are excluded from the PR. Local `check:tasks` will see duplicate task IDs until those exact local files can be removed through an allowed route.
