# 提示詞、上下文、駕馭、迴圈、圖形工程是什麼？AI 出錯，先別急著改指令｜AI 名詞十分鐘

slug：`ai-terms-prompt-to-graph-engineering`｜`source_guide: ai-term-harness-engineering`（五個名詞的中間一層；另外三篇文章連在說明欄本文）｜系列「AI 名詞十分鐘」（不編集數）｜企劃日 2026-10-03｜目標 9–11 分鐘（成片落在 9.5–10.5）｜插圖投影片（`format: slides`，`look` 留給工人從版畫預設裡挑）、說書式旁白（Gemini Sulafat）、繁中 CC｜卡片配方 **D 先地圖**（三集試片用掉 A、B、C；這集是五個名詞的總覽，先給一張樓層圖再逐層講）｜票 `2026-10-03-ai-terms-engineering-ladder-video`

這集與系列規格不同的一點：**一集講五個名詞**，不是一個。理由是這五個詞在 2026 年總是一起出現、互相定義（「圖形工程是把迴圈排成圖」「駕馭工程把提示詞和上下文包在裡面」），單講任何一個都得先解釋另外四個；而且觀眾的問題不是「某一個是什麼」，是「名詞一直換，我該追哪一個」。單一名詞的深講仍留給 `terms.json` 裡各自的那一集（提示詞工程、上下文工程在第 1 層，Harness Engineering 與 Loop Engineering 在第 3 層）；這集是它們的地圖，片尾指向各自的文章。

名詞的中文：站上文章把 Harness Engineering 譯作「代理執行環境工程」；坊間（KodeLab、數位時代、Data-DI）多用「駕馭工程」，站主的需求也寫「駕馭工程」。這集旁白用**駕馭工程**（好唸、跟「馬具」的原意接得上），字卡同時標英文與站上文章的譯名；Graph Engineering 旁白用**圖形工程**，字卡標英文。五個名詞的英文全名只放字卡，旁白全部說中文（連 Agent 也說「代理」），所以不動共用的 `lexicon.json`。

## 觀眾

台灣與其他華語觀眾優先，三種人：

- 會把文件、公告貼給 AI 整理、也開始試 AI 代理（讓它自己查資料、改檔案）的一般使用者。他們看過「提示詞工程」，最近又在社群看到「上下文工程」「Harness」「迴圈」「圖形」，覺得昨天學的今天就過時。
- 剛接 AI 自動化流程的小團隊或自由工作者：用過自動化工具把流程跑起來，卻卡在「出錯攔不住、跑一半重來、沒人敢改」。
- 讀過站上五篇工程名詞文章、想用十分鐘聽懂它們怎麼疊在一起的人。

他們會用聊天工具，不用懂程式。搜尋的說法：「harness engineering 是什麼」「駕馭工程」「context engineering 上下文工程 差別」「loop engineering 迴圈工程」「graph engineering 圖形工程」「AI agent 工程 名詞」「prompt engineering 過時」。

## 觀眾看完能做到的事

- 下次 AI 出錯，先不改指令，照五個問題找層：格式跑掉、口氣不對 → 一樓改指令；答不出你那份資料 → 二樓看它這次到底看到什麼；跑兩步就闖禍、或嘴上說做完了 → 三樓看誰在攔它、驗證跟產出分不分開；一直重試停不下來 → 四樓補停止條件和預算；做到一半當掉全部重來 → 五樓把流程畫成圖、每一步存進度。
- 評估任何「會自己跑」的 AI 流程時，問三件事再決定要不要用、要不要付錢：預算上限有沒有寫進流程、驗證的是不是寫答案的那個、權限界線是寫在工具裡還是只寫在提示詞裡。

## 站主觀點

提案，待站主確認（頻道立場草稿 2026-09-29 查證仍空白；對應草稿第 3、4、5 條與系列立場提案第 8、9 條；立場存進設定之後，撰稿把第一行改成「套用立場：N、M」）：

