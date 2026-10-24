---
id: 2026-10-11-image-status-reads-slides-image-key
title: keyframes --dry-run: imageStatus reads the key state from status.slides_image too
status: done
priority: P3
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:21:56Z
created_at: 2026-10-11T04:03:36Z
completed_at: 2026-10-24T13:22:17Z
branch: codex/open-tasks-reconcile-20261024
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
---

# keyframes --dry-run: imageStatus reads the key state from status.slides_image too

## Why

For a video whose `series.json` names an image model, `imageStatus` in
`tools/video/media/stages.mjs` looks for the vendor's key state only among `status.image`,
`status.clip` and `status.music`. On a site whose only MiniMax choice is the slides' image
model (the production site: `slides_image_model` is `image-01`, the drama's is Gemini), the dry
run of a cute explainer therefore prints
`server: minimax image-01 (provider key checked on submit)` instead of `ready`, although the
key is there ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 8). Cosmetic: filing already checked the
key. It also means a missing key is not reported as NO KEY by the dry run.

## Definition of done

- [x] `imageStatus` also reads the vendor's key state from `status.slides_image`, so the dry
      run says `ready` or NO KEY for a model whose vendor is configured only there.
- [x] A unit case in `stages.test.mjs`. Any test that pins the
      `(provider key checked on submit)` line for that situation is updated on purpose.

## Steps

- [ ] Read `imageStatus` after `2026-10-11-explainer-request-names-its-image-model` has landed (it adds a unit case there).

## How to verify

`node --test tools/video/media/stages.test.mjs`; `node tools/video/cli.mjs keyframes --dry-run`
on a cute explainer prints `minimax image-01 ready`.

## Notes

- 2026-10-24: Included `slides_image` in the existing provider-matched boolean
  credential lookup. A present `false` stays false; genuinely unknown vendors
  still defer the key check to the API. Other media choices are unchanged.
- The existing cross-vendor regression now covers both true/false slides-only
  credentials. It failed with `configured: null` on old source, then the complete
  `stages.test.mjs` passed 24/24 with zero skips on bundled Node 24.19.0.
  No key, provider, host setting or paid media request was changed.

- 2026-10-11 filed from the design's section 7, item 8.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- - [ ] `imageStatus` also reads the vendor's key state from `status.slides_image`, so the dry
- - [ ] A unit case in `stages.test.mjs`. Any test that pins the
- 2026-10-24 execution: slides_image key fallback added;24 tests passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
