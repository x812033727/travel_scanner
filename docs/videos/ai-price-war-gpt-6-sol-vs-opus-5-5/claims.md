# claims — ai-price-war-gpt-6-sol-vs-opus-5-5

2026-09-30 依站主 2026-09-28 選定的大綱 B「跟著價目表逐格讀」重寫：腳本、章節與示範都改了，本檔取代 2026-09-28 的舊清單。舊稿的 2026-09-29 兩輪獨立查核（`verify-p1-20260929.md`、`verify-p1-20260929-round2.md`）更正過的說法沒有帶回：不宣稱 Luna 降幅、不引 OpenAI 發布文原話、不說「批次型」、不說字數計價、不說快取一定命中。新稿尚未經獨立查核，`verify-*` 報告對的是舊稿，不代表本稿通過。

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。金額都是每百萬 token、標準處理、美元；情境帳單為官方單價實算（算式見 c17）。官方頁都在 2026-09-30 以編輯用 User-Agent 重新打開（OpenAI 價目表 `platform.openai.com/docs/pricing` 轉址到 `developers.openai.com/api/docs/pricing`，HTTP 200；表格取自頁面內嵌資料與該頁的 `.md` 版本）。

## 價目與官方說法

c1｜GPT-6 Sol 標準價、短脈絡：輸入 2、快取讀取 0.20、快取寫入 2.50、輸出 10｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜eight-prices, you-think, sol-table, cache-math, write-costs-more, batch-half, half-of-promo, sol-61, monthly-bill
c2｜GPT-6 Sol 標準價、長脈絡：輸入 4、快取讀取 0.40、快取寫入 5、輸出 15；頁面定義「Short context: ≤272K input tokens. Long context: >272K input tokens」｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜eight-prices, you-think, context-split, sol-table, answer-recap
c3｜批次頁 GPT-6 Sol 短脈絡 1／0.10／1.25／5，四格都是標準價的一半（長脈絡 2／0.20／2.50／7.50 亦然）；Batch API「50% cost discount」「each batch completes within 24 hours」｜https://developers.openai.com/api/docs/pricing 、 https://developers.openai.com/api/docs/guides/batch｜2026-09-30｜batch-half, other-tabs, answer-recap
c4｜快速模式（Fast）頁 GPT-6 Sol 短脈絡 4／0.40／5／20，是標準價的兩倍；頁面註記 Priority processing 於 2026-07-30 更名為 Fast mode｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜other-tabs
c5｜快取寫入是標準輸入價的 1.25 倍；快取讀取 0.1 倍（GPT-6.1 Sol 為 0.05 倍）；寫一次、完整讀九次是 2.15 倍，沒有快取十次是 10 倍｜https://developers.openai.com/api/docs/guides/prompt-caching｜2026-09-30｜cache-math, write-costs-more, sol-61, answer-recap
c6｜快取要相同的前綴；最短可快取長度 1,024 token（GPT-5.6 及之後）；快取項目不會永久保存｜https://developers.openai.com/api/docs/guides/prompt-caching｜2026-09-30｜cache-conditions
c7｜一個輸入 token 只會算成輸入、快取輸入、快取寫入其中一種，寫入不是額外加收；輸出價含看不見的推理 token（價目表表頭說明）｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜four-tokens
c8｜GPT-5.6 Sol 短脈絡 4／0.40／5／20；頁尾註記「GPT-5.6 Sol’s promotional pricing is available at least through November 21, 2026」；GPT-6 Sol 短脈絡四格都是它的一半（4→2、0.40→0.20、5→2.50、20→10）｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜promo-quote, half-of-promo, compare-to-last-gen, news-three-numbers, three-words
c9｜GPT-6 Sol 與 GPT-6 Luna 於 2026-09-22 上線（更新紀錄）；Claude Opus 5.5 公告頁日期同為 2026 年 9 月 22 日｜https://developers.openai.com/api/docs/changelog 、 https://www.anthropic.com/claude-opus-5-5｜2026-09-30｜news-three-numbers
c10｜2026-09-29 上線 gpt-6.1-sol，標準短脈絡 2／0.10／2.50／10；價目表旗艦區列 gpt-6-astra、gpt-6.1-sol、gpt-6-luna，gpt-6-sol 在展開後的全部模型區｜https://developers.openai.com/api/docs/changelog 、 https://developers.openai.com/api/docs/pricing｜2026-09-30｜sol-61, chase-new
c11｜GPT-6 Luna 標準短脈絡：輸入 0.10、快取讀取 0.01、快取寫入 0.125、輸出 0.50｜https://developers.openai.com/api/docs/pricing｜2026-09-30｜monthly-bill
c12｜Claude Opus 5.5：輸入 4、輸出 20、快取讀取 0.20、快取寫入 5｜https://claude.com/pricing 、 https://www.anthropic.com/claude-opus-5-5｜2026-09-30｜monthly-bill
c13｜Opus 5.5 對 Opus 5：輸入輸出各少 20%（5→4、25→20）、快取讀取少 60%（0.50→0.20）；「costs 40% less to run than Opus 5」是預設設定、一般工作負載下的成本估計，來自「costs less per token … and uses fewer tokens per task」｜https://www.anthropic.com/claude-opus-5-5｜2026-09-30｜news-three-numbers, anthropic-quote, cut-buckets, real-list-cut, three-words, compare-to-last-gen
c14｜Claude Opus 5（舊版）輸入 5、快取讀取 0.50、輸出 25，仍列在價目表的 Legacy models｜https://claude.com/pricing｜2026-09-30｜compare-to-last-gen, real-list-cut
c15｜Claude Sonnet 5.5（2026-09-28 發布）輸入 2、快取讀取 0.20、快取寫入 2.50、輸出 10，與 Sonnet 5 同價；價目表已把 Sonnet 5 移到舊版｜https://www.anthropic.com/claude-sonnet-5-5 、 https://claude.com/pricing｜2026-09-30｜monthly-bill
c16｜Gemini 3.8 Flash 標準：輸入 0.75、輸出 3.75、快取 0.075，「through December 31, 2026」；2027-01-01 起 1.50／7.50／0.15（單價翻倍）｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-30｜monthly-bill
c21｜Anthropic 原文：cache reads「make up the majority of agentic and coding work costs」（Opus 5.5 公告）｜https://www.anthropic.com/claude-opus-5-5｜2026-09-30｜anthropic-cache-quote

