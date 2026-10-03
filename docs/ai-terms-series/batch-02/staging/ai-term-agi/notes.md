# 查證與編輯紀錄：ai-term-agi

格式：主張｜來源網址｜查證日｜讀取方式。查證日皆為 2026-10-03（本批開工日，實際打開頁面的日期）。

## 讀取方式說明

- arXiv：`curl -sSL` 讀 `https://arxiv.org/abs/<id>`（摘要與版本日期），再讀 `https://arxiv.org/pdf/<id>` 以 pdftotext 轉文字核對原文。Levels of AGI 讀的是 v5（2025-09-24 修訂）；ICML 2024 論文集頁（PMLR 235）另開確認發表處。
- openai.com 三頁（章程、Planning for AGI and beyond、Microsoft 合作公告）直接 curl 與 WebFetch 皆回 403。改用 Wayback：CDX 查 `statuscode:200`，抓 `web/<時間戳>id_/<原網址>` 並加 `--compressed`。章程快照 20260917204605（另比對 20260910185345，全文相同）、Planning 快照 20261002040118、Microsoft 公告快照 20260927044013。`sources` 寫原網址。章程定義句另用 WebSearch 限定 openai.com 交叉確認措辭一致。
- 2026-04-27 雙方修約公告（https://blogs.microsoft.com/blog/2026/04/27/the-next-phase-of-the-microsoft-openai-partnership/ 直接 200；https://openai.com/index/next-phase-of-microsoft-partnership/ Wayback 20260905024804）今天讀過全文：沒有 AGI、專家小組或判定標準，分潤寫成 independent of OpenAI's technology progress。第二輪查核把合約內容縮成一句不會過時的話（AGI「曾」被寫進合作協議、官方公告沒寫判定標準），所以這兩頁不再列進 `sources`，只記在這裡。新聞稱修約「取消 AGI 條款」，官方沒這樣寫，文章不採用。
- Levels of AGI 另讀 ICML／PMLR 235 論文集版 PDF（https://raw.githubusercontent.com/mlresearch/v235/main/assets/morris24b/morris24b.pdf，由 PMLR 頁連結）：Level 4 叫 Virtuoso，表 2 的解鎖欄與 v5 相同，只差名稱。
- Microsoft 官方部落格公告、ARC Prize 官方頁、PMLR：直接 curl 回 200，讀完整文字。
- 查不到或只在二手轉述的內容一律不寫。Gubrud 1997 原文（foresight.org）404、Wayback 被擋，所以文章沒有寫 AGI 一詞的起源，只在這裡記一筆。

## 主張對照

