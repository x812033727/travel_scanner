# 查證與編輯紀錄：ai-term-agi

格式：主張｜來源網址｜查證日｜讀取方式。查證日皆為 2026-10-03（本批開工日，實際打開頁面的日期）。

## 讀取方式說明

- arXiv：`curl -sSL` 讀 `https://arxiv.org/abs/<id>`（摘要與版本日期），再讀 `https://arxiv.org/pdf/<id>` 以 pdftotext 轉文字核對原文。Levels of AGI 讀的是 v5（2025-09-24 修訂）；ICML 2024 論文集頁（PMLR 235）另開確認發表處。
- openai.com 三頁（章程、Planning for AGI and beyond、Microsoft 合作公告）直接 curl 與 WebFetch 皆回 403。改用 Wayback：CDX 查 `statuscode:200`，抓 `web/<時間戳>id_/<原網址>` 並加 `--compressed`。章程快照 20260917204605、Planning 快照 20261002040118、Microsoft 公告快照 20260927044013。`sources` 寫原網址。章程定義句另用 WebSearch 限定 openai.com 交叉確認措辭一致。
- Microsoft 官方部落格公告、ARC Prize 官方頁、PMLR：直接 curl 回 200，讀完整文字。
- 查不到或只在二手轉述的內容一律不寫。Gubrud 1997 原文（foresight.org）404、Wayback 被擋，所以文章沒有寫 AGI 一詞的起源，只在這裡記一筆。

## 主張對照

