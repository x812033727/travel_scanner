# verify-4.md：ai-pdf-quotes-to-comparison 第 4 輪事實查核（2026-10-26，獨立新工作階段）

本輪 payload 讀取的官方頁有兩頁，都是 ok=true、status 200：
- pypdf 6.21.2：https://pypdf.readthedocs.io/en/stable/user/extract-text.html
- openpyxl 3.1.3：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html

片中所有金額、稅率與條款都是原創練習 fixture，沒有官方頁。核對依據有三項：claims.md 已保存的原件摘錄、本輪逐式重算、卡片之間的一致性。第三方頁（Kevin Stratvert 兩頁、FableGuide）只當企劃參考，不用來確認任何數字，片中也沒有引用。

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|
| 1 ｜ 三家原報單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 ｜ opening-unit、cost-unit-baseline、missing-known ｜ fixture（claims.md 原件摘錄） ｜ CONFIRMED ｜ — |
| 2 ｜ 單價排序 丙<甲<乙（175<180<205） ｜ cost-start 35fs、cost-unit-baseline ｜ 重算 ｜ CONFIRMED ｜ — |
| 3 ｜ 需求：10 張 A6 105×148 mm、350 gsm、雙面全彩、7 個工作天 ｜ need-spec、need-delivery ｜ requirements.txt（root exact-text 紀錄） ｜ CONFIRMED ｜ —（全文仍未摘入，見懷疑項） |
| 4 ｜ viewer-prompt.txt 共 7 行全文 ｜ extract-core、description「畫面七行提示詞」 ｜ 卡片實數 7 行 ｜ CONFIRMED ｜ — |
| 5 ｜ 甲：商品稅 5%（第1頁）、運費 200 未稅（第2頁）、原句 "Shipping: TWD 200.00 excluding tax to the specified address" ｜ extract-aster、extract-aster-quote、m57n、26ya ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 6 ｜ 乙：205 含稅、運費 0 送達免運、交期 5 個工作天（第2頁） ｜ extract-birch ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 7 ｜ 丙原句 "Shipping: not quoted"（第2頁），JSON 欄位 value 為 null ｜ extract-missing-quote、extract-null ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 8 ｜ 甲 10 張：1,800＋90＋210＝2,100 ｜ cost-aster-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 9 ｜ 乙 10 張：10×205＝2,050 ｜ cost-birch-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 10 ｜ 丙原版總價待確認，不排入名次；目前乙比甲便宜 ｜ cost-initial-result、bcr5、tnrc ｜ 重算 ｜ CONFIRMED ｜ — |
| 11 ｜ e86a：丙商品含稅 1,837.50 比乙 2,050 低，運費只要不夠高，名次就會翻過來 ｜ missing-start ｜ 重算（差 212.50） ｜ CONFIRMED ｜ — |
| 12 ｜ 丙已知與未知；數量適用 10–20 ｜ missing-known ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 13 ｜ 修訂版原句 "Replaces CED-1026-v1; not an additional supplier."（第1頁） ｜ revision-identity ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 14 ｜ 修訂版補運費 250 未稅、運費稅 5%，單價 175 不變 ｜ revision-diff、hiqk ｜ fixture 摘錄 ｜ CONFIRMED ｜ — |
| 15 ｜ 丙修訂版 10 張：1,837.50＋262.50＝2,100.00，與甲同價；乙 2,050 仍最低 ｜ revision-total、revision-ranking、dyun、72xb ｜ 重算 ｜ CONFIRMED ｜ — |
| 16 ｜ request-20.json 共 4 行，quantity 為 20 ｜ quantity-edit ｜ 卡片實數；claims.md 記 46 bytes ｜ CONFIRMED ｜ — |
| 17 ｜ 實跑命令與輸出（需求數量 20、修訂版、甲乙丙修訂版），標「實跑 2026-10-26」 ｜ quantity-run、quantity-output ｜ claims.md 的 stdout winners 與 selected-comparison 紀錄 ｜ CONFIRMED ｜ —（本輪未附原始 stdout，見懷疑項） |
| 18 ｜ 三家單價適用 10–20 張，甲、丙修訂版運費在範圍內固定 ｜ quantity-ranges、sxtz、rgr9 ｜ fixture 摘錄（逐字句只見 birch） ｜ CONFIRMED ｜ —（見懷疑項） |
| 19 ｜ 甲 20 張：3,780＋210＝3,990 ｜ quantity-aster ｜ 重算 ｜ CONFIRMED ｜ — |
| 20 ｜ 乙 20 張：4,100 ｜ quantity-birch ｜ 重算 ｜ CONFIRMED ｜ — |
| 21 ｜ 丙修訂版 20 張：3,675＋262.50＝3,937.50，最低 ｜ quantity-cedar、quantity-ranking、gzzk、cbe9 ｜ 重算 ｜ CONFIRMED ｜ — |
| 22 ｜ pruf：甲乙差距在 20 張時反轉（10 張乙<甲，20 張甲<乙） ｜ quantity-birch ｜ 重算 ｜ CONFIRMED ｜ — |
| 23 ｜ 掃描圖片的抽取結果可能是空的（"the extracted text may be minimal or visually empty"；"pypdf is not OCR software."） ｜ handoff-scan 6hst/ctma、description「不做掃描影像 OCR」 ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html ｜ CONFIRMED ｜ — |
| 24 ｜ 表格排版可能把數字接錯（"Typically, tables are just absolutely positioned text."；"PDF files don’t contain a semantic layer."） ｜ handoff-table ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html ｜ CONFIRMED ｜ — |
| 25 ｜ openpyxl 只寫檔、不計算公式（"openpyxl never evaluates formula"） ｜ cost-workbook ehby、description ｜ https://openpyxl.readthedocs.io/en/stable/simple_formulae.html ｜ CONFIRMED ｜ — |
| 26 ｜ 交付三份檔案：可編輯比價表、待問清單、版本變動清單 ｜ handoff-output、description ｜ claims.md 實際輸出紀錄 ｜ CONFIRMED ｜ — |
| 27 ｜ description：Codex AI 文件分析、pypdf 抽文、精確小數計算；5% 為原創設定；資料日期 2026-10-26 ｜ youtube.description ｜ brief 與 claims.md ｜ CONFIRMED ｜ — |
| 28 ｜ youtube.title、thumbnail「先算總價／稅與運費別漏算」 ｜ youtube、thumbnail ｜ 與片中結果一致 ｜ CONFIRMED ｜ — |
| 29 ｜ missing-status 狀態欄規則（c18）、cost-total-check 含稅小計說明（c16） ｜ missing-status、cost-total-check ｜ 教學建議 ｜ OUT OF SCOPE ｜ — |
| 30 ｜ tags、outro CTA、訂閱語 ｜ youtube.tags、outro ｜ — ｜ OUT OF SCOPE ｜ — |

