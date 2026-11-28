# 製作交接紀錄：`sothatswhy-p21-car-sickness`（原來如此事務所 Ep P21）

- **題目**：為什麼會暈車，司機沒事蒙眼竟然照樣暈？（上架標題：`坐車看書就暈到想吐？其實會暈反而代表內耳超健康｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（零刪除同步，舊版移入 `_舊版/<UTC>/`）**：
  - 集數頂層成品目錄（`epDir`）：`1yopwkCx1lwvIDXLDGebbXnWkWk4QKhch`
  - 製作檔完整備份目錄（`workDir`）：`1vOD2-FCy40dLGrw4m3wxz0rv6FvwXxRo`（`製作檔/sothatswhy-p21-car-sickness`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **55 鏡、55 句**，`nobody: true` 純原理／機制／物件鏡共 **32 / 55（58.2%）**，`lint` 0 errors，`opening_hash` 維持不變。
   - 獨立查核 `verify-1.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；15 筆一手來源連結全數可開。
2. **視覺與 2x 放大獨立審圖**：
   - 55 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核與重繪修正後蓋下 `storyboard` 關卡（`ed8c9952e93a`）。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`；繁中副標精簡為「`司機沒事，蒙眼照樣暈！`」，完全退回左上乾淨藍天、零壓杯緣）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat` `tempo: 1.02`）+ `kid`（Gemini `Leda` `tempo: 1.06`），55/55 句驗證完成（4.62 字／秒 >= 4.4；`c011/c012/c031/c042` 皆實聽原檔 WAV 確認字正腔圓）。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33.3 LUFS`）。
   - 成片 `final.mp4`：總長 `08:36`（正片 `14,863 frames` = `08:15 >= 480s`，零人工冷場停頓），響度 `-14 LUFS`、True Peak `-2 dBFS`，SHA-256 `ff3329da22aa`。
4. **成片後獨立一般觀眾審查（兩輪，修畢複驗通過）**：
   - 第一輪獨立審查（8.4/10）指出後半段 `c033–c051` 連續 `750–1000ms` 停頓與縮圖副標略長；改採自然語速 `tempo 1.02/1.06` 全數拔除 `pause_after_ms` 並精簡九語副標後重新組裝，第二輪獨立複驗寫入 `review/audience-review.md`：**9.1 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 8 語配音 `.m4a`（`en, ja, ko, es, pt, id, th, vi`）全數完成；9 語 `.srt/.vtt` 於 8 語配音完成後重新對齊產出。
6. **QA 與上架包**：
   - `qa`：**11 / 11 ALL PASSED**（`assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, policy, disclosure` 全綠，Jev `0.60`，`final.mp4 sha256 ff3329da22aa`）。
   - `approve --gate final` 已核准（`ff3329da22aa`）。
   - `package`：**4 / 4 PASSED**（`upload/metadata.json` SHA-256 `eb26bf744ded`）。
