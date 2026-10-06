# ai-server-supply-chain-layers 查證記錄

查證日一律 2026-10-05。格式：主張｜來源網址｜查證日｜怎麼讀到的。
撰稿規則：不寫公司名、產品架構名（IEA 原文的 GPU 世代名稱一律改寫成「一家 GPU 廠商」「目前的架構」「已宣布的下一代」），不寫投資語言。

## 讀取方式總說明

- IEA 報告頁 `www.iea.org/reports/...` 對 curl 與 WebFetch 都回 403；Wayback（web.archive.org）與 archive.ph 經代理連線被重置（curl 35、WebFetch 拒絕），無法取快照。改讀 IEA 自己的資產主機 `iea.blob.core.windows.net` 上的報告 PDF（curl -sSL，HTTP 200，pdftotext -layout）。sources 保留報告頁原始網址。
  - Key Questions on Energy and AI：`https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf`（PDF 建立 2026-04-16、修改 2026-04-23，138 頁）
  - Energy and AI：`https://iea.blob.core.windows.net/assets/b8a83930-5c77-4da7-b795-270ab6a6c272/EnergyandAI.pdf`（2025-04，304 頁）；另一份 `.../34eac603-ecf1-464f-b813-2ecceb8f81c2/EnergyandAI.pdf`（修改 2025-04-30）同段文字一致
- JEDEC（jedec.org）對 curl 與 WebFetch 都回 403（Cloudflare），Wayback 連不上。HBM4 數字只能用 WebSearch 限定 `jedec.org` 的搜尋摘要讀，做了三次不同查詢，數字一致。這是摘要不是頁面原文，列為疑點。
- ASHRAE TC 9.9 文件：從 `https://tc0909.ashraetcs.org/` 首頁（HTTP 200）的連結下載 `tpc.ashrae.org/FileDownload?idx=...` PDF（HTTP 200，pdftotext）。
- IEEE 異質整合路線圖：`eps.ieee.org` PDF，curl HTTP 200，pdftotext。
- UALink、Ultra Ethernet Consortium：curl HTTP 200，去掉 HTML 註解與 script 後讀文字。
- OCP（opencompute.org）規格頁與檔案主機都回 403，沒有使用 OCP 的任何數字。

## 主張

### 資料中心用電（IEA）
- 全球資料中心用電 2025 年約 485 TWh｜https://www.iea.org/reports/key-questions-on-energy-and-ai｜2026-10-05｜PDF 第 10 頁執行摘要「485 TWh in 2025」
- 2024→2025 成長超過 15%、增加約 70 TWh、略高於全球用電 1.5%｜同上｜2026-10-05｜PDF 第 17 頁（印刷頁 17）「grew by more than 15% … adding around 70 TWh … slightly more than 1.5%」
- 2024 年約 415 TWh｜同上（第 24 頁 Base Case）；https://www.iea.org/reports/energy-and-ai（PDF 第 14、49 頁）｜2026-10-05｜PDF
- 基準情境 2030 年約 950 TWh、約占全球用電 3%｜Key Questions｜2026-10-05｜PDF 第 10 頁執行摘要、第 24 頁
- 以 AI 為主的資料中心用電到 2030 年變成三倍以上（約 465 TWh，正文未寫 465）｜Key Questions｜2026-10-05｜PDF 第 25–26 頁「increases by more than threefold to 2030」
- 伺服器平均約占現代資料中心用電 60%、儲存約 5%、網路設備最多 5%｜https://www.iea.org/reports/energy-and-ai｜2026-10-05｜PDF 第 52–53 頁
- 冷卻占比從高效率超大型資料中心約 7% 到效率較差的企業機房超過 30%｜Energy and AI｜2026-10-05｜PDF 第 53 頁
- 其餘包含不斷電系統電池與備用發電機、照明等設施｜Energy and AI｜2026-10-05｜PDF 第 53 頁
- PUE 定義（總用電除以 IT 用電，越低越有效率）｜Key Questions｜2026-10-05｜PDF 詞彙表第 118 頁
- PUE 頂尖超大型約 1.1–1.2、較舊或企業自營約 1.5–1.7｜Key Questions｜2026-10-05｜PDF 第 30 頁
- 許多地區併網等待可達五到十年｜Key Questions｜2026-10-05｜PDF 第 21 頁「as long as five to ten years in many jurisdictions」
- 1 TWh = 10 億度電（1 度 = 1 kWh）｜單位換算，不需來源｜—｜—

