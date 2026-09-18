# 科技（非 AI）候選：2026-09-16 至 2026-09-18

前期研究，查核日 **2026-09-18**。收錄範圍是 **2026-09-16 00:00 UTC 之後發布**的項目，
每一則都開原文頁讀到正文才算候選（狀態碼與 bytes 記在下面）。
範圍與界線見 [`tech.md`](tech.md)，來源規則見 [`BRIEF.md`](BRIEF.md)；
9/16 之前的候選在 [`candidates-tech-and-ai.md`](candidates-tech-and-ai.md)，本頁不重複。

所有請求都用 `curl -sL -A "Mokaair-editorial"`，沒有任何請求帶入個人資料。

---

## 掃過的管道與結果

判準照 `BRIEF.md`：**看 `<item>`／`<entry>` 數與最新一筆日期，不看狀態碼。**

| 管道 | 位址 | 取得狀況（2026-09-18） | 視窗內有幾則 |
| --- | --- | --- | --- |
| Apple Newsroom | `www.apple.com/newsroom/rss-feed.rss` | ✅ Atom，20 筆，最新 2026-09-16T13:59:28.902Z | **1**（攝影展，非科技新聞） |
| Apple Developer | `developer.apple.com/news/rss/news.rss` | ✅ 145 筆，最新 2026-09-16T17:03:39Z | **3** |
| Windows | `blogs.windows.com/feed/` | ✅ 10 筆，最新 **2026-09-14** | 0 |
| Windows 各子站 | `windows-insider`／`windowsexperience`／`msedgedev`／`windowsdeveloper`／`devices` 的 `/feed/` | ✅ 全部 200（insider 300 筆、其餘各 10 筆），最新分別 09-11／09-08／09-08／09-14／09-14 | 0 |
| NVIDIA | `nvidianews.nvidia.com/releases.xml` | ✅ 20 筆，最新 2026-09-17T13:00:55Z | **4**（全部偏 AI 基礎設施） |
| Google | `blog.google/rss/` | ✅ 20 筆，最新 2026-09-17T20:00Z | 11 則，其中**非 AI 主體者 1** |
| Google 子站 | `products-and-platforms`／`android`／`chrome`／`pixel` 的 `/rss/` | ✅ 各 20 筆，最新 09-16／09-10／09-10／09-15 | 0（Pixel、Android、Chrome 視窗內無新文） |
| Meta Engineering | `engineering.fb.com/feed/` | ✅ 9 筆，最新 **2026-09-03** | 0 |
| IETF Blog | `www.ietf.org/blog/feed/` | ✅ 598 筆，最新 **2026-09-11**（且多為組織事務） | 0 |
| 數位發展部 | `moda.gov.tw/press/press-releases/372` | ✅ 200、109,447 bytes，伺服器端算繪，最新 2026-09-17 | **2** |
| 中華電信 | `cht.com.tw/zh-tw/home/cht/messages` | ✅ 200、179,446 bytes，伺服器端算繪，頁面自稱 3,957 項 | **10**（實質 2） |
| 歐盟執委會（數位） | `digital-strategy.ec.europa.eu/en/news` | ✅ 200、69,094 bytes，13 篇列表 | **3** |
| ENISA | `www.enisa.europa.eu/news` | ✅ 200、85,190 bytes，最新 **2026-09-11**（CRA 單一通報平台，站上已寫） | 0 |
| 台灣 NCC | `ncc.gov.tw` | ❌ **整站是 Angular 外殼**，任何路徑（含 `robots.txt`、`sitemap.xml`）都回同一份 536 bytes 的 `<app-root>`，curl 取不到任何內容 | 未查到 |
| 行政院公報（NCC 替代管道） | `gazette.nat.gov.tw` | ⚠️ 可用但有前提，見下 | **0 則 NCC** |
| EUR-Lex（ELI） | — | — | 視窗內沒有任何可用 ELI 位址（KIDS Act 是提案，尚無 ELI） |

### 這一輪新踩到的四個坑，寫給下一個代理

1. **歐盟 press corner 的網頁是 Angular 外殼。**
   `ec.europa.eu/commission/presscorner/detail/en/ip_26_1890` 回 **200、21,967 bytes**，
   但 `<title>` 只有 `Press corner | European Commission`，去標籤後剩 34 個字。
   全文要走列印端點：
   `ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_26_1890/IP_26_1890_EN.pdf`
   （200、87,640 bytes、3 頁，pypdf 抽出 7,545 字）。
   **同一個端點對 factsheet `fs_26_1891` 回 404**，所以那份 factsheet 沒有讀到、也沒有引用。
   另外 `digital-strategy.ec.europa.eu/en/news-redirect/rss.xml` 回 **500**，要改抓 `/en/news` 列表頁。

