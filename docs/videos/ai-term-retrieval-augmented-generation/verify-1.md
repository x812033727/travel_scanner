# 查核第一輪：RAG 是什麼？有引用，為什麼還是答錯（2026-09-30）

獨立查核者，沒有寫過這份稿子。每一條都自己開：三個官方頁今天重抓（都 200），`demo_rag.py` 在 `SCRATCH/ai-term-retrieval-augmented-generation/verify/` 重跑一次（`docs` 與 `results` 和 `SCRATCH/demo/demo-rag.json` 相同），文章直接讀 `apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json`，正式站文章與總索引各 200。輔助腳本：`extract_claims.py`（主張清單 `claims-list.md`、聽眾檢查）、`check_description.py`（說明欄的六段與分數對 demo）、`write_verify.py`（這份）。

判定：CONFIRMED 確認 ／ CHANGED 改了 ／ NOT FOUND → CHANGED 找不到所以改 ／ OUT OF SCOPE 比喻、過場、風格。表格是 video.json **改完之後**的內容，「改前 → 改後」欄寫原句。

## 主張表（152 條）

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後／備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | RAG 是什麼？有引用，為什麼還是答錯｜AI 名詞十分鐘 | youtube.title | docs/videos/ai-terms/README.md §標題；brief.md §素材 | — | CONFIRMED | 格式「<名詞>是什麼？<反常識的一句>｜AI 名詞十分鐘」 |
| 2 | 回答附了引用，為什麼還是答錯？這集用十分鐘講清楚 RAG（檢索增強生成）的三個步驟，以及每一步怎麼讓它拿著證據答錯。 | youtube.description[0] | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | 三個步驟 |
| 3 | 給用過會附出處的 AI 問答、公司知識庫或文件助理，想知道該不該相信那個引用的人看。 | youtube.description[1] | — | — | OUT OF SCOPE | 受眾 |
| 4 | ・RAG 是先找、再答：答案是從找到的段落組出來的，找到的段落對不對，是另一回事。 | youtube.description[3] | https://docs.langchain.com/oss/python/deepagents/retrieval；https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 5 | ・自己跑一次關鍵字比對的檢索：六段虛構的課程規章，問退費，排第一的是今年一月就失效的舊版規則，材料費例外排最後。 | youtube.description[4] | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q1: P4 5.11 第一、P2 0.47 最後；P4 失效 2026-01-01 |
| 6 | ・拿著證據答錯的三種方式：資料沒更新、文件沒找齊、解讀過頭。 | youtube.description[5] | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 文章 description 的三種 |
| 7 | ・答錯時先分找錯還是讀錯：把正確條文直接交給模型再問一次；驗收清單五項。 | youtube.description[6] | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；brief.md | 200 | CHANGED | 「驗收清單五題」→「驗收清單五項」 |
| 8 | ・RAG 跟直接搜尋、微調差在哪；資料只有一頁時，直接放進上下文可能就夠。 | youtube.description[7] | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 9 | 示範用的六段虛構規章（教學設定，不是任何真實機構的規定）： | youtube.description[9] | demo-log.md §輸入 | — | CHANGED | 新增：六段全文（cta 的連帶） |
| 10 | 1. 一般退費規則，2026 年版，現行有效。開課前七天以上取消，退還課程費全額；開課前七天內取消，退還課程費八成；開課後不退費。 | youtube.description[10] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 11 | 2. 材料費例外。材料費於報名截止日後採購，採購後恕不退還，無論課程費是否退費。 | youtube.description[11] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 12 | 3. 課程分類。週末陶藝班與平日書法班屬手作課程，適用一般退費規則與材料費例外。 | youtube.description[12] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 13 | 4. 一般退費規則，2025 年版，已於 2026 年 1 月 1 日失效。開課前取消一律退還課程費全額，材料費另計。 | youtube.description[13] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 14 | 5. 報名方式。請以線上表單報名，報名截止日為開課前十天，名額有限，額滿為止。 | youtube.description[14] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 15 | 6. 停辦公告。2025 年秋季週末陶藝班因場地整修停辦，已繳費用依 2025 年版規則辦理。 | youtube.description[15] | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 逐字對 DOCS |
| 16 | 三題的排名（關鍵字比對，BM25 分數，2026-09-30 自行執行）： | youtube.description[16] | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CHANGED | 新增：三題完整排名（cta 的連帶） |
| 17 | ・「我報了週末陶藝班，開課前取消可以全額退費嗎？」：第 4 段 5.11、第 3 段 4.84、第 1 段 4.70、第 6 段 4.16、第 5 段 1.53、第 2 段 0.47 | youtube.description[17] | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 順序與分數逐項對 ranked（0 分三段合寫） |
| 18 | ・「報名之後不去了，錢拿得回來嗎？」：第 5 段 1.81、第 1 段 1.32、第 2 段 1.11，第 3、4、6 段 0 | youtube.description[18] | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 順序與分數逐項對 ranked（0 分三段合寫） |
| 19 | ・「去年停辦的週末陶藝班，退費怎麼算？」：第 6 段 6.38、第 3 段 4.84、第 1 段 0.56、第 2 段 0.47、第 4 段 0.42、第 5 段 0 | youtube.description[19] | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 順序與分數逐項對 ranked（0 分三段合寫） |
| 20 | 示範是自行執行的計算，不是任何產品介面的錄影；生成那一步的回覆是示意。 | youtube.description[21] | demo-log.md | — | CONFIRMED | — |
| 21 | AI 名詞總索引：https://mokaair.com/zh-TW/life/ai-terms-index?utm_source=youtube&utm_medium=video&utm_campaign=ai-term-retrieval-augmented-generation | youtube.description[22] | https://mokaair.com/zh-TW/life/ai-terms-index | 200 | CONFIRMED | utm_campaign = 影片代號 |
| 22 | RAG, 檢索增強生成, Retrieval-Augmented Generation, AI 引用, 知識庫問答, 向量搜尋, AI 名詞, AI 名詞十分鐘, Mokaair | youtube.tags | docs/videos/ai-terms/terms.json（aliases: RAG、檢索增強生成） | — | CONFIRMED | 「向量搜尋」不是 aliases，影片只說檢索器不一定是向量資料庫；只報告 |
| 23 | {"headline": "RAG", "tag": "AI 名詞十分鐘", "sub": "有引用，還是錯", "shot": "s-stamp"} | thumbnail.data | brief.md §素材；docs/videos/ai-terms/terms.json short=RAG | — | CONFIRMED | — |
| 24 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（arXiv 2005.11401，2020） ｜ https://arxiv.org/abs/2005.11401 ｜ checked_on 2026-09-30 | sources[0] | https://arxiv.org/abs/2005.11401 | 200 | CONFIRMED | Submitted 22 May 2020，NeurIPS 2020 |
| 25 | Google Cloud：RAG Engine overview ｜ https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview ｜ checked_on 2026-09-30 | sources[1] | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | 頁尾 Last updated 2026-09-28 UTC；舊網址 cloud.google.com/vertex-ai/… 302→ 這頁 |
| 26 | LangChain：Retrieval ｜ https://docs.langchain.com/oss/python/deepagents/retrieval ｜ checked_on 2026-09-30 | sources[2] | https://docs.langchain.com/oss/python/deepagents/retrieval | 200 | CONFIRMED | — |
| 27 | {"tag": "AI 名詞十分鐘", "title": "RAG 是什麼？", "subtitle": "有引用，為什麼還是答錯"} | hook.data (title) | brief.md | — | CONFIRMED | — |
| 28 | 它回答的時候附了條文，還標了出處。 | hook/rg293 | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | OUT OF SCOPE | 故事鉤子：「它回答」指的是 chat 卡的示意回覆，s-counter 才揭露是示意；只報告 |
| 29 | 可是那條規則，今年一月就失效了。 | s-stamp/rg26m | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P4「已於 2026 年 1 月 1 日失效」，今天 2026-09-30 → 今年一月；2027 起失真 |
| 30 | 十分鐘，看懂 RAG 的三步，還有它怎麼拿著證據答錯。 | s-stones/rgl64 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 三步是文章「建索引、檢索、生成」的框架 |
| 31 | {"title": "先問它一題", "messages": [{"side": "right", "name": "你", "text": "我報了週末陶藝班，開課前取消可以全額退費嗎？"}, {"side": "left", "name": "示意回覆", "text": "可以，開課前取消一律退還課程費全額。依據：一般退費規則 2025 年版"}]} | ask-refund.data (chat) | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 右邊逐字 = Q1；左邊名稱「示意回覆」，內容抄 P4 前半 |
| 32 | 先問它一題：我報了週末陶藝班，開課前取消，能全額退費嗎？ | ask-refund/rglg2 | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 旁白把「可以全額退費嗎」唸成「能全額退費嗎」，卡片是原句 |
| 33 | 示意的回覆是：可以，一律全額退，依據二〇二五年版規則。 | ask-refund/rgtjf | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 說明是示意 |
| 34 | 聽起來很有道理，連依據都寫給你了。 | s-seal/rg8cz | — | — | OUT OF SCOPE | — |
| 35 | 換作是你，會不會就信了？ | s-seal/rg2ka | — | — | OUT OF SCOPE | — |
| 36 | 這句回覆是我照它找到的第一段寫的示意。 | s-counter/rg7ed | demo-log.md §示意回覆 | — | CONFIRMED | — |
| 37 | 重點在它找到了什麼。 | s-counter/rgcmp | — | — | OUT OF SCOPE | — |
| 38 | 這是我自己跑的：六段虛構的課程規章，用關鍵字比對來檢索。 | s-six-cards/rgb3u | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | method: BM25 over character bigrams（關鍵字比對）；六段 |
| 39 | {"title": "六段虛構的課程規章", "items": ["現行退費規則（2026 年版）", "材料費例外：採購後不退", "課程分類：陶藝班屬手作課", "舊版退費規則（已失效）", "報名方式：截止日與名額", "停辦公告：依 2025 年版辦理"]} | six.data (bullets) | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 六項對 P1–P6 |
| 40 | 第一段，現行的退費規則，今年的版本，開課前七天以上取消全退。 | six/rg2m7 | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P1「開課前七天以上取消，退還課程費全額」；「全退」= 課程費全額 |
| 41 | 第二段，材料費例外：材料採購之後，不管課程費退不退，都不退。 | six/rgos5 | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P2 |
| 42 | 第三段，課程分類：週末陶藝班算手作課，適用前兩段。 | six/rgaf3 | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P3 |
| 43 | 第四段，舊版退費規則：開課前取消課程費一律全退，今年一月已經失效。 | six/rgr09 | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CHANGED | 「開課前取消一律全退」→「開課前取消課程費一律全退」（P4：退還課程費全額，材料費另計） |
| 44 | 第五段，報名方式：網路表單報名，截止日是開課前十天。 | six/rgfqu | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P5「線上表單」旁白唸「網路表單」（撰稿者避 lint 書面語） |
| 45 | 第六段，停辦公告：去年秋季的陶藝班停辦，退費照舊版規則。 | six/rgo6s | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P6 2025 年秋季 → 去年；依 2025 年版 = 舊版；2027 起失真 |
| 46 | 六段裡排第一的，是已經失效的舊版規則。 | s-queue-old/rgbeg | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q1: P4 5.11 第一 |
| 47 | 現行規則，只排第三。 | s-queue-old/rgzgs | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q1: P1 4.70 第三 |
| 48 | 材料費的例外條款，排在最後一名。 | s-last-card/rgyeb | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q1: P2 0.47 第六 |
| 49 | 只給前幾名，模型根本看不到它。 | s-last-card/rgann | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 只取前 k（k<6）就不含 P2 |
| 50 | 只把第一名交給模型，它很可能拿著那段真實文字答錯。 | s-handoff/rgd4y | brief.md §不做的事；demo-log.md §示意回覆 | — | CHANGED | 「它就拿著那段真實文字，答錯了」→「它很可能拿著那段真實文字答錯」（沒有跑過任何模型，生成只有示意） |
| 51 | 它沒有亂編。 | s-handoff/rgz0e | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | 示意回覆逐字抄 P4 |
| 52 | 你以為，附了出處，就是查證過。 | s-held-up/rgmrv | brief.md | — | OUT OF SCOPE | 你以為（企劃的框架） |
| 53 | 其實 RAG 只保證一件事：答案是從找到的段落組出來的。 | s-assembly/rgftv | brief.md §你以為／其實；https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | — | CONFIRMED | 「只保證」比文章「沒有把生成器變成必然正確的引用機器」強；只報告 |
| 54 | 找到的段落對不對，是另一回事。 | s-twins/rga0h | — | — | OUT OF SCOPE | — |
| 55 | 就像這兩本，長得幾乎一樣。 | s-twins/rgipg | — | — | OUT OF SCOPE | — |
| 56 | {"kicker": "檢索增強生成", "text": "先找、再答", "sub": "找到什麼，就照什麼答"} | define.data (big) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；https://docs.langchain.com/oss/python/deepagents/retrieval | 200 | CONFIRMED | 文章：先從外部資料找出相關內容，再交給模型組織回答；LangChain 2-Step「Retrieval always happens before generation」 |
| 57 | RAG，中文叫檢索增強生成，一句話：先找、再答。 | define/rgad3 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；https://docs.langchain.com/oss/python/deepagents/retrieval | 200 | CONFIRMED | — |
| 58 | 找到什麼，就照什麼答。 | define/rg5l9 | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | retrieved information becomes the context … as a guide for the generative AI model |
| 59 | 所以引用像收據，證明它拿了什麼，不證明拿對了。 | s-receipt/rgm26 | — | — | OUT OF SCOPE | 比喻 |
| 60 | 拿錯了，照樣蓋章。 | s-receipt/rgmi0 | — | — | OUT OF SCOPE | — |
| 61 | 那段話是真的，只是版本錯了。 | s-hourglass/rgyhz | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | — |
| 62 | 那它到底是怎麼找的？ | s-hourglass/rg0na | — | — | OUT OF SCOPE | — |
| 63 | {"title": "RAG 的三個步驟", "subtitle": "建索引、檢索、生成"} | ch-steps.data (chapter) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 64 | 先把它拆成三步，你就知道錯會出在哪一步。 | ch-steps/rgrtb | — | — | OUT OF SCOPE | — |
| 65 | 想像一間圖書館，館員不背書。 | s-drawer/rgnlz | — | — | OUT OF SCOPE | 比喻 |
| 66 | 他先去翻索引卡，再照卡片替你摘要。 | s-drawer/rggcj | — | — | OUT OF SCOPE | — |
| 67 | 索引卡上不只寫書名，還寫在哪一架、哪一版、誰能借。 | s-index-card/rgn2q | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 保留文件識別碼、章節、版本與權限 |
| 68 | 這就是建索引。 | s-index-card/rgavs | — | — | OUT OF SCOPE | — |
| 69 | {"title": "RAG 的三個步驟", "steps": [{"title": "建索引", "detail": "切段，留下文件、章節、版本、權限"}, {"title": "檢索", "detail": "問題變查詢，取回候選段落，必要時重排"}, {"title": "生成", "detail": "模型拿問題加段落，寫出有出處的答案"}]} | steps.data (steps) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）「資料如何走到答案裡」；https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | Google 順序 ingestion → transformation(chunks) → embedding → indexing → retrieval → generation |
| 70 | 第一步，建索引：文件切成段落，記下來自哪份文件、哪個版本、誰能看。 | steps/rgyee | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 71 | 第二步，檢索：問題變成查詢，取回幾段候選，必要時重新排序。 | steps/rgfnp | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 取回候選段落，必要時重新排序 |
| 72 | 第三步，生成：模型拿著問題加段落，寫出答案，還要標出處。 | steps/rgaxx | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 圖解 alt「有條件與出處的答案」 |
| 73 | 問題進來，先過抽屜，再到寫答案的桌子。 | s-belt/rg3i4 | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | — |
| 74 | 分工一直是這樣。 | s-belt/rgiyl | — | — | OUT OF SCOPE | — |
| 75 | {"svg": "apps/web/public/guides/ai-term-retrieval-augmented-generation/diagram-1.svg", "caption": "問題送入檢索器，索引給出段落，模型寫出有出處的答案"} | diagram.data (diagram) | apps/web/public/guides/ai-term-retrieval-augmented-generation/diagram-1.svg | — | CONFIRMED | SVG 存在，文字：讀者問題→檢索器→文件索引（版本與權限）→生成回答（條件與出處） |
| 76 | 圖解上就是這條線：問題進檢索器，索引給段落，模型寫答案。 | diagram/rgjto | apps/web/public/guides/ai-term-retrieval-augmented-generation/diagram-1.svg | — | CONFIRMED | — |
| 77 | 引用最好指到那一段，只給文件首頁，讀者還是得自己翻。 | s-page-link/rgpmk | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 78 | {"title": "建索引時別漏掉的", "items": ["條文連同適用課程、生效日期一起存", "別把條件切斷：截止條件要跟著走", "舊版要退出排名，不是只加新版"]} | index-care.data (bullets) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 79 | 建索引的時候，退費條文要連同適用課程和生效日期一起存。 | index-care/rg9my | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 80 | 只存一句可以退費，丟了下一段的截止條件，找到了也會答錯。 | index-care/rg4f0 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 文章「可能錯答」，旁白「也會答錯」 |
| 81 | 版本更新，要讓舊段落退出，不能只是把新版丟進去一起排名。 | index-care/rgdgg | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 82 | 檢索器不一定是向量資料庫，全文索引、結構化查詢也能做。 | s-not-only-vector/rgc6q | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 83 | 二〇二〇年提出這個詞的論文，把兩種記憶接在一起。 | s-two-boxes/rgpzq | https://arxiv.org/abs/2005.11401 | 200 | CONFIRMED | combine pre-trained parametric and non-parametric memory；We introduce RAG models；2020 |
| 84 | 一種鎖在模型參數裡，一種放在外面的索引裡，可以隨時換。 | s-keyhole/rg05s | https://arxiv.org/abs/2005.11401；https://arxiv.org/html/2005.11401 | 200 | CONFIRMED | parametric = seq2seq；non-parametric = dense vector index；全文 §Index hot-swapping「knowledge can be easily updated at test time」 |
| 85 | 今天的用法更廣：先檢索，把段落放進提示詞，一起交給模型。 | s-envelope/rg7le | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；https://docs.langchain.com/oss/python/deepagents/retrieval；https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview | 200 | CONFIRMED | — |
| 86 | 所以名字一樣，還是要問：資料從哪裡來，檢索器會不會變。 | s-same-name/rgio4 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 87 | 三步都對，答案才對。 | s-three-doors/rg9er | — | — | OUT OF SCOPE | — |
| 88 | 那哪一步，會讓它拿著證據答錯？ | s-three-doors/rgnnb | — | — | OUT OF SCOPE | — |
| 89 | 回到那六段規章，我問了三個問題，每題各排一次名。 | s-lineup/rger0 | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | — |
| 90 | {"title": "關鍵字檢索的排名，BM25 分數", "columns": ["問題", "第一名", "最後一名"], "rows": [["陶藝班開課前取消，能全額退？", "**舊版規則（已失效）** 5.11", "材料費例外 0.47"], ["報名後不去了，錢拿得回來？", "報名方式 1.81", "課程分類等三段 0"], ["去年停辦的陶藝班，退費怎麼算？", "停辦公告 6.38", "報名方式 0"]], "highlight": 0} | rankings.data (table) | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | 三列的第一名、最後一名、分數、highlight 0 全對；第二題最後三段同分 0（JSON 排序 P6、P4、P3）；三個問題是縮寫，原句在說明欄 |
| 91 | 第一題，排第一的是舊版規則，最後一名是材料費例外。 | rankings/rg2pd | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | — |
| 92 | 第二題換個問法，沒有退費兩個字，第一名變成報名方式。 | rankings/rgcls | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q2 原句沒有「退費」；P5 1.81 第一 |
| 93 | 第三題問去年停辦的班，第一名是停辦公告，找對了，但還沒答完。 | rankings/rgx7i | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | P6 6.38 第一；P6 指回 2025 年版 |
| 94 | 第一種答錯，資料沒更新：新舊規章一起競爭排名，這次舊版贏了。 | s-scale/rgfxi | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同）；https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | — | CONFIRMED | — |
| 95 | 第二種，文件沒找齊：材料費例外排最後，根本沒進上下文。 | s-pushed-back/rg2v7 | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | — |
| 96 | 第三種，解讀過頭：條文寫材料費另計，模型把它接成全額退。 | s-bridge/rgicb | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）「模型還可能引用真實文字，卻接出原文不支持的結論」；SCRATCH/demo/demo_rag.py（DOCS 原文） P4「材料費另計」 | — | CONFIRMED | 失敗類型的說明，不是示範結果；只報告 |
| 97 | 三種情況，它手上都是真的條文，答案都錯。 | s-three-stamps/rg4wt | — | — | OUT OF SCOPE | — |
| 98 | 這就是拿著證據答錯。 | s-three-stamps/rgcbe | — | — | OUT OF SCOPE | — |
| 99 | 第二題的教訓不一樣：問法一換，關鍵字比對就找錯了段落。 | s-rephrase/rg4et | SCRATCH/demo/demo-rag.json（查核重跑 demo_rag.py，docs 與 results 相同） | — | CONFIRMED | Q2 第一名 P5 報名方式 |
| 100 | 這就是為什麼會有語意搜尋和嵌入向量，那是另一集的事。 | s-keys/rguie | docs/videos/ai-terms/terms.json | — | CONFIRMED | embedding 第 1 層 #8 backlog、semantic-search 第 2 層 backlog，都還沒發布 |
| 101 | 第三題找對了停辦公告，公告卻說，依二〇二五年版規則辦理。 | s-notice-thread/rge28 | SCRATCH/demo/demo_rag.py（DOCS 原文） | — | CONFIRMED | P6「已繳費用依 2025 年版規則辦理」 |
| 102 | 系統得再回去找一次舊版，才答得了這個歷史個案。 | s-second-trip/rgxci | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 文章「變體」段 |
| 103 | 找對一段，不夠。 | s-second-trip/rgvwf | — | — | OUT OF SCOPE | — |
| 104 | 不能拿最新文件回答所有年份，也不能因為文句像就忽略時點。 | s-all-years/rg4e0 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 105 | 所以看引用要看兩件事：找到的是哪一版，條件有沒有整句帶進來。 | s-two-things/rgb5a | — | — | OUT OF SCOPE | 編輯歸納 |
| 106 | {"kicker": "完整示範", "title": "六段規章與三題排名", "sub": "全文在說明欄"} | cta.data (cta) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；demo-log.md；tools/video/core/metadata.mjs composeDescription | 200 | NOT FOUND → CHANGED | sub「說明欄第一行的文章」→「全文在說明欄」：文章沒有六段全文與排名 |
| 107 | 六段規章的全文和三題的排名，都在說明欄裡。 | cta/rgyya | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json）；demo-log.md；tools/video/core/metadata.mjs composeDescription | 200 | NOT FOUND → CHANGED | 「都在說明欄第一行的文章裡」→「都在說明欄裡」；六段全文與三題完整排名抄進 youtube.description |
| 108 | 所以答錯的時候，怎麼分是找錯，還是讀錯？ | s-fork/rgeff | — | — | OUT OF SCOPE | — |
| 109 | {"title": "答錯了，先分兩種", "left": {"heading": "檢索失誤", "points": ["正確條文沒進上下文", "改提示詞治不了", "修索引、切段、排序、版本"]}, "right": {"heading": "解讀失誤", "points": ["條文就在眼前，還是答錯", "查指令、上下文排列、驗證", "換模型之前先查這三樣"]}, "verdict": "先把正確條文直接交給模型"} | split.data (compare) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | callout「先看原文有沒有被取回」＋示範第二段 |
| 110 | 檢索失誤，是正確條文根本沒進上下文，改提示詞治不了。 | split/rghq0 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 111 | 解讀失誤，是條文就在眼前，它還是答錯，這才查指令和排列。 | split/rgvy3 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 112 | 分法很簡單：把正確的條文直接放到模型面前，再問一次。 | s-hand-clause/rg238 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 113 | 這樣答對了，問題多半出在檢索，去修索引、切段和排序。 | s-empty-drawer/rgf76 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 114 | 還是漏掉材料費，就查指令、上下文的排列和答案驗證。 | s-prompt-tinker/rgbtf | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 115 | 這樣一層一層查，比一直換模型更快找到原因。 | s-swap-models/rg4bo | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 116 | 先查抽屜，再怪桌子。 | s-swap-models/rgh55 | — | — | OUT OF SCOPE | — |
| 117 | 權限也算檢索品質：讀者能看什麼，要在檢索那一步就限制。 | s-locked-door/rgqax | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 118 | {"title": "三個不同的檢查", "items": ["來源可靠嗎：過期、矛盾、本來就錯", "使用者有權看嗎：檢索時就限制", "文字相關嗎：取回的只是內容"]} | checks.data (bullets) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 119 | 第一個檢查，來源可不可靠：文件可能過期、互相矛盾，或本來就錯。 | checks/rgtjm | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 120 | 第二個，使用者有沒有權看：不能先取回內部紀錄，再指望模型不說。 | checks/rg7kv | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 121 | 第三個，文字只是內容：文件裡寫著請忽略規則，也改不了你的任務。 | checks/rg25p | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 122 | 三個檢查，三個窗口，過了一個，不代表另外兩個也過。 | s-three-windows/rguzq | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 123 | {"title": "驗收清單", "items": ["常見題：答案要回到原文", "跨章節：兩段拼起來才答得了", "舊版干擾：新舊同時在索引裡", "資料沒涵蓋：它該說不知道", "缺資料時，坦白停住"]} | checklist.data (bullets) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 四種題型＋缺資料時坦白停住＝五項 |
| 124 | 驗收前準備一組題目，先放常見題，答案要能回到原文。 | checklist/rgm1m | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 125 | 再放跨章節的題，要把兩段拼起來才答得了。 | checklist/rgnyo | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 126 | 放一題舊版干擾，新舊規章同時留在索引裡。 | checklist/rguni | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 127 | 放一題資料沒涵蓋的，看它會不會硬答。 | checklist/rgi5w | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 128 | 缺資料的時候坦白停住，這就是好答案。 | checklist/rgcer | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 129 | 每一題記下取回哪些段落、哪句有依據、文件是哪個版本。 | s-ticked/rgkh2 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 130 | 留著這份紀錄，日後換模型或換索引，才能重做同一組比較。 | s-redo/rg4rn | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 131 | 那 RAG 跟搜尋、微調，到底差在哪？ | s-tools/rg0y7 | — | — | OUT OF SCOPE | — |
| 132 | 直接搜尋，交給你一疊片段，答案要你自己拼。 | s-pile/rg5u2 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 133 | RAG 多做了一步。 | s-pile/rguec | — | — | OUT OF SCOPE | — |
| 134 | {"title": "三個容易搞混的做法", "columns": ["方法", "做什麼", "要留意"], "rows": [["直接搜尋", "交付文件或片段", "讀者自己彙整"], ["**RAG**", "取回依據後生成回答", "檢索與引用仍要驗證"], ["微調", "訓練行為或能力", "不等於即時更新資料"]], "highlight": 1} | methods.data (table) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 文章「概念對照」表 |
| 135 | 搜尋，交出片段，讀者自己彙整。 | methods/rgrcr | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 136 | RAG，取回依據再生成回答，但檢索和引用都還要驗證。 | methods/rgwtb | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 137 | 微調，是訓練模型的行為，不等於即時更新資料。 | methods/rgiz3 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 138 | 微調像教它一種語氣或格式，你昨天改的辦法，它學不到。 | s-tuning/rgmbr | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 139 | 要它穩定守格式、學特殊語氣，微調更貼近，兩者也能併用。 | s-both/rgpjd | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 140 | {"title": "什麼時候值得建 RAG", "items": ["資料一直在更新", "答案要附出處", "一個模型服務好幾套資料", "只有一頁？直接放進上下文"]} | when.data (bullets) | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 141 | 資料一直在更新，模型訓練時不可能讀過你昨天改的辦法。 | when/rgh2g | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | 文章首段 |
| 142 | 答案要附出處，讓讀者追得回原文。 | when/rg8xe | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 143 | 一個模型要服務好幾套資料，也常從它開始。 | when/rgmm4 | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 144 | 資料只有一頁，直接整頁放進上下文，可能就夠了。 | when/rgqla | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 145 | 別為一頁紙蓋倉庫：複雜度要跟資料量、更新頻率和權限一起算。 | s-one-page/rg48c | https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation（apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json） | 200 | CONFIRMED | — |
| 146 | 我的看法是，驗收先看該找到的條文，有沒有進到模型眼前。 | s-two-rulers/rglor | brief.md §站主觀點 | — | CONFIRMED | 意見，標了「我的看法是」；brief 註明提案待站主確認 |
| 147 | 再看答案忠不忠於那段條文，兩件事分開量。 | s-second-ruler/rgw87 | brief.md §站主觀點 | — | CONFIRMED | 意見 |
| 148 | 一把尺量不了兩件事。 | s-second-ruler/rg6kz | — | — | OUT OF SCOPE | — |
| 149 | 我的看法是，它會改變兩個決定：信不信這個答案，給不給它權限。 | s-trust/rgof0 | brief.md §站主觀點 | — | CONFIRMED | 意見，標了「我的看法是」 |
| 150 | 下一個名詞是上下文視窗：找到的段落，還要放得進模型的桌面。 | s-window/rgyi2 | docs/videos/ai-terms/terms.json | — | CONFIRMED | context-window 第 1 層 #2，status planned（同批試片，還沒發布） |
| 151 | {"title": "有引用，不等於對", "cta": "先看它找到了什麼", "lines": ["完整文章在說明欄第一行", "下一個名詞：上下文視窗", "鄰近名詞：文件分塊、重新排序、微調"]} | wrap.data (outro) | tools/video/core/metadata.mjs composeDescription；docs/videos/ai-terms/terms.json | — | CONFIRMED | 組合後第一行是「🔗 文章：…」；文件分塊、重新排序、微調都在 related |
| 152 | 回到開場那一題：有引用，不等於對，先看它找到了什麼。 | wrap/rg3ma | — | — | OUT OF SCOPE | — |

