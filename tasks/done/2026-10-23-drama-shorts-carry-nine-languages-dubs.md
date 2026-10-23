---
id: 2026-10-23-drama-shorts-carry-nine-languages-dubs
title: Drama Shorts carry nine languages (dubs, CC, titles)
status: done
priority: P2
area: api
owner: claude-opus-5-5-shorts-1-5
claimed_at: 2026-10-23T11:57:38Z
created_at: 2026-10-23T11:57:10Z
completed_at: 2026-10-23T15:06:43Z
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

- [x] A drama Short (`shorts_line == "drama"`) may tick dubs on its language panel; lab and cut
      Shorts still may not.
- [x] The video page shows the language panel on a drama Short.
- [x] `node tools/video/cli.mjs import --from DIR --languages` sends a languages batch for a
      drama Short whose newest final cut is DIR's final.mp4.
- [x] The five Shorts are on the Shorts tab with their languages batches pending.

## Steps

- [x] Server rule and tests.
- [x] Web panel and test.
- [x] Tool and test.
- [x] Docs (LANGUAGES.md).
- [x] PR, merge, deploy (owner's go), then import the five Shorts and send their languages.

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
- Done 2026-10-23: PR #1783 (807debf07), deployed 14:12Z, verify 12/12 with
  `api-drama-short-dubs`. The five Shorts (`zhong-tian-qu-qi-e00N-short`) went up with
  `tools/video/shorts/cli.mjs import`, `qa --offline` and `push`; their languages batches
  (24 parts each) through `tools/video/cli.mjs import --languages`; the owner approved the cuts
  and the batches, and the upload packages wait for the owner.
- The Shorts upload package wants en/ja/ko CC (the Shorts settings' languages) and the full
  video's address. Both are QA inputs, so adding them after the first approval opens a new final
  review. Next time put `<l>.srt` into the build and `source.url` into meta.json before the
  first push. The episodes are on YouTube only inside the 1–5 compilation, so each Short links
  to its chapter (`shorts-dh.json` `full_video`).
- The package's `captions` item always fails on these Shorts: the foreign CC carry the system
  panel lines the zh-TW CC leave out, and end with the dubbed line, while `captionProblems`
  wants each caption on the zh-TW timeline to 2 ms. The owner approves it by hand.