## 實算（官方單價 × 示範用量）

c17｜三種示範用量（百萬 token）：聊天型 輸入 5、輸出 1；代理型 新輸入 12、快取讀取 48、輸出 4；大量整理 輸入 200、輸出 10。15 格帳單（美元，聊天／代理／大量整理）：Sol 20／73.6／500；Luna 1／3.68／25；Opus 5.5 40／137.6／1,000；Sonnet 5.5 20／73.6／500；Gemini 3.8 Flash 7.5／27.6／187.5。例：Sol 代理 12×2＋48×0.2＋4×10＝73.6。已用小腳本 `_tools/arith.py` 重算｜實算自 c1、c11、c12、c15、c16｜2026-09-30｜scenario-walk, monthly-bill
c18｜聊天型：GPT-5.6 Sol 促銷價 5×4＋1×20＝40，GPT-6 Sol 20，剛好一半｜實算自 c8、c1｜2026-09-30｜compare-to-last-gen
c19｜代理型：Opus 5 12×5＋48×0.5＋4×25＝184，Opus 5.5 137.6，少 25.217%（約兩成五）｜實算自 c13、c14｜2026-09-30｜compare-to-last-gen
c20｜代理型 Sol 73.6 之中，輸出 40（54.35%）、快取讀取 9.6（13.04%）；快取讀取 4,800 萬對輸出 400 萬＝12 倍｜實算自 c1、c17｜2026-09-30｜output-share, cache-output-ratio
c22｜聊天型 Sol 20 換 Luna 1，每月差 19 美元｜實算自 c17｜2026-09-30｜thirty-dollar-case
c23｜Opus 5.5 的聊天型（40 對 20）和大量整理（1,000 對 500）剛好是 Sol 的兩倍；Sonnet 5.5 三格與 Sol 相同；Gemini 3.8 Flash 三格都介於 Luna 與 Sol 之間｜實算自 c17｜2026-09-30｜monthly-bill
c24｜三種用量最便宜的都是 GPT-6 Luna；這張表只比價格，沒有比品質｜實算自 c17｜2026-09-30｜monthly-bill, price-not-quality
c25｜帳單只含輸入、快取讀取、輸出三種 token 費，未含快取寫入、儲存（Gemini 快取儲存另計每百萬 token 每小時 0.50）、工具與其他服務費；大量整理欄用標準價，沒有套批次折扣｜https://ai.google.dev/gemini-api/docs/pricing 、 https://developers.openai.com/api/docs/pricing｜2026-09-30｜scenario-walk, monthly-bill

