---
id: 2026-10-07-correct-japan-tax-free-shop-logo
title: Correct Japan tax-free refund conditions and complete four languages
status: done
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T06:31:58Z
created_at: 2026-10-07T05:10:25Z
completed_at: 2026-10-07T06:37:46Z
branch: codex/refund-source-correction-v2-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/japan-tax-free-refund-2026.json
  - apps/web/public/guides/japan-tax-free-refund-2026
  - docs/article-localization/source-corrections/20261007-refund-logo
  - docs/article-localization/installations/japan-tax-free-refund-2026.json
  - docs/article-localization/installations/bundles/05e3b08b830ab2e5
  - .codex/localization-staging/refund-v2-05e3b08b
---

# Correct Japan tax-free refund conditions and complete four languages

## Why

The public refund guide incorrectly says displaying the Japan Tax-free Shop
recognition logo is required to offer tax-free sales. The official MLIT symbol
FAQ says display is voluntary; licensing is the actual condition. This prevents
independent approval of the four missing-language drafts.

## Definition of done

- [x] Correct the exact source claim with independently reviewed, hash/version-bound evidence.
- [x] Preserve all other source content, article metadata, image bytes and credits.
- [x] Correct all four staged language documents against the approved source correction.
- [ ] Release only with fresh guarded source/target checks, backup and public validation.

## Steps

- [x] Pin the current published source and the exact wrong statement.
- [x] Prepare the exact source correction and four target-language wordings externally.
- [x] Obtain an independent `source_correction.py` receipt and validate its complete binding.
- [x] Apply only approved changes, finish image/text review and prepare guarded bundle/PR.
- [ ] Publish and verify the corrected source plus four missing languages through a release ticket.

## How to verify

Read MLIT's official symbolmark page and symbol-system Q&A section II Q2.
Use `source_correction.verify_review` against the fresh baseline to check the old
document, versions, exact pointer diff and corrected hash. Verify all staged
language wordings against the reviewed corrected source, then run bundle/content
checks. Publication must recheck source/draft hashes and article visibility.

## Notes

- Source finding evidence SHA `2f661ee74cbad36bbfc87fbfd919dfa93e3caa949ef3113187fa451f57107444`.
- Exact source pointer: `/blocks/12/items/3`. SVG factual text is not affected.
- Existing source hash `6358cae7243f026ec6a2a27e9f26394e5805759ce42932ef92032a1367ff7c27`.
- Proposed corrected source hash `ab0599f26b31567acf38f33a2ef8bb2d359271e9f1dd01f7b9479e7b47f12b6f`.
- The proposal adds the licensed-store condition and clarifies that the logo is
  optional. It leaves the refund process and all other claims unchanged.
- Supporting sources:
  https://www.mlit.go.jp/kankocho/tax-free/symbolmark.html
  https://www.mlit.go.jp/kankocho/tax-free/content/001845126.pdf
- Four original translation attempts and any render failures remain preserved;
  no review PASS is granted while they repeat the incorrect source claim.
- Source proposal, target wordings and raw evidence live outside the repository.
  The proposed source has not yet been applied or published.

- The final reviewed proposal adds the direct logo FAQ citation, preserving the
  previous nine sources. Approved pointers: `/blocks/12/items/3` and `/sources`.
- Genuine schema-v1 review SHA
  `76955fa323223bd974ebd2d6bcfee124502289f99261fecd43c24cc1b77b43d1`;
  `verify_review` passed against old published versions and three unchanged assets.
- A derived correction baseline retains original database guards and repository
  pack hash. Four new jobs reuse unchanged translated source fields and apply the
  reviewed wording/citation. Original jobs/attempts remain immutable; new provider
  calls: zero. All four new documents pass full materialization.
- English diagram labels were compacted and freshly rendered successfully.
  Final independent whole-document/image review is still required; source pack unchanged.

### Full-rule source correction v2

The whole-document review exposed additional source errors: exported goods used
as consumables versus any opened/used goods, refund timing after customs export
confirmation versus physical departure, and a new gold/platinum coin exclusion
mislabelled as an unchanged rule. These require seven exact source-document
changes, including the optional-logo condition and direct FAQ citation, plus two
source SVG text slots. The earlier logo-only proposal remains historical.

Genuine independent v2 editorial receipt SHA
552fd065bbe7ffd3d4460f2d890ce820423e003f40623359bb5b90877051bb7e;
source_correction.verify_review passed from original source 6358cae7... to
8f19020e8412793852dd6502faa35f88b5953c950b06d456f6b20564f0308bb7.
Approved source SVG: before 905b853bd85559828d1716f96ad3bad59b3b61c69fe88c479f66c3c292f29e1b,
after 9abff5f9592df1cb0313f614aad9056e88d5934a5134c8d3ecc8215e3383ed81.
Only the matching description and refund heading change; geometry/styles/fonts
and original photos/credits remain preserved.

Fresh external v2 jobs retain original database versions and repository pack
pin, use the reviewed corrected source/SVG, and reuse previous translation fields.
Distinct root executor applied nine independently proposed compact EN/JA labels
to address 14px layout defects. Prepared plan remains historical before-label
evidence; current field hashes are bound by the distinct application receipt.
No provider call, source-pack installation or production change has occurred.
Actual source-SVG admission, official materialization/render, independent four-
language final review, official install, content PR and guarded release remain.
This correction is outside the first 13-article/52-document PR #1365.

### Final local authoring and release handoff

Four genuine independent final text/visual/glyph PASS receipts bind the current
post-render bytes. The English month heading has one distinct root-applied
correction with preserved before-job evidence; it was independently rechecked.
Complete four-target evidence SHA
`1123f321497a81d02e20e40658a1960752939e4488fdedf72b1d7d0217c35b1b`.
The official Route A assembler and bundle verifier passed; manifest SHA
`05e3b08b830ab2e5aa89c117f8d87f41891a3174991e17631eaeefdc118f1585`.
The unchanged official local installer and replay completed with exit 0;
pack/source/target assets, receipts and journal were byte-identical after replay.
Installed five-language pack SHA
`4f960fbb5b3c87883dbbb5e4704e8d27069f3175eb3e4ad4d2a295c4ca319f59`.
All normalized root metadata equals the original; both photographs/credits and
unreviewed source leaves are preserved. External four jobs pass admitted drift
and artifact guards.

This ticket closes local authoring/review/installation within the content PR.
Its unchecked publication requirements are handed to the open scoped ticket
`2026-10-07-release-reviewed-japan-refund-source-and`, not waived. CI, owner
merge/deploy approval, fresh database guards, verified backup/restore, production
dry-run/publication approval and five-language public QA remain mandatory.
Production has not changed; old jobs, attempts, source SVG and input baselines
remain preserved in owner storage.
