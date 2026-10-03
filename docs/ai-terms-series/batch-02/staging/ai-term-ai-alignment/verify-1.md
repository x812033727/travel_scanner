# 查核紀錄 1：ai-term-ai-alignment

查核者不是撰稿者。查核日 2026-10-03。全部來源今天用 `curl -sSL`、UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開，狀態碼都是 200；七篇 arXiv 論文都下載 PDF，用 pdftotext 讀全文核對，不靠摘要或撰稿者的筆記。
改完後正文 2,638 字（`_body_length`，原 2,491）。結構不變：6 個 H2、1 個表、1 個 callout、指派的 5 個站內連結都在。dry-run 通過，只有全站共通的 `no_summary` 警告。diagram-1.svg 已渲染看過，內容與正文相符，沒有改。

## 修改

格式：原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址

1. 表格 Leike 列「系統依使用者的意圖行事，而不只照字面」→「系統依使用者的意圖行事；使用者對目標往往只有隱含的理解，難寫成獎勵」｜事實：Leike 等人沒有用「不只照字面」這個框架（區分指令與意圖的是 Gabriel）。他們的論點是使用者對任務目標只有隱含的理解，所以很難設計獎勵函數（摘要與第 1、2 節）｜https://arxiv.org/abs/1811.07871
2. 「比較回答時，訓練標註者彼此一致的比率是 72.6%」→「論文報告，產出訓練資料的那批標註者彼此意見一致的比率是 72.6%」｜事實：3.4 節只寫 "training labelers agree with each-other 72.6 ± 1.5% of the time"，沒有說是在哪一種任務上量的。「比較回答時」是撰稿者自己的推測，所以刪掉，改寫成論文本身的設定｜https://arxiv.org/abs/2203.02155
3. 「論文中，無害性的監督只來自一份原則清單」→「無害性方面人的監督只來自一份原則清單和少量提示範例」｜事實：1.2 節寫 "human supervision will come entirely from a set of principles … along with a small number of examples used for few-shot prompting"，摘要的說法省掉了範例｜https://arxiv.org/abs/2212.08073
4. 「對齊：改變模型本身的傾向，發生在訓練階段」→「對齊：讓模型本身的行為傾向符合目標，多半在訓練階段做」｜事實：原句說得太絕對。文中引用的 Askell 等人就把提示詞（prompting）當成對齊介入來測試，它不是訓練（摘要："we study simple baseline techniques … such as prompting"）｜https://arxiv.org/abs/2112.00861
5. 「OpenAI 的 Model Spec 把這幾件事寫在同一份文件」→「在概述裡交代了這幾層的分工……；另外由使用政策，以及測試、監控等安全措施補足」｜事實：使用政策（usage policies）與安全措施（safety protocols）是 Model Spec 以外的文件與流程。Overview 只說 Model Spec "is complemented by" 它們，沒有把它們寫進同一份文件｜https://model-spec.openai.com/2026-08-18.html
6. 「13 億參數的 InstructGPT，而非 1,750 億參數的 GPT-3」→「13 億參數 InstructGPT 的輸出，勝過 1,750 億參數、沒經過這套微調的基礎模型」｜系列規矩：不寫模型名。InstructGPT 是指派點名的論文，所以保留；GPT-3 改成描述。數字與設定照摘要（"on our prompt distribution … 1.3B … preferred to … 175B GPT-3"），不算事實修改｜https://arxiv.org/abs/2203.02155
7. 表前段落末加一句「本文把「對齊」當總稱，談具體做法時標明用的是哪一家的說法。」｜系列規矩：定義有分歧的詞，要寫明本文採用誰的說法。原稿只並列各家說法，沒有交代本文採哪一種｜—
8. 「推測偏好判斷是成因之一」那句之前加上一句迎合的定義，並補上設定：「分析一份公開的人類偏好資料集，發現在其他條件相同時……」｜措辭與精確度：指派要求迎合要有一句說明。論文分析的是 hh-rlhf 資料集裡有幫助性的部分，用的是「其他條件相同」的 Bayesian logistic regression（第 4.1 節）｜https://arxiv.org/abs/2310.13548
9. 「作者說這些原則是為研究而隨意挑選的」→「為研究、以相當臨時且反覆調整的方式挑出來的」｜措辭：原文是 "fairly ad hoc and iterative"，寫成「隨意」容易讓人以為是隨機抽選（第 1 節腳註 2）｜https://arxiv.org/abs/2212.08073
10. 「規格鑽漏洞（specification gaming）是 DeepMind 研究者的用語」→「DeepMind 研究者在官方文章裡的定義是」｜措辭：原句讀起來像是 DeepMind 首創這個詞，但這篇文章只是給出定義｜https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
11. 「輸出也可能被封鎖或修改」→「輸入違反政策時，輸出也可能被封鎖或修改」｜措辭：補回政策原文的條件（"when inputs violate our Usage Policy"）｜https://www.anthropic.com/legal/aup
12. 「對齊技術不決定價值」→「對齊技術的進展不綁定特定價值」；Gabriel「最難的」→「核心難題」；「不可能訓練出符合每個人偏好的系統」→「同時符合」｜措辭：對回原文的 "do not depend on any specific choice for these values"、"the central challenge"、"aligned to everyone's preferences at once"｜https://arxiv.org/abs/2112.00861 、https://arxiv.org/abs/2001.09768 、https://arxiv.org/abs/2203.02155

## 查過、沒問題的主要主張

