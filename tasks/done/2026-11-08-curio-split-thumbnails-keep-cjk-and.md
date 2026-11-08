---
id: 2026-11-08-curio-split-thumbnails-keep-cjk-and
title: Curio split thumbnails keep CJK and Thai lines whole
status: done
priority: P1
area: tools
owner: claude-opus-5-5-curio-redo-20
claimed_at: 2026-11-08T04:09:30Z
created_at: 2026-11-08T04:09:17Z
completed_at: 2026-11-08T04:09:30Z
branch: claude/curio-redo-20-episodes-ldnrq0
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
---

# Curio split thumbnails keep CJK and Thai lines whole

## Why

Rendering the new split thumbnails (layout e) for S06, S09, S17 and W03 in nine languages, the
browser cut Japanese headlines mid-word (「もう死んで／た？」「殺してしま／え？」) and a Thai sub line
mid-word (「โนบุนา／งะ」): scripts without word spaces wrap anywhere.

## Definition of done

- [x] In layout e, a headline in Chinese, kana or Hangul keeps the lines the writer broke with
      "\n" and shrinks (fitText) instead of wrapping; a Thai sub line does the same.
- [x] Latin headlines still wrap between words; no other layout changes.

## How to verify

`node --test tools/video/templates/templates.test.mjs`; the 36 thumbnails rendered for the four
episodes show no mid-word breaks, and render reports no fit problems.

## Notes

- Two Japanese headlines were then too wide for one line even at 60%; their line was broken at a
  pause in the thumbnail input (「もう／死んでた？」「殺して／しまえ？」), the words unchanged.
