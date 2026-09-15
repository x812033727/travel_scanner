# 82 搜尋引用

從 examples 根目錄執行：

```powershell
.venv/Scripts/python.exe 82/grounding-demo/main.py --fixture 82/response-fixtures/cited.json
```

輸出 citation-view.html，全為作者合成資料與示意元件。其他 fixture 測未搜尋、危險網址及中文位元組切割。具備金鑰與費用上限後才改 --live，不能同時用 --fixture。真實回應只留 RAM，終端機提供60秒內有效的單次本機檢視網址；不寫出真實 HTML 或回應檔。完整答案、引用與原始 Search Suggestions 一起顯示；不支援的主動 HTML 使整個 live 顯示停止，不移除 Google 元件冒稱完整展示。
