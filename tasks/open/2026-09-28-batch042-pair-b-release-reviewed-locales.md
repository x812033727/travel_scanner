---
id: 2026-09-28-batch042-pair-b-release-reviewed-locales
title: Release reviewed Batch042 Pair B locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T18:12:56Z
completed_at:
branch:
depends_on:
  - 2026-09-28-batch042-pair-b-install-reviewed-locales
scope:
  - docs/article-localization/releases/batch042-pair-b
---

# Release reviewed Batch042 Pair B locales

## Why

Release only technical-seo-checklist, seo-learning-roadmap, in zh-CN, en, ja and ko, after source repository and production gates pass.

## Definition of done

- [ ] Confirm merged content, independently reviewed hashes, and Batch042 live-source reconciliation.
- [ ] Complete same-image isolated Docker rehearsal and fresh scoped source/target-draft/version/visibility preflight.
- [ ] Verify backup, control concurrent writes, deploy needed assets/code and check health.
- [ ] Run exact-list import dry run; preserve later edits, hidden/withdrawn/expired state and existing locales.
- [ ] Import/publish only eligible missing locales, with a rerun showing unchanged and no unresolved journal entries.
- [ ] Verify all five language routes on desktop/mobile, body/images/alt, canonical/hreflang and published-language links.
- [ ] Record sanitized per-article draft-import, publication and actual browser acceptance evidence.

## How to verify

Use the existing guarded publishing flow and docs/article-localization/batch042-pair-b-evidence.md. Reconcile exact current hashes; historical receipts do not replace fresh preflight.

## Notes

Leave unclaimed while the required same-image rehearsal environment is unavailable. Source editorial follow-up remains separately recorded. No production write occurred in this localization work.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch042-pair-b/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
