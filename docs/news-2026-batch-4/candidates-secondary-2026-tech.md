# 科技（非 AI）次要新聞候選：2026-08-01 至 2026-09-15（台北時間）

批次 4.4 重建版，查核日 **2026-09-23**。
收錄範圍是 **2026-08-01 00:00 至 2026-09-15 23:59 台北時間**
（＝ 2026-07-31T16:00Z 至 2026-09-15T16:00Z）。
事件日一律換算成台北時間；官方只給日期、沒有時間的（Apple Newsroom、
Apple Developer、數發部、TSMC 新聞稿）照官方標示的日期記，不做加減。
只有官方頁面自己印出帶時區的時間戳時才換算，本輪唯一受影響的是 Meta Threads 那則，
見「窗口外」一節。

範圍與界線見 `docs/news-2026-batch-4/tech.md`，來源規則見 `BRIEF.md`，
去重清單是 `published-news-2026-09-23.md`（114 篇，其中 `tech-news-` 27 篇）。
**每一則候選都開原文頁讀到正文才列入**，狀態碼與 bytes 記在下面。

所有請求都用
`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔至少 1 秒，**沒有任何請求帶入任何人的姓名、電子郵件或個人資料**。
輔助腳本在 `_tools/tech/`（`fetch.sh`、`feed.py`、`text.py`、`apple.py`，
以及行政院公報的三個版本——**要用的是 `gazette_full.sh`**，
`gazette.sh`／`gazette50.sh`／`gazette_rest.sh` 是失敗過程，
留著是為了讓下一個代理不要重犯，理由寫在下面第 4 點），
抓下來的原始檔在 `_tools/tech/dl/`。

---

## 掃過的管道與結果

判準照 `BRIEF.md`：**看 `<item>`／`<entry>` 數與最新／最舊一筆日期，不看狀態碼。**
本視窗離查核日有一個半月，**多數 RSS 只留 10–25 筆，整段視窗已經滾出**，
這一欄特別標出「最舊一筆」就是為了讓下一個代理一眼看出哪些管道不能只靠 feed。

| 管道 | 位址 | 取得狀況（2026-09-23） | 視窗內幾則 |
| --- | --- | --- | --- |
| Apple Developer | `developer.apple.com/news/rss/news.rss` | ✅ 200／427,604 B，146 筆，最新 2026-09-18、最舊 2024-09-26 | **16** |
| Apple Newsroom | `www.apple.com/newsroom/rss-feed.rss` | ✅ 200／19,020 B，20 筆，最新 2026-09-22、**最舊 2026-08-18** | **1**（兒少安全 9/14） |
| Apple Newsroom 封存 | `www.apple.com/newsroom/archive/`＋`?page=2`、`?page=3` | ✅ 200／323,106 B、323,959 B、323,211 B。**第 1 頁只到 September 2026，8 月要翻到第 2、3 頁**（共 256 頁） | **9**（8/3 至 9/22） |
| Windows 主站 | `blogs.windows.com/feed/` | ✅ 200／134,262 B，10 筆，最新 09-21、最舊 **09-08** | 7 |
| Windows Experience | `/windowsexperience/feed/` ＋ `/2026/08/`、`/2026/09/` 月封存 | ✅ 200／91,599 B（10 筆）、109,973 B、111,808 B | **3** |
| Windows Developer | `/windowsdeveloper/feed/` | ✅ 200／149,692 B，10 筆，最新 09-14 | 3 |
| Windows Devices | `/devices/feed/` | ✅ 200／166,426 B，10 筆，最新 09-14 | 1 |
| Windows Insider | `/windows-insider/feed/` | ✅ 200／**3,078,373 B，300 筆**，涵蓋 2024-11-08 至 2026-09-21——**這是 Windows 唯一一個真的回得到整段視窗的 feed** | **9** |
| Microsoft Edge Dev | `/msedgedev/feed/` | ✅ 200／94,497 B，10 筆，最新 09-21、最舊 2026-05-20 | **5** |
| Microsoft Learn | `learn.microsoft.com/microsoft-edge/.../manifest-v3`、`/windows/apps/develop/security/age-signals/` | ✅ 200／50,456 B、56,942 B | 2（佐證用） |
| NVIDIA 新聞稿 feed | `nvidianews.nvidia.com/releases.xml` | ✅ 200／44,637 B，20 筆，**最舊 2026-09-10** | 0（整段視窗已滾出） |
| NVIDIA 部落格 feed | `blogs.nvidia.com/feed/` | ✅ 200／264,826 B，18 筆，**最舊 2026-09-10** | 0（同上） |
| NVIDIA 部落格 sitemap | `blogs.nvidia.com/sitemap_index.xml` → `post-sitemap3.xml` | ✅ 200／1,295 B、122,408 B，243 筆 | **51**（lastmod 落在視窗） |
| NVIDIA 新聞封存頁 | `nvidianews.nvidia.com/news`（`?page=2`） | ⚠️ 200／68,968 B、69,485 B，**清單由 JS 算繪，curl 取不到任何一筆** | 讀不到 |
| TSMC 新聞 | `pr.tsmc.com/english/latest-news`、`/english/news-archives` | ✅ 200／187,111 B、196,739 B，列表本身要靠 `href="/english/news/<id>"` 抽，共 9 個 id | **4** |
| ASML | `asml.com/en/news/press-releases` | ⚠️ 200／160,136 B，**只列出「Latest press releases」三則、全部 2026-09-08**，搜尋是 JS 驅動 | **2** |
| Sony Semiconductor Solutions | `sony-semicon.com/en/news/index.html` | ✅ 200／103,245 B，2026 年逐則列出（`/en/news/2026/<YYYYMMDDnn>.html`） | **1** |
| Google | `blog.google/rss/` | ✅ 200／30,046 B，20 筆，**最舊 2026-09-16** | 0（整段視窗已滾出） |
| Chrome Releases | `chromereleases.googleblog.com/feeds/posts/default` | ✅ 200／195,397 B，25 筆，**最舊 2026-09-10** | 0（靠 KEV 的 notes 欄補到 9/3、9/8 兩篇） |
| CISA 公告清單 | `cisa.gov/news-events/cybersecurity-advisories`（`?page=1`、`?page=2`） | ✅ 200／163,893 B、164,928 B、164,770 B | 視窗內 KEV 公告多則 |
| CISA KEV 目錄 | `cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | ✅ 200／1,744,369 B，catalogVersion 2026.09.22，1,721 筆 | **54** |
| CISA advisory feed | `cisa.gov/cybersecurity-advisories/all.xml` | ✅ 200／444,204 B，30 筆，**最舊 2026-09-16** | 0 |
| 歐盟執委會（數位） | `digital-strategy.ec.europa.eu/en/news`（`?page=1`–`3`） | ✅ 200／69,861 B、69,270 B、69,709 B、70,359 B。**無參數那一頁是第 0 頁，`?page=1` 才是第二頁**；兩頁合起來從 09-22 涵蓋到 07-31，第 3 頁已全在視窗前 | **12** |
| 歐盟 press corner 列印端點 | `.../presscorner/api/files/document/print/en/ip_26_1772/IP_26_1772_EN.pdf` | ✅ 200／79,538 B，2 頁，3,277 字 | 1 |
| 數位發展部 | `moda.gov.tw/press/press-releases/372` | ✅ 200／109,339 B，單頁即涵蓋到 2026-07-31，不必翻頁 | **5** |
| 數發部 數位政府 | `moda.gov.tw/digital-affairs/digital-service/354` | ✅ 200／89,891 B | —（找到 GSN 官方站） |
| GSN 政府網際服務網 | `gsn.nat.gov.tw`、`/GSNArticle/Contents?articleId=77` | ✅ 200／56,522 B、53,187 B | —（補 GSN IDC 研究紀錄） |
| 中華電信 | `cht.com.tw/zh-tw/home/cht/messages` | ⚠️ 200／179,281 B，頁面自稱 3,964 項，**但伺服器只算繪最新 10 則**，翻頁與月份篩選是帶 `__RequestVerificationToken` 的 POST | **未取得**（見下） |
| 中華電信 GSN 新聞稿 | `cht.com.tw/zh-tw/home/cht/messages/2026/0916-1830` | ✅ 200／153,013 B（上一輪是 153,184 B） | 1（窗口外，9/16） |
| 行政院公報（NCC 替代管道） | `gazette.nat.gov.tw/egFront/browseVolume.do` | ✅ 200，**視窗 46 天逐日查兩輪**（第二輪逐頁走完 8/1–9/10，見統計） | **1 則 NCC**（9/9，見下） |
| Google | `blog.google/robots.txt` | ✅ 200／153 B，只指向 `blog.google/sitemap.xml`——**那份本輪沒抓，是留給下一輪的缺口** | 未取得 |
| 台灣 NCC | `ncc.gov.tw` | ❌ 未查（整站 Angular 外殼，沿用上一輪結論，本輪沒有再浪費請求） | 未查到 |
| Samsung | `news.samsung.com/global/` | ❌ **curl (56) Recv failure: Connection was reset**，一個位元組都沒拿到 | 讀不到 |
| Wi-Fi Alliance | `wi-fi.org/press-releases` | ✅ 200／169,171 B，9 則，**最新 2026-08-11** | **1** |
| 3GPP | `3gpp.org/news` | ✅ 200／116,271 B，最新 2026-09-16 | 2（皆為組織事務） |
| GitHub changelog | `github.blog/changelog/feed/` | ✅ 200／44,978 B，10 筆，**最舊 2026-09-18** | 0 |
| Meta Newsroom | `about.fb.com/news/2026/09/threads-introduces-parental-supervision-for-teens-in-apac/` | ✅ 200／491,286 B | 1（**窗口外 9 小時**，見下） |

