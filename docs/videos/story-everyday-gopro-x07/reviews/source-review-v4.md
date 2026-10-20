# X07 GoPro Karma｜一手來源審查 v4

**凍結版本**：`video.json` SHA-256 `5d8177b7c6d18a50cd8e09b2c664a56dec90c03cd2a658d086abb2e1f7dccab3`；`shorts.json` SHA-256 `5e7669757586c0bd81ece04413beb4d40c3a98ffd4b79042feabd1f116e3ab02`。本次逐一核對長片 **93 句口播、13 張原生 stats 卡、YouTube 標題／說明／縮圖**，以及兩支 Shorts 的 **4 個候選標題、2 則說明、13 個 headline、17 句口播和 13 個 shot 引用**。93 個長片句 ID 均唯一，並與 `line-source-matrix.md` 的 93 行完全相符；17 句 Shorts 口播均與長片現有句子逐字相同，所有 shot ID 均存在。下列八份 SEC 原件的 HTML SHA-256 與 `source-notes.md` 一致。

**結論：FAIL。** `x070217`、`x070219`、`x070405` 和 Short 2 的 `titles[1]` 需修；`source-matrix.md` 的 K35／K36、`source-notes.md` 的 G16-Q3 摘要及「主線」同步修正。其餘 **90 句長片口播、13 張 stats 卡、長片 YouTube 欄位、兩支 Shorts 的 17 句口播／13 個 headline／2 則說明／另 3 個候選標題**均 PASS。指定的 K18、K34、K37 PASS；K35、K36 有下述措辭問題。

## 原件核驗

| 代號 | SEC 原件與本次主要段落 | HTML SHA-256 |
| --- | --- | --- |
| G16 | [FY2016 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043517000013/gpro2016-12x3110xk.htm)：Business／Products／Applications／Competition；Risk Factors／Karma、Seasonality；MD&A／2016 results。 | `294be433006d5467ad64e72db1b9c0e46f0f5ffa389883adefca89abe4e0930f` |
| G16-Q3 | [FY2016 Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1500435/000150043516000126/gpro2016-09x3010xq.htm)：MD&A／Third quarter 2016 results／Looking Ahead；簽署 2016-11-03。 | `834b4e67b56c003e20429956272fcc1a45e7db3d3426720a30661a97d961dbff` |
| G17 | [FY2017 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043518000010/gpro2017-12x3110xk.htm)：Business／Sales channels and customers；Risk Factors／Karma、Seasonality；MD&A／Revenue／2017 results。 | `8cb6dba4eb2ac81757f62e857dc466b0ac77fae340b4898de3fda685ea1e9440` |
| G17-Q1 | [FY2017 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/1500435/000150043517000028/gpro2017-03x3110xq.htm)：MD&A／Revenue。 | `f6cdc7eba51691289c4d41d89441afe706e3ce31b8ff4f8dc2c8bbba9fbacef1` |
| G17-Q3 | [FY2017 Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1500435/000150043517000059/gpro2017-09x3010xq.htm)：MD&A／Third quarter 2017 highlights／Gross margin。 | `6506568a9ca50c5648e3a1a6b992fd55764c5fc0b37f74e30b69b99c34d854c2` |
| G18-8K | [2018-01-08 8-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043518000002/gopro8-kjanuary2018.htm)：Item 2.05。 | `547d5ebd98aa85465ebc8403386e0f392f65f44d49680209a8dc6e73f9226c1c` |
| G18-P | [2018-01-08 公司公告，8-K Exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1500435/000150043518000002/pressreleasejanuary2018.htm)：Preliminary Q4 Results／2018 Products and Operating Expenses。 | `d88c67570367669eac7e2268d7807196823119eebad301fb298846eb97fb5df9` |
| G18 | [FY2018 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043519000013/gpro2018-12x3110xk.htm)：Business／Image stabilization；Risk Factors／inventory；MD&A／Revenue／Gross margin／Restructuring／Quarterly results note (1)。 | `261b77d4e0219a184a1fc4aef2de844a928b4a05b5efa07b0d6b20ee1eddccba` |

## 逐句 FAIL 與可執行修正

