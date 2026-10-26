# 查核第 2 輪：ai-shopping-agents-blocked

查核日 2026-10-22。第 2 輪是另一個獨立查核者（不是撰稿者，也不是第 1 輪）。範圍：第 1 輪改過的 18 列與 NOT FOUND 的 1 列全部重查，第 1 輪 CONFIRMED 的 78 列隨機抽三分之一（26 列，抽樣腳本 `_tools/verify/round2/sample.mjs`，結果 `sample.txt`），另外把第 1 輪留下的五個懷疑（#18、#27、#29、#34、#69）全部重判。共重查 49 列。

七個網址今天都以 `Mokaair-editorial/1.0` UA 重新抓過（同一主機間隔至少 1 秒），全部 HTTP 200、0 次轉址；去掉 `<!-- -->`、script、style 後逐句比對（`_tools/verify/round2/totext.mjs`，抓下來的頁面在 `_tools/verify/round2/live/`）。沒有用網路搜尋（0／5）。代號沿用第 1 輪：

- V1 = https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse （頁面時間 Oct 22, 2026, 12:30 PM UTC）
- V2 = https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping （Sep 21, 2026, 9:21 AM UTC，引 GeekWire）
- V3 = https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents （Oct 21, 2026, 7:30 PM UTC）
- W = https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers （沃爾瑪官方新聞稿，Oct. 21, 2026；第 6 章的官方來源）
- TC = https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/ （October 21, 2026）
- M1 = https://mokaair.com/zh-TW/life/ai-news-shopping-agents-blocked-20261022 （自家文章，不當證據）
- M2 = https://mokaair.com/zh-TW/life/ai-news-walmart-agent-gateway-20261021 （自家文章，不當證據）

## 逐條

「#」是第 1 輪 `verify-1.md` 的列號；「來由」：R1 改＝第 1 輪改過、R1 NF＝第 1 輪查無、抽樣＝隨機抽到的 CONFIRMED、懷疑＝第 1 輪留下的懷疑。

