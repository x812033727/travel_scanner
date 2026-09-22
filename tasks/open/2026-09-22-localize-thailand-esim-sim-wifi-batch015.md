---
id: 2026-09-22-localize-thailand-esim-sim-wifi-batch015
title: Localize Thailand eSIM SIM and WiFi guide in four missing languages
status: review
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

- [x] en, ja, ko and zh-CN contain complete translations of published zh-TW v8,
      including all blocks, tables, links, sources, alt/captions and conditions.
- [x] Four language-suffixed SVGs translate all visible text and accessibility
      metadata, preserve numeric branches and pass independent desktop/mobile render review.
- [x] The repository-only zh-TW AIO description remains byte-for-byte represented by
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
- [x] Draft and independently review the four documents and four SVGs.
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
- **Historical HOLD and narrowed scope:** preparation initially stopped because the
  current canonical assembler/publisher cannot simultaneously preserve the repository-
  only zh-TW description, prove full ArticlePack equality, and protect live zh-TW v8.
  The release owner later authorized translation, independent review and a draft content
  PR in parallel with the guard fix. Canonical release assembly, import and publication
  remain blocked on that independently reviewed guard. Never replace the repository
  description with live text, alter baseline hashes, or select/publish zh-TW.
- Fresh collision check found no open PR touching this slug and no active task scope
  overlap. The blocked AIO task mentions this slug but scopes only its own task file.
- Final document reviews: en raw `07b55d3561aaf33907f0a1da7b6520dc378ea4d14092364f8ba9bf1733a252f3`
  (`en-receipt-pass.json` SHA `c1236d2c6b9fcc2db63bf9b6d14f383bf542bfb08747fb8141f6edaba213f219`
  plus source-observation supplement SHA
  `b8d49c485cc034f85fca756a420f691853a736ce85ff59a94b1b2a00dec9012c`);
  ja raw `e46caece4393ad313d75930c07d01e505b56458cf5576f930ba45c6747074a6a`
  (full review SHA `89bdfef55fb677a121dc213c61496d298af89a6f2af9936be85158a772fa7815`,
  v4 supplement SHA `a76f1605066fc7aa29d1d90bdaa702524f13f54f6d42985151fe9ff40e307d22`);
  ko raw
  `6d621be93c98850396f59a1d7803a9b67df59fb66adc7551953221db536af8e3`
  (review SHA `7cbb3e995df3a16ee78613097973337f6bfac5cc919d35c0af317c45dc70bebd`);
  zh-CN raw
  `92029e44cb4de28f49ae8739297339d8318209d514c72806e79a0ad438bc9390`
  (review SHA `bc473091635ff44c8f6e9289a211b5cae6048dbeba71851e6e1c8833197a0d0f`).
  All four preserve the Taiwan-number/carrier audience,
  non-Thai passport rules, separate 60-day conditions and every table/source/link.
- A source observation found that published zh-TW v8 says to turn airplane mode off and
  then on. Translations use a neutral toggle without treating that as a source correction.
  Follow-up task `2026-09-22-review-thailand-airplane-mode-source` is unowned, blocked on
  this batch and requires primary-source verification plus independent review.
- Final SVG candidate: `svg-candidate-freeze-v4.json` SHA
  `baabd3fd1b430fda8a63c97cf789183630c8d7c380402c025a5050948652b32d`;
  exact v3-to-v4 delta SHA
  `12e95229ae4542b7d3b623d334e5cea56e07f6da202588588af3dc5a3c6b394a`.
  Independent receipt `svg-receipt-pass-v4.json` SHA
  `562a36769185b8144a1fd2a79dac2175b08cd3bfde790516fdcd4d3e4a1e60fa`
  binds all four SVGs, approved descriptions, numeric coverage and 16 desktop/mobile
  renders. Every prior WITHHOLD version and its evidence remains preserved outside Git.
- Scoped `ArticlePack` validation and `pack_cli lint --slug thailand-esim-sim-wifi`
  pass with only the source-structure summary warnings and the English length guideline.
