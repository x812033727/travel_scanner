---
id: 2026-09-20-five-language-article-batch-004
title: Five-language article batch 004
status: in-progress
priority: P1
area: docs
owner: codex-article-localization-batch004
claimed_at: 2026-09-20T08:22:41Z
created_at: 2026-09-20T08:22:34Z
completed_at:
branch: codex/article-localization-batch-004
depends_on: []
scope:
  - apps/api/app/guides/content/japan-train-disruption-plan.json
  - apps/api/app/guides/content/japan-travel-laundry-guide.json
  - apps/api/app/guides/content/kyoto-cycling-parking-guide.json
  - apps/api/app/guides/content/tokyo-rainy-day-museum-plan.json
  - apps/api/app/guides/content/hong-kong-ferry-tram-day.json
  - apps/web/public/guides/japan-train-disruption-plan
  - apps/web/public/guides/japan-travel-laundry-guide
  - apps/web/public/guides/kyoto-cycling-parking-guide
  - apps/web/public/guides/tokyo-rainy-day-museum-plan
  - apps/web/public/guides/hong-kong-ferry-tram-day
---

# Five-language article batch 004

## Why

Five published travel guides still have only their complete Traditional Chinese
document. Each lacks English, Japanese, Korean and Simplified Chinese, and each
has an editable SVG diagram containing Traditional Chinese labels. The exact
pack and asset paths above do not overlap another open task.

## Definition of done

- [ ] Five complete, independently reviewed documents per article, preserving
      the published source and all existing editorial state.
- [ ] Localized text-bearing diagrams pass visual and glyph review.
- [ ] An exact reviewed bundle installs idempotently; its content PR is merged,
      deployed, and only the missing public locales are published.
- [ ] Twenty new public pages pass desktop/mobile content, image, canonical,
      hreflang and same-language link checks.

## Steps

- [x] Claim five non-overlapping paths and capture a fresh production snapshot.
- [ ] Translate twenty missing documents and render twenty localized SVGs.
- [ ] Complete automated pre-review and independent editorial/artwork review.
- [ ] Assemble/install the reviewed bundle, then perform guarded PR and release.

## How to verify

Run `pipeline.py status` on the pinned baseline and all twenty jobs; inspect
the document and render hashes and independent review. Run the bundle
assembler/installer twice, focused guide tests, CI, a production dry-run, and
read-only post-publication database/browser audits on all twenty locales.

## Notes

Read-only production snapshot captured at 2026-09-20T08:23:08Z while deployed
repository HEAD was `80ad55c6a85b7a5635f9763c5837094aa5dbc513` before and
after. Snapshot SHA-256:
`b5c8baac5d10b4205c0ab35a5e52d618fc5c67c325267a4a67abba13d8384593`.
Branch base is `2699a1faf946ba94477873c014ae7d7534b61ebc`; combined baseline
SHA-256 is `0f4b4681059509928a0871c628a75c4ac1cd9dc7088991245111f70c9a1345b5`.
Each selected source document exactly matches its live published version;
all five are active/published and each lacks exactly `en`, `ja`, `ko`, `zh-CN`.
Production locale version is 8 for the train-disruption guide and 6 for the
other four. Full baseline and authoring evidence live outside the repository
at `C:\Users\x8120\.codex\article-localization-batch-004`. No pack or public
asset is changed before independent review.
