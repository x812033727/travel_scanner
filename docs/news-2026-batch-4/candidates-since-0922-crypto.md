# 幣圈候選：2026-09-22 起（批次 4.8 前期研究）

窗口：**2026-09-22 00:00 台北（2026-09-21T16:00Z）至 2026-09-26**。
查核日：**2026-09-26**。垂直界線見 `docs/news-2026-batch-4/crypto.md`：**只寫法規、技術與產業運作，不碰行情**。
上一輪清單在 `docs/news-2026-batch-4/candidates-since-0920-crypto.md`（兩則已寫成文章）。

所有請求都用 `curl -sSL -A 'Mokaair-editorial/1.0 (…)'`，同一主機間隔 ≥1 秒。
下面每一則都記了**狀態碼與 bytes**；被擋或讀不到的一律寫「未查到」或「讀不到」——**沒查到不等於沒發生**。

排除清單：`existing-packs.txt`（站上已有）與 `automation-candidates.tsv`（每小時自動化已撿起或將重跑，不論狀態）。

---

## 結論

**窗口內有三則能寫，再加兩則補遺，共五則。三則窗口內的題目都在亞洲或歐盟，美國這一輪的一手幣圈動作全部已被自動化清單撿走。**

- 美國：窗口內的一手幣圈事件只有聯準會 9/24 穩定幣兩案、CFTC 9302-26／9303-26，**三件都在 `automation-candidates.tsv`**；聯邦公報 9/21 起沒有新的幣圈文件。SEC 窗口內只有委員演講。
- 台灣：金管會 9/22 以後沒有新的幣圈新聞稿（存款代幣試辦已寫），法規預告與函釋頁**與上一輪同 bytes**，行政院公報窗口內 0 則。**台灣題只能靠補遺**：中央銀行 9/17 理監事會資料裡有一整題講穩定幣、存款代幣與 CBDC，這份 PDF 上一輪沒人掃過。
- 日本：**9/25 金融廳成立「AI 時代的鏈上金融論壇」**，是本輪最乾淨的制度題（三份一手文件全讀到）。
- 韓國：**9/23 金融委員會移送 4 件虛擬資產操縱案**，只有韓文版，英文頁沒有。
- 歐盟：**9/24 EBA 的 MiCA 檢討回應**；同週 ESMA 與 ESAs 兩則已在自動化清單。
- 補遺第二則是 **OFAC 9/17 制裁伊朗交易所 BitBank**：上一輪卡在公報名單是 TIFF，這次改讀財政部新聞稿，讀得到。
- MAS、SFC、FATF（本輪變 403）**讀不到**，不是「沒有發布」。

---

## 掃過的管道與結果

### 美國

bytes 一律是**解壓後落地的檔案大小**（`--compressed` 下 curl 回報的 `size_download` 是線上壓縮後的量，會偏小，本輪一開始踩到，已改）。

