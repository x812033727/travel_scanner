---
id: 2026-10-07-localize-korea-autumn-missing-locales
title: Localize Korea autumn travel information missing languages
status: done
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:41:35Z
created_at: 2026-10-07T05:27:03Z
completed_at: 2026-10-07T06:11:04Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/korea-autumn-leaves-2026.json
  - apps/web/public/guides/korea-autumn-leaves-2026
  - docs/article-localization/installations/korea-autumn-leaves-2026.json
  - docs/article-localization/installations/bundles/6503955dcf7b6e4c
---

# Localize Korea autumn travel information missing languages

## Why

The eligible public Korea autumn article has only zh-TW. en, ja, ko and zh-CN
need complete text and translated diagram labels.

## Definition of done

- [x] Independently review all four complete documents and rendered diagrams.
- [x] Install the exact reviewed bundle while preserving source, photos and credits.
- [x] Create a separate guarded publication/public-verification release ticket.

## Steps

- [x] Pin current source/assets and check active scopes.
- [x] Independently audit all source facts and map rows against primary evidence.
- [x] Prepare four pinned CLI jobs with workers=3 and retries=0.
- [x] Resolve field/layout issues without changing immutable inputs/attempts.
- [x] Complete independent review and official assemble/install/replay.
- [ ] Prepare reviewed content PR and guarded release handoff.
- [ ] Perform fresh guarded release and public validation.

## How to verify

Use the official pipeline, renderer, assembler and installer with genuine independent
review. Check protected numbers/dates, source hash, original image bytes and the
freshly verified Seoul/Jeju links. After release, fetch every public language page
and refresh the production coverage inventory.

## Notes

- Source SHA `411c2adea68e42f2c97406817c434a477d97d1b7a468919125b9adbaa812012e`.
- Pack SHA `c921d5f9219b1c18ad9e8e1bdb9f6fe15187f3c8b86bd2f756ef2b1add2abb22`.
- Independent source audit checked 19 blocks, ten maple/five ginkgo rows, arboretum
  admission/reservations and the KMA 21-mountain snapshot on 2026-10-07.
- Preserve dated forecasts and the original Taiwan audience. Four external jobs
  completed without retries; no production write has occurred.
- Independent review covered all 114 fields, 19 blocks, 9 sources, 38 SVG labels
  and the original photo. The distinct executor corrected one Korean written-out
  number while preserving immutable source/attempt bytes.
- Final bundle manifest SHA 6503955dcf7b6e4c41665199d1557a119800b613d7b0c0008c28b4bba803810e.
- Installed pack SHA 03fc5b852a460d33aad79f546e72dfd1df932add6cedef21dea462dc545d05d3.
- Official replay preserves exact output/journal bytes. Source/photos unchanged;
  topic order follows the authoritative database baseline, membership unchanged.
- Release ticket: 2026-10-07-release-localized-travel-life-wave-20261007.

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
