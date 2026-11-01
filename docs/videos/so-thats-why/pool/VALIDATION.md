# 第十批素材池驗證：2,797筆

日期2026-11-01；Node v24.22.1。歷史：[1,000](VALIDATION-1000.md)／[2,000](VALIDATION-2000.md)／[2,328](VALIDATION-2328.md)／[2,449](VALIDATION-2449.md)／[2,546](VALIDATION-2546.md)／[2,609](VALIDATION-2609.md)／[2,667](VALIDATION-2667.md)／[2,711](VALIDATION-2711.md)／[2,757](VALIDATION-2757.md)。

42新提案，2合併／0暫緩後新增40核心；另3來源修訂全併回舊題，不計核心。舊2,757入選及3,115 raw保留；新增2757雜湊快照，editorial豁免仍止於2000。當期raw 3160、核心3026、可選2856、入選2797、別名134、候補59。高相似待處理0不代表沒有漏合。

本批42來源URL／39首次加入，全庫4115、研究1156、入選使用2346／4195題來源關係。3來源修訂只是限定範圍，不核准舊完整答案；來源風險抽查和失敗詳[集中處置](reviews/wave10-editorial-integration.json)所綁審閱。

新增12題案、累計110，正文1:35–3:00未試讀。同核跨章累計核上限。全部98舊題案不變；G79/G59仍279字85秒／506字130秒，舊小樣未重跑。本批完整稿、實際試讀與新媒體皆0。數值探針驗固定整數/單位換算與虛構機率、計分、分配模型，不是實證調查。

相關Node **39/39**、Python **2/2**通過，無失敗／取消／略過；pool/series、473長片與2,287任務格式通過。無關任務警告未代改，未跑完整API/web CI。

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
| 詞面相似候選 | 4069.6 ms |
| 索引匯入 | 2496.1 ms |
| 同快照重匯 | 309.3 ms；UNCHANGED／0 writes |
| SQLite | 47,374,336 bytes |
| RSS快照 | 581,828,608 bytes |

只是目前真實資料的一次測量，不是延遲分位數或萬筆／十萬筆壓測。最終語意3160raw，新建0向量、2.328秒，新增截斷0；快取命中非冷啟動，歷史截斷限制保留。本批2組新提案人工合併對，詞面找到0、語意top10找到1；為事先知道結果的非隨機小集合，不是全庫召回率。

每題top5與作者相近對交非作者比較；三筆來源更新另核強制合併與限縮支持範圍。本批新增暫緩為空，不把空集合算成負向排除測試。瀏覽器核入選數、分頁、實際新合併／來源修訂別名與歷史別名、來源欄位、G37/G59/G79及新題案、桌面與390px手機；三圖由root查看。詳[瀏覽器收據](reviews/wave10-browser-qa.json)。

[最終驗證收據](reviews/wave10-final-validation.json)保存實際Git index blob、連結、核心預算與來源反查；[獨立整合讀回](reviews/wave10-final-independent-readback.json)另列範圍，作者不自核自己寫的事實。

距10k差7,203。121筆舊題全文／附件、完整影片包、試讀、觀眾測試、品質抽樣及大規模效能仍待完成。無正式寫入、付費媒體、部署或發布。
