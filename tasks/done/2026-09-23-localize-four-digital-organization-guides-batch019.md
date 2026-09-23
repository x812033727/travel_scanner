---
id: 2026-09-23-localize-four-digital-organization-guides-batch019
title: Localize four digital organization guides batch019
status: done
priority: P1
area: api
owner: codex-batch019
claimed_at: 2026-09-23T08:13:05Z
created_at: 2026-09-23T08:12:54Z
completed_at: 2026-09-23T09:11:57Z
branch: codex/article-localization-batch019-digital-organization
depends_on: []
scope:
  - apps/api/app/guides/content/browser-bookmark-project-folders.json
  - apps/api/app/guides/content/digital-receipt-archive.json
  - apps/api/app/guides/content/file-naming-system-for-home.json
  - apps/api/app/guides/content/phone-photo-declutter-workflow.json
  - apps/web/public/guides/browser-bookmark-project-folders
  - apps/web/public/guides/digital-receipt-archive
  - apps/web/public/guides/file-naming-system-for-home
  - apps/web/public/guides/phone-photo-declutter-workflow
---

# Localize four digital organization guides batch019

## Why

Four already-public life/productivity articles currently provide only zh-TW.
Complete en, ja, ko and zh-CN without changing existing source documents,
article metadata, publication state, photographs or image provenance.

## Definition of done

- [x] Sixteen complete language documents include every block, title, description,
      caption, alt text, source title and visible AI/provenance disclosure.
- [x] Sixteen localized SVG diagrams match the source semantics and pass desktop
      and mobile render review; textless original hero JPGs are preserved.
- [x] Independent content/image review binds the source and final artifact hashes.
- [x] Scoped pack/API/frontend/tool checks pass and the batch is submitted in a PR.
- [x] A separate release task records CI, merge, guarded import/publication and
      real public browser acceptance before claiming the languages are live.

## Steps

- [x] Inventory current repository, shared tasks, active branches and live source.
- [x] Claim exact four-article scope and split authorship into disjoint pairs.
- [x] Review outside-only translation/image candidates before root integration.
- [x] Preserve source models/assets and validate the exact integrated Git bytes.
- [x] Open the scoped PR and explicit remaining release task.

## How to verify

Use the existing article-localization pipeline and ArticlePack/GuideDocument
validators. Run scoped pack lint, content-pack/import tests, frontend lint,
i18n, typecheck/build, relevant tests, task validation and diff checks. Render
every new SVG, inspect reader-visible text and compare protected numbers/code,
links, source URLs/check dates and original metadata. Canonical assembly and
publication are separate acceptance gates, not implied by local content tests.

## Notes

Base: 017caac57c5ced78e95a58acb03981cab9874f92. Fresh read-only inventory captured
2026-09-23T08:08:30Z confirms each selected article is active/published at article
v1 with only zh-TW locale/published v6; full normalized draft/published/latest
source models match the repository. Existing source and image URLs and check
dates are preserved. No overlapping active scope or in-flight candidate found.

Outside evidence under `C:/Users/x8120/.codex/article-localization-release/`:
- `batch019-repo-only-candidates-20260923.json`, SHA256
  `e51293c301b1c82f1a5de50e73f7a5c09df3e46dd543a292baaf24f0a186828c`.
- `batch019-candidate-inventory/live-source-full-20260923T080827Z.json`, SHA256
  `ecce8f28e22246ed54bfa4ee67f07cd3aea007ce57829a93447651e3ffe31032`.

Author pair A owns browser bookmarks and digital receipts; pair B owns file
naming and phone photos. Authors write outside Git only. Root integrates after
independent review. Fifteen source blocks per article; source counts are 1, 2,
1 and 1 respectively. All four original hero JPGs were actually viewed and are
textless AI illustrations; localize disclosure wording while retaining provenance.
This task does not claim any new locale imported or published yet.

## Reviewed content and image evidence

The four packs now contain all five languages: the existing zh-TW document plus
en, ja, ko and zh-CN. Each of the sixteen new documents retains all fifteen blocks.
The twenty changed content files are exactly four packs and sixteen new SVGs;
the four original JPGs and four original SVGs remain byte-identical. Raw pack
metadata and the existing zh-TW document are preserved by reversible insertion.
Original source URLs, checked_on dates (2026-09-14), code and numeric conditions
are unchanged. AI/provenance descriptions are translated with creator identity
retained. No runtime code, schema, category, sort or visibility changes are made.

