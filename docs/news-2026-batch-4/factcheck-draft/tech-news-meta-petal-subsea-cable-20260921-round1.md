# tech-news-meta-petal-subsea-cable-20260921 第一輪查核報告

- 查核者：獨立第一輪查核代理（未參與撰稿）
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-meta-petal-subsea-cable-20260921.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-meta-petal-subsea-cable-20260921.json`
- 垂直／順序：科技，`display_order` 324；事件日 2026-09-21
- 結論：**需要第二輪**（DELTA-4-7 第 12 條要求，且本輪改了 17 處，其中 12 處是事實／準確度）

## 1. 來源重抓結果（2026-09-23 台北 01:28 起，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒，請求未帶任何人的姓名或 email）

| # | 網址 | HTTP | bytes | 是否讀到正文 | 與研究紀錄比對 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/` | 200 | 100,217 | 是（POSTED ON SEPTEMBER 21, 2026 到文末星號註腳全讀到） | bytes 完全相同；去標籤後與 `_raw/` 的 `petal.txt` **逐位元組相同**（`diff` 無差異） |
| 2 | `https://sumitomoelectric.com/press/2026/09/prs040` | 200 | 150,242 | 是（自印 22 September 2026，正文與三段具名引言全讀到） | bytes 完全相同；去標籤後與 `_raw/` 的 `sei-petal.txt` **逐位元組相同** |
| — | `https://www.nec.com/en/press/` | 403 | 380 | 否 | 與研究紀錄一致，NEC 自家頁今天仍讀不到 |
| — | `https://www.nec.com/en/global/prod/nw/submarine/news/` | 403 | 420 | 否 | 同上 |

研究紀錄 `sources[]` 與 `verified_facts[]` 合計 **41 條 `verbatim_quote`，今天全部仍是抓到的 body 的連續子字串**（`_tools/.../verify_quotes_petal.py`，0 problems），`verified_facts` 的 `url` 也都在 `sources[]` 裡。內容包內嵌的每一段英文引文（時間戳記、兩句時程、類比與註腳、標題）也逐字比對過，全部通過。

NEC 仍 403，所以 NEC 的敘述只能出自 Meta 貼文裡那段具名引言與住友電工的聯合稿；文章沒有越過這條線。**補充一點給站主與第二輪**：研究紀錄 `unverified_or_excluded` 寫「NEC 的說法只能引住友電工聯合稿」，但 Meta 的貼文本身也有一段掛 NEC 名義的具名引言（Eduardo Mateo, Chief Strategy Officer, Submarine Network Division），要用的話那也是一手來源。

## 2. 主張逐條核對（132 條）

判定：**確認**＝來源原文撐得住；**已改**＝本輪改掉；**查無**＝來源沒有寫、留給站主；**不適用**＝規格說不查。

### 標題與描述

| # | 主張 | 判定 |
| --- | --- | --- |
| 1 | 標題「Meta 宣布 Petal 跨洋海纜：容量 1 Pbps，預計 2029 年啟用」（40 字，≤60） | 確認 |
| 2 | 事件日 2026-09-21、Meta 工程部落格 | 確認 |
| 3 | 連接法國與美國 | 確認 |
| 4 | 全長約 7,000 公里 | 確認 |
| 5 | 「Meta 表示設計容量達 1 Pbps」 | 確認（見第 5 節開放問題） |
| 6 | 「是現有同距離海纜的兩倍」 | **已改**（掉了 most advanced 這個限定） |
| 7 | 預計 2029 年啟用 | 確認 |
| 8 | 從 8 對光纖到 2 芯光纖的容量演進 | 確認 |
| 9 | NEC、住友電工與 Orange 的分工 | 確認 |
| 10 | 兩份官方文件都沒有提到台灣或造價 | 確認 |
| 11 | 句尾只帶「（2026 年 9 月查證）」，沒有查證流水帳、沒有清點數字 | 確認 |
| 12 | `hero.alt` | 不適用（主圖由協調者繪製，規格明定不查不改） |

