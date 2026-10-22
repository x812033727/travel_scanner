---
id: 2026-10-22-independently-source-review-c11-ucc-script
title: Independently source-review C11 UCC script and visuals
status: done
priority: P2
area: docs
owner: codex-c11-independent-review
claimed_at: 2026-10-22T14:44:10Z
created_at: 2026-10-22T14:43:57Z
completed_at: 2026-10-22T14:47:41Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/reviews/independent-script-source-review.md
---

# Independently source-review C11 UCC script and visuals

## Why

C11's approved Treatment is not a line-level script approval. The 83 new narration lines and their illustrations need a separate direct-source and visual preflight before blind readers or the owner script gate.

## Definition of done

- [x] A SHA-bound receipt reviews all 83 narration lines, cites directly opened sources, and separates source, visual, and editorial verdicts.

## Steps

- [x] Reopen UCC, Hamada City, and Shimane Prefecture source pages and compare every line to its evidence boundary.
- [x] Verify every visual ID and image prompt against the story and Curio visual contract.
- [x] Record precise holds and the remaining owner, blind-read, and actual-duration gates.

## How to verify

`Get-FileHash -Path docs/videos/story-everyday-ucc-c11/script.md,docs/videos/story-everyday-ucc-c11/visual-plan.json,docs/videos/story-everyday-ucc-c11/script-source-notes.md -Algorithm SHA256`; independently open the seven direct source URLs named in the receipt; parse visual-plan.json and compare its line_id set to the 83 script IDs; `npm run check:tasks`; `git diff --check`.

## Notes

Claimed 2026-10-22 UTC as `codex-c11-independent-review` on the existing C11 script PR branch. The author's done ticket left an untracked local open duplicate after an auto-review blocked its deletion. Do not stage that ghost. This review touches only its own receipt and task file.

Direct reread supports 82/83 script lines; `c110208` says a complete four years, while source dates are 1965-09-14 and 1969-04. Narration lines `c110210` and `c110512` also expose editorial fact-check language. Independent visual text preflight passes ID parity and prompt contract, but timed illustration share and generated quality cannot be determined from this draft. Review receipt is `docs/videos/story-everyday-ucc-c11/reviews/independent-script-source-review.md`, tied to script SHA `553F5C14B5E4E7475875F2021F21AC86A3175BC024EA33B03DF3E60730C12438` and visual SHA `6B8FF62EE948B132C1E0B8B6942263D84628C96C42BA6E840B95E38CAB5DFEBA`.

`git diff --check` passed. `npm run check:tasks` exited 1 only because the author's previously done C11 task also exists as an untracked `tasks/open/2026-10-22-draft-c11-ucc-story-script-and.md`; its exact deletion was already `blocked by policy`. This review does not attempt to bypass it. The newly claimed review task is otherwise structurally valid.

`tasks done` wrote this done file but exited 1 because its newly created open copy remained on this checkout. I resolved that exact local path and removed the new copy with one direct `Remove-Item -LiteralPath`; that action succeeded. The author's separate blocked open duplicate was not touched and still makes the local task check fail.
