---
id: 2026-10-03-batch041-english-intake-length
title: Resolve Batch041 English intake length without losing information
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T10:02:59Z
completed_at:
branch:
depends_on:
  - 2026-09-28-review-batch041-on-page-and-image
scope:
  - apps/api/app/guides/content/on-page-seo-workflow.json
  - apps/api/app/guides/content/image-seo-workflow.json
---

# Resolve Batch041 English intake length without losing information

## Why

The Batch041 summary correction resolves the first-block failure in all ten
editions. Strict intake now passes eight editions, but the English documents
still fail its unchanged 1500-6000 body-length band: `on-page-seo-workflow` is
7020 characters and `image-seo-workflow` is 6526. These length failures existed
before the structural correction. Scoped pack lint reports them as advisories;
that does not make strict intake pass.

The complete English text was preserved. The owner has been asked whether to
keep it and retain this follow-up, or compact it while preserving every piece
of information. No response is inferred from the preselected option. Pending
an answer, keep the full text and report the strict failures accurately.

## Definition of done

- [ ] Record the owner's editorial choice before compacting the English text.
- [ ] If compacting is requested, both English editions pass the unchanged strict
      length band and retain every fact, step, qualification, example, link and
      source from the complete versions, with independent review.
- [ ] Refresh exact document/review hashes and run scoped pack, locale and intake
      checks after any edit; preserve all other locales and assets.
- [ ] Keep publication and live source reconciliation separate. Retaining the
      full text alone does not resolve or waive the strict length failure.

## Steps

- [ ] Read the complete five-language packs and the summary-correction evidence.
- [ ] Follow the owner's choice. If full text is retained, leave this ticket open.
- [ ] For an approved compact version, make an information-preservation checklist,
      obtain independent review and bind the review to the new exact hashes.

## How to verify

Run the existing strict intake `intake_check.py --from-content` separately for
both slugs and English. Also run scoped `app.guides.pack_cli lint` and locale
checks. Passing pack lint alone is insufficient; retain the strict output and
the independent semantic comparison.

## Notes

- Filed during the 2026-10-03 continuation on draft PR #1175, after searching the
  open queue for both slugs and length failures; no separate length ticket existed.
- The baseline for this follow-up is the summary-corrected repository content:
  on-page raw SHA-256
  `7219c405f799af8e0c52d751473aec92be68e05bd7ad02514a8a0e4010157df4`;
  image raw SHA-256
  `2811ab71370444a67d7cd1c40933cfe4d4b1e4ed5f96dde8c9345e73fa23815a`.
- Local source-correction evidence is retained outside Git in
  `batch041-summary-20261003`; receipt SHA-256
  `c753afebaf3f8ff5235dae2da7722aef8b6b014e02d141a45f0fef5767ca80a5`.
  It records actual repository before/after hashes, not live publication versions.
- Do not shorten content merely to hide a warning, change the global intake
  thresholds, reuse an old translation approval for edited hashes, or claim
  production publication from these local checks.
