---
id: 2026-10-05-ai-news-index-zh-tw-says
title: AI news index zh-TW says every linked article has five languages
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T06:49:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4/update_index.py
---

# AI news index zh-TW says every linked article has five languages

## Why

The zh-TW document of `ai-news-2026-january-september-index` links 16 articles that exist in
zh-TW only (batches 4.4, 4.6 and 4.7: Claude text watermark, Google AI student offer, OpenAI
zero data retention, the Hugging Face incident, the Cursor wind-down, Meta Muse, the Accenture
evaluation, the Australia youth-safety blueprint, Gemini Notebook study tools, Kimi K3 on
Bedrock, the math advisory group, frontier standards, life-sciences verification, Meta One,
OpenAI Academy paths, NVIDIA physical-AI safety). Three zh-TW sentences still promise five
languages for everything the index links:

- the description: 「連到五語完整解析」;
- the month table's caption (block 9): 「各月的新聞解析都提供五種語言」;
- block 24: 「繁體中文、簡體中文、英文、日文與韓文均提供全文，透過頁面的語言切換即可閱讀」.

A reader who follows one of those 16 links and switches language gets no translation. The other
four locales link only five-language articles, so their sentences are true.

## Definition of done

- [ ] The three zh-TW sentences no longer claim five languages for every linked article (for
      example "most articles are also in English, Japanese, Korean and Simplified Chinese"), or
      the 16 articles are localized (skill `article-localization`) and the sentences stay.
- [ ] No article count in the new wording (`update_index.py` `COUNT_RULE` guards the AI index).

## Steps

- [ ] Decide between rewording and localizing; the description is also in the scope of
      `2026-10-03-ai-news-index-month-range` (title and month range), so fold the description
      sentence into that ticket's run if it is still open.
- [ ] Add zh-TW rows to `EDITS` (description, block 24) and `CAPTION` (block 9) in
      `docs/news-2026-batch-4/update_index.py`; `--dry-run`, then run it with `--locale=zh-TW`.
- [ ] `pack_cli lint --kind life --slug ai-news-2026-january-september-index`.

## How to verify

`PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/update_index.py ai --locale=zh-TW --dry-run`
shows only the three sentences; the zh-TW page no longer says all linked articles are in five
languages.

## Notes

- Found by `2026-09-26-refresh-stale-parts-of-the-three` (2026-10-05), which rewrote the AI
  index's paragraphs 1 and 20 and the month table but left these three sentences alone: they
  are not the stale parts that ticket listed.
- zh-TW has 115 blocks and the other locales 99; the 16 extra blocks are exactly those links.
