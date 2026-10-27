# 事實、原始報價與實作主張：證據 ledger（第9輪查核更新）

## 更新紀錄

- 更新日期：2026-10-26（Asia/Taipei）。
- 本次是第9輪獨立查核，依 payload 中提供的 ledger 證據與官方頁抓取結果核對。
- 結論：c1–c31、c36–c38 在現行 video.json 中的用法全部 CONFIRMED。0 項更改，不修改 video.json。
- c32–c35 仍未定義，沒有被引用，也不補造。

## 證據保存說明

本檔逐字保留以下內容：
- 主張表
- 八頁抽文全文
- 需求、提示詞、request 與詢問草稿全文
- 實跑關鍵欄位

上一版 ledger 中較長的 JSON 原文收據沒有在本檔重抄，包括：
- AI 執行紀錄全文
- verification checks 全文
- 教材 ZIP 重播全文
- 官方來源 JSON

這些收據仍以原檔與 SHA-256 為準，清單見文末。

## 官方頁（2026-10-26 抓取成功）

- **openpyxl**：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html （頁首 openpyxl 3.1.3 documentation）。原句：「openpyxl never evaluates formula」。支持 c15 與描述中「openpyxl 只負責寫檔，不宣稱它會計算公式」。
- **pypdf**：https://pypdf.readthedocs.io/en/stable/user/extract-text.html （頁首 pypdf 6.21.2 documentation）。原句：「pypdf is not OCR software.」，另有「pypdf will also never be able to extract text from images.」。支持 c29 與描述中「這條抽文流程不做掃描影像 OCR」。
- **版本號的區分**：本機實裝版本為 pypdf 6.10.0、openpyxl 3.1.5。上面兩個是官網文件標籤，兩者不可混用。影片沒有唸出任何版本號。

## 主張與證據