### 摘要

| # | 主張 | 判定 |
| --- | --- | --- |
| 13 | S1 的日期／路由／長度／容量／時程 | 確認 |
| 14 | S2「改用 2 芯光纖搭配 24 對的系統，等效 48 對」（保留「等效」） | 確認 |
| 15 | S2「容量是**前一條海纜** Anjana 的兩倍」 | **已改**（來源沒說 Anjana 是前一條） |
| 16 | S2 Anjana 24 對、0.5 Pbps | 確認 |
| 17 | S3 Meta 出資並營運 | 確認（聯合稿原文） |
| 18 | S3 NEC 負責 2 芯系統的整體設計與建造 | 確認 |
| 19 | S3 住友電工提供 2 芯光纖 | 確認 |
| 20 | S3 Orange 協助法國端登陸 | 確認（Meta 貼文） |
| 21 | S4 沒有造價、登陸城市、啟用月份 | 確認 |
| 22 | S4 到查核日還沒有開始服務 | 確認 |

### 第一、二段

| # | 主張 | 判定 |
| --- | --- | --- |
| 23 | 2026 年 9 月 21 日 Meta 在工程部落格宣布 | 確認 |
| 24 | 串接法國與美國、約 7,000 公里 | 確認 |
| 25 | 1 Pbps 等於每秒 1,000 Tbps | 確認（Meta 貼文與聯合稿註腳都寫） |
| 26 | 是現有同距離最先進海纜的兩倍 | 確認 |
| 27 | 預計 2029 年啟用 | 確認 |
| 28 | Petal 不經過台灣 | 確認（跨大西洋、法國—美國；研究紀錄 `editorial_brief` 同判） |
| 29 | 沒有寫動工或商轉的確切時間 | 確認 |
| 30 | 查核日 2026-09-23 與研究紀錄 `checked_on` 一致 | 確認 |
| 31 | 讀的是 Meta 貼文與住友電工 9/22 聯合新聞稿 | 確認 |
| 32 | 聯合稿由三家公司具名 | 確認（頁面掛 Meta Platforms／NEC／Sumitomo Electric 三個名） |
| 33 | 「這一篇不重複那些數字，也不把 Petal 拿來跟台灣的海纜比較」 | **已改**（編輯流程寫進正文，DELTA-4-7 第 14 條） |

### 第一節「9 月 21 日的宣布」

| # | 主張 | 判定 |
| --- | --- | --- |
| 34 | 公告放在 Connectivity 分類 | 確認 |
| 35 | 頁面自印「POSTED ON SEPTEMBER 21, 2026」 | 確認（逐字） |
| 36 | 「標題是《Inside Petal》」 | **已改**（那只是標題前半） |
| 37 | Meta 寫 Petal 會是第一條在跨洋距離做到 petabit 等級容量的海纜 | 確認 |
| 38 | 「正文一律寫成 Meta 表示」 | **已改**（查證紀律＋「正文」自我指涉） |
| 39 | Petal 由 Meta 出資 | 確認 |
| 40 | 合作對象是 NEC 與住友電工 | 確認 |
| 41 | 法國端登陸由 Orange 協助 | 確認 |
| 42 | 「**法國電信集團** Orange」 | 查無（見第 5 節；未改） |
| 43 | Meta 寫 Expected、住友電工寫 scheduled，都指 2029 | 確認 |
| 44 | 全長約 7,000 公里 | 確認 |
| 45 | 兩份文件沒有寫登陸城市 | 確認 |
| 46 | Meta 只提到法國大西洋岸 | 確認 |
| 47 | 美國端連州名都沒有 | 確認（全文只有 the United States） |
| 48 | 沒有寫造價或投資金額 | 確認 |
| 49 | 「這兩頁都沒有出現台灣或亞太航線的字樣」 | **已改**（Meta 那一頁出現 Asia-Pacific 兩次） |

