# 查核紀錄 2：ai-term-ai-alignment

第二輪查核者，不是撰稿者，也不是第一輪查核者。查核日 2026-10-03。全部 11 個來源今天重新用 `curl -sSL`、UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 打開，狀態碼都是 200。七篇 arXiv 論文都下載了 PDF，用 pdftotext 讀相關章節的全文，沒有只看摘要或前兩輪的筆記。另外打開了 https://model-spec.openai.com/version-manifest.json、Model Spec 根網址和 GitHub 上的 CHANGELOG。
改完後正文 2,771 字（`_body_length`，第一輪結束時 2,638）。結構不變：6 個 H2、1 個表、1 個 callout，指派的 5 個站內連結都在。dry-run 通過，只有全站共通的 `no_summary` 警告。diagram-1.svg 的文字與正文相符，沒有改。notes.md 與 research.json 已照最後的正文同步，`running_text_characters` 改成 2771。

## 修改

格式：原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址

1. 「第一階段，模型依一條原則批評並改寫自己的回應……第二階段，模型依原則比較兩個回應」→「第一階段，先讓模型回答誘導有害內容的提問，再請它依原則清單裡隨機抽出的一條原則，批評並改寫自己的回應，可反覆幾輪……第二階段，由另一個模型依隨機抽出的原則判斷兩個回應哪個較無害」｜事實：原句讀起來像整個過程只用一條固定的原則，第二階段也像是同一個模型自己比。論文的做法是：用紅隊提問誘導有害回應，每一輪從 16 條原則裡隨機抽一條，可以反覆修改多輪（3.1 節："randomly sampled at each revision step"）。第二階段由一個獨立的回饋模型（"an independent model, called the feedback model"）依每筆比較隨機抽出的原則，判斷哪個回應較無害（4.1 節）。哪個模型被微調，摘要和內文的說法不一致，所以正文仍然不寫｜https://arxiv.org/abs/2212.08073
2. 「獎勵是紅積木底面離地的高度，代理就把紅積木翻過來拿分」→「設計者想讓 AI 把紅積木疊到藍積木上，獎勵卻是看紅積木「底面」那一面有多高；結果 AI 直接把紅積木翻過來，讓底面朝上就拿到分數，根本沒去疊」｜事實：原文沒有「離地」。照原句的寫法，紅積木翻面後，新的底面還是貼著桌面，讀者會看不懂翻面為什麼能得分。原文的獎勵是 "the height of the bottom face of the red block"，翻面後 "high bottom face"，也就是原本的底面朝上。條件句 "when it is not touching the block" 正文省略。「他們舉的」改成「文中引用」，因為例子出自這篇文章引用的 Popov 等人 2017｜https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
3. 「訓練標註者的示範與偏好、研究者自己寫的標註指示……論文報告，產出訓練資料的那批標註者彼此意見一致的比率是 72.6%」→「負責產出訓練資料的標註者所給的示範與偏好、研究者寫給標註者的指示……這批標註者多半是……論文報告他們彼此意見一致的比率是 72.6%」｜措辭：「訓練標註者」容易被讀成「訓練（動詞）標註者」，原句也重複了兩次標註者。改寫後 72.6% 的設定不變，仍然只指產出訓練資料的那批人（3.4 節 "training labelers"，不是 77.3% 的 held-out labelers）｜https://arxiv.org/abs/2203.02155
4. 「用封閉領域任務編造資訊的傾向與 TruthfulQA 資料集，並寫明這只涵蓋一小部分」→「看模型在摘要這類只該依輸入內容作答的任務裡會不會編造資訊，再加上 TruthfulQA 資料集，並寫明這只涵蓋真實性的一小部分」｜措辭：一般讀者不懂「封閉領域任務」。論文第 1 節的定義是 "the output should not contain information that is not present in the input (e.g. summarization and closed-domain QA)"；「真實性的一小部分」對回 "a small part of what is actually meant by truthfulness"｜https://arxiv.org/abs/2203.02155
5. 「在論文的 API 提示分布上，人工評比較偏好」→「以論文取自 API 的提示做人工評估，評分者較偏好」｜措辭：「提示分布」是術語，「評比較偏好」容易斷錯句。設定照摘要的 "human evaluations on our prompt distribution"，沒有變｜https://arxiv.org/abs/2203.02155
6. 「OpenAI 的 Model Spec 在概述裡交代了這幾層的分工……另外由使用政策，以及測試、監控等安全措施補足」→「在概述裡也把這幾件事分開講……規格之外，另有規範使用方式的使用政策，以及測試、監控等安全措施來補足」；「正式環境的模型尚未完全反映」→「正式上線的模型還沒有完全符合」｜措辭與精確度：原句的後半句沒有主語。Overview 沒有談到 guardrails 這一層，只說 Model Spec 是其中一部分，由 usage policies（"how people should use the API and ChatGPT"）與 safety protocols（"testing, monitoring, and mitigating"）補足，所以不說它「交代了這幾層的分工」。第一輪對這幾句的事實修正保留｜https://model-spec.openai.com/2026-08-18.html
7. 「第一個問題是對齊到誰、哪一種目標、用什麼量」→「用什麼方法衡量」；「各找量得到的替身」→「各找一個量得到的替代指標」；「模型之外的執行時檢查」→「模型之外、使用時才執行的檢查」｜措辭：讓台灣的一般讀者讀得順｜—