## 站內資料（非官方站）

c26｜站內文章〈API 價格比較：每百萬 token 各家多少〉（`ai-api-pricing-comparison-2026`）記的是各家官網 2026-09-15 當天的標準價，含八家、快取與批次折扣、一萬次對話算式；文章比 GPT-6 Sol／Luna 的價格更早，價格欄沒有 GPT-6 Sol 與 Luna｜`apps/api/app/guides/content/ai-api-pricing-comparison-2026.json`（repo 內容檔；正式站是否已上線未核對）｜2026-09-30｜wrap（說明欄也附連結）

## 站主的看法（不是可查證的說法）

- o1｜「新版本不用急著追，先用自己的用量算」｜站主觀點（立場 6）｜chase-new
- o2｜「每月帳單超過五十美元、輸出多、還在用貴的舊模型，才值得花時間算一次；聊天型小用量先別動」「每月省十九美元，未必值得你重測一輪」｜站主觀點與 brief 大綱｜switch-or-not, thirty-dollar-case（口播都標「我的看法是」）
- o3｜「降價不是換工具的理由，帳要自己算」｜站主觀點（立場 1、6）｜switch-or-not, wrap（畫面文字）
- o4｜代理型帳單「先看輸出、不是快取讀取」只限本片這組用量；片中與 Anthropic 原文（c21）並陳，明說兩種都可能對，差在快取讀取是輸出的幾倍｜站主觀點（立場 1、2）｜output-share, anthropic-cache-quote, cache-output-ratio

各場景在 `video.json` 的 `claims` 欄列出用到的 id；沒有數字或只有站主看法的場景（promise、price-not-quality、article-cta、switch-or-not、two-things-first）不列。

## 與企劃不同的地方

