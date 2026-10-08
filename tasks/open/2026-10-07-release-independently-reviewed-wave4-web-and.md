---
id: 2026-10-07-release-independently-reviewed-wave4-web-and
title: Release independently reviewed wave4 web and life article locales
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T16:42:11Z
completed_at:
branch:
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

- [ ] Record the merged content PR and exact deployment approval and deployed SHA.
- [ ] Reconcile a fresh production snapshot with all original source/version guards;
      recompile the reviewed bundle without expanding the authorized cohort.
- [ ] Isolated rehearsal, dry-run and database backup succeed before production writes.
- [ ] Publish 48 new language documents and six reviewed source corrections through
      unchanged durable phases; replay writes no new versions and pending is empty.
- [ ] Verify all five public languages on desktop/mobile with real native screenshot
      review, body/media hashes, canonical/hreflang/routes and complete sitemap evidence.
- [ ] Preserve actual link-check limitations, clear only the driver-owned hold and
      append verified publication to the existing completion ledger.
- [ ] Save sanitized README/evidence records in this release scope and close only
      after the real release and public acceptance complete.

## Steps

- [x] File a narrow release task dependent on the twelve-article authoring task.
- [ ] Approve/merge the exact content head and perform guarded normal deployment.
- [ ] Revalidate, rehearse, back up, publish, replay and verify the actual public cohort.
- [ ] Record actual completion; keep the global remaining-language task open.

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
- No deployment, production publication, public acceptance or release claim exists
  for this cohort. The owner's completed 32-article approval does not expand it.
- Keep original dated sources, failed attempts, STOP/uncertain provider requests and
  all unrelated content/video/settings unchanged unless separately authorized.