### 第二節「容量是怎麼長出來的」

| # | 主張 | 判定 |
| --- | --- | --- |
| 50 | 小標「從一對光纖到二十四對」 | **已改**（正文沒有「一對光纖」，來源的起點是 8 對） |
| 51 | 1980 年代 EDFA 之後有幾次轉折 | 確認 |
| 52 | 2010 年代同調光傳輸與非色散補償設計 | 確認 |
| 53 | 單纖容量十年內成長十倍以上 | 確認（10x and more） |
| 54 | 直到逼近 Shannon Limit 才慢下來 | 確認 |
| 55 | 「空間**分工**多工（SDM）」 | **已改**（spatial division multiplexing ＝空間分割多工） |
| 56 | SDM 是在一條海纜裡增加光纖 | 確認 |
| 57 | Marea 8 對 | 確認 |
| 58 | Amitié 16 對 | 確認 |
| 59 | Anjana 24 對、首條 0.5 Pbps 跨大西洋系統 | 確認 |
| 60 | Petal 2 芯搭配 24 對、等效 48 對、1 Pbps | 確認 |
| 61 | 是 Anjana 的兩倍 | 確認 |
| 62 | 表格 Marea 8 對／官方未列出容量 | 確認（頁面確實沒印 Marea 容量） |
| 63 | 表格 Marea 為 Meta 首條跨大西洋投資 | 確認（圖說原文） |
| 64 | 表格 Amitié 16 對／官方未列出容量 | 確認 |
| 65 | 表格 Anjana 24 對、0.5 Pbps、首條達此容量 | 確認 |
| 66 | 表格 Petal 2 芯等效 48 對、1 Pbps、預計 2029 | 確認 |
| 67 | 表格 caption 的出處與查核日（79 字，≤200） | 確認 |

### 第三節「Petal 為什麼改押 2 芯光纖」

| # | 主張 | 判定 |
| --- | --- | --- |
| 68 | Meta 列出三條能再把容量翻倍的路 | 確認（Three innovations could double capacity again） |
| 69 | 路線一：增加到 48 對 | 確認 |
| 70 | 路線二：L 波段，PLCN 做到 24 對 C+L | 確認 |
| 71 | 路線三：2 芯光纖 | 確認 |
| 72 | 「理由是不必讓整個海纜生態系重新驗證就能把容量做上去」 | **已改**（來源寫的是性質，不是選擇理由；而且重新驗證是更高電壓才需要） |
| 73 | 額定最高 18 kV | 確認 |
| 74 | 兩個難題：外徑不變下壓低衰減、壓低串音 | 確認 |
| 75 | 「做法是控制折射率差…」被寫成兩個難題的共同解 | **已改**（那只解串音；衰減的解是預型體用超高純度合成石英） |
| 76 | 幾乎量不到的串音 | 確認 |
| 77 | 單體中繼器內含 96 個放大器 | 確認（Petal's single-body 96 amp repeater） |
| 78 | FIFO 把 2 芯拆成兩條單芯放大再合回 | 確認 |
| 79 | 96 是單一中繼器內的放大器數，不是中繼器總數 | 確認（站主指定要寫清楚的那一條，文章寫對了） |
| 80 | 7,000 公里的海纜約需一百個中繼器是通則 | 確認（typically needs about a hundred；文章有標明是通則不是 Petal 規格） |
| 81 | 一條纜承載 1 petabit 比兩條 0.5 Pbps 省材料、資源與碳足跡 | 確認 |
| 82 | 圖說寫 Petal 是 Marea 的 5.5 倍 | 確認 |
| 83 | 頁面沒有印 Marea 的容量 | 確認 |
| 84 | 「這一篇沒有獨立核算」「這一篇不替 Meta 回推這個數字」 | **已改**（編輯流程寫進正文） |
| 85 | 圖解 `alt` | 不適用（圖尚未繪製，`_DRAWINGS` 依 DELTA-4-7 第 15 條還沒登記） |
| 86 | 圖說的四代數字與查核日 | 確認（與研究紀錄 `diagram.caption` 逐字相同，數字都在正文） |

