# verify-2 — ai-model-choice（第 2 輪查核，2026-09-24）

查核者：獨立查核代理，沒有寫這份稿子，也沒有做第 1 輪。查核對象是 `docs/videos/ai-model-choice/` 裡的 `video.json`、`claims.md`、`cost-flows.svg`，對照 `brief.md`、`verify-1.md`，以及來源文章 `apps/api/app/guides/content/ai-workflow-cost-quality-latency.json`（zh-TW）。

**方法：** 官方頁面一律用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 抓取，同一主機的兩次請求至少間隔 1.2 秒。抓回來先剝掉 `<!-- -->` 註解，再轉成純文字閱讀。請求裡沒有任何人的個人資料，Web search 用了 0 次。第三方網頁一律不拿來確認數字。輔助腳本、抓回的頁面和狀態碼紀錄都在 `<VIDEO_WORKDIR>/ai-model-choice/_tools/round2/`：`fetch.sh`、`pages/status.tsv`、`recompute.mjs`、`oldnums.mjs`、`listener.mjs`、`svgdiff.mjs`、`pick.mjs`。

**第 1 輪確認過的主張，抽查三分之一：** 從 26 條 CONFIRMED 用 `crypto.randomInt` 隨機抽 9 條，抽中 #9、#15、#16、#18、#24、#25、#27、#33、#34（見 `picked.txt`）。其中 #15、#16、#18、#33 剛好落在 Opus 5.5 重算的範圍，併入下表 #1、#13、#8、#21 一起查。另外 #10、#28、#31 碰到第 1 輪改過的場景，也一起重查了。

