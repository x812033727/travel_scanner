# 最後敘事R2：精確onlydiff

R1 source `fc5c2b2dce69763905273e049f32290f613354cc8d068532e67086dcfd2a3da2` → R2 `1a267cb77e4d3eeddffc850dca6616c68a3c66afcaed38576b6e776a3ca62bf2`。
R1 claims `02bcb6bc2bb7b540b2d5030f37e15fc54334d3f4063c15678e662f455f484dd7` → R2 `cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。

只改10句，移除兩個consumer場景／3句，stderr-contract移到valid-json-fields之前。無新場景／line ID。其餘所有旁白、完整metadata scope、六個章名／章首、第一章全部六景及全部程式／命令卡data不變。

| line ID | R1原句 | R2句 |
|---|---|---|
| 5rfa | 另一筆仍在途，還沒有完成配送的天數。 | 把剛剛的狀態條件，套到這筆在途紀錄。 |
| e77f | 照剛剛的狀態條件，它留在原表；空白不能補成零天。 | 它先被送達條件排除，空白也不能補成零天。 |
| xj3j | 這是作者安排的排錯練習，不是觀察到的AI失誤。 | 這條查詢只抽出欄位排錯，錯字是我刻意安排，不是AI失誤。 |
| i2fq | 這份輸出的第一行，是模式啟動說明文字。 | 先略過這次啟動文字，只解析後面那行合法JSON。 |
| yxh7 | 後面的JSON行本身合法；解析物件前，要先辨認並取出那一行。 | 整串輸出混有文字，不能當成單一物件。 |
| jngn | 代理模式把同一個問題整理成JSON錯誤物件。 | 從物件取出錯字名稱，再從說明文字找候選欄位。 |
| cjm4 | 類別和錯字名稱有各自欄位，說明文字還列出候選名稱。 | 我把候選名稱對回原表，找到多了結尾字母的正確拼法。 |
| 7g26 | 錯誤裡的候選名稱，能和原表欄位逐字對上。 | 把剛剛選出的原表欄位，寫回這份查詢。 |
| 2d84 | 補回結尾字母後，原本的條件、選欄和排序都不必換。 | 再接回原本的條件、選欄與排序，準備匯出同一張單。 |
| 5qhj | 第一列有欄名，重新開啟時就能對回原來的選欄。 | 讀回時，把欄位順序對回剛才的選欄，確認代號和路線沒有互換。 |

非命令卡只改stderr-contract的title／key，完整JSON前後值在r2-onlydiff.json。移除json-stream-question、consumer-expectation及其一個consumer loop，不改剩餘loops。21項claim的定義、證據、範圍逐欄保持R1；只有c12的實際場景列表隨刪景／移位更新，五欄完整。

公開命令、資料、SQL、兩組完整輸出、raw收據、proof、新舊ZIP及來源共98檔逐bytes保持R1。新公開ZIP SHA仍`74064ba70799606bf6c8fbc970109bfad26d0d8a02b73e2c5691534678b9fdf2`；沒有重跑SQL或重包。root封存R1的126列manifest亦全核對。

原raw/native reader3=12/13、reader4=11/13且false完整保留；本次不寫或讀未來R2分數。
