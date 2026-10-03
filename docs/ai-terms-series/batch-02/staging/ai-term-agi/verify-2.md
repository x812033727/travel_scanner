# 查核紀錄 2：ai-term-agi

查核者：第二輪獨立查核（不是撰稿者，也不是第一輪查核者）。查核日 2026-10-03。所有來源今天重新打開；User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。
openai.com 直接 `curl -sSL` 仍回 403，改走 Wayback：CDX 查 `statuscode:200` 後抓 `web/<時間戳>id_/<原網址>`（章程 20260917204605，另比對 20260910185345，兩份全文相同；Planning 20261002040118；2025-10 合作公告 20260927044013；2026-04 修約公告 20260905024804）。Levels of AGI 讀了 arXiv v5、v4 與 PMLR 235 論文集版 PDF（PMLR 頁連到的 morris24b.pdf），都用 pdftotext 轉文字逐句對照。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

1. 檢查清單第 1 項「誰說的：OpenAI 與 Microsoft 在 2025 年 10 月的官方公告寫到，OpenAI 宣告 AGI 後由獨立專家小組查驗，但沒寫標準；雙方 2026 年 4 月再修約，官方公告列出的條款已不再提到 AGI。…」→「誰說的：開發者自己宣布，還是第三方查驗過？AGI 也曾被寫進公司之間的合作協議，雙方的官方公告卻沒寫出判定標準，所以不論誰宣告，都要追問依據。」，並從 sources 移除兩筆 2026-04-27 修約公告、兩筆 2025 公告標題補「2025 年 10 月」｜這是講概念的長青文章，兩家公司的合約新聞很快就會過時；第一輪的兩句今天對官方頁都正確，但會隨下一次修約失效。改成一句不會過時的話：2025-10-28 兩家公告寫明協議保留 exclusive IP rights and Azure API exclusivity until AGI，以及 Once AGI is declared by OpenAI, that declaration will now be verified by an independent expert panel，所以「曾被寫進合作協議」成立；兩頁只寫由誰宣告、誰查驗，沒寫判定標準。2026-04-27 公告全文沒有 AGI，用「曾」就不必說條款現在還在不在。新聞說「AGI 條款已取消」，官方沒這樣寫，不採用｜https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ （直接 200）、https://openai.com/index/next-chapter-of-microsoft-openai-partnership/ （Wayback 20260927044013）；修約公告查過但不再引用：https://blogs.microsoft.com/blog/2026/04/27/the-next-phase-of-the-microsoft-openai-partnership/ 、https://openai.com/index/next-phase-of-microsoft-partnership/ （Wayback 20260905024804）
2. 「證明某系統不屬於某一級，只要找到一項人類做得到、它做不好的任務」→「只要找出一般人通常做得到、它卻做不好的任務」｜第 5 節原文是 simply requires identifying tasks that people can typically do but the system cannot adequately perform，tasks 是複數，對照的是 people can typically do。同一節又說通過門檻 will probably not be 100%（broad but imperfect generality），所以「一項」做不好就證明不屬於該級，跟論文自己的說法衝突。第一輪把這點列為懷疑但沒改｜https://arxiv.org/abs/2311.02462 （v5 第 5 節；PMLR 版同句）
3. 圖解 `diagram-1.svg`：原本「解鎖」箭頭只從通用欄指向自主性 → 改成窄、通用兩欄下方共用一個括號，從括號以箭頭連到自主性欄中央，括號下寫「解鎖：兩欄的能力提升，都可能讓較高的自主性變得可行」；`<desc>` 與 pack 的圖解 alt 同步補上這點；正文在自主性段補「論文的對照表推估，窄 AI 也可能解鎖自主性 1 到 4 級，5 級只列通用 AI。」並調整句序（「但能力不決定該用哪一級…」接在後面，讓「章程則…」仍緊接自主性的對比）｜論文表 2 的 Unlocking AGI Level(s) 欄：自主性 1 級 Possible: Emerging Narrow AI／Likely: Competent Narrow AI；2 級 Possible: Competent Narrow AI／Likely: Expert Narrow AI; Emerging AGI；3 級 Likely: Expert Narrow AI; Competent AGI；4 級 Possible: Exceptional（ICML 版 Virtuoso）Narrow AI；5 級只有 Likely: Exceptional AGI; ASI。第 6.3 節：Advances in model performance and generality unlock additional interaction paradigm choices；作者自稱 Our predictions，所以正文用「推估」。原圖暗示只有通用 AI 能解鎖。重新渲染到 /tmp/ai-term-agi-d1.png（1600×900）看過：沒有壓線、超框或疊字，括號說明與左右兩段底部文字不重疊｜https://arxiv.org/abs/2311.02462 （v5 表 2、第 6.3 節）、https://proceedings.mlr.press/v235/morris24b.html （PMLR 版表 2 解鎖欄相同）

措辭修改（不計入事實修改）：
- 「Level 3 Expert 是第 90 百分位，Level 4 Exceptional 是第 99 百分位」→「至少第 90 百分位」「至少第 99 百分位」｜表 1 原文是 at least 90th／99th percentile of skilled adults，與 Level 2 的「至少」對齊，也和圖上的「以上」一致｜https://arxiv.org/abs/2311.02462
- 「AGI 是人工智慧（Artificial Intelligence）底下的說法，可先看那篇。」→「底下的概念，不熟的話可先看那篇。」｜可讀性。

## 第一輪 6 處修改的複查

