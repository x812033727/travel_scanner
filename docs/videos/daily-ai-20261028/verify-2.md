# daily-ai-20261028 查核第 2 輪

查核日 2026-10-29。第二位查核代理，不是撰稿人，也不是第 1 輪的查核代理。
第 1 輪改了 7 個事實（超過 3 個），所以照 `automated.md` 再查一輪。本輪做了兩件事：一是重查第 1 輪改過的每一行，二是用新的眼光把整份稿子再看一遍（超過「已確認項目隨機抽三分之一」的要求）。
今天重新打開的頁面有兩類。站上 13 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.5 秒）全部 HTTP 200。`video.json` `sources` 列的 16 個官方頁或報導（間隔超過 1 秒）也全部 HTTP 200，沒有轉址，也沒有被擋。
來源代號沿用 `verify-1.md`：站上文章是 S1–S13，官方頁與報導是 O1–O16。

## 一、第 1 輪改過的 7 處（全部重查）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 微軟一季 100 億美元營收「來自越來越像對手的 OpenAI」 | 6uky | O8、S6 | 200 | CONFIRMED。O8 寫「even as they increasingly compete for the same customers」，quarter ended September 30，數字出自 regulatory filing on Wednesday。第 1 輪的改法忠於原文。 | |
| R2 | 卡片寫「逐步開放；計畫夥伴 650 多個」 | c-order.steps[1].detail | O1、O3、O4、S1 | 200 | CONFIRMED。O1：「gradually phase access to additional trusted partners through our Fairwind Program」。O3（Sep 02, 2026）：「more than 650 participating partners globally」。O4 今天仍寫「over 650 partners globally」，而且講的是 Argon 的存取。卡片已經不再暗示 650 個夥伴都拿到 Carbon。 | |
| R3 | 卡片來源「Google、Google DeepMind 2026-10-28」 | c-order.data.source | O1、O3、O4 | 200 | CHANGED（第 1 輪留給協調者決定的一項）。650 這個數字掛著 10-28 的日期，可是它出自 Fairwind 計畫頁：O3 是 2026-09-02，O4 沒有日期。只有順序（O1）是 10-28 的說法。 | 「Google、Google DeepMind 2026-10-28」→「Google 2026-10-28｜夥伴數：Google Fairwind 計畫頁」 |
| R4 | 「自助訂閱 Enterprise 的公司還要等，GitHub 說未來幾週公布日期」；卡片 detail「自助訂閱 Enterprise 者；GitHub 說未來數週公布」 | vrdm、g-steps.steps[1] | O11、S9 | 200 | CONFIRMED。O11：「If you manage your own subscription: Currently unavailable … will share dates in the coming weeks. Your current subscription is unaffected.」主詞是自行管理 GitHub Enterprise 訂閱的客戶，不是個人 Copilot 訂閱者。改過的句子不再讓個人訂閱者以為自己不能用。 | |
| R5 | 卡片 sub「Mokaair 文章：占比不能直接推論程式品質；GitHub 說代理偵測只是下限」 | g-quality.sub | O13、S10 | 200 | CONFIRMED。O13 的「Figures describe observed use, not model quality」確實在 Methodology › Model choice 底下，第 1 輪說得對。「It is a floor」在 Glossary › Agent signal。S10 寫著「不能直接推論程式品質」。歸屬正確。 | |
| R6 | 卡片來源「The Verge 2026-10-28｜Mosseri 本月的說法」 | i-limits.source | O14 | 200 | CONFIRMED。「actively working out what to do」與「I don't think it's practical … to ban AI content」是 O14 說的「Earlier this month」。「doesn't rank AI creators differently」與自我標示出自這場 podcast（Oct 28）。兩者都在 10 月，「本月」涵蓋得到。 | |
| R7 | 「Google 說敏感資料會加密，而且由你自己控制。」；卡片 sub「Google 說敏感資料會加密，由你在 Chrome 設定裡控制」 | 4nia、ch-mail.sub | O15、S12 | 200 | CONFIRMED。O15：「sensitive data is encrypted and you remain in control. You can manage whether enhanced autofill is enabled and what it can access via your Chrome settings.」今天的 O15 原始 HTML 裡「Photos」出現 0 次。dateModified 是 2026-10-28T20:21:02Z，datePublished 是 17:00Z。S12（17:19Z）還寫著 Google 相簿的擴大計畫，所以第 1 輪刪掉這句是對的。 | |
| R8 | 「南韓金融監管機關已經呼籲加強資安，南韓也計畫檢查民間幾十個資訊系統。」；kicker「南韓監管機關與政府」；key「南韓：要檢查數十個系統」 | g2yg、k-reg | O16、S13 | 200 | CONFIRMED。O16：「South Korea's financial regulator has called for stronger cybersecurity measures … The country also plans to conduct security checks on dozens of IT systems in the private sector.」S13 把檢查也歸給監管機構，但官方報導寫的主詞是 the country，以來源為準。 | |

