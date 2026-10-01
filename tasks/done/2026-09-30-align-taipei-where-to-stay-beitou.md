---
id: 2026-09-30-align-taipei-where-to-stay-beitou
title: Align taipei-where-to-stay Beitou to Songshan Airport time and transfers with zh-TW
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T10:23:01Z
created_at: 2026-09-30T10:13:40Z
completed_at: 2026-09-30T10:23:16Z
branch: claude/taipei-beitou-songshan
depends_on:
  - 2026-09-30-bring-taipei-where-to-stay-translations
scope:
  - apps/api/app/guides/content/taipei-where-to-stay.json
  - apps/web/public/guides/taipei-where-to-stay/diagram-1.svg
---

# Align taipei-where-to-stay Beitou to Songshan Airport time and transfers with zh-TW

## Why

Found while aligning the airport-bus text (`2026-09-30-bring-taipei-where-to-stay-translations`).
zh-TW now gives Beitou/Xinbeitou to Songshan Airport as about 41 to 43 minutes with two
transfers. The shared `diagram-1.svg` (en/ja/ko/zh-CN) still draws 松山機場 41 分 and
（轉乘 3 次）, and the translations say 41 minutes. zh-TW's own diagram has the new wording.

## Definition of done

- [x] en, ja, ko and zh-CN text and the shared diagram say what zh-TW says (time range and
      number of transfers), with nothing else changed.
- [x] Every number on the diagram appears in each locale's text; lint 0 errors; rendered check.
- [ ] After deploy, dry-run shows `update` for the four locales, then `--publish`.

## How to verify

Compare the zh-TW Beitou block and `diagram-1-zh-tw.svg` with each locale and `diagram-1.svg`.

## Notes

- 2026-09-30 (claude-opus-5-5): en/ja/ko/zh-CN tables and Beitou paragraphs now say
  about 41 to 43 minutes, NT$40, two transfers (at Beitou and Da'an), as zh-TW block 19
  and its own diagram do; the shared diagram draws 41–43 分・（轉乘 2 次）, and its
  `<desc>` plus the four image descriptions say the same. No other number changed.
  Rendered and checked; lint 0 errors; content pack tests green. (zh-TW's own table
  still says 約 41 分鐘; zh-TW was not in scope.) Left: import after merge and deploy.
