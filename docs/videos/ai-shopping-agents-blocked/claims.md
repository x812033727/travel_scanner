# 查核清單：ai-shopping-agents-blocked

撰稿 2026-10-22。每一行一個可查的主張：編號｜主張（旁白或畫面怎麼說）｜出處網址｜查證日｜用到它的場景 id。
片中沒有任何一次是本頻道的實測：所有嘗試都是 The Verge 記者（2026-10-22 報導的作者）自己做的，旁白每次都說「記者」。
The Verge 三篇與 TechCrunch 的網址都在 2026-10-22 以編輯 UA 重新開過（HTTP 200，無轉址）；沃爾瑪新聞稿是第 6 章唯一的官方來源；兩篇 Mokaair 文章的 JSON 存在 `_tools/sources/mokaair-*.json`。

c1｜在紐約，The Verge 記者請 Meta 的 AI 代理 Muse 去找一罐特定的面霜（「a specific face moisturizer」；記者在紐約：報導說西岸零售商不送到 New York、也不送到 my address）。查核第 1 輪：拿掉「2026 年 10 月」，報導沒寫實測日期（只知道在 Muse 9 月上市之後、10-22 刊出之前）｜https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse｜2026-10-22｜hook, apt-note
c2｜Muse 某天被 Target 的機器人檢查（bot check）擋下，隔天通過（「was caught in Target's bot check one day but was able to get through the next」）。查核第 1 輪：第 1 章章名與 qq3n 原寫「一天三種結果」，報導是兩天、三次嘗試、兩種結果，改成「擋了又放，放了又擋」／「時開時關」，說明欄同步｜同 c1｜2026-10-22｜guard-stops, bot-check, next-day-open, too-dumb, street-of-doors, target-door-ajar, ch4, closing
c3｜幾分鐘後記者改問某價位以下的床墊，Muse 又被 Target 擋下（「despite being able to pull from the site just a few minutes prior」）｜同 c1｜2026-10-22｜mattress-blocked, too-dumb
c4｜記者要 Muse 找穀物棒每一片的最低價，它給了 Sam's Club、Walmart、Costco 的選項（「it offered options from Sam's Club, Walmart, and Costco」）。查核第 2 輪：zd4i 原寫「手上三張收據」，收據表示已經付款，報導寫的是 offered options、Muse 沒有替她買，改「手上三張價目單」；插圖的紙片仍可讀成價目單，不用重畫｜同 c1｜2026-10-22｜receipts-tease, ch2, receipts-return
c5｜Muse 自己補充：Amazon 可能有最低價，但它被完全封鎖（hard-blocked）無法確認（quote 卡的英文句是 The Verge 記者的轉述，不是 Muse 的逐字輸出，卡片 source 標「記者轉述」）｜同 c1｜2026-10-22｜muse-caveat, three-questions
c6｜Amazon 封鎖 Muse：彈窗在一個星期天開始出現（報導 2026-09-21 週一刊出，彈窗是「on Sunday」＝9 月 20 日，旁白只說「九月一個星期天」），原文「continued access by an unauthorized AI agent violates Amazon's Conditions of Use, to which our customers have agreed.」；三個理由（Meta 未事先通知、Muse 瀏覽時不表明身分、疑似擷取顧客登入資料）是 GeekWire 報導、The Verge 轉引；Amazon 發言人向 The Verge 證實「requested that Meta remove Amazon」from Muse，並說第三方程式「should operate openly and respect service provider decisions about whether or not to participate」｜https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping ；https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse｜2026-10-22｜sunday-notice-tease, street-of-doors, gate-question, ch3, sunday-notice, popup-quote, three-reasons, remove-request, openly, three-doors, closing
c7｜Muse 推薦過一家不送到記者地址的連鎖超市；記者另外提到要跟它澄清一家西岸零售商不送到紐約（旁白合成「西岸的超市，根本不送到紐約」）｜同 c1｜2026-10-22｜west-coast-box
c8｜記者算上等回覆、要它多搜幾家、澄清送貨範圍的時間，認為自己搜大概還比較快（「it likely would have been faster to search myself」；查核第 1 輪在 3wra 補「大概」對應 likely）；她把代理比成「anxious and apologetic teenager」去跑腿，要一大堆指示、回來的東西不完全是要的；她也說最適合代理的是「finding the absolute lowest price on a product you already know you want」｜同 c1｜2026-10-22｜waiting-at-table, faster-myself, apologetic-runner, wrong-item, rote-task
c9｜The RealReal 實驗：商品放進購物車保留 20 分鐘，別人拿不到（「making it impossible for other people to swipe it」；10 件全放進去「effectively blocking other shoppers from purchasing them」，查核第 1 輪 45au 改「等於一件都拿不到」）；記者要 Muse 把喜歡的品牌最新上架的 10 件一次全放進購物車；她無意購買；每次 20 分鐘到期就要它再放一次；「On and on this went, all day」；最後是記者自己結束任務；「If I were a less honest, pure-hearted person, I would deploy an agent to run this personalized, technically allowed reserve system endlessly」；她擔心很快要跟別人的代理競爭｜同 c1｜2026-10-22｜boutique-tease, open-door-bell, ch5, realreal-rules, fitting-room-armful, twenty-minutes-again, queue-outside, stop-bell, second-runner, hold-tickets
c10｜Amazon 自家平台內有代理式購物功能：監控價格、自動補貨、依使用者設的規則購買（旁白「沒想到，Amazon 自己平台裡就有一個代理」）；站主觀點「生意的攻防」是意見｜同 c1｜2026-10-22｜own-runner, repeat-basket, two-shops, business-fight
c11｜Amazon 去年（2025）11 月告 Perplexity（Comet 購物功能），法官今年 8 月站在 Perplexity 那一邊；Amazon 的確認信自 7 月起拿掉品名與商品圖片，避免被外部 AI 讀取；紙底版表格「對方的代理也在站上買」出自 10-22 那篇（ignored its requests to stop its agent from shopping on the site，查核第 3 輪補記）｜https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping ；https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse｜2026-10-23｜amazon-stats, perplexity
c12｜JPMorgan Chase 執行長 Jamie Dimon 說銀行不會讓外部代理存取帳戶，對客戶和公司「too risky」（旁白不唸人名）｜同 c1｜2026-10-22｜bank-counter
c13｜沃爾瑪 2026-10-21 宣布讓代理替顧客購物、附規則；The Verge 寫「Next month」會讓你在網站上用 AI 代理（片尾「沃爾瑪下個月開」）。查核第 1 輪：開場預告 rbf3 原寫「同一週，沃爾瑪……」，接在九月的 Amazon 與 The RealReal 那一天後面，聽起來是同一週，報導沒寫 The RealReal 實驗的日期、Amazon 彈窗是 9 月，改「十月，沃爾瑪……」｜https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers ；https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents｜2026-10-22｜walmart-door-tease, street-of-doors, superstore-far, ch6, closing
c14｜Target 發言人：代理能否存取要看它怎麼做那件任務與有哪些防護；代理可能進得了網站的一部分、進不了另一部分，為了保護顧客資料與購物體驗；Target 有防護擋未授權的代理與機器人存取顧客帳號、發起交易。旁白 e7qb 是把發言人的話套回記者的兩次嘗試，是推論，不是發言人逐字；發言人說的是「may depend」，查核第 1 輪改成「可能就看那一次任務怎麼做」｜同 c1｜2026-10-22｜target-answer, guard-explains, three-doors, three-questions
c15｜Target 與 OpenAI、Google、Microsoft 有 AI 購物合作；報導列的名單裡沒有 Muse（旁白只說「報導列出的合作名單裡，沒有 Muse」，不說 Target 拒絕 Muse）｜同 c1｜2026-10-22｜partners
c16｜一般的防機器人系統也會攔下代理：沒有全面封鎖的網站，既有的防火牆也會讓代理時好時壞（「AI agents can also get caught in the web of general bot blocking systems」「existing firewalls can make agents inconsistent」）。報導寫 also，沒說比誰的決定更常見；查核第 1 輪 8uyh 的「更多時候」改「有時候」｜同 c1｜2026-10-22｜trolley-turnstile, turnstile-next-day
c17｜The RealReal 賣每月 12 美元的訂閱，讓買家搶先看新品（記者的說法；The RealReal 官網未查）｜同 c1｜2026-10-22｜realreal-rules
c18｜The RealReal 技術長 Luke Friang：「Our approach is to remain open to third-party AI agents, allowing them to browse, log in and interact with our marketplace, while maintaining safeguards against automated activity that could disrupt the customer experience」（旁白不唸人名）｜同 c1｜2026-10-22｜realreal-quote
c19｜Meta 發言人 Tracy Clayton：「users can take over at any time, Muse is designed to always ask permission before buying, and it applies ethical browsing principles when asked to do things that a human could not - like buying all the tickets to an event」；「The response from retailers has been overwhelmingly positive」（旁白不唸人名；「它會用它的瀏覽原則處理」是對 applies ethical browsing principles 的翻譯，原文沒有說「拒絕」；查核第 1 輪把 quote 卡的譯文補回 ethical：「套用合乎倫理的瀏覽原則」）。p68i 原寫「Muse 說一律會」，說這句的是 Meta 發言人，查核第 1 輪改「Meta 說一律會」｜同 c1｜2026-10-22｜meta-quote, handshake, three-questions
c20｜沃爾瑪新聞稿把 Muse、ChatGPT、Gemini 列為已有的對話式購物整合（「conversational commerce integrations with Muse, ChatGPT, Gemini and others」）｜https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers｜2026-10-22｜walmart-door
c21｜Agent Profiles：一個月內推出（launching in the next month）；第一次經由 Walmart Agent Gateway 用某個代理購物時自動建立；登入沃爾瑪帳號授權連結，只有沃爾瑪看得到（Only Walmart sees this）；顧客可選每筆核准，或在自設上限內自動購買，例子 $50、$100、$200；可隨時刪除設定檔。核准是「預設」每筆（Customers must approve agent purchases by default），也可設上限讓它自動買，所以第 6 章章名與卡片原寫「每一筆都要你點頭」改「每一筆預設要你點頭」（查核第 1 輪）。kg8h 原寫「Muse 第一次經過它的閘道」：沒有任何來源說 Muse 會走 Agent Gateway，改「代理第一次經過」（查核第 1 輪）。條款另有一條「即使在上限內，沃爾瑪仍可能要求額外核准」，旁白沒講，不算錯｜同 c20｜2026-10-22｜agent-profiles, limits, torn-ticket, three-questions, ch6
c22｜Walmart Agent Gateway 用 MCP 連線（新聞稿寫「MCP (model text protocol)」，實為 Model Context Protocol；旁白只說 MCP 並以白話解釋）；先對企業與開發者開測試版（新聞稿是未來式「We'll begin with a beta for companies and developers」；The Verge 寫「currently available in beta」，官方優先，查核第 1 輪 8e66「現在先」改「它會先」）；替代理找出顧客常買的東西（例子：酸種麵包、特定品牌牛奶）而不分享更廣的購買紀錄｜同 c20｜2026-10-22｜service-hatch, bread-milk, usual-items
c23｜代理看到的價格與人看到的一樣（「the prices that an AI agent sees are the same prices that a human would see on Walmart.com」）。three-doors 表的第三欄原寫「Muse 碰到的」，沃爾瑪那一列是還沒上線的規則、Muse 沒碰過，查核第 1 輪改「代理會碰到的」｜同 c20｜2026-10-22｜three-doors, closing
c24｜沃爾瑪給 AI 代理的條款：顧客預設必須核准代理購買；代理不得做超出購物者意圖的事；拿不到付款卡資料、不能新增或改付款方式；只能取得任務需要且顧客允許的資料；退貨流程適用，包括代理未照預期行動；不遵守就封鎖｜同 c20｜2026-10-22｜agent-terms
c25｜有沃爾瑪帳號就能用代理，不需要 Walmart+ 會員（只有 TechCrunch 寫，沃爾瑪新聞稿與 The Verge 都沒有）；Sam's Club 也能用代理購物（新聞稿、The Verge、TechCrunch 都寫）。查核第 1 輪：8qub 原寫「不用付費會員……Sam's Club 也一樣」，聽起來像 Sam's Club 也不用會員，沒有來源這樣說（Sam's Club 本身是會員制），改「Sam's Club 也能用代理買」；說明欄原寫「The Verge 與 TechCrunch……只補充不用付費會員、Sam's Club 也適用」，改成只有 TechCrunch 補充不需要 Walmart+｜https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/｜2026-10-22｜account-check
c26｜記者把一件古董洋裝的照片、年份、關鍵字、相似品備註與要搜的二手平台交給 Muse；Muse 哪裡都找不到那件洋裝，但提醒她同品牌有一場即將舉行的拍賣；記者說有時間與耐心帶它，Muse 能把特定物件的搜尋做得更深｜同 c1｜2026-10-22｜ny-again, ch7, photo-handoff, not-found, auction-hall, deeper-search
c27｜封鎖前 The Verge 曾用 Muse 在 Amazon 成功買到背心（tank tops）｜https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping｜2026-10-22｜three-doors
c28｜Muse 在 2026 年 9 月上旬推出（The Verge 2026-09-21 寫「launched Muse earlier this month」；旁白「那時 Muse 上市還不到一個月」）｜同 c27｜2026-10-22｜ch3

