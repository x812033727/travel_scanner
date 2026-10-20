# X09 BlackBerry｜一手來源與事實邊界

2026-10-20 直接讀取下列五份 SEC 原始 HTML，均回 HTTP 200。金額除另註外為美元；BlackBerry 財年在二月底結束，FY2017 不等於曆年 2017。文件與 SHA-256 供重新下載比對，原件不在儲存庫內。

| 代號 | 原件與直接可見的證據 | 下載 SHA-256 |
| --- | --- | --- |
| B15 | [FY2015 40-F 所附 AIF](https://www.sec.gov/Archives/edgar/data/1070235/000107023515000029/bbry-02282015x40fexhibit11.htm)，Devices／Enterprise Services／Production：該財年推出 Classic、Passport；與 Foxconn 共同開發／製造部分裝置，Foxconn 所製手機仍由 BlackBerry 買入轉賣，公司通常掌握材料採購方向；BES12 已跨 BlackBerry、iOS、Android、Windows Phone 管理。 | `bd0e27d1d570459c64956cc0372e8ff5719f2b47bbbc6c45b4d6ac18ed4d75da` |
| B17 | [FY2017 40-F 所附 AIF](https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit11.htm)，General Development／Mobility Solutions／Production／風險段落：BlackBerry 將 handset hardware development 全部外包；FY2017 與 TCL、Optiemus、PT BB Merah Putih 簽安全軟體及品牌授權，夥伴依區域設計、製造、銷售並提供客服，承諾遵守公司品質、安全及品牌準則；公司警告若不符合標準，品牌可能受損。TCL 宣布 KEYone，供貨從 FY2018 第一季開始。當時公司仍賣 DTEK50、DTEK60 及舊機，且風險段落提 FY2018 打算推一款由公司設計、第三方製造的手機；不能寫成 2017 後絕無公司設計的機型。 | `faae7366f1d2e1197ed599b513930ba078cc953732cc2f2c806692d581bfc55d` |
| M17 | [FY2017 40-F 所附 MD&A](https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit13.htm)，Consolidated Revenue：FY2016→FY2017 硬體及其他收入 US$884m→US$374m、舊服務接入費 US$779m→US$313m、軟體與服務 US$497m→US$622m；後者年增 US$125m 主要來自先前收購的 Good Technology 與 AtHoc。舊服務費關乎 BlackBerry 7 或更舊系統、用戶下降與方案組合變化，不是每支新手機都收同一筆費。 | `8cf6de67e2accbfc508a79ffe4bafd85a74221a9c4905ec00a3902c39ffbf94b` |
| M18 | [FY2018 40-F 所附 MD&A](https://www.sec.gov/Archives/edgar/data/1070235/000107023518000007/bb-02282018x40fexhibit13.htm)，Business Overview／Consolidated Revenue／Handheld Devices／Q4 Results：FY2017→FY2018 自有手持設備收入 US$374m→US$64m（−US$310m）。MD&A 原列占比 27.2%→6.6% 對應**調整後**總收入 US$1,374m→US$967m；若以 GAAP 合併收入 US$1,309m→US$932m 為分母，本稿另算約 28.6%→6.9%（374÷1,309；64÷932）。FY2018 第四季相較上年同期 US$55m→2m。公司把該年度設備收入下降主要歸於從委外製造轉向安全軟體授權、把新品牌手機的設計、製造、銷售和客服交給夥伴；過渡期間公司自有庫存不再補貨，新品牌手機不再由公司或代表公司的代工廠生產。FY2018 SAF US$313m→US$121m（−US$192m）、合併收入 US$1,309m→US$932m（−US$377m）。KEYone、Aurora、Motion 已於軟體與品牌授權計畫下推出，公司仍對舊 BlackBerry 10 平台提供更新並對已售手機提供修理。Licensing, IP and Other 年增 US$70m 至 US$196m 主要牽涉 Teletry 與先前簽下的 IP 授權，不能算成 KEYone 授權成果。手持設備類別還含舊機配件與修理服務，不能把 US$64m 當純手機銷量。 | `938b9d032e08ee00fb30638f00505ffa8904fae0859f2d8f1cd63185cd9c2157` |
| B20 | [FY2020 Form 10-K](https://www.sec.gov/Archives/edgar/data/1070235/000107023520000025/bbry-20200229.htm)，Notes to Consolidated Financial Statements／Revenue Recognition／Mobility（約第 79 頁）：FY2017–FY2018 多年期手機授權涵蓋安全軟體、服務及在很多情況下的品牌資產；銷量超過合約最低量時，Mobility 授權收入按夥伴所報授權產品銷售認列，未超過時基於工程服務承諾及最低金額於合約期間平均認列。這是收入認列，不是收現時點。原件約 4.9 MB，超過部分工人的單頁 3 MB 讀取上限，若走正式自動工人須另給可讀的原發行者摘要或標 `reviewer_only`。 | `54367d158e51eadd8cd8c17616f5ab363ecef92c9334c3d7244f5b2e4eee1230` |

## 這支故事可說與不可說

主問題鎖在**FY2017 宣布 KEYone 與硬體開發轉向夥伴**，再看 FY2018 公司舊手機庫存如何退出帳本。FY2015 Foxconn 已共同開發／製造部分手機，但那些手機仍由 BlackBerry 買入轉賣；FY2017 夥伴取得新品牌手機從設計到客服的工作，BlackBerry 保留安全軟體與品牌授權。這是商業模式改變，不是 2017 當天全停售或宣稱 2026 年仍有新機上市。

FY2018 US$64m 是公司自有手持設備收入，不能當 KEYone 授權夥伴銷量；當時授權計畫反而已有 KEYone、Aurora、Motion。Licensing, IP and Other 的增額主要受 Teletry 與早前 IP 授權影響，也不能當成手機授權成功的證據。FY2020 合約段落只說收入認列規則，不能說現金已收、手機授權補回所有缺口。插畫只作匿名概念示意，不畫真實商標、鍵盤布局、KEYone 外形或真人。

最後一段將舊收入變薄、FY2015 文件已提的降低庫存風險考量、FY2018 不再補自有手機庫存與夥伴負責新機的分工連起來，是本集有邊界的商業推論；五份 SEC 申報沒有把這次授權轉型歸因於單一可證明的動機，也沒有給出節省多少庫存成本。
