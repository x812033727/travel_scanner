# API 深入練習 81–86

全部合成資料由作者建立，MIT 授權見各篇 LICENSE。程式固定 google-genai 2.23.0；Python 支援版本依套件要求，本次實測 3.13.15 / Windows。沒有真實模型回應、帳密或已建立的 Google 資源。

單篇包解壓後包含篇號、lablib 與 requirements.txt。整批包多一層 examples 與 verification；下面安裝與單篇命令從 examples 目錄執行。

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

macOS/Linux 將 .venv/Scripts/python.exe 改成 .venv/bin/python；本批未在這兩個平台實跑。六篇文章附有完整操作步驟。沒有 --live 的查詢或送件 CLI 不會執行 Google 請求；86 服務另由 GEMINI_LAB_LIVE=1 啟用。

真實模式在自己的環境設定 GEMINI_API_KEY（不可寫入程式或公開包），GEMINI_MODEL 預設 gemini-3.8-flash。先核對帳號模型權限與本次成本上限。81–83 與86 問答採 Interactions；84 隱含快取同樣採 Interactions，手動快取與85 Batch 採 generateContent。兩種格式不可混用。

整批測試從外層目錄執行，使用剛建立的環境：
```powershell
examples/.venv/Scripts/python.exe -X utf8 verification/test_materials.py
```
測試使用真實 SDK 對本機 HTTP 服務及作者合成資料，不讀金鑰、不測雲端生成品質。fixture 模式的 service-evaluation.json 也不能當作雲端問答成績。

所有 ledger 都供單人依序操作。建立/上傳/送件逾時先核對原 ID，不要刪掉帳本重送。完整收據與實際驗收限制見原教學。下載包不提供正式多人服務、付費排程或生產環境部署設定。

