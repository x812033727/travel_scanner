# verify-3.md：ai-pdf-quotes-to-comparison 第 3 輪事實查核

查核日：2026-10-26（獨立新工作階段，未參考前輪結論，只用 payload 內 sources、claims.md 摘錄及獨立重算）。製作路線為「教學卡片」，所以每個示範都另外核對輸入、動作與實跑證據。

## 來源讀取狀態

- 官方頁 ok=true：
  - https://pypdf.readthedocs.io/en/stable/user/extract-text.html（pypdf 6.21.2 documentation）
  - https://openpyxl.readthedocs.io/en/stable/simple_formulae.html（openpyxl 3.1.3 documentation）
- 兩筆 HTTP 404 不是官方頁讀不到。它們是同一網址後面黏了「（頁面」這幾個全形字（被編成 %EF%BC%88…），起因是 claims.md 的網址後面直接接全形括號。乾淨網址都已讀到，沒有任何主張因此改用 Mokaair 文章作來源。
- 第三方頁（kevinstratvert.com 兩頁、fableguide.com）不確認任何數字，影片也沒有引用。
- 片中金額、稅率、頁碼與原句都是原創練習資料（fixture），沒有官方頁可對。這些項目的核對方式是兩種：一是 claims.md 已記錄的八頁原件摘錄與實跑紀錄，二是本輪逐式獨立重算。