沒有數字的主張：c6 的彈窗日期只說「九月一個星期天」（報導只寫 on Sunday，沒寫日期）；c13 的「下個月」沿用 The Verge 的 next month，沃爾瑪新聞稿寫 launching in the next month；c17 的 12 美元是記者的說法，The RealReal 官網沒查。

## 與企劃不同的地方

- 拿掉 `source_guide`：`lint` 只認 `apps/api/app/guides/content/` 裡的內容包，站上這篇是每小時自動新聞、只在資料庫裡，寫了就是一條錯誤；工人路線（`automation/flow.mjs` 的 `settle()`）遇到同樣情況也是刪掉 `source_guide`、把文章放進 `sources`。所以 Mokaair 的兩篇文章放在 `sources`，說明欄會在參考資料列出；`cta` 卡仍說「說明欄的文章」。
- 第 1 章原估 55 秒、第 2 章 85 秒、第 4 章 70 秒、第 6 章 100 秒；寫出來是 60／65／62／131 秒（lint 估計）：第 6 章多了條款五條各一句、不用付費會員與 Sam's Club、設定檔一個月內推出；第 2 章少講了一句站主觀點（「任何幫你找最低價的答案都少了一家最大的店」併進第 7 章與片尾）。
- 第 3 章的章名從「9 月 21 日，Amazon 跳出一行字」改成「Amazon 跳出的那一行字」：彈窗是 9 月 20 日（星期天）出現、報導 9 月 21 日刊出，章名不寫會被查核退回的日期；卡片副標寫 The Verge 2026-09-21。
- 第 3 章多了 Amazon 要求 Meta 把 Amazon 從 Muse 移除（企劃放在第 6 章的表）；第 6 章表格的 Amazon 列改講封鎖前 The Verge 用 Muse 在 Amazon 買到背心（c27），避免重述。
- 第 5 章的 `big`「Meta 說它會拒絕人做不到的事」沒有單獨做卡：Meta 的原句是 applies ethical browsing principles，沒有「拒絕」兩個字，併進 Meta 發言人的 `quote` 卡（mgg4）。
- 第 7 章的「交給代理之前先問三件事」表格只有兩欄（先問／現在查得到的答案），不是企劃寫的逐店欄位：五欄塞不下 1080p 的表格寬度。
- 「自己搜還比較快」與 Amazon 發言人「公開運作」兩張 `big` 卡改成 `shot`：插圖占比原本只有 48%，改完約 50%（以口語單位算；lint 的節奏檢查沒有警告）。
- 比喻只用一個：記者自己的「緊張又愛道歉的青少年去跑腿」（第 2 章），插圖裡的跑腿少年就是這個比喻；沃爾瑪新聞稿的「信用卡附卡」比喻沒進旁白、也沒上卡片。

