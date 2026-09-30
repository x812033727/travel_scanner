# 可查主張：RAG 是什麼？有引用，為什麼還是答錯

2026-09-30 撰稿者初查；另一位查核代理要對著 `video.json` 的旁白、字卡、標題、縮圖與說明欄逐條重開來源。格式：`編號｜主張（照旁白或字卡的寫法）｜來源｜查證日｜scene id`。示範的數字來源是 `demo-log.md`（自行執行的計算，不是任何產品介面的錄影）；文章指 `apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json`（zh-TW），網址 https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation 。

c1｜RAG，中文叫檢索增強生成，一句話：先找、再答；其實 RAG 只保證一件事：答案是從找到的段落組出來的｜https://docs.langchain.com/oss/python/deepagents/retrieval（原句 "Retrieval addresses these problems by fetching relevant external knowledge at query time. This is the foundation of Retrieval-Augmented Generation (RAG)"、"integrate retrieval with generation to produce grounded, context-aware answers"）｜2026-09-30｜s-assembly, define
c2｜二〇二〇年提出這個詞的論文，把兩種記憶接在一起：一種鎖在模型參數裡，一種放在外面的索引裡｜https://arxiv.org/abs/2005.11401（Submitted on 22 May 2020；原句 "models which combine pre-trained parametric and non-parametric memory for language generation"、"the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia"）｜2026-09-30｜s-two-boxes, s-keyhole
c3｜今天的用法更廣：先檢索，把段落放進提示詞，一起交給模型；名字一樣，還是要問資料從哪裡來、檢索器會不會變｜https://docs.langchain.com/oss/python/deepagents/retrieval（"2-Step RAG: Retrieval always happens before generation"）；https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview（"Generation: The retrieved information becomes the context added to the original user query"）；文章「一種組合方式，不是一個資料庫」｜2026-09-30｜s-envelope, s-same-name
c4｜三步：建索引（切段，留下文件、章節、版本、權限）、檢索（問題變查詢，取回候選段落，必要時重排）、生成（模型拿問題加段落，寫出有出處的答案）；圖解的線：問題進檢索器、索引給段落、模型寫答案｜https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview（流程順序 data ingestion → transformation/chunks → indexing → retrieval → generation）；文章「資料如何走到答案裡」與圖解 diagram-1.svg｜2026-09-30｜s-index-card, steps, s-belt, diagram
c5｜示範：六段虛構的課程規章（第一段現行退費規則 2026 年版、第二段材料費例外、第三段課程分類、第四段舊版規則已失效、第五段報名方式、第六段停辦公告），用關鍵字比對來檢索，三題各排一次名｜demo-log.md（BM25、字元二元組，2026-09-30 自行執行；`SCRATCH/demo/demo-rag.json`）｜2026-09-30｜s-six-cards, six, s-lineup
c6｜第一題「我報了週末陶藝班，開課前取消可以全額退費嗎？」：舊版規則（已失效）5.11 排第一、課程分類 4.84、現行規則 4.70 只排第三、停辦公告 4.16、報名方式 1.53、材料費例外 0.47 最後一名｜demo-log.md｜2026-09-30｜ask-refund, s-queue-old, s-last-card, rankings, s-scale, s-pushed-back
c7｜第二題「報名之後不去了，錢拿得回來嗎？」（沒有「退費」兩個字）：報名方式 1.81 第一、現行規則 1.32、材料費例外 1.11；課程分類、舊版規則、停辦公告都是 0（字卡「課程分類等三段 0」）｜demo-log.md｜2026-09-30｜rankings, s-rephrase
c8｜第三題「去年停辦的週末陶藝班，退費怎麼算？」：停辦公告 6.38 第一、課程分類 4.84、現行規則 0.56、材料費例外 0.47、舊版規則 0.42、報名方式 0 最後；公告原文「已繳費用依 2025 年版規則辦理」，所以系統得再找一次舊版｜demo-log.md｜2026-09-30｜rankings, s-notice-thread, s-second-trip, s-all-years
c9｜示意回覆「可以，開課前取消一律退還課程費全額。依據：一般退費規則 2025 年版」是照第一名段落（第四段舊版規則）的原文寫的示意，不是任何產品或模型的輸出；旁白明說「示意的回覆」「我照它找到的第一段寫的示意」｜demo-log.md §示意回覆｜2026-09-30｜ask-refund, s-counter, s-handoff
c10｜那條規則今年一月就失效了：第四段原文「2025 年版，已於 2026 年 1 月 1 日失效」，撰稿日 2026-09-30｜demo-log.md（第四段原文）｜2026-09-30｜hook, s-stamp, six, s-hourglass
c11｜拿著證據答錯的三種方式：資料沒更新（新舊規章一起競爭排名，舊版贏了）、文件沒找齊（材料費例外排最後，沒進上下文）、解讀過頭（條文寫材料費另計，模型接成全額退）｜文章「有來源仍可能答錯」（"模型還可能引用真實文字，卻接出原文不支持的結論"）與「資料如何走到答案裡」（"讓新舊規章同時競爭搜尋排名"）；示範數字見 c6｜2026-09-30｜s-scale, s-pushed-back, s-bridge, s-three-stamps
c12｜答錯先分兩種：把正確條文直接放到模型面前再問一次；答對就是檢索的問題（修索引、切段、排序）；還漏材料費就查指令、上下文排列、答案驗證；比一直換模型更快找到原因｜文章「示範：一個帶條件的退費問題」與 callout「先看原文有沒有被取回」｜2026-09-30｜split, s-hand-clause, s-empty-drawer, s-prompt-tinker, s-swap-models
c13｜權限也算檢索品質：讀者能看什麼要在檢索那一步限制；不能先取回內部紀錄再指望模型不說；取回的文字只是內容，文件裡寫著請忽略規則也改不了你的任務；來源可靠、使用者有權看、文字相關是三個不同的檢查｜文章「有來源仍可能答錯」第二段｜2026-09-30｜s-locked-door, checks, s-three-windows
c14｜驗收清單：常見題（答案要回到原文）、跨章節、舊版干擾、資料沒涵蓋；缺資料要坦白停住；每題記下取回哪些段落、哪句有依據、文件版本；留著紀錄日後換模型或換索引才能重做同一組比較｜文章「何時值得使用，如何驗收」第二段｜2026-09-30｜checklist, s-ticked, s-redo
c15｜直接搜尋：交付文件或片段，讀者自己彙整；RAG：取回依據後生成回答，檢索與引用仍要驗證；微調：訓練行為或能力，不等於即時更新資料｜文章對照表「概念對照」｜2026-09-30｜s-pile, methods, s-tuning
c16｜什麼時候值得建：資料一直在更新、答案要附出處、一個模型服務好幾套資料；要穩定守格式、學語氣時微調更貼近，兩者可併用；資料只有一頁時直接整頁放進上下文可能就夠；複雜度跟資料量、更新頻率、權限一起算｜文章「何時值得使用，如何驗收」第一段；「模型訓練時不可能讀過你昨天才修改的活動辦法」出自文章首段｜2026-09-30｜s-both, when, s-one-page
c17｜建索引別漏掉的：退費條文連同適用課程和生效日期一起存；只存一句「可以退費」丟了截止條件，找到了也會答錯；引用最好指到那一段，不是只給文件首頁；版本更新要讓舊段落退出，不能只加新版一起排名｜文章「資料如何走到答案裡」第二段｜2026-09-30｜s-page-link, index-care
c18｜檢索器不一定是向量資料庫，全文索引、結構化查詢也能做｜文章「一種組合方式，不是一個資料庫」第二段（"向量資料庫只是可能使用的儲存與相似度查詢元件，全文索引、結構化查詢也能扮演檢索角色"）｜2026-09-30｜s-not-only-vector
c19｜站主觀點（提案，待站主確認）：驗收先看該找到的條文有沒有進到模型眼前，再看答案忠不忠於那段條文，兩件事分開量；它會改變兩個決定：信不信這個答案、給不給它權限｜brief.md §站主觀點（對應頻道立場草稿第 3、4 條與系列立場提案第 8、9 條）｜2026-09-30｜s-two-rulers, s-second-ruler, s-trust