我的看法是，名詞換了五個，該修哪一層的判斷一直沒變。AI 出錯的時候先別急著改指令，先問它這一次看到什麼、有沒有東西在攔它、迴圈會不會停。這五個名詞會改變我的三個決定。第一，花不花錢：一個會自己跑的流程，預算上限要寫在流程裡、過關卡的時候檢查；停不住花費的系統不叫自主，叫燒錢。第二，信不信答案：驗證的人不能是寫答案的人，代理說「做完了」只是一句需要驗證的話，測試、頁面、紀錄才是證據。第三，給不給權限：安全靠寫在工具裡的界線——哪些檔案能改、哪些動作要人點頭、花到多少就停——不靠寫在提示詞裡的「不要做錯事」。我們自己做這支影片的產線就是這樣蓋的：規則在工具層，核准綁檔案雜湊，重寫有上限，一支影片有花費上限；示範是今天真的跑的指令，不是任何產品的畫面。我不說哪家代理產品比較好，不講模型名稱與排行榜。

## 示範或實算

示範不呼叫任何 AI 模型（本機沒有金鑰，也不冒充任何產品介面），示範的是**我們自己做這一集的產線**，每一項都是 2026-10-03 在這個 repo 真的執行、真的查到的，逐字抄在 `demo-log.md`：

| 層 | 示範什麼 | 在哪張卡 |
| --- | --- | --- |
| 三樓 駕馭 | **檢查工具擋下稿子**：在旁白故意放一個沒進發音字典的英文詞，跑 `node tools/video/cli.mjs lint --slug ai-terms-prompt-to-graph-engineering`，工具以錯誤擋下（結束碼 1），後面要花錢的合成、畫圖都不會開始。輸出逐字放進 `terminal` 卡，附執行日期與工具版本（repo 的 git 短碼） | 第 5 章 `lint-terminal` |
| 三樓 駕馭 | **寫在產線裡的數字**：一支插圖影片的花費上限預設 20 美元（`apps/api/app/video_automation/schemas.py` 的 `slides_max_usd_per_video`）、大綱重寫上限 2 次（`tools/video/automation/flow.mjs` 的 `MAX_REPLANS`）、旁白一直被聽錯時的改寫上限 2 輪（`MAX_REWRITE_ROUNDS`，`automation.test.mjs` 鎖定為 2）；每一道核准綁檔案雜湊，檔案改了舊核准失效（`docs/videos/HANDS-OFF.md`、`automated.md`） | 第 5 章 `ledger-stats`、`seal-wax` |
| 四樓 迴圈 | **我們自己的迴圈**：這支稿子寫、檢查、改、再檢查，`lint` 跑到零錯誤為止的次數；每一次的錯誤與警告數記在 `demo-log.md`，次數填進 `our-loop` 卡 | 第 6 章 `our-loop` |
| 五樓 圖形 | **產線就是一張圖**：`status --slug` 印出的 14 個步驟、每步一個關卡、進度從檔案算出來（不靠誰記得）、站主是其中一個節點（等他點頭時影片停在那一格，不用整支重來）。今天對 `ai-term-token` 跑一次 `status` 當證據 | 第 7 章 `our-graph` |

**出錯時長什麼樣**（系列立場提案第 9 條，每層一個）：一樓，公告寫得很順卻多了一行「免費材料」；二樓，資料在雲端卻沒進這次呼叫、或舊規章新規章混在一起；三樓，代理在驗證之前就宣布完成（Anthropic 2025-11 的長任務研究記錄的失敗方式）；四樓，同一個檔案改十幾次每次只動一點的死迴圈（LangChain 2026-02 的追蹤紀錄），以及重試一百次也不會讓錯的網址變對（站上文章的例子）；五樓，死在第四十步只能從頭來、停不住花費（Simmons 的說法）。

## 大綱

### 選項 A：先地圖（配方 D，採用）

一行說明：開場用觀眾自己的反應（AI 出錯就回去改指令）切入，第一章把五個名詞排成一張五層樓的表當地圖，之後一層一章、每層一個生活場景與一次「失敗的樣子」，第三層放我們自己產線的示範，最後一章把地圖變成診斷表回答開場。與 B（先示範）相比，觀眾在 1 分 40 秒內就拿到整張地圖，再往下聽每一層都知道它在哪個位置；與 C（先場景）相比少一點戲、多一點秩序，適合五個名詞的總覽。

