---
id: 2026-10-07-correct-tofukuji-autumn-ticket-price
title: Correct announced Tofukuji autumn garden ticket price
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-07T05:36:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-autumn-leaves-2026.json
  - docs/article-localization/source-corrections/20261007-tofukuji-price
---

# Correct announced Tofukuji autumn garden ticket price

## Why

November 2026 travel-period fee conflicts with operator announced November 1 effective increase; not a replacement of historical forecast dates.
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

- Slug: `japan-autumn-leaves-2026`; pointer: `/locales/zh-TW/blocks/12/items/0`.
- Finding SHA `7b2d2539837b7adb8cec29d2075b4881669ddd003c1e1f717141ebf0d79da4d0`.
- Authority: 拝観料金 table, 東福寺本坊庭園（方丈） adult fee: 500円（※令和8年11月1日より600円）
- Source image factual text is unaffected. Original pack remains unchanged.
- Supporting source: https://tofukuji.jp/guide/
- No translation/model attempt started for this held article.
- Fresh 2026-10-28 source review confirmed the fee correction against the
  operator's July 1 notice and current admission page. A private exact candidate
  changes only the adult garden fee paragraph and the existing official guide's
  checked_on date; the article already has the schema limit of twenty sources,
  so the corroborating notice is retained in evidence rather than adding a
  twenty-first citation or removing an unrelated source.
- Fee-only candidate SHA256:
  `ae4d669bd49de4183b24bd7e3200bda474e789ea4f16c72724f64feb9db39f8e`.
  It is bound to fresh clean published v4, preserves all four original assets,
  and remains unapplied without an independent approved correction receipt.
- Completing that fee fix alone will not unblock translation: new October 25
  official notices now announce reservation-based November evening/early-morning
  openings, making the old no-evening/unannounced blanket statements stale.
  Distinguish these later announcements from the original fee error. Official
  weekday/time and child-fee inconsistencies remain unresolved; do not invent a
  resolution or promote those conflicting numbers. Complete source-readiness
  report SHA256:
  `6025faf6ce41703508e4f246ecdb126e2d1487593ce75e8db0b1c5bb44a0f9d7`.
