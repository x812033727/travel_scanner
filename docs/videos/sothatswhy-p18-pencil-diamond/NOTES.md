# 製作交接紀錄：`sothatswhy-p18-pencil-diamond`（原來如此事務所 Ep P18）

- **題目**：鉛筆芯與鑽石都是碳，為什麼一個能畫圖通電、一個超硬卻怕敲？（上架標題：`鉛筆芯和鑽石都是碳，為何鑽石怕一敲、鉛筆還能通電？｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（零刪除同步，舊版移入 `_舊版/<UTC>/`）**：
  - 集數頂層成品目錄（`epDir`）：`1gYSFL8Alp5WsdYGwoQRi9rV2-2j-bkT2`
  - 製作檔完整備份目錄（`workDir`）：`1Z2VUJhR_MJK-0kFZ_v_3jtp2jJa6dCdw`（`製作檔/sothatswhy-p18-pencil-diamond`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **50 鏡、50 句**，`nobody: true` 純原理／機制／物件鏡共 **25 / 50（50.0%）**，`lint` 0 errors，`opening_hash` 維持不變。
   - 獨立查核 `verify-1.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；9 筆一手來源連結皆更新為官方有效連結（USGS `pp1802j.pdf`、GIA `diamond` 等）。
2. **視覺與 2x 放大獨立審圖**：
   - 50 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核與重繪修正後蓋下 `storyboard` 關卡。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat` `tempo: 1.0`）+ `kid`（Gemini `Leda` `tempo: 1.03`），50/50 句驗證完成（4.44 字／秒 >= 4.4；`p005/p009/p026/p028/p035/p036/p036b/p037` 全數重錄並實聽確認字正腔圓）。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33.5 LUFS`）。
   - 成片 `final.mp4`：總長 `08:23`（正片 `14,472 frames` = `08:02.4 >= 480s`，零冷場停頓），響度 `-14.1 LUFS`、True Peak `-1.9 dBFS`，SHA-256 `5d526cf8a534`。
4. **成片後獨立一般觀眾審查（兩輪，修畢複驗通過）**：
   - 第一輪獨立審查（8.7/10）僅抓出 `p009.wav` 單句「先記著」口齒含糊；單句重錄為「這猜想，先記好」並重新封裝後，第二輪獨立複驗寫入 `review/audience-review.md`：**9.1 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 8 語配音 `.m4a`（`en, ja, ko, es, pt, id, th, vi`）全數完成；9 語 `.srt/.vtt` 於 8 語配音完成後重新對齊產出。
6. **QA 與上架包**：
   - `qa`：**11 / 11 ALL PASSED**（`assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, policy, disclosure` 全綠，Jev `0.69`，`final.mp4 sha256 5d526cf8a534`）。
   - `approve --gate final` 已核准（`5d526cf8a534`）。
   - `package`：**4 / 4 PASSED**。
