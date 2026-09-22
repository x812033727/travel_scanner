---
id: 2026-09-21-taiwan-etiquette-typhoon-svg-copy
title: Correct typhoon closure text in Taiwan etiquette diagram
status: done
priority: P2
area: web
owner: codex-batch007-svg-hotfix
claimed_at: 2026-09-21T20:40:27Z
created_at: 2026-09-21T20:40:11Z
completed_at: 2026-09-21T21:35:35Z
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

PR #630 merged at `d8621daf47b7acd8fec617b735d76d9e79931268` with all eight PR checks and all four main CI jobs successful. Production activation used a verified `pg_dump -Fc` backup (SHA-256 `0528bcfdecd077bb3540b39b16693a6e6921fff047842b945177e40d352c433b`), followed by 20/20 signed-out desktop/mobile page checks and 22 visual screenshots. The public, internal, container and source SVG all match SHA-256 `48df75dc46eadfe0fbbf379ce5599847a7392542f2d529e8e19c4788e986c3af`; no article content was rewritten. The hold was cleared only after verification; host checkout is clean and ready. The production receipt archive SHA-256 is `7754785887fd77a4d05544132931a36b304069f2a2cf7a1ec50de554364e2cc7` at `C:\Users\x8120\.codex\article-localization-release\taiwan-etiquette-hotfix\hotfix-final-receipts.tar.gz`.
