# daily-ai-20261028 查核第 1 輪

查核日 2026-10-29。查核代理不是撰稿人。每一條旁白（`text`，本片沒有 `say`）、每張卡片的 `data`、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照：
站上 13 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，全部 HTTP 200，`news_date` 2026-10-28）與 `video.json` `sources` 列的 16 個官方頁或報導，2026-10-29 全部重新打開。

## 來源代號

站上文章（全部 200）：

| 代號 | slug |
| --- | --- |
| S1 | ai-news-gemini-4-carbon-20261028 |
| S2 | tech-news-gemini-4-carbon-20261028 |
| S3 | ai-news-alphabet-q3-earnings-gemini-carbon-20261028 |
| S4 | tech-news-macbook-pro-proled-xdr-20261028 |
| S5 | ai-news-microsoft-q1-fy27-results-20261028 |
| S6 | ai-news-microsoft-openai-revenue-20261028 |
| S7 | tech-news-github-universe-copilot-20261028 |
| S8 | ai-news-github-copilot-fusion-ga-20261028 |
| S9 | ai-news-github-enterprise-includes-copilot-20261028 |
| S10 | tech-news-github-octoverse-2026-agents-20261028 |
| S11 | ai-news-instagram-mosseri-ai-negativity-20261028 |
| S12 | ai-news-chrome-autofill-gmail-20261028 |
| S13 | tech-news-south-korea-finance-cyberattacks-20261028 |

官方頁與報導（2026-10-29 重開，全部 HTTP 200，沒有任何一頁拒絕容器；不需要退回站上文章）：

