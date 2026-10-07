---
id: 2026-10-07-localize-powerbank-flight-missing-locales
title: Localize power bank flight information missing languages
status: in-progress
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:35:00Z
created_at: 2026-10-07T05:34:59Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/power-bank-flight-rules-2026.json
  - apps/web/public/guides/power-bank-flight-rules-2026
  - docs/article-localization/installations/power-bank-flight-rules-2026.json
---

# Localize power bank flight information missing languages

## Why

The eligible public power bank flight rules article lacks en, ja, ko and zh-CN. Translate
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

- Source SHA `70bb325eaf6a828d0bdc89c1ee8db644a19a5182db263f892bd4ad2d447c1908`.
- Original pack SHA `d4dfb29421cf4e71d54cc1461479f3dd9755c258cbd1dabbf32e48b03e06560b`.
- Primary evidence and actual source-image review are in the private source audit.
- Four translation jobs completed with no automatic retry. Production writes: zero.
- All four whole-document/image reviews PASS, preserving the audience-specific
  ICAO/Taiwan/Korea/Japan dates and distinct airline charging/storage conditions.
  Actual final SVG label metrics are >=15px with no glyph/geometry issue.
- Final combined review evidence SHA dcda1e387709f18e872237cb722a7a810f74ec90362e6224592b6299875d69e6.
- Combined official manifest c96737f04540a86d55d3f9e4b398bdb0ef5da602387d90d7052b0bfd02ae4cff.
- Installed pack 1761f2190920742f763a571235b8fa61a17d88566c6c0ff962446f1c0f8b7faa.
- Official receipt 912d27fd2c16602ff9311601b6469eee48fa6f568cd001a141f26e42314eac58.
  Replay preserves pack/receipt/journal bytes; source/root metadata/assets exact.
- Final 13-pack lint EXIT0. Release ticket:
  2026-10-07-release-localized-travel-life-wave-20261007.
