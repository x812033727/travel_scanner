# tech-news-snapdragon-8-elite-gen6-20260922 查核報告（第一輪）

- 查核者：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-26（台北），重抓時間 14:32Z（台北 22:32）
- 內容包：`apps/api/app/guides/content/tech-news-snapdragon-8-elite-gen6-20260922.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-snapdragon-8-elite-gen6-20260922.json`（已附 `factcheck` 物件）
- 垂直：科技、`display_order` 339、`news_date` 2026-09-22
- 規格：`FACTCHECK-48.md`、`agents/tech/FACTCHECK.md`、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二型

## 摘要

- 查了 121 條主張：CONFIRMED 94、CHANGED 18、NOT FOUND 2（一句刪除、一格改寫）、OUT OF SCOPE 7。
- 事實修改：內容包 12 個不同的事實問題（16 處文字，第 2 節第 1–12 點），研究紀錄 2 個（時區指示三處、Adreno Neural Fusion 的寫法），另加一條 `must_not_write`。
- 讀者優先的歸因精簡 3 處（兩段各從四個歸因語減為兩個，一段刪掉重複的「原文是」）。
- 自檢：`check_article.py` → `OK tech-news-snapdragon-8-elite-gen6-20260922 zh-TW paragraphs 2415`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（預期中，exit 1）。
- 結論：`needs_second_round`（事實修改超過十處；沒有動到骨幹論述）。

## 1. 來源重抓

指令：`curl -sSL --max-time 30 -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒，請求裡沒有任何人的姓名或 email。落地檔在 `_raw/tech-news-snapdragon-8-elite-gen6-20260922/round1/`。

| # | 來源 | HTTP | 落地 bytes | 型別 | 正文 | 與研究代理 `_raw` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 新聞稿 `.md` | 200 | 8,917 | text/markdown | 是（front matter、Highlights、兩節正文、品牌名單、夥伴 PDF 連結） | 逐位元組相同 |
| 2 | Partner Quote Sheet PDF | 200 | 86,268 | application/pdf | 是（2 頁，pypdf 抽出八段引言） | 逐位元組相同 |
| — | 新聞稿 HTML（非 sources，只驗證外殼） | 200 | 13,616 | text/html | 否：可見文字 181 字元（標題＋「enable JavaScript」）；`<link id="geo-artifacts-markdown-link" rel="alternate" type="text/markdown">` 仍指向來源 1 | — |

- 研究紀錄 2 條 sources 與 25 條 `verified_facts` 的 `verbatim_quote`：**27/27 命中**（.md 精確連續子字串；PDF 為空白正規化、還原 pypdf 拆字 “T echnologies”／“T ogether” 後的連續子字串）。所有 `url` 都在 `sources[]` 裡。
- 詞界比對（兩份來源）：TSMC、foundry、Samsung、Taiwan、Hawaii、HST、PDT、PST、a.m.、p.m.、GHz、percent 皆 0 次；.md 的 9 個 `%` 都是網址 `%20`；fastest 只在 front matter title 與 H1（2 次）；**規格數字只有一個：`2nm`（1 次，在 8 Elite Gen 6 那一段）**。
- `checked_on` 2026-09-26：內容包兩條 source、研究紀錄、第二段、表格 caption、圖解 caption 一致，且就是我重抓的日期，不動。

## 2. 改掉的地方（before → after，來源）

來源簡寫：MD＝`https://www.qualcomm.com/news/releases/2026/09/snapdragon-leads-the-agentic-ai-age-with-two-of-the-world-s-fast.md`；PDF＝`https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/images/company/news-media/media-center/press-kits/snapdragon-summit-2026-press-kit/day-1/documents/PartnerQuoteSheet.pdf`。

