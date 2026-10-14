---
id: 2026-10-14-correct-a21-pringles-patent-fact-and
title: Correct A21 Pringles patent fact and re-review source plan
status: blocked
priority: P1
area: docs
owner: codex-8a78-a21
claimed_at: 2026-10-14T14:29:44Z
created_at: 2026-10-14T14:16:39Z
completed_at:
branch: codex/brand-stories-five-20261014
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

- [x] A21's origin, affected `must_verify` claim and source description accurately say the patent lists two possible processes and do not infer the actual launch-era formulation from it.
- [x] The 2004 formulation change and scope of the British case are clear; the five-film treatment was checked against the corrected source plan before generation.
- [x] A different reviewer read the primary patent and court judgment, recorded a fresh review bound to the updated story SHA, and the compiled `stories.json` validates with no new problems. The owner-approved story ID, slug, schedule slot and title are unchanged.

## Steps

- [x] Check the patent's filing and grant text boundary, and the 2008 judgment's paragraphs 1–2.
- [x] Update A21 JSON only where the claim or its supporting description is wrong; have an independent reviewer produce the new `reviews/A21.json`.
- [x] Recompile and inspect the generated diff, especially `stories.json` and `SCHEDULE.md`; no active production episode was touched.

## How to verify

Run `node tools/video/story-plans/validate.mjs --hash A21`, compare it with `reviews/A21.json.story_sha256`, then `node tools/video/story-plans/validate.mjs --only A21` and the full `node tools/video/story-plans/validate.mjs`; check the changed prose against patent paragraph beginning "The present packaging approach" and the court's 2004-formulation scope. `npm run check:tasks` and inspect the compiled diff.

## Notes

Filed during the five-film work in `docs/videos/brand-stories-five-20261014/` after read-only QA. This is a factual correction in the existing approved story bank, not permission to change its release order or perform a production-host import. The original 2026-09-28 review repeats the mistaken inference in its change log; a new independent review must not silently reuse it.

2026-10-14 completion: an independent reviewer checked US3498798A, the 2008 High Court decision and the 2009 Court of Appeal decision, narrowed the logline/question to Regular Pringles after the autumn 2004 reformulation, and bound the revised review to SHA `35f8de6e6f2c5ecbd56931a801aec89d58f663168a9f335882ba5d21e3eec34b`. `validate.mjs --write` regenerated `stories.json`; `SCHEDULE.md` had no diff. Full validation: 100 stories, 0 problems and 70 pre-existing thumbnail warnings. No host import or media generation occurred.

Board housekeeping is blocked: `npm run tasks -- done` wrote a completed copy to `tasks/done/` but left this open copy after its removal failed; a subsequent exact-file `Remove-Item` was rejected by automatic policy. The local duplicate makes `npm run check:tasks` fail. Keep only this open copy in the PR until the owner manually removes it, then add the completed copy and rerun the board check. Do not treat the local duplicate as a finished board move.
