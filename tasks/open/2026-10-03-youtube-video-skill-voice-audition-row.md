---
id: 2026-10-03-youtube-video-skill-voice-audition-row
title: youtube-video SKILL.md: index row for references/voice-audition.md (receipt-bound)
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T10:42:30Z
completed_at:
branch:
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

- [ ] `.agents/skills/youtube-video/SKILL.md` 去哪裡讀 table has a row for `references/voice-audition.md`
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
