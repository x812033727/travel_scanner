# verify-10.md｜ai-pdf-quotes-to-comparison 獨立事實查核（第10輪）

查核日：2026-10-26。查核對象：payload 內 video.json，共55 scenes／93 lines，與 ledger 末段所記相符。

證據來源分三類：
- claims ledger 內逐字附上的八頁 pypdf 抽文。
- 教材全文：requirements.txt、viewer-prompt.txt、request-20.json、request-21-invalid.json、questions-21.txt、analysis-prompt.txt。
- 實跑收據：lab-comparison.json、selected_result、quantity-21-relative-execution.json、archive replay。

今日官方頁抓取：pypdf extract-text 與 openpyxl simple_formulae 兩頁皆為 status 200，沒有失敗抓取。

本片所有金額、稅率、張數與交期都是原創虛構練習的數字，以練習原文與實跑紀錄核對；不涉及任何需要「官網 YYYY-MM-DD」標示的產品數字。

本片屬「製作路線：教學卡片」，每一個示範都已對照輸入、動作與實跑證據。

## 逐項查核

| # | claim | where | URL／證據 | verdict | before → after |
|---|---|---|---|---|---|
| 1 | 三家原報單價：甲180未稅、乙205含稅、丙175未稅 | opening-unit 表格；cost-unit-baseline；xnrg | aster.pdf p1「Unit price: TWD 180.00 excluding tax」；birch.pdf p1「TWD 205.00 including 5% goods tax」；cedar.pdf p1「TWD 175.00 excluding tax」 | CONFIRMED | — |
| 2 | 需求節錄是 requirements.txt 第7–8行、第8–9行，且逐字相符 | need-spec、need-delivery code | requirements.txt 全文：第7行「原始需求：10 張 A6…」，第8行「雙面全彩…」，第9行「比的是…」 | CONFIRMED | — |
| 3 | 十張、同一地址、7個工作天 | need-start ddpd；need-spec；need-delivery | requirements.txt 第7–8行 | CONFIRMED | — |
| 4 | 原檔名為 aster／birch／cedar.pdf，原件保留、輸出另存 | need-labels | 八頁抽文的檔名；requirements.txt 末行「原件只讀；輸出放另一個資料夾」 | CONFIRMED | — |
| 5 | 供應商、條件與5%稅率皆為虛構練習 | need-fiction；description | 每頁「Fictional training quote. The 5% rates are exercise assumptions…」；requirements.txt 第3–5行 | CONFIRMED | — |
| 6 | 分工為：文字 PDF 抽文 → AI 讀逐頁原文 → 精確小數計算 | need-route 表格；3639 | lab-ai-analysis-execution.json 的 scope_executed；Decimal 計算；generation receipt | CONFIRMED | — |
| 7 | 甲的單價在第1頁，運費在第2頁 | need-proof m57n；extract-aster；fd27 | aster.pdf p1 單價與商品稅；p2「Shipping: TWD 200.00 excluding tax…」「Shipping tax: 5%…」 | CONFIRMED | — |
| 8 | AI 收到需求與每份報價的兩頁文字 | extract-start nxct | 分析執行紀錄的 inputs：requirements、analysis-prompt、extracted-pages（八頁） | CONFIRMED | — |
| 9 | 七行提示詞為 viewer-prompt.txt 第1–7行全文 | extract-core code | viewer-prompt.txt 全文逐字相符 | CONFIRMED | — |
| 10 | 甲：單價180未稅（p1）、商品稅5%（p1）、運費200未稅（p2） | extract-aster 表格 | aster.pdf p1–p2 | CONFIRMED | — |
| 11 | 引句「Shipping: TWD 200.00 excluding tax to the specified address」 | extract-aster-quote | aster.pdf p2 逐字 | CONFIRMED | — |
| 12 | 乙：205含稅（p1）、運費0送達免運（p2）、交期5個工作天（p2） | extract-birch；mdte；q7x8 | birch.pdf p1–p2：「Shipping: TWD 0.00; delivery to the specified address is free」「Lead time: 5 business days」 | CONFIRMED | — |
| 13 | 引句「Shipping: not quoted」出自丙第2頁 | extract-missing-quote；7hi8 | cedar.pdf p2 逐字 | CONFIRMED | — |
| 14 | 空值示意 value null／page 2／evidence | extract-null code | analysis-prompt.txt 的 JSON 契約形狀；c9 normalized 值為 null | CONFIRMED（卡片標為示意） | — |
| 15 | 單價排序為丙→甲→乙 | cost-start 35fs；cost-unit-baseline | lab-baseline-and-normalized-order.json 的 unit_price_order | CONFIRMED | — |
| 16 | 甲十張：1,800＋90＋210＝2,100 | cost-aster-formula | lab-comparison.json original-10 Aster：goods_gross 1890.00、shipping_gross 210.00、delivered_total 2100.00 | CONFIRMED | — |
| 17 | 乙十張：10×205＝2,050，免運，不再加商品稅 | cost-birch-formula | birch.pdf p1「No second goods tax…」；lab-comparison.json 2050.00 | CONFIRMED | — |
| 18 | 十張原始結果：甲2,100.00、乙2,050.00、丙待確認；乙比甲便宜 | cost-initial-result；bcr5；tnrc | lab-comparison.json original-10，Cedar delivered_total 為 null | CONFIRMED | — |
| 19 | 丙的商品比乙便宜 | missing-start e86a | 丙 goods_gross 1837.50，乙 2050.00 | CONFIRMED | — |
| 20 | 丙已知 175未稅、5%、10–20；未知為運費、是否含稅、稅率或稅額 | missing-known | cedar.pdf p1–p2：「Shipping: not quoted」「Shipping tax: not quoted」「Quantity range: 10 to 20…」 | CONFIRMED | — |
| 21 | 詢問草稿未寄出，由下單者確認 | missing-question；missing-no-send | ledger c17：草稿未寄、沒有回覆 | CONFIRMED（草稿性質） | — |
| 22 | 「規格不同」一列是條件式使用規則 | missing-status | ledger c18：原創教學建議；本次三家規格相同 | CONFIRMED（未說成本次實例） | — |
| 23 | 修訂單引句「Replaces CED-1026-v1; not an additional supplier.」 | revision-identity | cedar-revised.pdf p1 逐字 | CONFIRMED | — |
| 24 | 修訂差異：運費由待確認變250未稅、運費稅變5%、單價175未稅不變 | revision-diff；hiqk | cedar-revised.pdf p2：「Shipping: TWD 250.00 excluding tax…」「Only delivery terms changed…」 | CONFIRMED | — |
| 25 | 丙修訂十張：1,837.50＋262.50＝2,100.00，與甲同價 | revision-total；ambg | lab-comparison.json revised-10 Cedar | CONFIRMED | — |
| 26 | 修訂後十張：乙2,050.00最低，丙比乙多50.00 | revision-ranking；dyun；loop | revised-ten-price-difference.json：cedar_minus_birch 為 50.00 | CONFIRMED | — |
| 27 | request-20.json 第1–4行全文：scenario revised、quantity 20 | quantity-edit | materials/request-20.json 全文 | CONFIRMED | — |
| 28 | 實跑命令（5行續行）與輸出資料夾 comparison-output | quantity-run code、caption「實跑 2026-10-26」 | lab-relative-command-execution.json：argv 逐字相同、exit 0、cwd 為 materials | CONFIRMED（有實跑證據） | — |
| 29 | 輸出：數量20、修訂版、甲乙丙修訂版三列 | quantity-output | selected_result 的 request {revised, 20}，rows 為 Aster、Birch、Cedar（cedar-revised.pdf） | CONFIRMED（有實跑證據） | — |
| 30 | 三家單價皆適用10–20張；甲200、丙250運費在範圍內固定；乙指定地址免運 | quantity-ranges；sxtz；rgr9 | aster p2、birch p2、cedar-revised p2 原文 | CONFIRMED | — |
| 31 | 甲二十張：3,780＋210＝3,990 | quantity-aster | revised-20 Aster 3990.00 | CONFIRMED | — |
| 32 | 乙二十張4,100，比甲多110.00，先後順序反轉 | quantity-birch；m8sb | revised-twenty-price-difference.json：110.00；十張時乙低於甲 | CONFIRMED | — |
| 33 | 丙修訂二十張：3,675＋262.50＝3,937.50，比甲少52.50 | quantity-cedar；gy4i | revised-twenty-cedar-gap.json：52.50 | CONFIRMED | — |
| 34 | 二十張排名：丙3,937.50、甲3,990.00、乙4,100.00 | quantity-ranking；cbe9；loop | revised_20_order 為 Cedar、Aster、Birch | CONFIRMED | — |
| 35 | request-21-invalid.json 全文 | range21-request | materials/request-21-invalid.json 全文 | CONFIRMED | — |
| 36 | 21張命令：只換 request 與 --out | range21-run | quantity-21-relative-execution.json 的 command 逐字相同 | CONFIRMED（有實跑證據） | — |
| 37 | 錯誤句「ValueError: Quantity outside explicitly quoted range」，且沒有建立結果資料夾 | range21-result；9jiq；egmv | 同上收據：exit 1、displayed_exact_last_line、output_directory_created=false | CONFIRMED（實際觀察到的失敗，不是預期值） | — |
| 38 | 21張詢問草稿文字 | range21-question | questions-21.txt 逐字相符；尚未寄出 | CONFIRMED | — |
| 39 | 試算表存的是值而非會自動重算的公式；需求一改要重產 | cost-workbook ehby；description | 官方 openpyxl 頁（今日 200）「openpyxl never evaluates formula」；lab xlsx 說明為 NOT a live formula calculator | CONFIRMED | — |
| 40 | 本流程只處理可選取文字的 PDF，不做掃描 OCR | description | 官方 pypdf 頁（今日 200）「pypdf is not OCR software」；requirements.txt 末段 | CONFIRMED | — |
| 41 | 本次 AI 分析也讀了 analysis-prompt.txt 契約 | description | analysis execution inputs 第2項 | CONFIRMED | — |
| 42 | 標題、縮圖（先算總價／稅與運費別漏算）、tags | youtube、thumbnail | 與片中結論一致，沒有額外數字 | CONFIRMED | — |
| 43 | 開場與 outro 問句、CTA | opening；outro | — | OUT OF SCOPE | — |