### 這一輪新踩到的六個坑，寫給下一個代理

1. **回頭查一個半月前的窗口，feed 幾乎全都不能用。**
   NVIDIA 兩個 feed、blog.google、Chrome Releases、GitHub changelog、CISA 的
   advisory feed，**最舊一筆都在 2026-09-10 之後**。判「視窗內 0 則」以前
   一定要先看最舊一筆的日期，否則會把「滾出去了」誤記成「沒有發生」。
   可用的替代管道各不相同：NVIDIA 走 `sitemap_index.xml` → `post-sitemap3.xml`
   （243 筆帶 `lastmod`），Windows 走 `/2026/08/`、`/2026/09/` 月封存頁，
   **或直接用 `blogs.windows.com/windows-insider/feed/`——它一個人有 300 筆、
   回得到 2024 年**，本輪的 Windows 11 26H2 就是從它撈到的，
   主站 feed 只有 10 筆完全看不到；
   Chrome 走 **CISA KEV JSON 的 `notes` 欄**（裡面直接印著該 CVE 對應的
   Chrome Releases 網址，不必猜）；Apple Newsroom 走 `archive?page=2`、`?page=3`。

2. **`nvidianews.nvidia.com/news` 的清單是 JS 算繪的。**
   200、68,968 bytes，看起來像成功，但抽不出任何一則新聞稿，只有
   `<select name="year">` 這個篩選器留在 HTML 裡。**這就是「大 body 的軟性失敗」**。
   NVIDIA 官方新聞稿在視窗內只能從 `robots.txt` 列出的 sitemap 反推。

3. **中華電信的索引頁比上一輪更難用。**
   上一輪只要最新幾則，這輪要整段視窗就卡住了：索引頁只算繪最新 10 則，
   翻頁與「全部月份」篩選都是帶 `__RequestVerificationToken` 的 POST，
   頁面裡沒有任何可重現的 GET 端點。猜端點等於捏造，所以本輪
   **中華電信 8/1–9/15 的清單是「未取得」，不是「沒有新聞」**。

