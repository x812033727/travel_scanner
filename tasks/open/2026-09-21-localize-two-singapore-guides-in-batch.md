---
id: 2026-09-21-localize-two-singapore-guides-in-batch
title: Localize two Singapore guides in batch 010
status: in-progress
priority: P1
area: docs
owner: codex-batch010-singapore
claimed_at: 2026-09-21T21:43:40Z
created_at: 2026-09-21T21:43:34Z
completed_at:
branch: codex/article-localization-batch-010-singapore-candidate
depends_on: []
scope:
  - apps/api/app/guides/content/singapore-4-day-itinerary.json
  - apps/api/app/guides/content/singapore-changi-airport-mrt-simplygo-guide.json
  - apps/web/public/guides/singapore-4-day-itinerary
  - apps/web/public/guides/singapore-changi-airport-mrt-simplygo-guide
---

# Localize two Singapore guides in batch 010

## Why

The published `singapore-4-day-itinerary` and
`singapore-changi-airport-mrt-simplygo-guide` each had only zh-TW. Their diagrams
also contain Chinese labels. Batch 010 adds the missing zh-CN, en, ja and ko
documents and localized diagrams without changing the visibility of either
article. The itinerary pack summary lagged behind the published zh-TW revision;
the published GuideDocument is the source of truth.

## Definition of done

- [x] Both packs contain complete zh-TW, zh-CN, en, ja and ko documents; the
      zh-TW documents match the published revisions byte-for-byte after
      canonical normalization.
- [x] Each new locale has a language-specific diagram. Existing photographs,
      author credits, licences and source URLs remain intact.
- [x] Local pack lint and focused content/asset checks pass, and all eight
      diagrams are rendered at desktop and 390px mobile width without label
      overflow or overlap.
- [ ] Independent editorial review accepts wording, eligibility, source facts
      and image legibility.
- [ ] Rebase on fresh main, recheck production version/visibility, then open
      and complete the bounded PR. Publication is handled by the release task.

## Steps

- [x] Pin published zh-TW v8/v6 and compare with the repository packs.
- [x] Translate all fields and source titles; localize explicit site URLs and
      preserve article references, whose renderer links only published locales.
- [x] Localize SVG labels and long descriptions; render/check desktop and mobile.
- [x] Capture source, pack, locale and asset hashes in external QA receipts.
- [ ] Have another reviewer inspect all eight documents and diagrams.

## How to verify

From this worktree, with the existing API virtual environment:

```powershell
cd apps/api
& 'C:\Users\x8120\.codex\worktrees\c5d9\travel_scanㄐ\apps\api\.venv\Scripts\python.exe' -m app.guides.pack_cli lint --slug singapore-4-day-itinerary
& 'C:\Users\x8120\.codex\worktrees\c5d9\travel_scanㄐ\apps\api\.venv\Scripts\python.exe' -m app.guides.pack_cli lint --slug singapore-changi-airport-mrt-simplygo-guide
cd ../..
npm run check:tasks
git diff --check
```

The external review bundle is
`C:\Users\x8120\.codex\article-localization-release\batch010-work\qa`.
Its `content-audit.json` validates structure, provenance, source dates and
URLs, source hashes, locale links, SVG references and critical numeric values.
`metrics.json` and 32 screenshots cover the eight diagrams at desktop and
three 390px scroll positions; text bounds and pairwise overlap are zero.

## Notes

- Read-only production snapshot:
  `C:\Users\x8120\.codex\article-localization-release\batch010-inventory\production-source.json`;
  inventory SHA-256
  `259cd6fea752edf87360f8986b06d6fa284da97d815965627854bbc3537e1f29`.
- Published source revisions: itinerary zh-TW v8
  `2ef11f1818758f946708a5d9fb18ee9dd0d74be8569aadac08ad8aa38fdd0af3`;
  Changi zh-TW v6
  `4b147220af61ad0b8b0d17d46883b50a1f2bdb58c28338e2b6372589c2a93805`.
- The itinerary's repository description was older than published; this
  candidate copies the published document into zh-TW before adding locales.
- Official source spot-checks: Changi train/taxi page, SimplyGo contactless
  card FAQ and adult fares, Gardens by the Bay Flower Dome, and ICA SG Arrival
  Card. Preserve the original checked-on dates in source records.
- Only `singapore-hawker-first-visit` and
  `singapore-gardens-indoor-outdoor` were published in all five locales at
  inventory time. The renderer turns absent-locale `article` references into
  plain text until their destinations are published. Explicit city and food
  directory URLs use each actual locale route.
- Both `pack_cli lint --slug` commands pass. They warn that the published
  source had no summary block and the full English translations exceed the
  advisory 6,000-character howto length; neither is a validation error.
- `pytest tests/test_guides_content_pack.py -q` is not a clean scoped check in
  this sparse worktree: SQLite import tests fail because the fixture lacks
  `guide_article_aliases`, and catalogue-wide image checks fail because the
  sparse worktree intentionally omits other articles' artwork. These failures
  are not reported as passes. Re-run full CI after the final rebase/PR.
- Candidate v2 corrects the English itinerary block 27 temporal cues: source
  `下午` is now "In the afternoon" and `傍晚` is "At dusk". The original
  candidate commit, manifest and review receipt remain as historical evidence;
  v2 needs its own independent editorial review. The earlier 4px mobile-image
  blocker used the older c5d9 ContentBlocks; re-evaluate it against the
  deployed d862 code with 1180px SVG horizontal scrolling.
- Base checkout is `d8621daf47b7acd8fec617b735d76d9e79931268`; main has
  advanced. Recheck fresh origin/main and live versions/visibility before a PR
  or any production publication. No PR or production write from this task yet.
