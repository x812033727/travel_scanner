# 系統一模型（System One Model）是什麼？它只從你列的選項裡挑，也會挑錯｜AI 名詞十分鐘

slug：`ai-term-system-one-model`｜`source_guide`：`ai-term-system-one-model`（文章還沒寫，票 `2026-10-03-ai-term-system-one-model-article`）｜系列「AI 名詞十分鐘」（不編集數）｜企劃日 2026-10-03｜目標 9–11 分鐘｜插圖投影片（`format: slides`、`look: tech-story`）、說書式旁白（Gemini Sulafat）、繁中 CC｜卡片配方 **B 先場景**｜企劃票 `2026-10-03-ai-terms-episode-system-one-plan`｜站主要決定的事、名詞庫的一列、研究紀錄在 [`notes.md`](notes.md)

名詞出處：TypeSafe 在 2026 年 9 月 15 日的發表文〈Introducing System One Models & Jev〉提出這個類別名，第一個這類模型叫 Jev。這是廠商自己創的詞，跟系列裡的 Agent Skills 一樣，片中一律說「TypeSafe 的說法是…」。中文名用天下文化版《快思慢想》的「系統一」。

## 觀眾

台灣與其他華語觀眾，三種人：

- 在社群或新聞看到「不聊天、只做決定的 AI」「System One」這類說法，想知道它跟聊天 AI 差在哪的人。
- 要讓程式自動處理留言、報名信、客服信的人：分類、轉給誰、要不要回信。他們現在多半是請聊天 AI 寫一段話，再想辦法從字裡把答案抓出來。
- 讀過站上「結構化輸出」「LLM-as-a-Judge」「推理模型」文章，想把這幾個名詞放在一起看清楚的人。

他們會用聊天工具，不用懂程式。搜尋的說法：「System One 模型」「系統一模型 是什麼」「不聊天的 AI」「決策模型 AI」「AI 只回答選項」「AI 分類 機率」。

## 觀眾看完能做到的事

- 下次要 AI 做選擇題時，自己寫好選項清單，而且一定放一個「信裡沒寫／其他」；再把選項順序倒過來問一次，看答案變不變。答案會跟著順序變，就不要讓它自動做決定。
- 拿到 AI 交回的選項和機率時，把「格式對」和「答案對」分開看：答案一定在清單裡，不代表是對的。事先決定把握不夠的交給誰處理。

## 站主觀點

提案，待站主確認（對應頻道立場草稿第 2、3、5 條與系列立場提案第 8、9 條；後台存的立場若條號不同，寫稿當天改成 `套用立場：N、M`）：

我的看法是：一個只交選項的模型，重點不是它多快，而是選項由誰寫、錯了由誰接。這個名詞改變我三個決定。

第一，交給它什麼。我只交給它懂行的人一秒就判斷得出來的題目，例如這兩則新聞是不是同一件事、這句錄音是不是照稿唸。要比日期先後、算金額、數數的題目，我們不出給它，留在程式裡。這是 TypeSafe 自己列的弱點，不是我猜的。

第二，怎麼寫它的選項。選項清單就是我給它的指令。只要清單可能不夠，我就加一個「沒寫」或「其他」。示範裡那道只給兩個日期的壞題，錯在出題的人，加上「沒寫」就修好了。看過失敗才算懂：出錯時我先分清楚是資料、指令、模型，還是我們自己的系統。有一天兩百多次檢查根本沒送出去，卻被記成「不確定」，錯的是我們的程式。

第三，信不信它的說法。「不會答出清單外」我只當成「格式一定對」，TypeSafe 自己的常見問題也寫了它可能選錯。我們在它發表後一週就接上，因為它解決的是我們真的有的問題。但 TypeSafe 說中文沒有英文準，我們還沒有用自己的內容量過，新聞發布關卡卻已經讓它直接判斷中文。這是我們接受的風險、要補的功課，不是它給的保證。

揭露（措辭與能不能公開說，站主確認後才定稿，見 `notes.md`）：Mokaair 按用量付費使用 TypeSafe 的模型。TypeSafe 沒有付錢、沒有給額度或優惠，也沒有參與、審閱或影響這支影片的內容。

## 示範或實算

**主案：寫稿當天實跑一次**（需要站主提供金鑰，這次企劃沒有呼叫）。腳本在 [`demo/`](demo/)，沿用站上自己的 Jev 客戶端，送出的請求跟站上的一模一樣；預設只印計畫、不連線，也不會印出金鑰。開跑前的失敗條件與讀法寫在 [`demo-log.md`](demo-log.md)，跑完照實填。

- 資料：「你好，我是王小美，想幫社團報名下週六的手作課，大概六個人。」29 個字，逐字取自站上〈結構化輸出〉文章的虛構情境。英文版是 Mokaair 的譯文，畫面標明。
- 五題一次送出：

| 題目 | 型別 | 選項 | 該選 |
| --- | --- | --- | --- |
| 信裡怎麼寫上課日期 | 選擇 | 寫了月和日／只說相對的日子／沒寫 | 只說相對的日子 |
| 同一題，選項倒過來 | 選擇 | 沒寫／只說相對的日子／寫了月和日 | 只說相對的日子 |
| 人數是估計的嗎 | 是非 | 0 到 1 的機率 | 是 |
| 上課是哪一天（壞題） | 選擇 | 10 月 10 日／10 月 17 日 | 沒有對的選項 |
| 同一題的修正版 | 選擇 | 10 月 10 日／10 月 17 日／信裡沒寫 | 信裡沒寫 |