1. **description**：「以及代工廠、規格數字、上市日與台灣資訊為何都還沒公布」→「以及新聞稿沒有寫的代工廠、時脈等規格數字、上市日與台灣資訊」（MD）。文章沒有、也無法說明「為何」；「都還沒公布」超出「這份新聞稿沒寫」——研究代理自己就讀到高通另有列出時脈與百分比的產品簡介 PDF（已排除），所以「規格還沒公布」是錯的否定句。長度 180→183。
2. **第一段（NOT FOUND，刪除）**：「這則新聞稿也在 Snapdragon Summit 期間發布。」MD 只有 `tags: ["Snapdragon Summit", …]`、夥伴 PDF 連結與 Event Hub 連結，沒有寫 Summit 的活動期間；研究紀錄 `must_not_write` 明寫「也不寫 Summit 的活動期間」。第二段與正文仍交代夥伴引言出自 Snapdragon Summit 的資料袋。
3. **summary 第 2 條**：「自研的 Oryon CPU、Adreno GPU 與 Hexagon NPU」→「自研的 Oryon CPU，以及 Adreno GPU 與 Hexagon NPU」（MD：`custom-built Qualcomm Oryon™ CPU, rearchitected Qualcomm® Adreno™ GPU, and the advanced Qualcomm® Hexagon™ NPU`——custom-built 只修飾 Oryon）。
4. **「沒有任何規格數字」（四處：summary 第 4 條、第四節第一段、FAQ 第 3 題、callout）**：新聞稿印了 `2nm process node`，文章自己也寫了四次 2 奈米。改成「2 奈米製程節點以外的規格數字」／「除了 2 奈米製程節點，新聞稿沒有給出任何規格數字」／「新聞稿除了 2 奈米製程節點，只有定性說法，沒有其他規格數字」（MD）。**指派訊息說「來源沒有任何規格數字」，這點與來源不符，以來源為準。**
5. **多旗艦策略那段**：「目的是把最新 AI 功能帶到更廣的高階裝置；同一段引言接著說，設計兩款平台是為了給手機廠（OEM）更多選擇。……——這同樣是高通的說法。」→「讓高通能把最新 AI 功能帶到更廣的高階裝置，而設計兩款平台讓手機廠（OEM）有更多選擇。……」（MD：`our multi-flagship strategy allows us to … while bringing our latest AI innovations to a broader range of premium devices. By designing two innovative platforms, we're giving OEMs greater choice`）。原句把「讓我們能」「藉此給予」寫成目的；同時把該段歸因語從四個減到兩個（「在新聞稿引言裡稱」「新聞稿也說」）。
6. **Adreno Neural Fusion**：「用 AI 產生遊戲畫面，高通稱能帶來……」→「用 AI 提供智慧化的遊戲圖形（intelligent graphics），帶來……」（MD：`using AI to deliver intelligent graphics`）。「產生遊戲畫面」會被譯成 frame generation，來源沒寫。段首「高通稱」與段尾「這三點都是高通的說法」仍在，歸因不減。研究紀錄 `verified_facts` 同句一併更正（草稿是照紀錄抄的）。
7. **表格「製程與架構」列的 Extreme 一格（NOT FOUND，改寫）**：「2 奈米製程節點；Oryon CPU、Adreno GPU、Hexagon NPU（新聞稿未單獨列製程）」→「新聞稿未列（8 Elite Gen 6 那段寫的是「同樣的」2 奈米製程節點）」。MD 的 Extreme 一節沒有製程、Oryon 或 Hexagon（Adreno 只以 Adreno Neural Fusion 出現）；`the same` 只修飾 `2nm process node`。改法就是研究紀錄 editorial_brief 建議的寫法，也對上表格 caption 的「新聞稿未列」。
8. **Xiaomi（夥伴段與 FAQ 第 4 題）**：「是唯一點名兩款都會用的，說即將推出的高階裝置會同時採用兩款平台」→「則點名兩款都會用，說會在即將推出的高階裝置上採用這兩款平台」（PDF：`By leveraging both … across our upcoming premium devices`）。「唯一」是 BRIEF 第 2 型禁用詞、讀者容易讀成「只有小米會兩款都用」；「同時採用」會被讀成每支都用兩顆，原文是 across devices。
9. **第三節最後一段**：「能確認的品牌與機型名稱僅止於這裡列出的部分」→「……這一篇列出的部分」。RedMagic 12Pro+ 不在這一節，只在第五節出現，「這裡」會讓那句話變錯（PDF）。
10. **第五節第二段**：「新聞稿裡「即將推出」的機型」→「夥伴引言裡「即將推出」的機型」。MD 沒有任何機型名稱；iQOO 16、iQOO Pad Ultra、RedMagic 12Pro+ 只在 PDF（研究紀錄 not_said 第 4 條）。
11. **FAQ 第 2 題**：「新聞稿與夥伴引言文件都沒有提到任何晶圓代工廠的名字，只寫兩款平台建構在 2 奈米製程節點上」→「……名字；新聞稿只寫 8 Elite Gen 6 建構在與 Extreme 版「同樣的」2 奈米製程節點上」。MD 沒有直接寫「兩款平台建構在 2 奈米」，PDF 完全沒有 2 奈米。
12. **FAQ 第 3 題**：「8 Elite Gen 6 則建構在「同樣的」2 奈米製程節點與 Oryon CPU、Adreno GPU、Hexagon NPU 上」→「……「同樣的」2 奈米製程節點上，採用 Oryon CPU、Adreno GPU 與 Hexagon NPU」。原句讓「同樣的」也罩住 CPU／GPU／NPU（MD）。
13. **研究紀錄（對 DELTA-4-8 第 4 條的更正）**：`event_date_basis`、`editorial_brief`、`must_not_write` 三處仍要求正文寫「美國夏威夷時間 9 月 22 日」，與協調者裁定相反（內容包本來就沒有這幾個字，圖解 caption 已由撰稿移除）。三處改成「照新聞稿印的「9 月 22 日」寫、可帶電頭茂宜島（Maui）、不寫任何時區」，免得第二輪照紀錄改回去。`must_not_write` 另加一條：Oryon／Adreno／Hexagon 與 2 奈米不寫成 Extreme 版另外列出的規格。