2. **中華電信的新聞稿不在 sitemap 裡。**
   `robots.txt` 指向 `cht.com.tw/home/eshop/sitemap/sitemap.xml`（200、721,522 bytes、6,829 個 `<loc>`），
   但裡面 4,893 個 `/messages/` 網址幾乎全是 HiNet 維護公告，新聞稿沒有逐筆列出。
   `/zh-tw/home/cht/messages/news` 回 **404**（body 卻有 139,959 bytes 的軟性 404）。
   **可用的是 `/zh-tw/home/cht/messages` 索引頁**：伺服器端算繪，每則是一個
   `div.list-item`，帶 `message-id`、標籤（新聞稿／重要公告／業務訊息，子標籤 公司／業務／財務／人資／ESG）、
   `h3.list-item-head` 與 `div.list-item-date`，內頁位址是 `/zh-tw/home/cht/messages/<年>/<MMDD-HHMM>`。

3. **行政院公報的日期參數要帶 cookie 才生效。**
   `browseVolume.do?action=doSearch&pubdate=YYYY-MM-DD` 在**沒有 session cookie** 時
   三個不同日期都回同一期（最新期），翻頁的 `action=doChangePage&pageNum=N` 也一樣。
   帶 `-c/-b` cookie jar 之後才正確。實測結果：
   2026-09-16 是第 032 卷第 173 期（33 筆、4 頁）、2026-09-17 是第 174 期（27 筆、3 頁）、
   **2026-09-18 回「共0筆資料」（查核當下尚未出刊）**。
   逐筆看過 60 筆，**沒有任何國家通訊傳播委員會的項目**。
   另外 `advancedSearchResult.do` 不論 GET 或 POST 都回 `error code：0001`，別再花時間。

4. **Apple 同一段話在兩個官方頁的空白字元不一樣。**
   ATT 那段話在 `developer.apple.com/news/?id=idsft9ai` 有四個不斷行空格
   （`European Union`、`iOS 27.2`、`iPadOS 27.2`、`and Romania.`），
   在 `developer.apple.com/app-store/user-privacy-and-data-use/` 卻全是一般空格。
   訂閱那則的正文更多（`Volume Purchasing`、`Group Purchases`、`App Store Connect`、
   `Bundles and Suites`、`StoreKit 2`、`or later`）。
   **用純 ASCII 空格去搜會零筆，不等於原文沒有這句話。**
   另外 `developer.apple.com/tw/news/?id=<id>` 對這三則都回 **404**，Apple 沒有發布繁中版。

---

## 候選清單