開場鉤子（口播）：「AI 做錯事的時候，你的第一個反應，是不是回去改指令？」→ 停 900 →「這三年，工程師換了五個名詞；十分鐘，排成一張樓層圖，你就知道該修哪一層。」

你以為／其實：「你以為這五個名詞是五波流行，新的來了舊的就該丟 → 其實它們是疊起來的樓房，每一層都還在，只是從主角變成零件；一條公式把它講最短：代理 ＝ 模型 ＋ 外面那一層」

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | AI 出錯，你先改指令？ | 17 | `title`：「從提示詞到圖形工程」副標「AI 出錯，先別急著改指令」；`shot`：社區布告欄前，志工手裡一疊揉皺的草稿 | （鉤子直接落在第二句） |
| 2 | 你以為是五個新詞，其實是五層樓 | 85 | `chapter`（你以為）；`shot`：老公寓樓梯間，搬家工人抱箱子上樓（其實是疊起來的樓房）；`big`：代理 ＝ 模型 ＋ 外面那一層／Agent = Model + Harness；`table`：五層樓 × 名詞 × 管的是什麼（5）；`shot`：兩個工人在樓層間傳箱子（各家樓層排法不同；照今年夏天一份學術綜述的點名）；`shot`：房東手上的一串鑰匙，挑出一把（名詞換了，先找是哪一層出問題沒變） | 「那一樓，提示詞工程，到底在管什麼？」 |
| 3 | 一樓 提示詞工程：單次對話的指令 | 105 | `chapter`；`shot`：活動中心志工桌，一張卡片、一支鉛筆（只有一個輸入框）；`shot`：志工把手寫公告釘上軟木板（例子：五樣資料改成公告）；`quote`：Google Cloud 提示工程指南的定義句；`chat`：右「你」把資料與要求分開 → 左「示意回覆」只保留給的事實（2）；`shot`：第二位志工皺眉指著公告、桌上一盤沒人要的餅乾（失敗：多了免費材料）；`steps`：寫清楚什麼算完成 → 分開原料與要求 → 給缺漏留出口（3）；`shot`：俯拍兩版公告並排、上方一排小案例卡（每次改版拿同一組案例重測；一家模型公司的提示文件開頭先問成功標準與測法）；`shot`：表單上日期欄空白（沒給日期變不出日期；資料有卻沒看到就不是一樓的事） | 「那它這一次，到底看到了什麼？」 |
| 4 | 二樓 上下文工程：這一次，它看到什麼 | 95 | `chapter`；`shot`：管理室櫃台，住戶問借交誼廳、管理員伸手拿架上的資料夾；`quote`：Anthropic 2025-09-29 的定義原句與譯文（1）；`shot`：漏斗與玻璃罐，少數紙條落下、一疊留在桌上（重點是這一次需要什麼證據）；`shot`：檔案室一整牆資料夾、管理員背影（在雲端不等於進了這次呼叫）；`shot`：兩位住戶各拿一本規章爭執、管理員舉手（來源衝突要回報）；`shot`：俯拍被公告淹沒的櫃台、手在翻找（塞越多越鈍：上下文腐化）；`shot`：合起來的小筆記本與便條（把決定寫在對話外；只留漂亮摘要會丟掉「不能收費」）；`diagram`：文章圖解（篩選版本與權限才進模型）；`shot`：住戶與管理員握手、鑰匙牌交接（資料對了指令對了，模型動手改東西誰攔它） | 「資料對了、指令對了，模型卻動手去改東西，誰來攔它？」 |
| 5 | 三樓 駕馭工程：模型外面的那一層 | 150 | `chapter`（英文原意是馬具）；`shot`：陰天牧場，馬站在木柵欄旁、馬伕扛著籠頭走來（沒有馬具就是野馬）；`shot`：特寫扣籠頭皮帶的手（定義）；`bullets`：LangChain 2026-03 的清單：系統提示詞、工具技能連接器、檔案系統沙盒瀏覽器、調度、鉤子（5）；`shot`：柵欄門與鐵閂（只要你不是模型，你就是馬具；提示詞與上下文成了零件）；`quote`：Hashimoto 2026-02 的那句與譯文（1）；`shot`：蹄鐵匠修蹄、另一人牽繩（做法兩種：規矩寫進開工必讀的檔案，或寫一個工具去檢查）；`shot`：印刷工坊，工人掀起剛印好的紙（拿我們自己的產線當例子）；`terminal`：真實的 lint 指令與輸出：字典沒有的詞被擋下、1 個錯誤（2）；`shot`：黃銅量規卡住變形的版（規矩在工具裡，不是提示詞裡的「不要做錯事」）；`shot`：櫃台上數硬幣進鐵盒（花費也寫在產線裡）；`stats`：20 美元／2 次／2 輪（3）；`shot`：火漆封印壓上文件（核准綁指紋，改一字就失效）；`cta`：說明欄第一行的文章；`shot`：年輕馬伕得意拍馬、身後馬鞍沒扣、老馬伕指著（失敗：驗證前就宣布完成）；`shot`：從馬背後方看韁繩與路（馬具裝好了還是你牽一步說一句，什麼時候它能自己跑） | 「什麼時候它能自己跑？」 |
| 6 | 四樓 迴圈工程：自己重試，也知道何時停 | 110 | `chapter`（口號：別再一句一句提示代理，去設計會提示它的迴圈）；`shot`：清晨田徑場，跑者在遠彎道、教練在內側欄杆（觀察執行檢查重試一圈一圈跑）；`steps`：Karpathy autoresearch：改一處 → 固定訓練五分鐘 → 比對指標 → 留或丟再一圈（4）；`shot`：穿睡袍的人清晨推開工具間的門，貓坐在一疊卡片上（一小時約十二圈、一晚約一百圈；小玩笑）；`shot`：長凳上一排水瓶、教練拿走一瓶（最怕停不下來；重試一百次不會讓錯網址變對）；`shot`：教練舉平手、跑者放慢（成功與失敗都要停止條件）；`diagram`：文章圖解（三個出口與進度紀錄）；`shot`：終點線一人拉帶、一人吹哨看腳（寫答案的和打分數的要分開）；`shot`：鞋尖磨出同一道溝（死迴圈：同一檔案改十幾次；有團隊在工具層數次數）；`big`：我們自己的迴圈：lint 跑了 N 次才歸零；`shot`：練習後空蕩的跑道、兩人收角錐（一個迴圈一次只做一件事，十個代理誰來排） | 「十個代理一起跑，誰來排？」 |
| 7 | 五樓 圖形工程：把迴圈排成一張圖 | 80 | `chapter`（今年夏天才被叫出名字）；`shot`：鐵路調度場五條岔線、調度員走在軌道間（定義：明確的圖而不是隱含的迴圈）；`steps`：節點只做一件事 → 邊是決定 → 狀態有格式每過一條邊存檔（3）；`shot`：特寫戴手套的手拉道岔桿（迴圈沒死，被降級：節點裡照樣跑小圈）；`shot`：側線上停著的貨車、輪下木楔、辦事員走開（死在第四十步重跑那個節點；等人簽核三天不佔視窗）；`shot`：煤斗旁插著量尺、工人用拇指讀高度（預算寫在狀態裡；停不住花費的叫燒錢）；`bullets`：我們的產線也是一張圖：14 步一步一關、進度從檔案算、站主也是節點（3）；`shot`：調度員與司機在調度室木桌上對照掛著彩色線頭的釘板（回到開場的問題） | 「那回到開場：AI 出錯的時候，到底該修哪一層？」 |
| 8 | 出錯了，修哪一層 | 70 | `chapter`（我的看法是：名詞換了五個，判斷沒變）；`table`：症狀 × 先看哪一層（5）；`shot`：修車廠，技師指著引擎蓋下的一個零件、車主抱胸看（三個決定：花不花錢、信不信、給不給權限）；`shot`：特寫技師從工具箱挑出一支扳手（一層一層找）；`compare`：代理迴圈 vs 迴圈工程／提示詞 vs 上下文（2）；`outro`：AI 出錯，先找哪一層；下一步 | 最後一句回答開場：「所以，AI 出錯的時候，先別急著改指令；五層樓，一層一層找。」 |

