# 查證與編輯紀錄：ai-term-grounding

查證日一律 2026-10-03（本批開工日）。格式：主張｜來源網址｜查證日｜讀取方式。所有頁面都用 `curl -sSL` 直接開到，狀態碼 200，沒有用 Wayback。User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。

## 產品用法（Google、Anthropic）

在生成式 AI 中，grounding 是把模型輸出連到可驗證資訊來源的能力；Google Cloud 文件列出的接法含 Google 搜尋、Google 地圖、Agent Search、RAG Engine、Elasticsearch、你的搜尋 API 等｜https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview｜2026-10-03｜curl -sSL，原網址 https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview 轉址到此（產品現稱 Gemini Enterprise Agent Platform，頁尾 Last updated 2026-10-01）
Google Cloud 文件把減少幻覺（reduces model hallucinations / reduces the chances of inventing content）列為接地的好處，措辭是 reduces｜同上｜2026-10-03｜同上
Gemini API 的 Grounding with Google Search 讓 Gemini 連到即時網路內容，並引用知識截止日以外的可驗證來源；用途含提高事實準確（Reduce model hallucinations）、取得即時資訊、提供引用｜https://ai.google.dev/gemini-api/docs/google-search｜2026-10-03｜curl -sSL（頁尾 Last updated 2026-09-23 UTC）
Gemini 流程：提示分析（模型判斷搜尋能否改善答案）、需要時自動產生一或多個查詢並執行、處理結果並生成回覆、回傳含引用註記的回答｜同上｜2026-10-03｜同上
回應含 google_search_call、google_search_result 步驟與帶 url_citation 註記的文字區塊，註記以起訖位置把一段文字連到來源網址；文件寫「當回應成功接地時」文字輸出才含註記（正文只轉述成「成功接地時會帶有引用註記」，不寫成「只有」）｜同上｜2026-10-03｜同上
Gemini 繁體中文頁面標題為「以 Google 搜尋建立基準」，內文另譯「以 Google 搜尋強化事實基礎」｜https://ai.google.dev/gemini-api/docs/google-search?hl=zh-tw｜2026-10-03｜curl -sSL
正文不寫模型名、計費方式與價格（該頁有 Gemini 3 系列、按搜尋查詢計費等，屬易變資訊，刻意不收）｜同上｜2026-10-03｜同上
Anthropic Citations：「Ground Claude's responses in your source documents」；文件預設自動切成句子，作為最小可引用單位；回應的文字區塊附引用，位置依文件類型為字元範圍（純文字）、頁碼（PDF）或內容區塊（自訂內容）｜https://platform.claude.com/docs/en/build-with-claude/citations｜2026-10-03｜curl -sSL
Anthropic 文件：因為 API 把引用解析成固定格式並直接取出 cited_text，引用「guaranteed to contain valid pointers to the provided documents」；文件沒有宣稱被引用段落一定支持整個句子（正文明寫「文件沒說」，這是對文件沉默處的說明，不是文件的話）｜同上｜2026-10-03｜同上

## 引用品質研究（數字只寫論文設定下的結果）

ALCE 基準：引用品質分引用召回（陳述是否被引用段落完整支持）與引用精確（偵測無關引用），用 NLI 模型 TRUE（T5-11B）自動判定｜https://arxiv.org/abs/2305.14627｜2026-10-03｜摘要頁加 https://arxiv.org/pdf/2305.14627v2 全文（pdftotext，讀 §3.3 與表 4–6）
同論文摘要：在 ELI5 資料集上，即使最好的模型也有 50% 的時間缺少完整引用支持；EMNLP 2023；模型為 ChatGPT（gpt-3.5-turbo-0301）、GPT-4、LLaMA 系列等 2023 年模型（正文只寫「2023 年用當時的模型」，不寫模型名）｜同上｜2026-10-03｜同上
Liu 等人：人工評估四個商用生成式搜尋引擎，平均 51.5% 的句子完整被引用支持、74.5% 的引用支持其所附句子；回應於 2023 年 2 月下旬到 3 月下旬取得；每個引用分完整、部分、無支持三級；精確率公式為 (完整＋部分)/總數，所以 74.5% 把部分支持算進去｜https://arxiv.org/abs/2304.09848｜2026-10-03｜摘要頁加 https://arxiv.org/pdf/2304.09848v2 全文（§1、§2.4、§3.1）
Rashkin 等人 AIS：評估陳述能否歸到已指明的來源，避免對事實真偽下絕對判斷，並說明要評估事實需搭配 source quality 等方法｜https://arxiv.org/abs/2112.12870｜2026-10-03｜摘要頁加 https://arxiv.org/pdf/2112.12870v2 全文（§2 相關工作段）

