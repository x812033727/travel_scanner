---
id: 2026-11-22-release-localized-ha-long-bay-cruise
title: Release localized ha-long-bay-cruise-from-hanoi and phuket-airport-transport-where-to-stay (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-22T06:37:42Z
completed_at:
branch:
depends_on:
  - 2026-11-22-localize-ha-long-bay-cruise-from
scope:
  - apps/api/app/guides/content/ha-long-bay-cruise-from-hanoi.json
  - apps/api/app/guides/content/phuket-airport-transport-where-to-stay.json
  - apps/web/public/guides/ha-long-bay-cruise-from-hanoi
  - apps/web/public/guides/phuket-airport-transport-where-to-stay
---

# Release localized ha-long-bay-cruise-from-hanoi and phuket-airport-transport-where-to-stay (en, ja, ko, zh-CN)

## Why

Wave 3C Batch 10 localized `howto/ha-long-bay-cruise-from-hanoi` and `howto/phuket-airport-transport-where-to-stay` into `en`, `ja`, `ko`, and `zh-CN` with 8 localized 1600×900 SVG diagrams and a validated `route-b-review-v1` receipt (`2026-11-22-localize-ha-long-bay-cruise-from`). Once the content PR is merged and deployed to production, run the guarded Route B host-side release pipeline (`prepare_route_b_bundle.py` → `publish_bundle.py`) to publish the 8 new guide locales live.

## Definition of done

- [ ] Content PR for `agy/localize-wave3c-halong-phuket-batch10` is merged and deployed (static SVGs live at `/guides/<slug>/diagram-1-{en,ja,ko,zh-cn}.svg`).
- [ ] `prepare_route_b_bundle.py` compiles a verified schema-1 release bundle against the live DB baseline for both slugs across `en`, `ja`, `ko`, `zh-CN`.
- [ ] `publish_bundle.py` dry-run, drafts, and publish-articles succeed with zero errors.
- [ ] All 8 new public URLs return HTTP 200 with localized titles, diagrams, and canonical/hreflang links (`ha-long-bay-cruise-from-hanoi` and `phuket-airport-transport-where-to-stay` in `en`, `ja`, `ko`, `zh-CN`).

## Steps

- [ ] Confirm content PR is merged and deployed to production.
- [ ] Build fresh baseline on the host (`build_baseline.py`) and verify pinned `zh-TW` hashes still match:
  - `ha-long-bay-cruise-from-hanoi`: `348eb359485656ea237d266cbbfe765cad4f1722370b13d5c487b15cbadf27d0`
  - `phuket-airport-transport-where-to-stay`: `dfcf9ca1968b5031e65f90b2f3ee69e15f6c32eafc8ead7a6cea8efa91236738`
- [ ] Run `prepare_route_b_bundle.py` for `--slug ha-long-bay-cruise-from-hanoi --slug phuket-airport-transport-where-to-stay --locale en --locale ja --locale ko --locale zh-CN`.
- [ ] Run `publish_bundle.py` (`dry-run` → `drafts` → `publish-articles`) after explicit owner go-ahead.
- [ ] Verify all 8 public pages and 8 diagram SVG URLs return HTTP 200.

## How to verify

```bash
for slug in ha-long-bay-cruise-from-hanoi phuket-airport-transport-where-to-stay; do
  for loc in en ja ko zh-CN; do
    curl -sI "https://mokaair.com/${loc}/guides/howto/${slug}" | head -n 1
  done
done
```

## Notes

- Depends on `2026-11-22-localize-ha-long-bay-cruise-from`.
- Validated `route-b-review-v1` receipt hashes recorded at localization completion:
  - `evidence_sha256`: `3470e699d979019e39d6ddde67209a3eff445df66c132ae13383ee3d90150dc4`
  - `review_sha256`: `55b91228358b4d27a83d51e34e29200847df2edc173231bc17f5be3589a97956`
- Never run `publish_bundle.py` without explicit owner approval and confirmed static SVG deploy.
