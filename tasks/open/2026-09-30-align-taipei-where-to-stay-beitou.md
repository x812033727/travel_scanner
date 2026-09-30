---
id: 2026-09-30-align-taipei-where-to-stay-beitou
title: Align taipei-where-to-stay Beitou to Songshan Airport time and transfers with zh-TW
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-30T10:13:40Z
completed_at:
branch:
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

- [ ] en, ja, ko and zh-CN text and the shared diagram say what zh-TW says (time range and
      number of transfers), with nothing else changed.
- [ ] Every number on the diagram appears in each locale's text; lint 0 errors; rendered check.
- [ ] After deploy, dry-run shows `update` for the four locales, then `--publish`.

## How to verify

Compare the zh-TW Beitou block and `diagram-1-zh-tw.svg` with each locale and `diagram-1.svg`.
