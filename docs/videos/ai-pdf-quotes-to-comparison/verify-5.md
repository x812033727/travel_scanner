# verify-5.md：ai-pdf-quotes-to-comparison 第 5 輪事實查核

查核日：2026-10-26。獨立新工作階段，沒有參考前輪結論。所有數字都重新從 payload 的 sources 或逐式重算確認。

官方頁今日讀取（ok=true，status 200）：
- pypdf 6.21.2：https://pypdf.readthedocs.io/en/stable/user/extract-text.html
- openpyxl 3.1.3：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html

第三方頁（Kevin Stratvert 兩頁、FableGuide）只用於企劃參考，不拿來確認任何數字，片中也沒有引用。

## 逐項判定

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|---|
| 1 ｜ 三家單價：甲 180 未稅、乙 205 含稅、丙 175 未稅 ｜ opening-unit、cost-unit-baseline、extract-aster、extract-birch、missing-known ｜ 原創 fixture（aster/birch/cedar.pdf 第1頁，claims.md 摘錄紀錄） ｜ CONFIRMED（教材設定，跨卡一致） ｜ — |
| 2 ｜ 需求：10 張 A6 105×148 mm、350 gsm 霧面白卡、雙面全彩、7 個工作天、比送達含稅總價 ｜ need-start、need-spec、need-delivery ｜ requirements.txt 第7–9行（claims.md 逐字比對紀錄） ｜ CONFIRMED（原創教材；全文仍未摘入，見最後一節） ｜ — |
| 3 ｜ 三家原檔名 aster/birch/cedar.pdf，原件只讀、輸出另存 ｜ need-labels ｜ 教材 materials ｜ CONFIRMED ｜ — |
| 4 ｜ 供應商、金額、5% 稅率皆為虛構練習設定 ｜ need-fiction、description ｜ brief ｜ CONFIRMED ｜ — |
| 5 ｜ 分工：抽文 → AI 整理欄位 → 精確小數計算 ｜ need-route、extract-start ｜ brief、claims.md ｜ CONFIRMED ｜ — |
| 6 ｜ 甲：運費在第2頁，200 未稅；商品稅 5% 在第1頁 ｜ need-proof、extract-aster、extract-aster-quote（"Shipping: TWD 200.00 excluding tax to the specified address"） ｜ aster.pdf 第1–2頁（claims.md 摘錄） ｜ CONFIRMED ｜ — |
| 7 ｜ viewer-prompt.txt 七行全文；欄位定義 ｜ extract-core、extract-fields、description「畫面七行提示詞」 ｜ 教材 materials ｜ CONFIRMED（卡片實數 7 行） ｜ — |
| 8 ｜ 乙：運費 0（送達免運）、交期 5 個工作天，在第2頁 ｜ extract-birch ｜ birch.pdf 第2頁 ｜ CONFIRMED；5 天在 7 天期限內 ｜ — |
| 9 ｜ 丙原版："Shipping: not quoted"（第2頁）；以 null 空值保存 ｜ extract-missing-quote、extract-null、missing-known ｜ cedar.pdf 第2頁 ｜ CONFIRMED ｜ — |
| 10 ｜ 單價排序 丙 175 < 甲 180 < 乙 205 ｜ cost-start、cost-unit-baseline ｜ 重算 ｜ CONFIRMED ｜ — |
| 11 ｜ 甲十張：1,800＋90＋210＝2,100 ｜ cost-aster-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 12 ｜ 乙十張：10×205＝2,050，運費 0 ｜ cost-birch-formula、cost-initial-result ｜ 重算 ｜ CONFIRMED ｜ — |
| 13 ｜ 丙原版總價待確認，不排入名次 ｜ cost-initial-result、missing-start ｜ 重算 ｜ CONFIRMED ｜ — |
| 14 ｜ 小數由計算工具依明示條件計算，不先四捨五入 ｜ cost-rounding、cost-workbook ｜ claims.md（Decimal） ｜ CONFIRMED ｜ — |
| 15 ｜ openpyxl 只寫已算值，不計算公式；改需求要重跑 ｜ cost-workbook（ehby）、description ｜ openpyxl 頁："openpyxl never evaluates formula" ｜ CONFIRMED ｜ — |
| 16 ｜ e86a：丙商品比乙便宜，運費不夠高名次就翻 ｜ missing-start ｜ 重算：1,837.5 < 2,050，差 212.5 ｜ CONFIRMED（條件句） ｜ — |
| 17 ｜ 給丙的詢問草稿；草稿需人確認後再寄 ｜ missing-question、missing-no-send ｜ — ｜ OUT OF SCOPE（教學建議） ｜ — |
| 18 ｜ 狀態欄規則 ｜ missing-status ｜ — ｜ OUT OF SCOPE（教學建議） ｜ — |
| 19 ｜ 修訂版取代原版："Replaces CED-1026-v1; not an additional supplier."（第1頁）；來源欄改連修訂版 ｜ revision-start、revision-identity、revision-diff、revision-links ｜ cedar-revised.pdf 第1頁 ｜ CONFIRMED ｜ — |
| 20 ｜ 丙修訂版：運費 250 未稅、稅 5%、單價 175 不變；十張 1,837.50＋262.50＝2,100.00 ｜ revision-diff、revision-total ｜ 重算 ｜ CONFIRMED ｜ — |
| 21 ｜ 修訂後十張：乙 2,050 最低；甲、丙同價 2,100 ｜ revision-ranking（dyun、u9p4） ｜ 重算 ｜ CONFIRMED ｜ — |
| 22 ｜ 新值要跟新頁碼 ｜ revision-links ｜ — ｜ CONFIRMED（流程描述） ｜ — |
| 23 ｜ request-20.json：scenario revised、quantity 20，共 4 行；命令與輸出 ｜ quantity-start、quantity-edit、quantity-prompt、quantity-run、quantity-output ｜ 教材；claims.md 實跑紀錄 ｜ CONFIRMED（卡片 4 行，與 caption 相符） ｜ — |
| 24 ｜ 三家單價適用 10–20 張；甲、丙運費範圍內固定；乙免運 ｜ quantity-ranges（sxtz、rgr9） ｜ 三家 PDF 第2頁 ｜ CONFIRMED（逐字原句只摘到 birch，另兩家見最後一節） ｜ — |
| 25 ｜ 甲二十張：3,780＋210＝3,990 ｜ quantity-aster、quantity-ranking ｜ 重算 ｜ CONFIRMED；不是十張的兩倍（4,200），v2vk 成立 ｜ — |
| 26 ｜ 乙二十張：4,100；甲乙名次相對十張反轉 ｜ quantity-birch（pruf） ｜ 重算 ｜ CONFIRMED ｜ — |
| 27 ｜ 丙修訂版二十張：3,675＋262.50＝3,937.50，最低 ｜ quantity-cedar、quantity-ranking（cbe9、nvu3） ｜ 重算 ｜ CONFIRMED ｜ — |
| 28 ｜ 交付：可編輯比價表、待問清單、版本變動清單 ｜ handoff-start、handoff-output ｜ brief、claims.md ｜ CONFIRMED ｜ — |
| 29 ｜ 掃描圖片時抽取結果可能是空的；本流程不做 OCR ｜ handoff-scan、description ｜ pypdf 頁："the extracted text may be minimal or visually empty"、"pypdf is not OCR software." ｜ CONFIRMED ｜ — |
| 30 ｜ 表格／多欄排版可能把數字接錯 ｜ handoff-table ｜ pypdf 頁："Typically, tables are just absolutely positioned text… That makes it hard to tell where columns / rows are." ｜ CONFIRMED ｜ — |
| 31 ｜ 「實跑 2026-10-26」 ｜ quantity-run caption、quantity-output source ｜ claims.md 的相對命令、stdout winners、selected-comparison 紀錄 ｜ CONFIRMED（有執行證據紀錄，不是預期結果） ｜ — |
| 32 ｜ 縮圖「先算總價／稅與運費別漏算」 ｜ thumbnail ｜ — ｜ CONFIRMED（與內容一致） ｜ — |
| 33 ｜ youtube.title「最低單價，真的最便宜？」 ｜ youtube.title ｜ 重算 ｜ CONFIRMED（十張時單價最低的丙不是最便宜） ｜ — |
| 34 ｜ description 的日期、工具角色、不宣稱測試商用產品上傳介面 ｜ youtube.description ｜ pypdf、openpyxl 頁；brief ｜ CONFIRMED ｜ — |
| 35 ｜ tags、outro CTA、開場鉤子 ｜ youtube.tags、outro、opening ｜ — ｜ OUT OF SCOPE ｜ — |

