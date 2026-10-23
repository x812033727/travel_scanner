---
id: 2026-10-23-display-approved-script-source-in-admin
title: Display imported approved script source in admin review cards
status: in-progress
priority: P1
area: web
owner: codex-c-series-ui-review
claimed_at: 2026-10-23T10:01:23Z
created_at: 2026-10-23T10:01:23Z
completed_at:
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
---

# Display imported approved script source in admin review cards

## Why

The C-series intake stores the owner's exact approved `script.md` in the review
payload as `source_md`. The existing script card renders narration scenes only, so
the original source and visual notes cannot be read in `/admin/videos`.

## Definition of done

- [ ] Cards with `source_md` show the complete original text beside scene narration.
- [ ] The original is escaped as text, collapsed by default, and scrollable.
- [ ] Older script cards without `source_md` keep their current layout.

## How to verify

Run the focused `admin-video-review-card.test.tsx` component test and web typecheck.