1. 章程「勝過」：兩份 Wayback 快照全文相同，原句 highly autonomous systems that outperform humans at most economically valuable work。「勝過」對，修改成立。
2. Microsoft／OpenAI 公告：第一輪寫的兩句都對得上官方頁（2025-10-28 兩頁同句；2026-04-27 兩頁沒有 AGI，分潤 independent of OpenAI's technology progress），沒有寫錯。這次是因為要經得起時間才改寫，見修改 1。
3. Virtuoso／Exceptional：PMLR 論文集版 PDF 與 arXiv v4 的 Level 4 都叫 Virtuoso（表 1、表 2、結論）；v5（2025-09-24 提交）腳註 3 寫 While Level 4 was originally called "Virtuoso AGI," we now use the term "Exceptional AGI" (Shah et al., 2025)。修改成立。
4. 第 5 節：we do not propose a benchmark in this paper. Instead, we work to clarify the ontology a benchmark should attempt to measure. We also discuss properties an AGI benchmark should possess. 修改成立；開放問題（哪些任務、要通過多少比例）也在同節。
5. Marcus：Case Study 7 原文 While failing some of these tasks may indicate a system is not an AGI, it is unclear that passing them is sufficient for AGI status。五項任務內容與文章舉的三項（看懂小說、任意廚房做菜、一萬行沒有錯誤的程式）相符。修改成立。
6. Legg 與 Hutter、Chollet、ARC Prize：Legg 與 Hutter 的論文標題就是 A Definition of Machine Intelligence，第 3.5 節 a definition of machine intelligence, it is not a practical test；Chollet 定義的是 intelligence（skill-acquisition efficiency over a scope of tasks, with respect to priors, experience, and generalization difficulty）；ARC Prize 頁 The ARC Prize definition of AGI: AGI is a system that can match the learning efficiency of humans，正下方以 More formally 引 Chollet 的定義，所以表格寫「據此」有依據。修改成立。

## 隨機抽查（其餘主張的三分之一，seed 20261003 抽 26 條中的 9 條）

- Morris 等人屬 Google DeepMind：v5 作者單位全部是 Google DeepMind（Seattle、Mountain View、London）。對。
- 多數定義談能力不談機制：原則 1 The majority of definitions focus on what an AGI can accomplish, not on the mechanism。對。
- 「哪些任務」「跟哪些人比」：Case Study 4 ambiguity around choices such as "what tasks?" and "which people?"。對。
- Chollet：先備知識與訓練資料能「buy」技能並 masks the system's own generalization power（摘要）。對。
- Chollet 的智慧定義含先備知識、經驗、泛化難度（II.2.1）。對。
- Level 1–3 的門檻：equal to or somewhat better than an unskilled human／at least 50th／at least 90th percentile of skilled adults。對（並補上「至少」，見措辭修改）。
- 系統可橫跨多格、建議 model card 寫出表現混合：documentation for frontier AI models, such as model cards, should detail this mixture of performance levels。對。
- Level 5 窄 AI：AlphaFold 是 Level 5 Narrow AI（Superhuman Narrow AI）。對。
- 示例裡「Chollet 稱這能『買到』分數」：第 II.1.3 節原文 "buy" unbounded performance on any given task。「分數」是 performance 的轉述，意思沒變。對。

抽樣以外也重讀了：Shah 等 2025 第 1 節以 Exceptional AGI (Level 4) 為範圍，把 novel risks from superintelligence 留作 future work；Chollet 的 general intelligence 是 spectrum、絕對意義的 AGI conceptually unsound；ARC is a work in progress, not a definitive solution；Planning for AGI and beyond（2023-02-24）的 AI systems that are generally smarter than humans；Case Study 6 對章程的三點評語；原則 4 Potential, not Deployment；arXiv 三篇的提交日期（2007-12-20、2019-11-05、2025-04-02）。都對。

## 耐久性與可讀性

- 正文出現的年份都是文件的發表或修訂年份（2007、2019、2023、2024、2025；另有指派連結的文章標題含 2026），不會隨新聞過時；合約條款、公司名與日期已從檢查清單拿掉。沒有任何 AGI 時程預測。
- 從頭讀過一遍：段落順序、6 個 H2、1 個表、1 個 callout、5 個指派連結都沒變；新加的一句放在「能力越強越能解鎖」之後，句序調過，讓「章程則把高度自主寫進定義」仍緊接在「不決定該用哪一級」之後。
- 系列規矩：沒有型號、價格、截止日期、排行榜分數；示例標了「示例（假想情境，未實測）」；沒有推論／推理用詞；台灣用語。圖上數字（Level 1–5、50／90／99、100%、自主性 0–5、製圖年份 2026）正文都有；新圖沒有加新數字。
- 正文 2,656 字（`app.guides.pack_ingest._body_length` 實算；第一輪後為 2,651）。
- dry-run：`cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest --from ../../docs/ai-terms-series/batch-02/staging --slug ai-term-agi --dry-run` 通過（exit 0），只有 `no_summary` 警告（之前就有）。
- `notes.md` 與 `research.json` 已同步：合約句的新依據、兩筆修約公告改列「查過未引用」、PMLR 版讀法、表 2 解鎖欄、`running_text_characters` 2656。

## 我懷疑但沒改的事

- `no_summary` 警告：沒有摘要區塊。加摘要會改結構，不在查核範圍。
- 圖說「右邊的自主性是另一條軸，由部署方式決定」：論文說的是 system designers and end-users will settle on a mode of human-AI interaction，摘要也把 autonomy 歸在 deployment considerations，所以意思沒錯，只是比原文籠統，沒改。
- 「AGI 也曾被寫進公司之間的合作協議」：官方依據只有 Microsoft 與 OpenAI 這一例；中文不分單複數，不算誇大，但讀者看不出是哪兩家，要看文末來源才知道。
- 「九種說法」那段的例子「機器有沒有意識」對應 Case Study 2 的 strong AI，論文的重點是沒有科學共識能判斷機器有沒有意識，文章只當例子列出，沒有展開，沒改。

facts_changed: 3
