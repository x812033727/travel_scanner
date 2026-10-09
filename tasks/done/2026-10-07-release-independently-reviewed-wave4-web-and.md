---
id: 2026-10-07-release-independently-reviewed-wave4-web-and
title: Release independently reviewed wave4 web and life article locales
status: done
priority: P1
area: docs
owner: codex-gpt6-root-release
claimed_at: 2026-10-08T07:46:40Z
created_at: 2026-10-07T16:42:11Z
completed_at: 2026-10-09T12:23:51Z
branch: codex/article-locales-wave4-release-20261008
depends_on:
  - 2026-10-07-localize-twelve-web-design-and-seo
scope:
  - docs/article-localization/releases/wave4-web-life-20261007
---

# Release independently reviewed wave4 web and life article locales

## Why

Twelve published life articles now have independently reviewed en, ja, ko and
zh-CN translations in the content worktree. Six require separately reviewed exact
zh-TW source corrections. Local assembly and installation do not publish them.
Release only this selected cohort after its exact content PR is approved and merged.

## Definition of done

- [x] Record the merged content PR and exact deployment approval and deployed SHA.
- [x] Reconcile a fresh production snapshot with all original source/version guards;
      recompile the reviewed bundle without expanding the authorized cohort.
- [x] Isolated rehearsal, dry-run and database backup succeed before production writes.
- [x] Publish 48 new language documents and six reviewed source corrections through
      unchanged durable phases; replay writes no new versions and pending is empty.
- [x] Verify all five public languages on desktop/mobile with real native screenshot
      review, body/media hashes, canonical/hreflang/routes and complete sitemap evidence.
- [x] Preserve actual link-check limitations, clear only the driver-owned hold and
      append verified publication to the existing completion ledger.
- [x] Save sanitized README/evidence records in this release scope and close only
      after the real release and public acceptance complete.

## Steps

- [x] File a narrow release task dependent on the twelve-article authoring task.
- [x] Approve/merge the exact content head and perform guarded normal deployment.
- [x] Revalidate, rehearse, back up, publish, replay and verify the actual public cohort.
- [x] Record actual completion; keep the global remaining-language task open.

## How to verify

Follow article-localization and deploy skills, the unchanged bundle publisher and
ops/release hold protocol. Bind every selected document, asset, reviewer and journal
to exact digests. Final evidence includes 60 public pages and 120 genuinely inspected
desktop/mobile views for this twelve-article cohort, with preserved existing languages.

## Notes

- Authoring bundle manifest:
  `a175e63ec2a7ef5b845e5416bd3b6f4f0a41ca8e2b90f9428ddb5cd8d6e2594c`.
  It has 12 articles, 156 assets and six independent source-correction reviews.
- All 48 targets passed genuine full text/native image/glyph/link review. Local
  install/replay and content checks succeeded; those are authoring evidence only.
- The authoring checkpoint preceded deployment and publication. The owner later
  explicitly approved the exact 13-article aggregate in PR #1374; the prior
  32-article approval was not used to authorize this release.
- Keep original dated sources, failed attempts, STOP/uncertain provider requests and
  all unrelated content/video/settings unchanged unless separately authorized.

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
- Sanitized scoped README and evidence: `docs/article-localization/releases/wave4-web-life-20261007/`.
  Full raw snapshots, screenshots, journals and failed attempts remain outside Git.
