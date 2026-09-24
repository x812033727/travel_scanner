# claims — ai-model-choice

一行一個可查核的主張。官方網址都在 2026-09-24（今天）用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重新打開核對過。假設與算法沿用來源文章 `ai-workflow-cost-quality-latency`（查證於 2026-09-18），但旗艦從文章的 Claude Opus 5 換成 Claude Opus 5.5，所以金額和文章不同（見「改用 Opus 5.5 重算」）。

c1｜Claude Opus 5.5 標準價：輸入每百萬 token 4 美元、輸出 20 美元（站主 2026-09-24 決定成本表的旗艦改用 Opus 5.5；原稿用的 Opus 5 是 5／25 美元）｜https://platform.claude.com/docs/en/about-claude/pricing｜2026-09-24｜scene cost-table, cascade-math

c2｜Claude Sonnet 5 標準價：輸入每百萬 token 2 美元、輸出 10 美元｜https://platform.claude.com/docs/en/about-claude/pricing｜2026-09-24｜scene cost-table

c3｜Gemini 3.5 Flash-Lite 付費層標準價：輸入每百萬 token 0.30 美元、輸出 2.50 美元（定價頁 Last updated 2026-09-23 UTC）｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-24｜scene cost-table（含 3c4s）, cascade-math

c4｜gpt-6-astra 標準價（短上下文）：輸入每百萬 token 10 美元、輸出 50 美元｜https://developers.openai.com/api/docs/pricing（舊網址 platform.openai.com/docs/pricing 會 301 轉到這裡）｜2026-09-24｜scene cost-table

c5｜Claude Opus 5.5 於 2026-09-22 發布（型號頁標 Latest、Released September 22, 2026），說明為「For long-running agentic coding and knowledge work」，標準價 4／20 美元；同日起 Claude Opus 5 列在 Legacy models (still available)。Anthropic 頁面沒有用 flagship 稱呼任何型號，陣容最上層是 Claude Fable 5.1（10／50 美元，延遲 Slower）｜https://platform.claude.com/docs/en/models/opus-5-5/overview 、https://platform.claude.com/docs/en/models/overview（舊路徑 about-claude/models/overview 會 307 轉到這裡）｜2026-09-24｜scene opus-5-5

c6｜單一旗艦（1 次 Claude Opus 5.5）在共同假設下一次請求成本 0.012＋0.012＝0.024 美元、每萬次 240 美元｜計算自 c1 ＋ c9 的假設｜2026-09-24｜scene cost-table

c7｜級聯（Gemini 3.5 Flash-Lite 先答，其中 30% 再加 1 次 Claude Opus 5.5）在共同假設下平均一次成本 0.0024＋0.3×0.024＝0.0096 美元、每萬次 96 美元，比單一旗艦省 60%｜計算自 c1 ＋ c3 ＋ c9 ＋ c10｜2026-09-24｜scene cost-table, cascade-math

c8｜並行互審（Claude Opus 5.5 與 gpt-6-astra 同答，Claude Sonnet 5 評審）在共同假設下一次成本 0.024＋0.06＋0.0104＝0.0944 美元、每萬次 944 美元，約為單一旗艦的 3.9 倍；評審那一步 0.0104 美元沿用來源文章的算法，Sonnet 5 價格沒變｜計算自 c1 ＋ c2 ＋ c4 ＋ c9｜2026-09-24｜scene cost-table

c9｜共同假設：一次請求平均輸入 3,000 個 token、輸出 600 個 token｜沿用來源文章 ai-workflow-cost-quality-latency 的示範假設，非官方數字、非量到的真實流量｜2026-09-24｜scene cost-table, cascade-math

c10｜級聯的升級比例假設為 30%｜沿用來源文章 ai-workflow-cost-quality-latency 的示範假設，非官方數字、非量到的真實流量｜2026-09-24｜scene cost-table, cascade-math

c11｜級聯的尾端（p95）延遲可能比單一旗艦更慢，前提是升級會多打一次呼叫、且輕量模型單次回應比旗艦快；來源文章說的是多數請求（p50）較快，不是平均值較快；並行互審每一筆都是「取較慢的一個，再加一次評審」｜沿用來源文章 ai-workflow-cost-quality-latency 的推論，非官方數字、本站沒有實測｜2026-09-24｜scene latency-table（含 md5s）

c12｜MMLU-Pro 是 TIGER-Lab 發布的多學科基準：約 12,000 題、14 個學科、每題 10 個選項；論文摘要說它在「mostly knowledge-driven」的 MMLU 之上加入「more challenging, reasoning-focused questions」，所以字卡不叫它「知識題」；資料集頁連到它自己的公開排行榜｜https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro 、https://arxiv.org/abs/2406.01574｜2026-09-24｜scene mmlu-pro

## 與企劃不同的地方

- 大綱 A 在「為什麼你會困惑」用 Opus 5.5 當「新模型剛上架」的例子；企劃書「示範或實算」段落另外提到 Opus 5.5 標準價比 Opus 5 便宜的發現，但那個發現是選項 C 專屬（brief.md 明寫「只在選項 C 用到，不影響上面主表」）。本片走選項 A，所以只用 Opus 5.5「是最新旗艦、才剛上架」這件事（c5），沒有用它比 Opus 5 便宜的價格比較，避免在旁白或字卡暗示這個選項 A 沒有查證過的價差結論。
- 主表（cost-table 場景）的欄位用「流程／呼叫組成／一次請求／每萬次」四欄，對應企劃書「示範或實算」段落給的簡表；沒有另外放來源文章原表的「標準價」「延遲的形狀」兩欄，那兩項改成獨立的 latency-table 場景與口播說明，字卡才放得下。
- 企劃書第 6 章的畫面清單只寫 `table`、`code`、`diagram` 三個場景；實際腳本在 code 場景（cascade-math）之後、diagram 之前的順序照企劃排列，內容一致，只是每個場景的口播行數比企劃書描述的更多，用來把「示範或實算」段落的假設、算法、換算都講清楚。

