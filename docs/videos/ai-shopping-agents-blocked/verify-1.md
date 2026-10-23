# 查核第 1 輪：ai-shopping-agents-blocked

查核日 2026-10-22。獨立查核者（不是撰稿者）。七個來源今天都以 `Mokaair-editorial/1.0` UA 重新抓過，同一主機間隔至少 1 秒，全部 HTTP 200、沒有轉址；去掉 `<!-- -->` 後逐句比對。沒有用網路搜尋（0／5）。抽出的全部字串在 `<home>\mokaair-work\videos\ai-shopping-agents-blocked\_tools\verify\claims-list.tsv`（240 條），聽感檢查的輸出在同資料夾的 `listener.txt`，重抓的頁面在 `_tools\verify\live\`。

網址代號（「HTTP」欄是今天的狀態碼）：

- V1 = https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse （The Verge 2026-10-22，記者實測與各方回應的主要來源）200
- V2 = https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping （The Verge 2026-09-21，引 GeekWire）200
- V3 = https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents （The Verge 2026-10-21）200
- W = https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers （沃爾瑪官方新聞稿，頁面日期 Oct. 21, 2026）200
- TC = https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/ （TechCrunch 2026-10-21）200
- M1 = https://mokaair.com/zh-TW/life/ai-news-shopping-agents-blocked-20261022 200（自家文章，不當證據）
- M2 = https://mokaair.com/zh-TW/life/ai-news-walmart-agent-gateway-20261021 200（自家文章，不當證據）

Target、Amazon、Meta、The RealReal、JPMorgan 的說法沒有官方頁面，只能以 V1／V2 的引述為準；第 6 章以 W 為準，V3／TC 只補充。

## 逐條

| # | 主張 | 在哪裡 | 網址 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 標題：AI 代理會買東西了，店家為什麼關門？Muse 被 Amazon 擋下的那一天 | youtube.title | V1, V2 | 200 | CONFIRMED（V2：popup started appearing on Sunday） | |
| 2 | 說明欄：Amazon 全擋、Target 時開時關、沃爾瑪替代理開了一扇有規則的門 | youtube.description | V1, V2, W | 200 | CONFIRMED | |
| 3 | 說明欄：跟著 Muse「看它在每一家店門口碰到什麼」 | youtube.description | V1 | 200 | CHANGED：記者沒有用 Muse 試過沃爾瑪（Agent Profiles 下個月才推出） | 每一家店門口 → 店門口 |
| 4 | 說明欄：片中每一次嘗試都是 V1 記者自己做的 | youtube.description | V1, V2 | 200 | CHANGED：背心那次是 V2（9 月測試），不是 V1 記者 | 片中每一次嘗試 → 片中記者的每一次嘗試；Amazon 那句補「以及封鎖前 The Verge 用 Muse 在 Amazon 買到背心」來自 V2 |
| 5 | 說明欄：Target 的機器人檢查一天三種結果 | youtube.description | V1 | 200 | CHANGED：見 #12 | 一天三種結果 → 擋了又放、放了又擋 |
| 6 | 說明欄：The Verge 與 TechCrunch 同日的報導只補充不用付費會員、Sam's Club 也適用 | youtube.description | W, V3, TC | 200 | CHANGED：「不需要 Walmart+」只有 TC 寫；Sam's Club 在 W 本身就有，不是補充 | → TechCrunch 同日的報導補充不需要 Walmart+ 付費會員 |
| 7 | 說明欄：Agent Profiles「一個月內推出」，Agent Gateway 先對企業與開發者開測試版 | youtube.description | W | 200 | CONFIRMED（launching in the next month；We'll begin with a beta for companies and developers） | |
| 8 | 說明欄：彈窗與三個理由來自 V2（引 GeekWire）；條款來自沃爾瑪 10-21 新聞稿 | youtube.description | V2, W | 200 | CONFIRMED | |
| 9 | tags（Muse、Meta Muse、Agent Gateway、Target、The Verge 等） | youtube.tags | V1, W | 200 | CONFIRMED | |
| 10 | 縮圖：被擋在門外；Amazon 全擋、Target 看情況、沃爾瑪開門 | thumbnail | V1, V2, W | 200 | CONFIRMED | |
| 11 | 標題卡：The Verge 報導 2026-10-22・Meta 的 Muse 代理 | hook.data.subtitle | V1 | 200 | CONFIRMED（Oct 22, 2026, 12:30 PM UTC） | |
| 12 | 第 1 章章名「同一家店，一天三種結果」 | hook.chapter | V1 | 200 | CHANGED：報導是兩天三次嘗試、兩種結果（擋／過／擋），不是一天三種 | → 同一家店，擋了又放，放了又擋（loops rg97 的 what 同步） |
| 13 | 2026 年 10 月，紐約，記者請 Muse 找一罐面霜 | f7mi | V1 | 200 | NOT FOUND（日期）：報導沒寫實測日期，只知在 Muse 9 月上市後、10-22 刊出前；紐約可由「wouldn't ship to New York」＋「doesn't ship to my address」推出，保留 | 2026 年 10 月，紐約，記者請… → 在紐約，一位記者請… |
| 14 | AI 代理是自己上網替你操作的 AI | ha3t | — | — | OUT OF SCOPE（定義） | |
| 15 | 它打開 Target 網站，被機器人檢查擋在門口 | pt4q | V1 | 200 | CONFIRMED（caught in Target's bot check one day） | |
| 16 | 那一關分辨人或程式 | 6tzk | — | — | OUT OF SCOPE（解釋 bot check） | |
| 17 | 隔天同一個指令，進去了 | ji24 | V1 | 200 | CONFIRMED（able to get through the next） | |
| 18 | 幾分鐘後改問床墊，又被擋 | rg97 | V1 | 200 | CONFIRMED（推論：報導說幾分鐘前還抓得到 Target，沒說是哪一次） | |
| 19 | 你以為它太笨／其實是店家不讓它進門（卡片同） | gu8c, xitp, too-dumb.data | V1 | 200 | CONFIRMED（整體框架） | |
| 20 | 它去比價，回來少一家店 | 3mw8 | V1 | 200 | CONFIRMED | |
| 21 | 九月一個星期天，Amazon 對 Muse 跳出一行字 | sxv9 | V2 | 200 | CONFIRMED（V2 刊於 2026-09-21 週一，on Sunday＝9-20） | |
| 22 | 它在二手精品網站做一件允許的事，做了一整天 | 9hgx | V1 | 200 | CONFIRMED（technically allowed；all day） | |
| 23 | 同一週，沃爾瑪替代理開另一扇門 | rbf3 | W, V1 | 200 | CHANGED：接在九月的 Amazon 與日期不明的 The RealReal 之後，「同一週」沒有根據；W 是 10-21 | 同一週 → 十月 |
| 24 | AI 代理會買東西了，店家為什麼反而把門關上？ | yr8y | — | — | OUT OF SCOPE（問句） | |
| 25 | 第 2 章章名與卡：比出來的最低價，少了一家店 | ch2 | V1 | 200 | CONFIRMED | |
| 26 | 記者接著派它找穀物棒每一片的最低價 | kczi | V1 | 200 | CONFIRMED（best per-piece granola bar price） | |
| 27 | 它回來，手上三張收據：Sam's Club、沃爾瑪、Costco | zd4i | V1 | 200 | CONFIRMED（offered options from Sam's Club, Walmart, and Costco；「收據」是插圖比喻，見最後的懷疑） | |
| 28 | Muse 自己補一句：Amazon 可能更便宜，但被完全封鎖，沒辦法確認（卡片英文為記者轉述） | gyp6, qexa, muse-caveat.data | V1 | 200 | CONFIRMED（卡片 source 標「記者轉述」正確） | |
| 29 | 清單裡還有一家西岸的超市，根本不送到紐約 | ztjr | V1 | 200 | CONFIRMED（推論：grocery chain that doesn't ship to my address 與 West Coast-based retailer wouldn't ship to New York 合成一家，報導沒說是同一家） | |
| 30 | 等回覆、要它多搜幾家、再澄清送貨範圍 | q7u5 | V1 | 200 | CONFIRMED | |
| 31 | 記者算下來，自己搜還比較快 | 3wra | V1 | 200 | CHANGED：原文 it likely would have been faster | → 記者算下來，自己搜大概還比較快 |
| 32 | 像派一個緊張又愛道歉的青少年去跑腿 | 5wst | V1 | 200 | CONFIRMED（anxious and apologetic teenager out to the store） | |
| 33 | 要交代一大堆，回來的東西又不完全是你要的 | eyiz | V1 | 200 | CONFIRMED（inordinate amount of instructions；not exactly what you asked for） | |
| 34 | 她也說，最適合交給代理的是只差找最低價的任務 | u67x | V1 | 200 | CONFIRMED（is where an agent could be truly useful；「最適合」略強，見懷疑） | |
| 35 | 我的看法是，最大的問題是它看得到的店不完整 | d6z5 | brief | — | OPINION，與站主觀點一致 | |
| 36 | Amazon 為什麼把它擋在外面？ | vdsh | — | — | OUT OF SCOPE（問句） | |
| 37 | 第 3 章卡副標 The Verge 2026-09-21 | ch3.data.subtitle | V2 | 200 | CONFIRMED（Sep 21, 2026） | |
| 38 | 那時 Muse 上市還不到一個月 | pt7h | V2 | 200 | CONFIRMED（9-21 稿寫 launched Muse earlier this month） | |
| 39 | Muse 的使用者打開 Amazon，看到一張告示 | h962 | V2 | 200 | CONFIRMED（popup message … for Muse users） | |
| 40 | 彈窗原文與譯文 | 5xny, u9it, popup-quote.data | V2 | 200 | CONFIRMED（逐字相符） | |
| 41 | 三個理由：Meta 沒事先通知；不表明自己是代理；看起來會抓顧客登入資料（卡片同，引 GeekWire） | zfjh, waad, 4vgw, three-reasons.data | V2 | 200 | CONFIRMED（didn't notify Amazon；failing to identify itself；seemingly capturing customer credentials） | |
| 42 | Amazon 要求 Meta 把 Amazon 從 Muse 拿掉 | bb47 | V1 | 200 | CONFIRMED（Amazon spokesperson confirmed … requested that Meta remove Amazon） | |
| 43 | 發言人說，替顧客去別家買的程式應公開運作、尊重店家要不要參與 | mj26 | V1, V2 | 200 | CONFIRMED（should operate openly and respect service provider decisions about whether or not to participate） | |
| 44 | Amazon 自己平台裡就有代理：盯價格、自動補貨、照你設的規則下單 | dx7y, 9xu3 | V1 | 200 | CONFIRMED（monitors prices, automatically reorders items, and purchases products based on rules set by human users） | |
| 45 | 去年 11 月告了 Perplexity；對方的代理也在站上買 | 9rar, amazon-stats.data[0] | V2, V1 | 200 | CONFIRMED（sued Perplexity in November last year；ignored its requests to stop its agent from shopping on the site） | |
| 46 | 今年 8 月法官站在 Perplexity 那邊 | 6kbe, amazon-stats.data[1] | V2 | 200 | CONFIRMED（a judge siding with Perplexity on the case in August） | |
| 47 | 7 月起確認信拿掉品名與圖片，不讓外面的 AI 讀 | uzsj, amazon-stats.data[2] | V2 | 200 | CONFIRMED（since July … item names and product images being omitted … mined by external AI services） | |
| 48 | JPMorgan 執行長：外面的代理碰帳戶太冒險 | qrrn | V1 | 200 | CONFIRMED（wouldn't allow outside agents to access accounts … too risky） | |
| 49 | 我的看法是，Amazon 的理由站得住，但它自己也在做代理；這是生意的攻防 | 4atb, ivq8 | brief | — | OPINION，與站主觀點一致 | |
| 50 | Amazon 的門鎖死了；那門沒鎖的店呢？ | tw6g | — | — | OUT OF SCOPE（轉場問句） | |
| 51 | 開頭那扇一天三種結果的門 | qq3n | V1 | 200 | CHANGED：見 #12 | 一天三種結果的門 → 時開時關的門 |
| 52 | Target 發言人：看任務怎麼做、網站有哪些防護 | sjh8, target-answer.data | V1 | 200 | CONFIRMED（may depend on how it went about the task and what safeguards are in place） | |
| 53 | 可能進得了一部分、進不了另一部分，為了保護顧客資料和購物體驗 | 5s29 | V1 | 200 | CONFIRMED | |
| 54 | 有防護擋沒授權的代理動帳號、發起交易 | sjn7 | V1 | 200 | CONFIRMED | |
| 55 | 所以它找面霜進得去、找床墊被擋，看的是那一次任務怎麼做 | e7qb | V1 | 200 | CHANGED：發言人說 may depend，旁白講成定論 | 看的是 → 可能就看 |
| 56 | Target 跟 OpenAI、Google、Microsoft 都有購物合作；名單裡沒有 Muse（卡片同） | f325, 5jiv, partners.data | V1 | 200 | CONFIRMED | |
| 57 | 更多時候，擋住代理的是網站本來就有的防機器人系統 | 8uyh | V1 | 200 | CHANGED：原文 can also get caught，沒有比較頻率 | 更多時候 → 有時候 |
| 58 | 沒有明文封鎖的店，代理也會今天進得去、明天進不去 | 34qh | V1 | 200 | CONFIRMED（existing firewalls can make agents inconsistent） | |
| 59 | 第 5 章章名與卡：購物車每 20 分鐘重填一次，填了一整天 | ch5 | V1 | 200 | CONFIRMED | |
| 60 | The RealReal 是二手精品網站 | vn6h | V1 | 200 | CONFIRMED（secondhand luxury fashion retailer） | |
| 61 | 每月 12 美元搶先看新品 | fwtf, realreal-rules.data[0] | V1 | 200 | CONFIRMED（$12-per-month subscription … early access；The RealReal 官網未查，卡片標「記者的說法」） | |
| 62 | 放進購物車保留 20 分鐘，別人拿不到 | ryff, realreal-rules.data[1] | V1 | 200 | CONFIRMED（reserves it for you for 20 minutes, making it impossible for other people to swipe it） | |
| 63 | 要 Muse 把喜歡的品牌最新上架的十件一次全放進購物車 | smvt, realreal-rules.data[2] | V1 | 200 | CONFIRMED（bulk-add all 10 of the newest listings from a favorite brand） | |
| 64 | 她根本不打算買；每 20 分鐘到期就再放一次；一整天 | 3bjz, 73c8, ymzn | V1 | 200 | CONFIRMED | |
| 65 | 門外想買的人，一件都拿不到 | 45au | V1 | 200 | CHANGED：原文 effectively blocking other shoppers | → 門外想買的人，等於一件都拿不到 |
| 66 | 最後是記者自己把任務停掉 | zfzc | V1 | 200 | CONFIRMED（I eventually ended the task） | |
| 67 | 如果她沒那麼老實，可以讓規則允許的占位系統永遠跑下去 | 38eh | V1 | 200 | CONFIRMED | |
| 68 | 她擔心很快也會跟別人的代理搶 | 6w3p | V1 | 200 | CONFIRMED（may soon be competing with someone else's agent） | |
| 69 | The RealReal 技術長的話（引文、譯文、旁白） | wuyy, nw45, realreal-quote.data | V1 | 200 | CONFIRMED（逐字相符；「回答」的框架見懷疑） | |
| 70 | 重填一整天的購物車是規則允許的事 | jgeg | V1 | 200 | CONFIRMED（technically allowed） | |
| 71 | Meta 發言人：隨時可接手、一律買前先問 | zk72 | V1 | 200 | CONFIRMED | |
| 72 | 碰到人做不到的事，像買光一場活動的票，它會用它的瀏覽原則處理 | mgg4 | V1 | 200 | CONFIRMED（旁白沒說「拒絕」，正確） | |
| 73 | meta-quote 卡譯文「它會套用它的瀏覽原則」 | meta-quote.data.translation | V1 | 200 | CHANGED：譯文漏了 ethical | → 它會套用合乎倫理的瀏覽原則 |
| 74 | Meta 說零售商的反應壓倒性地正面 | dgyj | V1 | 200 | CONFIRMED（overwhelmingly positive） | |
| 75 | 第 6 章章名「沃爾瑪替代理開了正門，但每一筆都要你點頭」（卡片同） | ch6.chapter, ch6.data.title | W | 200 | CHANGED：預設每筆核准，也可設上限自動買 | 每一筆都要你點頭 → 每一筆預設要你點頭 |
| 76 | 卡副標：沃爾瑪新聞稿 2026-10-21 | ch6.data.subtitle | W | 200 | CONFIRMED（Oct. 21, 2026） | |
| 77 | 十月二十一日沃爾瑪宣布代理可以替顧客買，但要照它的規矩 | whrm | W, TC | 200 | CONFIRMED | |
| 78 | 新聞稿把 Muse 列在已接上的應用程式，跟 ChatGPT、Gemini 並排 | yfj5 | W | 200 | CONFIRMED（conversational commerce integrations with Muse, ChatGPT, Gemini and others） | |
| 79 | Muse 第一次經過它的閘道，沃爾瑪就替它建設定檔 | kg8h, agent-profiles.data.steps[0] | W | 200 | CHANGED：W 寫的是任何代理第一次經過 Gateway 時自動建立；沒有來源說 Muse 會走 Gateway | Muse 第一次經過 → 代理第一次經過（卡片原本就沒寫 Muse） |
| 80 | 登入沃爾瑪帳號把設定檔連上去，只有沃爾瑪看得到 | 4k85, agent-profiles.data.steps[1] | W | 200 | CONFIRMED（Only Walmart sees this） | |
| 81 | 預設每一筆要你點頭，或在你設的上限內自動買 | xfqq, agent-profiles.data.steps[2] | W, V3 | 200 | CONFIRMED（must approve agent purchases by default） | |
| 82 | 上限例子 50、100、200 美元 | 78gd, limits.data | W | 200 | CONFIRMED（for example, $50, $100 or $200；V3 只舉 up to $100） | |
| 83 | 閘道叫 Agent Gateway，用 MCP 連線 | n59q | W, V3, TC | 200 | CONFIRMED（W 寫成 model text protocol，V3／TC 寫 Model Context Protocol；旁白只說 MCP） | |
| 84 | 現在先對企業和開發者開測試版 | 8e66 | W, V3 | 200 | CHANGED：官方是未來式 We'll begin with a beta（V3 寫 currently available in beta，以官方為準） | 現在先 → 它會先 |
| 85 | MCP 是讓代理直接跟網站系統對話的通用接口，不用一頁一頁點 | t2px | W, TC | 200 | CONFIRMED（白話解釋；W：faster, more reliable way than a web browser） | |
| 86 | 替代理找出你常買的，像酸種麵包和牛奶，卻不交出購物紀錄 | vewr | W | 200 | CONFIRMED（sourdough bread or a particular brand of milk … without sharing the customer's broader shopping history） | |
| 87 | 表格第三欄標題「Muse 碰到的」 | three-doors.data.columns[2] | W | 200 | CHANGED：沃爾瑪那一列是還沒上線的規則，Muse 沒碰過 | → 代理會碰到的 |
| 88 | Amazon：全擋；彈窗加條款，要求 Meta 移除 | three-doors.data.rows[0] | V1, V2 | 200 | CONFIRMED | |
| 89 | Target：看情況；機器人檢查，時開時關 | three-doors.data.rows[1] | V1 | 200 | CONFIRMED | |
| 90 | 沃爾瑪：正門加規則；預設每筆要本人核准，價格跟人一樣 | three-doors.data.rows[2] | W | 200 | CONFIRMED | |
| 91 | 封鎖前 The Verge 用 Muse 在 Amazon 買到過背心 | 9mxy | V2 | 200 | CONFIRMED（successfully purchase tank tops from Amazon） | |
| 92 | 代理看到的價格跟人看到的一樣 | jcf4 | W | 200 | CONFIRMED | |
| 93 | 條款：不能超出意圖；拿不到付款卡、不能新增或改付款方式；只拿需要且允許的資料；買錯退貨照退；犯規就封（卡片五條同） | wnnu, hde2, 7tpu, pqye, e5qx, agent-terms.data | W | 200 | CONFIRMED（五條逐條相符） | |
| 94 | 不用付費會員，有沃爾瑪帳號就行，Sam's Club 也一樣 | 8qub | TC, W | 200 | CHANGED：「不需要 Walmart+」只有 TC 寫，確認；但「Sam's Club 也一樣」聽起來是 Sam's Club 也不用會員，沒有來源（Sam's Club 本身是會員制）；來源只說 Sam's Club 也支援代理購物 | Sam's Club 也一樣 → ；Sam's Club 也能用代理買 |
| 95 | 設定檔一個月內推出，隨時可以刪掉 | 7e7h | W | 200 | CONFIRMED（launching in the next month；Delete an Agent Profile at any time） | |
| 96 | 我的看法是，先把規則寫清楚、每筆預設本人核准，比直接封鎖或完全放任都好 | 84qy, k8hh | brief | — | OPINION，與站主觀點一致 | |
| 97 | 記者最後派 Muse 去找一件東西；她找了很久的古董洋裝 | ikjq, 2ara | V1 | 200 | CONFIRMED（a vintage dress I've been hunting for） | |
| 98 | 第 7 章章名與卡：錢包要不要交給它 | ch7 | — | — | OUT OF SCOPE | |
| 99 | 照片、年份、關鍵字、該去哪些二手平台，全交給 Muse | ebxr | V1 | 200 | CONFIRMED（另有 notes about similar items，旁白省略不算錯） | |
| 100 | 哪裡都沒找到那件洋裝，但同品牌有一場拍賣會要開 | 4zg9, ts67 | V1 | 200 | CONFIRMED（could not find the dress for sale anywhere … upcoming auction of items from the same brand） | |
| 101 | 有時間和耐心帶它，它能把難找的東西找得更深 | 8nq6 | V1 | 200 | CONFIRMED | |
| 102 | 交出錢包前我會先問三件事 | ft39 | brief | — | OPINION，與站主觀點一致 | |
| 103 | 第一：Muse 說一律會先問，沃爾瑪預設每筆要核准 | p68i, three-questions.data.rows[0] | V1, W | 200 | CHANGED：說這句的是 Meta 發言人（卡片寫「Muse：一律先問」是產品描述，保留） | Muse 說一律會 → Meta 說一律會 |
| 104 | 第二：沃爾瑪給得出上限（50、100、200 美元），Meta 的回應裡沒有 | cspx, three-questions.data.rows[1] | W, V1 | 200 | CONFIRMED（Meta 兩段引言沒提上限） | |
| 105 | 第三：Amazon 完全進不去、Target 看情況；少了 Amazon 比價就不完整，代理不一定會主動講 | ntjj, three-questions.data.rows[2] | V1 | 200 | CONFIRMED（Sometimes, the agents will say as much）；後半是站主觀點 | |
| 106 | 我只派它做已知要買什麼、只差比價和下單的任務；店家有給設定的一定先設好 | 9963, 6tme | brief | — | OPINION，與站主觀點一致 | |
| 107 | 記者每一次嘗試的細節與條款整理在說明欄的文章裡 | wvu2, article-cta.data | M1, M2 | 200 | CONFIRMED（兩篇文章都在 sources，今天 200） | |
| 108 | 片尾：Amazon 關、Target 看情況、沃爾瑪下個月開，每筆預設要你核准 | dmat, closing.data | V3, W, TC | 200 | CONFIRMED（V3 Next month；W launching in the next month；TC rolling out next month） | |
| 109 | 你最想交給 AI 代理買的一樣東西是什麼？／訂閱頻道 | byrv, pa5b | — | — | OUT OF SCOPE | |

## 摘要

- 查了幾條：109 條（涵蓋 240 個字串中所有帶事實的部分），CONFIRMED 78、CHANGED 18 列（合為 15 處修改）、NOT FOUND 1（#13 f7mi 的「2026 年 10 月」，已拿掉）、OPINION 5、OUT OF SCOPE 7。
- 改了的 15 處：f7mi 拿掉日期；第 1 章章名＋qq3n＋loops＋說明欄的「一天三種結果」；e7qb 補「可能」；8uyh「更多時候」→「有時候」；3wra 補「大概」；45au 補「等於」；rbf3「同一週」→「十月」；kg8h「Muse」→「代理」；8e66「現在先」→「它會先」；8qub 的 Sam's Club；第 6 章章名與卡片補「預設」；p68i「Muse 說」→「Meta 說」；meta-quote 譯文補回 ethical；three-doors 第三欄標題；說明欄的來源歸屬（背心出自 V2、Walmart+ 只有 TC、「每一家店門口」）。沒有任何數字被改（12 美元、20 分鐘、10 件、50／100／200 美元都對）。
- 會過期的事實：「去年 11 月」「今年 8 月」（Amazon 告 Perplexity、法官判決；V2 2026-09-21）在 2027-01-01 後變錯；「沃爾瑪下個月開」「設定檔一個月內推出」（W 2026-10-21 launching in the next month）約 2026-11-21 後過期；Agent Gateway「會先開測試版」（W 2026-10-21）隨上線改變；Amazon 封鎖 Muse 的現況（V2 2026-09-21，V1 2026-10-22 仍稱 hard-blocked）。
- 站主觀點不符：無。d6z5、4atb／ivq8、84qy／k8hh、ft39、9963、6tme、ntjj 後半都與 brief 的站主觀點一致；但 brief 註明這段是提案、站主還沒確認。ft39／9963／6tme 用「我」但沒有「我的看法是」開頭，屬於三件事那一串的延續，報告不改。
- 聽感：超過 40 字的句子剩 5 句（f325 43、wuyy 42、yfj5 44、kg8h 41、9mxy 43；f7mi 原 42 已因拿掉日期縮短）；沒有「經查證」「根據官方文件」「本影片」；旁白沒有括號或網址；Latin 詞（Sam's Club、The RealReal、The Verge、Agent Profiles、Agent Gateway 等）的每個字都在字典裡；揭曉順序沒看到先於介紹句的情形。
- lint：`node tools/video/cli.mjs lint --slug ai-shopping-agents-blocked` → 0 errors, 1 warning（closing 單一畫面約 19 秒，是撰稿時就有的版型警告）。沒有任何行有 `say`，所以沒有 `say_for` 要更新。
- 懷疑但沒改：(1) wuyy「The RealReal 的技術長回答」接在「那店家，會擋這種事嗎？」之後，聽起來像技術長針對霸占購物車作答，實際是給 The Verge 的一般說法，屬結構／揭曉，留給站主；(2) zd4i「三張收據」是插圖比喻，Muse 只是列出選項、沒有買，聽者可能誤會成已購買；(3) u67x「最適合交給代理的」比原文 could be truly useful 稍強；(4) ztjr 把「不送到我地址的連鎖超市」與「不送到紐約的西岸零售商」合成一家，報導沒明說是同一家；(5) rg97「幾分鐘後」接在隔天成功那次之後，報導只說幾分鐘前還抓得到 Target，沒說是哪一次；(6) shorts.json 不在可改範圍，但第 1 支的「隔天同一個指令…幾分鐘後改問床墊」沿用同一推論，第 2 支「門外的人一件都拿不到」沒有「等於」，請撰稿者同步。
- 需要第二輪：是（本輪改了 15 處事實，多於 3 處）。
