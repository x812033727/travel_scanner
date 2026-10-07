---
id: 2026-10-07-accept-native-path-separators-in-stock
title: Accept native path separators in stock credit CLI test
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T10:24:14Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/media.test.mjs
---

# Accept native path separators in stock credit CLI test

## Why

The stock credit CLI test expects docs/videos/fixture-minimal/video.json with
forward slashes, while the actual successful Windows output uses native
backslashes. The substantive photo/credit assertions are unrelated to that
separator difference. Observed in the full Node24.19 tools run.

## Definition of done

- [ ] The real output path and photo/credit message are validated on both platforms.
- [ ] Incorrect paths or missing credits still fail the test.

## Steps

- [x] Record the actual native-backslash output and failing forward-slash regexp.
- [ ] Normalize or escape the expected native path in the narrow test assertion.
- [ ] Run the affected stock test on Windows and exact-head Linux CI.

## How to verify

Run node --test --test-name-pattern "stock fetch stores the photo" tools/video/media/media.test.mjs.
Do not change real media, provider requests or production stock behavior solely
to match a Linux path string in a Windows test.

## Notes

The full local tools run exited1; no media implementation change was made here.
