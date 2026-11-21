# C03 Moleskine｜獨立來源與書面配鏡查核

查核日：2026-10-25。查核者：`/root/find_rules`；協查：`/root/find_rules/c09_delta`。查核者未撰寫本集作者稿，未以作者自評、敘事盲讀或站主核准代替證據。

**結論：SOURCE PASS／WRITTEN VISUAL PASS。** 現稿143句來源PASS、110景書面配鏡PASS（100個shot、9張數字卡、1個outro）。這是r1完整獨立查核、r2精確修正與r3來源差分的接鏈結果；未變段不冒稱本輪重新開啟全部原件。

## 本次綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005` |
| narration-only.json | `3d5461032a626e9c3246b5b2214af504e3fffee81c1a83cdda38dc2ba532c235` |
| script.md | `1698aa0a955713ae5f0eaf9234ad307e32332aa7a02aaa966b8e34bd01736709` |
| claims.json | `c8eaf8b7d01704417b147ff7af3080e5a6041d964b9cc6830d5b0153f6eb4328` |

## 獨立查核收據與來源鏈

| 收據 | SHA-256 | 真實判定 |
| --- | --- | --- |
| history/r1/source-and-visual-independent.json | `74b85f25368a1126fa09218cdafc4470a6a77bb30fff7abdb43756fbde76707a` | 原稿144句141 PASS／3 HOLD；111景書面配鏡PASS。歷史HOLD保留。 |
| history/r2/source-r2-delta.json | `f40e8afb3f4e82d216ccae60b1ef2b6d92a801a9aa21861672e8827b69ad2a53` | 三項HOLD已解除，144句／111景來源與書面配鏡PASS。 |
| reviews/source-r3-delta.json | `b4b15def639f0addb280c3cd238de2fdd51d005697fe16a96e22d7ca7725f390` | 現版143句／110景來源與書面配鏡PASS。 |

各階段的四輸入與基線收據雜湊已實際讀檔核對；目前video、narration、claims逐行ID／文字／順序一致，script含相同順序旁白。完整逐句ID、文字SHA、來源anchors及書面配鏡判定在上述JSON收據。

## 本輪覆核要點

- 歷史作家與現代品牌保持一次連續、明歸品牌官網的型制區分；未聲稱歷史人物使用現代商標商品、真人背書或法國工坊直接傳承。商標精確日期仍為首次申請日。
- 新增排程三句直接讀2013招股書PDF159–160／印刷157–158，原PDF SHA `bf33730ab8fae0290e95c65ac1e70e734fdeb5061f99e96154f8071772e774fe`。既有商品用歷史銷售，新商品用商務部門預測；生產到上市之間平均3–6月，未改成純製造期、物流運送期、下單到出貨或今日固定交期。
- 結尾回呼既述「待寫的書」、較新半年批發／銷售回升與營業結果微降；「我更覺得」是明示旁白判讀，沒有買家付費因果或獲利保證。會計期間、估值／收入／減損／融資費用的原限定保留。
- r3實際刪除3景5句、新增2景3句及outro一行，另改4個保留句；105個保留場景完整物件相同，所有保留data／prompt／camera／字卡未變。新增兩景為匿名樣本與無字預測文件的概念插圖，沒有史實誤導；loops無失效端點。

## 範圍限制

本檔只承接實際做過的來源與**書面**配鏡查核。未讀敘事讀者答案，未核敘事通過、站主核准、實際TTS／音訊、生成後圖片、媒體沿用、實長、費用或成片。prompt的沿用資格不是實際媒體沿用證據。沒有付費API呼叫或後台寫入，也不授權上傳／發布。原r1 HOLD與歷史收據均未改寫。
