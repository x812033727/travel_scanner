---
id: 2026-09-20-article-localization-batch-006
title: Localize Hanoi Old Quarter guide into five languages (Batch 006 Hanoi)
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
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
  - apps/web/public/guides/hanoi-old-quarter-walking-guide
  - tasks/open/2026-09-20-article-localization-batch-006.md
---

# Localize Hanoi Old Quarter guide into five languages (Batch 006 Hanoi)

## Why

The published Hanoi Old Quarter guide has only a zh-TW document. Readers of the English, Japanese, Korean and simplified Chinese routes need complete body and diagram translations bound to the corrected published source version. The other three guides from the initial Batch 006 inventory are tracked in a separate unclaimed task.

## Definition of done

- [ ] The Hanoi pack has complete en, ja, ko and zh-CN review documents; the existing zh-TW prose and article visibility remain intact.
- [ ] Its text-bearing SVG has localized versions, preserved Mokaair attribution and checked 1600×900 renders.
- [ ] Every field, numeric claim, condition, source date, URL, link and image credit passes per-locale checks and independent editorial/visual review.
- [ ] Hash-bound, unpublished handoff lists the exact source versions and artifacts. Installation, PR, merge, deployment and publication are separate follow-up stages.

## Steps

- [x] Create an isolated worktree from current main; take a repeatable read-only production snapshot and compare each public revision with the repository pack.
- [x] Exclude Batch003/004, #593/Batch005 and other active scopes; claim the Hanoi pack and asset paths.
- [x] Prepare four explicit Hanoi locale jobs, translate all prose and SVG text, render diagrams, and validate against the original source.
- [ ] After the zh-TW sentence correction in PR #599 is merged, deployed and verified, re-snapshot Hanoi and rebind the four unsigned locale jobs to its published version/hash.
- [ ] Record independent reviewer findings and hand off the unsigned artifacts.

## How to verify

Run the article-localization pipeline against the newly pinned Hanoi live source and its explicit four-locale list; validate every materialized GuideDocument, field coverage, SVG text and render. Run `npm run check:tasks` in this worktree. No import or publication is part of this task's current authoring handoff.

## Notes

- Worktree: `C:/Users/x8120/.codex/worktrees/article-localization-batch-006/travel_scanㄐ`; base `956e32e74e6a359ae24d30e4c0719d3878612038`.
- Production read-only snapshot captured 2026-09-20T11:18:47Z, SHA-256 `95447800a4f467d42830af7d96fc4682e0a2bd99283a0b95d6fa49a9b855deeb`.
- `hanoi-old-quarter-walking-guide`: article v1, published zh-TW v6, document SHA `7414980741ec969be8132a476130d6fb725ac6e079594b4b993823235b84d3d0`.
- At the initial snapshot, repository zh-TW Hanoi document SHA matched the published revision; only zh-TW was published, the article was active, and valid_until was absent. Hero: Mokaair AI-generated illustration, explicitly not a photograph. Flow SVG: © Mokaair. Credit and license fields must be preserved/localized only where schema permits.
- External unsigned review handoff: `C:/Users/x8120/.codex/article-localization-batch-006/review-handoff.json`, SHA-256 `f1d3fc61ca4b822f358bbd90e6ab5c9f47a53f2beccdb4f300f6a98da15aa5cf`. It binds 16 jobs, 1,160 translated fields, 16 localized SVGs and 16 render previews. Validation covers schema, every field, unchanged nonlocalized scalars, image credits, hashes and automated layout. Author visually screened the diagrams; independent editorial and visual review remain pending. No product files have been installed in this worktree.
- Final read-only production resnapshot at 2026-09-20T11:36:16Z: `production-baseline-final.json` SHA-256 `51cad13d52c9a0d275d37943f258975ace1c89ee96b56810c4f083d689b9c322`. Hanoi's public zh-TW revision matched the first snapshot byte-for-byte; the four other locales remained absent.
- Release hold: Hanoi LinkBlock `/document/blocks/23/url` still targets zh-TW. The intended five-language destination paths were verified with HTTP 200 and matching `lang`/canonical in external `link-route-verification.json` SHA-256 `84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`. A separate narrow tooling change must rewrite controlled same-site URLs and rebind artifacts before review approval or publication.
- Source correction PR #599 changes only Hanoi `/blocks/11/text` to remove awkward grammar without changing the safety advice. The four translations must remain unsigned until the corrected zh-TW source is published, re-snapshotted and version-pinned. The existing Vietnam Tourism source link `https://vietnam.travel/places-to-go/northern-vietnam/ha-noi` returns HTTP 404; it is an unresolved link maintenance issue, not part of PR #599.
- On 2026-09-20 this task's scope was narrowed to Hanoi pack/art and this task file. The KL and two Singapore guides moved to a separate, unclaimed three-guide task; no product files were changed during this split.
