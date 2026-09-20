---
id: 2026-09-20-article-localization-batch-006
title: Localize four published Southeast Asia travel guides into five languages (Batch 006)
status: in-progress
priority: P2
area: api
owner: codex-batch006-author
claimed_at: 2026-09-20T11:20:54Z
created_at: 2026-09-20T11:20:50Z
completed_at:
branch: codex/article-localization-batch-006
depends_on: []
scope:
  - apps/api/app/guides/content/kuala-lumpur-airport-transfer-plan.json
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
  - apps/api/app/guides/content/singapore-hawker-first-visit.json
  - apps/api/app/guides/content/singapore-gardens-indoor-outdoor.json
  - apps/web/public/guides/kuala-lumpur-airport-transfer-plan
  - apps/web/public/guides/hanoi-old-quarter-walking-guide
  - apps/web/public/guides/singapore-hawker-first-visit
  - apps/web/public/guides/singapore-gardens-indoor-outdoor
---

# Localize four published Southeast Asia travel guides into five languages (Batch 006)

## Why

Four existing public Mokaair travel guides have only a published zh-TW document. Readers of the English, Japanese, Korean and simplified Chinese routes need complete body and diagram translations bound to the actual published source versions.

## Definition of done

- [ ] Four target packs have complete en, ja, ko and zh-CN review documents; the existing zh-TW prose and article visibility remain intact.
- [ ] Each text-bearing SVG has a localized version, preserved Mokaair attribution and a checked 1600×900 render.
- [ ] Every field, numeric claim, condition, source date, URL, link and image credit passes per-locale checks and independent editorial/visual review.
- [ ] Hash-bound, unpublished handoff lists the exact source versions and artifacts. Installation, PR, merge, deployment and publication are separate follow-up stages.

## Steps

- [x] Create an isolated worktree from current main; take a repeatable read-only production snapshot and compare each public revision with the repository pack.
- [x] Exclude Batch003/004, #593/Batch005 and other active scopes; claim these four exact pack and asset paths.
- [x] Prepare 16 explicit locale jobs, translate all prose and SVG text, render diagrams, and validate.
- [ ] Record independent reviewer findings and hand off the unsigned artifacts.

## How to verify

Run the article-localization pipeline against the pinned external Batch006 baseline and explicit four-slug list; validate every materialized GuideDocument, field coverage, SVG text and render. Run `npm run check:tasks` in this worktree. No import or publication is part of this task's current authoring handoff.

## Notes

- Worktree: `C:/Users/x8120/.codex/worktrees/article-localization-batch-006/travel_scanㄐ`; base `956e32e74e6a359ae24d30e4c0719d3878612038`.
- Production read-only snapshot captured 2026-09-20T11:18:47Z, SHA-256 `95447800a4f467d42830af7d96fc4682e0a2bd99283a0b95d6fa49a9b855deeb`.
- `kuala-lumpur-airport-transfer-plan`: article v1, published zh-TW v4, document SHA `45b44f725bd6c1c49fe4e9df48294a904f873d98ef977557652a7da105e79538`.
- `hanoi-old-quarter-walking-guide`: article v1, published zh-TW v6, document SHA `7414980741ec969be8132a476130d6fb725ac6e079594b4b993823235b84d3d0`.
- `singapore-hawker-first-visit`: article v1, published zh-TW v6, document SHA `ec29aa68e3dab66147b0964e27589889e7e1813b86a18024886eb52c33866a20`.
- `singapore-gardens-indoor-outdoor`: article v1, published zh-TW v6, document SHA `639194c34c9bec35ace1abc56b05f98b3f9eac63fa3589c6c0b8b5dca7d676f0`.
- For all four, current repository zh-TW document SHA matches the published revision; only zh-TW is published, article is active, valid_until is absent. Hero: Mokaair AI-generated illustration, explicitly not a photograph. Flow SVG: © Mokaair. Credit and license fields must be preserved/localized only where schema permits.
- Existing unrelated task references to the Singapore gardens guide are backlink notes, not active scope claims. If source or claim changes during work, stop that article and re-snapshot.
- External unsigned review handoff: `C:/Users/x8120/.codex/article-localization-batch-006/review-handoff.json`, SHA-256 `f1d3fc61ca4b822f358bbd90e6ab5c9f47a53f2beccdb4f300f6a98da15aa5cf`. It binds 16 jobs, 1,160 translated fields, 16 localized SVGs and 16 render previews. Validation covers schema, every field, unchanged nonlocalized scalars, image credits, hashes and automated layout. Author visually screened the diagrams; independent editorial and visual review remain pending. No product files have been installed in this worktree.
- Final read-only production resnapshot at 2026-09-20T11:36:16Z: `production-baseline-final.json` SHA-256 `51cad13d52c9a0d275d37943f258975ace1c89ee96b56810c4f083d689b9c322`. All four selected public articles and zh-TW published revisions match the first snapshot byte-for-byte; the four other locales remain absent.
- Release hold: the KL LinkBlock `/document/blocks/21/url` and Hanoi/Hawker LinkBlocks `/document/blocks/23/url` still target zh-TW. The intended five-language destination paths were all verified with HTTP 200 and matching `lang`/canonical in external `link-route-verification.json` SHA-256 `84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`. A separate narrow tooling change must rewrite those controlled same-site URLs and rebind the artifacts before review approval or publication.
