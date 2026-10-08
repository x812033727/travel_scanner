---
id: 2026-10-07-correct-vietnam-declaration-penalty
title: Correct Vietnam incoming declaration penalty distinction
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-07T05:36:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/vietnam-entry-2026-evisa.json
  - docs/article-localization/source-corrections/20261007-vietnam-penalty
---

# Correct Vietnam incoming declaration penalty distinction

## Why

Incorrect maximum penalty for over-declaration is folded into lower no-declaration / under-declaration maximum.
This source error blocks the four missing-language translations.

## Definition of done

- [ ] Prepare the exact source correction and direct supporting citation.
- [ ] Obtain an independent schema-v1 source-correction review bound to public versions/hashes.
- [ ] Finish four language documents and image review against the corrected source.
- [ ] Publish through a fresh guarded release and verify public results.

## Steps

- [x] Read the full source and check the concrete primary-source discrepancy.
- [x] Preserve hash-bound finding and actual primary response outside repository.
- [ ] Prepare/review the exact correction, preserving unrelated fields and asset bytes.
- [ ] Translate only after correction baseline/review is pinned.
- [ ] Complete guarded publication.

## How to verify

Read the cited primary page and exact provision. Use source_correction.verify_review
against a fresh baseline; check pointer before/after diff, source versions, assets
and draft/published hashes. Complete independent translation/image review and
public-language verification after release.

## Notes

- Slug: `vietnam-entry-2026-evisa`; pointer: `/locales/zh-TW/blocks/12/text`.
- Finding SHA `8881c982bc19ab0bf276bc9c8c233dcee13ea624d62ed0f0f4164e6b4254ae5d`.
- Authority: Nghị định 169/2026/NĐ-CP, Article 14, paragraphs 2(c) incoming non-/under-declaration: 10–20 million; paragraph3(c) over-declaration: 15–25 million VND. The cited government May20 article displays both provisions consecutively.
- Source image factual text is unaffected. Original pack remains unchanged.
- Supporting source: https://xaydungchinhsach.chinhphu.vn/muc-phat-voi-nguoi-xuat-nhap-canh-khong-khai-khai-sai-so-tien-mat-vang-mang-theo-vuot-muc-quy-dinh-119260520111349618.htm
- No translation/model attempt started for this held article.