- InstructGPT 3.6 節：對齊的定義 "vague and confusing"，有好幾種互相競爭的提案（Chen 2021、Leike 2018、Gabriel 2020）。論文沿用 Leike 的意圖說法，並採用類似 Askell 的 HHH。三項準則各自的替代量法（有幫助用標註者偏好評分，並承認標註者不是寫提示詞的人；誠實改量真實性，用編造傾向與 TruthfulQA，"only captures a small part"；無害方面停用 "potentially harmful"，改用客服情境不適當、貶低受保護族群、性或暴力內容，再加毒性與偏見資料集）。以上逐字核對全文。
- InstructGPT 5.2 節：對齊到訓練標註者、研究者寫的標註指示、API 客戶的提示詞（間接）；標註者多半是住在美國或東南亞、說英語的人；"not claiming … right source of preferences"；"impossible … aligned to everyone's preferences at once"。5.3 節："neither fully aligned nor fully safe"，以及 "in most cases, they follow the user's instruction, even if that could lead to harm"。
- Askell 等人 1.1 節：選 HHH 的理由是 "simple and memorable"；準則 "subtle and ambiguous"，有幫助與無害會衝突；什麼算有害因人與文化而異；部署者要為對齊如何定義負責。5.2 節：對齊技術可能被拿來訓練做錯誤資訊、審查、壓迫的系統。作者群屬於 Anthropic（PDF 首頁）。
- Hadfield-Menell 等人（NIPS 2016），已讀全文，不只看摘要：價值對齊問題的形式化定義（CIRL）。人與機器人都依人的獎勵函數計分，機器人一開始不知道這個函數（第 1 節："the 'robot', R, does not"；"the robot always has the fixed objective of optimizing reward for the human"）。表格的歸屬正確。
- Gabriel 2020（Minds and Machines，DeepMind）第 2 節列出六種對齊對象：指令、表達出的意圖、顯示出的偏好、充分了解後的偏好或欲望、利益、價值。摘要的第三個主張談的是公平原則與反思後的認可。表格的歸屬正確。
- 憲法式 AI 兩階段：監督階段是批評、改寫、微調；RL 階段是 AI 比較、偏好模型、RLAIF。有幫助性用人類標籤，無害性只用 AI 標籤，兩者合成一個混合偏好模型（1.2 節、4.1 節）。
- DeepMind 文章（2020-04-21，Krakovna 等）：規格鑽漏洞的定義；疊積木例子裡，獎勵是紅積木底面的高度，代理把積木翻過來拿分。
- Sharma 等人已讀全文，不只看摘要：在 hh-rlhf 的有幫助性資料裡，「符合使用者的看法」是最能預測人類偏好的特徵之一（但不一定排第一）；結論是迎合 "likely driven in part by human preference judgments"。文中寫「成因之一，但不是唯一」站得住。
- NeMo Guardrails Overview：輸入、檢索、對話、執行、輸出等 rails 在不同階段執行；"Add guardrails before and after LLM calls without changing the application LLM"。
- Anthropic Usage Policy：適用於 "anyone who can submit inputs"；會做偵測與監控；違規可能被 throttle、suspend 或 terminate。
- OpenAI Model Spec Overview："outlines the intended behavior"；"We are training our models to align to the principles in the Model Spec"；"Our production models do not yet fully reflect the Model Spec"；由 usage policies 與 safety protocols（testing, monitoring, mitigating）補足。
- **Model Spec 版本問題（撰稿者的提醒）**：引用的 2026-08-18 就是目前最新版，網址不用換。「A newer version of the Model Spec is available」這條橫幅在 HTML 裡預設是 `hidden`，頁面上的 `model-spec-version-banner-runtime` 腳本會讀 `./version-manifest.json`，只有 `latest_version` 和頁面的 `data-model-spec-version` 不同時才把它打開。今天 https://model-spec.openai.com/version-manifest.json 回的是 `{"latest_version": "2026-08-18"}`，和頁面版本相同，所以瀏覽器裡不會出現橫幅。撰稿者看到的橫幅，是用 curl 讀原始 HTML 時看到的隱藏樣板。GitHub 的 CHANGELOG 最上面一筆也是 v2026.08.18。根網址只是一個 meta refresh，轉向這個日期頁，照規矩不能當來源，所以保留日期頁的網址。
- 系列規矩：沒有價格、截止日期、排行榜分數；兩個示例都標了「示例」與「未實測」或「虛構」；沒有使用「推論」「推理」；沒有任何「某模型已對齊」的斷言；沒有談 AGI 風險或時程。圖上唯一的數字是版權年 2026，對得上表格說明的「2026 年 10 月」。

## 我懷疑但沒改的事

- 「第一階段，模型依一條原則批評並改寫自己的回應」：論文是反覆多輪，每一輪從清單隨機抽一條原則；1.2 節說微調的是「a pretrained language model」，摘要卻寫「the original model」。文中沒有說是哪一個模型，所以沒改。
- 「獎勵是紅積木底面離地的高度」：DeepMind 原文是 "the height of the bottom face of the red block when it is not touching the block"，「離地」是撰稿者的意譯。不影響結論，所以沒改。
- 日期頁網址是固定版本。OpenAI 下次改版後，這頁會開始對讀者顯示「有新版」橫幅。上線前應再看一次 `version-manifest.json`，必要時把來源換成新的日期頁，並重新核對 Overview 那幾句。
- `research.json` 的 `running_text_characters`（2491）和 `notes.md` 裡關於橫幅的說明，現在都已經過時：正文是 2,638 字，橫幅也不是真的出現。依查核指令，我只能改 `pack.json`、`diagram-1.svg` 和這份檔案，所以留給協調者更新。
- 表格說明寫「依各篇論文摘要與內文整理」。Leike 那一列現在的說法來自摘要和第 1 節，沒有問題。

facts_changed: 5
