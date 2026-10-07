---
id: 2026-10-07-localize-japan-cherry-blossom-2027
title: Localize Japan 2027 cherry blossom travel information
status: in-progress
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:49:24Z
created_at: 2026-10-07T05:07:49Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/japan-cherry-blossom-2027.json
  - apps/web/public/guides/japan-cherry-blossom-2027
  - docs/article-localization/installations/japan-cherry-blossom-2027.json
  - docs/article-localization/installations/bundles/c0a1433a8990c8fb
  - docs/article-localization/installations/bundles/78d78b438488a1f9
---

# Localize Japan 2027 cherry blossom travel information

## Why

This public travel-information article has only zh-TW. Add complete en, ja, ko
and zh-CN documents and translated diagram text while preserving its dated
historical observations, explicit unannounced 2027 forecasts and original photos.

## Definition of done

- [x] All four target documents preserve the 42-block source structure and facts.
- [x] Source zh-TW and original photos remain byte/hash preserved.
- [x] Every target text, SVG and raster has independent hash-bound review.
- [ ] Content/bundle checks pass and a content PR plus separate release ticket exist.

## Steps

- [x] Confirm fresh production source hash and four absent target database rows.
- [x] Independently review all source blocks, city date rows and editable text SVG.
- [x] Verify primary sources and distinguish historical data from future forecasts.
- [x] Prepare and start four pinned Codex jobs (three workers, zero retries).
- [x] Materialize/render, independently review and apply corrections.
- [x] Assemble/install a reviewed bundle and verify exact replay/source preservation.
- [ ] Complete content PR and separate guarded release handoff.

## How to verify

Compare the normalized source and original asset hashes before/after install;
run scoped content lint and localization/bundle checks. Reviews must bind final
document and artifact-manifest hashes plus image bytes. Live publication and
browser acceptance are tracked separately by the release ticket.

## Notes

- Source/publication hash `22742f2e2e550a0e6da5eccadf42a8b354b00b9b3d7dac32b20c47d4478c0a6d`.
- Pack hash `39602e86f31437e910d935946c8dba8eeba07c0d1810970a3b41c9d79a74c8e3`.
- Current independent source audit approved at 2026-10-07T05:04:41.095645+00:00.
  All eight city rows, historical 2026 dates, 1991–2020 normals and 2021–2026
  observations were checked against primary sources. Mint/Kiyomizu times and
  holiday dates were checked; 2027 prediction dates remain explicitly unannounced.
- Same-site links use the freshly verified Tokyo and Osaka/Kyoto routes.
- All job inputs, attempts, source-audit evidence and logs are in the owner's
  external persistent work directory. No new locale is claimed published yet.
- Final bundle manifest SHA 78d78b438488a1f94e231ec2786bd767f5216005f5e3c647300781d787f9f48a.
- Installed pack SHA 74b23461074f1c5e0b5e0697af224917553fcf3f2d623068538b1f383161da69.
- Content lint caught two English labels at 14px. A distinct party shortened
  those exact labels; genuine independent review approved the regenerated 16px
  diagram (SVG SHA 0d89e7d59c1c4b92523c8720320366e5cbbe8e2ab64a682959d63dd8a2dd2f28).
- Final English review SHA 22f5603c0c4f947ff7635f04f1c10e08c7f9b5a72daff4f34a83354f20c8bc0a.
- Final official installer receipt SHA 65aa92e53dfd6a0475ba5e1cc30eb48bdc13f25b3b562635747dc54a57a47090.
  Superseded candidate/receipt/journal remain preserved. Replay is byte-identical.
- Topic membership is preserved, with order normalized to the database baseline;
  ordered related picks, aliases and all other root fields remain preserved.
- Release ticket: 2026-10-07-release-localized-travel-life-wave-20261007.