4. **行政院公報有三個坑，缺一個就會漏資料。**
   (a) 日期參數要帶 cookie jar（`-c/-b`），否則每個日期都回最新一期——這是上一輪就記過的。
   (b) **分頁數不能從連結抽**：HTML 裡只出現 `doChangePage&pageNum=2`（就是「下一頁」），
   但頁面文字寫的是「共 37 筆資料，**第 1/4 頁**」。照連結抓只會拿到前 20 筆，
   本輪第一次掃描就是這樣漏掉了第 3 頁起的內容。要解析「第 1/N 頁」。
   (c) **頁面自己提供的 `action=doChangeEachpage&eachpage=50` 對後續的 `doSearch` 無效**，
   不能拿來省翻頁。
   (d) **冷 session 的結果不可重現，而且錯得很安靜。**
   實測三種情況：從全新 session 直接問 `pubdate=2026-08-18`，回
   「共 24 筆、第 1/3 頁、52,363 bytes」；同一個日期在循序走過來的 session 裡，
   兩次獨立掃描都穩定回「共 37 筆、第 1/4 頁、50,527 bytes」（逐日逐 byte 一致）；
   另一次冷 session 循序掃，第一天 2026-08-01 回「共 24 筆」，而另兩輪都回「共 0 筆」。
   **「共 24 筆資料，第 1/3 頁」就是日期沒有生效的特徵值**——看到它要起疑，
   不要當成那天真的只有 24 筆。
   目前可行的做法：開首頁 → 丟掉一個 `doSearch` 當暖機 → 從區間第一天依序走完，
   **中途不可續掃、不可跳日期，而且結論要用兩次獨立掃描互相核對**。
   可重複執行的腳本是 `_tools/tech/gazette_full.sh`，逐日紀錄留在 `dl/gzf-sweep.txt`
   與 `dl/gz-sweep.txt`，兩份可以直接對。

5. **Apple 同一週的兩則官方公告，Rosetta 的說法不一樣。**
   9/1 的 `?id=w5ngl9k2` 寫「macOS 27：最後一個支援 Rosetta 的版本」；
   9/9 的 `?id=k1mtkt1k` 寫「macOS 26 是最後一個支援 Intel Mac 與 Rosetta 的版本，
   macOS 27 只支援 Apple silicon」。**兩句話擺在一起才看得懂**，
   撰稿時兩則都要引，不可以只挑一則寫成定論。
   （Apple 頁面照例滿是不斷行空格與 U+2011，`_tools/tech/text.py` 會把它們
   印成 `<NBSP>`／`<NBHY>`，用純 ASCII 空白去搜會零筆。）

6. **Meta 的可見日期與機器可讀時間戳差一天。**
   Threads 那篇可見署名是 September 15, 2026，但頁內 JSON-LD 的
   `datePublished` 是 `2026-09-16T01:05:49+00:00`＝**台北 2026-09-16 09:05**。
   照 DELTA-4-5 第 5–6 項，有真實時區時間就要換算，所以它落在視窗外 9 小時。

---

## 候選清單

由高到低排序，**每一則都讀過正文**。10 則為上限，掃到但不寫的另表列在下面。

| 日期（UTC→台北） | 標題 | 來源狀態 | 建議 | 與既有文章重疊 | 建議 slug／不寫的理由 |
| --- | --- | --- | --- | --- | --- |
| 2026-09-14（Apple 標示日期，無時間） | Apple's new child safety features now available | ✅ 英文 200／144,974 B＋**繁中版 200／139,928 B**＋`apple.com/child-safety` 200／244,130 B | **重要** | 與 `ai-news-siri-ai-ios-27-20260914` 同屬 iOS 27，主體不同（一個是 Siri，一個是家長控制）；站上 27 篇科技文章沒有一篇碰家長控制 | `tech-news-apple-child-safety-ios27-20260914` |
| 2026-08-31 | Commission designates ChatGPT, Reddit, Roblox under Digital Services Act | ✅ 新聞頁 200／49,076 B＋**IP/26/1772 列印 PDF 200／79,538 B（2 頁、3,277 字）** | **重要** | 與 `tech-news-eu-kids-act-20260917` 同屬歐盟平台責任但**不同事件**（這是既成的指定處分，那是尚未通過的提案），正好互為對照 | `tech-news-eu-dsa-designation-20260831` |
| 2026-08-27（8/31 更新 ISO） | Releasing Windows 11, version 26H2 to the Release Preview Channel | ✅ 200／116,902 B | **重要** | 無。`tech-news-windows-cloud-rebuild-20260918` 寫的是 Insider 實驗頻道的功能，這則是年度版本本身 | `tech-news-windows-11-26h2-20260827` |
| 2026-09-08 | 同一天三份官方稿：ASML×TSMC 發起 12 吋光罩倡議、ASML×Samsung 宣布加入、ASML×Intel Foundry 談 6 吋縫合與 6×12 吋轉換 | ✅ TSMC 200／184,014 B（`pr.tsmc.com/english/news/3338`）＋ASML×Samsung 200／169,463 B＋ASML×Intel Foundry 200／169,189 B | **重要** | 無。站上 27 篇科技文章沒有任何一篇寫過半導體製程或設備 | `tech-news-high-na-euv-12inch-photomask-20260908` |
| 2026-09-01 | Upcoming changes to Rosetta support for Intel-based macOS apps | ✅ `?id=w5ngl9k2` 200／111,230 B＋`?id=k1mtkt1k` 200／113,477 B（說法不同，見坑 5） | **重要** | 無 | `tech-news-apple-rosetta-end-20260901` |
| 2026-08-11 | Sony Semiconductor Solutions and TSMC Agreed to Establish Joint Venture for Next-Generation Image Sensors | ✅ TSMC 200／182,841 B（`/english/news/3333`）＋**Sony 自己的同一則 200／104,724 B**（`sony-semicon.com/en/news/2026/2026081101.html`）＋同日董事會決議 200／181,358 B（`/english/news/3332`） | **重要** | 無 | `tech-news-tsmc-sony-image-sensor-jv-20260811` |
| 2026-08-07 | Moving the Microsoft Edge extensions ecosystem forward with Manifest Version 3 | ✅ 部落格 200／118,355 B＋`learn.microsoft.com/microsoft-edge/extensions/developer-guide/manifest-v3` 200／50,456 B（頁面日期 2026-09-15） | **重要** | 無 | `tech-news-edge-manifest-v2-sunset-20260807` |
| 2026-09-08 | Helping families and educators support safer experiences and healthier habits on Windows（Windows Age API） | ✅ 部落格 200／130,494 B＋文件 200／56,942 B（**從貼在文中的 `aka.ms/windows-age-api` 轉導，不是猜的**）＋同日姊妹篇 200／123,878 B | **重要** | 與第 1 則同月同題（平台端年齡分級），但廠商、機制與地區都不同，兩篇可互連 | `tech-news-windows-age-api-20260908` |
| 2026-09-04 與 2026-09-09 | CISA 把兩個 Chromium V8 漏洞列入已遭利用清單（CVE-2026-85046、CVE-2026-87491） | ✅ CISA 公告 200／53,212 B、200／53,723 B＋KEV JSON 200／1,744,369 B＋Chrome Releases 9/3 200／168,086 B、9/8 200／551,382 B | **次要** | 與 `tech-news-cisa-kev-linux-kernel-20260918`、`tech-news-cisa-kev-zyxel-gs1900-20260921` **形式相同但對象不同**（那兩篇是伺服器與交換器，這篇是一般人每天用的瀏覽器） | `tech-news-chromium-v8-kev-20260909` |
| 2026-08-24 | Update: New domain for Sign in with Apple | ✅ 200／108,097 B | **次要** | 無 | `tech-news-sign-in-with-apple-domain-20260824` |

