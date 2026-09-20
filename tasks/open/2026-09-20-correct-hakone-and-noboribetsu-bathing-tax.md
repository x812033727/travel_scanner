---
id: 2026-09-20-correct-hakone-and-noboribetsu-bathing-tax
title: Correct Hakone and Noboribetsu bathing tax age wording
status: in-progress
priority: P2
area: api
owner: codex-article-localization
claimed_at: 2026-09-20T08:37:35Z
created_at: 2026-09-20T08:37:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-onsen-ryokan-guide.json
---

# Correct Hakone and Noboribetsu bathing tax age wording

## Why

The published Traditional Chinese onsen guide says both Hakone and Noboribetsu
exempt children aged 12 and under. Noboribetsu exempts children **under** 12;
Hakone's rule also names elementary-school pupils and children until the first
March 31 on or after the day they legally attain age 12. In Japanese law that
attainment day is not necessarily the birthday, and March 31 itself is included.

## Definition of done

- [x] The source paragraph and tax table state each municipality's rule without
  excluding the attainment day or extending the school-year boundary.
- [ ] The exact source pack passes schema validation, CI, and guarded publication
  of only the existing zh-TW locale.

## Steps

- [x] Compare the two municipal tax pages and the education ministry's age-law
  explanation; independently review the March 31 boundary.
- [x] Correct the existing pack without changing prices, URLs or other prose.
- [ ] Merge reviewed CI, deploy, perform version-pinned dry run and publication.
- [ ] Verify desktop/mobile live page and preserved non-public locales.

## How to verify

Validate the pack with `ArticlePack.model_validate_json`, verify its normalized
`document_hash` and byte SHA-256, run `npm run check:tasks`, and require exact-head
PR CI. Production must match the old published version/hash before the guarded
draft and publish calls, then match the corrected published hash afterward.

## Notes

- Hakone: https://www.town.hakone.kanagawa.jp/www/contents/1100000000874/index.html
- Noboribetsu: https://www.city.noboribetsu.lg.jp/docs/2013031100289/
- Legal age: https://www.mext.go.jp/a_menu/shotou/shugaku/detail/1422233.htm
- Exact revised pack hash `febd82c4b31ef49e7a625efc4174e4174e6c5f8c4716bdd4e85997a2e6f985aa`;
  normalized zh-TW document hash `66c6ecf6f37010ea0f5cc514e541950c3543183f17496ddfe3c57fd837102a8d`.
- The correction changes the source used by Batch 003. Its onsen translations
  must be regenerated from a fresh published baseline and reviewed again.
