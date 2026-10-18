---
id: 2026-10-13-explainer-route-files-its-drama-under
title: Explainer route files its drama under the explainer category
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-13T13:11:37Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Explainer route files its drama under the explainer category

## Why

Since `2026-10-13-dub-narrator-only-explainer-dramas-tool`, the server and the language panel let
the owner tick a dub for a drama only when its project's category is `explainer` (觀念解說):
the narrator tells it alone. But the automated explainer route (cute-mystery, cute-cartoon,
flat-explainer) never writes a category. Its state has none (`flow.mjs` sets one only for long
anime, and `story.mjs` writes `story` for a brand story), and the writer's video.json shape in
`automation/explainer-series.mjs` has no `category`. `recorded()` in `flow.mjs` reports
`state.category ?? video.category`, so the project row stays uncategorised. Until the owner files
each such episode under 觀念解說 on its video page, its dub box stays grey.

## Definition of done

- [ ] A drama the explainer route makes reports category `explainer` (a state field set when the
  explainer episode is started, so `recorded()` sends it); a category the owner set on the page
  still wins (the site fills one only on a video nobody filed).
- [ ] A test in `automation.test.mjs` shows the report carries it.

## How to verify

`node --test tools/video/automation/automation.test.mjs`.

## Notes

Found while doing the dub change; not done there because `tools/video/automation` was in another
active task's scope (`2026-10-12-narrated-videos-open-on-a-30`). Until this lands, the owner files
the episodes by hand (video page → 分類 → 觀念解說), and the dub box opens.
