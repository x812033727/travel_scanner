# ai-server-supply-chain-layers 查核第一輪（2026-10-05）

格式：主張｜結果（ok / fixed / softened / removed）｜來源網址。
IEA 報告頁今天回 403，內容讀自 IEA 資產主機的 PDF（KQ = https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf ；EAI = https://iea.blob.core.windows.net/assets/b8a83930-5c77-4da7-b795-270ab6a6c272/EnergyandAI.pdf ，兩者 HTTP 200），sources 保留報告頁網址。

## 正文、摘要、表格、callout

- 全球資料中心用電 2025 年約 485 TWh｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 10 頁）
- 2030 年約 950 TWh、約占全球用電 3%｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 10、24 頁）
- 2024 年約 415 TWh｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 24 頁）
- 2024→2025 成長超過 15%、略高於全球用電 1.5%｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 17 頁）
- 以 AI 為主的資料中心用電到 2030 年變成三倍以上｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 25 頁）
- 1 TWh 是 10 億度電｜ok｜單位換算
- 伺服器約占用電 60%、儲存約 5%、網路最多 5%，其餘冷卻、不斷電設備、照明｜ok｜https://www.iea.org/reports/energy-and-ai（EAI 第 52–53 頁）
- 冷卻占比約 7% 到超過 30%｜ok｜https://www.iea.org/reports/energy-and-ai（EAI 第 53 頁）
- PUE 定義（總用電除以資訊設備用電）｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 詞彙表）
- PUE 頂尖約 1.1–1.2、較舊或企業自營約 1.5–1.7｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 30 頁）
- 許多地區併網等待五到十年｜fixed（「可能要」改「可能長達」，原文 as long as）｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁）
- 機櫃例子 2020 年 32 顆約 13 kW、目前每顆 1,000 W 每櫃 72 顆約 130 kW、已宣布下一代約 600 kW｜ok（不寫廠商與架構名）｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 40 頁）
- 到 2027 年冰箱大小的機櫃峰值用電約 65 戶家庭｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 10 頁）
- 晶片集中在同一機櫃可減少延遲與電力損耗｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 40 頁）
- 單顆晶片功率越來越高（表格）｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 40 頁）
- HBM 定義：多層記憶體晶粒垂直堆疊、寬介面｜ok（補上「資料傳輸率遠高於一般記憶體模組」）｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 詞彙表）
- JEDEC 2025 年 4 月發布 HBM4 標準｜softened（官方頁今天 403，只有搜尋摘要；改寫以官方公告為準）｜https://www.jedec.org/news/pressreleases/jedec%C2%AE-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard-advancing
- HBM4 介面 2048 位元｜removed（同上）｜同上
- HBM4 每疊頻寬最高 2 TB/s｜removed（同上）｜同上
- HBM4 可疊 4 到 16 層｜removed（同上）｜同上
- HBM4 單疊最高 64GB｜removed（同上）｜同上
- JEDEC 是「記憶體標準組織」｜fixed（改「微電子產業標準組織 JEDEC（固態技術協會）」，依 JEDEC 自述）｜https://www.jedec.org/rss.xml
- JEDEC 制定 HBM 標準｜ok｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf（第 3 頁）
- 領先的 GPU 系統記憶體 2023 年不到 150 GB、2027 年超過 1,000 GB｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁）
- 同樣容量 HBM 需三倍晶圓產能｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁）
- 2025 年下半年起高階記憶體成為 AI 伺服器生產速度的限制｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁）
- HBM 短缺預期至少到 2027 年底｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 10 頁）
- 2025 年高階晶片封裝產能是建置限制之一｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁）
- 封裝是晶片製造最後一步、提供供電與散熱｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 21 頁註 2）
- 並排在中介層上為 2.5D、疊在上方為 3D｜ok｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf（第 3–4 頁、圖 6）
- HBM 連線寬，並排較實際；3D 要克服散熱與大量導通孔；連線越短越快越省電｜ok｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf（第 3 頁）
- 小晶片（chiplet）放進同一封裝｜ok｜https://www.iea.org/reports/energy-and-ai（EAI 第 69 頁）
- 加速器包括 GPU 與 ASIC｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 30 頁、縮寫表）
- ASHRAE 2026：800 或 1,200 公釐大型機櫃、地板與天花板承重要求較高｜ok｜https://tpc.ashrae.org/FileDownload?idx=89ebd952-2bd7-48c2-8540-ed98b87cde51
- 縱向擴展：同一運算單元內加速器直接連起、讀寫彼此記憶體｜fixed（原文 within an AI computing pod，改「運算叢集（pod）」）｜https://ualinkconsortium.org/faq/
- UALink 1.0 每通道 200G、最多 1,024 顆、銅線、不加中繼器幾公尺、開放標準｜ok（補中文全名）｜https://ualinkconsortium.org/faq/
- 橫向擴展由 UEC 以乙太網路為基礎制定｜ok｜https://ultraethernet.org/ ；https://ualinkconsortium.org/faq/
- 資料搬移與互連占 AI 系統耗電比例上升｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 30 頁）
- 共同封裝光學已初步量產、用於機櫃之間的交換器｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 31 頁）
- 高密度伺服器風扇用電 10%–20% 不少見、50 kW 機櫃風扇至少 5 kW｜ok（2021 年白皮書）｜https://tpc.ashrae.org/FileDownload?idx=8f306d41-3160-4603-9869-395f7c1473ac
- 直接對晶片液冷快速普及｜ok｜https://tpc.ashrae.org/FileDownload?idx=09cb747c-22a9-4bd1-b397-2f77be04b530
- 冷板貼晶片、經 CDU 把熱交給機房冷卻水｜ok｜https://tpc.ashrae.org/FileDownload?idx=de056975-5882-4c0e-87b9-0197cb45a713
- 浸沒式冷卻把設備泡進冷卻液槽｜ok｜https://tpc.ashrae.org/FileDownload?idx=8f306d41-3160-4603-9869-395f7c1473ac
- 高密度機櫃超出氣冷能力（表格）｜fixed（ASHRAE 是到本十年末的預測，改「逐漸超出」）｜https://tpc.ashrae.org/FileDownload?idx=89ebd952-2bd7-48c2-8540-ed98b87cde51
- 從常見的 400 伏特交流提高到 800 伏特直流｜fixed（原文 400 V 未標交流；改「電壓 400 提高到 800 伏特，並從交流改為直流」）｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 41–42 頁）
- 電壓加倍銅線縮為四分之一、直流減少轉換次數｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 41 頁）
- GPU 同步運算使用電同步起伏｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 40 頁）
- 不到一秒擺動數十 MW、約額定容量一半｜ok（補「百萬瓦」）｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 41 頁）
- 電容處理毫秒級、電池處理較長時間｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 41–42 頁）
- 機櫃上的備援電池｜ok｜https://www.iea.org/reports/key-questions-on-energy-and-ai（KQ 第 56 頁 battery backup units on rack）
- callout：TWh 是「一年」累積的用電量｜fixed（TWh 是一段時間累積的用電量，這裡指一年）｜單位定義
- description 列 JEDEC 為依據｜fixed（JEDEC 頁面無法讀取，改列 IEEE）｜https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf

