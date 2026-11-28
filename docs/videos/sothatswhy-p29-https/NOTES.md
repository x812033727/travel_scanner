# 製作交接紀錄：`sothatswhy-p29-https`（原來如此事務所 Ep P29）

- **題目**：為什麼網址多了個 S（HTTPS）還不夠防詐騙？（上架標題：`網址小鎖頭竟然會騙人？幾乎所有釣魚站都有 HTTPS｜原來如此事務所`）
- **完成日期**：2026-11-23
- **版本規格**：2026-11-14 / 11-18 / 11-20 `#2197` 新規則完全重製版（劇場級動畫光影 × 厚塗水粉質感、2.5 頭身系列標準設定圖、黑猫滿版 `heimao-left` 九語縮圖、雙角色繁中 Gemini 旁白 + 8 語配音 + 9 語字幕）
- **Google Drive 備份目錄（零刪除同步，舊版移入 `_舊版/<UTC>/`）**：
  - 集數頂層成品目錄（`epDir`）：`17wKEo-6PvkA1_0LflpKiUHUCmB7XCOBT`
  - 製作檔完整備份目錄（`workDir`）：`1A0AQqP-iSdvjSrNkHFj2nCjqHt9YpJUd`（`製作檔/sothatswhy-p29-https` = `1zi1PMCGElzLKAXhIO1HrnANAoJfh9f1E`）

---

## 1. 成片與品質驗證總結

1. **腳本、查核與敘事盲測**：
   - `video.json`：共 **63 鏡、63 句**，`nobody: true` 純原理／機制／物件鏡共 **40 / 63（63.5%）**，`lint` 0 errors，`opening_hash`（`43302dfd99b35c06`）維持不變。
   - 獨立查核 `verify-2.md`（0 `NOT FOUND`）與盲測敘事評審皆通過；12 筆一手來源連結（IETF RFC 8446 / 9849、Google Chrome Security Blog、APWG、CT 等）全數可開。
2. **視覺與 2x 放大獨立審圖**：
   - 63 張 16:9 劇場級厚塗水粉插圖皆以內建 `generate_image` 繪製並透過 `keyframes import --provider external --usd 0` 匯入（未使用 MiniMax 生圖）；人物鏡以系列標準圖 `chief-canon-v2.png` / `kid-canon-v2.png` 鎖定外型。
   - 經獨立代理逐格 2x 放大審核與重繪修正後蓋下 `storyboard` 關卡（`bf3cfef8c3ff`）。
   - 九語黑猫滿版 `heimao-left` 縮圖全部產出並驗證通過（`1280x720 JPEG`；繁中副標精簡為「`多一個S到底防了誰？`」，完全退回左上乾淨藍天、零遮擋右側壞鎖頭與小偷）。
3. **成片音畫與配樂**：
   - 繁中雙角色旁白：`chief`（Gemini `Sulafat`）+ `kid`（Gemini `Leda`），63/63 句驗證完成（5.64 字／秒 >= 4.4）；`h034` 單句重錄對齊原字幕、`h035/h037/h055` 字幕對齊實音、`h051`（2026 年 3 月）與 `h060`（收件人）皆直接實聽原檔 WAV 確認字正腔圓。
   - 配樂：系列標準背景音樂 `sothatswhy-bed-r2.m4a`（`-33.3 LUFS`）。
   - 成片 `final.mp4`：總長 `08:27`（正片 `14,595 frames` = `08:06.5 >= 480s`），響度 `-14 LUFS`、True Peak `-2 dBFS`，SHA-256 `1871330504a4`。
4. **成片後獨立一般觀眾審查（兩輪，修畢複驗通過）**：
   - 第一輪獨立審查（8.0/10）指出後半段 `1400ms` 連環冷場、4 句字幕實音用詞差異與縮圖副標過長；全數修畢並重新組裝後，由獨立代理進行第二輪複驗並寫入 `review/audience-review.md`：**9.0 / 10 PASS**，**0 項 `must_fix`**。
5. **9 語字幕與 8 語配音**：
   - 8 語配音 `.m4a`（`en, ja, ko, es, pt, id, th, vi`）全數完成且零超長窗口；9 語 `.srt/.vtt` 於 8 語配音完成後重新對齊產出。
6. **QA 與上架包**：
   - `qa`：**11 / 11 ALL PASSED**（`assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, policy, disclosure` 全綠，`final.mp4 sha256 1871330504a4`）。
   - `approve --gate final` 已核准（`1871330504a4`）。
   - `package`：**4 / 4 PASSED**（`upload/metadata.json` SHA-256 `8a87643a3fcb`）。
