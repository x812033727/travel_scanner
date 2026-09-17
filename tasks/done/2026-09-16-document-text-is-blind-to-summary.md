---
id: 2026-09-16-document-text-is-blind-to-summary
title: _document_text is blind to summary and faq blocks
status: done
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-16T14:49:56Z
created_at: 2026-09-16T14:49:47Z
completed_at: 2026-09-16T14:57:11Z
branch: claude/brave-hopper-8ezxba
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guide_rich_blocks.py
---

# _document_text is blind to summary and faq blocks

## Why

`_document_text` 的 docstring 寫「Every string a reader sees, joined」，但它的分支停在
`LinkBlock`，**沒有 `SummaryBlock` 與 `FaqBlock`**。這兩種區塊是 #531 Phase 4 才加的，
當時補進了 `_body_parts`（所以 `text_length` 與 `finance_claim_language` 沒有這個洞），
`_document_text` 漏掉了。

兩個實際後果，而且新聞批次 4 的 36 篇**每一篇都強制帶這兩個區塊**，所以它從理論問題
變成每篇都會踩到：

- **簡體字掃描會漏。** 新聞批次的 `check_article.py` 用 `_document_text(zh)` 掃簡體字，
  摘要或 FAQ 答案裡的簡體字掃不出來。五語文章的 zh-TW 混進簡體字是很實際的風險。
- **圖上數字的規則會誤報。** `missing_diagram_numbers` 比對的就是 `_document_text`，
  所以圖上畫了一個只出現在摘要裡的數字，會被判成「文章沒有提到」。

## What changed

`_document_text` 加上兩個分支：`SummaryBlock` 取 `items`，`FaqBlock` 取每則的
question 與 answer。docstring 一併說明為什麼這兩種區塊要算進來。

FAQ 的 question 與 answer 分開 extend、不是串成一個字串，因為這個函式的輸出會被
`_NUMBER` 掃描；串起來會讓「問題結尾的數字」與「答案開頭的數字」黏成一個假的數字。
（`_body_parts` 那邊是計長度用的，串起來沒有影響，所以兩邊寫法不同是刻意的。）

## Definition of done

- [x] `_document_text` 回傳的字串含摘要與 FAQ，所以簡體字掃描掃得到它們，
      圖上只在摘要出現的數字不再被判成「文章沒有提到」。

## Steps

- [x] `_document_text` 加 `SummaryBlock` 與 `FaqBlock` 分支，docstring 說明理由。
- [x] 回歸測試，含正例與反例，並做變異驗證（拿掉修正會紅）。
- [x] 掃過 `pack_ingest` 其餘走訪區塊的函式，確認沒有第二處同類缺口。

## How to verify

```bash
cd apps/api
uv run pytest tests/test_guide_rich_blocks.py
uv run ruff check . && uv run mypy app && uv run pytest
uv run python -m app.guides.pack_cli lint --kind life    # 0 error
```

實際結果（2026-09-16）：**3,902 passed / 343 skipped / 0 failed**、
`lint --kind life` 845 篇 **0 error**、ruff 與 mypy 全過。

## Notes

- 回歸測試做過**變異驗證**：把兩個分支拿掉，`test_document_text_carries_the_summary_and_the_faq`
  會紅；放回去 9 passed。測試同時驗正例（圖上的 170GB/s 只出現在摘要、512GB 只出現在
  FAQ 答案，都不該被判缺）與反例（999GB 仍然要被判缺）。
- `search.document_text`（`search.py` 的另一個同名函式）**本來就有**摘要與 FAQ，
  而且 `tests/test_guides_search.py` 有一條測試逐字驗它。只有 `pack_ingest` 這個漏了。
- 掃過 `pack_ingest` 其餘走訪區塊的函式，沒有發現第二處同類缺口。
- 這個問題是批次 4 工具移植的驗證代理發現的，不是人工查出來的。

### 結案後的補強（同日）

批次 4 工具移植的驗證代理**獨立重跑了這個修正**，用 before/after 探針確認它真的有效：
zh-TW 摘要裡的簡體字，修正前 `exit=0 OK`、修正後 `exit=1 - simplified characters in zh-TW: 语这问题`；
FAQ 答案裡的簡體字同樣從 `exit=0` 變成 `exit=1`；圖上只在 FAQ 出現的數字，
修正前被誤報成「文章沒有提到」，修正後不再誤報。

同一批驗證也指出**原本的回歸測試沒有釘住那個刻意的決定**：commit 訊息說 question 與
answer 要分開 extend、不能串接，但測試在串接版本下**照樣會過**。已補上
`test_document_text_never_fuses_a_question_into_its_answer`：FAQ 的問題結尾是 `5`、
答案開頭是 `12GB`，串接會在接縫處生出文章從來沒寫過的 `512`。
串接版本下這條測試會紅，實測確認過。

