---
id: 2026-10-07-release-wave3-travel-and-life-article
title: Release wave3 travel and life article locales
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T07:57:01Z
completed_at:
branch:
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

- [ ] All fourteen articles have their four eligible missing locales public,
      verified from persisted production state and complete public page content.
- [ ] The reviewed Hong Kong source correction is published with its exact approved
      scope; all other original documents, public translations and media remain exact.
- [ ] Desktop/mobile body, images, captions, credits, same-language links,
      canonical/hreflang and complete sitemap coverage pass per locale.
- [ ] An official fresh inventory updates the global remaining-language count.

## Steps

- [ ] Resolve the stacked PR sequence; bind approval to the final exact PR/SHA and
      current main commits before any merge or deploy. Use no force/ignore-hold default.
- [ ] Read `ops/release/README.md` and deploy skill; perform a fresh host preflight.
- [ ] Verify exact deployed pack and API/web asset bytes in the actual images.
- [ ] Capture a new official full database snapshot and unchanged official baseline;
      recheck source versions/hashes, unpublished edits, visibility, aliases and holds.
- [ ] Compile the twelve life articles again with genuine original review rows;
      rebuild the two travel bundles using current real job/review bindings.
- [ ] Rehearse the actual reviewed cohort in an isolated copy of the deployed API image.
- [ ] Run actual production dry-run with pinned manifests and the same durable state.
- [ ] Obtain the required concrete owner publication choice, create pg_dump and
      prove hash/restore against an isolated database before the first write.
- [ ] Use the official phased publisher with owned hold/locks; preserve any uncertain
      outcome and resume the same state instead of issuing an unbound retry.
- [ ] Verify persisted public rows, all pages/assets/links and paginated sitemap;
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
owner's latest continuation authorizes preparation; an earlier exact deployment
choice remains unanswered. Fresh main contains additional commits, so a previous
main-delta disclosure must not be reused as deployment approval.

Paid-vs-organic source hold and four source-drift WordPress articles remain
excluded. Held Lunar content remains publication-aware plain text when its
requested translation is unavailable; this ticket does not release that hold.
