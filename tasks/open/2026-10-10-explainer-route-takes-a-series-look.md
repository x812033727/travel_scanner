---
id: 2026-10-10-explainer-route-takes-a-series-look
title: Explainer route: a series' own look, pillars and image model (MiniMax) instead of So That's Why's
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T16:20:00Z
completed_at:
branch:
depends_on:
scope:
  - docs/videos/explainer-route
---

# Explainer route: a series' own look, pillars and image model (MiniMax) instead of So That's Why's

## Why

The host's explainer route (`style_preset: "flat-explainer"`, migration 0113; prompts
`planner:bible-explainer` → `writer:explainer` → `verifier:explainer` in
`tools/video/automation/prompts.mjs`) is written for one series: `EXPLAINER_COMMON` names
docs/videos/so-thats-why/, the thumbnail's `tag` is one of 商業／科學／旅遊／科技, the look is the
`flat-explainer` preset, and its pictures are drawn with the drama settings' image model
(Gemini 3 Pro, US$0.134 a picture) unless the video is an episode of a series that names its
own `image_model` (`jobs.series_image_model`); a one-off request (`DramaRequestIn`) cannot name
one. On 2026-10-10 the owner decided two things the route cannot do: a new history-and-curiosity
series (docs/videos/history-curiosity/README.md) in a cute cartoon look drawn by MiniMax
`image-01`, and So That's Why itself redrawn by MiniMax in the same look family. Both must run
on the host once their local pilots pass.

## Definition of done

- [ ] Two new style presets for the explainer family, named once the owner picks from
      docs/videos/history-curiosity/look.md (working names `cute-cartoon` for So That's Why and
      `cute-mystery` for history-and-curiosity): `PRESETS` in `tools/video/core/drama.mjs`
      (style text positive-only, `negative: ""`, MiniMax takes no negative), the three
      `style_preset` CHECK constraints recreated by a migration like 0113, `StylePreset` in
      schemas.py, the settings and series forms' preset lists and their five `admin.json`
      labels. `isExplainer`, `EXPLAINER_PRESET` checks and `settle()` treat the new presets as
      explainers (narrator only, stills, no cast, the 8-minute floor).
- [ ] `DramaRequestIn.image_model` (optional, `_known_image_model`), stored on the one-off
      series row the request becomes, so `jobs._model` draws it with that model; the request
      form on /admin/videos shows the field with the catalog's choices and prices.
- [ ] The explainer prompts take the series' brief from the payload instead of So That's Why's
      text: series name, pillars (the thumbnail `tag` values and `pillar` ids), the episode's
      shape (sections and lengths), the content rules (docs/videos/history-curiosity/README.md
      §內容守則 for the new series; So That's Why keeps its own), and the `look` to write.
      `EXPLAINER_CARD_TEMPLATES` gains `screenshot` (and `photo` once
      2026-10-10-photo-paste-card lands) so a real photograph may sit between the stills.
- [ ] `prompt_budget_chars` for an explainer counts MiniMax's 1,500-character limit when the
      request names `image-01` (media/prompt-budget.mjs already knows the vendor).
- [ ] Tests on both sides; `ops/release/README.md`'s migration rules followed (one head).

## Steps

- [ ] Read docs/videos/so-thats-why/README.md §製作怎麼接現有產線, DRAMA-FLOW.md, migration
      0113 and `tasks/done/2026-09-28-sothatswhy-explainer-preset.md` for how the first
      preset was threaded through.
- [ ] Presets and migration first (small, deployable alone); then `image_model` on the
      request; then the prompts.
- [ ] Verify on the host after deploy: file one explainer request with `image-01`, watch the
      worker's `keyframes --dry-run` line say `minimax image-01`, and the first picture's job
      row name that model.

## How to verify

`cd apps/api && uv run pytest tests/test_video_media_jobs.py tests/test_video_automation_settings.py`;
`node --test tools/video/core/drama.test.mjs tools/video/automation/flow.test.mjs`;
`npm run check:i18n`; on the host, `/admin/videos` shows the new presets and the image-model
field, and a request made with them draws with MiniMax.

## Notes

- 2026-10-11 the design is in the repository: [`docs/videos/explainer-route/`](../../docs/videos/explainer-route)
  (`DESIGN.md`, the owner's decisions in `DECISIONS.md`, pull request 3's prompt texts in
  `prompt-texts.md`, the three work orders under `orders/`). The work lands as three pull
  requests in this order, each deployed before the next starts, each with its own child ticket
  that holds its files; this ticket's `scope` was narrowed to the design folder so it no longer
  holds code:
  1. presets, migration and family recognition on tools, API and web (design section 3): its
     ticket is filed by its implementer on that pull request's branch;
  2. `2026-10-11-explainer-request-names-its-image-model` (section 4): the request's image model, `image-01` by default
     for the cute presets, the key check at filing;
  3. `2026-10-11-cute-explainers-own-series-prompts` (section 5): the series' own prompts and the two presets in
     the request form.
  This ticket closes when the three are deployed and the owner has filed the first cute request.
- 2026-10-11 what moved out of the definition of done above, and where it went:
  - the names are final (`cute-cartoon`, `cute-mystery`); the series and binge forms do not
    offer them (an explainer is a one-off) and the request form offers them from pull request 3;
  - the series' brief reaches the prompts from a registry in the tools keyed by preset, as
    instruction text, **not** from the payload (new variants, so `flat-explainer`'s bytes do not
    move);
  - `screenshot` and `photo` cards for the host's explainer writer:
    `2026-10-11-host-explainer-writer-image-cards` (the cute presets get `steps` and `table` instead);
  - So That's Why "redrawn by MiniMax" on the host: only new `cute-cartoon` requests; the 192
    planned episodes move in `2026-10-11-sothatswhy-planned-episodes-move-to-cute`;
  - 奇聞檔案局's own intro, thumbnail series and Shorts theme (it takes the channel's for now):
    `2026-10-11-curio-series-own-intro-thumbnail-shorts`;
  - a cute explainer's failing picture blocks instead of being kept as the best take:
    `2026-10-11-cute-explainer-keeps-best-take`;
  - found by the design and filed separately: `2026-10-11-series-endpoints-cute-default-and-key`,
    `2026-10-11-explainer-named-gemini-model-draws-at`, `2026-10-11-long-series-own-image-model-disagreement`,
    `2026-10-11-image-status-reads-slides-image-key`, `2026-10-11-hands-off-explainer-bible-judged-with`,
    `2026-10-11-explainer-docs-that-are-payload-or`, `2026-10-11-explainer-shorts-saved-before-the-checker`,
    `2026-10-11-settings-default-style-offers-explainer-presets`.
  - "How to verify" above names `tools/video/automation/flow.test.mjs`, which does not exist;
    each child ticket has its own commands.

- 2026-10-10 filed from the history-and-curiosity plan. Local pilots
  (`2026-10-10-history-curiosity-pilot`) run as illustrated slides and do not need this; the
  host does.
- The slides' own image model (`slides_image_model`) was already switched to `image-01` by the
  owner on 2026-10-04; this ticket is about the drama-shaped explainer route.
