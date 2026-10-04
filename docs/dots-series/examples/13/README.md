# 第 13 課：合成銷售報表資料

這是教學用合成資料，金額為新臺幣整數，不含個資，不代表真實營收。`sales-v1.csv` 有八筆；`sales-update-v2.csv` 有五筆，包括 O008 的修正與四筆新增。第二批按 order_id 取後到資料覆蓋前值，不能直接相加。

單筆毛額＝units × unit_price；單筆淨額＝毛額 − discount − refund。discount、refund 都是整筆訂單金額，不是單件折扣。這是訂單淨額練習，不是正式會計營收；沒有成本、稅率與會計認列資料，不能算利潤。

欄位：order_id（訂單識別碼）、date（合成訂單日）、channel（web／store）、product（mug／notebook／tote）、units（購買件數，未扣退貨件）、unit_price（單價）、discount（整單折扣）、refund（整單退款）。

`expected-baseline.json` 是編輯先算的預期值，不是 dots 實測輸出。`verify_fixture.py` 以 Python 標準函式庫逐筆重算並對照。可由第二位覆核者用試算表重新計算，獨立保留結果。

實作流程：上傳 v1，要求資料檢查、淨額摘要與兩張分類圖；開啟成果；再上傳 update-v2，明確要求覆蓋 O008，產生更新報告。比對每一項預期值並儲存真實操作紀錄。不得把同一期間補資料解釋成營運成長。