## 計數

- CONFIRMED：42
- CHANGED：0
- NOT FOUND：0
- OUT OF SCOPE：1
- changed_facts：0

## 規則檢查

- 敘述中沒有「以官網為準」，也沒有其他免責句家族用語。
- 沒有「經查證／根據官方文件／截至查證／本影片」。
- 沒有個人資料。
- 沒有財務、稅務或法律建議：5%在片中明示為練習假設。
- 本片不需要產品數字卡片的「官網」來源標示，因為卡片引用的都是虛構練習原文。

## 即將到期的事實

- 練習報價寫有「Valid for this fictional exercise through 2026-11-30」。片中沒有說出這個日期，屬虛構條件，不影響發布。
- 官方 pypdf（6.21.2）與 openpyxl（3.1.3）的文件版本，片中都沒有引用。
- 本機實測版本 pypdf 6.10.0、openpyxl 3.1.5 只寫在 ledger，沒有上畫面。

## 意見核對

片中沒有標成站主意見的句子，也沒有未標記的主觀評價，與站主觀點立場（先算實際成本、回原文核對、只報真正執行的成果）一致。沒有不符之處。

## 有疑慮但未更動

1. description 的 GitHub commit 網址（7132d533…/materials）不在今日抓取的 sources 內，無法確認可以開啟。建議發布前由站主手動開一次。
2. description「教材包含需求、提示詞、來源 PDF 生成程式、逐頁抽文、可編輯比價表與版本紀錄」：archive replay 只證實 54 個 manifest 項目、雜湊相符，沒有逐項列出清單。generate_lab.py、extracted-pages、comparison.xlsx、change-log.json 都有個別紀錄，但查核者沒有看到 ZIP 成員清單全文。
3. missing-question 的草稿文字（「請補送到指定地址的運費…十到二十張費用是否相同」），ledger 只說依缺漏撰寫，沒有附 questions.txt 全文供逐字比對。它在卡片上標為可修改的草稿，不構成事實宣稱，所以沒有更動。
4. quantity-run 的實跑命令輸出到 comparison-output，ledger 註明位置在 repo 外；這不影響敘述的正確性。
