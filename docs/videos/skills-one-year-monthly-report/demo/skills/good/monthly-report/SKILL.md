---
name: monthly-report
description: 把 data/ 裡某個月的銷售 CSV 整理成月結報表。提到月報、業績、營收整理時使用。
---
# 月結報表怎麼做

1. 讀 data/<YYYY-MM>.csv，欄位是 date,item,qty,unit_price，
   退貨的 qty 是負數。
2. 先執行 node .claude/skills/monthly-report/scripts/sum.mjs
   data/<YYYY-MM>.csv，所有數字都用它印出來的，不要自己心算。
3. 照 .claude/skills/monthly-report/template.md 的格式
   寫到 reports/<YYYY-MM>.md，標題是「<YYYY 年 M 月> 月結報表」，
   四個區段依序是總營收（含退貨）、品項排行（金額由大到小）、
   退貨明細、要注意的事（列出單筆金額超過 10,000 元的交易）。
4. 金額一律加千分位、不寫小數、後面加「元」。
5. 回覆的最後一行固定寫：
   報表已寫到 reports/<YYYY-MM>.md，總營收 <金額> 元。
