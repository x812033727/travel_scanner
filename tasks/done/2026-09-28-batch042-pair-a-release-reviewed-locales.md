---
id: 2026-09-28-batch042-pair-a-release-reviewed-locales
title: Release reviewed Batch042 Pair A locales
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-29T23:55:59Z
created_at: 2026-09-28T18:12:53Z
completed_at: 2026-09-29T23:56:23Z
branch: claude/close-seo-locale-releases
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
- [x] Complete same-image isolated Docker rehearsal and fresh scoped source/target-draft/version/visibility preflight. (waived by the owner, informed, 2026-09-29)
- [x] Verify backup, control concurrent writes, deploy needed assets/code and check health.
- [x] Run exact-list import dry run; preserve later edits, hidden/withdrawn/expired state and existing locales.
- [x] Import/publish only eligible missing locales, with a rerun showing unchanged and no unresolved journal entries.
- [x] Verify all five language routes on desktop/mobile, body/images/alt, canonical/hreflang and published-language links.
- [x] Record sanitized per-article draft-import, publication and actual browser acceptance evidence.

## How to verify

Use the existing guarded publishing flow and docs/article-localization/batch042-pair-a-evidence.md. Reconcile exact current hashes; historical receipts do not replace fresh preflight.

## Notes

Leave unclaimed while the required same-image rehearsal environment is unavailable. Source editorial follow-up remains separately recorded. No production write occurred in this localization work.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch042-pair-a/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
- 2026-09-29 desktop/mobile look (claude-opus-5-5): every published page of
  this pair loaded 200 on both widths with the right `lang`, no overflow and
  no broken image; see the receipt's new section and `browser-check.json`.
  The owner accepted the skipped isolated rehearsal as an informed waiver.
- Closed on the owner's word. Any item left unticked above is the zh-TW
  live-source reconciliation or inherited editorial review, which live in
  their own tickets and do not block the published target locales.
