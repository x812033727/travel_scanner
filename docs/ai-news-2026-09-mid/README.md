# 2026 年 AI 新聞第三批：9 月中 7 篇與月份索引更新

補上前兩批（`docs/ai-news-2026-09`、`docs/ai-news-2026-ytd`）之後的 7 則消息，每篇提供 zh-TW、en、ja、ko、zh-CN 全文、原創主圖與 2×2 圖解。事件日 2026-07-08 至 2026-09-14，官方來源查核日一律 2026-09-15。題目由站主在 2026-09-15 從候選清單選定。篇目、事件日與五語網址見 [manifest.json](manifest.json) 與 [articles.md](articles.md)。

| 事件日 | slug | 主軸 |
|---|---|---|
| 2026-07-08 | `ai-news-gpt-live-voice-20260708` | ChatGPT 語音邊聽邊說、各方案模型與用量、錄音與訓練設定 |
| 2026-09-04 | `ai-news-google-assistant-gemini-20260904` | 行動裝置上的 Google Assistant 由 Gemini 接手、換手前後檢查 |
| 2026-09-10 | `ai-news-anthropic-threat-report-20260910` | Anthropic 九月威脅情報報告、帳號與 API 金鑰自保 |
| 2026-09-10 | `ai-news-openai-agents-api-20260910` | Agents API 公開 beta 的計費、資料落地與委託時要問的事 |
| 2026-09-10 | `ai-news-deepseek-v41-flash-20260910` | V4.1-Flash 上線、V4-Pro 去留的兩種官方說法、模型換手 |
| 2026-09-12 | `ai-news-pace-the-frontier-20260912` | Amodei〈We Must Pace the Frontier〉的主張與三位執行長的回應 |
| 2026-09-14 | `ai-news-siri-ai-ios-27-20260914` | Siri AI 英文 beta、台灣 iPhone 使用者現在能用什麼 |

內容包沿用 `kind=life`、既有 `ai` 主題與五語欄位，沒有 API、資料庫或前端變更。

## 查證

規則寫在 [BRIEF.md](BRIEF.md)：`sources` 只放一手來源（廠商公告、說明中心、API 文件、當事人原文），整合站只當線索；廠商能力歸因給廠商，本站沒有實測；分批開放、beta 與地區限制分開寫。每篇的研究紀錄在 `research/`，`unverified_or_excluded` 列出看到但沒寫進文章的說法與原因。

流程是一篇一個撰稿代理，寫完交給另一個代理獨立查核，查核者把文章拆成主張逐條對原文，紀錄在 `factcheck/`：

| 文章 | 主張數 | 改動 | 備註 |
|---|---|---|---|
| GPT-Live | 88 | 15 | 訓練開關條件寫錯；官方發布日是 7/8，slug 由原訂 0709 改名 |
| Google Assistant | 102 | 20 | 內建 Google 的車輛不是「一直用 Assistant」；說明頁仍保留切回步驟，與社群公告矛盾 |
| 威脅報告 | 92 | 18 | 駭客案「全部失敗」誤讀；非法蒸餾改寫為 Anthropic 單方指控 |
| Agents API | 56 | 15 | 「資料只在美國」改為官方原意「資料落地只支援美國」 |
| DeepSeek | 91 | 15 | V4-Pro「9/14 起改導向」與「繼續提供」分屬不同官方頁，未標日期 |
| Pace the Frontier | 92 | 38＋11 | 只刊在 Amodei 個人網站，不寫成「Anthropic 表示」；改動多，另做第二輪查核，補回「未對齊」「未受節制」等原文限定 |
| Siri AI | 95 | 16 | 台灣未被列為排除地區，不等於 Apple 確認台灣帳號可用 |

之後我逐篇讀過全文，另改了幾處：Google 篇標題改「換手前後」、威脅報告一處過度簡化的金鑰外洩說法、DeepSeek 標題改為「V4-Pro 去留有兩種說法」、Siri 隱私段「隨時驗證」改回 Apple 原意「持續驗證」、Pace 首段「應該」改回原文的「必須」。