| # | 來由 | 主張（現在的寫法） | 在哪裡 | 網址 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|---|
| 2 | 抽樣 | 說明欄：Amazon 全擋、Target 時開時關、沃爾瑪替代理開了一扇有規則的門 | youtube.description | V1, V2, W | 200 | CONFIRMED（V1 hard-blocked；caught in Target's bot check one day…；W terms for AI agents） | |
| 3 | R1 改 | 說明欄：看它在店門口碰到什麼 | youtube.description | V1 | 200 | CONFIRMED（記者沒有用 Muse 試沃爾瑪，「店門口」不再暗示每一家） | |
| 4 | R1 改 | 說明欄：片中記者的每一次嘗試都是 V1 記者自己做的；背心出自 V2 | youtube.description | V1, V2 | 200 | CONFIRMED（V2：We used it during testing to successfully purchase tank tops from Amazon） | |
| 5 | R1 改 | 說明欄：Target 的機器人檢查擋了又放、放了又擋 | youtube.description | V1 | 200 | CONFIRMED（caught … one day but was able to get through the next；mattress … once again blocked） | |
| 6 | R1 改 | 說明欄：TechCrunch 同日的報導補充不需要 Walmart+ 付費會員 | youtube.description | TC, W, V3 | 200 | CONFIRMED（TC：a Walmart+ membership is not necessary；W、V3 都沒有這句） | |
| 9 | 抽樣 | tags | youtube.tags | V1, W | 200 | CONFIRMED | |
| 10 | 抽樣 | 縮圖：被擋在門外；Amazon 全擋、Target 看情況、沃爾瑪開門 | thumbnail | V1, V2, W | 200 | CONFIRMED | |
| 12 | R1 改 | 第 1 章章名「同一家店，擋了又放，放了又擋」（loops rg97 同） | hook.chapter, loops | V1 | 200 | CONFIRMED（擋／過／擋三次，兩天以上） | |
| 13 | R1 NF | 在紐約，一位記者請 Meta 的 AI 代理 Muse 找一罐面霜 | f7mi | V1 | 200 | CONFIRMED（日期已拿掉；face moisturizer；紐約由 wouldn't ship to New York＋doesn't ship to my address 推出，推論合理） | |
| 18 | 懷疑 | 幾分鐘後改問床墊，又被擋 | rg97 | V1 | 200 | CONFIRMED（推論，見下方懷疑判定 4） | |
| 19 | 抽樣 | 你以為它太笨／其實是店家不讓它進門 | gu8c, xitp, too-dumb.data | V1 | 200 | CONFIRMED（AI agents are getting blocked left and right） | |
| 22 | 抽樣 | 它在二手精品網站做一件允許的事，做了一整天 | 9hgx | V1 | 200 | CONFIRMED（technically allowed reserve system；all day） | |
| 23 | R1 改 | 十月，沃爾瑪替代理開另一扇門 | rbf3 | W | 200 | CONFIRMED（Oct. 21, 2026） | |
| 25 | 抽樣 | 第 2 章章名與卡：比出來的最低價，少了一家店 | ch2 | V1 | 200 | CONFIRMED（Amazon might have had the lowest-priced option… couldn't confirm） | |
| 27 | 抽樣＋懷疑 | 它回來了，手上三張收據：Sam's Club、沃爾瑪、Costco | zd4i | V1 | 200 | CHANGED：「收據」是付過錢才有的東西；報導寫 it offered options from Sam's Club, Walmart, and Costco，Muse 沒有替她買（Meta 也說 Muse 買之前一律先問）。聽者會以為代理已經下單。改成同樣是紙片、但不代表付款的「價目單」，插圖不用重畫 | 手上三張收據 → 手上三張價目單 |
| 28 | 抽樣 | Muse 自己補一句：Amazon 可能更便宜，但被完全封鎖，沒辦法確認（卡片原文與譯文、source「記者轉述」） | gyp6, qexa, muse-caveat.data | V1 | 200 | CONFIRMED（逐字相符；英文句是記者轉述，卡片標示正確） | |
| 29 | 懷疑 | 清單裡還有一家西岸的超市，根本不送到紐約 | ztjr | V1 | 200 | CONFIRMED（推論，見下方懷疑判定 3） | |
| 31 | R1 改 | 記者算下來，自己搜大概還比較快 | 3wra | V1 | 200 | CONFIRMED（it likely would have been faster to search myself） | |
| 34 | 懷疑 | 她也說，最適合交給代理的，是只差找最低價的那種任務 | u67x | V1 | 200 | CONFIRMED（見下方懷疑判定 2） | |
| 38 | 抽樣 | 那時 Muse 上市還不到一個月 | pt7h | V2 | 200 | CONFIRMED（9-21 稿：When Meta launched Muse earlier this month；彈窗 9-20） | |
| 41 | 抽樣 | 三個理由：沒事先通知；不表明自己是代理；看起來會抓顧客登入資料（卡片同） | zfjh, waad, 4vgw, three-reasons.data | V2 | 200 | CONFIRMED（didn't notify Amazon；failing to identify itself when it browses；seemingly capturing customer credentials；引 GeekWire，卡片已標） | |
| 51 | R1 改 | 開頭那扇時開時關的門 | qq3n | V1 | 200 | CONFIRMED | |
| 53 | 抽樣 | 可能進得了一部分、進不了另一部分，為了保護顧客資料和購物體驗 | 5s29, target-answer.data.items[1] | V1 | 200 | CONFIRMED（Agents may be able to access one part of the site but not another, as a way to protect customer data and the shopping experience） | |
| 55 | R1 改 | 所以它找面霜進得去，找床墊被擋，可能就看那一次任務怎麼做 | e7qb | V1 | 200 | CONFIRMED（發言人 may depend on how it went about the task；「可能」對應 may） | |
| 57 | R1 改 | 有時候，擋住代理的不是誰的決定，是網站本來就有的防機器人系統 | 8uyh | V1 | 200 | CONFIRMED（AI agents can also get caught in the web of general bot blocking systems） | |
| 58 | 抽樣 | 沒有明文封鎖的店，代理也會今天進得去、明天進不去 | 34qh | V1 | 200 | CONFIRMED（even if a site doesn't have a blanket ban, existing firewalls can make agents inconsistent） | |
| 60 | 抽樣 | The RealReal 是二手精品網站 | vn6h | V1 | 200 | CONFIRMED（a secondhand luxury fashion retailer） | |
| 65 | R1 改 | 門外想買的人，等於一件都拿不到 | 45au | V1 | 200 | CONFIRMED（effectively blocking other shoppers from purchasing them） | |
| 69 | 懷疑 | The RealReal 的技術長回答：對第三方代理保持開放……（引文、譯文） | wuyy, nw45, realreal-quote.data | V1 | 200 | CONFIRMED（逐字相符；「回答」的框架見下方懷疑判定 5） | |
| 73 | R1 改 | meta-quote 卡譯文「它會套用合乎倫理的瀏覽原則」 | meta-quote.data.translation | V1 | 200 | CONFIRMED（applies ethical browsing principles） | |
| 75 | R1 改 | 第 6 章章名與卡「每一筆預設要你點頭」 | ch6.chapter, ch6.data.title | W | 200 | CONFIRMED（Customers must approve agent purchases by default；也可設上限） | |
| 77 | 抽樣 | 十月二十一日沃爾瑪宣布代理可以替顧客買，但要照它的規矩 | whrm | W, TC | 200 | CONFIRMED（W 頁面日期 Oct. 21, 2026；TC announced on Wednesday＝10-21） | |
| 78 | 抽樣 | 新聞稿把 Muse 列在已接上的應用程式，跟 ChatGPT、Gemini 並排 | yfj5 | W | 200 | CONFIRMED（conversational commerce integrations with Muse, ChatGPT, Gemini and others） | |
| 79 | R1 改 | 代理第一次經過它的閘道，沃爾瑪就替它建一個設定檔 | kg8h, agent-profiles.data.steps[0] | W | 200 | CONFIRMED（The first time you use an agent to shop through the Walmart Agent Gateway, Walmart will automatically create an Agent Profile for that agent） | |
| 80 | 抽樣 | 登入沃爾瑪帳號把設定檔連上去，只有沃爾瑪看得到 | 4k85, agent-profiles.data.steps[1] | W | 200 | CONFIRMED（Only Walmart sees this） | |
| 83 | 抽樣 | 這道閘道叫 Agent Gateway，用 MCP 連線 | n59q | W, V3, TC | 200 | CONFIRMED（W：MCP；V3、TC：Model Context Protocol） | |
| 84 | R1 改 | 它會先對企業和開發者開測試版 | 8e66 | W | 200 | CONFIRMED（We'll begin with a beta for companies and developers；V3 寫 currently available in beta，以官方未來式為準） | |
| 85 | 抽樣 | MCP 是讓代理直接跟網站系統對話的通用接口，不用一頁一頁點 | t2px | W, TC | 200 | CONFIRMED（白話；W：faster, more reliable way … than a web browser, following steps designed for people） | |
| 87 | R1 改 | 表格第三欄「代理會碰到的」 | three-doors.data.columns[2] | W | 200 | CONFIRMED | |
| 88 | 抽樣 | Amazon：全擋；彈窗加條款，要求 Meta 移除 | three-doors.data.rows[0] | V1, V2 | 200 | CONFIRMED（requested that Meta remove Amazon；Conditions of Use） | |
| 89 | 抽樣 | Target：看情況；機器人檢查，時開時關 | three-doors.data.rows[1] | V1 | 200 | CONFIRMED | |
| 90 | 抽樣 | 沃爾瑪：正門加規則；預設每筆要本人核准，價格跟人一樣 | three-doors.data.rows[2] | W | 200 | CONFIRMED（by default；the prices that an AI agent sees are the same prices that a human would see） | |
| 93 | 抽樣 | 代理條款五條（旁白五句與卡片） | wnnu, hde2, 7tpu, pqye, e5qx, agent-terms.data | W | 200 | CONFIRMED（beyond what the shopper intends；don't receive payment-card information and can't add or change payment methods；only the information needed for the task and allowed by the customer；returns process applies including if an agent doesn't act as intended；will be blocked） | |
| 94 | R1 改 | 不用付費會員，有沃爾瑪帳號就行；Sam's Club 也能用代理買 | 8qub | TC, W, V3 | 200 | CONFIRMED（TC：anyone with a Walmart account; a Walmart+ membership is not necessary；W、V3、TC 都寫 Sam's Club 支援代理購物） | |
| 95 | 抽樣 | 設定檔一個月內推出，隨時可以刪掉 | 7e7h | W | 200 | CONFIRMED（launching in the next month；Delete an Agent Profile at any time） | |
| 99 | 抽樣 | 照片、年份、關鍵字、該去哪些二手平台，全交給 Muse | ebxr | V1 | 200 | CONFIRMED（另有 notes about similar items，旁白省略不算錯） | |
| 103 | R1 改 | 第一：Meta 說一律會先問，沃爾瑪預設每筆要核准 | p68i, three-questions.data.rows[0] | V1, W | 200 | CONFIRMED（Meta 發言人：always ask permission before buying；W：by default） | |
| 104 | 抽樣 | 第二：沃爾瑪給得出上限，Meta 的回應裡沒有 | cspx, three-questions.data.rows[1] | W, V1 | 200 | CONFIRMED（Meta 發言人兩段原話沒提消費上限） | |
| 107 | 抽樣 | 記者每一次嘗試的細節與條款整理在說明欄的文章裡 | wvu2, article-cta.data | M1, M2 | 200 | CONFIRMED（兩篇今天 200，都在 sources） | |