- 呼叫次數：中文 1 次、英文 1 次，加上可選的日期探針 2 次，共 4 次。用 repo 的估算法，五題一次的請求約 460 個 token，只問兩題約 232 個。畫面只放 token 數和回應裡的用量，不放金額。
- 壞題事先登記兩種讀法，跑出哪一種就照實講：很有把握地挑了一個，或兩個日期各一半左右。兩種都歸類為**指令錯誤**，修正版那題就是證據。

**站上的生產紀錄**（已經發生的事，不用金鑰）：

| 紀錄 | 數字 | 出處 |
| --- | --- | --- |
| 旁白「妳」聽成「你」的甲句 | Jev 0.66，門檻 0.5，通過；沒有人聽過這句 | `docs/videos/series-plans/competition-20261002/pilot/review.md:55` |
| 旁白「妳」聽成「你」的乙句 | Jev 0.38，被標出來，等人工複聽 | `docs/videos/series-plans/competition-20261002/episodes/audio-check-summary.json`（WR-E01-L026） |
| 「姐」聽成「這」 | Jev 0.03，被標出來 | 同上（WR-E01-L022） |
| 每天的呼叫次數用完 | 243 次重複檢查有 207 次沒送到模型，卻被記成「不確定」；後來改成暫停排隊 | `tasks/done/2026-09-26-pause-news-candidates-when-the-jev.md:27-31` |
| 生成式模型的回覆壞掉 | 新聞產線第一次跑真實候選，頭五則有三則回覆沒通過程式的檢查，其中一則是 JSON 少了一個逗號 | `tasks/done/2026-09-24-let-news-model-replies-be-repaired.md:31-37` |

- 甲句和乙句是不同句子、不同次呼叫，不是對照實驗；只比文字。
- 最先漏掉「妳／你」的是我們自己的同音字規則：它用的拼音套件把「妳」讀成 nai3，所以這兩句才會送到 Jev。
- 兩句台詞來自還沒發表的作品，畫面只出現「妳→你」兩個字。

**在哪張卡**：第 2 章 `stats` 放「日期怎麼寫」三個選項的實測機率；第 3 章 `code` 放請求節錄；第 4 章 `terminal` 放實跑輸出（模型版本只出現在這張卡）、`table` 放五題的對照、`big` 放壞題的結果；第 5 章 `table` 與 `stats` 放生產紀錄；第 6 章 `steps` 放觀眾自己照做的四步。

**出錯時長什麼樣**（系列立場提案第 9 條）：

- 指令錯：清單裡沒有對的答案，它照樣挑一個。加上「信裡沒寫」就修好（第 4 章）。
- 模型錯：「妳」聽成「你」，一句過了、一句被標出來，同一種差別兩個答案（第 5 章）。
- 系統錯：呼叫次數用完，我們的程式把「沒問到」記成「不確定」（第 5 章）。

**備案：寫稿當天沒有金鑰**。旁白直接說「這次沒有實際呼叫它」，不用假數字。

- 第 2 章 `stats` 換成 shot。
- 第 4 章拿掉 `terminal`、實測的 `table` 和 `big`，改放 repo 的分級函式真的算一次的結果（`demo-log.md`，預設門檻 0.9／0.5）。同樣是九成「是」，是非題 0.90 在英文會被判「直接做」，二選一 (0.9, 0.1) 的信心值是 0.8，只到「交給人確認」。`big` 寫「同樣九成，一個自動做、一個交給人」，sub「這是我們自己程式的不一致」。
- 第 2 個「你以為／其實」改用 TypeSafe 常見問題那句引言撐。
- 第 5 章不變。

## 大綱

### 選項 B：先場景（配方 B）（推薦）

一行說明：開場是社團信箱收到一封報名信，程式要馬上決定「直接排進課表，還是回信問清楚」；先看決定長什麼樣，再給名字與來源，再講機制，第 4 章把同一封信真的交給它跑一次，第 5 章用站上的真實紀錄講它在哪裡錯過。跟 A 比，定義晚 20 秒出現；跟 C 比，不做「新模型對舊模型」的並排開場。三支試片依序用了 A、B、C，B 不會跟前一集連續重複。

開場鉤子（口播）：「社團信箱收到一封信：『想報名下週六的手作課，大概六個人。』程式得馬上決定：直接排進課表，還是先回信問清楚。」→ 停 900 →「負責判斷的 AI，它的答案，能直接交給程式去做嗎？」

- 約 66 個單位，加停頓約 17 秒，在 20 秒內落鉤。
- 三十秒承諾放在第 2 章第一句：「十分鐘，我把這封信真的交給它跑一次，看它怎麼答、哪裡會錯，再說我們網站把哪些決定交給了它。」

你以為／其實（第 2 章）：「你以為要 AI 做這個判斷，得先請它寫一段話，再叫程式從字裡把答案剪出來 → 其實有一類模型一個字都不寫：選項你先列好，它只交回一張卡，每個選項各幾成機率。」證據是第 2 章 `stats` 卡上這封信的實測機率。

