# 第五十批素材池驗證

由 3,528 增至 3,542 個入選核心。本批 14 個原提案、14 個新核心、14 筆來源閱讀紀錄，另 52 個方向未收。前版 3,917 筆原題、3,528 個入選與 547 組題案逐項保留。[舊庫快照](checkpoint-3528.json) · [本批整合](reviews/wave50-editorial-integration.json)

植物作者 pool_life_tech、覆核 pool_physics；光與成像作者 pool_physics、覆核 science_sources；考古證據作者 science_sources、覆核 pool_life_tech；選擇認知作者 root、覆核 science_sources。每題 top-5 共 70 個有向配對，另核 56 組作者手查近對，配對可能重疊。本輪新增 95 組分題理由。初篩已先剔除重複或證據不足的方向；正式提案沒有再判合併或排除。舊題之間未全面重查，不能由單批估全庫去重召回率。[植物覆核](reviews/wave50-physics-reviews-life.json) · [光與成像覆核](reviews/wave50-earth-reviews-physics.json) · [考古證據覆核](reviews/wave50-life-reviews-earth.json) · [選擇認知覆核](reviews/wave50-earth-reviews-human.json)

來源逐筆記錄 DOI、取用網址、版本、實讀範圍與快取雜湊；正文、圖、模型與推論的範圍分開列。[來源身分與範圍](reviews/wave50-central-checks.json) 前批 S49-003 原刊正文／圖說的落高單位不一致，原題案只採同落高對照，精確數字列製作前待核。[單位限制](reviews/wave49-root-scope-checks.json)

G548–G559 共 12 案，正文 59–88 秒；4 案以離線合成旁白量時，逐段音檔、全文連讀、WAV幀數、取樣率、雜湊與章節餘裕均留紀錄，其餘為紙上估時。[樣讀](reviews/wave50-timing.json)

## 本機檢查

- 45 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,931 筆原題重建索引，70 個本批有向近鄰與覆核版一致；檢查來源反查、前版保留及 SQLite 相同輸入重匯零寫入。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；逐張檢視三張截圖。實際 Git 暫存內容另驗雜湊及文字衛生。[完整紀錄](reviews/wave50-final-validation.json) · [搜尋頁檢查](reviews/wave50-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。早期閱讀題待補查的 14 份來源中，9 份有指定正文閱讀紀錄；R45-S005、S006、S007、S011、S013 五份仍待補查，製作前不能以其他近題論文替代原 DOI。

本批銅斧來源是預印本，內文配比矛盾已列限制，不採精確數字。[指定原文範圍](batches/wave50-earth.json) 本輪再查前批落高單位，仍未釐清原文矛盾，未新增來源閱讀或素材筆數。[本輪補查紀錄](reviews/wave50-prior-source-followup.json)

## 遠端 CI

本批開始時讀回前版 `faeba1adac`：23 項成功、0 項執行中、0 項失敗。這是前版CI，本批新提交需另讀最新結果；PR1971仍為draft並保留no-auto-merge。歷史a881970的full-stack-smoke失敗紀錄保留於[前次分診](reviews/wave48-prior-ci-triage.json)，不改寫歷史結果。
