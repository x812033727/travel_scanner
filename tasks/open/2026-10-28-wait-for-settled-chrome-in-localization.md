---
id: 2026-10-28-wait-for-settled-chrome-in-localization
title: Wait for settled chrome in localization browser captures
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-28T13:03:09Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/article-localization/references/bundle-release.md
---

# Wait for settled chrome in localization browser captures

## Why

The 2026-10-28 AI-foundation release captured all sixty article bodies and 120
screenshots, but waiting for fonts and article images did not ensure the site
navigation had left its discovery-status loading placeholder. One Simplified
Chinese inference desktop capture retained that placeholder; a separate actual
capture after the navigation links became visible showed the complete header.
A different English desktop capture ended before the final copyright strip,
while its mobile capture included it. These are capture-readiness limitations,
not evidence that the translated documents or site navigation are missing.

## Definition of done

- [ ] The bundle-release acceptance guidance requires bounded, observable site-navigation readiness and stable page geometry before desktop/mobile capture.
- [ ] It distinguishes original capture limitations from confirmed product defects and requires append-only supplemental evidence when needed.
- [ ] It preserves the original screenshot hashes, genuine view timestamps and failed attempts rather than replacing evidence or treating partial views as complete.
- [ ] Capture guidance requires rechecking the actual pacing deadline after a timer wakes and retaining real timing telemetry; exact-threshold failures are never hidden by rewriting timestamps.

## Steps

- [ ] Document a specific site-header selector, completed navigation state, font/image readiness and stable document-height checks for each viewport.
- [ ] Document independent review of visible article text, source/footer boundaries and intended horizontal scroll regions without claiming invisible pixels were reviewed.
- [ ] Describe how a narrow supplemental capture is linked to its original PNG and actual network receipt without rerunning successful publication or overwriting captures.

## How to verify

Review the guidance against the actual 2026-10-28 AI-foundation release evidence.
A delayed navigation-status response should prevent a final settled-header claim.
A page-height change should be reconciled before claiming a full footer capture.
Keep article-body correctness, network success and visual acceptance separate.
Run `npm run check:tasks` and any checks needed by the eventual documentation edit.

## Notes

- The original browser report SHA is
  `99f4e98c0740ed56e0dc8290a2ec1c3f93dcd2da9ee6cd8be89a0b82a546eb49`.
- Original affected header PNG:
  `fa4c7e806f6528c17ead6f023fbfc0dc81194512b50c7e71810db99b07ff069b`.
- Settled-header supplemental PNG:
  `fb5dcbfde0ecb1ca711cdfec665ff7f273b83e6eb429aeb86d83ad30198c654e`.
  Its nineteen actual requests were HTTP 200. An earlier supplemental attempt
  also had nineteen HTTP 200 responses, then stopped on a local ambiguous
  `header` locator. That failed attempt remains preserved; `.site-header` resolves
  the selector without changing or retrying a failed HTTP response.
- This unclaimed follow-up does not authorize publication, deployment, modifying
  the sealed original collector/captures, or changing current production code.

- The same capture had one recorded 1299 ms request-start interval against a
  configured 1300 ms minimum (ids 250 to 251). All other 459 gaps met the minimum,
  all 461 responses were HTTP 200 and there was no recorded request overlap.
  The original strict assembler stopped, and its failure remains preserved.
  Independent review SHA:
  `02eced16f3cec65ebd0820488c0fda3290e90ffdd8b32dd83e376140e54d9b4e`.
  The collector used a single timeout followed by Date.now without rechecking
  its deadline. Do not infer the precise clock cause from those wall timestamps.
  A separately reviewed, exact-capture operational decision may record this
  deviation explicitly; it must not become a generic relaxed threshold or a
  claim that strict 1300 ms pacing passed. This task addresses future capture
  guidance and does not alter the original sealed evidence.