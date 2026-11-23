# 製作交接紀錄：`sothatswhy-p06-bubble-film`（原來如此事務所 Ep P06）

- **題目**：方框吹出圓泡泡、透明水變彩虹、頭頂變黑就快破？同一層肥皂膜怎麼同時搞定形狀跟光？（上架標題：`方框為何吹出圓泡泡？透明水變彩虹、頭頂一黑竟快破！｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（零刪除同步，舊版移入 `_舊版/<UTC>/`）**：
  - 集數頂層成品目錄（`epDir`）：`1I9ZqDj35TqviYPWM8aoRExPFbIORSjSh`
  - 製作檔完整備份目錄（`workDir`）：`1Oj7rzA5XT8QOGJ97o47HCc6I9T_862K5`（`製作檔/sothatswhy-p06-bubble-film`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **53 鏡、53 句**，`nobody: true` 純原理／機制／物件鏡占比達 **60%+**，`lint` 0 errors，`opening_hash` 維持不變。
   - 獨立查核 `verify-3.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；10 筆一手來源連結（Exploratorium、Virginia Tech、Wolfram MathWorld、CU Boulder、OpenStax Thin Film Interference）全部 HTTP 200 通過。
2. **視覺與 2x 放大獨立審圖**：
   - 53 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核並修正 11 項 `must_fix` 後蓋下 `storyboard` 關卡（`2b72d24b80be`）。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat` `tempo: 1.02`）+ `kid`（Gemini `Leda` `tempo: 1.06`），53/53 句驗證完成（4.54 字／秒 >= 4.4；`b021, b035c, b038, b042, b044b` 皆已重錄並實聽確認字正腔圓）。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33.5 LUFS`）。
   - 成片 `final.mp4`：總長 `08:38.7`（`15,560 frames`，正片 `08:17.7 >= 480s`，零冷場停頓），響度 `-14 LUFS`、True Peak `-2 dBFS`，SHA-256 `4aa6ff88aa16`。
4. **成片後獨立一般觀眾審查（兩輪，修畢複驗通過）**：
   - 第一輪獨立審查（8.9/10）僅抓出 `b021.wav` 單句因舊 `say` 頓號誘發「碰出」讀成「碰觸」；移除 `say` 覆寫單句重錄並重組後，第二輪獨立複驗寫入 `review/audience-review.md`：**9.2 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 8 語配音 `.m4a`（`en, ja, ko, es, pt, id, th, vi`）全數完成並壓進安全節奏；9 語 `.srt/.vtt` 於 8 語配音完成後重新對齊產出。
6. **QA 與上架包**：
   - `qa`：**10 / 11 PASSED**（`assemble, render, narration, pace, captions, metadata, facts, links [10/10], thumbnail, disclosure` 全綠；`policy` Jev 針對科普對照技術教學立場評 `0.50`，同 G654 走 `--manual-review` 送站主核准）。
   - `approve --gate final` 已核准（`4aa6ff88aa16`）。
   - `package`：**4 / 4 PASSED**（`metadata.json sha256 9694dc4303b0`，`language_choice` 已對齊 `/admin/videos` 8 語設定）。
