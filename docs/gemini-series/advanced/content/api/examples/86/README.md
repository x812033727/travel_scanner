# 86 本機文件助手

從examples根目錄執行：

```powershell
$env:GEMINI_LAB_LIVE='0'
.venv/Scripts/python.exe -m uvicorn app:app --app-dir 86/document-service --host 127.0.0.1 --port 8765
```

開啟 http://127.0.0.1:8765 ，查S003容量預期260，點來源核對全文，再返回；S011應缺證據。另開終端機執行：

```powershell
.venv/Scripts/python.exe 86/document-service/evaluate.py --output service-fixture-evaluation.json
```

20題通過只證明作者資料流。真實模式需GEMINI_API_KEY、GEMINI_STORE_NAME、GEMINI_LAB_LIVE=1，停止原程序重啟；evaluate另需--live。不自動讀.env，.env.example只供參考。

索引必須是自己的十份目前v1規格，與documents.json全文一致；若83已更新v2，先同步本機對照與golden題庫或另建v1索引。模型只有File Search，/orders/DEMO-001另提供只讀合成訂單，不讓模型修改。

引文存在仍需核對主張；單人本機教材沒有多人登入/正式部署。Ctrl+C停止後依83/84/85各帳本清理雲端資源，帳單另查，不把作者測試寫成真實Gemini評測。
