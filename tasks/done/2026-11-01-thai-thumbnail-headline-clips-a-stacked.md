---
id: 2026-11-01-thai-thumbnail-headline-clips-a-stacked
title: Thai thumbnail headline clips a stacked vowel+tone mark (e.g. สั้น)
status: done
priority: P2
area: tools
owner: claude-opus-5.5
claimed_at: 2026-11-01T03:45:15Z
created_at: 2026-11-01T03:38:31Z
completed_at: 2026-11-01T03:47:49Z
branch:
depends_on: []
scope:
  - tools/video/templates/theme.css
---

# Thai thumbnail headline clips a stacked vowel+tone mark (e.g. สั้น)

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [x] A Thai thumbnail headline shows stacked vowel and tone marks whole.

## Steps

- [x] Room above the line box for :lang(th) headline and sub.
- [x] Redraw daily-ai-20261029's th thumbnail with the original wording and look at it.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Evidence (2026-11-01)

daily-ai-20261029 th headline "สั้นลง": ั + ้ stack above ส and the tone mark is cut to a flat bar at the top
of the line box. Still clipped after #1961's fitText change (redrawn with current code). Worked around for
this video by rewording to "กระชับ" (no stacked marks). Needs line-height / padding-top for :lang(th)
headlines, and a QA check for ink above the line box.

## Done (2026-11-01)

Cause: `.fit { overflow: hidden }` on the headline, with Thai above-base marks taller than a 1.1 line box.
`.thumb h1:lang(th)` gets `padding-top: 0.22em; line-height: 1.3`, `.sub:lang(th)` `padding-top: 0.15em`.
Redrawn on the host with the original "สั้นลง\nแต่**ผิด**": the tone mark is whole. theme.css only feeds
the frame cache key (theme_hash is not compared for staleness), so approved cuts are untouched.
Left: a QA check for ink above the line box (qa/thumbnail.mjs) — not in this scope.