## 翻譯

前兩批用站上 Gemini 供應商翻譯，那些腳本只能在正式站 API 容器內跑。這批改在本機由代理翻譯，規格見 [TRANSLATION.md](TRANSLATION.md)。`merge_locale.py` 把每個語言併入內容包，比對區塊型別、表格維度與來源網址，且不動 zh-TW。介面名稱（ChatGPT、Google、Apple 設定）由翻譯者對照各語言官方說明頁。

翻譯完成後，四位審稿代理各審一個語言、七篇逐段對照 zh-TW，只交修正清單，由 `apply_corrections.py` 統一套用，避免多個代理同時寫同一檔案。套用 98 筆（[translation-corrections.json](translation-corrections.json)），不採用 12 筆（[translation-corrections-rejected.json](translation-corrections-rejected.json)）：多數是審稿者要把繁中說明頁的介面譯名放回其他語言版，但翻譯者已對過該語言的官方頁；另有 3 筆韓文 Siri 功能名稱，Apple 韓國功能適用範圍頁的正式名稱就是原譯。

## 圖像與索引

`build_assets.py` 沿用前兩批的繪圖元件與配色，每篇新增一個主圖構圖，用 Edge headless 渲染成 1600×900 JPEG（每張約 60 KB），圖解是研究紀錄裡四格文字的 SVG。contact sheet（`hero-sheet-*`、`diagram-1-sheet-*`）逐張看過；`renders/` 是忽略的中間產物。

`update_index.py` 原地更新 `ai-news-2026-january-september-index`：五語各加 7 個連結、篇數 31 → 38、7 月與 9 月的表格與段落、兩條新來源。7 篇事件日都在 9 月 14 日以前，所以 slug 與標題的日期範圍不變。同時修好 #497 以來日文版月份標題的錯位：原本 9 個「2026年N月のニュース解説」被 callout 文字與 8 個文章標題佔住。

## 本機驗證

- `check_article.py <slug> --full --assets`：7 篇全 OK（結構、字數 1,800–3,000、簡體字掃描、事件日與查核日、表格 ≤ 4 欄、連結文字等於目標標題、五語對應、圖片存在且 ≤ 300 KB、圖上數字出現在正文）。
- `python -m app.guides.pack_cli lint --kind life`：0 error。7 篇英文正文 7,700–10,100 字元，超過 6,000 的 `text_length` 建議值，只是警告；前兩批同樣如此（Glasswing 英文 8,599），沒有為了字數刪條件。
- `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py`：12 passed、5 skipped（PostgreSQL 項目由 CI 執行）。
- 讀內容包的假 API ＋ `next dev`：35 個語言頁都回 200、有 h1、表格、6 個 hreflang、無 robots meta，主圖與圖解都載得到；手機寬 375 px 沒有橫向溢出，最擠的 DeepSeek 英文表格每列 ≤ 113 px；索引五語都連到 38 篇，日文月份標題正確。

## 已知限制

- sources 上限 4 條，部分查到的一手資料只留在研究紀錄（例如 Agents API 的子代理數上限、Google Assistant 社群另一則寫 9 月 3 日起分批移除的公告）。
- DeepSeek「繼續提供 V4-Pro」的說明官方未標日期；Siri AI 的「符合資格的地區」是否含台灣，Apple 未說明；三篇都照實寫成未說明。
- 查核途中順帶發現、不在本批範圍的既有文章問題，記在任務票的 Notes。

## 刊登

尚未匯入正式站。合併並部署後，用 `guides-import` 帶 `--slug` 只匯入本批 7 篇與索引，先 `--dry-run`（預期 35 create、索引 5 update），確認沒有其他批次的文章後才 `--publish`，再逐頁驗證。線上文章 sitemap 目前約 925 列，加上 35 列後仍在 1,000 上限內；拆分 sitemap 的票是 `2026-09-14-sitemap-split-before-1000-rows`。