## 摘要

- 查了 152 條：CONFIRMED 117、CHANGED 5（其中說明欄新增的兩個區塊是 cta 的連帶）、NOT FOUND → CHANGED 2、OUT OF SCOPE 28（比喻、過場、受眾、風格）。真正找不到的只有一件事：cta 說六段規章全文與三題排名「在說明欄第一行的文章裡」，文章沒有。
- 改了 4 個事實（連帶一起算一個）：
  1. `six/rgr09`：「開課前取消一律全退」→「開課前取消課程費一律全退」。P4 原文是「退還課程費全額，材料費另計」，第四章「條文寫材料費另計」靠這條。
  2. `s-handoff/rgd4y`：「它就拿著那段真實文字，答錯了」→「它很可能拿著那段真實文字答錯」。沒有跑過任何模型，生成只有示意；brief §不做的事寫明不宣稱模型會怎麼回答。字數與原句相同（23 個單位），s-handoff 不再超過 8 秒。
  3. `cta` 卡 sub「說明欄第一行的文章」→「全文在說明欄」，`rgyya`「都在說明欄第一行的文章裡」→「都在說明欄裡」；六段全文（逐字自 demo_rag.py）與三題完整排名（逐項對 demo-rag.json）抄進 `youtube.description`，本文最後一行仍是總索引，組合後第一行仍是文章連結（composeDescription）。站主若把示範補進文章（content-pipeline 票），這兩處可以改回「文章」。
  4. `youtube.description`「驗收清單五題」→「驗收清單五項」（卡片五個項目 = 四種題型 + 缺資料時坦白停住；brief 也寫「五項」）。