## 圖

- diagram-1：「網路：機櫃內縱向擴展、機櫃之間橫向擴展」｜fixed（改叢集內、叢集之間）｜https://ualinkconsortium.org/faq/
- diagram-1：「機櫃配電 400 V 交流 改為 800 V 直流」｜fixed（改「配電／400 V 提高到 800 V／交流改為直流」，desc 同步）｜https://www.iea.org/reports/key-questions-on-energy-and-ai
- diagram-1 數字 400、800、2026 都在正文｜ok｜pack.json
- hero.svg 沒有數字，alt 與畫面一致｜ok｜hero.png

## sources

- https://www.iea.org/reports/key-questions-on-energy-and-ai｜ok（403，PDF 200 讀取，保留原網址）｜同左
- https://www.iea.org/reports/energy-and-ai｜ok（403，PDF 200 讀取，保留原網址）｜同左
- JEDEC HBM4 新聞稿｜removed（403，今天無法讀到原頁）｜https://www.jedec.org/news/pressreleases/jedec%C2%AE-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard-advancing
- https://eps.ieee.org/wp-content/uploads/2025/11/ch02_hpc.pdf｜fixed（200；標題補 2021 年版）｜同左
- ASHRAE Snapshot 89ebd952｜ok（200，June 2026）｜https://tpc.ashrae.org/FileDownload?idx=89ebd952-2bd7-48c2-8540-ed98b87cde51
- ASHRAE Bulletin 09cb747c｜fixed（200；標題改原名）｜https://tpc.ashrae.org/FileDownload?idx=09cb747c-22a9-4bd1-b397-2f77be04b530
- ASHRAE 白皮書 8f306d41｜fixed（200；標題補 2021 年）｜https://tpc.ashrae.org/FileDownload?idx=8f306d41-3160-4603-9869-395f7c1473ac
- ASHRAE 白皮書 de056975｜fixed（200；標題補 2019 年）｜https://tpc.ashrae.org/FileDownload?idx=de056975-5882-4c0e-87b9-0197cb45a713
- https://ualinkconsortium.org/faq/｜ok（200）｜同左
- https://ultraethernet.org/｜ok（200）｜同左

## 站內連結

- local-ai-gpu-buying-guide、ai-model-tiers-explained、local-llm-hardware-requirements｜ok（都在允許清單，目標文章存在）｜https://mokaair.com/zh-TW/life/
