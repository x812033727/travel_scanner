# 本機驗證與未執行項目

2026-09-14，Windows、Python 3.13.15。解壓完整驗證包後，從根目錄執行 `python verification/test_materials.py`；只使用 Python 標準函式庫，不連線、不讀取帳號、不呼叫模型。

測試檢查人工評分紀錄的完整性、信件引用與未知欄位、摘要期間與來源狀態。成功不表示模型答案正確；內容意義仍須回到原始資料人工核對。程式會把實際測試數寫入 fixtures.json。

第 53 篇的 budget-reference.html 可直接用瀏覽器開啟。依 test-cases.csv 輸入三組數字，另試空白、文字、負值、小數人數、超出範圍、修改欄位後舊結果清除與重設。在 360 像素與桌面寬度檢查無水平捲動。作者的 verify-budget.mjs 使用專案既有 Playwright 執行本機 HTML，並保存 browser-budget.json 與兩張截圖。

尚待真實操作：51 的 20 份模型回答與人工評分、52 的 24 份 Gems 回歸輸出、53 的 Canvas 生成／修正過程、54 的 Workspace 帳號與交接操作、55 的 Android 和 iPhone 實機與電腦接續、56 的一次手動及一次真實排程、暫停／恢復／刪除及下一次觸發觀察。範本的 not_run 不能自行改為通過；沒有用合成輸出代替實測。

下載包中的照片依 examples/55/photo-license.json 的 CC0 1.0；其他作者練習檔依各篇 LICENSE.txt。範例信件、手冊、客服題庫與新聞測試資料均為作者合成。
