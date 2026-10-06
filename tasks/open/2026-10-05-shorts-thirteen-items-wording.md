---
id: 2026-10-05-shorts-thirteen-items-wording
title: Shorts docs and comments still say twelve QA items after the grammar item
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T18:22:57Z
completed_at:
branch:
depends_on:
  - 2026-10-05-shorts-six-beat-grammar-qa
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - apps/api/app/video_shorts/models.py
  - apps/api/app/video_reviews/admin_service.py
---

# Shorts docs and comments still say twelve QA items after the grammar item

## Why

The Shorts quality check grew a thirteenth item, `grammar` (ticket
`2026-10-05-shorts-six-beat-grammar-qa`): the tool's `ITEM_IDS`, the server's
`SHORTS_QA_ITEMS`, `docs/videos/SHORTS.md` and the shorts reference now say thirteen,
but three places outside that ticket's scope still say twelve: the youtube-video
`SKILL.md` (the `.agents` original and its `.claude` copy, both receipt-bound and
compared by `npm run test:tools`) in its Shorts row and its reference table, and two
comments in `apps/api/app/video_shorts/models.py` (the auto-approval field) and
`apps/api/app/video_reviews/admin_service.py` (where `SHORTS_QA_AUTO_APPROVED_NOTE` is
applied). Nobody reading them should be told the wrong count.

## Definition of done

- [ ] No file in the repository says a Short passes twelve quality checks: the count is
      thirteen, or taken from `SHORTS_QA_ITEMS` / `ITEM_IDS`.

## Steps

- [ ] `.agents/skills/youtube-video/SKILL.md`: "12 項自動品管" and "12 項品管" become 13 in
      the Shorts row and the reference table; copy the file byte for byte to
      `.claude/skills/youtube-video/SKILL.md`.
- [ ] The two API comments: "twelve" becomes "thirteen", or "its own" with no number.
- [ ] The two `SKILL.md` files are receipt-bound: an independent reviewer adds the duration
      receipt increment (`.agents/skills/dev-and-ci/references/duration-receipt.md`).

## How to verify

```bash
grep -rn "12 項自動品管\|12 項品管\|twelve checks" .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md apps/api/app/video_shorts/models.py apps/api/app/video_reviews/admin_service.py
npm run test:tools
node tools/video/long-form/cli.mjs check
```

## Notes

- Filed from the grammar ticket, whose scope could not take these files. The web fixtures in
  `apps/web/components/admin-video-shorts.test.tsx` also carry "12 項全過" summaries, but as
  data the fake site returns, not a count the web computes; they can stay.
