# 第六批素材池驗證：2,609筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)。

## 資料與編輯

[集中處置](reviews/wave6-editorial-integration.json)：64原題逐題非作者覆核，0合併／1暫緩，新增63核心，舊2,546全保留。raw 2959、核心2838、可選2668、入選2609、別名121、候補59。高相似待處理0不代表沒有漏合。

植物園藝16、日常機構23、天氣天空25；來源為指定段落與風險抽查，不是完整答案逐主張核准。每組覆核綁定作者檔SHA、記來源讀取範圍及修訂讀回。合併：無；暫緩：J6016。新暫緩題不進入選卡片或題組。

本批64個不同研究URL、64首次加入全庫；全庫3919、研究952、入選使用2161／3964題來源關係。2,895舊raw改寫0；2546快照加入必讀清單，editorial欄位檢查基線仍是2000。

## 組片與示範

新增9題組，累計69；2:20–4:15正文預算包含開場回扣。各新題組與G59逐核心累計預算另驗。G59由200秒3核心收為140秒2核心，M5010移出本片但仍入選；M5008音訊案例不另計核心或疊加PNG情境時間。

機構定位題組290→230秒，移出的J6003仍留池；植物開花題265→225秒，刪重複澄清/回顧。果實題只保留摘要支持的生長素誘導需要活性GA，不擴成雙向互相必要；進完整稿前仍須補全文條件。

[G59本機收據](reviews/wave6-g59-demo.json)與[非作者覆核](reviews/wave6-g59-independent-review.json)記錄公式、4個指定向量、全部65,536組8位元左右值、49組16位元邊界、128組64樣本序列、改錯殘差及略去奇偶的反例。桌面與手機按鈕操作、表格橫向捲動和頁面無錯誤已驗。僅為整數小樣，沒有位元流、Rice、CRC、檔案壓縮率或音訊播放；沒有完整旁白試讀或觀眾測試。

前批G37示範與FLAC檔案探針保留，本輪沒有重跑其實驗，也不升格其證明範圍。

## 檢查與效能

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

相關Node測試35/35、Python2/2通過，0失敗／取消／略過；pool與series check、473既有長片、2,287任務格式通過。實際測試結果、Git index blob雜湊、題組逐核心累計預算及本地連結記在[驗證收據](reviews/wave6-final-validation.json)。沒有宣稱API/web全套檢查皆重跑；無關任務警告不代改。

| 當次動作 | 單次實測 |
| --- | --- |
| 詞面近似生成 | 4214.8 ms |
| 索引匯入 | 2454.0 ms |
| 同快照再匯入 | 196.5 ms；UNCHANGED／0 writes |
| SQLite | 40,869,888 bytes |
| RSS快照 | 374,730,752 bytes |

搜尋、所有新別名與暫緩、RFC來源反查至G59均讀回；測量是本機真實資料單次，不是延遲分位數或萬筆／十萬筆壓測。最終語意輸入2959raw、新建0向量、2.962秒，不是冷啟動完整建向量耗時。

本批沒有新增人工合併對，因此不計算本批已知合併命中率；53個方向在作者鎖定前已記為不另收錄，不能把它們當63個新核心之外的素材數。近似配對的保留理由在獨立覆核與去重紀錄，未為本批調門檻，也未證明全庫沒有漏合。

[瀏覽器收據](reviews/wave6-browser-qa.json)驗入選數、50→100分頁、新別名／暫緩、來源與新增理解欄位、G37/G59及全部新題組、390px無橫溢與零頁面錯誤；桌面／手機截圖查看狀態記在收據。

距10k仍差7,391；完整稿、試讀、獨立品質抽樣與規模驗證尚未完成。沒有正式資料寫入、付費媒體、配音或發布。
