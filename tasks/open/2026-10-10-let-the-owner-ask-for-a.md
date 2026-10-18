---
id: 2026-10-10-let-the-owner-ask-for-a
title: Let the owner ask for a tutorial video from an official page
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-10T09:02:30Z
completed_at:
branch:
depends_on:
  - 2026-10-10-official-pages-the-news-writer-declined
scope:
  - apps/api/app/video_automation/slides_requests.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/admin_api.py
  - apps/web/components/admin-video-slides-requests.tsx
  - tools/video/automation/flow.mjs
  - docs/videos/AUTOMATION.md
---

# Let the owner ask for a tutorial video from an official page

## Why

The owner follows the official accounts by hand (`docs/official-ai-accounts.md`) and wants
to turn a post into a tutorial video. Today the only way to ask for one specific video on
`/admin/videos` is the slides request, and it accepts only a published zh-TW lifestyle
article of the site (`apps/api/app/video_automation/slides_requests.py`,
`SlidesRequestIn {source_guide, note}`). An official page the site has no article about
can only be asked for in a chat with a session, or left to the planner to pick from the
candidate topics.

## Definition of done

- [ ] On `/admin/videos` the owner can paste an official https URL with a note and get a
      slides video planned from that page alone, the way a requested article is.
- [ ] The URL is accepted only from a host the news scanner already treats as a
      first-party source, or the owner confirms the host; decide which and write it here.
- [ ] `docs/videos/AUTOMATION.md` describes it beside the article request.

## Steps

- [ ] `VideoSlidesRequest.source_guide` is a NOT NULL slug (`models.py`), `create_request`
      requires a published article, and the worker enforces `requiredGuide` in `flow.mjs`:
      a URL request needs a migration, the schema, the form and the worker's planner
      payload (`requested_guide` has a sibling).
- [ ] The planner prompt for a requested page, modelled on the requested article.
- [ ] Tests on the API, the form and the worker.

## How to verify

Ask for a video of an official page on `/admin/videos` and see the worker plan that page
and nothing else.

## Notes

- Several of these files are bound by the duration receipt
  (`tools/video/long-form/review.mjs`); plan for an independent DURATION_ONLY increment.
- The content-value rules ask for hands-on evidence for a tutorial, and the automated
  route cannot operate a tool yet (`2026-10-09-give-the-automated-route-a-way`). Until it
  can, a requested official page gives an update-style video resting on what the page
  shows.