示範在第 5 章（terminal、stats、seal-wax）、第 6 章（our-loop）、第 7 章（our-graph）。結尾的下一步（只有一個）：說明欄第一行的文章（代理執行環境工程）；片尾另列提示詞、上下文、迴圈三篇文章與「代理迴圈」（下一個名詞，先讀文章）。總長約 710 秒估計（lint 用每分鐘 250 單位估約 12 分，實際合成約每分鐘 300 字，成片約 10 分鐘）；旁白約 2,700 個口語單位；shot 約 70 張、卡片約 28 張（含 8 張章節卡），畫面狀態約 130 個。

### 選項 B：先示範（配方 C）

一行說明：開場就播我們自己的檢查工具把稿子擋下來的那一幕（真實的 lint 輸出），用「這一層叫駕馭工程」倒著往下講提示詞與上下文，再往上講迴圈與圖形；順序是示範 → 三樓 → 一樓二樓 → 四樓五樓 → 診斷表。與 A 相比前三十秒就看到真的東西，但觀眾要到第 3 章才拿到整張地圖，而且「三樓」先講會讓五層的順序在腦中打結。

開場鉤子（口播）：「我們的 AI 寫完這支影片的稿子，第一個把它擋下來的，不是人，是一行指令。」→ 停 900 →「這一層今年有個新名字，叫駕馭工程；它上面還有兩層，下面還有兩層。」

