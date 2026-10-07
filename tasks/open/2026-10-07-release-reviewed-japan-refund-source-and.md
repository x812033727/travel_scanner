---
id: 2026-10-07-release-reviewed-japan-refund-source-and
title: Release reviewed Japan refund source and four locales
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-07T06:29:51Z
completed_at:
branch:
depends_on:
  - 2026-10-07-correct-japan-tax-free-shop-logo
scope:
  - docs/article-localization/releases/2026-10-07-refund-v2
---

# Release reviewed Japan refund source and four locales

## Why

The Japan refund guide needs an exact independently reviewed Traditional Chinese
source correction and four missing public locales. Local installation and a
content PR cannot replace production publication or public-page validation.

## Definition of done

- [ ] Obtain exact content PR/SHA merge/deploy approval and verify the deployed runtime.
- [ ] Capture a fresh full production baseline and verify original source/draft/target/visibility/version guards.
- [ ] Verify the seven source-pointer corrections, two source-SVG text slots and four independent final language reviews against the actual release bytes.
- [ ] Obtain publication approval after the exact dry-run, recoverable backup/restore and same-image proof.
- [ ] Publish through the official durable phases and verify all five public language routes, images and hashes.
- [ ] Record publication, replay, browser evidence and a fresh missing-language inventory.

## Steps

- [ ] Merge/deploy the reviewed content change without force or hold bypass.
- [ ] Build a new guarded correction bundle from fresh database versions; stop for any unpublished source edit or target drift.
- [ ] Execute verified backup, isolated runtime proof, exact production dry-run and approved phases with shared locks/owned hold.
- [ ] Perform five-language public acceptance and preserve sanitized release records.

## How to verify

Use the official source-correction verifier, assembler, bundle publisher and
progress reporter. Compare source/target versions, normalized document hashes,
root metadata, original-photo bytes and every selected diagram. A schema-v1
browser-evidence record must bind actual public pages to the released manifest.
Preserve a refused/interrupted journal and hold; never use a new state for a blind retry.

## Notes

Exact scope: `japan-tax-free-refund-2026`, one zh-TW source correction plus `en`,
`ja`, `ko`, `zh-CN`. This is separate from PR #1365's 13 articles / 52 documents.
Approved source review SHA
`552fd065bbe7ffd3d4460f2d890ce820423e003f40623359bb5b90877051bb7e`;
old source `6358cae7243f026ec6a2a27e9f26394e5805759ce42932ef92032a1367ff7c27`;
corrected source `8f19020e8412793852dd6502faa35f88b5953c950b06d456f6b20564f0308bb7`.
The reviewed corrected source SVG is
`9abff5f9592df1cb0313f614aad9056e88d5934a5134c8d3ecc8215e3383ed81`.
Both photographs, geometry/styles/fonts and article metadata are protected.
Original provider attempts and pre-correction jobs remain preserved in owner storage.
No deployment or publication has occurred; final local review/installation is
tracked by the prerequisite authoring ticket. Source-review approval is editorial
evidence and does not authorize a production release.
