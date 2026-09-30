# 查核第二輪：RAG 是什麼？有引用，為什麼還是答錯（2026-09-30）

第二輪獨立查核者，沒寫過這份稿子，也不是第一輪的查核者。範圍：第一輪標 CHANGED 的每一條、加長輪（2026-09-30，+26 句、+19 個 shot、+1 張 `recap` 卡）新增的每一句、第一輪 CONFIRMED 的隨機三分之一（seed 20260930，117 條抽 39 條）、聽眾審稿改過的 10 句與 shorts 第二支。

每一條都自己開：`demo_rag.py` 在 `SCRATCH/ai-term-retrieval-augmented-generation/verify2/` 重跑一次（Python 3.11.15，`docs` 與 `results` 和 `SCRATCH/demo/demo-rag.json` 完全相同）；六段規章逐字對 `demo_rag.py` 的 `DOCS`；文章對 `apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json`（和 `SCRATCH/article-ai-term-retrieval-augmented-generation.md`、正式站頁面一致）；今天重抓 arXiv abs（200，Submitted 22 May 2020，v4 2021-04-12，NeurIPS 2020）、arXiv html 全文（200，§Index hot-swapping）、Google Cloud RAG Engine overview（200，Last updated 2026-09-28 UTC）、LangChain Retrieval（200）、正式站文章（200）與總索引（200，有連到這篇）。輔助腳本：`extract_claims.py`（179 條主張清單 `claims-list.md`、聽眾檢查、claims.md 與 video.json 交叉比對）、`check_description.py`（說明欄六段與三題排名對 demo）、`sample_confirmed.py`（抽樣）。

縮寫：ART = 文章（正式站 https://mokaair.com/zh-TW/life/ai-term-retrieval-augmented-generation ＋ 內容包 JSON）；DEMO = `SCRATCH/demo/demo-rag.json`（第二輪重跑相同）；DOCS = `SCRATCH/demo/demo_rag.py` 的六段原文；LOG = `demo-log.md`；BRIEF = `brief.md` §站主觀點；GOOGLE = https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview ；LANGCHAIN = https://docs.langchain.com/oss/python/deepagents/retrieval ；ARXIV = https://arxiv.org/abs/2005.11401 。

判定：CONFIRMED 確認 ／ CHANGED 改了 ／ NOT FOUND 找不到 ／ OUT OF SCOPE 情境句、比喻、風格。表格是 video.json 目前的內容；這一輪沒有改任何一句，所以「改前 → 改後」欄只有備註。

## 主張表（93 條）