## 第 1 輪留下的五個懷疑

1. zd4i「三張收據」：改。收據代表付過款，報導是 it offered options，沒有購買；聽者會誤會成代理已經替她下單。改「三張價目單」，句長與插圖的紙片意象都不變，loops（3mw8 → zd4i）的 what「穀物棒的比價清單少了哪一家」仍成立。
2. u67x「最適合」vs could be truly useful：不改。報導把它放在「代理的其他用法都很累人」的對比裡（A more rote task like finding the absolute lowest price on a product you already know you want is where an agent could be truly useful），「最適合」是這個對比的合理轉述，來源沒有反駁；略強，但不構成錯誤。
3. ztjr 把連鎖超市與西岸零售商合成一家：不改。兩件事都出現在同一次穀物棒比價（a grocery chain that doesn't ship to my address；a West Coast-based retailer wouldn't ship to New York），彼此一致，來源沒有反駁「同一家」，也沒有證實；記為推論。
4. rg97「幾分鐘後」的先後：不改。報導只說床墊那次被擋時，幾分鐘前還抓得到 Target（despite being able to pull from the site just a few minutes prior）；旁白「幾分鐘後改問床墊，又被擋」保留了「幾分鐘前還進得去」這個事實，至於幾分鐘前那次是不是面霜，來源沒說，也沒反駁；記為推論。
5. wuyy 把技術長的一般說法講成「回答」：不改。技術長確實是以電子郵件回覆 The Verge（told The Verge in an email），內容講的正是防止干擾顧客體驗的自動行為，與 3fx2 的問題相關；它是一般立場而不是針對購物車實驗的回覆，這是結構與 loops 的安排，不是事實錯誤，留給站主。