### 第四節「誰出資、誰施工」

| # | 主張 | 判定 |
| --- | --- | --- |
| 87 | 聯合稿的三方分工（Meta 出資並營運／NEC 設計建造／住友電工供纖） | 確認（逐字） |
| 88 | 「**Meta 出資並營運這句分工，只有聯合新聞稿才寫**」 | **已改**（Meta 貼文自己寫 our latest cable investment；只有「營運」是聯合稿獨有） |
| 89 | Meta 貼文說 NEC 是統包供應商、負責製造與安裝最終產品 | 確認 |
| 90 | Meta 引 Orange 國際網路事業群主管 | 確認（EVP, Orange International Networks） |
| 91 | 「1 petabit 是 terabit 里程碑之後 25 年的重要突破」 | 確認 |
| 92 | Meta 用肯定語氣寫世界第一 | 確認（will be the first…） |
| 93 | 「住友電工具名的聯合新聞稿**用詞比較保守**，寫這套系統力求成為世界第一個**商用** petabit 級光纖海纜系統」 | **已改**（把兩句不同強度的話混成一句，方向還相反） |
| 94 | 類比原文與中文對照 | 確認（逐字） |
| 95 | 原文帶星號 | 確認 |
| 96 | 「**平均**每個音訊串流約 0.16 Mbps」 | **已改**（註腳寫 ~0.16 Mbps，沒有「平均」） |
| 97 | 約 62.5 億個同時串流 | 確認（≈ 6.25 billion） |
| 98 | 「引用時把條件一併寫出」 | **已改**（編輯指令寫進正文） |

### 第五節「官方還沒有說的事」

| # | 主張 | 判定 |
| --- | --- | --- |
| 99 | 不清楚 2029 年哪一個月、沒有開工日與鋪設時程 | 確認 |
| 100 | 沒有寫每一對或每一芯的容量 | 確認 |
| 101 | 「也沒有寫調變格式或**使用哪個頻段**」 | **已改**（L 波段有出現，講的是沒有選的 PLCN 那條路；限縮成 Petal） |
| 102 | 沒有寫容量會不會賣給其他業者、沒有寫其他投資方 | 確認（Meta 只寫 invite the ecosystem to invest alongside us，沒有點名） |
| 103 | 兩份文件沒有提到台灣、Petal 不經過台灣、2029 年才預計啟用 | 確認 |
| 104 | 大約 99% 洲際資料流量走海底光纖 | 確認（Approximately 99%） |
| 105 | 頁面沒有標年份或出處 | 確認 |
| 106 | 「這一篇照樣寫成 Meta 的說法，不當成有年份的統計」 | **已改**（編輯流程寫進正文） |
| 107 | 可以查 Connectivity 分類與住友電工新聞稿頁 | 確認 |
| 108 | 兩份文件講的都還是預計與排定 | 確認 |

### FAQ、callout、結尾連結、來源