讀者優先（協調者核可的歸因精簡，不算事實修改）：Extreme 那段「高通稱／新聞稿列出／高通稱／這三點都是高通的說法」→「高通稱……並列出……／這三點都是高通的說法」；8 Elite Gen 6 那段刪去「原文是「許多相同的」，」（同句括號已有 many of the same）；多旗艦那段見第 5 點。

## 3. 指派訊息點名要先查的事

| 項目 | 結果 |
| --- | --- |
| 日期「9 月 22 日」、電頭茂宜島、沒有時區、沒有「夏威夷時間」 | 內容包 CONFIRMED（「夏威夷」0 次，第一段與 callout 寫「沒有印出時刻或時區」）。研究紀錄三處相反指示已改（第 2 節第 13 點）；紀錄裡剩下的 2 次「夏威夷」只在 `factcheck.changes` 的 before 欄，是修改紀錄。 |
| 圖解 caption＝紀錄 `diagram.caption` | CONFIRMED，逐字相同（check_article 也檢查）。 |
| 沒有規格數字、時脈、百分比、代工廠 | 時脈、百分比、代工廠：CONFIRMED，全文 0。規格數字：**來源有一個 2nm**，改為「2 奈米製程節點以外」（第 4 點）。FAQ 第 2 題的問句寫了「台積電」、答句說新聞稿沒有任何代工廠——這是研究紀錄 editorial_brief 建議的題目，未改，列為待決。 |
| 「Two of the World's Fastest」 | CONFIRMED：寫成「全球最快的行動 SoC 之二」並附英文原文，標題裡的高通說法、正文無測試條件（MD 的 fastest 只在標題）。 |
| 品牌：including 不是全名單；配對只來自各品牌自己的引言 | CONFIRMED（名單依原文順序九個；表格與正文的配對與 PDF 一致：HONOR、Motorola、RedMagic、vivo→Extreme；Xiaomi→兩款；OPPO 未點名）。「唯一」與「同時採用」已改（第 8 點）。 |
| RedMagic 12Pro+、iQOO 16／iQOO Pad Ultra 只照引言寫 | CONFIRMED：12Pro+ 只寫「RedMagic 提到的」，沒寫搭載哪一款；iQOO 兩款寫「首批之一」（among the first）、沒補裝置類型。出處從「新聞稿裡」改為「夥伴引言裡」（第 10 點）。 |
| Motorola 的 for the first time | CONFIRMED：「要把 Extreme Gen 6「第一次」（for the first time）帶進自己的旗艦產品線」，保留歧義、沒延伸。 |
| 8 Elite Gen 6「許多相同的」，沒有自創差異 | CONFIRMED；表格 Extreme 一格被誤填的 CPU／GPU／NPU 已拿掉（第 7 點），FAQ 第 3 題的「同樣的」範圍已收窄（第 12 點）。 |
| 沒有上市日、售價、台灣資訊，要直接說 | CONFIRMED：第一段、summary、第四節、FAQ 第 1 題、callout 都直接說，並限定「查核到 2026 年 9 月 26 日」。 |
| 篇幅相稱、不灌水、不加來源 | 段落字數 2,445→2,415；`sources[]` 仍兩條，沒有新增。 |

