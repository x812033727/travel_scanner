---
id: 2026-09-20-correct-nikko-pass-eligibility-for-accompanying
title: Correct NIKKO PASS eligibility for accompanying Japanese nationals
status: in-progress
priority: P2
area: api
owner: codex-article-localization
claimed_at: 2026-09-20T09:40:50Z
created_at: 2026-09-20T09:40:44Z
completed_at:
branch: codex/nikko-pass-eligibility
depends_on: []
scope:
  - apps/api/app/guides/content/nikko-day-trip-from-tokyo.json
---

# Correct NIKKO PASS eligibility for accompanying Japanese nationals

## Why

The published `zh-TW` paragraph says `NIKKO PASS 只賣外國旅客`.
Tobu Railway's current official [All Area conditions](https://www.tobu.co.jp/en/ticket/nikko/all.html)
explicitly allow Japanese nationals accompanying foreign travelers to buy it too.
Its [FAQ](https://www.tobu.co.jp/en/faq/) says a passport must be presented
when buying the tourist pass. Four staged Batch 005 translations copied the
overly narrow eligibility statement and must wait for a version-pinned source correction.

## Definition of done

- [ ] Correct only the eligibility paragraph in the published zh-TW source and preserve unrelated content and article visibility.
- [ ] Pin the live revision, review the precise change, deploy and publish it with a guarded revision/backup/browser receipt.
- [ ] Refresh Batch 005's four Nikko translations against the corrected source before signing or publishing them.

## Steps

- [x] Identify official eligibility and passport conditions.
- [x] Reconcile the 2026-09-20 read-only live snapshot with the repository pack and prepare an exact source correction PR.
- [ ] After green CI, merge, guarded deploy and publish the source revision; refresh translation baseline.

## How to verify

Compare the deployed zh-TW page with Tobu's official conditions, verify the
published document hash and locale revision, and check signed-out desktop/mobile
pages. The four translated pages must remain unavailable until their new review.

## Notes

Official source checked 2026-09-20. The All Area page's Note says Japanese
nationals accompanying foreign travelers can purchase; the FAQ describes
non-Japanese citizens visiting Japan and accompanying Japanese customers, and
requires passport presentation. Do not infer citizenship from reading language.
The World Heritage Area page should be rechecked during the correction PR.
Read-only snapshot at 2026-09-20 09:12 UTC: article version 2, only zh-TW,
locale version/published version 6, document SHA-256
`5d81e30fa50ff59e2e4f18f774bf1ba1f5f1eff5a8c36f45f062e4a6a8ba6c61`,
pack SHA-256 `90ed494224cabb3dfba94f9b7d209f5716787ee7344dab96e7214e2e7a353497`.
The release must refresh this snapshot before any database write.
