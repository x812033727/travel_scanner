# verify-7.md：第 7 輪事實查核

日期：2026-10-26（Asia/Taipei），獨立新工作階段。

製作路線為「教學卡片」。凡是宣稱已執行的示範，都另外對照輸入、動作與實跑證據。

## 逐項查核

| # | claim | where | URL | verdict | before → after |
|---|---|---|---|---|---|
| 1 | c1 原報單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 | opening-unit（xnrg）、cost-unit-baseline、extract-aster、extract-birch、missing-known | 原創練習 PDF 第1頁（fixture，非網頁；claims.md c1） | CONFIRMED | — |
| 2 | c2 需求為 10 張 A6（105×148 mm）、350 gsm、雙面全彩、同地址、7 個工作天內交貨；卡片標「第7–8行」「第8–9行」 | need-start、need-spec、need-delivery | requirements.txt（教材；claims.md c2） | CONFIRMED | — |
| 3 | c3 三份原檔清單，原件只讀、輸出另存 | need-labels | 教材 materials | CONFIRMED | — |
| 4 | c4 供應商與 5% 稅率是虛構練習設定 | need-fiction、description | brief、claims.md c4 | CONFIRMED | — |
| 5 | c5 分工：抽文、AI 讀逐頁原文、精確小數計算 | need-route、extract-start | brief、claims.md c5 | CONFIRMED | — |
| 6 | c6 甲的運費在第2頁，200 未稅；原句 Shipping: TWD 200.00 excluding tax… | need-proof、extract-aster、extract-aster-quote | aster.pdf 第2頁（fixture） | CONFIRMED | — |
| 7 | c7 提示詞共 7 行，卡片標「全文」 | extract-core、extract-fields、description | viewer-prompt.txt | CONFIRMED（實數 7 行） | — |
| 8 | c8 乙免運、交期 5 個工作天 | extract-birch | birch.pdf 第2頁（fixture） | CONFIRMED | — |
| 9 | c9 丙原句「Shipping: not quoted」，欄位值為 null | extract-missing-quote、extract-null、missing-known | cedar.pdf 第2頁（fixture） | CONFIRMED | — |
| 10 | c10 單價排序 175 < 180 < 205 | cost-start、cost-unit-baseline | 由 c1 推得 | CONFIRMED | — |
| 11 | c11 甲十張：1800 + 90 + 210 = 2100 | cost-aster-formula、cost-initial-result | 獨立重算 | CONFIRMED | — |
| 12 | c12 乙十張：10 × 205 = 2050 | cost-birch-formula、cost-initial-result | 獨立重算 | CONFIRMED | — |
| 13 | c13 丙十張總價待確認，不排入名次 | cost-initial-result（tnrc）、missing-start | 由 c9 推得 | CONFIRMED | — |
| 14 | e86a 丙商品含稅 1837.5 比乙 2050 低 212.5，條件句成立 | missing-start | 獨立重算 | CONFIRMED | — |
| 15 | c14、c15 試算表寫入已算值，不會自己重算公式 | cost-rounding、cost-workbook（ehby）、description | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html（逐字：openpyxl never evaluates formula） | CONFIRMED | — |
| 16 | description：pypdf 抽文不做掃描影像 OCR | description | https://pypdf.readthedocs.io/en/stable/user/extract-text.html（逐字：pypdf is not OCR software.） | CONFIRMED | — |
| 17 | c17 詢問草稿的措辭 | missing-question、missing-no-send | — | OUT OF SCOPE | — |
| 18 | c18 狀態欄使用規則 | missing-status | — | OUT OF SCOPE | — |
| 19 | c19 修訂版原句 Replaces CED-1026-v1; not an additional supplier. | revision-start、revision-identity、revision-links | cedar-revised.pdf 第1頁（fixture） | CONFIRMED | — |
| 20 | c20 修訂版運費 250 未稅、稅 5%，單價 175 不變；十張：1837.50 + 262.50 = 2100.00 | revision-diff、revision-total | 獨立重算 | CONFIRMED | — |
| 21 | c21 十張修訂後乙 2050 最低，甲丙同價 2100 | revision-ranking（dyun、u9p4） | 獨立重算 | CONFIRMED | — |
| 22 | c22 來源欄改為對應修訂版 | revision-links | claims.md c22 | CONFIRMED | — |
| 23 | c23 request-20.json 共 4 行，quantity 為 20 | quantity-start、quantity-edit、quantity-prompt | 教材 materials | CONFIRMED | — |
| 24 | c23、c31 命令與輸出：需求數量 20、修訂版、甲乙丙修訂版，卡片標「實跑 2026-10-26」 | quantity-run、quantity-output | lab receipts（claims.md c31） | CONFIRMED（依 claims.md 既有收據紀錄；原始 stdout 與 selected-comparison.json 未附在本輪 payload，見文末） | — |
| 25 | c24 三家單價都適用 10–20 張，甲、丙運費在範圍內固定，乙免運 | quantity-ranges（sxtz、rgr9） | 三家 PDF 第2頁（fixture） | CONFIRMED（依 claims.md；第2頁逐字全文仍待摘入） | — |
| 26 | c25 甲二十張：3780 + 210 = 3990 | quantity-aster、quantity-ranking | 獨立重算 | CONFIRMED | — |
| 27 | c26 乙二十張：4100；相對十張，甲乙名次反轉 | quantity-birch（pruf）、quantity-ranking | 獨立重算 | CONFIRMED | — |
| 28 | c27 丙修訂版二十張：3675 + 262.50 = 3937.50，最低 | quantity-cedar、quantity-ranking（cbe9） | 獨立重算 | CONFIRMED | — |
| 29 | nvu3 名次換人是因為固定運費占比改變，不是降價 | quantity-ranking | 由 c25–c27 推得 | CONFIRMED | — |
| 30 | c36 request-21-invalid.json 共 4 行，quantity 為 21 | range21-request | claims.md c36 收據（request_sha256） | CONFIRMED | — |
| 31 | c36 只換需求檔與輸出資料夾，其他輸入不變 | range21-run（cegb） | claims.md c36 收據（command、analysis、extracted 檔名一致；執行時間 2026-10-26T09:16:45Z） | CONFIRMED | — |
| 32 | c36 實跑：exit 1、最後一行「ValueError: Quantity outside explicitly quoted range」、output_directory_created=false | range21-result（9jiq）、quote 卡 | claims.md c36 收據（stderr 與 displayed_exact_last_line 逐字相符） | CONFIRMED（有實跑證據） | — |
| 33 | egmv 21 張超出三份報價寫明的 10–20 張範圍 | range21-result | c24、c36 | CONFIRMED | — |
| 34 | c37 重報 21 張的文字只是草稿，尚未寄出 | range21-question | materials/questions-21.txt（claims.md c37） | CONFIRMED | — |
| 35 | description：資料與實作日期 2026-10-26、七行提示詞、Codex 分析、不宣稱測過商用上傳介面 | description | brief | CONFIRMED | — |
| 36 | title 與 thumbnail（不含數字）、tags | youtube、thumbnail | — | OUT OF SCOPE | — |
| 37 | outro 的 CTA 與留言提問 | outro | — | OUT OF SCOPE | — |