### 十則的一句話重點

1. **Apple 兒少安全（9/14）**：iOS 27／iPadOS 27／macOS 27 上路的家長控制——
   新增「時間額度」可依社群、娛樂、遊戲等**類別**設定，Safari 新增「要求瀏覽」
   （開新網站要家長核准），「通訊安全」除既有的裸露外**新增攔截血腥與暴力內容**，
   並涵蓋即時 FaceTime。Apple 明寫「部分功能可能不是所有地區、語言或機型都能用」，
   **沒有列出地區清單**，所以不能寫成台灣一定有。有繁中官方版可引。
2. **歐盟 DSA 指定（8/31）**：ChatGPT 被指定為**超大型線上搜尋引擎（VLOSE）**，
   Reddit 與 Roblox 為超大型線上平台（VLOP），門檻是歐盟境內月均 4,500 萬使用者
   （由業者自報）；通知後**四個月、即 2027 年 1 月**要符合額外義務；
   ChatGPT 由愛爾蘭 Coimisiún na Meán、Reddit 與 Roblox 由荷蘭 ACM 協同監理；
   至此累計指定 **28 個**平台與搜尋引擎。執委會把 ChatGPT 定性為「混合服務」。
3. **Windows 11 26H2 進 Release Preview（8/27，8/31 補 ISO）**：
   今年的年度功能更新 **Build 26300.9278**，先進 Release Preview 頻道，
   一般可用性寫的是「今年稍晚」；以 **enablement package（eKB）** 方式交付，
   24H2／25H2／26H2 共用同一條維護分支，所以很多功能其實已經隨月更陸續到位。
   **對讀者最有用的是一個硬日期**：**Windows 11 24H2 的家用版與專業版
   2026 年 10 月 13 日停止更新**（企業版與教育版到 2027 年 10 月 12 日）。
   商用裝置這一版會把先前未預設開啟的 Windows 設定備份、工作列的
   App 專屬動作與部分檔案總管改良打開。
4. **12 吋光罩與 High NA EUV（9/8）**：這是本輪最完整的一組——**同一天、
   同一場會議（Monterey 的 SPIE Photomask Technology + EUV Lithography），
   三份官方稿把台積電、三星、Intel Foundry 排在同一條路線上**。
   TSMC 稿：9 月 7 日會前成立產業聯合倡議，目標 **2031 年建立 12 吋光罩試產線、
   2033 年進入先進製程量產**，TSMC 自己的 High NA EUV **從 2030 年起用於先進製程量產**，
   初期仍用 6 吋光罩。Samsung 稿：**宣布加入該 12 吋光罩倡議**，
   並計畫 **2028 年把 High NA EUV 用於 DRAM 量產，官方自稱是業界首次**。
   Intel Foundry 稿：稱自己「三年多來主導大尺寸光罩倡議」，
   近期做法是**在 6 吋光罩上用或不用「縫合」（stitching）**，再轉向 6×12 吋；
   並提到 2024 年裝設第一台商用 EXE 系統、已出貨第一個用 High NA 量產的邏輯產品。
   **三份稿都沒有金額**，TSMC 那份的參與者只寫「已表達興趣」，
   ASML 的稿尾明列前瞻性陳述免責——寫的時候不要把 2028／2031／2033 說成承諾。
5. **Rosetta 收尾（9/1）**：macOS 26.4 起，啟動依賴 Rosetta 的 App 可能跳系統通知；
   **Apple 明確保留「依賴 Intel 框架的舊有、已無人維護的遊戲」**的 Rosetta 支援。
   9/1 與 9/9 兩則對「哪一版是最後一版」寫法不同，必須並陳。
6. **Sony＋TSMC 合資（8/11）**：在日本熊本縣合志市設立
   Advanced Vision Semiconductor Manufacturing Corporation，**預計 2029 年量產**
   智慧型手機影像感測器；Sony 出資約 **4,650 億日圓**（含以分割方式移轉既有廠房）、
   TSMC 約 **2,820 億日圓**，Sony 為唯一控制股東並派任代表董事；
   **尚待主管機關核准**，且額外投資是「以取得日本政府支持為前提」。
   同日董事會另核准約 **294.425 億美元**的資本支出。
7. **Edge 停用 Manifest V2（8/7）**：2026 年 8 月起開始消費者端轉換，
   目標 **2026 年底完成消費者端、2027 年初開始企業端**；
   官方數字是前段 MV2 擴充功能已有 **95%** 轉到 MV3，
   Edge Add-ons 上「還有實際使用量」的 MV2 擴充功能只剩 **58 個**，
   其中**只有 3 個**沒有現成的 MV3 版本。文件端的時程表另寫「2026 年 9 月中旬
   開始對部分使用者顯示淘汰警告」，與部落格的重點不完全一樣，兩邊都要引。
8. **Windows Age API（9/8）**：Windows 新增平台級年齡訊號 API——
   `GetUserAgeRangeAsync`（年齡分組為 **未滿 10、10–12、13–15、16–17、18+**，
   不給出生日期）、`GetAgeVerificationStatusAsync`、`CheckAgeStatusAsync`；
   Microsoft Age Verification「驗證一次、到處可用」**目前只在新加坡、巴西、澳洲的
   Microsoft 商店上線**（台灣不在名單上）；API 現階段只對 Windows Insider 開放，
   `CheckAgeStatusAsync` 要等後續更新。法國等地區會在開機設定時提高家長控制的能見度。
