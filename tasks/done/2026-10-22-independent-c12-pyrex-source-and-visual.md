---
id: 2026-10-22-independent-c12-pyrex-source-and-visual
title: Independent C12 Pyrex source and visual delta v2 review
status: done
priority: P1
area: docs
owner: codex-c12-source-delta
claimed_at: 2026-10-22T15:59:05Z
created_at: 2026-10-22T15:56:21Z
completed_at: 2026-10-22T16:07:22Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v2.md
---

# Independent C12 Pyrex source and visual delta v2 review

## Why

The C12 Pyrex author revised 34 narration rows and eight visual rows after blind read A. A new independent source and image chronology review must bind to the new file hashes before the script moves to another gate.

## Definition of done

- [x] Record a hash-bound verdict for each changed narration and visual ID against reopened primary sources.
- [x] Identify any new cross-row chronology or product-material contradiction.

## Steps

- [x] Confirm the exact script and visual hashes and compare all 80 row IDs against the previous reviewed version.
- [x] Reopen the cited museum, manufacturer, and product sources.
- [x] Save the independent receipt and run targeted repository checks.

## How to verify

`Get-FileHash` on both inputs; a row-ID diff against Git head `6a5bdcc569905f41b7bbb15db7a338fa703c2c55`; `npm run check:tasks`; `npm run test:docs-videos`.

## Notes

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v2.md`. The 34 changed narration IDs PASS; seven changed visual IDs PASS; visual O09 is HOLD because it places a complete battery jar in a family kitchen before Jesse brings cut jar bottoms home in I02. The original museum Pyrex FAQ was inaccessible directly, so its search-index text was cross-checked against live museum research and collection pages. Both input hashes matched the author receipt; 80 IDs in each file were unique, same order, and the exact changed-ID sets matched. `git diff --check` passed. `npm run check:tasks` exited 1 only for two existing duplicate open/done ghost task IDs (blind-narration-review-a-for-c12 and independently-audit-c12-pyrex-script-and); they were preserved. `npm run test:docs-videos` showed ten passing unrelated tests before it was stopped at the parent agent's direction; no full-suite result is claimed. The O09 repair is handed to the active author/parent work rather than filed as a competing task.
