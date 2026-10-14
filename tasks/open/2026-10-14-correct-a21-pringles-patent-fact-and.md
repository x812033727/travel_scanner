---
id: 2026-10-14-correct-a21-pringles-patent-fact-and
title: Correct A21 Pringles patent fact and re-review source plan
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-14T14:16:39Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-plans/brand-stories-100/stories/A21.json
  - docs/videos/story-plans/brand-stories-100/reviews/A21.json
  - docs/videos/story-plans/brand-stories-100/stories.json
  - docs/videos/story-plans/brand-stories-100/SCHEDULE.md
---

# Correct A21 Pringles patent fact and re-review source plan

## Why

The approved A21 brand-story plan says the 1970 patent description rules out raw potato slices and specifies a potato dough as the product's actual process (`stories/A21.json` origin, `must_verify`, and source `supports`). The [US 3,498,798 patent text](https://patents.google.com/patent/US3498798A/en) explicitly permits **either raw potato slices or potato-based dough** for the packaging method. It does not establish which process a 1966 or launch-era Pringles product used. The later British VAT case concerned Regular Pringles after a formulation change in autumn 2004, as the [2008 High Court judgment paragraphs 1–2](https://caselaw.nationalarchives.gov.uk/ewhc/ch/2008/1558) says. A worker reading the current plan could regenerate a false origin scene or confuse the court's product with the patent examples. The five-film treatment fixes the wording locally, but the worker does not ingest it.

## Definition of done

- [ ] A21's origin, affected `must_verify` claim and source description accurately say the patent lists two possible processes and do not infer the actual launch-era formulation from it.
- [ ] The 2004 formulation change and scope of the British case are clear; any dependent script copy is checked before generation.
- [ ] A different reviewer reads the primary patent and court judgment, records a fresh review bound to the updated story SHA, and the compiled `stories.json` validates with no new problems. Preserve the owner-approved story ID, slug, schedule slot and title unless the owner changes the plan.

## Steps

- [ ] Check the patent's filing and grant text boundary, and the 2008 judgment's paragraphs 1–2.
- [ ] Update A21 JSON only where the claim or its supporting description is wrong; have an independent reviewer produce the new `reviews/A21.json`.
- [ ] Recompile and inspect the generated diff, especially `stories.json` and `SCHEDULE.md`; do not mutate an active production episode or assume the host will update from Git automatically.

## How to verify

Run `node tools/video/story-plans/validate.mjs --hash A21`, compare it with `reviews/A21.json.story_sha256`, then `node tools/video/story-plans/validate.mjs --only A21` and the full `node tools/video/story-plans/validate.mjs`; check the changed prose against patent paragraph beginning "The present packaging approach" and the court's 2004-formulation scope. `npm run check:tasks` and inspect the compiled diff.

## Notes

Filed during the five-film work in `docs/videos/brand-stories-five-20261014/` after read-only QA. This is a factual correction in the existing approved story bank, not permission to change its release order or perform a production-host import. The original 2026-09-28 review repeats the mistaken inference in its change log; a new independent review must not silently reuse it.