## 摘要

- 重查：49 列（第 1 輪改過 18 列＋查無 1 列＋抽樣 26 列＋懷疑另加 4 列）；CONFIRMED 48、CHANGED 1（zd4i「收據」→「價目單」，video.json 與 claims.md c4 同步）、NOT FOUND 0。第 1 輪的 18 處修改全部站得住，#13 拿掉日期後的寫法也成立。沒有任何數字被改（12 美元、20 分鐘、10 件、50／100／200 美元都與來源一致）。
- 會過期的事實：「去年 11 月」「今年 8 月」（V2 2026-09-21：sued Perplexity in November last year、a judge siding with Perplexity … in August）在 2027-01-01 後變錯；「沃爾瑪下個月開」「設定檔一個月內推出」（W 2026-10-21 launching in the next month；V3 Next month；TC rolling out next month）約 2026-11-21 後過期；Agent Gateway「會先對企業和開發者開測試版」（W 2026-10-21）隨上線改變；Amazon 封鎖 Muse 的現況（V2 2026-09-21，V1 2026-10-22 仍寫 hard-blocked）。
- 站主觀點不符：無。d6z5、4atb／ivq8、84qy／k8hh、ft39、9963、6tme、ntjj 後半都與 brief 的站主觀點一致；brief 註明那一段是提案、站主還沒確認。
- 聽感（只報告）：超過 40 字的句子 5 句（f325 43、wuyy 42、yfj5 44、kg8h 41、9mxy 43），與第 1 輪相同；zd4i 改後仍在 40 字內；沒有「經查證」「根據官方文件」「本影片」；旁白沒有括號或網址；Sam's Club、The RealReal、The Verge、Agent Profiles、Agent Gateway 每個字都在字典（lint 沒有字典錯誤）；kg8h 先說「它的閘道」、下一張 n59q 才說「這道閘道叫 Agent Gateway」，不算先揭曉後介紹。
- lint：`node tools/video/cli.mjs lint --slug ai-shopping-agents-blocked` → 0 errors, 1 warning（closing 單一畫面約 19 秒，撰稿時就有的版型警告）。zd4i 沒有 `say`，沒有 `say_for` 要更新。
- 懷疑但沒改：u67x、ztjr、rg97、wuyy 四條見上（推論或框架，來源沒有反駁）；mgg4 旁白「用它的瀏覽原則處理」省略 ethical，卡片譯文已補，旁白不算錯；shorts.json 不在可改範圍，第 1 輪提醒的兩處（第 1 支沿用 rg97 的推論、第 2 支「一件都拿不到」少了「等於」）仍要撰稿者同步（shorts.json 沒有用到「收據」，這一處不用跟）。
- 需要第三輪：否（本輪只改了 1 處事實，不多於 3 處）。