| 日期 | 標題 | 來源狀態 | 建議 | 與既有文章重疊 | 研究紀錄／不寫的理由 |
| --- | --- | --- | --- | --- | --- |
| 2026-09-17 | EU KIDS Act to restrict social media platforms' access to children in the EU | ✅ 執委會新聞頁 200／49,928 B；IP/26/1890 PDF 200／87,640 B；Q&A 200／68,346 B；提案頁 200／53,786 B | **重要** | 無 | `research/tech-news-eu-kids-act-20260917.json` |
| 2026-09-18 | 中華電信完成「臺馬第四海纜」建設　建構三路由備援　全面強化馬祖通訊韌性 | ✅ 200／154,303 B | **重要** | 接續 `tech-news-taiwan-matsu-cable-20260623`（不同事件） | `research/tech-news-taiwan-matsu-cable-tm4-20260918.json` |
| 2026-09-16 | Updates to App Tracking Transparency in the European Union | ✅ 200／106,682 B＋隱私說明頁 200／131,579 B | **重要** | 與 `tech-news-apple-eu-business-terms-20260818` 同屬 Apple 歐盟，主題不同 | `research/tech-news-apple-att-eu-20260916.json` |
| 2026-09-16 | Get your subscriptions ready for iOS 27 | ✅ 200／117,728 B＋組合方案頁 200／115,481 B＋說明頁 200／370,868 B | 次要（可升重要） | 無 | `research/tech-news-app-store-bundles-multiseat-20260916.json` |
| 2026-09-17 | 申辦就學貸款免奔波！ 數發部MyData線上一鍵備齊戶籍資料 | ✅ 200／87,313 B＋MyData 首頁 200／199,165 B | 次要 | 無 | `research/tech-news-moda-mydata-student-loan-20260917.json` |
| 2026-09-16 | 中華電信GSN IDC新機房啟用攜手打造政府數位韌性新里程碑 | ⚠️ 200／153,184 B，但**只有一條一手來源** | 次要（補來源前不可動筆） | 無 | `research/tech-news-taiwan-gsn-idc-20260916.json` |
| 2026-09-17 | EU and Korea deepen cooperation on secure satellite connectivity | ✅ 200／49,645 B | 次要（備選） | 無 | 不寫：這是一份行政安排的簽署，IRIS² 第一階段官方寫「排定 2029 年底前發射」，對台灣讀者只剩「低軌衛星備援」這個間接連結；同批次已有臺馬海纜寫同一個主題且更近。留給下一輪 |
| 2026-09-16 | NVIDIA Vera Rubin NVL72 Delivers Leading Performance in MLPerf Inference v6.1 Debut | ✅ 200／118,710 B | 次要（備選） | **高度重疊** `tech-news-nvidia-vera-rubin-20260915`（同一代平台，差一天） | 不寫：全篇是 NVIDIA 自己的效能宣稱（3.7x、2.5x、99%、1.6x、30x），主體是 AI 推論效能，照 `tech.md` 應歸 AI 垂直；而且站上 9/15 那篇才寫過 Vera Rubin |
| 2026-09-16 | Emerald AI, Google and NVIDIA Launch Alliance to Advance Flexible AI Data Centers | ✅ 200／110,377 B | 不寫 | 無 | 全文零數字、零日期、零成員名單，範圍明寫是美國電網；`tech.md` 要的是「具名、可查」的題目，這則給不出來 |
| 2026-09-16 | 3 new ways we're improving Search profiles for publishers | ✅ 200／357,942 B | 不寫 | 無 | 唯一的具體門檻（YouTube／Instagram／X／TikTok 合計 10,000 名追蹤者）明寫只給美國創作者與出版者；對台灣一般讀者沒有適用性 |
| 2026-09-16 | 林宜敬部長率團訪美華府 從AI到資安深化臺美數位韌性合作 | ✅ 200／94,081 B | 次要（備選，跨垂直） | 與 `tech-news-taiwan-sovereign-ai-corpus-20260915` 部分重疊（主權 AI、模型評測） | 不寫：主體是 AI 政策與外交，照 `tech.md` 的分界應由 AI 垂直評估。可用的硬事實只有數發部說的「臺灣每日面臨約 260 萬次網路攻擊」一句，且未附統計期間與方法 |
| 2026-09-16 | Get ready with the latest beta releases（Apple Developer） | ✅ 200／108,122 B | 不寫 | 與 `tech-news-iphone-duo-20260909` 重疊 | 主體是 iOS/iPadOS/macOS/tvOS/visionOS/watchOS 27.2 beta。**唯一有新聞價值的一句已記下**：iPhone Duo 於 10 月 23 日上市時將搭載 **iOS 27.1**（不是 27.0 或 27.2），Xcode 27.1 才會加入 iPhone Duo 的開發支援。建議把這句補進既有的 iPhone Duo 那篇，不要另開一篇 |
| 2026-09-16 | Celebrating "What Holds Us" on iPhone 18 Pro（Apple Newsroom） | ✅ feed 已確認 | 不寫 | — | 攝影展宣傳，不是科技新聞 |
| 2026-09-17 | Cute Critters Come to the Cloud: 'Aniimo' Launches on GeForce NOW | ✅ feed 已確認 | 不寫 | — | GeForce NOW 每週片單 |
| 2026-09-16 | University of Manchester Uses NVIDIA Earth-2 to Forecast Air Pollution Across the UK | ✅ feed 已確認 | 不寫 | — | AI 應用案例，主體是模型不是硬體 |
| 2026-09-16 | Commission welcomes the design of first Important Project of Common European Interest in AI | ✅ 列表頁已確認 | 不寫（轉 AI 垂直） | — | 主體是 AI 產業政策 |
| 2026-09-17 | European Citizens' Panel on Democratic Resilience | ✅ 列表頁已確認 | 不寫 | — | 不是科技題目 |
| 2026-09-16 至 09-18 | 中華電信另外 8 則（iPhone 開賣與資費、亞運轉播、漫遊優惠、Hami Point 與 Ponta、網路門市抽獎、兩則 ESG、一則中秋活動） | ✅ 索引頁已確認 | 不寫 | iPhone 相關與 `tech-news-iphone-duo-20260909`／`tech-news-apple-september-hardware-20260909` 重疊 | 資費與優惠屬購買資訊，`tech.md` 禁止做成購買建議；其餘是行銷與公益活動 |
| 2026-09-16／09-17 | 行政院公報第 032 卷第 173、174 期（共 60 筆） | ✅ 帶 cookie 後逐頁讀過 | 不寫 | — | 逐筆檢視 60 筆，**沒有任何 NCC 項目**，也沒有任何通訊傳播相關法規或公告 |

