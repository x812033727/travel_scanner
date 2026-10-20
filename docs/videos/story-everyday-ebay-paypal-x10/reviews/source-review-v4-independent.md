# X10 eBay／PayPal｜v4 獨立來源差異審查

- 審查日期：2026-10-20。**主片 `video.json` 與 Short 1 的來源邊界：PASS。Short 2 的來源年份歸屬：FAIL。整份 v4 前製文字包：FAIL，另有 `shorts.md` 第 8 行的來源年份錯置。** Short 2 的結論有 E22 原件支持，但現有剪輯的「隔年年報」指向錯誤年份，說明欄也漏列 E22。此收據只審來源邊界；不代替敘事盲讀、配音時長或成片審查。
- 主片 `video.json` SHA-256：`3898814710b0a480835505521beb0faca7a8303c7da9d4079d5d09141c0062b3`。
- 兩支短片 `shorts.json` SHA-256：`4b007288aa79d10ef2b90749f9fd4b349230f8c40b52d45f4c18f9c4b899e70d`。
- v3 基線：[來源收據](source-review-v3-delta-root.md) 綁定主片 `39edff49f6d35ca8d98f1bb0f1fdf5672dc64e5ed0cf87191c6de6ddf9b99999`、Shorts `ae05695fecbe98b89ef344d53fe5127bebb2b2c644d3586fd92139a8f027c9dc`；本次逐項比較 `9ffee456..4f1c6a67`。前版 PASS 不直接沿用於新 SHA。

## 原件與改句

獨立重新取得並閱讀 SEC 原件：[E18Q FY2018 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/1065088/000106508818000020/ebay10-qq12018.htm)、[E19 FY2019 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508820000006/ebay201910-k.htm)、[E20 FY2020 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508821000006/ebay-20201231.htm)、[E21 FY2021 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508822000006/ebay-20211231.htm)、[E22 FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1065088/000106508823000006/ebay-20221231.htm)。此次下載的 E20 HTML SHA-256 為 `6c456ee3970ba04daca892f3946fb0b07ac5b9b20aec2eccbee2cd3a3689e417`，與 `/tmp/x10-root-09.html` 一致；文件標題為 `ebay-20201231`，CIK `0001065088`、財年 `2020`。E18Q、E19、E21、E22 的重新下載檔也與相應既存原件逐位元相同。

| v4 改動 | 獨立核對及判定 |
| --- | --- |
| 新 B24、`source-notes.md`／`source-matrix.md`；`x100612`、`x100613` | **PASS。** E20 `Our Marketplace` 原文稱 managed payments 為買賣雙方提供「a simplified end-to-end payments experience」；下一段稱「We can offer buyers more flexibility and choice in how they'd like to pay and offer sellers a more streamlined way to run their businesses.」B24 明列這是 eBay 的產品主張。`x100612` 以「eBay 說」歸因完整流程較簡便，`x100613` 隨即限定不是每位買家的實測體驗。新視覺改為匿名買賣雙方看抽象付款路線，沒有把多付款選項畫成已量得的效果。 |
| `x100717`、企劃一句答案及 Treatment | **PASS。** `x100717` 用「主張……這是它當時的產品理由」標出公司說法；買家選擇及賣家經營兩部分均在 E20，同一措辭也見 E21 `Our Marketplace`。這是 **2020–2021 年公司對自管付款的說法**，不能倒寫成 2015 年董事會分拆 PayPal 的理由，也不能當作分拆改善績效的因果證據；現稿的企劃與 Treatment 已保留這一界線。E18Q 只把付款中介能力列入產品開發重點，E19 才回顧 2018 年開始實際中介及 2019 年採用。 |
| `x100501`、`x100716`，新章名及鏡頭文字 | **PASS。** E18Q `Product Development` 是開發優先項，不是當季全面上線；新 `x100501` 正確限定。`x100716` 是 2015 股權分派和後續市集付款管理的編輯歸納，沒有冒充文件引語。2014、2015、2018、2020、2021 章名對應原件時間；「unpowered」測試台及抽象付款路線不再以畫面預先宣稱真實上線或實測付款選項。 |
| 主片標題、說明與資訊卡；Short 1 | **PASS。** 主片標題沿用「為何又接手收款」的問句；說明仍區分 26% Net TPV、2019 累計處理額和 2021 多因素收入變動。13 張原生統計卡在 v3→v4 未改，日期、母群及單位仍對應 E02/E14/E15Q/A15/E19/E20/E21。Short 1 新「分拆當天有兩件事」對應 2015-07-17 股權分派與營運協議。兩支 Short 共 13 句，逐句均與指定主片同鏡頭原句相同（13/13），但逐字相同不足以保證剪出來後的跨句指代仍成立。 |
| Short 2 | **FAIL（年份指代／說明欄來源）。** E18Q 只列開發重點；E19 才回顧 2018 開始中介、2019 美國採用加快；E20 記載 2020 合約到期後擴張；E21 記載 2021 完成所有市場遷移；**E22** 才明說「Since late 2021, eBay has managed payments for all transactions on our Marketplace platforms」。Short 2 將 `x100602`（FY2020 年報）直接接到 `x100703`「**隔年年報**說得更清楚：自二〇二一年底，平台交易都由它管理付款」；在 Short 的現有順序裡，「隔年」自然指向 FY2021 年報，該文件並無「所有交易」原句。Short 2 說明欄只列 FY2019–2021 10-K，未列真正支持該句的 FY2022 10-K。主片在兩句間有 `x100702` 的 FY2021 年報錨點，故主片指代成立；Short 的剪輯少了該錨點。 |

## 需修正的來源歸屬

`shorts.md` 第 8 行新版流程寫「**2018 年報確認開始中介**」。按一般文件年份讀法，這指 FY2018 年報；但本包所列證據是 **E19 FY2019 Form 10-K** 的追溯句：「Since we began intermediating payments in 2018, ...」。E18Q 只列開發中的付款中介能力；不能用它證明已於該季上線。該行前面的「2018 付款中介回到開發清單」也帶有未由 E18Q 證實的「回到」意味。建議把兩處合成「2018 季報列付款中介能力為開發重點 → 2019 年報回顧自 2018 年開始中介」。

Short 2 可以直接改用主片 `x100702`（「eBay 當年年報說，所有市場的自管付款遷移已完成」）及其同鏡頭 `x10-b07-s02`，讓 Short 的證據停在已列出的 E21；若保留 `x100703` 的「所有交易」，則需在 Short 內補足 FY2021→FY2022 的指代，並於說明欄列 E22。上述只指出來源修正路徑，本次未修改稿件或兩個 JSON。
