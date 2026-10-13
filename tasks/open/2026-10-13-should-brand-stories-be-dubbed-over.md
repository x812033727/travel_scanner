---
id: 2026-10-13-should-brand-stories-be-dubbed-over
title: Owner decision: may a brand story be dubbed over its burned-in zh-TW subtitles
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-13T13:07:39Z
completed_at:
branch:
depends_on:
  - 2026-10-13-dub-narrator-only-explainer-dramas-tool
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/web/components/admin-video-reviews.tsx
  - docs/videos/DUBS.md
---

# Owner decision: may a brand story be dubbed over its burned-in zh-TW subtitles

## Why

Since `2026-10-13-dub-narrator-only-explainer-dramas-tool`, a drama is dubbed when the narrator
tells it alone. The dub tool (`tools/video/dubs/cli.mjs` `spokenByCharacter`) reads the script
and accepts any drama in which no line has a speaker other than `narrator`. A brand story
(category `story`) is such a drama: `core/story.mjs` lint refuses any other speaker, and the
story's recurring figures (`storyCast` in `tools/video/automation/story.mjs`) are drawn, never
heard; they carry the narrator's voice only because lint wants one. So the tool would dub a story.

The site does not offer it. The server (`apps/api/app/video_reviews/admin_service.py`
`DUBBABLE_DRAMA_CATEGORIES`) and the language panel (`apps/web/components/admin-video-reviews.tsx`
`DUBBABLE_DRAMA_CATEGORIES`) allow a drama's dub for category `explainer` only, because a brand
story burns its zh-TW subtitles into the picture (`composeStory` writes
`subtitles: { burn_in: true }`). An English, Japanese or Korean dub would play under Chinese text
that cannot be switched off. Whether that is acceptable is a product call for the owner, not
something to unlock as a side effect.

Nothing here changes an automatic default either way: a hands-off brand story gets its languages
from the server (`drama_caption_locales`: titles, descriptions and captions, never a dub). Turning
dubs on there would dub every brand story automatically and spend money nobody approved; that
would be a separate decision.

## The question for the owner

1. May the owner tick a dub for a brand story by hand, over its burned-in zh-TW subtitles?
   (A: yes, add `story` to both `DUBBABLE_DRAMA_CATEGORIES`; B: only after stories stop burning
   subtitles and use switchable CC; C: no.)
2. If yes, should hands-off stories ever get a dub automatically? (Default: no.)

## Definition of done

- [ ] The owner has answered, and the answer is written in `docs/videos/DUBS.md` §已知限制.
- [ ] If A: `story` is in both `DUBBABLE_DRAMA_CATEGORIES` sets (server and page), with the
  server and page tests extended the way the explainer case is; the dub tool needs no change.

## How to verify

`cd apps/api && uv run pytest tests/test_video_reviews.py -k languages_once` and
`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`.

## Notes

Not to be claimed until the owner answers; the scope is what an A answer would touch.
