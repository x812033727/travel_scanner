# X10 eBay／PayPal｜v6 獨立來源差異複核

**判定：PASS，限 v6 的來源與畫面資料邊界。** 審查者 `/root`，2026-10-20。主片 `video.json` SHA-256 `ff55b13fe19506d4f79586567fe47887f77dcb1b5b8d3aa9736d46416083179b`；兩支 Shorts `shorts.json` SHA-256 `d599da0a337d4740f9526d863fb6546a1f12f5df9ad33087bd46dd839b3d3c00`。v5 的逐項來源審查 [PASS](source-review-v5-independent.md) 限舊雜湊；本次複核新四句、配圖與 Short 1 的改引，不代替敘事盲讀或配音時長。

| v6 變動 | SEC 原件與界線 | 判定 |
| --- | --- | --- |
| `x100101` 明說「想像二〇一八年春天的一筆 eBay 訂單」，配匿名結帳示意；`x100102` 說當春付款中介列入產品開發重點。 | 第一景清楚標示為**想像情境**，沒有聲稱拍到或查到某一筆實際訂單。[FY2018 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/1065088/000106508818000020/ebay10-qq12018.htm) `Product Development` 確有 intermediated payments 能力的開發重點；季報於 2018 春申報，不能由此推成 Q1 已全面推出，片中仍到後章才用 FY2019 年報回顧實際中介付款。配圖無可讀品牌介面或具體交易數字。 | PASS |
| `x100401` 用「開頭那份營運協議」明確回呼分拆時同日的協議，`x100402` 交代 2015 年 7 月股東一比一獲配股票。 | [2015 分拆資料文件](https://www.sec.gov/Archives/edgar/data/1633917/000119312515237232/d877527dex991.htm)說明每股 eBay 配一股 PayPal、另訂商業合約；[FY2015 Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1065088/000106508815000252/ebay10-qq32015.htm)證實 2015-07-17 股權分派完成；[2015 Operating Agreement](https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm)約定分拆後的付款合作。新句未把分拆寫成 eBay 現金出售 PayPal。 | PASS |
| Short 1 由 `x100401` 改引用 `x100402` 與 `x100406`，後者說 PayPal 未因分拆立刻退出 eBay 結帳；Short 2 未更動來源主張。 | E15Q／P15 支持股權分派；A15 支持分拆後 PayPal 付款合作延續。Short 1 的現金出售問句仍由 `x100405` 否定，續留付款的句子沒有暗示 PayPal 在後年被全面排除。Short 2 的 FY2022 年報錨點及 E22 說明仍與 v5 來源審查一致。兩支仍逐句引用同版主片的同鏡旁白；敘事順序與實際 25–55 秒仍交盲讀／TTS。 | PASS |

其餘統計卡、年度口徑、主片「為何自管」的公司自述界線均沿用 v5 審過的內容；新 `x100401` 配圖的空白股權／協議文件沒有展示未說出的條款。若再修改 JSON，這份收據即不覆蓋新稿。
