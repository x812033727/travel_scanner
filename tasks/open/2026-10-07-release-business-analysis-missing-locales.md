---
id: 2026-10-07-release-business-analysis-missing-locales
title: Release business analysis missing locales
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-07T06:35:38Z
completed_at:
branch:
depends_on:
  - 2026-10-07-recheck-business-models-and-five-forces
  - 2026-10-07-recheck-pestle-and-swot-locales
scope:
  - docs/article-localization/releases/2026-10-07-business-analysis-wave
---

# Release business analysis missing locales

## Why

Four public life articles have complete, independently reviewed repository
translations but still lack English, Japanese, Korean and Simplified Chinese
publication in the retained production snapshot. Publish those sixteen missing
documents through the existing guarded Route B flow.

## Definition of done

- [ ] Verify exact content PR/SHA approval, merge and actual deployed pack/asset bytes.
- [ ] Capture a fresh full database baseline and confirm all sixteen selected targets remain missing and sources unchanged.
- [ ] Compile a new manifest from final Git candidates and the genuine independent reviews.
- [ ] Obtain publication approval after real backup/restore, runtime proof and the actual dry-run.
- [ ] Publish with durable guards, verify all sixteen public pages and refresh the overall missing-language inventory.

## Steps

- [ ] Merge/deploy the reviewed content/evidence PR after exact-head checks.
- [ ] Recheck current source, target, draft, version, visibility, expiry and hold state.
- [ ] Compile, verify, rehearse, back up and present the exact production operation plan.
- [ ] Execute approved phases and byte-identical replay; verify real pages/images/canonical/hreflang/links on desktop and mobile.

## How to verify

Use `prepare_route_b_bundle.py`, `publish_bundle.py` and `report_progress.py`.
Bind all source/document/image hashes to genuine review rows with their actual
translator, reviewer and review time. A public GET cannot prove absence of private
draft rows; the release requires a fresh database-backed baseline. Do not select
zh-TW, existing published targets, source holds or articles outside this cohort.

## Notes

Selected slugs: `business-models-b2b-d2c`, `porter-five-forces`,
`pestle-business-scan`, `swot-tows-action-plan`; four missing locales each.
Fresh source/asset/public target safety plan SHA
`50fd8c5c08558acb95ecc2fe10d66b4e36d2217e84db2c1472ff91980d71fe9a`.
Business/Five Forces independent eight-target review SHA
`46dc2bb0461d3f01b2796ee30100a921217ad78c64be63bc29e4a6f72da4c0a4`;
PESTLE/SWOT independent eight-target review SHA
`c6402686d5f3fc348d05ef10235bffec78b5207f2ceee7f7ab7a83b55076448b`.
The authoring tickets record three exact Business EN/JA diagram corrections;
all original source documents, source artwork, credits and root metadata remain
unchanged. This is separate from PR #1365 and the Japan refund source-correction
release. No production import or publication has occurred.
