# 第四十六批素材池驗證

由 3,458 增至 3,483 個入選核心。本批 26 個原提案、25 個新核心、28 筆來源紀錄，另 48 個方向未收。前版 3,845 筆原題、3,458 個入選與 497 個片案逐項保留。[舊庫快照](checkpoint-3458.json) · [本批整合](reviews/wave46-editorial-integration.json)

閱讀作者 root、覆核 pool_physics；動物作者 pool_life_tech、覆核 science_sources；冰雪作者 science_sources、覆核 pool_life_tech。每題 top-5 共 130 個有向配對，另核 73 組作者手查近對，配對可能重疊。本輪新增 166 組分題理由；1 個提案合併，0 個提案排除；不能由單批估全庫去重召回率。雪層毛細屏障合回D2090，是人工讀舊未收紀錄找到的漏檢正例，不在該題語意top-5中。舊題之間本輪未全面重查。[閱讀覆核](reviews/wave46-physics-reviews-reading.json) · [動物覆核](reviews/wave46-earth-reviews-life.json) · [冰雪覆核](reviews/wave46-life-reviews-earth.json)

閱讀組 6 份指定正文、8 份原作者摘要；覆核另補讀部分作者稿，未因此將全部14份標成全文。修正學習者整句讀時定位至作者稿第18頁，保留無空格與逐字分隔的無顯著差異。字重改善換行落點但未顯著縮短總讀時；語音預覽的數值趨勢未升格為顯著效果。

動物題區分活體觀察、干預與模型反事實；冰雪題區分冰形影像、模型流場及有限樣本。氣泡融冰僅兩次水槽比較，雪的三個弱層案例不只改坡度；不把模型箭頭冒充直接量測。[來源身分與範圍](reviews/wave46-central-checks.json)

G498–G514 共 17 案，正文 44–72 秒；5 案離線合成旁白量時，其餘紙上估時。兩個舊核心的新題案作者為root、編輯覆核pool_physics；P45-006的原素材獨立查核仍沿用前批root收據，沒有把原作者重新署名當新獨立查核。[題案覆核](reviews/wave46-physics-reviews-carry.json) · [樣讀](reviews/wave46-timing.json) · [前批待辦完成](reviews/wave46-prior-work-resolution.json)

## 本機檢查

- 44 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,871 筆原題重建索引，130 個本批有向近鄰與覆核版一致；檢查來源反查、前版保留及 SQLite 相同輸入重匯零寫入。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；逐張檢視三張截圖。實際 Git 暫存內容另作雜湊及文字衛生檢查。[完整紀錄](reviews/wave46-final-validation.json) · [搜尋頁檢查](reviews/wave46-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。