## 我懷疑但沒動的事

（每一條後面的「查核第 1 輪」是獨立查核者的結論，見 `verify-1.md`。）

- The Verge 2026-10-22 的報導沒有寫明記者在紐約，只寫西岸零售商「wouldn't ship to New York」與 doesn't ship to my address；企劃與旁白說「紐約」是從這裡推的。查核第 1 輪：兩句合起來足以推出她的地址在紐約，保留；開場原本的「2026 年 10 月」報導沒寫，已拿掉。
- 記者是否真的把 Target 的床墊查詢與面霜查詢放在同一天：報導寫 blocked by Target 「despite being able to pull from the site just a few minutes prior」，開場「同一家店，一天三種結果」把三次嘗試講成相鄰的兩天，是企劃的寫法。查核第 1 輪：「一天三種結果」不成立（兩天、兩種結果），章名改「擋了又放，放了又擋」、qq3n 改「時開時關」、說明欄同步；rg97「幾分鐘後改問床墊」接在隔天那次之後，報導只說幾分鐘前還抓得到 Target 的資料，沒說是哪一次，保留並記為推論。
- 沃爾瑪新聞稿寫「MCP (model text protocol)」，TechCrunch 寫 model context protocol；旁白只說 MCP。查核第 1 輪：The Verge 與 TechCrunch 都寫 Model Context Protocol，新聞稿是筆誤；旁白只說 MCP，不用改。
- 第 5 章「門外想買的人，一件都拿不到」：報導寫 effectively blocking other shoppers from purchasing them；是否真有人在等，報導沒說。查核第 1 輪：記者寫了 other shoppers interested in these items，「門外想買的人」站得住；「一件都拿不到」補成「等於一件都拿不到」對應 effectively。
- 第 6 章「有沃爾瑪帳號就行」來自 TechCrunch，沃爾瑪新聞稿沒有這一句。查核第 1 輪：TechCrunch 原句「Agent support is available for anyone with a Walmart account; a Walmart+ membership is not necessary」，今天重開仍在；同一句後面的「Sam's Club 也一樣」改成「Sam's Club 也能用代理買」（見 c25）。
- Target 的門「時開時關」是否與 Target 自己的機器人檢查有關，報導只引發言人的一般說法，沒有針對記者的那兩次。查核第 1 輪：報導明寫「caught in Target's bot check」，所以是 Target 的機器人檢查；但發言人說的是 may depend，e7qb 改「可能就看那一次任務怎麼做」。
- 「Meta 的回應裡沒有」消費上限（cspx）：Meta 給 The Verge 的回應沒提上限，但 Muse 的產品頁沒查，不能說 Muse 沒有這項功能；卡片寫「Meta 的回應沒提」。查核第 1 輪：Meta 發言人的兩段原話確實沒提上限，寫法正確，保留。
- 關鍵影格 `account-check` 的 prompt 有「warehouse-club entrance next door」當 Sam's Club 的暗示，畫出來可能看不出來，不影響事實。查核第 1 輪：不是事實，不動。