---

## 值得寫的六則：逐則說明

### 1. 歐盟 KIDS Act（2026-09-17）— 建議「重要」

執委會 9 月 17 日在史特拉斯堡通過《EU KIDS Act》提案（EU Keeping Internet Digital Spaces
Accountable and Trustworthy）。內容分四個支柱：禁止社群平台接觸未滿 13 歲兒童、
全歐盟一致把「自行開設帳號」的年齡定在 15 歲、13 到未滿 15 歲由監護人開設受控的
mini account（每日至多一小時、聯絡人須經同意）；對社群、影音、線上遊戲、
AI 陪伴與聊天機器人課以「安全設計」義務（禁無停點的無限捲動、禁 streak 機制、
禁睡眠時段推播，AI 陪伴預設關閉）；要求以零知識證明式的年齡驗證取代自填生日；
並把舉證責任反轉到月活 4,500 萬以上的超大型平台身上，罰則上限全球年營業額 6%。

**對台灣讀者的解釋價值**：台灣不在適用範圍，但被點名的服務類別正是台灣讀者每天在用的。
真正可轉移的是兩件事——「未滿 15 歲」這條線背後的分級設計，以及
「怎麼證明年齡而不暴露身分」這個技術問題。**最容易寫錯的地方是狀態**：
這是提案，已送交歐洲議會與理事會，四份官方文件裡**沒有任何適用日**。

**重疊**：站上 14 篇科技文章沒有任何一篇碰兒少保護或平台責任。
`tech-news-eu-cra-reporting-20260911` 是最好的對照組（已適用 vs 尚未適用）。

### 2. 臺馬第四海纜完工（2026-09-18）— 建議「重要」

中華電信 9 月 18 日宣布全長近 300 公里的臺馬第四海纜完成建置、登陸、測通，
與既有第二、第三海纜形成三路由互為備援；投入近新臺幣 14 億元，
臺馬聯外海纜由兩條增為三條、整體傳輸容量提升至約 1.9 Tbps，
另有 12.6 Gbps 臺馬微波骨幹與低中高軌多元衛星。

**對台灣讀者的解釋價值**：這是本視窗內關聯度最高的一則，而且它替站上一則
未完成的報導收尾——`tech-news-taiwan-matsu-cable-20260623` 停在數發部說「即將於近期完工」。
**要注意三件事**：中華電信叫「臺馬第四海纜」、數發部叫「臺馬四號海纜（TM4）」；
數發部的國內海纜清單同時列著臺馬一到四號共四條，而中華電信只講三路由，
**不可以據此寫臺馬一號已停用**；查核日數發部新聞發布頁還沒有對應公告。

### 3. Apple 調整歐盟的 App 追蹤透明度（2026-09-16）— 建議「重要」

自 iOS 27.2 與 iPadOS 27.2 起，歐盟的開發者可選用另一個版本的 ATT 詢問框
（版面與文字不同，可加一個標示為 Additional Information 的文字按鈕）；
在德國、法國、義大利、波蘭、羅馬尼亞這**五個國家只能用新版**；
歐盟的裝置設定從「Allow Apps to Request to Track」改名為
「Allow Apps to Request to Link Your Activity Across Companies」；
開發者可在使用者上次回答滿一年後再問一次，不論上次是同意或拒絕。

**對台灣讀者的解釋價值**：那個框每個 iPhone 使用者都看過。這則可以同時說明
「那個框到底在問什麼」（Apple 對 tracking 的定義）、「按不允許會怎樣」（廣告識別碼回傳全零），
以及「為什麼同一個 App 在不同地區行為不一樣」。
**最容易寫錯的地方**：Apple 全文沒有提到 DMA，只寫「與部分歐洲競爭主管機關達成協議」與
「法律要求」——和 `tech-news-apple-eu-business-terms-20260818` 完全一樣的陷阱。

### 4. App Store 訂閱可以綁在一起賣（2026-09-16）— 建議「次要」，可升「重要」

