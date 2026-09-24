# verify-1 — ai-model-choice（第 1 輪查核，2026-09-24）

查核者：獨立查核代理（不是撰稿者）。對象：`docs/videos/ai-model-choice/video.json`，外加 `claims.md`、`brief.md`（選項 A）。

**方法偏差，請先看：** 這次執行時，環境把本 session 隔離在 `video-gemini` worktree，所以所有 shell 指令（curl、node）和對 `video-skill` 的寫入都被拒絕，`video-gemini` 裡也沒有這支影片的草稿。官方頁面改用 WebFetch 讀取：用的是工具自己的 User-Agent，請求裡沒有任何個人資料。WebFetch 不會印出狀態列，所以「200*」代表頁面內容有回來，非 2xx 回應會直接報錯。Web search 用了 0 次。修正**只是暫存，還沒套用**：修正內容在 `_tools/verify-1-patch.json`，執行 `node <VIDEO_WORKDIR>/ai-model-choice/_tools/apply-verify-1.mjs <ROOT>` 會套用修正，並把這份檔案複製到 `docs/videos/ai-model-choice/verify-1.md`。**lint 沒有跑。**

逐條抽出的清單：`_tools/verify-1-claims.txt`。

## 逐條表

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 新模型幾乎每週上架 | hook.b9ft、three-reasons.items[0]、dzyc、youtube.description | https://ai.google.dev/gemini-api/docs/changelog ；https://platform.claude.com/docs/en/models/opus-5-5/overview | 200* | CONFIRMED：光 Google 的 changelog 就在 08-13、08-26、08-27、09-02、09-03、09-15、09-17、09-22 各有新模型；Anthropic 在 09-22 發布 Opus 5.5 | — |
| 2 | 排行榜跟著（每週）換第一名 | b9ft、description、rup3 | — | — | OUT OF SCOPE：修辭前提，出自站主觀點；沒有官方排行榜能證明「每週換第一名」 | — |
| 3 | Opus 5.5 這個名字、「這幾週」剛上架、才推出沒多久 | opus-5-5.data.text/kicker/sub、ne4z、ce66 | https://platform.claude.com/docs/en/models/opus-5-5/overview | 200* | CONFIRMED：頁面寫「Latest. Released September 22, 2026.」 | — |
| 4 | 把 Opus 5.5 叫「新旗艦」 | ne4z | https://platform.claude.com/docs/en/about-claude/models/overview | 200* | OUT OF SCOPE（用詞）：Anthropic 沒有用 flagship 稱呼任何型號；最上層是 Fable 5.1（10／50 美元，延遲 Slower），Opus 5.5 是「for most workloads」的起點。見「懷疑但沒改」 | — |
| 5 | 幾乎每一家都在更新 | ztd6 | Gemini changelog；Anthropic models overview；https://developers.openai.com/api/docs/pricing（gpt-6 系列） | 200* | CONFIRMED | — |
| 6 | 每次上新款，官方都會說比較聰明、比較便宜 | ixaq | Gemini 定價頁 | 200* | OUT OF SCOPE（修辭）：反例是 Gemini 3.5 Flash-Lite 輸入 0.30 美元，比 3.1 Flash-Lite 的 0.25 美元貴 | — |
| 7 | 同一家分好幾個等級，光旗艦就有好幾代 | three-reasons.items[1]、m4yz | https://platform.claude.com/docs/en/about-claude/pricing | 200* | CONFIRMED：有 Fable／Mythos／Opus／Sonnet／Haiku 五個等級；Opus 5.5、5、4.8、4.7、4.6、4.5 都還有標價 | — |
| 8 | 排行榜分數不代表你的工作 | three-reasons.items[2]、mz8p、myth-compare | — | — | OUT OF SCOPE（觀點，與站主觀點一致） | — |
| 9 | MMLU-Pro 是排行榜常考的題目 | mmlu-pro.data.kicker/text、sb9i | https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro | 200* | CONFIRMED：資料集頁連到它自己的公開排行榜 | — |
| 10 | MMLU-Pro 考很廣的知識、橫跨很多學科、題目很多 | jfv6、b5k7 | 同上；https://arxiv.org/abs/2406.01574 | 200* | CONFIRMED：約 12K 題、14 個學科、每題 10 個選項 | — |
| 11 | MMLU-Pro「考的是知識題」 | mmlu-pro.data.sub | https://arxiv.org/abs/2406.01574 | 200* | CHANGED：論文摘要說它是在「mostly knowledge-driven」的 MMLU 上加入「reasoning-focused questions」 | 考的是知識題，不是你每天的工作 → 考的是跨學科難題，不是你每天的工作 |
| 12 | 旗艦比較慢、單次比較貴；小模型回得快、便宜很多 | question-one-what.data、5vuj、esy5、myth-compare.left | https://platform.claude.com/docs/en/about-claude/models/overview | 200* | CONFIRMED：官方的相對延遲是 Slower／Moderate／Fast／Fastest；單次成本 0.0024 對 0.03 美元，差 12.5 倍 | — |
| 13 | 共同假設：輸入 3,000、輸出 600 個 token | qrhy、jq27、j8hk、description、diagram | 來源文章 `ai-workflow-cost-quality-latency.json` | repo | CONFIRMED（片中有標明是示範假設） | — |
| 14 | 旗艦（Claude Opus 5）5／25 美元 → 一次 0.03、每萬次 300 | cost-table.rows[0]、zi3w、7ake、description、diagram、code | https://platform.claude.com/docs/en/about-claude/pricing | 200* | CONFIRMED：3000×5/1e6 + 600×25/1e6 = 0.03 | — |
| 15 | 小模型（Gemini 3.5 Flash-Lite）0.30／2.50 美元 → 0.0024 | cascade-math.code、pwwg | https://ai.google.dev/gemini-api/docs/pricing | 200* | CONFIRMED（付費層標準價；頁面 Last updated 2026-09-23 UTC），兩次讀取結果一致 | — |
| 16 | 級聯平均 0.0114、每萬次 114 | cost-table.rows[1]、cqc2、7ake、code、caption、description、diagram | 計算 | — | CONFIRMED：0.0009+0.0015=0.0024；0.3×0.03=0.0090；合計 0.0114；×10,000=114 | — |
| 17 | 級聯比一路用旗艦省六成以上 | y3wa、nshw、gixy | 計算 | — | CONFIRMED：1−0.0114/0.03 = 62% | — |
| 18 | gpt-6-astra 標準價、短上下文 10／50 美元 → 0.06 | cost-table.rows[2]（沒寫出來，隱含在數字裡） | https://platform.openai.com/docs/pricing → https://developers.openai.com/api/docs/pricing | 301→200* | CONFIRMED（兩次讀取；長上下文是 20／75 美元） | — |
| 19 | Claude Sonnet 5 2／10 美元；評審輸入 4,200、輸出 200 → 0.0104 | cost-table.rows[2]（隱含） | https://platform.claude.com/docs/en/about-claude/pricing；來源文章 | 200* | CONFIRMED：0.0084+0.002 = 0.0104 | — |
| 20 | 並行互審 0.1004、每萬次 1,004；三次呼叫；大約一毛錢 | cost-table.rows[2]、gr8m、nqci、rnz4、description、diagram | 計算 | — | CONFIRMED：0.03+0.06+0.0104 = 0.1004；×10,000 = 1,004；是單一旗艦的 3.35 倍 | — |
| 21 | 30% 升級比例是假設 | r5g8、description、code | 來源文章 | repo | CONFIRMED（片中有標明是假設） | — |
| 22 | 旗艦官方定價，輸入比輸出便宜很多 | fwvj | Anthropic 定價頁 | 200* | CONFIRMED：5 對 25 美元 | — |
| 23 | 便宜的小模型輸入輸出都只要幾毛錢等級 | 3c4s | Gemini 定價頁 | 200* | CHANGED：輸出是每百萬 token 2.50 美元 | 便宜的小模型，輸入輸出都只要幾毛錢等級。 → 便宜的小模型，每百萬 token 輸入只要三毛，輸出兩塊半美元。 |
| 24 | 有官方的 token 計數工具 | zmm5 | Anthropic 定價頁（連到 token counting endpoint） | 200* | CONFIRMED | — |
| 25 | 金額算到小數點後四位 | 99au | 來源文章 | repo | CONFIRMED（算法說明；0.03 = 0.0300） | — |
| 26 | 2026 年 9 月官方定價頁標準價 | 5ban、cost-diagram.caption、description、sources[].checked_on | 三個定價頁 | 200* | CONFIRMED：checked_on 維持 2026-09-24 | — |
| 27 | 假設來自站上另一篇文章 | 59f5 | 來源文章 | repo | CONFIRMED | — |
| 28 | 延遲：單一旗艦一次呼叫；級聯多數一次、被升級的疊加兩次 | latency-table.rows[0..1]、b3z3、j9je、586z | 來源文章的推論 | repo | CONFIRMED（推論，xj6a 有標明） | — |
| 29 | 並行互審：多數請求 = 兩個取較慢；p95 = 再加評審 | latency-table.rows[2] | 來源文章：「一次並行時間（取較慢的模型）加一次評審時間」 | repo | CHANGED：評審時間每一筆請求都要加，不是只有 p95 才加 | 兩個一起等，取較慢／再加一次評審時間 → 兩個取較慢，再加評審／同樣要加一次評審 |
| 30 | 「平均最快的做法」在最慢時不一定最快 | md5s | 來源文章：「p50 會比一路用旗艦快」 | repo | CHANGED：來源講的是 p50（多數請求），不是平均值；而且投影片標題寫的就是「不是平均值」 | 平均最快的做法… → 多數請求最快的做法… |
| 31 | p95 = 最慢的那百分之五，並標明是推論 | xj6a、latency-table.title | 來源文章 | repo | CONFIRMED（講法偏鬆，見聽眾檢查） | — |
| 32 | 級聯三步：小模型先答、打分數、不夠才升級 | cascade-steps.data、q8jz、afyf、7imm | 來源文章 | repo | CONFIRMED（做法描述；見「懷疑但沒改」） | — |
| 33 | 一天一萬次，一年下來差距非常大 | n74c | 計算 | — | CONFIRMED：(300−114)×365 = 67,890 美元 | — |
| 34 | 完整算式與比較表在說明欄的文章裡 | outro.data.cta、2fhy、2bxn、description | `tools/video/package/metadata.mjs`（`articleUrl` 由 `source_guide` 產生） | repo | CONFIRMED：產生說明欄時會自動附上文章連結 | — |
| 35 | 站主觀點：先分開算三個量／大部分用級聯／並行互審留給輸不起的決定／排行榜換第一名不是換模型的理由 | my-approach-bullets、dz86…b6u2、description | brief.md | — | OUT OF SCOPE（觀點，一致） | — |
| 36 | 標題與縮圖「排行榜第一名不一定適合你」 | youtube.title、thumbnail | — | — | OUT OF SCOPE（觀點） | — |
| 37 | 標籤 | youtube.tags | — | — | OUT OF SCOPE（不是事實主張） | — |

