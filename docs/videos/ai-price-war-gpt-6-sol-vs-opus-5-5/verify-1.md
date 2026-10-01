# verify r1 — ai-price-war-gpt-6-sol-vs-opus-5-5（2026-09-30，選項 B 重寫稿）

獨立查核第 1 輪，對象是 2026-09-30 依選項 B 重寫的 `video.json`（33 場景、121 句）。舊報告（`verify-1.md`、`verify-p1-20260929*.md`）查的是舊稿，本輪不沿用其結論；每個說法都在 2026-09-30 以編輯用 User-Agent 重開官方頁。抽出的說法清單與原始頁面存在 `mokaair-work/videos/ai-price-war-gpt-6-sol-vs-opus-5-5/_tools/verify-r1/`（`claim-list-source.txt`、`*.html`、`oai-pricing.md`、`arith.py`）。

## 來源與 HTTP 狀態

| 代號 | URL | HTTP |
| --- | --- | --- |
| P | https://developers.openai.com/api/docs/pricing（platform.openai.com/docs/pricing 轉址到此；`.md` 版同樣 200） | 200 |
| CL | https://developers.openai.com/api/docs/changelog | 200 |
| PC | https://developers.openai.com/api/docs/guides/prompt-caching | 200 |
| B | https://developers.openai.com/api/docs/guides/batch | 200 |
| OA | https://openai.com/index/introducing-gpt-6-sol-and-luna/ | 200（本日可讀） |
| O55 | https://www.anthropic.com/claude-opus-5-5 | 200 |
| S55 | https://www.anthropic.com/claude-sonnet-5-5 | 200 |
| CP | https://claude.com/pricing | 200 |
| G | https://ai.google.dev/gemini-api/docs/pricing | 200 |
| ART | repo `apps/api/app/guides/content/ai-api-pricing-comparison-2026.json`；正式站 /zh-TW/life/ai-api-pricing-comparison-2026 | 200 |

## 說法表