## 逐條表

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 便宜的小模型（Gemini 3.5 Flash-Lite）每百萬 token 輸入 0.30、輸出 2.50 美元；一次 0.0024 美元（第 1 輪改過；抽中 #15） | 3c4s、cascade-math.code、pwwg | https://ai.google.dev/gemini-api/docs/pricing | 200 | CONFIRMED：付費層 Standard，輸入「$0.30 (text / image / video / audio)」，輸出「$2.50」，而且輸出價含 thinking token；頁面 Last updated 2026-09-23 UTC | — |
| 2 | 多數請求最快的做法，最慢時不一定最快（第 1 輪改過） | md5s | 來源文章 | repo | CONFIRMED：文章寫的是級聯「p50 會比一路用旗艦快」、「p95 反而可能比單一旗艦更慢」；並行互審的 p50 要取兩個裡較慢的一個再加一次評審，所以多數請求最快的是級聯 | — |
| 3 | 並行互審：兩個取較慢，再加評審／同樣要加一次評審（第 1 輪改過） | latency-table.rows[2]、gnsn | 來源文章 | repo | CONFIRMED：文章原句是「一次並行時間（取較慢的模型）加一次評審時間」，每一筆請求都要加 | — |
| 4 | MMLU-Pro「考的是跨學科難題」（第 1 輪改過） | mmlu-pro.data.sub | https://arxiv.org/abs/2406.01574 ；https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro | 200；200 | CONFIRMED：論文摘要寫它在「mostly knowledge-driven」的 MMLU 上加入「more challenging, reasoning-focused questions」；資料集頁寫「12K complex questions across various disciplines」 | — |
| 5 | MMLU-Pro 題目多、學科廣（第 1 輪 #10，因同場景改過而重查） | jfv6、b5k7 | 同上 | 200 | CONFIRMED：test split 有 12,032 列；學科表 14 列；每題「typically has ten」個選項 | — |
| 6 | Claude Opus 5.5 標準價 4／20 美元（c1） | cost-table.rows[0]、cascade-math.code、description、cost-diagram.caption | https://platform.claude.com/docs/en/about-claude/pricing ；https://platform.claude.com/docs/en/models/opus-5-5/overview | 200；200 | CONFIRMED：定價表寫「$4 / MTok」「$20 / MTok」；型號頁寫「priced at $4 / $20 USD per million input / output tokens」 | — |
| 7 | Claude Sonnet 5 標準價 2／10 美元（c2） | cost-table.rows[2]（隱含）、description | https://platform.claude.com/docs/en/about-claude/pricing | 200 | CONFIRMED | — |
| 8 | gpt-6-astra 標準價，短上下文 10／50 美元（c4；抽中 #18） | cost-table.rows[2]（隱含）、description | https://developers.openai.com/api/docs/pricing （舊網址 platform.openai.com/docs/pricing 回 301 轉到這裡） | 200 | CONFIRMED：Standard 表的短上下文欄是輸入 $10.00、輸出 $50.00；長上下文是 $20.00／$75.00 | — |
| 9 | 一次請求輸入 3,000、輸出 600 個 token，是示範假設（c9） | qrhy、jq27、j8hk、description、svg | 來源文章 | repo | CONFIRMED：文章寫「這組數字是示範用的假設，不是量到的真實流量」 | — |
| 10 | 升級比例 30%，是示範假設（c10） | r5g8、cascade-math.code、description | 來源文章 | repo | CONFIRMED | — |
| 11 | 單一旗艦一次 0.024 美元、每萬次 240 美元（c6） | cost-table.rows[0]、cost-flows.svg、description | 計算 | — | CONFIRMED：見下方算式 | — |
| 12 | 「一次大約兩分半美金」 | zi3w | 計算 | — | CONFIRMED（四捨五入）：0.024 美元是 2.4 美分，以半分為單位取整就是兩分半，「大約」這個說法成立；聽感問題見聽眾檢查 | — |
| 13 | 級聯平均一次 0.0096 美元、每萬次 96 美元，以及 code 字卡的三段算式（c7；抽中 #16，第 1 輪的 0.0114 已由站主改掉） | cost-table.rows[1]、cascade-math.code／caption、cost-flows.svg、description | 計算 | — | CONFIRMED：0.0024 + 0.3 × 0.024 = 0.0096；code 字卡 highlight [7] 標的正是 `cascade_avg` 那一行 | — |
| 14 | 「級聯平均下來，大約一分錢」 | cqc2 | 計算 | — | CONFIRMED：0.96 美分 | — |
| 15 | 級聯比一路用旗艦省六成 | y3wa、nshw、gixy | 計算 | — | CONFIRMED：1 − 0.0096 ÷ 0.024 = 60.00%，正好六成 | — |
| 16 | 「單一旗艦要兩百四十美元，級聯不到一百美元」 | 7ake | 計算 | — | CONFIRMED：240、96 | — |
| 17 | 評審那一步 0.0104 美元 | cost-table.rows[2]（隱含）、claims c8 | 來源文章；Anthropic 定價頁 | repo；200 | CONFIRMED：文章寫評審讀「3,000 加 600 加 600、等於 4,200 個 token，輸出假設 200 個」，用 Sonnet 5 的 2／10 美元計價。旗艦換成 Opus 5.5 以後，兩份回答仍假設各 600 個 token，所以 4,200 不變 | — |
| 18 | 並行互審一次 0.0944 美元、每萬次 944 美元（c8） | cost-table.rows[2]、cost-flows.svg、description | 計算 | — | CONFIRMED：0.024 + 0.06 + 0.0104 = 0.0944，是單一旗艦的 3.93 倍 | — |
| 19 | 「並行互審要三次呼叫，將近一毛錢」 | gr8m | 計算 | — | CONFIRMED：9.44 美分，比 10 美分少，「將近」成立 | — |
| 20 | 旗艦的官方定價，輸入比輸出便宜很多 | fwvj | Anthropic 定價頁 | 200 | CONFIRMED：Opus 5.5 輸入 4 美元，輸出 20 美元，差 5 倍 | — |
| 21 | 一天一萬次，一年差距非常大（抽中 #33） | n74c | 計算 | — | CONFIRMED：(0.024 − 0.0096) × 10,000 × 365 = 52,560 美元 | — |
| 22 | 價格是 2026 年 9 月官方定價頁的標準價，旗艦以 Claude Opus 5.5 計 | 5ban、cost-diagram.caption、description | 三個定價頁 | 200 | CONFIRMED | — |
| 23 | 圖解只換了三個金額 | cost-flows.svg、assets[0].source | `apps/web/public/guides/ai-workflow-cost-quality-latency/diagram-1.svg` | repo | CONFIRMED：逐段比對 41 段，只有 #20、#28、#36 三段不同，分別是 0.03→0.024、0.0114→0.0096、0.1004→0.0944 | — |
| 24 | 圖解的 `<desc>` 寫單價查證於 2026 年 9 月 18 日 | cost-flows.svg `<desc>` | https://platform.claude.com/docs/en/models/opus-5-5/overview | 200 | CHANGED：Opus 5.5 在 2026-09-22 才發布，9 月 18 日不可能查到它的價格；這段是從文章圖解原封不動抄來的 | 單價查證於 2026 年 9 月 18 日官方定價頁的標準價 → 單價查證於 2026 年 9 月 24 日官方定價頁的標準價 |
| 25 | `sources` 四個網址與 checked_on | video.json sources | 四個網址都直接回 200 | 200 | CONFIRMED：checked_on 維持 2026-09-24，也就是今天 | — |
| 26 | 「這幾週，又有一個新的大型模型剛上架」（item 3，改過） | ne4z | https://platform.claude.com/docs/en/models/opus-5-5/overview | 200 | CONFIRMED：頁面寫「Released September 22, 2026」、狀態「Active (latest)」；這句已經不再稱它為旗艦 | — |
| 27 | 型號叫 Opus 5.5、才上架沒多久 | ce66、opus-5-5.data | 同上 | 200 | CONFIRMED | — |
| 28 | 小模型的價錢跟旗艦比「幾乎可以忽略」／「幾乎不用什麼錢」 | wkwi、pwwg | 計算 | — | OUT OF SCOPE（屬於判斷）：現在小模型每次花費是旗艦的 10%，占級聯平均的 25%（第 1 輪時是 8%／21%）。見「懷疑但沒改」 | — |
| 29 | MMLU-Pro 是排行榜常考的題目（抽中 #9） | mmlu-pro.data.kicker、sb9i | https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro | 200 | CONFIRMED：資料集頁有 Leaderboard 連結，2026.03.11 還更新過一次排行榜 | — |
| 30 | 有官方的 token 計數工具（抽中 #24） | zmm5 | https://platform.claude.com/docs/en/about-claude/pricing | 200 | CONFIRMED：頁面寫「you can estimate it in advance with the token counting endpoint」 | — |
| 31 | 金額算到小數點後四位（抽中 #25） | 99au | 計算 | — | CONFIRMED：0.024（等於 0.0240）、0.0096、0.0944 | — |
| 32 | 假設來自站上另一篇文章（抽中 #27） | 59f5 | 來源文章 | repo | CONFIRMED | — |
| 33 | 完整算式與比較表在說明欄的文章裡（抽中 #34） | 2fhy、2bxn、outro.data.cta、description | `tools/video/core/metadata.mjs`：`composeDescription` 會附上由 `source_guide` 產生的 `articleUrl`；來源文章 | repo | CONFIRMED（就字面而言）：連結會附上，文章裡也有算式和比較表。**但文章的表仍用 Claude Opus 5 計算**（0.03／0.0114／0.1004、少 62%、查證於 9 月 18 日），和影片的數字對不起來。這要站主決定怎麼處理，見「懷疑但沒改」第 1 條 | — |

