---
id: 2026-10-13-local-assemble-warns-when-its-branding
title: Local assemble warns when its branding package is older than the host's
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-13T13:44:53Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/cli.mjs
  - tools/video/core/branding.mjs
  - docs/videos/BRANDING.md
---

# Local assemble warns when its branding package is older than the host's

## Why

The channel outro was lengthened to 21 s with music and room for YouTube end-screen cards on
2026-10-12 (`mokaair-brand-package-v4-endscreen`), and installed on the production host only.
This machine's `<workdir>/_branding/current.json` stayed on `mokaair-brand-package-v2-cc`
(installed 2026-10-04), so the five 奇聞檔案局 recuts assembled locally on 2026-10-13 pinned the
old 3 s outro: no music, no end-screen room. Nothing said so; the owner found it watching the
cut. The local copy was brought to v4 by hand that day (`branding --install
~/mokaair-work/channel-outro-20261012/package-v4/channel`).

## Definition of done

- [ ] A local `assemble`/`compile` of a new long video says, before it encodes, when the branding
      it is about to pin is not the one the site's worker uses (the id and hash of both), and
      how to install the current one; it does not silently go ahead.
- [ ] It works offline (no site reachable): it says it could not compare, it does not fail.
- [ ] BRANDING.md says local builds must match the host's package and how to check.

## Steps

- [ ] Find where the host's current branding can be read without SSH (an existing /admin or
      automation endpoint, or the worker's report); if none exists, decide with the owner
      whether to add a read-only one or keep a checked-in expected id instead.
- [ ] Add the comparison to the assemble/compile preflight, with tests.

## How to verify

Point a scratch workdir at an older package, run `assemble --dry-run` (or the preflight) and see
the warning; install the current one and see it go away.

## Notes

- Related: 2026-10-12-play-the-channel-intro-bumper-after (bumper position), being done on
  branch claude/bumper-after-condensation.
