# 查核第 2 輪：google-ai-search-ads-exception

查核日 2026-10-24，另一個代理（沒寫稿、不是第 1 輪）。本輪全部重新抓網頁（curl，HTTP 全部 200，無轉址），去標籤後逐字比對；存在 `<VIDEO_WORKDIR>/google-ai-search-ads-exception/_tools/verify/round2/`。網頁搜尋 0 次。

P＝https://policies.google.com/privacy?hl=en（頁面寫 Effective October 16, 2026）；A＝https://policies.google.com/privacy/archive/20261001?hl=en（Effective October 1, 2026）；H1＝https://support.google.com/websearch/answer/16859283?hl=en；H1tw＝同頁 ?hl=zh-Hant；H2＝17212611；H3＝17026260；H4＝17025248；H5＝17265703；B＝https://blog.google/products-and-platforms/products/search/personal-intelligence-ai-mode-search/（頁面日期 Jan 22, 2026）；M＝Mokaair 文章（存檔，datePublished 2026-10-23T17:29Z）。

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 10/16 生效、多了一句 | cyck、date、title、縮圖 | P | 200 | CONFIRMED | |
| 2 | 幾天後 The Verge 報導、承諾加例外 | hbzk、說明欄 | M（二手，只當時間點） | 存檔 | CONFIRMED | |
| 3 | 說明欄不寫 The Verge 日期（第 1 輪改） | description | M | 存檔 | CONFIRMED | |
| 4 | 讀摘要、做推論、也能拿去選廣告；不把信交給廣告商（第 1 輪改） | s6xc | H1「That same info may be used to show you ads」「advertisers will not have access」 | 200 | CONFIRMED | |
| 5 | 只管按過 Connect 的人；「你選擇」＝Connect | duti、mwqx | P「unless you choose…」、H1 | 200 | CONFIRMED（見懷疑事項：政策也點名 Gemini Apps） | |
| 6 | 廣告三條的第二條、在 Provide personalized services 段 | v7fy、keqw | P 第 119–124 行 | 200 | CONFIRMED | |
| 7 | old quote 逐字 | old.data.quote | A | 200 | CONFIRMED（程式比對 includes＝true） | |
| 8 | 前一版十五天前生效 | ba73 | A Oct 1 → P Oct 16 | 200 | CONFIRMED | |
| 9 | new quote 逐字 | new.data.quote | P | 200 | CONFIRMED（逐字） | |
| 10 | 舊版 interests and activity；新版多 personalized content | 4273、8mvy、compare 卡 | A 107、P 121 | 200 | CONFIRMED | |
| 11 | example quote 逐字；A 沒有 | example、37kx | P 120 | 200 | CONFIRMED（逐字；A 無） | |
| 12 | 新段點名 Search、Gemini Apps；Photos、Gmail、Drive；照拿資料那個服務的規矩 | qdy7、4scp、allow 卡 | P 120 | 200 | CONFIRMED | |
| 13 | policy-page 選擇器 data-name="personalized-ads" 唯一 | policy-page.steps | P HTML | 200 | CONFIRMED（出現 1 次） | |
| 14 | 問餐廳看訂過哪幾家；週末去哪可能翻 Gmail 買過什麼（第 1 輪改） | rz4b | H1 | 200 | CONFIRMED | |
| 15 | 兩組：Workspace（Gmail、Google Calendar）、Google Photos | c586、hpnd、apps 卡 | H1 | 200 | CONFIRMED | |
| 16 | Calendar 只限美國英文；台灣在清單、繁中在語言清單 | g8yq、3fvn | H1 | 200 | CONFIRMED | |
| 17 | Photos 不是每個地區都開，頁面沒列 | hpnd、3fvn | H1 | 200 | CONFIRMED | |
| 18 | 預設不連、18 歲以上、隨時可斷開 | 7mh2、xv9t | H1「18 and above」「at any time」、H2、B「strictly opt-in」 | 200 | CONFIRMED | |
| 19 | Photos 要先開 Face Groups 選臉、Estimate missing locations | photos-prep | H1 | 200 | CONFIRMED | |
| 20 | Connect 一按所有搜尋服務都能存取 | x7ux | H1 Note | 200 | CONFIRMED | |
| 21 | 服務清單 AI Mode、Discover、Ask Maps、Shopping、Flights、Hotels、Translate、News | services 卡 | H1（寫 Hotel）、H2 與 H1 頂部公告（寫 Hotels） | 200 | CONFIRMED | |
| 22 | Discover 的中文名 | pnub | H1tw「Google 搜尋 (含 AI 模式、探索)」 | 200 | CHANGED（名稱） | 探索動態算 → Google 探索都算 |
| 23 | 廣告商看不到信；搜尋拿摘要、片段、推論；品牌、餐廳 | h9id、3pu4、table | H1 | 200 | CONFIRMED | |
| 24 | 同一份可選廣告；拿不到信箱、相簿、姓名、信箱地址 | dspx、table | H1；P 第 124 行 | 200 | CONFIRMED | |
| 25 | not-directly quote 逐字 | not-directly | H1 | 200 | CONFIRMED（逐字） | |
| 26 | 訓練練摘要、片段、推論，不是整個信箱 | 8jv9、training 左卡 | H1 | 200 | CONFIRMED | |
| 27 | 人工審核：一小部分、看之前先跟帳戶脫鉤 | chw8、training 右卡 | H1「we take steps to protect your privacy, such as disconnecting interactions from your Google Account and reducing personal information …, unless it's to address abuse or harm」 | 200 | CHANGED（是舉例且有例外，原句說成必然） | 看之前先跟你的帳戶脫鉤 → 看之前會先做保護，例如跟你的帳戶脫鉤；卡 A subset, detached from your account → A subset; steps such as detaching |
| 28 | 有不想被人看到的信就不要連，Google 寫的 | dbt8 | H1「Please don't connect … that you wouldn’t want a reviewer to see」 | 200 | CONFIRMED | |
| 29 | 短信摘要可能就是整封 | xsz7 | H1 | 200 | CONFIRMED | |
| 30 | 敏感類別「例如」四類，兩版都有（第 1 輪改） | ptg5、n6xb | P 122、A 108、H1 | 200 | CONFIRMED | |
| 31 | 登山車 → YouTube 運動用品，兩版都有 | f25v | P 121（新版多 in Search）、A 107 | 200 | CONFIRMED | |
| 32 | 「信件摘要也走同一條路」 | 75f6 | H1 只說「may be used to show you ads」，沒說投在哪個服務；P 也沒說 | 200 | CHANGED（暗示會出現在 YouTube，來源沒寫） | 也走同一條路 → 也可能拿來選廣告 |
| 33 | My Ad Center 可控制，兩版都有；說明欄網址 | 7j2v、ad-center、description | P、A；P 連結 myadcenter.google.com | 200 | CONFIRMED | |
| 34 | 說明欄三個設定網址（第 1 輪加） | description | H1 href www.google.com/search-personalization/；H4 href myactivity.google.com/search-services/settings；P myadcenter | 200 | CONFIRMED | |
| 35 | 四步（On your computer）；PR 沒開不能連 | steps-connect | H1「What you need」與四步 | 200 | CONFIRMED | |
| 36 | 已連上的在同一頁斷開 | tew4 | H1 只有「You can adjust your settings, including disconnecting content apps from Search services, at any time」；H5 的斷開路徑（myaccount.google.com/connections）是第三方 Connected Apps，不是 Connected Content Apps | 200 | CHANGED（推論） | 在同一頁斷開 → 隨時可以在設定裡斷開 |
| 37 | help-page 選擇器 article ol | help-page | H1 HTML | 200 | CONFIRMED | |
| 38 | 斷開不刪 History；可改進產品、訓練；自己刪 | n427、bqmd | H1 | 200 | CONFIRMED | |
| 39 | 關掉路徑：Google 帳戶 › Data & privacy › Personalization settings | steps-off | H3、H4 | 200 | CONFIRMED | |
| 40 | 關掉仍用位置、語言；存的地點、追蹤股票都在；不關不刪 History | usjx、dchc | H3 | 200 | CONFIRMED | |
| 41 | AI Mode 個人化要 PR 和 history 都開；18 歲 | hgcg、tradeoff | H2 | 200 | CONFIRMED | |
| 42 | 開關留著不連，AI Mode 還從搜尋學 | jqm3 | H2 | 200 | CONFIRMED | |
| 43 | History 另一開關；只關掉／關掉並刪掉 | zu39、ns6r | H3、H4 | 200 | CONFIRMED | |
| 44 | 分批推出、可能還是 Web & App Activity | dvnq、rollout | H3、H4 | 200 | CONFIRMED | |
| 45 | 早就有的開關（意見）；B 是 2026-01-22 | rbea、c26、sources | B 頁面「Jan 22, 2026」；步驟「Select Connected Content Apps」「Connect Workspace and Google Photos」；AI Pro/Ultra、美國英文、strictly opt-in | 200 | CONFIRMED | |
| 46 | 我猜台灣多數人沒按過 | 7qs5 | — | — | OUT OF SCOPE（意見已標） | |
| 47 | title、縮圖、tags | youtube | P、H1–H4 | 200 | CONFIRMED | |

