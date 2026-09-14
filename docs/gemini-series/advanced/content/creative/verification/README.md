# 創作批次的本機檢查

完整包解壓後執行 `python verification/test_materials.py`。使用標準函式庫，不連線或呼叫模型。二十項檢查包含資料清理基準、重複與衝突訂單、缺值、幣別、退款、大額訂單、日期、模型模式限制、日期變更依賴及未完成媒體紀錄。

單篇包可執行 `python creative_checks.py sales 67` 或 `python creative_checks.py affected 68`。完整包則將程式和資料夾加上 `examples/`。Flow 能力摘錄只對照 2026-09-14 官方文件，未驗證真實帳號介面；實際操作前重查模型、模式、長度與成本。

第 67 篇的 XLSX 使用 bundled Node 與 @oai/artifact-tool 製作，公式、四張頁籤與六個預覽已檢查，台幣總額 45,340、美元 50，分幣別。修改一筆單價會更新總額。儲存檔另檢查公式快取、日期型別、原始空值與圖表引用。尚未匯入 Google Sheets。

此 Windows bundled renderer 在完成預覽與 XLSX 匯出後的 native teardown 曾以 0xC0000005 結束。六張預覽已逐張檢視，最終相同版面使用 `build-workbook.mjs --skip-previews` 匯出並以 exit 0 完成；另行讀取儲存 ZIP／XML 核對，不以列印成功訊息忽略異常退出。

圖片是作者原創向量參考、刻意故障圖或分鏡，非模型輸出。第 63、64、65、66、68 篇所需的真實圖片、失敗生成案例、影片、版本與觀察仍待完成。瀏覽器回報 User unavailable，本次零模型呼叫、零影片生成、未發布。

程式與作者原創素材依各資料夾 MIT LICENSE。沒有第三方商品、人像或私人交易資料。