沒有編號的句子是比喻與過場（圖書館館員、收據、天平、太短的木板、兩把尺），不是事實主張；「語意搜尋和嵌入向量，那是另一集的事」指系列的嵌入向量那一集（`docs/videos/ai-terms/terms.json` 第 8 個名詞），還沒發布。

## 與企劃不同的地方

- 開場第二句：OUTLINE 寫「去年一月就失效了」，但示範資料第四段是「已於 2026 年 1 月 1 日失效」，撰稿日是 2026-09-30，所以旁白、說明欄與 Shorts 都寫「今年一月就失效了」；「去年」留給第六段的停辦公告與第三題（2025 年秋季）。
- 卡片：配方 C 的十張之外加了五張 `bullets`（六段規章、建索引別漏掉的、三個不同的檢查、驗收清單、什麼時候值得建）與一張 `table`（三種做法），共 16 張；配方卡片彼此的順序不變，但 `cta` 放在第四章示範之後、第五章 `compare` 之前（OUTLINE 的章節節拍把 cta 放在第四章；同一份 OUTLINE 的配方列成 compare → cta，兩者互相矛盾，取「示範之後、中段」那條規則）。
- shot 52 個（PACKET 說大約 38 到 45）：每個 shot 一到兩句、估計都在 8 秒內，插圖佔 60%；少於這個數量，不是到不了 9.5 分鐘，就是有畫面會超過 8 秒。
- 第四章把「三種答錯方式」和「第二題換問法、第三題還要再找舊版」分開講，OUTLINE 是列在同一段。
- 第六章多了「別為一頁紙蓋倉庫」的比喻與 `bullets`「什麼時候值得建 RAG」，內容來自文章的「何時值得使用」節。
- 站主觀點在旁白多講了後半句「它會改變兩個決定：信不信這個答案、給不給它權限」，是 brief §站主觀點同一個看法的一部分，不是新意見。

