---
id: 2026-10-07-accept-windows-separators-in-stock-fetch
title: Accept Windows separators in stock fetch output regression
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T04:08:54Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/media.test.mjs
---

# Accept Windows separators in stock fetch output regression

## Why

The stock-fetch regression at media.test.mjs:483 expects the diagnostic source
path to contain forward slashes. On Windows the actual successful output uses
the native separator in `docs\\videos\\fixture-minimal\\video.json`; the
picture and credit were stored correctly, but the assertion fails.

## Definition of done

- [ ] The regression verifies the same source asset/credit on Windows and Linux
      while accepting the platform's diagnostic path separator.

## Steps

- [ ] Narrow the assertion to preserve the asset-count/credit behavior check.
- [ ] Run the focused case on Windows and Linux.

## How to verify

`node --test --test-name-pattern="stock fetch stores the photo"
tools/video/media/media.test.mjs`.

## Notes

Observed in the 2026-10-07 complete Windows tools run, actual exit 1. Raw evidence
is retained outside Git in
`<home>/mokaair-work/handoff/renewed-finals-20261007/native-unit-full-tools-check-20261007.log`.
No provider or production operations are needed for this mocked regression.
