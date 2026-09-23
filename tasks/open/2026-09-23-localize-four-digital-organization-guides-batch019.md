---
id: 2026-09-23-localize-four-digital-organization-guides-batch019
title: Localize four digital organization guides batch019
status: in-progress
priority: P1
area: api
owner: codex-batch019
claimed_at: 2026-09-23T08:13:05Z
created_at: 2026-09-23T08:12:54Z
completed_at:
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

- [ ] Sixteen complete language documents include every block, title, description,
      caption, alt text, source title and visible AI/provenance disclosure.
- [ ] Sixteen localized SVG diagrams match the source semantics and pass desktop
      and mobile render review; textless original hero JPGs are preserved.
- [ ] Independent content/image review binds the source and final artifact hashes.
- [ ] Scoped pack/API/frontend/tool checks pass and the batch is submitted in a PR.
- [ ] A separate release task records CI, merge, guarded import/publication and
      real public browser acceptance before claiming the languages are live.

## Steps

- [x] Inventory current repository, shared tasks, active branches and live source.
- [x] Claim exact four-article scope and split authorship into disjoint pairs.
- [ ] Review outside-only translation/image candidates before root integration.
- [ ] Preserve source models/assets and validate the exact integrated Git bytes.
- [ ] Open the scoped PR and explicit remaining release task.

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
