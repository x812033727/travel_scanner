---
id: 2026-10-20-brand-story-titles-say-so-in
title: Brand story titles say so in every language
status: done
priority: P2
area: tools
owner: claude-opus-5-5-story-title-tag
claimed_at: 2026-10-20T10:25:54Z
created_at: 2026-10-20T10:25:51Z
completed_at: 2026-10-20T10:26:47Z
branch:
depends_on: []
scope:
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/package/metadata.mjs
---

# Brand story titles say so in every language

## Why

The owner asked on 2026-10-20 that every brand story's YouTube title end with 「| 品牌故事」,
worded per language, for these six adapted stories and every brand story after them.

## Definition of done

- [x] A video with `category: "story"` gets its locale's story tag before the captions tag in the
      packaged title and every localization (「…？｜品牌故事｜CC字幕」, 「…｜Brand Story｜CC Subtitles」).
- [x] The tag is added once, replaces another language's, and is left off when even the short
      captions tag would no longer fit in 100 characters.
- [x] Other videos' titles do not change.

## How to verify

```bash
node --test tools/video/core/metadata.test.mjs tools/video/package/metadata.test.mjs
```

## Notes

- The bar is the channel's full-width 「｜」, as the captions tag already uses.
- The site's `captioned()` (apps/api/app/video_youtube/requests.py) strips and re-adds only the
  captions tag, so the story tag before it survives the way out unchanged.
- Videos already packaged take the tag when they are packaged again.