| # | 主張 | 判定 |
| --- | --- | --- |
| 109 | A1「Expected to enter service in 2029」 | 確認（逐字） |
| 110 | A1「scheduled to commence operation in 2029」 | 確認（逐字） |
| 111 | A1 兩份都只寫到年份 | 確認 |
| 112 | A2「都沒有提到台灣或亞太航線」 | **已改**（同 49） |
| 113 | A3 1 Pbps ＝每秒 1,000 Tbps、最先進海纜的兩倍 | 確認 |
| 114 | A3「平均每個音訊串流」 | **已改**（同 96） |
| 115 | A4 8／16／24 對與 Anjana 0.5 Pbps | 確認 |
| 116 | A4 Petal 等效 48 對、1 Pbps、Anjana 的兩倍 | 確認 |
| 117 | A5 聯合稿的三方分工 | 確認 |
| 118 | A5 Meta 貼文說法國端登陸由 Orange 協助 | 確認 |
| 119 | A5 兩份文件都沒有寫造價 | 確認 |
| 120 | A6「聯合新聞稿用詞比較保守」 | **已改**（同 93） |
| 121 | A6 Meta 寫大規模部署多芯光纖技術 | 確認（at scale 的限定有保留） |
| 122 | callout 標題「預計 2029 年啟用，不是已經完工」 | 確認 |
| 123 | callout 的出處、查核日、沒有獨立技術驗證 | 確認 |
| 124 | callout 兩份文件沒有造價／登陸城市／啟用月份／台灣 | 確認 |
| 125 | 第一個結尾連結 text 與 `tech-news-2026-index` 的 zh-TW title | 確認（**逐字相同**，程式比對） |
| 126 | 第二個結尾連結 text 與 `tech-news-taiwan-matsu-cable-tm4-20260918` 的 zh-TW title | 確認（**逐字相同**，程式比對） |
| 127 | `sources[1]` 網址／標題／`checked_on` 2026-09-23 | 確認（今天 200／100,217 bytes） |
| 128 | `sources[2]` 網址／標題／`checked_on` 2026-09-23 | 確認（今天 200／150,242 bytes） |
| 129 | 研究紀錄 `hero_label`（9.00 units）與 `diagram` 四格額度 | 確認（全在規格內；圖上數字都出現在正文） |
| 130 | 研究紀錄 41 條 `verbatim_quote` | 確認（今天全部仍是連續子字串） |
| 131 | slug 後綴 20260921 ＝ `news_date` 2026-09-21 ＝第一段「2026 年 9 月 21 日」 | 確認 |
| 132 | NEC 官方頁今天是否讀得到 | 確認為讀不到（兩個網址都 403） |

**小計：132 條主張，109 條確認、20 條改（對應 17 處實際編輯，其中 3 個錯誤各出現在正文與 FAQ 兩地）、1 條查無、2 條不適用。**

## 3. 改掉的 17 處（下面分 19 條說明，因為有 3 個錯誤各要在正文與 FAQ 兩地改；原文 → 改成什麼 → 來源怎麼寫）

事實／準確度 12 處：