## 二、全片重看（第 1 輪標 CONFIRMED 的項目）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Google 10 月 28 日發表 Gemini 4 Carbon，稱是自家最強模型 | 3ywc；open | O1 | 200 | CONFIRMED（「our strongest model」，Oct 28, 2026） | |
| 2 | 強項是找出、驗證、修補漏洞，屬 Google 自述 | 34ue、p6m3；c-open | O1 | 200 | CONFIRMED（vulnerability detection, validation, and remediation） | |
| 3 | Google 說內部團隊看到它一連跑好幾天，處理大型程式碼裡的多步驟工程任務 | ke8d、nqyy；c-long | O1 | 200 | CONFIRMED（run for days … across large codebases） | |
| 4 | 第一批是一部分網路防禦人員，從本週開始；最後才輪到開發者、企業、消費者 | 8uhp、eyn8；c-order | O1 | 200 | CONFIRMED | |
| 5 | 卡片 sub「Google：Carbon 先給受邀的網路防禦人員」 | c-you.sub | O1、O2 | 200 | CHANGED。卡片寫成「Google：」的話，但 Google 沒有說「受邀」。O1 用「a subset of cyber defenders」，O2 用「a subset of trusted cyber defenders」。 | 「Google：Carbon 先給受邀的網路防禦人員」→「Google：Carbon 先給受信任的網路防禦人員」；claims.md c13 跟著改 |
| 6 | 沒有給一般人日期；先收集回饋、調整防護，再盡快開放 | 24mt、hkip；c-when | O1 | 200 | CONFIRMED（as soon as possible，沒有日期） | |
| 7 | 導入期與兩週前推出的 Argon 同價：2／10 美元；導入期後 4／20 美元；旁白說「都變成兩倍」 | ehud、t8i5；c-price | O1 | 200 | CONFIRMED（「will launch at the same introductory price as Argon at $2 … $10」，「After the introductory period expires … $4 … $20」，正好兩倍） | |
| 8 | Gemini 應用程式 10 億使用者、Alphabet +25%、Cloud +103%，都是 Google 自述 | cbmk、u8jx；c-users | O2 | 200 | CONFIRMED（逐字相符，卡片與旁白都標了 Google 自述） | |
| 9 | SEC-bench Pro 88.2%、ExploitGym 54.8%、CWE-bench 71.0%，Google 公布 | c-watch.sub | O1 | 200 | CONFIRMED | |
| 10 | 預購 10/28、11/6 供貨、美國起價 US$2,899（14 吋 M5 Pro）、首批 30 個國家與地區 | c2te、wpub、ad6d；m-open | O6 | 200 | CONFIRMED（「starting today, October 28 … 30 countries and regions, including the U.S.」「Friday, November 6」「14-inch … featuring M5 Pro starts at $2,899 (U.S.)」） | |
| 11 | 新聞稿沒有列國家；台灣日期與售價未公布 | 8dhz、jm8d；m-tw | O6 | 200 | CONFIRMED（全文沒有 Taiwan，也沒有國家名單；稿子沒有猜台灣的日期或價格） | |
| 12 | Mac 第一次支援觸控；觸控轉成點擊，很多現有 App 直接能用 | dayw、pw8p；m-touch | O6 | 200 | CONFIRMED（「Touch capabilities on the Mac for the first time」「macOS automatically translates touches into clicks」） | |
| 13 | 兩層發光像素疊在一起、Dynamic Island、2000 尼特、24 小時，以及 Apple 說的「全球最好」 | dq7p、p4rg、rzdt；m-screen、m-claims | O6、S4 | 200 | CONFIRMED（tandem OLED、「world's best laptop display」，都標了 Apple 自述） | |
| 14 | 100 億美元、約占總營收近 11%、各部分比例不清楚、20% 未證實、72 億是過去的欠款、2026 年 4 月協議分享營收到 2030 年 | 9ufx、cudy、d248、gx3u；ms-open、ms-what、ms-profit、ms-watch | O8 | 200 | CONFIRMED | |
| 15 | Windows OEM 與裝置 −22%、Azure +48% | cwwy；ms-pc | O7、O9 | 200 | CONFIRMED（O7：「Windows OEM and Devices revenue decreased 22%」「Azure revenue increased 48%」；O9：比較基期是 year-ago quarter） | |
| 16 | OpenAI 有大量服務跑在微軟雲端 | winz、xwbu；ms-you | O9 | 200 | CONFIRMED（「OpenAI still runs a lot of its services on Microsoft's cloud」） | |
| 17 | Fusion 正式推出；Standard／High／Max；成本約一半（GitHub 自述）；限時 7 折；四種用戶端可用；更新用戶端再試 | cm6e–43m2、9fip、4ped、kjn3、mt77；g-open、g-claim、g-try、g-steps[2] | O10 | 200 | CONFIRMED（「within two points of Claude Code with Opus 5.5 Max … about half the average API cost per task」「30% discount」「Update your client to try it out」） | |
| 18 | Enterprise 授權用戶取得 Copilot；用量從第一次請求起就計費；補全照用，Chat、審查、雲端 Copilot 要等預算 | 8qq4、mfex、z499、h52n；g-ent、g-budget | O11 | 200 | CONFIRMED | |
| 19 | 3 月 17%、9 月超過四成 | n34q、u8nb；g-octo | O13 | 200 | CONFIRMED（「more than 40% … up from 17% in March」） | |
| 20 | 最後要負責的，還是審查它的人 | khsw | O12 | 200 | CONFIRMED（「stay accountable for what ships」） | |
| 21 | Mosseri 的引文、自我標示、排序的回答、名人深偽仍是問題 | 9aab–4mm8、agi4、8p5h、8gdz、m9nr、bbfk、zeib；i-open、i-label、i-rank、i-deepfake | O14 | 200 | CONFIRMED（引文逐字相符；podcast 是 Colin and Samir） | |
| 22 | Chrome 從今天起從 Gmail 帶資料，由 Gemini 驅動；訂單、物流、航班；先開放美國的 Personal Intelligence 使用者，桌面、Android、iOS | ny3q–nec3；ch-open、ch-us | O15 | 200 | CONFIRMED | |
| 23 | 大信證券 38,490 名客戶的姓名、電子郵件、手機外洩；未來資產與 Bithumb 週三通報、未證實資料被偷；約一個月前的那一波；Artex；大信已通知客戶並配合調查 | ustm–bdmv；k-open、k-three、k-bg、k-artex、k-reg.sub | O16 | 200 | CONFIRMED | |
| 24 | 縮圖、標題、說明欄 | thumbnail、youtube | O1、O6、O8、S1–S13 | 200 | CONFIRMED（13 個 Mokaair 網址都回 200、已發布；公司自述與台灣未公布的事項都寫明了） | |

