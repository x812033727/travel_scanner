---
id: 2026-10-03-youtube-video-skill-voice-audition-row
title: youtube-video SKILL.md: index row for references/voice-audition.md (receipt-bound)
status: review
priority: P3
area: docs
owner: codex-voice-audition-index-20261003
claimed_at: 2026-10-03T12:02:21Z
created_at: 2026-10-03T10:42:30Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# youtube-video SKILL.md: index row for references/voice-audition.md (receipt-bound)

## Why

PR #1174 added `.agents/skills/youtube-video/references/voice-audition.md` (how to audition voice-style wordings
before changing `accent.mjs` or `STORY_VOICE_STYLE`) and pointed at it from `script-writing.md` and `drama.md`
only, because `SKILL.md` is bound by the long-form duration receipt and two other PRs were carrying receipt
increments at the time. The skill's 去哪裡讀 table is the index agents read first; without a row there the
reference is easy to miss.

## Definition of done

- [x] `.agents/skills/youtube-video/SKILL.md` 去哪裡讀 table has a row for `references/voice-audition.md`
      (換口音或口吻的寫法之前怎麼試聽、改哪些檔), mirrored byte for byte to `.claude/skills/youtube-video/SKILL.md`.
- [ ] The long-form duration receipt is rebound by an independent reviewer
      (`.agents/skills/dev-and-ci/references/duration-receipt.md`); `node tools/video/long-form/cli.mjs check` passes.

## How to verify

```bash
node --test tools/skills.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

Best done on the next PR that already touches `youtube-video/SKILL.md`, so the receipt increment is shared.

- 2026-10-03: Added only the voice-audition reference row to the existing reference table; both SKILL.md files are byte-for-byte identical. No voice, provider, login, duration or production setting changed. Independent duration-receipt review is still pending; the author does not edit review.md/review.json.
- Claim exception: normal claim was rejected only by the historical `2026-10-03-illustrated-slides-round-2-a-family` review metadata from merged PR #1172. Force-claimed only this new ticket after a fresh four-path gate (2 open PRs, 493 refs, 33 live remote heads, 972 unique task blobs and 28 registered worktrees) found no active implementation or dirty collision. Preserved the original ticket, owner, media acceptance and all other worktree bytes. Independent docs-two-path review had already verified the 108 main baseline bindings. Evidence: private `voice-audition-index-20261003/four-scope-gate-final.json` SHA256 `8ece646335b747d81e433bd058fc107a1429184041bbd24080ae96f72f552891`; `normal-claim.log` and `force-claim.log`.
- Validation: bundled Node 24.19 `node --test tools/skills.test.mjs` passed all 6 cases (0 failures/skips). Source-only proof shows exactly one inserted index row and identical mirrored bytes; final SHA256 for each SKILL.md is `c5549733c632dac550e4063d272e5decda07910e63fb58740e3fdabb89099958`. The independent reviewer owns the duration receipt update and subsequent long-form checks; that second DoD remains unchecked until their evidence is complete.
