---
id: 2026-10-19-show-each-video-s-drive-backup
title: Show each video's Drive backup state on its review card and detail
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-19T17:28:59Z
completed_at:
branch:
depends_on:
  - 2026-10-15-video-backup-web
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
---

# Show each video's Drive backup state on its review card and detail

## Why

The settings tab's backup card (`2026-10-15-video-backup-web`) answers "is every uploaded video in
Google Drive" for the whole channel. The owner also wants to see it on the video itself: on its
review card and its detail page, whether Drive has it (done, with time, size and folder), is
still waiting, failed (and why), is blocked by Drive space, or lacks files (which). That part was
left out because `admin-video-reviews.tsx`, `admin-video-review-card.tsx`,
`apps/web/messages/*/admin.json` and `apps/api/app/video_reviews/*` were held by
`2026-10-12-let-managers-link-a-private-studio` and `2026-10-19-imported-video-languages-eight`.

## Definition of done

- [ ] `ProjectSummary` (apps/api/app/video_reviews/schemas.py) carries `backup`: the view
      `app/video_backup/admin_status.py` `backup_view` builds (state, folder, tier, bytes, at,
      missing, error, overdue), so the list and the detail need no second request.
- [ ] The review card and the project detail show a chip with that state, its time and size
      when done, the missing files when partial, and the reason when failed or blocked; a
      link to `/admin/videos?tab=settings#video-backup-settings`.
- [ ] Copy in all five locales (`lib/video-backup-messages` already has the state labels).

## Steps

- [ ] Add `backup` to `_summary` in `admin_service.py` from `backup_view(project, config,
      now)`, reading the settings row once per list, not once per video.
- [ ] The chip component, reusing `stateLabel` from `components/admin-video-backup.tsx`.
- [ ] Tests for both.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_backup.py
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- Wait for the two tasks above to land, or rebase onto them; the scope may need
  `apps/web/components/admin-video-reviews.tsx` once they release it.