## 摘要

- 查了 32 條：第 1 輪改過的 8 項（7 處事實，外加它留給協調者決定的卡片來源欄），再加上全片重看的 24 條。CONFIRMED 30 條，CHANGED 2 條，NOT FOUND 0 條。
- 改動 2 處，都是卡片上的歸屬，旁白一句都沒動：
  - c-order.data.source：「Google、Google DeepMind 2026-10-28」→「Google 2026-10-28｜夥伴數：Google Fairwind 計畫頁」。
  - c-you.sub：「Google：Carbon 先給受邀的網路防禦人員」→「Google：Carbon 先給受信任的網路防禦人員」，claims.md c13 跟著改。
- 第 1 輪的 7 處修改：全部對照今天的官方頁確認是對的，沒有退回任何一處。
- 公司自述：Carbon 的跑分、Gemini 10 億使用者、Alphabet 與 Cloud 的成長率、Fusion 的得分與成本、Octoverse 的占比、Apple 的亮度、續航與「全球最好」，都還標著是誰說的。
- 台灣：沒有任何一句猜台灣的開放時間或價格。
- 操作步驟：只有「Chrome 設定」與「更新用戶端」，都是來源原話。
- 會過期的事實：
  - Carbon 的開放範圍與導入價（O1，Oct 28, 2026；導入期哪天結束沒有公布）。
  - Fusion 的限時 7 折（O10，沒有結束日）。
  - GitHub Enterprise 自助訂閱的開放日期（O11，「in the coming weeks」）。
  - MacBook Pro 的台灣名單與價格（O6，Oct 28）。
  - Chrome 開放的國家（O15，dateModified 2026-10-28T20:21Z）。
  - Fairwind 夥伴數（O4 沒有日期，今天寫 over 650）。
- 觀點：v-main、v-order、v-unsure 都標成觀點，也跟 brief.md〈站主觀點〉一致，沒有不一致的地方。
- 聽眾檢查（只報告）：超過 40 字的句子與第 1 輪相同，是 8qq4 與 nec3 兩句；改過的 g2yg 在 40 字以內。沒有查證式旁白，沒有括號或網址，也沒有提前揭曉。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261028` → `daily-ai-20261028: 0 errors, 0 warnings`。
- 懷疑但沒改：
  - 站上文章 S12 還寫著 Google 相簿的擴大計畫，O15 已經拿掉。S13 把「檢查數十個系統」歸給監管機構，O16 的主詞是南韓。這兩篇站上文章需要另外開票更正，不在本查核能改的範圍。
  - 7pqy「替每個人買 Copilot 的座位」比 O11 的「how many seats」略寬，第 1 輪也提過，沒改。
  - 同一頁 Newsroom 的相關稿列了 10-27 另一款「14-inch MacBook Pro with M6」。稿子講的是 10-28 的 PROLED XDR 機種，起價 2,899 美元是指這一款，沒有混用。
- 需要第三輪：否。本輪改了 2 處，不超過 3 處，而且都只是卡片歸屬。在第二輪範圍內，這份稿子已經查核完成。