| ID | 主張 | 現版 scene | 證據（逐字） | 第9輪 |
| --- | --- | --- | --- | --- |
| c1 | 甲180未稅、乙205含稅、丙175未稅 | opening-unit | aster p1「Unit price: TWD 180.00 excluding tax」；birch p1「Unit price: TWD 205.00 including 5% goods tax」；cedar p1「Unit price: TWD 175.00 excluding tax」 | CONFIRMED |
| c2 | 10張A6、350gsm霧面白卡、雙面全彩、同址、7工作天；比送達總價 | need-start、need-spec、need-delivery | requirements.txt 第7–9行（全文見下） | CONFIRMED |
| c3 | 原檔保留、輸出另存 | need-labels | 命令 --out comparison-output；ledger c3 | CONFIRMED |
| c4 | 全為虛構練習，5%為計算假設 | need-fiction | 各頁「Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.」 | CONFIRMED |
| c5 | 逐頁抽文、Codex AI 判讀、Decimal 計算、openpyxl 寫值 | need-route、extract-start | AI 執行紀錄（provider OpenAI、agent OpenAI Codex agent，model identifier 未揭露）；ledger c5 | CONFIRMED |
| c6 | 甲單價與商品稅在p1，運費200未稅與運費稅5%在p2 | need-proof、extract-start、extract-aster、extract-aster-quote | aster p2「Shipping: TWD 200.00 excluding tax to the specified address」「Shipping tax: 5% of shipping net amount」 | CONFIRMED |
| c7 | 七行 viewer-prompt | extract-core、extract-fields | viewer-prompt.txt 全文（見下） | CONFIRMED |
| c8 | 乙205含稅、免運、5工作天 | extract-birch、extract-review | birch p2「Shipping: TWD 0.00; delivery to the specified address is free」「Lead time: 5 business days」 | CONFIRMED |
| c9 | 丙原版運費未報，值 null | extract-missing-quote、extract-null、extract-review、missing-start、missing-known | cedar p2「Shipping: not quoted」「Shipping tax: not quoted」；comparison original-10 Cedar delivered_total null | CONFIRMED |
| c10 | 單價排序 丙→甲→乙 | cost-start、cost-unit-baseline | baseline unit_price_order Cedar, Aster, Birch | CONFIRMED |
| c11 | 甲10張 1800+90+210=2100 | cost-aster-formula、cost-initial-result | comparison original-10 Aster goods_gross 1890.00、shipping_gross 210.00、delivered_total 2100.00 | CONFIRMED |
| c12 | 乙10張 2050，不二次加稅 | cost-birch-formula、cost-initial-result | birch p1「No second goods tax is added to this inclusive unit price.」；delivered_total 2050.00 | CONFIRMED |
| c13 | 原始10張乙低於甲，丙待確認 | cost-initial-result、missing-start | original-10 lowest_comparable Birch；Cedar comparable false | CONFIRMED |
| c14 | Decimal 計算，不先四捨五入 | cost-rounding、cost-workbook | ledger c14 | CONFIRMED |
| c15 | 試算表為已算值，改需求要重產 | cost-workbook | openpyxl 官網「openpyxl never evaluates formula」；lab-execution「NOT a live formula calculator」 | CONFIRMED |
| c16 | 含稅不重複加稅 | 無現版 scene 引用 | birch p1 同上 | 背景 |
| c17 | 待問清單／詢問草稿，未寄出 | missing-question、missing-no-send | results/questions.txt；ledger c17 | CONFIRMED |
| c18 | 狀態分類是教學規則 | missing-status | 原創教學建議；本次只有丙運費缺漏 | CONFIRMED |
| c19 | 修訂版取代原版，同一家 | revision-start、revision-identity、revision-diff、revision-links | cedar-revised p1「Replaces CED-1026-v1; not an additional supplier.」；p2「Only delivery terms changed; all goods specifications and prices remain.」 | CONFIRMED |
| c20 | 丙修訂10張 1837.50+262.50=2100.00 | revision-diff、revision-total、revision-ranking | revised-10 Cedar goods_gross 1837.50、shipping_gross 262.50、delivered_total 2100.00 | CONFIRMED |
| c21 | 修訂10張乙最低，甲丙同價 | revision-ranking | revised_10_groups [[Birch],[Aster,Cedar]] | CONFIRMED |
| c22 | 來源欄改指修訂版 | revision-links | revised-10 Cedar price_source「cedar-revised.pdf p.1」、shipping_source「cedar-revised.pdf p.2」 | CONFIRMED |
| c23 | request-20.json quantity 20 驅動修訂情境 | quantity-start、quantity-edit、quantity-prompt、quantity-run、quantity-output | request-20.json 全文；selected_result request {scenario revised, quantity 20} | CONFIRMED |
| c24 | 三家10–20適用；甲200、丙250範圍內固定；乙免運 | quantity-ranges | 各 p2「Quantity range: 10 to 20 pieces inclusive」；aster「Shipping remains TWD 200.00 net for 10 to 20 pieces.」；cedar-revised「Shipping remains TWD 250.00 net for 10 to 20 pieces.」 | CONFIRMED |
| c25 | 甲20張 3990 | quantity-aster、quantity-ranking | selected_result Aster goods_gross 3780.00、shipping_gross 210.00、delivered_total 3990.00 | CONFIRMED |
| c26 | 乙20張 4100 | quantity-birch、quantity-ranking | selected_result Birch 4100.00 | CONFIRMED |
| c27 | 丙修訂20張 3937.50，最低 | quantity-cedar、quantity-ranking | selected_result Cedar goods_gross 3675.00、shipping_gross 262.50、delivered_total 3937.50、lowest_comparable true | CONFIRMED |
| c28 | XLSX／CSV／questions／change-log 實際輸出 | 無現版 scene 引用 | output_files 清單 | 背景 |
| c29 | pypdf 不做 OCR | 無現版 scene 引用（描述有用到） | pypdf 官網「pypdf is not OCR software.」 | CONFIRMED（描述） |
| c30 | 表格／多欄語義可能失去 | 無現版 scene 引用 | pypdf 官網「Missing Semantic Layer」 | 背景 |
| c31 | 相對命令在 materials 實跑，exit 0，20張3列 | quantity-run、quantity-output | cwd …/repro-package/materials；argv 與 code 卡逐字相同；exit_code 0；stdout winners revised-20 Cedar | CONFIRMED |
| c32–c35 | 未定義 | 無 | — | 不補造 |
| c36 | 21張被拒，exit 1，未建立 comparison-21 | range21-request、range21-run、range21-result | quantity-21-relative-execution.json：executed_at 2026-10-26T09:16:45Z、exit_code 1、最後一行「ValueError: Quantity outside explicitly quoted range」、output_directory_created false | CONFIRMED |
| c37 | 21張重報詢問草稿 | range21-question | questions-21.txt「想改成21張，請重報同規格的單價、運費和交期。」 | CONFIRMED |
| c38 | 修訂10張丙比乙多50.00；20張乙比甲多110.00；丙比甲少52.50 | revision-ranking、quantity-birch、quantity-cedar | Decimal 差額紀錄：cedar_minus_birch 50.00、birch_minus_aster 110.00、aster_minus_cedar 52.50（輸入 lab-comparison.json，SHA-256 c392e116…） | CONFIRMED |

