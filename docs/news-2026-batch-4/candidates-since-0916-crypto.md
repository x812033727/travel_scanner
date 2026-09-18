# 幣圈候選：2026-09-16 起（批次 4.5 前期研究）

窗口：**2026-09-16 00:00 UTC 至 2026-09-18**（以**發布日**界定）。
查核日：**2026-09-18**。垂直界線見 [`crypto.md`](crypto.md)：**只寫法規、技術與產業運作，不碰行情**。
先前的候選清單在 [`candidates-crypto.md`](candidates-crypto.md)（C1–C11 已全部寫成文章）。

所有請求都用 `curl -sL -A "Mokaair-editorial"`。下面每一則都記了**狀態碼與 bytes**，
被擋或讀不到的一律寫「未查到」或「讀不到」——**沒查到不等於沒發生**。

---

## 結論

**窗口內有三則可以直接開稿，另有一則是這三天最大的事件但全文讀不到。**

三則可寫的都不在美國的聯邦公報上：兩則來自英國 FCA，一則是 CFTC 的職員函。
只看聯邦公報會把這三天判成「沒有幣圈新聞」，那是錯的（見下面「一個會騙人的零」）。

台灣、日本、歐盟、韓國在這三天**沒有**幣圈項目；新加坡 MAS 與香港 SFC 在本容器**讀不到**。

---

## 掃過的管道與結果

### 美國

| 管道 | 結果 |
| --- | --- |
| Federal Register API，機關過濾 SEC | HTTP 200、17,414 bytes、17 筆（9/16–9/17），全部是 SRO 規則申報、NMS Plan 與 OMB 資料蒐集展延，**無幣圈** |
| 同上，CFTC | 200、2,195 bytes、1 筆：2026-09-16 `Whistleblower Award Determination`（Rule），**非幣圈** |
| 同上，FinCEN／OCC／NCUA／Federal Reserve | 各 200，`count` 皆為 **0** |
| 同上，FDIC | 200、1,052 bytes、1 筆：9/17 Sunshine Act 會議通知，**非幣圈** |
| 同上，Treasury | 200、1,987 bytes、1 筆：9/16「Racial Nondiscrimination in Private Schools; Hearing」，**非幣圈** |
| Federal Register **全文檢索**（`conditions[term]`，gte 2026-09-16） | `crypto` 0、`stablecoin` 0、`digital asset` 0、`blockchain` 0、`virtual currency` 0、`tokenized` 0。對照組 `securities` 命中 **55 筆**，證明索引有資料 |
| Federal Register 2026-09-18 當日 | `count` **0**。**今天的公報在本容器還查不到**，所以 9/18 若有幣圈刊登，本次掃不到 |
| Federal Register 公開閱覽（public inspection current） | 200、191,967 bytes、117 筆，`filed_at` 只有 9/16 與 9/17；SEC 的部分全是 SRO 申報與 Sunshine Act，**無幣圈** |
| SEC 新聞稿 RSS `/news/pressreleases.rss` | 200、18,415 bytes、25 則。**9/17 有一則幣圈**（見候選表第 4 列） |
| SEC 聲明 RSS `/news/statements.rss` | 200、11,983 bytes、25 則。9/17 有三位委員對同一件事的聲明；9/16 的三則是 Rule 14a-8 委託書題目，**非幣圈** |
| SEC 演講 RSS `/news/speeches.rss` | 200、11,353 bytes、25 則，9/17 是 24 小時交易圓桌，**非幣圈** |
| `www.sec.gov` 的 HTML 頁 | **403**，body 1,922–1,924 bytes，標題 `SEC.gov │ Request Rate Threshold Exceeded`。以 `Mokaair-editorial`、curl 預設 UA、加 `Accept`／`Accept-Language`、去掉 `www.` 四種組合各試一次，**全部 403**。另外 `/news/{rulemaking,rules,proposed,final,orders,exorders,litigation}.rss` 六個路徑都 **404**（53,435 bytes 的軟性 404） |
| CFTC 新聞稿 RSS `/RSS/RSSGP/rssgp.xml` | 200、4,644 bytes、10 則。**9/17 有一則幣圈**；9/16 與 9/18 沒有新聞稿 |
| CFTC 新聞稿列表頁 `/PressRoom/PressReleases` | 200、64,997 bytes、38 列（伺服器端算好的表格，含日期＋編號），與 RSS 一致 |
| CFTC 職員函下載端點 `/csl/<函號>/download` | 26-25 回 200、232,223 bytes PDF（7 頁）；26-09 回 200、312,032 bytes PDF（7 頁）。**兩份都抽到全文** |
| OFAC Recent Actions | 200、44,672 bytes。9/16、9/17 各一批，標題是伊朗／古巴／白俄／俄羅斯／委內瑞拉的指定與除名，**標題沒有加密資產字樣**。未逐筆比對 SDN 名單裡是否含數位資產位址 |
| FinCEN `/news-room/news`、OCC `/news-issuances/news-releases/index.html` | **404**，未查到可用列表 |

