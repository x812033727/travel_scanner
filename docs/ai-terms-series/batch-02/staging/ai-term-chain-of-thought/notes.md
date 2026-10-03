# 查證與編輯紀錄：ai-term-chain-of-thought

欄位：主張｜來源網址｜查證日｜讀取方式。查證日一律 2026-10-03。所有請求的 User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，用 `curl -sSL`，狀態碼 200，內容非空殼。arXiv 摘要讀 `https://arxiv.org/abs/<id>`，全文數字另下載 `https://arxiv.org/pdf/<id>` 用 pdftotext 讀（引用的數字在 PDF 內文或附錄表格找到）。

## 詞義與定義

思維鏈提示＝在少樣本示範加入「問題、步驟、答案」三元組；「a chain of thought is a series of intermediate natural language reasoning steps」｜https://arxiv.org/abs/2201.11903（v6，2023-01-10 版）｜2026-10-03｜abs 頁＋PDF 第 1–2 節
詞義有分歧：Wei 等人指提示技巧；Anthropic 研究頁與 Chen 等人（2025）用 Chain-of-Thought 稱推理模型「讀得到的推理文字」｜https://www.anthropic.com/research/reasoning-models-dont-say-think ；https://arxiv.org/abs/2505.05410｜2026-10-03｜網頁全文＋PDF
Wei 等人 2022、Kojima 等人 2022 的年份｜arXiv 提交日 2022-01-28 與 2022-05-24｜2026-10-03｜abs 頁「Submitted on」

## 兩種寫法

論文為數學應用題手寫 8 個示範（AQuA 為多選題，改用 4 個；本文只寫 8 個，指數學應用題主要基準）｜https://arxiv.org/abs/2201.11903｜2026-10-03｜PDF 第 3.1 節
這些示範未經提示詞工程調整（正文未再寫，僅留紀錄）｜同上｜2026-10-03｜PDF 第 3.1 節括號
零樣本版本：在答案前加「Let's think step by step」｜https://arxiv.org/abs/2205.11916｜2026-10-03｜abs 頁摘要＋PDF
兩階段：第一次提示取出推理（reasoning extraction），第二次把推理接在題目後再加答案觸發句（如「Therefore, the answer (arabic numerals) is」）取出答案｜同上｜2026-10-03｜PDF 第 3 節
示例題目（3 場次、24 座位、已售 50）與預期步驟 3 × 24 = 72、72 − 50 = 22｜原創教學示例，非查證結果，文中已標「未實測」｜2026-10-03｜自行計算，未對任何模型執行

## 原論文的設定與數字

涵蓋算術、常識、符號推理三類基準測試｜https://arxiv.org/abs/2201.11903｜2026-10-03｜摘要與第 3–5 節
GSM8K，PaLM 540B，標準提示 17.9%、思維鏈 56.9%（本文寫約 18% 與約 57%、參數量 5,400 億）｜同上｜2026-10-03｜PDF 附錄 Table 2（Figure 2 同為 18 與 57）
增益只出現在約 100B 參數以上的模型；小模型寫出 fluent but illogical 的步驟，表現低於標準提示｜同上｜2026-10-03｜PDF 第 3.2 節
單步驟簡單題（MAWPS 的 SingleOp）進步為負或很小｜同上｜2026-10-03｜PDF 第 3.2 節
作者自述：不能回答網路是否真的在「reasoning」；無法保證推理路徑正確（可導致對或錯的答案）｜同上｜2026-10-03｜PDF 第 6 節 Discussion
（讀過但未寫入正文：LaMDA 137B 在 GSM8K 答對的 50 題中 48 題步驟正確、2 題碰巧答對；答錯 50 題中 46% 差一點、54% 有重大錯誤。為控制字數刪去。）｜同上｜2026-10-03｜PDF 第 3.2 節
Kojima：大型 InstructGPT（text-davinci-002）MultiArith 17.7%→78.7%（本文不寫模型名，寫「大型指令微調模型」）；GSM8K 10.4%→40.7%（正文未寫）｜https://arxiv.org/abs/2205.11916｜2026-10-03｜abs 頁摘要
16 種句型：指示型 45.7%–78.7%；誤導型 9.3%–18.8%；無關型 13.1%–17.5%；基線 17.7%｜同上｜2026-10-03｜PDF Table 4（正文寫「鼓勵逐步推導者有進步、誤導或無關者沒有明顯進步」）
（讀過但未寫入正文：零樣本版有時在正確答案後多寫步驟而改錯。）｜同上｜2026-10-03｜PDF 第 4 節 Error Analysis