1. **description**「是現有同距離海纜的兩倍」→「是現有同距離**最先進**海纜的兩倍」。
   來源：`doubling what today’s most advanced subsea cables carry at this distance`。掉了 most advanced 等於把 Meta 的宣稱放大成對所有同距離海纜的兩倍。
   `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

2. **summary 第 2 句**「容量是前一條海纜 Anjana…的兩倍」→「容量是 Anjana…的兩倍」。
   來源只寫 `recently to Anjana’s 24 fiber pairs` 與 `This is double Anjana’s capacity`，沒有說 Anjana 是 Meta 的前一條海纜（同一頁頁尾的舊文清單裡還有 2025 年 10 月的 Candle）。同上網址。

3. **小標**「容量是怎麼長出來的：從一對光纖到二十四對」→「…：從 8 對光纖到 24 對」。
   正文從頭到尾沒有寫過「一對光纖」，來源給的起點是 Marea 的 8 對。同上網址。

4. **P3**「標題是《Inside Petal》」→「標題《Inside Petal》後面接的就是『世界第一條 petabit 等級跨洋海纜』這個主張」。
   頁面標題全文是 `Inside Petal: Building the World’s First Petabit-Class Transoceanic Subsea Cable`，把前半當成標題等於漏掉 Meta 自己在標題上就下的宣稱。同上網址。

5. **P5**「這兩頁都沒有出現台灣或亞太航線的字樣」→「兩頁的文章主體都沒有出現台灣；Meta 那一頁只有頁尾舊文清單印過 Asia-Pacific，講的是另一條海纜」。
   Meta 頁面上 `Asia-Pacific` 出現 **2 次**（Read More in Connectivity 與 Related Posts 裡 2025-10-05 那篇 Candle 海纜的標題）。原句是會被一次搜尋推翻的否定句；研究紀錄 `not_said` 本來就限定在「正文」，是內容包放寬了。同上網址。

6. **FAQ A2**「都沒有提到台灣或亞太航線」→ 同 5 的限縮寫法。同上網址。

7. **P6**「空間**分工**多工（SDM）」→「空間**分割**多工（SDM）」。
   來源 `spatial division multiplexing (SDM)`，division 是分割不是分工。同上網址。

8. **P8**「Meta 表示 Petal 選了第三條路，理由是不必讓整個海纜生態系重新驗證就能把容量做上去，供電也維持在現有設備上限內（額定最高 18 kV）」→「Petal 選的是第三條，目的是在跨大西洋距離做到 1 Pbps。貼文另外寫，Petal 會留在現有供電設備的上限內（額定最高 18 kV）——電壓再高上去，整個海纜生態系就得重新驗證」。
   來源把 18 kV 寫成設計性質（在中繼器那一節），不是選第三條路的理由；而且 `requalification of the subsea ecosystem **necessary at higher equipment voltages**` 的條件被刪掉了。選 2 芯的目的來源自己寫了：`to make the leap to 1 Pbps at transatlantic distances`。同上網址。

9. **P9**「Meta 說明，做法是控制芯與周圍介質的折射率差、讓兩個芯的光訊號反向傳輸，結果是幾乎量不到的串音」→「壓低衰減靠的是製作預型體時使用超高純度合成石英，壓低串音則是控制…」。
   來源分成兩句：`The former is achieved by using ultra-pure synthetic silica during the manufacture of the preform. The latter is achieved by carefully controlling for high refractive indexes…`。原文把「後者」的解法寫成兩個難題的共同解。同上網址。

10. **P11**「——Meta 出資並營運這句分工，只有聯合新聞稿才寫」→「Meta 的貼文只說 NEC 是統包供應商…並把 Petal 稱作自己最新的海纜投資；『營運』這兩個字只出現在聯合新聞稿裡」。
    Meta 貼文寫 `Our latest cable investment, Petal` 與 `Petal is a key piece of Meta’s subsea cable investments`，所以「出資」不是聯合稿獨有；`operate` 一詞在 Meta 頁面**出現 0 次**，聯合稿才寫 `Meta will fund and operate the cable system`。
    `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/` 與 `https://sumitomoelectric.com/press/2026/09/prs040`

11. **P13**「住友電工具名的聯合新聞稿用詞比較保守，寫這套系統力求成為世界第一個商用 petabit 級光纖海纜系統」→「三家公司具名的聯合新聞稿同一頁就有兩種強度，開頭直接寫 Petal 是世界第一個商用 petabit 級光纖海纜系統，後面談規格時改成『力求成為』世界第一個 petabit 級，而且沒有再提商用」。
    這是本輪最重的一處。聯合稿的**標題**是 `…the World’s First Petabit Transoceanic Submarine Cable System`、**首段**是 `have started collaboration to build “Petal”, the world’s first commercial petabit (*) optical submarine cable system`（直述，不是「力求」），而 `aims to be the world’s first petabit-class optical submarine cable system` 那一句**沒有 commercial**。原句把兩句混成一句，還把整份稿說成「比 Meta 保守」，方向相反。
    `https://sumitomoelectric.com/press/2026/09/prs040`

12. **FAQ A6**「聯合新聞稿用詞比較保守…」→ 同 11 的寫法。同上網址。

13. **P14／FAQ A3**「**平均**每個音訊串流約 0.16 Mbps」→「每個音訊串流約 0.16 Mbps」（兩處）。
    註腳原文 `an audio stream bitrate of ~0.16 Mbps (160 kbps)`，`~` 是「約」，不是平均值；頁面全文沒有 average。
    `https://engineering.fb.com/2026/09/21/connectivity/petal-petabit-transoceanic-subsea-cable/`

