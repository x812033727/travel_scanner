# A01 r12 獨立全文複審：離線稿 PASS，正式製作 HOLD

日期：2026-10-18。審查對象為本目錄 `candidate/`、`source-map.json`、`plan-source-addition.json` 與建立器；`manifest.json` 的 SHA-256 是 **`17CC760B8573F97D189DB7C476D57C61EDDD4050F79E54A0460EEE5C15B7A9D3`**。本結論只對此精確版本有效。r12 從 r11 manifest `39BCC9E69C4D89EEA044E145ABB592C587183796E92BB13646C83F82511D289A` 修訂，並針對 [r11 的 n14 P1 更正附錄](../A01-editorial-candidate-20261018-r11/independent-full-review-addendum-20261018.md) SHA-256 `ED0C8932DBE71440CCE9E7A3E6D55EC791EF2785010B53F282357C52CEDDF1D7` 重新審查；不繼承 [r11 原報告](../A01-editorial-candidate-20261018-r11/independent-full-review-20261018.md)的 PASS。

**結論：離線稿 P0 = 0、P1 = 0；P2 見下表。** r11 `n14` 的無來源與「所有旅客都得提箱」問題已在 r12 的口播、主張和畫面同時修好。可把 r12 用作正式機**唯讀**資料銜接與差異審查的候選基準；它還不是正式機實際六章稿，也沒有 `story/reviews/script-review.json`。逐筆主張目前仍是 `PENDING`，**不得據本報告匯入或啟動付費製作**。

## 全稿與機械覆核

我重讀了六段全文、65 個場景、77 句口播與 78 筆主張，逐項核對 64 張插畫鏡頭及片尾卡的敘事位置，並將 r11／r12 候選檔逐檔比較。`candidate/series.json` 和 `lexicon.json` 位元組未變；`candidate/script.md` 僅改 `now-06/tszs` 一句及從它計算出的末尾雜湊；`candidate/video.json` 僅改同一句、第 64 鏡提示詞，並加一筆 Travelpro 來源；`candidate/claims.md` 僅改 `n14`。其餘人物、年份、章序、11 組回路、縮圖、標題、公開說明及片尾口播沒有旁支更動。

獨立解析現版資料：65 鏡、77 句、78 個不同主張 ID、78 個場景主張引用；沒有缺漏、孤兒、重複 ID 或空白主張網址。18 個不同主張網址與 `candidate/video.json.sources`、`source-map.json.source_index` 是同一組；來源表的 78 個 ID 逐筆指向各自主張的相同 URL，沒有錯配。`node build.mjs --check` 退出碼 0；300 CPM lint 0 error、31 warning，可愛插畫檢查 0 error。這些只證明離線產物和機械規則一致，不代表實測配音或已核准像素。

## r11 P1：`now-06/tszs`／`n14` 已修

| 證據與位置 | 獨立判讀 |
| --- | --- |
| [Travelpro 官方 2021-09-15 比較頁](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)，「Advantages of Rolling Suitcases」及「Disadvantages of Rolling Suitcases」 | 該頁說輪箱一般移動容易，但**對部分旅客**，用輪箱應付樓梯或顛簸人行道可能困難。這是品牌官方對當代輪箱使用的比較說明，不是旅客比例的統計，也不證明任何早期原型的歷史性能。 |
| `candidate/script.md:286-288`／`candidate/video.json` 第 64 鏡 `now-06/tszs` | 新句「到了樓梯前，有些人推輪箱也會犯難；平地好走，不代表每一段路都順手」保留「有些人」與可能的路況限制。「平地好走」是來源所述一般移動較容易的口語概括；整句沒有再說每個人都必須提箱、輪子改變重量或早期發明者解決了樓梯。 |
| `candidate/claims.md:95` 的 `n14`；`source-map.json` 最後一筆；`candidate/video.json.sources` 最後一筆 | 同一個官方 URL、2026-10-18 查核日與限定範圍均已記錄；第 64 鏡仍引用 `n14`，現在可追到相應來源。 |
| `now-06` 圖片提示詞 | 匿名旅客停在短樓梯前，普通輪箱直立、雙輪仍著地；手靠近提把但沒有必然提起或攀階的動作。這是可能犯難的示意，不冒充歷史照片或特定產品測試。 |