## 4. 逐條主張表

判定：C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND（改寫或刪除）、OS＝OUT OF SCOPE（文字風格）。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | 高通發表兩款 Snapdragon 旗艦手機平台 | C | MD `two new flagship mobile platforms` |
| 2 | title | 「Extreme 版與 8 Elite Gen 6 差在哪」 | OS | 文章答的是定性差別 |
| 3 | description | 9/22 同時發表兩款 | C | MD 頁首、front matter |
| 4 | description | 電頭茂宜島 | C | MD `location: "MAUI"` |
| 5 | description | 夥伴引言點名品牌 | C | PDF |
| 6 | description | 代工廠等「為何都還沒公布」 | CH | 第 2 節第 1 點 |
| 7 | description | 句尾「（2026 年 9 月查證）」、無選題計數 | C | DELTA-4-7 第 14 條 |
| 8 | meta | slug 尾碼＝news_date＝第一段 2026-09-22；order 339；topics | C | DELTA-4-8 第 4 條；check_article |
| 9 | 第一段 | 高通（Qualcomm Technologies）9/22 發布新聞稿 | C | MD `Qualcomm Technologies, Inc. unveiled today` |
| 10 | 第一段 | 兩款新的高階行動平台與正式名稱 | C | MD |
| 11 | 第一段 | 新聞稿在 Snapdragon Summit 期間發布 | NF→刪 | 第 2 節第 2 點 |
| 12 | 第一段 | 電頭茂宜島（Maui） | C | MD |
| 13 | 第一段 | 沒有印出時刻或時區 | C | 詞界比對 0 次 |
| 14 | 第一段 | 查核到 9/26 沒看到台灣上市消息 | C | 兩份來源 Taiwan 0 次 |
| 15 | 第二段 | 9/26 查核 | C | 我今天重抓，與紀錄一致 |
| 16 | 第二段 | 讀新聞稿全文與 Summit 資料袋裡的夥伴引言文件 | C | MD、PDF 路徑 `press-kits/snapdragon-summit-2026-press-kit/day-1` |
| 17 | 第二段 | 沒做測試、不提供購買建議 | OS | 編輯聲明 |
| 18 | summary 1 | 日期、兩款、電頭 | C | MD |
| 19 | summary 2 | 高通稱「多旗艦策略」 | C | MD 引言 |
| 20 | summary 2 | 8 Elite Gen 6 與 Extreme 版同樣的 2 奈米節點 | C | MD `the same advanced 2nm process node` |
| 21 | summary 2 | 「自研的」罩住三個元件 | CH | 第 2 節第 3 點 |
| 22 | summary 2 | 許多相同的功能帶到更多頂級手機 | C | MD `many of the same … top-tier smartphones` |
| 23 | summary 3 | including 名單與順序 | C | MD Highlights 第 3 點 |
| 24 | summary 3 | 沒有配對、沒有日期 | C | MD |
| 25 | summary 4 | 沒有代工廠 | C | 詞界 0 |
| 26 | summary 4 | 沒有「任何」規格數字 | CH | 第 2 節第 4 點 |
| 27 | summary 4 | 沒有上市日、售價、台灣 | C | MD、PDF |
| 28 | summary 4 | 沒寫少了哪些功能 | C | MD |
| 29 | 第一節 | 小標 | C | MD |
| 30 | 第一節 | 標題稱「全球最快的行動 SoC 之二」＋英文原文 | C | MD title／H1 |
| 31 | 第一節 | 正文沒有測試條件或比較對象 | C | fastest 只在標題 |
| 32 | 第一節 | 行動手機事業資深副總裁暨總經理 | C | MD `Senior Vice President and General Manager of Mobile Handsets` |
| 33 | 第一節 | 多旗艦策略（multi-flagship strategy） | C | MD |
| 34 | 第一節 | 「目的是」把最新 AI 功能帶到更廣的高階裝置 | CH | 第 2 節第 5 點 |
| 35 | 第一節 | 設計兩款「是為了」給 OEM 更多選擇 | CH | 第 2 節第 5 點 |
| 36 | 第一節 | 兩款結合效能與裝置端智慧、AI／遊戲／相機／連網四方面進步 | C | MD Highlights 第 2 點 |
| 37 | 第二節 | 小標 | C | — |
| 38 | 第二節 | 高通稱 Extreme 是自己最強大的行動平台 | C | MD `most powerful mobile platform` |
| 39 | 第二節 | 用於最先進的 Android 手機 | C | MD |
| 40 | 第二節 | 列出三項新功能 | C | MD `New features:` 三點 |
| 41 | 第二節 | AI 代理：更快、更個人化、更可靠、隨一天作息調整 | C | MD |
| 42 | 第二節 | Adreno Neural Fusion「用 AI 產生遊戲畫面」 | CH | 第 2 節第 6 點 |
| 43 | 第二節 | 更沉浸、更豐富的畫面、更長的遊戲時間 | C | MD |
| 44 | 第二節 | AI 相機：APV、Intelligent Pixel Control | C | MD |
| 45 | 第二節 | 沒附續航、幀率或其他數字 | C | MD |
| 46 | 第二節 | 8 Elite Gen 6 建構在「同樣的」先進 2 奈米節點 | C | MD |
| 47 | 第二節 | 自研 Oryon CPU、重新架構的 Adreno GPU、Hexagon NPU | C | MD |
| 48 | 第二節 | 沒有另外為 Extreme 單獨寫製程 | C | MD |
| 49 | 第二節 | 沒寫哪一家晶圓廠 | C | 詞界 0 |
| 50 | 第二節 | 差別只給一句：許多相同的 AI、遊戲、影像、連網功能 | C | MD |
| 51 | 第二節 | 沒列少了哪些功能 | C | MD |
| 52 | 表格 | 表頭三欄 | C | — |
| 53 | 表格 | 定位／Extreme | C | MD |
| 54 | 表格 | 定位／Gen 6 | C | MD |
| 55 | 表格 | 製程與架構／Extreme：2 奈米＋Oryon／Adreno／Hexagon | NF→改寫 | 第 2 節第 7 點 |
| 56 | 表格 | 製程與架構／Gen 6 | C | MD |
| 57 | 表格 | 新功能／Extreme | C | MD |
| 58 | 表格 | 新功能／Gen 6：未逐項列出 | C | MD |
| 59 | 表格 | 夥伴點名／Extreme：HONOR、Motorola、RedMagic、vivo、Xiaomi | C | PDF |
| 60 | 表格 | 夥伴點名／Gen 6：Xiaomi | C | PDF（非 Extreme 的 8 Elite Gen 6 只在 Xiaomi 段出現） |
| 61 | 表格 caption | 日期、查核日、「新聞稿未列」 | C | 改寫後 Extreme 一格正好以「新聞稿未列」起頭 |
| 62 | 第三節 | 裝置「將」在全球手機品牌旗艦機首度登場 | C | MD `will debut in flagship smartphones from leading global OEMs` |
| 63 | 第三節 | including 名單與順序 | C | MD |
| 64 | 第三節 | 兩款合寫、沒配對、沒日期、未來式 will debut | C | MD |
| 65 | 第三節 | 夥伴說法放在 Summit 的夥伴引言文件 | C | MD `To hear from key industry players, visit Snapdragon Summit Partner Quote Sheet` |
| 66 | 第三節 | HONOR 產品總裁點名 Extreme | C | PDF `President of Products at HONOR` |
| 67 | 第三節 | RedMagic 點名 Extreme | C | PDF |
| 68 | 第三節 | Motorola 全球產品行銷主管、for the first time | C | PDF，歧義保留 |
| 69 | 第三節 | vivo 資深副總裁暨技術長：iQOO 16、iQOO Pad Ultra「首批之一」 | C | PDF `among the first devices` |
| 70 | 第三節 | Xiaomi「唯一」點名兩款 | CH | 第 2 節第 8 點 |
| 71 | 第三節 | Xiaomi 高階裝置「同時採用」兩款 | CH | 第 2 節第 8 點 |
| 72 | 第三節 | OPPO 沒點名任一款 | C | PDF |
| 73 | 第三節 | 都是即將推出、沒有上市日 | C | PDF `upcoming` ×3、無日期 |
| 74 | 第三節 | 機型「僅止於這裡列出」 | CH | 第 2 節第 9 點 |
| 75 | 第三節 | 之後各品牌可能再公布新機 | OS | 保留的活資料提醒 |
| 76 | 圖解 | caption 與紀錄逐字相同 | C | check_article |
| 77 | 圖解 | alt 四格內容 | C | 與紀錄 nodes 一致 |
| 78 | 第四節 | 沒有任何晶圓代工廠名字 | C | 詞界 0（兩份） |
| 79 | 第四節 | 沒有時脈、核心數、快取、記憶體或「其他」規格數字 | CH | 第 2 節第 4 點 |
| 80 | 第四節 | 除標題外沒有跑分或比較對象 | C | MD |
| 81 | 第四節 | 沒有上市日、售價、地區與市場資訊（含台灣） | C | MD、PDF |
| 82 | 第四節 | 兩份來源沒提台灣上市時間或販售機型 | C | Taiwan 0 |
| 83 | 第四節 | 少了哪些功能沒寫 | C | MD |
| 84 | 第五節 | 標明是編輯設計的例子 | C | DELTA／brief |
| 85 | 第五節 | 兩款名稱只差「Extreme」 | C | MD |
| 86 | 第五節 | 規格數字、上市日、售價新聞稿沒寫（指手機） | C | MD |
| 87 | 第五節 | 可留意高通新聞室與 Snapdragon Summit 活動頁 | C | MD 指向 Event Hub |
| 88 | 第五節 | 「新聞稿裡」即將推出的機型 | CH | 第 2 節第 10 點 |
| 89 | 第五節 | vivo 的 iQOO 16、iQOO Pad Ultra；RedMagic 的 RedMagic 12Pro+ | C | PDF（12Pro+ 原文無空格，照抄） |
| 90 | 第五節 | 台灣販售以品牌公布為準 | OS | 建議語 |
| 91 | FAQ 1 | 沒提台灣、沒有上市日或售價、查核日未查到 | C | MD、PDF |
| 92 | FAQ 2 | 問句提「台積電」 | OS | 研究紀錄 editorial_brief 建議的題目；待決 |
| 93 | FAQ 2 | 兩份文件都沒有代工廠名字 | C | 詞界 0 |
| 94 | FAQ 2 | 「只寫兩款平台建構在 2 奈米」（主詞含夥伴文件） | CH | 第 2 節第 11 點 |
| 95 | FAQ 3 | 最強大的行動平台＋三項新功能 | C | MD |
| 96 | FAQ 3 | 「同樣的」罩住 CPU／GPU／NPU | CH | 第 2 節第 12 點 |
| 97 | FAQ 3 | 沒有「任何」規格數字 | CH | 第 2 節第 4 點 |
| 98 | FAQ 3 | 沒寫少了哪些功能 | C | MD |
| 99 | FAQ 4 | including 名單、不是完整名單、沒配對 | C | MD；研究紀錄（including＝不是全名單） |
| 100 | FAQ 4 | HONOR、Motorola、RedMagic、vivo 點名 Extreme | C | PDF |
| 101 | FAQ 4 | Xiaomi「同時採用」 | CH | 第 2 節第 8 點 |
| 102 | FAQ 4 | OPPO 沒點名 | C | PDF |
| 103 | FAQ 5 | 標題說法、正文無測試或比較 | C | MD |
| 104 | FAQ 5 | 「宣傳用語」 | OS | 定性描述，已歸因 |
| 105 | callout | 9/22 新聞稿、電頭茂宜島、無時刻時區、查核日 9/26 | C | MD |
| 106 | callout | 「只有定性說法，沒有規格數字」 | CH | 第 2 節第 4 點 |
| 107 | callout | 沒有代工廠、上市日、售價、台灣 | C | MD、PDF |
| 108 | callout | 名單以「包括」起頭、不是完整名單 | C | MD |
| 109 | callout | 夥伴引言裡的機型都沒有日期 | C | PDF |
| 110 | callout | 首句「這兩款平台是……新聞稿」、以品牌資料為準的建議 | OS | 主詞不通，文字問題 |
| 111 | 連結 1 | text＝`tech-news-2026-index` 的 zh-TW title，逐字；五語齊 | C | 內容包比對 |
| 112 | 連結 2 | text＝`tech-news-nvidia-mediatek-20260831` 的 zh-TW title，逐字；五語齊 | C | 內容包比對 |
| 113 | sources 1 | title、`.md` 網址、checked_on | C | 200／8,917 B |
| 114 | sources 2 | title、PDF 網址、checked_on | C | 200／86,268 B |
| 115 | 紀錄 | hero_label「同一代旗艦分兩級」 | C | 兩款都是 Gen 6、「not one, but two new flagship mobile platforms」 |
| 116 | 紀錄 | diagram title | C | — |
| 117 | 紀錄 | 節點「Extreme 版／高通稱最強的行動平台」 | C | MD |
| 118 | 紀錄 | 節點「8 Elite Gen 6／同為 2 奈米、許多功能相同」 | C | MD `same advanced 2nm`、`many of the same` |
| 119 | 紀錄 | 節點「首發品牌／「包括」起頭，不是全名單」、「沒寫的事／代工廠、規格、上市日、台灣」 | C | MD（圖上數字 2 在正文） |
| 120 | 紀錄 | event_date_basis／editorial_brief／must_not_write 的「夏威夷時間」指示 | CH | 第 2 節第 13 點 |
| 121 | 紀錄 | verified_facts 的「用 AI 產生遊戲畫面」 | CH | 第 2 節第 6 點 |