- 示範數字：table 卡三列的第一名、最後一名、分數、`highlight: 0`，以及 rgbeg／rgzgs／rgyeb／rg2pd／rgcls／rgx7i／rgfxi／rg2v7／rge28 的排名說法，全部對得上重跑後的 demo-rag.json；六段內容對 demo_rag.py 的 DOCS（改了 rgr09 一處）；「2026 年 1 月 1 日失效」→「今年一月」正確。
- 定義：「先找、再答」對文章首段與 LangChain「Retrieval always happens before generation」；「找到什麼，就照什麼答」對 Google「retrieved information becomes the context」；二〇二〇年論文「兩種記憶」對 arXiv 摘要（parametric ＋ non-parametric memory；submitted 22 May 2020）；「可以隨時換」對全文 §Index hot-swapping；來源可追溯對摘要「providing provenance」。沒有推薦任何產品，沒有價格、方案、模型名稱、排行榜；chat 卡左邊名稱「示意回覆」，說明欄也寫「生成那一步的回覆是示意」。
- 會過期的事實：「今年一月就失效」（rg26m、rgr09、說明欄、shorts）與「去年秋季」（rgo6s）、Q3 的「去年」只在 2026 年成立，2027 年要改；Google Cloud 頁面 Last updated 2026-09-28，舊 Vertex 網址今天仍轉址；arXiv v4 2021-04-12。
- 意見：s-two-rulers、s-second-ruler、s-trust 都標了「我的看法是」，內容與 brief §站主觀點一致；但 brief 自己註明「提案，待站主確認」，README 說頻道立場 2026-09-29 仍空白 → 站主確認前不算定案，只報告。
- 聽眾檢查（只報告）：110 句沒有一句超過 40 個單位（lint 也沒警告）；沒有「本影片」「經查證」「根據官方文件」；拉丁字母只有 RAG（lexicon 有）；沒有括號、網址；reveal 都在介紹該項目的那一句。hook 的「它回答的時候附了條文」在 s-counter 揭露示意前約 40 秒，屬企劃的開場寫法。
- lint：`node tools/video/cli.mjs lint --slug ai-term-retrieval-augmented-generation` → 0 錯誤、1 個原有警告（平均 6.5 秒換畫面，撰稿者已說明不再拆）。輸出：

