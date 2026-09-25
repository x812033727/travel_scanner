---
id: 2026-09-25-let-the-owner-drop-a-video
title: Let the owner drop a video on /admin/videos, and keep the worker off topics already made
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T12:33:58Z
created_at: 2026-09-25T12:33:51Z
completed_at: 2026-09-25T12:51:35Z
branch: claude/video-auto-drop
depends_on: []
scope:
  - apps/api/app/video_reviews
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0093_video_project_dropped.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/web/app/api/video/automation/videos
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - tools/video/automation
  - tools/video/review
  - tools/video/cli.mjs
  - docs/videos/AUTOMATION.md
---

# Let the owner drop a video on /admin/videos, and keep the worker off topics already made

## Why

The first automatic draft on production (2026-09-25 12:27Z, `google-ai-student-plan-taiwan`)
picked the same topic and the same source article (`ai-news-gemini-student-offer-20260820`) as
`gemini-student-offer`, which batch 2 had already scripted, fact-checked and narrated. Two gaps:

- The worker only knows the videos in its own `docs/videos` volume. The pilot and batch 2 live
  on branches, and nothing on the site tells the worker about them or about any video on
  /admin/videos it did not make.
- /admin/videos has no way to drop a video. Sending an outline back makes the worker re-plan
  under the same slug, so a new topic would keep the old slug, and the old slug would end up in
  the description's `utm_campaign`.

The owner chose to keep batch 2's version, leave the automatic draft untouched until this
lands, and then drop it.

## Definition of done

- [x] A video on /admin/videos can be dropped with a reason, after a confirmation. It shows as
      dropped, its pending reviews can no longer be decided, and its previews are deleted.
- [x] The worker stops a video the owner dropped. A dropped video no longer counts toward
      "waiting drafts", and its topic still counts as made.
- [x] Before planning, the worker reads every video on /admin/videos (slug, title, source
      article, dropped or not) as well as its own. The planner is told to skip their topics,
      and a plan whose slug or source article is already used is refused.
- [x] `review-push` and the worker report the source article, so the site knows it.

## Steps

- [x] API: `video_projects` gets `source_guide` and `dropped_at`, `dropped_note`, and
      `dropped_by_user_id` (migration 0093); `POST /admin/videos/{slug}/drop`; submitting to
      a dropped video is refused; a tool route lists the videos.
- [x] Web: `/api/video/automation/videos`, the drop button and the dropped state on the page,
      messages in five locales.
- [x] Tools: the worker reads the list, stops dropped videos, and checks source articles;
      `review-push` sends `source_guide`.
- [x] `docs/videos/AUTOMATION.md`: the drop and what the worker compares against.

## How to verify

- `uv run pytest tests/test_video_reviews.py tests/test_video_reviews_integration.py`,
  `npm run test:web -- admin-video-reviews`, `node --test tools/video/automation/*.test.mjs`.
- After the deploy: push the pilot and batch 2 to /admin/videos with `review-push`. Drop
  `google-ai-student-plan-taiwan` on the page. The worker's next run then logs it as dropped,
  and when the next draft is due the planner receives the earlier videos.

## Notes

- "The article a video retells" means `source_guide`. When it is missing, it is the first
  `mokaair.com/<locale>/guides/<slug>` URL the video cites. Articles cited only in passing do not
  count, otherwise a planner could never cite a common explainer twice.
- A dropped video cannot be restored. Dropping is the owner's deliberate click after a
  confirmation, and a restore would need the worker to resume a state it has already left. If a
  restore is ever needed, add it as a separate ticket.
- `POST /reviews` for a dropped video returns 409 `video_project_dropped`. The report
  (`PUT /video/reviews/{slug}`) is still accepted and leaves `dropped_at` untouched, so a tool
  that has not heard yet cannot un-drop it.
- The worker's `docs/videos` is the named volume `video_docs`. It was filled from the image once,
  on the first deploy, so later deploys do not refresh `README.md` or anything else in it. That
  is harmless today because the worker writes `lexicon.json` itself, but it will matter once a
  merged video or a shared file there needs to reach the worker.
- Found while rolling this out: the host's Claude Code was 2.1.259, and Claude Opus 5.5 needs
  2.1.280 or newer. The first run failed until `claude update` (now 2.1.282).