9. **兩個 Chromium V8 漏洞（9/4、9/9）**：CVE-2026-85046（型別混淆，
   修在 Chrome **152.0.7977.82/.83**，2026-09-03 釋出，該版共 12 個安全修正，
   High、獎金 1,000 美元、2026-08-04 由 Salvatore Gulizia 通報，CISA 要求 9/18 前處理）
   與 CVE-2026-87491（越界寫入，修在 **Chrome 153.0.8010.36/.37**，2026-09-08，
   CISA 要求 9/23 前處理）。**CISA 的說明寫明會波及 Chrome、Edge、Opera 等
   所有 Chromium 瀏覽器**。要注意的分寸：**Google 的兩篇版本說明都沒有寫
   「已遭利用」**，「已遭實際利用」這句話只來自 CISA 的 KEV 收錄理由。
   照 `tech.md`，只寫影響範圍與該做什麼（對版本號），不寫攻擊手法。
10. **Sign in with Apple 換網域（8/24）**：新產生的中繼信箱改發在
    **`private.icloud.com`**，原有的 `privaterelay.appleid.com` 繼續收轉信；
    Apple 明寫「經再次評估與社群回饋後」，**iCloud+ 的「隱藏我的電子郵件」維持
    在 `icloud.com`**。對讀者的意義是：白名單、退訂與客服比對信箱時會看到新網域。

---

## 掃到但不寫（含已在站上的重複）

