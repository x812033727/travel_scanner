# A01 輪子行李箱 r23：安檢時序與 1989 年營運用語修正 — HOLD

r23 只從已固定的 r22 另建，處理 [r22 獨立史實差異審查](../A01-editorial-candidate-20261019-r22/independent-fact-delta-review-20261019.md)的 P1／P2 與[敘事盲讀](../A01-editorial-candidate-20261019-r22/blind-story-review-20261019.md)的同一 P1、片長裕度建議。建置器逐檔核對 r22 manifest SHA-256 `9AB4E2BCA9411951E9471E414EC4170A3ED3D793D645ED9C5921CB941E12B33D`，並固定兩份審查收據 SHA-256 `8432218884329F8BD2978C0661658457C605D1D3E7EADCEE209D3D0230B9B3ED`／`A8BAD7081B7C6E44FF116F41D21A0B005A85DCA58FD91C8F72A36CDE2E93BDBE`。前版收據只說明要改什麼，**不等於 r23 審核通過**。

## 與 r22 的精確差異

- `turn-07` 已交代先見安檢困境、**回車庫**把推車鎖上硬殼箱再帶回機場；`turn-09b` 改為簡短分清這只螺絲推車箱，與 [Travelpro 官方沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)記的直立雙輪、可收拉桿 Rollaboard。[2012 年 USA TODAY／ABC 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)記有安檢、車庫與回機場順序，沒有給該事件確切年份；本版不把兩個設計直接視為同一物，也不排定兩者的精確先後。
- `now-11` 口播、`n42` 主張，以及兩份 23／25 來源企劃的 `chapters.turn.point`／`must_verify[4].claim`，一律改為 Travelpro 所述 **1989 年將營運從車庫搬到倉庫**。原文 `moved operations` 不單獨證明生產線搬遷。
- `engine-09` 把兩句廣告解說收成一句「廣告主打『會滑行的行李箱』。」；被刪的是口播 line ID `393x`，英文原句 `The Luggage That Glides` 仍保存在 `e34` 的來源主張供核對。
- `now-1993-test` 把 1993 年四家輪箱測試引入句收短；下一鏡的測試結果與來源主張不變。未刪掉鉤子、Macy's 進貨轉折、安檢員對話或片尾回收。

來源 URL、引用索引、鏡序及 setup／payoff 不變；74 筆主張全部仍為 `PENDING`。`source-map.json`、`source-alignment.json`、`validation.json` 記錄精確差異。保留 r22／較早候選和審查收據位元組不動。本版只供新的獨立史實與敘事審查，不能承接舊版 PASS。

## 使用界線

紙上片長由字數與固定剪點估算，未做實際配音、停頓、剪輯或成片試看。Winnetka 原站、1939 年原報紙目視及先前收據列出的來源限制仍在。正式機六章銜接、新 worker 主張 ID／來源合併、verifier、listener、兩名敘事讀者和正式 `story/reviews/script-review.json` 尚未完成。維持 **HOLD**：本候選不授權主機寫入、解除 STOP、付費媒體製作或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r23/build.mjs --check
```
