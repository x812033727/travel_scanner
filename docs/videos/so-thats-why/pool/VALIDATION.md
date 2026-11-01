# 第四批素材池驗證：2,449筆

日期：2026-11-01；Node v24.19.0。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)。

## 資料與編輯

[集中處置](reviews/wave4-editorial-integration.json)：129原題逐題非作者覆核，4合併／4暫緩，新增121核心，舊2,328全保留。當期raw 2790、核心2673、可選2508、入選2449、別名117、候補59。高相似待處理0不代表沒有漏合。

食品29、建築34、交通50、文字16；外站是風險抽查，不是每項完整答案已核准。糖與水分作用、錯誤來源定位、雙葉牆過細模型及BOM舊題重複均已修訂並由原覆核者讀回。Failed fetch、摘要與作者副本讀回各自明列，不算全文重讀。

第四批91個不同研究URL，89個首次入庫；全庫3799，累計研究831，入選使用2054／3772題來源關係。來源合併保留閱讀origin與小節。舊2,661 raw改寫0、舊入選退休0；1k/2k/2328快照必讀且SHA檢查。

## 組片與實測

累計48組題組，新10組150–345秒。食物3片210／160／150秒，建築335／345秒，交通250／270／295秒，文字220／170秒。開場回扣計入總長；尚未試讀。短解說最低兩章的工具修正允許自然章數，但不自動判定內容好看；來源、時間、入選ID及非核准狀態檢查仍在。

G37 295→220秒、6→3素材，一份具體treatment由另一編輯覆核。受控小樣補上Worker內部完成時間與主執行緒接收事件後，started→timer→done及跨context先後檢查通過。單次回報約54.7／702.2／54.9ms，Worker本體約700.1ms；不含Worker啟動，不是總任務效能比較。相對卡片位移桌面180.375／0px、手機109.5／0px。兩版截圖已查看；沒有完整人聲、成片或觀眾測試。

文字探針5項通過；Node24.19/ICU78.3/Unicode17與閱讀UTS51 revision31的標準版本分開。未驗字型/ZWJ呈現、OCR或所有軟體。

## 檢查與真實資料效能

可重跑範圍：

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

相關測試結果：Node 33/33、Python 2/2通過，0失敗/取消/略過；pool及series check通過，既有473長片／2287任務格式檢查通過。既有無關任務警告未代改。。詳[驗證收據](reviews/wave4-final-validation.json)。未宣稱本機全套tools/docs-videos或API/web皆重跑。

| 當次動作 | 實測 |
| --- | --- |
| 詞面近似生成 | 2996.4 ms |
| 索引匯入 | 1738.5 ms |
| 同快照再匯入 | 263.1 ms；UNCHANGED／0 writes |
| SQLite | 37,736,448 bytes |
| RSS快照 | 540,676,096 bytes |

搜尋、4個新別名、4個暫緩題、Unicode來源反查相依題組皆已讀回。測量僅本機真實資料單次，不是延遲分位數、併發或萬筆／十萬筆壓測。當期語意輸入2790raw、增量建2向量、2.957秒；不能視為從零建立耗時。

[瀏覽器收據](reviews/wave4-browser-qa.json)驗入選數、50→100分頁、全部新合併／暫緩、U4011唯一正確來源、G37與10個新題組、390px手機無橫溢及零頁面錯誤；截圖人工確認狀態記在收據。manifest與Git staged blob、內部連結檢查亦記同一驗證收據。

沒有正式資料寫入、媒體製作或發布。10k目標仍差7,551；下一輪仍需以新機制、來源與試讀成果增加可用內容。
