---
id: 2026-10-07-support-proven-thumbnail-encoding-in-renewal
title: Support proven thumbnail encoding in renewed-final publish packages
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T01:42:32Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
  - docs/videos/BRANDING.md
---

# Support proven thumbnail encoding in renewed-final publish packages

## Why

The approved EP01 and EP02 thumbnails are PNG files of 2,300,538 and 2,181,977
bytes. Native renewed-final preparation preserves those exact bytes as
`upload/thumbnail.jpg`; package staging correctly refuses images above 2 MiB.
The existing submission binder also correctly rejects replacing that file after
preparation. A source-bound codec export must be explicit rather than overwriting
the owner's image, changing a receipt, or regenerating paid artwork.

## Definition of done

- [ ] An oversized approved thumbnail can gain a bounded encoding derivative with
      original evidence retained, exact source approval and unchanged final,
      metadata, selected-language contract and canonical receipt.
- [ ] Lossless and JPEG derivatives declare their actual pixel relationship;
      changed geometry, missing source evidence, stale approvals and oversize output
      fail closed. A codec export never pretends to be a new human approval.
- [ ] The actual package report, API schema and Python package consumer validate
      emitted files; uncertain review submission remains held without blind retry.
- [ ] Transport declares the actual image byte type even when historical upload
      filenames end in `.jpg` but their approved contents are PNG.

## Steps

- [ ] Review the guarded operator projection from the 2026-10-07 handoff and choose
      a narrow native receipt/derivative contract without weakening source guards.
- [ ] Add regressions for changed originals, incorrect encoding claims, metadata
      identity, image size, MIME accuracy, canonical preservation and unknown
      submission outcomes. Extend scope to the native attachment transport if needed.
- [ ] Document codec export versus new artwork and owner review requirements.

## How to verify

Run focused handoff tests and the real Python package reader against emitted
fixtures. Compare decoded geometry and actual pixels for lossless output; for JPEG
retain encoder settings, both file hashes and measured quality with an explicit
lossy declaration. This ticket does not authorize paid media or production writes.

## Notes

- Operator evidence lives outside Git at
  `<home>/mokaair-work/handoff/renewed-finals-20261007` and on the host at
  `/root/renewed-finals-20261007`.
- Ordinary bounded PNG compression could not bring EP01 below the actual limit;
  preserving unchanged approved artwork through a high-quality JPEG codec export
  is separate from generating a new image. Retain the complete original PNG and
  its content-credential bytes as evidence; changed files must not claim that the
  original credential signature remains valid.
- Do not relax native exact-hash binding merely because the API accepts a file.
  An explicit derivative contract must independently prove the source and all
  other package bytes before a review is submitted.
- Independent live-source review found the same filename issue for EP03-EP06:
  the original PNG bytes fit the size limit, but default `uploadCandidate` derives
  `image/jpeg` from `.jpg`. Their new base reviews are accepted by the actual Python
  parser, which does not sniff image bytes; that parser pass is not MIME validation.
  Selected-dub holds still prevent complete upload packages. Correct this before
  any future upload. Review submission deduplicates the metadata SHA even for
  superseded rows, so merely resubmitting corrected file declarations is not a
  legitimate repair. Preserve the approved source and use an explicit versioned
  package/source contract; never mutate a prior review or its receipt.