| 日期 | 標題／事項 | 來源狀態 | 判定 | 理由 |
| --- | --- | --- | --- | --- |
| 2026-09-14 | More choice and possibility with Windows PCs at IFA | ✅ feed 已確認 | **不寫（重複）** | 這個網址**已經是 `tech-news-windows-project-zenith-20260904` 的 sources 之一** |
| 2026-09-03 | Sparks Fly 那則的實際標題是 “…IFA…NVIDIA PAIR…RTX Spark”（`blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/`） | ✅ 200／128,588 B，讀過全文 | **不寫（重複＋轉 AI 垂直）** | 全篇主體是本機 AI 代理與模型（Hermes Agent、OpenClaw、Perplexity、llama.cpp／vLLM 最佳化、Nemotron／GLM／Qwen／DeepSeek）；唯一屬於科技垂直的事實是「RTX Spark Windows PC 十月由 Lenovo、Acer 推出」，而那正是 Project Zenith 那篇已經用 IFA 9/14 那則寫過的同一個事件叢集 |
| 2026-09-14 | Perplexity Portable Computer Is Now Available on Windows, Powered by NVIDIA RTX | ✅ 200／113,341 B，讀過全文 | **不寫（轉 AI 垂直）** | 主體是 Perplexity 的本機 AI 代理，照 `tech.md` 應由 AI 垂直評估。**唯一可用的硬體事實**：需要 24GB 以上 VRAM 的 GeForce RTX／RTX PRO，DGX Station 支援「即將推出」 |
| 2026-09-08 | Listening to families. Improving Microsoft Family. | ✅ 200／123,878 B，讀過全文 | **不寫** | 通篇是「我們修好了哪些 bug」，沒有版本號、沒有日期、沒有任何可查核的門檻值。同日那篇 Age API 才有內容（已列為候選 7） |
| 2026-08-03／08-19／09-01 | 數發部 MyData 三則（線上申換護照、身障牌照稅免稅、幼兒園報名） | ✅ 200／88,255 B、87,348 B、87,830 B | **不寫（改維護票）** | 自然形態是 **`tech-news-moda-mydata-student-loan-20260917`** 的新一節：同一個 MyData 機制、同一種「文件不落到使用者手上」的說明，只是換了應用場景。建議開一張維護票把三個場景補進那篇 |
| 2026-08-18 | Changes for apps in the European Union | ✅ feed 已確認 | **不寫（重複）** | 已是 `tech-news-apple-eu-business-terms-20260818` |
| 2026-08-18 | Updated Apple Developer Program License Agreement now available | ✅ 200／106,601 B，讀過全文 | **不寫（改維護票）** | 只有一句新事實——歐盟新條款寫進授權合約 Attachment 14，**2026 年 10 月 1 日生效**。這一句應該補進 `tech-news-apple-eu-business-terms-20260818`，不要另開一篇 |
| 2026-09-09 | App Store submissions now open for the latest OS releases | ✅ 200／113,477 B，讀過全文 | **不寫（改維護票）** | 兩件事值得補進別的文章：Rosetta 那句（見候選 4），以及 **2027 年 4 月起上傳 App Store Connect 必須用 iOS 27／tvOS 27／visionOS 27／watchOS 27 SDK** 這個期限 |
| 2026-08-27 | Tax and price updates for apps, In-App Purchases, and subscriptions | ✅ 200／110,454 B，讀過全文 | **不寫** | 變動全在摩洛哥（新增 20% VAT）、剛果共和國（新增 18% VAT）、坦尚尼亞（DST 2%→3%），價格調整只涉及以色列、印尼、摩洛哥、剛果共和國。**全篇沒有一個字提到台灣**，對本站讀者沒有適用性 |
| 2026-08-12 | Updates to age ratings for the Republic of Korea | ✅ 200／109,761 B，讀過全文 | **不寫（備選）** | 內容具體（拿 GRAC 分級編號可覆寫韓國分級為 All／12+／15+／19+；2026 年 10 月起兩個內容描述由 All 改為 12+），但**只適用韓國 App Store**，且是開發者後台操作。若站主想要第 11 則，它可以和候選 1、7 併成「各平台的年齡分級」專題 |
| 2026-08-05 | Get ready for new creative assets on the App Store | ✅ 200／108,164 B，讀過全文 | **不寫** | 是 App Store 行銷素材的設計規範預告，沒有日期、沒有規則變更，對讀者沒有可用資訊 |
| 2026-08-04 與 2026-08-26 | 數發部 115 年公民科技試驗場域（科技防災）開跑與決選 | ✅ 200／86,978 B（20324）＋200／91,114 B（20470），**兩則都讀過全文** | **不寫（備選，第 11 順位）** | 素材夠：29 組通過資格審查、4 組出線與基隆（防災士培訓報名平臺）、新北（弱勢機構災情即時回報）、苗栗（志工與物資管理）、南投（全民災情通報與視覺化）合作，每組獎勵 **新臺幣 30 萬元等值禮品（券）**，成果依「公共程式標準」（Standard for Public Code）上架到數發部 GitHub，時程是 9 月起需求訪談、年底完成原型與使用者測試、**116 年第一季**移轉程式碼。**只是它是一個試辦計畫，讀者現在用不到任何東西**，所以排在十則之外。**如果站主要在科技這一輪放一則台灣政府題，這是首選**，撰稿前要補官網 `cttaiwan.moda.gov.tw` |
| 2026-08-17 | Improving File Explorer & Context Menu: faster, simpler, and more customizable | ✅ 200／121,776 B，讀過全文 | **不寫（備選）** | 題目很貼近讀者（右鍵選單重設計、可自訂顯示項目、重新命名不再被雲端同步打斷、網址列支援引號與雙反斜線、中鍵開新分頁、檔案大小改用 KB／MB／GB），但**只推給 Windows Insider**，而且效能宣稱全是「更快、更少凍結」這類沒有數字的說法。等它隨正式版出貨再寫 |
| 2026-08-13 | Apple opens Advanced Manufacturing Center in Houston | ✅ 200／191,776 B，讀過全文 | **不寫（備選）** | 主體是一個 20,000 平方英尺的免費製造訓練中心（Apple 在美國的第二個製造學習據點），政治場合的成分很重。**唯一屬於供應鏈的硬事實只有一句**：同一座休士頓廠已在出貨 AI 伺服器，並將於「今年稍晚」開始生產 **Mac mini**——沒有給日期、沒有給產能、沒有說台灣或中國那一側會不會減少。要寫得等這句有後續 |
| 2026-08-03／08-10／08-11／08-27 | Apple Newsroom 四則（Leagues Cup、MLB 九月賽程、Apple Arcade 兩則） | ✅ 封存頁已確認 | **不寫** | 體育轉播與遊戲上架宣傳，不是科技新聞 |
| 2026-08-11 | NVIDIA 800 VDC power architecture for AI factories | ✅ 200／110,687 B，讀過全文 | **不寫（備選）** | 唯一非廠商自述的部分是 OCP：NVIDIA／Google／Microsoft 2026 年 3 月發布共同白皮書、2026 年 7 月發布 LVDC Solid-State Transformer Specification v0.3，80 家以上廠商依規格開發；其餘（MGX 800 VDC 電源機櫃 2026 下半年、row power center 每列 2 MW／2027 年）都是 NVIDIA 自己的時程。站上已有 `tech-news-eu-data-centre-rating-20260921` 與 `tech-news-nvidia-vera-rubin-20260915` 兩篇資料中心題 |
| 2026-08-10（滾動更新頁，原始發布 7/1、標示更新 8/5） | NVIDIA and Partners Build in America for America | ✅ 200／137,283 B，讀過全文 | **不寫** | 這是一頁**持續更新的匯整頁，沒有固定事件日**，引用它等於引用一個會變的東西。其中的台灣角度（緯創 Fort Worth 廠）另有專文，但日期是 **2026-07-21**（✅ 200／114,457 B），在視窗外 |
| 2026-08-06 至 09-10 | NVIDIA GeForce NOW Thursday 六則、What Is Cloud Gaming 說明頁 | ✅ sitemap 已確認 | **不寫** | 每週遊戲片單與名詞解釋，不是新聞 |
| 2026-08-12／08-25／08-26／08-27／09-15 | NVIDIA Spectrum-Six、NVLink Fusion（XPU 與 NVHBM）、Vera CPU delivery、Vera Rubin LPX、Vera Rubin NVL72 efficiency | ✅ sitemap 已確認 | **不寫（高度重疊）** | 全部是 Vera Rubin 世代的機櫃與互連，站上 `tech-news-nvidia-vera-rubin-20260915` 已經寫過同一代平台；且都是 NVIDIA 自家效能宣稱 |
| 2026-09-03 | NVIDIA to Acquire Hugging Face | ✅ feed 已確認 | **不寫（重複）** | 已是 `ai-news-nvidia-hugging-face-20260903` |
| 2026-09-10 | TSMC August 2026 Revenue Report | ✅ 200／177,656 B | **不寫** | 月營收數字屬行情，`tech.md` 的科技垂直不做 |
| 2026-09-01 | Second EU-Taiwan Semiconductor Industry Dialogue | ✅ 200／48,583 B，讀過全文 | **不寫（備選）** | 有台灣關聯（8/31 在台北、SEMICON Taiwan 2026 場邊、ChipDiplo 承辦、提到 European Chips Act 2.0 提案），但**通篇是兩場座談的議程摘要，沒有任何承諾、金額或日期**。若站主想要，它得等 Chips Act 2.0 本身有進度時再寫 |
| 2026-08-07 | Commission accelerates IRIS² deployment with enhanced security and expanded satellites network | ✅ 列表頁已確認 | **不寫（備選）** | 上一輪已經把 IRIS² 判為「台灣關聯只有間接的低軌衛星備援」，這一則是同一條線的簽約進度 |
| 2026-09-09／09-09／09-07／09-01／08-31／08-26／08-20／08-04／08-03 | 歐盟另外 9 則（European Innovation Act 提案、Digital Connectivity Awards 延期、EU-Greenland 2 億歐元、ECCC 徵案 9,600 萬歐元、Virkkunen 赴 G20、Virkkunen 出席 gamescom、Digital Europe 資料專案、Scaleup Europe Fund 50 億歐元、第四次 GPAI 工作小組） | ✅ 列表頁已確認 | **不寫** | 補助、基金、行程與產業政策提案，不是讀者用得上的規則變更；GPAI 那則屬 AI 垂直 |
| 2026-08-20／08-25 | Windows 365 turns five、Expanding the Windows on Arm app ecosystem | ✅ feed 已確認 | **不寫** | 前者是週年行銷，後者是開發者生態進度，沒有對使用者生效的變更 |
| 2026-08-24／09-03／09-08 | WebView2 改兩週一版、Interop 2027 徵求提案、Edge 擴充功能審查加速 | ✅ feed 已確認 | **不寫** | 三則都只影響開發者流程 |
| 2026-08-11 | Wi-Fi Alliance and prpl Foundation partner to accelerate carrier-grade Wi-Fi | ✅ 200／134,386 B，讀過全文 | **不寫** | 視窗內 Wi-Fi Alliance 唯一一則，但通篇是合作意向，沒有規格、沒有時程、沒有認證項目 |
| 2026-08-27／08-29 | 3GPP RAN5 Leadership Election、Magic in the air as RAN celebrate | ✅ 200／102,365 B、104,894 B | **不寫** | 組織事務，與 `BRIEF.md` 對 IETF 的處置同理 |
| 2026-09-09 | 國家通訊傳播委員會公告：委託「台灣德國萊因技術監護顧問股份有限公司」辦理電信管制射頻器材、電信終端設備審驗業務，有效期間自 115 年 9 月 9 日至 118 年 9 月 8 日（行政院公報第 032 卷第 168 期） | ✅ 逐日走查時在 2026-09-09 第 2 頁讀到 | **不寫（備選）** | **這是本站第一次真的從行政院公報撈到 NCC 的項目**，證明這條替代管道可用（上一輪兩期 60 筆全是空的）。但它本身是一則委託審驗機構的行政公告，可寫的只有「台灣的手機、路由器、Wi-Fi 設備上市前由誰做審驗」這一層背景，撐不起一篇。**留給下一輪：如果要寫「台灣的電信設備審驗怎麼運作」，這是唯一有日期、有期間、有具名機構的官方切入點** |
| 2026-08-01 至 09-15 | 行政院公報 46 天逐日全頁走查 | ✅ 見下方統計 | **不寫** | 除了上一列那一則，**沒有其他國家通訊傳播委員會的項目**，也沒有其他通訊傳播相關法規 |