| # | 說法 | 位置 | 來源 | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- |
| 1 | GPT-6 Sol 標準頁有八個價格（4 種 token × 短／長脈絡） | ki36, pc4t, eight-prices, you-think, 說明欄 | P | CONFIRMED | |
| 2 | 短脈絡 ≤272K 輸入 token，超過為長脈絡（27 萬 2 千） | ippg, context-split | P「Short context: ≤272K input tokens」 | CONFIRMED | |
| 3 | GPT-6 Sol 短 2／0.20／2.50／10、長 4／0.40／5／15 | sol-table, qjec–ja6c | P、CL | CONFIRMED | |
| 4 | 一個輸入 token 只算成輸入、快取讀取、快取寫入其中一種 | 6kug | P 表頭 tooltip「Input tokens are either Input, Cached Input, or Cache Write and writes are not an additive fee」 | CONFIRMED | |
| 5 | 輸出含看不見的思考 token | b3y9, four-tokens | P 表頭 tooltip「Output prices include … reasoning tokens」 | CONFIRMED | |
| 6 | 快取寫入 1.25 倍、讀取 0.1 倍；寫一次讀九次 2.15 倍對 10 倍 | cache-math, 4by8–spkw | PC | CONFIRMED | |
| 7 | 快取寫入 $2.50 > 輸入 $2，白付兩成五 | write-costs-more | P、PC | CONFIRMED | |
| 8 | 快取要前綴相同、至少 1,024 token、會過期、不保證命中 | cache-conditions | PC（GPT-5.6 及之後 1,024；「not stored indefinitely」；「doesn’t guarantee a cache hit」） | CONFIRMED | |
| 9 | 價目表分頁；批次頁 Sol 1／5，剛好對折；24 小時內完成 | batch-half, kex8–x5cg | P（Standard／Batch／Flex／Fast／Ultrafast 分頁）、B「50% cost discount」「completes within 24 hours」 | CONFIRMED | |
| 10 | 快速模式是標準價兩倍，Sol 輸出 20 | other-tabs, eniv | P Fast：gpt-6-sol 4／0.40／5／20 | CONFIRMED | |
| 11 | GPT-5.6 Sol 促銷價「at least through November 21, 2026」原文 | promo-quote, v74j | P | CONFIRMED | |
| 12 | 註記的位置：「頁面最下面」「頁尾」 | gb49, promo-quote.data.kicker/source | P：註記在旗艦模型表格正下方，下面還有 Cyber、多模態、影像等區塊 | CHANGED | 「再往頁面最下面看」→「再往表格下面看」；kicker「價目表頁尾小字」→「價目表旗艦表格下方小字」；source「頁尾註記」→「旗艦模型表格下方註記」；claims c8 同步 |
| 13 | GPT-5.6 Sol 短 4／0.40／5／20，GPT-6 Sol 四格剛好一半 | half-of-promo, ym8g–ef3k | P | CONFIRMED（四格都精確 50%） | |
| 14 | 新聞的五成是跟 GPT-5.6 促銷價比 | tuik, news-three-numbers, 86x9 | OA「reducing API prices for Sol and Luna by 50% compared with their GPT‑5.6 promotional pricing」 | CONFIRMED | |
| 15 | GPT-6.1 Sol 2026-09-29 上線，2／0.10／2.50／10；旗艦區換成它，GPT-6 Sol 要展開全部模型 | sol-61, ntee–2djf | CL（Sep 29 條目原文列四價）、P（預設列 astra、6.1-sol、luna，gpt-6-sol 在「All models」內） | CONFIRMED | |
| 16 | GPT-6 Sol 快取讀取註「九月二十二日」 | sol-61.data | CL Sep 22 | CONFIRMED | |
| 17 | 三種示範用量 | scenario-walk | 撰稿自訂（示範） | OUT OF SCOPE（非事實） | |
| 18 | 15 格帳單：Sol 20／73.6／500；Luna 1／3.68／25；Opus 5.5 40／137.6／1,000；Sonnet 5.5 20／73.6／500；Gemini 3.8 Flash 7.5／27.6／187.5 | monthly-bill, hjxw | 單價 P、CP、O55、S55、G；`arith.py` 以分數重算 | CONFIRMED（15 格全對） | |
| 19 | Luna 聊天型一個月一塊 | bazf | 同上 | CONFIRMED | |
| 20 | Opus 5.5 聊天與大量整理剛好是 Sol 兩倍 | vpac | 40／20、1,000／500 | CONFIRMED | |
| 21 | Sonnet 5.5 與 Sol 同單價、三格同帳單；以 Sonnet 5.5 取代 brief 的 Sonnet 5 | e9gz, monthly-bill | S55「priced the same as Sonnet 5 at $2 … $10 … $0.20」（2026-09-28）；CP 主表 Sonnet 5.5 2／10／0.20／寫入 2.50，Sonnet 5 已在 Legacy | CONFIRMED | |
| 22 | Gemini 3.8 Flash 0.75／0.075／3.75 為促銷價，年底後翻倍 | 6jr2 | G「through December 31, 2026」，2027-01-01 起 1.50／0.15／7.50 | CONFIRMED | |
| 23 | 三種用量最便宜都是 Luna；Gemini 介於中間 | yvvp, 6jr2 | 實算 | CONFIRMED | |
| 24 | 聊天型 GPT-5.6 Sol 促銷價 40 → GPT-6 Sol 20，剛好一半 | compare-to-last-gen, jeek | 5×4＋1×20＝40 | CONFIRMED | |
| 25 | 代理型 Opus 5 184 → Opus 5.5 137.6，少約 25% | kqwi, 6kqy | CP Legacy：Opus 5 5／0.50／25；12×5＋48×0.5＋4×25＝184；1−137.6/184＝25.2% | CONFIRMED | |
| 26 | 代理型 Sol 73.6 中輸出 40（54%），快取讀取 9.6（13%） | output-share, kdtw, rfmv | 實算 54.35%、13.04% | CONFIRMED | |
| 27 | Anthropic 原文「make up the majority of agentic and coding work costs」 | anthropic-cache-quote | O55「Cache reads (which make up the majority of agentic and coding work costs)」 | CONFIRMED（逐字） | |
| 28 | 快取讀取是輸出的 12 倍（4,800 萬對 400 萬） | cache-output-ratio | 實算 | CONFIRMED | |
| 29 | 9 月 22 日兩家同一天發布 | x5eq, news-three-numbers.source | CL Sep 22、OA「September 22, 2026」、O55「September 22, 2026」 | CONFIRMED | |
| 30 | Opus 5.5「40% less to run than Opus 5」，預設設定、一般工作負載下的估計，含每任務 token 變少 | anthropic-quote, dz5g, vnit, hcrz, gxii | O55「costs 40% less to run」「at default settings … on typical workloads」「costs less per token … and uses fewer tokens per task, which nets out to a 40% drop」 | CONFIRMED | |
| 31 | 輸入輸出 5→4、25→20 少兩成；快取讀取 0.50→0.20 少六成 | real-list-cut, cut-buckets, tq5v | O55 價格表與內文；CP | CONFIRMED | |
| 32 | Opus 5.5 4／0.20／20，寫入 5 | monthly-bill | CP、O55 | CONFIRMED | |
| 33 | 聊天型 Sol 換 Luna 每月省 19 | thirty-dollar-case, bxsk | 20−1 | CONFIRMED | |
| 34 | 結尾〈API 價格比較〉在站上 | wrap, y3mp, 說明欄 | ART：repo 與正式站都在（200），標題相符；記的是 2026-09-15 各家標準價（gpt-6-astra、gpt-5.6-terra／sol／luna、Fable 5.1、Opus 5、Sonnet 5、Haiku 4.5、gemini-3.8-flash 等），沒有 GPT-6 Sol、Luna、Opus 5.5、Sonnet 5.5 | CONFIRMED（說明欄已註「九月中旬」，口播說「數字還是回官網對」） | |
| 35 | 中段 cta 的來源文章〈GPT-6 Sol 與 Luna 推出…〉 | article-cta | 正式站 /zh-TW/life/ai-news-gpt-6-sol-luna-20260923 200，標題相符 | CONFIRMED | |
| 36 | 標題、縮圖、標籤 | youtube, thumbnail | 以上各項 | CONFIRMED | |

