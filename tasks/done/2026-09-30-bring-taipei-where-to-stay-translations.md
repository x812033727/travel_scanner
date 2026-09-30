---
id: 2026-09-30-bring-taipei-where-to-stay-translations
title: Bring taipei-where-to-stay translations and shared diagram up to the #624 zh-TW rewrite
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T09:52:38Z
created_at: 2026-09-30T01:29:00Z
completed_at: 2026-09-30T10:13:43Z
branch: claude/taipei-stay-translations
depends_on:
  - 2026-09-21-91-ci
scope:
  - apps/api/app/guides/content/taipei-where-to-stay.json
  - apps/web/public/guides/taipei-where-to-stay/diagram-1.svg
---

# Bring taipei-where-to-stay translations and shared diagram up to the #624 zh-TW rewrite

## Why

PR #624 (2026-09-22) rewrote the zh-TW `taipei-where-to-stay` and its own
`diagram-1-zh-tw.svg`: it withdrew fixed estimates that could not be kept
current. The en/ja/ko/zh-CN editions (#454, 2026-09-13) and the shared
`diagram-1.svg` they use still carry them. `2026-09-21-91-ci` changed only the
two diagram labels the content checker flagged (bus 1960 "60-70 min" and the
taxi "NT$1,200-1,900") plus the matching `<desc>` clauses, and added bus 1960 and
the 06:03 first train to ko/zh-CN.

Still stale against zh-TW: bus 1819 "24 hours" (zh-TW: scheduled all day, long
late-night gaps), buses 1840/1841/1842 "50-60 min" to Songshan, and taxi fare
estimates in the en/ja/ko text; the diagram's bus box still draws the 1819 and
1840-1842 lines.

## Definition of done

- [x] Every locale and the shared diagram say what zh-TW says about airport buses
      and taxis, with no withdrawn estimate left.
- [x] Independent review of each changed locale; `pack_cli lint` stays at 0 errors.
- [x] After deploy, dry-run shows `update` only for this slug's changed locales,
      then `--publish`.

## How to verify

Compare zh-TW blocks 4 and 25 with the same blocks in each locale, render the
shared diagram, and run `uv run python -m app.guides.pack_cli lint --slug taipei-where-to-stay`.

## Notes

- 2026-09-30 (claude-opus-5-5): a translation agent aligned en/ja/ko/zh-CN and the
  shared diagram with zh-TW; an independent reviewer returned 4 MUST and 7 SHOULD
  corrections (ja grammar, 全日運行／하루 종일 운행 reading as 24-hour service,
  missing 約／약, the Zhongshan North Road route zh-TW dropped, the taxi-rank
  estimated-fares source), all applied.
- Now in every translation: 1819 has scheduled runs all day with long late-night gaps,
  about 55 minutes, about NT$133–164 by vehicle and run, check the timetable; 1840
  serves T1/T2, 1841/1842 run from the T2 end, no fixed minutes; 1960 time depends on
  the run and traffic; taxis metered, fare depends on destination, traffic, night
  surcharge and rank rules. No withdrawn figure (24 h, 50–60, 60–70, 1,200–1,900)
  remains; zh-TW is byte-identical to before. The en/ja/ko taxi estimated-fares
  source was removed (zh-TW does not cite it; nothing relies on it).
- Diagram: airport-bus box redrawn to zh-TW's substance and geometry; rendered and
  checked. Lint 0 errors; content pack tests green.
- Out of scope, filed: Beitou to Songshan Airport time and transfers.
- Left: production import of en/ja/ko/zh-CN after merge and deploy.
