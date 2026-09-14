---
name: review-change
description: 審查指定練習 diff，回報有證據的正確性問題；用於要求檢查程式變更時。
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

讀取參數指定的 diff 檔案。參數：$ARGUMENTS。
若沒有指定檔案，請讀者提供，不自行選取整個專案。
只讀取練習材料，不修改、提交、上傳或建立 PR。
以本技能 templates/report.md 的欄位回報；每項發現要有具體行號、重現條件、影響與驗證狀態。
找不到證據時回報沒有已確認問題，不湊數。
