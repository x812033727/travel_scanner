# 第十五批素材池驗證：2,939筆

日期2026-11-02；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)／[2,797](VALIDATION-2797.md)／[2,837](VALIDATION-2837.md)／[2,870](VALIDATION-2870.md)／[2,897](VALIDATION-2897.md)／[2,921](VALIDATION-2921.md)。

19提案，0合併／0暫緩，新收19；另1個舊核心改為合併變體，淨增18核心。64方向未收。舊2,921題保留2920個獨立核心與1個合併變體；3,287 raw原文不變，新增2921雜湊快照，共14個歷史快照，舊合併在適用checkpoint逐一聲明。當期raw 3306、核心3168、入選2939、可選2998、別名138、候補59。高相似待處理0不代表沒有漏合。

本批20來源URL／20首次加入，全庫4258、研究1299、入選使用2485／4354題來源關係。來源查讀及失敗範圍見[集中處置](reviews/wave15-editorial-integration.json)綁定的非作者收據；不代表全庫逐句事實或媒體權利已核准。

新增13題案，累計172，正文1:45–3:20尚未試讀；每個核心跨章累計核上限。159舊題案不變。G108仍259字80秒、G79仍279字85秒、G59仍506字130秒；本批完整稿、互動小樣、實際試讀與新媒體均0，舊小樣未重跑。

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
| 詞面相似候選 | 23602.6 ms |
| 索引匯入 | 18087.1 ms |
| 同快照重匯 | 624.6 ms，UNCHANGED／0 writes |
| SQLite | 48,058,368 bytes |
| RSS快照 | 363,446,272 bytes |

是目前真實資料一次測量，不是延遲分位數或萬筆／十萬筆壓測。最終語意3306raw，新建0向量、3.66秒，新增截斷0；快取命中不算冷啟動，歷史截斷限制保留。本批新提案沒有人工合併對，不能從空集合推論全庫無重複。另從舊入選未明列distinct的語意近鄰取最高6對，另加1對來源閱讀延伸比較，兩人判讀後合併1對，其餘保留；這是刻意挑選的比較，不是隨機品質估計。詳[舊題抽查](reviews/wave15-old-pair-integration.json)。

共同top5與作者近似對由非作者逐題比較。瀏覽器核入選數、分頁、歷史別名N098/L042與本批實際新增的合併別名、來源欄位、G37/G59/G79/G108及所有新題案篩選、1440px桌面及390px手機；3圖root實看，詳[收據](reviews/wave15-browser-qa.json)。新增合併別名已逐個核對。本批無新增暫緩列，未執行負向列排除斷言。

[最終驗證收據](reviews/wave15-final-validation.json)用於記錄實際Git index blob、連結與新題案核心總秒數，請依分項狀態判讀；[獨立整合讀回](reviews/wave15-final-independent-readback.json)綁定穩定檔與tests物件，作者不自核自身事實。editorial豁免仍止於2000。

距10k差7,061。121筆舊題完整答案／附件、品質抽樣、完整稿與試讀、採用回寫、大規模效能仍未完成。無正式寫入、付費媒體、部署或發布。