## 第9輪待人工確認（未更動）

- 描述中的 GitHub 教材連結（commit 7132d533a9649aebbf3733e58a93bbe68bdddffa）不在 sources 內，發布前需要人工點開確認。
- quantity-prompt 的對話文字是建議觀眾用的寫法，不是實跑時的輸入。實跑時 AI 讀的是 request-20.json。
- 旁白說「改數量設定檔」，畫面顯示 request-20.json，教材另有 request.json（quantity 10）。兩者對應關係需要和教材 README 保持一致。

## 八頁抽文全文（pypdf 實際輸出，逐字）

### aster.pdf 第1頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
ASTER PRINT / PRICE SHEET
aster.pdf    |    Page 1 of 2
Quote AST-1026 / Original / 2026-10-26
Currency: TWD
Item: A6 postcard (105 x 148 mm)
Paper: 350 gsm matte white card
Print: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 180.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,800.00
The delivered total also includes page 2 terms.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Aster / original / fictional exercise only
1 / 2
```

### aster.pdf 第2頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
ASTER / DELIVERY AND SCOPE
aster.pdf    |    Page 2 of 2
Quote AST-1026 / Terms belonging to page 1
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 180.00 excluding tax throughout this range.
Shipping: TWD 200.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 200.00 net for 10 to 20 pieces.
Lead time: 7 business days
Payment: one payment after acceptance
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Aster / original / fictional exercise only
2 / 2
```

### birch.pdf 第1頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
BIRCH / SIMPLE ALL-IN OFFER
birch.pdf    |    Page 1 of 2
Offer BIR-20261026 / Original / 2026-10-26
For: one A6 postcard design, printed identically
Size: A6 postcard (105 x 148 mm)
Stock: 350 gsm matte white card
Printing: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Currency: TWD
Unit price: TWD 205.00 including 5% goods tax
No second goods tax is added to this inclusive unit price.
Read page 2 for shipping and quantity range.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Birch / original / fictional exercise only
1 / 2
```

### birch.pdf 第2頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
BIRCH / INCLUDED IN YOUR OFFER
birch.pdf    |    Page 2 of 2
Offer BIR-20261026 / Included terms
Quantity range: 10 to 20 pieces inclusive
The TWD 205.00 tax-inclusive unit price stays the same in this range.
Shipping: TWD 0.00; delivery to the specified address is free
Shipping tax: TWD 0.00; no separate shipping charge or shipping tax
Shipping tax mode: inclusive; shipping tax rate: 0%
Lead time: 5 business days
Payment: one payment after acceptance
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Birch / original / fictional exercise only
2 / 2
```

