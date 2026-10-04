---
id: 2026-10-04-adopt-approved-devday-bookend-replacement-and
title: Adopt approved DevDay bookend replacement and retain original YouTube thumbnail
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-04T04:41:53Z
completed_at:
branch:
depends_on:
  - 2026-10-01-hand-off-owner-approved-renewed-finals
scope:
  - docs/videos/branding-release/2026-10-04-devday-handoff.md
---

# Adopt approved DevDay bookend replacement and retain original YouTube thumbnail

## Why

The DevDay 2026 explainer was produced locally without the channel bookend default.
An isolated replacement adds the existing verified five-second opener and
three-second outro while retaining every encoded body video packet and the
original approved YouTube thumbnail. Its owner renewal must be approved before
the canonical production snapshot, chosen languages, and publish package can
adopt the new final. The existing source-bound handoff implementation remains a
dependency; never bypass its stale-source protection.

## Definition of done

- [ ] Read back the latest exact owner-approved renewed final before any activation;
      pending approval leaves both original and candidate snapshots intact.
- [ ] Activate only a verified source-bound canonical snapshot and regenerate every
      selected caption/dub/presentation manifest for the five-second offset.
- [ ] Publish/language review sources and downloadable final bytes match the renewed
      final SHA, branding hash, original body proof, and current language selection.
- [ ] The publish and actual YouTube thumbnail attachment remains the original
      approved JPEG SHA-256 `49ddfda07a3c7ac95a00920ac27a385c51e8afef32ba4ceed9de9561940f721b`.
- [ ] No paid narration/picture regeneration, automatic approval, upload, scheduling,
      or uploader enablement occurs without its separate existing authorization.

## Steps

- [ ] Inspect the external `branding-audit-20261004` candidate/receipt and fresh
      owner review, publication state, language choices, and worker inactivity.
- [ ] Apply the completed dependency's verified handoff; preserve original decisions,
      source final/checks/timeline/narration, image caches, and all caption/dub bodies.
- [ ] Rebuild canonical checks, metadata/chapters, captions, and selected language
      proofs without rewriting approval identities to make checks pass.
- [ ] Package and submit the current source-bound publish/languages review, then
      verify exact downloadable media and original thumbnail byte hashes.

## How to verify

Compare the final and attachment SHA-256 values against the current owner-approved
renewal. Verify seven chapters, every caption's +5000 ms offset from the unchanged
body timeline, unchanged original thumbnail bytes, and all chosen language source
bindings. A pending renewal or successful HTTP response is not canonical adoption
or YouTube publication. Record activity guards immediately before activation.

## Notes

Submitted owner renewal review: `101dc061-4b83-4845-9137-a9a71ff32d27`, created
2026-10-04T04:53:58Z and read back as `pending`, `manual_review=true`.
Original final/publish decisions were retained as superseded with unchanged files;
`ready_to_upload=false`, YouTube id/schedule null. Read fresh owner approval before
adoption; the audit submission is not authorization to approve or upload.

Source final SHA-256: `01deb03e57d1010e234da402dc64137bda329df92a1b04e85120441ada2245ab`.
Candidate final SHA-256: `4c1041bb469cde7ba3047cbdf11e363045689cc73d25812d0273da88ba896514`.
Branding SHA-256: `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`.
The isolated candidate has 24301 encoded frames; source body has 24061, intro150,
outro90. Nominal frame-grid duration is 810.0333 seconds; actual container duration
is 810.1000 seconds. Body packet timestamps shift exactly five seconds and all
24061 compressed video packet hashes match the original. The original AAC tail
holds the last body picture by under 0.1 seconds at the outro; do not confuse that
container timing with the exact cue/body offset.

Current owner-selected languages are en/ja/ko metadata+captions+dub and zh-CN
metadata+captions. Read them again at adoption; do not invent completed translations
or reuse stale timing. The independent audit and preservation proof are outside Git.
