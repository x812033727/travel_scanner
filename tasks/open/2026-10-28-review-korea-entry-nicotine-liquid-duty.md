---
id: 2026-10-28-review-korea-entry-nicotine-liquid-duty
title: Review Korea entry nicotine liquid duty free qualification
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-28T03:08:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/korea-entry-2026-k-eta-e-arrival.json
  - docs/article-localization/source-corrections/20261028-korea-nicotine-qualification
---

# Review Korea entry nicotine liquid duty free qualification

## Why

The published zh-TW Korean entry guide lists nicotine liquid 20 ml at blocks/12/text
without the cited Incheon Customs page's below-1-percent nicotine qualification.
Today's primary-source reading found the omitted condition in both live and
repository body text, so this source remains on hold before translation.

## Definition of done

- [ ] Independently confirm the complete current customs source and the exact omitted duty-free qualification.
- [ ] Review a minimal correction and preserve unrelated source/media and separate description-draft content.
- [ ] Bind source correction to current public/draft versions and hashes, then obtain concrete approval before live publication.
- [ ] Start four-language localization only from the corrected public source and verified route inputs.

## Steps

- [ ] Recheck ownership, current primary rules and all source claims; do not infer separate import or criminal thresholds.
- [ ] Review `電子菸尼古丁液 20 毫升（尼古丁含量低於 1%）` as the minimal phrase replacement.
- [ ] Resolve description drift without overwriting the repository draft or quietly expanding the live change.
- [ ] Complete guarded source publication and later Busan route admission before preparing locale jobs.

## How to verify

Primary reference: [Incheon Airport Customs entry declaration procedure](https://www.customs.go.kr/incheon_airport/cm/cntnts/cntntsView.do?mi=12546&cntntsId=6689),
read 2026-10-28. Exact duty-free line: `전자담배 니코틴용액20ml(니코틴함량 1%미만)`.
The finding concerns the duty-free item's qualification; it does not establish
any separate criminal import threshold. Re-run source, document and image guards
before admitting a correction or translation.

## Notes

Current public source content hash (transport envelope removed):
`8117fd7da6f85e2b2cd01b07fbe45d38b44ebff73b1dc1d071adb57315025531`.
The repo also has a genuine description difference. The current diagram does not
mention nicotine liquid, so no SVG correction is inferred. Official raw captures,
current body and exact proposed finding remain in private retained evidence;
readiness SHA `e3d621fc90d9b82c834cd658887ca7f204c5abb418347271bd14408eb3a692ff`.
No specific existing correction task was found. This source change is outside the
already approved seventeen-life-article production release. The current Busan
allowlist failure does not prove the destination page is missing live.
