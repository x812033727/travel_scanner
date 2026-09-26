---
id: 2026-09-26-refresh-stale-parts-of-the-three
title: Refresh stale parts of the three news indexes (crypto hero says four regions, AI month table, Japan heading)
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-26T16:55:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4/build_assets.py
  - apps/web/public/guides/crypto-news-2026-index
---

# Refresh stale parts of the three news indexes (crypto hero says four regions, AI month table, Japan heading)

## Why

Batch 4.8's index run (2026-09-27) added its links and moved the expansion dates in all five
locales, and found older parts of the three index articles that no batch has kept up:

- The crypto index's hero image and its alt still say four regions and a four-item list; the
  index now covers six (Taiwan, US, UK, EU, Japan, Korea). Stale since batch 4.5 added the UK.
- The crypto index's Japan narrative heading 「建議報告、後續立法與資安」 does not cover the FSA's
  2026-09-25 on-chain finance forum.
- The AI index's paragraphs 1 and 20 and the September row of its month table name none of the
  articles from batches 4.4, 4.6, 4.7 or 4.8 (ads in Taiwan, Google Vids, the new models).
- The tech index's description lists topics only up to batch 4.5; its en description is at
  472 of 500 characters.

## Definition of done

- [ ] The crypto index hero is redrawn for six regions, and its alt matches, in five locales.
- [ ] The three narrative parts above describe what the indexes now link, in five locales, with
      no article counts (the AI index's `COUNT_RULE`).

## Steps

- [ ] Edit through `docs/news-2026-batch-4/update_index.py` (`EDITS`, `INSERT`) — never rerun
      `build_*_index.py`, which rewrites zh-TW and discards the relinked inlines and translations.
- [ ] Redraw the crypto index hero (`_crypto_index` in `build_assets.py`).
- [ ] `pack_cli lint --kind life --slug <index>` for the three; content tests.

## How to verify

Each index's description, summary, hero and headings name the same set of regions and topics
in all five locales.

## Notes

- Found by the batch 4.8 index agent; its run and table layout are described in
  `docs/news-2026-batch-4/HANDOVER.md` §1h.
