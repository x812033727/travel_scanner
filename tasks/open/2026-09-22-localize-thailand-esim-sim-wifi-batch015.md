---
id: 2026-09-22-localize-thailand-esim-sim-wifi-batch015
title: Localize Thailand eSIM SIM and WiFi guide in four missing languages
status: in-progress
priority: P1
area: docs
owner: codex-batch015-thailand-pin
claimed_at: 2026-09-22T04:41:05Z
created_at: 2026-09-22T04:41:04Z
completed_at:
branch: codex/article-localization-batch015-thailand
depends_on: []
scope:
  - apps/api/app/guides/content/thailand-esim-sim-wifi.json
  - apps/web/public/guides/thailand-esim-sim-wifi
---

# Localize Thailand eSIM SIM and WiFi guide in four missing languages

## Why

The published `thailand-esim-sim-wifi` guide has only zh-TW. Add reviewed en, ja,
ko and zh-CN documents and localized diagram text without changing the existing
published zh-TW locale. The repository zh-TW document already contains an unpublished
answer-first description edit, so the release must preserve both facts: translations
are based on published zh-TW v8, while the final repository pack keeps the repository
description.

## Definition of done

- [ ] en, ja, ko and zh-CN contain complete translations of published zh-TW v8,
      including all blocks, tables, links, sources, alt/captions and conditions.
- [ ] Four language-suffixed SVGs translate all visible text and accessibility
      metadata, preserve numeric branches and pass independent desktop/mobile render review.
- [ ] The repository-only zh-TW AIO description remains byte-for-byte represented by
      the final full pack; zh-TW is excluded from import and publication.
- [ ] A narrow assembler/publisher guard independently proves full repository
      ArticlePack equality while source-version checks remain pinned to live zh-TW v8.
- [ ] Scoped lint, review, canonical bundle, rerun/version-conflict tests and release
      evidence pass before the draft PR advances to publication steps.

## Steps

- [x] Recheck current main, open PR file lists and active task scopes; claim the one-slug scope.
- [x] Capture a fresh complete production source in one repeatable-read, read-only transaction.
- [x] Freeze live/repository hash metadata and the exact `/description` divergence.
- [ ] Land and independently validate the narrow four-locale publication guard.
- [ ] Draft and independently review the four documents and four SVGs.
- [ ] Assemble, freeze and independently review the four-locale-only release wrapper.
- [ ] Open/update the narrow draft PR, then follow the authorized guarded release sequence.

## How to verify

Preparation evidence is outside the repository at
`C:\Users\x8120\.codex\article-localization-release\batch015`.

```text
npm run check:tasks
python -m json.tool C:\Users\x8120\.codex\article-localization-release\batch015\live-source.json
python -m json.tool C:\Users\x8120\.codex\article-localization-release\batch015\baseline-metadata.json
```

Later implementation must run the scoped content lint, numeric/link/description guards,
SVG render inspection, canonical assembler/publisher verification, synthetic rerun and
source-version conflict tests.

## Notes

- Worktree: `C:\Users\x8120\.codex\worktrees\article-localization-batch015-thailand`.
  Base: `c54fd5ca4754203f7d43315fa153ffc42fb06980`.
- Fresh production capture at `2026-09-22T12:42:01.818653+08:00`: article v2;
  only zh-TW locale v8/published v8; normalized source SHA-256
  `c1713cf8093002a714768c41cdb261612eee62214efaf9987a573ad5e328687b`.
- Repository pack SHA-256
  `819ec2536ba86f72eaf8a4dc93336db27e4b2c6312fad9f86be85c77979b99e3`;
  repository zh-TW normalized SHA-256
  `75849407039bd388311b54bc776f145c8816437a988f212050e9d12792047259`.
  After GuideDocument normalization, the only live/repository document difference is
  `/description`; blocks, sources, hero and image fields are equal.
- **HOLD:** the current canonical assembler/publisher cannot simultaneously preserve
  that repository-only zh-TW description, prove full ArticlePack equality, and protect
  the live zh-TW source. Do not replace the repository description with live text, edit
  baseline hashes, select/publish zh-TW, or draft translations until the narrow guard
  has an independent PASS receipt.
- Fresh collision check found no open PR touching this slug and no active task scope
  overlap. The blocked AIO task mentions this slug but scopes only its own task file.