| 管道 | 網址 | 狀態／bytes | 筆數 | 窗口內與幣圈相關 |
| --- | --- | --- | --- | --- |
| Federal Register API，SEC | `…/documents.json?conditions[agencies][]=securities-and-exchange-commission&conditions[publication_date][gte]=2026-09-21` | 200／44,423 | 54（含 9/28 預排） | 只有 9/22 刊登的 Innovation Exemption 命令（2026-19388，**已寫**）。其餘是 SRO 申報：9/23 Bitnomial、KalshiEX、Coinbase Derivatives 的 security futures 規則，9/24 Coinbase Derivatives 保證金——**都是證券期貨產品規則，不是加密資產規則** |
| 同上，CFTC | `commodity-futures-trading-commission` | 200 | 2 | 9/22 資料蒐集展延、9/21 Privacy Act，**非幣圈** |
| 同上，OCC | `comptroller-of-the-currency` | 200 | 1 | 9/22 MRA 更正，**非幣圈** |
| 同上，FDIC | `federal-deposit-insurance-corporation` | 200 | 6 | 9/22 Merger Transactions（Question 60 提 PPSI，上一輪已判「改維護票」）、State Bank Parity；9/24 資料蒐集 |
| 同上，Federal Reserve | `federal-reserve-system` | 200 | 7 | 只有銀行控股公司申請公告。**9/24 聯準會穩定幣兩案尚未刊登公報** |
| 同上，Treasury／OFAC／IRS／NCUA | 各機關 slug | 各 200 | 16／9／4／1 | OFAC 9/22、9/23 兩次制裁通知與一般許可；IRS 無數位資產項目 |
| 同上，FinCEN | `financial-crimes-enforcement-network` | 200 | **0** | — |
| Federal Register **全文檢索**（gte 2026-09-21） | `conditions[term]="…"` | 各 200 | `stablecoin` 2、`payment stablecoin` 2、`tokenized` 1、`blockchain` 1、`distributed ledger` 1、`digital asset` 2、`crypto` 5、`virtual currency` 0 | 全部指向三份文件：SEC 命令 2026-19388（已寫）、FDIC 併購草案 2026-19308、OFAC 9/17 行動的 9/22 公報通知 2026-19287；`crypto` 另外四筆是國防部軍售（`cryptographic`）。**窗口內沒有新的幣圈公報文件** |
| SEC 新聞稿 RSS | `/news/pressreleases.rss` | 200／18,377 | 25 | 最新 9/23（2026-93 市場統計、2026-92 詐欺案、9/22 2026-91 OTC Link 譴責），**窗口內 0 則幣圈** |
| SEC 聲明 RSS | `/news/statements.rss` | 200／11,584 | 25 | 最新 9/17，窗口內 0 則 |
| SEC 演講 RSS | `/news/speeches.rss`（轉到 `speeches-statements.rss`） | 200／11,466 | 25 | 9/23 Peirce「Looking for Change in Haystacks」（SIFMA 數位資產會議）；9/22 Uyeda 美債市場會議。演講不成篇（見懷疑清單） |
| SEC 訴訟公告 RSS | `/enforcement-litigation/litigation-releases/rss` | 200／10,434 | 25 | 9/21–9/25 共 6 則（LR-26643～26648），標題看不出幣圈，**未逐頁核對** |
| CFTC 新聞稿 RSS | `/RSS/RSSGP/rssgp.xml` | 200／4,637 | 10 | 9/22 9302-26（mention markets）、9/24 9303-26（加密資產 FAQ 更新）——**兩則都在自動化清單，排除** |
| OCC 新聞 RSS | `/rss/occ_news.xml` | 200／9,518 | 10 | 窗口內只有 9/23 房貸績效報告，**非幣圈** |
| 聯準會新聞稿 RSS | `/feeds/press_all.xml` | 200／14,486 | 20 | **9/24「payment stablecoin」兩案徵詢意見**——自動化清單有同一事件（CoinDesk 9/24 “Federal Reserve moves on proposals to implement GENIUS Act”），**排除** |
| FDIC 新聞稿列表 | `/news/press-releases` | 200／79,836 | — | 窗口內：9/25 Nano Banc 倒閉承接、8 月執法行動。**非幣圈** |
| 財政部新聞稿列表 | `home.treasury.gov/news/press-releases` | 200／71,370 | — | 最新 **sb0633（9/22 副部長美債市場演講）**，9/23 之後 0 則。**9/17 sb0632 是 OFAC 對伊朗加密交易所 BitBank 的制裁**（見候選表，補遺） |
| 財政部 sb0632 內頁 | `/news/press-releases/sb0632` | 200／77,674 | — | **正文全部讀到** |
| OFAC Recent Actions | `ofac.treasury.gov/recent-actions` | 200／44,814 | 10 | 窗口內：9/23 剛果相關除名、9/24 TSRA 報告。最近的幣圈是 **9/17 Iran-related Designations** |
| OFAC 9/17 行動頁 | `/recent-actions/20260917` | 200／49,581 | — | SDN 新增條目讀到：`BITBANK … Website www.bitbank3.com; alt. Website www.bitbank.com … [IRAN] [IRAN-EO13902]`，**沒有列數位貨幣地址** |
| FinCEN 新聞列表 | `/news` | 200／46,707 | 8 | 最新 **09/16/2026**（FinCEN Exchange 談 Operation Economic Outcast），窗口內 0 則 |

### 台灣

| 管道 | 網址／參數 | 狀態／bytes | 筆數 | 窗口內與幣圈相關 |
| --- | --- | --- | --- | --- |
| 金管會新聞列表（**不帶關鍵字**，`pagesize=60`） | `home.jsp` POST，`id=96`、`mcustomize=news_list.jsp`、`dtable=News`、`aplistdn=…` | 200／184,609 | 60 | 最新 **2026-09-24**，頁尾「更新日期：2026-09-24」。9/22–9/24 共 11 則：9/22 存款代幣試辦（**已寫**）、9/22「金管會『不會』以LINE聯繫民眾，請民眾慎防二次詐騙」、臺股儀表板、永續揭露、台灣人壽裁罰、連假保險提醒、證期局每日新聞×3。**除已寫的存款代幣外沒有幣圈項目** |
| 金管會 9/22 LINE 詐騙提醒內頁 | `…news_view.jsp&dataserno=202609220003` | 200／111,745 | — | 正文讀到：偽冒金管會「沒收犯罪所得返還」「退款」文書、誘加 LINE。**全文沒有虛擬資產或加密貨幣**，是一般二次詐騙，**不列** |
| 證期局每日新聞 9/22、9/23、9/24 | `dataserno=202609220005`／`202609230002`／`202609240006` | 200／111,123、112,619、110,438 | — | 「虛擬／加密／穩定幣／代幣」**各 0 次**（只有裁罰與公司債補正） |
| 金管會法規草案預告 | `home.jsp?id=133&parentpath=0,3` | 200／145,399 | 4 列 | 最新 **2026-09-07**，窗口內 0 則。**bytes 與上一輪完全相同** |
| 金管會最新法令函釋 | `home.jsp?id=128&parentpath=0,3` | 200／160,419 | 15 列 | 最新 **2026-09-21**（上一輪已判非幣圈），窗口內 0 則。bytes 與上一輪相同 |
| 行政院公報首頁（取 cookie） | `gazette.nat.gov.tw/egFront/` | 200／53,652 | — | — |
| 同上全文「虛擬資產」 | `advancedSearchResult.do?action=doQuery…` | 200／50,767 | **40**（上一輪 39） | 最新仍是 **2026-09-03 財政部令**（營業稅），窗口內 0 則。多出的一筆不在前 10 筆，未追 |
| 同上「虛擬通貨」 | — | 200／55,120 | 52 | 窗口內 0 則 |
| 同上「穩定幣」 | — | 200／38,837 | 3 | 最新 2026-09-03，窗口內 0 則 |
| 同上「代幣」 | — | 200／51,565 | 21（上一輪 20） | 窗口內 0 則 |
| 同上「加密資產」 | — | 200／36,150 | 1（上一輪 0） | 那一筆是 **2024-10-04**，窗口外 |
| 中央銀行新聞稿列表 | `cbc.gov.tw/tw/lp-302-1.html` | 200／44,884 | 19 | 窗口內 7 則全是統計與定存單標售。**9/17 理監事會「外界關心之議題」第七題是 CBDC／穩定幣／存款代幣**（見候選表，補遺） |
| 中央銀行 9/17 記者會頁 | `/tw/cp-302-192885-9e975-1.html` | 200／41,359 | — | 附兩份 PDF |
| 中央銀行「外界關心之議題」PDF | `/tw/dl-227629-e320dda7bf1745d4a0a7aaf935eb0e8c.html` | 200／**2,514,163**（54 頁，pypdf 抽出 35,741 字） | — | 第 43–46 頁「七、數位時代央行貨幣發展趨勢之相關議題」Q1–Q4 **讀到** |
| 中央銀行即時新聞澄清 | `/tw/np-1164-1.html` | 200／**52** | — | **空殼**，讀不到 |

