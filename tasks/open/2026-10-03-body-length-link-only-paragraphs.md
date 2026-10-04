---
id: 2026-10-03-body-length-link-only-paragraphs
title: _body_length counts link-only paragraphs although its docstring excludes link labels
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-pack-ingest-fixes
claimed_at: 2026-10-04T14:46:39Z
created_at: 2026-10-03T12:04:03Z
completed_at:
branch: claude/pack-ingest-body-length-render-svg
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guide_rich_blocks.py
---

# _body_length counts link-only paragraphs although its docstring excludes link labels

## Why

`_body_parts` 的 docstring 寫它算的是 running text，「not the title, captions or link labels」；`link` 區塊確實不算，
但一個只含一個 `article` inline 的 `rich_paragraph`（站內「延伸閱讀」那種單行連結）整段算進正文。
後果：連結多的頁面字數被高估。`ai-terms-index` 有 105 條這種連結，正文因此一度跑到 5,910 字逼近 life 的 6,000 警告線，
2026-10-03 只好把連結文字縮成名詞本身。

## Definition of done

- [x] 只含連結 inline、沒有其他文字的 `rich_paragraph` 不算進 `_body_length`（句子中的連結照算，因為它是句子的一部分）。
- [x] 測試涵蓋兩種情況。
- [ ] 全站 `pack_cli lint` 沒有新的 `text_length` 警告（低於 1,500 的那端要看一下）。見 Notes：多了兩個 ja 的下限警告，轉到 `2026-10-04-two-ja-life-articles-read-under`。

## Steps

- [x] 改 `_body_parts`、加測試、跑全站 lint 比對前後字數。

## How to verify

`uv run pytest tests/test_guide_rich_blocks.py tests/test_guides_pack_ingest.py -q`；`pack_cli lint --kind life`。

## Notes

- `pack_ingest.py` 在 `2026-09-14-codex-learning-series`（blocked）的 scope 裡，要先協調。
- 2026-10-04 認領（claude-opus-5-5-pack-ingest-fixes，分支 `claude/pack-ingest-body-length-render-svg`，與
  `2026-10-03-render-svg-full-chrome-crop` 同一個 PR）：
  - `2026-09-14-codex-learning-series` 是 `blocked` 而且沒有 owner；`tools/tasks.mjs` 的 `HOLDS_SCOPE` 只有
    `in-progress`／`review`，blocked 的票不占 scope，認領沒有被它擋。
  - 認領被 `2026-10-03-illustrated-slides-round-2-a-family`（review，claude-fable-5-1-illustration-round2，scope 含整個
    `apps/api/tests`）擋下，用 `--force` 蓋過：那張票的分支 `claude/video-production-tutorial-optimization-f5d1bc`
    已經以 #1172（`b0a264567`，2026-10-03T10:34Z）合併進 main，只是票沒 `done`。
- 做法：`_links_only(block)` —— 每個 inline 都是 `link`／`article`，或是只有空白的文字 —— 的 `rich_paragraph`
  不進 `_body_parts`。中間夾任何非空白字（例如 `、`）就算句子，照算。`_document_text` 不變：讀者看得到那一行，
  圖表數字規則與簡體字掃描照樣讀它。`finance_claim_language` 也讀 `_body_parts`，所以它同樣不再讀單行連結的標籤，
  跟 `link` 區塊一致；全站 lint 前後除了 `text_length` 以外沒有任何一行不同（finance 警告沒有增減）。
- 量測（全站 1,178 個 pack、2,450 個（pack, locale），在改動前後各跑一次 `_body_length` 與
  `pack_cli lint --kind intel|howto|life`）：
  - 1,059 個 pack 有這種段落（全站 6,268 段：6,262 段是單一 `article` inline，6 段是單一外部 `link`），2,239 個（pack, locale）字數下降，
    中位數 −54 字，最多 −4,604（`ai-news-2026-january-september-index` en 14,351 → 9,747）；沒有任何一個變多。
    `ai-terms-index` zh-TW 5,444 → 3,506。
  - `text_length` 警告：intel 2 → 2、howto 56 → 55、life 384 → 362。25 個超過上限的（pack, locale）回到範圍內
    （例如 `tech-news-2026-index` zh-TW 6,812 → 5,667、`singapore-hawker-first-visit` en 6,249 → 5,968）。
  - 新增的下限警告兩個，都是 ja：`household-inventory-spreadsheet` 1,538 → 1,496、`weekly-review-reset-routine`
    1,512 → 1,482。兩篇各只扣掉一行站內連結，zh-TW 原文本來就有 `text_length` 警告（984 → 960、984 → 957），
    所以低於下限的 pack 數前後都是 19 個。依指示不改內容，開了 `2026-10-04-two-ja-life-articles-read-under` 追蹤。
  - 改動後離下限 200 字以內、但還在線上的：`shared-household-calendar` ja 1,509、`phone-document-scanning-workflow`
    ja 1,524、`reading-notes-that-you-reuse` ja 1,546、`file-naming-system-for-home` ja 1,583 等 12 個（多數是 ja）。
