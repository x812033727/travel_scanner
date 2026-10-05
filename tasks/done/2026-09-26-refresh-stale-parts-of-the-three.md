---
id: 2026-09-26-refresh-stale-parts-of-the-three
title: Refresh stale parts of the three news indexes (crypto hero says four regions, AI month table, Japan heading)
status: done
priority: P3
area: docs
owner: claude-opus-5-5-news-indexes-refresh
claimed_at: 2026-10-05T06:14:39Z
created_at: 2026-09-26T16:55:04Z
completed_at: 2026-10-05T06:53:31Z
branch: claude/news-indexes-refresh
depends_on: []
scope:
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/crypto-news-2026/research/crypto-news-2026-index.json
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

- [x] The crypto index hero is redrawn for six regions, and its alt matches, in five locales.
- [x] The three narrative parts above describe what the indexes now link, in five locales, with
      no article counts (the AI index's `COUNT_RULE`).

## Steps

- [x] Edit through `docs/news-2026-batch-4/update_index.py` (`EDITS`, `INSERT`) — never rerun
      `build_*_index.py`, which rewrites zh-TW and discards the relinked inlines and translations.
- [x] Redraw the crypto index hero (`_crypto_index` in `build_assets.py`).
- [x] `pack_cli lint --kind life --slug <index>` for the three; content tests.
- [ ] `guides-import --slug crypto-news-2026-index --slug tech-news-2026-index --slug
      ai-news-2026-january-september-index --publish` on the host: publish after merge
      (coordinator, owner consent).

## How to verify

Each index's description, summary, hero and headings name the same set of regions and topics
in all five locales.

## Notes

- Found by the batch 4.8 index agent; its run and table layout are described in
  `docs/news-2026-batch-4/HANDOVER.md` §1h.
- Done 2026-10-05 by claude-opus-5-5-news-indexes-refresh (branch `claude/news-indexes-refresh`).
  `update_index.py ai tech crypto` (dry run first) wrote every change; no link added, no date
  moved. `EDITS` learned a `"hero_alt"` target (the hero is not a block); 4.11's tables are kept
  as `_NEW_4_11`, `_EDITS_4_11`, `_INSERT_4_11`. The rows are one-shot like every batch's: a
  second run refuses.
- Scope grew by two paths: `docs/news-2026-batch-4/update_index.py` (the Steps say to edit
  through it) and `docs/crypto-news-2026/research/crypto-news-2026-index.json`, whose
  `hero_label` (printed on the hero) said 「四個地區」 in five locales; it now says six.
- Crypto: `_crypto_index` draws six panels (Taiwan law with a dashed commencement circle, US
  bank, UK balance, EU seal, Japan lock, Korea order-book bars under a lens) and a six-item
  list; alt rewritten in five locales (en 196 of 200 characters). The Japan heading (block 24)
  now ends with the onchain finance forum in five locales.
- AI: paragraph 1 gains one sentence for everything linked after 4.5, paragraph 20 names the
  late-September models, the ads rollout in Taiwan and Google Vids. zh-TW links 16 zh-TW-only
  articles (4.4, 4.6, 4.7) that the other four locales do not, so the zh-TW rows also name
  those. The September row gains pricing, ads, video (zh-TW also 學習); zh-TW's August row also
  gains 4.4's student offer and data retention, which the ticket did not list but which are the
  same staleness. `COUNT_RULE` passed.
- Tech: the description listed batch 4.2's thirteen topics; it now also names Snapdragon 8 Elite
  Gen 6, App Store subscriptions, the WordPress and Synology patches, the KIDS Act and (zh-TW,
  ja, ko, zh-CN) the ATT prompt; zh-TW also Googlebook. en rewritten whole: 493 of 500.
- Sources opened 2026-10-05 with the editorial User-Agent (log in the PR): the FSA forum page,
  the Opus 5.5, Sonnet 5.5, GPT-6.1 Sol and Google Vids pages, the ChatGPT changelog, the ads
  availability help page (Taiwan: Available), the Claude Code mods post, the first source of each
  zh-TW-only AI article named, and the Qualcomm, WordPress, Synology, Apple and EU pages named in
  the tech description: all HTTP 200. Only `openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/`
  answered 403 (Cloudflare). No `checked_on` moved: the new text only names what each index links,
  each linked article carries its own dated sources, and the facts the indexes already drew from
  their cited sources were not re-verified. The FSA forum page now reads 令和8年9月30日更新;
  whoever next rereads `crypto-news-japan-onchain-finance-forum-20260925` should look.
- Rendered on Windows with Playwright's `chromium_headless_shell-1243` via `CHROMIUM_BIN`
  (`build_assets.py crypto --slug=crypto-news-2026-index`); heroes are about 75 KB, under the
  guideline. The run also rewrote the five diagram SVGs with CRLF and nothing else; Python's
  text mode on Windows writes CRLF, so the JSONs and SVGs were put back to LF.
- Left alone on purpose: the AI title, description and opening sentence (`2026-10-03-ai-news-index-month-range`,
  owner decision), the month table's missing October row and an October narrative (same ticket);
  the tech hero, which shows four kinds of story as its title does. Filed
  `2026-10-05-ai-news-index-zh-tw-says`: three zh-TW sentences promise five languages for every
  linked article.
- Checks that stay red for reasons older than this change: `intake_check.py --from-content` on
  the three indexes reports "first block is not summary" (the index layout puts the summary third)
  and, for crypto zh-TW, three self-references (本文/這篇, all in the investment-disclaimer
  callout); `space_cjk.py --locale=zh-CN` flags the 4.8 forum paragraph (block 27), whose
  Japanese forum name is quoted with “…” instead of 「…」.
