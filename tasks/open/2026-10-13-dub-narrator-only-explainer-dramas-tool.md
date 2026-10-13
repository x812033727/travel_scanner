---
id: 2026-10-13-dub-narrator-only-explainer-dramas-tool
title: Dub narrator-only explainer dramas: tool, server and language panel
status: review
priority: P2
area: tools
owner: claude-opus-5.5-dub-narrated-drama
claimed_at: 2026-10-13T12:50:27Z
created_at: 2026-10-13T12:46:40Z
completed_at:
branch: claude/dub-narrated-drama
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - docs/videos/DUBS.md
  - docs/videos/LANGUAGES.md
---

# Dub narrator-only explainer dramas: tool, server and language panel

## Why

Dubbing was refused for every `format: "drama"` video at three layers, because a drama with
characters needs a foreign voice per character. The cute explainer series is drama-format but
narrator-only, so dubbing it is the same job as dubbing a slides video. The owner tried to tick
dubbing for five narrator-only explainer episodes and could not.

## Definition of done

- [x] `dub` refuses only a drama in which some line has a speaker other than `narrator`, saying
  which line and who speaks it, with exit 3 (the owner's), so the worker records a skipped dub
  (`flow.mjs` `giveUpDub`) and the video goes on. A narrator-only drama is dubbed, cast or not.
- [x] The server (`admin_service.py` `DUBBABLE_DRAMA_CATEGORIES`) accepts a dub for a drama of
  category `explainer` and refuses (422) every other drama, `story` and no category included.
- [x] The language panel enables the dub box for an `explainer` drama and keeps it greyed out with
  the `dubDramaLater` tooltip otherwise.
- [x] No automatic default changed: hands-off brand stories still get `drama_caption_locales`
  (no dub), and "tick the defaults" never ticks a dub.
- [x] `DUBS.md` and `LANGUAGES.md` say a narrator-only explainer drama can be dubbed.
- [ ] An independent DURATION_ONLY increment to `docs/videos/long-form/review.json` for the bound
  files this changes (arranged by the coordinator; author and reviewer must differ).

## Steps

- [x] Tool: `spokenByCharacter` in `tools/video/dubs/cli.mjs`, a SpeechError for the owner.
- [x] Server and page: one `DUBBABLE_DRAMA_CATEGORIES` per layer, each naming the other two.
- [x] Tests extended where they live: `dubs.test.mjs`, `test_video_reviews.py`,
  `admin-video-reviews.test.tsx`; each fails without its change.
- [x] Docs.

## How to verify

`node --test tools/video/dubs/dubs.test.mjs`;
`cd apps/api && uv run pytest tests/test_video_reviews.py -k languages_once`;
`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`.

## Notes

- Pull request: #1482 (https://github.com/x812033727/travel_scanner/pull/1482).

- Brand stories (`story`) are narrator-only in sound (their recurring figures are drawn, never
  heard; `core/story.mjs` refuses any other speaker), so `hasCast` would have refused them while
  the speaker test accepts them. They stay out of the server and page sets because their zh-TW
  subtitles are burned in: task `2026-10-13-should-brand-stories-be-dubbed-over` asks the owner.
- The old refusal was a UsageError (exit 2), which `makeDub` turns into a block of the whole video;
  only exit 3 is a skipped dub. The new refusal is exit 3 on purpose.
- The automated explainer route writes no category, so its dramas are uncategorised until the
  owner files them under 觀念解說: task `2026-10-13-explainer-route-files-its-drama-under`.
- Bound by the duration receipt and changed here: `apps/api/app/video_reviews/admin_service.py`,
  `apps/web/components/admin-video-reviews.test.tsx`, `tools/video/dubs/dubs.test.mjs`.
  `long-form/cli.mjs check` and `long-form/review.test.mjs` fail on exactly these until the
  increment lands.
- `2026-10-12-let-managers-link-a-private-studio` still reads in-progress over the admin files,
  but its PR #1475 merged on 2026-10-12; the claim here was forced for that reason.
