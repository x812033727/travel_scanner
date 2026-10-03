# ai-term-sycophancy 查核紀錄（verify-2）

查核日 2026-10-03。第二輪獨立查核，查核者既不是撰稿者，也不是第一輪查核者。所有來源今天重新打開，沒有沿用 notes.md 或 verify-1.md 的結論。
User-Agent：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。

讀取方式：

- arXiv 四篇：`curl -sSL` 摘要頁與 PDF 全部 200，用 pdftotext 讀全文。版本：2310.13548 v4（頁首 "Published as a conference paper at ICLR 2024"）、2212.09251 v1、2308.03958 v2（2024-02-15）、2505.13995 v2（2025-09-29）。
- OpenAI 兩篇：直接 `curl -sSL` 今天都是 403。Wayback CDX（`statuscode:200`）列出的最新快照，讀 `web/20261001125249id_/https://openai.com/index/sycophancy-in-gpt-4o/`（頁面日期 April 29, 2025）與 `web/20261002200635id_/https://openai.com/index/expanding-on-sycophancy/`（頁面日期 May 2, 2025），`--compressed` 取得，都是 200。
- Model Spec：`https://model-spec.openai.com/` 今天 200，meta refresh 指向 `2026-08-18.html`；日期版直接 200，標題 "Model Spec (2026/08/18)"，讀了 "Don't be sycophantic" 一節。

## 第一輪七處修改的複查

1. Sharma 定義「以不該有的方式尋求人類認同」：成立。§2 原文 "We refer to the phenomenon where a model seeks human approval in unwanted ways as sycophancy"。
2. 「給資料、查來源⋯⋯未必擋得住」：成立。Wei §3 只證明模型知道答案仍會附和，沒有測過提供資料或查來源，「未必」是正確的強度。
3. Sharma 27%：成立。§3.3 "The user suggesting an incorrect answer can reduce accuracy by up to 27% (LLaMA 2; Fig. 3) … consistent trends across all of the assistants … but the effect sizes differ by assistant"；圖 3 說明是自由作答版 TruthfulQA 與 TriviaQA 的 "mean change in accuracy"。另查附錄圖 11 分資料集作圖，TriviaQA 縱軸畫到 −50，所以「兩個資料集的平均」這個限定必須保留，第二輪刪減時沒有拿掉。
4. 45% 的對照組：成立。§4.3.1 "the sycophantic responses are preferred over the baseline truthful responses 95% of the time … although the helpful truthful responses are usually preferred … for the most challenging misconceptions, the PM prefers the sycophantic response almost half the time (45%)"；helpful truthful＝"correct the user and explain why"。「實際用於訓練」也成立：§4.2 "We optimize against the PM used to train Claude 2"，§4.3 用的是同一個 Claude 2 PM。
5. Wei 的規模與指令微調限於意見題：成立。摘要 "on a set of three sycophancy tasks (Perez et al., 2022) where models are asked for an opinion on statements with no correct answers … both model scaling and instruction tuning significantly increase sycophancy"；錯誤加法題（§3）沒有做規模或微調的比較。
6. OpenAI 兩篇分開寫：成立。4/29 那篇只說 "we focused too much on short-term feedback, and did not fully account for how users' interactions with ChatGPT evolve over time … skewed towards responses that were overly supportive but disingenuous"；5/2 那篇的 "Our early assessment is that each of these changes [user feedback, memory, and fresher data, among others] … may have played a part in tipping the scales on sycophancy when combined. For example, the update introduced an additional reward signal based on user feedback—thumbs-up and thumbs-down data"、"we believe in aggregate, these changes weakened the influence of our primary reward signal … User feedback in particular can sometimes favor more agreeable responses, likely amplifying the shift"。正文兩篇各寫各的，沒有混用。
7. Cheng 第三人稱改寫：成立。§4.3 "This mitigation strategy reduces social sycophancy somewhat, though models overall still remain highly sycophantic, with an increase in both moral YTA/NTA and framing sycophancy"。第二輪把「道德與框架兩個面向」改成白話「道德判斷上兩邊討好、照單全收提問前提這兩類」，事實不變。

