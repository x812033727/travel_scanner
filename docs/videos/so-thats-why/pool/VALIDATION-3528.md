# 第四十九批素材池驗證

由 3,514 增至 3,528 個入選核心。本批 14 個原提案、14 個新核心、16 筆來源閱讀紀錄，另 46 個方向未收。前版 3,903 筆原題、3,514 個入選與 537 組題案逐項保留。[舊庫快照](checkpoint-3514.json) · [本批整合](reviews/wave49-editorial-integration.json)

食物作者 pool_life_tech、覆核 pool_physics；薄片與織物作者 pool_physics、覆核 science_sources；水滴冰霜作者 science_sources、覆核 pool_life_tech。每題 top-5 共 70 個有向配對，另核 58 組作者手查近對，配對可能重疊。本輪新增 105 組分題理由。初篩已先剔除重複或證據不足的方向；正式提案沒有再判合併或排除。舊題之間未全面重查，不能由單批估全庫去重召回率。[食物覆核](reviews/wave49-physics-reviews-life.json) · [薄片與織物覆核](reviews/wave49-earth-reviews-physics.json) · [水滴冰霜覆核](reviews/wave49-life-reviews-earth.json)

來源逐筆記錄 DOI、取用網址、版本、實讀範圍與快取雜湊；正文、圖、模型與推論的範圍分開列。[來源身分與範圍](reviews/wave49-central-checks.json) S49-003 原刊正文／圖說的落高單位不一致，現案只採同落高對照，精確數字列製作前待核。[單位限制](reviews/wave49-root-scope-checks.json)

G538–G547 共 10 案，正文 65–87 秒；3 案以離線合成旁白量時，逐段音檔、全文連讀、WAV幀數、取樣率、雜湊與章節餘裕均留紀錄，其餘為紙上估時。[樣讀](reviews/wave49-timing.json)

## 本機檢查

- 45 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,917 筆原題重建索引，70 個本批有向近鄰與覆核版一致；檢查來源反查、前版保留及 SQLite 相同輸入重匯零寫入。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；逐張檢視三張截圖。實際 Git 暫存內容另驗雜湊及文字衛生。[完整紀錄](reviews/wave49-final-validation.json) · [搜尋頁檢查](reviews/wave49-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。前批 14 份閱讀來源中，9 份有指定正文閱讀紀錄；R45-S005、S006、S007、S011、S013 五份仍待補查，製作前不能以其他近題論文替代原 DOI。

## 遠端 CI

上一批提交 a638b454d 的 23 項遠端檢查已全部通過，包含 full-stack-smoke 與 Lighthouse。本輪沒有修改應用程式來處理前前批的瀏覽器失敗；該次失敗仍保留原始紀錄，不能因此判為偶發錯誤。本輪新提交須另等 CI 結果。
