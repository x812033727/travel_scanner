# 第二輪獨立查核共用規格：新聞批次 4.3 AI

你是**一篇** AI 新聞的**第二輪**獨立查核代理。你沒有參與撰稿，也沒有參與第一輪。

## 先讀

1. 第一輪用的規格（規則全部適用）：`C:\Users\x8120\AppData\Local\Temp\claude\C--Users-x8120-mokaair--claude-worktrees-travel-guide-articles-planning-eab8c5\6bc15b49-339e-47bf-9727-38b4d1d65292\scratchpad\agents\ai\FACTCHECK-AI.md`
2. 第一輪的報告：`C:\Users\x8120\mokaair\.claude\worktrees\travel-guide-articles-planning-eab8c5\docs\news-2026-batch-4\factcheck-draft\<slug>.md`
3. 草稿的兩個檔：內容包 `...\apps\api\app\guides\content\<slug>.json`、研究紀錄 `...\docs\ai-news-2026-09-late\research\<slug>.json`

## 範圍（不是整篇重做）

1. 覆核第一輪**改動過的每一個段落**，以及**第一輪新寫進去的每一句**——新寫的句子沒有人查過，要逐句回 `sources[]` 原文。來源自己重抓：`curl -sL -A "Mokaair-editorial"`（主機拒絕這個 UA 時可退回 curl 預設 UA，不要自訂別的）。**任何請求的 UA、標頭、查詢字串、表單都不得帶入任何人的 email 或個人資料。** 讀不到正文的來源不能撐任何句子。
2. 研究紀錄的每一條 `verbatim_quote` 用程式做**連續字串**比對（對你抓到的正文）；含 `...`、`…` 或 `|` 的引文逐片段看是不是同一句、有沒有把不同段落拼在一起。對不上的換成對得上的連續片段，或刪掉那條事實並同步改正文。
3. 回掃第一輪有沒有為了塞字數刪掉但書、限定詞或歸因（「最高／up to」「預計」「可能」「OpenAI 表示」…）。但書不可以為了字數刪；要騰字就刪重複的敘述。段落字數不得超過 3,000。
4. `summary` ⊆ 正文、FAQ 的答案 ⊆ 正文、圖解 nodes 的數字都出現在正文；範圍不明的否定句（「官方沒有說」）一律限縮到「本文引用的這幾頁、查核日」。
5. 界線再掃一次：不帶 `finance` 主題、沒有投資免責 callout、只有一個一般 callout；沒有訂閱、購買、升級或投資建議；沒有推定台灣可用；廠商宣稱全部歸因；不重寫站上既有 AI 文章、不與它們矛盾。
6. 指派訊息裡另外點名的疑點。

## 交付

- 結果附加在同一份報告檔的最後，開一節「## 第二輪」。
- 研究紀錄的 `factcheck` 底下加 `second_round`（日期、查了幾條、改了幾處、結論）。
- 改完自己跑（從 `apps/api`，用 `./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug>`，不要用 `uv run`）：只能剩允許的 FAIL——索引標題那一條，以及第二個連結的標題／目標那一條。
- 只動這三個檔。不要 git add／commit，不要在 repo 裡留暫存檔。

## 回報（最後一則訊息，繁體中文，12 行以內）

查了幾條、又改了幾處、最重的三處、留給站主的事、自檢最後輸出、結論（`ok` 或 `needs_owner`）。
