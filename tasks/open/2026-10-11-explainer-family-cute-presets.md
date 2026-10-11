---
id: 2026-10-11-explainer-family-cute-presets
title: Explainer family PR 1: cute-cartoon and cute-mystery presets on tools, API and web
status: in-progress
priority: P2
area: api
owner: claude-opus-explainer-pr1
claimed_at: 2026-10-11T03:57:49Z
created_at: 2026-10-11T03:57:19Z
completed_at:
branch: claude/explainer-presets
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/duration.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/branding.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/core/explainer-family.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/shorts/episode.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/explainer-family.test.mjs
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/migrations/versions/0130_video_cute_presets.py
  - apps/api/tests/test_migration_0130_video_cute_presets.py
  - apps/api/tests/test_video_explainer_family.py
  - apps/api/tests/test_video_explainer_duration.py
  - apps/web/lib/video-presets.ts
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-explainer-family.test.tsx
  - apps/web/components/admin-video-explainer-duration.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/videos/DRAMA.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Explainer family PR 1: cute-cartoon and cute-mystery presets on tools, API and web

First of the three pull requests of
[2026-10-10-explainer-route-takes-a-series-look](2026-10-10-explainer-route-takes-a-series-look.md).
It is a ticket of its own so that the parent does not hold `flow.mjs` and `prompts.mjs` for
three pull requests.

## Why

The host's explainer route knows one preset, `flat-explainer`, and every place that asks "is
this an explainer" compares with that one name. The owner decided on 2026-10-10 that two more
looks run on the same route: `cute-cartoon` (原來如此事務所, So That's Why redrawn as a cute
cartoon) and `cute-mystery` (奇聞檔案局, the history-and-curiosity series). Before either can be
given its own prompts or its own image model, the three sides have to know the names and agree
on two separate questions that today are one comparison:

- **the family**: is this a narrator-only explainer (no cast, stills only, 8 to 20 minutes, the
  question-shaped bible and brief)? All three presets are.
- **the identity**: whose bookends, thumbnail and Shorts theme does it wear? `flat-explainer`
  and `cute-cartoon` are So That's Why's; `cute-mystery` wears the channel's until that series
  has an identity of its own.

The owner's fourth decision bounds the work: nothing that exists may move. `flat-explainer`'s
preset text, prompts, payloads, look hash, image keys and unfinished journals stay byte for byte.

## Definition of done

- [x] `cute-cartoon` and `cute-mystery` are presets in the tools (the two decided look texts,
      positive only), in the API (the ORM tuple, the schema's Literal, the three CHECK
      constraints through migration 0130) and in the web's labels (three blocks, five locales).
- [x] Every "is an explainer" site asks the family (`isExplainerPreset` / `is_explainer_preset`)
      and the three identity sites ask `explainerSeries`; a test refuses a bare comparison with
      `flat-explainer` in the tools.
- [x] The request form on /admin/videos still offers five style options: the cute presets are
      held back until the pull request that gives them their prompts. A test pins the hold.
- [x] Once a one-off's bible is written it can no longer move between two different explainer
      presets (409 `video_series_explainer_fixed`), as it already could not cross between an
      explainer and a story.
- [x] `flat-explainer` did not move: its preset bytes, look hash, visual hash, composed prompt,
      image keys, the four instruction texts, the three stage calls of a one-off and a bible
      job's inputs are pinned by digest, recorded on main before the change and green after it.
- [ ] The duration receipt (`docs/videos/long-form/review.json`, `review.md`) is re-issued for
      the 20 bound files by an agent that did not write this change.
- [ ] Merged, deployed with web, API and tools in one deploy, and the host checks below pass.

## Steps

- [x] Pin-only tests on main, seen green, committed alone.
- [x] Tools: `PRESETS`, `EXPLAINER_PRESETS`, `isExplainerPreset`, `explainerSeries`, and the
      sites in `core/{drama,duration,lint,branding}.mjs`, `render/plan.mjs`,
      `shorts/episode.mjs`, `automation/{series,flow}.mjs`.
- [x] API: `models.STYLE_PRESETS`, `schemas.StylePreset` / `EXPLAINER_PRESETS` /
      `is_explainer_preset`, `series.py`, migration `0130_video_cute_presets` and its tests.
- [x] Web: `lib/video-presets.ts`, `STYLE_PRESETS`, `requestMinutes`, 30 label strings.
- [x] `docs/videos/DRAMA.md` `look` row.
- [ ] Receipt re-issued by an independent reviewer; `node tools/video/long-form/cli.mjs check` green.
- [ ] Before merge: `git fetch` and `uv run alembic heads` again (see the note on the number).

## How to verify

```bash
node --test tools/video/core/explainer-family.test.mjs tools/video/automation/explainer-family.test.mjs \
  tools/video/core/duration.test.mjs tools/video/core/branding.test.mjs \
  tools/video/automation/prompts.test.mjs tools/video/automation/series.test.mjs
cd apps/web && npx vitest run components/admin-video-explainer-family.test.tsx \
  components/admin-video-explainer-duration.test.tsx components/admin-video-series.test.tsx \
  components/admin-video-reviews.test.tsx
cd apps/api && uv run alembic heads && uv run pytest tests/test_video_explainer_family.py \
  tests/test_video_explainer_duration.py tests/test_video_series.py tests/test_schema.py
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0130_video_cute_presets.py   # needs PostgreSQL
```

