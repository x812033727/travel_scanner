---
id: 2026-10-11-cute-explainers-own-series-prompts
title: Cute explainers are written from their own series' prompts; the request form offers cute-cartoon and cute-mystery
status: in-progress
priority: P2
area: tools
owner: claude-opus-explainer-pr3
claimed_at: 2026-10-11T10:45:22Z
created_at: 2026-10-11T04:01:38Z
completed_at:
branch: claude/explainer-series-prompts
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/explainer-family.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/explainer-cute.test.mjs
  - tools/video/core/explainer-family.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-settings-drama.tsx
  - apps/web/lib/video-presets.ts
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

- [x] New `tools/video/automation/explainer-series.mjs` with exactly the source of
      `prompt-texts.md` section 3 (LF, UTF-8, no BOM); the other changes of design 5.2 items 2
      to 8 (`instructionsFor`, `settle`, `variantOf`, `documentVariant`, `genre_spec: null` for a
      profiled explainer, the discussion variants, the cute card list, the picture-variety lint,
      the nine checks in `media/keyframes.mjs`, `REQUEST_PRESETS` with seven values). Hunks:
      `orders/pr3-on-6a26eff.diff` beside the design.
- [x] The ten new instruction digests are **recomputed from the committed file** and pinned
      (never copied from `orders/order-pr3.json`); the nine digests of existing texts
      (`prompt-texts.md` section 5) are unchanged.
- [x] The tests of design 5.3, including the fallback assertion for
      `instructionsFor("planner", "drama", "", "explainer-mystery")` and the re-pin of the
      request form to seven option values.
- [x] `acceptBestPictures` is left alone (design 5.2, option (b)): a cute explainer whose shot
      still fails after two prompt-fix rounds blocks with `prompt_fixes:keyframes` and waits for
      the owner's retry. `docs/videos/DRAMA-FLOW.md` section 二 says so.
- [x] No file that `prompts.mjs references()` reads is edited (design section 1), nor
      `apps/api/**`, `apps/web/messages/**`, `templates.mjs`, `lint.mjs`, `plans.json`.
- [ ] The duration receipt is re-issued for the 8 bound files of design 5.4 by an agent that
      did not write the change, and `node tools/video/long-form/cli.mjs check` passes.
- [ ] Deployed (web and worker tools in one release) and the host checks of design 5.7 items 1
      to 3 read; items 4 to 7 wait for the owner's first cute request.

## Steps

- [ ] Confirm pull request 2 is on main and on the host, and that no one-off row in a cute
      preset has an episode short of the script gate (design 5.7 item 1).
- [x] Read design sections 1, 2 and 5, `prompt-texts.md`, and `orders/order-pr3.json` for the
      test lists the design refers to. `orders/verify-pr3.mjs.txt` is the script the prototype
      was checked with: turn it into `node:test` cases group by group.
- [x] Apply the hunks by their quoted statements (the diff was made on a prototype of pull
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
- 2026-10-11 implemented on `claude/explainer-series-prompts` (pull request not opened by the
  implementer). Claimed with `--force`: the refusal named `2026-10-10-let-the-owner-re-request-a`,
  whose pull request #1432 is merged while its ticket is still in `tasks/open`.
- **One addition to the source of `prompt-texts.md` section 3**, asked by the reviewers of pull
  request 2: the two cute *writer* texts gain one bullet that says what the payload's top-level
  `prompt_budget_chars` is (the flat explainer's text explains the key only on `fix.targets`, and
  does not move). So `writer:explainer-cartoon` is 14,310 characters and `writer:explainer-mystery`
  16,423; the other eight texts hash exactly as `prompt-texts.md` section 4 lists them. All ten
  digests are pinned in `explainer-series.test.mjs`, computed from the committed file.
- Byte-stability: the first commit after the claim holds only tests, written and run on main
  before any code changed (`6c6b4e6f6`): the composed instructions of the existing explainer and
  discussion variants, bare, with a one-off's row and with standing instructions; the bible and
  bible-discussion payloads of a flat-explainer and of a story one-off; what `settle` keeps of a
  flat-explainer look; its six cards; its discuss variant; its scored judge rubric. They pass
  unedited after the change, as do `prompts.test.mjs`'s four pins and `series.test.mjs`
  `EXPLAINER_STAGE_PINS`.
- Also done here, from pull request 2's review: a test in `automation.test.mjs` where the
  writer's budget is not capped by the writer's own 1000 (793, 770 and 756 for the three presets
  under a MiniMax limit lowered for the test), so a wrong vendor or look turns it red; and the
  request form no longer offers "same as the drama settings" for a preset with a model of its own
  (`requestImageModel` returns `listed`; a default the catalogue lacks is listed by its id).
  The hold on the settings' default-style select (`DEFAULT_STYLE_HELD_PRESETS`) is removed.
- Tests of pull request 1 that pinned "a cute preset runs the explainer's stages" were changed on
  purpose: `automation/explainer-family.test.mjs`, `core/explainer-family.test.mjs` (a cute look
  now gets the two variety warnings on the flat fixture) and the two cute loop tests in
  `series.test.mjs`, replaced by one end-to-end run per cute preset.
- `node tools/video/long-form/cli.mjs check` is red on nine bound files and nothing else: the
  eight of design 5.4 and `tools/video/automation/automation.test.mjs` (the budget test). The
  receipt is the independent reviewer's to re-issue.
- Not done: the receipt, the deploy and the host checks; `npm run test:tools` whole (see the pull
  request text for what was run).