### 日本

| 管道 | 網址 | 狀態／bytes | 筆數 | 窗口內與幣圈相關 |
| --- | --- | --- | --- | --- |
| 金融廳「報道発表資料」 | `/news/index.html` | 200／60,425 | — | 最新 **令和８年９月25日**（7 則）。窗口內 12 則，幣圈相關的是 **9/25「AI時代を見据えたオンチェーン金融フォーラム」の公表** 與同日「（第１回）の開催の公表」（見候選 2）。9/24「MUデジタルバンク設立準備株式会社に対する銀行業の免許の付与」是一般銀行執照，**非幣圈** |
| 金融廳：フォーラム公表頁 | `/news/r8/singi/20260925.html` | 200／35,662 | — | **正文讀到**：令和８年９月25日、金融庁；「AI時代を見据えたオンチェーン金融イニシアティブ」下設跨部會「フォーラム」；所管是**資産運用・保険監督局 暗号資産・ステーブルコイン課 デジタル決済企画室** |
| 金融廳：第１回開催頁 | `/news/r8/singi/20260925-2.html` | 200／35,261 | — | **正文讀到**：令和８年９月30日（水）14:00–15:00，中央合同庁舎第７号館；議事「関係省庁等報告、討議」；**不受理一般旁聽**，議事概要會後公開 |
| 別紙１（イニシアティブ概要） | `/singi/ai_onchain/01.pdf` | 200／239,344（1 頁，抽出 799 字） | — | **讀到**：フォーラム做「官民連携でのロードマップ作成」「決済高度化プロジェクト（PIP）の継続・拡大」「日銀当座預金のオンチェーン対応」等；另設兩個研究會，檢討「様々な資産のトークン化」「ステーブルコイン」「DEX・DeFiやウォレット提供業者」「国債等のトークン化対応」「量子コンピュータによる危殆化リスクの把握」等 |
| 別紙２（成長投資金融戦略 2026-07-21 抜粋） | `/singi/ai_onchain/02.pdf` | 200／429,967 | — | 已下載，**未抽文字**（時限內只讀別紙１） |
| 金融廳英文新聞 | `/en/news/index.html` | 200／31,559 | — | **bytes 與上一輪完全相同**，最新仍 2026-09-15，英文版尚未跟上 9/25 |
| 窗口外、同一頁上 | — | — | — | 9/15「2026事務年度金融行政方針の公表」、9/11「無登録で貸金業を行っている者等（Bit Hills Inc.）に対する警告書」——前者未讀全文（見懷疑清單），後者是**貸金業**不是暗號資產交換業 |

### 歐盟

| 管道 | 網址 | 狀態／bytes | 筆數 | 窗口內與幣圈相關 |
| --- | --- | --- | --- | --- |
| EBA 新聞稿 | `/publications-and-media/press-releases` | 200／74,599 | 13 | 窗口內 4 則：9/25 Risk Dashboard、9/25 CRD 第 113 條 ITS 徵詢、**9/24「The EBA identifies priorities for the review of MiCA」**、9/23 ESAs 秋季風險更新 |
| EBA MiCA 檢討回應新聞稿 | `/publications-and-media/press-releases/eba-identifies-priorities-review-mica` | 200／57,434 | — | **正文全部讀到**（見候選 1） |
| EBA 回應全文 PDF | `/sites/default/files/2026-09/12cb4f01-…/EBA response to EC targeted consultation on MiCA review.pdf` | 200／949,075（41 頁） | — | 已下載，**時限內未抽文字**；開稿時要讀 |
| ESMA 新聞 | `/press-news/esma-news` | 200／97,360 | 10 | 窗口內 3 則：9/24 Euribor 報價行異動（非幣圈）、**9/23「ESMA sets new supervisory priority on digital innovation from 2027」**、9/23 ESAs 秋季風險更新 |
| ESMA 9/23 數位創新監理重點 | — | — | — | **排除**：自動化清單 9/24 有同一事件（CoinDesk “European watchdogs prepare direct oversight of AI and tokenization in retail finance”，網址含 `ai-and-tokenization-a-supervisory-priority-in-2027`） |
| ESAs 9/23 秋季風險更新 | — | — | — | **排除**：自動化清單 9/24 “Quantum threat to Bitcoin could materialize before commercial viability, EU regulators warn” 極可能是同一份（網址 `eu-financial-watchdogs-warn-quantum-computing…`）；未逐字比對 CoinDesk 內文，但依「同事件就排除」從嚴處理 |

