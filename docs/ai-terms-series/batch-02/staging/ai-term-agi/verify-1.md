# 查核紀錄 1：ai-term-agi

查核者：獨立查核（非撰稿者）。查核日 2026-10-03。所有來源今天重新打開；User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。
openai.com 直接 `curl -sSL` 回 403，改走 Wayback：CDX 查 `statuscode:200` 後抓 `web/<時間戳>id_/<原網址>`（章程 20260917204605、Planning 20261002040118、2025-10 合作公告 20260927044013、2026-04 修約公告 20260905024804）。arXiv 讀 abs 頁的版本紀錄，再用 pdftotext 讀 PDF 全文；Levels of AGI 讀了 v5 與 v1，另讀 PMLR 235 論文集版 PDF。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

1. 導言「有的看能否取代有經濟價值的工作」→「有的看在多數有經濟價值的工作上能否勝過人類」｜章程原文是 outperform humans at most economically valuable work，是「勝過」不是「取代」；「取代」是勞動替代（需要部署），正是 Morris 等人拿來和章程區分的概念｜https://openai.com/charter/ （Wayback 20260917204605）
2. 檢查清單第 1 項「…由獨立專家小組查驗，但沒寫標準，仍要追問依據。」→「…但沒寫標準；雙方 2026 年 4 月再修約，官方公告列出的條款已不再提到 AGI。不論誰宣告，都要追問依據。」並在 sources 加兩筆 2026-04-27 官方公告｜2025-10 公告的句子本身正確（兩家官方頁同句），但 2026-04-27 雙方又宣布修約，兩家官方公告全文都沒有 AGI 或專家小組，只寫分潤「independent of OpenAI's technology progress」。只寫 2025 年那句會讓讀者以為那仍是現行安排。新加的句子只陳述公告寫了什麼，不寫「AGI 條款已刪除」（那是新聞的解讀，官方沒說）｜https://blogs.microsoft.com/blog/2026/04/27/the-next-phase-of-the-microsoft-openai-partnership/ （直接 200）、https://openai.com/index/next-phase-of-microsoft-partnership/ （Wayback 20260905024804）、https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/
3. 「Level 4 Exceptional 是第 99 百分位，」→ 加「（ICML 論文集版稱 Virtuoso，2025 年的 arXiv 修訂版改名）」｜文章把論文標為 ICML 2024，但 ICML／PMLR 235 版與 arXiv v1–v4 的 Level 4 叫 Virtuoso；Exceptional 是 2025-09-24 的 v5 才改的（v5 版本註記與腳註 3；名稱沿用 Shah 等 2025）。讀者打開 ICML 版會對不上｜https://arxiv.org/abs/2311.02462 、https://proceedings.mlr.press/v235/morris24b.html
4. 「Morris 等人沒有提出 AGI 基準，只列出開放問題」→「沒有提出 AGI 基準，而是討論基準該量什麼、該具備哪些性質，並列出開放問題」｜第 5 節原文：we do not propose a benchmark… Instead, we work to clarify the ontology a benchmark should attempt to measure. We also discuss properties an AGI benchmark should possess.「只」不正確｜https://arxiv.org/abs/2311.02462
5. 「Marcus 提出的五項任務…：失敗一項可說明還不是，全過也不足以說明是。」→「論文指出，沒通過其中幾項可能表示還不是，全部通過卻不一定足以說明是。」｜Case Study 7 原文：failing some of these tasks may indicate a system is not an AGI, it is unclear that passing them is sufficient。原句把「不確定是否足夠」寫成「不足以」，把「可能表示」寫成「可說明」｜https://arxiv.org/abs/2311.02462
6. 定義表「Legg 與 Hutter｜在廣泛環境中達成目標」→「定義機器智慧：在廣泛環境中達成目標」；「Chollet、ARC Prize｜技能習得效率」→「Chollet 定義智慧是技能習得效率，ARC Prize 據此定義 AGI」｜正文正確寫了 Legg 與 Hutter 定義的是機器智慧，但表格「怎麼定義」欄在 AGI 定義對照表裡沒標明，會被讀成 AGI 定義；Chollet 同樣定義的是 intelligence，給 AGI 定義的是 ARC Prize 頁｜https://arxiv.org/abs/0712.3329 、https://arxiv.org/abs/1911.01547 、https://arcprize.org/arc-agi

措辭修改（不計入事實修改）：
- 「但不一定有明確經濟價值的能力沒被涵蓋」→「但像藝術創意這類沒有明確經濟價值的能力未必量得進去」｜原文說這些能力 may be indirectly accounted for…remains unclear，語氣放軟並補上原文的例子｜https://arxiv.org/abs/2311.02462
- 「在陌生廚房做菜」→「在任意一間廚房做菜」｜原文 cooking in an arbitrary kitchen｜同上
- 來源標題補「v5，2025 年修訂」，標出讀的是哪一版｜同上
- 圖解 `diagram-1.svg`「設計者可以刻意選低一級」→「設計者可以刻意選較低的級別」｜原文是 lower levels of autonomy may be desirable，不限於低一級；重新渲染確認沒有壓線或超框｜同上
- 圖解的 alt「Level 1 到 Level 5 對應 50、90、99 百分位與勝過 100% 的人」→ 改為 Level 2 到 4 對應三個百分位、Level 5 勝過 100% 的人｜Level 1 沒有百分位（原文對照的是沒有技能的人），原本五級對四個值｜同上

