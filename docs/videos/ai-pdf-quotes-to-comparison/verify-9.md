# verify-9.md：ai-pdf-quotes-to-comparison 第9輪獨立查核

查核日：2026-10-26。查核者為新工作階段，沒有看過先前查核結果。payload 的每頁 sources 都抓取成功（status 200），沒有標示失敗的抓取。本片沒有任何數字需要以 Mokaair 文章作來源。

本片的金額、稅率、數量範圍、交期、檔名與頁碼，全部來自原創虛構練習 PDF，沒有官方頁面可以佐證。依教學卡片路線，這些數字改以兩種證據核對：
- claims ledger 內逐字附上的八頁 pypdf 抽文
- 實跑收據：argv、exit code、stdout、stderr、selected_result、comparison.json，以及 Decimal 差額紀錄

工具行為只用官方頁核對：openpyxl 不計算公式、pypdf 不是 OCR。

## 逐項查核

| # | claim | where | URL | verdict | before → after |
|---|---|---|---|---|---|
| 1 | 甲180未稅、乙205含稅、丙175未稅 | opening-unit rows；xnrg | 練習原文 aster/birch/cedar.pdf p1（ledger 抽文） | CONFIRMED | — |
| 2 | 需求節錄＝requirements.txt 第7–8行、第8–9行 | need-spec、need-delivery code/caption | materials/requirements.txt 全文（ledger） | CONFIRMED（逐字、行號相符） | — |
| 3 | 原檔 aster/birch/cedar.pdf 保留，輸出另存 | need-labels；d78a | ledger c3；quantity-run 輸出至 comparison-output | CONFIRMED | — |
| 4 | 供應商、金額、5%稅率均為虛構練習 | need-fiction；description | 每頁「Fictional training quote. The 5% rates are exercise assumptions…」 | CONFIRMED | — |
| 5 | 抽文→AI欄位→精確小數計算後寫表 | need-route；extract-start | ledger c5、AI執行紀錄 | CONFIRMED | — |
| 6 | 甲單價在第1頁、送貨條件在第2頁 | need-proof；extract-aster；fd27 | aster.pdf p1「Unit price: TWD 180.00 excluding tax」「Goods tax: 5%」；p2「Shipping: TWD 200.00 excluding tax…」 | CONFIRMED | — |
| 7 | 引文「Shipping: TWD 200.00 excluding tax to the specified address」 | extract-aster-quote | aster.pdf p2 | CONFIRMED（逐字） | — |
| 8 | 七行提示詞全文、第1–7行 | extract-core | materials/viewer-prompt.txt 全文 | CONFIRMED（逐字） | — |
| 9 | 乙205含稅、運費0免運、交期5工作天，出處p1/p2 | extract-birch；mdte、q7x8 | birch.pdf p1「TWD 205.00 including 5% goods tax」；p2「Shipping: TWD 0.00; delivery to the specified address is free」「Lead time: 5 business days」 | CONFIRMED | — |
| 10 | 丙原版「Shipping: not quoted」在第2頁；值為 null | extract-missing-quote；extract-null；7hi8 | cedar.pdf p2 | CONFIRMED | — |
| 11 | 單價排序 丙175→甲180→乙205 | cost-unit-baseline；35fs | baseline-and-normalized-order.json unit_price_order | CONFIRMED | — |
| 12 | 甲10張：1,800＋90＋210＝2,100 | cost-aster-formula | comparison.json original-10 Aster goods_gross 1890.00、shipping_gross 210.00、delivered_total 2100.00 | CONFIRMED | — |
| 13 | 乙10張 10×205＝2,050，不重複加稅 | cost-birch-formula | birch.pdf p1「No second goods tax is added…」；comparison.json 2050.00 | CONFIRMED | — |
| 14 | 十張原版：甲2,100.00、乙2,050.00、丙待確認；乙比甲便宜 | cost-initial-result；bcr5、tnrc | comparison.json original-10（Cedar delivered_total null） | CONFIRMED | — |
| 15 | 以精確小數計算，不先四捨五入單價 | cost-rounding | ledger c14（Decimal） | CONFIRMED | — |
| 16 | 試算表是已算值、不是會自己重算的公式 | cost-workbook；ehby；description | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html「openpyxl never evaluates formula」（官網 2026-10-26） | CONFIRMED | — |
| 17 | 丙商品比乙便宜，運費不夠高名次就翻轉 | e86a | comparison.json：Cedar goods_gross 1837.50 ＜ Birch 2050.00 | CONFIRMED（算術） | — |
| 18 | 丙已知：175未稅、商品稅5%、數量10–20；未知：運費、含稅與否、稅率 | missing-known | cedar.pdf p1–p2 | CONFIRMED | — |
| 19 | 詢問草稿未寄出 | missing-question；missing-no-send | ledger c17 | CONFIRMED（未宣稱已寄出或已回覆） | — |
| 20 | 狀態欄三分類為教學規則 | missing-status | ledger c18 | CONFIRMED（條件式示例，source 已標原創教學建議） | — |
| 21 | 引文「Replaces CED-1026-v1; not an additional supplier.」 | revision-identity | cedar-revised.pdf p1 | CONFIRMED（逐字） | — |
| 22 | 修訂：運費250未稅、運費稅5%、單價175不變 | revision-diff；hiqk | cedar-revised.pdf p2「Shipping: TWD 250.00 excluding tax…」「Only delivery terms changed…」 | CONFIRMED | — |
| 23 | 丙修訂10張 1,837.50＋262.50＝2,100.00，與甲同價 | revision-total；ambg | comparison.json revised-10 Cedar | CONFIRMED | — |
| 24 | 修訂十張：乙2,050最低，丙比乙多50 | revision-ranking；dyun | revised-ten-price-difference.json cedar_minus_birch 50.00 | CONFIRMED | — |
| 25 | 來源欄改指修訂版 | revision-links | comparison.json revised-10 price_source「cedar-revised.pdf p.1」 | CONFIRMED | — |
| 26 | request-20.json 第1–4行全文 | quantity-edit | materials/request-20.json 全文 | CONFIRMED（逐字） | — |
| 27 | 命令與 cwd（materials），實跑 2026-10-26 | quantity-run；6wkf、74dc | lab-relative-command-execution.json argv 逐字、exit 0；教材重播 2026-10-26T09:24:56Z | CONFIRMED（實跑證據） | — |
| 28 | 輸出：數量20、修訂版、甲乙丙修訂版共3列 | quantity-output | selected_result（request quantity 20、scenario revised、3 rows） | CONFIRMED | — |
| 29 | 三家單價適用10–20；甲200、丙250運費範圍內固定；乙免運 | quantity-ranges；sxtz、rgr9 | aster/birch/cedar-revised p2「Quantity range: 10 to 20 pieces inclusive」「Shipping remains TWD 200.00/250.00 net for 10 to 20 pieces」 | CONFIRMED | — |
| 30 | 甲20張 3,780＋210＝3,990 | quantity-aster | selected_result Aster | CONFIRMED | — |
| 31 | 乙20張 4,100；比甲多110 | quantity-birch；m8sb | selected_result；revised-twenty-price-difference.json 110.00 | CONFIRMED | — |
| 32 | 丙20張 3,675＋262.50＝3,937.50；比甲少52.50 | quantity-cedar；gy4i | selected_result；revised-twenty-cedar-gap.json 52.50 | CONFIRMED | — |
| 33 | 20張排名 丙→甲→乙，最低換成丙 | quantity-ranking；cbe9 | baseline-and-normalized-order revised_20_order；stdout winners revised-20 Cedar | CONFIRMED | — |
| 34 | request-21-invalid.json 第1–4行全文 | range21-request | materials/request-21-invalid.json | CONFIRMED（逐字） | — |
| 35 | 21張命令；實跑 2026-10-26 | range21-run | quantity-21-relative-execution.json argv 逐字，executed_at 2026-10-26T09:16:45Z | CONFIRMED | — |
| 36 | 「ValueError: Quantity outside explicitly quoted range」；未建立資料夾 | range21-result；9jiq、egmv | 同收據：exit_code 1、stderr 最後一行、output_directory_created false | CONFIRMED（實跑） | — |
| 37 | 21張重報詢問草稿全文 | range21-question | materials/questions-21.txt 全文 | CONFIRMED（逐字，標示尚未寄出） | — |
| 38 | 抽文流程不做掃描影像 OCR | description | https://pypdf.readthedocs.io/en/stable/user/extract-text.html「pypdf is not OCR software.」（官網 2026-10-26） | CONFIRMED | — |
| 39 | 使用 Codex AI 文件分析、AI 也讀了 analysis-prompt.txt 的 JSON 契約 | description | ledger AI 執行紀錄 inputs 第2項 analysis-prompt.txt | CONFIRMED | — |
| 40 | 資料與實作日期 2026-10-26 | description | 各收據時間戳 | CONFIRMED | — |
| 41 | 縮圖與 asset 說明「十張實算A2100/B2050/C未知」 | thumbnail；assets | comparison.json original-10 | CONFIRMED | — |
| 42 | 標題、標籤 | youtube | — | OUT OF SCOPE（無數字主張） | — |
| 43 | GitHub 教材連結（含 commit hash） | description | 未在 sources 中 | OUT OF SCOPE（非數字事實；見下方「懷疑但未改」） | — |