### 其他法域

| 管道 | 網址 | 狀態／bytes | 筆數 | 窗口內與幣圈相關 |
| --- | --- | --- | --- | --- |
| 韓國金融委員會（韓文報導資料） | `fsc.go.kr/no010101` | 200／120,203 | 10 | 最新 **2026-09-23**（第 16 次定例會議當天，多則）。**9/23「가상자산시장 불공정거래 혐의자 수사기관 고발·통보」**（見候選 3）。9/24–9/26 為秋夕連假，0 則 |
| 同則內頁 | `/no010101/87783` | 200／88,604 | — | 標題、日期、承辦「가상자산과」讀到 |
| 同則 PDF（보도참고자료，5 頁） | `/comm/getFile?srvcId=BBSTY1&upperNo=87783&fileTy=ATTACH&fileNo=2` | 200／646,943（pypdf 抽出 3,583 字） | — | **正文全部讀到**：4 件、手法、使用者注意事項、金融委「가상자산과」與金監院「가상자산조사국」聯絡人 |
| 韓國金融委員會（英文新聞稿） | `/eng/pr010101` | 200／76,566 | 13 | **bytes 與上一輪完全相同**，最新仍 Sep 16。**英文版沒有 9/23 那則**——只掃英文會漏 |
| 英國 FCA 新聞 | `/news` | 200／186,294 | — | 窗口內：9/25 ITI Capital 特別管理、9/25「Twenty-four CFD firms closing…」、9/23 money mules、9/23 演講「Building the next generation of market infrastructure」、9/22 債務建議 |
| FCA 9/25 CFD 新聞稿 | `/news/press-releases/twenty-four-cfd-firms-closing-crackdown-misuse-uk-authorisation` | 200／175,276 | — | 全頁 `crypto` 只在側欄導覽（Cryptoassets、Crypto investment scams），**非幣圈** |
| FCA 9/23 市場基礎設施演講 | `/news/speeches/building-next-generation-market-infrastructure` | 200／187,531 | — | 談代幣化、穩定幣作結算資產、將與英格蘭銀行發布聯合 tokenisation roadmap、擬就「relevant tokenised investment assets」諮詢保管規則。**演講，不單獨成篇**；9/24 英國銀行代幣化存款試行已在自動化清單 |
| 香港金管局新聞稿 | `hkma.gov.hk/eng/news-and-media/press-releases/` | 200／116,768 | 10 | 9/23–9/25 共 10 則：詐騙提示、存保 20 週年、與印尼央行跨境支付合作、Coin Collection（實體硬幣）。**沒有穩定幣發牌項目** |
| 香港 SFC e-Distribution 新聞 | `apps.sfc.hk/edistributionWeb/gateway/EN/news-and-announcements/news/` | 200／**3,908** | — | **前端渲染空殼**，讀不到 |
| 新加坡 MAS | `/news` | 200／853,817 | — | 整份仍是維護頁「Sorry, this service is currently unavailable.」（與前兩輪同 bytes），**讀不到** |
| FATF 新聞 | `/en/the-fatf/news.html` | **403**／5,556 | — | **Cloudflare「Just a moment...」挑戰頁**（上一輪同網址 200），不繞過，**讀不到** |

### 協議與技術

| 管道 | 網址 | 狀態／bytes | 筆數 | 窗口內 |
| --- | --- | --- | --- | --- |
| Bitcoin Core GitHub releases API | `api.github.com/repos/bitcoin/bitcoin/releases?per_page=5` | 200／11,620 | 5 | 最新 **v31.1（2026-07-08）**、v30.3／v29.4（07-10），**窗口內 0 個版本** |
| Ethereum Foundation 部落格 feed | `blog.ethereum.org/feed.xml`（轉到 `/en/feed.xml`） | 200／527,621 | 639 | 最新 **2026-09-09**（Reddit AMA 公告），窗口內 0 則 |
| BIS 新聞稿 RSS | `bis.org/doclist/all_pressrels.rss` | 200／14,577 | 10 | 窗口內只有 9/23 Basel III 監測（資本與流動性指標），**非幣圈** |
| XRP Ledger 升級延後、Solana 150 ms 結算第二測試網、「Shielded Bitcoin」論文 | — | — | — | **全部在自動化清單，排除**，未另查一手來源 |

---

## 候選清單

