# curio-w08-claw-machine 製作筆記

- **選題**：後台題目池（`/admin/videos?tab=pools` → 奇聞檔案局 → 單集題）第 1 名 `N9075`（總分 9.68／底分 9.62／需求 10，W-商業與品牌奇聞）。
- **代號**：遠端分支 `claude/curio-w-batch-2-scripts` 已占 `W04`–`W07`，本集採用 `curio-w08-claw-machine`，Drive 備份資料夾為 `AI/備份/AI劇/奇聞檔案局/W08/製作檔/`。
- **來源核實**：8 筆一手／機構來源全數經 GET 測通 HTTP 200（`archive.org/details/arcade-1-1993-book-scans` 與 `gcis.nat.gov.tw/elawAp/api/lawAttachment/243`；後者 HEAD 回 403 但 GET 200）。
- **畫風與合規**：
  - 2026-11-14 劇場級動畫光影 × 厚塗水粉質感，50% 以上純物件／場景鏡（`nobody: true`），`Ada` 出場鏡鎖定 `ada-canon-v2.png`（3.5 頭身修長比例）。
  - 縮圖採 2026-11-20 `heimao-left` 規則：第一行點名「夾娃娃機」（九語皆明寫主體），畫面零商標、零版權角色、零文字。
  - 1956 人物紅線：唯一點名真人 William D. Bartlett 逝於 1948 年；在世受訪修復師、日台開發與官員一律不點名、不入畫。
- **2026-11-21 檢查點（等待 Gemini TTS 日額度重置續跑）**：
  - 已完成並通過：`lint`（**0 errors, 0 warnings**，含全 9 語）、獨立查核 `verify-2.md`（**24/24 CONFIRMED**）、3 角色 `opening-review`（**9.0 / 9.0 / 9.0 PASSED**）、2 位盲讀敘事審查（**14/14 PASS**）、60／60 張 2K 關鍵影格經獨立 2 倍 4 象限審圖全數通過並以 `--provider external --usd 0` 匯入、9 語 `heimao-left` 縮圖渲染並目視驗收、8 語 `i18n`（`en,ja,ko,es,pt,id,vi,th`）經獨立品質稽核修正通過；後台已送審 `script` 與 `storyboard`（`pending`）。
  - 唯一卡點：伺服器 Gemini 金鑰之 `gemini-3.8-flash-tts`（預設）與 `gemini-3.8-flash-lite-tts`（實測約 19 句觸頂）雙雙達 Google 單日請求上限（HTTP 429）。已切回預設 `gemini-3.8-flash-tts` 保留既有 **93／119 句**快取（僅剩 27 句／595 字元，全片正文預估 08:06 ≥ 08:00）。
  - 雲端備份：`AI/備份/AI劇/奇聞檔案局/W08/製作檔/`（資料夾 ID `1ZpMQOzbu53QCBOQ-0AJPMA0BIM3p0SKc` / `1vrmthZCGtgrtZ5McoqAvTgN-NTHrsKWA`）。
  - 續跑指令：待太平洋時間午夜額度重置（台灣 16:00）或後台更新 Gemini 金鑰後，從 `tts --slug curio-w08-claw-machine` 接續 → `check-audio` → `music` → 8 語 MiniMax `dub`＋`check-audio --second-opinion` → `clips` → `assemble --adopt-branding` → `captions` → `qa`（11/11）→ 獨立 `review/audience-review.md` → Drive 零差異覆寫備份 → `review-push --gate audio / final`。