## 進度

- [x] 骨架通過 schema
- [x] 第 1 章（hook … street-of-doors）
- [x] 第 2 章（ch2 … gate-question）
- [x] 第 3 章（ch3 … target-door-ajar）
- [x] 第 4 章（ch4 … open-door-bell）
- [x] 第 5 章（ch5 … superstore-far）
- [x] 第 6 章（ch6 … ny-again）
- [x] 第 7 章（ch7 … closing，含 cta 與 outro）
- [x] loops 表 11 條（4 條是開場預告）
- [x] 字典新增 13 個詞
- [x] lint 0 錯誤、2 警告（outro 單一狀態 19 秒是版型本身；開場 60 秒在估計邊緣）
- [x] shorts.json 兩支
- [x] 查核（另一個代理）：第 1 輪 2026-10-22 完成（`verify-1.md`，改了 15 處事實）；第 2 輪 2026-10-22 完成（`verify-2.md`，改了 1 處事實：zd4i「收據」→「價目單」），不需要第 3 輪
- [ ] 站主在 /admin/videos 選大綱、核准

## 說故事關卡之後的改動（2026-10-22，協調者）

- 第一輪盲評 66 分、十三題過六題；依意見改稿，事實、數字、名字與引文都沒動：開場預告句停在結果之前（3mw8、9hgx、rbf3）、片尾回答「為什麼」（dmat）、回收時點名（e7qb、vn6h、whrm）、重述的句子刪掉或改成新事實（jgeg、34qh、ntjj、6tme、84qy、p68i）、Amazon 的三個日期改照時間順序念（amazon-stats 的 reveal 與列順序：去年 11 月 → 7 月 → 今年 8 月）、第 4、7 章章名改成發生的事。
- 刪掉兩個岔出去的 shot：`bank-counter`（qrrn，JPMorgan 執行長，c12）與 `account-check`（8qub，不用 Walmart+、Sam's Club，c25）；刪掉 8e66（閘道先對企業和開發者開測試版）。c12、c25 與「測試版」那一條仍在上表，影片裡已不再講，說明欄若提到要一併看。
- 聽稿修正（第一輪，協調者）：超過 40 字的五句縮短、第 6 章「拿得到什麼」改「規矩是什麼」、第 7 章三件事改成問句。
- 第二輪盲評 74 分、過十題（剩 one_line、no_recap、no_detour）。第三輪改動：刪 `three-doors` 表（9mxy 背心那一句留在說明欄；nsdf 刪；jcf4「價格跟人一樣」改成新 shot `same-shelf-price`，c23）、刪 `handshake`（dgyj「零售商反應壓倒性正面」，c19 仍在上表）；9rar／uzsj／6kbe 綁回 Muse（「Muse 不是第一個」「九月，輪到 Muse 看到告示」，日期不變）；片尾 dmat 改成答案句（店家要代理公開、照規矩走），不再重述 Amazon 的三個理由；p68i 改成判斷準則；9963 改成點名回呼；xitp 改「問題在門，不在它」。
- 第三輪盲評 78 分、過十一題（剩 payoffs：p68i 謎語式回答；no_recap：34qh、6kbe 後半句、cspx）。第四輪改動：p68i 改成直接回答（Meta 說 Muse 會、沃爾瑪寫進設定）、刪 `turnstile-next-day`（34qh）、6kbe 拿掉「九月輪到 Muse」、cspx 只講 Meta 的回應沒有答案、e7qb 縮短。三輪盲評都記在工作區 `review/narrative.json`（規則是最多兩輪，第三輪是多做的）；之後交給站主在後台判。
- 旁白與成片品管之後（2026-10-23）：旁白第二次聽檢 73c8 又被兩個轉寫聽成「到齊」，改成「二十分鐘一到」；插圖兩輪後 5 張（boutique-tease、street-of-doors、receipts-return、second-runner、torn-ticket）用 `--accept-best` 保留最好的一張，成片關卡會標人工審看。第一次 qa 8／11：旁白未核准（站主）、pace（outro 19 秒）、policy（Jev 有示範 0.44）。修法：片尾答案拆成兩張 shot（answer-street：dmat；answer-table：nvep 新 id）、outro 只留留言題與訂閱句；第七章加 granola-apply／granola-verdict 兩張 shot（dsks、bix6），把三個問題套在穀物棒那一次（事實都來自 c4、c19、c24 既有主張，「下單我自己來」是站主做法）；4zg9 加一個問句補 90 秒內的鉤子。

