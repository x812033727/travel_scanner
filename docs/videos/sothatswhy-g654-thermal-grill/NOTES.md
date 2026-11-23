# 製作交接紀錄：`sothatswhy-g654-thermal-grill`（原來如此事務所 Ep G654）

- **題目**：為什麼溫水加冰水會燙得像被燒傷？（上架標題：`冰水加溫水竟像燙傷！皮膚為何被騙｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（已驗證 `0 differences`）**：
  - 集數頂層成品目錄（`epDir`）：`18G9zupAKBCnEF3Ildy0icIN6UXbU7GTX`（`121 files, 0 differences`：含 `final.mp4`、`thumbnail.jpg`、`narration.wav`、`timeline.json`、`metadata.json`、`thumbnails/`、`captions/`、`dubs/*.m4a`、`keyframes/`、`descriptions/`）
  - 製作檔完整備份目錄（`workDir`）：`1Qg8S7BtIYWpqmeu5DC1qRcE31rbLgYtm`（`製作檔/sothatswhy-g654-thermal-grill`，`2,108 files, 0 differences`，含 `_todrive/latest.json` 與 `SHA256SUMS`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **65 鏡、65 句**，`nobody: true` 純原理／裝置／圖解鏡比例符合系列規範（45%–65%），`lint` 0 errors。
   - 獨立查核 `verify-1.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；來源連結 14 筆可開（3 筆 DOI 因出版商阻擋自動化抓取回 HTTP 403）。
2. **視覺與 2x 放大獨立審圖**：
   - 65 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核與重繪修正後蓋下 `storyboard` 關卡。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat`）+ `kid`（Gemini `Leda`），65/65 句通過 `check-audio`（0 異常；`g052` 以 `say` 微調後完全吻合）。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33 LUFS`）。
   - 成片 `final.mp4`：`15,474 frames`（總長 `08:35`，正片 `08:14 >= 480s`），響度 `-14 LUFS`、True Peak `-2 dBFS`，SHA-256 `3bd320e7a920`。
4. **成片後獨立一般觀眾審查**：
   - 已由獨立代理完成並寫入 `review/audience-review.md`：**9.1 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 9 語 `.srt/.vtt`（`zh-TW, en, ja, ko, es, pt, id, vi, th`）皆在 8 語配音完成後重新對齊產出。
   - 8 語配音 `.m4a` 全數完成且零超長窗口（`en` max 1.10x、`ja` 1.13x、`ko` 1.11x、`es` 1.15x、`pt` 1.11x、`id` 1.11x、`th` 1.12x、`vi` 1.01x；`en/ja/ko/es/pt/id/th` 雙角由 MiniMax 合成，`vi` 小問行因 MiniMax 單聲線設計由 Gemini 補齊）。
6. **QA、上架包與後台推送**：
   - `qa`：**10 / 11 PASS**（`assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, disclosure` 全數通過；`policy` 因頻道立場設定為科技教學故 Jev `0.36–0.42` 屬系列預期常態）。
   - `approve --gate final` 已核准（`3bd320e7a920`）。
   - `package`：**4 / 4 PASSED**（`upload/metadata.json` SHA-256 `f1ed902a15d5`）。
   - `/admin/videos` `review-push` 已推送完成：**`outline`、`script`、`storyboard`、`audio`、`final`、`dubs`、`publish`** 全部進入 `pending` 待站主審核（`languages` 依規則須待站主於後台核准 `final` 後開放）。