## 重算（單價皆為 2026-09-24 官方頁所見）

```
單一旗艦 Opus 5.5：3,000 × 4 ÷ 1,000,000 = 0.012
                    600 × 20 ÷ 1,000,000 = 0.012
                    0.012 + 0.012 = 0.024 美元；× 10,000 = 240 美元
小模型 Flash-Lite：  3,000 × 0.30 ÷ 1,000,000 = 0.0009
                    600 × 2.50 ÷ 1,000,000 = 0.0015
                    0.0009 + 0.0015 = 0.0024 美元
級聯：              0.30 × 0.024 = 0.0072
                    0.0024 + 0.0072 = 0.0096 美元；× 10,000 = 96 美元
                    1 − 0.0096 ÷ 0.024 = 0.60 → 省 60%
gpt-6-astra：       3,000 × 10 ÷ 1,000,000 + 600 × 50 ÷ 1,000,000 = 0.03 + 0.03 = 0.06
評審 Sonnet 5：     輸入 = 3,000（原始問題）+ 600 + 600（兩份回答）= 4,200；輸出假設 200
                    4,200 × 2 ÷ 1,000,000 + 200 × 10 ÷ 1,000,000 = 0.0084 + 0.0020 = 0.0104
並行互審：          0.024 + 0.06 + 0.0104 = 0.0944 美元；× 10,000 = 944 美元
                    0.0944 ÷ 0.024 = 3.93 倍
一年差距（每天一萬次）：(0.024 − 0.0096) × 10,000 × 365 = 52,560 美元
口播取整：          兩分半 ≈ 2.4 美分；一分錢 ≈ 0.96 美分；將近一毛錢 = 9.44 美分 < 10；
                    六成 = 60.00%；兩百四十 = 240；不到一百 = 96
```

評審步驟的假設：評審要讀原始問題與兩份回答，輸入是 3,000 + 600 + 600 = 4,200 個 token，輸出假設 200 個。這是來源文章自己寫的假設（並行互審那一段），不是官方數字。旗艦換成 Opus 5.5 以後，兩份回答仍照共同假設各 600 個 token，所以這一步維持 0.0104 美元。文章支持這個數字。

## 摘要