### 加速器與 HBM
- 加速器是 GPU、TPU 這類做 AI 平行運算的專用晶片；也包括推論用的特定用途積體電路（ASIC）｜Key Questions｜2026-10-05｜PDF 第 25 頁、第 29 頁。正文刻意不寫 TPU（是單一公司的產品線），改寫 ASIC
- HBM 定義：垂直堆疊多個記憶體晶粒，以寬介面連接｜Key Questions｜2026-10-05｜PDF 詞彙表
- JEDEC 於 2025 年 4 月（4 月 16 日）發布 JESD270-4 HBM4｜https://www.jedec.org/news/pressreleases/jedec%C2%AE-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard-advancing｜2026-10-05｜WebSearch 限 jedec.org 摘要（頁面 403）
- HBM4 介面 2048 位元、每腳最高 8 Gb/s、總頻寬最高 2 TB/s（每一疊）｜同上｜2026-10-05｜WebSearch 摘要；2048 × 8 Gb/s ≈ 2 TB/s 自行驗算一致
- HBM4 支援 4、8、12、16 層堆疊，24 Gb 或 32 Gb 晶粒，最高 64GB（32 Gb 16 層）｜同上｜2026-10-05｜WebSearch 摘要
- 【查核第一輪 2026-10-05】以上 HBM4 日期與數字全部從正文刪除，改寫「以官方公告為準」；JEDEC 新聞稿從 sources 移除（見文末「查核第一輪」）。
- （未寫入正文）JESD270-4A 為 HBM4 1.1 版，2025 年 12 月；JESD330-4 SPHBM4 於 2026 年發布，能裝在有機基板上｜https://www.jedec.org/standards-documents/docs/jesd270-4a ；https://www.jedec.org/news/pressreleases/new-jedec%C2%AE-sphbm4-standard-enables-hbm4-class-bandwidth-organic-substrates｜2026-10-05｜WebSearch 摘要，因無法讀原頁而刪除
- 2023 年領先的 GPU 系統記憶體不到 150 GB，2027 年將超過 1,000 GB（IEA 引用 SemiAnalysis）｜Key Questions｜2026-10-05｜PDF 第 21 頁
- 同樣 GB 數，HBM 需要一般記憶體三倍的晶圓產能（IEA 引用 Micron 2024）｜Key Questions｜2026-10-05｜PDF 第 21 頁
- 2025 年下半年到 2026 年初，高階記憶體成為 AI 伺服器生產速度的限制｜Key Questions｜2026-10-05｜PDF 第 21 頁「binding constraint on the rate of AI server production」
- HBM 短缺預期至少延續到 2027 年底｜Key Questions｜2026-10-05｜PDF 第 10 頁執行摘要「persist through at least the end of 2027」

### 先進封裝
- 封裝是晶片製造最後一步，把晶粒包起來，提供供電與散熱｜Key Questions｜2026-10-05｜PDF 第 21 頁註 2
- 記憶體晶粒可並排放在中介層上（2.5D）或疊在處理器上（3D）；HBM 連線寬，並排較實際；3D 要處理散熱與大量導通孔；連線短則資料率高、搬移耗能低｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf｜2026-10-05｜HIR 2021 第 2 章第 3–4 頁與圖 6
- 小晶片（chiplet）：同一封裝裡放多個專用處理單元｜https://www.iea.org/reports/energy-and-ai｜2026-10-05｜PDF 第 69 頁硬體做法清單
- 2025 年高階晶片封裝產能是建置限制之一｜Key Questions｜2026-10-05｜PDF 第 21 頁

### 主機板、整機與網路
- 多顆晶片緊密聯網才能像一台電腦；集中是為了減少電力損耗與延遲｜Key Questions｜2026-10-05｜PDF 第 40 頁
- 高效能運算的趨勢是 800 或 1,200 公釐的大型機櫃；地板與天花板承重要求較高｜https://tpc.ashrae.org/FileDownload?idx=89ebd952-2bd7-48c2-8540-ed98b87cde51｜2026-10-05｜ASHRAE TC 9.9 Technical Snapshot（Issued June 2026）PDF
- UALink 200G 1.0：每通道 200G、最多 1,024 顆加速器、銅線，不加中繼器最遠幾公尺；用於縱向擴展，加速器之間直接 load/store｜https://ualinkconsortium.org/faq/｜2026-10-05｜curl 200
- UEC 主要處理橫向擴展｜同上 FAQ｜2026-10-05｜curl 200
- Ultra Ethernet Consortium：以乙太網路為基礎、為 AI 與 HPC 大規模網路制定完整通訊堆疊，目前規格 1.0.3｜https://ultraethernet.org/｜2026-10-05｜curl 200
- 記憶體存取、資料搬移與互連占 AI 系統耗電比例上升｜Key Questions｜2026-10-05｜PDF 第 30 頁
- 共同封裝光學已進入初期量產，用於機櫃之間的 AI 網路交換器（晶片之間預計 2027–2028 年，正文未寫）｜Key Questions｜2026-10-05｜PDF 第 31 頁

