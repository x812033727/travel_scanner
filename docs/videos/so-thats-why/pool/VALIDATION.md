# 第七批素材池驗證：2,667筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)。

58原題經非作者逐題編輯覆核，0合併、0暫緩，新增58核心，舊2,609全保留。當期raw 3017、核心2896、可選2726、入選2667、別名121、候補59。高相似待處理0不代表沒有漏合。詳[集中處置](reviews/wave7-editorial-integration.json)。

本批60個不同來源URL、60首次加入；入選使用2220個URL／4030個題來源關係。來源閱讀範圍與修正綁定SHA保存；題級查核不是完整答案逐句核准。2,959舊raw未改寫，2609快照加入必讀registry，editorial欄位豁免仍止於2000。

新增9題組、累計78，正文2:40–4:35；新片及G59逐核心時間累計另驗。G59完整旁白草稿書面預算130秒，沒有新增核心、配音或試讀。原wave6 treatment及小樣保持原檔，未重跑；[稿件覆核](reviews/wave7-g59-narration-review.json)不取代聽眾、音訊或成片驗收。

相關Node測試36/36、Python2/2通過；pool/series、473既有長片及任務格式檢查通過。檢查命令：

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

檢查、Git index blob雜湊、題組預算及本地文件連結在[最終驗證收據](reviews/wave7-final-validation.json)。沒有宣稱重跑API/web全部測試；無關任務警告不代改。

| 單次本機動作 | 實測 |
| --- | --- |
| 詞面相似候選 | 1937.2 ms |
| 索引匯入 | 2568.0 ms |
| 再匯同快照 | 415.2 ms；UNCHANGED／0 writes |
| SQLite | 40,886,272 bytes |
| RSS快照 | 569,114,624 bytes |

搜尋、既有別名與來源反查均讀回；本批新增別名／暫緩集合為空；效能只是真實當期資料單次，非延遲分位數或萬筆／十萬筆壓測。最終語意輸入3017raw，新建0向量、2.341秒，新增截斷0；不是冷啟動耗時，歷史截斷限制仍存在。

本批無新增人工合併對，不計算已知合併命中率，也不因此宣稱全庫沒有漏合。另8組舊高分對由兩人比較條件後保留不同核心；未重開所有舊來源。未針對本批調相似度門檻。

[瀏覽器檢查](reviews/wave7-browser-qa.json)驗入選數、分頁、既有別名、來源與欄位（本批無新增合併或暫緩）、G37/G59及新題組、桌面及390px手機頁面。截圖人工查看結果寫在收據，程式通過不能代替觀眾看懂。

距10k還差7,333。完整影片劇本包、旁白試讀、觀眾測試、獨立品質抽樣與萬筆以上效能仍未完成。沒有正式資料寫入、付費媒體、製作或發布。
