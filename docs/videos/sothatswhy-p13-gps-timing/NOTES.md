# 製作交接紀錄：`sothatswhy-p13-gps-timing`（原來如此事務所 Ep P13）

- **題目**：GPS 藍點為何在大樓間狂跳對街、重開地圖還卡半天？手機定位靠的其實全是「時間」！（上架標題：`GPS藍點為何狂跳對街？差百萬分之一秒竟然就偏三百公尺！｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（零刪除同步，舊版移入 `_舊版/<UTC>/`）**：
  - 集數頂層成品目錄（`epDir`）：`1ujihXrU3uzqJaCRf-gip-EVxu-1kif50`
  - 製作檔完整備份目錄（`workDir`）：`1Wp51xUPtdZzenF_pdePSyNLP1aNRZuld`（`製作檔/sothatswhy-p13-gps-timing`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **52 鏡、52 句**，`nobody: true` 純原理／機制／物件鏡共 **33 / 52（63.5%）**，`lint` 0 errors，`opening_hash` 維持不變。
   - 獨立查核 `verify-2.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；14 筆一手來源連結（GPS.gov、U.S. DoD SPS Standard、ESA Navipedia、Springer Living Reviews in Relativity Ashby 2003、NAVIGATION Blay et al. 2021、NOAA、NIST CODATA 等）全數通過。
2. **視覺與 2x 放大獨立審圖**：
   - 52 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核與重繪修正後蓋下 `storyboard` 關卡（`4a43ca64f183`）。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat` `tempo: 1.02`）+ `kid`（Gemini `Leda` `tempo: 1.06`），52/52 句驗證完成（4.63 字／秒 >= 4.4；`t014, t018, t026` 皆已重錄並實聽確認字正腔圓）。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33.3 LUFS`）。
   - 成片 `final.mp4`：總長 `08:29.0`（`15,270 frames`，正片 `08:08.0 >= 480s`，零冷場停頓），響度 `-14 LUFS`、True Peak `-2 dBFS`，SHA-256 `56faa480980f`。
4. **成片後獨立一般觀眾審查（兩輪，修畢複驗通過）**：
   - 第一輪獨立審查（8.8/10）僅抓出 `t014.wav` 開頭「鐘校準後」誤讀成「中校整後」；為 `t014` 補上語音覆寫 `say` 單句重配並重組後，第二輪獨立複驗寫入 `review/audience-review.md`：**9.1 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 8 語配音 `.m4a`（`en, ja, ko, es, pt, id, th, vi`）全數完成並壓進安全節奏；9 語 `.srt/.vtt` 於 8 語配音完成後重新對齊產出。
6. **QA 與上架包**：
   - `qa`：**10 / 11 PASSED**（`assemble, render, narration, pace, captions, metadata, facts, links [14/14], thumbnail, disclosure` 全綠；`policy` Jev 針對科普對照技術教學立場評 `0.51`，同 G654／P06 走 `--manual-review` 送站主核准）。
   - `approve --gate final` 已核准（`56faa480980f`）。
   - `package`：**4 / 4 PASSED**（`metadata.json sha256 2b4c1124898f`，`language_choice` 已對齊 `/admin/videos` 8 語設定）。