### cedar.pdf 第1頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR PRINT / GOODS QUOTATION
cedar.pdf    |    Page 1 of 2
Quotation CED-1026-v1 / Original / 2026-10-26
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
This is a goods quotation; see page 2 before comparing delivery.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / original / fictional exercise only
1 / 2
```

### cedar.pdf 第2頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR / TERMS REQUIRING CLARIFICATION
cedar.pdf    |    Page 2 of 2
Quotation CED-1026-v1 / Original delivery terms
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 175.00 excluding tax throughout this range.
Shipping: not quoted
Shipping tax: not quoted
Lead time: 7 business days
Payment: one payment after acceptance
Do not assume shipping is free; ask for a written delivery quote.
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / original / fictional exercise only
2 / 2
```

### cedar-revised.pdf 第1頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR PRINT / REVISED QUOTATION
cedar-revised.pdf    |    Page 1 of 2
Quotation CED-1026-v2 / Revised / 2026-10-26
Replaces CED-1026-v1; not an additional supplier.
Currency: TWD
Product: A6 postcard (105 x 148 mm)
Material: 350 gsm matte white card
Print specification: double-sided full colour; one identical artwork
Quoted quantity: 10 pieces
Unit price: TWD 175.00 excluding tax
Goods tax: 5% of goods net amount
Goods net amount at 10 pieces: TWD 1,750.00
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / revised / fictional exercise only
1 / 2
```

### cedar-revised.pdf 第2頁

```text
MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT
CEDAR / WRITTEN DELIVERY CLARIFICATION
cedar-revised.pdf    |    Page 2 of 2
Quotation CED-1026-v2 / Revised delivery terms
Quantity range: 10 to 20 pieces inclusive
Unit price stays TWD 175.00 excluding tax throughout this range.
Shipping: TWD 250.00 excluding tax to the specified address
Shipping tax: 5% of shipping net amount
Shipping remains TWD 250.00 net for 10 to 20 pieces.
Lead time: 7 business days
Payment: one payment after acceptance
Only delivery terms changed; all goods specifications and prices remain.
Valid for this fictional exercise through 2026-11-30.
Fictional training quote. The 5% rates are exercise assumptions, not tax advice or a real offer.
Cedar / revised / fictional exercise only
2 / 2
```

## 需求、提示詞、request 與詢問草稿全文

### materials/requirements.txt

SHA-256 c3c38e75c01b15a10b8fe8540e367fad8eeebbf0a0dcc7f8fcd4d00100759fa3

```text
練習案例：比較三家虛構供應商的明信片印刷報價

本教材完全原創，所有供應商與交易條件均屬虛構。
金額單位為練習用新臺幣 TWD。5% 是本練習指定的計算假設，
不是對任何真實交易稅法、稅率或會計處理的判斷。

原始需求：10 張 A6 明信片（105 × 148 mm），350 gsm 霧面白卡紙，
雙面全彩，所有稿件相同；送到同一個指定地址，7 個工作天內交貨。
比的是符合需求、送達且含明示稅額的總價，不是單價。
規格或費用沒寫就列待確認，不能把缺漏視為 0，也不能自行補稅。

後續練習一：Cedar 補寄 cedar-revised.pdf。保留原檔，使用修訂版替代
Cedar 原報價重做 10 張比較，列出改了哪些欄位。
後續練習二：數量改成 20 張，其餘條件相同。先確認各報價的數量
適用範圍與運費，再重算；不可假設原來的最低總價仍然最低。

