---
id: 2026-10-28-correct-misleading-ai-concept-source-links
title: Correct misleading AI concept source links and zero-shot image text
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-28T13:45:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-fine-tuning.json
  - apps/api/app/guides/content/ai-term-few-shot-prompting.json
  - apps/api/app/guides/content/ai-term-multimodal-ai.json
  - apps/api/app/guides/content/ai-term-zero-shot-prompting.json
  - apps/web/public/guides/ai-term-zero-shot-prompting/hero.svg
  - docs/article-localization/source-corrections/20261028-ai-concept-links
---

# Correct misleading AI concept source links and zero-shot image text

## Why

Full source review before localization found four public Traditional Chinese AI
articles with a normal-language word linked to an unrelated AI term. Three
labeling/provenance usages point to Token; an appliance product-evaluation phrase
points to AI Evals. Actual image review also found zero-shot's hero description
describes objects not present in its original illustration. These source issues
must be explicitly corrected before translating the affected articles.

## Definition of done

- [ ] All four exact misleading ArticleInline nodes become TextInline without changing visible text or unrelated source values.
- [ ] Zero-shot hero alternative text and matching SVG desc accurately describe its actual illustration; visible geometry and original JPEG remain preserved.
- [ ] An independent native source-correction review binds the complete old/new documents, current source/draft/published versions and all changed asset hashes.
- [ ] Scoped content checks, candidate review and a source-fix PR pass; guarded publication and subsequent fresh localization baselines have explicit separate release evidence.

## Steps

- [ ] Finish complete source and primary-reference review; document/image inspection is complete but multimodal primary-reference review remains.
- [x] Prepare four exact one-inline candidates outside Git without applying them to repository or production.
- [ ] Integrate the zero-shot hero-description correction into its candidate and independently review the complete final delta.
- [ ] Recheck ownership and source/target drift, claim this scope, apply reviewed candidates and run source-correction/content checks.
- [ ] Prepare a separate guarded correction release before starting translations against the corrected sources.

## How to verify

Use source_correction.verify_review against the fresh pinned source rows. Reverse
each exact pointer change and confirm the complete prior document is restored.
For removed links, concatenated visible inline text must remain identical. Verify
source image hashes and actual pixels; source alt changes require new independent
approval and do not inherit a PASS from this narrow link-only candidate review.
Keep raw snapshots, documents, candidate files and reviewer evidence outside Git.

## Notes

- Fresh repeatable-read snapshot at 2026-10-28T13:31:16 UTC came from deployed
  `911443f2d0fb102dbe501d265849746af185a787`. All four source rows were clean
  and published; the target locales were absent. This is preparation evidence,
  not action-time production permission or publication.
- Exact original pointers:
  - fine-tuning `/blocks/5/inlines/1`: sequence labeling uses the word 標記,
    but it links to `ai-term-token`.
  - few-shot-prompting `/blocks/10/inlines/1`: marking an example inapplicable
    uses 標記, but it links to `ai-term-token`.
  - multimodal-ai `/blocks/19/inlines/1`: source/provenance labeling uses 標記,
    but it links to `ai-term-token`.
  - zero-shot-prompting `/blocks/10/inlines/1`: appliance product evaluation
    uses 評測, but it links to `ai-term-evals`.
- Four link-only candidate index SHA256:
  `b80984106e8147e6616345fe2acd1b926398eb2e22ffd991dff937f77eb9009a`.
  Each candidate has one node change, no visible-text/image/metadata/source-date
  changes, schema validation and exact reverse reconstruction. These candidates
  are not installed or published and do not contain approved review receipts.
- A later independent review produced four native source-correction receipts
  for these exact link-only deltas; verify_review and readback passed four times.
  Review-index SHA256:
  `5bbebf8101a1e9a4d45b2f8830a0f7cf380d7a3f0182f5d00e01e8f949965351`.
  This approves only the pinned four node changes, not publication or complete
  source readiness. Zero-shot's image-description issue remains, and multimodal
  still needs its full primary-source audit. Native schema normalization resolved
  an initial omitted-description versus empty-string comparison; the initial
  failure and unchanged raw exact-reconstruction checks remain preserved.
- Complete seven-article actual source-image review SHA256:
  `885aaae8a427f89937e7ad8d1f99a6c7bc0802cf051c776260ceed45559f3db4`.
  Zero-shot's hero shows an open manual, orange circle and right-pointing arrow;
  its old description instead claims a question marker and a step card. Confirm
  the exact proposed wording and SVG metadata against the actual pixels again.
- Tokenization's two alt/SVG metadata corrections belong to the separate active
  two-concept localization task. Knowledge-cutoff retains its own uncompleted
  thirteen-source freshness review; neither is included in this scope.