你以為／其實（第 4 章）：「你以為它只會從清單裡挑，就不會答錯 → 其實清單裡沒有對的答案時，它照樣挑一個。」證據是壞題的實測結果，加上 TypeSafe 常見問題的原句：答案不會跑出清單，但可能選錯。

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`版型`：呈現內容；括號是逐條出現的次數） | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 一封報名信，AI 該怎麼判斷 | 18 | `title`：「系統一模型（System One Model）是什麼？」，副標「它只從你列的選項裡挑，也會挑錯」；`shot`：手作工坊門口的木信箱，一封信從投信口滑進來，工作台上有一團毛線和一把剪刀；`shot`：月台邊一節載著信封的小推車，停在三條岔軌前，一位小小的站務員手搭在轉轍器拉桿上；`shot`：推車輪子停在岔口的特寫 | 「負責判斷的 AI，它的答案，能直接交給程式去做嗎？」 |
| 2 | 系統一模型是什麼：不寫字，只交選項和機率 | 85 | `shot`：工坊長桌上攤著那封信和三張空白答案卡（三十秒承諾）；`shot`：家用織機一針一針織出長圍巾（你以為：先請 AI 寫一段話）；`shot`：一隻手拿剪刀，想從圍巾花紋裡剪下一小段（再叫程式從字裡剪出答案）；`shot`：剪下的毛線掉進兩個收件格之間的縫（寫出來的答案，格式偶爾會壞：我們新聞產線第一次上線，頭五則有三則回覆沒通過檢查）；`shot`：一張只有三排圓格的答案卡，一格被鉛筆塗滿（其實：只交一張卡）；`stats`：「這封信，它的全部回答」，三格是「寫了月和日」「只說相對的日子」「沒寫」的機率，寫稿當天實測，source「Mokaair 實測，<ran_on>」（3）；`shot`：三個秤盤，砝碼一大兩小（每個選項各幾成）；`shot`：答案卡直接插進課表木盒，桌上沒有剪刀（程式直接用，不用解析）；`shot`：工坊門口掛上一塊新的空白木牌，小小的木匠正在釘（TypeSafe 在 2026 年 9 月的發表文裡提出這個名字）；`big`：揭露，kicker「先說清楚」、text「Mokaair 按用量付費使用 TypeSafe 的模型」、sub「TypeSafe 沒有付錢，也沒有參與或審閱這支影片」（措辭站主確認）；`bullets`：「同一類東西，幾種叫法」：系統一模型（TypeSafe）／決策模型（Cloudflare、Liquid AI）／類似的分類器（Together）（3）；`shot`：夜市攤販一眼就從一排碗裡端起熟客要的那碗（名字借自康納曼《快思慢想》：「系統一代表著快的思考」）；`shot`：同一攤後面，一個人在小桌上把積木一塊塊排開推演（「系統二是慢的思考」；康納曼講的是人，不是模型） | 「一個字都不寫，它到底怎麼在選項之間做選擇？」 |
| 3 | 系統一模型怎麼運作：資料進去，選項和機率出來 | 105 | `chapter`；`diagram`：文章 `ai-term-system-one-model` 的 `diagram-1.svg`（左：一個 token 接一個 token 寫出字串，再交給程式解析，可能讀不懂；右：一份資料加你列的題目和選項，每個選項一個機率，程式直接用）；`shot`：市集評審長桌，中間一籃蘋果，三位評審各拿一張空白題卡（TypeSafe 文件的比喻：資料是攤在專家小組面前的材料）；`shot`：三位評審同時舉起空白木牌（每一題在同一次請求裡各自獨立評）；`quote`："A System One model evaluates a state and returns typed answers and probabilities."，譯「系統一模型評估一份資料，交回有型別的答案和機率。」（1）；`code`：第 4 章真的送出的請求節錄，≤8 行、每行 ≤64 字元，中文說明「題目和選項都是你寫的」，標亮只給兩個日期的那一題；`shot`：一排分揀木格（從清單挑一個）；`shot`：刻度尺上一顆木珠停在兩格之間（在你訂的等級上打分數，可以落在兩級中間）；`shot`：一枚硬幣在拇指上方翻轉（一句話成立的機率）；`stats`：「只有三種題目」：從清單挑一個，最多 255 個選項／打分數，2 到 10 級／是非，0 到 1 的機率，source「TypeSafe 文件，以官網為準」（3）；`shot`：評審桌上的籃子被塞進舊鞋、漁網、空瓶，評審皺眉（TypeSafe 自己寫：資料裡不相干的東西會降低準度）；`shot`：老果農瞄一眼蘋果就點頭（TypeSafe 的建議：問懂行的人一秒內判斷得出的事；要慢慢推的就拆成小題，由程式組合）；`shot`：一籃十顆蘋果，八顆貼著綠色圓點（TypeSafe 說機率經過校準，但校準講的是一大群答案，不保證眼前這一題）；`shot`：夜市攤販端錯一碗，客人愣住（康納曼說，錯誤是系統一造成的，系統二沒擋下來；TypeSafe 也承認這個名字帶著「容易出錯」的意思） | 「那把那封報名信真的交給它，它會在哪裡錯？」 |
| 4 | 實測：系統一模型會選錯嗎 | 140 | `chapter`；`shot`：月台上，信封躺在推車裡，前方三條岔軌（這次的選項就是軌道）；`chat`：標題「同一封報名信」，右邊「報名信」：「你好，我是王小美，想幫社團報名下週六的手作課，大概六個人。」（虛構情境）（1）；`shot`：站務員在推車上釘一張空白便條（開跑前先寫好什麼算失敗）；`terminal`：寫稿當天的實跑輸出，≤8 行、每行 ≤78 字元（1）；`shot`：站務員一次翻起五面號誌旗（五題一起回來）；`shot`：推車緩緩滑進中間那條軌道；`table`：「先寫好的對照」，欄位是 題目／該選／它選／最高機率，五列（日期怎麼寫、選項倒過來、人數是估計的嗎、只給兩個日期、加上「沒寫」），標亮第 4、5 列（5）；`shot`：同一排號誌旗左右對調（TypeSafe 自己寫，有些情況下它會偏向排第一個的選項，所以倒過來再問一次）；`shot`：岔口只剩兩條軌道，兩條都通往錯的月台（故意出的壞題；第二個你以為／其實）；`shot`：站務員的手被迫在兩根拉桿之間擇一；`big`：照預先登記的讀法寫實測結果，kicker「只給兩個日期」、text「它很有把握地挑了一個」或「兩個日期各一半左右」，sub「TypeSafe 自己寫：它回答的是你寫的題目，不是你想問的」；`shot`：岔軌旁多鋪一條通往「退回」的空白軌道，推車滑上去（修正版：加上「信裡沒寫」，它就選了這條）；`quote`："If you provide a list of categories, it can’t invent a category outside that list, but it can choose the wrong one."，譯「你給它一份分類清單，它不會發明清單外的分類，但可能選錯。」，TypeSafe 官網常見問題（1）；`shot`：廚房裡，餅乾模具壓出形狀完美的餅乾，餡卻包錯了（形狀對，內容錯）；`shot`：天平兩端各放一個信封，一個蓋紅郵戳、一個蓋藍郵戳（同一封信的英文版由 Mokaair 翻譯；中英結果落在門檻兩邊就照實說）；`compare`：標題「同一封信，兩種回答」，左「會寫字的生成式模型」：寫一段話，程式要再解析／能自己說「信裡沒寫」、講理由／回覆的格式可能壞掉；右「系統一模型」：只交你列的選項和每個選項的機率／跳不出清單，連「信裡沒寫」都要你先列／一樣會選錯（2）；旁白補一句：「公平地說，用結構化輸出把生成式模型綁在格式裡，它一樣跳不出清單。TypeSafe 說的差別，是它從一開始就為這種決定訓練，每個選項都附機率。」；`shot`：站務員拿著被退回的信封走向牆上的電話（把握不夠或選了「沒寫」，就回信問清楚） | 「格式一定對，答案會選錯。那我們自己的網站，真的把哪些決定交給了它？」 |
| 5 | 系統一模型實際怎麼用：新聞去重、旁白核對 | 95 | `chapter`；`shot`：編輯部長桌，兩個幾乎一樣的包裹並排，一位小小的編輯拿放大鏡比對；`table`：「我們交給它的三種決定」，欄位是 用在哪／問它什麼／答案怎麼用：新聞去重／跟已發布的是不是同一件事／0.85 以上當重複、0.25 以下當新的、中間交給編輯；新聞發布／這篇能不能發布，五個語系各問一次／五個都過站主設的門檻就自動發布，中文也直接算；旁白核對／錄到的跟稿子是不是同一句／低於 0.5 標出來，一句都沒標就自動核准（3，標亮第 3 列）；`shot`：印刷廠輸送帶把一箱箱封好的包裹直接送上貨車，旁邊沒有人（自動發布前沒人再看一次）；`shot`：錄音室麥克風前的小人，耳機掛在一旁；`stats`：「同一種差別，兩個答案」：0.66 是「妳」聽成「你」的甲句，通過／0.38 是「妳」聽成「你」的乙句，被標出來／0.03 是一個字整句聽錯，被標出來；note「不同句子、不同次呼叫，不是對照實驗；只比文字」；source「Mokaair 製作紀錄，門檻 0.5」（3）；`shot`：兩支幾乎一樣的音叉，一支放進「通過」木盒，一支擱在一旁；`shot`：篩網上一個小破洞，一顆小石子漏下去（先漏掉這一對的，是我們自己的同音字規則）；`shot`：一位小小的編輯接住被標出來的信封（這次錯在保守那一邊，交給人聽）；`shot`：一個空掉的木籤筒，後面一排包裹被貼上黃色貼紙（呼叫次數用完那天，243 次重複檢查裡有 207 次根本沒送到模型，卻被我們的程式記成「不確定」；後來改成暫停排隊）；`shot`：四個抽屜，分別放卷宗、題卡、齒輪、一截水管（出錯先分清楚：資料、指令、模型，還是我們自己的系統）；`shot`：兩疊封好的信放在兩個秤上，一疊紅郵戳、一疊藍郵戳（TypeSafe 說中文沒有英文準，要先用自己的內容測；我們還沒有系統地量過） | 「那你手上的工作，哪些該交給這種只交選項的模型？」 |
| 6 | 什麼工作該交給系統一模型 | 80 | `chapter`；`shot`：餐廳廚房，主廚瞄一眼就把三塊牛排分到三個盤子（懂行的人一秒判斷得出來）；`bullets`：答案能事先列成選項，清單裡有「沒寫／其他」（如果你要把客服信分成五類）／懂行的人一秒判斷得出來，不用算數、數數、比日期（如果你的判斷要算錢或比日期，留給程式）／量大要快，而且先想好錯了由誰接（如果你要讓程式自動處理一整天的留言）（3）；`shot`：學徒把一大籃馬鈴薯按大小分成三籃；`shot`：夜市攤位前排著長隊，老闆一碗接一碗出餐（量大、要快）；`shot`：算盤、一碗要數的紅豆、兩張空白日期卡被推到桌子另一邊（TypeSafe 自己列的弱點：不是計算機、數數不可靠、把日期當文字讀）；`shot`：一條繞好幾個彎的山路，遠處一個慢慢走的旅人（要一步步推的事，TypeSafe 自己也說，複雜數學、像下棋的規劃交給大型推理模型）；`shot`：主廚只接過一張小題卡，把厚厚的任務手冊推回去（題目寫成一句話；大問題拆成小題，由程式組合）；`shot`：一卷捲得很厚的信紙卡在出菜口（要它寫回覆、寫摘要，就不是它的工作）；`steps`：「你自己就能做的檢查」：列好選項 → 加一個「沒寫／其他」 → 選項倒過來再問一次 → 把握不夠的交給人（4）；`shot`：安全網接住一個掉下來的盤子（錯了由誰接） | 「它聽起來像推理模型的反面，又像縮小版的聊天 AI，它到底跟誰不一樣？」 |
| 7 | 系統一模型跟推理模型、小型語言模型、LLM-as-a-Judge 差在哪 | 85 | `chapter`；`shot`：屋頂工作台上並排三樣東西：一雙登山鞋、一台小織機、一塊評分木牌；`table`：欄位是 名詞／交出什麼／跟系統一模型差在哪：推理模型（Reasoning Model）／先寫出好幾步想法再寫答案／常被比作系統二，慢，適合要繞彎的題目；小型語言模型（Small Language Model）／還是一個字一個字寫，只是模型比較小／差在交出什麼，不在大小，系統一模型多大 TypeSafe 沒公布；以語言模型擔任評審（LLM-as-a-Judge）／常常先寫評語再給分／同一份工作，系統一模型只交分數和每一級的機率（3）；`shot`：山路和林間捷徑在岔口分開，登山客走了山路；`shot`：小織機也在一針一針地織（小模型還是在寫字）；`shot`：一位工匠把大織機的針板換成只有三個孔的模板（另一家廠商拿開放的小模型微調出「類似的分類器」；Cloudflare 也說分類模型早就有了）；`shot`：評審手上的長評語被剪掉，只留一塊分數木牌；`shot`：一本空白記錄本和二十封信放在秤旁（這些機率能不能信，要拿自己的資料量）；`shot`：回到開場的月台，推車滑進「退回」軌道，站務員拿起電話（回答開場）；`shot`：工坊桌上，一隻手在答案卡最後多畫一個空白圓格（站主觀點一句）；`shot`：手作教室裡，社團成員圍著桌子動手做（日期問清楚了，課照常開）；`outro`：title「系統一模型」、lines「只從你列的選項裡挑」「『沒寫』也要是一個選項」「把握不夠，交給人」、cta「說明欄第一行：系統一模型是什麼」 | 最後一句回答開場：「所以，負責判斷的 AI 不用寫一句話：它從你列的選項裡挑一個，附上每個選項的機率。它的答案能交給程式，但不能直接照做：『信裡沒寫』也要是一個選項，把握不夠的，交給人。」 |