### 一、第一輪改過的（16 條）

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後／備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 第四段，舊版退費規則：開課前取消課程費一律全退，今年一月已經失效。 | six/rgr09 | DOCS P4 | — | CONFIRMED | P4「開課前取消一律退還課程費全額，材料費另計」「已於 2026 年 1 月 1 日失效」；今天 2026-09-30 → 今年一月 |
| 2 | 只把第一名交給模型，它很可能拿著那段真實文字答錯。 | s-handoff/rgd4y | brief.md §不做的事；LOG §示意回覆 | — | CONFIRMED | 沒跑過任何模型，「很可能」留著；shorts.json 第二支已同步（#93） |
| 3 | {"kicker": "完整示範", "title": "六段規章與三題排名", "sub": "全文在說明欄"} | cta.data (cta) | youtube.description；tools/video/core/metadata.mjs composeDescription | — | CONFIRMED | 六段全文與三題排名都在說明欄本文（#7–#16）；組合後第一行是文章連結、本文接在後面 |
| 4 | 六段規章的全文和三題的排名，都在說明欄裡。 | cta/rgyya | 同上 | — | CONFIRMED | — |
| 5 | ・答錯時先分找錯還是讀錯：把正確條文直接交給模型再問一次；驗收清單五項。 | youtube.description[6] | ART 示範節第二段；checklist.data | 200 | CONFIRMED | checklist 卡 5 項（四種題型＋缺資料時坦白停住） |
| 6 | 示範用的六段虛構規章（教學設定，不是任何真實機構的規定）： | youtube.description[9] | LOG §輸入 | — | CONFIRMED | — |
| 7 | 1. 一般退費規則，2026 年版，現行有效。開課前七天以上取消，退還課程費全額；開課前七天內取消，退還課程費八成；開課後不退費。 | youtube.description[10] | DOCS P1 | — | CONFIRMED | 整行逐字相等 |
| 8 | 2. 材料費例外。材料費於報名截止日後採購，採購後恕不退還，無論課程費是否退費。 | youtube.description[11] | DOCS P2 | — | CONFIRMED | 整行逐字相等 |
| 9 | 3. 課程分類。週末陶藝班與平日書法班屬手作課程，適用一般退費規則與材料費例外。 | youtube.description[12] | DOCS P3 | — | CONFIRMED | 整行逐字相等 |
| 10 | 4. 一般退費規則，2025 年版，已於 2026 年 1 月 1 日失效。開課前取消一律退還課程費全額，材料費另計。 | youtube.description[13] | DOCS P4 | — | CONFIRMED | 整行逐字相等 |
| 11 | 5. 報名方式。請以線上表單報名，報名截止日為開課前十天，名額有限，額滿為止。 | youtube.description[14] | DOCS P5 | — | CONFIRMED | 整行逐字相等 |
| 12 | 6. 停辦公告。2025 年秋季週末陶藝班因場地整修停辦，已繳費用依 2025 年版規則辦理。 | youtube.description[15] | DOCS P6 | — | CONFIRMED | 整行逐字相等 |
| 13 | 三題的排名（關鍵字比對，BM25 分數，2026-09-30 自行執行）： | youtube.description[16] | DEMO（method、date） | — | CONFIRMED | method "BM25 over character bigrams, pure Python"，date 2026-09-30 |
| 14 | ・「我報了週末陶藝班，開課前取消可以全額退費嗎？」：第 4 段 5.11、第 3 段 4.84、第 1 段 4.70、第 6 段 4.16、第 5 段 1.53、第 2 段 0.47 | youtube.description[17] | DEMO Q1 | — | CONFIRMED | 問句逐字＝Q1；六項順序與分數逐項相等（JSON 的 4.7 寫成 4.70） |
| 15 | ・「報名之後不去了，錢拿得回來嗎？」：第 5 段 1.81、第 1 段 1.32、第 2 段 1.11，第 3、4、6 段 0 | youtube.description[18] | DEMO Q2 | — | CONFIRMED | 問句逐字＝Q2；前三項相等；0 分三段在 JSON 排 P6、P4、P3（同分，順序無意義），說明欄合寫 |
| 16 | ・「去年停辦的週末陶藝班，退費怎麼算？」：第 6 段 6.38、第 3 段 4.84、第 1 段 0.56、第 2 段 0.47、第 4 段 0.42、第 5 段 0 | youtube.description[19] | DEMO Q3 | — | CONFIRMED | 問句逐字＝Q3；六項順序與分數逐項相等 |

