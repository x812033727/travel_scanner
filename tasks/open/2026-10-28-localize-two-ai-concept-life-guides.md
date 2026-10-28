---
id: 2026-10-28-localize-two-ai-concept-life-guides
title: Localize two AI concept life guides into four languages
status: in-progress
priority: P1
area: api
owner: codex-gpt6-ai-concepts-20261028
claimed_at: 2026-10-28T13:35:22Z
created_at: 2026-10-28T13:34:08Z
completed_at:
branch: codex/localize-ai-concepts-20261028
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-tokenization.json
  - apps/web/public/guides/ai-term-tokenization
  - apps/api/app/guides/content/ai-term-foundation-model.json
  - apps/web/public/guides/ai-term-foundation-model
---

# Localize two AI concept life guides into four languages

## Why

The owner requested continued completion of missing travel-information and life
article languages. These two public AI concept life articles have no English,
Japanese, Korean or Simplified Chinese documents in the repository or the fresh
selected production snapshot. This narrow content child of the existing
missing-locale program adds the eight documents and translates all text-bearing
artwork. Foundation-model's source remains unchanged. Tokenization needs two
explicitly reviewed alternative-text and matching SVG description corrections;
its article body, original JPEG, visible diagram text and geometry remain intact.

## Definition of done

- [ ] Fresh production source/visibility/version and target-absence bindings pass, and full source text/artwork review finds no unresolved blocking issue.
- [ ] All eight translations and their artwork pass schema/layout checks and independent hash-bound text, glyph and actual visual review.
- [ ] Native assembly, installation and replay pass; only independently approved tokenization source alt/SVG metadata corrections may differ from the original sources.
- [ ] Applicable content checks pass and a guarded content PR exists; a separate release task owns deployment/publication and public acceptance.

## Steps

- [x] Check current branches, worktrees, open PR file scopes, old jobs and publish holds before claim.
- [x] Export the selected read-only production snapshot and build the scoped native baseline.
- [x] Complete current primary-source and actual original-image review before starting translation.
- [ ] Prepare and run the unchanged native pipeline using the current ChatGPT login, at most three workers, no quota/auth retries and an external STOP sentinel.
- [ ] Render every job, obtain independent reviews and apply only recorded corrections with retained failed attempts.
- [ ] Assemble/install/replay, verify preservation, run scoped checks and open the content/release PR cycle.

## How to verify

Use the unchanged build_baseline.py, pipeline.py, render.mjs, assemble_bundle.py
and install_bundle.py with exact selected slugs/locales. Verify independent
review hashes against final native artifact manifests; schema success is not
editorial or visual acceptance. Run native pipeline/artifact/layout checks,
content-pack checks and task validation. CI must provide the real PostgreSQL
release-safety gate. Keep raw production data, jobs and reviews outside Git.

## Notes

- At 2026-10-28T13:31:16 UTC, a bounded repeatable-read snapshot from deployed
  `911443f2d0fb102dbe501d265849746af185a787` confirmed all seven sources public,
  active and unexpired, with clean published drafts and no target locale rows.
  The original ten-candidate snapshot also covers three held travel articles;
  this content scope selects only tokenization and foundation-model.
- All seven published canonical documents exactly match repository sources;
  no repository-only description preservation admission is needed.
- Scoped seven-article baseline SHA256:
  `d62d596e344498f584795b0be3eaa8c81b3f0ce82bbbafe10cf2ef889867bd11`.
  This is a selected-article baseline, not a whole-site census.
- The completed earlier 48-translation production release is separate. Its
  receipt PR #1913 does not authorize merging or publishing this new cohort.
- Travel source-correction tasks and the twelve-article AI income/investing
  batch retain their existing scope; no held or other-owned article is included.
- Initial preparation covered seven AI candidates and 28 unstarted jobs. Full
  source review found general labeling text incorrectly linked to the Token
  article in fine-tuning, few-shot-prompting and multimodal-ai; these are excluded
  pending explicit source corrections. Knowledge-cutoff requires a separate full
  refresh of its thirteen time-sensitive sources and is also excluded. Their
  original prepared inputs remain outside Git, without model calls or edits.
- The unpublished task id/title/scope was narrowed from seven, then three, to two before
  any translation attempt or content change. The original seven-source baseline
  and fresh snapshot remain immutable evidence of the candidate inventory.
- All 44 open PR file lists were checked, including the full exact-head local
  diff for a 9,286-file PR whose API result stopped at 3,000. No selected path
  overlaps were found; the native ownership survey also found no active task.
- Complete zero-shot source review additionally found the phrase about product
  evaluation in an appliance-manual example linked to the AI-evals article.
  That source is also held for explicit correction, rather than silently fixing
  its meaning only in translations. No translation attempts were made for it.
- Actual source-image review also found tokenization's hero and diagram
  descriptions claimed details not depicted. The two alt strings and matching
  SVG desc metadata have an exact correction candidate. It must receive an
  independent native source-correction receipt before application or tokenization
  translation. Original candidate jobs/baselines remain unchanged; corrected
  jobs use a new work root and a derived baseline retaining the old database pins.
- Foundation-model alone passed full text/primary-source and actual image
  review, and its four native translation calls have started. Its inputs remain
  the original clean published document.
- Tokenization's source correction now has independent native approval:
  `9653389d926c83b7015bff4827c6084ef95f3c147fc4a177e4b22f8905dad980`.
  Root applied only the two approved alt changes and matching SVG desc changes
  locally after verify_review passed. Four native old/new renders have identical
  pixels; original JPEG bytes, visible SVG text/geometry and body are unchanged.
  The actual public diagram SVG and unchanged JPEG are bound in the native
  receipt; editable hero.svg companion hashes/pixel identity are separately bound
  by independent evidence. No production document has been changed.
