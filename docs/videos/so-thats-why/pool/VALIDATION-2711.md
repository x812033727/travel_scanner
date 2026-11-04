# 第八批素材池驗證：2,711筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)。

46新提案由非作者逐題編輯覆核，2合併、0暫緩，新增44核心；另6來源修訂合併回舊核心。舊2,667全保留、3,017 raw未改，2667快照加入必讀registry。當期raw 3069、核心2940、可選2770、入選2711、別名129、候補59。高相似待處理0不代表沒有漏合。

本批59個不同來源URL、52首次加入；入選使用2265 URL／4087題來源關係。六舊核心只新增指定機制閱讀，不是整份舊答案或附件全面重核；原始紀錄保留。來源更新合併與新題去重分開計算。詳[集中處置](reviews/wave8-editorial-integration.json)及[來源更新覆核](reviews/wave8-science-reviews-source-refresh.json)。

新增10題組、累計88，正文1:45–4:20未試讀；逐核心時間合計驗上限。舊78題組全部不變，G59仍130秒文字草稿。本批完整旁白、試讀及新媒體均0；原小樣未重跑。

相關Node測試37/37、Python2/2通過；pool/series、473既有長片及任務格式檢查通過。實際Git index blob雜湊、本地連結、資料與索引在[最終驗證](reviews/wave8-final-validation.json)，[非作者最終讀回](reviews/wave8-final-independent-readback.json)另存範圍。命令：

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

未宣稱重跑API/web全部測試；無關任務警告不代改。

| 單次本機動作 | 實測 |
| --- | --- |
| 詞面相似候選 | 8545.3 ms |
| 索引匯入 | 4881.3 ms |
| 同快照再匯 | 359.4 ms；UNCHANGED／0 writes |
| SQLite | 42,733,568 bytes |
| RSS快照 | 401,084,416 bytes |

搜尋、既有及新別名與來源關係讀回；本批新增暫緩集合為空，沒有據此宣稱測過暫緩列排除。只是當期真實資料一次測量，不是延遲分位數或萬筆／十萬筆壓測。最終語意3069raw，新建0向量、19.152秒，新增截斷0；快取命中非冷啟動，歷史截斷限制仍存在。

新提案有2組人工合併對，詞面找到0、語意top10找到1。六筆明知同核心的來源修訂另列，不計入去重檢索成績；此非隨機集合不是全庫召回率。新題近鄰及作者指定相近對由非作者比較，未針對本批調門檻。[瀏覽器檢查](reviews/wave8-browser-qa.json)驗入選數、分頁、新舊別名、來源與欄位、新題組及桌面／390px手機；本批新增暫緩集合為空。截圖人工檢視不能代表觀眾看懂。

距10k還差7,289。完整影片包、實際試讀、觀眾測試、獨立品質抽樣與萬筆以上效能仍待完成。本批無正式寫入、付費媒體、製作或發布。
