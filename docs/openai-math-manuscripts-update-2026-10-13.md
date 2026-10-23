# OpenAI 數學手稿既刊稿五語更正工作單（2026-10-13）

## 範圍與目前證據

- 目標：已刊 `ai-news-openai-math-manuscripts-20261006`，路徑 `/{zh-TW,zh-CN,en,ja,ko}/life/ai-news-openai-math-manuscripts-20261006`。本文記錄逐語改稿、後台版本、審稿、發布稽核與公開頁讀回。
- 2026-10-13 修改前唯讀公開頁核對：五語原標題、描述、摘要、首段、數量表與 FAQ 都以「722」呈現，沒有交代 10/07 後現存 719。五語原文把 AGMAI 轉述 OpenAI 宣稱「數百個問題」寫成 AGMAI 自己認定；來源僅列 10/07 查證的 The Verge，驗證提示與 FAQ 因而寫「資訊僅來自 The Verge」。
- **已刊五語沒有「42% 未形式化」或「10 份完整思考過程」錯句**。那兩句只出現在已退件的重複新聞候選 `62a29197-da43-4d14-a30d-8a3f8aca341f`；不可把候選草稿複製進既刊稿。
- 本篇 Guide ID：`0fe56758-5ac9-468e-b86e-71dabc7e0cd4`。管理員編輯器於修改前顯示五語草稿／已發皆為 v2；2026-10-13 五語逐一保存、三輪獨立審稿後發布，五個公開頁及 `guide_article_published` 稽核逐語讀回。版本與時間見下表。
- 搜尋同題時另見**另一篇已刊五語** `ai-news-openai-math-manuscripts-20261007`，Guide ID `e31a32b6-2f93-4a7a-ba45-ecc729e138b6`。該篇 zh-TW 標題／描述／摘要／內文／表格／FAQ 仍有 `162/722` 約 `22%` 的舊 Lean 形式化數字；OpenAI 官方 10/07 修訂紀錄現列主要結果 `300/719` 約 `42%` 已形式化。該 Guide 的分類還勾選「加密貨幣與區塊鏈」且附加密資產免責段，需另票釐清；**本票只編輯 10/06 Guide**。

## 一手來源與可寫的事實

