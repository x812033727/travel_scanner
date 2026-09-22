---
id: 2026-09-21-taiwan-zh-tw-third-sub-batch
title: Taiwan zh-TW third sub-batch: Kaohsiung and Tainan itineraries
status: review
priority: P2
area: docs
owner: codex-taiwan-zh-tw-batch003
claimed_at: 2026-09-21T14:26:02Z
created_at: 2026-09-21T14:26:00Z
completed_at:
branch: codex/taiwan-zh-tw-batch-003
depends_on: []
scope:
  - apps/api/app/guides/content/kaohsiung-3-day-itinerary.json
  - apps/api/app/guides/content/tainan-2-day-itinerary.json
  - apps/web/public/guides/kaohsiung-3-day-itinerary/diagram-1-zh-tw.svg
  - apps/web/public/guides/tainan-2-day-itinerary/diagram-1-zh-tw.svg
---

# Taiwan zh-TW third sub-batch: Kaohsiung and Tainan itineraries

## Why

The published Kaohsiung three-day and Tainan two-day itineraries had English,
Japanese, Korean and Simplified Chinese revisions, but no Traditional Chinese
revision. They are the next conflict-free Taiwan pair after the Jiufen/night-market
and Taipei Metro/Taoyuan Airport batches. This batch adds complete `zh-TW`
documents and localized text diagrams without importing, publishing or otherwise
writing to production.

## Definition of done

- [x] Both packs contain a complete, schema-valid `zh-TW` `GuideDocument` with the
      same block and source counts as the fresh published `zh-CN` source revision.
- [x] Titles, descriptions, body copy, tables, callouts, links, image text,
      captions, alternative text and source titles are Traditional Chinese; internal
      article links use `/zh-TW/`.
- [x] Current transport, admission, payment, driving and entry conditions are
      checked against primary official sources, with eligibility stated by document
      or status rather than inferred from reading language.
- [x] Each article uses its own `diagram-1-zh-tw.svg`, with no clipping, overlap,
      replacement glyphs or unsupported number visible at desktop and 390 px.
- [x] Focused content-pack, link, tooling and task checks pass; inherited lint
      errors from the existing shared diagrams are recorded separately.
- [x] The final content, diagrams and evidence have independent review with no
      blockers.
- [x] An unmerged pull request carries the reviewed commit.

## Steps

- [x] Capture the two published source revisions in one read-only repeatable-read
      transaction and bind article, locale and content hashes.
- [x] Translate and edit Kaohsiung, including the 85% electronic-ticket fare,
      payment modes, TWAC eligibility and museum closure exceptions.
- [x] Translate and edit Tainan, correcting Shalun Line times, route 98 service,
      historic-site concessions, THSR payment and reciprocal international-licence
      rules.
- [x] Create and render the two Traditional Chinese SVG variants.
- [x] Validate field parity, schema, SVG numbers, focused tests and the task board.
- [x] Rebase onto current `origin/main` with unchanged content hashes and obtain
      final independent review.
- [x] Push and open the pull request.

## How to verify

- `uv run python <evidence>/validate_targets.py`
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guides_pack_ingest.py -q`
- `npm run test:tools`
- `npm run check:tasks`
- `git diff --check`
- `node <evidence>/render_svgs.cjs`
- `uv run python -m app.guides.pack_cli lint --slug <slug>` (the new `zh-TW`
  documents have no errors; see Notes for inherited findings)

## Notes

- Production source evidence is
  `C:\Users\x8120\.codex\article-localization-release\taiwan-zh-tw-batch003\live-source.json`,
  captured at `2026-09-21T14:27:13.272677+00:00` in one `REPEATABLE READ, READ
  ONLY` transaction. Its SHA-256 is
  `45da9c92e16d50f41821d18a1cfe2b1e815c42cd568a18b656fd51ff72fee9bd`.
- Kaohsiung source: article version 2, `zh-CN` locale/published version 6,
  published document SHA-256
  `78c91c7201e87ec499e25d5fcd094d105c214caa1e1af80fe516224ba55fdecd`.
  Tainan source: article version 2, `zh-CN` locale/published version 4, SHA-256
  `757a7352a4afb9686be374c7ac695eb55395c33eedf7cb3378bcf46bd11aa44b`.
- Current target document hashes are recorded by `translation-audit.json`:
  Kaohsiung
  `313d1d96d5d867e05358308d0f52466deceb8fbff34ee3f6f955a3df54c85c96`;
  Tainan `199c909df9bc633450e643dbb2115f65dd157ce2bd05ac18a7e906190cba8fe9`.
- The branch was rebased from `991e1795db7c91a1c283727947e0cfa31b067b42`
  to `bb53e361bb6c1ac35a00ac0f65e49c0b304ac034` after Batch 002 merged. After
  final review corrections, a fresh fetch and rebase check still resolved to
  `bb53e361`; `post-rebase-hashes.json` proves the two packs are canonically
  identical and the two SVGs text-identical across that final check.
- Primary-source corrections include: Shalun to Tainan about 20-25 minutes,
  06:25-23:39; route 98's Qigu last return at 17:30 and 18:30 short working from
  Anping; explicit historic-site concession eligibility; reciprocal international
  driving permit rules; THSR's restricted co-branded EasyCard use; Kaohsiung
  Metro/LRT electronic fares at 85% of published fare; TWAC eligibility by document
  status; and mode-specific Kaohsiung payments.
- SVG render report and four PNGs are in the external evidence `renders/` folder.
  Desktop and 390 px each report zero outside nodes, overlaps and missing glyphs
  (65 visible text nodes for Kaohsiung and 75 for Tainan).
- Focused API tests pass `43 passed, 5 skipped`; repository tool tests pass
  `75 passed, 1 skipped`; `npm run check:tasks`, target validation and
  `git diff --check` pass.
- Independent final review approved the source facts, locale-only pack changes,
  SVG render evidence and rebase hashes with no blockers.
- Pull request: https://github.com/x812033727/travel_scanner/pull/622 (unmerged).
- At baseline `origin/main` `bb53e361bb6c1ac35a00ac0f65e49c0b304ac034`, the full
  pack lint already reports Kaohsiung shared-diagram number errors in `en`, `ja`,
  `ko`, `zh-CN`, and a Tainan shared-diagram error in `ja`. The added `zh-TW`
  diagrams report no missing numbers. `baseline-diagram-audit.json` records the
  exact inherited findings.
- No production import, publication, deployment, merge or write was performed.
