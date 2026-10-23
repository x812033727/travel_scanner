---
id: 2026-10-16-move-brand-stories-from-drama-to
title: Move brand stories from Drama to Videos
status: done
priority: P2
area: web
owner: codex-gpt6-brand-story-tab
claimed_at: 2026-10-16T12:19:17Z
created_at: 2026-10-16T12:18:33Z
completed_at: 2026-10-16T13:02:07Z
branch: codex/brand-stories-video-tab-20261016
depends_on: []
scope:
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
---

# Move brand stories from Drama to Videos

## Why

Brand-story videos are already in the Videos catalog under the story category, but their series list, import, and management page live under Drama. This sends the owner to the wrong workspace and leaves old Drama bookmarks pointing at the misplaced page.

## Definition of done

- [x] Videos > Brand stories contains the story series list, import, detail page, and individual video catalog.
- [x] Drama no longer lists story series; old Drama story links open the new Videos location.
- [x] Existing story production, review, CC, and dubbing data remain intact.

## Steps

- [x] Move story series UI into the Videos story category with a dedicated URL key.
- [x] Remove story series from Drama and redirect legacy deep links.
- [x] Cover navigation and filtering with focused tests.

## How to verify

Run targeted Vitest tests for the video browser, stories, and series, plus web lint, i18n check, typecheck, and task-board check. Verify that `?tab=reviews&category=story` shows story series and catalog and that `?tab=drama&series=<story>` redirects.

## Notes

The shared `admin-video-reviews.tsx` is in three other actively owned task scopes. This ticket avoids that file. Story videos remain in the Videos catalog, but the top-level `needs you` / `ready to upload` reminder groups still filter them out until that separately owned code can be changed. The database `kind=story` and video `format=drama` encode production rules and are not a UI placement target.

The story list and old-bookmark redirect live in `admin-video-stories.tsx`, which the existing Drama component imports. The wrapper renders the list only on the Videos tab, and the story page redirects a legacy Drama deep link into Videos. The API's `list_series(kind="series")` filters by kind in its SQL query. This leaves `admin-video-series.tsx` and its test byte-identical to main; their duration review bindings remain current, and `node tools/video/long-form/cli.mjs check` passes. A hypothetical older API that ignored the `kind` filter could show a story in the generic Drama series list; the current server filters it.

Implementation uses `?tab=reviews&category=story&story_series=<slug>` for the story page. Old `?tab=drama&series=<story>` links redirect after checking the saved kind; an unrelated series opened through a hand-edited story URL returns to Drama. A series can be imported before its first video, even when the story facet has count zero. The story detail scrolls into view on direct links because the shared Videos page has other sections above the catalog.

Verification so far: targeted series/story tests 55/55 (including a no-tab Videos bookmark), TypeScript typecheck, web ESLint, i18n check, `tools/tasks.mjs check`, and the long-form plan/review check all exited 0. CI's first run exposed the duration receipt binding when the Drama component was edited; the revised implementation above avoids editing it and needs a fresh CI run. The full local web unit run was stopped after all three CI web-unit shards passed.