## 統計

- 共 43 項。
- CONFIRMED 41 項，CHANGED 0 項，NOT FOUND 0 項，OUT OF SCOPE 2 項。
- changed_facts＝0；video 不修改（null）。
- 旁白與描述都沒有使用「以官網為準」等免責語族。旁白中也沒有查證用語。

## 即將過期的事實

- 練習 PDF 都寫明「Valid for this fictional exercise through 2026-11-30」。影片沒有唸出這個日期。不過教材包在 2026-11-30 之後若仍沿用「有效報價」的說法，就需要留意。
- 官方文件版本標示：pypdf stable 頁首為 6.21.2，openpyxl 為 3.1.3。影片沒有提到這兩個版本號，因此不受影響。

## 觀點不符

無。本片沒有站主個人觀點句。各操作建議（先寫需求、回原文核對、只報真正執行結果）都符合站主觀點的立場 1、3、4、6、7，也沒有虛構站主的經驗或習慣。

## 懷疑但未改

1. **GitHub 教材連結**：描述中的連結與 commit 7132d533… 無法用 sources 核對連結是否存在。建議發布前人工點開確認。它不是數字事實，所以沒有更動。
2. **quantity-prompt 對話卡**：「你的要求」是建議觀眾使用的句子。實跑時 AI 收到的是 request-20.json 檔案，並不是這段對話文字。卡片沒有聲稱這是實際對話截圖或執行結果，所以維持原樣。
3. **需求檔名不一致**：q57z／7dp4 說「打開數量設定檔改成二十」，畫面顯示的檔案是 request-20.json；教材另有 request.json（quantity 10）。觀眾實際是改 request.json 還是另存成 request-20.json，屬於操作描述的一致性問題，不是事實錯誤，因此沒有改動。
4. **AI 的實際輸入**：extract-start 說把兩頁文字「連同需求」交給 AI。實際上 AI 也收到了 analysis-prompt.txt，描述已另行揭露，沒有隱瞞。
