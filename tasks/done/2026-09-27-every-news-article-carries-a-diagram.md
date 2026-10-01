---
id: 2026-09-27-every-news-article-carries-a-diagram
title: Every news article carries a diagram that names Jev and uses the title as its alt text
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-30T11:09:03Z
created_at: 2026-09-27T09:42:32Z
completed_at: 2026-09-30T11:10:28Z
branch: claude/news-drop-process-diagram
depends_on: []
scope:
  - apps/api/app/news_automation/assets.py
  - apps/api/tests/test_news_assets_storage.py
---

# Every news article carries a diagram that names Jev and uses the title as its alt text

## Why

`assets.py` inserts the same figure into every automated news article, in every locale. Its
caption is 「Mokaair 編輯查核流程」 and its description is
「消息會先蒐集來源、獨立查核，再交由 Jev 判斷。」 (`DIAGRAM_COPY`), and its `alt` is
`document.title`. Readers do not know who or what "Jev" is. The alt text describes the
article rather than the image. The figure sits under whatever heading happens to precede it,
for example the AEMA principles or a public-sector section. All four reviewers of the
2026-09-27 held drafts raised it independently. Every published automated news article has
it too.

## Definition of done

- [x] The figure either no longer names an internal tool (it describes the process in words a
      reader understands) or is dropped from news articles.
- [x] Its `alt` describes the image.
- [x] Already published articles are corrected, or a follow-up ticket records how.

## Steps

- [x] Decide with the owner: keep a process figure (reworded) or drop it.
- [x] Change `DIAGRAM_COPY` and the `alt` for all five locales, with tests.
- [x] Plan the correction of published articles. Their revisions are versioned, so it is a
      republish, not an edit in place.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_assets_storage.py -q
```

## Notes

- The figures are served from `/guides/news-assets/`, which answered 500 until PR #851.
- 2026-09-30 (claude-opus-5-5): the owner chose to drop the figure. `ensure_assets` no
  longer draws or inserts it (`DIAGRAM_COPY` and `render_diagram` are removed), still strips
  any old news-asset image block from a candidate processed again, and marks that
  candidate's old diagram assets deleted and not public. The "alt describes the image" item
  is moot with no figure. Tests: storage tests now expect hero + social only (2 assets) and
  serve the hero; a new test drops an old figure from the text and its public asset. News
  suites (assets, automation, pipeline): 144 passed; ruff and mypy clean.
- Published articles: 69 carry it (read-only count 2026-09-30); the republish is
  `2026-09-30-remove-the-process-figure-from-the`.
