# A01 輪子行李箱 r10：來源與敘事修訂候選 — HOLD

這是只針對 A01 的**離線稿**。基底是站主選定 7–8 分鐘旁白正文的 [r9](../A01-duration-decision-20261018-r9/README.md)，其 `manifest.json` SHA-256 為 `E414858F7EC6EBD0B07711E0A025CD96C04A80434C9CFFF5CCBC6EBF7E498EE4`。修訂依據為 [r8 獨立全文審稿](../A01-r8-independent-full-editorial-review-20261018.md)，SHA-256 `71EF4677C20262AD1DF336C626A1662D3C010F1938C3225D6DC9CBCC5AD88CF5`；該審稿結論是 **HOLD**，不是已核准的審稿收據。`build.mjs` 對 r9、審稿與輸出逐檔驗雜湊，原 r8/r9、試作系列及 B18 皆不修改。

## 本輪修正

1. `video.json.sources` 由目前播出主張的 16 個不同 URL 重建。`source-map.json` 列出每個 URL 對應的主張 ID；只存在歷史註記但未被此稿主張引用的來源不進上傳說明。這解決 r8 全文審稿指出的 P1 索引不一致。正式工人會把企劃的來源重新合進章稿，因此正式機接入時仍須驗證 worker 實際輸出的來源清單和說明欄；本地 16 筆相符不能代替該步。
2. 1921 年安妮塔帶孩子等候的地點改為**未指明**，畫面不再畫成特定車站。1939 年茶會所見只是一場有輪箱的報導，不證明與 1928 年是同一只實物或連年使用。
3. 1939 年後的重複轉場與 1970 年代阿魯巴返程負擔合成一鏡；Sadow 的兩只 27 吋傳統箱及孩子行李保留，人物之間不編造發明交接。底面兩半的技術專利旁白及無法解釋它的畫面一同移除；拖帶及提把的可查專利敘述保留。
4. 開場車庫與後段車庫指定相同構圖、工作檯和燈位，待取得核准的第一張圖後用其作回場參考。`turn-09b` 才揭露雙輪與伸縮拉桿。大問題「箱子早能滾，還缺什麼才能走進日常？」新增 `x7r4→r3n03` 回路；payoff 是 `now-1993-retail` 場景的 `r3n03` 口播「回到開頭」，位置在機組先用、旅客看見之後、記者試箱之前，以 1993 年商店可買到多品牌的證據回扣。`jtmg→3zwf` 只回收車庫外形揭示。結尾再回答社會習慣、零售採納和使用設計三道障礙，並明說 Anita、Sadow、Plath 沒有可證實的直接發明傳承。
5. 1993 年零售資料移到記者試箱之前。記者把衣物和書放入外袋後才發問，下一鏡即交代她這只箱子的收納結果；不把單次實測推成所有機艙的通則。

來源邊界沿用逐鏡 `claims.md`，全部保持 `PENDING`。改動所用的一手或直接回憶材料包括 [Winnetka 歷史學會的 1921 年記述](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)、[Sadow 受訪回憶](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)、[Plath 的專利](https://patents.google.com/patent/US4995487A/en)、[Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage/)及[1993 年《洛杉磯時報》記者試箱](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)。網站或公司回顧各只能證明其所記，畫面是可愛插畫而非歷史證物重建。

## 產生與檢查

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r10/build.mjs --check
```

`validation.json` 包含 250／275／300 口語單位每分鐘的**紙上估時**、lint、可愛插畫提示檢查和 URL 集合相等驗證。這版在 300／275／250 CPM 分別估 **439.7／474.6／514.8 秒**；較慢的 250 估值仍超過站主 420–480 秒正文目標，須以實際配音決定如何處理，不能機械加速。`x7r4→r3n03` 的 payoff 在 **第 56／65 鏡**，按 300 CPM 紙上時間約從正文起 **359.1 秒**進入；它與開場 setup 之間的紙上間隔是 322.5 秒。這些估時不能當真實 TTS、停頓或成片時長。5 秒片頭與 21 秒片尾是另一組資產，不拿它們補正文。敘事是否吸引人，仍須逐鏡完整複審及不知稿情的聽者聽真實台灣口音音檔；不能以問號數或 URL 數自動判 PASS。

**下一關仍為 HOLD：**先給 r10 做獨立全文來源、敘事、畫面複審；再量實際 TTS 與盲聽；另核對正式機六章資料、worker 的企劃來源重併、A01 專屬片長關卡、工作與預算。沒有新的 `story/reviews/script-review.json`、版本與主機前檢前，不匯入、不製作付費媒體、不把此候選冒充正式章稿或完片。B18 和後五集的十分鐘規格不受本稿影響。
