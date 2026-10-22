---
id: 2026-10-22-draft-patagonia-c09-narration-and-illustrated
title: Draft Patagonia C09 narration and illustrated shot plan
status: done
priority: P2
area: docs
owner: codex-c09-patagonia
claimed_at: 2026-10-22T13:29:56Z
created_at: 2026-10-22T13:29:50Z
completed_at: 2026-10-22T13:39:40Z
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09/script.md
  - docs/videos/story-everyday-patagonia-c09/visual-plan.md
  - docs/videos/story-everyday-patagonia-c09/script-evidence.md
---

# Draft Patagonia C09 narration and illustrated shot plan

## Why

The owner adopted the independently checked C09 Patagonia Treatment on PR #1685, bound to `treatment.md` SHA-256 `0769134247D8D98407FDE2DCE3DD8026AF1681CB408A855C62F9708915991FDD` and `source-matrix.md` SHA-256 `EC8E598C9099EBE0FFD51CBF89807C96962C62618A41BE8BA3A66A48986EEA2C`. This is **Treatment approval only**; the owner has not approved a script or any paid production. A full narration and shot-by-shot visual draft are the next reviewable gate before any paid TTS, image or music production. The script must preserve the 1972 Chouinard Equipment / 1973 Patagonia clothing-label distinction, the original foreword's limited piton exception, the undated scan edition caveat, and the 1977 independent evidence of continued sales.

## Definition of done

- [x] Narration script has a continuous six-chapter story, a concrete 30–60 second cold open, real 30–45 second hooks, at least eight named setup/payoff loops, and line-level source notes.
- [x] Every narration line maps one-to-one to a shot or card plan with Curio `cute-mystery` constraints; estimated illustrated share is at least 70% and no more than three cards are consecutive.
- [x] Author self-check and mechanical checks are recorded, with independent source review, two blind readers, visual preflight, owner script approval, actual TTS duration and any paid budget still explicitly pending.

## Steps

- [x] Confirm revised Treatment and source matrix hashes match the independent PASS receipt, and confirm the owner adoption in the parent task.
- [x] Close the already-owned Treatment task before claiming this narrower script task.
- [x] Draft `script.md`, `visual-plan.md`, and `script-evidence.md` without altering Treatment, source matrix, or review receipt.
- [x] Count lines, visual types, card runs and estimated body length; check source boundaries and push this ticket, its three owned files and the previously owned Treatment task's completion record to draft PR #1685.

## How to verify

Compare Treatment and matrix SHA-256 to the independent review receipt. Count narration IDs and visual-plan IDs and require exact bijection, check `shot` share and maximum consecutive cards, `git diff --check`, `npm run check:tasks` where the worktree permits it, and read PR draft/no-auto-merge status after pushing. Independent reviewers, owner script approval and actual voice length are separate gates.

## Notes

The Treatment task's `npm run tasks -- done` wrote its done copy but left its own open copy behind. The author removed that exact open copy after confirming both paths, so this new ticket could be claimed without `--force`. Two unrelated policy-blocked duplicate review-ticket open copies remain untracked and must not be staged or deleted as a workaround. The original C09 Treatment and matrix files are outside this task's scope.

Author output: 98 body lines plus 3 outro lines, 2,458 body Hanzi, 101 matching visual IDs, 84 `shot` and 17 `stats` overall; body 82 `shot` and 16 `stats`, at most 2 consecutive cards, 83.7% shot share by count and a 78.5% conservative designed time share (5 seconds per shot versus 7 per card). At 300 Hanzi/minute, body is about 8:12 **as an estimate**, not a TTS measurement. The source and hook audit is in `script-evidence.md`. Script SHA-256 `3AEDEFFF6019A6F85F5BD6207B1FED9C3BD0CEAF4B4BF357A56C221F896BDA09`; visual plan SHA-256 `60D56443D75C3BBAEA472AD1F4672CC8E8D7B03E85D497ACDA43C8BB79311214`.

`git diff --check` passed. `npm run check:tasks` exits 1 because a different review ticket has both a tracked done copy and an untracked open copy; this author will not remove the policy-blocked open copy. Other long-held scope warnings are pre-existing. This task completes only the **author draft**; next gates remain independent line-level source review, two blind readers, visual and pronunciation preflight, owner approval, real TTS body duration and separate paid budget approval.