| 來源 | 2026-10-13 核得內容 | 編輯界線 |
| --- | --- | --- |
| [OpenAI 10/06 原始儲存庫 README，鎖定 `adc7f124` 版本](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) | 初版列 722 份手稿、372 個結果家族；列出 10 個結果的刪節版推理摘要；說有些結果未有 Lean 形式化。此 commit 日期經 GitHub 讀為 2026-10-06T21:58:50Z。 | 722 必加「10/06 首發」或同等時點，不寫成現存數量。 |
| [OpenAI 10/07 修訂紀錄](https://github.com/openai/math/blob/main/history.md) | 一處符號錯誤使 3 份相依手稿撤回；另有 14 份手稿修補；另有 13 份更新引用。新加 6 項形式化及 5 項輔助成果後，主要結果形式化比例列為 **300／719，約 42%**。 | 42% 是「已形式化」覆蓋率；不能倒寫成未形式化，不能當成整批自然語言證明已獲獨立審核。 |
| [OpenAI 現行 README](https://github.com/openai/math/blob/main/README.md) | 現行目錄 719 份、372 個結果家族；說明不同成果處於不同驗證階段，未形式化成果可能有問題；推理摘要列 10 個結果。 | `main` 會變；發佈前重看，必要時釘住 commit。 |
| [OpenAI 10/06 公告](https://openai.com/index/sharing-ai-progress-in-mathematics/) | 公告 repo、Lean 形式化、**10 份模型推理摘要**及平均約三小時 ChatGPT Pro thinking 等效算力；與 AGMAI 諮詢。 | 公告用 `summaries of the model's reasoning`，repo 寫 `abridged summaries`；不是每份手稿的完整思考過程。 |
| [AGMAI 10/06 聲明](https://agmai.org/)與[9/29 建議](https://agmai.org/general-sep29/) | AGMAI 說 OpenAI **報稱**提出數百個未解問題的解答；其諮詢不代表評價成果影響或背書取得過程，仍由數學界評估。它是獨立的 Institute for Advanced Study 顧問團，並非普林斯頓大學的組織。 | 不寫「AGMAI 證實數百個問題已解」。如提及機構，譯成「高等研究院／Institute for Advanced Study」，不寫普林斯頓大學附屬。 |
| [Bastounis 等原始論文，arXiv:2610.08144](https://arxiv.org/abs/2610.08144) | 研究特定的 OpenAI Navier–Stokes 自然語言與 Lean 證明落差，作者指出該例的形式化未對應原自然語言論證。 | 該論文**不是**這 719 份手稿的逐篇審核；若引入正文，須點名特定案例及論文作者主張，不能推論整批被駁倒。最小更正可暫不加入。 |

## 後台欄位對照與關卡

五語公開頁的同一舊說法會重複於：`title`、`description`、`summary` 前兩項、「發生了什麼事／What happened」首段、「公布方式／How it was released」段落與表格的手稿數、附帶資料和 AGMAI 行、驗證提醒、FAQ「本次公布什麼／是否證實」及來源。**每處都要按語言同時改**；保留文章的其餘新聞脈絡，避免把 10/06 的 722 直接全域取代成 719。

公開唯讀 `/api/travel/guides/life/ai-news-openai-math-manuscripts-20261006?locale=<語言>` 的五語 `document.blocks` 型別序列一致。零起算的重點索引是 `0 summary`、`2 首段 paragraph`、`5 揭露段 paragraph`、`6 table`、`10 驗證 callout`、`13 faq`；`title`、`description`、`sources` 在 block 外。這只是公開版索引，操作前仍要以管理員草稿讀回為準。

1. 在 `/zh-TW/admin/guides` 用完整 slug 搜尋，記 Guide ID、五語 `draft version`、`published version`、既有來源及最近修訂理由。若草稿已較公開頁新，以草稿為基底，不覆蓋他人更動。
2. 各語先更新 `title`／`description`／摘要／首段／數量表／驗證提示／FAQ，加入下面對應的文字。其他段落保留原文，但把「僅 The Verge」改成新的已核來源組合。
3. `sources` 至少補初版 OpenAI README、10/07 `history.md`、現行 README、OpenAI 公告、AGMAI 聲明；設定實際查證日期 2026-10-13。若使用 arXiv 批評，須另經數學內容人工覆核並精確限定案例。來源標題要符合各語文章語言。
4. 逐語由另一位審閱者對照上述一手頁、校正文法及術語，核 722／719／300、撤回 3 與另修 14、10 份摘要的單位、AGMAI 非背書立場。獨立審閱者先核核心五語文案與一手事實，再逐欄核管理員實存 v3；第二輪 en PASS、其餘四語因 AGMAI 措辭和來源標題 FAIL。四語實存 v4 修正後，第三輪以本工作單的完整 v3 加下方 v4 差異逐欄核對，五語 PASS，才進入發布。此獨立覆核針對文件所記完整草稿文案與一手來源；管理員儲存版本與公開頁另由操作員讀回。既刊 Guide 管理頁的程序是版本化草稿保存與理由／確認發布；新聞候選 AI judge 並非這個 Guide 的發布關卡。
5. 每語保存後讀回草稿版本，使用管理頁預覽及檢查，填具體更正原因發布；讀回 `published version`、`published` 修訂記錄和相同語公開頁。任何版本衝突、429、審閱失敗或公開頁舊內容都不能算完成。

## 各語可貼入的核心文案

以下句子可分配到各語的描述、摘要、首段與 FAQ；表格數量行應簡化為「10/06 首發 722；10/07 後現存 719；372 個結果家族」，附帶資料行標為「10 個結果的刪節版推理摘要、算力估計、嘗試問題數統計」。不要將整段塞進單一 SEO 欄位。

### zh-TW

- 建議標題：`OpenAI 首發 722 份數學手稿，修訂後現存 719 份：學界仍待驗證`
- 建議描述：`OpenAI 10 月 6 日首發 722 份數學手稿，10 月 7 日撤回 3 份並修訂另外 14 份，現存 719 份。官方儲存庫稱主要結果約 42% 已形式化；AGMAI 強調其諮詢不構成背書。`
- 時序／形式化：`OpenAI 於 10 月 6 日首發 722 份數學手稿，分屬 372 個結果家族。其 10 月 7 日修訂紀錄顯示，一處符號錯誤導致 3 份手稿撤回，另有 14 份修訂；現存 719 份。OpenAI 儲存庫將主要結果的形式化比例列為 300／719（約 42%）。這是已形式化的比例，不代表整批自然語言證明已獲獨立驗證。`
- AGMAI：`AGMAI 轉述 OpenAI 報稱提出數百個未解問題的解答，但明言其諮詢不構成對成果影響或產出過程的背書；成果仍須由數學界評估。`
- 推理摘要：`OpenAI 另公開涵蓋 10 個結果的刪節版模型推理摘要，以及算力估計與嘗試問題數統計；這不是每份手稿的完整思考過程。`
- 驗證提示／FAQ：`截至本次核對，OpenAI 儲存庫列有部分主要結果的 Lean 形式化，AGMAI 則保留學界評估的立場；不能把形式化比例讀成所有解答已獲獨立確認。`

### zh-CN

- 建议标题：`OpenAI 首发 722 份数学手稿，修订后现存 719 份：仍待学界验证`
- 建议描述：`OpenAI 10 月 6 日首发 722 份数学手稿，10 月 7 日撤回 3 份并修订另外 14 份，现存 719 份。官方仓库称主要结果约 42% 已形式化；AGMAI 强调其顾问工作不构成背书。`
- 时序／形式化：`OpenAI 于 10 月 6 日首次发布 722 份数学手稿，分属 372 个结果家族。其 10 月 7 日修订记录显示，一处符号错误导致 3 份手稿被撤回，另有 14 份经过修订；现存 719 份。OpenAI 仓库将主要结果的形式化比例列为 300／719（约 42%）。这是已形式化的比例，不代表整批自然语言证明已获独立验证。`
- AGMAI：`AGMAI 转述 OpenAI 声称提出数百个未解问题的解答，但明确表示其顾问工作不构成对成果影响或研究过程的背书；成果仍须由数学界评估。`
- 推理摘要：`OpenAI 另公布涵盖 10 个结果的删节版模型推理摘要，以及算力估计和尝试问题数的统计；这不是每份手稿的完整思考过程。`
- 验证提示／FAQ：`截至本次核查，OpenAI 仓库列有部分主要结果的 Lean 形式化，AGMAI 则认为仍需数学界评估；不能把形式化比例理解为所有解答均获独立确认。`

### en

- Suggested title: `OpenAI Initially Released 722 Math Manuscripts; 719 Remain After Revisions`
- Suggested description: `OpenAI released 722 math manuscripts on October 6. Three withdrawals and 14 other revisions on October 7 left 719. Its repository says about 42% of top-line results are formalized; AGMAI says its advisory role is not an endorsement.`
- Timeline / formalization: `OpenAI initially published 722 math manuscripts across 372 result families on October 6. Its October 7 history records three withdrawals after a sign error and revisions to 14 other manuscripts, leaving 719. The repository says 300/719 top-line results, about 42%, are formalized. That is the formalized share, not a measure of independent validation of every natural-language proof.`
- AGMAI: `AGMAI described OpenAI as reporting solutions to hundreds of open questions. It said its advisory role was neither an endorsement of the process nor a judgment of the results' impact; assessment remains with the mathematics community.`
- Reasoning summaries: `OpenAI also released abridged summaries of the model's reasoning for ten listed results, alongside compute estimates and statistics on attempted problems. These are not full reasoning records for every manuscript.`
- Verification note / FAQ: `The repository includes Lean formalizations for some top-line results, while AGMAI says the mathematics community must assess the work. The formalization share should not be read as independent confirmation of every result.`

### ja

- 見出し案：`OpenAIの数学原稿、初回722本から719本に：撤回後も学界の評価待ち`
- 説明文案：`OpenAIは10月6日に数学原稿722本を公開し、10月7日に3本を撤回、別の14本を修正した。現行の収録数は719本。主要結果の約42％が形式化済みという数字はOpenAI側の記載で、AGMAIの助言は成果の影響に対する評価や、その生成過程への支持を意味しない。`
- 時系列／形式化：`OpenAIは10月6日に372の成果群（ファミリー）に属する722本の数学原稿を公開した。10月7日の改訂記録によると、符号の誤りを受けて3本を取り下げ、別の14本を修正し、現行の収録数は719本となった。リポジトリは主要結果の形式化率を300／719（約42％）と記している。これは形式化済みの割合であり、自然言語の証明すべてが独立に検証された割合ではない。`
- AGMAI：`AGMAIは、OpenAIが数百の未解決問題への解答を報告したと説明した。同時に、助言は成果の影響に対する評価や研究過程への支持を意味せず、判断は数学界に委ねられると明言している。`
- 推論要約：`OpenAIは、一覧に挙げた10の結果についてモデルの推論を短くまとめた資料も公開し、計算量の推定や試行した問題数の統計も示した。各原稿の完全な思考過程を公開したという意味ではない。`
- 検証注記／FAQ：`リポジトリには一部の主要結果にLean形式化があるが、AGMAIは評価を数学界に委ねている。形式化率を全結果の独立検証率とみなすことはできない。`

### ko

- 제목 제안：`OpenAI 수학 원고, 최초 722편에서 719편으로: 철회 후에도 학계 검토 중`
- 설명 제안：`OpenAI는 10월 6일 수학 원고 722편을 공개했고, 10월 7일 3편을 철회하고 다른 14편을 수정했다. 현재 목록에는 719편이 남아 있다. 주요 결과 약 42%가 형식화됐다는 수치는 OpenAI 저장소의 발표이며, AGMAI의 자문은 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않는다.`
- 시점／형식화：`OpenAI는 10월 6일 372개 결과군에 속한 수학 원고 722편을 처음 공개했다. 10월 7일 수정 기록에 따르면 부호 오류로 3편을 철회하고 별도의 14편을 수정해 현재 목록에는 719편이 남아 있다. 저장소에 따르면 주요 결과의 형식화 비율은 300/719, 약 42%다. 이는 형식화된 비율이며 모든 자연어 증명이 독립적으로 검증됐다는 뜻은 아니다.`
- AGMAI：`AGMAI는 OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명했다. 동시에 자문이 결과의 영향이나 도출 과정에 대한 보증을 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.`
- 추론 요약：`OpenAI는 목록에 오른 10개 결과에 대한 모델 추론의 축약 요약과 연산량 추정치, 시도한 문제 수의 통계도 공개했다. 모든 원고의 전체 사고 과정을 공개했다는 뜻은 아니다.`
- 검증 안내／FAQ：`저장소에는 일부 주요 결과의 Lean 형식화가 포함되어 있지만 AGMAI는 평가가 수학계의 몫이라고 밝혔다. 형식화 비율을 모든 결과의 독립 검증 비율로 해석해서는 안 된다.`

## 執行紀錄

| 語言 | 草稿原版 | 保存後版 | 已發原版 | 新已發版 | 管理員稽核 | 公開頁回讀 |
| --- | --- | --- | --- | --- | --- | --- |
| zh-TW | 2 | 4，2026/10/13 17:07 | 2 | 5，17:10:27 | 第三輪 PASS；`guide_article_published` 成功 | [zh-TW 公開頁](https://mokaair.com/zh-TW/life/ai-news-openai-math-manuscripts-20261006)：標題、描述、正文、FAQ 與來源讀回 |
| zh-CN | 2 | 4，2026/10/13 17:07 | 2 | 5，17:11:13 | 第三輪 PASS；`guide_article_published` 成功 | [zh-CN 公開頁](https://mokaair.com/zh-CN/life/ai-news-openai-math-manuscripts-20261006)：標題、描述、正文與來源讀回 |
| en | 2 | 3，2026/10/13 16:59 | 2 | 4，17:11:45 | 第三輪 PASS；`guide_article_published` 成功 | [en 公開頁](https://mokaair.com/en/life/ai-news-openai-math-manuscripts-20261006)：標題、描述、正文與來源讀回 |
| ja | 2 | 4，2026/10/13 17:06 | 2 | 5，17:12:14 | 第三輪 PASS；`guide_article_published` 成功 | [ja 公開頁](https://mokaair.com/ja/life/ai-news-openai-math-manuscripts-20261006)：標題、描述、正文與來源讀回 |
| ko | 2 | 4，2026/10/13 17:06 | 2 | 5，17:12:41 | 第三輪 PASS；`guide_article_published` 成功 | [ko 公開頁](https://mokaair.com/ko/life/ai-news-openai-math-manuscripts-20261006)：標題、描述、正文與來源讀回 |

以上發布時間為 2026-10-13 台北時間。後台 [稽核紀錄](https://mokaair.com/zh-TW/admin/audit) 依 Guide ID 和語言列出五筆 `guide_article_published`，狀態皆「成功」；ko 稽核事件 `6a211d2a-6289-4d02-8dd2-ca00610510d9` 的理由明載 722／719 時序、300／719 約 42% 已形式化、AGMAI 歸因和五語覆核。公開頁五語均讀回 10/06 首發 722、10/07 撤 3 並另修 14 後現存 719、372 個結果家族、300／719 約 42% **已形式化**、10 個結果的刪節版推理摘要、AGMAI 諮詢界線，以及五個新增一手來源；未把形式化比例寫成全部成果獨立驗證率。其他四語 FAQ 的完整文案另在管理員保存版本及本工作單經獨立覆核。

## 實存 v3 草稿逐欄覆核稿

以下為 2026-10-13 經管理員編輯器保存的實際文字。每語均保留原有 The Verge 來源（查證日期 2026-10-07），另加同一組五個一手網址，查證日期皆為 2026-10-13：

1. `https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md`
2. `https://github.com/openai/math/blob/main/history.md`
3. `https://github.com/openai/math/blob/main/README.md`
4. `https://openai.com/index/sharing-ai-progress-in-mathematics/`
5. `https://agmai.org/`

未列的舊稿欄位保持原 v2 文字；以下每個代號對應管理員編輯器的欄位。此區記錄**草稿**，不是已發內容。每語均應由第二位審閱者按本區逐欄核對，尤其是表格與 FAQ。

### zh-TW 實存 v3

- `title`：OpenAI 首發 722 份數學手稿，修訂後現存 719 份：學界仍待驗證
- `description`：OpenAI 10 月 6 日首發 722 份數學手稿，10 月 7 日撤回 3 份並修訂另外 14 份，現存 719 份。官方儲存庫稱主要結果約 42% 已形式化；AGMAI 強調其諮詢不構成背書。
- `hero.alt`：OpenAI 數學手稿發布新聞示意圖
- `summary`（逐行）：
  1. OpenAI 10 月 6 日首發 722 份數學手稿，分屬 372 個結果家族；10 月 7 日撤回 3 份並修訂另外 14 份，現存 719 份。
  2. OpenAI 儲存庫列主要結果形式化比例為 300／719，約 42%；這不代表整批自然語言證明已獲獨立驗證。
  3. AGMAI 轉述 OpenAI 報稱提出數百個未解問題的解答，但明言其諮詢不構成背書，成果仍須由數學界評估。
- `paragraph 3`：OpenAI 於 10 月 6 日首發 722 份數學手稿，分屬 372 個結果家族，由尚未對外發布的模型產出。其 10 月 7 日修訂紀錄顯示，一處符號錯誤導致 3 份手稿撤回，另有 14 份修訂；現存 719 份。AGMAI 轉述 OpenAI 報稱提出數百個未解問題的解答，但明言其諮詢不構成對成果影響或產出過程的背書；成果仍須由數學界評估。
- `paragraph 6`：OpenAI 在 GitHub 儲存庫公開手稿、修訂紀錄、運算量估計及嘗試問題數統計，並公開涵蓋 10 個結果的刪節版模型推理摘要；這不是每份手稿的完整思考過程。OpenAI 稱平均每項結果使用相當於約三小時 ChatGPT Pro thinking 的算力。儲存庫把主要結果的形式化比例列為 300／719（約 42%）；這是已形式化的比例，不代表整批自然語言證明已獲獨立驗證。
- `table 7`：

```text
項目|OpenAI 官方資料與 AGMAI 聲明
手稿數量|10/06 首發 722 份；10/07 後現存 719 份，分屬 372 個結果家族
修訂紀錄|因一處符號錯誤撤回 3 份，另外修訂 14 份
主要結果已形式化|300／719，約 42%；非整批成果獨立驗證率
附帶資料|10 個結果的刪節版推理摘要、算力估計、嘗試問題數統計
AGMAI 的立場|轉述 OpenAI 報稱數百個解答；諮詢不構成背書
```

- `table 7.caption`：依 OpenAI 儲存庫、官方公告及 AGMAI 聲明整理；數量以 10 月 7 日修訂後為準
- `callout 11.text`：OpenAI 儲存庫列有部分主要結果的 Lean 形式化；300／719（約 42%）是已形式化的比例，不是全部結果獲獨立驗證的比例。AGMAI 明言諮詢不構成對成果影響或產出過程的背書，仍須由數學界評估。
- `faq 14.answer 1`：OpenAI 在 10 月 6 日首發 722 份數學手稿，涵蓋 372 個結果家族。10 月 7 日因符號錯誤撤回 3 份並修訂另外 14 份，現存 719 份；詳見官方儲存庫修訂紀錄。
- `faq 14.answer 2`：尚未全數證實。OpenAI 儲存庫列主要結果 300／719（約 42%）已形式化，但這不表示整批自然語言證明獲獨立驗證；AGMAI 也表示成果仍須由數學界評估。
- `faq 14.answer 3`：AGMAI 是與高等研究院（Institute for Advanced Study）相關的數學與 AI 獨立顧問團。它轉述 OpenAI 報稱數百個未解問題的解答，但明言其諮詢並非對成果或產出過程的背書。
- 新增來源名稱，依上列網址順序：`OpenAI 數學手稿儲存庫：10 月 6 日初版 README（鎖定版本）`；`OpenAI 數學手稿儲存庫：10 月 7 日修訂紀錄`；`OpenAI 數學手稿儲存庫：現行 README`；`OpenAI：Sharing AI progress in mathematics`；`AGMAI：OpenAI 數學成果諮詢聲明`。

### zh-CN 實存 v3

- `title`：OpenAI 首发 722 份数学手稿，修订后现存 719 份：仍待学界验证
- `description`：OpenAI 10 月 6 日首发 722 份数学手稿，10 月 7 日撤回 3 份并修订另外 14 份，现存 719 份。官方仓库称主要结果约 42% 已形式化；AGMAI 强调其顾问工作不构成背书。
- `hero.alt`：OpenAI 数学手稿发布新闻示意图
- `summary`（逐行）：
  1. OpenAI 10 月 6 日首发 722 份数学手稿，分属 372 个结果家族；10 月 7 日撤回 3 份并修订另外 14 份，现存 719 份。
  2. OpenAI 仓库列主要结果形式化比例为 300／719，约 42%；这不代表整批自然语言证明已获独立验证。
  3. AGMAI 转述 OpenAI 声称提出数百个未解问题的解答，但明确表示其顾问工作不构成背书，成果仍须由数学界评估。
- `paragraph 3`：OpenAI 于 10 月 6 日首发 722 份数学手稿，分属 372 个结果家族，由尚未对外发布的模型产出。其 10 月 7 日修订记录显示，一处符号错误导致 3 份手稿被撤回，另有 14 份经过修订；现存 719 份。AGMAI 转述 OpenAI 声称提出数百个未解问题的解答，但明确表示其顾问工作不构成对成果影响或研究过程的背书；成果仍须由数学界评估。
- `paragraph 6`：OpenAI 在 GitHub 仓库公布手稿、修订记录、算力估计及尝试问题数统计，还公布涵盖 10 个结果的删节版模型推理摘要；这不是每份手稿的完整思考过程。OpenAI 称平均每项结果使用相当于约三小时 ChatGPT Pro thinking 的算力。仓库将主要结果的形式化比例列为 300／719（约 42%）；这是已形式化的比例，不代表整批自然语言证明已获独立验证。
- `table 7`：

```text
项目|OpenAI 官方资料与 AGMAI 声明
手稿数量|10/06 首发 722 份；10/07 后现存 719 份，分属 372 个结果家族
修订记录|因一处符号错误撤回 3 份，另外修订 14 份
主要结果已形式化|300／719，约 42%；不是整批成果的独立验证率
附带资料|10 个结果的删节版推理摘要、算力估计、尝试问题数统计
AGMAI 的立场|转述 OpenAI 声称数百个解答；顾问工作不构成背书
```

- `table 7.caption`：依据 OpenAI 仓库、官方公告及 AGMAI 声明整理；数量以 10 月 7 日修订后为准
- `callout 11.text`：OpenAI 仓库列有部分主要结果的 Lean 形式化；300／719（约 42%）是已形式化的比例，不是全部结果获独立验证的比例。AGMAI 明确表示其顾问工作不构成对成果影响或研究过程的背书，成果仍须由数学界评估。
- `faq 14.answer 1`：OpenAI 在 10 月 6 日首发 722 份数学手稿，涵盖 372 个结果家族。10 月 7 日因符号错误撤回 3 份并修订另外 14 份，现存 719 份；详见官方仓库修订记录。
- `faq 14.answer 2`：尚未全部证实。OpenAI 仓库列主要结果 300／719（约 42%）已形式化，但这不表示整批自然语言证明获独立验证；AGMAI 也表示成果仍须由数学界评估。
- `faq 14.answer 3`：AGMAI 是与高等研究院（Institute for Advanced Study）相关的数学与 AI 独立顾问团。它转述 OpenAI 声称数百个未解问题已有解答，但明确表示顾问工作并非对成果或研究过程的背书。
- 新增来源名稱，依上列網址順序：`OpenAI 数学手稿仓库：10 月 6 日初版 README（固定版本）`；`OpenAI 数学手稿仓库：10 月 7 日修订记录`；`OpenAI 数学手稿仓库：现行 README`；`OpenAI：Sharing AI progress in mathematics`；`AGMAI：OpenAI 数学成果顾问声明`。

### en 實存 v3

- `title`: OpenAI Initially Released 722 Math Manuscripts; 719 Remain After Revisions
- `description`: OpenAI released 722 math manuscripts on October 6. Three withdrawals and 14 other revisions on October 7 left 719. Its repository says about 42% of top-line results are formalized; AGMAI says its advisory role is not an endorsement.
- `hero.alt`: Illustration of OpenAI math manuscript release
- `summary` (each line):
  1. OpenAI initially released 722 math manuscripts across 372 result families on October 6; three withdrawals and 14 other revisions on October 7 left 719.
  2. OpenAI's repository lists 300/719 top-line results, about 42%, as formalized. This is not independent validation of every natural-language proof.
  3. AGMAI described OpenAI as reporting solutions to hundreds of open questions, while saying its advisory role does not endorse the process or judge the results' impact.
- `paragraph 3`: OpenAI initially published 722 math manuscripts across 372 result families on October 6, produced by a model that has not been publicly released. Its October 7 history records three withdrawals after a sign error and revisions to 14 other manuscripts, leaving 719. AGMAI described OpenAI as reporting solutions to hundreds of open questions. It said its advisory role was neither an endorsement of the process nor a judgment of the results' impact; assessment remains with the mathematics community.
- `paragraph 6`: OpenAI's GitHub repository provides the manuscripts, revision history, compute estimates and statistics on attempted problems. OpenAI also released abridged summaries of the model's reasoning for ten listed results, rather than full reasoning records for every manuscript. OpenAI says an average result used the equivalent of roughly three hours of ChatGPT Pro thinking. The repository lists 300/719 top-line results, about 42%, as formalized; that is not independent validation of every natural-language proof.
- `table 7`:

```text
Item|OpenAI primary sources and AGMAI statement
Manuscripts|722 initially on Oct. 6; 719 remain after Oct. 7, across 372 result families
Revision history|Three withdrawn after a sign error; 14 other manuscripts revised
Top-line results formalized|300/719, about 42%; not an independent validation rate for all results
Supporting material|Abridged reasoning summaries for ten results, compute estimates and attempted-problem statistics
AGMAI's position|Describes OpenAI as reporting hundreds of solutions; advisory role is not endorsement
```

- `table 7.caption`: Compiled from the OpenAI repository and announcement and the AGMAI statement; counts reflect October 7 revisions
- `callout 11.text`: OpenAI's repository includes Lean formalizations for some top-line results. The 300/719 figure, about 42%, is the formalized share, not independent validation of every result. AGMAI says its advisory role does not endorse the process or judge the results' impact; the mathematics community must assess the work.
- `faq 14.answer 1`: OpenAI initially released 722 manuscripts across 372 result families on October 6. Its October 7 history records three withdrawals after a sign error and 14 other revisions, leaving 719.
- `faq 14.answer 2`: Not all have been independently verified. OpenAI's repository lists 300/719 top-line results, about 42%, as formalized, but that does not validate every natural-language proof. AGMAI says the mathematics community must assess the work.
- `faq 14.answer 3`: AGMAI is an independent Advisory Group on Mathematics and Artificial Intelligence associated with the Institute for Advanced Study. It described OpenAI as reporting solutions to hundreds of open questions, while making clear that its advisory role does not endorse the process or judge the results' impact.
- New source names in the URL order above: `OpenAI math repository: initial October 6 README (pinned commit)`; `OpenAI math repository: October 7 revision history`; `OpenAI math repository: current README`; `OpenAI: Sharing AI progress in mathematics`; `AGMAI statement on OpenAI mathematics work`.

### ja 實存 v3

- `title`：OpenAIの数学原稿、初回722本から719本に：撤回後も学界の評価待ち
- `description`：OpenAIは10月6日に数学原稿722本を公開し、10月7日に3本を撤回、別の14本を修正した。現行の収録数は719本。主要結果の約42％が形式化済みという数字はOpenAI側の記載で、AGMAIの助言は成果の影響に対する評価や、その生成過程への支持を意味しない。
- `hero.alt`：OpenAIの数学原稿公開を表すイメージ画像
- `summary`（逐行）：
  1. OpenAIは10月6日に372の成果群に属する数学原稿722本を公開し、10月7日に3本を撤回、別の14本を修正した。現行の収録数は719本。
  2. OpenAIのリポジトリは主要結果の形式化率を300／719（約42％）と記しているが、自然言語の証明すべてが独立に検証された割合ではない。
  3. AGMAIはOpenAIが数百の未解決問題への解答を報告したと説明しつつ、助言は成果や生成過程への支持を意味せず、評価は数学界に委ねられるとした。
- `paragraph 3`：OpenAIは10月6日に372の成果群（ファミリー）に属する722本の数学原稿を公開した。10月7日の改訂記録によると、符号の誤りを受けて3本を取り下げ、別の14本を修正し、現行の収録数は719本となった。AGMAIはOpenAIが数百の未解決問題への解答を報告したと説明した。同時に、助言は成果の影響に対する評価や研究過程への支持を意味せず、判断は数学界に委ねられると明言している。
- `paragraph 6`：OpenAIはGitHubのリポジトリで原稿、改訂記録、計算量の推定、試行した問題数の統計を公開した。さらに一覧に挙げた10の結果についてモデルの推論を短くまとめた資料も公開したが、各原稿の完全な思考過程ではない。OpenAIによると、結果1件当たりの平均計算量はChatGPT Pro thinking約3時間分に相当する。リポジトリは主要結果の形式化率を300／719（約42％）と記しているが、自然言語の証明すべてが独立に検証されたことを示す数字ではない。
- `table 7`：

```text
項目|OpenAIの一次資料とAGMAIの声明
原稿数|10月6日の初回公開は722本、10月7日以降は719本。372の成果群に分類
改訂記録|符号の誤りで3本を撤回、別の14本を修正
形式化済みの主要結果|300／719、約42％。全成果の独立検証率ではない
付随資料|10の結果の短縮版推論要約、計算量の推定、試行した問題数の統計
AGMAIの立場|OpenAIが数百の解答を報告したと説明。助言は支持や評価を意味しない
```

- `table 7.caption`：OpenAIのリポジトリと公式発表、AGMAIの声明を基に作成。原稿数は10月7日の改訂後
- `callout 11.text`：OpenAIのリポジトリには一部の主要結果にLean形式化がある。300／719（約42％）は形式化済みの割合であり、すべての結果の独立検証率ではない。AGMAIは助言が成果の影響への評価や研究過程への支持を意味せず、評価は数学界に委ねられると明言している。
- `faq 14.answer 1`：OpenAIは10月6日に372の成果群に属する722本の原稿を初めて公開した。10月7日に符号の誤りで3本を撤回し、別の14本を修正したため、現行の収録数は719本。
- `faq 14.answer 2`：すべてが独立に確認されたわけではない。OpenAIのリポジトリは主要結果300／719（約42％）を形式化済みとしているが、自然言語の証明すべての検証を意味しない。AGMAIも評価は数学界に委ねられるとしている。
- `faq 14.answer 3`：AGMAIは高等研究院（Institute for Advanced Study）に関連する、数学とAIについての独立した助言グループ。OpenAIが数百の未解決問題への解答を報告したと説明しつつ、助言は成果や研究過程への支持を意味しないと明言している。
- 新增來源名稱，依上列網址順序：`OpenAI数学原稿リポジトリ：10月6日の初版README（固定版）`；`OpenAI数学原稿リポジトリ：10月7日の改訂記録`；`OpenAI数学原稿リポジトリ：現行README`；`OpenAI：Sharing AI progress in mathematics`；`AGMAI：OpenAIの数学成果に関する声明`。

### ko 實存 v3

- `title`：OpenAI 수학 원고, 최초 722편에서 719편으로: 철회 후에도 학계 검토 중
- `description`：OpenAI는 10월 6일 수학 원고 722편을 공개했고, 10월 7일 3편을 철회하고 다른 14편을 수정했다. 현재 목록에는 719편이 남아 있다. 주요 결과 약 42%가 형식화됐다는 수치는 OpenAI 저장소의 발표이며, AGMAI의 자문은 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않는다.
- `hero.alt`：OpenAI 수학 원고 공개를 표현한 이미지
- `summary`（逐行）：
  1. OpenAI는 10월 6일 372개 결과군에 속한 수학 원고 722편을 처음 공개했고, 10월 7일 3편을 철회하고 다른 14편을 수정했다. 현재 목록에는 719편이 남아 있다.
  2. OpenAI 저장소에 따르면 주요 결과 300/719, 약 42%가 형식화됐다. 이는 모든 자연어 증명이 독립적으로 검증됐다는 뜻은 아니다.
  3. AGMAI는 OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명하면서, 자문이 결과나 도출 과정에 대한 보증을 뜻하지 않는다고 밝혔다.
- `paragraph 3`：OpenAI는 10월 6일 372개 결과군에 속한 수학 원고 722편을 처음 공개했다. 10월 7일 수정 기록에 따르면 부호 오류로 3편을 철회하고 별도의 14편을 수정해 현재 목록에는 719편이 남아 있다. AGMAI는 OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명했다. 동시에 자문이 결과의 영향이나 도출 과정에 대한 보증을 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.
- `paragraph 6`：OpenAI는 GitHub 저장소에 원고, 수정 기록, 연산량 추정치와 시도한 문제 수의 통계를 공개했다. 목록에 오른 10개 결과에 대한 모델 추론의 축약 요약도 공개했지만, 모든 원고의 전체 사고 과정은 아니다. OpenAI에 따르면 결과 하나에 쓰인 평균 연산량은 ChatGPT Pro thinking 약 3시간에 해당한다. 저장소는 주요 결과의 형식화 비율을 300/719, 약 42%로 제시한다. 이는 모든 자연어 증명이 독립적으로 검증됐다는 뜻이 아니다.
- `table 7`：

```text
항목|OpenAI 1차 자료와 AGMAI 성명
원고 수|10월 6일 최초 722편, 10월 7일 이후 현재 719편. 372개 결과군
수정 기록|부호 오류로 3편 철회, 별도의 14편 수정
형식화된 주요 결과|300/719, 약 42%. 전체 성과의 독립 검증률이 아님
함께 공개된 자료|10개 결과에 대한 축약 추론 요약, 연산량 추정치, 시도한 문제 수 통계
AGMAI의 입장|OpenAI가 수백 건의 해답을 보고했다고 설명. 자문은 보증이 아님
```

- `table 7.caption`：OpenAI 저장소와 공식 발표, AGMAI 성명을 바탕으로 정리. 원고 수는 10월 7일 수정 이후 기준
- `callout 11.text`：OpenAI 저장소에는 일부 주요 결과의 Lean 형식화가 포함돼 있다. 300/719, 약 42%는 형식화된 비율이며 모든 결과의 독립 검증률이 아니다. AGMAI는 자문이 결과의 영향이나 도출 과정에 대한 보증을 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.
- `faq 14.answer 1`：OpenAI는 10월 6일 372개 결과군에 속한 원고 722편을 처음 공개했다. 10월 7일 부호 오류로 3편을 철회하고 다른 14편을 수정해 현재 목록에는 719편이 남아 있다.
- `faq 14.answer 2`：모두 독립적으로 검증된 것은 아니다. OpenAI 저장소는 주요 결과 300/719, 약 42%가 형식화됐다고 제시하지만 모든 자연어 증명이 검증됐다는 뜻은 아니다. AGMAI도 평가는 수학계의 몫이라고 밝혔다.
- `faq 14.answer 3`：AGMAI는 고등연구원(Institute for Advanced Study)과 관련된 수학·AI 독립 자문단이다. OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명하면서도, 자문이 성과나 도출 과정에 대한 보증을 뜻하지 않는다고 명시했다.
- 新增來源名稱，依上列網址順序：`OpenAI 수학 원고 저장소: 10월 6일 최초 README(고정 커밋)`；`OpenAI 수학 원고 저장소: 10월 7일 수정 기록`；`OpenAI 수학 원고 저장소: 현재 README`；`OpenAI: Sharing AI progress in mathematics`；`AGMAI: OpenAI 수학 성과 관련 성명`。

## 第二輪獨立審稿與實存 v4 差異

獨立審閱者對上列 v3 全文逐欄查核：**en PASS；zh-TW、zh-CN、ja、ko FAIL**。所有語言的 722→719 時序、撤 3／另修 14、300／719 約 42% **已形式化**、10 個結果的刪節推理摘要與平均約三小時 ChatGPT Pro thinking 均通過；問題集中於 AGMAI 對「成果影響的評價」和「產出過程的背書」必須分開，及非英語來源名稱。以下四語當時按回饋在管理員編輯器保存 v4 草稿；每語未列欄位與上列 v3 完全相同。第三輪已用本段差異覆蓋 v3 對應欄位審稿，五語 PASS 後才發布；最終版本與稽核見「執行紀錄」。

### zh-TW v4 改動欄位

- `paragraph 3`：OpenAI 於 10 月 6 日首發 722 份數學手稿，分屬 372 個結果家族，由尚未對外發布的模型產出。其 10 月 7 日修訂紀錄顯示，一處符號錯誤導致 3 份手稿撤回，另有 14 份修訂；現存 719 份。AGMAI 轉述 OpenAI 報稱提出數百個未解問題的解答，但明言其諮詢不等於對成果影響的評價，也不構成對產出過程的背書；成果仍須由數學界評估。
- `callout 11.text`：OpenAI 儲存庫列有部分主要結果的 Lean 形式化；300／719（約 42%）是已形式化的比例，不是全部結果獲獨立驗證的比例。AGMAI 明言其諮詢不等於對成果影響的評價，也不構成對產出過程的背書，仍須由數學界評估。
- `faq 14.answer 3`：AGMAI 是與高等研究院（Institute for Advanced Study）相關的數學與 AI 獨立顧問團。它轉述 OpenAI 報稱數百個未解問題的解答，但明言其諮詢不等於對成果影響的評價，也不構成對產出過程的背書；成果仍須由數學界評估。
- 第四個新增來源名稱：`OpenAI：分享 AI 在數學領域的進展（Sharing AI progress in mathematics）`。

### zh-CN v4 改動欄位

- `paragraph 3`：OpenAI 于 10 月 6 日首发 722 份数学手稿，分属 372 个结果家族，由尚未对外发布的模型产出。其 10 月 7 日修订记录显示，一处符号错误导致 3 份手稿被撤回，另有 14 份经过修订；现存 719 份。AGMAI 转述 OpenAI 声称提出数百个未解问题的解答，但明确表示其顾问工作不等于对成果影响的评价，也不构成对研究过程的背书；成果仍须由数学界评估。
- `callout 11.text`：OpenAI 仓库列有部分主要结果的 Lean 形式化；300／719（约 42%）是已形式化的比例，不是全部结果获独立验证的比例。AGMAI 明确表示其顾问工作不等于对成果影响的评价，也不构成对研究过程的背书，成果仍须由数学界评估。
- `faq 14.answer 3`：AGMAI 是与高等研究院（Institute for Advanced Study）相关的数学与 AI 独立顾问团。它转述 OpenAI 声称数百个未解问题已有解答，但明确表示顾问工作不等于对成果影响的评价，也不构成对研究过程的背书；成果仍须由数学界评估。
- 第四個新增來源名稱：`OpenAI：分享人工智能在数学领域的进展（Sharing AI progress in mathematics）`。

### ja v4 改動欄位

- `summary` 第三行：AGMAIはOpenAIが数百の未解決問題への解答を報告したと説明した。助言は成果の影響に対する評価や生成過程への支持を意味せず、評価は数学界に委ねられるとした。
- `table 7` 最末行：`AGMAIの立場|OpenAIが数百の解答を報告したと説明。成果の影響への評価でも生成過程への支持でもない`
- `faq 14.answer 3`：AGMAIは高等研究院（Institute for Advanced Study）に関連する、数学とAIについての独立した助言グループ。OpenAIが数百の未解決問題への解答を報告したと説明した。助言は成果の影響に対する評価や研究過程への支持を意味せず、評価は数学界に委ねられると明言している。
- 第四個新增來源名稱：`OpenAI：数学分野におけるAIの進展の共有（Sharing AI progress in mathematics）`。

### ko v4 改動欄位

- `summary` 第三行：AGMAI는 OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명했다. 자문은 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않으며, 평가는 수학계의 몫이라고 밝혔다.
- `paragraph 3`：OpenAI는 10월 6일 372개 결과군에 속한 수학 원고 722편을 처음 공개했다. 10월 7일 수정 기록에 따르면 부호 오류로 3편을 철회하고 별도의 14편을 수정해 현재 목록에는 719편이 남아 있다. AGMAI는 OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명했다. 동시에 자문은 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.
- `table 7` 最末行：`AGMAI의 입장|OpenAI가 수백 건의 해답을 보고했다고 설명. 결과의 영향에 대한 평가나 도출 과정에 대한 지지가 아님`
- `callout 11.text`：OpenAI 저장소에는 일부 주요 결과의 Lean 형식화가 포함돼 있다. 300/719, 약 42%는 형식화된 비율이며 모든 결과의 독립 검증률이 아니다. AGMAI는 자문이 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.
- `faq 14.answer 3`：AGMAI는 고등연구원(Institute for Advanced Study)과 관련된 수학·AI 독립 자문단이다. OpenAI가 수백 건의 미해결 문제에 대한 해답을 보고했다고 설명했다. 자문은 결과의 영향에 대한 평가나 도출 과정에 대한 지지를 뜻하지 않으며, 평가는 수학계의 몫이라고 명시했다.
- 第四個新增來源名稱：`OpenAI: 수학 분야 AI 발전 공유 (Sharing AI progress in mathematics)`。
