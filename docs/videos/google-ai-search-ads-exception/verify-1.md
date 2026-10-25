# 查核第 1 輪：google-ai-search-ads-exception

查核日 2026-10-24。來源：存檔 HTML（`_tools/sources/`，2026-10-24 存，去標籤後逐字比對）＋本輪新開 B（Google 官方部落格，curl HTTP 200）。P＝policies.google.com/privacy?hl=en（Effective October 16, 2026）；A＝privacy/archive/20261001（Effective October 1, 2026）；H1＝answer/16859283；H2＝17212611；H3＝17026260；H4＝17025248；H5＝17265703（Connected Apps，第三方 app，跟本片的 Connected Content Apps 不同）；M＝Mokaair 文章（HTTP 200，datePublished 2026-10-23T17:29Z）；B＝blog.google personal-intelligence-ai-mode-search（Jan 22, 2026）。The Verge 本機抓不到。網頁搜尋用了 2 次。

## 主張表

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 政策 10/16 生效、多了一句 | open cyck、date、title、縮圖 sub | P「Effective October 16, 2026」 | 存檔 | CONFIRMED | |
| 2 | 幾天後 The Verge 報導、原本承諾加了例外 | open hbzk | M（10/23 前已報導） | 200 | CONFIRMED（「幾天後」未唸數字） | |
| 3 | 說明欄「The Verge 2026-10-23」 | youtube.description | M 沒寫 The Verge 的日期，只證明不晚於 10/23 | 200 | NOT FOUND | 刪掉日期 |
| 4 | 會讀摘要、做推論、拿去選廣告；不把信交給廣告商 | short-answer s6xc | H1「may be used to show you ads」「advertisers will not have access」 | 存檔 | CHANGED（may） | 拿去選廣告 → 也能拿去選廣告 |
| 5 | 只管自己按過 Connect 的人 | who duti | P unless you choose；H1 You get to choose | 存檔 | CONFIRMED | |
| 6 | 廣告三條規矩的第二條、在個人化服務和廣告那一段 | date v7fy、policy-page keqw | P 段名「Provide personalized services, including content and ads」，三個 bullet 第二個 | 存檔 | CONFIRMED | |
| 7 | 舊版 quote 逐字 | old.data.quote | A 第 109 行 | 存檔 | CONFIRMED（含 ’） | |
| 8 | 前一版才十五天前生效 | old ba73 | 10/1 → 10/16 | 存檔 | CONFIRMED | |
| 9 | 新版 quote 逐字 | new.data.quote | P 第 123 行 | 存檔 | CONFIRMED | |
| 10 | 舊版廣告依據「興趣和活動」、新版多「個人化內容」 | compare-versions 4273/8mvy 與卡片 | A「interests and activity across Google services」；P「interests, activity, or personalized content from Google services」 | 存檔 | CONFIRMED | |
| 11 | example quote 逐字 | example.data.quote、37kx | P 第 120 行；A 無此段 | 存檔 | CONFIRMED | |
| 12 | 新段落點名 Search、Gemini Apps；Photos、Gmail、Drive；照拿資料那個服務的規矩 | allow 卡片、qdy7、4scp | P「including services like Search or Gemini Apps … subject to the policies and settings of the accessing service」 | 存檔 | CONFIRMED | |
| 13 | policy-page focus 選擇器 | policy-page.steps | P 的 data-name="personalized-ads" 只出現一次，`</p>` 後緊接 `<ul>` | 存檔 | CONFIRMED（render 時再看） | |
| 14 | 「你選擇」＝Connect，在搜尋個人化設定 | connect mwqx | H1 四步 | 存檔 | CONFIRMED | |
| 15 | 問餐廳看你訂過哪幾家；問週末去哪翻 Gmail 買過什麼 | why-connect rz4b | H1「like using past restaurant reservations」「might look into past purchases from Workspace apps, like Gmail」 | 存檔 | CHANGED（might） | 它會翻 → 它可能翻 |
| 16 | 兩組：Workspace（Gmail、Google Calendar）、Google Photos | apps c586/hpnd、卡片 | H1「Google Workspace (currently Gmail and Google Calendar)」「Google Photos」 | 存檔 | CONFIRMED | |
| 17 | Calendar 只開給美國英文 | apps g8yq | H1「only available in the US in English」 | 存檔 | CONFIRMED | |
| 18 | 台灣在支援清單上 | apps g8yq/3fvn | H1 Asia-Pacific 列有 Taiwan；語言列有 Chinese (Traditional) | 存檔 | CONFIRMED | |
| 19 | Photos 不是每個地區都開、哪些地區沒寫 | apps hpnd/3fvn | H1「isn’t available in all regions」，頁面沒列地區 | 存檔 | CONFIRMED（「我沒查到」誠實） | |
| 20 | 預設沒有連、十八歲以上、隨時可以斷開 | apps 7mh2/xv9t、卡片 | H1「18 and above」「You get to choose」「at any time」；H2「18 or older」「connect or disconnect … at any time」；B「strictly opt-in」 | 存檔／200 | CONFIRMED | |
| 21 | Photos 要先開 Face Groups 選自己的臉、開 Estimate missing locations；沒做搜尋拿不到相簿的個人化 | photos-prep | H1 Manage Google Photos settings 段 | 存檔 | CONFIRMED | |
| 22 | Connect 一按所有搜尋服務都能存取 Workspace 和 Photos | where-stops x7ux | H1 Note「all Search services will be permitted to access」 | 存檔 | CONFIRMED | |
| 23 | 所有搜尋服務＝Search（AI Mode、Discover）、Maps（Ask Maps）、Shopping、Flights、Hotel(s)、Translate、News | services 卡片、pnub/fqdv | H1 Note 逐項；H2 同（寫 Hotels） | 存檔 | CONFIRMED | |
| 24 | 廣告商看不到信；搜尋拿到摘要、片段、推論 | table h9id/3pu4、卡片 | H1 Ads 兩題 | 存檔 | CONFIRMED | |
| 25 | 推論例：常買的品牌、喜歡的餐廳類型 | table 3pu4 | H1「preferred brands and dining preferences」 | 存檔 | CONFIRMED | |
| 26 | 同一份可以拿去選廣告；拿不到信箱、相簿、姓名、信箱地址 | table dspx、卡片 | H1；P「such as your name or email, unless you ask us to」 | 存檔 | CONFIRMED | |
| 27 | not-directly quote 逐字 | not-directly.data.quote、mdcm | H1 | 存檔 | CONFIRMED | |
| 28 | 訓練：練摘要、片段、推論，不是整個信箱 | training 8jv9、左卡 | H1「do not train … directly on your Gmail inbox … we train … off of these summaries, excerpts, generated media, and inferences」 | 存檔 | CONFIRMED | |
| 29 | 人工審核：一小部分、看之前先跟帳戶脫鉤 | training chw8、右卡 | H1「a subset of that data … is reviewed by human reviewers」「we take steps … such as disconnecting interactions from your Google Account … unless it's to address abuse or harm」 | 存檔 | CONFIRMED（省略 abuse/harm 例外，見下） | |
| 30 | 有不想被人看到的信就不要連，Google 自己寫的 | training dbt8 | H1「Please don't connect … that you wouldn’t want a reviewer to see」 | 存檔 | CONFIRMED | |
| 31 | 短信的摘要可能就是整封 | how-short xsz7 | H1「the summary may just be the email or file」 | 存檔 | CONFIRMED | |
| 32 | 敏感類別：種族、宗教、性傾向、健康；兩版都有 | sensitive ptg5/n6xb | P、A、H1 都是「such as race, religion, sexual orientation, or health」 | 存檔 | CHANGED（such as 是舉例） | 有四類… → 有幾類…，例如… |
| 33 | 登山車 → YouTube 運動用品廣告，兩版都有 | bikes f25v、卡片 | P、A | 存檔 | CONFIRMED | |
| 34 | My Ad Center 可以控制廣告用的資料，兩版都有 | ad-center 7j2v、卡片 | P 121、A 107 同句「You can control what information we use to show you ads by visiting your ad settings in My Ad Center.」 | 存檔 | CONFIRMED | |
| 35 | 「連結我放在說明欄」（My Ad Center、search-personalization、myactivity） | s3gu、7j2v、bqmd | 說明欄與 sources 原本都沒有這三個網址 | — | CHANGED | 說明欄補三個網址 |
| 36 | 四步（On your computer） | steps-connect、s3gu/can6/nmqp/8rnf | H1 逐字；What you need「You must have Personalized Recommendations enabled」 | 存檔 | CONFIRMED | |
| 37 | 已連上的在同一頁斷開 | tew4 | H1 只寫「disconnecting … at any time」，沒寫在哪一頁 | 存檔 | CONFIRMED（推論，見下） | |
| 38 | help-page focus `article ol` | help-page.steps | `<article>` 之後第一個 `<ol>` 就是四步 | 存檔 | CONFIRMED | |
| 39 | 斷開不刪 Search Services History；還能改進產品、訓練模型；要自己刪 | history-stays、all-off-q | H1 逐字；設定頁 href＝myactivity.google.com/search-services/settings（H4） | 存檔 | CONFIRMED | |
| 40 | 關掉路徑：Google 帳戶 › Data & privacy › Personalization settings › 關 PR | steps-off | H3、H4 逐字；Google Account 連結＝myaccount.google.com | 存檔 | CONFIRMED | |
| 41 | 關掉之後仍用目前位置、語言；存的地點、追蹤的股票都在；不關不刪 History | off-keeps | H3「Current location」「Language and device type」「saved places in Maps … stock watchlists」「Turning this setting off doesn’t: Turn off or delete Search Services History」 | 存檔 | CONFIRMED | |
| 42 | AI Mode 個人化要這個開關和搜尋紀錄都開著；18 歲以上 | tradeoff hgcg、卡片 | H2「available if you're 18 or older and have history and personalized recommendations enabled」 | 存檔 | CONFIRMED | |
| 43 | 開關留著不連，AI Mode 還從你的搜尋學 | tradeoff jqm3、右卡 | H2「references previous searches and activity saved in your Search Services History」 | 存檔 | CONFIRMED | |
| 44 | History 是另一個開關、另一頁；只關掉／關掉並刪掉 | separate | H3；H4「select Turn off, then choose to Turn off or Turn off and delete activity」 | 存檔 | CONFIRMED | |
| 45 | 還在分批推出，名字可能還是舊的 | rollout、說明欄 | H3、H4「rolling out gradually over the next few months … still controlled by Web & App Activity」 | 存檔 | CONFIRMED | |
| 46 | 「把一個早就有的開關寫進政策」（意見） | my-call-1 rbea | B：2026-01-22 起 AI Pro/Ultra 美國英文可 Connect（步驟寫 Connected Content Apps） | 200 | CONFIRMED 前提（新增 c26、sources 加 B） | |
| 47 | 「我猜台灣大多數人這一步還沒按過」 | my-call-3 7qs5 | 無數據；已用「我猜」標意見、未唸數字 | — | OUT OF SCOPE（意見，合 brief） | |
| 48 | 說明欄：段名、10/16 與 10/01 兩版、說明中心內容 | youtube.description | P、A、H1–H4 | 存檔 | CONFIRMED | |
| 49 | 標題「10 月 16 日改的那一句」、縮圖「10/16 多了一句 unless」 | youtube.title、thumbnail | P | 存檔 | CONFIRMED | |
| 50 | tags | youtube.tags | 名詞皆見於 P/H1–H4 | 存檔 | CONFIRMED | |