## 逐項查核

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|
| 1 ｜ 三家單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 ｜ opening-unit、cost-unit-baseline、extract-aster/birch、missing-known ｜ materials（三家 PDF 第1頁，claims.md 摘錄） ｜ CONFIRMED ｜ — |
| 2 ｜ 需求：10 張 A6 105×148 mm、350 gsm 霧面白卡、雙面全彩、同一地址、7 個工作天、比送達含明示稅額總價 ｜ need-spec、need-delivery（requirements.txt 第7–9行） ｜ materials/requirements.txt ｜ CONFIRMED（依 claims.md 紀錄的逐字比對；兩張卡共用的第8行內容一致） ｜ — |
| 3 ｜ 原檔 aster.pdf／birch.pdf／cedar.pdf，原件只讀、輸出另存 ｜ need-labels、quantity-run ｜ materials ｜ CONFIRMED ｜ — |
| 4 ｜ 供應商、價格、5% 稅率為虛構練習設定 ｜ need-fiction、description ｜ brief ｜ CONFIRMED ｜ — |
| 5 ｜ 分工：pypdf 抽文 → AI 讀逐頁原文整理欄位 → 精確小數計算 ｜ need-route、extract-start、description ｜ pypdf 官方頁；claims.md 實跑紀錄 ｜ CONFIRMED ｜ — |
| 6 ｜ 甲單價在第1頁、運費在第2頁；原句 "Shipping: TWD 200.00 excluding tax to the specified address" ｜ need-proof、extract-aster、extract-aster-quote ｜ aster.pdf 第1–2頁（claims.md 摘錄） ｜ CONFIRMED ｜ — |
| 7 ｜ viewer-prompt.txt 全文 7 行；欄位定義 ｜ extract-core、extract-fields、description「畫面七行提示詞」 ｜ materials/viewer-prompt.txt ｜ CONFIRMED（實數 7 行） ｜ — |
| 8 ｜ 乙 205 含稅、送達免運 0、5 個工作天（≤ 需求 7 天） ｜ extract-birch、extract-review ｜ birch.pdf 第1–2頁 ｜ CONFIRMED ｜ — |
| 9 ｜ 丙第2頁 "Shipping: not quoted"；JSON 值 null、page 2；已知與未知分列；數量 10–20 ｜ extract-missing-quote、extract-null、missing-known ｜ cedar.pdf 第2頁 ｜ CONFIRMED ｜ — |
| 10 ｜ 單價排序：丙 175 → 甲 180 → 乙 205 ｜ cost-start、cost-unit-baseline ｜ 重算 ｜ CONFIRMED ｜ — |
| 11 ｜ 甲十張：1,800＋90＋210＝2,100 ｜ cost-aster-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 12 ｜ 乙十張：10×205＝2,050，運費 0，不重複加稅 ｜ cost-birch-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 13 ｜ 丙原版總價待確認，不排名次；十張時乙比甲便宜 ｜ cost-initial-result、missing-start ｜ 重算 ｜ CONFIRMED ｜ — |
| 14 ｜ 由計算工具依明示條件算小數，不先四捨五入單價 ｜ cost-rounding、cost-workbook ｜ claims.md（Decimal 實跑） ｜ CONFIRMED ｜ — |
| 15 ｜ 試算表存的是已算好的值；openpyxl 只寫檔、不計算公式 ｜ cost-workbook、description ｜ https://openpyxl.readthedocs.io/en/stable/simple_formulae.html 「openpyxl never evaluates formula」 ｜ CONFIRMED ｜ — |
| 16 ｜ 含稅小計旁的稅額不可再加一次 ｜ cost-total-check ｜ — ｜ OUT OF SCOPE（方法建議，不含事實數字） ｜ — |
| 17 ｜ 詢問草稿內容；草稿未寄出，由下單者確認 ｜ missing-question、missing-no-send ｜ claims.md ｜ CONFIRMED ｜ — |
| 18 ｜ 狀態欄規則 ｜ missing-status ｜ — ｜ OUT OF SCOPE（教學建議） ｜ — |
| 19 ｜ 修訂版 "Replaces CED-1026-v1; not an additional supplier."；修訂版只改運費與運費稅，單價仍 175 ｜ revision-start、revision-identity、revision-diff ｜ cedar-revised.pdf 第1–2頁 ｜ CONFIRMED ｜ — |
| 20 ｜ 丙修訂版十張：1,837.50＋262.50＝2,100.00，與甲同價 ｜ revision-total、revision-ranking ｜ 重算 ｜ CONFIRMED ｜ — |
| 21 ｜ 補件後十張仍是乙 2,050 最低 ｜ revision-ranking ｜ 重算 ｜ CONFIRMED ｜ — |
| 22 ｜ 來源欄改指向修訂版 ｜ revision-links ｜ claims.md 輸出紀錄 ｜ CONFIRMED ｜ — |
| 23 ｜ request-20.json：scenario "revised"、quantity 20；輸出的需求數量為 20、採用修訂版、供應商只有甲、乙、丙修訂版 ｜ quantity-start、quantity-edit、quantity-prompt、quantity-output ｜ materials、selected-comparison.json（實跑） ｜ CONFIRMED ｜ — |
| 24 ｜ 三家單價都適用 10–20 張；甲、丙運費在此範圍內固定；乙免運 ｜ quantity-ranges ｜ 三家 PDF 第2頁 ｜ CONFIRMED（措辭有疑慮，見「懷疑但未改」） ｜ — |
| 25 ｜ 甲二十張：3,780＋210＝3,990 ｜ quantity-aster、quantity-ranking ｜ 重算 ｜ CONFIRMED ｜ — |
| 26 ｜ 乙二十張：20×205＝4,100；甲乙名次反轉（十張乙低，二十張甲低） ｜ quantity-birch、quantity-ranking ｜ 重算 ｜ CONFIRMED ｜ — |
| 27 ｜ 丙修訂版二十張：3,675＋262.50＝3,937.50，最低 ｜ quantity-cedar、quantity-ranking ｜ 重算 ｜ CONFIRMED ｜ — |
| 28 ｜ 交付物：可編輯比價表、待問清單、版本變動清單 ｜ handoff-start、handoff-output、description ｜ claims.md 輸出紀錄 ｜ CONFIRMED ｜ — |
| 29 ｜ 掃描圖片的抽文結果可能是空的或殘缺；要改用有辨識能力的流程；本流程不做 OCR ｜ handoff-scan、description ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html 「the extracted text may be minimal or visually empty」「pypdf is not OCR software.」 ｜ CONFIRMED ｜ — |
| 30 ｜ 表格換行或多欄排版可能把數字接錯地方 ｜ handoff-table ｜ 同上 pypdf 頁：「Typically, tables are just absolutely positioned text.」「PDF files don’t contain a semantic layer.」 ｜ CONFIRMED ｜ — |
| 31 ｜ build_comparison.py 命令於 2026-10-26 實跑 ｜ quantity-run、quantity-output ｜ claims.md 相對命令與 stdout winners 紀錄 ｜ CONFIRMED（有實跑紀錄，不是預期結果；原始 stdout 不在本 payload） ｜ — |
| 32 ｜ e86a：丙商品比乙便宜，運費不夠高名次就會翻 ｜ missing-start ｜ 重算：1,837.50 對 2,050，差 212.50 ｜ CONFIRMED（條件句成立） ｜ — |
| 33 ｜ youtube.title、thumbnail（先算總價／稅與運費別漏算／AI 比較 PDF 報價） ｜ youtube、thumbnail ｜ — ｜ CONFIRMED（沒有數字主張） ｜ — |
| 34 ｜ description：日期 2026-10-26、可選取文字 PDF、不宣稱實測商用 AI 上傳介面、教材連結 ｜ youtube.description ｜ brief、兩個官方頁 ｜ CONFIRMED ｜ — |
| 35 ｜ tags、outro CTA ｜ youtube.tags、outro ｜ — ｜ OUT OF SCOPE ｜ — |