### 二、加長輪新增的句子與卡片（27 條）

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後／備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 17 | 如果你是管公司知識庫的人，同事拿到這句，還會再翻規章嗎？ | s-colleague/0w7b7o | brief.md §觀眾 | — | OUT OF SCOPE | 情境句，沒有事實主張 |
| 18 | 第二名是課程分類：陶藝班算手作課，適用哪幾條，沒說退多少。 | s-second-card/0zvk9v7b | DEMO Q1；DOCS P3 | — | CONFIRMED | Q1 第二名 P3 4.84；P3「屬手作課程，適用一般退費規則與材料費例外」，沒有金額 |
| 19 | 照現行規則和例外，該答的是課程費看天數，材料費採購後不退。 | s-right-answer/1d99 | DOCS P1、P2；LOG §示意回覆 | — | CONFIRMED | P1 七天以上全額／七天內八成／開課後不退；P2「採購後恕不退還」 |
| 20 | 它不是一個裝資料的資料庫，是一種先找再答的組合方式。 | s-not-a-db/39i2gl80 | ART「一種組合方式，不是一個資料庫」 | 200 | CONFIRMED | — |
| 21 | 我的看法是，引用只是可以點開核對的線索，不是正確的保證。 | s-clue-tag/6m5s | BRIEF | — | CONFIRMED | 意見，標了「我的看法是」；brief 原句逐字 |
| 22 | 如果你在公司裡管文件，第一步就是你的事：哪一版、誰能看，先標好。 | s-tab-folders/71j7e1w | ART「保留文件識別碼、章節、版本與權限」 | 200 | CONFIRMED | 前半情境句；後半（版本、權限在建索引那一步）對文章 |
| 23 | 三步是不是同一個服務做的，不影響分工，拆開看才知道修哪裡。 | s-three-desks/80yflb | ART「這些步驟是否由同一服務執行，不影響概念上的分工」「分層檢查比一再更換模型更容易找出原因」 | 200 | CONFIRMED | — |
| 24 | 外面那份資料只在作答當下用。 | s-calendar-swap/88iewhp | ART 首段「外部資料在這裡是當次作答依據，不必先變成模型參數」 | 200 | CONFIRMED | — |
| 25 | 資料更新和模型訓練，從此分開。 | s-calendar-swap/8nua3lc | ART 首段「這讓資料更新與模型訓練可以分開處理」；https://arxiv.org/html/2005.11401 §Index hot-swapping | 200 | CONFIRMED | — |
| 26 | 第一題裡，停辦公告排第四，報名方式第五，都在例外條款前面。 | s-ladder/ceyi | DEMO Q1 | — | CONFIRMED | P6 4.16 第四、P5 1.53 第五、P2 0.47 第六 |
| 27 | 前兩種，模型還沒出場就錯了；第三種，才是模型讀錯。 | s-curtain/dteh | ART callout「把檢索失誤與解讀失誤分開」；DEMO Q1 | 200 | CONFIRMED | 前兩種是排名與取回的事（示範裡實際發生）；第三種對文章「引用真實文字，卻接出原文不支持的結論」 |
| 28 | 反過來，題目裡有精確的課程代碼時，只靠語意相近也未必好。 | s-pegboard/dxot71s | ART「有精確課程代碼的題目，未必適合只靠語意相近」 | 200 | CONFIRMED | — |
| 29 | 可是在這一題，舊版規則只排第五，靠關鍵字，它不會自己浮上來。 | s-net/e5pqgb80 | DEMO Q3 | — | CONFIRMED | P4 0.42 第五（六段裡倒數第二）；「不會自己浮上來」的前提和 rgann 一樣：只取前幾名 |
| 30 | 如果你是拿到答案的人，別急著看結論，先點開它引的那一段。 | s-lift-sheet/ej39 | brief.md §觀眾看完能做到的事 1 | — | OUT OF SCOPE | 情境句與做法，沒有事實主張 |
| 31 | 答對的樣子是：課程費可能退，材料費要看採購狀態，各引各的條文。 | s-two-tags/hvn67 | ART 示範節「說明可能退回課程費，但材料費仍需查採購狀態，並引用相應條文」 | 200 | CONFIRMED | — |
| 32 | 沒搜到例外，不等於沒有例外。 | s-empty-hole/io8t | ART「不是把沒有搜到例外當成不存在例外」 | 200 | CONFIRMED | — |
| 33 | 只有一般規則時，它該說資料不足。 | s-empty-hole/k6is | ART「若索引只包含一般規則，系統應表達資料不足」 | 200 | CONFIRMED | — |
| 34 | 再記兩個時間：等多久，更新後多久查得到。 | s-stopwatch/m9ylx | ART「再記錄等待時間與文件更新後何時可查到」 | 200 | CONFIRMED | — |
| 35 | 更新了卻查不到，也要記。 | s-stopwatch/pzptxzd2 | ART 同上 | 200 | CONFIRMED | 前一句的引申（查不到＝「何時可查到」沒有答案），不是新事實 |
| 36 | 用了向量資料庫就是 RAG？沒有生成那一步，它還是搜尋。 | s-idle-desk/qleo65 | ART「沒有生成答案的向量搜尋仍是搜尋，不能單憑用了向量便稱為完整 RAG」 | 200 | CONFIRMED | — |
| 37 | 如果你只是要問自己的筆記，先把幾頁整個貼進去，再談建不建索引。 | s-notebook-paste/rwu5ee | ART「若資料只有短短一頁，直接提供整頁上下文可能足夠，未必需要完整索引服務」「個人筆記問答」 | 200 | CONFIRMED | 情境句；文章的門檻是「短短一頁」，旁白放寬成「幾頁」，同集 rgqla 與 when 卡都說「一頁」——不是數字或名稱，只報告 |
| 38 | 權限那一件，不能靠提示詞裡的不要透露，要在檢索那一步就擋住。 | s-crossed-bubble/sohx | BRIEF；ART「在查詢時依讀者身分限制範圍」「再期待模型自行不透露」 | 200 | CONFIRMED | 緊接 rgof0 的「我的看法是」；文章也這樣寫 |
| 39 | 第一，RAG 是先找、再答，引用只證明它拿了什麼。 | recap/sse0 | ART 首段；LANGCHAIN「Retrieval always happens before generation」 | 200 | CONFIRMED | — |
| 40 | 第二，建索引、檢索、生成，三步各有各的錯法：資料沒更新、文件沒找齊、解讀過頭。 | recap/ttzt | ART「資料如何走到答案裡」；ART description 的三種 | 200 | CONFIRMED | 31 單位，全片最長，≤ 40 |
| 41 | 第三，答錯先分找錯還是讀錯：把正確條文直接交給模型，再問一次。 | recap/u7oe | ART 示範節第二段 | 200 | CONFIRMED | — |
| 42 | 就查指令、上下文的排列和答案驗證。 | s-prompt-tinker/uzkq0xi | ART「則檢查指令、上下文排列或答案驗證」 | 200 | CONFIRMED | rgbtf 拆出的後半句 |
| 43 | {"title": "這集的三個要點", "items": ["先找、再答：引用只證明拿了什麼", "三步各有各的錯法", "答錯先分找錯還是讀錯"]} | recap.data (bullets) | ART；brief §你以為／其實 | 200 | CONFIRMED | 三項對 #39–#41 |

