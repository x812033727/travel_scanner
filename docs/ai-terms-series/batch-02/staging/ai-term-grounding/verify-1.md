# 查核紀錄 1：ai-term-grounding

查核者：Claude（claude-opus-5-5），不是撰稿者。查核日 2026-10-03。所有頁面都在今天用 `curl -sSL` 重新打開（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`），沒有沿用撰稿者的 notes.md 或 research.json；論文讀 arXiv 摘要頁，ALCE、Liu 等人、AIS 三篇另讀 PDF 全文（pdftotext）。

## 修改

1. 「回答再標出每個說法對應哪一段資料」→「回答再把其中的說法標上對應的來源」｜Gemini 的 url_citation 只把回答中的一段文字（start_index、end_index）連到來源網址與標題，不指出來源裡的哪一段；只有 Anthropic 會附被引用的原文。原句把兩家說成都對到「哪一段資料」，也暗示「每個說法」都有標｜https://ai.google.dev/gemini-api/docs/google-search
2. 「保證的是位置有效，文件沒說那一段足以支持整句」→「文件也把引用描述成支持該說法的段落，但寫明『保證』的只有位置有效，沒有保證那一段足以支持整句」｜Anthropic 文件開頭寫「Citations return the exact passages that support each claim」，並說每個文字區塊附「a list of citations that support the claim」，所以不能說文件「沒說」引用支持說法；文件用 guaranteed 的只有「valid pointers to the provided documents」｜https://platform.claude.com/docs/en/build-with-claude/citations
3. 「74.5% 的引用支持所附的句子，這個比率還把部分支持算進去」→「……；後者在一句由幾個引用合起來才完整支持時，也把各自只支持一部分的引用算進去」｜論文 §2.4：精確率是 (Tfs＋Tps)/N，Tps 只算「所附引用合起來完整支持該句，且沒有任何一個引用單獨完整支持」時的部分支持引用；原句寫成無條件算入｜https://arxiv.org/abs/2304.09848（全文 https://arxiv.org/pdf/2304.09848v2 §2.4）
4. 「它們是兩三年前的系統」→「它們是三年多前的系統」｜Liu 等人的回應取得於 2023 年 2–3 月；ALCE v2（2023-10）用的模型最晚是 2023 年 7 月推出的 LLaMA-2-Chat。到 2026 年 10 月都是三年多｜https://arxiv.org/abs/2304.09848 、https://arxiv.org/abs/2305.14627
5. 新增一段（在視覺接地段之後、總索引連結之前）：「此外，心理學家 Clark 與 Brennan 1991 年的〈Grounding in Communication〉用這個詞指對話中的協作過程：交談雙方設法確認剛說的話已被理解，把它納入共同基礎（common ground）。它談的是人與人的溝通，本文同樣不展開。」並在 sources 加這一筆｜撰稿者提出對話接地值得一提；原文寫「they try to ground what has been said—that is, make it part of their common ground」「grounding is the collective process by which the participants try to reach this mutual belief」，兩位作者通訊地址都是心理學系。出版社 DOI 10.1037/10096-006 對 curl 回 403，改用 Clark 在 Stanford 網站放的章節 PDF（200，application/pdf）｜https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf

措辭修改（不算事實修改）：
- 「這個詞另外還有兩個很不一樣的意思」→「另外至少還有兩個」｜配合第 5 項，避免和新增的對話用法矛盾。
- 「論文摘要寫到最好的模型也有大約一半的陳述缺少完整的引用支持」→「論文摘要寫到，最好的模型也有一半的情況缺少完整的引用支持」｜摘要原文是「lack complete citation support 50% of the time」；引用召回率雖是逐句平均，但掛在「摘要寫到」之下就照摘要的說法。https://arxiv.org/abs/2305.14627
- 「Google Cloud 文件把接地定義為……的能力，流程可拆成三步」→「……的能力。產品裡的流程，本文拆成三步來看」｜Google Cloud 那頁沒有三步流程，原句容易讀成那頁的說法。
- sources 第 3 筆標題改為「Google Cloud：Grounding overview（Gemini Enterprise Agent Platform 文件；舊 Vertex AI 網址轉址至此）」，跟現在的頁面標題一致。

改完的正文長度（`_body_length`）：2,723 字（原 2,542）；6 個 H2、1 個表、1 個 callout，五個指派連結都在。dry-run 只剩 `no_summary` 警告，`dry run: nothing written`。diagram-1.svg 沒改：圖上文字、`<desc>` 和正文示例一致，7 月 1 日、7 月 8 日在正文都有，2026 對到表格說明。

## 查過、沒問題的主要主張

- Vertex AI 舊網址的最後落點：`https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview` → 301 → `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview` → 301 → `https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview`（200，頁名「Grounding overview | Gemini Enterprise Agent Platform」，頁尾 Last updated 2026-10-01 UTC）。pack 用的就是最後這個網址。
- Google Cloud：「grounding is the ability to connect model output to verifiable sources of information」；好處列「Reduces model hallucinations」；接法表有 Google Search、Google Maps、Agent Search（寫明用 RAG）、RAG Engine、Elasticsearch（寫明用 RAG）、your search API、Web Grounding for Enterprise、Parallel web search。所以「RAG 是 Google 分類裡接地的做法之一」「措辭是降低」都成立。
- Gemini API「Grounding with Google Search」（Last updated 2026-09-23 UTC）：連到即時網路內容、引用知識截止日之外的可驗證來源；用途列 Reduce model hallucinations、Answer questions about recent events、Provide citations；流程是 Prompt Analysis（判斷搜尋能否改善答案）→ If needed 自動產生並執行一或多個查詢 → 處理結果 → 回傳帶 inline annotations 的回答；「When a response is successfully grounded」才描述註記；每個 url_citation 以 start_index、end_index 把一段文字連到來源網址。正文的「要不要搜尋是模型判斷的」「開了搜尋工具不保證每次都有搜尋與引用」是從 If needed 與 successfully grounded 推得，沒有寫過頭。
- 繁中頁（上次更新 2026-09-24）標題「以 Google 搜尋建立基準」，內文「以 Google 搜尋強化事實基礎」。
- Anthropic Citations：「Ground Claude's responses in your source documents」；純文字與 PDF 預設切成句子，作為最小引用單位（自訂內容不再切）；回應附 cited_text 與位置（字元範圍、頁碼或內容區塊）；「guaranteed to contain valid pointers to the provided documents」的理由是 API 解析引用並直接取出 cited_text。
- ALCE（Gao、Yen、Yu、Chen，EMNLP 2023）：引用召回＝陳述是否被所引段落完整支持，引用精確＝偵測無關引用，兩者都用 NLI 模型 TRUE（T5-11B）判定；ELI5 是長篇問答；摘要寫「even the best models lack complete citation support 50% of the time」；實驗模型都是 2023 年的（表 6，ChatGPT VANILLA 引用召回 51.1）。正文沒寫模型名。
- Liu、Zhang、Liang：人工評估（Mechanical Turk 評分員）四個商用生成式搜尋引擎，1,450 個查詢，回應在 2023 年 2 月下旬到 3 月下旬取得；平均 51.5% 句子完整被引用支持、74.5% 引用支持所附句子；每個引用分 full、partial、no support 三級（正文示例清單借用這三級並標明出處）。
- Rashkin 等 AIS：全文 §2 寫「we avoid absolute judgments regarding "factuality"」，並說需要搭配「source quality」等方法評估事實。
- Harnad 1990：arXiv cs/9906002，期刊資訊 Physica D 42: 335–346，DOI 10.1016/0167-2789(90)90087-6；摘要有內在意義 vs. 依附人腦解讀、中文對中文字典的比喻、由下而上接到感官投射形成的非符號（iconic、categorical）表徵的候選解法。正文三點都對。
- Harnad 2024：arXiv 2402.02243 v1 為 2024-02-03；摘要寫 ChatGPT 缺少「direct sensorimotor grounding to connect its words to their referents」。ChatGPT 只在這一句當成該論文的討論對象出現，另一次在來源標題，沒有當成產品介紹或比較。
- Mollo、Millière：摘要寫 LLM 可以滿足指稱接地的兩個條件，「even without multimodality or embodiment」。正文把兩邊立場並列、不下結論，符合「不寫成定論」。
- Flickr30k Entities：為說明裡的實體提及標註邊界框，定義「localization of textual entity mentions in an image」基準。Kosmos-2：把指稱表示成「[text span](bounding boxes)」的 Markdown 連結。
- 系列規矩：沒有型號、價格、截止日期、排行榜分數；Gemini、Claude 只當成指派點名的 API 功能出現；示例標「虛構示例，沒有實測任何產品」，結果寫成「預期結果」；「自然語言推論（NLI）」的推論＝inference 用對，全文沒有「推理」；沒有「接地後就不會幻覺」這類保證；台灣用語。
- 所有 sources 今天都回 200，`checked_on` 2026-10-03 合理；沒有新聞或部落格。

## 站內既有文章 gemini-api-search-grounding-citations（只回報，沒有修改）

`apps/api/app/guides/content/gemini-api-search-grounding-citations.json` 寫「此版本 SDK 的引用欄位說明以 UTF-8 位元組計算位置」，FAQ 也說中文切錯「可能把位元組位置當成字元位置」。今天的狀況：

- Gemini「Grounding with Google Search」指南（2026-09-23）沒有寫 start_index、end_index 的單位。它的 Python、JavaScript、Java 範例直接對文字字串切片（Python 依碼位，JS、Java 依 UTF-16），Go 範例 `text[start:end]` 依位元組切，範例之間不一致。
- Interactions API 參考頁 https://ai.google.dev/api/interactions-api（Last updated 2026-10-02 UTC）的 UrlCitation.start_index 寫「Index indicates the start of the segment, measured in bytes.」，end_index 只寫「End of the attributed segment, exclusive.」。
- python-genai 文件 https://googleapis.github.io/python-genai/genai.html 裡 generateContent 的 Segment.start_index、end_index 寫「measured in bytes」。

所以「以位元組計」今天仍有官方參考頁支持，但「UTF-8」三個字在這些頁面上找不到，是合理推論，不是原文。該文的來源列的是指南與 SDK 首頁（2026-09-14 查證），沒有列 Interactions API 參考頁；若要補強，可以把那一頁加為來源。

## 我懷疑但沒改的事

- research.json 的 `running_text_characters`（2,542）和 notes.md 的字數已經過時，改完是 2,723；兩份也沒有 Clark 與 Brennan 這筆來源。依指令我只寫 pack.json 與 verify-1.md，沒動這兩份。
- 2,723 字超過 brief 的目標區間 2,100–2,500，但在 1,800–3,000 的上限內；多出來的主要是新增的對話接地段與 Liu 的條件說明。
- 機制段的「放進上下文：取回的內容進入上下文」是本文自己的概括；Gemini 指南只寫模型「processes the search results, synthesizes the information」，沒有用 context 一詞。我已把三步改成本文自己的拆法，沒有再改這句。
- Harnad 2024 的期刊版是 Frontiers in Artificial Intelligence 第 7 卷 1490698（2024-12-20 線上、2025-02-12 出版），題名少了「Grounding」。正文寫「2024 年的論文」，來源用 arXiv 題名，兩者都對得上；只是讀者用期刊題名找會找不到同一個字串。
- Mollo 與 Millière 的 arXiv 已更新到 v3（2025-12），註明 accepted in Philosophy and the Mind Sciences；正文只用摘要層級的立場，沒有受影響。
- Clark 與 Brennan 的 PDF 放在作者 Stanford 網頁上，是掃描的章節；PDF 首行把 Brennan 寫成「S. A.」（章節本身署名 Susan E. Brennan）。出版社頁對 curl 回 403，所以沒有改用出版社網址。
- ALCE 的「一半」只對摘要說的最好模型；同篇表 6 中加上 RERANK 的 ChatGPT 在 ELI5 的引用召回升到 69.3。正文沒寫這點，也不需要寫，在此記錄。

facts_changed: 5
