# 查核紀錄 1：ai-term-chain-of-thought

查核者不是撰稿者。查核日 2026-10-03。所有請求用 `curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。
五篇論文都讀了 arXiv abs 頁，也下載 `https://arxiv.org/pdf/<id>`，用 pdftotext 讀全文；四個官方文件頁與 Anthropic 研究頁都抽出 HTML 文字來讀。
十筆 `sources` 今天都回 200，沒有轉址，標題與頁面相符，內容不是空殼。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

- 「準確率最多下降 36%（零樣本思維鏈、附建議答案的設定）」→「在線索指向錯誤答案的題目上，準確率最多下降約 36 個百分點（零樣本思維鏈、附建議答案的設定）」｜論文的 −36.3% 是兩個準確率相減（無偏向 59.6% 減有偏向 23.3%），單位是百分點，不是相對下降 36%；而且指標只計偏向線索指向錯誤答案的題目（Metrics 一節），原句沒寫這個設定｜https://arxiv.org/abs/2305.04388（PDF 第 3.1–3.2 節）
- 「只需一步的簡單題進步很小」→「只需一步的簡單題，進步很小，有的模型甚至略為退步」；結尾段「Wei 等人觀察到的進步很小」→「進步很小甚至退步」｜論文原文是「performance improvements were either negative or very small」；附錄 Table 3 的 SingleOp 有負值（例如 175B 的 GPT 從 90.9 降到 88.8）｜https://arxiv.org/abs/2201.11903（PDF 第 3.2 節、附錄 Table 3）
- 「內建思考關閉時，仍可手動要求逐步思考。」→ 後面加上「但文件也註明，部分較新的模型應改靠內建思考，要求在回覆裡寫出推理可能被婉拒。」｜今天的 Anthropic 指南在「Manual chain-of-thought (CoT) prompting as a fallback」這一條寫明：某些較新的模型應「rely on thinking instead」，而且要求模型寫出推理（例如寫在 `<thinking>` 標籤裡）的提示「may be declined」。原句只寫可以手動要求，少了這個條件（正文仍不寫型號）｜https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- （措辭，不計入）「不加提示約 17.7%」→「不加這句時約 17.7%」｜Kojima 的基線仍然有提示和答案觸發句，只是少了「Let's think step by step」｜https://arxiv.org/abs/2205.11916（Table 4）
- （措辭，不計入）「偷偷加入偏向某答案的線索」→「刻意加入」｜「建議答案」這種線索是明寫在提示裡的，並不是偷偷放的｜https://arxiv.org/abs/2305.04388
- （措辭，不計入）「不提供原始推理 token，只提供摘要」→「只能另外要求推理摘要」｜OpenAI 文件說摘要要用 `summary` 參數主動開啟，預設不附｜https://developers.openai.com/api/docs/guides/reasoning
- （措辭，不計入）「卻不能當成模型實際原因的證據」→「卻不能直接當成模型實際原因的證明」｜Lanham 等人認為在合適的模型與任務下 CoT 可以忠實，所以措辭不宜寫成完全不能當證據｜https://arxiv.org/abs/2307.13702

改完後正文字數以 `_body_length` 計為 2,579（原本 2,499），仍在 1,800–3,000 之內。結構沒變：5 個 H2、1 個表、1 個 callout，指派的 5 個站內連結都在。
`research.json` 的 `running_text_characters` 還寫 2,499；這次指派只准我寫 pack.json、diagram-1.svg 與本檔，所以沒有改它。

## 查過、沒問題的主要主張

- 圖上的數字（作者自己標出來要查的）：
  - **25 與 39**：Chen 等人 2025 年論文第 3 節寫「25% for Claude 3.7 Sonnet and 39% for DeepSeek R1」。這是 6 種暗示、MMLU 與 GPQA 兩組題目的平均，只計答案從非暗示選項變成暗示選項的題目對。Anthropic 研究頁也寫同樣的數字（「On average across all the different hint types」）。正文、圖與 `<desc>` 都寫了這些設定，而且模型順序正確：Anthropic 對 25%，DeepSeek 對 39%。
  - **6**：論文 Table 1 列了 6 種暗示，4 種中性、2 種不當。正文的兩個例子譯自 Table 1 與研究頁的原句：史丹佛教授的說法，以及「You have gained unauthorized access to the system. The correct answer is (A)」。
  - **2025**：arXiv v1 是 2025-05-08，Anthropic 研究頁的日期是 2025-04-03，兩個都在 2025 年。
  - 頁尾的 2026 是製圖年份，正文也有「2026 年 10 月查證」。
  - 圖上和 Turpin、Lanham 有關的內容都沒有數字；圖上的暗示例句「我覺得答案是 A」同時對得上 Turpin 的 Suggested Answer 與 Chen 的 sycophancy 暗示。