## 計數

- CONFIRMED 31
- OUT OF SCOPE 4
- CHANGED 0
- NOT FOUND 0

video.json 未修改。

## 規則檢查

- 免責語家族（以官網為準、公告沒寫、我不唸、不在這裡唸、不替你填、「公告沒寫，不代表沒有」）在旁白與 description 中都沒有出現。
- 查證用語「經查證」「根據官方文件」「截至查證」「本影片」在旁白中沒有出現。
- 沒有財務、稅務、法律建議：稅率標明是計算假設（need-fiction、description）。
- 沒有個人資料。
- 沒有虛構站主經驗。
- 片中沒有介面元素名稱。
- payload 沒有站主的常設指示段落，旁白也沒有使用敘事者名字或口號，符合規則。

## 即將過期

- 片中金額全是原創 fixture，沒有會過期的價格。
- pypdf（6.21.2）與 openpyxl（3.1.3）的行為描述以 2026-10-26 讀到的版本為準，套件改版後要重讀。

## 觀點不符

無。旁白沒有未標示的站主觀點，所有立場都是流程建議。這些建議符合站主觀點 1、3、4、6、7：先算清實際成本、AI 整理後回原文核對、只報本次實際執行的成果。

## 懷疑但未改

- **sxtz「三份報價都寫明，單價在範圍內保持相同」與 quantity-ranges 的「範圍內固定」運費**：逐字原句只確認到 birch 第2頁。aster.pdf 與 cedar-revised.pdf 第2頁全文仍未摘入 claims.md。程式依範圍重算，21 張被拒絕，語意成立，所以未改。
- **requirements.txt 全文仍未摘入**：need-spec、need-delivery 依前輪的逐字比對紀錄採信。
- **八頁 PDF 原件摘錄沒有附在本輪 payload**：三張引言卡的原句與 fixture 值，依 claims.md 紀錄、重算與跨卡一致性判定。
- **quantity-run／quantity-output 標「實跑」**：本輪 payload 沒有附原始 stdout 或 selected-comparison.json，成片前要對照 lab receipts 做視覺核對。
- **建議**：下輪 payload 附上 PDF 第2頁全文、requirements.txt 與 stdout，讓上面四項可以直接核對。