### 台灣

| 管道 | 結果 |
| --- | --- |
| 金管會新聞列表（`news_list.jsp` 表單，`pagesize=100`）關鍵字「虛擬資產」 | 200、145,465 bytes、**30 則**，最新一則 **2026-08-04**（`dataserno=202608040002`，推動轉帳規則）。**窗口內 0 則** |
| 同上，關鍵字「加密資產」 | 200、125,229 bytes、**0 則**（該列表只搜標題） |
| 同上，關鍵字「穩定幣」 | 200、125,188 bytes、**0 則** |
| 同上，關鍵字「虛擬通貨」 | 200、132,441 bytes、7 則，最新 **2024-11-21** |
| 金管會全部新聞列表（不帶關鍵字，`pagesize=60`） | 200、185,070 bytes。9/17 三則（住宅火險提醒、中小企業放款、證期局每日新聞）、9/16 一則（證期局每日新聞），**無幣圈**；9/18 當天尚未上架 |
| 行政院公報全文查詢「虛擬資產」 | 200、50,767 bytes、10 則，最新 **2026-09-03**（財政部令，見下面「窗口外的線索」）。**窗口內 0 則** |
| 同上，「穩定幣」3 則／「虛擬通貨」10 則／「代幣」10 則／「加密資產」**0 則** | 皆 200，窗口內都沒有項目 |
| 行政院公報卷期瀏覽（`browseVolume.do?pubdate=…`） | 200、49,738 bytes，但回的是最近刊登的混合清單而不是指定日期那一期；抓到的 10 則裡「虛擬／加密／穩定幣／代幣」各 0 次。**這條路徑不可靠，用關鍵字全文查詢代替** |
| 全國法規資料庫《虛擬資產服務法》`pcode=G0400163` | 200、92,407 bytes。2026-09-18 仍顯示「※本法規部分或全部條文尚未生效，**最後生效日期：未定**」，公布日民國 115 年 7 月 22 日、全文 56 條、施行日期由行政院定之。**窗口內沒有變動** |
| `law.fsc.gov.tw` 法規內容 `id=GL004301` | 200、105,035 bytes（本次只確認可取得，未細讀） |

> ⚠ **行政院公報的查詢端點要照首頁熱門關鍵字連結的完整參數**。
> `advancedSearchResult.do?action=doQuery&keywords=<enc>&fields=text` 單獨用會回 **HTTP 500**；
> 可用的形式是重複三組 `keywords`／`fields`／`logics`：
> `…?action=doQuery&keywords=<enc>&fields=text&logics=AND&keywords=&fields=text&logics=AND&keywords=&fields=text`。

### 日本

| 管道 | 結果 |
| --- | --- |
| FSA 英文新聞索引 `/en/news/index.html` | 200、31,559 bytes。最新一則 **2026-09-15**（FSA Strategic Priorities），**窗口內 0 則** |
| FSA 日文「報道発表資料」`/news/index.html` | 200、57,794 bytes。令和８年９月17日四則全是課徴金納付命令（內線交易、虛偽記載、相場操縦）；９月16日兩則是內閣府令公布與監督指針改正案的 パブコメ 結果 |
| 上述 9/16 兩則逐則開頁 | `/news/r8/sonota/20260916/20260916.html` 200、37,885 bytes；`/news/r8/shouken/20260916/20260916.html` 200、36,997 bytes。兩頁「暗号資産」與「電子決済手段」各 **0 次**，**非幣圈** |
| `/newsmenu.html` | **404**（36,020 bytes 軟性 404），正確路徑是 `/news/index.html` |
| JVCEA 首頁 | 200、104,510 bytes。窗口內只有 **2026.09.16「新規取扱銘柄のお知らせ」**（上架公告），屬標的／行情範疇，`crypto.md` 明文排除 |

### 歐盟

| 管道 | 結果 |
| --- | --- |
| ESMA 新聞頁 | 200、97,890 bytes，最新 **10/09/2026**，**窗口內 0 則** |
| ESMA RSS `/rss.xml` | 200、73,077 bytes、10 則，與新聞頁一致（RSS 沒有 `pubDate`，日期要看網頁） |
| EBA 新聞稿頁 | 200、75,117 bytes。窗口內只有 **2026-09-16「European Parliament confirms Thomas Gstädtner as Executive Director of the EBA」**，**非幣圈** |
| EBA RSS `/rss.xml` | 200、18,166 bytes、10 則。9/16 的 e-mail alert 只帶上面那一則人事案 |
| EBA `/regulation-and-policy/markets-crypto-assets` | **404**（10,517 bytes） |