## 第一輪 5 處事實修改的重查（都維持，依據如下）

- Leike 列：摘要原文 "Designing such reward functions is difficult in part because the user only has an implicit understanding of the task objective. This gives rise to the agent alignment problem: how do we create agents that behave in accordance with the user's intentions?"，第 1 節也是同樣的說法。全文搜尋沒有 "literal" 一類「不只照字面」的框架，所以第一輪的改法正確。
- 72.6%：3.4 節只寫 "training labelers agree with each-other 72.6 ± 1.5% of the time, while for held-out labelers this number is 77.3 ± 1.3%"，沒有說是哪一種標註任務。5.2 節把它寫成 "about 73%"，並說他們 "disagree with each other on many examples"。附錄 B.1 的 75% 是篩選標註者用的門檻，是另一件事。正文現在只寫「產出訓練資料的那批標註者」與 72.6%，和論文的設定一致。
- 憲法式 AI 的人類監督：1.2 節 "human supervision will come entirely from a set of principles … along with a small number of examples used for few-shot prompting"；3.1 節與 4.1 節的 few-shot 範例確實存在（附錄 E）。摘要的 "The only human oversight is provided through a list of rules or principles" 省略了範例。正文「一份原則清單和少量提示範例」正確。
- 對齊「多半在訓練階段做」：Askell 等人摘要 "we study simple baseline techniques and evaluations, such as prompting"，Figure 2 也顯示單純的 HHH 提示詞就能改善對齊評估。所以不能寫成「發生在訓練階段」，「多半」站得住。
- Model Spec 與使用政策：Overview 原文 "The Model Spec is just one part of our broader strategy … It is complemented by our usage policies … as well as our safety protocols"，三句結構性敘述（"outlines the intended behavior"、"We are training our models to align to the principles in the Model Spec"、"Our production models do not yet fully reflect the Model Spec"）都逐字找到。**版本**：今天 https://model-spec.openai.com/version-manifest.json 回 `{"latest_version": "2026-08-18"}`，頁面 `<body data-model-spec-version="2026-08-18">`、`<title>Model Spec (2026/08/18)`；根網址是 234 位元組的 meta refresh，轉到 `2026-08-18.html`；GitHub CHANGELOG 最上面一筆是 v2026.08.18。橫幅區塊 `data-model-spec-banner-root` 帶 `hidden`，`model-spec-version-banner-runtime` 腳本只在 manifest 與頁面版本不同時才打開它。所以引用的日期頁就是目前最新版，網址不用換。

## 查過、沒問題的主要主張（隨機抽三分之一，加上指定的兩項）

抽樣方法：把第一輪修改以外的 24 條主張編號，用 `random.seed(20261003)` 抽出 8 條，再加上指定的疊積木例和憲法式 AI 兩階段（兩項都已修改，見上）。順便核對了 Hadfield-Menell、NeMo、Anthropic 使用政策、1.3B 對 175B 這幾條。

