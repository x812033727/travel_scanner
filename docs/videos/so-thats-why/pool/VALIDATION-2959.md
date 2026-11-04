# 第十六批素材池驗證：2,959筆

日期2026-11-02；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)／[2,797](VALIDATION-2797.md)／[2,837](VALIDATION-2837.md)／[2,870](VALIDATION-2870.md)／[2,897](VALIDATION-2897.md)／[2,921](VALIDATION-2921.md)／[2,939](VALIDATION-2939.md)。

20提案，0合併／0暫緩，新收20；另0個舊核心改為合併變體，淨增20核心。59方向未收。舊2,939題保留2939個獨立核心與0個合併變體；3,306 raw原文不變，新增2939雜湊快照，共15個歷史快照，舊合併在適用checkpoint逐一聲明。當期raw 3326、核心3188、入選2959、可選3018、別名138、候補59。高相似待處理0不代表沒有漏合。

本批20來源URL／20首次加入，全庫4278、研究1319、入選使用2505／4375題來源關係。來源查讀及失敗範圍見[集中處置](reviews/wave16-editorial-integration.json)綁定的非作者收據；不代表全庫逐句事實或媒體權利已核准。

新增13題案，累計185，正文1:45–3:25尚未試讀；每個核心跨章累計核上限。舊G09日食題由11:00縮為3:05；混合食N252移出本片但留在素材池，其餘171舊題案不變。G108仍259字80秒、G79仍279字85秒、G59仍506字130秒；本批完整稿、互動小樣、實際試讀與新媒體均0，舊小樣未重跑。

相關Node **44/44**、Python **2/2**通過，無失敗／取消／略過；pool/series、473長片、2,287任務格式通過。無關任務警告未代改，未跑完整API/web CI。

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
| 詞面相似候選 | 18632.2 ms |
| 索引匯入 | 10419.4 ms |
| 同快照重匯 | 1146.2 ms，UNCHANGED／0 writes |
| SQLite | 48,181,248 bytes |
| RSS快照 | 393,936,896 bytes |

是目前真實資料一次測量，不是延遲分位數或萬筆／十萬筆壓測。最終語意3326raw，新建0向量、3.223秒，新增截斷0；快取命中不算冷啟動，歷史截斷限制保留。本批新提案沒有人工合併對，不能從空集合推論全庫無重複。另從舊入選未明列distinct的語意近鄰取最高6對，兩人判讀後合併0對，其餘保留；這是刻意挑選的比較，不是隨機品質估計。詳[舊題抽查](reviews/wave16-old-pair-integration.json)。

共同top5與作者近似對由非作者逐題比較。瀏覽器核入選數、分頁、歷史別名N098/L042、來源欄位、縮編G09、G37/G59/G79/G108及所有新題案篩選、1440px桌面及390px手機；3圖root實看，詳[收據](reviews/wave16-browser-qa.json)。本批無新增合併別名，未執行新增別名斷言。本批無新增暫緩列，未執行負向列排除斷言。

[最終驗證收據](reviews/wave16-final-validation.json)用於記錄實際Git index blob、連結與新題案核心總秒數，請依分項狀態判讀；[獨立整合讀回](reviews/wave16-final-independent-readback.json)綁定穩定檔與tests物件，作者不自核自身事實。editorial豁免仍止於2000。

距10k差7,041。121筆舊題完整答案／附件、品質抽樣、完整稿與試讀、採用回寫、大規模效能仍未完成。無正式寫入、付費媒體、部署或發布。