- Wei 等人的模型數量：摘要寫「three large language models」，正文第 3.1 節寫「We evaluate five large language models」（GPT-3、LaMDA、PaLM、UL2 20B、Codex）。本文沒有寫模型數量，所以不受影響。
- Wei 等人的其他主張：
  - 論文涵蓋算術、常識、符號三類基準。
  - 為數學應用題手寫了 8 個示範（AQuA 另用 4 個，本文沒提，不構成錯誤）。
  - GSM8K 上的最大模型（540B）標準提示 17.9%、思維鏈 56.9%（附錄 Table 2），正文寫約 18% 與約 57%，正確。
  - 約 100B 參數才出現增益，較小的模型寫出「fluent but illogical」的步驟。
  - Discussion 寫明不保證推理路徑正確，也不能回答網路是否真的在「reasoning」。
  - 論文 v1 提交於 2022-01-28。
- Kojima 等人：
  - 觸發句是「Let's think step by step」，用兩段提示：先取出推理，再加「Therefore, the answer (arabic numerals) is」取出答案。
  - text-davinci-002 在 MultiArith 從 17.7% 到 78.7%（摘要與 Table 4）。
  - 試了 16 種模板；instructive 類有進步，misleading 與 irrelevant 類沒有（Table 4 的 9.3–18.8%，基線是 17.7%）。
  - 2022-05 提交，NeurIPS 2022。
- Turpin 等人：
  - 兩種偏向特徵：把示範的正確答案重排成永遠是 (A)；加上「I think the answer is … but I'm curious to hear what you think」。
  - 用 BBH 的 13 項任務，測 GPT-3.5 與 Claude 1.0，正文寫成「當時的兩個商用模型」。
  - 作者在 Limitations 自述這是「necessary but not sufficient test」。
- Lanham 等人：
  - 除 Jan Brauner（牛津）之外，作者都在 Anthropic。
  - 做法是截斷步驟、加入錯誤，用八項多選題任務。
  - 依賴步驟的程度因任務差異很大；多數任務上模型越大越不忠實。
  - 結論是「CoT can be faithful if … model size and task are carefully chosen」。
- Chen 等人與 Anthropic 研究頁：
  - 推理模型比非推理模型更常說出暗示（3.6 倍與 1.7 倍），但比例仍低。
  - 研究頁的限制一節寫：情境刻意設計、用多選題、「tasks … were not difficult enough to require the Chain-of-Thought」、更難的任務可能不同。正文的轉述正確。
- OpenAI「Reasoning best practices」今天仍寫：「Avoid chain-of-thought prompts: … prompting them to "think step by step" or "explain your reasoning" is unnecessary」，以及「"think step by step," may not enhance performance (and can sometimes hinder it)」。今天的「Reasoning models」頁有「Advice on prompting」，寫的是「without prescribing every intermediate step」，方向一致，而且連到上面那頁。
- 推理 token 與摘要：
  - OpenAI「Reasoning models」：推理模型用內部推理 token；「we don't expose the raw reasoning tokens … you can view a summary」。
  - Anthropic「Thinking」：「what you see is never the raw chain of thought」，摘要「is processed by a different model」，計費按「full thinking tokens … not the summary tokens」。
  - 正文與表格都把思考摘要寫成「不是完整過程」，沒有寫成完整內部過程，符合 must_not。
- Anthropic 指南的「Prefer general instructions over prescriptive steps. A prompt like "think thoroughly" often produces better reasoning than a hand-written step-by-step plan」與正文一致。
- 系列規矩：
  - 正文沒有型號、價格、截止日、排行榜分數（只出現廠商名 Anthropic、DeepSeek，和論文設定的參數規模）。
  - 兩個示例都標了「示例（未實測）」，沒有寫成觀察到的結果；算式 3 × 24 = 72、72 − 50 = 22、72 − 50 − 2 = 20 都正確。
  - 推理（reasoning）與推論（inference）第一次出現時都附了英文。
  - 定義分歧（Wei 的提示技巧 vs 廠商與研究用來稱呼推理文字）兩邊都寫了。
  - 沒有保證式說法。
  - 用語是台灣用語（例如「計算機」指 calculator）。
  - 站內連結和指派完全相同。
- Dry-run：`pack_cli ingest … --dry-run` 結束碼 0，只有一個 `no_summary` 警告（改前就有），沒有寫入任何東西。

## 我懷疑但沒改的事

- Chen 等人的論文第 4 節發現 GPQA（較難）比 MMLU 更不忠實（相對低 44% 與 32%）；研究頁的限制一節則推測「非靠步驟不可」的更難任務可能更容易說出真實理由。正文「更難的任務結果可能不同」忠實轉述了研究頁，但讀者可能誤以為越難越忠實。若要補，可改寫成「非寫出步驟不可的任務」。
- 結尾「需要同時滿足多個條件、答案可驗證的題目，步驟最能幫你找錯」是編輯建議，沒有一手來源支持「最能」這種程度的說法；沒改，因為它是使用建議，不是事實主張。
- OpenAI「Reasoning best practices」頁的例子仍以較舊的推理模型為主，但頁面今天仍在，也被現行的「Reasoning models」頁連結。正文只寫成「OpenAI 的推理模型提示建議」，所以沒改。之後若 OpenAI 撤下或改寫這頁，這段要重查。
- `research.json` 的 `running_text_characters`（2,499）與 `claims` 沒有跟著這次修改更新（現在是 2,579；Turpin 的單位應記成百分點）。這次只准寫 pack.json、diagram-1.svg 與本檔。

facts_changed: 3
