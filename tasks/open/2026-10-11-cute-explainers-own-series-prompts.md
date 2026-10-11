---
id: 2026-10-11-cute-explainers-own-series-prompts
title: Cute explainers are written from their own series' prompts; the request form offers cute-cartoon and cute-mystery
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:01:38Z
completed_at:
branch:
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/explainer-cute.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-explainer-family.test.tsx
  - apps/web/components/admin-video-request-image-model.test.tsx
  - docs/videos/DRAMA-FLOW.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Cute explainers are written from their own series' prompts; the request form offers cute-cartoon and cute-mystery

## Why

Pull request 3 of the three that make up `2026-10-10-explainer-route-takes-a-series-look` (the design is
[`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md), section 5; the texts are `prompt-texts.md` beside it). After pull
requests 1 and 2 the presets `cute-cartoon` (原來如此事務所) and `cute-mystery` (奇聞檔案局) exist
and are drawn by MiniMax `image-01`, but a request in either would still be planned, written and
fact-checked from the `flat-explainer` prompts, which name So That's Why's pillars and forbid the
chibi figures the cute looks ask for. This change gives each cute preset its own planner, writer,
verifier and discussion texts from one registry keyed by preset, lets them use `steps` and
`table` cards, judges their pictures with the nine yes/no checks, and adds the two presets to
the request form. `flat-explainer`'s prompt bytes do not move.

**Pull request 2 (`2026-10-11-explainer-request-names-its-image-model`) must have landed and been deployed first**, and pull request 1
before it.

## Definition of done

- [ ] New `tools/video/automation/explainer-series.mjs` with exactly the source of
      `prompt-texts.md` section 3 (LF, UTF-8, no BOM); the other changes of design 5.2 items 2
      to 8 (`instructionsFor`, `settle`, `variantOf`, `documentVariant`, `genre_spec: null` for a
      profiled explainer, the discussion variants, the cute card list, the picture-variety lint,
      the nine checks in `media/keyframes.mjs`, `REQUEST_PRESETS` with seven values). Hunks:
      `orders/pr3-on-6a26eff.diff` beside the design.
- [ ] The ten new instruction digests are **recomputed from the committed file** and pinned
      (never copied from `orders/order-pr3.json`); the nine digests of existing texts
      (`prompt-texts.md` section 5) are unchanged.
- [ ] The tests of design 5.3, including the fallback assertion for
      `instructionsFor("planner", "drama", "", "explainer-mystery")` and the re-pin of the
      request form to seven option values.
- [ ] `acceptBestPictures` is left alone (design 5.2, option (b)): a cute explainer whose shot
      still fails after two prompt-fix rounds blocks with `prompt_fixes:keyframes` and waits for
      the owner's retry. `docs/videos/DRAMA-FLOW.md` section 二 says so.
- [ ] No file that `prompts.mjs references()` reads is edited (design section 1), nor
      `apps/api/**`, `apps/web/messages/**`, `templates.mjs`, `lint.mjs`, `plans.json`.
- [ ] The duration receipt is re-issued for the 8 bound files of design 5.4 by an agent that
      did not write the change, and `node tools/video/long-form/cli.mjs check` passes.
- [ ] Deployed (web and worker tools in one release) and the host checks of design 5.7 items 1
      to 3 read; items 4 to 7 wait for the owner's first cute request.

## Steps

- [ ] Confirm pull request 2 is on main and on the host, and that no one-off row in a cute
      preset has an episode short of the script gate (design 5.7 item 1).
- [ ] Read design sections 1, 2 and 5, `prompt-texts.md`, and `orders/order-pr3.json` for the
      test lists the design refers to. `orders/verify-pr3.mjs.txt` is the script the prototype
      was checked with: turn it into `node:test` cases group by group.
- [ ] Apply the hunks by their quoted statements (the diff was made on a prototype of pull
      request 1; re-check each site against what actually merged).
- [ ] Run `npm run test:tools` whole once, without piping it through `tail`.
- [ ] Hand the receipt to an independent agent; then deploy.

## How to verify

`node --test tools/video/automation/explainer-series.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/series.test.mjs tools/video/automation/discuss.test.mjs tools/video/core/explainer-cute.test.mjs tools/video/media/look-keyframes.test.mjs`;
`npm run typecheck:web && npm run test:web`; `node tools/video/long-form/cli.mjs check`. On
the worker, the SHA-256 of `instructionsFor("writer", "drama", "", "explainer")` still starts
`185af9a7` and of `("planner", "drama", "", "bible-explainer")` `55ffd024`. On `/admin/videos`
the request form lists the two cute presets, minutes 8 to 20, `MiniMax image-01` preselected.

## Notes

- 2026-10-11 filed from the design. No host model has read the new texts: the first episode of
  each series is a pilot the owner reads at the bible and script gates, and it may block at
  keyframes (design 5.6). Every later wording change stops an unfinished cute run with
  `video_ai_receipt_input_changed`, never a `flat-explainer` one.
- Wording the owner may overrule at the first script gate (design section 9): 奇聞檔案局's
  likeness rule, the dropped 「示意」 label, the thumbnail tags 奇異現象 and 預言.
