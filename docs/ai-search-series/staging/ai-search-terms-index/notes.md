# ai-search-terms-index 查證記錄

這一篇是**總索引**，本身不提出新的事實主張：它摘要十篇專文已經查證過的內容，並把
`catalogue.json` 的 `disagreements` 逐條寫成正文。

因此 `sources` 收的是十篇裡的**錨點來源**——也就是撐住索引那張比較表與五個分歧點的一手來源。
每一筆都由該篇的撰稿代理在 **2026-09-14** 當天以 WebFetch／WebSearch 讀取一手網址後寫入該篇的
`sources`，本篇沿用同一組網址與同一個查證日，沒有另行宣稱更新的查證。下表標出每一筆是哪一篇驗的。

| 主張 | 來源網址 | 查證日 | 由哪一篇查證 |
| --- | --- | --- | --- |
| GEO 出自 2023 年的一篇論文，論文有自己的查詢集與指標 | https://arxiv.org/abs/2311.09735 | 2026-09-14 | `ai-search-geo` |
| Google 的官方指南定義了 AEO 與 GEO，且說為生成式 AI 最佳化仍然是 SEO | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | `ai-search-geo`、`ai-search-aio` |
| Google 官方文件說明 AI 功能與網站的關係，沒有額外的最佳化要求 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | `ai-search-geo`、`ai-search-generated-answers` |
| E-E-A-T 出自搜尋品質評分指南，那份文件是寫給人類評分者看的 | https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf | 2026-09-14 | `ai-search-eeat` |
| llms.txt 是社群提案，提案本身說明它要解決什麼問題 | https://llmstxt.org/ | 2026-09-14 | `ai-search-llms-txt` |
| 各 user-agent 的用途與界線（訓練、檢索、索引是三件事） | https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers | 2026-09-14 | `ai-search-llmo`、`ai-search-llms-txt` |
| 功能會被收掉：FAQ 複合式搜尋結果的淘汰與說明文件移除紀錄 | https://developers.google.com/search/updates | 2026-09-14 | `ai-search-structured-data`、`ai-search-llms-txt` |
| AI 模式的官方產品說明 | https://support.google.com/websearch/answer/16011537 | 2026-09-14 | `ai-search-generated-answers`、`ai-search-measuring-citations` |

## 比較表每一格的依據

| 表格內容 | 依據 |
| --- | --- |
| 「AIO：查證的文件裡沒有這個縮寫」 | `ai-search-aio` 的查證結論。該篇把主張限縮為「本文查證的 Google 官方文件與說明頁裡沒有出現 AIO」，**不寫成「Google 從來沒用過」**；本篇沿用同樣的限縮寫法。 |
| 「GEO：論文有；業界沿用名字沒沿用指標」 | `ai-search-geo`。論文的 GEO-Bench 與兩個指標在該篇寫明，索引不重複數字。 |
| 「AEO：混用與區分兩派並存」 | `ai-search-aeo`。兩派各有來源，該篇明說不裁決。 |
| 「SEO：可以，有官方報表」 | `ai-search-seo` 與 `ai-search-measuring-citations`。索引只寫「有官方報表」，報表的涵蓋範圍與限制在量測那篇。 |

## 圖上的數字

`diagram-1.svg` 出現的阿拉伯數字只有兩個：`2023`（GEO 論文年份）與落款的 `2026`。
兩者都原字串出現在正文（「2023 年的一篇論文」、「2026 年 9 月 14 日」）。
`hero.svg` 完全沒有數字。`missing_diagram_numbers` 回傳空清單。

初稿的正文原本用中文數字寫日期（「二〇二六年九月十四日」），與系列其他九篇的寫法不一致，
也會讓落款的 `2026` 在正文找不到對應字串。已改為阿拉伯數字。

## 沒有寫進去的東西

- **沒有新的成效數字。** 索引不引用任何百分比，包括 GEO 論文的那個——那是該篇的工作，
  而且必須連同它的設定一起讀。
- **沒有替五個分歧裁決。** 正文明寫「本系列都不替任何一方裁決，只寫出誰這樣主張」。
- **沒有宣稱收錄結果。** callout 明寫本系列沒有量測過搜尋引擎實際的收錄或引用結果。
