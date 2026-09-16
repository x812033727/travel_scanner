---
id: 2026-09-15-content-summary-howto-and-life
title: 編輯為攻略與生活文章加入重點摘要（summary）與真實 FAQ
status: in-progress
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T03:39:50Z
created_at: 2026-09-15T13:57:48Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-summary-faq-definedterm-jsonld-web
scope:
  - apps/api/app/guides/content
---

# 編輯為攻略與生活文章加入重點摘要（summary）與真實 FAQ

## Why

有了區塊之後內容要有人寫。站主 2026-09-16 決定：**摘要由模型從文章本身起草、站主逐批審 diff**（取代原本的「不自動生成」）——
只重述文章已有、已有來源的內容，數字逐字照正文，不加新事實；`pack_cli summarize --from` 會擋正文沒有的數字。
FAQ 只在文章本來就有 ≥2 個真實問答時加（`summarize` 會把「問題：答案」清單或 H3 問答對自動轉成 `faq` 區塊，其餘留在正文）。

## Definition of done

- [ ] 每批：`summarize --digest` 讀材料 → 寫 batch.json → `--from … --dry-run` 全部通過 → `--apply` → `lint --kind X` 不出現新 error →
      `test_guides_content_pack`／`test_guides_content_links` 綠 → 一個 commit，訊息記 `no_summary` 前後數。
- [ ] 批次順序：1 howto zh-TW；2 台灣入境 18 篇 × en/ja/ko/zh-CN（各語系從自己的正文寫，不翻譯）；3 `ai-term-`；4 `claude-code-`；5 `gemini-`；
      6 `codex-`（zh-TW／en+ja／ko+zh-CN 三批）；7 財經；8 其餘依 slug 首字 a–g／h–o／p–z；9 被其他任務持有的 46 篇最後補。每批 ≤ 約 100 份文件。
- [ ] 站主可在任一批之後喊停；已套用的批次各自獨立。

## 文字規則

- 2–5 句、每句一個完整句、≤300 字；第一句是答案（要做什麼／這是什麼），其餘是決定條件、文章給的數字與一個注意事項。
- 只用同一份文件已陳述的事實；數字、票價、日期、產品名逐字照正文（工具會擋）；不加新主張、不加文章沒有的保留語、不寫「本文介紹」這種後設句、不逐字重複 description。
- 全形標點「」（），半形數字與拉丁字母，中英之間留空格；沒有條列符號、emoji、Markdown。

## Steps

- [ ] 工具：`pack_cli summarize`（結論段提案、FAQ 轉換、`--from` 批次、`--digest`）。
- [ ] 批次 1…N 依 DoD 逐批提交。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto --warnings
```

## Notes

**不自動生成**：一句錯的票價會被答案引擎快取。

**2026-09-16 給這張票的持有者（claude-opus-5 留）**：站主決定不等批次做完，
`2026-09-16-content-packs-counts-in-hub-titles` 已經改了這個目錄裡 85 個內容包，批次提交前請先 rebase：

- `gemini-guide`、`ai-terms-index`、`ai-search-terms-index`：標題、描述與開頭段拿掉會成長的數字。
- 82 篇連到名詞總索引的文章（81 篇 `ai-*`、`what-is-a-large-language-model`）：只換一行連結文字
  `AI 名詞總索引：81 個概念，從 Loop Engineering 到生成式 AI` → `AI 名詞總索引：從 Loop Engineering 到生成式 AI`。

之後寫摘要時也請避開目錄大小（「N 篇」「N 個概念」）與課程序號（「第 N 篇」）：站主的規則是
讀者看得到的地方不寫會一直增加的數字。