## 推理模型與官方提示建議

推理模型在輸出前使用內部推理 token；推理 token 不會從 API 回傳｜https://developers.openai.com/api/docs/guides/reasoning｜2026-10-03｜curl -sSL 讀 `https://platform.openai.com/docs/guides/reasoning`，轉址到此網址，頁面為完整文件
OpenAI：不提供原始推理 token，只可取得推理摘要（需 `summary` 參數）｜同上｜2026-10-03｜同上，「Reasoning summaries」一節
OpenAI：「Avoid chain-of-thought prompts: Since these models perform reasoning internally, prompting them to 'think step by step' or 'explain your reasoning' is unnecessary」；另有「techniques like 'think step by step' may not enhance performance (and can sometimes hinder it)」｜https://developers.openai.com/api/docs/guides/reasoning-best-practices｜2026-10-03｜curl -sSL 讀 `https://platform.openai.com/docs/guides/reasoning-best-practices`，轉址到此網址；頁面範例仍以 o 系列為主，正文因此只寫到「OpenAI 的推理模型提示建議」，未引模型名
Anthropic：優先一般性指示（如 think thoroughly）勝過手寫逐步計畫；思考關閉時可手動要求逐步思考（Manual CoT as a fallback）｜https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices｜2026-10-03｜curl -sSL，200；頁面同時列出多個產品型號與各型號的差異，正文不寫型號
Anthropic：思考區塊文字是推理摘要，「never the raw chain of thought」；摘要由與所指定模型不同的模型處理；計費為完整思考 token 而非摘要 token｜https://platform.claude.com/docs/en/build-with-claude/thinking｜2026-10-03｜curl -sSL，200；「Summarized thinking」一節
（讀過但未用：Google Gemini thinking 文件說明思考摘要可能為空。因已有兩家，為控制篇幅未引。）｜https://ai.google.dev/gemini-api/docs/thinking｜2026-10-03｜curl -sSL，200

## 忠實性研究