## 查過、沒問題的主要主張

- 章程的 AGI 定義句與中譯「高度自主、在多數具經濟價值的工作上勝過人類的系統」逐字相符；「章程把高度自主寫進定義」正確（Wayback 20260917204605）。
- Planning for AGI and beyond（2023-02-24）寫 AI systems that are generally smarter than humans；全文搜 measure、test、criteria、declare、threshold，沒有 AGI 的判定方法。
- 2025-10-28 的 Microsoft 部落格與 OpenAI 官方頁都有同一句 Once AGI is declared by OpenAI, that declaration will now be verified by an independent expert panel；兩頁都沒寫小組的標準。文章沒有引用公告裡的其他合約條款（IP、分潤、2030、2032、算力門檻都沒寫）。
- Morris 等：Google DeepMind 作者群；ICML 2024 立場論文（PMLR 235:36308–36321）；九個案例（圖靈測試、強 AI／意識、類比人腦、人類認知任務、學習任務、經濟價值工作、Coffee Test／Marcus、ACI、前沿 LLM）；目標、預測、風險三者；Case Study 6 對章程的優缺點（不問機制、經濟價值可當量尺、隱含需要部署）；原則 1 與原則 4。
- 兩軸：performance＝depth、generality＝breadth；Narrow＝clearly scoped task or set of tasks；General＝wide range of non-physical tasks, including metacognitive tasks like learning new skills；Level 1 等於或略優於沒有技能的人，Level 2/3/4 至少第 50/90/99 百分位（skilled adults），Level 5 勝過 100% 的人；「表現分五級」與結論的 five levels of performance 相符（另有 Level 0 No AI 列，不影響）。
- 系統可橫跨多格、建議 model card 寫出表現分布；Level 5 窄 AI（AlphaFold 例）；ASI＝Level 5 General，是本論文的定義。
- 自主性六級（No AI、Tool、Consultant、Collaborator、Expert、Agent）；capabilities unlock but do not determine；選擇不必是能力允許的最高；結論 AGI is not necessarily synonymous with autonomy。
- 不對稱：Determining that something is not an AGI… simply requires identifying tasks…；It is impossible to enumerate the full set of tasks；Marcus 的五項任務內容。
- Legg 與 Hutter（arXiv 2007-12）：非正式定義 Intelligence measures an agent's ability to achieve goals in a wide range of environments；Υ(π) 以 2^-K(μ) 加權，越簡單權重越大；K 不可計算；第 3.5 節 a definition of machine intelligence, it is not a practical test。
- Chollet（2019）：先備知識與訓練資料可「buy」技能、掩蓋泛化能力；智慧＝skill-acquisition efficiency over a scope of tasks, with respect to priors, experience, and generalization difficulty；general intelligence is not a binary property… It is a spectrum；把絕對意義的 AGI 當目標 conceptually unsound；ARC is a work in progress, not a definitive solution。
- ARC Prize 頁：The ARC Prize definition of AGI: AGI is a system that can match the learning efficiency of humans；把 "a system that can automate the majority of economically valuable work" 稱為 a useful goal 但 an incorrect measure of intelligence；「基金會」由 arcprize.org/about（ARC Prize Foundation is a non-profit）支持。
- Shah 等 2025（Google DeepMind）：以 Exceptional AGI（Level 4，99 百分位、廣泛非物理任務）為討論水準，把 novel risks from superintelligence 留作 future work。論文的時程假設文章沒寫。
- 系列規矩：沒有型號、價格、截止日期、排行榜分數；全文沒有任何 AGI 時程預測（正文、表格、圖、alt 都查過）；九成正確率的例子標了「示例（假想情境，未實測）」；沒有推論／推理用詞；定義分歧兩邊都寫並標明是誰的說法；台灣用語；圖上數字（Level 1–5、50／90／99、100%、自主性 0–5）正文都有。
- 指派連結五個都在；sources 每筆網址今天打開（openai.com 三＋一頁經 Wayback，其餘直接 200），標題相符。
- 改後正文 2,651 字（`_body_length`，原 2,495）；6 個 H2、1 個表、1 個 callout 不變。dry-run 通過，只有 `no_summary` 警告（改前就有）。

## 我懷疑但沒改的事

- 新聞（unite.ai、monkfrom.earth 等）說 2026-04 修約「取消了 AGI 條款」、專家小組不再有作用；兩家官方公告只是不再提 AGI，沒有明說，所以文章只寫「公告不再提到 AGI」，沒有寫條款被刪。
- `research.json` 的 `running_text_characters` 仍是 2495（現在是 2651），`notes.md` 與 `research.json` 也還沒記 2026-04 修約公告與兩筆新來源；這兩個檔不在查核者可寫的範圍。
- dry-run 的 `no_summary` 警告：沒有摘要區塊。加摘要會改結構，不在查核範圍，留給撰稿者或編輯決定。
- 圖解的「解鎖」箭頭只從通用欄指向自主性，但論文表 2 裡窄 AI 也會解鎖 1–4 級自主性；這是視覺簡化，沒改。
- 「證明不屬於某一級，只要找到一項…任務」：原文是 identifying tasks（複數）；意思沒變，沒改。

facts_changed: 6