### 散熱
- 機櫃例子：2020 年架構每顆約 400 W、每櫃 32 顆、約 13 kW；目前架構每顆 1,000 W、每櫃 72 顆、約 130 kW；已宣布的下一代約 600 kW、朝 1 MW 前進｜Key Questions｜2026-10-05｜PDF 第 40 頁（IEA 原文點名廠商與架構名，正文不寫）
- 到 2027 年，冰箱大小的機櫃峰值用電可能相當於約 65 戶家庭｜Key Questions｜2026-10-05｜PDF 第 10 頁執行摘要
- 高密度伺服器風扇用電占 10%–20% 不少見；50 kW 機櫃風扇至少 5 kW｜https://tpc.ashrae.org/FileDownload?idx=8f306d41-3160-4603-9869-395f7c1473ac｜2026-10-05｜ASHRAE TC 9.9 白皮書 2021，第 10 頁
- 直接對晶片液冷正快速普及｜https://tpc.ashrae.org/FileDownload?idx=09cb747c-22a9-4bd1-b397-2f77be04b530｜2026-10-05｜ASHRAE TC 9.9 Technical Bulletin（Issued May 2026）第 1 頁
- 冷板貼在處理器上、最常見是在機櫃外設冷卻液分配單元（CDU）｜https://tpc.ashrae.org/FileDownload?idx=de056975-5882-4c0e-87b9-0197cb45a713｜2026-10-05｜ASHRAE Water-Cooled Servers 白皮書 2019，第 8 頁
- 高效能運算冷卻常同時有氣冷與液冷，液冷需要 CDU；高密度一般機櫃在本十年末超出氣冷能力｜ASHRAE Technical Snapshot 2026｜2026-10-05｜PDF
- 液冷定義：以水或介電液體帶熱，每單位體積吸熱遠高於空氣｜Key Questions｜2026-10-05｜PDF 詞彙表
- 浸沒式冷卻：設備放進冷卻液槽（tank）｜ASHRAE 白皮書 2021｜2026-10-05｜PDF 第 19 頁

### 供電
- 從 400 伏特提高到 800 伏特、交流改直流；電壓加倍銅線大小縮為四分之一；直流減少轉換步驟｜Key Questions｜2026-10-05｜PDF 第 42 頁
- 不斷電系統電池與備用發電機｜Energy and AI｜2026-10-05｜PDF 第 53 頁
- 數十 MW、約額定容量一半的擺動在不到一秒內發生（IEA 引用 Elevate Energy Consulting 2025）｜Key Questions｜2026-10-05｜PDF 第 42 頁
- 電容處理毫秒級、鋰電池處理較長時間｜Key Questions｜2026-10-05｜PDF 第 42–43 頁
- 機櫃上的備援電池（battery backup units on rack）｜Key Questions｜2026-10-05｜PDF 第 56 頁
- 圖上「400 V 交流改為 800 V 直流」與正文一致；圖上沒有其他數字（2026 只在頁尾與表格說明）

## 圖
- diagram-1.svg：結構圖，中間一層包一層（機櫃與網路 → 主機板與整機 → 先進封裝 → 加速器與 HBM、中介層），左供電、右散熱。圖上數字：400、800、2026，正文都有。
- hero.svg：深色機櫃八層等高托盤（不是由低到高的長條）、藍色冷卻水管、橘色電線接閃電圓標、虛線放大到圓圈裡的封裝（晶片、兩疊記憶體、中介層、冷卻管），一行字「從晶片到機櫃」56 px。

## 查核第一輪（2026-10-05，另一位代理）

讀取方式：自己重抓每個來源（curl -sSL，UA 為規定字串），PDF 用 pdftotext -layout，HTML 去掉註解與 script 後讀。檔案在 `_tools/ai-server-supply-chain-layers/v1/`。逐條結果在 verify-1.md。