| ID／矩陣 | 現稿問題及原件邊界 | 建議修正 |
| --- | --- | --- |
| `x070217`、K35、`source-notes.md` G16-Q3 摘要及主線 | 「十月二十三日，Karma 在 **GoPro 網站**開始販售。」G16-Q3 MD&A／Third quarter 2016 results 只寫 **“became available online beginning October 23, 2016”**，未指定 GoPro.com；緊前一句描述 HERO5 時才明列 “online retailers and at GoPro.com”。不能把相機的具體網站套給 Karma。 | 「十月二十三日起，Karma 開始在線上販售。」K35 與來源筆記的「官網」一併改成「線上」。 |
| `x070219`、K35 | 「在召回前，公司已警告 Karma **供貨量略低於預期**。」G16-Q3 MD&A／Looking Ahead 是**當時對全年及假期供應的預測**：production issues resulted in lower than expected supply of HERO5 Black cameras, **“and to a lesser extent lower supply of Karma drones,”** which **“will limit our ability to meet estimated retailer and distributor demand”**。`to a lesser extent` 比較的是 Karma 與 HERO5 受影響程度，並未把 Karma 對自身預估的差額量化為「略低」。現稿也容易讓已發生結果與預測混淆。 | 「召回前，公司預期 Karma 供貨也會低於原先估計，但影響程度小於 HERO5 Black。」勿把預估需求說成已確認訂單或把生產問題接成斷電原因。 |
| `x070405`、K36 | 「**直營通路**營收年增……」G17-Q1 MD&A／Revenue 用的是 **“direct channel revenue”**；G17 Business／Sales channels and customers 說 direct sales 包含直接售予多數美國零售商、部分歐洲零售商，以及網站消費者。「直營通路」易被理解為 GoPro 自有零售／僅 DTC，原件沒有該限制。K36 與 `source-notes.md` G17-Q1 摘要沿用此詞。Karma、HERO5 Black 和配件共同有助營收年增的歸因本身正確，不能拆出 Karma 金額。 | 「**直接銷售通路**營收年增，季報說 Karma、HERO5 Black 和配件都有貢獻。」矩陣可加註直接銷售也包括對零售商銷售。 |
| Short 2 `titles[1]` | 「**相機降價牽出的** US$80.5m，Karma 也在其中」將整筆營收減項的起因收窄為相機降價。G17 MD&A／2017 results 指多款相機及 Karma；G18 MD&A／Quarterly results note (1) 精確說 US$80.5m 為 **price protection and marketing development funds**，與 **camera and drone selling prices** 調整相關，未拆個別產品或支持項目的金額。 | 「相機與 Karma 調價相關的 US$80.5m 營收減項」。 |

## 其餘 90 句與指定主張

| 範圍 | PASS 行 ID | 核對重點 |
| --- | --- | --- |
| 開場 | `x070101`–`x070108` | G16 部分機體飛行中斷電、全數撤回；G18-8K 的 2018-01-02 董事會批准日與 G18-P 公開日分開。 |
| 產品章 | `x070201`–`x070216`、`x070218`、`x070220` | G16 產品設計、GoPro Passenger、多用途是公司信念；G17 專業服務成本比較。`x070218` 的「十一月初已進入美國大型零售店」符合 G16-Q3 的 “now available at major U.S. retailers” 與 11 月 3 日簽署日。 |
| 撤回章 | `x070301`–`x070316` | G16 的全額退款**提供**、無已報相關傷害／財損、第四季佔全年總收入 46%、HERO5 生產延誤與 Karma 撤回共同限制滿足**原先估計**節慶需求、2016 Q4 為當時歷來第二高季度；G17 明說 FY2016 未認列 Karma 無人機收入。2017-02-16 簽署的 G16 已提美國第一季恢復出貨，口播未假定承諾晚於復售。 |
| 復售與帳務 | `x070401`–`x070404`、`x070406`–`x070415` | G17 2 月美國復售、3 月底國際分銷；G17-Q1 有 HERO5 Black/Karma 綑綁；G17-Q3 39.6% 對 Q2 35.6% 的**季增主因 HERO6 Black**、較少 Karma 銷售只是次因；G17/G18 分開 US$80.5m 合併營收減項與 US$14.9m Karma 減記及費用。`x070407` 的「較前季少」只限 2017 Q2→Q3。 |
| 退場章 | `x070501`–`x070515` | G18-P 的 #2 僅 GoPro **自稱 2017 年其價位帶**，未給地區、界線或分母；競爭、毛利及**當時對未來幾年**歐美監管影響的預期是公司表述。G18 的公司毛利率 39.0%→32.6%，−143／−180 bps 是 2017 對 2016 **公司毛利率變動**的拆分，非每架飛機的結果。 |
| 關閉與收尾 | `x070601`–`x070619` | G17 的庫存難以售完是**風險提醒**；G18 說 2018 年**全年持續出售**剩餘 Karma 庫存、第一季關閉空中業務、整體重組實際費用 US$17.8m、無人機及配件**收入同比少** US$62.0m。G18 Business／Image stabilization 仍把 Karma Grip 列作 **standalone accessory**；G18-P 的既有客戶支援承諾有歸屬且未外推至今日。 |

