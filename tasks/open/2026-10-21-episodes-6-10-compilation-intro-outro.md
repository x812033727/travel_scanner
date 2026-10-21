---
id: 2026-10-21-episodes-6-10-compilation-intro-outro
title: 種田娶妻打天下 episodes 6-10 compilation: intro, outro, eight languages, imported
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-6-10
claimed_at: 2026-10-21T14:10:56Z
created_at: 2026-10-21T14:09:05Z
completed_at:
branch: claude/zhong-tian-qu-qi-e006-010
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales
---

# 種田娶妻打天下 episodes 6-10 compilation: intro, outro, eight languages, imported

## Why

The owner asked on 2026-10-21 for 「製作6-10」 after the 1-5 compilation went up the same way: one
YouTube video of episodes 6-10 wrapped in the channel intro and end-screen outro, with the eight
dub tracks and CC files merged on its own timeline, links in every description, imported to
/admin/videos with its languages batch. `compile-dh.mjs` builds it; what was missing is each
language's title and description for the 6-10 range in `youtube-locales/<locale>.json`.

## Checklist

- [x] `compilation["6-10"]` in all eight youtube-locales files, on the 1-5 pattern.
- [x] Build: `DUBS=en,ja,ko,es,pt,id,vi,th node compile-dh.mjs 6 10 e006-010.mp4`.
- [x] Check the cut, the nine CC files, the eight tracks' length, the links.
- [ ] `prep-import.mjs 6-10`, `import`, `import --languages`; after the owner approves the cut, `import --publish`.

## Notes

Claimed with --force over 2026-10-19-30-1-24: the same series line, whose only open item is the owner re-reviewing episodes 1-24; it does not touch youtube-locales.
