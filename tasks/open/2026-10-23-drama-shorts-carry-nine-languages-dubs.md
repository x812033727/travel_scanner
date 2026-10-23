---
id: 2026-10-23-drama-shorts-carry-nine-languages-dubs
title: Drama Shorts carry nine languages (dubs, CC, titles)
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-shorts-1-5
claimed_at: 2026-10-23T11:57:38Z
created_at: 2026-10-23T11:57:10Z
completed_at:
branch: claude/shorts-1-5-editing-87d7bf
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_languages_imported.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - tools/video/import
  - docs/videos/LANGUAGES.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo
---

# Drama Shorts carry nine languages (dubs, CC, titles)

## Why

The owner (2026-10-23) wants the 種田娶妻打天下 Shorts (one an episode, cut by
`hailuo/shorts-dh.mjs` from the imported episodes) in the Shorts tab with the same nine
languages the episodes carry: zh-TW plus en, ja, ko, es, pt, id, vi, th titles, CC and dub
tracks. Each Short's dubs are the episode's own tracks cut to the same span, so nothing has to
be made. The site refuses it: `_dub_allowed` returns False for every Short, the video page
hides the language panel for a Short, and `import --languages` takes only a video the long
import put there.

## Definition of done

- [ ] A drama Short (`shorts_line == "drama"`) may tick dubs on its language panel; lab and cut
      Shorts still may not.
- [ ] The video page shows the language panel on a drama Short.
- [ ] `node tools/video/cli.mjs import --from DIR --languages` sends a languages batch for a
      drama Short whose newest final cut is DIR's final.mp4.
- [ ] The five Shorts are on the Shorts tab with their languages batches pending.

## Steps

- [ ] Server rule and tests.
- [ ] Web panel and test.
- [ ] Tool and test.
- [ ] Docs (LANGUAGES.md).
- [ ] PR, merge, deploy (owner's go), then import the five Shorts and send their languages.

## How to verify

`cd apps/api && uv run pytest tests/test_video_languages_imported.py`, `npm run test:web --
admin-video-reviews`, `node --test tools/video/import/import.test.mjs`; on the site, a drama
Short's page shows the panel and its languages batch lists eight locales.

## Notes

- Claimed with `--force`: 2026-10-13-dub-narrator-only-explainer-dramas-tool and
  2026-10-19-worker-video-languages-five also list admin_service.py, but both are in review and
  their code is already on main (the explainer dub rule and the five languages).
- Publishing a Short still uses the Shorts package (titles and CC of the Shorts settings'
  locales); the owner uploads to Studio by hand, taking the other languages from the batch.