```
ai-term-retrieval-augmented-generation: 0 errors, 1 warnings
WARN  scenes: a new picture every 6.5 s on average; aim for 6 s or less (estimated; the final gate measures the synthesized timeline)

Estimate: 9.9 min, 110 lines, 2107 spoken units
Azure billable characters (estimate): 7830, 1.6% of the free tier's 500,000 a month
Chapters (estimated times):
  00:00 有引用，還是錯
  00:15 先跑一次：問退費，它引了舊版
  02:31 RAG 的三個步驟：建索引、檢索、生成
  04:31 拿著證據答錯的三種方式
  06:19 先看原文有沒有被取回
  08:14 RAG 跟搜尋、微調差在哪
```

- 懷疑但沒動：
  - `rgftv`「RAG 只保證一件事：答案是從找到的段落組出來的」比文章「沒有把生成器變成必然正確的引用機器」強，也和第五章「條文就在眼前還是答錯」有點緊張；是 brief 的「其實」句，留給站主。
  - `rgicb`「條文寫材料費另計，模型把它接成全額退」是失敗類型的說明，不是示範結果；若要完全不替模型代言，可加「可能」。
  - `rg2m7` 把 P1「退還課程費全額」說成「全退」（P1 沒提材料費，第二段緊接著講）；沒改。
  - `rankings` 卡三個問題是縮寫（「陶藝班開課前取消，能全額退？」），分數是用原句算的，原句現在在說明欄；沒動版面。
  - `youtube.tags`「向量搜尋」不是 terms.json 的 alias，影片只有一句「檢索器不一定是向量資料庫」。
  - `s-keys`「那是另一集的事」與片尾「下一個名詞：上下文視窗」指的集都還沒發布（terms.json planned／backlog）；README 說沒發布就指文章，由 package 決定。
  - shorts.json 第二支 s-handoff 一幕仍是「只把第一名交給模型，它就拿著真實的文字答錯了」，與長片改後不一致；查核不改 shorts.json，請撰稿者同步。
  - 文章示範段的問句是「開課前取消可以全額退嗎」，demo 的 Q1 是「可以全額退費嗎」（多「費」字），BM25 用的是後者；卡片與說明欄都是後者，沒問題，只是文章與影片不完全同句。
- 第二輪：**要**。這一輪改了 4 個事實（超過 3 個）；第二輪請重查 rgr09、rgd4y、cta／rgyya、說明欄（五項＋新增的六段與排名），再隨機抽三分之一已確認的條目。
