# 2026-10-07 OpenAI 數學手稿 Guide 五語更正（2026-10-13）

## 目標與界線

- 正式站 Guide ID `e31a32b6-2f93-4a7a-ba45-ecc729e138b6`，slug `ai-news-openai-math-manuscripts-20261007`；與 10/06 另一篇 Guide ID `0fe56758-5ac9-468e-b86e-71dabc7e0cd4` 不同。
- 2026-10-13 後台唯讀顯示五語皆為草稿 v2／已刊 v2，原稿將 `162／722 ≈ 22%` 寫進描述、摘要、驗證段、兩張表格及 FAQ；五語亦誤掛 `crypto`，附加密資產免責與 crypto 主題連結。
- 此工作單列出**已儲存的逐欄全文**；正式站草稿、獨立覆核、發布及公開頁回讀詳見末段執行紀錄。

## 一手來源（2026-10-13 開啟）

| 來源 | 可確認的事實與用法 |
| --- | --- |
| [OpenAI 10/06 初版 README，固定 commit](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) | 首發目錄有 722 份手稿、372 個結果家族；722 必標明為當時數量。初版已說部分未形式化成果可能有問題。 |
| [OpenAI 10/07 修訂紀錄](https://github.com/openai/math/blob/main/history.md) | 一處符號錯誤使 3 份相依手稿撤回，另修 14 份；新增 6 項形式化及 5 項輔助成果後，主要結果已形式化比例為 **300／719，約 42%**。這是形式化覆蓋率，不能寫成所有自然語言證明已被獨立確認。 |
| [OpenAI 現行 README](https://github.com/openai/math/blob/main/README.md) | 現行 719 份手稿、372 個家族，不同成果處於不同驗證階段；10 份模型推理資料是刪節摘要。`main` 可再變，發布前重讀。 |
| [OpenAI 10/06 公告](https://openai.com/index/sharing-ai-progress-in-mathematics/) | 官方說明內部模型、GitHub 發布、Lean 與 10 份推理摘要；不是每份手稿的完整思考紀錄。 |
| [AGMAI 10/06 聲明](https://agmai.org/)及[9/29 建議](https://agmai.org/general-sep29/) | 顧問工作不構成對成果影響或產出過程的背書；數學界仍須評估。建議每項結果披露模型、提示、摘要推理、時間與算力。 |
| [Anthropic 費馬證明儲存庫](https://github.com/anthropics/fermats-last-theorem) | 公開的是 Lean 證明程式碼與檢查材料；對照表不寫「全部內容」或暗示完整研究過程皆公開。 |

後台原有 Decrypt 來源保留為 2026-10-07 查證的二手報導，Andrew Sutherland／Anthropic 等轉述仍歸因於該報導。本次數字與時序改以 OpenAI 一手紀錄為準。所有新增官方來源的 `checked_on` 為 2026-10-13；不得把 10/07 新數字歸因於原 Decrypt 報導。

## 欄位與分類操作

下面 `summary` 的四行仍是原有重點摘要 1；`p3`、`p4`、`p7`、`p14` 是既有段落編號，`table9` 與 `table17` 是既有表格，`faq1` 和 `faq2` 是原有 FAQ 前兩題。各語未列欄位保留 v2 原文。`title` 變更後，主圖 alt 仍描述 10/06 初版 722 篇的新聞插畫，不必宣稱現行數量。

`faq2 question` 維持 v2 原文，各語分別是「這些結果都已證實正確嗎？」、「这些结果都已证实正确吗？」、“Are these results all confirmed correct?”、「これらの結果はすべて正しいと確認されているのですか？」、「이 결과들은 모두 올바르다고 확인됐나?」。保存草稿與公開回讀時須確認仍與新答案相接。

- 取消 `crypto`（加密貨幣與區塊鏈）主題，選取 `ai-news`（AI 新聞與趨勢）。分類是整篇 Guide 共用，儲存後切換語言核對。
- 各語移除區塊 21 的投資／加密資產免責，將末段「查看同分類最新消息」連結網址從 `/{locale}/life/topics/crypto` 改為 `/{locale}/life/topics/ai-news`；連結文字維持各語原文。
- 逐語加入六個官方來源（上述初版 README、history、現行 README、公告、AGMAI 10/06 聲明、Anthropic 儲存庫），保留原有 Decrypt。官方來源名稱採各語自然譯名，查證日期 2026-10-13。
- 草稿先保存並讀回，交另一位審閱者逐欄核對。只有獨立審閱 PASS 後，才分語發布並檢查版本、稽核、公開頁。

## zh-TW 預定草稿逐欄文字

**title**：OpenAI 數學手稿首發 722 篇、現存 719 篇：主要結果約 42% 已形式化

**description**：OpenAI 10 月 6 日首發 722 篇數學手稿；10 月 7 日撤回 3 篇並另修訂 14 篇，現存 719 篇。OpenAI 儲存庫列主要結果 300／719（約 42%）已形式化；這不等於全部論證已獲獨立驗證。

**summary**：

```text
OpenAI 10 月 6 日首發 722 篇數學手稿，10 月 7 日撤回 3 篇後現存 719 篇，分屬 372 個結果家族。
OpenAI 修訂紀錄列主要結果 300／719（約 42%）已形式化；這不是整批成果經獨立驗證的比例。
MIT 的 Andrew Sutherland 表示，「單一提示、單一代理」的說法在模型釋出並能重現前仍屬未驗證。
對一般讀者來說，「AI 一次解出數百道數學難題」目前仍是公司的說法，尚待數學界評估。
```

**p3**：OpenAI 10 月 6 日在 GitHub 首發 722 篇由未公開內部模型產出的數學手稿；10 月 7 日因一處符號錯誤撤回 3 篇，另修訂 14 篇，現存 719 篇。Decrypt 引述 OpenAI 發言人的說法：幾乎所有成果都來自交給單一 AI 代理（能自行分步完成任務的 AI 程式）的單一提示（也就是交給 AI 的一段指令文字），但部分可能經過多次嘗試。

**p4**：這些手稿分成 372 個「家族」。OpenAI 儲存庫說明，一個家族可能包含主定理、附帶論證、推論或替代證明；因此 10 月 6 日的 722 是首發手稿數，10 月 7 日後現存 719 篇，都不是已解決問題的數量。OpenAI 表示向模型提出大約 4,000 個問題，並保留它判斷夠重要的輸出來發布。

**p7**：Lean 是逐步機械式檢查證明的工具；把證明翻譯成 Lean 並通過檢查，稱為「形式化」。OpenAI 10 月 7 日修訂紀錄列主要結果 300／719（約 42%）已形式化，並說明 3 篇撤回與另外 14 篇修補。這是形式化覆蓋率，不代表每篇自然語言論證都經獨立確認。OpenAI 仍提醒，部分未形式化結果可能有問題，取得新的 Lean 形式化後會陸續補上。

**table9**：

```text
項目|OpenAI 官方紀錄與 Decrypt 報導
手稿數量|10/06 首發 722 篇；10/07 撤回 3 篇後現存 719 篇，分屬 372 個結果家族
主要結果已形式化比例|OpenAI 10/07 列 300／719，約 42%；不等於全數獨立驗證
已公開的推理資料|10 個結果的刪節版推理摘要與平均算力數字，沒有公開提示
平均算力|每項結果平均相當於約三小時 ChatGPT Pro 思考算力（據 OpenAI）
模型狀態|內部模型，尚未釋出
```

**table9 caption**：依 OpenAI 儲存庫現行數據與原 Decrypt 報導整理的數學手稿發布概況

**p14**：也有人較為正面。據 Decrypt，Abhishek Saha 教授寫道「It is a very big day for mathematics」（這是數學界非常重大的一天），但指出多數問題屬於「現有研究計畫內的卓越進展」或「令人驚訝的突破」。Decrypt 指出，在 10 月 6 日首發的 722 篇手稿中，屬於千禧年難題等級的只有一個，即 Quasi-Riemann Hypothesis；該首發數字不代表現存手稿數。

**table17**：

```text
比較點|OpenAI 手稿發布|Anthropic 費馬證明
內容|10/06 首發 722 篇，10/07 後現存 719 篇，宣稱為新成果|形式化 Wiles 於 1995 年發表的定理，不宣稱新結果
Lean 檢查|OpenAI 列主要結果 300／719（約 42%）已形式化|證明經 Lean 檢查，共 1,300 萬行
公開方式|GitHub 儲存庫；提示未公開|Lean 證明程式碼與檢查材料公開於 GitHub
```

**table17 caption**：依 OpenAI 10 月 7 日修訂紀錄、Anthropic 儲存庫與 Decrypt 報導整理的兩項發布對照

**faq1 question**：722 篇手稿代表 OpenAI 解決了 722 道數學難題嗎？

**faq1 answer**：不是。722 是 10 月 6 日首發的手稿數，10 月 7 日撤回 3 篇後現存 719 篇，分屬 372 個結果家族。家族可包含主定理、推論或替代證明，不能把手稿數當成已解決問題數。

**faq2 answer**：尚未。OpenAI 10 月 7 日列主要結果 300／719（約 42%）已形式化，但這不代表全部自然語言論證都獲獨立驗證；儲存庫也提醒部分未形式化結果可能有問題。

**callout18**：OpenAI 已將主要結果形式化比例更新為 300／719（約 42%），但形式化不是整批成果的獨立背書。模型與提示尚未完整公開，外界仍需評估各份手稿及「單一提示、單一代理」的說法。

## zh-CN 預定草稿逐欄文字

**title**：OpenAI 数学手稿首发 722 篇、现存 719 篇：主要结果约 42% 已形式化

**description**：OpenAI 10 月 6 日首发 722 篇数学手稿；10 月 7 日撤回 3 篇并另修订 14 篇，现存 719 篇。OpenAI 存储库称主要结果 300／719（约 42%）已形式化；这不等于全部论证已获独立验证。

**summary**：

```text
OpenAI 10 月 6 日首发 722 篇数学手稿，10 月 7 日撤回 3 篇后现存 719 篇，分属 372 个结果家族。
OpenAI 修订记录称主要结果 300／719（约 42%）已形式化；这不是整批成果获独立验证的比例。
MIT 的 Andrew Sutherland 表示，“单一提示、单一代理”的说法在模型发布并能复现前仍属未验证。
对普通读者来说，“AI 一次解出数百道数学难题”目前仍是公司的说法，尚待数学界评估。
```

**p3**：OpenAI 10 月 6 日在 GitHub 首发 722 篇由未公开内部模型产出的数学手稿；10 月 7 日因一处符号错误撤回 3 篇，另修订 14 篇，现存 719 篇。Decrypt 引述 OpenAI 发言人的说法：几乎所有成果都来自交给单一 AI 代理（能自行分步完成任务的 AI 程序）的单一提示（也就是交给 AI 的一段指令文字），但部分可能经过多次尝试。

**p4**：这些手稿分成 372 个“家族”。OpenAI 存储库说明，一个家族可能包含主定理、附带论证、推论或替代证明；因此 10 月 6 日的 722 是首发手稿数，10 月 7 日后现存 719 篇，都不是已解决问题的数量。OpenAI 表示向模型提出大约 4,000 个问题，并保留它判断足够重要的输出来发布。

**p7**：Lean 是逐步机械式检查证明的工具；把证明翻译成 Lean 并通过检查，称为“形式化”。OpenAI 10 月 7 日修订记录称主要结果 300／719（约 42%）已形式化，并说明撤回 3 篇、另外修补 14 篇。这是形式化覆盖率，不代表每篇自然语言论证都经独立确认。OpenAI 仍提醒，部分未形式化结果可能有问题，取得新的 Lean 形式化后会陆续补上。

**table9**：

```text
项目|OpenAI 官方记录与 Decrypt 报道
手稿数量|10/06 首发 722 篇；10/07 撤回 3 篇后现存 719 篇，分属 372 个结果家族
主要结果已形式化比例|OpenAI 10/07 列 300／719，约 42%；不等于全部获独立验证
已公开的推理资料|10 个结果的删节版推理摘要与平均算力数字，未公开提示
平均算力|每项结果平均相当于约三小时 ChatGPT Pro 思考算力（据 OpenAI）
模型状态|内部模型，尚未发布
```

**table9 caption**：依据 OpenAI 存储库现行数据与原 Decrypt 报道整理的数学手稿发布概况

**p14**：也有人较为正面。据 Decrypt，Abhishek Saha 教授写道“It is a very big day for mathematics”（这是数学界非常重大的一天），但指出多数问题属于“现有研究计划内的卓越进展”或“令人惊讶的突破”。Decrypt 指出，在 10 月 6 日首发的 722 篇手稿中，属于千禧年难题级别的只有一个，即 Quasi-Riemann Hypothesis；该首发数字不代表现存手稿数。

**table17**：

```text
比较点|OpenAI 手稿发布|Anthropic 费马证明
内容|10/06 首发 722 篇，10/07 后现存 719 篇，宣称为新成果|形式化 Wiles 于 1995 年发表的定理，不宣称新结果
Lean 检查|OpenAI 列主要结果 300／719（约 42%）已形式化|证明经 Lean 检查，共 1,300 万行
公开方式|GitHub 存储库；提示未公开|Lean 证明代码与检查材料公开于 GitHub
```

**table17 caption**：依据 OpenAI 10 月 7 日修订记录、Anthropic 存储库与 Decrypt 报道整理的两项发布对照

**faq1 question**：722 篇手稿代表 OpenAI 解决了 722 道数学难题吗？

**faq1 answer**：不是。722 是 10 月 6 日首发的手稿数，10 月 7 日撤回 3 篇后现存 719 篇，分属 372 个结果家族。家族可以包含主定理、推论或替代证明，不能把手稿数当成已解决问题数。

**faq2 answer**：尚未。OpenAI 10 月 7 日称主要结果 300／719（约 42%）已形式化，但这不代表全部自然语言论证都获独立验证；存储库也提醒部分未形式化结果可能有问题。

**callout18**：OpenAI 已将主要结果形式化比例更新为 300／719（约 42%），但形式化不是整批成果的独立背书。模型与提示尚未完整公开，外界仍需评估各篇手稿及“单一提示、单一代理”的说法。

## en proposed draft field text

**title**: OpenAI's Math Manuscripts: 722 at Launch, 719 After Withdrawals; About 42% of Top-Line Results Formalized

**description**: OpenAI initially released 722 math manuscripts on October 6. Three withdrawals and 14 other revisions on October 7 left 719. Its repository says 300/719 top-line results, about 42%, are formalized; that does not independently validate every proof.

**summary**:

```text
OpenAI released 722 math manuscripts on October 6; after three withdrawals on October 7, 719 remain across 372 result families.
OpenAI's revision history says 300/719 top-line results, about 42%, are formalized. This is not the share of all results independently validated.
MIT's Andrew Sutherland says the 'single prompt, single agent' claim is unverified until the model is released and results can be reproduced.
For general readers, 'AI solved hundreds of hard math problems at once' remains a company claim for the mathematics community to assess.
```

**p3**: OpenAI initially released 722 math manuscripts on GitHub on October 6, produced by an unreleased internal model. On October 7 it withdrew three after a sign error and revised 14 others, leaving 719. Decrypt quotes an OpenAI spokesperson saying nearly all results came from a single prompt (a block of instruction text given to the AI) handed to a single AI agent (an AI program that carries out tasks step by step on its own), though some may have taken multiple attempts.

**p4**: The manuscripts are grouped into 372 result families. OpenAI's repository says a family may contain a principal result, companion arguments, consequences or alternative proofs. Thus 722 was the initial manuscript count on October 6 and 719 is the count after the October 7 withdrawals; neither is a count of solved problems. OpenAI says it posed about 4,000 problems to the model and selected the outputs it considered significant enough for publication.

**p7**: Lean is software that mechanically checks a proof's logical steps; translating a proof into Lean and passing the check is called formalization. OpenAI's October 7 history lists 300/719 top-line results, about 42%, as formalized and records three withdrawals plus revisions to 14 other manuscripts. This measures formalization coverage, not independent validation of every natural-language argument. OpenAI still warns that some unformalized results could have issues and says it will add formalizations as they become available.

**table9**:

```text
Item|OpenAI records and Decrypt reporting
Number of manuscripts|722 at the October 6 release; 719 after three October 7 withdrawals, across 372 result families
Top-line results formalized|OpenAI lists 300/719, about 42%, on October 7; not independent validation of all results
Reasoning material released|Abridged reasoning summaries for ten results and average compute figures; prompts not released
Average compute|About three hours of ChatGPT Pro thinking compute per result (per OpenAI)
Model status|Internal model, not yet released
```

**table9 caption**: OpenAI math manuscript release, updated with its repository records and the original Decrypt report

**p14**: Others are more positive. Per Decrypt, Professor Abhishek Saha wrote 'It is a very big day for mathematics', but noted that most of the problems fall into the categories of 'exceptional advances within an existing program' or 'surprising breakthroughs'. Decrypt says only one in the original October 6 release of 722 manuscripts is at the level of a millennium problem: the Quasi-Riemann Hypothesis. That original count is not the number of manuscripts currently listed.

**table17**:

```text
Point of comparison|OpenAI manuscript release|Anthropic Fermat proof
Content|722 manuscripts at the October 6 release; 719 after October 7, presented as new results|Formalizes the theorem Wiles published in 1995; no new result claimed
Lean check|OpenAI lists 300/719 top-line results, about 42%, formalized|Proof checked in Lean, 13 million lines
How it was released|GitHub repository; prompts not released|Lean proof code and verification materials public on GitHub
```

**table17 caption**: Comparison updated with OpenAI's October 7 history, Anthropic's repository and the original Decrypt report

**faq1 question**: Does 722 manuscripts mean OpenAI solved 722 math problems?

**faq1 answer**: No. There were 722 manuscripts at the October 6 release and 719 after three October 7 withdrawals, grouped into 372 result families. A family can include a principal result, consequences or alternative proofs. The manuscript count is not a count of solved problems.

**faq2 answer**: Not yet. OpenAI says 300/719 top-line results, about 42%, are formalized as of its October 7 history. That does not independently validate every natural-language argument, and the repository warns that some unformalized results could have issues.

**callout18**: OpenAI updated its top-line formalization figure to 300/719, about 42%, but formalization is not independent endorsement of the entire collection. The model and prompts have not been fully released, and outside assessment of the manuscripts and the 'single prompt, single agent' claim remains necessary.

## ja 予定草稿の変更欄全文

**title**：OpenAIの数学原稿、初回722本から719本に：主要結果の約42％を形式化

**description**：OpenAIは10月6日に数学原稿722本を公開し、10月7日に3本を取り下げ、別の14本を修正した。現行の収録数は719本。リポジトリによると主要結果の300／719（約42％）が形式化済みだが、全証明の独立検証を意味しない。

**summary**：

```text
OpenAIは10月6日に数学原稿722本を公開し、10月7日に3本を取り下げた。現在は719本で、372の成果群に分かれる。
OpenAIの改訂記録では主要結果の300／719（約42％）が形式化済み。これは全成果が独立に検証された割合ではない。
MITのAndrew Sutherland氏は「単一プロンプト・単一エージェント」という主張は、モデルが公開され再現できるまで未検証だと述べた。
「AIが数百の数学難問を一度に解いた」という見方は現時点では企業側の主張であり、数学界による評価が必要だ。
```

**p3**：OpenAIは10月6日、未公開の内部モデルが生成した数学原稿722本をGitHubで初公開した。10月7日には符号の誤りを受けて3本を取り下げ、別の14本を修正し、現行の収録数は719本となった。DecryptはOpenAI広報の説明として、ほぼすべての成果が、単一のAIエージェント（自ら段階的にタスクをこなすAIプログラム）に与えた単一のプロンプト（AIに渡す指示文）から得られたが、一部は複数回の試行を経ている可能性があると伝えている。

**p4**：原稿は372の成果群（ファミリー）に分かれる。OpenAIのリポジトリによると、1つの成果群には主定理、付随する議論、系、別証明などが含まれうる。したがって、722は10月6日の初回原稿数、719は10月7日の取り下げ後の収録数であり、いずれも解決した問題の件数ではない。OpenAIはモデルに約4,000問を与え、重要と判断した出力を選んで公開したという。

**p7**：Leanは証明の論理的な手順を機械的に検査するソフトウェアで、証明をLeanに翻訳して検査を通すことを「形式化」と呼ぶ。OpenAIの10月7日の改訂記録は、主要結果の300／719（約42％）が形式化済みとし、3本の取り下げと別の14本の修正を記録している。これは形式化の割合であり、自然言語の論証すべてが独立に検証された割合ではない。OpenAIは形式化されていない結果の一部には問題がある可能性を認め、形式化を追加していくとしている。

**table9**：

```text
項目|OpenAIの公式記録とDecryptの報道
原稿数|10月6日の初回は722本。10月7日に3本を取り下げ、現行は719本、372の成果群
主要結果の形式化率|OpenAIの10月7日の記録で300／719（約42％）。全成果の独立検証率ではない
公開された推論資料|10の結果に関する短い推論要約と平均計算量。プロンプトは非公開
平均計算量|各結果あたり平均約3時間分のChatGPT Pro思考計算量に相当（OpenAIによる）
モデルの状態|内部モデル、未公開
```

**table9 caption**：OpenAIの現行リポジトリとDecryptの元記事を踏まえた数学原稿公開の概要

**p14**：より肯定的な声もある。Decryptによると、Abhishek Saha教授は「It is a very big day for mathematics」（数学にとって非常に大きな日だ）と書いたが、多くの問題は「既存の研究計画内での卓越した進展」か「驚くべきブレークスルー」に当たると指摘した。Decryptは、10月6日に初公開された722本のうち、ミレニアム懸賞問題級なのはQuasi-Riemann Hypothesisの1件だけだと伝えた。この初回の本数は現行の収録数ではない。

**table17**：

```text
比較点|OpenAIの原稿公開|Anthropicのフェルマー証明
内容|10月6日に722本を初公開、10月7日以降は719本。新規成果を主張|Wiles氏が1995年に発表した定理を形式化、新結果の主張なし
Lean検査|OpenAIは主要結果の300／719（約42％）を形式化済みと記載|証明はLeanで検査済み、1,300万行
公開方法|GitHubリポジトリ、プロンプトは非公開|Leanの証明コードと検査用資料をGitHubで公開
```

**table17 caption**：OpenAIの10月7日の改訂記録、Anthropicのリポジトリ、Decryptの元記事を踏まえた公開事例の比較

**faq1 question**：722本の原稿は、OpenAIが722の数学難問を解いたという意味ですか？

**faq1 answer**：いいえ。722本は10月6日の初回の原稿数で、10月7日に3本を取り下げた後は719本です。原稿は372の成果群に分かれ、1つの成果群に主定理、系、別証明などが含まれうるため、原稿数を解決した問題の件数とはみなせません。

**faq2 answer**：まだです。OpenAIの10月7日の記録によると、主要結果の300／719（約42％）が形式化済みです。ただし自然言語の論証すべてが独立に検証されたわけではなく、リポジトリは未形式化の結果の一部に問題がある可能性を認めています。

**callout18**：OpenAIは主要結果の形式化率を300／719（約42％）に更新したが、形式化は全原稿に対する独立したお墨付きではない。モデルやプロンプトはまだ十分に公開されておらず、各原稿と「単一プロンプト・単一エージェント」という主張には外部の評価が必要だ。

## ko 예정 초안의 변경 필드 전문

**title**：OpenAI 수학 원고, 최초 722편에서 719편으로…주요 결과 약 42% 형식화

**description**：OpenAI는 10월 6일 수학 원고 722편을 처음 공개했고, 10월 7일 3편을 철회하고 다른 14편을 수정했다. 현재 목록에는 719편이 남아 있다. 저장소는 주요 결과의 300/719, 약 42%가 형식화됐다고 밝히지만 모든 증명의 독립 검증을 뜻하지는 않는다.

**summary**：

```text
OpenAI는 10월 6일 수학 원고 722편을 처음 공개했고, 10월 7일 3편을 철회해 현재는 372개 결과군에 속한 719편이 남아 있다.
OpenAI 수정 기록은 주요 결과의 300/719, 약 42%가 형식화됐다고 밝힌다. 전체 성과가 독립적으로 검증됐다는 뜻은 아니다.
MIT의 Andrew Sutherland는 '단일 프롬프트, 단일 에이전트'라는 주장은 모델이 공개되고 재현되기 전까지 검증되지 않은 것이라고 말했다.
'AI가 수백 개의 수학 난제를 한 번에 풀었다'는 말은 아직 회사의 주장으로, 수학계의 평가가 필요하다.
```

**p3**：OpenAI는 10월 6일 비공개 내부 모델이 만든 수학 원고 722편을 GitHub에 처음 공개했다. 10월 7일 부호 오류 때문에 3편을 철회하고 다른 14편을 수정해 현재 목록에는 719편이 남아 있다. Decrypt는 OpenAI 대변인의 말을 인용해, 거의 모든 결과가 단일 AI 에이전트(스스로 단계를 나눠 작업을 수행하는 AI 프로그램)에 준 단일 프롬프트(AI에게 주는 지시문)에서 나왔지만 일부는 여러 번 시도했을 수 있다고 전했다.

**p4**：원고는 372개 결과군으로 나뉜다. OpenAI 저장소에 따르면 한 결과군에는 주요 정리, 부수 논증, 따름정리 또는 대체 증명이 포함될 수 있다. 따라서 722는 10월 6일 최초 원고 수, 719는 10월 7일 철회 이후 현행 수이며, 어느 쪽도 해결된 문제 수가 아니다. OpenAI는 모델에 약 4,000개의 문제를 제시하고 중요하다고 판단한 출력만 골라 공개했다고 밝혔다.

**p7**：Lean은 증명의 논리 단계를 기계적으로 검사하는 소프트웨어이며, 증명을 Lean으로 옮겨 검사를 통과하는 것을 '형식화'라고 한다. OpenAI의 10월 7일 수정 기록은 주요 결과 300/719, 약 42%가 형식화됐다고 밝히며 3편 철회와 다른 14편의 수정도 기록한다. 이는 형식화 비율이지 모든 자연어 논증의 독립 검증 비율이 아니다. OpenAI는 형식화되지 않은 일부 결과에 문제가 있을 수 있으며, 형식화 자료를 확보하는 대로 추가하겠다고 밝혔다.

**table9**：

```text
항목|OpenAI 공식 기록과 Decrypt 보도
원고 수|10월 6일 최초 722편, 10월 7일 3편 철회 후 현재 719편, 372개 결과군
주요 결과 형식화 비율|OpenAI의 10월 7일 기록상 300/719, 약 42%. 전체 독립 검증 비율은 아님
공개된 추론 자료|10개 결과에 관한 축약 추론 요약과 평균 연산량 수치. 프롬프트는 비공개
평균 연산량|결과당 평균 약 3시간 분량의 ChatGPT Pro 사고 연산량(OpenAI 설명)
모델 상태|내부 모델, 미공개
```

**table9 caption**：OpenAI 현행 저장소와 Decrypt 원보도를 바탕으로 정리한 수학 원고 공개 개요

**p14**：보다 긍정적인 반응도 있었다. Decrypt에 따르면 Abhishek Saha 교수는 "It is a very big day for mathematics"(수학계에 매우 중요한 날이다)라고 썼지만, 대부분의 문제는 '기존 연구 계획 안에서의 뛰어난 진전' 또는 '놀라운 돌파구'에 속한다고 지적했다. Decrypt는 10월 6일 처음 공개된 원고 722편 중 밀레니엄 난제급은 Quasi-Riemann Hypothesis 하나뿐이라고 전했다. 이 최초 수치는 현재 원고 수가 아니다.

**table17**：

```text
비교 항목|OpenAI 원고 공개|Anthropic 페르마 증명
내용|10월 6일 최초 722편, 10월 7일 이후 현재 719편. 새로운 성과를 주장|Wiles가 1995년 발표한 정리를 형식화, 새로운 결과 주장 없음
Lean 검사|OpenAI는 주요 결과 300/719, 약 42%가 형식화됐다고 기록|증명이 Lean으로 검사됨, 총 1,300만 줄
공개 방식|GitHub 저장소, 프롬프트는 비공개|Lean 증명 코드와 검증 자료를 GitHub에 공개
```

**table17 caption**：OpenAI의 10월 7일 수정 기록, Anthropic 저장소와 Decrypt 원보도를 반영한 두 공개 사례 비교

**faq1 question**：원고 722편은 OpenAI가 수학 난제 722개를 풀었다는 뜻인가?

**faq1 answer**：아니다. 722편은 10월 6일 최초 원고 수이고, 10월 7일 3편을 철회한 뒤 현재는 719편이다. 원고는 372개 결과군으로 나뉘며 한 결과군에 주요 정리, 따름정리 또는 대체 증명이 포함될 수 있다. 원고 수를 해결된 문제 수로 볼 수 없다.

**faq2 answer**：아직 아니다. OpenAI의 10월 7일 기록에 따르면 주요 결과 300/719, 약 42%가 형식화됐다. 그러나 모든 자연어 논증이 독립적으로 검증됐다는 뜻은 아니며, 저장소는 형식화되지 않은 일부 결과에 문제가 있을 수 있다고 경고한다.

**callout18**：OpenAI는 주요 결과의 형식화 비율을 300/719, 약 42%로 갱신했지만 형식화가 전체 원고에 대한 독립적인 보증은 아니다. 모델과 프롬프트는 아직 충분히 공개되지 않았으며, 각 원고와 '단일 프롬프트, 단일 에이전트' 주장에는 외부 평가가 필요하다.

## 執行與驗證紀錄

| 語言 | 原草稿／已刊 | 保存後草稿 | 獨立覆核 | 已刊新版 | 公開頁及稽核讀回 |
| --- | --- | --- | --- | --- | --- |
| zh-TW | v2／v2 | v5；逐欄重載核對 | PASS | v6 | [公開頁](https://mokaair.com/zh-TW/life/ai-news-openai-math-manuscripts-20261007)；稽核成功 17:26:10 |
| zh-CN | v2／v2 | v3；逐欄重載核對 | PASS | v4 | [公開頁](https://mokaair.com/zh-CN/life/ai-news-openai-math-manuscripts-20261007)；稽核成功 17:26:55 |
| en | v2／v2 | v3；逐欄重載核對 | PASS | v4 | [公開頁](https://mokaair.com/en/life/ai-news-openai-math-manuscripts-20261007)；稽核成功 17:25:27 |
| ja | v2／v2 | v3；逐欄重載核對 | PASS | v4 | [公開頁](https://mokaair.com/ja/life/ai-news-openai-math-manuscripts-20261007)；稽核成功 17:27:34 |
| ko | v2／v2 | v3；逐欄重載核對 | PASS | v4 | [公開頁](https://mokaair.com/ko/life/ai-news-openai-math-manuscripts-20261007)；稽核成功 17:28:01 |

2026-10-13 執行證據：

- 五語修改欄位（title、description、summary、p3、p4、p7、table9、p14、table17、FAQ 1／2、callout18 及表格說明）在草稿保存後逐語重載，與本文件的精確文案比對無差異。各語原 Decrypt 來源仍在，另六筆一手／官方來源的網址、譯名和查證日期 `2026-10-13` 已重載讀回。日期欄位需觸發輸入事件才會持久化；zh-TW 初次保存未帶日期，修正後以 v5 重載確認，其他四語在保存前完成同一操作並重載確認。
- 五語草稿均移除錯置的投資／加密資產提示框，末段連結改至各語 `/life/topics/ai-news`。共用分類從 `crypto` 改成 `ai-news` 後，逐語重載均確認 AI 新聞已勾選、加密貨幣未勾選。
- 另一名獨立審閱者對五語精確草稿及來源進行查核，修正了 top-line 限定、每項結果算力及 Anthropic 公開範圍等措辭後給予 **PASS**；該 PASS 僅涵蓋本文草稿，不代替 CMS 或公開頁讀回。
- 每語在草稿與分類確認後由管理員編輯器個別發布，修訂紀錄各有新的 `published` 版本。於[後台稽核](https://mokaair.com/zh-TW/admin/audit?target=e31a32b6-2f93-4a7a-ba45-ecc729e138b6&page=1)按 Guide ID 篩選，五筆 `guide_article_published` 事件的目標語言及結果均為成功，另有分類更新及草稿保存事件；韓文發布事件詳情可讀到本次更正原因。
- 五個公開頁逐語讀回標題及正文中的首發 722／現存 719、主要結果 300／719 約 42% 的形式化限定；未見舊 `162／722`、幣圈主題連結或投資免責；AI 新聞分類及連結可見。英文公開頁另核到七筆來源及六筆新增來源的 2026-10-13 查證日期。

正式站更正不透過 AI 新聞候選的 judge；本次 Guide 使用既有版本化草稿、獨立審稿及管理員發布機制。未合併、未部署任何程式碼；這些 CMS 內容編輯不需要程式碼部署。