全文的其他史料邊界仍清楚：未標年的 Plath 安檢與車庫回憶不被硬併到 [Travelpro 所記 1987 年直立設計及 1989 年搬倉](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)；`turn-09/jm3w` 明列 [Plath 校友刊第 17 頁的 1988 年自述](https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf)與公司年份差異。[1993 年記者的四品牌試箱報導](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)只被用來證明當時可在通路買到，不推出市場銷量或普及率。片尾明說 Anita、Sadow、Plath 三條人物線沒有可證實的直接傳承。r12 沒有復活 r11 已修的年份或銷量 P1。

## 敘事、畫面與 P2 驗收項

前五鏡連續留下 Anita 旅後是否續用、Sadow 樣品能否上架、機師車庫實驗和「有輪還缺什麼」等可辨問題；安妮塔的家族反應、百貨現場試拉及 Plath 的安檢動作分別回收。`hook-06/jtmg`→第 46 鏡 `turn-07/q4zn`、`hook-06/x7r4`→第 56 鏡 `now-1993-retail/r3n03` 在 300 CPM 文字代理下仍相隔約 **264.8／322.8 秒**。第 56 鏡前句 `r11n01` 已重提三種阻力；新第 64 鏡把主題帶到現代旅程的路況限制，與片尾「用得順手」銜接。因果回答分階段落在家族接受、零售通路、機組採用及實際使用，不把 1928→1970→1987 說成單一發明傳承。

| P2 位置 | 真實媒體階段須驗的問題 |
| --- | --- |
| 第 56 鏡 `now-1993-retail/r11n01→r3n03` | 44 個口語單位約佔 10.1 秒，但現為一張店櫃 still；首句回顧跨年代三種阻力，可能與單一店面畫面不合。實剪可短切本片先前已核准的相關鏡頭，再回店櫃，不必為此新買圖。 |
| 第 48–50 鏡 `turn-07c→turn-09/jm3w→turn-09b` | 安檢員答「好」與直立拉桿揭露之間插入 1987／1988 年份分歧；歸屬正確，仍需盲聽確認故事張力沒有被日期插句打斷。 |
| `x7r4→r3n03` 主鉤子 | 322.8 秒只是文字代理。實音盲聽確認第 56 鏡的「三關」提醒足以讓觀眾記得開場問題，並聽出 1993 年可買到不等於已普及。 |
| 第 65 鏡 `now-outro` 與獨立片尾 | 三句共 67 口語單位，300 CPM 代理約 15.8 秒，後接獨立 21 秒片尾；需驗真實停頓、字幕節奏與結尾長度。 |
| `hook-06`／`turn-07`、Sadow 重訪鏡頭及新 `now-06` | 車庫回場的同角度、匿名人物、箱子與 MiniMax 可愛畫風目前只有提示詞；需在圖像聯絡表驗像素連續性。新樓梯鏡不能生成必然搬箱或攀階的情境。 |

正文 1,823 個口語單位，300／275／250 CPM 代理分別 **434.0／468.4／507.9 秒**。前兩個值落在 A01 的 420–480 秒正文範圍，250 CPM 超出。5 秒片頭與 21 秒獨立片尾不計入正文；未做實際 TTS、盲聽或成片，不能宣稱真實片長已通過。

## 正式機來源重併與收據界線

**離線來源集合通過，不等於正式機企劃已更新。** `candidate/series.json` 的 `plan.sources` 仍是 23 筆舊企劃來源，沒有新 Travelpro URL；`candidate/video.json.sources` 是本地 18 筆被主張引用的來源。`plan-source-addition.json` 明標 `PROPOSED_NOT_IMPORTED_OR_HOST_REVIEWED`。實際 worker 會由正式機 `beats.sources` 重併，可能得到另一組公開來源網址或重建影片資料。必須先唯讀核對正式機六章、章稿雜湊、企劃及來源清單，再判斷如何納入新 URL，重看合併後的 `video.json`、`script.md`、`claims.md`、`verify-1.md`、說明欄和來源索引。任何與本 SHA 不同的實際稿都需獨立差異審查。

本報告不簽正式 `story/reviews/script-review.json`，也不滿足該收據所需的實際六章、事實、敘事與雜湊綁定。所有 78 項候選主張仍是 `PENDING`；TTS 時長、盲聽、圖片聯絡表、成片審核、工作／預算與主機安全前檢均未完成。本輪沒有接主機、產圖、合成旁白、啟動付費工作或上傳 YouTube。A01、B18 與後五集的付費製作仍 **HOLD**。