Bundles 與 Suites 讓多個訂閱變成一筆 App 內購買，
**多開發者組合最多五個開發者**，同一個組合裡每個訂閱的週期必須相同，
App 要用 StoreKit 2 且支援 iOS 27／iPadOS 27／macOS 27／tvOS 27 起的系統，官方時程是「今年稍晚」。
多人席次（multiseat）**公告當天起在 App Store Connect 預設開啟**，
量購（Volume Purchasing）2026 年 10 月 22 日推出、團體購買（Group Purchases）官方只寫 this winter。
說明頁另有一個分界：2026 年 9 月 14 日前建立、且沒有用 StoreKit 2 或開啟家人共享的訂閱，預設為關閉。

**對台灣讀者的解釋價值**：「一個人、一個 App、一份訂閱」這個模式同時鬆掉了兩個假設。
**官方三頁都沒有寫地區範圍，也沒有提到台灣**，而且多開發者組合的分潤規則完全沒說。

### 5. 數發部 MyData 接上臺灣銀行就學貸款（2026-09-17）— 建議「次要」

115 學年度上學期就學貸款受理到 9 月 30 日。學生在臺灣銀行就學貸款入口網線上申貸時，
可透過 MyData 直接取得內政部戶政司的現戶全戶戶籍資料，官方說法是全面替代該項紙本證明。

**對台灣讀者的解釋價值**：有明確截止日、今天就用得到。
真正值得寫的不是便民本身，而是 MyData 的運作模式：文件不落到使用者手上，
而是經本人同意後由 A 機關直送 B 機關。**限制**：臺灣銀行那一端的官方頁面本次沒有取得，
研究紀錄的 `sourcing_verdict` 標為 `partial`，撰稿前要自己補。

### 6. 中華電信 GSN IDC 新機房（2026-09-16）— 建議「次要」，**補來源前不可動筆**

政府網際服務網的新機房，9 月 15 日舉行落成啟用暨營運授權交接典禮。
自民國 113 年 6 月啟動建置、115 年 6 月完成，各機關自 115 年 7 月起陸續移轉，
中華電信預計 115 年 12 月達 70% 進駐率、116 年全部完成。

**限制**：目前**只有中華電信一方的公告**，不符合 `BRIEF.md` 至少兩條一手來源的要求。
數發部的 GSN 官方頁面本次沒有找到（猜過的 `moda.gov.tw/digital-affairs/digital-service/operations/8265`
回 404，**不可引用**）。沒有金額、沒有地點、沒有規模、沒有機關數。

---

## 讀不到／查不到的事件

- **NCC**：`ncc.gov.tw` 整站回同一份 536 bytes 的 Angular 外殼，
  連 `robots.txt` 與 `sitemap.xml` 都是同一份，curl 完全取不到內容。
  改走行政院公報，2026-09-16 與 09-17 兩期共 60 筆逐筆看過，**沒有 NCC 項目**；
  2026-09-18 查核當下尚未出刊。所以是「**未查到**」，不是「沒有發生」。
- **歐盟 KIDS Act 的 factsheet（FS/26/1891）**：列印端點回 404，沒有讀到，
  研究紀錄裡沒有一條事實來自它。
- **KIDS Act 的提案全文 PDF**：找到網址但**沒有下載**，所以研究紀錄不得引用任何條號。
- **臺灣銀行就學貸款入口網**：數發部新聞稿以文字提及但沒有超連結，本次沒有取得網址。
  照 `BRIEF.md`，猜網址等於捏造，所以沒有寫。
- **數發部的 GSN 頁面**：從已知選單沒有走到，猜的路徑回 404。

## 不確定、需要協調者裁示的地方

1. **第 4 則（App Store 訂閱）要放重要還是次要。** 素材密度足以撐重要，
   但功能尚未對消費者開放，而且官方沒說地區。
2. **第 2 則與既有 `tech-news-taiwan-matsu-cable-20260623` 的分工**，
   研究紀錄裡已經寫死了界線，但這是同一條海纜的第二篇，要不要發由站主決定。
3. **同一天三則 Apple Developer 公告拆兩篇**（ATT 與訂閱）會不會太集中，
   兩篇的第二個 link 也都指向 `tech-news-apple-eu-business-terms-20260818`，需要錯開。
4. **EU-Korea IRIS² 衛星那則**是這一輪最接近門檻的「沒寫」項目。
   如果站主想要第七則，它是首選，但台灣關聯只有間接的低軌衛星備援。
5. **NCC 這條線到現在還是空的。** 本輪找到的替代管道（行政院公報帶 cookie）可用，
   但只涵蓋公報刊登的法規與公告，NCC 的新聞稿與會議決議仍然讀不到。