## 摘要

- 查了 50 項：確認 44、改 5（s6xc、rz4b、ptg5、說明欄刪 The Verge 日期、說明欄補三個網址）、查不到 1（The Verge 的確切日期，已刪）；另 1 項意見不查。
- 會過期的事實：H1–H4 都寫設定「rolling out gradually over the next few months」，介面名稱可能改；政策現行版 Effective October 16, 2026，新版生效就要重看；Calendar 只限 US English、Photos 地區限制都可能擴大。
- 意見：rbea、7qte、sxya/tm32、7qs5 都有標記，跟 brief 站主觀點一致；brief 把「台灣大多數人還沒按過」寫成事實，旁白用「我猜」更穩，不改。
- 聽眾檢查（只報告）：pnub「探索動態」不是 Google Discover 在台灣常見的名稱（說明中心中文多作「探索」），可請站主決定；75f6「也走同一條路」容易聽成信件摘要會變成 YouTube 廣告，H1 只說會拿來投廣告、沒說投在哪；沒看到驗證旁白、括號或網址在旁白裡。
- lint：0 錯 1 警告（outro 一句，刻意）。
- 懷疑但沒改：chw8「看之前先跟你的帳戶脫鉤」省略了 H1 的「such as」與「unless it's to address abuse or harm」；tew4「在同一頁斷開」是推論（H1 只說隨時可斷開）；B（1 月）寫「Training is contained to limited info, like specific prompts」，現行 H1 改說會用摘要訓練，片中照現行 H1，沒有問題，但如果站主想講「訓練範圍變大」需另查。
- 需要第二輪：是（本輪事實改動 5 項，超過 3）。
