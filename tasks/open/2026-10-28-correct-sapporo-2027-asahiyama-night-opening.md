---
id: 2026-10-28-correct-sapporo-2027-asahiyama-night-opening
title: Correct Sapporo 2027 Asahiyama night opening
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-28T07:36:34Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/sapporo-snow-festival-2027.json
  - apps/web/public/guides/sapporo-snow-festival-2027
---

# Correct Sapporo 2027 Asahiyama night opening

## Why

Fresh official-source review found a newly announced Asahiyama Zoo night opening
on February 5-7, 2027, until 20:30 with final entry at 20:00, during the Sapporo
festival period. The reviewed published v6 source still uses an absolute
"winter only until 15:30" heading and discusses only the 2026 special opening.
Its SVG also has an unqualified 10:30-15:30 label. Correct these dated statements
before translating this article, retaining the distinction between normal hours
and the newly confirmed exception.

## Definition of done

- [ ] Fresh official notice, source version/hash and exact affected pointers/assets are pinned.
- [ ] Body, SVG and matching image descriptions correctly distinguish general winter hours and the 2027 special opening.
- [ ] Existing repo-only description changes are explicitly preserved/admitted, without silently adding them to a narrow source correction.
- [ ] Independent source/visual review, applicable checks and guarded publication/readback complete before localization resumes.

## Steps

- [ ] Recheck current published source and other owners' scopes before claiming content files.
- [ ] Review the bounded candidate from the source audit, including headings, paragraph, SVG visible text/desc and image description.
- [ ] Render and independently review changed source artwork and exact document diffs.
- [ ] Publish through the normal source-correction safeguards, then create a fresh localization source baseline.

## How to verify

Read the current zoo official notice and normal winter schedule, retain the exact
URL/body/date evidence, and verify that the special dates fall within the
article's itinerary period. Run ArticlePack/SVG checks and compare all unchanged
fields/assets. Verify actual published document/image hashes after release.

## Notes

The independent October 28 source audit marks this article SOURCE_HOLD and
prepares a private candidate from the reviewed published v6 source. Initial
affected body pointers are `/blocks/15` and `/blocks/16`; the SVG general-hours
label at y=681 and matching descriptions also require review. No original source,
repository pack, baseline, model job or production row has been changed.

The separate `2026-10-07-enable-verified-sapporo-localization-route` task remains
necessary for the destination-route admission. Its earlier full-source PASS is
historical and cannot approve this new dated source. Raw primary-source captures,
hash-bound findings and candidate diffs remain outside Git. This task is open
and unclaimed; it does not authorize taking another owner's active source scope.

The private exact source-correction candidate has since passed an independent
review with zero findings. Receipt SHA256:
`5eb707ca6a54c196effbadb4f0761c705ac603dc60aee4e7654e703234f96068`.
That review confirms exactly five document pointers and three SVG text nodes,
unchanged diagram geometry/date bars, and actual viewing of the candidate plus
an independently rendered image. It verifies candidate correctness only; fresh
production source/version/asset guards and explicit repository-description
admission remain required before any apply. No source HOLD has been cleared.