## 摘要

- 說法 36 項：確認 34、更正 1（#12 促銷價註記的位置）、查無 0、範圍外 1（#17 示範用量）。事實更正 1 項，未達第二輪門檻。
- 會過期：GPT-5.6 Sol 促銷價「at least through November 21, 2026」（沒有固定結束日）；Gemini 3.8 Flash 促銷價到 2026-12-31，2027-01-01 起翻倍；GPT-6.1 Sol 2026-09-29 才上線，旗艦區與 gpt-6-sol 的位置還可能再動（下架時 sol-61 與整張表都要重看）；Opus 5 與 Sonnet 5 目前只在 Legacy 區。上片前重查這四項。
- 站主觀點：chase-new（立場 6）、switch-or-not、thirty-dollar-case、ycu2 都標了「我的看法」或在同場景有標記，也與 brief 相符。不相符的一處：brief 說「代理型的帳單大頭是輸出 token，而不是新聞裡強調的快取讀取」，片中沒有把它當看法講出來，改成本片示範用量的實算（54%），並放上 Anthropic 原文、說「兩種都可能對」。這比 brief 弱，但官方原文與 brief 衝突，依規則以官方為準，現在的處理是對的；要不要保留更強的說法由站主決定。
- 補充數字給站主判斷：以 GPT-6 Sol 的價，快取讀取 token 要超過輸出的 50 倍（10 ÷ 0.20）費用才會超過輸出；Opus 5.5 要 100 倍（20 ÷ 0.20）。本片示範是 12 倍；長時間的寫程式代理常見更高的比例，所以示範用量的選擇會決定結論。
- 聽眾檢查：沒有超過 40 字的句子、沒有查證用語、沒有括號或網址；拉丁字詞都在字典裡；揭示順序沒有問題。小提醒：thirty-dollar-case 問的是「帳單 30 美元」，答案卻用聊天型那格（Sol 20 美元）算，聽起來數字對不上（brief 就是這樣設計，未改）。
- lint：更正後 `0 errors, 0 warnings`（估計 9.5 分鐘、121 句）。
- 懷疑但沒動：wrap 的「價目表在站上〈API 價格比較〉那篇」──那篇沒有片中五個模型裡的四個（只有 Gemini 3.8 Flash），口播已說回官網對，但站主可考慮改成只說「各家比較」；GPT-6 Luna 的「五成」只對輸入與快取成立（輸出 1.20→0.50 少 58%），片中沒提 Luna 降幅，所以不影響。
- 第二輪：不需要（事實更正 1 項，≤ 3）。