你以為／其實：「你以為 AI 做得好不好，看的是指令寫得多好 → 其實一個代理等於模型加上外面那一層，提示詞只是那一層裡的一個零件」

| # | 章節 | 秒 | 場景 | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 第一個擋下稿子的不是人 | 30 | `title`；`terminal`：真實的 lint 輸出（2）；`shot`：印刷工坊 | 「這一層叫什麼？」 |
| 2 | 三樓 駕馭工程 | 130 | `shot`×3 牧場；`big`：公式；`bullets`：清單（5）；`quote`：Hashimoto（1）；`stats`：20／2／2（3） | 「它底下的兩層是什麼？」 |
| 3 | 一樓二樓：指令與資料 | 170 | `shot`×6 活動中心與管理室；`chat`（2）；`quote`：Anthropic（1）；`diagram`：上下文圖解 | 「什麼時候它能自己跑？」 |
| 4 | 四樓五樓：迴圈與圖 | 190 | `shot`×8 田徑場與調度場；`steps`：autoresearch（4）；`steps`：三個承諾（3）；`big`：我們的迴圈；`bullets`：我們的圖（3） | 「出錯了，修哪一層？」 |
| 5 | 診斷表 | 80 | `table`（5）；`compare`（2）；`shot`×2 修車廠；`outro` | 回答開場 |

示範在第 1、2、4 章。風險：五層的順序被打亂（3 → 1、2 → 4、5），總覽型的影片最需要順序；`terminal` 卡放在第一分鐘，還不知道什麼是「產線」的觀眾看不懂那行輸出。

### 選項 C：先場景（配方 B）

一行說明：從牧場的馬和馬具開始講故事——一匹有力氣的馬怎麼從被人牽著、到裝上馬具、到自己跑圈、到一整個馬隊被排成隊形——用一個場景串五層，最後才給名詞表。與 A 相比更像一個故事、插圖更一致，但五個名詞要到第 6 分鐘才一次出現，搜尋這些名詞進來的觀眾會等太久；而且馬的比喻只對「駕馭」貼切，硬套在「提示詞」「圖形」上會失真。

開場鉤子（口播）：「一匹馬再有力氣，沒有馬具，就只是一匹野馬。」→ 停 900 →「這三年，AI 工程圈吵的其實都是同一件事：怎麼替一個夠聰明的模型，裝上對的馬具。」

你以為／其實：「你以為聰明的模型自己就會做事 → 其實能做事的是模型加上外面那一層；一個同模型不換、只改外面那一層的實驗，分數跳了一個世代（LangChain 2026-02，以該文為準，不講模型名）」