## 摘要

- 查了 37 條：CONFIRMED 26、CHANGED 4（#11、#23、#29、#30）、NOT FOUND 0、OUT OF SCOPE 7。四項修正**已暫存、還沒套用**（環境阻擋，見上）。
- **快過期的事實：** Opus 5.5 在 2026-09-22 發布（型號頁），「這幾週剛上架」過幾週就不成立。Claude Opus 5 從 2026-09-22 起列為「Legacy models (still available)」。Sonnet 5 的 2／10 美元原本是上市優惠價，現已轉為標準價，原定 2026-09-01 漲到 3／15 美元的計畫取消。Gemini 定價頁 Last updated 2026-09-23 UTC。OpenAI 與 Anthropic 定價頁上沒有標日期。
- **觀點不一致：** md5s 原本寫「平均最快」，企劃書寫的是「平均最省」，來源文章寫的是「p50 較快」；已改成「多數請求最快」。mmlu-pro 字卡的「知識題」是企劃書大綱指定的用字，官方說明優先，請站主確認。其餘觀點都有標明（dz86 與說明欄的「我的看法是」），也和站主觀點一致。
- **聽眾檢查（只回報）：** 沒有超過 40 字的句子（改後最長是 3c4s，約 33 字）。沒有查證式旁白、括號或網址。拉丁字母詞 Opus、MMLU-Pro、p95、token、AI 都在 lexicon 裡。question-one-what 的 5vuj 在場景第一句就揭示，但「第一題：做什麼工作」從沒唸出來；latency-table 的 b3z3 也在第一句就揭示，表格前沒有口頭引介。xj6a 的「p95…是我的推論」會讓人以為 p95 本身是推論（真正的推論是級聯的 p95 可能比較慢），而且 p95 是最慢 5% 的門檻值，不是那 5% 本身。afyf 的「答得不夠有把握，才打分數送審」順序顛倒了，應該是分數決定有沒有把握。
- **lint：沒有跑**（node 被擋）。套用修正後要跑 `node <ROOT>/tools/video/cli.mjs lint --slug ai-model-choice`。修正前是 0 errors、1 warning（開場約 31 秒）。
- **懷疑但沒改：** (1) 成本表的「單一旗艦」其實是 Claude Opus 5（現已是 legacy），但片中從沒說出型號，而且兩個場景前才把 Opus 5.5（4／20 美元）介紹成新旗艦。觀眾很可能以為 0.03 美元是 Opus 5.5 的價錢；換成 Opus 5.5，單一旗艦是 0.024 美元、級聯是 0.0096 美元。要不要改由站主決定（企劃書選了 A）。(2) 四個計價型號在旁白、字卡、說明欄都沒出現，觀眾自己算不出這些數字。(3) Anthropic 沒有把 Opus 5.5 叫做 flagship。(4) 級聯成本沒有算打分數那一步的費用（與來源文章相同）。(5) sources[2] 的網址會 301 轉到 developers.openai.com/api/docs/pricing；sources 裡也沒有 MMLU-Pro 與 Opus 5.5 型號頁。(6) wkwi 說「幾乎可以忽略」，但小模型的費用佔旗艦的 8%、佔級聯平均的 21%。
- **需要第二輪：是。** 本輪有 4 項事實修正（超過 3 項）；而且修正還沒套用、lint 也還沒跑，所以這份稿子目前**不算已查證**。
