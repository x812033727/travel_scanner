# 查核第 3 輪：ai-shopping-agents-blocked（紙底版）

查核日 2026-10-23，獨立查核者（不是撰稿者）。對象：紙底版重寫的 `video.json`（49 景、82 句）。第 1、2 輪（`verify-1.md`、`verify-2.md`）查的是上一版插圖腳本，事實表仍成立；這一輪逐句查新腳本的旁白、卡片 `data`（含 `keys`、`numeral`、表格、引文與譯文）、縮圖、標題、說明欄與標籤，並核對每景引用的 c 編號是否涵蓋它說的話。

來源今天重開（`curl -sSL -A "Mokaair-editorial/1.0 (...)"`，同一主機間隔 1.5 秒，存在 `<VIDEO_WORKDIR>/ai-shopping-agents-blocked/_tools/verify/round3/live/`）：

| 代號 | URL | HTTP | 備註 |
|---|---|---|---|
| V22 | https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse | 200 | 無轉址、無更正 |
| V21 | https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping | 200 | 無轉址、無更正（2026-09-21） |
| VW | https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents | 200 | 無轉址 |
| WM | https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers | 200 | 無轉址（Oct. 21, 2026） |
| TC | https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/ | 200 | 無轉址 |

`round3/phrases.mjs` 把 67 句原文逐字比對今天的頁面，0 句缺。網路搜尋 1 次（Amazon／Muse 封鎖的後續），沒有找到解除封鎖的消息。

## 主張表