## 紙底版（2026-10-23）

照 `brief.md`〈新規則版（2026-10-23）〉重寫成 `theme: "paper"` 的短片「一個概念」（三種門），沒有 `shot`；上一版 53 張插圖的腳本留在 `<VIDEO_WORKDIR>/ai-shopping-agents-blocked/_tools/v1-illustrated/video.json`。事實一條都沒有新增，每個場景的 `claims` 只引用上表既有的 c 編號；數字（20 分鐘、10 件、50／100／200 美元、去年 11 月、今年 7／8 月、12 美元）與上表相同。lint 估 8.3 分鐘、82 句、1822 口語單位、49 景 70 個狀態（68 個帶圖示、大數字、表格、步驟、對照或引文）。

每一章用到的 c 編號：

- 開場「AI 代理不是會幫我買了嗎？」（open … promise）：c13（10 月 21 日沃爾瑪）、c6（Amazon 關門，一個月前）、c1（記者派 Muse）、c4／c9／c27（動詞清單：搜商品、比價、放購物車、下單）、c5（少了一家店它不一定會講）、c21（承諾句的沃爾瑪上限）。
- 「它真的買得到嗎？」（target-door … rote-rule）：c1、c2、c3（Target 擋、過、擋）、c14（Target 的說法，只用「看那次任務怎麼做、網站有哪些防護」一句）、c16（比喻停點：擋的是所有自動程式）、c4（三家店）、c5（Muse 自己補的那句）、c7（西岸超市不送到紐約）、c8（自己搜大概還比較快；記者說真正用得上它的，可能是已經知道要買什麼、只差比價的任務）。
- 「Amazon 為什麼把門關上？」（sunday … still-blocked）：c6（星期天、彈窗原文、三個理由、要求移除、「公開運作」）、c10（Amazon 自己的代理）、c11（告 Perplexity、確認信、法官）。「現在還擋不擋」是照實說不確定，報導日之後沒有新消息。
- 「門開著會怎樣？」（realreal … tickets）：c9（20 分鐘、10 件、一整天、門外的人、記者自己停掉、永遠跑下去、跟別人的代理搶）、c17（12 美元只在卡片副標）、c18（技術長）、c19（Meta 發言人）。
- 「有沒有店家把規矩寫清楚？」（walmart … owner-rules）：c13、c20（Muse 與 ChatGPT、Gemini 並列，只在卡片副標）、c21（設定檔三步、預設核准、上限例子、上限內仍可能再核准、隨時可刪）、c22（Agent Gateway 用 MCP、先開測試版只在卡片副標）、c23（價格跟人一樣）、c24（條款）。
- 「那我要不要用？」（three-questions … closing）：c19、c5、c4、c21（三件事套在穀物棒那一趟）、c8（站主用法呼應記者的選法）、c2／c6／c13（答案卡）。

