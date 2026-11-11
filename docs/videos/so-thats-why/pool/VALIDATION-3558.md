# 第五十一批素材池驗證

由 3,542 增至 3,558 個入選核心。本批 17 個原提案、16 個新核心（L51-005 併入 L51-004）、18 筆來源閱讀紀錄，另 57 個方向未收。前版 3,931 筆原題、3,542 個入選與 559 組題案逐項保留。[舊庫快照](checkpoint-3542.json) · [本批整合](reviews/wave51-editorial-integration.json)

動物與微生物、熱板液滴與燭火、考古磁性與海天觀測、廚房與身體感知四線各由一位作者撰寫，再由另一位未參與撰寫的覆核者讀原文、原圖與近鄰。四線首輪皆判需修正，作者依意見修文後由原覆核者讀回，最終四線皆為題級通過。每題 top-5 共 85 個有向配對，另核 59 組作者手查近對，配對可能重疊；覆核者另以關鍵字補查 22 次。本輪新增 137 組分題理由與 1 組合併。作者修文後以最終草稿重算近鄰，新出現的 10 組由整合者逐組判為不同核，這部分不是獨立覆核。舊題之間未全面重查，不能由單批估全庫去重召回率。[動物與微生物覆核](reviews/wave51-independent-reviews-life.json) · [熱板液滴與燭火覆核](reviews/wave51-independent-reviews-physics.json) · [考古磁性與海天觀測覆核](reviews/wave51-independent-reviews-earth.json) · [廚房與身體感知覆核](reviews/wave51-independent-reviews-human.json)

來源逐筆記錄 DOI、取用網址、版本、實讀範圍與快取雜湊；作者快取 36 個雜湊重核相符。日食研究與舊 S21 同一 DOI，不另算獨立證據；香檳氣泡題只讀預印本。[來源身分與範圍](reviews/wave51-central-checks.json)

G560–G575 共 16 案，正文 50–72 秒，全部為紙上估時；本批未做離線合成連讀，不是真人試讀。[片長取捨](reviews/wave51-pacing-revisions.json)

## 本機檢查

- 45 項相關 Node 測試與 2 項 Python 測試，另驗素材池、系列、長片與任務檔。
- 依最終 3,948 筆原題重建索引，SQLite 相同輸入重匯零寫入；檢查來源反查、前版保留與合併別名導向。
- 桌面分頁、來源展開、所有新片案篩選、手機關鍵字及題號搜尋；檢視桌面與手機截圖。[完整紀錄](reviews/wave51-final-validation.json) · [搜尋頁檢查](reviews/wave51-browser-qa.json)

這些檢查不代表完整製作稿或成片驗收，亦不是實際一萬／十萬筆效能測試。早期閱讀題待補查的 14 份來源中，9 份有指定正文閱讀紀錄；R45-S005、S006、S007、S011、S013 五份仍待補查，製作前不能以其他近題論文替代原 DOI。前批 S49-003 落高單位矛盾仍未釐清，本批未再補查。[單位限制](reviews/wave49-root-scope-checks.json)

## 遠端 CI

本批開始時讀回前版 `3f588e4565`：23 項成功、0 項執行中、0 項失敗。這是前版CI，本批新提交需另讀最新結果；PR1971仍為draft並保留no-auto-merge。歷史a881970的full-stack-smoke失敗紀錄保留於[前次分診](reviews/wave48-prior-ci-triage.json)，不改寫歷史結果。[前版CI讀回](reviews/wave51-prior-ci-status.json)