數量：秒數加總 608 秒（18＋85＋105＋140＋95＋80＋85）；shot 60 個，約占片長六成；卡片 26 張，含 5 張章節卡。畫面平均約 6 秒換一次，撰稿時任何一張卡停留都不超過 8 秒。旁白照系列規格寫到 2,650–2,750 個單位。版型序列跟三支試片的相似度：token 0.58、上下文視窗 0.46、RAG 0.38，都低於 0.8 的警告線（寫稿後用 `video.json` 重算）。

骨架：配方 B 的相對順序都在：`title`(1) → `shot`(1) → `shot`(1) → `stats`(2) → `chapter`(3) → `diagram`(3) → `shot`(3) → `quote`(3) → `code`(3) → `shot`(3) → `compare`(4) → `chapter`(5) → `bullets`(6) → `shot`(6) → `outro`(7)。

示範在第 4 章，第 5 章是站上的真實紀錄。結尾的下一步（只有一個）：說明欄第一行的文章〈系統一模型是什麼〉。說明欄另外列鄰近名詞的文章（推理模型、小型語言模型、LLM-as-a-Judge）、〈結構化輸出〉和總索引，口頭只講一個下一步。

### 選項 A：先誤解（配方 A）

一行說明：從「又快又便宜的 AI，就是縮小、變笨的聊天機器人」切入，用定義和介面推翻它，再講機制、示範、站上用法、什麼時候用、跟誰搞混；「是什麼」最早回答，但「其實」只能靠「它的定義裡沒有大小」撐，而且容易像在替廠商辯護。