### 三、第一輪 CONFIRMED 的隨機三分之一（39 條，seed 20260930）

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後／備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 44 | RAG 是什麼？有引用，為什麼還是答錯｜AI 名詞十分鐘 | youtube.title | docs/videos/ai-terms/README.md §標題；brief.md §素材 | — | CONFIRMED | 縮寫通行的名詞直接用縮寫 |
| 45 | ・RAG 是先找、再答：答案是從找到的段落組出來的，找到的段落對不對，是另一回事。 | youtube.description[3] | LANGCHAIN；ART | 200 | CONFIRMED | 2-Step RAG「Retrieval always happens before generation」 |
| 46 | ・自己跑一次關鍵字比對的檢索：六段虛構的課程規章，問退費，排第一的是今年一月就失效的舊版規則，材料費例外排最後。 | youtube.description[4] | DEMO Q1；DOCS P4 | — | CONFIRMED | P4 5.11 第一、P2 0.47 最後；2026-01-01 → 今年一月 |
| 47 | ・RAG 跟直接搜尋、微調差在哪；資料只有一頁時，直接放進上下文可能就夠。 | youtube.description[7] | ART 表「概念對照」、「短短一頁」 | 200 | CONFIRMED | — |
| 48 | 1. 一般退費規則，2026 年版，…開課後不退費。 | youtube.description[10] | DOCS P1 | — | CONFIRMED | 同 #7 |
| 49 | 3. 課程分類。週末陶藝班與平日書法班屬手作課程，適用一般退費規則與材料費例外。 | youtube.description[12] | DOCS P3 | — | CONFIRMED | 同 #9 |
| 50 | 4. 一般退費規則，2025 年版，已於 2026 年 1 月 1 日失效。… | youtube.description[13] | DOCS P4 | — | CONFIRMED | 同 #10 |
| 51 | 5. 報名方式。請以線上表單報名，報名截止日為開課前十天，名額有限，額滿為止。 | youtube.description[14] | DOCS P5 | — | CONFIRMED | 同 #11 |
| 52 | {"tag": "AI 名詞十分鐘", "title": "RAG 是什麼？", "subtitle": "有引用，為什麼還是答錯"} | hook.data (title) | brief.md §素材 | — | CONFIRMED | 與 youtube.title 一致 |
| 53 | 這句回覆是我照它找到的第一段寫的示意。 | s-counter/rg7ed | LOG §示意回覆；DEMO Q1 top1 = P4 | — | CONFIRMED | chat 卡左邊逐字取自 P4 第二句，名稱「示意回覆」 |
| 54 | 第一段，現行的退費規則，今年的版本，開課前七天以上取消，退課程費全額。 | six/rg2m7 | DOCS P1 | — | CONFIRMED | 聽眾審稿後的新句；P1「2026 年版」「開課前七天以上取消，退還課程費全額」 |
| 55 | 第六段，停辦公告：去年秋季的陶藝班停辦，退費照舊版規則。 | six/rgo6s | DOCS P6 | — | CONFIRMED | 2025 年秋季 → 去年；依 2025 年版＝舊版（P4）；2027 起失真 |
| 56 | 只給前幾名，模型根本看不到它。 | s-last-card/rgann | DEMO Q1 | — | CONFIRMED | P2 第六，只取前 k（k<6）就不含 |
| 57 | 其實 RAG 只保證一件事：答案是從找到的段落組出來的。 | s-assembly/rgftv | brief.md §你以為／其實；ART「沒有把生成器變成必然正確的引用機器」 | 200 | CONFIRMED | 「只保證」是 brief 的「其實」句，比文章強；只報告（同第一輪） |
| 58 | 找到什麼，就照什麼答。 | define/rg5l9 | GOOGLE | 200 | CONFIRMED | "The retrieved information becomes the context added to the original user query as a guide for the generative AI model" |
| 59 | {"title": "RAG 的三個步驟", "steps": [建索引：切段，留下文件、章節、版本、權限 / 檢索：問題變查詢，取回候選段落，必要時重排 / 生成：模型拿問題加段落，寫出有出處的答案]} | steps.data (steps) | ART「資料如何走到答案裡」；GOOGLE | 200 | CONFIRMED | Google 順序 data ingestion → transformation (chunks) → embedding → indexing → retrieval → generation |
| 60 | 第三步，生成：模型拿著問題加段落，寫出答案，還要標出處。 | steps/rgaxx | ART；圖解 alt「有條件與出處的答案」 | 200 | CONFIRMED | — |
| 61 | {"svg": "apps/web/public/guides/ai-term-retrieval-augmented-generation/diagram-1.svg", "caption": "問題送入檢索器，索引給出段落，模型寫出有出處的答案"} | diagram.data (diagram) | apps/web/public/guides/ai-term-retrieval-augmented-generation/diagram-1.svg | — | CONFIRMED | SVG 存在（2,251 bytes）；文字：讀者問題 → 檢索器 → 文件索引（版本與權限）→ 生成回答（條件與出處） |
| 62 | 引用最好指到那一段，只給文件首頁，讀者還是得自己翻。 | s-page-link/rgpmk | ART「引用連結最好定位到實際段落；只有文件首頁連結，讀者仍得在長篇內容裡找證據」 | 200 | CONFIRMED | — |
| 63 | 版本更新，要讓舊段落退出，不能只是把新版丟進去一起排名。 | index-care/rgdgg | ART「版本更新也要讓舊段落退出適用範圍，不能只是新增新版，讓新舊規章同時競爭搜尋排名」 | 200 | CONFIRMED | — |
| 64 | 今天的用法更廣：先檢索，把段落放進提示詞，一起交給模型。 | s-envelope/rg7le | ART「常指先檢索、再把內容放進提示詞的應用流程」；LANGCHAIN「supply the retrieved content as context to the LLM (2-Step RAG)」；GOOGLE | 200 | CONFIRMED | — |
| 65 | 所以名字一樣，還是要問：資料從哪裡來，檢索器會不會變。 | s-same-name/rgio4 | ART「看到名稱相同，仍需確認資料從哪裡來，以及檢索器是否會隨訓練改變」 | 200 | CONFIRMED | — |
| 66 | 第二題換個問法，沒有退費兩個字，第一名變成報名方式。 | rankings/rgcls | DEMO Q2 | — | CONFIRMED | Q2 原句無「退費」；P5 1.81 第一 |
| 67 | 第三種，解讀過頭：條文寫材料費另計，模型可能把它接成全額退。 | s-bridge/rgicb | DOCS P4「材料費另計」；ART「引用真實文字，卻接出原文不支持的結論」 | 200 | CONFIRMED | 聽眾審稿後加了「可能」；仍是失敗類型的說明，不是示範結果 |
| 68 | 這就是為什麼會有語意搜尋和嵌入向量，那是另一集的事。 | s-keys/rguie | docs/videos/ai-terms/terms.json | — | CONFIRMED | embedding 第 1 層 #8 backlog、semantic-search 第 2 層 backlog，都還沒發布 |
| 69 | {"title": "答錯了，先分兩種", left 檢索失誤：正確條文沒進上下文／改提示詞治不了／修索引、切段、排序、版本；right 解讀失誤：條文就在眼前，還是答錯／查指令、上下文排列、驗證／換模型之前先查這三樣；verdict 先把正確條文直接交給模型} | split.data (compare) | ART callout「先看原文有沒有被取回」＋示範節第二段；brief §能做到的事 2 | 200 | CONFIRMED | — |
| 70 | 解讀失誤，是條文就在眼前，它還是答錯，這才查指令和排列。 | split/rgvy3 | ART | 200 | CONFIRMED | — |
| 71 | 分法很簡單：把正確的條文直接放到模型面前，再問一次。 | s-hand-clause/rg238 | ART「可以先把正確條文直接交給模型」 | 200 | CONFIRMED | — |
| 72 | 這樣答對了，問題多半出在檢索，去修索引、切段和排序。 | s-empty-drawer/rgf76 | ART「若這樣能答對，原本問題多半在檢索」；brief §能做到的事 2 | 200 | CONFIRMED | — |
| 73 | {"title": "三個不同的檢查", "items": ["來源可靠嗎：過期、矛盾、本來就錯", "使用者有權看嗎：檢索時就限制", "文字相關嗎：取回的只是內容"]} | checks.data (bullets) | ART「有來源仍可能答錯」兩段 | 200 | CONFIRMED | — |
| 74 | 三個檢查，三個窗口，過了一個，不代表另外兩個也過。 | s-three-windows/rguzq | ART「來源可靠、使用者有權看，以及文字相關，是不同的檢查」 | 200 | CONFIRMED | — |
| 75 | {"title": "驗收清單", "items": ["常見題：答案要回到原文", "跨章節：兩段拼起來才答得了", "舊版干擾：新舊同時在索引裡", "資料沒涵蓋：它該說不知道", "缺資料時，坦白停住"]} | checklist.data (bullets) | ART「何時值得使用，如何驗收」第二段 | 200 | CONFIRMED | 五項 |
| 76 | 驗收前準備一組題目，先放常見題，答案要能回到原文。 | checklist/rgm1m | ART「常見且可由原文確認的問題」 | 200 | CONFIRMED | — |
| 77 | 再放跨章節的題，要把兩段拼起來才答得了。 | checklist/rgnyo | ART「跨章節」 | 200 | CONFIRMED | 「兩段拼起來」是「跨章節」的白話 |
| 78 | 缺資料的時候坦白停住，這就是好答案。 | checklist/rgcer | ART「缺資料時是否坦白停住」 | 200 | CONFIRMED | — |
| 79 | 直接搜尋，交給你一疊片段，答案要你自己拼。 | s-pile/rg5u2 | ART「搜尋工具通常交付文件清單或片段」、表「讀者自行彙整答案」 | 200 | CONFIRMED | — |
| 80 | {"title": "什麼時候值得建 RAG", "items": ["資料一直在更新", "答案要附出處", "一個模型服務好幾套資料", "只有一頁？直接放進上下文"]} | when.data (bullets) | ART「何時值得使用」第一段 | 200 | CONFIRMED | — |
| 81 | 下一個名詞是上下文視窗：找到的段落，還要放得進模型的桌面。 | s-window/rgyi2 | docs/videos/ai-terms/terms.json | — | CONFIRMED | context-window 第 1 層 #2，status planned（同批試片，還沒發布）；沒發布就由 package 指文章 |
| 82 | {"title": "有引用，不等於對", "cta": "先看它找到了什麼", "lines": ["完整文章在說明欄第一行", "下一個名詞：上下文視窗", "鄰近名詞：文件分塊、重新排序、微調"]} | wrap.data (outro) | tools/video/core/metadata.mjs composeDescription；terms.json related；ART 文末連結 | — | CONFIRMED | 組合後第一行「🔗 文章：…」；chunking、reranking、fine-tuning 都在 related 與文章連結 |

