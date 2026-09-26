# 科技（非 AI）候選：2026-09-22 至 2026-09-26

批次 4.8 前期研究，查核日 **2026-09-26**。收錄範圍是 **事件日在 2026-09-22 00:00 台北（2026-09-21T16:00Z）之後**的項目，
掃描結束時間 **2026-09-26T13:22Z**（台北 2026-09-26 21:22）。另依指示提出 **兩則補遺**（事件日 2026-09-12～09-21、沒有人寫過），在表格與逐則說明裡都標「補遺」。
每一則進入候選的都開原文頁讀到正文才算（狀態碼與 bytes 記在下面）。
範圍與界線見 repo 的 `docs/news-2026-batch-4/tech.md`，來源規則見 `BRIEF.md`；
上一輪（09-20～09-22）的候選在 `candidates-since-0920-tech.md`，本頁不重複，已判過的項目只在「不寫」裡點名。

所有請求都用 `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"`，
同一主機間隔 ≥1 秒，沒有任何請求帶入任何人的姓名、email 或個人資料。
DuckDuckGo 的 HTML 搜尋只拿來找線索（查詢字串只有題目關鍵字），結果不進任何來源欄。

排除清單：`existing-packs.txt`（站上已有的 45 個新聞包）與 `automation-candidates.tsv`（185 筆，不論狀態，同一事件即排除）。
每一則候選都逐一比對過，結果寫在各則的「重疊」欄。

---

## 掃過的管道與結果

判準照 `BRIEF.md`：**看 `<item>`／`<entry>` 數與最新一筆日期，不看狀態碼。** bytes 是解壓後落地的檔案大小（`--compressed`，所以和線上傳輸量不同）。
feed 筆數與 KEV 總數都是**當下快照**，只用來判斷「拿到了沒有」，不是可以寫進文章的事實。