開場鉤子（口播）：「有一類 AI 一個字都不寫，只交回選項和機率。」→ 停 900 →「你以為又快又便宜的 AI，就是縮小、變笨的聊天機器人？那它到底是什麼？」

你以為／其實：「你以為又快又便宜的 AI，就是縮小、變笨的聊天機器人 → 其實這一類的分界在它交出什麼：TypeSafe 文件寫它不寫回覆、不寫程式、也不解釋自己的推理；它多大，TypeSafe 沒有公布。」

| # | 章節 | 秒 | 場景 | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 一個字都不寫的 AI | 18 | `title`；`shot`：空白的答案卡；`shot`：收起來的織機 | 「那它到底是什麼？」 |
| 2 | 系統一模型不是縮小版的聊天機器人 | 85 | `chapter`；`big`「0 句回覆」；`shot`：大小不同的兩台織機（大小不是重點）、答案卡、木牌、夜市攤販（名字的來源） | 「它不寫字，那要怎麼回答？」 |
| 3 | 資料進，選項和機率出 | 110 | `chapter`；`diagram`；`steps`（4）；`shot`：評審桌、分揀木格、刻度尺、硬幣 | 「丟一封真的信給它，會怎樣？」 |
| 4 | 拿一封報名信實際問一次 | 125 | `chapter`；`chat`；`terminal`；`stats`（3）；`big`；`quote`；`shot`：月台、岔軌、退回軌道 | 「我們站上真的把它用在哪裡？」 |
| 5 | 系統一模型實際怎麼用 | 85 | `chapter`；`table`（3）；`stats`（3）；`shot`：編輯部、錄音室、木籤筒 | 「什麼時候該用？」 |
| 6 | 什麼時候該用系統一模型 | 85 | `chapter`；`bullets`（3，每條一個「如果你…」）；`shot`：廚房、算盤、山路 | 「它跟小模型差在哪？」 |
| 7 | 跟小型語言模型、推理模型、LLM-as-a-Judge 差在哪 | 92 | `chapter`；`compare`（2）；`shot`：登山鞋、小織機、評分木牌；`outro` | 回答開場 |