依「對台灣一般讀者的重要性」排序。**補遺**＝事件日在 2026-09-12～09-21、沒有人寫過的題（上限兩則，本輪用了兩則）。

| # | 事件日（台北） | 題目 | 建議 slug | 來源狀態 | 建議 | 重疊檢查 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **2026-09-25** | 日本金融廳成立「AI時代を見据えたオンチェーン金融フォーラム」，9/30 首次開會 | `crypto-news-japan-onchain-finance-forum-20260925` | ✅ 公表頁 200／35,662、開會頁 200／35,261、別紙１ PDF 200／239,344，**三份都讀到正文** | **重要** | 無重疊 |
| 2 | **2026-09-17**（補遺） | 中央銀行理監事會「外界關心之議題」說明穩定幣、存款代幣與 CBDC 的差異與分層共存 | `crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917` | ✅ 記者會頁 200／41,359；PDF 200／2,514,163，第七題全文讀到 | **重要** | 與已寫的存款代幣試辦**相鄰但不同事件**（見下） |
| 3 | **2026-09-23** | 韓國金融委員會把 4 件虛擬資產市場操縱案移送檢調（API 自動下單哄抬、發行方雇人對敲灌量以維持上架） | `crypto-news-korea-market-manipulation-referrals-20260923` | ✅ 列表 200／120,203；內頁 200／88,604；PDF 200／646,943，**全文讀到** | **重要** | 無重疊 |
| 4 | **2026-09-24** | EBA 回應歐盟執委會 MiCA 檢討諮詢：多發行人穩定幣、分類邊界、加密借貸與 DeFi | `crypto-news-eba-mica-review-priorities-20260924` | ✅ 新聞稿 200／57,434 讀到；回應 PDF 200／949,075 **已下載未讀** | **次要偏重要** | 無重疊（自動化清單的是 ESMA 9/23 與 ESAs 9/23，不同文件） |
| 5 | **2026-09-17**（補遺；美東 9/17） | 美國財政部 OFAC 制裁伊朗加密交易所 BitBank 及其開發商、三名關係人 | `crypto-news-ofac-iran-bitbank-sanctions-20260917` | ✅ 財政部 sb0632 200／77,674 全文讀到；OFAC 9/17 行動頁 200／49,581 讀到 SDN 條目 | **次要** | 無重疊；上一輪因公報名單是 TIFF 判「不寫」，**現在財政部新聞稿讀得到，理由消失** |

### 1. 日本金融廳「AI 時代的鏈上金融論壇」

- **slug**：`crypto-news-japan-onchain-finance-forum-20260925`；**事件日**：2026-09-25（令和８年９月25日公表；首次會議 2026-09-30）。
- **一手來源**
  - 金融廳「『AI時代を見据えたオンチェーン金融フォーラム』について」`https://www.fsa.go.jp/news/r8/singi/20260925.html`——200／35,662。
  - 金融廳「（第１回）の開催について」`https://www.fsa.go.jp/news/r8/singi/20260925-2.html`——200／35,261。
  - 別紙１「AI時代を見据えたオンチェーン金融イニシアティブ」`https://www.fsa.go.jp/singi/ai_onchain/01.pdf`——200／239,344（1 頁）。
  - （未讀）別紙２「成長投資を促進するための金融戦略」（2026年７月21日）抜粋 `…/ai_onchain/02.pdf`——200／429,967。
- **為什麼重要**：日本把穩定幣、代幣化存款、各種資產代幣化、DEX／DeFi 與錢包業者、國債代幣化、日銀當座預金上鏈、量子電腦風險**放進同一個跨部會檢討框架**，承辦單位是「暗号資産・ステーブルコイン課」。台灣 9/22 剛開放銀行試辦存款代幣，鄰國的監理路線圖是讀者最容易拿來對照的參考點；而且這是**制度題**，完全不碰行情。
- **容易寫錯**
  - 這是**成立檢討場域**，不是修法、不是核准任何產品。別紙１列的都是「以下に関する制度の在り方等について点検・検討」的項目，不可寫成「日本將開放 DeFi」「日本決定國債代幣化」。
  - 「日銀当座預金のオンチェーン対応」列在フォーラム的工作項目下，**不是日銀的決定**；不可寫成「日銀宣布把準備金上鏈」。
  - 第１回「一般傍聴の受付はいたしません」，議事概要會後才公開——9/30 之後才知道討論了什麼，**開稿時要重抓一次**。
  - 頁面沒有列出「関係省庁等」有哪些機關，也沒寫「暗号資産・ステーブルコイン課」何時成立，**不要自己補**。兩個研究會的正式名稱照抄別紙１（「デジタル・分散型金融への対応のあり方等に関する研究会」「AI等の健全な利活用の推進に関する研究会」），頁面沒說它們是新設還是既有。
  - 金融廳**英文新聞頁 bytes 與上一輪完全相同、還停在 9/15**，只看英文會以為沒這件事。
- **重疊檢查**：`existing-packs.txt` 無日本題；`automation-candidates.tsv` 全檔 grep `japan|fsa|onchain|on-chain` 只命中 RockawayX「private credit onchain」（業者募資，不同事件）。**無重疊。**

### 2. 中央銀行：穩定幣、存款代幣與 CBDC 的差異（補遺）

