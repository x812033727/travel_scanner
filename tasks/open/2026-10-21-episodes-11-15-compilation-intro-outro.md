---
id: 2026-10-21-episodes-11-15-compilation-intro-outro
title: 種田娶妻打天下 episodes 11-15 compilation: intro, outro, eight languages, imported
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-11-15
claimed_at: 2026-10-21T15:50:42Z
created_at: 2026-10-21T15:50:38Z
completed_at:
branch: claude/zhong-tian-qu-qi-e011-015
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales
---

# 種田娶妻打天下 episodes 11-15 compilation: intro, outro, eight languages, imported

## Why

The owner asked on 2026-10-21 「接著製作11-15」 after the 6-10 compilation: the same video for
episodes 11-15, wrapped in the channel intro and end-screen outro, with the eight dub tracks and
CC files on its own timeline and links in every description, imported to /admin/videos.

## Checklist

- [x] `compilation["11-15"]` in all eight youtube-locales files, on the 1-5 pattern.
- [ ] Build: `DUBS=en,ja,ko,es,pt,id,vi,th node compile-dh.mjs 11 15 e011-015.mp4`.
- [ ] Check the cut, the nine CC files, the eight tracks' length, the links.
- [ ] `prep-import.mjs 11-15` and `import`; `--languages` once the owner ticks the panel; `--publish` once the cut is approved.

## Notes

Stacked on claude/zhong-tian-qu-qi-e006-010 (PR #1653), which adds the 6-10 entries to the same files.
