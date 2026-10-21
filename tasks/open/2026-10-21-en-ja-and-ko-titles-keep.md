---
id: 2026-10-21-en-ja-and-ko-titles-keep
title: en, ja and ko titles keep a combined dub and captions segment instead of a second tag
status: in-progress
priority: P2
area: api
owner: claude-opus-5.5-caption-tail
claimed_at: 2026-10-21T11:03:44Z
created_at: 2026-10-21T07:10:00Z
completed_at:
branch: claude/caption-tag-combined-tail
depends_on: []
scope:
  - apps/api/app/video_youtube/requests.py
  - apps/api/tests/test_video_languages_imported.py
  - apps/api/tests/test_video_youtube_story_title.py
---

# en, ja and ko titles keep a combined dub and captions segment instead of a second tag

## Why

The site puts each language's captions tag on a title on its way to YouTube
(`requests.captioned`). A title whose last segment already says dub and captions together keeps
its words only in es, pt, id, vi and th; en, ja and ko get a second tag after it. The 種田娶妻打天下
1–5 compilation's titles would go out as 「Farm, Marry, Conquer Ep. 1–5 | Dub + CC｜CC Subtitles」,
「…第1–5話 | 吹替＋CC字幕｜字幕付き」 and 「…제1–5화 | 더빙 + CC 자막｜CC 자막」 (found while checking
the compilation's upload package, PR #1648; the owner asked on 2026-10-21 to fix and deploy it).
The Japanese one also joins with a full-width 「＋」, which the combined pattern does not read.

## Checklist

- [x] `captioned` keeps a combined segment in every language, and reads 「＋」 as well as 「+」.
- [x] Tests: en, ja and ko combined titles unchanged; plain titles tagged as before; a brand
      story's tag goes before the combined segment in en too.
- [ ] ruff, mypy, pytest; PR; deploy; read the compilation's titles back through the code on the host.

## Notes

Claimed with --force: 2026-10-19-worker-video-languages-five (status review, code merged in #1611/#1614, only pilots left) and 2026-10-19-imported-video-languages-eight (done, closed in PR #1648) cover apps/api/app/video_youtube as a directory; neither changes requests.py any more.
