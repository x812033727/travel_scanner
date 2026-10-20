# X09 BlackBerry｜v7 獨立來源差異審查

**來源判定：PASS。** 審查者 `/root`，2026-10-20。鎖定 `video.json` SHA-256 `774c84a401b0c08112ec89073d12d9b1a14cb924a40684fc8235c0e70a4ecf27`、`shorts.json` SHA-256 `6341e807ec1c2b06562faaa2b38a65bd90e4dcfe679b5f4bbbec98d2c61e7214`。此收據只判定 v6 失敗項與 v7 新敘述的來源邊界；先前原始文件查核見 [v3](source-audit-v3-independent.md)、[v5](source-audit-v5-delta.md) 和 [v6](source-audit-v6-independent.md)。不替代兩位新盲讀、媒體生成與成片驗收。

| v7 敘述／數字 | 獨立對原件核查 |
| --- | --- |
| `x090506` FY2018 自有設備收入約占合併總收入 **6.9%**；`x090507` 同法 FY2017 約 **28.6%**。 | [FY2018 40-F MD&A](https://www.sec.gov/Archives/edgar/data/1070235/000107023518000007/bb-02282018x40fexhibit13.htm) 的 Consolidated Revenue 列 Handheld US$64m／US$374m 與 GAAP consolidated US$932m／US$1,309m。本稿自行計算 64÷932=6.87%、374÷1,309=28.57%，語音明說「以合併總收入作分母換算」與「約」。該 MD&A 另列 6.6%／27.2%，對應調整後收入 US$967m／US$1,374m；`source-matrix.md` B14、`source-notes.md` M18 已清楚區分，沒有再混搭分母。**PASS**。 |
| `x090503` 與 Short 2 區分 FY2016→17 硬體及其他下降的需求轉弱／機型老化，與 FY2018 公司自有設備下降的授權轉型。 | [FY2017 MD&A](https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit13.htm) 的 Hardware and Other Revenue／Consolidated Revenue 說明前一段原因；FY2018 MD&A Consolidated Revenue 把後一段 US$310m 降幅主要連到從委外手機製造轉向安全軟體授權及夥伴負責新機。兩期收入類別並未被說成純手機支數。**PASS**。 |
| `x090512`–`x090516` 庫存不補貨、後續品牌手機由夥伴做、舊機修理和 BlackBerry 10 更新；Short 2 庫存收束。 | FY2018 MD&A Consolidated Revenue 明說公司自有 handset inventory 不再補貨，因手機不再由公司或代表公司的工廠製造；Handheld Devices 類別含配件及修理；Business Overview 明說繼續提供舊機保外修理和 BlackBerry 10 更新。Short 2 把 US$64m 限為公司自有收入、明說非 KEYone 銷量，未把全額當手機本體。**PASS**。 |
| `x090520`–`x090525` FY2018 合併收入 US$932m、Licensing/IP/Other US$196m／年增 US$70m，且混合類別無法證明 KEYone 收益；`x090601`–`x090603` 專利再授權及舊 IP 合約。 | FY2018 MD&A Consolidated Revenue 直接列上述金額，並把年增主要連到 Teletry arrangement 與先前 IP 授權入帳。稿未把這筆增額算給品牌手機。**PASS**。 |
| `x090616`–`x090617` 舊收入壓力與新機庫存風險的最後推論。 | FY2015 AIF Production 曾列降低庫存風險為 Foxconn 合作考量；FY2017 MD&A 列硬體、舊服務下降；FY2018 MD&A 列轉型與庫存不補貨。稿先說申報未把授權轉向歸給單一動機，再以「可推得」作有限商業推論，沒有稱公司正式宣布此唯一原因或估算節省金額。**PASS，需保留推論標記**。 |

五份 SEC 原件 URL 及原始 HTML SHA-256 列於 [source-notes.md](../source-notes.md)。本次直接核對本機保存的 SEC 原件文字及兩個鎖定 JSON；沒有採用品牌新聞稿或二手整理替代來源。v7 的 8 張數字卡維持文件的期別、類別和金額；Short 1 的 Foxconn 買進轉賣與 TCL 授權分工分別由 FY2015、FY2017 AIF 支持。正式 TTS 時仍須以實際語音檢查百分比和財年讀法。