示範在第 4 章；下一步是說明欄第一行的文章。風險：配方 A 和校準那份企劃相同；「縮小變笨」正是 TypeSafe 常見問題自己的問法，片子會像在替廠商回答；第 2 章塞了約 10 個重點，第 7 章平均約 8.4 秒換一個畫面，超過上限。

### 選項 C：先示範（配方 C）

一行說明：開場就並排同一封信、同一題：會寫字的模型回一段文字，系統一模型交回一張機率卡；證據最先出現，但整個開場押在寫稿當天兩邊都跑成功，而且並排正是 TypeSafe 發表文的示範格式，最像模型比較。

開場鉤子（口播）：「同一封報名信，同一題三選一。一個 AI 用文字回答你；另一個一個字都不寫，只交回一個選項，和每個選項的機率。」→ 停 900 →「它的答案，能不能直接交給程式去做？」

你以為／其實：「你以為系統一模型是比較小、比較便宜的聊天 AI → 其實它根本不寫字：開場那張機率卡就是它全部的回答；TypeSafe 說它懂語言，但不寫自由文字、不當聊天機器人。」

| # | 章節 | 秒 | 場景 | 收尾問題 |
| --- | --- | --- | --- | --- |
| 1 | 同一封信，兩種回答 | 20 | `title`；`chat`（2）；`shot`：兩張並排的回答 | 「後面那張卡，能直接交給程式嗎？」 |
| 2 | 系統一模型是什麼，名字從哪來 | 95 | `big`「它不寫字」；`stats`（3，實測）；`bullets`（3）；`quote`（《快思慢想》）；`shot`：答案卡、夜市攤販 | 「這些機率是怎麼來的？」 |
| 3 | 怎麼運作：資料進去，選項和機率出來 | 100 | `chapter`；`steps`（4）；`diagram`；`shot`：評審桌、分揀木格 | 「那它出錯的時候長什麼樣？」 |
| 4 | 實測：清單裡沒有對的答案 | 115 | `chapter`；`table`（5）；`big`；`shot`：岔軌、退回軌道 | 「什麼時候該照做、什麼時候交給人？」 |
| 5 | 什麼時候該用，我們站上怎麼用 | 100 | `chapter`；`bullets`（3）；`stats`；`shot`：編輯部、錄音室 | 「它跟誰不一樣？」 |
| 6 | 跟推理模型、小型語言模型、LLM-as-a-Judge 差在哪 | 85 | `chapter`；`compare`（2）；`shot`：登山鞋、小織機 | 「回到開頭：能直接交給程式嗎？」 |
| 7 | 不會答出清單外，不等於不會錯 | 85 | `quote`（官網常見問題）；`shot`：餅乾模具、電話；`outro` | 回答開場 |

示範在第 1、4 章；下一步是說明欄第一行的文章。風險：沒有金鑰就沒有開場；TypeSafe 自己承認那種並排示範「讓我們的模型看起來比較有利」，系列也不做模型比較；配方 C 不能緊接在 RAG 後面；shot 只占約 52%，貼著五成的下限。

## 會過期的事實

措辭規則：

