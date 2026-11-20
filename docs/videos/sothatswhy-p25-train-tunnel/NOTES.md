# 製作交接紀錄：`sothatswhy-p25-train-tunnel`（原來如此事務所 P25 — 黑猫十步重製版）

- **題目**：為什麼高鐵車頭要做成長鼻子？（上架標題：`高鐵車頭拉出15公尺長鼻，竟然不是為了破風？｜原來如此事務所`）
- **更新日期**：2026-11-20
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1TxaxA5sx5Ksw5kdAJTYQv1CR8Dz6aKNZ`（`AI/備份/AI劇/原來如此事務所/建築交通與商業制度/P25`）
  - 製作檔父目錄（`製作檔`）：`1D463NdLjfoKXSxv8Nls1K7gNwefvJiwT`
  - 製作檔目錄（`workDir`）：`1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`（`P25/製作檔/sothatswhy-p25-train-tunnel`）

---

## 1. 已完成階段與雜湊（2026-11-20 新規全部通過並備份至 Google Drive `0 differences`）

1. **黑猫十步劇本、8 語 i18n 與查核清單**：
   - `brief.md`（SHA-256 `438c4a04b03c1b11261e36bd91b58133cd41475e7cfaa6c2ec731cad041ce689`）
   - `claims.md`（SHA-256 `4f4830cf924f267dede7a9108fc64071dd992825c903b7e26cec121b6c418985`）
   - `video.json`（SHA-256 `271fb6278496b253da86465be699b889d4d1b0585eaf1033dbcaca314291f201`）：共 **85 鏡、85 句**，`intro_at: "none"`（0:00 直接進第一鏡對話）、單一熟悉提問無問題菜單、前 15 秒呼應黑猫滿版縮圖副標、45%–65% `nobody: true` 純原理／機構鏡、`lint` **0 errors、0 narrative/title/i18n warnings**。
   - `script.md`（SHA-256 `e781b195a18ab9df8b7dc0a021854d115d682d2554c676688145d704296000cd`）
   - `verify-1.md`～`verify-4.md`：獨立來源查核 `PASS`。
2. **盲測 14 題敘事審查與前 300 秒三角色嚴苛審稿（皆滿票通過）**：
   - `review/narrative.json`（`narrative_hash: 3966bf44dda147dc`）：兩名獨立盲測讀者 `14/14` 全數 `YES`（`passed: true`）。
   - `review/opening-review.json`（`opening_hash: 712d95759390af290e4c7deb782adbf1c0da36cc62fbfd4559ecd133c762a35a`）：三名獨立審查代理（`newcomer 9.2`、`scroller 9.2`、`stickler 9.2`）全數 `would_stay_300: true`、`swipe_at: null`、`problems: []`。
3. **85 張「劇場級動畫光影 × 厚塗水粉質感」關鍵影格與 9 語黑猫滿版縮圖（全數完成，US\$0.00）**：
   - 全數以內建 `generate_image` 搭配 V2 標準 2.5 頭身設定圖（`chief-canon-v2.png` + `kid-canon-v2.png`）繪製並經 2x 四宮格審查，`keyframes import --provider external --usd 0` 匯入，`look` 與 `storyboard` 關卡已核准。
   - 9 語滿版黑猫縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）已透過 `render` 產出並完成字區與人物零遮擋目檢。
4. **繁中雙角色 Gemini 旁白快取進度**：
   - `audio/` 目錄已快取 `gemini-3.8-flash-tts` 80 句與 `gemini-3.8-flash-lite-tts` 前 26 句（`p001`–`p026`）；剩餘未合成句（預設 `flash-tts` 剩 32 句，或 `flash-lite-tts` 剩 59 句）因 2026-11-20 Google AI Ultra 帳號池當日 Gemini TTS RPD 配額耗盡（`HTTP 429 video_speech_upstream_busy`）暫停。

---

## 2. Gemini TTS 每日配額重置後（或後台切換新 Ultra 帳號後）一鍵續跑指令

> 站主若於 `/admin/settings` 的 Google AI Ultra 帳號池對尚有當日 TTS 額度的帳號點「從此開始」，或於太平洋時間午夜（`America/Los_Angeles` 00:00）RPD 自動重置後，直接執行以下指令即可完成成片、8 語 MiniMax 配音、QA、獨立成片審查與後台推送：

```bash
export VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos
export VIDEO_SECOND_OPINION="/home/antigravity/.cache/whisper-venv/bin/python /home/antigravity/x812033727/travel_scanner/tools/video/tts/whisper_second_opinion.py"

# 1. 若從全新雲端 VM 接手，先從 Google Drive 製作檔目錄 1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd 還原工作目錄（含快取音檔與 85 張關鍵影格）
# 2. 補齊剩餘繁中 Gemini 旁白（Sulafat + Leda）並跑雙重轉錄審查：
node tools/video/cli.mjs tts --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs check-audio --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs approve --slug sothatswhy-p25-train-tunnel --gate audio --workdir "$VIDEO_WORKDIR" --note "zh-TW Sulafat+Leda >=4.4 chars/s & check-audio passed"

# 3. 產生 beat-motion-v5 鏡頭表、組裝成片、產生 9 語字幕、合成 8 語 MiniMax 配音與 QA（11/11）：
node tools/video/cli.mjs clips --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs assemble --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs captions --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs dub --slug sothatswhy-p25-train-tunnel --provider minimax --locale en,ja,ko,es --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs dub --slug sothatswhy-p25-train-tunnel --provider minimax --locale pt,id,vi,th --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs qa --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"

# 4. 派獨立代理完成成片一般觀眾視角挑刺審查（寫入 review/audience-review.md，確認標題與縮圖副標承諾兌現、各維度 >= 7.5、總分 >= 8.0），如有瑕疵修畢重跑 qa 11/11 後核准打包：
node tools/video/cli.mjs approve --slug sothatswhy-p25-train-tunnel --gate final --workdir "$VIDEO_WORKDIR" --note "Independent audience review & QA 11/11 passed"
node tools/video/cli.mjs package --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"

# 5. 先將完整工作目錄備份回 Google Drive 製作檔父目錄 1D463NdLjfoKXSxv8Nls1K7gNwefvJiwT 驗證 0 differences，再推上後台 /admin/videos：
node tools/video/cli.mjs review-push --slug sothatswhy-p25-train-tunnel --gate final --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-push --slug sothatswhy-p25-train-tunnel --gate publish --workdir "$VIDEO_WORKDIR"
```
