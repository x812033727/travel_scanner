---
id: 2026-09-28-batch042-pair-a-release-reviewed-locales
title: Release reviewed Batch042 Pair A locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T18:12:53Z
completed_at:
branch:
depends_on:
  - 2026-09-28-batch042-pair-a-install-reviewed-locales
scope:
  - docs/article-localization/releases/batch042-pair-a
---

# Release reviewed Batch042 Pair A locales

## Why

Release only seo-search-intent, seo-content-quality, in zh-CN, en, ja and ko, after source repository and production gates pass.

## Definition of done

- [ ] Confirm merged content, independently reviewed hashes, and Batch042 live-source reconciliation.
- [ ] Complete same-image isolated Docker rehearsal and fresh scoped source/target-draft/version/visibility preflight.
- [ ] Verify backup, control concurrent writes, deploy needed assets/code and check health.
- [ ] Run exact-list import dry run; preserve later edits, hidden/withdrawn/expired state and existing locales.
- [ ] Import/publish only eligible missing locales, with a rerun showing unchanged and no unresolved journal entries.
- [ ] Verify all five language routes on desktop/mobile, body/images/alt, canonical/hreflang and published-language links.
- [ ] Record sanitized per-article draft-import, publication and actual browser acceptance evidence.

## How to verify

Use the existing guarded publishing flow and docs/article-localization/batch042-pair-a-evidence.md. Reconcile exact current hashes; historical receipts do not replace fresh preflight.

## Notes

Leave unclaimed while the required same-image rehearsal environment is unavailable. Source editorial follow-up remains separately recorded. No production write occurred in this localization work.