- **查了 33 條：** CONFIRMED 31、CHANGED 1（#24）、NOT FOUND 0、OUT OF SCOPE 1（#28）。第 1 輪改過的四條（3c4s、md5s、latency 第三列、MMLU-Pro 字卡）全部維持。Opus 5.5 重算的每一個數字，我都從今天官方頁上的單價重算過，全部對得上。
- **舊數字：** `video.json` 和 `cost-flows.svg` 裡都找不到 0.03、0.0114、0.1004、300、114、1,004、62%、「六成以上」、「三分錢」（`oldnums.mjs` 只命中 3000 的子字串和 SVG 座標）。唯一留下的舊資訊是 SVG `<desc>` 裡「9 月 18 日」這個查證日期，已改成 9 月 24 日。
- **本輪修改：** 事實修正只有 1 處，就是 cost-flows.svg 的 `<desc>` 日期。`video.json` 沒有動。`claims.md` 有三處更新：開頭一句（原本寫「與來源文章一致」，實際上旗艦已換掉）、c4 與 c5 的網址換成轉址後的最終網址，並新增「查核第 2 輪」一節。
- **快過期的事實：** Opus 5.5 發布日是 2026-09-22，所以「這幾週剛上架」「才推出沒多久」只能再撐幾週，上架前請確認。Gemini 定價頁 Last updated 2026-09-23 UTC。Anthropic 和 OpenAI 的定價頁沒有標日期。
- **聽眾檢查（只回報，沒改）：** 沒有超過 40 字的句子（最長是 3c4s，32 字），沒有查證式旁白、括號或網址，也沒有 `say` 欄位。拉丁字母詞 Opus、MMLU-Pro、p95、token、AI 都在 lexicon 裡。(1) zi3w 的「兩分半」在台灣口語裡第一個聯想是「兩分三十秒」，而且這句緊接在延遲那一章之後；另外這是全片唯一說「美金」的地方，其他地方都說「美元」。(2) b5k7 的「蓋的學科」像是漏了「涵」字。(3) xj6a 還是說「最慢的那百分之五叫 p95」，但 p95 其實是那個門檻值（第 1 輪已報告）。(4) 5vuj 與 b3z3 在場景的第一句就揭示，前面沒有先唸出標題（第 1 輪已報告）。
- **lint：** 改完之後 `node tools/video/cli.mjs lint --slug ai-model-choice` 的結果是 0 errors、1 warning（開場約 31 秒，和改之前相同）。
- **懷疑但沒改：**
  1. **說明欄文章的數字對不起來（上架前要決定）。** 2fhy、2bxn、outro 的 cta 和說明欄都說完整算式與比較表在文章裡，但文章的表還是 Claude Opus 5 的 0.03／0.0114／0.1004 美元、少 62%，查證日也是 9 月 18 日。觀眾照影片說的去對照，會看到另一組數字。文章不在我能改的範圍，要在口播裡解釋又得加新的一句，所以沒動。建議二選一：一是透過 content-pipeline 把文章的成本段改成 Opus 5.5（Opus 5 在定價頁已經移到 Additional models）；二是在說明欄加一句「文章的表以 Claude Opus 5 計算，算法相同」。
  2. Opus 5.5 的型號頁寫「Adaptive thinking is always on and can't be turned off」。如果 thinking token 也按輸出計價（Gemini 定價頁明寫輸出價含 thinking token；Anthropic 定價頁沒寫，我也沒去查 thinking 的文件），那 600 個輸出 token 這個假設用在 Opus 5.5 上，會比用在文章的 Opus 5 上更樂觀。片中已經標明 600 是示範假設，所以沒改。
  3. Anthropic 定價頁寫，Claude 4.7 以後的 tokenizer 處理同一段文字「approximately 30% more tokens」。也就是說，「每個模型都是 3,000／600 個 token」只是方便比較的簡化。
  4. 成本表仍把 Opus 5.5 標成「單一旗艦」，但 Anthropic 陣容的最上層是 Fable 5.1（10／50 美元）；官方的說法是「start with Claude Opus 5.5 for most workloads」。這是流程裡的角色名稱，不是在說它是官方的旗艦，所以沒改。
  5. wkwi 說小模型的費用「幾乎可以忽略」，但它占級聯平均的 25%。如果觀眾自己的升級比例更低，這個占比還會更高。
  6. 企劃書與站主觀點寫的是「省六成以上」，照新金額算是正好六成。企劃書不能改，撰稿者已經記錄這件事。
  7. `sources` 裡沒有 MMLU-Pro 的資料集頁和論文。
- **需要第三輪：不需要。** 本輪只有 1 處事實修正（沒有超過 3 處），而且這處只在不會顯示出來的 SVG `<desc>` 裡。但如果站主為了第 1 條改了 2fhy、2bxn、cta 或說明欄，改過的那幾句要再查一次。
