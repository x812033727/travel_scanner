---
id: 2026-10-30-admin-video-delete-dropped
title: Delete a dropped video from /admin/videos
status: review
priority: P1
area: api
owner: claude-opus-5-5-delete-dropped
claimed_at: 2026-10-30T19:32:22Z
created_at: 2026-10-30T19:27:26Z
completed_at:
branch: claude/vigorous-mclaren-46921c
depends_on: []
scope:
  - apps/api/app/video_reviews
  - apps/api/app/video_automation/series.py
  - apps/api/app/auth/service.py
  - apps/api/app/admin/user_schemas.py
  - apps/api/tests/test_video_reviews_delete.py
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-delete.tsx
  - apps/web/components/admin-video-delete.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/lib/admin-video-delete-copy.ts
  - apps/web/lib/admin-video-delete-messages
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Delete a dropped video from /admin/videos

## Why

The owner is remaking the catalog under the new rules, so `/admin/videos` has piled up dropped
videos (`story-adapt-dolby-licensing`, `curio-s13`, the old `story-everyday-*`). A drop keeps the
row on purpose, so there was no way to clear them. Owner's words: a dropped video gets a delete
button, and deleting removes it from the database and the admin entirely.

## Definition of done

- [ ] A dropped video shows a delete button (its page and its catalog row); any other does not,
      and the API refuses it.
- [ ] After a delete, neither the list nor the database has the video.
- [ ] A worker holding the slug does not bring the row back, and the slug can be registered anew.
- [ ] API and web tests.

## Steps

- [x] Map what a video's slug touches.
- [x] `app/video_reviews/deletion.py`, the DELETE route, the `videos.delete` step-up scope.
- [x] The `on_site` fence: `upsert_project` answers 410, `report()` and `review-push` send it, and
      `bookkeeping` marks a deleted video dropped.
- [x] The dialog, five languages in `apps/web/lib/admin-video-delete-messages/`. A new
      `messages/` namespace is no way round `admin.json`: the i18n check wants it listed in
      `uiText.namespaces` there.
- [ ] Checks; the duration receipt's increment by an independent reviewer.

## How to verify

```bash
(cd apps/api && uv run pytest tests/test_video_reviews_delete.py -q)
(cd apps/web && npx vitest run components/admin-video-delete.test.tsx)
node --test --test-name-pattern="deleted|on_site|only missing" tools/video/automation/automation.test.mjs
```

On the site: drop a test video, open it, 永久刪除, type the slug, enter the password when asked. It
leaves the list; `SELECT * FROM video_projects WHERE slug = ...` is empty; `admin_audit_logs` has
`video_project_deleted` with what the row said.

## Notes

`deletion.py`'s docstring is the list of what goes and what stays.

- **Why a flag and not a tombstone.** A table or an audit lookup of deleted slugs would refuse
  every later report, and `script-intake.mjs` and any re-import expect a 404 followed by a PUT to
  work. `on_site` tells the two apart without keeping anything: a sender that was answered before
  and finds no row is looking at a delete; a first report registers the slug.
- **Why the worker asks before believing the list.** The worker's list is the newest 200 of 412
  videos, so absence proves nothing. `leaveIfDeleted` asks for the row itself, once a run.
- **A done video is not checked.** It reports only while the site lists it (`languages` returns
  null for an unlisted one), so it cannot bring a row back.
- **Step-up.** Backend convention 8 for a destructive operation. The site allows five step-ups an
  hour, so the dialog tries the delete first and asks for the password only when the site does;
  one password covers five minutes of clearing.
- **Not handled, small:** a Short remade under the same title could be matched by
  `claim.match_uploads` to the old upload still on YouTube, because a deleted project's id no
  longer counts as taken. A stage job already queued when the delete lands still runs once, as it
  does for a drop made a moment after dispatch.
