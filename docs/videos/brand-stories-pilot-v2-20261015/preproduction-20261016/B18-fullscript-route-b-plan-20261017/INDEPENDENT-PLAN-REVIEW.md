# B18 Route B 分階段對位方案：獨立審查收據

- 審查日：2026-10-17；審查者：Codex `/root/b18_script_scene_alignment/b18_route_b_plan_review`，未編寫這份 Route B 方案。
- 範圍：本目錄的設計方案、覆蓋率驗證，對照固定的父版企劃／六章 85 景與第三版全文。**結論：設計候選 PASS，P1 0、P2 0；製作與採用仍 HOLD。** 這不是新版企劃、正式章稿、已查核主張或媒體的核准。
- 固定父版：flow `sha256.json` SHA-256 `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`；B18 row `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`；row 審稿 `6e06d5ddd1d4d836a105450e15b49fc98203e7ea0a595c7bba1596630fb73dc8`。
- 固定全文：第三版 `B18.md` SHA-256 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`；其獨立全文審稿 `review-candidate.md` SHA-256 `603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4`。
- 本次受審方案：`route-b-plan.json` SHA-256 `3b3183525d995950bc9366ecffd82595938817eca09a8a4d6ca95100d1e88985`；`check.mjs` SHA-256 `f2c816dc5ed61678a566b9e5e7beadaabf84957acc4949f9b0bcdf050b3fbe7e`；`verification.json` SHA-256 `330440f1169ba98caac3df5290800e7c61103c7524ae64f00e4b7b78729e2b9b`。`node .../B18-fullscript-route-b-plan-20261017/check.mjs --check` 讀回 `PASS_STAGED_DESIGN_ONLY_HOLD`：25 段、85 個舊 scene ID、65 個舊 claim ID，舊稿 2,264 與新稿 3,007 個口播可見字元，相差 743；所有舊 claim 仍為 `UNCHECKED`。

## 查核結果

1. **開場與時間線。** 第三版 H02 的第三問是後場到客席；父版 `hook.point` 與 `hook-s006/h7` 尚指向權利期滿。方案要求連同企劃、scene、畫面及 setup/payoff 一起修改，沒有把舊企劃錯認為已對齊。第三版 T01 的 1967 仙台／東京擴張須另加法院來源、reviewer-only 事實與獨立 row 審查；方案沒有把法院的特定第 579776 號 1972 年期滿擴張成所有權利同日屆滿。
2. **來源邊界。** [法院官方判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P8 L476–495 確實記錄獲授權的訴外元祿在 1967 年開仙台直營首店、東京錦糸町連鎖首店；P10 L574–578 只認定特定實用新案屆滿與其後其他業者營業。[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)另記後場直線送盤及以盤色／裝飾區分價位。方案把 1967 項列為須 `reviewer_only` 的新事實、盤色列為可讀來源的新事實，並保留 1978 說法衝突而不口播。
3. **逐段／逐景／主張落點。** 25 個口播段落各有同章的 scene 區間，85 個舊 scene ID 恰好各用一次；65 個舊 claim ID 亦各有保留或改寫處置。初稿曾漏明確落點：`o6/o7` 的舊 `origin-s012` 改屬 O04，但主張須進 O01；`e9` 的舊 `engine-s053` 改屬 E04，但新主張須進 E05。修正版分別指定 `origin-s011` 與 `engine-s056`，檢查器現會要求 claim 的目標 scene 屬於目標段落。其餘要改的來源、事實索引、畫面與舊主張去向已列出；這只是下一輪實作的設計，不表示 scene 台詞與 claim 已實際改寫。
4. **畫面及時長。** 以父版 template 計的 66 個插圖 scene、最大連續 2 卡只是重排前提；改稿後仍須重算插圖比例、卡片串接及實際 `say_for`。方案已標出 O03、E02、T01、N02 的逐鏡時長風險，沒有把 300 字／分離線估算當 TTS 成績，也明示 85 景若不足須先隔離增景與估成本。

## 保留意見與效力

- **P3，已註明：**第三版受審 `B18.md` 內的「尚無獨立審稿」是寫稿當時的歷史狀態；同資料夾後出的 hash-bound `review-candidate.md` 已給離線全文 PASS。Route B README 已加註，受審稿未因此改字。
- 本收據只核上列 SHA 的**分階段設計完整性**。新版 row、企劃來源審查、85 景 88 句的正式改稿、65 筆逐章 verifier、listener／narrative、實際 TTS／Jev、MiniMax 插圖、繁中 CC、成片和站主看片仍未完成。B18 未有費用上限核准；本次沒有主機寫入、付費呼叫、上傳或發布。任何受審檔變動，都要重新核對本收據。
