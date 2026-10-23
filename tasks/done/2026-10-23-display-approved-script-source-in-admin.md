---
id: 2026-10-23-display-approved-script-source-in-admin
title: Display imported approved script source in admin review cards
status: done
priority: P1
area: web
owner: codex-c-series-ui-review
claimed_at: 2026-10-23T10:01:23Z
created_at: 2026-10-23T10:01:23Z
completed_at: 2026-10-23T11:12:17Z
branch: codex/everyday-story-review-import-20261023
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Display imported approved script source in admin review cards

## Why

The C-series intake stores the owner's exact approved `script.md` in the review
payload as `source_md`. The existing script card renders narration scenes only, so
the original source and visual notes cannot be read in `/admin/videos`.

## Definition of done

- [x] Cards with `source_md` show the complete original text beside scene narration.
- [x] The original is escaped as text, collapsed by default, and scrollable.
- [x] Older script cards without `source_md` keep their current layout.

## How to verify

Run the focused `admin-video-review-card.test.tsx` component test and web typecheck.
The duration review binds this card and the five admin message files by SHA-256; obtain an
independent delta review before rebinding `review.md` and `review.json`.

2026-10-23: #1778 merged after the focused component test, web typecheck and
independent duration-review increment passed; its exact SHA was deployed. API
readback confirms nine new C-series cards carry full `source_md`; the earlier C03
approved card remains in its legacy format without this field. The UI renders
`source_md` as escaped text inside a collapsed scroll area and leaves legacy cards
on their existing scene view.
