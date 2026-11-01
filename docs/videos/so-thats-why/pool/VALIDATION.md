# 第五批素材池驗證：2,546筆

日期2026-11-01；Node v24.19.0。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)。

## 資料與編輯

[集中處置](reviews/wave5-editorial-integration.json)：105原題逐題非作者覆核，4合併／4暫緩，新增97核心，舊2,449全保留。raw 2895、核心2774、可選2605、入選2546、別名121、候補59。高相似待處理0不代表沒有漏合。

身體36、紡織23、水工程27、影音19；外部來源為指定段落和風險抽查，不是完整答案逐主張核准。來源讀取失敗、研究者解釋、摘要和作者副本讀回都有紀錄。M5017補K頻率權重才與一般RMS分開；W5004補淨去磷的排泥出口；A5012修正迴路層次。暫緩題不出現在入選卡片或題組。

本批59個不同研究URL，56個首次加入全庫；全庫3855、研究888、入選使用2107／3889題來源關係。2,790舊raw改寫0；新2449快照加入必讀清單，新題欄位檢查仍從2000基線起算。

## 組片與實驗

新12題組，累計60；2:15–5:50正文預算含開場回扣。音量片205→135秒，移出的真峰值仍在素材池；FLAC使用M5008案例但核心計M5004，70秒只計一次且不加PNG原情境。逐核心累計上限及所有新題組篩選均另驗。

[FLAC探針](reviews/wave5-media-probe.json)固定自製訊號，indep/mid_side首框配置1/10；兩模式解碼皆與192,000 bytes原PCM一致，輸入含27,432組奇數左右和。輸出大小不能外推為普遍壓縮率，未證明預測器實際選擇，也沒有聽感或成片驗證。原G37受控示範與treatment保留，本次不重測、不新增完整稿。

## 檢查與效能

可重跑範圍：

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

相關Node測試34/34、Python2/2通過，0失敗／取消／略過；pool與series check、既有473長片與2287任務格式通過。Git staged blob雜湊和本地連結檢查記在[驗證收據](reviews/wave5-final-validation.json)。沒有宣稱API/web全套檢查皆重跑。既有無關任務警告不代改。

| 當次動作 | 單次實測 |
| --- | --- |
| 詞面近似生成 | 4280.8 ms |
| 索引匯入 | 1800.4 ms |
| 同快照再匯入 | 165.0 ms；UNCHANGED／0 writes |
| SQLite | 40,869,888 bytes |
| RSS快照 | 553,103,360 bytes |

肌肉／針織／污水搜尋、全部新別名與暫緩、FLAC來源反查相依題組已讀回。測量是本機真實資料單次，不是延遲分位數或萬筆／十萬筆壓測。最終語意輸入2895raw、新建2向量、3.322秒；不是冷啟動建向量耗時。

當批4個已知人工合併對：詞面找到1、語意top10找到0。樣本小且非隨機，不作全庫品質推論或用來調門檻。

[瀏覽器收據](reviews/wave5-browser-qa.json)驗入選數、50→100分頁、新別名／暫緩、M5013色度來源、G37及12個新題組、390px無橫溢及零頁面錯誤。桌面／手機截圖實際查看狀態記在收據。

沒有正式資料寫入、付費媒體、配音或發布。距10k仍差7,454；完整稿、試讀、獨立品質抽樣與規模驗證仍待後續。