---

## 已有研究紀錄（視窗外，但指示要求重查）

**`tech-news-taiwan-gsn-idc-20260916`**（研究紀錄 `sourcing_verdict: partial`）

- 原本唯一的來源重抓成功：`cht.com.tw/zh-tw/home/cht/messages/2026/0916-1830`，
  **200／153,013 B**（上一輪是 153,184 B，差在頁尾的即時區塊，正文未變）。
- **上一輪缺的第二條一手來源找到了**，而且不是猜出來的：
  從數發部自己的選單（核心業務 → 數位政府）
  `moda.gov.tw/digital-affairs/digital-service/354`（✅ 200／89,891 B）
  頁內就掛著官方連結 **`https://gsn.nat.gov.tw/`（✅ 200／56,522 B）**，
  另有「關於GSN」`gsn.nat.gov.tw/GSNArticle/Contents?articleId=77`（✅ 200／53,187 B）。
  研究紀錄裡記著的 `moda.gov.tw/digital-affairs/digital-service/operations/8265`
  本輪再試仍是 **404／4,014 bytes**，確認那是死路，不要再試。
- GSN 官方站的公告區還補上了研究紀錄明列的一個空白（「舊機房會不會退役」）：
  **2026-05-20「GSN IDC台北國光機房將辦理汰除作業」**。
  這條要自己去讀全文再引，本輪只確認它存在於官方公告清單上。
- 其餘限制（沒有金額、沒有地點、沒有規模、70% 進駐率是目標不是成績）維持不變。

---

## 窗口外、上一輪留下（給站主裁示）

| 日期 | 標題 | 來源 | 備註 |
| --- | --- | --- | --- |
| 2026-09-16（台北，Meta 可見署名 9/15） | Threads introduces parental supervision for teens in APAC | ✅ `about.fb.com/news/2026/09/threads-introduces-parental-supervision-for-teens-in-apac/` 200／491,286 B，讀過全文 | **差 9 小時落在視窗外**（JSON-LD `datePublished` 2026-09-16T01:05:49Z）。更關鍵的是**範圍**：全文只寫「Asia Pacific countries」，**沒有列出任何一個國家，也沒有出現 Taiwan**；頁面上出現的 Japan／Korea 只是語言切換選單。所以**不能寫成台灣已上線**。內容本身很具體（家長可看七日使用時間與日均、設每日時間上限與封鎖時段、睡眠模式預設 22:00–07:00 靜音並自動回覆、管理標註與隱私設定；未滿 16 歲要家長同意才能放寬 Teen Account 預設值；入口是 familycenter.meta.com/supervision）。**如果站主要把候選 1（Apple）、候選 7（Windows）做成「三大平台的兒少工具」專題，這是第三塊**，但必須寫明日期與地區的不確定 |
| 2026-03-12 | Adjustments to the China storefront of the App Store on iOS and iPadOS | `developer.apple.com/news/?id=dadukodv` | feed 已確認日期與標題，本輪未讀正文 |
| 2026-03-26 | Update on regulated medical device apps in the European Economic Area, United Kingdom, and United States | `developer.apple.com/news/?id=nyqbfz1y` | 同上 |
| 2026-03-31 | App Store expands support to 11 new languages | `developer.apple.com/news/?id=97t4mt64` | 同上 |
| 2026-05-08 | Brazilian betting license requirement for App Store availability | `developer.apple.com/news/?id=x4eyetnp` | 同上 |
| 2026-07-21 | Wistron Opens Advanced Manufacturing Plant in Fort Worth | `blogs.nvidia.com/blog/wistron-manufacturing-texas/` ✅ 200／114,457 B，讀過全文 | 台灣企業在美設廠：D1 廠 324,000 平方英尺、已量產 GB300 Grace Blackwell Ultra Superchip、將產 Vera Rubin Superchip、7 億美元承諾、500 個職缺年底擴到 1,000。**日期在視窗外**，但如果站主想補「台廠赴美」這條線，這是最乾淨的一則 |

---

## 讀不到／查不到

