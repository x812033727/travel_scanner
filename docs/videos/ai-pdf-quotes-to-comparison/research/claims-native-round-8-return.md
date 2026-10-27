# 事實、原始報價與實作主張：完整證據 ledger

更新日期：2026-10-26（Asia/Taipei）。第8輪獨立查核結果附於文末；c1–c37 的原有證據列一律未改。

本片只教同一件事：把三家原創虛構報價整理成有逐欄來源、能依共同需求比較的表，依修訂版、數量20及超出範圍的21張追蹤結果。供應商、交易條件及5%稅率皆為明示練習假設，不對應真實採購或稅法判斷。

原有的完整 ledger 內容（復原來源、c1–c37 表格、八頁抽文、需求與提示詞全文、計算結果、實跑收據）保持原樣，請勿以本段取代；本輪只在文末追加查核紀錄。

## 第8輪獨立查核（2026-10-26）

查核者為新工作階段的獨立查核者，沒有看過先前任何查核。

### 結果

- c1–c27、c31、c36、c37：現版引用的每個數字、頁碼、引句、檔名行號都逐一對照本 ledger 內的逐字證據，全部 CONFIRMED。逐字證據包括：八頁 pypdf 抽文、requirements.txt、viewer-prompt.txt、request-20.json、request-21-invalid.json、questions-21.txt、comparison.json、selected_result、quantity-21 receipt。
- 工具行為以今日抓取的官方頁核對：
  - https://pypdf.readthedocs.io/en/stable/user/extract-text.html（今日 200，頁標 pypdf 6.21.2）：「pypdf is not OCR software」支持描述中的「不做掃描影像 OCR」。
  - https://openpyxl.readthedocs.io/en/stable/simple_formulae.html（今日 200，頁標 openpyxl 3.1.3）：「openpyxl never evaluates formula」支持 c15 與描述中的「只負責寫檔」。
- CHANGED 0、NOT FOUND 0；video.json 未修改。

### 重點逐字核對

- requirements.txt 行號：第7行「原始需求…」、第8行「雙面全彩…」、第9行「比的是…」，與 need-spec（第7–8行）、need-delivery（第8–9行）相符。
- 引句與原頁逐字一致：
  - aster.pdf p2「Shipping: TWD 200.00 excluding tax to the specified address」
  - cedar.pdf p2「Shipping: not quoted」
  - cedar-revised.pdf p1「Replaces CED-1026-v1; not an additional supplier.」
- 算式核對：
  - 10張：甲 1800+90+210=2100；乙 2050；丙修訂 1837.50+262.50=2100.00。
  - 20張：甲 3990；乙 4100；丙修訂 3937.50。
  - 以上均與 comparison.json 相符。
- 實跑證據：
  - 20張命令：exit 0；selected_result 為數量20、修訂情境、3列。
  - 21張命令：exit 1，stderr 末行「ValueError: Quantity outside explicitly quoted range」，output_directory_created=false。

### 到期與待追蹤

- 練習報價有效期至 2026-11-30（虛構教材）。
- 官方頁版本標籤會隨 stable 更新；片中未引用版本號。
- sources 中兩筆 404 是網址誤接全形註記所致；正確網址已成功抓取。