- **slug**：`crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917`；**事件日**：2026-09-17（理監事聯席會議後記者會）。
- **一手來源**
  - 中央銀行新聞稿「115年9月17日央行理監事會後記者會簡報及外界關心之議題」`https://www.cbc.gov.tw/tw/cp-302-192885-9e975-1.html`——200／41,359。
  - 附件「115年9月17日央行理監事會外界關心之議題.pdf」`https://www.cbc.gov.tw/tw/dl-227629-e320dda7bf1745d4a0a7aaf935eb0e8c.html`——200／2,514,163（54 頁）。第七題「數位時代央行貨幣發展趨勢之相關議題」在 PDF 第 44–47 頁（頁面印的頁碼是 43–46）。
- **為什麼重要**：央行用一張表把三者按「發行主體及價值基礎、應用場景、存取及流通方式、監管架構」分開（穩定幣「大多為非銀行機構」、以準備資產為價值基礎、在公共區塊鏈上運作；存款代幣由商業銀行發行、「持有人須在銀行開戶」「通常在私有區塊鏈上運作」；CBDC 分零售型與批發型），並主張三者「可在不同層級共存、互補」。**這正是 9/22 金管會存款代幣試辦那篇讀者最需要、而那篇沒有的背景**，而且是台灣自己的主管機關講的。
- **容易寫錯**
  - 這是**記者會的問答資料**，不是政策決定；央行沒有宣布發行 CBDC 或任何時程。
  - 表格裡的限定詞（「大多」「通常」「原則上僅能在銀行客戶之間轉移」）一個都不能刪（BRIEF 錯誤型態 3）。
  - Q3「除美國川普第二任上台後明確中止推動CBDC計畫外，多數主要經濟體與台灣持續進行相關研究或試點」與 Q4 數位人民幣轉型是**央行的整理**，出處註記「各國央行官網、Atlantic Council及國際媒體報導；本行自行整理」「中田理惠(2026)」——要寫成「央行整理指出」，不是本站查證的事實。
  - **不可把央行 9/17 與金管會 9/22 寫成聯合行動或同一份文件**；存款代幣那篇的研究紀錄明載金管會新聞稿全文「中央銀行」0 次。
  - PDF 頁碼與印刷頁碼差 1，引用時寫清楚用哪一種。
- **重疊檢查**：`existing-packs.txt` 有 `crypto-news-taiwan-deposit-token-pilot-20260922`，其研究紀錄 grep `cbc.gov.tw` 0 次、未引用這份 PDF——**不是同一事件**。自動化清單無台灣題。**站主可選**：獨立成篇，或改成存款代幣那篇的補充段落（維護票）。

### 3. 韓國金融委員會：4 件虛擬資產市場操縱案移送檢調

- **slug**：`crypto-news-korea-market-manipulation-referrals-20260923`；**事件日**：2026-09-23（第 16 次金融委員會定例會議議決，會後發布）。
- **一手來源**
  - 金融委員會報導資料列表 `https://www.fsc.go.kr/no010101`——200／120,203。
  - 內頁 `https://www.fsc.go.kr/no010101/87783`——200／88,604。
  - 보도참고자료 PDF `https://www.fsc.go.kr/comm/getFile?srvcId=BBSTY1&upperNo=87783&fileTy=ATTACH&fileNo=2`——200／646,943（5 頁）。
- **為什麼重要**：這是「詐騙型態與一般人自保」類（`crypto.md` 可寫清單）的好素材：①②兄弟兩人用 API 小額市價單反覆對敲製造「호가창 반짝임 효과」（掛單簿閃爍、看似熱絡）引誘散戶；③借用他人帳戶規避交易所 API 次數限制；④發行方高層雇用「마켓메이킹 업자」以人頭帳戶對敲，灌出的量「전체 거래량의 90% 이상」，先上中型交易所、再拿假量申請大型交易所上架；發行基金會是避稅天堂的紙上公司、白皮書人物「실체가 불분명하거나 가공의 인물」。台灣讀者一樣會碰到這些手法。
- **容易寫錯**
  - **고발（刑事告發）與 수사기관 통보（通報偵查機關）不同**：③是告發，①②④是通報。全部都是「혐의자」，**不是定罪**。
  - 新聞稿**沒有**寫幣種、交易所名稱、不法所得金額，也**沒有**引用法條名稱（全文 `가상자산이용자보호법` 0 次）——不要從媒體或記憶補。
  - 金融委的使用者注意事項裡有「추격매수 자제」（勿追高）這類字眼；本站要寫成**主管機關對操縱跡象的警示**，不可改寫成本站的買賣建議（`crypto.md` 禁止「買賣時機」）。
  - 聯絡單位是金融委「가상자산과」與金監院「가상자산조사국」，調查主體是「금융당국(금융위·금감원)」，不要只寫金融委。
  - **韓國金融委英文新聞頁 bytes 與上一輪一模一樣、停在 Sep 16，沒有這則**；只掃英文會漏掉。9/24–9/26 秋夕連假，後續若有英文版會更晚。
- **重疊檢查**：existing-packs 無韓國題；自動化清單 grep `korea` 0 筆。**無重疊。**

### 4. EBA：MiCA 檢討的優先事項

