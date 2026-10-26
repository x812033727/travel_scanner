# verify-8.md｜ai-pdf-quotes-to-comparison｜獨立事實查核（2026-10-26，第8輪）

範圍：video.json 全部 55 場景的旁白 text、slide data、thumbnail、youtube.title／description／tags，以及 sources 清單。本片的金額、稅率、頁碼與數量全部來自原創虛構練習 PDF，不是產品官方數字。核對依據有三類：
- claims.md 內逐字貼出的八頁 pypdf 抽文、requirements.txt、viewer-prompt.txt、request-*.json、questions-21.txt。
- 實跑收據：comparison.json、selected_result、quantity-21 receipt。
- 工具行為以今日成功抓取的官方頁核對：pypdf 頁 200、openpyxl 頁 200。

本片屬於「製作路線：教學卡片」，所有示範都另外對照了輸入、動作與實跑證據。

## 逐項結果

| # ｜ claim ｜ where ｜ URL ｜ verdict ｜ before → after |
|---|---|---|---|---|
| 1 ｜ 甲180未稅／乙205含稅／丙175未稅 ｜ opening-unit 表；xnrg ｜ aster/birch/cedar.pdf p1 抽文 ｜ CONFIRMED ｜ — |
| 2 ｜ 需求：10張 A6 105×148、350gsm 霧面白卡、雙面全彩、同地址、7工作天 ｜ need-spec code（第7–8行）、ddpd ｜ requirements.txt 第7–8行（逐行計數吻合） ｜ CONFIRMED ｜ — |
| 3 ｜ 第8–9行節錄與「送達總價不是單價」 ｜ need-delivery code、d8h7、jfix ｜ requirements.txt 第8–9行 ｜ CONFIRMED ｜ — |
| 4 ｜ 原檔 aster/birch/cedar.pdf 保留、輸出另存 ｜ need-labels ｜ requirements.txt 末行；c3 收據 ｜ CONFIRMED ｜ — |
| 5 ｜ 供應商、金額、5%稅率皆虛構 ｜ need-fiction；description ｜ 每頁 Fictional training quote 註記；requirements.txt 第3–5行 ｜ CONFIRMED ｜ — |
| 6 ｜ 抽文→AI欄位→精確小數計算 ｜ need-route；description ｜ c5 收據；analysis-execution JSON ｜ CONFIRMED ｜ — |
| 7 ｜ 甲單價在p1、送貨條件在p2 ｜ need-proof、extract-aster、fd27 ｜ aster.pdf p1/p2 ｜ CONFIRMED ｜ — |
| 8 ｜ 兩頁文字連同需求交給AI ｜ extract-start ｜ analysis-execution inputs 1–3 ｜ CONFIRMED ｜ — |
| 9 ｜ 七行提示詞全文 ｜ extract-core code「第1–7行｜全文」 ｜ viewer-prompt.txt（逐字一致） ｜ CONFIRMED ｜ — |
| 10 ｜ 甲：單價180未稅p1、商品稅5% p1、運費200未稅p2 ｜ extract-aster 表 ｜ aster.pdf p1/p2 ｜ CONFIRMED ｜ — |
| 11 ｜ 引句「Shipping: TWD 200.00 excluding tax to the specified address」 ｜ extract-aster-quote ｜ aster.pdf p2 逐字 ｜ CONFIRMED ｜ — |
| 12 ｜ 乙：205含稅p1、運費0免運p2、交期5工作天p2 ｜ extract-birch、mdte、q7x8 ｜ birch.pdf p1/p2 ｜ CONFIRMED ｜ — |
| 13 ｜ 丙p2「Shipping: not quoted」 ｜ extract-missing-quote、extract-null（page 2） ｜ cedar.pdf p2 逐字 ｜ CONFIRMED ｜ — |
| 14 ｜ 單價排序 丙→甲→乙 ｜ cost-start、cost-unit-baseline、35fs ｜ baseline-and-normalized-order.json ｜ CONFIRMED ｜ — |
| 15 ｜ 甲10張 1,800+90+210=2,100 ｜ cost-aster-formula ｜ comparison.json original-10；aster p1/p2 ｜ CONFIRMED ｜ — |
| 16 ｜ 乙10張 2,050，不重複加商品稅 ｜ cost-birch-formula ｜ birch p1「No second goods tax…」；comparison.json ｜ CONFIRMED ｜ — |
| 17 ｜ 十張：甲2,100.00、乙2,050.00、丙待確認 ｜ cost-initial-result、bcr5、tnrc ｜ comparison.json original-10 ｜ CONFIRMED ｜ — |
| 18 ｜ 工作簿只有已算值，不是會重算的公式；openpyxl 只寫檔 ｜ cost-workbook、ehby；description ｜ https://openpyxl.readthedocs.io/en/stable/simple_formulae.html「openpyxl never evaluates formula」；lab-execution xlsx 說明 ｜ CONFIRMED ｜ — |
| 19 ｜ 丙商品比乙便宜，運費夠低就會翻轉 ｜ e86a ｜ comparison.json：丙 goods_gross 1837.50 < 乙 2050.00 ｜ CONFIRMED（邏輯成立） ｜ — |
| 20 ｜ 丙已知：175未稅、商品稅5%、適用10–20；未知：運費、含稅狀態、稅額 ｜ missing-known、j2ja ｜ cedar.pdf p1/p2 ｜ CONFIRMED ｜ — |
| 21 ｜ 詢問草稿未寄出 ｜ missing-question、missing-no-send ｜ c17（草稿、無回覆） ｜ CONFIRMED（措辭沒有說已寄出） ｜ — |
| 22 ｜ 狀態欄三分類（規格不同屬條件式示例） ｜ missing-status ｜ c18 ｜ OUT OF SCOPE（教學建議） ｜ — |
| 23 ｜ 引句「Replaces CED-1026-v1; not an additional supplier.」 ｜ revision-identity、mrmd ｜ cedar-revised.pdf p1 逐字 ｜ CONFIRMED ｜ — |
| 24 ｜ 修訂：運費250未稅、運費稅5%、單價仍175未稅 ｜ revision-diff、hiqk ｜ cedar-revised.pdf p1/p2；「Only delivery terms changed」 ｜ CONFIRMED ｜ — |
| 25 ｜ 丙修訂10張 1,837.50+262.50=2,100.00 ｜ revision-total、ambg ｜ comparison.json revised-10 ｜ CONFIRMED ｜ — |
| 26 ｜ 十張：乙2,050.00最低，甲丙2,100.00同價 ｜ revision-ranking、dyun、u9p4 ｜ comparison.json revised-10；revised_10_groups ｜ CONFIRMED ｜ — |
| 27 ｜ 來源欄改指向修訂版 ｜ revision-links ｜ revised-10 price/shipping_source = cedar-revised.pdf ｜ CONFIRMED ｜ — |
| 28 ｜ request-20.json 第1–4行全文 ｜ quantity-edit ｜ materials/request-20.json 逐字 ｜ CONFIRMED ｜ — |
| 29 ｜ materials 資料夾執行的命令（實跑 2026-10-26） ｜ quantity-run code、6wkf、74dc ｜ lab-relative-command-execution：cwd materials、argv 逐字、exit 0、另存 comparison-output ｜ CONFIRMED（有實跑證據） ｜ — |
| 30 ｜ 輸出：數量20、修訂版、甲乙丙修訂版共3列 ｜ quantity-output ｜ selected_result（request quantity 20 / revised；3 rows，Cedar 來源為 cedar-revised.pdf） ｜ CONFIRMED（有實跑證據） ｜ — |
| 31 ｜ 三家單價皆適用10–20；甲200、丙修訂250在範圍內固定；乙免運 ｜ quantity-ranges、sxtz、rgr9 ｜ aster p2、birch p2、cedar-revised p2 ｜ CONFIRMED ｜ — |
| 32 ｜ 甲20張 3,780+210=3,990 ｜ quantity-aster ｜ revised-20 ｜ CONFIRMED ｜ — |
| 33 ｜ 乙20張 4,100；甲乙差距反轉 ｜ quantity-birch、pruf ｜ revised-20（10張乙低，20張甲低） ｜ CONFIRMED ｜ — |
| 34 ｜ 丙修訂20張 3,675+262.50=3,937.50 ｜ quantity-cedar ｜ revised-20 ｜ CONFIRMED ｜ — |
| 35 ｜ 二十張：丙3,937.50最低、甲3,990.00、乙4,100.00 ｜ quantity-ranking、cbe9、nvu3 ｜ revised-20；verification winners ｜ CONFIRMED ｜ — |
| 36 ｜ request-21-invalid.json 全文；命令只換需求檔與輸出夾 ｜ range21-request、range21-run ｜ materials 檔；quantity-21 receipt argv ｜ CONFIRMED ｜ — |
| 37 ｜ 拒絕計算「ValueError: Quantity outside explicitly quoted range」，沒有建立資料夾 ｜ range21-result、9jiq、egmv ｜ quantity-21 receipt：exit 1、output_directory_created=false ｜ CONFIRMED（有實跑證據） ｜ — |
| 38 ｜ 21張重報詢問句 ｜ range21-question ｜ questions-21.txt 逐字 ｜ CONFIRMED（草稿，尚未寄出） ｜ — |
| 39 ｜ description：文字 PDF、不做掃描 OCR ｜ youtube.description ｜ https://pypdf.readthedocs.io/en/stable/user/extract-text.html「pypdf is not OCR software」 ｜ CONFIRMED ｜ — |
| 40 ｜ description：Codex 分析也讀了 analysis-prompt.txt 契約，沒有實測商用 AI 上傳介面 ｜ youtube.description ｜ analysis-execution inputs、not_read_or_used ｜ CONFIRMED ｜ — |
| 41 ｜ title、thumbnail（先算總價／稅與運費別漏算）、tags ｜ youtube、thumbnail ｜ — ｜ CONFIRMED／OUT OF SCOPE ｜ — |
| 42 ｜ video.sources 兩頁 checked_on 2026-10-26 ｜ sources ｜ 兩頁今日皆為 200 ｜ CONFIRMED ｜ — |

