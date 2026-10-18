# A01 r23 獨立史實與企劃差異審查（有界通過，候選仍 HOLD）

- 審查對象：`story-rolling-suitcase-v2` 的 r23 隔離離線候選。綁定 r23 `manifest.json` SHA-256 `A5978F8318C87E62F48D9E00330FCDC45FFAF50161601D99017922F4AF888CF4`；所依 r22 manifest `9AB4E2BCA9411951E9471E414EC4170A3ED3D793D645ED9C5921CB941E12B33D`、r22 獨立史實差異收據 `8432218884329F8BD2978C0661658457C605D1D3E7EADCEE209D3D0230B9B3ED`。r22 的 HOLD 不是 r23 的審核結果。
- 本次綁定輸出：`candidate/video.json` `100b6c8be2bc9641a665f68260b34466ce6ae36628e2d5e3304c3c3708c7f17d`；`candidate/script.md` `625c87218e9a016f3141764ae56fceb6e1da1c2d78ac5466a672ad070f3a563f`；`candidate/claims.md` `028273e43e14478bb46f66a19b8d044762b5e23c1dd7a8944c0239f94019f4ad`；23 來源 `candidate/series.json` `d617f9bbae74b023dff458874197c162d13b0e32429e13175f19ae1df0ada150`；25 來源 `proposed-25-source-series.json` `3b309de8d1fcb4b36efe44fd04a3ce844f407e13d5dcba6c75549d10c869d264`。已獨立讀回 manifest 所列全部輸出 SHA-256，皆相符。
- 結論：**本次來源／企劃差異 P0 0、P1 0、P2 0**。r22 P1 安檢時序和 P2 `operations` 用字均已修到可由原件支持，未發現 r23 新增史實越界或 claim／scene 孤兒。這只表示有界差異審查通過；候選仍為 `HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE`，**不是正式 worker 的 script-review PASS**，不授權主機寫入、付費製作或上架。

## r22 兩項問題的回歸

1. **安檢與車庫時序（原 P1）**：r22 `turn-09b` 把鎖箱說成「安檢時」；r23 `candidate/script.md` `turn-09b` 約第 223 行改為「安檢故事裡，鎖在箱上的是推車；Travelpro 記的 Rollaboard，則是直立雙輪、可收拉桿」。它不再說 Plath 在安檢現場鎖箱；前面的 `turn-07` 約第 211 行仍明說「他在車庫用螺絲鎖住推車和硬殼箱，再把這個組合帶回機場」。[USA TODAY／ABC 2012 原報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)第 7–12 行正是安檢看見難題、回車庫固定推車、再到機場，以及後來直立雙輪可伸縮把手 Rollaboard 的敘事；沒有給安檢／車庫事件的精確年份。r23 保留場景順序，畫面 `turn-09b` 仍明示不是螺絲推車箱實物。
2. **1989 `operations`（原 P2）**：r23 `n42` claim、`now-11` 口播（約第 246 行），與兩份企劃 `chapters.turn.point`（約第 78 行）及 `must_verify[4].claim`（約第 122 行）一致改為「1989 年將營運從車庫搬到倉庫」。[Travelpro 官方歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)第 275 行原文為 `moved operations from his garage to a warehouse`；新中文沒有額外指定生產線搬遷。公司史另將直立雙輪伸縮把手設計記於 1987 年；r23 沒有把未標年的 ABC 車庫安檢故事直接等同於該年定型產品。

## r23 其他精確變動

- `engine-09` 從兩句英文口號與翻譯收成一句「廣告主打『會滑行的行李箱』」。[Travelpro 官方歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)第 266 行明說 Macy's 的 campaign 使用相應英文口號，中文改寫沒有擴大主張；`e34` 仍指向該原文。刪去的 line ID `393x` 不承載獨立 claim；`engine-09` 的 `e34` 和留存 line `kzmj` 均存在。
- `now-1993-test` 從較長的場景引導改為「記者把四家輪子登機箱帶上路實測」。[Judi Dash 1993 年 LA Times 一手實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)第 217–240 行明說四條產品線、四家主要品牌、在地面與機艙測試；新句沒有把樣本擴成全市場調查。`n55` 與 scene `now-1993-test` 對位不變。
- r23 僅 `n42` 一項 claim 文字與核對日期改動；其他 73 項 claim 行與 r22 相同。口播 `3zwf/kzmj/jspd/r3n02` 文字變動，`393x` 移除；兩份企劃只有相同的 `chapters.turn.point` 和 `must_verify[4].claim` 兩欄變動。畫面 prompt、18 筆公開來源 URL、23／25 筆企劃 URL、場景順序與 setup/payoff 均未改；未變的 claim 仍依 r21 全文及 r22 差異審查的有界證據，不能把那些前版收據當 r23 正式核准。

## 機械回歸與限制

- `node .../A01-editorial-candidate-20261019-r23/build.mjs --check` 退出碼 0：65 scenes、**76 lines**、74 claims、18 public sources、1836 spoken units；250／275／300 cpm 紙上估時 510.8／470.9／436.3 秒；lint／cute 錯誤 0。這不是實際 TTS 或剪輯長度。
- 獨立交叉比對 `candidate/claims.md`、video scene claims、`source-map.json` claim IDs、`source-alignment.json` claim rows：四組皆為同一 74 個唯一 ID；65 個 scene ID 唯一，76 個 line ID 唯一，已刪的 `393x` 不再被引用。18 個公開來源存在且 URL 索引未漂移；沒有 claim／scene 孤兒。
- 仍沿用 r21／r22 已披露的原件取得限制：Winnetka 官方頁瀏覽逾時、據官方搜尋索引；1939 Midland 大型掃描 PDF 未逐頁目視，僅官方庫 OCR 索引；RNPA 2016 PDF 本輪未重看，r19 曾直接核 pp. 46–48；Chinook 官方 PDF 與 sl8 鏡像未位元組比對；Briggs & Riley 新聞稿依 PRNewswire 原站索引。這些資料的 74 個 claim 仍標 `PENDING`，本次不宣稱完成正式逐項一手證物查核。
- 正式機六章資料銜接、worker claim ID／source merge、verifier、listener、兩名獨立敘事讀者、實際 TTS／剪輯長度與正式 `story/reviews/script-review.json` 均不在本次審查範圍。需另以 r23 逐關卡讀回，才可改變候選 HOLD。

本收據只在 r23 目錄新增；沒有改候選、r22／舊收據、任務票、PR、主機或付費資產。