- **slug**：`crypto-news-eba-mica-review-priorities-20260924`；**事件日**：2026-09-24。
- **一手來源**
  - EBA 新聞稿「The EBA identifies priorities for the review of MiCA」`https://www.eba.europa.eu/publications-and-media/press-releases/eba-identifies-priorities-review-mica`——200／57,434，正文讀到。
  - 「EBA response to EC targeted consultation on MiCA review」PDF（網址見上方歐盟表）——200／949,075（41 頁），**已下載、本輪未讀**。
- **為什麼重要**：MiCA 是全世界最完整的加密資產專法，也是台灣《虛擬資產服務法》子法常被拿來對照的範本。EBA 點名要優先修的地方：第三國「multi-issuer schemes」（同一穩定幣在歐盟內外同時發行）的風險、準備金中「minimum amount of reserves to be held as deposits」要重檢、MiCA 範圍與定義要釐清、建議考慮納管加密資產借貸（含 CASP 幫客戶接 DeFi 借貸協議）、檢討申報框架。
- **容易寫錯**
  - 這是 EBA 對執委會諮詢的**回應**，不是規則；修不修由執委會提案、再走立法程序。
  - 限定詞照抄：多發行人方案的風險是「significant to very significant」；借貸是「encourages the European Commission to consider regulating」，不是「要求」。
  - 「39 EMTs have been issued under MiCA and 0 ARTs have been authorised」是**以 2026-09-01 為基準日**的快照（BRIEF 錯誤型態 4），要連基準日一起寫。
  - 兩個生效日不同：ART／EMT 規定（Title III、IV）2024-06-30，MiCA 全面適用 2024-12-30。
  - 開稿前**必須讀 41 頁 PDF**，新聞稿只是摘要；本輪沒讀，不能用本清單的摘要代替。
- **重疊檢查**：existing-packs 有 `crypto-news-eba-third-party-risk-20260918`（DORA 第三方風險指引，不同文件）。自動化清單的歐盟兩則是 ESMA 9/23「supervisory priority on digital innovation from 2027」與 ESAs 9/23 秋季風險更新（量子），**不是這份**。**無重疊。**

### 5. OFAC 制裁伊朗加密交易所 BitBank（補遺）

- **slug**：`crypto-news-ofac-iran-bitbank-sanctions-20260917`；**事件日**：2026-09-17（美東；台北時間可能已是 9/18，開稿時以財政部頁面為準並換算）。
- **一手來源**
  - 財政部新聞稿 sb0632「Operation Economic Outcast Disrupts Digital Asset Exchange Enabling the Iranian Regime」`https://home.treasury.gov/news/press-releases/sb0632`——200／77,674，正文讀到。
  - OFAC Recent Actions 2026-09-17「Iran-related Designations; Cuba Designations; Belarus-related Designations Removals」`https://ofac.treasury.gov/recent-actions/20260917`——200／49,581，SDN 條目讀到。
  - （旁證）聯邦公報 2026-19287（9/22 刊登），名單是 TIFF 圖檔，讀不到名字——上一輪就是卡在這裡。
- **為什麼重要**：依 E.O. 13902 以「operating in the digital asset sector of the Iranian economy」為由制裁一家交易所與其軟體開發商（Pishtaz Simorgh，Dot One 子公司）及三名 Zanjani 關係人；財政部稱 BitBank 在 6–7 月替 IRGC 移轉「hundreds of millions of dollars’ worth of Bitcoin」，並提醒非美國人也有次級制裁風險。對台灣讀者的意義在**合規**：交易所與銀行為什麼要做制裁名單篩查。
- **容易寫錯**
  - **同名不同家**：SDN 條目是「BITBANK (Arabic: بیتبانک) (a.k.a. BITBANK3), … Tehran, Iran; Website www.bitbank3.com; alt. Website www.bitbank.com」。不可與其他國家同名的合法業者混為一談，也不要自己推論那些網域屬於誰。
  - SDN 條目**沒有列任何數位貨幣地址**；「數億美元比特幣」是財政部的說法，要寫「財政部表示」。
  - **日期在財政部自己的頁面上不一致**：新聞稿本文與 OFAC 行動頁都是 September 17, 2026，但財政部新聞列表的 featured 區塊 `<time datetime=2026-09-16T20:00:00Z>` 顯示「September 16, 2026」。用 9/17，並在研究紀錄記下這個差異。公報刊登日 9/22 是另一個日期。
  - 「Operation Economic Outcast」「Economic D-Day（2026-08-24）」是官方行動名稱，照抄，不要意譯成政策結論。
- **重疊檢查**：existing-packs 無；自動化清單 grep `iran|treasury|ofac|fincen` 0 筆幣圈列。上一輪清單把這件（以公報通知的形式）判「不寫」，理由是「行動日在窗口外＋名單讀不到」——**名單讀不到的問題已由財政部新聞稿解決**，窗口外的問題由補遺規則處理。**無重疊。**

### 看過、判定不列的項目

