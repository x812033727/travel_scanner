# 查核第 4 輪：ai-shopping-agents-blocked（紙底版）

查核日 2026-10-23，獨立查核者（不是撰稿者，也不是第 1–3 輪的查核者）。範圍照第 4 輪規則：第 3 輪改的五處全部重查；第 3 輪確認的 45 條隨機抽三分之一（16 條）；統籌在第 3 輪之後改寫的 5i3t、owner-use 卡、vaf7、dxbj、xiq6、2y4r 對照來源與 `brief.md` 站主觀點。

來源今天重開（`curl -sSL -A "Mokaair-editorial/1.0 (...)"`，請求之間隔 1.5 秒、同一主機至少 3 秒，存在 `<VIDEO_WORKDIR>/ai-shopping-agents-blocked/_tools/verify/round4/live/`，`<!-- -->`、script、style 先剝掉再讀）：

| 代號 | URL | HTTP | 備註 |
|---|---|---|---|
| V22 | https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse | 200 | 無轉址、無更正（Oct 22, 2026） |
| V21 | https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping | 200 | 無轉址、無更正 |
| VW | https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents | 200 | 無轉址 |
| WM | https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers | 200 | 無轉址 |
| TC | https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/ | 200 | 無轉址 |

網路搜尋 1 次（Amazon 封鎖 Muse 的後續）：結果都是 2026 年 9 月的報導，沒有 10 月解除封鎖或 Meta 移除 Amazon 的消息。

## 一、第 3 輪改過的五處

| # | 主張 | 位置 | 來源 | HTTP | 結論 | 修改前 → 修改後 |
|---|---|---|---|---|---|---|
| R3-7 | Target：可能要看那次任務怎麼做、網站有哪些防護 | door-01/wx69、door-01.data.sub、說明欄 | V22（How successful an agent is at accessing a site may depend on how it went about the task and what safeguards are in place） | 200 | 確認 | |
| R3-14 | 記者說，最用得上它的是已經知道要買什麼、只差比最低價的任務 | rote-rule/n3fs、rote-rule.data.kicker、key | V22（A more rote task like finding the absolute lowest price on a product you already know you want is where an agent could be truly useful） | 200 | 改：原文沒有「最」，且是 could 的保留語氣（與 R3-7 補「可能」同理） | n3fs「記者說，最用得上它的是：……」→「記者說，真正用得上它的，可能是：已經知道要買什麼、只差比最低價的任務。」；kicker「記者說它最用得上的」→「記者說它可能真正用得上的」；key「知道要買什麼、只差比價時最有用」→「只差比價的任務，它可能真有用」（14 字）；text、sub 不變 |
| R3-33 | 卡片：很快，你可能得跟別人的代理搶 | why-not-block.data.sub、key | V22（my future self, who may soon be competing with someone else's agent doing this same thing） | 200 | 確認（「可能得」對 may soon；旁白 g8eg 以「她擔心的是」框住） | |
| R3-37 | 第三種門：先登記、每一筆預設要老闆點頭、可設上限 | door-03/8fej、door-03.data.sub | WM（Customers must approve agent purchases by default；spending limit they set） | 200 | 確認 | |
| R3-45 | 行動三：像沃爾瑪即將推出的設定檔，先設好再派它出門 | actions/q3kh、actions.data.steps[2].detail | WM（Agent Profiles, launching in the next month）；TC（rolling out next month）；VW（Next month） | 200 | 確認（11 月下旬後會過期，見摘要） | |

## 二、統籌在第 3 輪之後改寫的句子

| # | 主張 | 位置 | 來源 | HTTP | 結論 | 備註 |
|---|---|---|---|---|---|---|
| C-1 | 以我的用法，只派它做已經知道要買什麼、只差比價和下單的任務，每一筆買之前要它先問我 | owner-use/5i3t | brief.md 站主觀點 | — | 意見，與 brief 一致 | brief：「只派它做我已經知道要買什麼、只差比價和下單的任務；每一筆購買前要它先問我」。第 3 輪報的「下單我自己來」不符已消失，也不再和行動清單第二件互相拉扯 |
| C-2 | owner-use 卡：以我的用法／每一筆買之前，先問我／只派它做知道要買什麼、只差比價和下單的任務；key「每一筆買之前，要它先問我」 | owner-use.data | brief.md 站主觀點 | — | 意見，與 brief 一致 | |
| C-3 | 今年，法官站在 Perplexity 那一邊；Amazon 的確認信也拿掉了品名和圖片 | perplexity/vaf7 | V21（a judge siding with Perplexity on the case in August；Confirmation emails … since July, with specific item names and product images being omitted） | 200 | 確認 | 旁白不唸月份，表格 rows 的「今年 7 月起」「今年 8 月」不變；以 2026-10-23 看「今年」＝2026 年，V21 發布於 2026-09-21，兩個月份都在 2026 年 |
| C-4 | Muse 不是第一個：去年十一月，Amazon 告了 Perplexity，它的代理也在站上買 | perplexity/dxbj | V21（It sued Perplexity in November last year）；V22（ignored its requests to stop its agent from shopping on the site） | 200 | 確認 | 「去年」以 V21 的 2026-09 為準＝2025 年 11 月，對 2026-10-23 的觀眾也成立；「它的代理」緊接 Perplexity，聽得出是 Perplexity 的代理 |
| C-5 | 我的看法是，Amazon 的理由站得住；但它自己也在做代理，這是生意的攻防，不只是安全 | business/xiq6 | brief.md 站主觀點；V22（own on-platform agentic shopping feature） | 200 | 意見，與 brief 一致；「它自己也在做代理」事實確認 | |
| C-6 | 這道正門叫 Agent Gateway，用 MCP 讓代理直接跟系統對話，不用一頁一頁點 | gateway/2y4r | WM（The Walmart Agent Gateway: Talking to agents, like agents；agents may shop … through a web browser, following steps designed for people；by using an MCP）；TC（new MCP server … lets an AI agent search across Walmart's online inventory and make purchases） | 200 | 確認 | 卡片副標「會先對企業與開發者開測試版」仍照官方未來式（We'll begin with a beta for companies and developers） |

