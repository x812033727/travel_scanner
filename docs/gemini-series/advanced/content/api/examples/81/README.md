# 81 只讀工具呼叫

先依上一層 README 安裝；從 examples 根目錄執行：

```powershell
.venv/Scripts/python.exe 81/function-loop/main.py '查詢 DEMO-001 的數量與狀態' --live --output tool-observation.json
```

orders.json 只有兩筆合成資料。tool-cases.json 列出正常、查無、非法參數與循環案例。工具只有 lookup_order，不能修改或動態執行任意字串。真實請求最多三次、每回最多四個工具要求且有時間上限；檢查輸出的 status、trace、call_id 與 tool_results。工具成功與模型回答正確分開驗收。沒有金鑰與成本上限時只跑整批本機測試。
