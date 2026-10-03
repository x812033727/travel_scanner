# 查核紀錄 2：ai-term-grounding

查核者：Claude（claude-opus-5-5），第二輪，不是撰稿者也不是第一輪查核者。查核日 2026-10-03。所有來源今天重新用 `curl -sSL` 打開（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`），13 筆 sources 全部回 200；Liu 等人、ALCE、AIS 三篇另讀 arXiv PDF 全文（pdftotext），Clark 與 Brennan 讀 Stanford 的章節 PDF。沒有沿用第一輪的抓取結果。

## 修改

沒有事實性修改。第一輪的五處修改今天都對得上來源（見下一節），隨機抽查的主張也都成立。

措辭修改（不算事實修改；目的是讓一般讀者讀得順，並把正文從 2,723 字縮到 2,593 字，結構不變：6 個 H2、1 個表、1 個 callout、五個指派連結都在）：

1. 「放進上下文：取回的內容進入上下文，回答依據它寫成」→「放進上下文：這是本文的概括，指取回的內容和你的問題一起交給模型，回答依據它寫成」｜原句緊接在「Gemini API 文件說……」之後，讀起來像在轉述文件；Gemini 指南只寫模型「processes the search results, synthesizes the information, and formulates a response」，Gemini 與 Anthropic 兩頁的流程說明都沒有用 context 一詞，所以標明是本文的概括。「產品裡的流程，本文拆成三步來看」順手縮成「實際流程，本文拆成三步」，「Anthropic 的 Citations 文件談的是你交給 API 的文件，系統預設……」縮成「Anthropic 則用你交給 API 的文件，預設……」｜https://ai.google.dev/gemini-api/docs/google-search 、https://platform.claude.com/docs/en/build-with-claude/citations
2. 「引用只告訴你這句話從哪裡來，沒說來源真的這樣寫。Anthropic 文件說，……文件也把引用描述成支持該說法的段落，但寫明『保證』的只有位置有效……」→「引用告訴你這句話出自哪裡，不代表來源真的這樣寫。以 Anthropic 文件為例，它把引用描述成支持說法的原文段落，但用上『保證』一詞的只有一點：因為 API 會解析引用並直接取出原文，引用一定指向你提供的文件中有效的位置。那一段是否足以支持整句，文件沒有保證……」｜內容同第一輪的修正，只把順序改成先講文件的描述、再講保證的範圍；「沒說」改「不代表」，因為引用本身就隱含「來源這樣寫」的主張｜https://platform.claude.com/docs/en/build-with-claude/citations
3. ALCE：「把引用品質拆成『陳述有沒有被引用的段落完整支持』與『有沒有無關的引用』兩項，判定交給 NLI 模型」→「用 NLI 模型自動判定陳述是否被所引段落完整支持」｜後面的 50% 只關係到前一項（引用召回），引用精確這項讀者用不到；NLI 判定仍寫出，作為數字的設定｜https://arxiv.org/abs/2305.14627（全文 §3.3）
4. Liu：「……74.5% 的引用支持所附的句子；後者在一句由幾個引用合起來才完整支持時，也把各自只支持一部分的引用算進去」→「……74.5% 的引用支持所附的句子（幾個引用合起來才完整支持一句時，各自只支持一部分的也算在內）」；回應取得時間併進主句｜條件與第一輪一致：Tps 只在「所附引用合起來完整支持，且沒有任何一個單獨完整支持」時計入，「合起來才完整支持」的「才」帶出後一個條件｜https://arxiv.org/pdf/2304.09848v2 §2.4
5. 導言「這個詞另外至少還有兩個很不一樣的意思，一個來自認知科學，一個來自電腦視覺。本文先分開……」→「這個詞在認知科學、電腦視覺等領域另有很不一樣的意思，所以下面先分清三種用法，再看產品裡怎麼運作，以及有引用為什麼還要核對。」；第六個 H2「另外兩種接地：符號與影像」→「其他用法：符號、影像與對話」｜第一輪在這一節加了 Clark 與 Brennan 的對話用法，標題寫「兩種」卻講了三種｜—
6. Clark 與 Brennan 一句：「用這個詞指對話中的協作過程：交談雙方設法確認……，把它納入共同基礎」→「……裡用這個詞指對話中的協作：雙方設法確認剛說的話已被理解，納入彼此的共同基礎（common ground）。這是人與人的溝通，本文不展開。」｜只縮句，主張不變｜https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf
7. 其他縮句：刪「這是供應商文件裡的用法」（後句「各家範圍不一定相同」已涵蓋）；AIS 的英文全名改成「歸因評估框架 AIS」（全名留在來源標題）；RAG 段的接法例子刪 Elasticsearch，並把「分類裡」重複的兩句合併；「核對並不因此消失」→「但核對這一步省不掉」；Harnad 段刪「發表於 Physica D」（期刊資訊留在來源標題）；視覺接地段刪和表格重複的「它問的是詞指圖上哪一塊」；示例處理句「標資料未寫」→「註明來源沒寫」、「補一個合理的位置」→「補一個看似合理的出處」；「用處在於」→「但能」。

另外同步了 `notes.md` 與 `research.json`：加入 Clark 與 Brennan 這筆來源（含出版社 DOI 回 403、改用作者網站 PDF 的讀法）；Anthropic 一條改掉已過時的「文件沒說」說明；Liu 一條把「74.5% 把部分支持算進去」改成有條件的說法；Gemini 一條寫明 url_citation 只連到網址與標題、正文的三步是本文的拆法；Harnad 2024 補上 v2 與期刊版資訊；`running_text_characters` 以 `_body_length` 實算為 2,593（不含站內連結文字 72 字為 2,521）。

dry-run：`dry run: nothing written`，只剩 `no_summary` 警告（範本 ai-term-sandbox 也有）。diagram-1.svg、hero.svg 沒動；圖上的 7 月 1 日、7 月 8 日在正文示例都有，2026 對到表格說明，dry-run 的圖上數字檢查通過。

## 第一輪五處修改的複查

1. Gemini url_citation（第一輪修改 1）：Gemini 指南（Last updated 2026-09-23 UTC）寫「Each url_citation annotation links a text segment (defined by start_index and end_index) to a source URL」，範例註記只有 type、url、title、start_index、end_index，沒有指向來源內的段落。正文「回答再把其中的說法標上對應的來源」「Gemini 的引用註記把回答中的一段文字連到來源網址」成立。繁中頁（上次更新 2026-09-24）同義：「將回覆內容的各個部分連結至來源」。
2. Anthropic 的保證範圍（第一輪修改 2）：今天頁面仍寫「Citations return the exact passages that support each claim」「a list of citations that support the claim」，以及「Because the API parses citations into the response formats … and extracts cited_text directly, citations are guaranteed to contain valid pointers to the provided documents」。頁面上 guaranteed 只出現在這一句。第一輪的判斷成立，第二輪只改語序。
3. Liu 等人 74.5%（第一輪修改 3）：摘要「only 74.5% of citations support their associated sentence」；§2.4「let Tps be the number of citations that partially supports its associated statement, where the associated statement is fully supported by the union of its associated citations and no associated citation fully supports the statement by itself」，精確率 (Tfs＋Tps)/N；圖 2 說明也寫「Partially-supporting citations only improve citation precision when their associated statement is supported by the union of its citations and no other associated citation fully supports the statement by itself」。正文括號的條件成立。
4. 「三年多前」（第一輪修改 4）：Liu 等人 §3.1「Responses were scraped between late February and late March 2023」；ALCE v1 2023-05-24、v2 2023-10-31，實驗模型都是 2023 年的。到 2026-10-03 為三年多（最近的也超過三年兩個月）。成立。
5. Clark 與 Brennan（第一輪修改 5）：Stanford PDF 回 200（application/pdf，12 頁掃描）。章節第 128 頁：「In conversation, for example, the participants try to establish that what has been said has been understood. In our terminology, they try to ground what has been said—that is, make it part of their common ground.」；同一跨頁另有「grounding is the collective process by which the participants try to reach this mutual belief」。通訊地址兩人都在心理學系（Stanford、SUNY Stony Brook）；書目為 Resnick、Levine、Teasley 編《Perspectives on socially shared cognition》，APA Books，1991。出版社 https://doi.org/10.1037/10096-006 今天仍對 curl 回 403（轉到 content.apa.org），psycnet 也是 403，所以維持作者網站的 PDF。正文的「心理學家」「1991」「確認剛說的話已被理解」「共同基礎（common ground）」「協作」都對得上。

## 隨機抽查（其餘 23 條主張抽 8 條，Python `random.seed(20261003)` 抽樣）

- 產品文件的定義「讓模型的回答連到可以查證的來源」、Google Cloud「把模型輸出連到可驗證資訊來源的能力」：Grounding overview（Gemini Enterprise Agent Platform，Last updated 2026-10-01 UTC）原文「In generative AI, grounding is the ability to connect model output to verifiable sources of information.」舊 Vertex AI 網址今天仍轉址到這頁。成立。
- Anthropic Citations「讓回答對回你提供的文件」：頁首「Ground Claude's responses in your source documents.」成立。
- Anthropic「API 會解析引用並直接取出原文」：同上第 2 項。成立。
- ALCE 用 NLI 模型判定陳述是否被所引段落完整支持：全文「citation recall, which determines if the output is entirely supported by cited passages」，判定用 TRUE（T5-11B，在 NLI 資料集上微調）。成立；「自然語言推論」對 inference，全文沒有「推理」。
- Google Cloud 接法例子 Google 搜尋、你自己的搜尋 API、RAG Engine：表格有 Grounding with Google Search、Grounding with your search API、Grounding with RAG Engine（「a configurable managed RAG service」），另有 Agent Search、Elasticsearch 寫明用 RAG。「在 Google 的分類裡 RAG 是接地的做法之一」成立。
- Harnad 2024「ChatGPT 缺少直接的感覺動作接地」：摘要「what it is that ChatGPT lacks, which is direct sensorimotor grounding to connect its words to their referents」。成立。
- Kosmos-2「把文字片段與邊界框一起輸出」：摘要「we represent refer expressions as links in Markdown, i.e., "[text span](bounding boxes)"」。成立。

抽樣外順手確認：Gemini 用途（Reduce model hallucinations、Answer questions about recent events、cite verifiable sources beyond its knowledge cutoff）；流程 Prompt Analysis → If needed 產生並執行查詢；「When a response is successfully grounded」才描述註記；繁中頁標題「以 Google 搜尋建立基準」；Google Cloud「Reduces model hallucinations」；Liu 的 full、partial、no support 三級與「人工評估四個商用生成式搜尋引擎」；AIS 全文「we avoid absolute judgments regarding "factuality"」與「complementary evaluation methods such as "source quality"」；Harnad 1990 摘要的 intrinsic vs. parasitic、Chinese/Chinese dictionary、bottom-up nonsymbolic representations，期刊 Physica D 42: 335–346；Mollo 與 Millière「We argue that LLMs can meet both conditions, even without multimodality or embodiment」；Flickr30k Entities 為說明中的實體標邊界框並定義「localization of textual entity mentions in an image」。系列規矩（沒有型號、價格、截止日期、排行榜分數；示例標明虛構、結果寫成「預期結果」；沒有「接地後就不會幻覺」；符號接地不下定論；台灣用語）在精簡後都維持。

## 我懷疑但沒改的事

- 第六節現在講三種其他用法，但第一節的辨識表仍是三列（產品、符號、視覺），沒有對話這一列。對話用法只是一句帶過，表格加列會把篇幅拉回去，所以沒加；標題已改成「其他用法」避免「兩種」對不上。
- Clark 與 Brennan 的來源是作者 Stanford 個人網頁上的掃描 PDF，不是出版社頁；出版社 DOI 對 curl 回 403。PDF 首行把 Brennan 寫成「S. A.」，章節署名是 Susan E. Brennan，來源標題沒有寫縮寫，不受影響。
- 「符號接地問題出自 Harnad 1990 年的論文」：這個名稱由該文提出是通行說法，但我只讀了摘要與 arXiv HTML 的開頭，沒有另找文獻史來源證明「之前沒人這樣叫」。
- Harnad 2024 的期刊版（Frontiers in Artificial Intelligence 7: 1490698）題名少了「Grounding」，arXiv 現在有 v2（2025-02-17）。正文的「2024 年的論文」對得上 v1 與期刊卷次。
- 正文 2,593 字，在指示的 2,300–2,600 內，但仍高於 brief 的目標 2,100–2,500；再往下縮就要動示例或研究段的設定說明，我判斷那些是讀者需要的。
- 第一輪回報的站內既有文章 gemini-api-search-grounding-citations 的「UTF-8 位元組」問題不在本文範圍，我沒有重查，也沒有動。
- 程序：我在 repo 根目錄跑過一次唯讀的 `git status --short`（看工作區有沒有多出檔案），違反「不跑 git」，沒有改動任何東西。

facts_changed: 0