## 計數

- CONFIRMED 33
- CHANGED 0
- NOT FOUND 0
- OUT OF SCOPE 4
- changed_facts = 0；video.json 未修改，回傳 null。

## 規則檢查

- **免責語**：旁白與 description 都沒有免責語家族用語（以官網為準、公告沒寫、我不唸、不代表／不等於句型），也沒有查證用語（經查證、根據官方文件、截至查證、本影片）。
- **數字來源**：所有金額都是原創練習 fixture，不涉及會過期的官方價格。第三方頁（FableGuide、Kevin Stratvert）只出現在 brief 的選題觀測，沒有用來佐證任何上片數字。
- **敘事者設定**：本輪沒有站主常設指示，旁白也沒有使用敘事者名字、口頭禪或固定結語。
- **個人資料**：沒有任何人的個人資料。
- **建議類內容**：沒有財務、稅務、法律或政治建議；稅率明標為練習假設。
- **示範證據**：預期結果沒有被寫成已觀察到的成功。21 張的拒絕結果有實跑收據；20 張的旁白只要求觀眾自行確認輸出。

## 即將過期的事實

- 沒有會過期的價格或方案。
- pypdf 6.21.2 與 openpyxl 3.1.3 的行為描述，以 2026-10-26 讀取的文件為準；套件改版後需要重讀。

## 觀點不符

- 旁白中沒有未標示的站主個人觀點。
- 內容與站主觀點立場 1、3、4、6、7 一致：先算清實際成本、回原文核對、只報實際執行的結果。

## 懷疑但未改

- **20 張實跑證據**：quantity-run 與 quantity-output 標「實跑 2026-10-26」。依據是 claims.md 記錄的 c31 lab receipts，但本輪 payload 沒有附原始 stdout 或 selected-comparison.json，無法直接逐字核對。成片前必須對照 receipts；對不上時，兩張卡要改標為預期輸出。
- **原件全文待摘入**：aster.pdf、cedar.pdf、cedar-revised.pdf 第2頁的逐字全文，以及 requirements.txt 全文，仍待摘入。這些是 sxtz、quantity-ranges 與 need-spec／need-delivery 行號的依據。
- **21 張的卡片情緒標記**：range21 四張卡的 emotion 都寫成同一句，屬於風格問題，未處理。
