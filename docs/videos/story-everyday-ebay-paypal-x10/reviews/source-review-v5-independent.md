# X10 eBay／PayPal｜v5 獨立來源差異審查

**判定：PASS，限此版稿件的來源邊界。** 主片 `video.json` SHA-256 `f3d24233b82f41379b5126a06fcec8f9ec7759a17b403b2fa5a58a27b80f9bb4`；兩支 Shorts `shorts.json` SHA-256 `b7a3d36dc11ec780b65089b2fca1167893e06ba771ed912e578ae94a30a49d6e`。審查者 `/root`，2026-10-20。此收據不核准盲讀、配音、圖像或成片；v4 的 FAIL 收據保留為修訂史。

我重新對照 SEC 原件與 v5 的逐句稿、資訊卡、Shorts 和說明欄，特別檢查 v4 的年份錯置及新增的「為何自管」說法：

| 主張／修訂 | 原件與核對 | 判定 |
| --- | --- | --- |
| 開頭 `x100105` 改成分拆日仍有買賣雙方的付款需求，並未提前宣稱 PayPal 留在結帳。 | [E15Q：2015 Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1065088/000106508815000252/ebay10-qq32015.htm)證實 2015-07-17 股權分派；[A15：營運協議](https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm)證實另有付款合作安排。這句是一般情境示意，不虛構特定交易實錄。 | PASS |
| `x100611`–`x100614` 和片尾 `x100717` 將理由限定為公司的產品說法。 | [E20：FY2020 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508821000006/ebay-20201231.htm)的 *Our Marketplace* 說 managed payments 提供「a simplified end-to-end payments experience」，並稱可給買家「more flexibility and choice」、賣家「a more streamlined way to run their businesses」。原件沒有以繼續交給 PayPal 的反事實方案作比較。v5 已說「公司主張」及「沒證明夥伴做不到」，沒有把自述寫成獨立成效實驗或唯一動機。 | PASS |
| `x100703` 和 Short 2 都明指 FY2022 年報，描述「自 2021 年底」管理平台所有交易付款；Short 2 說明列 E22。 | [E21：FY2021 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508822000006/ebay-20211231.htm)只明說 2021 年完成**所有市場**的 managed-payments 遷移；[E22：FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508823000006/ebay-20221231.htm)才寫「Since late 2021, eBay has managed payments for all transactions on our Marketplace platforms」。v5 不再用會誤指 FY2021 年報的「隔年年報」；Short 2 的來源列表也補 E22。 | PASS |
| Short 2 獨立七句的時間序列。 | FY2019 10-K 回顧 2018 起中介付款和 2019 美國採用加快；E20 記載 2020-07 合約到期後擴張及公司自述產品利益；E22 事後回顧 2021 年底的全平台交易付款。順序與年度相符；並未把 2019 採用說成所有賣家完成，也沒有說 PayPal 被排除。 | PASS |
| 數字卡與 Short 1。 | 2014 年 26% 的分母仍是 PayPal **Net TPV**；2019 >US$2.0B 仍標累計付款處理額而非營收；2020 >1,000,000 是自管付款活躍賣家；2021 +US$1.5B 是淨交易收入年增，旁白仍保留其他推動因素。Short 1 的「每股配一股」和非現金出售對應 E15Q／P15，合作延續對應 A15。沒有新資料類別越界。 | PASS |

片中「自管」指 eBay 管理市集結帳與賣家收款流程，不指它成為每筆交易的銀行或排除 PayPal 付款選項。來源矩陣的 B24 對應 E20 的公司說法；v5 `shorts.md` 將 Short 2 正確標為 FY2022 回顧，與權威 `shorts.json` 一致。兩支 Short 的敘事獨立性、開頭懸念與畫面提早洩底仍交給未讀舊審查的盲讀者判定。
