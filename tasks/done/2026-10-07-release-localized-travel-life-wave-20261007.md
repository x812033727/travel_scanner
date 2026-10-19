---
id: 2026-10-07-release-localized-travel-life-wave-20261007
title: Release reviewed travel and life localization wave 20261007
status: done
priority: P1
area: ops
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T12:12:35Z
created_at: 2026-10-07T05:55:30Z
completed_at: 2026-10-07T16:11:53Z
branch: codex/article-locales-release-20261007
depends_on:
  - 2026-10-07-localize-japan-cherry-blossom-2027
  - 2026-10-07-localize-japan-refund-and-golden-week
  - 2026-10-07-localize-korea-autumn-missing-locales
  - 2026-10-07-recheck-unpublished-wordpress-security-locales
  - 2026-10-07-recheck-wordpress-business-and-launch-locales
  - 2026-10-07-recheck-wordpress-translation-and-member-locales
  - 2026-10-07-localize-singapore-entry-missing-locales
  - 2026-10-07-localize-powerbank-flight-missing-locales
scope:
  - docs/article-localization/releases/2026-10-07-travel-life-wave
---

# Release reviewed travel and life localization wave 20261007

## Why

Thirteen public articles have 52 absent target locale rows. Their existing or newly
authored en, ja, ko and zh-CN documents need guarded database publication after
the reviewed content PR is merged and its exact revision is deployed.
This release owns release records only, with owner approval at deployment and
publication gates; it does not claim the entire 862-article program is complete.

## Definition of done

- [x] Merge content PR with all required checks green on the exact head.
- [x] Obtain exact PR/SHA deployment approval and verify deployed content/assets.
- [x] Bind this cohort's 52 authorized targets to the freshly reviewed production bundles.
- [x] Verify the owner-approved publication plan against the real dry-run and recoverable restore rehearsal.
- [x] Publish through the same durable journals per pinned bundle; verify replay writes nothing.
- [x] Verify all target pages, diagrams, language links and desktop/mobile layouts.
- [x] Save sanitized release evidence and refresh the full production gap inventory.

## Steps

- [x] Verify no conflicting staged release, lock or publish hold before deployment.
- [x] Freeze exact merged Git candidate bytes and independently reviewed target hashes.
- [x] Compile with a fresh post-deployment full baseline, checking every selected target's actual database state.
- [x] Use dry-run, drafts, publish-articles and publish-hubs with the same pins/state.
- [x] Rebuild/check article links, rerun dry-run and perform public acceptance.
- [x] Record release results in README.md/evidence.json and open the record PR.

## How to verify

Follow article-localization bundle-release and ops/release/README.md. Use the
official Route B compiler and publish_bundle.py, with an explicit deployed root,
active admin actor and version/hash guards. Full production export must confirm
52 newly public locales; public checks must bind final document and asset hashes.
No raw DB identities, machine paths, credentials or screenshots belong in Git.

## Notes

- Cohort: marketing-mix-models, brand-tone-vibe-marketing,
  marketing-plan-small-business, wordpress-security-basics, wordpress-business-site,
  wordpress-local-to-live, wordpress-plugin-theme-translation,
  wordpress-member-registration, japan-golden-week-2027,
  japan-cherry-blossom-2027, korea-autumn-leaves-2026,
  singapore-entry-2026-sg-arrival-card, power-bank-flight-rules-2026.
- All targets are en, ja, ko and zh-CN. No zh-TW publication is selected.
- A synthetic isolated same-deployed-image rehearsal passed 13 cases. That proves
  the tested publisher behavior; it is neither production approval nor publication.
- Source-error articles are outside this cohort. Singapore entry and powerbank
  completed genuine final independent review before this cohort was frozen.
- Unclaimed pending content completion; no production write has occurred.
- 2026-10-07 update: the owner explicitly approved merge of PR #1370, normal
  deployment and publication of all 32 articles. Reviewed head
  `403d8204c27fd89653990cb1b8e624a1f87c5bcc` had 21 successful checks; merged and
  deployed revision is `7524c25995d59f3826227e693d52f2ef5b3a19a2`.
  The official post-deployment verifier recorded 11 passes and zero failures.
  Actual container reads matched all 32 pack files and 338 asset files.
  Fresh baseline is `02c126e6a56a45544b0769b15cc18d74bb26af86420be3e6beda4712aa920054`.
  All nine production dry-runs and the full database backup completed. The real
  isolated restore/publication rehearsal is running; no production article write
  has occurred. The earlier synthetic rehearsal remains historical evidence.
  This record's life-eight subset shares a pinned journal with the separate
  business-four record; count only this task's own article operations.

### Actual owner-approved publication and public acceptance

This scoped record is now backed by genuine publication: 13 articles, 52 previously missing languages, 0 approved source corrections and 52 selected publication operations. Normal deployment, the real restore/publication rehearsal and production replay passed. The original driver completed with exit 0 at 2026-10-07T15:40:06 UTC and cleared its owned hold after verified evidence transfer.

Public verification covered 65 five-language pages and 130 original desktop/mobile views in this record. Four actual independent reviewers read disjoint partitions; all document/image/DOM/canonical/hreflang/sitemap guards passed. The eight record outputs were validated and copied only into their existing claimed release scopes. Sanitized evidence is `docs/article-localization/releases/2026-10-07-travel-life-wave/evidence.json`.

The full post-publication census observed 830 incomplete articles / 3,320 missing language documents. The global program remains open. All-guides link checks exited 1 in every locale; selected findings are exclusively unpublished related target languages. Actual per-record counts and this limitation are retained in evidence.json, rather than claiming an all-guides PASS. The earlier authoring/rehearsal notes above remain historical checkpoints. The record PR is the final documentation step.

The sanitized release-record draft PR is https://github.com/x812033727/travel_scanner/pull/1373. Its record files preserve the exact verified bytes and actual publication evidence. This scoped release is complete; the global localization program remains open.
