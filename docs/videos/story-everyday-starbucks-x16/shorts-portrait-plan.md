# X16 星巴克｜兩支 Shorts 的逐拍 9:16 裁切交接

離線規劃，綁定主片 `9f59ef1533c74c0347e40d5534bb390aa00310ab4b5274e9f6172e68bf3c58fc`、Shorts `1491b408cd15131425167b18093d1411af8ae8d979ee6082f923658bdfdc8498`。**尚無插畫、直式渲染或手機實測**。表內是實際要採用的第一版 9:16 裁切與原生文字覆蓋；生成後要逐鏡核對焦點，再在相同範圍內調整，不能把數字當作 AI 畫在圖上的文字。

主片畫布 1920×1080，每拍選一張真正的 `shot`，用 608×1080 視窗依表列 x 值裁切（y=0），等比輸出 1080×1920。圖片提示詞要求人物臉、手與主道具留在中央 x=656–1264；本表 x 的小幅移動用於把該拍道具放到直式中心，交接時仍須看原圖確認。若焦點落出裁切，先調 x（合法 0–1312），保不住才在同一整片預算內重畫。

原生 9:16 文字與字幕安全區：畫布 1080×1920；所有 headline／大字／資料列置於 x=78–902、下緣 y≤1380；字幕條 x=80–900、y=1430–1595，任何字不進最下方操作區。後製字卡顯示品牌與精確數字，插畫無可讀字、店招、杯標或商標。360px 寬手機預覽須逐拍看對比、遮擋與兩行字幕，正式版再跑工具 `layout` 與 25–55 秒時長。

| Short／拍 | 重用 shot | 608×1080 裁切左上角 | 直式焦點 | 原生 headline（在安全區） |
| --- | --- | --- | --- | --- |
| 1／1 | `x16-b01-s01` | `x=656, y=0` | one blank closure notice in anonymous clerk's hands | 約 600 家 |
| 1／2 | `x16-b01-s03` | `x=630, y=0` | one new-looking plain shop key | 約七成很新 |
| 1／3 | `x16-b03-s09` | `x=680, y=0` | one anonymous owner with plain key | 新店先中？ |
| 1／4 | `x16-b03-s05` | `x=700, y=0` | selected inner ring of plain shop pieces | 分母：入選店 |
| 1／5 | `x16-b03-s11` | `x=610, y=0` | wider outer ring of plain shop pieces | 別算成全部 |
| 1／6 | `x16-b03-s07` | `x=656, y=0` | one plain shop ledger | 看單店利潤 |
| 1／7 | `x16-b03-s08` | `x=690, y=0` | one key beside unmarked street model | 還看未來回報 |
| 1／8 | `x16-b03-s17` | `x=640, y=0` | owner weighs plain key over ledger | 問題是單店帳 |
| 2／1 | `x16-b05-s13` | `x=656, y=0` | plain downward tile in analyst's hand | 2009：−6% |
| 2／2 | `x16-b06-s02` | `x=700, y=0` | plain upward tile beside older one | 2010：+7% |
| 2／3 | `x16-b06-s16` | `x=635, y=0` | one closed folio beside storefront model | 關店一招？ |
| 2／4 | `x16-b06-s03` | `x=656, y=0` | one older shop token inside ring | 同店：滿 13 月 |
| 2／5 | `x16-b06-s04` | `x=690, y=0` | blank extra calendar leaf outside ring | 第 53 週已排除 |
| 2／6 | `x16-b06-s07` | `x=620, y=0` | barista serves one anonymous customer | 交易與客單價↑ |
| 2／7 | `x16-b06-s13` | `x=656, y=0` | barista arranges plain tools at counter | 效率也改了 |
| 2／8 | `x16-b06-s16` | `x=675, y=0` | analyst fits several plain wooden pieces | 不能獨算關店 |

Short 2 第 3／8 拍刻意重用同一張多塊拼圖的插畫，首拍裁左 x=635 呈現未合上，尾拍裁右 x=675 呈現整體；正式剪輯靠後製字卡與鏡頭推移區分，不宣稱兩張不同素材。兩支不套長片片頭片尾，繁中字幕由工具另出，不把字幕燒進長片畫面。