- 腳本照 brief 的選項 B（站主 2026-09-28 選定）：開場鉤子、章節順序、示範放第 5 章（brief 排在第 4 章）、結尾下一步都用 B 的；舊稿（選項 A）的章節順序與大半場景已重寫，只留逐字相同的 9 句（id 沿用）。
- 章節從 B 的六章拆成七章：B 的第 1 章「一個模型八個價格」拆成「為什麼有八個價格」（22 秒，鉤子與「你以為…其實…」）和「八格怎麼讀」，因為 lint 要求開場章節不超過 30 秒；快取一章、批次促銷一章、帳單一章、Anthropic 三個數字一章、答案一章依 B。Anthropic 三個數字那章開頭補了一個回顧新聞三個百分比的場景。
- 收尾的下一步：B 指定站內文章〈API 價格比較：每百萬 token 各家多少〉，該文存在（見 c26），但 `source_guide`（brief 與站主指定，沒有改）仍是〈GPT-6 Sol 與 Luna 推出…〉，說明欄第一行由工具依 `source_guide` 自動放那篇。所以：中段 cta（`article-cta`）指向說明欄第一行的來源文章；結尾口播與 outro 卡片講〈API 價格比較〉，並在 `youtube.description` 本文最後一段放它的連結（帶 UTM，格式照 docs/videos/README.md）。這是唯一一處說明欄第一行不等於結尾下一步的地方，請站主確認是否接受，或改 `source_guide`。
- brief 的「表格 5 列 × 3 情境」保留，但把 Claude Sonnet 5 改成 Claude Sonnet 5.5：Sonnet 5.5 在 2026-09-28 發布，價目表已把 Sonnet 5 移到舊版；兩者同價（2／0.20／10），數字沒有變。
- brief 寫「不算長脈絡價格、不算快取寫入、不算 Fast mode；各講一句『另有價格』」。B 的第 1、2、3 章本來就要讀這些格子，所以片中逐格讀了長脈絡、快取寫入、批次與快速模式的官方價格（c2、c3、c4、c5），但每月帳單（第 5 章）仍只算標準價的輸入、快取讀取、輸出三種，並口播與說明欄註明。
- brief 的第 3 章「批次五折與促銷價」的 quote 用 GPT-5.6 Sol 促銷價「至少到 2026-11-21」，本稿改引價目表頁尾原文（c8）；OpenAI 發布文原話不引（該頁本環境回 403，且 2026-09-29 查核已刪）。
- 「40% 少的是任務成本」的說法照 2026-09-29 查核後的措辭（含單價與每任務 token 用量變化，不保證每個人省四成）。
- 加了 brief 沒有的兩件官方事實：GPT-6.1 Sol 於 2026-09-29 上線、旗艦區已換成它，快取讀取只要 0.10（c10）；Anthropic 自己寫快取讀取占代理與寫程式工作成本的大宗（c21）。前者是讀價目表的實際障礙（片中要找 GPT-6 Sol 得展開全部模型），後者與站主「代理型大頭是輸出」的看法並陳，見下。

## 我懷疑但沒動的事

- 站主觀點寫「代理型的帳單大頭是輸出 token，而不是新聞裡強調的快取讀取」，但 Anthropic 公告寫快取讀取占代理與寫程式工作成本的大宗（c21）。本稿把站主的說法限縮為「我這組例子」（Sol 代理用量，快取讀取是輸出的 12 倍，輸出占 54%），並在 anthropic-cache-quote 與 cache-output-ratio 兩個場景把 Anthropic 的說法放在一起，明說兩種都可能對、差在比例。站主若要更強的說法，需要有一組真實用量佐證，請決定。
- 「每月帳單超過 50 美元才值得算」的門檻來自 brief 大綱，不是官方數字，也沒有獨立測試；口播標「我的看法是」。
- `article-cta` 的說明欄第一行文章〈GPT-6 Sol 與 Luna 推出…〉是否已在正式站上線、內容是否如標題，本輪沒有到正式站核對（2026-09-29 查核也標 NOT FOUND）。〈API 價格比較〉同理，且它記的是 2026-09-15 的價格，不含 GPT-6 Sol／Luna；口播與說明欄都說「數字還是回官網對」。
- `openai.com/index/introducing-gpt-6-sol-and-luna/` 本輪沒有嘗試（brief 標明 403）；片中沒有任何數字只靠該頁。「便宜五成」在片中是靠價目表與更新紀錄的四格對半實算，沒有引 OpenAI 自己怎麼說。
- 價格 2026-09-30 當天有效：GPT-5.6 Sol 促銷價至少到 2026-11-21、Gemini 3.8 Flash 促銷價到 2026-12-31；上片前要重查。GPT-6.1 Sol 剛上線，價目表旗艦區的列還可能再動。
- 語音：Sol、Luna、Opus、Sonnet、Flash 在字典裡是 null（照原字唸）；版本號用 `say` 寫成中文（GPT 六、GPT 五點六、GPT 六點一、Opus 五點五、Sonnet 五點五、Gemini 三點八 Flash）。聽稿時請留意 Sol、Luna 有沒有被唸成別的字。

## 進度

- 2026-09-30：video.json 與 claims.md 依選項 B 重寫完成，33 個場景、121 句、7 章；`lint` 0 錯誤 0 警告，估計 9.5 分鐘（實際語速較快，約 8 分鐘）。字典沒有新增（用到的拉丁字詞都已在 `lexicon.json`）。
- 未做：獨立查核（新稿）、旁白試聽、站主對「與企劃不同的地方」的確認。