Evidence below is under
`C:/Users/x8120/.codex/article-localization-release/batch019-digital-organization/`:

- Pair A independent review: `independent-bookmark-receipt-review-v1/receipt-pass.json`,
  SHA256 `53e4552dd9a41eefc48ceb67a70e6503dd8b40a341bd3630c1461f364f23142d`.
  Reviewer `Codex /root/batch018_resume_review` read all eight complete documents
  and independently inspected all eight localized diagrams on desktop/mobile;
  949 checks passed, including 512 strict protected-field checks. The initial
  fit-width mobile preview was supplemented by complete horizontal-scroll views:
  `author-bookmark-receipt/mobile-render-receipt-v2.json`, SHA256
  `08b59f4c759335f903adf81037b46d52e0be4a83709301f0de446d2c85c3b91f`.
- Pair B independent review: `independent-review-files-photos/independent-review-pass.json`,
  SHA256 `d298a5f0930a5f5eb4158a522b5ce860ed548b87916ac27815c53a8166303411`.
  Reviewer `Codex /root/resume_release_audit` read all eight complete documents,
  inspected desktop/mobile renders and independently checked geometry/fonts;
  500 strict protected-field checks passed. The eight SVG accessible titles were
  corrected to the full translated article titles before approval; final author
  mapping `author-files-photos/author-receipt-final-v2.json`, SHA256
  `0ff2d004ef264ee8ae23c3611eaeec231edc08bb1e551f21c4a0ef78cbc0742b`.
- Across the two reviews, all 1,012 strict protected fields pass with zero numeric
  equivalence exceptions. Authors did not independently approve their own prose.
- Mechanical integration review: `independent-integration-review/candidate-pass.json`,
  SHA256 `552f135ba30c0737058176e3381a1d6193c065f04cee6cc27a8a95901e5d29d4`;
  candidate `integration-candidate-v1/integration-manifest.json`, SHA256
  `e369a040eb4c83f1546639a57c5463b846b5aee4dd67138f63d7e524d3019bbe`.
  It binds both independent reviews, exact sixteen document/SVG pairs, full
  normalized source preservation and eight original assets. Source paths at
  017caac57c5ced78e95a58acb03981cab9874f92 and integrated base
  819f6f33288b53be4d7ae1d7fa9d200b91e00b1a have identical source bytes.
- Applied exact twenty-file mapping: `integration-applied.json`, SHA256
  `504616fa72dd88b94e5fd4ce8cdcdc0de274971f17d59112a6dc4b3457e06b12`.

## Local validation and release boundary

Immutable command logs and final file hashes are in `test-evidence/summary-pass.json`,
SHA256 `e4fcc4dcd25215626561129be03944db50f236dfb3b82d8dbc251ea4cc519440`.
The exact integrated content hashes were checked before and after every command.
Node v24.19.0 was used for all actual JavaScript checks.

- Four scoped pack lints passed with zero errors and 32 editorial advisories
  (`no_summary` and `text_length`); original structure was retained without padding.
- `tests/test_guides_content_pack.py` and `tests/test_guides_pack_ingest.py`:
  64 passed, 5 PostgreSQL integration cases skipped (`RUN_INTEGRATION_TESTS=0`).
- Nine relevant guide/content/image/sitemap/frontend suites: 333 tests passed.
- Tool tests: 81 passed, 1 Windows/Bash temporary-directory case skipped.
- Frontend lint, i18n, typecheck, production build, task validation and diff checks
  passed. Full CI and applicable PostgreSQL release-safety evidence remain release
  gates; local skipped tests are not represented as executed.

Remaining work is tracked by the separate open task
`2026-09-23-release-localized-digital-organization-guides-batch019`.
CI, merge, canonical release freeze, deployment, import/publication and actual
public browser acceptance are not completed by this content-authoring task.

Submitted as [PR #680](https://github.com/x812033727/travel_scanner/pull/680).
Before submission, synchronized the approved documentation-only main commit
24969fe4e4705545cd3ea5e05868e1e947c00248 recording batches 007/017. The twenty
reviewed content files and eight original images remain exact hash matches;
task validation and diff checks passed again. This task is closed inside its PR
for completed content authoring and review. CI/merge and all release acceptance
remain pending in the open dependent release task.