- **Samsung**：`news.samsung.com/global/` 直接 `curl (56) Recv failure: Connection was reset`，
  一個位元組都沒拿到。上一輪記的是「feed 被擋」，本輪連 HTML 首頁都連不上。
  **所以三星在這個視窗是「讀不到」，不是「沒有發表」。**
- **中華電信 2026-08-01 至 09-15 的新聞稿清單**：索引頁只算繪最新 10 則，
  翻頁與月份篩選都是帶 `__RequestVerificationToken` 的 POST，沒有可重現的 GET 端點；
  猜端點等於捏造，所以沒有清單。單篇內頁位址格式是
  `/zh-tw/home/cht/messages/<年>/<MMDD-HHMM>`，知道日期與時間才進得去。
- **NVIDIA 官方新聞稿（`nvidianews.nvidia.com`）在 9/10 以前的清單**：
  封存頁由 JS 算繪，feed 只回到 9/10。本輪用 `blogs.nvidia.com` 的 sitemap 補到
  部落格側，**但 `nvidianews.nvidia.com/news/...` 那一層的新聞稿沒有完整清單**。
- **台灣 NCC 的網站**：本輪沒有再試（整站 Angular 外殼，上一輪已證實連 `robots.txt`
  與 `sitemap.xml` 都回同一份 536 bytes 的 `<app-root>`）。
  替代管道行政院公報這次**查出東西了**（9/9 委託審驗機構那則），所以這條線不再是全空的；
  但要清楚：公報只涵蓋「刊登在公報上的法規與公告」，
  **NCC 的新聞稿、委員會議紀錄與裁處案仍然讀不到**。
- **ASML 官網上「ASML×TSMC」那一份**：ASML 的
  `asml.com/en/news/press-releases`（✅ 200／160,136 B）只列出「Latest press releases」
  **三則、全部是 2026-09-08**（Eindhoven 新園區、Intel Foundry、Samsung），
  **沒有 TSMC 那一則**；搜尋框是 JS 驅動，`Sorry, we were not able to find a match`
  是初始狀態不是查無資料。所以候選 3 的 TSMC 側目前只有 TSMC 自己的稿，
  但 Samsung 與 Intel Foundry 兩份 ASML 官方稿都明確提到同一個 12 吋光罩倡議，
  已足以構成兩條以上一手來源。**若要引 ASML 對 TSMC 的說法，還要再找 ASML 的原稿。**
- **Samsung 的新聞稿**：`news.samsung.com` 連不上（見上），
  本輪 Samsung 的官方說法**是從 ASML 的聯合發布稿取得的**——
  這是三星這條線目前唯一可行的繞道，記下來給下一輪。
- **`cttaiwan.moda.gov.tw`**（公民科技試驗場域官網）：新聞稿裡有連結，本輪未抓。
- **blog.google 8/1–9/15 的清單（時間到了，沒做完）**：`blog.google/rss/` 與各產品子 feed
  都只有 20 筆、最舊 2026-09-16，整段視窗已滾出。
  `blog.google/robots.txt`（✅ 200／153 B）只指向一份 **`blog.google/sitemap.xml`**，
  **那份 sitemap 本輪沒有抓**。下一個代理從那裡接手，
  重點是 8 月的 Pixel Drop／Android 版本這一類（站上已有
  `tech-news-pixel-drop-20260915` 與 `tech-news-googlebook-launch-20260921` 可對照）。
- **其他沒做完的方向**（時間到了，不是查不到）：
  TSMC 的 Arizona／Dresden 擴廠金額（本輪只拿到 8/11 董事會核准的
  約 294.425 億美元總額，沒有分廠別）；SIA 統計（照指示除非有結構角度否則跳過，本輪未查）；
  `nvidianews.nvidia.com` 9/10 以前的新聞稿（封存頁 JS 算繪）；
  中華電信 8/1–9/15 的清單（POST 帶 token）。
- **Wi-Fi Alliance 2026-08-11 之後**：官網 press releases 只有 9 則，最新就是 8/11。
  `wi-fi.org/news-events` 與 `/news-events/newsroom` 都回 **404**（body 仍有 12–13 萬 bytes
  的軟性 404，不要被 body 大小騙了），正確入口是首頁掛的 `/press-releases`。

---

## 統計

- **掃過的管道**：36 個（含分頁、月封存與 sitemap 共 72 個位址）。
- **視窗內讀到正文的官方頁**：42 篇。
- **建議「重要」**：8 則（候選 1–8）。
- **建議「次要」**：2 則（候選 9–10）。
- **不寫**：30 類（表列），其中
  **重複 4 則**（Windows PCs at IFA、NVIDIA IFA、Apple 歐盟條款、NVIDIA×Hugging Face）、
  **改維護票 3 類**（MyData 三則 → `tech-news-moda-mydata-student-loan-20260917`；
  Apple 授權合約 Attachment 14 → `tech-news-apple-eu-business-terms-20260818`；
  9/9 提交公告的兩句 → Rosetta 與 iPhone Duo 兩篇）、
  **轉 AI 垂直 2 則**、其餘是素材不足或與讀者無關。
- **窗口外另列**：6 則。
- **行政院公報**：2026-08-01 至 09-15 共 **46 天逐日查核，做了兩輪**。
  - 第一輪（`dl/gz-sweep.txt`，46 天 × 前 2 頁）：出刊日 32 天、停刊 14 天，每日 15–44 筆。
  - 第二輪（`dl/gzf-sweep.txt`，全新 session 循序、**每天走完所有分頁**）：
    走到 **2026-09-10** 為止（8/1–9/10 共 41 天、102 個頁面），**9/11–9/15 這 5 天
    只有第一輪的前 2 頁覆蓋**，這是本輪唯一一個沒做完的格子。
  - 兩輪都只找到 **1 則國家通訊傳播委員會的項目**：2026-09-09 第 032 卷第 168 期，
    委託台灣德國萊因辦理電信管制射頻器材與電信終端設備審驗（已列在「掃到但不寫」）。
    兩輪獨立命中同一筆，可以互相佐證。
  - 原始頁在 `_tools/tech/dl/gz/`（第一輪）與 `_tools/tech/dl/gzf/`（第二輪）。
- **完成掃描時間（UTC）**：2026-09-22T23:05Z 開始，**2026-09-23T00:01Z 停止**。