「我」的句子五句，來源：sx6e、xiq6、fezk、5i3t 來自 brief 的站主觀點；druk 是照實說不確定（Amazon 現在還擋不擋 Muse）。5i3t／owner-use 在第 3 輪之後由統籌改成 brief 站主觀點原話（只派它做已經知道要買什麼、只差比價和下單的任務，每一筆買之前要它先問我），是站主做法，不是報導。玩笑兩句：desu（按重新整理的那隻手）、fp4t（搶演唱會票的手速）。

門的編號照影片出現的順序：01 看情況（Target）、02 全擋（Amazon）、03 正門加規則（沃爾瑪）；brief 的列法是「全擋／看情況／正門加規則」，只是順序不同。

這一版沒有用到、仍留在上表的：c12（JPMorgan 執行長，上一版就已刪，岔路）、c15（Target 與 OpenAI、Google、Microsoft 的合作名單：不介紹別家代理，brief〈不做的事〉）、c25（不用 Walmart+、Sam's Club 也能用：上一版就已刪）、c26（古董洋裝與拍賣會：新規則版的最後一章改成行動清單，沒有位置）、c28（Muse 上市不到一個月：第 3 章開場那一個狀態已經 36 個口語單位，加了會超過 8 秒）。c11 的「7 月起確認信拿掉品名與圖片」只在表格那一列，旁白只說「確認信也拿掉了品名和圖片」，不唸月份（每章最多唸兩個數字）。c22 的「先對企業與開發者開測試版」只在卡片副標。