- 廠商的說法一律講成「TypeSafe 說…」「TypeSafe 自己寫…」；上限數字只放字卡，標「以官網為準」。
- 不說「不會幻覺」「不會出錯」「不會有型別錯誤」，最多說「不會答出清單外，但會選錯」。
- 不說「這個詞是 9 月 15 日發明的」，說「在 2026 年 9 月的發表文裡提出」；精確日期只放來源和說明欄。
- 旁白不唸 Jev、網址、函式名稱。康納曼已在 2024 年 3 月 27 日過世，不用現在式描述他。

| 事實（片中用法） | 來源與原文 | 開啟日 |
| --- | --- | --- |
| 類別名稱、提出日期 | https://typesafe.ai/blog/introducing-system-one-models-and-jev ："Sep 15, 2026"；"TypeSafe AI is releasing our first System One Model" | 2026-10-03 |
| 定義、不寫回覆、校準講的是一群答案 | https://docs.typesafe.ai/concepts/system-one ："A System One model evaluates a state and returns typed answers and probabilities."；"System One models do not write replies, produce code, or generate explanations of their reasoning."；"Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct." | 2026-10-03 |
| 資料像攤在專家小組面前的材料 | https://docs.typesafe.ai/concepts/state ："Think of state as the material you would present to a panel of experts before asking them to make a judgment." | 2026-10-03 |
| 每題各自獨立、同一次請求 | https://docs.typesafe.ai/introduction ："Every question is evaluated in parallel and in isolation against the same state in one go." | 2026-10-03 |
| 選項上限 255，建議加「其他」 | https://docs.typesafe.ai/primitives/choice ："A Choice question accepts up to 255 options"；"Add an `other` or `none of the above` option when the list might not cover every input, so the model can say none of the others fit." | 2026-10-03 |
| 分數 2 到 10 級，可以落在兩級中間 | https://docs.typesafe.ai/primitives/score ："Should have at least two levels; the API accepts up to 10."；"it can land between two levels" | 2026-10-03 |
| 是非題 0 到 1，沒有另外的信心值 | https://docs.typesafe.ai/primitives/noul ："There is no separate `confidence` value for a Noul, unlike a Choice or a Score." | 2026-10-03 |
| 問懂行的人一秒判斷得出的事，大問題拆小題 | https://docs.typesafe.ai/primitives ："Ask for a judgment a knowledgeable person makes in a second given the right context."；"break the task into small questions and compose the answers in code" | 2026-10-03 |
| 弱點（只適用 jev-1.13，頁面註明 Last reviewed 2026-10-02） | https://docs.typesafe.ai/model-jaggedness/jev-1.13 ："answers the question you wrote, not the one you meant"；"Jev is not a calculator."；"does not count reliably"；"reads dates as text, not as ordered quantities"；"In some cases, we observed that the order of a Choice's options can affect the answer, and `jev-1.13` leans toward the option that comes first."；"unrelated material in the `state` costs you accuracy"。換模型版本就要重查；站上固定用 `jev-1.13.0`（`apps/api/app/config.py:265`） | 2026-10-03 |
| 中文沒有英文準 | https://docs.typesafe.ai/models ："English is the primary training language and where accuracy is currently best. Other languages, including CJK scripts, are handled but not equally well; test on your own content before relying on Jev for a non-English workload" | 2026-10-03 |
| 「可能選錯」的引言卡；跟 JSON mode 的差別；複雜數學交給推理模型 | https://typesafe.ai/ 首頁常見問題（在折疊選單裡，寫稿當天用瀏覽器重開）："If you provide a list of categories, it can’t invent a category outside that list, but it can choose the wrong one."；"System One Models are trained for structured decisions from the start, returning typed answers with calibrated probabilities."；"Some tasks requiring extended reasoning, such as complex mathematics or chess-like planning, may be better suited to large reasoning models." | 2026-10-03 |
| 名字帶著「容易出錯」的意思 | 發表文的常見問題："“System 1 thinking” has also implied error-prone." | 2026-10-03 |
| 其他叫法 | Cloudflare 2026-10-01 部落格 https://blog.cloudflare.com/clef-decision-models/ ："While classifier models have been around for some time, Jev introduces a new decision model concept"；Liquid AI https://docs.liquid.ai/lfm/models/decision-models ："Decision models are a new class of AI model purpose-built for structured decisions."；Together https://www.together.ai/blog/how-to-train-your-own-jev ："our own Jev-like classifier" | 2026-10-03 |
| 系統一、系統二 | 天下文化書摘 https://bookzone.cwgv.com.tw/article/30366 ：「系統一代表著快的思考，系統二是慢的思考。」書籍頁 https://bookzone.cwgv.com.tw/book/BCB490D （康納曼著，洪蘭譯）；諾貝爾演講 https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf ："System 1, which generated the error, and System 2 which failed to detect and correct it"；過世日期 https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/facts/ | 2026-10-03 |
| 站上的門檻與開關 | 新聞去重 0.85／0.25（`apps/api/app/news_automation/ai.py:433`）；新聞發布每個語系問一次、寫死 `cjk_autopilot=True`（`ai.py:352-361`，站主 2026-09-25 決定），門檻是後台設定，2026-09-26 紀錄從 0.9 調成 0.55（`tasks/done/2026-09-26-news-reviewers-hold-translations-for-the.md:52-53`，**寫稿當天到後台確認現值**）；旁白標記門檻 0.5（`tools/video/tts/check.mjs:53`），零標記且設定開著就自動核准（`apps/api/app/video_reviews/admin_service.py:1446-1458`，**寫稿當天確認設定**） | repo 2026-10-03 讀過 |
| 站上的生產紀錄 | 0.66、0.38、0.03（2026-10-02，UTC）；207／243（2026-09-26）；頭五則三則失敗（2026-09-24）。歷史紀錄不會變，但乙句的人工複聽狀態可能會變 | repo 2026-10-03 讀過 |