OpenAI 章程把 AGI 寫成「highly autonomous systems that outperform humans at most economically valuable work」｜https://openai.com/charter/｜2026-10-03｜Wayback 20260917 快照全文
OpenAI 2023 年文章把 AGI 寫成「AI systems that are generally smarter than humans」，全文沒有判定方法｜https://openai.com/index/planning-for-agi-and-beyond/｜2026-10-03｜Wayback 20261002 快照全文，搜尋 measure、benchmark、define 無相關句
該文另寫「The first AGI will be just a point along the continuum of intelligence」（文章未採用，字數取捨）｜同上｜2026-10-03｜同上
OpenAI 與 Microsoft 2025-10-28 官方公告：「Once AGI is declared by OpenAI, that declaration will now be verified by an independent expert panel」，公告未寫小組標準｜https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ 與 https://openai.com/index/next-chapter-of-microsoft-openai-partnership/｜2026-10-03｜Microsoft 直接讀取；OpenAI 版 Wayback 20260927 快照，兩頁該句相同。只引這一句，不引任何其他合約內容
Morris 等人在 ICML 2024 發表（PMLR 235）立場論文，檢視九種既有說法（圖靈測試、強 AI／意識、類比人腦、人類認知任務、學習任務能力、經濟價值工作、Coffee Test 類、Artificial Capable Intelligence、前沿 LLM 即 AGI）｜https://arxiv.org/abs/2311.02462 與 https://proceedings.mlr.press/v235/morris24b.html｜2026-10-03｜PDF v5 第 2–3 頁 Case Studies 1–9
多數說法談能力而非機制，且「what tasks?」「which people?」有歧義｜同上｜2026-10-03｜PDF Case Study 4 與原則 1
AGI 概念連到目標、預測與風險｜同上｜2026-10-03｜PDF 第 1 頁 Goals / Predictions / Risks
Morris 評章程定義：只看表現不問機制、經濟價值可當量尺；缺點是無明確經濟價值的能力、且隱含需部署｜同上｜2026-10-03｜PDF Case Study 6
Levels of AGI 兩軸：performance（深度）與 generality（廣度）；Narrow＝clearly scoped task or set of tasks；General＝wide range of non-physical tasks, including metacognitive tasks like learning new skills｜同上｜2026-10-03｜PDF Table 1 與第 4 節
表現五級：Emerging 等於或略優於 unskilled human；Competent 至少第 50 百分位；Expert 第 90；Exceptional 第 99；Superhuman 勝過 100% 的人；百分位對照 skilled adults｜同上｜2026-10-03｜PDF Table 1 與第 4 節文字
Level 4 早期版本叫 Virtuoso，後改 Exceptional（文章因字數取捨沒寫，這裡留紀錄，讀舊文章時會遇到）｜同上｜2026-10-03｜PDF 第 4 頁腳註 3
窄 AI 每一級都有；Level 5 窄 AI 單一任務勝過所有人；Level 5 General＝ASI｜同上｜2026-10-03｜PDF Table 1 與第 5 頁 ASI 段
同一系統可橫跨多格，建議 model card 逐項寫出表現混合｜同上｜2026-10-03｜PDF 第 4 頁
自主性六級（No AI、Tool、Consultant、Collaborator、Expert、Agent）；被能力「unlock」但不 determined by；選擇不必是能力允許的最高；AGI 不必然等於自主｜同上｜2026-10-03｜PDF Table 2、第 6.2 節與結論
原則 4「Potential, not Deployment」｜同上｜2026-10-03｜PDF 第 3 節原則 4
未提出基準；開放問題＝通用程度含哪些任務、通過多少比例；基準應為 living benchmark｜同上｜2026-10-03｜PDF 第 5 節（文章只寫開放問題，living benchmark 一句因字數刪除）
證明「不是」某級只需找出做不好的任務；通過多數題（含新任務）才可「實務上」假定具備該級｜同上｜2026-10-03｜PDF 第 5 節；文章的「列不完的任務」是對「impossible to enumerate the full set of tasks」的轉述
Marcus 五項任務：失敗一項可顯示非 AGI，通過不足以充分｜同上｜2026-10-03｜PDF Case Study 7（看懂電影、看懂小說、任意廚房做菜、10,000 行無 bug 程式、自然語言證明轉符號）。文章只舉三項並寫「如」
Morris 認為 AGI 大致有「極端風險」疑慮最可能出現在 Exceptional 與 ASI（文章未採用）｜同上｜2026-10-03｜PDF 第 6.1 節
Legg 與 Hutter 2007：非直接定義 AGI；非正式定義 intelligence measures an agent's ability to achieve goals in a wide range of environments；形式化 Υ(π)=Σ 2^(-K(μ)) V，簡單環境權重大；K 不可計算，是定義不是實用測試｜https://arxiv.org/abs/0712.3329｜2026-10-03｜PDF 第 2.6、3.3、3.5 節
Chollet 2019：只量技能不足，先備知識與資料可「buy」技能；智慧＝skill-acquisition efficiency over a scope of tasks, with respect to priors, experience, and generalization difficulty；ARC 為進行中的作品而非定論｜https://arxiv.org/abs/1911.01547｜2026-10-03｜PDF 摘要、II.1.1、II.2.1、III.2
Chollet：general intelligence 不是二分性質而是光譜；把 AGI 設為絕對目標在概念上不成立｜同上｜2026-10-03｜PDF 第 II.1.2 節結尾
Chollet：基準應不含系統或開發者事前已知的任務，並明列所假設先備知識｜同上｜2026-10-03｜PDF II.3.2
ARC Prize 官方頁：AGI＝「a system that can match the learning efficiency of humans」；稱「a system that can automate the majority of economically valuable work」是有用的目標但是 incorrect measure of intelligence（頁面對章程定義的轉述措辭與章程原文略有出入，文章用頁面原話並標明是 ARC Prize 的說法）｜https://arcprize.org/arc-agi｜2026-10-03｜直接 curl 200，全文
Shah 等 2025（Google DeepMind）以 Exceptional AGI（Level 4，99 百分位、廣泛非物理任務）為討論的能力水準，並把 superintelligence 的新風險列為 future work｜https://arxiv.org/abs/2504.01849｜2026-10-03｜PDF 第 1–2 頁。論文另有時程假設，文章不寫（本篇不預測時間）

## 編輯說明

- 正文 2,495 字（演算法同 `_body_length`）；不含 rich_paragraph 內站內連結標籤為 2,413 字。
- 圖解數字：Level 1–5、百分位 50 / 90 / 99、100%、自主性 0–5、製圖年份 2026，皆在正文或表格說明中出現。
- 示例（九成正確率的新聞）是假想情境，未實測、不指任何真實公司。
- 不寫任何模型名、價格、排行榜分數；不預測 AGI 時程；ASI 的說法只用 Morris 等人的定義並標明不是共通用法。
- SVG 為自繪向量圖，非 AI 產圖；hero 無文字、無 logo。