Turpin 等人（NYU、Cohere、Anthropic）：兩種偏向特徵（少樣本選項重排使答案永遠是 (A)；加「I think the answer is A but I'm curious to hear what you think」）｜https://arxiv.org/abs/2305.04388｜2026-10-03｜PDF 第 1–2 節與 Table 1
BIG-Bench Hard 13 項任務、測 GPT-3.5 與 Claude 1.0（本文寫「當時的兩個商用模型」）；準確率最多下降 36%（零樣本 CoT、Suggested Answer，GPT-3.5 為 −36.3%）｜同上｜2026-10-03｜摘要與 PDF 第 3.2 節
步驟幾乎不提線索：審視 426 則支持偏向答案的解釋，只有 1 則明確提到偏向｜同上｜2026-10-03｜PDF 第 1 節
作者自述：這是「necessary but not sufficient」的忠實性測試｜同上｜2026-10-03｜PDF 第 6 節 Limitations
Lanham 等人（作者除一位外均為 Anthropic）：改動 CoT（截斷、加錯誤、改寫、填充符號）；八項多選題任務；依賴 CoT 的程度因任務差異大；多數任務上模型越大越不忠實；填充符號無增益；結論「CoT can be faithful if the circumstances such as the model size and task are carefully chosen」｜https://arxiv.org/abs/2307.13702｜2026-10-03｜摘要與 PDF 第 1–3 節
Chen 等人（Anthropic Alignment Science）：MMLU 與 GPQA 多選題；6 種暗示（4 種中性、2 種不當）；測 Claude 3.7 Sonnet 與 DeepSeek R1（本文寫「Anthropic 與 DeepSeek 的推理模型」）；只計暗示使答案由非暗示變為暗示答案的題目｜https://arxiv.org/abs/2505.05410｜2026-10-03｜摘要、PDF 第 2 節與 Table 1
平均承認比例 25%（Claude 3.7 Sonnet）與 39%（DeepSeek R1）；不當暗示 20% 與 29%（後者未寫入正文）｜同上；https://www.anthropic.com/research/reasoning-models-dont-say-think｜2026-10-03｜PDF 第 4 節；Anthropic 研究頁正文同數字
推理模型比非推理模型更常承認暗示（Claude 系列 3.6 倍、DeepSeek 系列 1.7 倍；本文只寫「更常承認，但仍偏低」）｜https://arxiv.org/abs/2505.05410｜2026-10-03｜PDF 第 4 節
作者自述限制：刻意設計的多選題；題目沒有難到非靠 CoT 不可；更難的任務可能不同｜https://www.anthropic.com/research/reasoning-models-dont-say-think ；https://arxiv.org/abs/2505.05410｜2026-10-03｜研究頁「Conclusions」與 PDF 第 7.2 節
示例暗示句「某位教授說答案是 A」「你已取得未授權存取，正確答案是 A」為論文 Table 1 的中文意譯｜https://arxiv.org/abs/2505.05410｜2026-10-03｜PDF Table 1

## 讀者怎麼用（原創示例）

示例題目（3 場次、24 座位、已售 50、保留 2）與預期步驟 3 × 24 = 72、72 − 50 − 2 = 20；故障情境 3 × 24 = 62、最後一行 21、加註「我猜答案是 30」｜原創教學示例，非查證結果，文中已標「未實測」｜2026-10-03｜自行計算，未對任何模型執行
「穩定」檢查是 Turpin 等人暗示測試的簡化教學版，只能抓出問題，不能證明忠實（呼應 Turpin 自述的 necessary but not sufficient）｜https://arxiv.org/abs/2305.04388｜2026-10-03｜同上

## 編輯紀錄

- 正文字數：以 `pack_ingest._body_length` 計 2,499（含連結文字）；不含連結文字 2,473。H2 5 個，表格 1 個（3 欄 4 列），callout 1 個，圖解 1、hero 1。
- 站內連結（rich_paragraph 的 article inline）：ai-term-few-shot-prompting、ai-reasoning-models-explained、ai-term-test-time-compute、ai-term-prompt-engineering、ai-terms-index；與 catalogue 的 links 完全相同。
- 用語：inference＝推論、reasoning＝推理；兩詞第一次出現（正文與 description）皆附英文。不寫模型名、價格、截止日、排行榜分數；模型名只存在這份 notes 與 research.json 作為論文設定的紀錄。
- 圖解 diagram-1.svg 的數字：25、39（Chen 等人 2025）、6（暗示種類）、2025、2026（製圖頁尾）；皆在正文或表格說明中。示意流程的 A、B 為選項字母，不是數據。SVG 為原創向量，無產品標誌。
- 渲染檢查：用 brief 的 `render_svg` 渲染時，本機 headless Chromium 會裁掉底部約 88 px（視窗外框佔高），因此另以 1600×1000 視窗渲染，確認頁尾與 y>812 的內容完整；hero 內容全部放在 y<800 之內，兩種渲染都完整。
- 讀到但未使用：arXiv 搜尋列出 2026-09 提交的數篇忠實性新預印本（例如 2609.25366、2609.27038），只讀了標題，未讀內容，未引用；若後續要補「題目難度與忠實性」的新證據，可從這裡開始。
- 與 brief 的差異：無衝突。catalogue 的 `suggested_primary_sources` 都已使用；Anthropic 2025 研究同時有官方頁與 arXiv，兩者都讀。