### 其他法域

| 管道 | 結果 |
| --- | --- |
| 英國 FCA 新聞列表 `/news` | 200、185,794 bytes，伺服器端算好的列表、每則帶 `dd/mm/yyyy` 與分類。**9/16 與 9/17 各一則幣圈**。當天稍後再抓一次，沒有新增 18/09 的項目 |
| 韓國 FSC 英文新聞稿 `/eng/pr010101` | 200、76,566 bytes。窗口內只有 **2026-09-16「FSC Proposes Rule Changes under Revised FSCMA on Valuation Method in M&A Transactions」**，**非幣圈**。最近的幣圈項目是 2026-09-04（證券代幣化路線圖）與 2026-08-11（VASP 登記與 AML 規則），都在窗口外 |
| 新加坡 MAS `/news` | HTTP **200 但 body 是維護頁**：「Sorry, this service is currently unavailable.」——**讀不到**。與 `candidates-crypto.md` 先前記的「這個容器連不到 MAS」一致。MAS 的穩定幣論詢仍未回到一手來源 |
| 香港 SFC | `/en/Newsroom`、`/en/Newsroom/Latest-news`、`/en/Newsroom/News`、`/en/Newsroom/News/News-and-announcements`、`/en/Newsroom/News/Enforcement-news` **全部 404**（85,214 bytes 的軟性 404 頁）；`apps.sfc.hk/edistributionWeb/…` 回 200 但是 3,908 bytes 的 SPA 殼。**讀不到** |
| FATF publications | 200、170,701 bytes，頁上最新項目 **2026-06-19**，**窗口內 0 則** |
| BIS `/list/press_releases/index.htm` | **404**（111,896 bytes），**未查到**可用列表 |

### 一個會騙人的零

聯邦公報的全文檢索在 2026-09-16 之後對 `crypto`、`stablecoin`、`digital asset`、
`blockchain`、`tokenized`、`virtual currency` 六個詞**全部命中 0 筆**，
而同一個窗口裡 SEC 與 CFTC 各有一件加密資產相關的實質動作。

原因是**兩件事都不走聯邦公報**：CFTC 的是部門層級的職員函（`cftc.gov/csl/<函號>/download`），
SEC 的豁免命令則還沒送到公報。`candidates-crypto.md` 把 Federal Register API 記成
「`sec.gov` 被 403 擋掉時的官方刊登管道」是對的，但它**不是美國幣圈監理的全集**。

---

## 候選清單