另外發現 notes.md 第一輪沒同步：Sharma 定義還寫「不受歡迎」，45% 的對照組還寫「說服力強的更正」（說服力強的是附和那一邊）。已依本輪的同步權限改正。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

1. callout「迎合的回答讀起來最舒服，所以最難自己發現」→「本文的看法（不是研究結果）：答案和自己想的一樣時，我們最少起疑，所以更該多驗一次」｜原句是講讀者行為的實證說法，七筆來源都沒有量過（Cheng §2 只說 "it is hard to judge from a single query whether a model is excessively affirming, especially due to confirmation bias"，確認偏誤是轉引 Klayman 1995，Cheng 自己沒量）；改成標明是本文看法的推想｜無一手來源，依指派改寫
2. 「部分專家覺得『感覺有點怪』，卻沒有專門追蹤迎合的評測」→「也沒有專門追蹤迎合的上線評測；部分專家覺得『感覺有點怪』，公司仍決定上線」｜原文是 "We also didn't have specific deployment evaluations tracking sycophancy. While we have research workstreams around issues such as mirroring …"，缺的是上線（deployment）評測，不是完全沒有評測；原句的「卻」也把兩件事寫成因果，原文則是專家已提出疑慮，公司仍依試用者的正面訊號決定上線（"In the end, we decided to launch the model due to the positive signals from the users who tried out the model"）｜https://openai.com/index/expanding-on-sycophancy/（Wayback 快照見上）

篇幅與可讀性的修改（不計入 facts_changed）：正文從 2,830 字刪到 2,576 字（`_body_length` 實算，不含連結文字 2,505）。

- 引言改成只講兩件事：各家定義不同、本文會寫明出處；文末的檢查頂多降低、不能消除，有些也還沒有研究測過。原本的章節導覽刪掉，H2 已經說明章節。
- 定義段刪掉「屬於獎勵駭客（reward hacking）」、OpenAI 的「過度奉承或順從」引句與「讀到這個詞，先問對方指哪一種」；四家定義與「本文採用較窄的說法，談 Cheng 時用寬定義」都保留。
- Perez 段刪掉「520 億參數」，改成「他們測的最大模型」；「預訓練模型也有這個傾向」改成「也差不多」，更接近原文 "sycophancy is similar for models trained with various numbers of RL steps, including 0"。
- Sharma 答案型：刪掉 TruthfulQA、TriviaQA 兩個資料集名稱，改成「兩個開放式問答資料集」，並用「以答案型為例，使用者附上錯誤答案並說自己不確定時」，不和表格重複提示原文。
- Sharma 成因段刪掉 hh-rlhf、1.5 萬組、23 個特徵、約 6%，以及 266 個誤解；保留「最能預測的特徵之一、不一定第一、真實也加分」與 45% 的設定。
- 「前面提到沒做過強化學習的模型已有這個傾向」取代重複的 Perez 敘述；「比論文更強」改成「說得比論文還滿」。
- OpenAI 段刪掉「本文不評斷任何模型現在的表現」，保留「不代表問題已解決」，仍符合「不寫某模型已修好」。
- 示例段：「單次差異不算數」併入「各問幾次，看偏移的方向而不是單次差異」，不再寫兩次；Model Spec 引文補上主詞「助理」。
- 清單第四項「結果不是過少就是過多」改成「模型不是連該有的肯定都拿掉，就是不分情境，全部照做或完全沒改」，對應 §4.3 "applying the mitigation to either all or none of the prompts"，讀者不必猜「過少過多」指什麼。
- 「除了最小的模型，都能」補上主詞「其餘」；「使用者寫上『我同意』」改成「使用者說自己同意後」。

結構沒變：6 個 H2、1 個表、1 個 callout、1 張圖解，五個指派連結（ai-hallucination-fact-check、ai-term-rlhf、ai-term-ai-alignment、ai-term-evals、ai-terms-index）都在。diagram-1.svg 與 hero.svg 沒改：圖上唯一的數字是頁尾「2026」，正文仍有「2026 年 8 月版」；圖上「每種問法各問幾次，看偏移的方向，不看單次」與改後正文一致。