On the host after the deploy (read-only):

1. `alembic current` prints the new head; `/ready` is 200.
2. `SELECT conrelid::regclass, conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conname IN ('ck_video_drama_preset','ck_video_drama_request_style','ck_video_drama_series_style');`
   lists seven presets on each of the three.
3. The per-preset row counts of `video_drama_requests`, `video_drama_series` and the settings
   row equal the numbers noted before the deploy; no row uses a cute preset.
4. /admin/videos: the settings' default-style select shows the two new labels and no raw key;
   the request form has five style options; the series and binge forms four.
5. In the worker's checkout:
   `node -e "import('./tools/video/core/drama.mjs').then((m) => console.log(m.EXPLAINER_PRESETS.join(','), m.lookHash({ format: 'drama', look: { preset: 'flat-explainer' }, characters: [] }), m.resolveLook({ preset: 'cute-mystery' }).negative === ''))"`
   prints `flat-explainer,cute-cartoon,cute-mystery bd2b3b49af8e9623 true`.
6. The worker's log has no `video_ai_receipt_input_changed` and no `must be one of` look error.

## Notes

- **Migration number.** Main's head is `0128_video_languages_four`. `0129` is taken by the open
  pull request #1432 (`claude/dub-retry-request`, `0129_video_dub_retries`, also revising 0128;
  all its checks were green and it was only behind main when this was written), so this
  migration is `0130_video_cute_presets`. It revises `0128_video_languages_four` for now,
  because 0129 is not on this branch and a `down_revision` that does not exist breaks every
  test module. **Whichever of the two merges second has to re-point**: if #1432 merges first,
  change this file's `Revises:` line and `down_revision` to `0129_video_dub_retries` (nothing
  else: the number, the file name and the test constants already fit); if this merges first,
  #1432 renumbers to 0131 and revises 0130. `tests/test_schema.py` goes red on two heads, so
  it cannot be missed.
- **Deploy.** Web, API and tools in one deploy. Every machine that runs the worker pulls the
  tools before any cute row exists: an old worker would take a cute one-off as a story, pay for
  a bible with a cast and be refused each round. Do not pick a cute preset as the drama default
  in the settings tab before the prompts pull request: that select is server-driven and lists
  the two as soon as the API does, and `settle()` falls back to the settings' preset. Do not
  file a cute request by a direct API call either: until the prompts land it is written from
  So That's Why's prompts and drawn by the settings' image model.
- **Rollback.** The previous release reads the upgraded database while no row uses a cute name;
  if one does, its list endpoints answer 500 until that row is changed. The downgrade refuses
  while such a row exists.
- **Not edited on purpose.** `.agents/skills/youtube-video/references/drama.md` (it is read
  into every drama payload, so one changed byte re-keys every unfinished drama stage),
  `tools/video/templates/templates.mjs`, `tools/video/long-form/{plans,admin-catalog}.mjs` and
  `docs/videos/long-form/plans.json` (the 192 planned episodes stay on `flat-explainer`), and
  the receipt (`review.json`, `review.md`: they are in this ticket's scope for the reviewer).
- **`settle()` line that reads the settled look.** `settled.characters = isExplainerPreset(settled.look?.preset) ? [] : ...`
  reads the writer's own preset for a non-explainer request, so a story writer that answers
  `look.preset: "cute-cartoon"` has its cast emptied exactly as one answering `"flat-explainer"`
  does today. Existing behaviour, now three names wide; left as it is.
- **What a cute request does until the prompts land.** It runs the `bible-explainer` and
  `explainer` variants unchanged (the writer is told to answer `look.preset: "flat-explainer"`,
  and `settle()` writes the request's preset back). A `cute-mystery` video is therefore briefed
  with So That's Why's thumbnail on the channel's layout, which QA refuses. That is why the form
  holds the presets back.
- **The payload digests were measured on Windows** (`series.test.mjs`
  `EXPLAINER_STAGE_PINS`). If Linux CI disagrees on a payload digest and not on the
  instructions digest, pin `Object.keys(payload).sort()` and `payload.drama_settings` instead.
- **The "no bare comparison" test** sees `===` and `!==` beside `EXPLAINER_PRESET` or the
  literal only; it does not see `.includes("flat-explainer")`, a `switch` or a `Set`.
- **Claimed with `--force`.** The refusal named `2026-10-10-photo-paste-card`, whose pull request
  #1425 is merged; its ticket is still in `tasks/open` and overlaps `render/plan.mjs` and
  `core/lint.mjs`.
- Follow-ups nobody has filed yet (from the design): `screenshot` and `photo` cards for the
  host's explainer writer; 奇聞檔案局's own intro, thumbnail series and Shorts theme (until then
  its Shorts carry the `illustrated` series).
