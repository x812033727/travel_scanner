---
id: 2026-10-07-release-business-analysis-missing-locales
title: Release business analysis missing locales
status: in-progress
priority: P1
area: ops
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T13:21:54Z
created_at: 2026-10-07T06:35:38Z
completed_at:
branch: codex/article-locales-release-20261007
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

- [x] Verify exact content PR/SHA approval, merge and actual deployed pack/asset bytes.
- [x] Capture a fresh full database baseline and confirm all sixteen selected targets remain missing and sources unchanged.
- [x] Compile a new manifest from final Git candidates and the genuine independent reviews.
- [x] Verify the owner-approved publication plan against real backup/restore, runtime proof and the actual dry-run.
- [x] Publish with durable guards, verify all sixteen public pages and refresh the overall missing-language inventory.

## Steps

- [x] Merge/deploy the reviewed content/evidence PR after exact-head checks.
- [x] Recheck current source, target, draft, version, visibility, expiry and hold state.
- [x] Compile, verify, rehearse, back up and present the exact production operation plan.
- [x] Execute approved phases and verify zero database writes on replay, unchanged write-phase journal bytes and the genuine dry-run audit event; verify real pages/images/canonical/hreflang/links on desktop and mobile.

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

2026-10-07 update: the owner explicitly approved normal merge/deployment/publication
of all 32 articles. Revision `7524c25995d59f3826227e693d52f2ef5b3a19a2` is deployed;
the official verifier recorded 11 passes and zero failures, and actual container
reads matched the selected pack/asset bytes. Fresh baseline SHA is
`02c126e6a56a45544b0769b15cc18d74bb26af86420be3e6beda4712aa920054`.
The new first-life manifest retains all genuine review rows and includes these
four articles with the separate eight-article life cohort. Record only this
task's sixteen target operations. All production dry-runs and the full database
backup completed; real isolated restore/publication rehearsal is running.
Publication and public acceptance remain pending.

### Actual owner-approved publication and public acceptance

This scoped record is now backed by genuine publication: 4 articles, 16 previously missing languages, 0 approved source corrections and 16 selected publication operations. Normal deployment, the real restore/publication rehearsal and production replay passed. The original driver completed with exit 0 at 2026-10-07T15:40:06 UTC and cleared its owned hold after verified evidence transfer.

Public verification covered 20 five-language pages and 40 original desktop/mobile views in this record. Four actual independent reviewers read disjoint partitions; all document/image/DOM/canonical/hreflang/sitemap guards passed. The eight record outputs were validated and copied only into their existing claimed release scopes. Sanitized evidence is `docs/article-localization/releases/2026-10-07-business-analysis-wave/evidence.json`.

The full post-publication census observed 830 incomplete articles / 3,320 missing language documents. The global program remains open. All-guides link checks exited 1 in every locale; selected findings are exclusively unpublished related target languages. Actual per-record counts and this limitation are retained in evidence.json, rather than claiming an all-guides PASS. The earlier authoring/rehearsal notes above remain historical checkpoints. The record PR is the final documentation step.