## 三、第 3 輪確認項的隨機抽查（16 條，編號沿用 verify-3.md）

| # | 主張 | 位置 | 來源 | HTTP | 結論 |
|---|---|---|---|---|---|
| 1 | 10 月 21 日沃爾瑪替代理開門；一個月前 Amazon 關門 | open/6czz | WM、TC（announced on Wednesday；2026-10-21 是星期三）、V21（popup on Sunday，V21 發布於 2026-09-21 星期一，即 9-20 起） | 200 | 確認 |
| 3 | 搜商品、比價、放購物車、下單 | verbs/h54m | V22、V21（purchase tank tops from Amazon） | 200 | 確認 |
| 6 | Target 擋、隔天進、幾分鐘後改問床墊又擋 | target-door | V22 | 200 | 確認（「幾分鐘後」接在隔天那次之後仍是推論，第 1、3 輪已記） |
| 9 | 穀物棒每片最低價三家：Sam's Club、沃爾瑪、Costco | granola | V22 | 200 | 確認 |
| 12 | 一家西岸超市不送到紐約 | faster/fidw | V22 | 200 | 確認 |
| 15 | 一個星期天，Muse 使用者看到告示 | sunday/erea | V21 | 200 | 確認 |
| 18 | 三個理由 | reasons | V21（According to GeekWire…） | 200 | 確認 |
| 20 | 發言人要求移除；引文 should operate openly… | openly | V22 | 200 | 確認（引文逐字） |
| 26 | The RealReal 二手精品、每月 12 美元搶先看 | realreal | V22 | 200 | 確認 |
| 29 | 時間一到再放一次、一整天、記者自己停掉 | all-day/278c、stopped/y2ie | V22 | 200 | 確認 |
| 31 | 要是沒那麼老實，規則允許的占位可以永遠跑下去 | forever/y46v | V22 | 200 | 確認 |
| 35 | Meta 發言人：隨時可接手、一律買前先問、人做不到的事套用倫理瀏覽原則 | meta-says、tickets | V22（引文逐字；原文是 is designed to always ask permission） | 200 | 確認 |
| 39 | Agent Profiles 三步：第一次經過閘道自動建立、登入帳號連結只有沃爾瑪看得到、預設每筆或上限內自動買 | profiles | WM | 200 | 確認 |
| 40 | 上限例子 50、100、200 美元 | limit | WM | 200 | 確認 |
| 42 | 條款各條、違反就封鎖 | terms | WM | 200 | 確認 |
| 48 | 說明欄（彈窗與三個理由、背心、一個月內推出、測試版、隨時可刪、價格一樣） | youtube.description | V21、V22、WM | 200 | 確認 |

## 摘要

- 重查：27 條（第 3 輪改的 5 條＋統籌改寫的 6 處＋隨機抽查 16 條）；確認 26；改 1（R3-14 rote-rule 的「最用得上」→「真正用得上…可能是」）；查無 0。
- 會過期的事實：沃爾瑪 Agent Profiles「launching in the next month」（新聞稿 2026-10-21，約 11 月 21 日前；actions 的「即將推出」到時要改）；Agent Gateway「We'll begin with a beta for companies and developers」（官方未來式，The Verge 寫 currently available in beta）；Amazon 是否仍封鎖 Muse（V22 2026-10-22 仍寫封鎖；今天搜尋 1 次沒有 10 月的新消息，druk 照實標不確定）。
- 意見不符：無。5i3t／owner-use 已改成 brief 站主觀點原話，第 3 輪報的不符已消失；sx6e、xiq6、fezk 仍與 brief 一致。
- 聽稿（只報告）：超過 40 字的句子（含標點逐字計）qcpx 43、wx69 42、ve6e 41、erea 43、dxbj 48、vaf7 44、xiq6 44、2y4r 45、5i3t 42；n3fs 改後 36 字。沒有查證式旁白、括號或網址；拉丁詞都在字典裡；沒有先於介紹句的揭示。所有 `key`／`keys` 都在 24 字以內。
- lint：`node tools/video/cli.mjs lint --slug ai-shopping-agents-blocked` 0 錯誤、1 警告（outro 只有一句，版型本身，撰稿者已記）；估計 8.4 分鐘、82 句、1835 口語單位。
- 懷疑但沒動：8eug「Muse 一律在買之前先問你」原文是 is designed to always ask permission（設計如此，卡片引文逐字，三件事表標「Meta 說會」，歸屬清楚）；V21 的「a judge siding with Perplexity」第三方報導寫成上訴法院的裁決，官方來源只寫 a judge，保留「法官」；open 的「開了門」是宣布日、功能下個月才推出（第 3 輪已記）。
- 需要第 5 輪：否（本輪只改 1 處事實，未超過 3 處）。
