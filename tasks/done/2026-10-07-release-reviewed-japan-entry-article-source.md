---
id: 2026-10-07-release-reviewed-japan-entry-article-source
title: Release reviewed Japan entry article source and missing locales
status: done
priority: P1
area: docs
owner: codex-gpt6-root-release
claimed_at: 2026-10-08T07:46:49Z
created_at: 2026-10-07T16:50:42Z
completed_at: 2026-10-09T12:23:58Z
branch: codex/article-locales-wave4-release-20261008
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

- [x] All four targets and final native images have genuine independent reviews;
      the exact content head passes CI and is approved and merged.
- [x] Fresh production snapshot/source/version/image guards match the reviewed intent.
- [x] Isolated rehearsal, dry-run and database backup complete before any real write.
- [x] Publish exactly four missing languages and the approved zh-TW correction using
      unchanged durable phases; replay creates no new versions and pending is empty.
- [x] Verify five public pages and ten personally inspected desktop/mobile views,
      including native glyphs/media/body, canonical/hreflang, routes and sitemap.
- [x] Clear only the owned release hold and record actual public completion in the
      ledger and sanitized release README/evidence before closing this task.

## Steps

- [x] File the narrow release task and its existing authoring dependency.
- [x] Bind final reviewed bundle and exact PR/SHA; obtain the concrete release choice.
- [x] Revalidate/rehearse/back up/publish/replay, then prove public acceptance.

## How to verify

Use article-localization, deploy and ops/release hold workflows without --force or
--ignore-hold. Recompute current reviewed document/asset/source-correction bindings;
verify the actual journal and all five public language documents after publication.

## Notes

- Source review SHA:
  `9ec315b0adeb31ea3d2f9ecd1ae236960cdfe54d4144b2f18d011421faa6f4e4`.
  Desired canonical zh-TW source:
  `4709f8e36b080bc76a1703704db2744b28409fcc31289eebf5c3105c7ca3f3c5`.
- Source intent includes ten document leaves, one visible SVG text label and one accessible SVG description. The
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
  Scoped pack lint and translation checks passed at authoring. The subsequent
  explicit owner approval and actual release are recorded below.

## Actual release completion

- Owner approved PR #1374 at `a80e9cb55d3174fc0bdfaa56d00ccf580866345c` for
  normal main integration, merge, deployment and publication of 13 articles,
  52 new locales and seven reviewed zh-TW source corrections. The integrated
  head `271efebb21460a271913623b1913daf7722510d6` preserved all approved content
  and passed all 22 CI checks; merge/deployment was
  `c6454463d0eb53e4c8166be0b93a587598c03208`.
- All nine durable phases completed with two settled production journals, a
  consistent 161-table backup and genuine isolated restore/replay verification.
  Preserve the first read-only capture failure and its capture-only recovery,
  plus the observed users-row publication lock and explicit journal resumption
  after five committed operations. No automatic retry, force or hold bypass.
- Actual public acceptance covered 65 five-language pages, 130 personally
  inspected desktop/mobile originals and 187 raw media files. The source media
  guards contain 38 unchanged originals and one approved Japan SVG replacement.
  Only this driver's owned hold was cleared.
- Independent postpublication audit SHA
  `38501204a086da589f32bedbe77b819f8bcf5dad41a3fb57a54727aad02eb866`
  passed with no open finding and preserved the prior 44 articles/220 documents.
  One Root completion-ledger CAS appended this release; actual after SHA
  `3df618ed6f2c6142eddf50d31d0b57fdf4af95088b0c5e4aa9b72d8526f5f7da`.
  Total published localization: 57 articles and 228 new language documents.
- Global links checks actually exit 1; the life cohort has nine unpublished
  related-target findings per new locale, rendered as plain text by the frontend.
  Japan has no selected finding. Preserve this limitation and leave remaining
  localization work open. The observed 2026-10-08 20:02 Asia/Taipei census has
  805 incomplete articles and 3,220 missing language documents.
- The private record validators' original schema failures are preserved.
  Read-only compatibility fixes use the authentic journal/deployment fields and
  strengthen original raw deployment receipt bindings; they do not rerun release
  phases, edit original receipts or add publication targets.
- Sanitized scoped README and evidence: `docs/article-localization/releases/wave4-japan-entry-20261007/`.
  Full raw snapshots, screenshots, journals and failed attempts remain outside Git.
