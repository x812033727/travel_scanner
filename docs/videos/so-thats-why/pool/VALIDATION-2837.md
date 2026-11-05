# 第十一批素材池驗證：2,837筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)／[2,797](VALIDATION-2797.md)。

41提案，1合併／0暫緩，淨增40核心。舊2,797入選及3,160 raw保留，新增2797雜湊快照，共10個歷史快照；editorial豁免仍止於2000。當期raw 3201、核心3066、可選2896、入選2837、別名135、候補59。高相似待處理0不代表沒有漏合。

本批38來源URL／38首次加入，全庫4153、研究1194、入選使用2384／4243題來源關係。限定支持、來源風險抽查與失敗詳[集中處置](reviews/wave11-editorial-integration.json)所綁審閱；未核准所有舊完整答案與媒體授權。

新增12題案、累計122，正文1:40–3:10未試讀。同核跨章累計核上限。舊109題案不變，G108從110縮至80秒，259字完整旁白及原創虛構數字小樣由非作者核範圍、算術與刪段。小樣實核144有效／5無效輸入、3預設、鍵盤端點、桌面手機，root看2圖。完整旁白文字新增1份、互動小樣新增1個；實際試讀、錄音及新媒體皆0。G79/G59及其小樣未重跑。

相關Node **40/40**、Python **2/2**通過，無失敗／取消／略過；pool/series、473長片與2,287任務格式通過。無關任務警告未代改，未跑完整API/web CI。

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

| 單次本機動作 | 實測 |
| --- | --- |
| 詞面相似候選 | 5036.8 ms |
| 索引匯入 | 2574.4 ms |
| 同快照重匯 | 212.0 ms；UNCHANGED／0 writes |
| SQLite | 47,726,592 bytes |
| RSS快照 | 576,696,320 bytes |

目前真實資料的一次測量，不是延遲分位數或萬筆／十萬筆壓測。最終語意3201raw，新建0向量、2.181秒，新增截斷0；快取命中不是冷啟動，歷史截斷限制保留。本批1組新提案人工合併對，詞面找到0、語意top10找到1；為事先知道結果的非隨機小集合，不是全庫召回率。

每題top5、作者相近對與修改差異交非作者比較。本批新增暫緩為空，不把空集合算成負向排除測試。素材池瀏覽器核入選數、分頁、實際新合併與歷史別名、來源欄位、G37/G59/G79/G108及所有新題案、桌面與390px手機；3圖由root查看。詳[瀏覽器收據](reviews/wave11-browser-qa.json)。G108算術／介面另有[收據](reviews/wave11-g108-demo.json)，不是實證調查或真實學生資料。

[最終驗證收據](reviews/wave11-final-validation.json)保存實際Git index blob、連結、核心預算與來源反查；[獨立整合讀回](reviews/wave11-final-independent-readback.json)另列範圍，作者不自核自己寫的事實。

距10k差7,163。121筆舊題全文／附件、完整影片包、試讀、觀眾測試、品質抽樣及大規模效能仍待完成。無正式寫入、付費媒體、部署或發布。
