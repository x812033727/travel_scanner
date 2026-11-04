# 第四十八批素材池驗證

由 3,501 增至 3,514 個入選核心。本批 13 個原提案、13 個新核心、14 筆來源閱讀紀錄，另 47 個方向未收。前版 3,890 筆原題、3,501 個入選與 528 組題案逐項保留。[舊庫快照](checkpoint-3501.json) · [本批整合](reviews/wave48-editorial-integration.json)

動物感知作者 pool_life_tech、覆核 pool_physics；聲音作者 pool_physics、覆核 science_sources；地質作者 science_sources、覆核 pool_life_tech。每題 top-5 共 65 個有向配對，另核 56 組作者手查近對，配對可能重疊。本輪新增 111 組分題理由。初篩已先剔除重複或證據不足的方向；正式提案沒有再判合併或排除。舊題之間未全面重查，不能由單批估全庫去重召回率。[動物感知覆核](reviews/wave48-physics-reviews-life.json) · [聲音覆核](reviews/wave48-earth-reviews-physics.json) · [地質覆核](reviews/wave48-life-reviews-earth.json)

來源逐筆記錄 DOI、取用網址、版本、實讀範圍與快取雜湊；正文、圖、模型與推論的範圍分開列。[來源身分與範圍](reviews/wave48-central-checks.json)

G529–G537 共 9 案，正文 65–100 秒；3 案以離線合成旁白量時，逐段音檔、全文連讀、WAV幀數、取樣率、雜湊與章節餘裕均留紀錄，其餘為紙上估時。[樣讀](reviews/wave48-timing.json)

## 本機檢查

- 45 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,903 筆原題重建索引，65 個本批有向近鄰與覆核版一致；檢查來源反查、前版保留及 SQLite 相同輸入重匯零寫入。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；逐張檢視三張截圖。實際 Git 暫存內容另驗雜湊及文字衛生。[完整紀錄](reviews/wave48-final-validation.json) · [搜尋頁檢查](reviews/wave48-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。前批 14 份閱讀來源中，9 份有指定正文閱讀紀錄；R45-S005、S006、S007、S011、S013 五份仍待補查，製作前不能以其他近題論文替代原 DOI。

## 遠端 CI

前一版 a881970 的遠端 CI 為 22 項成功、1 項 full-stack-smoke 失敗；手機旅程在 openOptionalStops 超時，不列為已修或已知偶發錯誤。新提交的 CI 需另讀回。[前版失敗定位](reviews/wave48-prior-ci-triage.json)
