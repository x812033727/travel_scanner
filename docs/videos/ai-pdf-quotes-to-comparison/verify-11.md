# verify-11.md：ai-pdf-quotes-to-comparison 第11輪獨立事實查核

查核日：2026-10-26。輸入：payload 內 video.json（56 scenes）、claims ledger 與 sources。本片的金額、稅率、張數、檔名、頁碼與命令，都來自原創虛構練習 PDF 與本地實跑收據。ledger 逐字附上八頁 pypdf 抽文全文、requirements.txt、viewer-prompt.txt、request-*.json、questions-21.txt、comparison.json、selected_result，以及 12／13／20／21 張的實跑 argv、exit code、stdout 與 stderr。我逐項核對了原句，並用 Decimal 心算覆核所有算式。官方頁 openpyxl、pypdf 均已讀到（status 200），只用來支持功能說明。本片沒有在畫面或旁白中說出任何產品版本號、價格或限制。

| # | claim | where | URL | verdict | before → after |
|---|---|---|---|---|---|
| 1 | 甲180未稅、乙205含稅、丙175未稅 | opening-unit rows; cost-unit-baseline; xnrg | aster/birch/cedar.pdf p1 抽文（ledger） | CONFIRMED | — |
| 2 | requirements.txt 第7–8行、8–9行逐字節錄 | need-spec, need-delivery code/caption | materials/requirements.txt 全文（ledger） | CONFIRMED（第7行「原始需求」、第8行「雙面全彩」、第9行「比的是」，行號正確） | — |
| 3 | 三家原檔 aster/birch/cedar.pdf，原件只讀、輸出另存 | need-labels; d78a | requirements.txt 第21行；lab receipts | CONFIRMED | — |
| 4 | 供應商、條件與5%稅率為虛構練習 | need-fiction; fvzv; 3742; description | requirements.txt 第3–5行；各頁 Fictional training quote 註記 | CONFIRMED | — |
| 5 | 流程：文字 PDF 抽文 → AI 讀逐頁原文 → 精確小數計算 | need-route; 3639; description | lab-ai-analysis-execution.json；https://pypdf.readthedocs.io/en/stable/user/extract-text.html | CONFIRMED | — |
| 6 | 甲的單價在第1頁，送貨條件在第2頁 | m57n; need-proof | aster.pdf p1/p2 | CONFIRMED | — |
| 7 | viewer-prompt 第1–7行全文 | extract-core code/caption | materials/viewer-prompt.txt | CONFIRMED（七行逐字相符） | — |
| 8 | 甲：180未稅 p1、商品稅5% p1、運費200未稅 p2 | extract-aster rows | aster.pdf p1–2 | CONFIRMED | — |
| 9 | 原句「Shipping: TWD 200.00 excluding tax to the specified address」 | extract-aster-quote | aster.pdf p2 | CONFIRMED（逐字） | — |
| 10 | 乙：205含稅 p1、運費0送達免運 p2、交期5工作天 p2 | extract-birch; q7x8 | birch.pdf p1–2 | CONFIRMED | — |
| 11 | 原句「Shipping: not quoted」位於丙第2頁 | extract-missing-quote; extract-null page 2; 7hi8 | cedar.pdf p2 | CONFIRMED | — |
| 12 | 只按單價排序為丙→甲→乙 | cost-unit-baseline; 35fs | lab-baseline-and-normalized-order.json | CONFIRMED | — |
| 13 | 甲10張：1,800＋90＋210＝2,100 | cost-aster-formula | aster.pdf；comparison.json original-10 | CONFIRMED | — |
| 14 | 乙10張：10×205＝2,050，運費0，不重複加商品稅 | cost-birch-formula | birch.pdf p1「No second goods tax…」 | CONFIRMED | — |
| 15 | 十張原始：甲2,100、乙2,050、丙待確認；乙比甲便宜 | cost-initial-result; bcr5; tnrc | comparison.json original-10 | CONFIRMED | — |
| 16 | 丙商品（1,837.50）比乙（2,050）便宜，運費不夠高就會翻轉名次 | e86a | comparison.json goods_gross | CONFIRMED（臨界值為含稅運費212.50，屬條件式敘述） | — |
| 17 | 試算表寫入的是已算值，不會自己重算；openpyxl 不計算公式 | cost-workbook; ehby; description | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html「openpyxl never evaluates formula」；lab-execution xlsx 說明 | CONFIRMED | — |
| 18 | 丙已知：175未稅、商品稅5%、數量10–20；未知：運費、含稅狀態、稅額 | missing-known; j2ja | cedar.pdf p1–2 | CONFIRMED | — |
| 19 | 給丙的詢問是草稿、尚未寄出 | missing-question; missing-no-send | ledger c17 | CONFIRMED（未宣稱已寄出或已回覆） | — |
| 20 | 狀態欄分類（條件完整／費用缺漏／規格不同） | missing-status | ledger c18（教學建議） | CONFIRMED（條件式教學規則，未說本次真有規格不同的報價） | — |
| 21 | 原句「Replaces CED-1026-v1; not an additional supplier.」 | revision-identity | cedar-revised.pdf p1 | CONFIRMED | — |
| 22 | 修訂版：運費250未稅、運費稅5%，商品單價175未稅不變 | revision-diff; hiqk | cedar-revised.pdf p1–2「Only delivery terms changed」 | CONFIRMED | — |
| 23 | 丙修訂10張：1,837.50＋262.50＝2,100.00，與甲相同 | revision-total; ambg | comparison.json revised-10 | CONFIRMED | — |
| 24 | 補件後10張：乙2,050最低；甲、丙皆2,100；丙比乙多50 | revision-ranking; dyun | comparison.json；revised-ten-price-difference.json | CONFIRMED | — |
| 25 | request-20.json 第1–4行全文 | quantity-edit | materials/request-20.json | CONFIRMED | — |
| 26 | 20張命令（cwd 為 materials）實跑 exit 0 | quantity-run code/caption「實跑 2026-10-26」 | lab-relative-command-execution.json | CONFIRMED（argv 逐字相符） | — |
| 27 | 輸出：數量20、修訂情境、三家各一列 | quantity-output | selected_result | CONFIRMED | — |
| 28 | 三家單價皆適用10–20張；甲200未稅、丙250未稅運費在範圍內固定；乙指定地址免運 | quantity-ranges; sxtz; rgr9 | 三家 p2 原文 | CONFIRMED | — |
| 29 | 甲20張：3,780＋210＝3,990 | quantity-aster | revised-20 | CONFIRMED | — |
| 30 | 乙20張4,100，比甲多110，名次與十張時相反 | quantity-birch; m8sb | revised-20；revised-twenty-price-difference.json | CONFIRMED | — |
| 31 | 丙20張：3,675＋262.50＝3,937.50，比甲少52.50 | quantity-cedar; gy4i | revised-20；cedar-gap.json | CONFIRMED | — |
| 32 | 20張排名：丙3,937.50、甲3,990、乙4,100 | quantity-ranking; cbe9 | revised-20 | CONFIRMED | — |
| 33 | request-12／13.json 全文 | threshold-request12/13 | ledger c39 | CONFIRMED | — |
| 34 | 12／13張兩條命令實跑 exit 0，輸出分存兩個資料夾 | threshold-run12/13 | quantity-threshold actual_runs | CONFIRMED | — |
| 35 | 12張：甲2,478、乙2,460、丙2,467.50，乙最低；13張：甲2,667、乙2,665、丙2,651.25，丙最低 | threshold-results | selected_result ×2；我另行 Decimal 覆核 | CONFIRMED | — |
| 36 | 12張時乙比丙少7.50；13張時丙領先13.75 | 6nxr; 7jrk | margin_calculation | CONFIRMED（13.75為丙對次低者乙的差距） | — |
| 37 | 丙−乙：+7.50 → −13.75；每多一張 205.00−183.75＝21.25 | threshold-margin; e5gd; petb | additional_actual_decimal_derivation | CONFIRMED | — |
| 38 | request-21-invalid.json 全文；命令只換需求檔與輸出資料夾 | range21-request/run | quantity-21-relative-execution.json | CONFIRMED | — |
| 39 | 實跑錯誤「ValueError: Quantity outside explicitly quoted range」，沒有建立輸出資料夾 | range21-result; 9jiq; egmv | 同上：exit 1、output_directory_created false | CONFIRMED | — |
| 40 | 詢問草稿「想改成21張，請重報同規格的單價、運費和交期。」 | range21-question | materials/questions-21.txt | CONFIRMED（逐字；標示尚未寄出） | — |
| 41 | 本次 PDF 可選取文字；此抽文流程不做 OCR | description | pypdf 官方「pypdf is not OCR software」；requirements.txt 第20行 | CONFIRMED | — |
| 42 | AI 分析也讀取 analysis-prompt.txt 的 JSON 契約 | description | ai-analysis-execution inputs #2 | CONFIRMED | — |
| 43 | 素材說明「十張實算 A2100／B2050／C未知」 | assets.source | comparison.json original-10 | CONFIRMED | — |
| 44 | 標題、縮圖、標籤 | youtube.title; thumbnail; tags | — | OUT OF SCOPE（屬風格；沒有可查核的數字） | — |
| 45 | 開場鉤子與設問句（6vwc、hg9m、ajsk、kv5r、indq、c49q、pruf） | opening*; 各 big 卡 | — | OUT OF SCOPE（後續均有對應答案，答案已在上列核對） | — |

