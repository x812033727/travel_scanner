# 第四十七批素材池驗證

由 3,483 增至 3,501 個入選核心。本批 19 個原提案、18 個新核心、21 筆來源閱讀紀錄，另 51 個方向未收。前版 3,871 筆原題、3,483 個入選與 514 組題案逐項保留。[舊庫快照](checkpoint-3483.json) · [本批整合](reviews/wave47-editorial-integration.json)

植物作者 pool_life_tech、覆核 pool_physics；光學作者 pool_physics、覆核 science_sources；河床作者 science_sources、覆核 pool_life_tech。每題 top-5 共 95 個有向配對，另核 66 組作者手查近對，配對可能重疊。本輪新增 143 組分題理由。正式提案中 1 題併回既有核心，0 題排除。舊題之間未全面重查，不能由單批估全庫去重召回率。[植物覆核](reviews/wave47-physics-reviews-life.json) · [光學覆核](reviews/wave47-earth-reviews-physics.json) · [河床覆核](reviews/wave47-life-reviews-earth.json)

來源逐筆記錄 DOI、取用網址、版本、實讀範圍與快取雜湊；正文、圖、模型與推論的範圍分開列。兩個閱讀來源只追加同網址的閱讀紀錄，沒有新增原題或改寫前版原始記錄。[來源身分與範圍](reviews/wave47-central-checks.json) · [閱讀補查](reviews/wave47-physics-reviews-reading-refresh.json)

G515–G528 共 14 案，正文 38–94 秒；3 案以離線合成旁白量時，逐段音檔、全文連讀、WAV幀數、取樣率、雜湊與章節餘裕均留紀錄，其餘為紙上估時。[樣讀](reviews/wave47-timing.json)

## 本機檢查

- 45 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,890 筆原題重建索引，95 個本批有向近鄰與覆核版一致；檢查來源反查、前版保留及 SQLite 相同輸入重匯零寫入。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；逐張檢視三張截圖。實際 Git 暫存內容另驗雜湊及文字衛生。[完整紀錄](reviews/wave47-final-validation.json) · [搜尋頁檢查](reviews/wave47-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。前批閱讀來源仍有 R45-S005、S006、S007、S011、S013 五份缺指定正文覆核，製作前需補查。

首輪瀏覽器檢查發現補查來源只進索引、未顯示於題卡。已將題卡篩選改為同批來源或明確指定題號（含合併前ID），補上隔離其他題目閱讀紀錄的回歸測試，並重驗兩張實際閱讀題卡。內容來源與舊原題不因此重算。
