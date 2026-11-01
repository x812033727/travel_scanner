---
id: 2026-11-01-daily-brief-lead-picture-finds-no
title: Daily brief lead picture finds no official source: brief sources are only mokaair articles
status: done
priority: P2
area: tools
owner: claude-opus-5.5
claimed_at: 2026-11-01T03:44:58Z
created_at: 2026-11-01T03:38:30Z
completed_at: 2026-11-01T03:47:47Z
branch:
depends_on: []
scope:
  - tools/video/automation/lead-picture.mjs
  - tools/video/automation/lead-picture.test.mjs
---

# Daily brief lead picture finds no official source: brief sources are only mokaair articles

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [x] A brief whose sources are only the site's articles gets the official page's og:image in its thumbnail box.

## Steps

- [x] Follow the lead article's JSON-LD citation when no source is off-site.
- [x] Tests for both paths and the refusals; live check on 20261029 and 20261030.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Evidence (2026-11-01)

`leadSource()` takes the first non-mokaair entry of `video.sources`. daily-ai-20261029 has 6 sources and
daily-ai-20261030 has 8, all `mokaair.com/zh-TW/life/...` (20261028 still had 16 official ones). So
`findLeadPicture` throws "the script names no official source" and #1961's picture never appears on a
current brief. The official page is one hop away: the lead article links
`https://deploymentsafety.openai.com/gpt-6-luna-october-28-2026-addendum` (og:image worked when fetched by hand).
Fix: when every source is ours, follow the first source's article to its first external citation.

## Done (2026-11-01)

- `findLeadPicture` falls back to the lead article: when no source is off-site, it reads the first
  mokaair source's page and takes the first off-site https `citation` in its JSON-LD
  (`apps/web/lib/structured-data.ts` writes one CreativeWork per source). `leadArticle`,
  `articleCitation` exported; `lead-picture.test.mjs` covers both paths, the refusals, and pins that the
  page still writes `citation:`.
- Live check on the host (worker container, scratch copy): daily-ai-20261029 → deploymentsafety.openai.com
  og:image; daily-ai-20261030 → blog.cloudflare.com og:image. Both failed before.
- Not changed: `leadPicture` still skips videos already on YouTube (the thumbnail is in the visual hash).