## 計數
CONFIRMED 43；CHANGED 0；NOT FOUND 0；OUT OF SCOPE 2。changed_facts＝0，video.json 不需要修改。

## 規則檢查
- 「以官網為準」整個家族的用語：旁白與描述中都沒有出現。
- 查證用語（經查證、根據官方文件、截至查證、本影片）：旁白中沒有出現。
- 個人資料：沒有。
- 金融、稅務建議：沒有。描述與旁白都明說5%只是練習假設。
- 示範宣稱（教學卡片路線）：凡標「實跑」的卡片（quantity-run、quantity-output、threshold-run12/13、range21-result）都有 argv、exit code、stdout 或 stderr 收據支撐。qrv8「打開試算表…核對」是給觀眾的操作指示，沒有宣稱已在試算表介面中實際操作或看到結果。

## 即將過期的事實
- 三家練習報價都寫「Valid for this fictional exercise through 2026-11-30」。這是虛構有效期，畫面沒有引用，但 2026-11-30 之後若改說「目前有效」就要重查。
- 官方文件頁首的版本號（pypdf 6.21.2、openpyxl 3.1.3）會隨 stable 版更新。本片沒有說出版本號，所以不受影響。

## 意見與站主觀點
沒有發現未標記為站主的意見。旁白中的勸告（例如「別讓報價替你決定」「別自己編一個升級價」）都是操作建議，與站主觀點第1、3、4、6、7點一致：先算清實際成本、回到原文核對、只報本次真正執行的結果。

## 懷疑但未修改
- 7jrk「丙就領先十三元七角五分」：數字是對乙（次低者）的差距；丙對甲的差距是15.75。語意正確，所以未改。
- e86a「只要運費不夠高，名次就會翻過來」：這是條件式說法，臨界值為含稅運費212.50。未改。
- 描述只寫到「從十張改成二十張」，沒有提到12／13／21張的段落。這是內容完整度問題，不是事實錯誤，未改。
- comparison.xlsx 在 lab 執行與 ZIP 重播中的 SHA 不同（13524／13525 bytes）。重播 JSON 自己說明是不同次輸出。畫面沒有引用這個雜湊，所以只記錄、未改。