## 統計

- CONFIRMED：41
- OUT OF SCOPE：1
- CHANGED：0
- NOT FOUND：0
- changed_facts = 0，video 不變（null）。

## 檢查規則

- 「以官網為準」整個家族：旁白與 description 都沒有出現。
- 查證字眼（經查證、本影片等）：沒有進入旁白。
- 個人資料：沒有。

## 即將到期的事實

- 四份練習報價都寫明「Valid … through 2026-11-30」（虛構教材，片中沒有唸出）。
- 官方頁今日版本標籤為 pypdf 6.21.2 與 openpyxl 3.1.3 documentation，片中沒有引用任何版本號。
- 若日後在片中加入版本號，需要重新查核。

## 觀點不符

無。片中沒有「我的看法是／以我的用法」的站主觀點，也沒有未標記的主觀評價。整體立場符合站主觀點：先算實際成本、回原文核對、只報真正執行的成果。

## 懷疑但未更動

1. **7dp4「把數量改成二十」：** 教材已附 quantity=20 的 request-20.json，命令讀的也是這個檔，可以理解為觀眾自行修改 request.json。屬於措辭問題，不是事實錯誤，未改。
2. **quantity-ranges 的來源寫「三家 PDF 第2頁」：** 丙實際取自 cedar-revised.pdf 第2頁（第四個檔案）。卡片標題寫「丙修訂版」，供應商仍是三家，不構成錯誤，未改。
3. **sources 中兩筆 404：** 兩個網址被誤接全形註記（「（2026-10-26」）。正確網址同時抓取成功，不影響任何結論。
4. **description 的 GitHub 連結：** 不在 sources 內，無法核對內容，未改。
5. **ledger 的 c2 寫「第7–10行」，卡片節錄第7–8與第8–9行：** 兩者是包含關係，不衝突。