## 我懷疑但沒動的事

- `lexicon.json` 把 RAG 唸成「R A G」；業界常唸成一個字。要不要改，等試聽再決定（PACKET 說不改字典）。
- 年份用「二〇二五」「二〇二〇」：沿用系列其他影片的寫法，但 Gemini 對「〇」的唸法沒試聽過。
- `rankings` 表第一列第二格用了 `**舊版規則（已失效）** 5.11` 加 `highlight: 0`，兩層強調；版面太滿就去掉粗體。
- 「線上表單」會撞到 lint 的書面語「上表」，改成「網路表單報名」；其他集如果寫「線上」接「表」開頭的詞會踩到同一條，值得在工具票裡提一下。
- 第二題最後一名有三段同分 0，字卡合併成「課程分類等三段 0」，旁白沒唸最後一名。
- 節奏警告「平均 6.5 秒換一次畫面，目標 6 秒」：要降到 6 秒得再拆約 8 個 shot（會到 60 個），與 38 到 45 的指引相反，所以沒動；每個狀態最長 7.8 秒，插圖 60%，最終品管只擋這兩項。

## 進度

- 2026-09-30：brief.md、spec.json → video.json（68 景、52 個 shot、110 句、估 9.9 分）、claims.md、demo-log.md、shorts.json 全部寫完；`lint` 0 錯誤、1 個警告（average）。
- 待：查核代理覆核 c1–c19（重開三個官方頁與文章）；試聽「RAG」與「〇」；`tts --dry-run` 看實際長度；站主確認 brief 的站主觀點提案。
