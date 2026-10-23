---
id: 2026-10-16-show-brand-story-review-reminders-in
title: Show brand-story review reminders in Videos
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-16T12:44:21Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# Show brand-story review reminders in Videos

## Why

Brand-story videos use `format=drama` for their production pipeline, but belong to Videos > Brand stories for owner review. The Videos page currently filters every `format=drama` item out of its top-level `needs you` and `ready to upload` groups. The story series page and video catalog still provide a path to each review, but the prominent reminders omit them.

## Definition of done

- [ ] A brand-story video awaiting owner review appears in the Videos `needs you` group and opens its review detail.
- [ ] A brand-story video ready to upload appears in the Videos `ready to upload` group.
- [ ] Other drama and Shorts remain outside those Videos groups, with no duplicate cards.

## Steps

- [ ] Coordinate with the active owners of `admin-video-reviews.tsx` before claiming this scope.
- [ ] Narrow the reminder-group filter to include story category and add focused tests.

## How to verify

Test pending/ready story fixtures alongside ordinary drama and Shorts; run the relevant web tests, lint, typecheck, and task-board check.

## Notes

Filed during the brand-story workspace move on 2026-10-16. The affected review file is declared by three already owned tickets (`2026-10-12-let-managers-link-a-private-studio`, `2026-10-10-let-the-owner-re-request-a`, and `2026-10-13-dub-narrator-only-explainer-dramas-tool`), so this ticket is intentionally unclaimed. The separate workspace move adds story series management to Videos without editing those active scopes.
