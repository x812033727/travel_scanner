---
id: 2026-10-07-release-wave3-travel-and-life-article
title: Release wave3 travel and life article locales
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T12:12:46Z
created_at: 2026-10-07T07:57:01Z
completed_at: 2026-10-07T16:11:55Z
branch: codex/article-locales-release-20261007
depends_on:
  - 2026-10-07-recheck-newsletter-and-marketing-locales-wave3a
  - 2026-10-07-recheck-social-strategy-and-wordpress-locales
  - 2026-10-07-localize-taiwan-2027-holiday-planning
  - 2026-10-07-correct-hong-kong-public-possession-scope
  - 2026-10-07-enable-verified-hong-kong-localization-routes
  - 2026-10-07-coordinate-wave3-localization-installation-journals
scope:
  - docs/article-localization/releases/wave3-20261007
---

# Release wave3 travel and life article locales

## Why

Wave3 prepares twelve existing life translations and the missing languages of
Taiwan2027 holiday planning and Hong Kong entry guidance. Public availability
requires its own guarded release after authoring, exact-version approval and
deployment. Local review, installation and CI do not close this release ticket.

## Definition of done

- [x] All fourteen articles have their four eligible missing locales public,
      verified from persisted production state and complete public page content.
- [x] The reviewed Hong Kong source correction is published with its exact approved
      scope; all other original documents, public translations and media remain exact.
- [x] Desktop/mobile body, images, captions, credits, same-language links,
      canonical/hreflang and complete sitemap coverage pass per locale.
- [x] An official fresh inventory updates the global remaining-language count.

## Steps

- [x] Confirm the first two content PRs are merged and the third is based on current
      main; bind approval to the final exact PR/SHA before merge or deployment.
      Use no force/ignore-hold default.
- [x] Read `ops/release/README.md` and deploy skill; perform a fresh host preflight.
- [x] Verify exact deployed pack and API/web asset bytes in the actual images.
- [x] Capture a new official full database snapshot and unchanged official baseline;
      recheck source versions/hashes, unpublished edits, visibility, aliases and holds.
- [x] Compile the twelve life articles again with genuine original review rows;
      rebuild the two travel bundles using current real job/review bindings.
- [x] Rehearse the actual reviewed cohort in an isolated copy of the deployed API image.
- [x] Run actual production dry-run with pinned manifests and the same durable state.
- [x] Obtain the required concrete owner publication choice, create pg_dump and
      prove hash/restore against an isolated database before the first write.
- [x] Use the official phased publisher with owned hold/locks; preserve any uncertain
      outcome and resume the same state instead of issuing an unbound retry.
- [x] Verify persisted public rows, all pages/assets/links and paginated sitemap;
      record an honest release receipt and refresh the global census.

## How to verify

Use the official baseline builder, route-B compiler and route-A assembler,
`publish_bundle.verify_bundle`, same-image rehearsal and guarded publisher. Bind
all evidence to exact database versions, manifest/source/document/asset hashes
and actual deployed image IDs. Pace public reads sequentially by at least1.3s.

## Notes

Selection: content-marketing-calendar, email-newsletter-planning,
influencer-collaboration, kit-newsletter-setup, mailchimp-wordpress-newsletter,
short-video-marketing, social-media-planning, stp-persona-research,
wordpress-500-error, wordpress-ad-placement, wordpress-social-embeds,
wordpress-social-login, taiwan-long-weekends-2027-flight-planning,
hong-kong-entry-2026. Targets: en, ja, ko, zh-CN. No hubs are selected.

The retained04:45 production snapshot is preparation evidence only. At creation
there are zero production writes, and this ticket is open and unclaimed. The
owner's latest continuation authorizes preparation. A later live observation
confirms the first two content PRs merged; this observation supplies no new
deployment/publication choice. The third branch is based on current main. Use
its final exact PR/head and current main delta for the concrete owner choice;
do not reuse an old draft-head question as deployment approval.

Paid-vs-organic source hold and four source-drift WordPress articles remain
excluded. Held Lunar content remains publication-aware plain text when its
requested translation is unavailable; this ticket does not release that hold.

2026-10-07 update: the owner explicitly selected merge of PR #1370, normal
deployment and publication of the complete 32-article cohort. Reviewed head
`403d8204c27fd89653990cb1b8e624a1f87c5bcc` had 21 successful CI checks; merged and
deployed revision is `7524c25995d59f3826227e693d52f2ef5b3a19a2`. The official
post-deployment verifier recorded 11 passes and zero failures. Actual container
reads matched all 32 selected packs and 338 assets. The fresh full snapshot and
baseline preserve all original database guards; Hong Kong's admitted source
baseline retains its exact independent correction review.

The twelve life packs were recompiled with the original review rows. Taiwan and
Hong Kong retain their original payload/review bytes with the fresh baseline
binding. All nine real production dry-runs completed, followed by a synchronized
full database backup and catalog verification. The real isolated restore and
same-image publication/replay rehearsal is running. No production article write
or public acceptance has occurred. The earlier preparation-only notes remain
historical observations.

### Actual owner-approved publication and public acceptance

This scoped record is now backed by genuine publication: 14 articles, 56 previously missing languages, 1 approved source corrections and 57 selected publication operations. Normal deployment, the real restore/publication rehearsal and production replay passed. The original driver completed with exit 0 at 2026-10-07T15:40:06 UTC and cleared its owned hold after verified evidence transfer.

Public verification covered 70 five-language pages and 140 original desktop/mobile views in this record. Four actual independent reviewers read disjoint partitions; all document/image/DOM/canonical/hreflang/sitemap guards passed. The eight record outputs were validated and copied only into their existing claimed release scopes. Sanitized evidence is `docs/article-localization/releases/wave3-20261007/evidence.json`.

The full post-publication census observed 830 incomplete articles / 3,320 missing language documents. The global program remains open. All-guides link checks exited 1 in every locale; selected findings are exclusively unpublished related target languages. Actual per-record counts and this limitation are retained in evidence.json, rather than claiming an all-guides PASS. The earlier authoring/rehearsal notes above remain historical checkpoints. The record PR is the final documentation step.

The sanitized release-record draft PR is https://github.com/x812033727/travel_scanner/pull/1373. Its record files preserve the exact verified bytes and actual publication evidence. This scoped release is complete; the global localization program remains open.
