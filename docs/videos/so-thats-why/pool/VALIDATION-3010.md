# 第二十一批素材池驗證：3,010筆

2026-11-02，Node v24.22.1。13提案新增13核心；0合併、0暫緩，另45方向未收。raw3379、核心3239、可選3069、入選3010、別名140、候補59。

舊3,366原題、2,997入選、215題案與來源閱讀保留；新增2997雜湊快照，共20個歷史快照。本批來源對核心及題案反查已核，不連外監控。

三組作者與非作者角色見[整合紀錄](reviews/wave21-editorial-integration.json)。root負責中央資料、兩份其他作者來源定點閱讀與太空組撰寫；太空組由pool_physics覆核。詳[中央檢查](reviews/wave21-central-checks.json)，不稱root為第三次整批來源查核。題級覆核不等於完整稿核准。

新增11題案正文1:20–1:55，未試讀；每核心跨章累計不超素材上限，每節拍不超45秒。開場轉場回扣已含；完整稿、試讀、小樣與媒體均0，舊小樣未重跑。

## 本機驗證

44個相關Node測試、2個Python測試通過；pool/series、473長片企劃及2287任務格式檢查通過。未改正式工具行為或加重複固定筆數測試；既有無關任務警告保留。

```text
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

SQLite第二次匯入UNCHANGED／0 writes；搜尋、歷史別名、新來源及全部新題案篩選已核。1440×1000桌面、390×844手機與展開來源畫面由root目讀；無水平溢出或pageerror。

最終語意處理3379raw、新建0向量、新增截斷0、2.27秒。屬快取增量，不是冷啟動或召回率。65有向top5及49作者近似對逐對判讀，本輪未另抽舊對舊，不推全庫沒有漏合。

[驗證收據](reviews/wave21-final-validation.json)記來源映射、真實Git暫存blob、文件連結及片長累計。本機相關檢查與雲端CI分開，不是成片驗收。

歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)／[2,797](VALIDATION-2797.md)／[2,837](VALIDATION-2837.md)／[2,870](VALIDATION-2870.md)／[2,897](VALIDATION-2897.md)／[2,921](VALIDATION-2921.md)／[2,939](VALIDATION-2939.md)／[2,959](VALIDATION-2959.md)／[2,977](VALIDATION-2977.md)／[2,982](VALIDATION-2982.md)／[2,988](VALIDATION-2988.md)／[2,997](VALIDATION-2997.md)。121歷史題完整刷新、真實萬筆／十萬筆、品質抽樣、試讀及採用仍未完；未購付費媒體，無完整模型帳單，不稱研究零成本。