| # | 主張 | 位置 | 來源 | HTTP | 結論 | 修改前 → 修改後 |
|---|---|---|---|---|---|---|
| 1 | 10 月 21 日沃爾瑪替代理開門；一個月前 Amazon 關門 | open/6czz、open.data | WM、VW、V21 | 200 | 確認（「開門」是宣布；VW：opening its doors to AI shoppers） | |
| 2 | 隔天 The Verge 記者寫她派 Meta 的 Muse 去買東西 | reporter/qcpx、reporter.data | V22（Oct 22, 2026） | 200 | 確認 | |
| 3 | 代理會搜商品、比價、放購物車、下單 | verbs/h54m、verbs.data | V22（c4、c9）、V21（背心，c27） | 200 | 確認 | |
| 4 | 門開不開是店家決定；比價少一家它不一定會講 | stakes/fpjh、2t6w | V22（Sometimes, the agents will say as much） | 200 | 確認 | |
| 5 | 承諾句：三種門、三件事、沃爾瑪上限 | promise/t3xu | WM（c21） | 200 | 確認 | |
| 6 | Target 找面霜被機器人檢查擋；隔天同一指令進去；幾分鐘後改問床墊又擋 | target-door/g8uj、5e27、ztxw、data | V22 | 200 | 確認（「幾分鐘後」接在隔天那次之後是推論，第 1 輪已記） | |
| 7 | Target：看任務怎麼做、網站有哪些防護 | door-01/wx69、door-01.data.sub、說明欄 | V22（may depend on how it went about the task and what safeguards are in place） | 200 | 改（少了 may） | 「Target 說，看那次任務怎麼做、網站當時有哪些防護」→「Target 說，可能要看那次任務怎麼做、網站有哪些防護」；卡片副標、說明欄同步 |
| 8 | 機器人檢查擋的是所有自動程式，不只 Muse | not-only-muse/ve6e、data | V22（general bot blocking systems；safeguards preventing unauthorized agents and bots） | 200 | 確認 | |
| 9 | 穀物棒每片最低價：Sam's Club、沃爾瑪、Costco | granola/taip、jwwd、data（numeral 3） | V22 | 200 | 確認 | |
| 10 | 引文 Amazon might have had the lowest-priced option… 與譯文；Muse 自己補的 | muse-caveat、p4ma、9skt | V22（逐字；記者轉述，卡片已標） | 200 | 確認 | |
| 11 | 交給代理：少的那家要它肯講才知道 | three-tabs/qbyv、data | V22（Sometimes, the agents will say as much） | 200 | 確認 | |
| 12 | 一家西岸超市不送到紐約 | faster/fidw、data.sub | V22（grocery chain that doesn't ship to my address；West Coast-based retailer wouldn't ship to New York） | 200 | 確認（兩句合成，第 1 輪已接受） | |
| 13 | 等回覆、多搜幾家、澄清送貨範圍，自己搜大概還比較快 | faster/5pwn、data | V22（likely would have been faster） | 200 | 確認 | |
| 14 | 記者：已經知道要買什麼、只差比最低價的才交給它 | rote-rule/n3fs、rote-rule.data | V22（A more rote task like finding the absolute lowest price on a product you already know you want is where an agent could be truly useful） | 200 | 改（報導沒說她「只」交這種任務，是「最用得上」） | 「記者的選法是：……的，才交給它」→「記者說，最用得上它的是：已經知道要買什麼、只差比最低價的任務」；kicker「記者的選法」→「記者說它最用得上的」、text →「已經知道要買什麼的任務」、sub →「只差比出最低價」、key →「知道要買什麼、只差比價時最有用」 |
| 15 | 一個星期天，Muse 使用者看到告示 | sunday/erea、data | V21（A popup message started appearing on Sunday for Muse users） | 200 | 確認 | |
| 16 | 彈窗原文與譯文 | popup、6vzr、8swe | V21（逐字，引 GeekWire） | 200 | 確認 | |
| 17 | 第二種門全擋＝使用條款彈窗 | door-02/a7bt | V21、V22（hard-blocked from browsing） | 200 | 確認 | |
| 18 | 三個理由：沒通知、不表明身分、看起來會抓登入資料 | reasons/avjj、fsmh、k2gc、data | V21（According to GeekWire…；failing to identify itself；seemingly capturing customer credentials） | 200 | 確認 | |
| 19 | 「不是」因為會亂買 | reasons/avjj | V21（理由中沒有買錯） | 200 | 確認 | |
| 20 | 發言人：要求 Meta 把 Amazon 從 Muse 拿掉；引文 should operate openly… | openly.data.kicker、quote、fwer、359n | V22（requested that Meta remove Amazon；逐字） | 200 | 確認 | |
| 21 | Amazon 自己的代理：盯價格、自動補貨、照規則下單 | own-agent/vf3r、data | V22 | 200 | 確認 | |
| 22 | 去年 11 月告 Perplexity，對方的代理也在站上買 | perplexity/dxbj、rows[0] | V21（November last year）、V22（stop its agent from shopping on the site） | 200 | 確認；c11 只列 V21，補記 V22 出處 | |
| 23 | 今年 7 月起確認信拿掉品名與圖片 | perplexity rows[1]、vaf7 | V21（since July） | 200 | 確認 | |
| 24 | 今年 8 月法官站在 Perplexity 那一邊 | perplexity rows[2]、vaf7、說明欄 | V21（in August） | 200 | 確認 | |
| 25 | 現在還擋不擋不知道，先當作還在擋 | still-blocked/druk、data | V22（仍寫 Muse 進不去 Amazon）；搜尋 1 次無新消息 | 200 | 確認（標示為不確定，保留） | |
| 26 | The RealReal 二手精品；每月 12 美元搶先看 | realreal/ysce、data | V22 | 200 | 確認 | |
| 27 | 購物車保留 20 分鐘，別人拿不到 | twenty/yieg、data | V22（reserves it for you for 20 minutes, making it impossible for other people to swipe it） | 200 | 確認 | |
| 28 | 最新上架 10 件一次全放；她不打算買 | ten/emy8、xgqr、data | V22 | 200 | 確認 | |
| 29 | 時間一到再放一次，一整天；記者自己停掉 | all-day/278c、stopped/y2ie、data | V22（On and on this went, all day (I eventually ended the task)） | 200 | 確認 | |
| 30 | 門外的人等於一件都拿不到 | stopped/y2ie、all-day.data.sub、stopped.data | V22（effectively blocking other shoppers） | 200 | 確認（卡片 text 沒寫「等於」，見「懷疑但沒動」） | |
| 31 | 要是沒那麼老實，規則允許的占位可以永遠跑下去 | forever/y46v、data | V22（less honest, pure-hearted…technically allowed reserve system endlessly） | 200 | 確認 | |
| 32 | 她擔心很快也會跟別人的代理搶 | why-not-block/g8eg | V22（may soon be competing with someone else's agent） | 200 | 確認（旁白有「擔心」） | |
| 33 | 卡片：很快，你會跟別人的代理搶 | why-not-block.data.sub、key | V22（may soon） | 200 | 改（預測寫成定論） | 「很快，你會跟別人的代理搶」→「很快，你可能得跟別人的代理搶」（sub 與 key） |
| 34 | The RealReal 技術長引文（中間以「…」省略 allowing them to browse, log in and interact with our marketplace,） | realreal-quote、mdbm、v2ap | V22（逐字） | 200 | 確認：省略的是「允許瀏覽、登入、互動」的補充，意思不變，旁白與 keys 把這三個動作補回 | |
| 35 | Meta 發言人：隨時可接手、一律買前先問、人做不到的事套用倫理瀏覽原則，例如買光一場的票 | meta-says、8eug、a35m、tickets | V22（逐字） | 200 | 確認 | |
| 36 | 沃爾瑪：代理可以替顧客買但要照規矩；已接上 Muse、ChatGPT、Gemini | walmart/x8e3、data | WM（integrations with Muse, ChatGPT, Gemini and others；terms for AI agents） | 200 | 確認 | |
| 37 | 第三種門：先登記、每一筆要點頭、可設上限 | door-03/8fej、door-03.data.sub | WM（Customers must approve agent purchases by default；spending limit） | 200 | 改（少了「預設」，與「可設上限」互相矛盾） | 「每一筆要老闆點頭」→「每一筆預設要老闆點頭」；副標「每筆點頭」→「預設每筆點頭」 |
| 38 | Agent Gateway 用 MCP 讓代理直接跟系統對話，不用一頁一頁點；先對企業與開發者開測試版 | gateway/2y4r、data | WM（MCP；following steps designed for people；We'll begin with a beta）、TC（MCP server） | 200 | 確認 | |
| 39 | Agent Profiles：第一次經過閘道自動建立；登入帳號連結、只有沃爾瑪看得到；預設每筆核准或上限內自動買 | profiles/c72f、evku、hdi7、data | WM | 200 | 確認 | |
| 40 | 上限例子 50、100、200 美元（numeral 100） | limit/8rxu、data | WM（$50, $100 or $200） | 200 | 確認 | |
| 41 | 上限內沃爾瑪仍可能要求再核准 | limit-trap/zmdp、data | WM（may require additional approvals even for purchases within an agent's spending limits） | 200 | 確認 | |
| 42 | 條款：拿不到付款卡、不能新增或改付款方式；不超出意圖；只拿需要且允許的資料；退貨照退含代理沒照預期；違反就封鎖 | terms/35d6、u8h7、mtuc、data | WM（逐條） | 200 | 確認 | |
| 43 | 號碼牌＝帳號裡的代理設定檔；代理看到的價格跟人一樣 | token-stop/aezm、data | WM | 200 | 確認 | |
| 44 | 三件事表：Meta 說會先問、可接手；Meta 回應沒提上限；Amazon 它自己講了 | three-questions/pgy9、qkgp、ecah、data | V22 | 200 | 確認 | |
| 45 | 行動三：店家有給上限的，像沃爾瑪，先設好 | actions/q3kh、actions.data.steps[2].detail | WM（Agent Profiles, launching in the next month） | 200 | 改（「你現在先做」聽起來今天就能在沃爾瑪設上限；設定檔一個月內才推出） | 「像沃爾瑪，先設好再派它出門」→「像沃爾瑪即將推出的設定檔，先設好再派它出門」；detail「像沃爾瑪的 Agent Profiles」→「像沃爾瑪即將推出的 Agent Profiles」 |
| 46 | 答案：Amazon 關、Target 看情況、沃爾瑪開門加規矩 | answer/za58、data、closing.data | V21、V22、WM | 200 | 確認 | |
| 47 | 標題、縮圖（被擋在門外；Amazon 全擋、Target 看情況、沃爾瑪開門） | youtube.title、thumbnail | 同上 | 200 | 確認 | |
| 48 | 說明欄各條（除第 7 列已同步者） | youtube.description | V21、V22、WM | 200 | 確認（「隨時可刪」WM：Delete an Agent Profile at any time） | |
| 49 | 標籤 | youtube.tags | — | — | 確認（沒有事實） | |
| 50 | 意見句 sx6e、xiq6、fezk、5i3t 與留言題、訂閱句 | 各景 | brief.md 站主觀點 | — | 意見，見下 | |