## 另外兩種用法

Harnad 1990，Physica D 42: 335–346：形式符號系統的語意詮釋如何內在於系統而不是依附人腦；中文對中文字典的比喻；候選解法是由下而上、接到感官投射形成的非符號（圖像與類別）表徵｜https://arxiv.org/abs/cs/9906002｜2026-10-03｜摘要頁加全文 HTML https://arxiv.org/html/cs/9906002（arXiv 沒有 PDF；Elsevier 的 DOI 只轉到一頁殼，不當來源）
Harnad 2024：認為 ChatGPT 缺少直接的感覺動作接地（direct sensorimotor grounding）｜https://arxiv.org/abs/2402.02243｜2026-10-03｜只讀摘要頁（正文只寫摘要層級的立場）
Mollo 與 Millière：論證 LLM 可以達成指稱接地（referential grounding），即使沒有多模態或具身｜https://arxiv.org/abs/2304.01481｜2026-10-03｜只讀摘要頁
Flickr30k Entities：為圖片說明標註實體與邊界框（27.6 萬個），定義文字實體在影像中定位的評測（正文不寫數字）｜https://arxiv.org/abs/1505.04870｜2026-10-03｜只讀摘要頁
Kosmos-2：多模態模型，把文字片段與邊界框以連結形式一起表示與輸出｜https://arxiv.org/abs/2306.14824｜2026-10-03｜只讀摘要頁

## 編輯紀錄

「示例」的圖書館夏季講座、來源 A、來源 B 與三句回答都是虛構教學設定，沒有對任何產品實測；圖上的 7 月 1 日、7 月 8 日只在示例中出現，正文都有。圖上的 2026 是製圖年份，正文表格說明有 2026 年 10 月。
分級借用 Liu 等人的「完整、部分、無支持」三級；示例中的第三句標「文字相符，來源待查」是本文自訂的第四種情形（文字對得上，來源可靠性有疑問），不是論文的分類。
RAG 與接地的關係：只採 Google Cloud 文件的分類（RAG Engine 是接地的一種接法），正文已寫明「其他廠商未必同樣劃分」；「接地關心說法能否回到來源，RAG 是先檢索再生成的流程」是本文的區分說明，不是引文。
正文不使用的東西：模型名與版本、價格與計費、排行榜分數、「接地後就不會幻覺」這類保證、符號接地問題的定論。
來源 11 筆加 1 筆同一文件的繁中頁，都是官方文件或論文頁，沒有新聞、部落格、內容農場。
字數：以 pack_ingest 的 `_body_length` 算是 2,542（含 rich_paragraph 內的站內連結文字 72 字）；不含連結文字為 2,470。本批 brief 寫「不含連結文字」，但程式實際會把 rich_paragraph 裡的連結文字算進去；兩個數字都在 1,800–3,000 內。
SVG 為原創向量插圖，非 AI 產圖；hero 沒有文字、沒有 logo。
自驗：dry-run 通過，只剩 `no_summary` 警告（範本 ai-term-sandbox 同樣有）。brief 指定的渲染指令使用 chromium-1194/chrome-linux/chrome，視窗會被裁掉底部約 88 px（白帶），所以另用 chromium_headless_shell-1194 的 headless_shell 看完整 1600×900，兩張圖都沒有疊字或超框；正式 ingest 的預設會先選 headless_shell。