## 計數

- CONFIRMED：31
- OUT OF SCOPE：4
- CHANGED：0
- NOT FOUND：0
- changed_facts：0，video.json 未修改。

## 規則檢查

- 旁白與 description 都沒有出現「以官網為準」那一組免責字詞。
- 旁白沒有出現查證用語（經查證、根據官方文件、截至查證、本影片）。
- 沒有虛構站主的經驗，沒有個人資料。
- 沒有財務、稅務或法律建議；稅率已明說只是練習假設。
- 站主的標準指示沒有提供旁白名字或口頭禪，片中也沒有自創。

## 即將過期

- 片中金額都是原創 fixture，沒有會過期的價格。
- pypdf 行為描述以 6.21.2 文件為準，openpyxl 以 3.1.3 文件為準，兩者都是 2026-10-26 讀取。之後套件改版時要重查「不做 OCR」與「不計算公式」這兩句。

## 觀點不符

無。片中沒有未標示的站主觀點。教學指示符合站主觀點的立場 1、3、4、6、7：先算清實際成本，AI 整理後回原文核對，只報實跑成果。

## 懷疑但未改

1. **sxtz「三份報價都寫明，單價在這段數量範圍內保持相同」及 quantity-ranges 的「範圍內固定」**
   - claims.md 只有 birch 第2頁有逐字句。aster 與 cedar-revised 的摘錄只到 "Quantity range: 10 to 20 pieces inclusive"，而且註明省略了其他段落。
   - 甲與丙「運費在範圍內固定」這點，claims.md 摘錄沒有逐字原句；brief 說有書面依據。
   - 未見反證，所以沒有改。請補上 aster.pdf 與 cedar-revised.pdf 第2頁全文，證實後再保留「寫明」二字。
2. **requirements.txt 全文仍未摘入 claims.md。** need-spec 與 need-delivery 目前依 verifier-followup-exact-text.json 的逐字比對紀錄採信。
3. **quantity-run 與 quantity-output 標「實跑 2026-10-26」。** 本 payload 沒有原始 stdout 或 selected-comparison.json 本文，只有 claims.md 的紀錄。重算結果與紀錄一致，但請保留 receipts 供成片前視覺核對。
4. **兩筆 404 是 claims.md 的網址格式問題，不是官方頁失效。** 已在 claims.md 用空格把網址和括號隔開，避免下輪再抓到錯誤網址。