### 四、聽眾審稿改過的句子（11 條：數字與名稱有沒有被改到）

| # | 主張 | 位置 | 網址或示範檔 | HTTP | 判定 | 改前 → 改後／備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 83 | 十分鐘，看懂 RAG，檢索增強生成的三步，和它怎麼拿著證據答錯。 | s-stones/rgl64 | ART 首段（RAG＝檢索增強生成）、三步 | 200 | CONFIRMED | 只加了中文全名；數字沒動 |
| 84 | 示意的回覆是：可以，課程費一律全退，依據二〇二五年版規則。 | ask-refund/rgtjf | chat 卡；DOCS P4 | — | CONFIRMED | 「課程費一律全退」＝卡片「一律退還課程費全額」；二〇二五＝P4 2025 年版 |
| 85 | 第一段，現行的退費規則，今年的版本，開課前七天以上取消，退課程費全額。 | six/rg2m7 | DOCS P1 | — | CONFIRMED | 同 #54；七天、全額沒動 |
| 86 | 第三種，解讀過頭：條文寫材料費另計，模型可能把它接成全額退。 | s-bridge/rgicb | DOCS P4；ART | 200 | CONFIRMED | 同 #67；只加「可能」 |
| 87 | 不能拿最新的文件回答所有年份，文句再像，也要看是哪一年的。 | s-all-years/rg4e0 | ART 變體段「不能拿最新文件回答所有年份，也不能因為文句高度相似便忽略適用時點」 | 200 | CONFIRMED | 沒有數字 |
| 88 | 還是漏掉材料費？ | s-prompt-tinker/rgbtf | ART「若仍漏掉材料費」 | 200 | CONFIRMED | 拆句；後半是 #42 |
| 89 | 別為一頁紙蓋倉庫：要多複雜，得看資料量、更新頻率和權限。 | s-one-page/rg48c | ART「工程複雜度應跟資料規模、更新需求與資料權限一起考量」 | 200 | CONFIRMED | 三個因素沒動 |
| 90 | 要它穩定守格式、學特殊語氣，微調更貼近，兩個也能一起用。 | s-both/rgpjd | ART「若需求是穩定遵守格式或學會特殊語氣，微調可能更貼近問題，兩者也能併用」 | 200 | CONFIRMED | — |
| 91 | 搜尋，交出片段，讀者自己整理。 | methods/rgrcr | ART 表「讀者自行彙整答案」 | 200 | CONFIRMED | methods 卡仍寫「彙整」，字卡不受口語限制 |
| 92 | 一個模型要服務好幾套資料，也常從 RAG 開始。 | when/rgmm4 | ART「同一模型要服務多個資料集合時，RAG 常是合適起點」 | 200 | CONFIRMED | — |
| 93 | 只把第一名交給模型，它很可能拿著真實的文字答錯。／headline「拿著真的條文，很可能答錯」 | shorts.json 第二支 s-handoff（唯讀） | 長片 rgd4y | — | CONFIRMED | 與長片一致；shorts.json 沒動 |

