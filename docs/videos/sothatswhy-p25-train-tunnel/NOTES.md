# 製作交接紀錄：`sothatswhy-p25-train-tunnel`（原來如此事務所 P25 — 黑猫十步成片交付版）

- **題目**：為什麼高鐵車頭要做成長鼻子？（上架標題：`高鐵車頭拉出15公尺長鼻，竟然不是為了破風？｜原來如此事務所`）
- **更新日期**：2026-11-21
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1TxaxA5sx5Ksw5kdAJTYQv1CR8Dz6aKNZ`（`AI/備份/AI劇/原來如此事務所/建築交通與商業制度/P25`）
  - 製作檔父目錄（`製作檔`）：`1D463NdLjfoKXSxv8Nls1K7gNwefvJiwT`
  - 製作檔目錄（`workDir`）：`1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`（`P25/製作檔/sothatswhy-p25-train-tunnel`）

---

## 1. 已完成階段與驗證收據（備份至 Google Drive `0 differences` 並推送 `/admin/videos`）

1. **黑猫十步劇本、8 語 i18n 與查核清單**：
   - `brief.md`（SHA-256 `438c4a04b03c1b11261e36bd91b58133cd41475e7cfaa6c2ec731cad041ce689`）
   - `claims.md`（SHA-256 `4f4830cf924f267dede7a9108fc64071dd992825c903b7e26cec121b6c418985`）
   - `script.md`（SHA-256 `e781b195a18ab9df8b7dc0a021854d115d682d2554c676688145d704296000cd`）
   - `verify-1.md`～`verify-4.md`：獨立來源查核 `PASS`。
   - `review/narrative.json`（`narrative_hash: 3966bf44dda147dc`）：兩名獨立盲測讀者 `14/14` 全數 `YES`（`passed: true`）。
   - `review/opening-review.json`（`opening_hash: 712d95759390...`）：前 300 秒三角色嚴苛審查通過（`9.2 / 9.2 / 9.2`，`problems: []`）。
2. **85 張「劇場級動畫光影 × 厚塗水粉質感」關鍵影格與 9 語黑猫滿版縮圖**：
   - 全數以內建 `generate_image` 搭配 V2 標準 2.5 頭身設定圖（`chief-canon-v2.png` + `kid-canon-v2.png`）繪製並經 2x 四宮格審查，`nobody: true` 純機制／物件鏡共 **50 / 85 鏡（58.8%）**，零 MiniMax 生圖（US\$0.00）。
   - 9 語滿版黑猫縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）單行不換行、零壓臉遮眼。
3. **繁中雙角色 Gemini 旁白、成片組裝、QA `11/11` 與獨立成片觀眾視角審查**：
   - 繁中旁白（所長 `gemini:Sulafat` `tempo: 1.08` ＋ 小問 `gemini:Leda` `tempo: 1.12`）：85/85 句雙重轉錄審查 `0` 標記通過，全片平均語速 **`5.10`／`4.97 字／秒`**（≥ `4.4` 字／秒）。
   - `final.mp4`（`sha256: d0ff7a637893`，`18254` frames，`-14 LUFS`，true peak `-1.8 dBFS`，music bed `-33.4 LUFS`）與 9 語 `.srt` 字幕（`zh-TW, en, ja, ko, es, pt, id, vi, th`）通過 **`qa` `11 of 11 checks passed`**。
   - `review/audience-review.md`：獨立審查子代理（`a099c232322807d7468b91b79bd32535`）抓出 6 鏡圖解對照證據裁邊（`#19, #33, #37, #42, #43, #61`）與 7 鏡 2.5 頭身角色頭頂／手部裁切（`#28, #49, #60, #63, #70, #77, #84`），連同 `#17` 節奏微調共 14 鏡已全數改為 `"pull out"`／`"drift"` 重組並複驗 85 鏡結尾定格 100% 完整在框，六維度評分全數 `≥ 9.1`、總平均 **`9.23 / 10`** 正式放行。
   - `upload/` 上架包已透過 `package` 產出並通過 `4/4` 核對（`metadata.json` SHA-256 `a0440a48112c`）。
4. **8 語多語配音（全數 8/8 完成）**：
   - `dubs/{en,ja,ko,es,pt,id,vi,th}.m4a`（**全數 8 語含背景配樂混音**，`vi` 小問亦已完成 Gemini `Leda` 合成）全數收入 `upload/dubs/`，並完成 Google Drive 完整備份核驗（**`0 differences`**）與 `/admin/videos` `outline`、`script`、`final`、`publish` 推送。

---

## 2. 本集製作經驗教訓（2.5 頭身角色禁用 `"tilt down"` 與 `beat` 模式下 `"drift"` 的循環特性）

- **問題 1（2.5 頭身禁用 `"tilt down"`）**：2.5 頭身 Q 版角色的圓大頭佔據畫面上半部（`y ≈ 5%–48%`），套用 `"tilt down"`（`panZoom: 1.2` 下移至 `y = 16.7%–100%`）必然從眉毛／鏡框上方橫切整個頭頂。
- **問題 2（`still_motion: "beat"` 下 `"drift"` 會轉為五步循環）**：`tools/video/assemble/drama.mjs` 在 `still_motion: "beat"` 時，會將 `"drift"` 依鏡號 `turn % 5` 展開為 `["push-in", "pan-right", "pull-out", "pan-left", "tilt-up"]`；若寬幅對照鏡需要保證結尾 `1.0x` 全幅零裁切，必須明確指定 **`"pull out"`**（或 `"static camera"`），不能依賴 `"drift"`。

---

## 3. 站主核准 `final`/`publish` 後推送 `languages` 關卡指令

```bash
export VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos

# 站主於 /admin/videos 核准 final 與 publish 後，拉回核准狀態並推送 8 語 languages 批次：
node tools/video/cli.mjs review-pull --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-push --slug sothatswhy-p25-train-tunnel --gate languages --workdir "$VIDEO_WORKDIR"
```