## 查核第 1 輪（2026-09-24，見 verify-1.md）

- 3c4s：「輸入輸出都只要幾毛錢等級」與官方價不符（Gemini 3.5 Flash-Lite 輸出每百萬 token 2.50 美元），改成「每百萬 token 輸入只要三毛，輸出兩塊半美元」。
- md5s：來源文章的推論是多數請求（p50）較快，不是平均較快；「平均最快」改成「多數請求最快」。
- latency-table 第三列：並行互審每一筆都要加評審時間，不是只有 p95 才加；改成「兩個取較慢，再加評審／同樣要加一次評審」。
- mmlu-pro.data.sub：「知識題」改成「跨學科難題」（企劃書大綱原本寫「知識題」，官方說明優先）。

## 改用 Opus 5.5 重算（2026-09-24，站主決定）

- 查核第 1 輪指出：成本表的「單一旗艦」其實是 Opus 5，但前兩場把 Opus 5.5 介紹成新型號，觀眾會以為 0.03 美元是 Opus 5.5 的價錢。站主選擇整張表改用 Opus 5.5 重算。
- 金額：單一旗艦 0.024、級聯 0.0096（省 60%）、並行互審 0.0944 美元；口播改成「兩分半」「一分錢」「將近一毛錢」「省了六成」「兩百四十美元／不到一百美元」。
- 圖解改用 `cost-flows.svg`：複製自來源文章的 `diagram-1.svg`，只換三個金額（卡片等寬，不是比例長條）。
- `ne4z` 不再說「新旗艦」：Anthropic 沒有把 Opus 5.5 叫旗艦，陣容最上層是 Fable 5.1。
- 企劃書與站主觀點寫的是「省六成以上」（Opus 5 的 62%）；改算後正好六成，口播照新數字說，企劃書不改，因為大綱核准綁它的雜湊。
- OpenAI 定價頁的來源網址改成轉址後的 `developers.openai.com/api/docs/pricing`，並把 Opus 5.5 的型號頁加進 `sources`。

## 查核第 2 輪（2026-09-24，見 verify-2.md）

- 四個單價在官方頁重新看過：Opus 5.5 4／20、Sonnet 5 2／10、Gemini 3.5 Flash-Lite 0.30／2.50（定價頁 Last updated 2026-09-23 UTC）、gpt-6-astra 短上下文 10／50 美元。c6–c8 的金額照算一遍都對：0.024／240、0.0096／96（正好省 60%）、0.0944／944（約 3.93 倍）。評審那一步 0.0104 來自文章：原始問題 3,000 加兩份回答各 600、共 4,200 個輸入 token，輸出假設 200 個。
- `cost-flows.svg` 的 `<desc>` 還寫「單價查證於 2026 年 9 月 18 日」，那時 Opus 5.5 還沒發布；改成 9 月 24 日。
- c4、c5 的網址換成轉址後的最終網址。
- 上面「我懷疑但沒動的事」第一條說 cost-table 有「貴三倍以上」的口播，現在的 video.json 裡沒有這句；照新金額算是 3.93 倍。

## 我懷疑但沒動的事

- 「並行互審比單一旗艦貴三倍以上」這個講法（cost-table 場景的口播）是 0.1004 美元 ÷ 0.03 美元 ≈ 3.35 倍，直接算出來的比例，不是來源文章白紙黑字寫的倍數（來源文章只寫「是單一旗艦的三倍以上」），但算法一致，沒有另外動它。
- latency-table 場景把「p95」翻成口播「最慢的那百分之五」，這是我自己選的白話講法，來源文章原文只說「p95 是第 95 百分位數」，語意一致但沒有逐字照抄，沒有另外查證這個講法本身。
- MMLU-Pro 的說明（c12）引用的是資料集官方頁面而非某一篇論文，頁面上的介紹文字本身沒有標注查證或發表日期；因為它是穩定的資料集描述而非會過期的價格或版本號，沒有另外去找論文版本核對。

## 進度

- 大綱：選項 A，8 章／17 個場景，已依 brief.md 的章節與版型逐一對應。
- video.json：17 個場景、157 行旁白、2,939 個原始字元，`lint` 0 errors／1 warning（開場鉤子在 250 字／分鐘的保守估計下約 31 秒，超出 30 秒門檻；以頻道實際語速 300 字／分鐘換算約 29.4 秒，在門檻內，判定為估計法造成的警告，不修改內容）。
- 發音字典：新增 `AI`、`Opus`、`MMLU-Pro`、`p95`、`token` 五個詞，已列在 lexicon.json。
- claims.md：12 條可查核主張，全部在 2026-09-24 當天重新打開官方頁核對過。
- 尚未進行：fact-check（verify-1.md，由另一個代理做）、聽眾優先審稿、`tts` 正式合成、`render`、`assemble`、字幕、站主核准與上架。
