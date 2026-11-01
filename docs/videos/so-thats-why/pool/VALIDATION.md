# 第九批素材池驗證：2,757筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)。

46提案經非作者逐題編輯覆核，0合併、0暫緩，新增46核心。舊2,711入選及3,069raw全留、未改；新增2711雜湊快照，editorial豁免仍止於2000。當期raw 3115、合併後核心2986、可選2816、入選2757、別名129、候補59；高相似待處理0不代表無漏合。

本批45不同來源URL、45首次加入；入選使用2308 URL／4143題來源關係。來源的實讀範圍與讀法見批次和審閱，不把題級篩選當完整稿逐句核准。處置見[集中紀錄](reviews/wave9-editorial-integration.json)。

新增10題組、累計98，正文1:50–4:20未試讀。舊題組只有G79改為85秒/279字完整旁白文字，其餘87不變；G79兩核心不重算素材。每個核心同片合計驗上限。G59和既有小樣未改、未重跑；本批實際試讀、新媒體均0。

相關Node **38/38**、Python **2/2**通過；pool/series、473既有長片及2,287任務格式通過。實際Git index blob、資料/來源反查及連結檢查見[最終收據](reviews/wave9-final-validation.json)，[非作者最終讀回](reviews/wave9-final-independent-readback.json)另列獨立範圍。

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

無關任務警告不代改；沒有宣稱本機跑API/web完整CI。

| 單次本機動作 | 實測 |
| --- | --- |
| 詞面相似候選 | 3247.6 ms |
| 索引匯入 | 2643.5 ms |
| 同快照重匯 | 197.7 ms；UNCHANGED／0 writes |
| SQLite | 42,733,568 bytes |
| RSS快照 | 416,153,600 bytes |

只是當期真實資料一次測量，不是延遲分位數、萬筆／十萬筆壓測。最終語意3115raw，新建0向量、2.381秒，新增截斷0；快取命中非冷啟動，歷史截斷限制保留。

本批未新增人工合併對，不據此推論沒有漏合。每題top5近鄰及作者指定相近對交非作者讀機制/條件，沒有因本批調門檻。本批新增暫緩與新別名集合為空，不把空集合說成測過負向排除或新增別名。瀏覽器核入選數、分頁、歷史別名、來源欄位、G37/G59/G79及新題組、桌面／390px手機；3張截圖由root查看，不能代表觀眾看懂。詳[瀏覽器收據](reviews/wave9-browser-qa.json)。

距10k差7,243。完整影片包、試讀、觀眾測試、獨立品質抽樣及大規模效能仍待完成；無正式寫入、付費媒體、製作或發布。