shorts.json 兩支重寫成沒有 `shot` 的字卡（`big`／headline），事實同上：第 1 支 c1、c2、c3、c4、c5、c13；第 2 支 c9、c17、c18、c19（只說「店家和 Meta 怎麼回應，完整的在長片」）。

字典沒有新增：這一版用到的拉丁詞（AI、Amazon、The Verge、Meta、Muse、Target、Sam's Club、Costco、Perplexity、The RealReal、Agent Gateway、MCP）在上一版就都在了。

lint 剩一個警告：outro 只有一句（訂閱句）。答案句與留言題各自放在它前面的 `big` 卡（answer、ask），每個狀態都在 8 秒以內，照 10-23 啟動訊息的做法。

## 查核第 3 輪（2026-10-23，紙底版，獨立查核者）

五個來源（The Verge 三篇、沃爾瑪新聞稿、TechCrunch）今天以編輯 UA 重開，全部 HTTP 200、無轉址、無更正註記；對照用的 67 句原文今天都還逐字在頁面上（`_tools/verify/round3/phrases.txt`），`sources` 這五筆的 `checked_on` 改 2026-10-23。改了五處事實的強度，全表見 `verify-3.md`：

- c14：wx69 與 door-01 卡片副標原寫「Target 說，看那次任務怎麼做」，發言人說的是 may depend（第 1 輪已因同一原因改過 e7qb），改「可能要看」，說明欄同步；「當時」拿掉（原文 what safeguards are in place）。
- c8：rote-rule 原寫「記者的選法是：……才交給它」，報導只說這類任務「is where an agent could be truly useful」，沒說她只交這種任務，改「記者說，最用得上它的是……的任務」，卡片 kicker／text／sub／key 同步。
- c9：why-not-block 卡片副標與 key 原寫「很快，你會跟別人的代理搶」，原文 may soon be competing，改「你可能得」。
- c21：door-03 的比喻句 8fej 與卡片副標補「預設」（Customers must approve agent purchases by default；第 1 輪改章名時的同一理由）。
- c21：Agent Profiles 是「launching in the next month」，片中行動清單 q3kh 原寫「像沃爾瑪，先設好再派它出門」，配上「你現在先做三件」聽起來今天就能設，改「像沃爾瑪即將推出的設定檔」，卡片 detail 同步。