## 摘要

- 查了 93 條：CONFIRMED 91、CHANGED 0、NOT FOUND 0、OUT OF SCOPE 2（s-colleague/0w7b7o、s-lift-sheet/ej39 兩句「如果你是…」，沒有事實主張）。第一輪改過的 16 處全部站得住；加長新增的 26 句與 `recap` 卡每一句的依據都在 demo JSON、`demo_rag.py` 的原文、文章或 brief §站主觀點裡；隨機抽的 39 條沒有一條翻案；聽眾審稿的 10 句沒有改到任何數字與名稱。
- 改了 0 個事實。`video.json` 一個字沒動；`claims.md` 只改兩處連帶：c9 把 rgd4y 的引文改成實際句子「它很可能拿著那段真實文字答錯」（原本多了一個「就」），並把「shorts.json 第二支仍是…待撰稿者同步」的過時註記改成已同步；「進度」加這一輪一行。
- 示範數字：`demo_rag.py` 重跑後 `docs`、`results` 與原 JSON 完全相同；說明欄六段整行逐字等於 DOCS，三題排名逐項等於 `ranked`；chat 卡右邊逐字＝Q1、左邊取自 P4 第二句；`rankings` 卡三列的第一名、最後一名、分數與 `highlight: 0` 全對；新句 0zvk9v7b（Q1 第二 P3 4.84）、ceyi（Q1 第四 P6 4.16、第五 P5 1.53）、e5pqgb80（Q3 第五 P4 0.42）、1d99／hvn67（P1＋P2 的正確答法）都對得上。
- 會過期的事實：「今年一月就失效」（rg26m、rgr09、說明欄、shorts 兩支）、「去年秋季」（rgo6s）、「去年停辦」（rgx7i、rankings 第三列、說明欄與 Q3 原句）只在 2026 年成立，2027 年要改；Google Cloud 頁面 Last updated 2026-09-28 UTC；arXiv abs 顯示 Submitted 22 May 2020、v4 2021-04-12；LangChain 頁面沒有日期；上下文視窗（planned）與嵌入向量、語意搜尋（backlog）那幾集都還沒發布，片尾與 s-keys 的「另一集」目前只能指文章。
- 意見：rglor、rgw87、rgof0、6m5s 都以「我的看法是」開頭，sohx 緊接 rgof0；內容與 brief §站主觀點逐句相符，沒有不符。brief 自己註明「提案，待站主確認」，README 說頻道立場 2026-09-29 仍空白——站主確認前不算定案，只報告。
- 聽眾檢查（只報告）：136 句最長 31 單位（recap/ttzt），沒有超過 40；沒有「本影片」「經查證」「根據官方文件」；拉丁字母只有 RAG（lexicon 有，唸「R A G」）；沒有括號、網址；每張卡的 reveal 數等於項目數，且都跟著介紹該項的那一句；hook 的「它回答的時候附了條文」到 s-counter 才揭露是示意（第一輪已報，加長輪在中間又插了 s-colleague，揭露更晚一句）。
- lint：`node tools/video/cli.mjs lint --slug ai-term-retrieval-augmented-generation` → 0 錯誤、2 個已知警告（平均 6.6 秒換畫面；估 12.5 分超過 9–11，README 說估計值可留）。136 句、2,681 單位、88 景、71 個 shot，與 claims.md 進度所寫相同。
- 懷疑但沒動：
  - rwu5ee「先把幾頁整個貼進去」：文章與同集的 rgqla、when 卡都說「一頁」，這句放寬成「幾頁」；是情境句的建議，不是數字，留給站主。
  - rgftv「RAG 只保證一件事」與第一輪同一個疑慮：比文章「沒有把生成器變成必然正確的引用機器」強，也比 rgicb「模型可能接出原文不支持的結論」強（連「從段落組出來」都不保證）；是 brief 的「其實」句，沒動。
  - rgann「模型根本看不到它」與 e5pqgb80「它不會自己浮上來」都隱含「只取前幾名」；六段全給它就看得到。旁白沒說取幾名。
  - 說明欄第二題的 0 分三段寫「第 3、4、6 段」，JSON 的同分順序是 6、4、3；同分的順序沒有意義，沒動。
  - `youtube.tags`「向量搜尋」不是 terms.json 的 alias（第一輪已報）。
  - 說明欄「第 1 段 4.70」：JSON 是 4.7，同一個值。
- 第三輪：**不用**。這一輪改了 0 個事實（規則：超過 3 個才要）。
