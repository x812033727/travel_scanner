# X19 Uber v6｜獨立 SEC 原件與修稿查核

**本版事實 PASS；雙盲敘事及正式媒體另驗。** 綁定 `video.json` SHA-256 `a3149c4904182bf473a7d452c3e5a80de790402c4b240e10da4b2610e1dfbaf8`、`shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`、`source-matrix.md` `b8fdd00b82d6bae3a4979583f9aad5ec5f8cdd39519b5a7ec41e1e47f0ea1cd6`、`drafts/narration.md` `57d29905fafd83eab2352a351d671680b48ea362540777166cfb90851af898f1`、`visual-plan.md` `f60cdcadb58c5f4ed75e1357aee6a176fdd52c8cc00815f187a45e1cf80b9a14`。舊版查核不能替新 SHA 背書；任何受審檔案更改須重審。

2026-10-21 我從矩陣 URL 重新 HTTP GET S1–S8、S3a、S5a 共十份 SEC issuer originals，全部 HTTP 200、各低於 3 MiB。今日 raw response 比矩陣記錄的 10/20 快照各多 9 bytes，raw SHA 如下，**不等於**昨日原始 SHA。每份只在一個 SEC 安全 script 標籤的網址不同；把今日標籤替換成保存的該份舊標籤後，十份逐位元組全等於 10/20 原件。這是透明的固定標籤比對，不是宣稱兩日 raw SHA 相同。

| 原件 | 今日 raw bytes | 今日 raw SHA-256 | 僅替換尾部 script 標籤後等於 10/20 快照 |
| --- | ---: | --- | --- |
| S1 | 548,316 | `4aef7703ea764828bc5f93a9b1792c66653df195514aea77206b07e27f272512` | 是 |
| S2 | 829,748 | `7b0c4bd318d0cd35899157b6027c21966225833a5590d0d973721b85e49c6780` | 是 |
| S3 | 53,764 | `f1d55c4ff0cc805b5182fb4762691bb47af7ff8e571513480523329af8cac5b5` | 是 |
| S3a | 37,486 | `1c93dbf8e1d25f0ea3d1876b10672e1aa61107b68b51c104f87db728e074a461` | 是 |
| S4 | 512,053 | `ab2391b5d58283794e266c2d2ae664b2a13a02ec796af7df2ea3af388ec71eef` | 是 |
| S5 | 8,692 | `efa0a6afb043dd3009cbe0c514b59b2ca0424b4475d9097b3b5608dac3156d30` | 是 |
| S5a | 33,744 | `66201fcd39ff41e2f4b5d6589de0cae6bedfcccebfc70fa789d084b35e8419f0` | 是 |
| S6 | 499,879 | `a61d34a9ad1be17ab40692314e3ebedceb4d988a44b3b3ec8e2ef93241abddfc` | 是 |
| S7 | 520,393 | `55891e3d97914c0b699734703265da8ce3387f2c891329c188e7dcbebe181b40` | 是 |
| S8 | 583,078 | `9270b2d4aa90a0225e510c8666eed917b6c96fb98ca73f427ccc8e667fcc6d82` | 是 |

v6 改句和主要數字逐項核對：

- **司機、餐廳與 2020 Q2 反超，S1／S2。** S1 Q1 司機端接 Eats 改進與**四月**美加近 40% 當月活躍載客司機跨接外送是兩個時點。S1 5 月初宣布退出八個虧損 Eats 市場，也稱某些市場免新餐廳啟用費並加快加入；`x190215` 只報一次八市場數字，`x190218` 改講餐廳上線後還要有顧客下單，屬機制示意而非捏造可量化貢獻。S2 2020 Q2 Mobility／Delivery Gross Bookings 分別 **US$3.046bn／US$6.961bn**，對上年同期 **US$12.188bn／US$3.386bn**；所用 −75%／+106% 為報告幣別。平台總訂單額 US$10.224bn、公司 GAAP 營收 US$2.241bn、公司 GAAP 淨損 US$1.775bn、兩部門調整後 EBITDA +US$50m／−US$232m 都是不同尺度，旁白未互當。
- **Postmates 簽約與交割時序，S3／S3a／S4／S5／S5a。** S3a 的 8-K 明列 **2020-07-06**、約 US$2.65bn 的 **all-stock** 擬收購；S5a 與 S5 確認 **2020-12-01** 全股票交易完成且美國業務才**開始**整合。S3 電話會議逐字稿雖也稱 all-stock，但有一句孤立的 `stockholders will receive 100% cash consideration` 與該 8-K 及後續成交公告不一致；本票以正式 8-K 和交割公告確認股票口徑，不把孤句當成現金收購。Q2 截至六月，Q3 仍未交割；`x190401–412` 及 Short 2 不倒稱收購造成六月反超或第三季既有網路的成長。S4 Q3 Mobility／Delivery 訂單額 US$5.905bn／US$8.550bn，Delivery 同比 +134%；11/5 公告時雜貨配送已到含台灣的十多國，並未把該國數倒填為九月業績。
- **v6 虧損與因果修正，S2／S5／S6。** S5 說交割時兩個消費者 App 仍分開、背後商家配送網才開始接合；S6 2021 Q2 說 App **大致**整合，近 500 萬消費者、16 萬配送員、逾 2.5 萬商家遷移。`x190505–510` 的動作與措辭符合這些揭露，沒有把遷入名單等同實際留存。S6 的 2021 Q2 **Delivery 部門** adjusted EBITDA 為 −US$161m；S2 同季一年前為 −US$232m，所以同比虧損收窄 **US$71m**，S6 原件亦直接寫 `improved ... by $71 million YoY`。`x190515–516` 明確限於部門合計帳，沒有把收窄、後來轉正或整合單獨歸因 Postmates；矩陣也沒有逐筆收購損益可反推。這修正了 v5 未回答的收購因果提問。
- **後續反轉，S7／S8。** S7 2021 Q4 Delivery 部門 adjusted EBITDA **+US$25m**，`x190601` 一開章就回答上章「轉正嗎」，`x190602` 給數值；這是單季非 GAAP 部門指標。S8 2022 Q4 Mobility／Delivery 訂單額 **US$14.894bn／US$14.315bn**，同比兩者 +31%／+6%；兩個部門當季 Segment Adjusted EBITDA **+US$1.012bn／+US$241m**。稿子沒說這是最早再反超的季度、公司 GAAP 淨利或全年部門獲利。兩支 Shorts 重用已核對的 Q2 日期／分母與交割時序，沒有新增獨立未據主張。

主片必要原件均在 3 MiB 內，作者矩陣稱所需段落在解析前約 16k 字；本票檢查的是完整原件，正式工人仍應實際驗證擷取。此事實 PASS 不代表同 SHA 的兩位全新首讀者敘事 PASS，也不代表實測 TTS 正文 ≥8:00、正式 5 秒片頭／21 秒片尾、圖像／字幕／手機 QA、US$25 實支、MP4 或真實 YouTube 連結已完成。