| 代號 | URL |
| --- | --- |
| O1 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/ （Oct 28, 2026） |
| O2 | https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/ |
| O3 | https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/ （Sep 02, 2026） |
| O4 | https://deepmind.google/fairwind-program/ |
| O5 | https://www.theverge.com/tech/1021339/google-gemini-4-carbon-cybersecurity-frontier |
| O6 | https://www.apple.com/newsroom/2026/10/apple-unveils-groundbreaking-macbook-pro-with-proled-xdr-display/ |
| O7 | https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/press-release-webcast |
| O8 | https://techcrunch.com/2026/10/28/microsoft-recorded-10-billion-in-revenue-from-openai/ |
| O9 | https://techcrunch.com/2026/10/28/microsoft-hits-10-quarters-of-record-breaking-revenue-in-a-row/ |
| O10 | https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/ |
| O11 | https://github.blog/changelog/2026-10-28-github-enterprise-now-includes-access-to-github-copilot/ |
| O12 | https://github.blog/news-insights/company-news/github-universe-2026-evolving-every-layer-of-the-stack/ |
| O13 | https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/ |
| O14 | https://www.theverge.com/ai-artificial-intelligence/1021644/adam-mosseri-instagram-ai-negativity |
| O15 | https://blog.google/products-and-platforms/products/chrome/enhanced-autofill-gmail/ （datePublished 2026-10-28T17:00Z，dateModified 2026-10-28T20:21Z） |
| O16 | https://techcrunch.com/2026/10/28/south-koreas-financial-industry-hit-by-fresh-wave-of-cyberattacks/ |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 月 28 日 Google 發表 Gemini 4 Carbon，說是自家最強模型 | 3ywc；open.data | S1、S2、O1 | 200 | CONFIRMED（O1：「our strongest model」，Oct 28, 2026） | |
| 2 | 一般人現在用不到，先拿到的是另一群人 | jixu；open.data.key | O1、O5 | 200 | CONFIRMED | |
| 3 | 同一天，微軟一季有 100 億美元營收來自 OpenAI | 6uky；open-ms.data | O8、S6 | 200 | CONFIRMED（O8：regulatory filing on Wednesday，quarter ended September 30） | |
| 4 | OpenAI 是微軟的「對手」 | 6uky | O8 | 200 | CHANGED（O8 只說 increasingly compete for the same customers） | 「來自它的對手 OpenAI」→「來自越來越像對手的 OpenAI」 |
| 5 | 新 MacBook Pro 讓 Mac 第一次能用手指點螢幕 | e3w6；open-mac.data | O6、S4 | 200 | CONFIRMED（「Touch for the first time on Mac」） | |
| 6 | Carbon 強在網路安全，是 Google 自己的說法 | 34ue；c-open.data | O1 | 200 | CONFIRMED（已標 Google 自述） | |
| 7 | 找出漏洞、驗證能否被利用、寫出修補 | p6m3；c-open.data.text | O1 | 200 | CONFIRMED（detection, validation, remediation；前一句已歸給 Google） | |
| 8 | Google 說內部團隊看到它一連跑好幾天，在大型程式碼裡做多步驟工程任務 | ke8d、nqyy；c-long.data | O1、O5 | 200 | CONFIRMED（「run for days … across large codebases and low-level systems」） | |
| 9 | 第一批：一部分網路防禦人員，從這一週開始 | 8uhp；c-order.steps[0] | O1 | 200 | CONFIRMED（Starting this week … a subset of cyber defenders） | |
| 10 | 再透過 Fairwind 計畫擴大到更多受信任夥伴 | 33jb；c-order.steps[1].title | O1、O5 | 200 | CONFIRMED（gradually phase access to additional trusted partners） | |
| 11 | Fairwind 受信任夥伴「全球超過 650 個」 | c-order.steps[1].detail | O3、O4 | 200 | CHANGED（650 多個是整個計畫的夥伴數，O3 2026-09-02、O4 今日仍寫 over 650；Carbon 是「逐步」開放給其中更多夥伴，卡片原寫法像 650 個都拿到 Carbon） | 「全球超過 650 個」→「逐步開放；計畫夥伴 650 多個」 |
| 12 | 最後才輪到開發者、企業、一般消費者 | eyn8；c-order.steps[2] | O1 | 200 | CONFIRMED | |
| 13 | c-order 卡片來源「Google、Google DeepMind 2026-10-28」 | c-order.data.source | O1、O3、O4 | 200 | CONFIRMED（O1 是 10-28；650 的數字出自 O3 9-02 與 O4，見「懷疑但沒改」） | |
| 14 | 一般人何時能用 Google 沒給日期；先收集回饋、調整防護，再盡快開放 | 24mt、hkip；c-when.data | O1、O2 | 200 | CONFIRMED（「as soon as possible」「soon」，沒有日期） | |
| 15 | 導入期跟兩週前推出的 Argon 同價 | ehud；c-price.source | O1 | 200 | CONFIRMED（Argon launched two weeks ago；same introductory price） | |
| 16 | 每百萬 token 輸入 2 美元、輸出 10 美元；導入期後 4 美元、20 美元；旁白「都變成兩倍」 | t8i5；c-price.rows | O1 | 200 | CONFIRMED（2→4、10→20，正好兩倍） | |
| 17 | 財報會議上 Google 說 Gemini 應用程式 10 億使用者 | cbmk；c-users.stats[0] | O2 | 200 | CONFIRMED（「The Gemini app is now at one billion users」，已標自述） | |
| 18 | Alphabet 營收年增 25% | c-users.stats[1] | O2 | 200 | CONFIRMED（grew 25% year-over-year，自述） | |
| 19 | Google Cloud 營收成長 103% | c-users.stats[2] | O2 | 200 | CONFIRMED（grew 103%，O2 沒寫比較基期，卡片也沒寫「年增」，正確） | |
| 20 | 這些都是 Google 自己的說法，還沒有第三方確認 | u8jx | O2、S3 | 200 | CONFIRMED（談話稿；S3 註明無第三方確認） | |
| 21 | 你手機上的 Gemini 現在不是 Carbon | 6i4n；c-you.data | O1、O2 | 200 | CONFIRMED（推論：消費者尚未開放；卡片 sub「Carbon 先給受邀的網路防禦人員」對） | |
| 22 | 不用去找下載，不要點來路不明的連結 | j78y；c-you2.data | O1 | 200 | CONFIRMED（頻道建議，依 #14） | |
| 23 | SEC-bench Pro 88.2%、ExploitGym 54.8%、CWE-bench 71.0%（Google 公布） | c-watch.data.sub | O1 | 200 | CONFIRMED（evaluated without guardrails） | |
| 24 | 要看何時開放給開發者、跑分有沒有第三方重測 | zayn、jsdi | — | — | OUT OF SCOPE（觀點與待觀察事項） | |
| 25 | Apple 同一天發表新款 MacBook Pro | 57h2；m-open | O6 | 200 | CONFIRMED | |
| 26 | 發表當天開放預購（10/28），11 月 6 日開始供貨 | c2te；m-open.stats[0..1] | O6 | 200 | CONFIRMED（pre-order starting today, October 28；Friday, November 6） | |
| 27 | 美國起價 US$2,899，14 吋 M5 Pro | wpub；m-open.stats[2] | O6 | 200 | CONFIRMED | |
| 28 | 首批包含美國在內的 30 個國家與地區 | ad6d；m-open.stats[3] | O6 | 200 | CONFIRMED（30 countries and regions, including the U.S.） | |
| 29 | Apple 新聞稿沒有列出是哪些國家；台灣上市日期與售價未公布 | 8dhz、jm8d；m-tw.data | O6 | 200 | CONFIRMED（O6 只寫 30 countries and regions, including the U.S.，全文沒有 Taiwan；沒有猜台灣價格或日期） | |
| 30 | Mac 第一次支援觸控螢幕 | dayw；m-touch | O6 | 200 | CONFIRMED | |
| 31 | 「以前的 Mac：螢幕不能點」 | m-touch.left | O6 | 200 | CONFIRMED（由 #30 推出） | |
| 32 | 系統把觸控轉成滑鼠點擊，很多現有 App 不用更新就能用 | pw8p；m-touch.right | O6 | 200 | CONFIRMED（「many existing apps work with Touch right away, because macOS automatically translates touches into clicks」） | |
| 33 | 兩層自己會發光的像素疊在一起（tandem OLED） | dq7p；m-screen.text | O6、S4 | 200 | CONFIRMED（O6：tandem OLED；「兩層」的白話解釋出自 S4） | |
| 34 | Dynamic Island 搬到 Mac | p4rg；m-screen | O6 | 200 | CONFIRMED | |
| 35 | 峰值亮度 2000 尼特、續航最長 24 小時（Apple 自述） | m-screen.sub | O6 | 200 | CONFIRMED（up to 2000 nits peak HDR and SDR；up to 24 hours） | |
| 36 | 亮度、續航、「全球最好的筆電螢幕」都是 Apple 的說法 | rzdt；m-claims | O6 | 200 | CONFIRMED（「the world's best laptop display」） | |
| 37 | 要不要買，等獨立評測和台灣價格 | 2iiy | — | — | OUT OF SCOPE（建議；沒有推薦買或不買） | |
| 38 | 微軟交出的監管文件給了一個數字 | rgcw；ms-open.source | O8 | 200 | CONFIRMED（the company said in a regulatory filing on Wednesday） | |
| 39 | 兩家越來越常搶同一批客戶 | 2sdn；ms-open.left | O8 | 200 | CONFIRMED | |
| 40 | 這一季 100 億美元營收來自 OpenAI；約占總營收近 11% | 9ufx；ms-open.right | O8 | 200 | CONFIRMED（nearly 11% of $92.3 billion） | |
| 41 | 有營收分成也有使用微軟雲端的部分，各占多少不清楚；TechCrunch 已詢問 | cudy、d248；ms-what.data | O8 | 200 | CONFIRMED（「not clear how much … came from revenue-sharing payments or Azure」） | |
| 42 | 據報 20% 分成比例未獲雙方證實 | ms-what.sub | O8 | 200 | CONFIRMED | |
| 43 | 這是營收，不是獲利 | 93bt；ms-profit | O8 | 200 | CONFIRMED（O8 只說 revenue） | |
| 44 | OpenAI 還欠微軟 72 億美元，是過去交易欠款，不是另一筆營收 | gx3u；ms-profit.sub | O8 | 200 | CONFIRMED（$7.2 billion … not additional revenue） | |
| 45 | 新電腦預裝 Windows 授權加微軟自家裝置，營收比去年少 22% | cwwy；ms-pc.stats[0] | O7、O9 | 200 | CONFIRMED（O7：Windows OEM and Devices revenue decreased 22%；O9：from the year-ago quarter） | |
| 46 | Azure 營收 +48% | ms-pc.stats[1] | O7 | 200 | CONFIRMED | |
| 47 | 成長集中在雲端和 AI 基礎設施 | 86uc；ms-pc.keys | O7、O9、S5 | 200 | CONFIRMED（O9：driven on the strength of Microsoft Cloud；O7：Agents and Infra +25%；見「懷疑但沒改」） | |
| 48 | 你用的 OpenAI 服務有大量跑在微軟雲端 | winz、xwbu；ms-you | O9 | 200 | CONFIRMED（「OpenAI still runs a lot of its services on Microsoft's cloud」） | |
| 49 | 依 2026 年 4 月協議，OpenAI 須在上限內分享營收至 2030 年 | ms-watch.sub | O8 | 200 | CONFIRMED | |
| 50 | 同一天 GitHub 宣布 Copilot Fusion 正式推出，系統替你決定模型 | cm6e、x8ep；g-open | O10 | 200 | CONFIRMED（generally available） | |
| 51 | Standard 日常、High 困難任務與深度推理、Max 最強模型最複雜任務 | 4qn7、43m2；g-open.rows | O10 | 200 | CONFIRMED | |
| 52 | GitHub 說在一項程式代理評比裡 Fusion 得分很接近 Claude Code、成本更低 | 9fip、4ped；g-claim | O10 | 200 | CONFIRMED（Fusion Max 60，within two points of Claude Code with Opus 5.5 Max，about half the average API cost per task；已標 GitHub 自述） | |
| 53 | 限時模型費用 7 折 | g-claim.sub | O10 | 200 | CONFIRMED（30% discount，限付費 Copilot 方案） | |
| 54 | 所有 Copilot 方案可用：VS Code、Copilot app、Copilot CLI、JetBrains IDE | g-try.sub | O10 | 200 | CONFIRMED | |
| 55 | 這是 GitHub 自己公布的結果，要用自己的專案試 | kjn3 | O10 | 200 | CONFIRMED | |
| 56 | 以前公司另外買 Copilot 座位，座位數和用量分開管 | 7pqy；g-ent.left | O11 | 200 | CONFIRMED（how many seats … and how much AI usage） | |
| 57 | 跟業務團隊合作的公司，每個 GitHub Enterprise 授權用戶都能取得 Copilot | 8qq4；g-ent.right | O11 | 200 | CONFIRMED（working with a GitHub or Microsoft account team；Talk to your sales team） | |
| 58 | 改成按 AI 用量的預算付費 | mfex；g-ent.right | O11、O12 | 200 | CONFIRMED（metered from the first request against your enterprise budget） | |
| 59 | 預算用完存取權不收回，自動補全照用 | z499；g-budget | O11 | 200 | CONFIRMED | |
| 60 | Copilot Chat、程式碼審查、雲端 Copilot 要等預算 | h52n；g-budget.sub | O11 | 200 | CONFIRMED | |
| 61 | 公司有 Enterprise 授權，先問 IT 帳戶轉換了沒 | xx5m；g-steps.steps[0] | O11 | 200 | CONFIRMED（頻道建議；O11：talk to your sales team about … transitioning an existing enterprise account） | |
| 62 | 「自己訂閱的還不能用」，未來幾週公布日期 | vrdm；g-steps.steps[1] | O11 | 200 | CHANGED（「Currently unavailable」只指自行管理訂閱的 GitHub Enterprise 客戶，O11 還說 Your current subscription is unaffected；原句會讓個人 Copilot 訂閱者以為自己不能用，而 Fusion 在所有 Copilot 方案都能用） | vrdm「自己訂閱的還不能用，…」→「自助訂閱 Enterprise 的公司還要等，GitHub 說未來幾週公布日期。」；卡片 detail「GitHub 說未來數週公布」→「自助訂閱 Enterprise 者；GitHub 說未來數週公布」 |
| 63 | 想試 Fusion，先把編輯器更新到最新版 | mt77；g-steps.steps[2] | O10 | 200 | CONFIRMED（「Update your client to try it out」；沒有寫選單路徑） | |
| 64 | pull request 是把程式修改合併進專案的提案 | b3hr | S10 | 200 | CONFIRMED（名詞解釋） | |
| 65 | 今年 3 月 AI 代理起草的 PR 17%（不到兩成），9 月超過四成 | n34q、u8nb；g-octo.stats | O13 | 200 | CONFIRMED（「more than 40% … up from 17% in March」；17% 確實不到兩成） | |
| 66 | GitHub 平台資料，偵測為下限 | g-octo.source | O13 | 200 | CONFIRMED（Agent signal … It is a floor） | |
| 67 | 這個數字講的是用了多少，不是寫得多好 | gm5u；g-quality.text | S10 | 200 | CONFIRMED（旁白是頻道推論；S10 寫「不能直接推論程式品質」） | |
| 68 | 卡片 sub「GitHub：模型相關數字描述使用情況，不是品質」 | g-quality.sub | O13 | 200 | CHANGED（O13 的「Figures describe observed use, not model quality」是模型選擇那一節的方法說明，不是講代理起草 PR 的占比；放在這張卡會變成把 GitHub 的話套到另一個數字上） | →「Mokaair 文章：占比不能直接推論程式品質；GitHub 說代理偵測只是下限」 |
| 69 | 第一份草稿越來越常是 AI 寫的，最後要負責的還是審查它的人 | khsw | O12、O13 | 200 | CONFIRMED（O12：Developers … stay accountable for what ships；O13：review is how developers shape what comes back） | |
| 70 | 同一天 The Verge 報導 Instagram 負責人在訪談裡說焦慮和憤怒「不只正在變糟，還會繼續變糟」 | 9aab、ufrn、4mm8；i-open | O14 | 200 | CONFIRMED（引文逐字相符；Colin and Samir podcast） | |
| 71 | Instagram 正開始要求 AI 帳號自我標示，讓人知道內容是真是假 | agi4、8p5h；i-label | O14 | 200 | CONFIRMED（逐字引文） | |
| 72 | 還在研究怎麼處理 AI 假內容；全面禁止 AI 內容不實際 | 3x4h、cmzq；i-limits | O14 | 200 | CONFIRMED（O14：Earlier this month … 「actively working out what to do」「I don't think it's practical … to ban AI content」） | |
| 73 | 不替 AI 創作者另外排序 | i-limits.right | O14 | 200 | CONFIRMED（doesn't rank AI creators differently） | |
| 74 | i-limits 卡片來源「Mosseri 的訪談說法」 | i-limits.source | O14 | 200 | CHANGED（#72 的兩句 The Verge 寫明是本月稍早的說法，不是這場訪談） | 「The Verge 2026-10-28｜Mosseri 的訪談說法」→「The Verge 2026-10-28｜Mosseri 本月的說法」 |
| 75 | 「Do we rank AI content as well as we rank non-AI content? Probably not.」 | 8gdz、m9nr；i-rank | O14 | 200 | CONFIRMED（逐字） | |
| 76 | 名人深偽在 Instagram 上仍是問題（The Verge） | bbfk、zeib；i-deepfake | O14 | 200 | CONFIRMED | |
| 77 | 名人推薦影片先看標示；沒標示不能當真人保證 | 9bq8、992s、fpm7；i-you、i-you2 | O14 | 200 | CONFIRMED（頻道建議，依 #71「AI accounts to label themselves」） | |
| 78 | 同一天 Google 宣布 Chrome 強化自動填入開始從 Gmail 帶資料，由 Gemini 驅動 | ny3q；ch-open | O15 | 200 | CONFIRMED（Starting today … pulled directly from Gmail；Using Gemini with Personal Intelligence） | |
| 79 | 建議填入訂單編號、物流追蹤、航班訂位 | jgmd；ch-open.steps[2] | O15 | 200 | CONFIRMED | |
| 80 | 表單例子「客服、退換貨、旅遊」 | ch-open.steps[0].detail | S12 | 200 | CONFIRMED（出自 S12 的說明；O15 沒有列表單種類，見「懷疑但沒改」） | |
| 81 | 先開放美國；對象是 Chrome 裡用 Gemini 並啟用 Personal Intelligence 的人；桌面、Android、iOS | zcsi、nec3；ch-us | O15 | 200 | CONFIRMED | |
| 82 | 台灣什麼時候開放，Google 還沒講 | vqd6；ch-us | O15 | 200 | CONFIRMED（O15 只有 U.S.；沒有猜台灣時間） | |
| 83 | 它讀的是你的電子郵件內容 | usrd；ch-mail.text | O15 | 200 | CONFIRMED | |
| 84 | Google 說敏感資料會加密 | 4nia；ch-mail.sub | O15 | 200 | CONFIRMED | |
| 85 | 之後還要擴大到 Google 相簿裡的圖片資訊 | 4nia；ch-mail.sub | O15 | 200 | NOT FOUND（O15 今日全文與原始 HTML 都沒有 Photos；頁面 dateModified 2026-10-28T20:21Z，晚於 S12 的 17:19Z，Google 發文後拿掉了這一句） | 4nia「Google 說敏感資料會加密，之後還要擴大到 Google 相簿裡的圖片資訊。」→「Google 說敏感資料會加密，而且由你自己控制。」（O15：you remain in control）；sub「…；之後要擴大到 Google 相簿的圖片資訊」→「Google 說敏感資料會加密，由你在 Chrome 設定裡控制」 |
| 86 | 前提是自己先啟用 Personal Intelligence | awt2；ch-switch.steps[0] | O15、S12 | 200 | CONFIRMED（O15：users with Personal Intelligence enabled） | |
| 87 | 在 Chrome 設定裡決定開不開、能讀哪些內容 | qgrp、e8nn；ch-switch.steps[1..2] | O15 | 200 | CONFIRMED（「manage whether enhanced autofill is enabled and what it can access via your Chrome settings」；卡片只寫「Chrome 設定」，沒有編造選單路徑） | |
| 88 | 同一天 TechCrunch 報導，大信證券 38,490 名客戶個資外洩（三萬八千多名） | ustm；k-open.stats[0] | O16 | 200 | CONFIRMED（according to local news） | |
| 89 | 姓名、電子郵件、手機號碼 | stxw；k-open.stats[1] | O16 | 200 | CONFIRMED | |
| 90 | 未來資產和一家加密貨幣交易所週三各自通報資安事件，都還沒證實資料被偷 | ttwk、pief；k-three | O16 | 200 | CONFIRMED（Mirae Asset Global Investments、Bithumb；on Wednesday, per local media） | |
| 91 | 大約一個月前南韓金融機構才被攻擊過一輪 | h759；k-bg | O16 | 200 | CONFIRMED | |
| 92 | 研究人員把 9 月那波連到疑似在中國的駭客，用 AI 滲透測試工具（Artex）；這次原因還在調查 | chmw、w3bs；k-artex | O16 | 200 | CONFIRMED | |
| 93 | 南韓金融監管機關呼籲加強資安 | g2yg；k-reg | O16 | 200 | CONFIRMED | |
| 94 | 「監管機關」計畫檢查民間幾十個資訊系統 | g2yg；k-reg.kicker、key | O16 | 200 | CHANGED（O16：「The country also plans to conduct security checks on dozens of IT systems in the private sector」，主詞是南韓，不是監管機關） | g2yg「…呼籲加強資安，並計畫檢查…」→「…呼籲加強資安，南韓也計畫檢查民間幾十個資訊系統。」；kicker「南韓金融監管機關」→「南韓監管機關與政府」；key「監管機關：要檢查數十個系統」→「南韓：要檢查數十個系統」 |
| 95 | 大信證券說已通知受影響客戶、正配合調查 | bdmv；k-reg.sub | O16 | 200 | CONFIRMED | |
| 96 | 收到通知先從官方 App 或官網確認、不點信裡連結；確認後改密碼；小心冒充訊息 | 588j、y66e、hy2j；k-you | S13 | 200 | CONFIRMED（「以官方管道確認」出自 S13；其餘是一般防護建議，卡片來源欄已註明「其餘為一般防護建議」；沒有任何設定路徑） | |
| 97 | 我的看法三段 | v-main、v-order、v-unsure | brief.md | — | OUT OF SCOPE（觀點，見下） | |
| 98 | 片尾：問 IT、看標示、確認通知來源 | uc79；closing | — | — | OUT OF SCOPE（對應 #61、#77、#96） | |
| 99 | 縮圖「最強 不給你」「Carbon、MacBook Pro 觸控、微軟收 OpenAI 100 億」 | thumbnail.data | O1、O6、O8 | 200 | CONFIRMED | |
| 100 | 標題「Google 最強模型 Carbon，為什麼先不給你用？｜AI 科技快報 10/28」 | youtube.title | O1 | 200 | CONFIRMED | |
| 101 | 說明欄：排名、跑分、使用者數、成長率是公司自述；台灣首批、售價、Carbon 與 Chrome 在台灣開放時間官方都沒公布；不推薦購買、不示範攻擊 | youtube.description | O1、O2、O6、O15 | 200 | CONFIRMED | |
| 102 | 說明欄 13 個 Mokaair 網址 | youtube.description | S1–S13 | 200 | CONFIRMED（13 篇都 200、已發布） | |
| 103 | tags | youtube.tags | — | — | OUT OF SCOPE | |