- IEA 兩個報告頁今天 curl 與 WebFetch 仍回 403，Wayback CDX 經代理連線被重置（curl 35），WebFetch 不允許 web.archive.org。改讀 IEA 資產主機上的 PDF（兩份都 HTTP 200）：Key Questions on Energy and AI（PDF 建立 2026-04-16、修改 2026-04-23，138 頁）、Energy and AI（2025-04，304 頁）。sources 保留報告頁原始網址。
- JEDEC：新聞稿頁、JESD270-4／270-4A 文件頁、jedec.org 無 www、Business Wire 與 Morningstar 轉載頁今天全部 403，archive.ph 連線被重置。只有 `https://www.jedec.org/rss.xml` 回 200，但內容只到 2020 年，沒有 HBM4。HBM4 的日期、2048 位元、2 TB/s、4 到 16 層、64GB 在今天的官方頁面上看不到，只有搜尋摘要，依規則刪除數字，改寫「以官方公告為準」，JEDEC 新聞稿從 sources 移除。
- JEDEC 的中文描述：rss.xml（HTTP 200）裡的 JEDEC 自述是「the global leader in the development of standards for the microelectronics industry」，所以「記憶體標準組織」改成「微電子產業標準組織」。JEDEC 制定 HBM 標準的依據改為 IEEE HIR 2021 年版第 2 章第 3 頁「JEDEC has also recently published a standard for HBM 3」。
- HBM 定義補上「資料傳輸率遠高於一般記憶體模組」｜Key Questions 詞彙表「achieving significantly higher data transfer rates than conventional memory modules」。
- 400→800 伏特：IEA 第 41–42 頁原文是「increasing the voltage from the standard 400 volts to 800 volts … and by shifting from alternating current (AC) to direct current (DC)」，沒有說 400 伏特是交流。正文與圖改為「電壓從 400 伏特提高到 800 伏特，並從交流改為直流」；圖上方框「機櫃配電」改「配電」（IEA 講的是整個資料中心的配電）。
- 縱向擴展的範圍：UALink FAQ 原文是「scale-up connection for up to 1,024 accelerators within an AI computing pod」，不是限於一個機櫃。正文「同一個運算單元」改「同一個運算叢集（pod）」；圖上「機櫃內縱向擴展、機櫃之間橫向擴展」改「叢集內縱向擴展、叢集之間橫向擴展」，desc 同步。UALink 補中文全名。
- ASHRAE 2026 Snapshot：「GPC High Density – kW/Rack exceeding the cooling capability of air toward the end of the decade」是對未來的預測。表格「高密度機櫃超出氣冷能力」改「逐漸超出」。
- 併網等待：IEA 第 21 頁「can be as long as five to ten years」，改「可能長達五到十年」。
- 單位中文：kW、MW 第一次出現補「千瓦」「百萬瓦」。callout 的 TWh 改為「一段時間累積的用電量（這裡指一年）」。
- sources 標題補年份：IEEE HIR 是 2021 年版（PDF 標題 Heterogeneous Integration Roadmap, 2021 Version）；ASHRAE 白皮書 2021、2019 年；Technical Bulletin 原標題 TCS Coolant Integrity and System Readiness Best Practices（Issued May 2026）。四份 ASHRAE PDF 都在 TC 9.9 網站首頁（tc0909.ashraetcs.org，HTTP 200）有連結。
- 其餘 IEA、ASHRAE、IEEE、UALink、UEC 主張逐句對過原文，數字一致。

## 查核第二輪（2026-10-05，另一位代理）

讀取方式同第一輪：自己重抓全部來源，檔案在 `_tools/ai-server-supply-chain-layers/v2/`。IEA 報告頁、JEDEC 仍回 403，Wayback 連線被重置。IEA 讀資產主機 PDF（200）；JEDEC 只有 rss.xml 回 200。逐條結果在 verify-2.md。

- 封裝：HIR 2021 第 3 頁原文「Adjacent placement appears to be an attractive solution」，正文「較實際的做法」改成「較容易做到」，並刪掉句中的 IEEE 出處敘述。
- 風扇：ASHRAE 2021 白皮書第 10 頁原文「not uncommon for some of the denser servers」，正文補上「2021 年」「部分」，並寫明 5 kW 是照這個比例推算的。
- PUE：KQ 第 30 頁原文「Best-in-class hyperscale facilities」，正文補上「超大型資料中心」。
- 400 V：KQ 第 43 頁另有「400-volt AC power」的寫法，第 41 頁沒有標交流。正文維持第一輪的寫法，不改。
- 導言第一段改成用一句話回答標題問題。

## 跨篇核對（2026-10-05）

- 新增姊妹篇連結：ai-concept-stocks-explained、thematic-etf-index-rules（七層表格後）；連結文字不用投資語言、不寫公司名。
