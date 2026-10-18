---
id: 2026-10-07-release-localized-travel-life-wave-20261007
title: Release reviewed travel and life localization wave 20261007
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-07T05:55:30Z
completed_at:
branch:
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

- [ ] Merge content PR with all required checks green on the exact head.
- [ ] Obtain exact PR/SHA deployment approval and verify deployed content/assets.
- [ ] Build a new production baseline and reviewed bundle with 52 authorized targets.
- [ ] Obtain publication approval after read-only dry-run and verify a recoverable backup.
- [ ] Publish through one durable journal; verify replay writes nothing.
- [ ] Verify all target pages, diagrams, language links and desktop/mobile layouts.
- [ ] Save sanitized release evidence and refresh the full production gap inventory.

## Steps

- [ ] Verify no conflicting staged release, lock or publish hold before deployment.
- [ ] Freeze exact merged Git candidate bytes and independently reviewed target hashes.
- [ ] Compile with a fresh post-deployment full baseline, checking every target absent.
- [ ] Use dry-run, drafts, publish-articles and publish-hubs with the same pins/state.
- [ ] Rebuild/check article links, rerun dry-run and perform public acceptance.
- [ ] Record release results in README.md/evidence.json and open the record PR.

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