| 管道 | 位址 | 取得狀況（2026-09-26） | 視窗內有幾則 |
| --- | --- | --- | --- |
| Apple Newsroom | `www.apple.com/newsroom/rss-feed.rss` | ✅ Atom 200／19,035 B，20 筆，最新 2026-09-22T12:59Z | 2（上一輪都判過：Mac mini 上市日＝維護票、Music Hall＝不寫） |
| Apple Developer | `developer.apple.com/news/rss/news.rss` | ✅ 200／427,604 B，146 筆，最新 **2026-09-18T17:00Z**（視窗外） | 0 |
| Apple 安全性更新 | `support.apple.com/en-us/100100` | ✅ 200／316,120 B，伺服器端算繪 | 1（watchOS 27.0.1，09-23，頁面寫 “This update has no published CVE entries.”） |
| Windows 主站 | `blogs.windows.com/feed/` | ✅ 200／142,738 B，10 筆，最新 2026-09-25T17:02Z | **4**（Surface 1、Insider 2、Edge 1；Edge 與 09-21 月報上一輪已判） |
| Microsoft 官方部落格 | `blogs.microsoft.com/feed/` | ✅ 200／158,035 B，10 筆，最新 2026-09-25T12:03Z | 1（新 Copilot，自動化已 `published` → 排除） |
| 台灣微軟新聞中心 | `news.microsoft.com/zh-tw/feed/` | ⚠️ 200／24,569 B，10 筆，但**最新一筆 2025-08-29**——死 feed，不能拿來證明「台灣沒有公告」 | 無法判斷 |
| NVIDIA | `nvidianews.nvidia.com/releases.xml` | ✅ 200／44,488 B，20 筆，最新 2026-09-24T14:00Z | 8（全部已在自動化清單或上一輪判過） |
| Google 主站 | `blog.google/rss/` | ✅ 200／29,574 B，20 筆，最新 2026-09-24T17:00Z | 20（幾乎全是 AI 主體） |
| Google 子站 | `blog.google/products-and-platforms/rss/` | ✅ 200／30,153 B，20 筆，最新 2026-09-24T17:00Z | 6（與主站重複） |
| Chrome Releases | `chromereleases.googleblog.com/feeds/posts/default`（轉到 feedburner） | ✅ 200／256,123 B，25 筆，最新 2026-09-26T00:47Z | 14（09-22 Stable 154 寫 “108 security fixes”，**全文無 “in the wild”**） |
| Meta Engineering | `engineering.fb.com/feed/` | ✅ 200／227,368 B，9 筆，最新 2026-09-24T00:00Z | 2 |
| Meta Newsroom | `about.fb.com/news/feed/` | ✅ 200／152,086 B，10 筆，最新 2026-09-24T21:15Z | 5（Connect 2026 四則＋新加坡警方合作 1） |
| GitHub changelog | `github.blog/changelog/feed/` | ✅ 200／47,524 B，10 筆，最新 2026-09-25T23:24Z | 10 |
| WordPress.org News | `wordpress.org/news/feed/` | ✅ 200／287,223 B，10 筆，最新 2026-09-22T14:01Z | **2**（7.1.2 安全版、OWA 輪值主席） |
| Qualcomm 新聞室 | `www.qualcomm.com/news/releases` | ❌ 200／9,377 B，**React 外殼、無正文** | — |
| Qualcomm sitemap | `www.qualcomm.com/sitemap.xml`（`robots.txt` 指向的那一份） | ✅ 200／1,677,790 B，`<lastmod>` 可用 | 4 則新聞稿（09-22 Snapdragon 8 Elite Gen 6、09-23 PickNik 收購與 Sound Elite Gen 2、09-24 Apple 專利授權） |
| Qualcomm 新聞稿 Markdown 版 | 新聞稿頁 `<link rel="alternate" type="text/markdown">` 指向的同名 `.md` | ✅ Snapdragon 稿 200／8,917 B（同一篇 HTML 版 200／13,616 B，去標籤後只有 140 字）；**OnQ 部落格與 press kit 的 `.md` 回 404／6,717 B** | — |
| Qualcomm IR | `investor.qualcomm.com/rss/pressrelease.aspx` | ✅ 200／68,693 B，10 筆，最新 **2026-09-08** | 0（Apple 授權稿不在 IR feed） |
| MediaTek 新聞室 | `www.mediatek.com/press-room` | ✅ 200／118,603 B，伺服器端算繪 | 0（最新 09-21；09-15 天璣 9600 Pro 列為補遺） |
| TSMC 新聞 | `pr.tsmc.com/english/latest-news` | ✅ 200／187,111 B | 0（最新 2026-09-10 營收） |
| Intel 新聞室 | `newsroom.intel.com/feed/`（轉址到 `intel.com/…/newsroom/home.html`，**不是 feed**） | ✅ 200／560,776 B，HTML 列表 | 0（最新 09-21，Googlebook） |
| PlayStation／Xbox | `blog.playstation.com/feed/`、`news.xbox.com/en-us/feed/` | ✅ 200／210,084 B、200／215,838 B，各 10 筆 | 16，全是遊戲與周邊，無硬體或政策 |
| CISA 公告列表 | `www.cisa.gov/news-events/cybersecurity-advisories` | ✅ 200／163,834 B，最新 2026-09-25 | 4 則 KEV 公告（09-22、09-24、09-25 ×2）＋1 份 ICS fact sheet |
| CISA KEV JSON | `www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | ✅ 200／1,752,832 B，`catalogVersion` 2026.09.25、`dateReleased` 2026-09-25T18:58Z | **9 個 CVE**（09-22 四、09-24 二、09-25 三；另 09-21 Zyxel 已寫） |
| CVE Program API | `cveawg.mitre.org/api/cve/<CVE-ID>` | ✅ 查 10 筆，各 200／2,474～5,139 B | — |
| TWCERT/CC TVN | `www.twcert.org.tw/tw/lp-132-1.html` | ✅ 200／30,231 B，伺服器端算繪 | 1 則看過內頁（TVN-202609009，公開日 09-23）；TVN-202609010 未查日期 |
| Synology 資安公告 | `www.synology.com/en-global/security/advisory` | ✅ 200／144,090 B | 0（SA-26:13 發布於 09-18，列為補遺） |
| 數位發展部 | `moda.gov.tw/press/press-releases/372` | ✅ 200／109,359 B，伺服器端算繪 | 2（09-24 屏東通訊建設、09-22 NGO/NPO 數據轉型手冊） |
| 中華電信 | `cht.com.tw/zh-tw/home/cht/messages` | ✅ 200／179,506 B，伺服器端算繪 | 10（實質 1：09-23 6G Summit Taipei） |
| 經濟部 | `moea.gov.tw/MNS/populace/news/News.aspx?kind=1&menu_id=40` | ✅ 200／137,357 B | 0 則科技題（油價、鋼品配額、變電所、設計展、形象展） |
| 行政院 本院新聞 | `ey.gov.tw/Page/6485009ABEC1CB9C`（從首頁導覽列取得的真實網址） | ✅ 200／128,180 B | 0（09-24 第 4022 次院會無數位、電信、資安議案） |
| 行政院 部會新聞（NCC 替代管道之一） | RSS `ey.gov.tw/RSS_Content.aspx?ModuleType=4`＋列表 `ey.gov.tw/Page/B31C61707D4FEEEF?page=7…15&PS=15&`（頁面自己給的分頁連結） | ✅ RSS 200／141,057 B，100 筆，涵蓋到 2026-09-23T16:00Z；列表第 7～15 頁各 200，涵蓋到 09-21 | **0 則 NCC**；數發部 2 則（同上） |
| 行政院公報（NCC 替代管道之二） | `gazette.nat.gov.tw/egFront/browseVolume.do`（上一輪的 cookie 配方，一個日期一個 jar） | ✅ 09-23 第 032 卷第 178 期（29 筆）、09-24 第 179 期（33 筆）逐筆看過；**09-25 回「共 0 筆」**（中秋節）；09-22 第 177 期上一輪已看 | **0 則 NCC** |
| 歐盟執委會（數位） | `digital-strategy.ec.europa.eu/en/news` | ✅ 200／69,674 B | 6（DSA 董事會第 20 次會議、反假訊息守則第二批報告、公民團體圓桌、Virkkunen 訪格陵蘭、ADACities 延期、EIB 投資協定） |
| 歐盟 DMA 專站 | `digital-markets-act.ec.europa.eu/news_en` | ✅ 200／104,072 B，最新 **2026-07-23**（Google 罰款） | 0 |
| 歐盟競爭案件登錄 | `competition-cases.ec.europa.eu/latest-updates/InstrumentDMA` | ❌ 200／56,823 B，**JS 外殼、去標籤只剩 29 字** | 未查到（線索見文末） |
| ENISA | `www.enisa.europa.eu/news` | ✅ 200／85,294 B，最新 **2026-09-22**（威脅情勢報告，站上已寫） | 0 |
| FTC | `www.ftc.gov/news-events/news/press-releases` | ✅ 200／1,038,209 B | 2 則 09-22～09-24（1 則平台與冒名詐騙廣告，入選） |
| Federal Register | API `documents.json`（FTC＋impersonation）與 `public-inspection-documents/current.json` | ✅ 200／13,591 B、200／168,493 B | FTC 的 ANPRM **截至查核時尚未刊登，也不在公開檢閱清單** |
| 台灣 NCC | `www.ncc.gov.tw/` | ❌ **403／5,469 B，Cloudflare「Just a moment...」挑戰頁**（上一輪記的是 536 B 的 Angular 外殼，這一輪換成挑戰頁）。規則禁止繞過機器人驗證，**沒有再試** | 未查到 |
| FCC | `www.fcc.gov/news-events/headlines` | ❌ **403／392 B** | 未查到 |
| Samsung Newsroom | `news.samsung.com/global/latest` | ❌ 60 秒逾時、0 B | 未查到 |
| ASUS 資安公告 | `www.asus.com/content/asus-product-security-advisory/` | ❌ 200／292,576 B，但正文是 JS 轉址（去標籤 1,678 字，只有導覽） | 未查到 |
| MSRC | `msrc.microsoft.com/blog/feed`（轉到部落格首頁）、`…/update-guide/vulnerability/CVE-2026-65660` | ❌ 首頁 200／92,702 B 無日期列表；CVE 頁 200／2,717 B 外殼 | 未查到 |

### 這一輪新踩到的五個坑，寫給下一個代理

1. **Qualcomm 新聞室整站是 React 外殼，但每篇新聞稿都有官方 Markdown 版。**
   HTML 頁的 `<head>` 裡有 `<link id="geo-artifacts-markdown-link" rel="alternate" type="text/markdown" href="….md">`，
   `.md` 帶 front matter（`publishedDate`、`location`、`newsroomType`）與全文。**找新聞稿清單要走 `sitemap.xml` 的 `<lastmod>`**，
   新聞稿列表頁與 `/news/rss` 都拿不到（後者 404）。OnQ 部落格與 press kit 沒有 `.md`（404），所以 Summit 第二天的內容沒讀到。
   `sources[]` 要放**你讀到的 `.md` 網址**，並在研究紀錄寫明 HTML 版是外殼，否則就是規則 7 的「放了讀不到的網址」。
2. **KEV 的日期要逐個 CVE 看，不能看公告日。** 09-25 那則公告裡的 MikroTik CVE-2026-67279 看起來是新事件，
   但同一條攻擊鏈的 CVE-2026-67277 與 CVE-2026-86060 **早在 2026-09-10 就進了 KEV**，CERT Polska 在 **09-05** 就寫了「actively exploited」。
   CVE Program API 的 ADP 區塊（`containers.adp[].metrics[].other.type == "kev"`）直接給 `dateAdded`，比翻 KEV 網頁快。
3. **NCC 的替代管道多了一條：行政院「部會新聞」。** 發布機關下拉選單有「國家通訊傳播委員會」，
   篩選要走 ASP.NET postback（本輪沒有送表單），但**頁面自己給了 GET 分頁連結 `?page=N&PS=15&`** 與一條 100 筆的 RSS，
   逐頁翻到 09-21 為止沒有任何 NCC 項目。注意：這只證明「這條管道沒有」，**沒有驗證 NCC 平常會不會出現在這裡**。
4. **行政院公報 09-25 回 0 筆是中秋節，不是管道壞了。** 下一個代理若查 09-25／09-26 的空結果，先想放假日。
5. **同一篇官方稿的英文版與繁中版不一樣。** 聯發科天璣 9600 Pro 的繁中稿寫「台積電 2 奈米製程」，英文稿正文完全沒有 TSMC；
   Synology 的 `zh-tw` 公告頁內容仍是英文。細節見第 4、2 則。

---

## 候選清單

依「對台灣一般讀者的重要性」排序。`display_order` 未指派，由協調者決定。

| # | 事件日（台北） | 標題 | 來源狀態 | 建議 | 與既有文章重疊 | 建議 slug |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 發布 **09-22** 22:01；KEV **09-25**（美東）＝台北 09-26 | WordPress 7.1.2 修補核心嚴重漏洞，三天後被 CISA 列入已遭利用清單 | ✅ WP 發布文 200／154,558 B；GHSA 200／205,292 B；CISA 公告 200／53,409 B；KEV JSON 200／1,752,832 B；CVE 紀錄 200／2,798 B | **重要** | 無；但是八天內第三篇以 KEV 起頭的文章（`tech-news-cisa-kev-linux-kernel-20260918`、`tech-news-cisa-kev-zyxel-gs1900-20260921`） | `tech-news-wordpress-712-kev-20260925` |
| 2 | **補遺** 09-18 16:17 | Synology DSM 嚴重漏洞公告 SA-26:13（兩個 CVSS 9.8、無緩解措施） | ✅ 公告 200／125,185 B；列表 200／144,090 B；CVE 紀錄 200／2,505 B、200／2,474 B | **重要** | 無；站上沒有任何 Synology 或 NAS 題目 | `tech-news-synology-dsm-sa2613-20260918` |
| 3 | 09-22（茂宜島電頭；台北可能已是 09-23） | 高通發表 Snapdragon 8 Elite Extreme Gen 6 與 8 Elite Gen 6 | ✅ `.md` 200／8,917 B；夥伴引言 PDF 200／86,268 B／2 頁；sitemap 200／1,677,790 B | **重要** | 無；Googlebook 那篇只提到 Snapdragon X Elite | `tech-news-snapdragon-8-elite-gen6-20260922` |
| 4 | **補遺** 09-15 15:30 | 聯發科發表天璣 9600 Pro 與天璣 9600M | ✅ 英文稿 200／103,027 B；繁中稿 200／99,551 B | **重要**（可與第 3 則合併） | `tech-news-nvidia-mediatek-20260831` 是不同事件 | `tech-news-mediatek-dimensity-9600-20260915` |
| 5 | 09-24（美東） | 美國 FTC 預告立法程序：研議要求平台擋冒名詐騙廣告 | ✅ 新聞稿 200／1,001,890 B；ANPRM 擬刊文本 PDF 200／518,683 B／43 頁；FR API 200／13,591 B（尚未刊登） | 次要（可升重要） | 無 | `tech-news-ftc-impersonation-scam-ads-20260924` |
| 6 | 09-23（美國；台北 09-24 04:30） | 微軟新 Surface Pro 12 吋與 Surface Laptop 13 吋（Snapdragon X2 Plus） | ✅ 200／144,061 B | 次要 | 無 | `tech-news-surface-x2-plus-20260923` |
| 7 | 09-23 | 健保卡元件 Linux 版（全景 CGServiSign／NHIServisign）OS 指令注入漏洞 | ✅ TVN 中文 200／23,741 B；TVN 英文 200／17,191 B；CVE 紀錄 200／3,720 B；⚠️ 健保署端頁面未取得 | 次要（補第二來源前不可動筆） | 無 | `tech-news-nhi-servisign-linux-20260923` |
| 8 | 09-22 11:19 PDT＝台北 09-23 02:19 | Chrome 154 進入穩定版，一次修補 108 個安全問題 | ✅ Chrome Releases feed 200／256,123 B；⚠️ 文章頁 200／353,811 B 正文由腳本載入 | 備選 | 與 `tech-news-chromium-v8-kev-20260909` 同產品、不同事件 | `tech-news-chrome-154-20260922` |

### 看過、不寫的（視窗內）

| 事件日 | 項目 | 為什麼不寫 |
| --- | --- | --- |
| 09-25 | CISA 把 MikroTik RouterOS CVE-2026-67279 加入 KEV | **事件其實在視窗與補遺期之外**：MikroTik 公告 09-03、CERT Polska 09-05 就寫「actively exploited」、同一攻擊鏈的 CVE-2026-67277／86060 **09-10 已入 KEV**。09-25 只是第三個 CVE。另注意編號不一致：MikroTik 公告列 67276／86060／67277，CERT-PL 發的 CVE 紀錄與 KEV 則有 67279；KEV 的 notes 連結還掛著 `?utm_source=chatgpt.com`，別照抄 |
| 09-24 | Qualcomm 與 Apple 續約全球專利授權，自 2027-04-01 生效 | ✅ `.md` 200／4,086 B，全文只有兩句。IR feed（最新 09-08）沒有、Apple Newsroom 沒有、`sec.gov` 依 `BRIEF.md` 會 403——**只有一條一手來源，不到兩條的下限**。若之後找到 8-K 或 Apple 端說法再議 |
| 09-22／09-24／09-25 | KEV：Arista VeloCloud Orchestrator、F5 BIG-IP APM、Check Point ×2（09-22）、WSO2、Adobe Commerce／Magento（09-24）、Microsoft SharePoint（09-25） | 企業設備與伺服器軟體，一般讀者沒有可做的事；本週 KEV 題目以第 1 則 WordPress 為代表，避免第四篇 KEV |
| 09-23 | Meta Connect 2026（Ray-Ban Meta Audio、Meta VR Glasses、Ray-Ban Display 新功能）＋Meta 工程部落格 Private Processing for AI glasses | **排除**：自動化清單已有同一事件（The Verge “Meta Connect 2026: The biggest news and announcements”、TechCrunch “Meta introduces camera-free AI glasses” 等，狀態 rejected） |
| 09-23 | Meta 與新加坡警方合作處理 370 萬個帳號、粉專與內容 | 範圍是新加坡；可當第 5 則 FTC 那篇的背景線索（不進 `sources`） |
| 09-21 | 聯發科 Dimensity CX C10 Max（台積電 3 奈米，供「即將推出的」Googlebook 機種） | 改維護票，補進 `tech-news-googlebook-launch-20260921`：那篇目前只寫 Intel 與 Snapdragon 兩種處理器 |
| 09-23 | 高通收購 PickNik、Snapdragon Sound Elite Gen 2 | 機器人軟體與耳機音訊平台，一般讀者適用性低；未讀全文 |
| 09-23～24 | 中華電信「2026 6G Summit Taipei」 | ✅ 200／148,397 B。研討會新聞稿，沒有頻譜、時程或政策決定；站上已有 `tech-news-taiwan-6g-spectrum-20260910` |
| 09-24 | 數發部訪查屏東通訊建設 | ✅ 200／89,565 B。訪視稿；可用的只有普及服務數字（1.6 萬戶電話、8,500 戶寬頻、296 具公用電話、55 所偏鄉學校）與前瞻計畫 303 臺 5G 基地臺，沒有新制度或時程 |
| 09-22 | 數發部《NGO/NPO數據轉型手冊》 | 主體是 AI 驅動公共服務，照 `tech.md` 轉 AI 垂直評估 |
| 09-24 | GitHub「Require proof of presence for high-impact actions」 | ✅ 200／102,773 B。公開預覽，只限 EMU 企業且用 Microsoft Entra ID 當 IdP |
| 09-23～24 | 歐盟 DSA 董事會第 20 次會議、反假訊息行為準則第二批報告、公民團體圓桌、Virkkunen 訪格陵蘭 | 會議紀錄與報告上架，沒有新決定 |
| 09-22～24 | Google 部落格（Gemini 3.8 系列、Vids、Flow、MedGemma、Connected Apps 等） | AI 主體；Project Suncatcher、Google Beam 已在自動化清單 |
| 09-25 | 新 Copilot（Home、Code、Autopilot） | 自動化已 `published` |
| 09-23 | watchOS 27.0.1 | Apple 安全性更新頁寫無 CVE |
| 09-25 | Windows Insider 新版組建 | 例行 Beta／Experimental 組建 |
| 09-24 | 行政院第 4022 次院會 | 只有防疫資訊基盤一案沾到資訊系統，主體是衛福 |

---

## 值得寫的八則：逐則說明

### 1. WordPress 7.1.2 修補核心嚴重漏洞，隨後被列入已遭利用清單 — 建議「重要」

- **建議 slug** `tech-news-wordpress-712-kev-20260925`（若協調者認為核心事件是修補而不是 KEV，改用 `…-20260922`，兩個日期都要寫進正文）
- **事件日** 修補：2026-09-22（WordPress.org 發文 14:01Z＝台北 22:01）；CVE 紀錄發布 2026-09-22T16:44Z＝**台北 09-23 00:44**；
  KEV：CISA 公告日 2026-09-25（美東），KEV 目錄 `dateReleased` 2026-09-25T18:58Z＝**台北 09-26 02:58**
- **一手來源**
  - WordPress.org「WordPress 7.1.2 Release」`wordpress.org/news/2026/09/wordpress-7-1-2-release/` — 200／154,558 B
  - GitHub 安全公告 GHSA-7hp8-65ch-5whp（wordpress-develop）`github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp` — 200／205,292 B
  - CISA「CISA Adds One Known Exploited Vulnerability to Catalog」`cisa.gov/news-events/alerts/2026/09/25/cisa-adds-one-known-exploited-vulnerability-catalog` — 200／53,409 B
  - 佐證（不必進 `sources`）：KEV JSON 200／1,752,832 B；CVE-2026-87902 紀錄 `cveawg.mitre.org/api/cve/CVE-2026-87902` 200／2,798 B
- **讀到的內容**：WordPress 說這是修補「critical severity」漏洞的安全版，建議立即更新；支援自動背景更新的網站會自動開始更新。
  GHSA 標 Critical、CVSS v4 9.2，受影響範圍列到 4.7.0～7.1.1 各分支，修補版本從 7.1.2、7.0.6、6.9.9 一路回補到 4.7.37。
  漏洞要在**伺服器環境與佈景主題兩邊條件都成立**時才會變成遠端執行程式碼（GHSA 標題用 “conditional RCE”）；
  GHSA 點名受影響的佈景主題包括 Twenty Twelve、Twenty Fourteen，以及 Neve、Hestia、Sydney 等第三方主題。
  CISA 09-25 以「active exploitation」的證據把它列入 KEV，給聯邦機關的期限是 2026-09-28。
- **為什麼重要**：WordPress 是台灣中小企業、個人品牌與媒體最常見的架站系統。這則有明確的讀者行動
  （確認版本到 7.1.2 或所在分支的修補版、確認自動更新沒有被主機商關掉），而且「已遭利用」讓它不只是例行更新。
- **容易寫錯的地方**
  1. **不是所有 WordPress 網站都能被打穿。** 要寫「在特定佈景主題與伺服器設定下」。
     照 `tech.md`，**不寫**前提裡的具體攻擊鏈（GHSA 提到的 PEAR 元件與 PHP 設定細節），只寫影響範圍與該做什麼。
  2. GHSA 的佈景主題清單是 “such as”，**不是全清單**，不可寫「只有這五個主題受影響」。
  3. 命名兩邊不一樣：GHSA 標題是 “Unauthenticated path traversal in page-template resolution leading to conditional RCE”，
     CISA 叫 “WordPress Core Remote File Inclusion Vulnerability”（GHSA 標的 CWE 是 CWE-98）。兩個都是官方說法，要附各自出處，不要擇一改寫。
  4. **自動更新不等於已更新。** 發布文的原意是「支援自動背景更新的網站會開始更新」，不能寫成「所有網站已自動修好」。
  5. 4.7 以前的版本**不在受影響範圍表裡**——那是沒列，不是安全（那些分支早已不受支援）。寫「官方修補只回溯到 4.7」。
  6. 2026-09-28 的期限只約束美國聯邦民事機關（BOD 26-04）。BOD 26-04 是 **2026-06-10** 發布的舊指令（✅ 200／84,350 B），不要寫成新制度。
  7. CISA 沒有給受害網站數量或地區，**不可寫「大量台灣網站遭入侵」**。
- **重疊**：`existing-packs.txt` 無 WordPress；`automation-candidates.tsv` 無。
  **站主要決定**：這會是八天內第三篇用 KEV 起頭的文章，角度必須是「WordPress 7.1.2 與怎麼確認自己的網站」，不要再解釋 KEV 是什麼。

### 2.【補遺】Synology DSM 嚴重漏洞公告 SA-26:13 — 建議「重要」

- **建議 slug** `tech-news-synology-dsm-sa2613-20260918`
- **事件日** 2026-09-18 16:17:35（UTC+8，公告自己標的 Publish Time；Last Updated 相同）；兩筆 CVE 紀錄發布於 2026-09-18T08:19Z／08:21Z
- **一手來源**
  - Synology「Synology-SA-26:13 DSM」`synology.com/en-global/security/advisory/Synology_SA_26_13` — 200／125,185 B
  - CVE-2026-13684 紀錄 `cveawg.mitre.org/api/cve/CVE-2026-13684` — 200／2,505 B（CNA：synology）
  - CVE-2026-13639 紀錄 `cveawg.mitre.org/api/cve/CVE-2026-13639` — 200／2,474 B
  - 佐證：公告列表 200／144,090 B；`zh-tw` 公告頁 200／121,371 B（**內容仍是英文**，沒有在地化版本）；DSM 版本說明頁 200／121,415 B 是 JS 外殼（去標籤 770 字），沒讀到
- **讀到的內容**：Severity **Critical**，一次修 8 個 CVE。其中 CVE-2026-13684（SCGI）與 CVE-2026-13639（登入邏輯的熵不足）
  CVSS 3.1 都是 9.8、向量 `PR:N`，讓遠端攻擊者可讀寫任意檔案並造成阻斷服務；另有 3 個需要登入、2 個需要管理員權限、1 個只洩漏非敏感資訊。
  修補版本：DSM 7.4-90075、7.3.2-86009-4、7.2.2-72806-9、7.2.1-69057-12 以上。**Mitigation：None**。
- **為什麼重要**：Synology 是台灣公司，DSM 是台灣家庭、工作室與中小企業最常見的 NAS 系統，很多台會開外網存取。
  兩個免登入的 9.8 加上「沒有緩解措施」，讀者唯一能做的就是更新——這是一則有明確行動、而且讀者手上很可能就有設備的題目。
- **容易寫錯的地方**
  1. **沒有已遭利用的證據。** CISA ADP 在 2026-09-18T19:13Z 對兩筆 9.8 的評估是 `Exploitation: none`，KEV（2026.09.25 版）也沒有 Synology。不可寫「遭攻擊」。
  2. **不是「八個嚴重漏洞」**：嚴重（Critical）只有兩個，其他是 Important／Moderate，而且多數需要登入。
  3. CVE 紀錄對 **7.2.1 以前的版本標 `unknown`**——不是「不受影響」。DSM 7.1、6.2 的讀者不能從這份公告得到答案。
  4. 「Mitigation: None」要照寫成「官方表示沒有緩解措施」，不要自己補「關閉 QuickConnect 就安全」之類的建議（公告沒寫）。
  5. 事件日 09-18 在本輪視窗外，是**補遺**；正文要寫發布日，不要寫成本週新公告。
  6. 只寫受影響元件名稱（SCGI、登入邏輯），不寫任何利用細節。
- **重疊**：`existing-packs.txt` 無；`automation-candidates.tsv` 無；前兩輪候選檔（0916、0920）都沒有列。

### 3. 高通發表 Snapdragon 8 Elite Extreme Gen 6 與 8 Elite Gen 6 — 建議「重要」

- **建議 slug** `tech-news-snapdragon-8-elite-gen6-20260922`
- **事件日** 2026-09-22（新聞稿電頭 “MAUI”，`publishedDate: "Sep 22, 2026"`，sitemap `<lastmod>` 2026-09-22）。**新聞稿沒有時刻**；夏威夷是 UTC−10，台北日期可能已是 09-23，正文要寫「美國夏威夷時間 9 月 22 日」
- **一手來源**
  - Qualcomm 新聞稿 Markdown 版 `qualcomm.com/news/releases/2026/09/snapdragon-leads-the-agentic-ai-age-with-two-of-the-world-s-fast.md` — 200／8,917 B
    （同名 HTML 頁 200／13,616 B 是外殼，去標籤只剩標題 140 字；`.md` 是 HTML 頁 `<link rel="alternate" type="text/markdown">` 指向的官方版本）
  - Snapdragon Summit 2026 夥伴引言 PDF `qualcomm.com/content/dam/…/snapdragon-summit-2026-press-kit/day-1/documents/PartnerQuoteSheet.pdf` — 200／86,268 B／2 頁
- **讀到的內容**：兩款旗艦手機平台同日發表，Qualcomm 稱為 “multi-flagship strategy”。8 Elite Gen 6 “built on the same advanced 2nm process node”，
  採 Oryon CPU、重新設計的 Adreno GPU 與 Hexagon NPU，可提供 Extreme 版「許多相同」的功能給更多高階機。
  Extreme 版列的新功能：Adreno Neural Fusion（用 AI 輔助遊戲繪圖）、APV（Advanced Professional Video）支援、Intelligent Pixel Control。
  首發品牌列「including HONOR, iQOO, Motorola, OnePlus, OPPO, REDMI, RedMagic, vivo, and Xiaomi」。
  夥伴引言裡 HONOR、Motorola、RedMagic 明確點名 Extreme Gen 6，Motorola 說這是它的旗艦產品線第一次採用 Extreme 版。
- **為什麼重要**：接下來幾個月在台灣上市的 Android 旗艦大多會用這兩顆之一。「同一代分兩級」會直接影響讀者怎麼看規格表，
  而且和第 4 則聯發科同週期出現，是這一季的晶片主線。
- **容易寫錯的地方**
  1. **新聞稿與夥伴引言都沒有寫晶圓代工廠**（以 TSMC、foundry 詞界比對，2026-09-26 查核兩份文件皆 0 次）。不可寫「台積電 2 奈米」——那是聯發科繁中稿的寫法，不是高通的。
  2. **新聞稿沒有時脈、核心數、跑分或百分比。** 產品頁是行銷頁，照 `tech.md` 不得當能力宣稱來源，所以規格數字目前**沒有可用來源**，寧可不寫。
  3. 標題的 “Two of the World’s Fastest Mobile SoCs” 是高通宣稱，一律「高通表示」。
  4. 品牌名單是 “including”，**不是全清單**；名單裡沒有 Samsung，不等於 Samsung 不用。也不要自己把各品牌配到 Extreme 或非 Extreme，只有三家引言有講。
  5. 新聞稿沒有任何上市日、機種或台灣資訊。
  6. `sources[]` 要放 `.md` 網址（讀到的是它），研究紀錄寫明 HTML 版是外殼。
- **重疊**：`existing-packs.txt` 無；`automation-candidates.tsv` 只有 “PrismML brings its tiny LLMs to Qualcomm-powered smart glasses”（不同事件）。
  `tech-news-googlebook-launch-20260921` 只提 Snapdragon X Elite。**可與第 4 則合併**成一篇「2 奈米旗艦手機晶片」，見文末裁示事項。

### 4.【補遺】聯發科發表天璣 9600 Pro 與天璣 9600M — 建議「重要」

- **建議 slug** `tech-news-mediatek-dimensity-9600-20260915`
- **事件日** 2026-09-15（英文稿電頭 “HSINCHU, Taiwan – Sept. 15, 2026”，頁面標 03:30 PM，後設時間 2026-09-15 07:30:00，即台北 15:30）
- **一手來源**
  - 英文稿 `mediatek.com/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips` — 200／103,027 B
  - 繁中稿 `mediatek.com/zh-tw/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips` — 200／99,551 B
    （標題「用 AI 顛覆 AI！聯發科技發布首款 2 奈米旗艦 5G Agentic AI 晶片－天璣 9600 Pro」）
- **讀到的內容**：2 奈米；2+3+3 全大核（2 個 C2-Ultra 最高 4.55GHz、3 個 C2-Pro 4.35GHz、3 個 C2-Pro 3.1GHz）；34.5MB 快取；
  首次支援 LPDDR6 與 UFS 5.0；NPU 1090；G2-Ultra NX GPU；Imagiq 1290 ISP；4K240 慢動作。另同時發表較普及的天璣 9600M。
  所有百分比（單核 17%、多核 15%、多核功耗 61%、NPU prefill 51%、每瓦 token 55%、GPU 27%／24%／18%）都是聯發科宣稱，英文稿帶星號註腳。
- **為什麼重要**：台灣公司、2 奈米世代的旗艦手機晶片，和第 3 則高通同一季對打。對台灣讀者，這是「台灣晶片設計＋台灣代工」最直接的一個消費端題目。
- **容易寫錯的地方（這則幾乎全在語系差異，適用 `BRIEF.md` 規則 8）**
  1. **台積電只出現在繁中稿。** 繁中稿寫「藉由先進的台積電 2 奈米製程輔以與台積電設計技術協同優化（DTCO）」；
     英文稿正文沒有 TSMC，只在 “first company to announce reaching this threshold” 的超連結目標裡指向一篇更早的「採用台積電 2 奈米」新聞稿。寫台積電時要掛繁中稿。
  2. **61% 的條件**：英文 “61% reduction in multi-core power consumption”，繁中「多核功耗相較於上一代峰值性能則節省 61%」——繁中多了「在上一代峰值性能下」這個條件，要連條件一起寫。
  3. **對沖詞**：英文 “up to 17% higher single-core … up to 15% higher multi-core”，繁中寫成「提升 17%」「提升 15%」，掉了 up to。繁中稿以英文版的「最高」為準。
  4. **上市時間**：英文 “expected to launch this quarter”，繁中「將於近期上市」。不可換算成日期，也不可寫成「9 月底前」。
  5. **30B**：英文 “models up to 30B parameters”，繁中「高達 30B 的混合專家模型（MoE）」，範圍不同，兩版都要附出處。
  6. 兩版的高層引言不同（英文只有徐敬全；繁中多了陳冠州），不要拼成同一段。
  7. 「first company to announce reaching this threshold」是聯發科自述，不是事實。新聞稿沒有列任何手機品牌。
  8. 事件日 09-15 在本輪視窗外，是**補遺**。
- **重疊**：`existing-packs.txt` 無；`automation-candidates.tsv` 無；`tech-news-nvidia-mediatek-20260831` 是 NVIDIA 合作案，研究紀錄裡的「Dimensity」只指 Dimensity Auto 車用平台。

### 5. 美國 FTC 預告立法程序，研議要求平台擋冒名詐騙廣告 — 建議「次要」，可升「重要」

- **建議 slug** `tech-news-ftc-impersonation-scam-ads-20260924`
- **事件日** 2026-09-24（FTC 新聞稿與法規頁日期）；ANPRM **尚未刊登於聯邦公報**
- **一手來源**
  - FTC 新聞稿「FTC Seeks Public Comment on Whether to Update Rule on Impersonation of Government and Businesses to Address Platforms’ Role in Promoting Impersonation Scams」
    `ftc.gov/news-events/news/press-releases/2026/09/ftc-seeks-public-comment-whether-update-rule-impersonation-government-businesses-address-platforms` — 200／1,001,890 B
  - ANPRM 擬刊文本 `ftc.gov/system/files/ftc_gov/pdf/r207000_impersonation_anprm_1.pdf` — 200／518,683 B／43 頁（16 CFR Part 461、RIN 3084-AB90、Matter No. R207000）
  - 佐證：法規頁 `ftc.gov/legal-library/browse/federal-register-notices/rule-impersonation-government-businesses-anprm` 200／987,326 B；
    Federal Register API 200／13,591 B 與公開檢閱清單 200／168,493 B（**兩者都沒有這份 ANPRM**）
- **讀到的內容**：FTC 在考慮是否修改《冒充政府與企業規則》或採取其他行動，處理社群、搜尋引擎等平台的廣告最佳化工具
  「may be furthering」冒名詐騙的問題；徵詢的措施包括審核廣告主、監控廣告、調查與下架確認的冒名廣告、處分違規廣告主。
  委員會以 2-0 通過送刊。新聞稿引用的數字：2025 年收到超過 100 萬件冒名詐騙通報、通報損失近 35 億美元；
  通報有損失的消費者中近 30% 說最初是在社群平台被接觸，通報損失 21 億美元。
- **為什麼重要**：台灣讀者對「臉書上的名人投資詐騙廣告」非常熟悉。美國主管機關正式開始問「平台要不要為自己最佳化出去的詐騙廣告負責」，
  是平台責任這條線上的一個具體節點；`tech.md` 的法規範圍明列「平台責任」。
- **容易寫錯的地方**
  1. **ANPRM 不是草案、更不是新規則**：FTC 是在「徵詢是否需要立法」，現在平台沒有任何新義務。
  2. **意見截止日是公式**：擬刊文本寫 “[INSERT DATE 60 DAYS AFTER DATE OF PUBLICATION IN THE FEDERAL REGISTER]”。截至 2026-09-26 查核未刊登，**不可寫日期**。
  3. 35 億、21 億、30% 都是**消費者自行通報**的數字，新聞稿自己說真實損失可能更高；不要寫成「平台造成 35 億美元損失」。
  4. “may be furthering” 是 FTC 的對沖措辭，不可寫成「FTC 認定平台助長詐騙」。
  5. 適用範圍是美國；不要寫成對台灣有效力。若要對照台灣制度，要另找台灣的一手來源，不可憑印象寫法條。
- **重疊**：`existing-packs.txt` 無；`automation-candidates.tsv` 無（自動化的 FTC 相關項目只有幣圈）。

### 6. 微軟新 Surface Pro 12 吋與 Surface Laptop 13 吋（Snapdragon X2 Plus）— 建議「次要」

- **建議 slug** `tech-news-surface-x2-plus-20260923`
- **事件日** 2026-09-23（Microsoft Devices Blog；feed 時間 20:30Z＝台北 09-24 04:30）
- **一手來源**：Microsoft Devices Blog「Introducing the next Surface Pro 12-inch and Surface Laptop 13-inch with Snapdragon X2 Plus…」
  `blogs.windows.com/devices/2026/09/23/introducing-surface-pro-12-inch-and-surface-laptop-13-inch-with-snapdragon-x2/` — 200／144,061 B。
  **第二條一手來源目前沒有**（台灣微軟新聞中心 feed 停在 2025-08-29），撰稿前要補，例如微軟官方規格／上市地區說明頁。
- **讀到的內容**：在 Snapdragon Summit 上發表；Surface Pro 12 吋起價 US$1,149.99、Surface Laptop 13 吋起價 US$1,199、Surface Mouse US$79.99（觸覺回饋、Bluetooth 6.0），
  **10 月 13 日起在 “select markets” 上市**。Pro 12 吋無風扇、500 nits 螢幕；Laptop 13 吋官方電池 22.5 小時（附註腳）；
  Pro 12 吋另提供 5G 選配（寫在企業客戶段落）。效能宣稱：Office 最高快 17%、電池效率最高 18%、繪圖超過 60%、NPU 本機推論最高 95%。
- **為什麼重要**：主流價位的 Windows on Arm 筆電改版，和第 3 則同一場高通活動；讀者會想知道規格差異與何時能買到。
- **容易寫錯的地方**
  1. **台灣不在文中**，只有 “select markets”；不可寫台灣上市日或台幣價格。上一代在台灣的上市資訊只存在於那個死 feed 裡，不能當這一代的依據。
  2. **同一頁的註腳編號前後不一致**：開頭段寫「18% … ²、60% … ³、95% … ⁴」，下方條列同樣三個數字標「⁸」「²,⁹」「³,⁸」。引用數字前要把對應註腳逐條讀完，不能只看上標。
  3. 所有百分比都是「最高」且為微軟宣稱；「22.5 小時」要連註腳條件一起寫。
  4. 5G 選配寫在企業段落，不可推定消費者版也有。
  5. 文中沒有說 X2 Plus 是本週新發表的晶片，不要寫「首款搭載全新 X2 Plus」。
- **重疊**：`existing-packs.txt` 無 Surface；`automation-candidates.tsv` 的微軟項目是 Copilot（不同事件）。

### 7. 健保卡元件 Linux 版（全景 CGServiSign／NHIServisign）OS 指令注入漏洞 — 建議「次要」，補第二來源前不可動筆

- **建議 slug** `tech-news-nhi-servisign-linux-20260923`
- **事件日** 2026-09-23（TVN 公開日期）；CVE 紀錄發布 2026-09-23T08:18Z＝台北 16:18
- **一手來源**
  - TWCERT/CC TVN-202609009（中文）`twcert.org.tw/tw/cp-132-11213-28a81-1.html` — 200／23,741 B
  - TWCERT/CC TVN-202609009（英文）`twcert.org.tw/en/cp-139-11214-89281-2.html` — 200／17,191 B
  - CVE-2026-15027 紀錄 `cveawg.mitre.org/api/cve/CVE-2026-15027` — 200／3,720 B（CNA：twcert）
  - ⚠️ **健保署或全景自己的公告／下載頁沒有取得**（搜尋線索被 DuckDuckGo 以 202 限流），三條都出自同一個 CNA，嚴格說還算不上兩條獨立來源
- **讀到的內容**：影響產品「Linux版NHIServisign_1.0.23.1227」；全景軟體的 CGServiSign 有 OS Command Injection，
  未經身分鑑別的遠端攻擊者可誘導受害者瀏覽惡意網頁，在受害者本機執行任意指令；CVSS 4.0 為 8.6、CVSS 3.1 為 8.8；
  解法是更新到 Linux 版 NHIServisign 1.0.26.0625（含）以上。CISA ADP 評估 `Exploitation: none`、`Automatable: no`。
- **為什麼重要**：這是視窗內唯一一則「台灣特有、個人電腦上就有」的資安題目——用健保卡做網路服務的 Linux 使用者要自己更新元件。
- **容易寫錯的地方**
  1. **只列了 Linux 版**，不可擴大到 Windows、macOS。
  2. **只列了一個受影響版本（1.0.23.1227）**，不可寫「1.0.26.0625 以前全部受影響」。
  3. 沒有已遭利用的證據。
  4. 產品名兩個：CVE 用 CGServiSign，TVN 影響產品寫 NHIServisign，要一起寫並說明關係，不要自己推定「所有使用 ServiSign 的網銀元件」。
  5. 受眾很小（Linux 桌面＋健保卡），排序因此放在第 7。
- **重疊**：`existing-packs.txt` 無；`automation-candidates.tsv` 無。

### 8. Chrome 154 進入穩定版，一次修補 108 個安全問題 — 建議「備選」

- **建議 slug** `tech-news-chrome-154-20260922`
- **事件日** 2026-09-22 11:19 PDT（＝18:19Z＝台北 **09-23 02:19**）
- **一手來源**：Chrome Releases「Stable Channel Update for Desktop」
  `chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0856730748.html` — 200／353,811 B，
  但**正文由腳本載入**（去掉 script 後只剩 1,879 字，版本號只出現在標記裡）；全文實際是從 feed 項目讀的（feed 200／256,123 B）。
  研究紀錄要照規則 7 寫明這一點。**撰稿前要補**第二條來源（Chrome 安全頁或 Chromium 部落格）。
  注意 9 月有兩篇同名文章，另一篇 `…_0194356994.html`（200／167,488 B）不是 154 版。
- **讀到的內容**：Chrome 154 升到 Windows、Mac、Linux 穩定版（154.0.8037.57，Win／Mac 另有 .58），「will roll out over the coming days/weeks」；
  文中寫 “This update includes 108 security fixes.”；同日 Extended Stable 152.0.7977.140、Android 154.0.8037.57、iOS 154.0.8037.55。
  **全文沒有 “in the wild”**。
- **為什麼重要**：幾乎每位讀者都有 Chrome；數量異常大。但沒有已遭利用的漏洞，新聞性比第 1～7 則低。
- **容易寫錯的地方**
  1. 嚴重度分布（我照清單數出來是 Critical 11、High 25、Medium 47、Low 25）是**研究者自己數的**，官方只印了總數 108，照規則 9 不可當事實寫。
  2. 「108 個修補」不是「108 個被利用的漏洞」。
  3. 分批推送，不能寫「今天所有人都已更新」。
- **重疊**：`tech-news-chromium-v8-kev-20260909`（V8 零時差）同產品、不同事件；`automation-candidates.tsv` 無。

---

## 讀不到／查不到的事件

- **NCC**：官網整站回 Cloudflare 挑戰頁（403／5,469 B），規則禁止繞過。
  替代管道：行政院公報 09-23（第 178 期 29 筆）、09-24（第 179 期 33 筆）逐筆看過，**無 NCC 項目**，09-25 為中秋節 0 筆；
  行政院「部會新聞」RSS（100 筆，到 09-23T16:00Z）與列表第 7～15 頁（到 09-21）**無 NCC 項目**。
  所以是「**NCC 新聞稿未查到**」，不是「沒有發生」。
- **FCC**：403／392 B。Federal Register 公開檢閱清單有一筆 FCC「Meetings; Sunshine Act」（文件號 2026-19920，預定 09-29 刊登），**內容沒讀**。
- **Samsung**：60 秒逾時。
- **ASUS 資安公告**：頁面是 JS 轉址，沒有取得公告列表。**QNAP**：列表 200／191,192 B，但我的日期比對沒有命中，沒有逐則確認。
- **Qualcomm Summit 第二天**：OnQ 部落格與 press kit 沒有 `.md`（404），sitemap 只列出 4 則新稿；PC 平台是否另有發表**沒查到**。
- **歐盟競爭案件登錄**：JS 外殼（29 字）。
- **Synology DSM 版本說明頁**：JS 外殼（770 字）。
- **健保署的 NHIServisign 更新公告**：沒找到（見第 7 則）。
- **Qualcomm 對 Apple 授權的 8-K**：`sec.gov` 依 `BRIEF.md` 會 403，本輪沒有嘗試。

## 需要協調者裁示的地方

1. **第 3、4 則要不要合併**成一篇「2 奈米旗艦手機晶片：天璣 9600 Pro 與 Snapdragon 8 Elite Gen 6」。
   合併的好處是讀者真正的問題是「下一支旗艦手機用哪顆」；缺點是一篇在視窗內、一篇是補遺，而且兩家的語系與代工廠寫法差異很大，研究紀錄會很長。
   若合併，slug 建議用較晚的事件日 `tech-news-2nm-flagship-phone-chips-20260922`。
2. **第 1 則的 slug 日期**用 09-22（修補）還是 09-25（KEV）。
3. **第 1 則是否算「第三篇 KEV」**：站主上一輪對 Zyxel 已經說過同機制要他決定。
4. **兩則補遺（第 2、4 則）都要，還是只留一則。** 兩則都在 09-15～09-18，距今一週多。

## 來源與既有說法衝突、以來源為準的地方

1. 上一輪寫「NCC 整站是 Angular 外殼」；本輪實測是 **Cloudflare 挑戰頁（403）**。以本輪觀察為準。
2. `candidates-tech-and-ai.md` 的 feed 表寫 CISA 的 `all.xml` 回 403；本輪改走 **KEV JSON，200 可用**，而且逐 CVE 帶 `dateAdded`，比公告頁可靠。
3. 視窗以台北日期界定，但幾則官方日期是美國或夏威夷當地日期：WordPress 的 KEV 在台北已是 09-26、Surface 在台北是 09-24、
   Snapdragon 新聞稿沒有時刻。slug 照指示用「事件日」，本頁一律用**官方電頭或公告上的日期**，並在各則寫出台北換算。
4. CISA 09-25 的公告讓 MikroTik 看起來是本週事件；CVE 紀錄的 ADP 欄位與 KEV JSON 都顯示同一攻擊鏈 09-10 就入 KEV，**以來源為準判為視窗外的舊事件**。

---

## 懷疑但沒有查證的事

1. **歐盟 DMA 對 Google Search 的案件在 09-25 有新動作**：DuckDuckGo 的搜尋摘要顯示 `competition-cases.ec.europa.eu` 有一列
   「25.09.2026 DMA.100193 Alphabet - Online Search Engine - Google Search - Art. 6 (5)」，但該頁是 JS 外殼，DMA 專站新聞最新仍是 07-23。可能是新決定，也可能只是案卷上架文件。
2. **FCC 10 月公開會議議程**（上面那筆 Sunshine Act 通知）可能含頻譜或電信項目，沒讀。
3. **NCC 09-23 委員會議的決議**：搜尋摘要只看到 NCC 首頁有「2026 防制科技犯罪研習班」與「EuroDIG」兩則活動稿，沒有決議稿。
4. **Snapdragon Summit 第二天的 PC 平台發表**：OnQ 標題有 “snapdragon-summit-agentic-ai-pcs-linux”，內容沒讀到。
5. **新 Surface 與 Snapdragon 8 Elite Gen 6 手機的台灣上市與售價**：沒有任何官方來源。
6. **WordPress 漏洞的實際受害規模或是否有台灣網站受害**：CISA 沒給，沒找到其他一手來源。
7. **健保署是否另外推播 NHIServisign 更新**。
8. **Qualcomm–Apple 授權的條件與金額**：只有兩句新聞稿，是否有 8-K 沒查。
9. **ASUS、QNAP 在視窗內是否有路由器或 NAS 公告**：頁面沒有成功解析。
10. **TWCERT 其他 TVN（例如 TVN-202609010 融易網路 GPM LIGHT）** 的公開日期沒查。

---

## 統計

- 掃過的管道：管道表 44 列（部分列合併兩條以上管道；其中 7 列讀不到或只有外殼：Qualcomm 新聞列表、歐盟競爭案件登錄、NCC、FCC、Samsung、ASUS、MSRC），
  另加行政院公報 62 筆、行政院部會新聞 RSS 100 筆與列表 9 頁逐筆檢視。
- **候選 8 則**：重要 4（WordPress、Synology〔補遺〕、Snapdragon、天璣 9600〔補遺〕）、次要 3（FTC 冒名詐騙廣告、Surface、健保卡元件 Linux 版）、備選 1（Chrome 154）。
- **不寫**：MikroTik（事件在 09-05／09-10）、Qualcomm–Apple 授權（只有一條來源）、其餘 7 個企業產品 KEV、Meta Connect（自動化已有）、
  C10 Max（改維護票給 Googlebook 那篇）、以及活動稿、AI 主體與例行更新各項，見「看過、不寫的」表。
- **維護票 1**：`tech-news-googlebook-launch-20260921` 補一段聯發科 Dimensity CX C10 Max（聯發科 09-21 新聞稿 200／99,688 B：台積電 3 奈米、NPU 890 最高 55 TOPS、供「即將推出的」Googlebook 機種）。
