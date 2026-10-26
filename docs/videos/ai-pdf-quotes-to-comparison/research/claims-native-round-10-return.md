## 第10輪獨立查核附加段（2026-10-26）

本段附加在現行 claims.md 末尾，不取代前文任何內容。

查核範圍：現行 video.json，55 scenes／93 lines。

證據來源：
- 本 ledger 逐字附上的八頁 pypdf 抽文與教材全文。
- lab-comparison.json、selected_result、quantity-21 收據、三份 Decimal 差額紀錄。
- 今日抓取成功（status 200）的官方頁：https://pypdf.readthedocs.io/en/stable/user/extract-text.html （「pypdf is not OCR software」）與 https://openpyxl.readthedocs.io/en/stable/simple_formulae.html （「openpyxl never evaluates formula」）。

| ID | 第10輪結論 | 本輪核對到的原文／實跑證據 |
| --- | --- | --- |
| c1 | CONFIRMED | 三份 PDF 第1頁的 Unit price 原句 |
| c2 | CONFIRMED | requirements.txt 第7–9行與兩張 code 卡逐字相符，行號正確 |
| c3 | CONFIRMED | 檔名與「原件只讀；輸出放另一個資料夾」 |
| c4 | CONFIRMED | 每頁 Fictional training quote 註記 |
| c5 | CONFIRMED | analysis-execution 的 inputs 與 scope_executed |
| c6 | CONFIRMED | aster p1 單價與商品稅；p2「Shipping: TWD 200.00 excluding tax to the specified address」 |
| c7 | CONFIRMED | viewer-prompt.txt 七行逐字相符 |
| c8 | CONFIRMED | birch p1 含稅205；p2 免運、5 business days |
| c9 | CONFIRMED | cedar p2「Shipping: not quoted」「Shipping tax: not quoted」；original-10 Cedar 為 null |
| c10 | CONFIRMED | unit_price_order 為 Cedar、Aster、Birch |
| c11 | CONFIRMED | Aster 10張 2100.00 |
| c12 | CONFIRMED | Birch 10張 2050.00 |
| c13 | CONFIRMED | original-10 只有甲乙可比，乙最低 |
| c14、c15 | CONFIRMED | Decimal 計算；openpyxl 官方頁（2026-10-26 抓取成功） |
| c17、c18 | CONFIRMED（草稿與條件式規則） | 沒有寄出，也沒有說成本次實例 |
| c19 | CONFIRMED | cedar-revised p1「Replaces CED-1026-v1; not an additional supplier.」 |
| c20 | CONFIRMED | revised-10 Cedar：1837.50＋262.50＝2100.00 |
| c21 | CONFIRMED | revised_10_groups：乙單獨一組最低，甲丙同價 |
| c22 | CONFIRMED | revised 列的來源欄指向 cedar-revised.pdf |
| c23、c31 | CONFIRMED（實跑） | argv 與 code 卡逐字相同、exit 0、selected_result 為數量20、三列 |
| c24 | CONFIRMED | 三家第2頁的 10 to 20 inclusive 與固定運費原句 |
| c25 | CONFIRMED | 3990.00 |
| c26 | CONFIRMED | 4100.00 |
| c27 | CONFIRMED | 3937.50 |
| c36 | CONFIRMED（實跑負面輸入） | exit 1、最後一行 ValueError、output_directory_created=false |
| c37 | CONFIRMED | questions-21.txt 與卡片逐字相符；尚未寄出 |
| c38 | CONFIRMED | 差額 50.00、110.00、52.50 |

本輪結果：CHANGED 0、NOT FOUND 0；video.json 不需更動。

待站主確認的兩項：
- description 的 GitHub commit 連結不在今日 sources 內，請發布前手動開一次。
- ZIP 成員清單沒有附全文，所以 description 的教材內容列舉只做到部分佐證。