## 計數

| 判定 | 數量 |
|---|---|
| CONFIRMED | 28 |
| CHANGED | 0 |
| NOT FOUND | 0 |
| OUT OF SCOPE | 2 |

video.json 本輪未修改。

## 規則檢查

- **免責語家族**：旁白與 description 都沒有出現「以官網為準」「公告沒寫」「我不唸」「不在這裡唸」「不替你填」，也沒有「不代表／不等於」用來說某件事沒寫。
- **查證用語**：旁白沒有出現「經查證」「根據官方文件」「截至查證」「本影片」。
- **個人資料、建議類內容**：沒有個人資料。沒有財務、稅務或法律建議；稅率已在 need-fiction 與 description 標明是練習假設。
- **教學示範**：quantity-run 與 quantity-output 的「實跑」標示，以 claims.md 的實跑紀錄為依據，沒有把預期結果寫成觀察到的成功。

## 即將過期

- 金額全是原創 fixture，沒有會過期的價格或方案。
- pypdf 6.21.2 與 openpyxl 3.1.3 的行為描述以 2026-10-26 讀取的頁面為準。套件改版後要重讀這兩頁。

## 觀點不符

無。片中沒有未標示為站主看法的個人意見。內容與站主觀點的立場 1、3、4、6、7 一致：先算清實際成本、回原文核對、只報實際執行的結果。

## 懷疑但未改

1. **sxtz「這三份報價都寫明，單價在這段數量範圍內保持相同」**
   - 已保存的摘錄中，只有 birch 第2頁有逐字句。
   - aster 與 cedar-revised 只見 "Quantity range: 10 to 20 pieces inclusive"。
   - quantity-ranges 卡上「範圍內固定」運費的逐字原句也還沒摘入。
   - 程式拒絕 21 張，語意上成立，所以沒有改。仍待把兩份 PDF 第2頁全文摘入 claims.md。
2. **requirements.txt 全文仍未摘入**
   - need-spec 標第7–8行，need-delivery 標第8–9行，兩卡的第8行內容一致。
   - 目前依 root exact-text 紀錄採信。
3. **實跑證據未附原始 stdout**
   - 本輪 payload 沒有附 quantity-run／quantity-output 的原始 stdout，也沒有附 selected-comparison.json 原檔。
   - 成片前應對照 lab receipts 做一次視覺核對。
4. **fixture 原件摘錄不在本輪 payload**
   - 原件摘錄放在 claims.md 第 1 輪以前、已保留的段落，本輪 payload 只附摘要說明，沒有附原文。
   - 本輪依重算與跨卡一致性判定。建議下輪 payload 附上八頁原文摘錄。