## 素材

- 文章：`apps/api/app/guides/content/ai-term-system-one-model.json`，**還不存在**。依系列規則先走 skill `content-pipeline` 寫文章，發布後才出片。
- 圖解：文章的 `apps/web/public/guides/ai-term-system-one-model/diagram-1.svg`，內容是左「逐字生成，再解析，可能讀不懂」對右「一份資料加題目，每個選項一個機率，程式直接用」，© Mokaair，登記在 `assets`。〈結構化輸出〉那張圖解有英文字，而且示範的是同一封信的同一種失敗，不拿來代用。
- 示範：[`demo/`](demo/) 的腳本與 [`demo-log.md`](demo-log.md)。
- 一手來源（`video.json` 的 `sources` 至少挑兩個）：TypeSafe 發表文；TypeSafe 文件 concepts/system-one、concepts/state、introduction、primitives（含 choice、score、noul）、models、model-jaggedness/jev-1.13；typesafe.ai 首頁常見問題；Cloudflare 部落格、Liquid AI 文件、Together 部落格；天下文化書籍頁與書摘、諾貝爾演講。
- 站上程式（Mokaair 自有，只講做法，不放程式畫面）：`apps/api/app/ai/jev.py`、`apps/api/app/news_automation/ai.py:311-435`、`tools/video/tts/check.mjs`、上面列的生產紀錄檔。
- 同一封信的出處：`apps/api/app/guides/content/ai-term-structured-outputs.json`（zh-TW 示例，虛構情境）。
- 插圖（look `tech-story`，每章有自己的地點和道具）：手作工坊與木信箱、月台與轉轍器、號誌旗與推車；織機與圍巾、答案卡上的圓格、秤盤和砝碼；夜市攤販、市集評審與蘋果籃、分揀木格、刻度尺加木珠、翻轉的硬幣；餅乾模具、編輯部和包裹、印刷廠輸送帶、錄音室麥克風、音叉、篩網上的破洞、木籤筒、四個抽屜；餐廳廚房、算盤和紅豆、山路和旅人、屋頂工作台、登山鞋、評分木牌。全部不畫文字（含書頁、招牌、鐘面、螢幕、月曆）、logo、真人、產品畫面，也不用機器人、筆電、燈泡、大腦。
- 縮圖：「三排圓格的答案卡，一格被塗滿」那個 shot；tag「AI 名詞十分鐘」、headline「系統一模型」、sub「只從你的清單裡挑」。
- 鄰近名詞：推理模型（`reasoning-model`）、小型語言模型（`small-language-model`）、LLM-as-a-Judge（`llm-as-a-judge`），文章另外連大型語言模型、幻覺。
- `lexicon.json` 要新增：TypeSafe、System、One、Model、Reasoning、Small、Language、Judge、as（LLM-as-a-Judge）、Liquid、Together、Mokaair（揭露句要唸）。LLM、AI、Cloudflare、token 已經有。
- Shorts：一句話定義（「它一個字都不寫，只從你列的選項裡挑一個、附上機率」）；第 2 章的你以為／其實（先寫一段話再剪答案 → 只交一張卡）。

## 不做的事

- 不講價格、免費輸出、每百萬 token 多少錢、193.6×／444.6×、「快兩個數量級」、延遲秒數、評測分數、任何模型名稱（GPT、Claude 等）、排行榜。
- 不描述架構、大小、取樣方式，不展開 RLCD 訓練法；這些廠商都沒公開細節。
- 不說「不會幻覺」「不會出錯」「型別錯誤在數學上不可能」。
- 不講創辦人經歷、「隱身兩年」、Jev 取名自傑文斯、Doom 和維基賽跑的示範：那是產品新聞，不是名詞。
- 不做新聞報導式包裝：標題、縮圖、旁白不出現「爆紅」、發表日、提早體驗、等候名單、註冊連結；副標不用「不聊天只做決定」。
- 旁白和章節名稱不說 Jev；模型版本只出現在 `terminal` 卡。
- 不做模型比較：生成式模型那一邊只用我們自己產線的歷史紀錄，不拿某個模型跑分對比。
- 不放假數字或示意 JSON 冒充真實回覆；沒跑過的不說「我測過」。
- 不說「站上不讓它單獨對中文做決定」，也不暗示我們量過中文準度。
- 不承諾還沒發布的影片；「這些機率能不能信」只講要拿自己的資料量。
- 不露出未發表作品的台詞，「妳→你」以外一律不出現。
- 不用「判別式模型」這個詞，不冒充 TypeSafe 的介面，不截文件頁面的畫面。
- 旁白不出現「本影片」「經查證」「根據官方文件」。
