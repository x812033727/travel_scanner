# X07 GoPro Karma｜一手來源審查 v5

**凍結版本**：`video.json` SHA-256 `8e4bbe084bbc4e1be597a636683b9205c07ff3dc327f50c0b834755e0df65d74`；`shorts.json` SHA-256 `bd585ce79159c27eea93897b6d64f99c65662bc6c9c0fb8d777c5db0d93b9d3f`。

**結論：PASS。** v4 的四個來源措辭問題已修正。v5 有 **94 句**長片口播（v4 的一個供貨句拆成兩句）、**13 張**原生 stats 卡、兩支 Shorts 的 **17 句**口播、**13 個**headline、**13 個**shot 引用、**4 個**候選標題及**2 則**說明。逐一核對目前檔案：94 個句 ID 唯一，與 `line-source-matrix.md` 的 94 行文字完全一致；17 句 Shorts 口播都逐字存在於目前長片，13 個 shot ID 均能在長片 scene 中找到。八份 SEC HTML 的檔案雜湊都與 `source-notes.md` 記錄相符。未編輯任何製作檔。

## v4 → v5 變動核對

| 位置 | v5 內容／改動 | 原件與判定 |
| --- | --- | --- |
| `x070217` | 「十月二十三日起，Karma 在線上開賣。」移除 v4 的「GoPro 網站」。 | **PASS**。[G16-Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1500435/000150043516000126/gpro2016-09x3010xq.htm) MD&A／Third quarter 2016 results 寫 Karma “became available **online** beginning October 23, 2016”，未指明 GoPro.com。 |
| `x070219`–`x070220` | 「在召回前，公司**已預期** Karma 供貨低於原先估計。」「但這個供貨問題，**比新相機的輕一些**。」v4 單句的「已警告」「略低」改為預測、相對程度；原 `x070220` 的問句文字搬至 `x070221`。 | **PASS**。G16-Q3 MD&A／Looking Ahead 說生產問題造成 HERO5 Black supply lower than expected，**“and to a lesser extent lower supply of Karma drones”**，並前瞻可能無法滿足**估計**節慶需求。申報簽署 2016-11-03，早於召回；腳本未把供貨生產問題當斷電原因。K35 明列 HERO5 Black，因此口播的「新相機」所指有據。 |
| `x070405` | 「**直接銷售通路**營收年增，季報把 Karma、**新相機**和配件並列原因。」取代 v4「直營通路」；緊前 `x070404` 已明指 HERO5 Black。 | **PASS**。[G17-Q1 10-Q](https://www.sec.gov/Archives/edgar/data/1500435/000150043517000028/gpro2017-03x3110xq.htm) MD&A／Revenue 寫 **direct channel revenue** 的同比增加 benefited from **Karma, HERO5 Black and accessories**；[G17 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043518000010/gpro2017-12x3110xk.htm) Business／Sales channels and customers 說 direct sales 亦包括直接賣給零售商，不限品牌自有門市或 DTC。腳本沒有拆出 Karma 單項金額。 |
| Short 2 `titles[1]` | 「**相機與 Karma 調價相關**的 US$80.5m 營收減項」取代 v4 只以相機降價作因的標題。 | **PASS**。[G18 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043519000013/gpro2018-12x3110xk.htm) MD&A／Quarterly results note (1) 列 $80.5m **reduction in revenue**，由相機與無人機價格調整相關的 **price protection and marketing development funds** 構成；未把整筆歸 Karma 或單純價格保護。 |
| `source-matrix.md` K35／K36、`source-notes.md` G16-Q3／G17-Q1／主線、`treatment.md` 產品與復售章 | 已同步改成「線上」、召回前**預期**供貨不足且 Karma 程度較 HERO5 Black 小、「直接銷售通路」含對零售商直售。 | **PASS**。原件界線與上述四項吻合。K35 未推算實際銷量或已證實訂單；K36 未將通路年增全歸 Karma。 |

本輪依 v4 審查時保存的完整逐句、卡及 Shorts 文字輸出比對，除上表與新增 `x070220`／後移的 `x070221` 外，其餘可見敘述和數值維持原審查內容；再對 v5 全量逐句重核來源。v4 JSON 未另存一份可供二進位 diff 的副本，因此這是**欄位及內容層級**的差異核對；上方兩個 SHA 直接核對 v5 凍結檔案。

## 全量核對範圍

| 長片範圍 | 數量／結果 | 一手來源邊界 |
| --- | --- | --- |
| `x070101`–`x070108` | 8／PASS | G16 撤回、G18-8K 的董事會批准日、G18-P 公告日與公司退場理由不混淆。 |
| `x070201`–`x070221` | 21／PASS | G16 產品與策略、G17 Karma 開發成本、G16-Q3 上架與供貨**預測**；不把網購限定為官網。 |
| `x070301`–`x070316` | 16／PASS | G16 全數撤回、全額退款**提供**、無相關傷害／財損報告、FY2016 Q4 佔公司全年營收 46% 與當時歷來第二高季度、HERO5 生產問題和 Karma 撤回並列；G17 2016 未認列 Karma 無人機收入。 |
| `x070401`–`x070415` | 15／PASS | G17 2017 年 2 月美國復售、3 月底國際分銷；G17-Q1 綑綁和通路；G17-Q3 Q2→Q3 公司毛利改善主因 HERO6 Black、較少 Karma 銷售僅次因；US$80.5m 營收減項與 US$14.9m Karma 減記及費用分開。 |
| `x070501`–`x070515` | 15／PASS | G18-P 的 #2 是 GoPro **自稱 2017 年其價位帶**，未給地區／價帶界線／市占分母；監管說法是當時對**未來幾年**的預期。G18 的 39.0%→32.6%、−143／−180 bps 是 FY2017 對 FY2016 **公司毛利率**比較與拆分。 |
| `x070601`–`x070619` | 19／PASS | G17 停產庫存未必售完是風險預告；G18 說 2018 年全年持續售出剩餘 Karma 庫存、Q1 關閉空中業務、公司重組實費 US$17.8m、無人機及配件**收入同比少** US$62.0m，並仍列 Karma Grip 為單獨販售配件；G18-P 既有客戶支援承諾未外推至今。 |

**13 張 stats 卡均 PASS**：`x07-b03-s06`（FY2016 Q4／公司全年營收 46%）、`x07-b03-s13`（FY2016 Karma 已認列收入 US$0）、`x07-b04-s01`（2017.02 美國復售）、`x07-b04-s11`（FY2017 Q4 合併營收減項 US$80.5m）、`x07-b04-s14`（同季 Karma 減記及費用 US$14.9m）、`x07-b05-s02`（2018-01-02 批准／01-08 公告）、`x07-b05-s04`（公司自稱 2017 年其價位帶 #2）、`x07-b05-s08`（歐美當時監管環境及未來市場預期）、`x07-b05-s10`（FY2016→FY2017 公司毛利率 39.0%→32.6%）、`x07-b05-s11`（其中 Karma 銷售相對相機毛利 −143 bps）、`x07-b05-s12`（Karma 及配件存貨／採購單費用 −180 bps）、`x07-b06-s06`（FY2018 公司整體重組 US$17.8m）、`x07-b06-s08`（FY2018 Karma 無人機及配件收入同比 −US$62.0m）。數值、分母、會計類別與 v4 審查結果一致。

`youtube.title`、`youtube.description`、`thumbnail.data` **PASS**：復售與隔年退場時序、價位帶**公司自述**、歐美監管的未來預期、US$80.5m 合併營收減項與 US$62.0m 同比收入下降均無擴大。縮圖「停飛？」為問句，所引 `x07-b02-s08` 是無標誌產品示意。

**Short 1**：兩個候選標題、說明、6 個 headline、8 句口播及 `x07-b01-s01`／`x07-b03-s01`／`x07-b04-s02`／`x07-b05-s05`／`x07-b05-s03`／`x07-b01-s01` 六個 shot 引用均 **PASS**。**Short 2**：兩個候選標題（含本輪修正的 `titles[1]`）、說明、7 個 headline、9 句口播及 `x07-b04-s07`／`x07-b04-s08`／`x07-b04-s10`／`x07-b04-s10`／`x07-b04-s12`／`x07-b04-s13`／`x07-b04-s15` 七個 shot 引用均 **PASS**。兩支 Shorts 不把公司自稱排名當獨立統計，也不將季度 Karma 銷售比較外推全年；其 17 句口播與長片現行句子逐字相符。

**八份一手資料**：G16、G16-Q3、G17、G17-Q1、G17-Q3、G18-8K、G18-P、G18 的 SEC URL 及 HTML SHA-256 皆依 `source-notes.md` 核對為 **PASS**；完整 URL 與雜湊見該檔案及 [v4 審查](source-review-v4.md) 的原件表。