## 摘要

- 查了 47 項（第 1 輪改過的 7 項全部重查，其餘幾乎全部重開頁面查，不只三分之一）：確認 42、改 4（chw8＋卡片、tew4、75f6、pnub）、查不到 0、意見 1。
- 事實改動 3 項：chw8（脫鉤是「例如」且有 abuse/harm 例外）、tew4（頁面沒寫在哪一頁斷開）、75f6（來源沒說摘要會投在 YouTube）。pnub 是名稱改正（Google 台灣說明頁寫「探索」），不算事實改動。
- 第 1 輪的改動都成立：s6xc、rz4b、ptg5、說明欄刪 The Verge 日期、說明欄三個網址、c26、B 的日期。
- 會過期：P 現行版 Effective October 16, 2026；H1–H4 都說設定「rolling out gradually over the next few months」；Calendar 只限 US English、Photos 地區限制可能擴大。
- 意見：rbea、7qte、sxya、tm32、7qs5 都有標，跟 brief 站主觀點一致。
- 聽眾檢查（沒改）：pnub「地圖裡的 AI 問答」Google 台灣叫「問問 Google 地圖」，可唸正式名；37kx 省略了「some of」（may process some of the data），可接受；34p5／b8y5「第三層」是口語數法，頁面沒這樣數；8rnf「還寫著 Connect 就是還沒交出去」是從步驟推的 UI 狀態，說明頁沒寫已連接時按鈕叫什麼；3fvn「我沒查到」有一點查證口吻。沒有聽起來像本頻道登入或實測過的句子。
- lint：0 錯 1 警告（outro 一句，刻意）；估 9.0 分鐘。
- 懷疑但沒改：duti／mwqx 把「你選擇」等同搜尋的 Connect 按鈕；政策新段也點名 Gemini Apps 可以存取 Gmail 等資料，但沒有任何頁面說 Gemini Apps 是「support personalized ads」的服務，所以旁白目前只講有文件的那條路，合理但不是政策原文的全部；B（1 月）寫訓練只限 prompts 和回應，現行 H1 改寫成會用摘要訓練，片中照現行 H1。
- 第三輪：不需要（事實改動 3 項，沒有超過 3）。
