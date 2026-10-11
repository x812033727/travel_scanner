---
id: 2026-10-11-settings-default-style-offers-explainer-presets
title: Decide whether the settings tab's default-style select should stop offering explainer presets
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-11T04:03:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-settings-drama.tsx
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
---

# Decide whether the settings tab's default-style select should stop offering explainer presets

## Why

The drama settings tab's default-style select is server-driven: it lists every name in the
API's `STYLE_PRESETS`, so it offers `flat-explainer` today and the two cute presets as soon as
pull request 1 of `2026-10-10-explainer-route-takes-a-series-look` is deployed ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 3.5 and section 7 item 12).
`settle()` falls back to the settings' preset when a request names none. An explainer preset as
the site-wide default would make every story request without its own preset a narrator-only
video with no cast, and before `2026-10-11-cute-explainers-own-series-prompts` a cute default would be written from So That's Why's
prompts. The design only warns the operator not to pick one; nothing refuses it.

## Definition of done

- [ ] A decision from the owner: keep offering them, or offer only the story presets as the
      default (the request, series and binge forms already choose per work).
- [ ] If they are removed: the settings API refuses an explainer preset as `drama_preset` with a
      message that says why, the select does not list them, and a row that already holds one is
      reported rather than silently changed.
- [ ] Tests on both sides (`settings.py` is bound by the duration receipt: re-issue it).

## Steps

- [ ] Read which row value the host holds now.

## How to verify

`cd apps/api && uv run pytest tests/test_video_automation_settings.py`; `/admin/videos`
settings tab lists only the story presets.

## Notes

- 2026-10-11 filed from the design's section 7, item 12.