| # | 章節 | 秒 | 場景 | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 野馬 | 20 | `title`；`shot`：牧場 | 「馬具是什麼？」 |
| 2 | 牽著走：指令與資料 | 150 | `shot`×6 馬伕用口令與手勢；`chat`；`quote`×2 | 「什麼時候它能自己跑？」 |
| 3 | 裝上馬具 | 140 | `shot`×5；`bullets`（5）；`stats`（3）；`terminal`（2） | 「跑圈誰來喊停？」 |
| 4 | 自己跑圈 | 120 | `shot`×5 馬場跑圈；`steps`（4）；`diagram` | 「一整隊馬怎麼排？」 |
| 5 | 排成隊形 | 100 | `shot`×4 馬隊；`steps`（3）；`bullets`（3） | 「這五層叫什麼名字？」 |
| 6 | 五個名字與診斷表 | 70 | `table`（5）；`table`（5）；`outro` | 回答開場 |

示範在第 3、4、5 章。風險：一個比喻撐十分鐘，插圖的「同一個地點或物件不超過三分之一」會踩線（lint 的 motif 警告）；名詞太晚出現。

## 會過期的事實

- 「圖形工程」是 2026 年夏天才被命名、各家樓層排法仍無共識：Josh C. Simmons 的文章（他把階梯排成提示詞 → 上下文 → 迴圈 → 圖形，**沒有**駕馭那一層）與 arXiv 2608.21156 的綜述（五個都點名：Prompt、Context、Harness、Loop、Graph）；數位時代 2026-07-28 也寫「誰上誰下還沒有定論」。影片只說「各家排法不一樣，這集照一份今年夏天的學術綜述排」。https://www.drjoshcsimmons.com/writing/we-are-entering-the-graph-engineering-phase 、https://arxiv.org/abs/2608.21156 （2026-08-21 v1、08-26 v2）
- 定義句（寫稿當天確認）：Anthropic 2025-09-29「Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference」、「Prompt engineering refers to methods for writing and organizing LLM instructions for optimal outcomes」、「context rot」https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ；LangChain 2026-03-10「Agent = Model + Harness」「If you're not the model, you're the harness」與清單（System Prompts；Tools, Skills, MCPs；Bundled Infrastructure；Orchestration Logic；Hooks/Middleware）https://www.langchain.com/blog/the-anatomy-of-an-agent-harness ；Hashimoto 2026-02-05 的那句 https://mitchellh.com/writing/my-ai-adoption-journey ；Google Cloud 提示工程指南（上次更新 2026-05-04）https://cloud.google.com/discover/what-is-prompt-engineering?hl=zh-TW ；Claude 文件「Before prompt engineering」三個前提 https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- 失敗的樣子：Anthropic 2025-11-26「a later agent instance would look around, see that progress had been made, and declare the job done」「Claude's tendency to mark a feature as complete without proper testing」https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents ；LangChain 2026-02-17「doom loops… (10+ times in some traces)」「LoopDetectionMiddleware that tracks per-file edit counts」https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering （該文的分數與模型名**不講**）
- 迴圈工程：Addy Osmani 2026-06-07（引述 Steinberger「You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents.」）https://addyosmani.com/blog/loop-engineering/ ；Karpathy autoresearch README（「trains for 5 minutes, checks if the result improved, keeps or discards, and repeats」「approx 12 experiments/hour and approx 100 experiments while you sleep」「The agent only touches train.py」，署名 March 2026）https://raw.githubusercontent.com/karpathy/autoresearch/master/README.md （github.com 對我們的 UA 回 403，用 raw）
- 圖形工程的三個承諾、「The loop is not dead. It got demoted.」「a graph can wait three days for a human sign-off」「If you cannot stop an agent at a spend threshold, you are not running an autonomous system. You are running up a bill.」：Simmons（同上）；LangGraph 文件「nodes do the work, edges tell what to do next」、checkpointer 用於 human-in-the-loop 與 fault tolerance https://docs.langchain.com/oss/python/langgraph/graph-api 、https://docs.langchain.com/oss/python/langgraph/persistence
- 我們產線的數字綁在 repo 的 main：`slides_max_usd_per_video` 預設 20（`apps/api/app/video_automation/schemas.py`）、`MAX_REPLANS = 2`（`tools/video/automation/flow.mjs`）、`MAX_REWRITE_ROUNDS` 2（`automation.test.mjs` 鎖定）、14 個步驟（`status` 的輸出）。改了設定或程式，字卡要跟著改。https://raw.githubusercontent.com/x812033727/travel_scanner/main/apps/api/app/video_automation/schemas.py 、https://raw.githubusercontent.com/x812033727/travel_scanner/main/tools/video/automation/flow.mjs 、https://raw.githubusercontent.com/x812033727/travel_scanner/main/docs/videos/HANDS-OFF.md
- OpenAI 2026-02 的〈Harness engineering〉對我們的 UA 回 403（Wayback 也連不上），所以它的數字（團隊人數、程式行數）**不講**；影片不提這篇。
- 站內文章（查證日 2026-09-14）：https://mokaair.com/zh-TW/life/ai-term-harness-engineering 、ai-term-prompt-engineering、ai-term-context-engineering、ai-term-loop-engineering、ai-terms-index（2026-10-03 都回 200）。「代理迴圈」那一集還沒上架：片尾先指文章 https://mokaair.com/zh-TW/life/ai-term-agent-loop