K18 的 46% 是 **FY2016 第四季／FY2016 全公司收入**，不是 Karma 節日損失，PASS。K34 將停產庫存的銷售不確定性保留為 G17 當時的預警，並與 G18 的「sold throughout 2018」實績分開，PASS。K37 將 2017 Q2→Q3 集團毛利改善的主要因素與次要 Karma 因素分開，PASS。K35 的 10 月 23 日與 11 月初時間節點成立，但販售網站及供貨預測措辭 FAIL。K36 的綑綁與三類商品共同推動直接銷售通路營收成立，通路名稱措辭 FAIL。

## 13 張 stats 卡與發布欄位

**13 張均 PASS**：`x07-b03-s06`（FY2016 Q4 佔全年公司收入 46%，G16 Seasonality）、`x07-b03-s13`（FY2016 Karma 無人機已認列收入 US$0，G17 Revenue）、`x07-b04-s01`（2017.02 美國復售，G17 Risk Factors）、`x07-b04-s11`（US$80.5m 合併營收減項，G17 2017 results／G18 Quarterly results note (1)）、`x07-b04-s14`（US$14.9m Karma 減記及費用，G17 2017 results）、`x07-b05-s02`（1/2 批准／1/8 公告，G18-8K／G18-P）、`x07-b05-s04`（自稱價位帶 #2，G18-P）、`x07-b05-s08`（公司預期未來幾年可銷市場受當時監管環境影響，G18-P）、`x07-b05-s10`（39.0%→32.6%，G18 Gross margin）、`x07-b05-s11`（−143 bps，G18 Gross margin）、`x07-b05-s12`（−180 bps，G18 Gross margin）、`x07-b06-s06`（整體重組 US$17.8m，G18 Restructuring）、`x07-b06-s08`（無人機及配件收入同比 −US$62.0m，G18 Revenue）。

`youtube.title`、`youtube.description`、`thumbnail.data` 均 **PASS**。標題的 2017 復售／隔年退出與 G17／G18-P 時序相符；說明保留公司自述的價位帶邊界、監管預期、US$80.5m 合併口徑及 US$62.0m 收入同比口徑。縮圖「停飛？」為問句，所引 `x07-b02-s08` 是可拆穩定器的匿名示意，沒有暗示已證實事故傷害。

## Shorts 逐項核對

| Short／beat | shot ID | headline | 口播對應的長片行 ID | 結果 |
| --- | --- | --- | --- | --- |
| 1／hook | `x07-b01-s01` | 2016：新飛機飛行中斷電 | `x070101`, `x070102` | PASS |
| 1／setup | `x07-b03-s01` | 全部撤回，提供退款 | `x070301`, `x070302` | PASS |
| 1／turn | `x07-b04-s02` | 2017 美國復售 | `x070401` | PASS |
| 1／proof | `x07-b05-s05` | GoPro 自稱｜其價位帶第 2 | `x070504` | PASS |
| 1／payoff | `x07-b05-s03` | 售完庫存後退出 | `x070503` | PASS |
| 1／loop | `x07-b01-s01` | 公司說：競爭與毛利壓力 | `x070506` | PASS |
| 2／hook | `x07-b04-s07` | 第三季 Karma 銷售較前季少 | `x070407` | PASS |
| 2／setup | `x07-b04-s08` | 公司毛利率季增｜主因仍是新相機 | `x070408`, `x070409` | PASS |
| 2／turn | `x07-b04-s10` | 年底相機改價 | `x070410` | PASS |
| 2／proof | `x07-b04-s10` | US$80.5M 營收減項 | `x070411` | PASS |
| 2／proof | `x07-b04-s12` | 相機及 Karma｜兩種支持 | `x070412` | PASS |
| 2／payoff | `x07-b04-s13` | 另有 Karma 減記及費用 | `x070413`, `x070414` | PASS |
| 2／loop | `x07-b04-s15` | 飛機還能繼續賣嗎？ | `x070415` | PASS |

Short 1 的 `titles[0]`、`titles[1]`、`description`，Short 2 的 `titles[0]`、`description` 均 **PASS**：沒有把公司自稱名次寫成獨立市占證明、把 US$80.5m／US$14.9m 合成 Karma 單品虧損，或把 2017 Q3 的毛利季變動擴大為全年結果。Short 2 `titles[1]` 依上表 **FAIL**。13 個 headline 的年份、範圍與 17 句口播的來源均成立；全部 shot ID 存在，畫面為概念示意，不冒充真實事故或獨立市占調查。
