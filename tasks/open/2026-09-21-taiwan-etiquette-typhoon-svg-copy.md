---
id: 2026-09-21-taiwan-etiquette-typhoon-svg-copy
title: Correct typhoon closure text in Taiwan etiquette diagram
status: review
priority: P2
area: web
owner: codex-batch007-svg-hotfix
claimed_at: 2026-09-21T20:40:27Z
created_at: 2026-09-21T20:40:11Z
completed_at:
branch: codex/taiwan-etiquette-svg-typo
depends_on: []
scope:
  - apps/web/public/guides/taiwan-etiquette-safety-tips/diagram-1-zh-tw.svg
  - tasks/open/2026-09-21-taiwan-etiquette-typhoon-svg-copy.md
---

# Correct typhoon closure text in Taiwan etiquette diagram

## Why

The published zh-TW Taiwan etiquette diagram says「颱風停班課」, omitting
「停」from「停課」. The article prose is already correct.

## Definition of done

- [x] The zh-TW SVG reads「颱風停班停課由各縣市政府決定」with all other content unchanged.
- [x] Desktop and actual 390px scroller renders show legible, unclipped text.

## Steps

- [x] Correct the single SVG text node.
- [x] Render and review desktop/mobile sizes; open a scoped PR.

## How to verify

Compare the one-line Git diff, run `npm run check:tasks`, and inspect
1600×900 and 390px-wide browser renders.

## Notes

Base commit: `51e716da6c789e7eeba4c36ad1780095e89b4e48`.
The SVG diff changes exactly one text node. Chrome rendered it at 1600×900
and inside a 390px-wide horizontal scroller, checked at left and right scroll
positions. Evidence: `C:\Users\x8120\.codex\article-localization-release\taiwan-batch007-svg-hotfix-qa`.