14. **P15**「也沒有寫調變格式或使用哪個頻段」→「也沒有寫 Petal 用的調變格式或頻段」。
    L 波段在頁面上有出現，講的是 Petal **沒有選**的那條路（PLCN 的 24 對 C+L）；不限縮就與第三節自相矛盾。同上網址。

讀者優先（DELTA-4-7 第 14 條，協調者已授權的編輯）5 處：

15. **P3** 刪「正文一律寫成 Meta 表示」——把查證紀律寫進正文，而且用「正文」指涉自己；同一段的歸因也從 3 個降到 1 個。
16. **P10** 刪「這是 Meta 自己的說明，這一篇沒有獨立核算」「這一篇不替 Meta 回推這個數字」，改成直述「這個倍數只能當成 Meta 給的相對值，回推不出 Marea 有多大」。歸因從 3 個降到 2 個。
17. **P14** 刪句末「引用時把條件一併寫出」——那是寫給撰稿者的指令，不是給讀者的內容。
18. **P16** 刪「這一篇照樣寫成 Meta 的說法，不當成有年份的統計」，改成「是 Meta 的說法，不是可以拿來引用的統計」。
19. **P2** 「這一篇不重複那些數字，也不把 Petal 拿來跟台灣的海纜比較」改成「那是另一個題目——距離、用途與規模都和 Petal 不是同一類」。不比較是靠不比較做到的，不是靠宣告。

（17 處文字取代＋1 處標點整理；上面的 19 條編號含 3 處同一錯誤在正文與 FAQ 的第二地點。）

## 4. 查過而且正確的部分（站主指定的六件事全部通過）

- **2029 年、還沒有蓋**：全篇每一個 2029 都帶「預計」或「排定」，callout 標題直接寫「不是已經完工」。兩份來源分別是 `Expected to enter service in 2029` 與 `scheduled to commence operation in 2029`。
- **沒有衛星、沒有 IRIS²**：內容包全文「衛星」0 次、`IRIS` 0 次、「歐盟」0 次。研究紀錄判斷不收 IRIS²，撰稿照做了。
- **沒有拿臺馬海纜做比較**：全篇沒有距離、容量、投資規模的並列或倍數；唯一出現「臺馬」與「1.9 Tbps」的地方是第二個結尾連結的逐字標題（規格要求逐字照抄）。本輪把第二段那句「不把 Petal 拿來比較」的宣告刪掉之後，文章更不會引導讀者去比。
- **容量宣稱全部歸因給 Meta**：1 Pbps、兩倍、5.5 倍、世界第一、「單一世代最大躍進」都掛在 Meta 或聯合稿名下；本站沒有實測的話寫在 callout 與第二段。
- **串流類比帶著註腳條件**：星號、1 Pbps 總容量、約 0.16 Mbps、約 62.5 億個同時串流四個條件在正文與 FAQ 都寫了，而且明說是類比不是規格。
- **「約一百個中繼器」與 96**：文章寫明一百個是「7,000 公里海纜的業界通則、不是 Petal 的規格」，96 是「單一中繼器內部的放大器數量，不是海纜的中繼器總數」——和來源的 `typically needs about a hundred repeaters` 與 `Petal’s single-body 96 amp repeater` 一致。
- **NEC 的說法**：文章沒有把 NEC 寫成自己發過公告，NEC 的角色分別引自 Meta 貼文（統包供應商）與聯合稿（2 芯系統的設計建造）。
- 科技垂直界線：沒有購買建議、沒有推薦式比價、沒有免責 callout（只有一個 callout，正確）、沒有攻擊手法或斷纜地緣政治。
- 日期一致性：slug `20260921` ＝ `news_date` `2026-09-21` ＝第一段「2026 年 9 月 21 日」；`checked_on` `2026-09-23` 在內容包兩條 source、研究紀錄、第二段、表格 caption、圖說六處一致。
- 兩個結尾連結的 text 與目標內容包的 zh-TW `title` **逐字相同**（程式比對，非目視）。