所有來源 PDF 都是可選取文字的 PDF。本流程不示範掃描影像 OCR。
原件只讀；輸出放另一個資料夾。重要欄位都保留檔名和頁碼。
```

### materials/viewer-prompt.txt

SHA-256 6b491f229d7f5e12f53c2f56de3c812614f4ec7ac96e9042127aa45bb6d3a5c4

```text
請比較 requirements.txt 與三家報價的逐頁原文。
先列規格、適用數量、幣別、單價、稅、運費、交期。
每個欄位附檔名、頁碼及支持它的原句。
沒寫的填待確認，不能當作零或自行補價格。
Cedar 修訂版取代原版參與比價，原檔保留。
確認規格和數量可比，再按已知稅與運費計算總價。
交付可編輯比價表、待問問題及修訂前後差異。
```

### request 檔

三個 request 檔都只有 4 行：`{`、scenario 行、quantity 行、`}`。scenario 皆為 revised，差別只在 quantity：

| 檔名 | quantity | SHA-256 |
| --- | --- | --- |
| materials/request.json | 10 | 7c1d5d568212a5c6e31042f1e7f8fc542950956814ce044b1f3a05868e8a9b30 |
| materials/request-20.json | 20 | 53f882946086d999e5ccbcf14755a176a92907e2c984920c2f3653c10be8eb62 |
| materials/request-21-invalid.json | 21 | 0f3f6f5c96284192bfc545f951e9c24f68b3867837f05ec8efa67f213fb99b4e |

### materials/questions-21.txt

SHA-256 dbbc86c25a90002c3538dd34d58eb3da14a86f273f5bce2e55a53da9137d26fe

```text
想改成21張，請重報同規格的單價、運費和交期。
```

### materials/analysis-prompt.txt

SHA-256 dc159f0d4ad8713e3c7d28cc9a43df823ec20fe2bd25687105f1001c7d29921f，2387 bytes。全文保存在上一版 ledger 與原檔，本檔不重抄。

## 實跑關鍵欄位

### 20張相對命令（research/lab-relative-command-execution.json）

- **cwd**：/workspace/work/ai-pdf-01/repro-package/materials
- **argv**：python3 build_comparison.py --analysis ../research/lab-ai-extraction.json --extracted ../research/lab-extracted-pages.json --request request-20.json --out comparison-output
- **結果**：exit_code 0；stderr 為空。
- **stdout 摘要**：checks 17，all_passed true，winners 為 original-10 Birch、revised-10 Birch、revised-20 Cedar。
- **selected_result**：Aster 3990.00、Birch 4100.00、Cedar（cedar-revised.pdf）3937.50 lowest。
- **selected-comparison.json**：SHA-256 aafb2cefc8d163c2631ec55d7d60d95ad3fa195457781a255ddf17d940064a64。

### 21張（research/quantity-21-relative-execution.json）

- **檔案 SHA-256**：67baa2c706b7a4c77992a6880e7ac9f038465760a8fe6bdc78305e4a86bb5fec
- **執行時間**：2026-10-26T09:16:45Z
- **argv**：同上，但 --request request-21-invalid.json --out comparison-21
- **結果**：exit_code 1；stdout 為空。
- **stderr 最後一行**：ValueError: Quantity outside explicitly quoted range
- **output_directory_created**：false

### 教材 ZIP 重播（research/lab-materials-archive-replay-20261026.json）

- 檔案 SHA-256：2a11ffbba4f022c2daa39a339cd97a2e9b56b3b9a442d6c0bd46d6824a8bda0b
- 執行時間：2026-10-26T09:24:56Z
- 20張命令 exit 0，總價與上相同；21張命令 exit 1，未建立資料夾。

## 未重抄收據的 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| research/lab-comparison.json | c392e1162b791ecedc82a2bcb9ca2dd41ea73a71d424c50755828c242f3d25ab |
| research/lab-baseline-and-normalized-order.json | 9de1c612ae82e3c4dbdf00abe1aaf2c509a7925cb2e00eecf888f629588eaa2c |
| research/lab-verification-request-20.json | 580591e663d330e16e07d28a9f98ee4dee720f8093f46fb90d2c83d1e8b1b4c9 |
| research/lab-ai-extraction.json | f86e3a0eef16325197aa2c1409b125ec91a792d15b1e195522d77da4630d07b8 |
| research/lab-extracted-pages.json | 586eb5f78b158217cdb63e9625124034c0f45e4be9491a80efbc5b2518f6158c |
| build_comparison.py | 35103b82d83b527b897bbc171e8d71e40431ebc0c4412a9c3ce62b898b160ea1 |
| 原始完整 ledger（git a2c088e49e93f1a6c0ccea8730a23da43bde74ee） | 91e1de197b7f157603dc989dd8ff56a195599469cc71211c6802c9c75bec3e3f |

上一版（第8輪後）ledger 的完整內容，仍以該版檔案為準。