計數：C 94、CH 18、NF 2、OS 7，共 121（CH 18 條對應第 2 節的 13 個事實問題：同一事實出現在多處時逐處計）。

## 5. 讀者優先檢查

- 「本文」0 次；第二段用「這篇文章的資料在……查核」（DELTA-4-7 第 14 條的寫法）。
- 第一段只有一個歸因語（「新聞稿電頭寫的地點是」）。刪掉 Summit 那句後仍只有一個。
- 正文段落的歸因語：多旗艦那段、Extreme 那段各由四個減為兩個；8 Elite Gen 6 那段刪掉重複的「原文是」。第三節夥伴引言那段是五家公司各自的說法，逐一歸因是 tech.md 的規定，未壓縮（待決第 1 條）。
- description 句尾只有「（2026 年 9 月查證）」；title、description、summary 沒有選題計數。
- 沒有購買建議、推薦式比價；廠商宣稱（最強大、最快之二、三項新功能、夥伴引言）都有歸因；「將首度登場」「即將推出」「首批之一」的未來式都在。

## 6. 留給協調者

1. 第三節夥伴引言段有五個「點名／說」。每一個都是不同公司的宣稱，改成直述會變成本站替廠商背書；建議維持。
2. FAQ 第 2 題問句含「台積電」（研究紀錄建議的題目，答句是「新聞稿沒有寫」）。若裁定「全文不出現任何代工廠名稱」，要換問法，例如「是哪一家晶圓廠做的？」。
3. callout 第一句「這兩款平台是高通 2026 年 9 月 22 日發布的新聞稿」主詞不通（平台≠新聞稿），屬文字問題，第一輪沒改；翻譯前可順手改成「這兩款平台出自……的新聞稿」。
4. 指派訊息說兩份來源都沒有規格數字，實際上新聞稿印了 `2nm`（1 次）。以來源為準，文章保留 2 奈米，並在四處「沒有規格數字」的句子加上「2 奈米製程節點以外」。

## 7. 自檢輸出（原樣）

```
OK tech-news-snapdragon-8-elite-gen6-20260922 zh-TW paragraphs 2415
exit=0
```

```
tech-news-snapdragon-8-elite-gen6-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-snapdragon-8-elite-gen6-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-snapdragon-8-elite-gen6-20260922/diagram-1.svg
1 entries checked
exit=1
```

輔助檔：`_tools/tech-news-snapdragon-8-elite-gen6-20260922/`（`edit_round1.py`、`edit_round1b.py`、`edit_round1c.py`、`quotes.py`、`inspect.py`、`backup/` 裡的修改前檔案、`pack.diff`、`record.diff`、各次輸出）。