## 5. 留給協調者／站主的開放問題

1. **「設計容量」這個詞**（description、P1、FAQ A3）。兩份來源都沒有出現 design capacity：Meta 寫 `Petal will deliver 1 Pbps`。文章用「Meta 表示設計容量達 1 Pbps」是往保守方向走（還沒蓋的纜只能談設計值），研究紀錄 `unverified_or_excluded` 也裁定「兩份來源都只寫設計容量」，所以**本輪未改**；但嚴格說是把一個來源沒說的詞掛在 Meta 名下。若要更貼原文，可改成「Meta 表示容量為 1 Pbps」，並在 P15 保留「來源沒有寫初期可用或可售容量」那一條。
2. **「法國電信集團 Orange」**（P4、FAQ A5）。來源只寫 `support on the French landing from Orange`、`landing party in France` 與職稱 `EVP, Orange International Networks`，沒有「法國電信集團」這個描述。事實上沒有錯，但它不在 `sources[]` 裡，**本輪未改**，請裁定是留著還是改成「Orange」。
3. **研究紀錄的一處敘述已修**：`verified_facts` 裡「對世界第一用的是 aims to be，比 Meta 頁面的 will be 保守」這句只引了聯合稿兩種強度中的一種，會把第二輪帶往同一個錯誤。本輪把那一條的 `fact` 改寫成同時交代標題／首段的直述與規格段的 `aims to be`（`verbatim_quote` 未動，仍是原文連續字串）。
4. **NEC 仍 403**（兩個網址、380 與 420 bytes）。若之後抓得到 NEC 自己的稿，值得補進 `sources[]`；但要注意 Meta 貼文裡本來就有一段掛 NEC 名義的具名引言，研究紀錄「NEC 的說法只能引聯合稿」寫得比實際窄。
5. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug（DELTA-4-7 第 15 條是刻意的）。定稿數字已經固定：8／16／24／48／0.5／1／2029，圖上不得出現 Marea 的容量或任何回推值。

## 6. 自檢輸出（原樣）

```
OK tech-news-meta-petal-subsea-cable-20260921 zh-TW paragraphs 2908
check exit=0
```

```
tech-news-meta-petal-subsea-cable-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-meta-petal-subsea-cable-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-meta-petal-subsea-cable-20260921/diagram-1.svg
1 entries checked
lint exit=1
```

`pack_cli lint` 只剩 `image_missing` 與 `raw_internal_url` 兩類，是出圖與 relink 之前的預期狀態。段落字數 2823 → 2908（上限 3000，**刻意留 92 字給第二輪**），description 195 → 198（上限 200）。

## 7. 結論

**needs_second_round。** DELTA-4-7 第 12 條本來就要求兩輪，而且本輪改了 17 處、其中 12 處是事實或準確度，兩處（第 11、第 5 項）動到骨幹敘述。第二輪請特別重查：

- 第 11 項（聯合稿的兩種強度）——那是本輪改動最大的判斷，P13 與 FAQ A6 兩處都要回到 `sumitomoelectric.com/press/2026/09/prs040` 的標題、首段與規格段逐句核。
- 第 10 項（Meta 貼文沒有 operate、但有 our latest cable investment）。
- 第 5、6 項（Asia-Pacific 在 Meta 頁面的實際出現位置與次數）。
- 第 9 項新寫進去的「超高純度合成石英」那一句（第一輪新增、沒有人查過）。
- 第 8 項新寫進去的「目的是在跨大西洋距離做到 1 Pbps」與 18 kV 的條件句。
- 第 4 項改寫後的標題敘述（《Inside Petal》後面那段副標的中文轉述）。
