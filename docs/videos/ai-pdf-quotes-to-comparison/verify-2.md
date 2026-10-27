# 第 2 輪事實查核（verify-2.md）

查核日：2026-10-26。範圍：video.json 全部 lines 的 text、各 slide data、thumbnail、youtube.title、description、tags。

證據來源分兩類。
- 官方頁（今日讀取，ok=true）：pypdf Extract Text、openpyxl Simple Formulae。
- 本片原創 fixture 原文與實跑收據：claims.md 內的八頁逐字摘錄、lab-comparison 三情境輸出、相對命令 stdout。

所有金額都是原創練習設定，不來自官方頁，所以卡片標示「原創練習｜…」或「實際計算｜…」，不需要「官網 YYYY-MM-DD」。payload 內沒有失敗的 fetch，也沒有 mokaair.com 文章。Kevin Stratvert 與 FableGuide 是第三方頁，沒有用來確認任何數字，影片也沒有引用它們。

| # | claim | where | URL | verdict | before → after |
|---|---|---|---|---|---|
| 1 | 甲 180 未稅、乙 205 含稅、丙 175 未稅 | opening-unit；cost-unit-baseline；missing-known；revision-diff | aster/birch/cedar.pdf 第1頁摘錄 | CONFIRMED | — |
| 2 | 需求：10 張 A6 105×148、350 gsm 霧面白卡、雙面全彩同稿、同址、7 工作天；比送達含稅總價 | need-start；need-spec；need-delivery；ddpd | requirements.txt 第7–9行（claims 記錄 exact string equality 通過）；三份 PDF 規格原文 | CONFIRMED | — |
| 3 | 三份原檔 aster/birch/cedar.pdf 保留，輸出另存 | need-labels；74dc | generation-receipt；相對命令輸出在 repo 外 | CONFIRMED | — |
| 4 | 供應商、金額、5% 稅率皆為虛構練習 | need-fiction；description | requirements.txt 第1–5行；PDF fictional 註記 | CONFIRMED | — |
| 5 | 流程：文字 PDF 抽文 → AI 讀逐頁原文 → 精確小數計算後寫表；Codex 分析、pypdf、Decimal、openpyxl | need-route；description | ai-analysis-execution 身分；https://pypdf.readthedocs.io/en/stable/user/extract-text.html | CONFIRMED | — |
| 6 | 甲單價與商品稅在第1頁，運費 200 未稅及其 5% 稅在第2頁；原句 "Shipping: TWD 200.00 excluding tax to the specified address" | need-proof；extract-aster；extract-aster-quote | aster.pdf 第1–2頁摘錄（逐字相符） | CONFIRMED | — |
| 7 | 七行 viewer-prompt 全文；欄位定義 | extract-core；extract-fields | viewer-prompt.txt（442 bytes，root 逐字比對相等） | CONFIRMED | — |
| 8 | 乙 205 含 5% 商品稅、運費 0 送達免運、交期 5 個工作天 | extract-birch；mdte；q7x8 | birch.pdf 第1–2頁摘錄 | CONFIRMED | — |
| 9 | 丙原版 "Shipping: not quoted"，shipping_amount 保留 null | extract-missing-quote；extract-null；missing-known | cedar.pdf 第2頁摘錄；lab-comparison original-10 運費 null | CONFIRMED | — |
| 10 | 單價排序 丙→甲→乙 | cost-start；cost-unit-baseline | 175<180<205；baseline-and-normalized-order | CONFIRMED | — |
| 11 | 甲 10 張：1,800＋90＋210＝2,100 | cost-aster-formula；cost-initial-result | 重算 10×180、×5%、200×1.05；lab-comparison | CONFIRMED | — |
| 12 | 乙 10 張：10×205＝2,050，運費 0，不二次加稅 | cost-birch-formula；cost-initial-result | birch "No second goods tax is added…" | CONFIRMED | — |
| 13 | 原始 10 張：乙 2,050 低於甲 2,100；丙待確認 | cost-initial-result；bcr5；tnrc | lab-comparison original-10；stdout winners Birch | CONFIRMED | — |
| 14 | Decimal 計算，不先四捨五入單價 | cost-rounding | build_comparison.py；verification 17/17 | CONFIRMED | — |
| 15 | 試算表寫入已算值與來源；openpyxl 不計算公式；改需求要重跑 | cost-workbook；description | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html "openpyxl never evaluates formula" | CONFIRMED | — |
| 16 | 已含稅小計不可再加稅 | cost-total-check | birch 第1頁原文 | CONFIRMED | — |
| 17 | 給丙的詢問草稿未寄出 | missing-question；missing-no-send | questions.txt；未寄出 | CONFIRMED | — |
| 18 | 狀態欄分類（條件完整／費用缺漏／規格不同） | missing-status | 原創教學建議 | OUT OF SCOPE | — |
| 19 | 修訂版原句 "Replaces CED-1026-v1; not an additional supplier."；仍為三家 | revision-start；revision-identity | cedar-revised.pdf 第1頁摘錄 | CONFIRMED | — |
| 20 | 修訂改動：運費 待確認→250 未稅、運費稅→5%、單價 175 不變 | revision-diff | cedar-revised.pdf 第2頁 "Only delivery terms changed…" | CONFIRMED | — |
| 21 | 丙修訂 10 張：1,837.50＋262.50＝2,100.00，與甲同價 | revision-total；revision-ranking | 重算 10×175×1.05、250×1.05 | CONFIRMED | — |
| 22 | 修訂後 10 張乙 2,050 最低，甲丙 2,100 同價 | revision-ranking；dyun | lab-comparison revised-10 | CONFIRMED | — |
| 23 | 來源欄改指向修訂版 | revision-links | selected-comparison 來源 cedar-revised.pdf | CONFIRMED | — |
| 24 | request-20.json 第1–4行全文；quantity 20、scenario revised | quantity-edit；quantity-output | 46 bytes 逐字重算相符；selected-comparison.json | CONFIRMED | — |
| 25 | 畫面命令（5 行續行）於 materials 實跑 2026-10-26，exit 0 | quantity-run | lab-relative-command-execution argv 逐字相符 | CONFIRMED | — |
| 26 | 三家適用 10–20 張；甲 200 未稅固定、乙免運、丙修訂 250 未稅固定 | quantity-ranges；sxtz；rgr9 | 三家第2頁摘錄 | CONFIRMED（見「懷疑但未改」） | — |
| 27 | 甲 20 張：3,780＋210＝3,990 | quantity-aster；quantity-ranking | 重算 20×180×1.05 | CONFIRMED | — |
| 28 | 乙 20 張：20×205＝4,100 | quantity-birch；quantity-ranking | 重算 | CONFIRMED | — |
| 29 | 丙修訂 20 張：3,675＋262.50＝3,937.50，最低 | quantity-cedar；quantity-ranking；thumbnail「換人贏了」；title | 重算；stdout winners revised-20 Cedar | CONFIRMED | — |
| 30 | 輸出可編輯比價表、待問清單、版本變動清單 | handoff-output | 輸出檔清單 comparison.xlsx、questions.txt、change-log.json | CONFIRMED | — |
| 31 | 掃描影像抽文可能是空的，需改用辨識流程；本次流程不做 OCR | handoff-scan；description | pypdf："the extracted text may be minimal or visually empty… consider using OCR software"、"pypdf is not OCR software." | CONFIRMED | — |
| 32 | 表格與多欄排版可能接錯 | handoff-table | pypdf："tables are just absolutely positioned text… hard to tell where columns / rows are" | CONFIRMED | — |
| 33 | description 的 GitHub 連結（固定 commit） | description | 教材路徑 | CONFIRMED（payload 未抓取該頁，但連結不帶數字） | — |
| 34 | tags、片尾 CTA、留言提問 | tags；outro | — | OUT OF SCOPE | — |