| 日期 | 項目 | 為什麼不列 |
| --- | --- | --- |
| 9/24 | 聯準會「payment stablecoin」兩案徵詢 | 自動化清單同一事件 |
| 9/22、9/24 | CFTC 9302-26 mention markets、9303-26 加密資產 FAQ | 自動化清單同一事件 |
| 9/23 | ESMA 2027 數位創新監理重點；ESAs 秋季風險更新 | 自動化清單同一事件（見歐盟表） |
| 9/23 | SEC 委員 Peirce 在 SIFMA 數位資產會議演講 | 演講是個人意見（她自己寫 “My views are my own”），內容是 Innovation Exemption（已寫）與金融監控；她 9/25 宣布離任已在自動化清單 |
| 9/23 | FCA 演講「Building the next generation of market infrastructure」 | 演講，只預告「upcoming joint tokenisation roadmap」與將諮詢代幣化資產保管規則，沒有文件可寫 |
| 9/22 | 金管會「不會以 LINE 聯繫民眾」 | 一般二次詐騙，全文無虛擬資產 |
| 9/24 | JVCEA「取扱廃止銘柄のお知らせ」 | 個別幣種下架公告，`crypto.md` 明文排除 |
| 9/25 | OCC Corporate Decision 1394（Mission Lane Bank 設立） | 金融科技信用卡銀行，非幣圈 |
| 9/22 | FDIC 併購草案 Question 60（PPSI） | 上一輪已判改維護票，理由不變 |

---

## 讀不到／查不到

| 管道 | 症狀 | 處置 |
| --- | --- | --- |
| 新加坡 MAS `/news` | 200／853,817，整份是維護頁（第三輪同 bytes） | **讀不到**，不可寫「MAS 沒有發布」 |
| 香港 SFC e-Distribution | 200／3,908，前端渲染空殼 | **讀不到**；金管局列表讀得到，但它不是 SFC |
| FATF `/en/the-fatf/news.html` | **403**／5,556，Cloudflare「Just a moment...」（上一輪同網址 200） | 不繞過挑戰頁，**讀不到** |
| 中央銀行即時新聞澄清 `/tw/np-1164-1.html` | 200／**52** bytes | 空殼，**讀不到** |
| SEC 訴訟公告 LR-26643～26648 | RSS 讀到標題，內頁未抓 | 標題看不出幣圈，**未逐頁核對** |
| EBA MiCA 回應 PDF、金融廳別紙２ | 已下載（200／949,075、200／429,967） | 受時限所限**未抽文字**，開稿時要讀 |
| 自動化清單的 CoinDesk 連結 | 依規則不當來源，未抓 | 「同事件」判定是依標題與網址 slug，**沒有逐篇讀 CoinDesk 內文**；ESAs 量子那則是從嚴判同事件 |

**一個工具陷阱（給下一個代理）**：`curl --compressed -w '%{size_download}'` 回報的是**線上壓縮後的 bytes**，不是內容大小（SEC 新聞稿 RSS 回報 5,667，落地檔案 18,377）。本輪一開始這樣記錯，已改成記落地檔案大小；照抄別人的「bytes」前先確認是哪一種。

---

## 懷疑但未查證

1. **金融廳 9/15「2026事務年度金融行政方針」**可能有暗號資產／穩定幣段落（這次的論壇很可能就是方針的落實），未讀全文；補遺名額已用完。
2. **韓國金融委 9/23 那則會不會有英文版**：英文頁停在 Sep 16，秋夕後可能補上；目前只有韓文來源。
3. **SEC 訴訟公告 9/21–9/25 六則**有沒有涉及加密資產的詐欺案，只看了標題。
4. **FATF 10 月全會前的文件**（例如虛擬資產定向更新）——本輪 403，無法確認窗口內有沒有發布。
5. **新加坡 MAS、香港 SFC** 窗口內的穩定幣／VATP 動作：兩站都讀不到。
6. **行政院公報「虛擬資產」從 39 筆變 40 筆**，多出的那一筆不在前 10 筆，可能是較舊文件被補索引，未追。
7. **FCA 9/23 演講說的「upcoming joint tokenisation roadmap」與代幣化資產保管規則諮詢**：尚未發布，屬預告。
8. **BitBank 的 SDN「alt. Website www.bitbank.com」**：這個網域目前指向誰、跟其他同名業者有沒有關係，本輪沒查，文章也不應處理。
9. **聯準會 9/24 穩定幣兩案**若之後刊登聯邦公報，會變成一份新的公報文件；本輪依自動化清單排除，但公報刊登本身算不算「同事件」請協調者判斷。

---

## 統計

| 項目 | 數字 |
| --- | --- |
| 窗口 | 2026-09-21T16:00Z → 2026-09-26（台北 9/22 00:00 起） |
| 本輪 HTTP 請求（`fetch-log.tsv`） | 82 次（81 次 200、1 次 403；含 5 次因中文檔名寫檔失敗而改 ASCII 檔名重抓的行政院公報查詢），全部帶 `Mokaair-editorial/1.0` UA，未含任何個人資料 |
| 讀到內容的管道 | 美國 21、台灣 15、日本 6、歐盟 5、其他法域 10、協議 3 |
| 讀不到 | 4（MAS、SFC、FATF、央行澄清頁） |
| 候選 | **5**（窗口內 3、補遺 2） |
| 因自動化清單排除的一手事件 | 5（聯準會穩定幣、CFTC 9302／9303、ESMA 數位創新、ESAs 風險更新） |
