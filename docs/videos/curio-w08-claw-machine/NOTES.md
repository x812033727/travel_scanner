# curio-w08-claw-machine 製作筆記

- **選題**：後台題目池（`/admin/videos?tab=pools` → 奇聞檔案局 → 單集題）第 1 名 `N9075`（總分 9.68／底分 9.62／需求 10，W-商業與品牌奇聞）。
- **代號**：遠端分支 `claude/curio-w-batch-2-scripts` 已占 `W04`–`W07`，本集採用 `curio-w08-claw-machine`，Drive 備份資料夾為 `AI/備份/AI劇/奇聞檔案局/W08/製作檔/`。
- **來源核實**：8 筆一手／機構來源全數經 GET 測通 HTTP 200（`archive.org/details/arcade-1-1993-book-scans` 與 `gcis.nat.gov.tw/elawAp/api/lawAttachment/243`；後者 HEAD 回 403 但 GET 200）。
- **畫風與合規**：
  - 2026-11-14 劇場級動畫光影 × 厚塗水粉質感，50% 以上純物件／場景鏡（`nobody: true`），`Ada` 出場鏡鎖定 `ada-canon-v2.png`（3.5 頭身修長比例）。
  - 縮圖採 2026-11-20 `heimao-left` 規則：第一行點名「夾娃娃機」（九語皆明寫主體），畫面零商標、零版權角色、零文字。
  - 1956 人物紅線：唯一點名真人 William D. Bartlett 逝於 1948 年；在世受訪修復師、日台開發與官員一律不點名、不入畫。
- **2026-11-22 全片組裝、8 語配音、獨立觀眾審片與備份（全數完成）**：
  - 前置關卡全數通過：`lint`（**0 errors, 0 warnings**，全 9 語）、獨立查核 `verify-2.md`（**24/24 CONFIRMED**）、3 角色 `opening-review`（**9.0 / 9.0 / 9.0 PASSED**）、2 位盲讀敘事審查（**14/14 PASS**）、60／60 張 2K 關鍵影格 2x 四象限獨立審圖通過並匯入（`--provider external --usd 0`）。
  - `zh-TW` `Sulafat` TTS：119/119 句完成（正文 `08:09`，實測語速 `4.85 字/秒` >= `4.4 字/秒`）；`check.json` 13 句標記經實聽 13 個 `.wav` 全數確認為 ASR 誤聽或自然口語，0 處唸錯；Lyria 配樂 3x 無縫循環（`music/d7ef806b3905b8b6.mp3`）。
  - 成片組裝：`final.mp4`（`15,311` 格，`-14 LUFS`，真峰值 `-1.9 dBFS`，配樂底噪 `-30.7 LUFS`，sha256 `7f8b9f45e5e5`）；`captions` 零警告；收短 `en`/`es`/`pt`/`id` 四語縮圖主標後重渲，9 語縮圖全數零警告；`qa` 9/11 過關（僅待站主核准 `narration` 與站台立場分數 `0.36`，`建議 0.05`、`業配 0.04`）。
  - 獨立成片一般觀眾審片（`review/audience-review.md`）：**`9.1 / 10`**（`Would watch to end: Yes`，視聽／配音零阻斷瑕疵；已依建議將 `brief.md` 站主觀點改為正向表述）。
  - 8 語 MiniMax 配音全數混音完成（均含配樂底軌）：`en.m4a`（19 MB，收緊 `w072`–`w073`）、`ja.m4a`（17 MB，收緊 `w026`–`w027`）、`ko.m4a`（17 MB）、`es.m4a`（18 MB，收緊 `w034`–`w035`）、`pt.m4a`（18 MB，收緊 `w072`–`w073`）、`id.m4a`（19 MB）、`vi.m4a`（19 MB）、`th.m4a`（18 MB，收緊超窗 10 窗）。
  - `/admin/videos` 關卡：`script`、`storyboard`、`audio`、`final`（`7f8b9f45e5e5`）、`dubs`（`fde840a74e2f`）皆已核准並決定全 8 語系；2026-11-23 完成全 9 語字幕、`package`（`4/4`，`metadata.json` `f72fa242ffcb`），推送完整備份層級 `publish`（`717c16de`，`94` 檔，`pending`）與 8 語 `languages`（`fcb272aa`，`cad806c138a4`，`34` 檔，`pending`）至 `/admin/videos`。
  - Google Drive 零差異備份：已移至正確分類資料夾 `AI/備份/AI劇/奇聞檔案局/W-商業與品牌奇聞/W08/`（`1ZpMQOzbu53QCBOQ-0AJPMA0BIM3p0SKc`，`40/40` `0 differences`）與 `W08/製作檔/`（`1vrmthZCGtgrtZ5McoqAvTgN-NTHrsKWA`，`upload/`＋`captions/`＋`review/`＋`approvals.json`＋`languages.json` 皆 `0 differences`）。

