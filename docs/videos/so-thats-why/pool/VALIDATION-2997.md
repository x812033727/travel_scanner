# 第二十批素材池驗證：2,997筆

2026-11-02，Node v24.22.1。10提案新增9核心；1正式合併、0暫緩，另32方向未收。raw3366、核心3226、可選3056、入選2997、別名140、候補59。

舊3,356原題、2,988入選、208題案與來源閱讀保留；新增2988雜湊快照，共19個歷史快照。所有本批來源對核心及題案反查已核，不連外監控。

pool_physics與pool_life_tech各自撰寫後互換查核，詳[整合紀錄](reviews/wave20-editorial-integration.json)內的兩份非作者收據。root完成[中央檢查與定點來源抽查](reviews/wave20-central-checks.json)、文件及測試，不稱第三次整批逐主張核准。題級覆核不等於完整稿核准。

新增7題案正文1:30–2:25未試讀；逐核心跨章累計不超素材上限，節拍不超過45秒，已含開場轉場回扣。完整稿、試讀、小樣及媒體均0，舊小樣未重跑。

## 本機驗證

44個相關Node測試、2個Python測試通過；pool/series、473長片企劃及2287任務格式檢查通過。未改正式工具行為、未加重複固定筆數測試；既有無關任務警告保留。

```text
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

SQLite第二次匯入UNCHANGED／0 writes；搜尋、歷史別名、新來源連結及全部新題案篩選已核。1440×1000桌面、390×844手機及展開來源畫面由root目讀；無水平溢出或pageerror。

最終語意處理3366raw、新建向量0、新增截斷0、2.595秒。屬快取增量而非冷啟動或召回率。新題top5及作者近似對逐對判讀；本輪未另抽舊對舊，不推全庫無漏合。

[驗證收據](reviews/wave20-final-validation.json)記實際Git暫存blob、文件連結、來源映射與片長累計。本機相關檢查與完整雲端CI分開，不是成片驗收。

歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)／[2,797](VALIDATION-2797.md)／[2,837](VALIDATION-2837.md)／[2,870](VALIDATION-2870.md)／[2,897](VALIDATION-2897.md)／[2,921](VALIDATION-2921.md)／[2,939](VALIDATION-2939.md)／[2,959](VALIDATION-2959.md)／[2,977](VALIDATION-2977.md)／[2,982](VALIDATION-2982.md)／[2,988](VALIDATION-2988.md)。121歷史題完整刷新、真實萬筆／十萬筆、品質抽樣、試讀及採用仍未完；未購付費媒體，無完整模型帳單，不稱研究零成本。