OpenAI 章程把 AGI 寫成「highly autonomous systems that outperform humans at most economically valuable work」｜https://openai.com/charter/｜2026-10-03｜Wayback 20260917 快照全文
OpenAI 2023 年文章把 AGI 寫成「AI systems that are generally smarter than humans」，全文沒有判定方法｜https://openai.com/index/planning-for-agi-and-beyond/｜2026-10-03｜Wayback 20261002 快照全文，搜尋 measure、benchmark、define 無相關句
該文另寫「The first AGI will be just a point along the continuum of intelligence」（文章未採用，字數取捨）｜同上｜2026-10-03｜同上
檢查清單第 1 項：AGI 曾被寫進公司之間的合作協議，雙方官方公告沒寫判定標準。依據是 2025-10-28 兩家公告的「continues to have exclusive IP rights and Azure API exclusivity until Artificial General Intelligence (AGI)」與「Once AGI is declared by OpenAI, that declaration will now be verified by an independent expert panel」，兩頁都沒寫小組用什麼標準｜https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ 與 https://openai.com/index/next-chapter-of-microsoft-openai-partnership/｜2026-10-03｜Microsoft 直接讀取；OpenAI 版 Wayback 20260927 快照，兩頁內容相同。文章不寫公司名、日期與任何具體條款；用「曾」是因為 2026-04 修約公告已不再提 AGI（見上方讀取方式）
Morris 等人在 ICML 2024 發表（PMLR 235）立場論文，檢視九種既有說法（圖靈測試、強 AI／意識、類比人腦、人類認知任務、學習任務能力、經濟價值工作、Coffee Test 類、Artificial Capable Intelligence、前沿 LLM 即 AGI）｜https://arxiv.org/abs/2311.02462 與 https://proceedings.mlr.press/v235/morris24b.html｜2026-10-03｜PDF v5 第 2–3 頁 Case Studies 1–9
多數說法談能力而非機制，且「what tasks?」「which people?」有歧義｜同上｜2026-10-03｜PDF Case Study 4 與原則 1
AGI 概念連到目標、預測與風險｜同上｜2026-10-03｜PDF 第 1 頁 Goals / Predictions / Risks
Morris 評章程定義：只看表現不問機制、經濟價值可當量尺；缺點是無明確經濟價值的能力、且隱含需部署｜同上｜2026-10-03｜PDF Case Study 6
Levels of AGI 兩軸：performance（深度）與 generality（廣度）；Narrow＝clearly scoped task or set of tasks；General＝wide range of non-physical tasks, including metacognitive tasks like learning new skills｜同上｜2026-10-03｜PDF Table 1 與第 4 節
表現五級：Emerging 等於或略優於 unskilled human；Competent 至少第 50 百分位；Expert 第 90；Exceptional 第 99；Superhuman 勝過 100% 的人；百分位對照 skilled adults｜同上｜2026-10-03｜PDF Table 1 與第 4 節文字
Level 4 在 ICML／PMLR 版與 arXiv v1–v4 叫 Virtuoso，2025-09-24 的 v5 改稱 Exceptional（沿用 Shah 等 2025）；文章在 Level 4 處註明｜同上｜2026-10-03｜v5 PDF 第 4 頁腳註 3；PMLR PDF Table 1
窄 AI 每一級都有；Level 5 窄 AI 單一任務勝過所有人；Level 5 General＝ASI｜同上｜2026-10-03｜PDF Table 1 與第 5 頁 ASI 段
同一系統可橫跨多格，建議 model card 逐項寫出表現混合｜同上｜2026-10-03｜PDF 第 4 頁
自主性六級（No AI、Tool、Consultant、Collaborator、Expert、Agent）；被能力「unlock」但不 determined by；選擇不必是能力允許的最高；AGI 不必然等於自主｜同上｜2026-10-03｜PDF Table 2、第 6.2 節與結論
表 2 的 Unlocking AGI Level(s) 欄：自主性 1–4 級列有窄 AI（Emerging／Competent／Expert／Exceptional Narrow AI，Possible 或 Likely），5 級只列 Exceptional AGI 與 ASI；作者稱這是他們的 predictions。正文寫「論文的對照表推估」，圖解改成兩欄共用括號再連到自主性｜同上｜2026-10-03｜v5 與 PMLR PDF Table 2、第 6.3 節
原則 4「Potential, not Deployment」｜同上｜2026-10-03｜PDF 第 3 節原則 4
未提出基準，而是釐清基準該量什麼（ontology）並討論 AGI 基準應具備的性質；開放問題＝通用程度含哪些任務、通過多少比例；基準應為 living benchmark｜同上｜2026-10-03｜PDF 第 5 節（living benchmark 一句因字數未寫）
證明「不是」某級只需找出 people can typically do、系統做不好的 tasks（複數）；通過多數題（含新任務）才可「實務上」假定具備該級，門檻多半不是 100%｜同上｜2026-10-03｜PDF 第 5 節。文章寫「找出一般人通常做得到、它卻做不好的任務」，不寫「一項」，因為論文也說通過比例 probably not 100%；「列不完的任務」轉述 impossible to enumerate the full set of tasks
Marcus 五項任務：failing some of these tasks may indicate a system is not an AGI, it is unclear that passing them is sufficient｜同上｜2026-10-03｜PDF Case Study 7（看懂電影、看懂小說、任意廚房做菜、10,000 行無 bug 程式、自然語言證明轉符號）。文章只舉三項並寫「如」
Morris 認為 AGI 大致有「極端風險」疑慮最可能出現在 Exceptional 與 ASI（文章未採用）｜同上｜2026-10-03｜PDF 第 6.1 節
Legg 與 Hutter 2007：非直接定義 AGI；非正式定義 intelligence measures an agent's ability to achieve goals in a wide range of environments；形式化 Υ(π)=Σ 2^(-K(μ)) V，簡單環境權重大；K 不可計算，是定義不是實用測試｜https://arxiv.org/abs/0712.3329｜2026-10-03｜PDF 第 2.6、3.3、3.5 節
Chollet 2019：只量技能不足，先備知識與資料可「buy」技能；智慧＝skill-acquisition efficiency over a scope of tasks, with respect to priors, experience, and generalization difficulty；ARC 為進行中的作品而非定論｜https://arxiv.org/abs/1911.01547｜2026-10-03｜PDF 摘要、II.1.1、II.2.1、III.2
Chollet：general intelligence 不是二分性質而是光譜；把 AGI 設為絕對目標在概念上不成立｜同上｜2026-10-03｜PDF 第 II.1.2 節結尾
Chollet：基準應不含系統或開發者事前已知的任務，並明列所假設先備知識｜同上｜2026-10-03｜PDF II.3.2
ARC Prize 官方頁：AGI＝「a system that can match the learning efficiency of humans」，定義下方直接引 Chollet 的正式定義（文章的「據此」）；稱「a system that can automate the majority of economically valuable work」是有用的目標但是 incorrect measure of intelligence（頁面對章程定義的轉述措辭與章程原文略有出入，文章用頁面原話並標明是 ARC Prize 的說法）｜https://arcprize.org/arc-agi｜2026-10-03｜直接 curl 200，全文
Shah 等 2025（Google DeepMind）以 Exceptional AGI（Level 4，99 百分位、廣泛非物理任務）為討論的能力水準，並把 superintelligence 的新風險列為 future work｜https://arxiv.org/abs/2504.01849｜2026-10-03｜PDF 第 1–2 頁。論文另有時程假設，文章不寫（本篇不預測時間）

## 編輯說明

- 正文 2,656 字（第二輪查核後以 `app.guides.pack_ingest._body_length` 實算）；不含 rich_paragraph 內站內連結標籤為 2,574 字。
- 圖解數字：Level 1–5、百分位 50 / 90 / 99、100%、自主性 0–5、製圖年份 2026，皆在正文或表格說明中出現。
- 圖解的「解鎖」：原本只有一支箭頭從通用欄指向自主性，會被讀成只有通用 AI 能解鎖；第二輪改成窄與通用兩欄下方共用一個括號，再以箭頭連到自主性欄中央，括號下寫「解鎖：兩欄的能力提升，都可能讓較高的自主性變得可行」。
- 示例（九成正確率的新聞）是假想情境，未實測、不指任何真實公司。
- 不寫任何模型名、價格、排行榜分數；不預測 AGI 時程；ASI 的說法只用 Morris 等人的定義並標明不是共通用法。
- SVG 為自繪向量圖，非 AI 產圖；hero 無文字、無 logo。