## 摘要

- 查了 103 條：CONFIRMED 91、CHANGED 6、NOT FOUND 1、OUT OF SCOPE 5。事實改動 7 處（含 NOT FOUND 刪掉的一句），分布在 6uky、c-order.steps[1]、vrdm 與 g-steps.steps[1]、g-quality.sub、i-limits.source、4nia 與 ch-mail.sub、g2yg 與 k-reg 卡片。
- `sources` 16 個網址 2026-10-29 全部重開為 HTTP 200，`checked_on` 全部改成 2026-10-29；沒有頁面回 403，沒有需要退回站上文章的地方。
- 公司自述：Carbon 的排名與跑分、Gemini 10 億使用者、Alphabet +25%、Cloud +103%、Fusion 的得分與成本、Octoverse 的占比、Apple 的亮度與續航都有標「Google／GitHub／Apple 說」或「自述」，沒有「已獨立證實」的說法。
- 台灣：MacBook Pro 首批名單、台灣上市日與售價、Carbon 與 Chrome 功能在台灣的開放時間都照實說「沒有列出、還沒公布」，沒有猜。
- 操作步驟：Chrome 只寫「Chrome 設定」，GitHub 只寫「更新用戶端」，都是來源原話，沒有編造的選單路徑。南韓那則的「官方 App 或官網、不點連結、改密碼」是一般防護建議，卡片已標明。
- 會過期的事實：Carbon 開放範圍與導入價（O1，Oct 28, 2026；導入期結束日沒公布）；GitHub Enterprise 自助開放日期（O11，「in the coming weeks」）；Fusion 7 折（O10，「for a limited time」，沒有結束日）；MacBook Pro 台灣名單與價格（O6，Oct 28）；Chrome 開放國家（O15，modified 2026-10-28T20:21Z，已經改過一次）。
- 觀點：v-main、v-order、v-unsure 都以「我的看法」「我覺得」「我不確定」標成觀點，與 brief.md〈站主觀點〉一致；沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 2 句——8qq4（47 字，「現在跟業務團隊合作的公司，每個 GitHub Enterprise 授權用戶都能取得 Copilot，」）與 nec3（46 字）；沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後；lint 字典檢查 0 警告（撰稿人新增的字典詞仍未試聽）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261028` → `daily-ai-20261028: 0 errors, 0 warnings`（估計 11.1 分鐘，128 句）。
- 懷疑但沒改：
  - c-order 卡片來源寫「Google、Google DeepMind 2026-10-28」，但 650 的數字出自 O3（2026-09-02）與 O4（無日期）；卡片已改成「計畫夥伴」，日期標記留給協調者決定要不要拆。
  - ms-open 與章名寫「收進 100 億」：O8 說的是認列的營收，同季還有 72 億應收未收；ms-profit 已經講清楚是營收不是獲利，所以沒改。
  - 86uc「成長集中在雲端和 AI 基礎設施」：O9 提醒雲端營收不全是 AI，O7 的部門名稱是 Agents and Infra；說法可接受，沒改。
  - ch-open 的「客服、退換貨、旅遊」是 S12 的舉例，O15 沒有列；卡片來源寫 Google，屬於舉例而非數字，沒改。
  - 7pqy「替每個人買 Copilot 的座位」：O11 只說要管理買了幾個座位，「每個人」略寬，沒改。
  - S12 還寫著 Google 相簿的擴大計畫，O15 已經拿掉；站上文章需要另外開票更正（不在本查核可改的範圍）。
- 需要第二輪：**是**。本輪改了 7 個事實（超過 3 個），照 automated.md 要由另一個代理寫 `verify-2.md`。在第二輪完成前，這份稿子不能稱為已查核。