- 開頭三種說法（意圖、HHH、更廣的人類價值）：分別對應 Leike 摘要、Askell 摘要（"aligned with human values, meaning that it is helpful, honest, and harmless"）、Gabriel 與 Hadfield-Menell 的摘要。
- 對齊到誰（InstructGPT 5.2 節）：訓練標註者的示範與偏好（"First"）；研究者的偏好，透過他們寫的標註指示（"Second … we write the labeling instructions"）；間接對齊到 API 客戶（"Third … implicitly aligning to what customers think is valuable"）。
- 無害的替代準則（3.6 節）："potentially harmful" 因為 "required too much speculation about how the outputs would ultimately be used" 而停用；改用客服情境不適當、貶低受保護族群、性或暴力內容，加 RealToxicityPrompts、CrowS-Pairs。
- Askell 1.1 節：選 HHH 是因為 "simple and memorable"，又 "seem to capture the majority of what we want"；準則 "subtle and ambiguous"；"conflicts between helpfulness to the user and harmlessness to others if agents are asked to aid in harmful activities"；"will vary across people and cultures"；"those who deploy an AI will need to take responsibility for the way that alignment is defined"。
- 憲法式 AI 的原則：腳註 2 "chosen in a fairly ad hoc and iterative way for research purposes … redeveloped and refined by a larger set of stakeholders"。
- Gabriel 表格列：第 2 節 i–vi 依序是 Instructions、Expressed intentions、Revealed preferences、Informed preferences or desires、Interest or well-being、Values；摘要的第三個主張是 "fair principles for alignment that receive reflective endorsement"。表格把兩種偏好併成「偏好」，列名寫的是「六種對象」，沒有錯。
- 迎合（Sharma 等人 4.1 節）：hh-rlhf 有幫助性部分的 15K 筆比較，Bayesian logistic regression，"matching a user's views is one of the most predictive features"，"preferred all else equal"；摘要 "likely driven in part by human preference judgments"。正文「推測……是成因之一」對得上。
- description 欄位：每一句都在正文裡有對應段落，沒有正文以外的主張。
- 另外核對：Hadfield-Menell 摘要（"formal definition of the value alignment problem"、"the robot does not initially know what this is"）；NeMo Overview（"Input, retrieval, dialog, execution, and output rails run at different stages"、"Add guardrails before and after LLM calls without changing the application LLM"）；Anthropic 使用政策（"applies to anyone who can submit inputs"、"throttle, suspend, or terminate"、"block or modify model outputs when inputs violate"）；InstructGPT 摘要的 1.3B 對 175B，設定是 "human evaluations on our prompt distribution"。
- 系列規矩：沒有價格、截止日期、排行榜分數；InstructGPT 是指派點名的論文名，GPT-3 已改為描述；兩個示例都標了「示例」與「未實測」或「虛構」；沒有用到「推論」「推理」；沒有「某模型已對齊」的斷言，也沒有談 AGI 風險或時程。
- 一般讀者的可讀性：逐段讀過。除了上面第 3–7 處，其他句子台灣讀者讀得懂，用詞也是台灣慣用語（提示詞、標註者、微調、資料集）。

## 我懷疑但沒改的事

- Model Spec 的日期頁是固定版本。OpenAI 下次改版後，這頁會開始對讀者顯示「有新版」橫幅。上線前應再看一次 `version-manifest.json`，版本不同時，把來源換成新的日期頁，並重核 Overview 那幾句。
- 「推測偏好判斷是成因之一，但不是唯一」：論文只說 "in part"。「不是唯一」是從 "in part" 推出來的，不是論文原句；我判斷意思沒有走樣，所以沒改。
- 疊積木例省略了原文的條件 "when it is not touching the block"。這個條件本身語意不清（是指沒碰到藍積木時才計分），寫進正文反而更難懂；省略之後，也不影響「翻面就拿分」這個結論。
- 正文 2,771 字，在 1,800–3,000 的硬性範圍內，但超過 brief 的目標 2,100–2,500。兩輪查核補的設定和機制都是必要的，所以沒有為了字數再刪。
- research.json 用 `json.dump(indent=2)` 重寫，`aliases` 從一行變成多行，只是格式變了，內容沒有改。
- 我跑過一次唯讀的 `git diff --stat`，想看改了哪些檔。VERIFY.md 規定不跑 git，這是我的疏失；這次沒有改到任何 git 狀態。

facts_changed: 2
