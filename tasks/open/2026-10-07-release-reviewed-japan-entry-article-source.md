---
id: 2026-10-07-release-reviewed-japan-entry-article-source
title: Release reviewed Japan entry article source and missing locales
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T16:50:42Z
completed_at:
branch:
depends_on:
  - 2026-10-07-correct-japan-entry-customs-source-before
scope:
  - docs/article-localization/releases/wave4-japan-entry-20261007
---

# Release reviewed Japan entry article source and missing locales

## Why

The published Japan entry article needs an independently reviewed exact source
correction and four missing language documents. The authoring task preserves all
original versions, photographs and metadata and binds each target to genuine reviews.
Release only after the exact content PR and normal deployment receive owner approval.

## Definition of done

- [ ] All four targets and final native images have genuine independent reviews;
      the exact content head passes CI and is approved and merged.
- [ ] Fresh production snapshot/source/version/image guards match the reviewed intent.
- [ ] Isolated rehearsal, dry-run and database backup complete before any real write.
- [ ] Publish exactly four missing languages and the approved zh-TW correction using
      unchanged durable phases; replay creates no new versions and pending is empty.
- [ ] Verify five public pages and ten personally inspected desktop/mobile views,
      including native glyphs/media/body, canonical/hreflang, routes and sitemap.
- [ ] Clear only the owned release hold and record actual public completion in the
      ledger and sanitized release README/evidence before closing this task.

## Steps

- [x] File the narrow release task and its existing authoring dependency.
- [ ] Bind final reviewed bundle and exact PR/SHA; obtain the concrete release choice.
- [ ] Revalidate/rehearse/back up/publish/replay, then prove public acceptance.

## How to verify

Use article-localization, deploy and ops/release hold workflows without --force or
--ignore-hold. Recompute current reviewed document/asset/source-correction bindings;
verify the actual journal and all five public language documents after publication.

## Notes

- Source review SHA:
  `9ec315b0adeb31ea3d2f9ecd1ae236960cdfe54d4144b2f18d011421faa6f4e4`.
  Desired canonical zh-TW source:
  `4709f8e36b080bc76a1703704db2744b28409fcc31289eebf5c3105c7ca3f3c5`.
- Source intent includes ten document leaves and two original SVG text slots. The
  existing repository answer-first description is explicitly included in that review.
- Preserve original source cutoff, all citation dates except approved sources/8,
  original photographs, original versions, valid_until and unrelated metadata.
- Four original provider attempts and all local validation/render failures remain
  preserved. Local repairs and rendered state do not establish publication.
- This cohort remains separate from the completed 32-article owner approval.
- All four genuine final reviews and the unchanged official assembler now passed.
  Authoring manifest:
  `fc048145476869d1e7ec5fffba794908d0b58065fcb84b04477a3ea046791a3c`.
  One pack and seven assets were installed with8 verified journal operations.
  Identical replay and original photograph/metadata preservation passed; authoring
  completion receipt SHA:
  `c83c899a2606f17aed486197dd7bc77d5a6d0d1b6d8001ce0bd6eeafcd97ca2a`.
  Scoped pack lint and translation checks passed. Content PR/SHA, owner release
  choice, production rehearsal/backup/phases and public acceptance remain pending.