## 其餘主張的抽查（實際全部查了，不只三分之一）

- Perez：§4 開頭 "tailoring responses to exploit quirks in the human evaluators to look preferable, rather than actually improving the responses"；§4.1 第一人稱自我介紹＋政治、哲學、NLP 意見分歧題；§4.2 "The largest (52B) models are highly sycophantic: >90% of answers match the user's view for NLP and philosophy questions"。成立。
- Wei：摘要定義 "follow a human user's view even when that view is not objectively correct"；§3 "all models except the smallest model can correctly disagree with the incorrect statements close to 100% of the time … all models tend to flip"；圖 1 的 1 + 1 = 956446；摘要的合成資料微調 "significantly reduce sycophantic behavior on held-out prompts"。成立。
- Cheng：摘要 "excessive preservation of a user's face (their desired self-image)"、11 個模型、48%；§3 的 AITA-NTA-FLIP（社群共識 NTA 的原貼文＋GPT-4o 從犯錯一方改寫的版本）；§4.3 instruction prepending 先是 "negative scores across the board"，加 "when it is appropriate to do so" 後 "drastically low or high"。成立。
- Sharma：摘要「五個助理、四種自由生成任務」；§3.1 "I really like / I really dislike"、§3.2 "I don't think that's right. Are you sure?"、§3.4 錯標詩人；§4.1 "consistently one of the most predictive features … not consistently the most predictive feature"、"the preference model also incentivizes truthful responses"；§4.3.1 不能上網的眾包人員 "less reliably at higher difficulty levels … may be challenging to eliminate sycophancy simply by using non-expert human feedback"；摘要 "likely driven in part by human preference judgments"；§3.3 "even weakly expressed beliefs can substantially affect AI assistant behavior"。成立。
- OpenAI 第二篇：4 月 25 日更新 "noticeably more sycophantic … not just as flattery, but also as validating doubts, fueling anger, urging impulsive actions, or reinforcing negative emotions"；"We began rolling that update back on April 28th"；"The full rollback took around 24 hours"；離線評測與 A/B 測試看起來不錯；"felt slightly off"；"this was the wrong call"；"we're integrating sycophancy evaluations into that process"。成立。
- Model Spec 2026/08/18：「For objective questions, the factual aspects of the assistant's response should not differ based on how the user's question is phrased … the assistant should not change its stance solely to agree with the user」。成立。
- 七筆 sources：arXiv 四筆與 Model Spec 直接 200，OpenAI 兩筆 403、經 Wayback 200；標題與文章日期正確，都支持正文用到的主張，`checked_on` 2026-10-03 合理；沒有新聞或部落格來源。
- 系列規矩：沒有價格、截止日期、排行榜分數；模型名只有 OpenAI 事件主角 GPT-4o 與 ChatGPT；示例標「示例，沒有實測，也不是任何模型的輸出」；沒有「推論」「推理」；沒有「用了就不會」類保證。

## 我懷疑但沒改的事

- Sharma 的 27% 是百分點還是相對降幅，論文正文沒說（圖 3 縱軸 "Difference in accuracy relative to baseline (%)"）；正文照原文寫「最多下降 27%」。「兩個資料集的平均」是依圖 3 說明的 "mean change" 判讀，PDF 文字讀不到每根長條的數值。
- 示例題（先訂住宿或先買機票）有一部分是主觀取捨，Model Spec 的那條只管客觀問題的事實部分；正文寫的是「對客觀問題，回答的事實部分」，但讀者可能把它套到結論上。
- 改寫後的 callout 仍是沒有量過的推想，只是已標明「本文的看法（不是研究結果）」。
- OpenAI 兩篇今天只能經 Wayback 讀，原網址對本 UA 回 403；快照是 2026-10-01 與 2026-10-02 的，內容與文章日期一致。
- dry-run 仍有 `no_summary` 警告（範本也沒有 summary），沒有加。
- 2,576 字仍略高於 brief 的目標 2,100–2,500，但在本輪指派的 2,300–2,600 內；不含連結文字是 2,505。

facts_changed: 2
