---
id: 2026-10-07-localize-singapore-entry-missing-locales
title: Localize Singapore entry information missing languages
status: done
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:34:59Z
created_at: 2026-10-07T05:34:58Z
completed_at: 2026-10-07T06:11:05Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/singapore-entry-2026-sg-arrival-card.json
  - apps/web/public/guides/singapore-entry-2026-sg-arrival-card
  - docs/article-localization/installations/singapore-entry-2026-sg-arrival-card.json
---

# Localize Singapore entry information missing languages

## Why

The eligible public Singapore entry article lacks en, ja, ko and zh-CN. Translate
every paragraph and diagram label while preserving the original Taiwan audience.

## Definition of done

- [x] Independently review four complete texts and rendered diagrams.
- [x] Install exact reviewed bundle preserving source, original assets and credits.
- [x] Hand off guarded publication/public verification to a separate release ticket.
- [ ] Merge reviewed content PR with required checks green.

## Steps

- [x] Pin current public source and assets; check active scopes.
- [x] Independently read source body/SVG and verify current primary rules.
- [x] Prepare four external CLI jobs, workers=3, retries=0.
- [x] Resolve precise field/layout issues, preserving attempts and immutable inputs.
- [x] Obtain genuine whole-document/image review and assemble/install.
- [x] File separate guarded release ticket; do not claim publication from install.

## How to verify

Use official pipeline, renderer, assembler and installer with hash-bound independent
review. Verify protected dates/amounts, article eligibility, original image bytes
and audience-specific rules. Refresh production inventory after publication.

## Notes

- Source SHA `da8e25410e593e7655d59c0477838e4a941fd5a6fbf8a3ea487ec346b5dfdeee`.
- Original pack SHA `54a4850e9697ff65e2d43d20d1874755cc4e8ca57e30ffdde83e49e831c44ae6`.
- Primary evidence and actual source-image review are in the private source audit.
- Four translation jobs completed with no automatic retry. Production writes: zero.
- All four whole-document/image reviews PASS; actual English signage remains
  original pixels with faithful translated alt/caption. Final SVG labels >=15px.
- Final combined review evidence SHA dcda1e387709f18e872237cb722a7a810f74ec90362e6224592b6299875d69e6.
- Combined official manifest c96737f04540a86d55d3f9e4b398bdb0ef5da602387d90d7052b0bfd02ae4cff.
- Installed pack 4755ccc9798a013ae9551d380f68563c794ce245538555467ea5fe73500aad48.
- Official receipt 1a72c899d21f2afb6b6e17d5949097e76f3008e63c73a8b282d2a01161a86c2c.
  Replay preserves pack/receipt/journal bytes; source/root metadata/assets exact.
- Final 13-pack lint EXIT0. Release ticket:
  2026-10-07-release-localized-travel-life-wave-20261007.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