| 日期 | 標題 | 來源狀態 | 建議 | 重疊 | 研究紀錄／不寫的理由 |
| --- | --- | --- | --- | --- | --- |
| **2026-09-16** | FCA 發布政策聲明 **PS26/18《Cryptoasset perimeter guidance》**：加密資產活動何時需要 FCA 授權的最終指引。新制 2027-10-25 生效、授權申請 2026-09-30 開放、想用過渡規定者 2027-02-28 截止；既有登記不自動轉換 | ✅ 新聞稿 200／175,820 bytes、出版品頁 200／177,578 bytes、PS26/18 PDF 200／1,579,276 bytes（140 頁、抽出 316,691 字元），**三份都讀到正文** | **重要** | 與 `crypto-news-mica-transition-ends-20260701`、`crypto-news-taiwan-vasp-act-20260630` 只在「制度時程對照」上相鄰，不重寫 | [`research/crypto-news-fca-perimeter-guidance-20260916.json`](research/crypto-news-fca-perimeter-guidance-20260916.json) |
| **2026-09-17**（行動日 **09-10**） | FCA 與 HMRC、倫敦警察廳對倫敦三處涉嫌非法點對點加密資產交易的場所發出停止並終止通知書。依 MLRs 2017；FCA 表示英國目前沒有任何一家登記的點對點加密資產業者 | ✅ 新聞稿 200／175,752 bytes、4 月那篇 200／176,507 bytes、Firm Checker 說明頁 200／85,989 bytes，**三份都讀到正文** | **次要** | 與上一則同為 FCA，研究紀錄已寫好分界（新制 vs 現行洗錢防制） | [`research/crypto-news-fca-p2p-crypto-crackdown-20260917.json`](research/crypto-news-fca-p2p-crypto-crackdown-20260917.json) |
| **2026-09-17** | **CFTC 職員函 26-25**：市場參與者部門把「被動軟體提供者」不必登記為介紹經紀商的無異議立場，從 2026-03-17 只對單一申請人（自我保管加密資產錢包開發商）生效，擴大到所有同類業者，附十項條件 | ✅ 新聞稿 200／34,508 bytes、函 26-25 PDF 200／232,223 bytes、函 26-09 PDF 200／312,032 bytes，**三份都讀到正文** | **次要**（若站主想要第二篇美國題可升重要） | 與 `crypto-news-sec-crypto-interpretation-20260323`、`crypto-news-sec-regulation-crypto-assets-20260821` 不重疊（商品交易法的中介機構登記 vs 證券法） | [`research/crypto-news-cftc-passive-software-20260917.json`](research/crypto-news-cftc-passive-software-20260917.json) |
| **2026-09-17** | **SEC 發布「Innovation Exemption」**：對「Tokenized Securities Venues（TSV）」給予暫時、附條件的豁免，使其不受 1934 年證券交易法「exchange」定義拘束，以交易代幣化 NMS 股票，並同時徵詢意見（新聞稿 2026-90） | ⚠ **只讀到官方 RSS**（`/news/pressreleases.rss` 200／18,415 bytes）給的標題、連結、`pubDate`（Thu, 17 Sep 2026 08:55:00 -0400）與官方一句話摘要（官方自己截斷在「…to trade…」）。新聞稿 HTML 與命令全文 **403**；聯邦公報**尚未刊登**，公開閱覽清單也沒有 | **重要，但現在不能開稿** | 與既有兩篇 SEC 不重疊，是新題 | **不寫**：湊不出 2–4 條「自己讀到正文」的白名單來源，只靠一句被截斷的摘要寫不出一篇。**建議做法**：用 Federal Register API 監看 `conditions[term]=tokenized` 或 `Tokenized Securities Venues`，刊登後立刻開票；或在能讀 `sec.gov` 的環境取得命令全文再開 |
| **2026-09-17** | SEC 三位委員各發一份關於 Innovation Exemption 的聲明（Atkins、Peirce、Uyeda，09:00–09:20 ET） | ⚠ 只讀到 `/news/statements.rss`（200／11,983 bytes）的標題、作者與時間；內文頁 **403** | **不寫** | 併入上一則 | **不寫**：只有標題不能寫成內容或立場。可以在上一則裡寫「同日有三位委員各發表一份聲明」這個事實，不得引述或推測內容 |
| **2026-09-16** | JVCEA「新規取扱銘柄のお知らせ」 | ✅ 首頁列表 200／104,510 bytes 讀到 | **不寫** | — | **不寫**：這是特定標的的上架公告，落在 `crypto.md` 明文排除的「任何具體標的當成可以持有的東西」界線內 |

---

## 窗口外的線索（本批次不寫，建議另外開票）

掃描時撈到一則**很接近、但在窗口外**的台灣題目，記在這裡以免下一個代理重查：

- **2026-09-03｜財政部令｜台財稅字第 11504611390 號**
  「有關營業人銷售『虛擬資產服務法』第 3 條第 1 款及第 6 款所定虛擬資產及穩定幣，
  非屬營業稅課稅範圍之相關規定」
  行政院公報 032 卷 164 期（出刊日 2026-09-03），類型為行政規則（行政程序法第 159 條第 2 項第 2 款）。
  詳目頁 `https://gazette.nat.gov.tw/egFront/detail.do?metaid=168088`（200／28,835 bytes），
  另有網頁文字版與 PDF 兩個檔案連結。
  這正好補上 `candidates-crypto.md` 說「已搜過 `mof.gov.tw`／`etax.nat.gov.tw`／`ntbt.gov.tw`，
  沒有找到 2026 年的專門公告」的那個缺口——**公告在行政院公報上，不在國稅局網站上**。
  稅務申報實務在 `crypto.md` 的可寫清單裡，建議單獨開一張票（事件日 2026-09-03）。

---

## 給下一個代理的三條管道筆記

1. **CFTC 的實質決定常常是職員函，不是規則。** `https://www.cftc.gov/csl/<函號>/download`
   回 200 且是 `application/pdf`，可直接抽文字。只看聯邦公報會整批漏掉。
2. **FCA 的出版品頁比新聞稿好用。** `/publications/policy-statements/<編號>` 把
   「Consultation opens／Consultation closes／Policy statement」三個日期分欄列出，
   還有「First published／Last updated」，不必從版面猜日期。
   另外 **FCA 會回頭修訂已發布的新聞稿並在頁面上方標明改了哪一段**——
   2026-04-22 那篇在 2026-05-18 被改過，補上「以個人身分進行的點對點交易不需要 FCA 登記」
   這句關鍵但書，只讀最初版本會把整件事寫錯。
3. **執法類新聞的「行動日」與「公布日」常差一週以上**，而且 FCA 把行動日放在
   `Notes to editors` 而不是內文（本例 9/10 對 9/17）。抄列表上的日期會寫錯事件日。