## 素材

- 文章（zh-TW，Mokaair 自有）：`apps/api/app/guides/content/ai-term-harness-engineering.json`（報名網站、完成條件、「只在提示詞寫不要做錯事不能代替權限」）、`ai-term-prompt-engineering.json`（社區公告：親子植栽、週六上午、交誼廳、要報名、費用未定；失敗＝補出免費材料）、`ai-term-context-engineering.json`（借交誼廳；漏斗；來源衝突；把決定寫在對話外）、`ai-term-loop-engineering.json`（展覽活動表；重試一百次不會讓錯網址變對；五步；停止條件）。
- 圖解（`diagram` 版型各用一次，`assets` 登記，© Mokaair）：`apps/web/public/guides/ai-term-context-engineering/diagram-1.svg`（版本與權限篩選才進模型）、`apps/web/public/guides/ai-term-loop-engineering/diagram-1.svg`（執行、驗證、三個出口、持久紀錄）。提示詞與駕馭的圖解這集不用（卡片已夠多）。
- 示範資料：`demo-log.md`（2026-10-03 的 lint 執行紀錄、status 輸出、常數出處）。
- 官方與一手來源（2026-10-03 開過，純文字存在撰稿 scratchpad）：見「會過期的事實」。
- 插圖：全部 AI 生成，`look` 留給工人挑版畫預設；八個章節各自的地點與道具：布告欄、老公寓樓梯間、活動中心志工桌、管理室與檔案室、牧場與印刷工坊、清晨田徑場、鐵路調度場、修車廠。不畫字、logo、真人、產品畫面、螢幕。縮圖用樓梯間那張 shot，大字「五層樓」。
- 鄰近名詞（`terms.json` 的 `related`）：代理迴圈（`ai-term-agent-loop`，片尾的下一個名詞）、提示詞串接、上下文壓縮、子代理、代理式工程。

## 不做的事

- 不講模型名稱、價格、方案、排行榜、跑分：LangChain 實驗的分數與模型名不講，只說「同一個模型不換、只改外面那一層」都不提數字；OpenAI 的文章抓不到就整篇不提。
- 不講 2022、2023 這類年份當事實（只有來源頁面上的日期才講：「去年秋天」「今年二月」「今年三月」「今年夏天」各對應一篇一手來源）。
- 不說哪一家的樓層排法是對的；不替「駕馭工程」「圖形工程」發明通用定義——每個定義都說「一家模型公司」「一家代理框架公司」「一位工程師」「一位研究者」是誰的說法，字卡標出處。
- 不冒充任何聊天產品或代理產品的介面：`chat` 卡的回覆標「示意回覆」；`terminal` 卡是我們自己的工具、自己跑的輸出。
- 不說「我測過」任何代理產品；我們的示範只限這個 repo 的工具與設定。
- 不深講各層的機制：分詞、RAG、壓縮、子代理、MCP、評測各有自己那一集；這集每層只講「管什麼、失敗長什麼樣、怎麼分辨」。
- 旁白不出現英文名詞（Agent 說「代理」、Harness 說「馬具」或「駕馭工程」），不唸網址、檔名、程式常數名；不出現「本影片」「經查證」「根據官方文件」。
- 不用原來如此事務所的任何梗；不重複 token、上下文視窗、RAG 三集的開場與場景（紙帶、罐子、圖書室櫃台）。
