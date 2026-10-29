---
id: 2026-10-28-correct-misleading-ai-concept-source-links
title: Correct misleading AI concept source links and zero-shot image text
status: review
priority: P2
area: api
owner: codex-next-source-readiness
claimed_at: 2026-10-29T01:06:46Z
created_at: 2026-10-28T13:45:32Z
completed_at:
branch: codex/ai-concept-source-corrections-20261029
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
The complete multimodal audit also requires the Chinese expansion of OCR on
first use; this stays within the already scoped multimodal content pack.

## Definition of done

- [x] All four exact misleading ArticleInline nodes become TextInline without changing their visible text or unrelated source values.
- [x] Multimodal expands OCR to 光學字元辨識（OCR） on first use without changing its conditional explanation.
- [x] Zero-shot hero alternative text and matching SVG desc accurately describe its actual illustration; visible geometry and original JPEG remain preserved.
- [x] An independent native source-correction review binds the complete old/new documents, current source/draft/published versions and all changed asset hashes.
- [ ] Scoped content checks, candidate review and a source-fix PR pass; guarded publication and subsequent fresh localization baselines have explicit separate release evidence.

## Steps

- [x] Finish complete source and primary-reference review, including multimodal's full audit and a targeted current primary-reference refresh for all four sources.
- [x] Prepare four exact one-inline candidates outside Git without applying them to repository or production.
- [x] Integrate the zero-shot hero-description correction into its candidate and independently review the complete final delta.
- [x] Recheck ownership and source/target drift, claim this scope, apply reviewed candidates and run source-correction/content checks.
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
- Follow-on preparation after the PR #1914 content checkpoint remains local to
  this future source task; none of these candidates has been applied or published.
  Multimodal's complete 32-block audit checked its two cited primary pages and
  eight additional official pages, with facts passing. It also found OCR lacked
  its Chinese expansion on first use at `/blocks/0/items/2`. A new private
  candidate combines that exact expansion with the existing wrong-link removal.
  Independent full-source/delta readback passed with zero findings; native review
  SHA256 `a64fe387361cf5e7854852a72247abd26dba70f2f854a43802923cc1a6158108`.
  Corrected canonical SHA256:
  `0c13a13cfa8909d81533ca563f8f688b62f9a1a35410409f7445b1cb9571b961`.
- Zero-shot's complete private candidate now combines its link removal, accurate
  hero alternative text and matching SVG desc. Exact reverse reconstruction and
  independent actual viewing/re-rendered pixel equality passed. Native review
  SHA256 `b1c8b852fc4af0143f39e4b1c4eef49d8ca0b42e48d936dbe70fecaf314ccf89`;
  corrected canonical SHA256:
  `cdb0f81143fbdcf55694fab817fd25e73fc0867ae35f2db3dcc1c859fceb3eba`.
- These approvals bind private candidates and the retained original pins only.
  Recheck fresh production/repository versions and ownership before applying;
  preserve original source dates and assets. They do not authorize publication
  and must not reuse the old link-only receipt for a changed full candidate.
- A fresh read-only snapshot at 2026-10-29T00:56:21.795830+00:00 revalidated all
  four original documents, current versions, clean drafts, absent target rows
  and twelve source assets. Snapshot SHA256:
  `54bdec3f6b4729a911ba430aa688e12e158ccdc0427b22af6671400bd42217ad`.
  Native source-correction verification passed for the four complete candidates;
  their exact old/new hashes and independent reviewers are recorded in
  `docs/article-localization/source-corrections/20261028-ai-concept-links/evidence.json`.
- The four reviewed candidates and zero-shot SVG description are now installed
  on the isolated source-correction branch based on
  `7e380b739645d942cf225c8c70ddb7290d253641`. The prior follow-on notes above were
  preserved verbatim. Original attempts and raw evidence remain external.
  This draft adds no translations and does not authorize or perform publication.
- Local checks passed: four scoped pack lint entries, four native reviews against
  the final staged blobs, twelve source asset hashes and two existing packaged
  content/image tests. Task validation passed with unrelated existing warnings.
  Final staged verification SHA256:
  `9229ce60eaf8c3e7b717c1d19fb1749700ac1a58780f1ba2cc893980e4331e12`.
- Keep this task open until the separate guarded source publication and a fresh
  corrected-source localization baseline have their own evidence. The current
  two-article translation release grants no production authority for these four
  sources.