## 摘要

- 主張：50 條；確認 45；改 5（#7、#14、#33、#37、#45）；查無 0。
- c 編號覆蓋：perplexity 景（c11）的「對方的代理也在站上買」出自 V22，不在 c11 原本的出處裡，已在 claims.md 補記；其他各景的 c 編號都涵蓋旁白與卡片。
- 會過期的事實：沃爾瑪 Agent Profiles「launching in the next month」（新聞稿 2026-10-21，約 11 月 21 日前）；Agent Gateway「We'll begin with a beta for companies and developers」（新聞稿未來式；The Verge 寫 currently available in beta）；Amazon 是否仍封鎖 Muse（V22 2026-10-22 仍寫封鎖；今天搜尋無新消息，druk 照實標不確定）。
- 意見不符：5i3t／owner-use「比價參考，下單我自己來」與 brief 站主觀點「只派它做我已經知道要買什麼、只差比價和下單的任務；每一筆購買前要它先問我」不一致（brief 讓代理下單、每筆先問；稿子說自己下單），也和行動清單第二件「要它每一筆買之前先問你」互相拉扯；請站主決定，未改。其餘三句（sx6e、xiq6、fezk）與 brief 一致。druk 的不確定標示保留。
- 聽稿（只報告）：超過 40 字的句子（以字元計，拉丁字母逐字算）qcpx 42、wx69 41（本輪加「可能要」後）、erea 42、dxbj 49、xiq6 47、2y4r 46；lint 以口語單位計沒有警告。沒有查證式旁白、括號或網址。拉丁詞 The Verge、Sam's Club、The RealReal、Agent Gateway、Costco、Perplexity、MCP、Muse、Target、Meta、Amazon 都以單字在字典裡（extract 腳本的片語比對是誤報）。
- lint：0 錯誤、1 警告（outro 只有一句，版型本身，撰稿者已記）；估計 8.4 分鐘、82 句、1835 口語單位。
- 懷疑但沒動：stopped 卡片 text「想買的人，一件都拿不到」與 key 沒寫「等於」（旁白有；保留期間原文是 impossible for other people to swipe it，算站得住）；walmart 卡片副標「已接上的應用程式：Muse、ChatGPT、Gemini」沒寫「等」（原文 and others，列出的三個都對）；open 的「沃爾瑪替 AI 代理開了門」是宣布日，實際功能下個月才推出（The Verge 也這樣寫，行動清單已補「即將推出」）；not-only-muse「擋的是所有自動程式」讀成「針對的對象」才成立；target-door「幾分鐘後」接在隔天那次之後是推論（第 1 輪已記）。
- 需要第 4 輪：是（本輪改了 5 處事實，超過 3 處）。第 4 輪只需重查 #7、#14、#33、#37、#45 與隨機三分之一的確認項。