另：c11 表格那一列「對方的代理也在站上買」出自 The Verge 2026-10-22（Amazon said the AI company had ignored its requests to stop its agent from shopping on the site），9-21 那篇只寫 Comet shopping experience；事實成立，c11 的出處補記 10-22 那篇。

## 查核第 4 輪（2026-10-23，獨立查核者，不是第 1–3 輪）

五個來源今天再以編輯 UA 重開，全部 HTTP 200、無轉址（`_tools/verify/round4/live/`）。第 3 輪改的五處裡四處成立（c14「可能要看」、c9「你可能得」、c21「預設」、c21「即將推出的設定檔」）；改了一處：

- c8：rote-rule 第 3 輪改成「記者說，最用得上它的是……」，原文是「A more rote task like … is where an agent could be truly useful」，沒有「最」，也有 could 的保留。n3fs 改「記者說，真正用得上它的，可能是：……的任務」，卡片 kicker 改「記者說它可能真正用得上的」、key 改「只差比價的任務，它可能真有用」，text／sub 不變。

統籌在第 3 輪後改寫的 5i3t、owner-use 卡、vaf7、dxbj、xiq6、2y4r 都對得上來源與 brief 站主觀點，第 3 輪報的 5i3t 意見不符已消失。全表見 `verify-4.md`。
- 紙底版旁白（2026-10-23）：第一次合成 8:05 正文，聽檢 8 句被標（她／它／他、記者→記著、搜→收、店→點、公告→公號、搶→吵、代理→戴莉）改措辭後重錄；qa 10／11（只剩旁白等站主；policy 這一版 Jev 過了）。行動清單卡因查核加長的步驟說明放不下，拿掉卡片標題、縮短說明。