## 計數
- CONFIRMED 31
- CHANGED 0
- NOT FOUND 0
- OUT OF SCOPE 3

video.json 沒有修改（video = null）。

## 即將過期的事實
- 官方文件版本與行為以 2026-10-26 讀取為準：pypdf 6.21.2 頁面、openpyxl 3.1.3 頁面。若未來版本加入 OCR 或公式計算，handoff-scan 與 cost-workbook 的說法要重查。
- 片中所有金額都是原創 fixture，不會過期。

## 觀點不符
- 腳本沒有出現未標示為站主的觀點。
- 敘事立場（先算清需求與成本、回原文核對、只報實際執行結果）與站主觀點 1、3、4、6、7 一致。
- 片中沒有自稱站主的經驗或習慣。
- 「以官網為準」這一類免責語在旁白中出現 0 次。

## 懷疑但未改
- sxtz「這三份報價都寫明，單價在這段數量範圍內保持相同」：只有 birch 第2頁的摘錄逐字寫出 "unit price stays the same in this range"。aster 與 cedar-revised 的摘錄只有 "Quantity range: 10 to 20 pieces inclusive"，而且摘錄已註明省略其他段落。程式與 AI 都依此範圍重算，21 張被拒絕，語意上成立，所以不改。建議下一輪把兩份 PDF 第2頁全文摘入 claims，確認是否有同句。
- requirements.txt 第7–9行全文不在 payload 內，只能依 claims 記錄的 root exact string equality 結果採信。第1輪的待補事項（摘入第1–10行全文）仍然未完成。
- 「規格不同」是條件式範例，本次三家規格全部相同；卡片沒有暗示本次真的有不合規格的報價，所以不動。
