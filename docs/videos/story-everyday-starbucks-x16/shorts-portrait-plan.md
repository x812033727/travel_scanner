# X16 星巴克｜兩支 Shorts 的逐拍 9:16 裁切交接

離線規劃，綁定主片 `d8e09768665f3ad1783a9a43d62c2ede5a374f35682642cba45521dd7b32ef67`、Shorts `bae123630bfaf9cb49c97998515ecd0f12720beec3bab2d2658d124fff053c37`。**尚無插畫、直式渲染或手機實測**。表內是實際要採用的第一版 9:16 裁切與原生文字覆蓋；生成後要逐鏡核對焦點，再在相同範圍內調整，不能把數字當作 AI 畫在圖上的文字。

主片畫布 1920×1080，每拍選一張真正的 `shot`，用 608×1080 視窗依表列 x 值裁切（y=0），等比輸出 1080×1920。圖片提示詞要求人物臉、手與主道具留在中央 x=656–1264；本表 x 的小幅移動用於把該拍道具放到直式中心，交接時仍須看原圖確認。若焦點落出裁切，先調 x（合法 0–1312），保不住才在同一整片預算內重畫。

原生 9:16 文字與字幕安全區：畫布 1080×1920；所有 headline／大字／資料列置於 x=78–902、下緣 y≤1380；字幕條 x=80–900、y=1430–1595，任何字不進最下方操作區。後製字卡顯示品牌與精確數字，插畫無可讀字、店招、杯標或商標。360px 寬手機預覽須逐拍看對比、遮擋與兩行字幕，正式版再跑工具 `layout` 與 25–55 秒時長。

| Short／拍 | 重用 shot | 608×1080 裁切左上角 | 直式焦點 | 原生 headline（在安全區） |
| --- | --- | --- | --- | --- |
| 1／1 | `x16-b01-s01` | `x=656, y=0` | clerk opens blank notice beside generic cafe doorway | 約 600 家 |
| 1／2 | `x16-b01-s03` | `x=630, y=0` | clerk holds new-looking plain shop key | 約七成很新 |
| 1／3 | `x16-b01-s04` | `x=680, y=0` | owner studies blank storefront plan | 按什麼選？ |
| 1／4 | `x16-b03-s05` | `x=700, y=0` | owner weighs new-looking key beside selection ring | 分母：入選店 |
| 1／5 | `x16-b03-s02` | `x=610, y=0` | planner spreads plain shop tokens across blank map | 橫跨各大市場 |
| 1／6 | `x16-b03-s08` | `x=656, y=0` | analyst opens separate blank shop ledger | 看單店利潤 |
| 1／7 | `x16-b03-s09` | `x=690, y=0` | planner compares two blank future ledgers | 還看未來回報 |
| 1／8 | `x16-b03-s10` | `x=640, y=0` | planner moves plain storefront model on map | 場址也要考量 |
| 2／1 | `x16-b04-s15` | `x=656, y=0` | clerk sets new-looking key aside from mature store ring | 2009：−6% |
| 2／2 | `x16-b02-s04` | `x=700, y=0` | planner studies two differently sized ledgers | 2010：+7% |
| 2／3 | `x16-b03-s16` | `x=635, y=0` | clerk holds generic shop key beside lease folder | 關店一招？ |
| 2／4 | `x16-b04-s14` | `x=656, y=0` | analyst keeps mature-store tile apart from selection card | 同店：滿 13 月 |
| 2／5 | `x16-b04-s02` | `x=690, y=0` | clerk shifts selected tokens on blank calendar | 第 53 週已排除 |
| 2／6 | `x16-b02-s05` | `x=620, y=0` | barista arranges unmarked tools and cups | 交易與客單價↑ |
| 2／7 | `x16-b02-s14` | `x=656, y=0` | barista practises with plain counter tool | 店內也在改 |
| 2／8 | `x16-b03-s12` | `x=675, y=0` | planner weighs generic storefront model beside two ledgers | 不能獨算關店 |

每拍重用一張各自不同的主片插畫，表內焦點與對應 shot 提示詞逐字核對；裁切座標仍須在正式出圖後逐拍驗看。兩支不套長片片頭片尾，繁中字幕由工具另出，不把字幕燒進長片畫面。
