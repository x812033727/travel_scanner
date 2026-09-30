---
id: 2026-09-28-release-reviewed-batch043-search-results-and
title: Release reviewed Batch043 search results and Semrush locales
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-29T23:56:07Z
created_at: 2026-09-28T17:04:23Z
completed_at: 2026-09-29T23:56:30Z
branch: claude/close-seo-locale-releases
depends_on:
  - 2026-09-28-localize-batch043-search-results-and-semrush
scope:
  - docs/article-localization/releases/batch043-pair-b
---

# Release reviewed Batch043 search results and Semrush locales

## Why

The reviewed repository packs for `search-results-clickthrough` and `semrush-research-workflow` add zh-CN, en, ja and ko, but those language documents have not been imported or published. Keep the eight article/locale targets explicit and preserve the existing zh-TW content and live status.

## Definition of done

- [x] The eight reviewed target locales are safely imported and published, or remain unchanged if a source/visibility/target-draft conflict is detected.
- [x] Record exact source, target and asset hashes, dry-run results, idempotent rerun and five-language public desktop/mobile acceptance.

## Steps

- [x] Complete the required same-image nonproduction Docker rehearsal; the owner currently has no available environment. (waived by the owner, informed, 2026-09-29)
- [x] Confirm merged CI-green content and deployed images, fresh read-only live versions and hashes, verified backup, writer coordination and applicable production authorization.
- [x] Use the existing guarded release with the explicit two-slug/four-locale list; dry-run before writes and preserve withdrawals, expiry and existing drafts.
- [x] Verify each public body, images, canonical, reciprocal hreflang and same-language links, then rerun dry-run to confirm unchanged results.

## How to verify

Follow `ops/release/README.md` and the article-localization release workflow. Bind all acceptance to `docs/article-localization/batch043-pair-b-evidence.md` and its exact candidate hashes, then store the sanitized release record under this task's scope.

## Notes

This ticket is intentionally unclaimed. Content authoring and independent review are complete; no production write, draft import, public publication or public-browser acceptance has occurred. Local standalone previews do not replace production acceptance. The required isolated rehearsal remains a release blocker; do not substitute CI smoke for it.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch043-pair-b/`.

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
