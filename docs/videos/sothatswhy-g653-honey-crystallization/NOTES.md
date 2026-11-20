# 製作交接紀錄：`sothatswhy-g653-honey-crystallization`（原來如此事務所 G653 — 黑猫十步重製版）

- **題目**：為什麼純蜂蜜放久會變白結塊？（上架標題：`蜂蜜放久變白結塊，竟然不是摻了假糖？｜原來如此事務所`）
- **更新日期**：2026-11-20
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1HtZhPqx62cGU1eLJwUNn5kXyWQRA-7S8`（`AI/備份/AI劇/原來如此事務所/飲食與廚房科學/G653`）
  - 製作檔父目錄（`製作檔`）：`1c4tgB6xOEiOoBctYieK9feTDgtyjFQIT`
  - 製作檔目錄（`workDir`）：`1xAfL9Ejlz8zjevh8p5TsGiDHbAiWuEgI`（`G653/製作檔/sothatswhy-g653-honey-crystallization`）

---

## 1. 已完成階段與雜湊（2026-11-20 新規全部通過並備份至 Google Drive `0 differences`）

1. **黑猫十步劇本（R44 定稿）、8 語 i18n 與查核清單**：
   - `brief.md`（SHA-256 `82cfd3c553c5e2934933ac88c79a06c2f001346b21412c13256784fe9d7f3046`）
   - `claims.md`（SHA-256 `0e84ff32a91eb6363a5f56b8d04c5943e09e2a529d411886d6e0759948d759b8`，嚴守 V184 食品標示與科學邊界：僅談結晶機制、水糖比例、HMF 四十毫克國際品質界線與控溫晶種法，零療效／零抗氧化宣稱）
   - `video.json`（SHA-256 `3c983ad7ce768d56b7119c79359ee4295815874282561b716924662d06e9e5d1`）：共 **70 鏡、70 句**，`intro_at: "none"`、單一熟悉提問無問題菜單、前 15 秒呼應縮圖副標、45%–65% `nobody: true` 機構／微觀原理鏡、所長 `tempo: 1.08` + 小問 `tempo: 1.12` 確保語速 `>= 4.4 字／秒`、`lint` **0 errors、0 narrative/title/i18n warnings**。
   - `script.md`（SHA-256 `2f064afd571b069e7eaf1fb145920ec4bbc86356bd6038e287a1193647f53b50`）
   - `verify-1.md`：獨立來源查核 `PASS`。
   - `i18n/{en,ja,ko,es,pt,id,vi,th}.json`：70 句 8 語口語化翻譯與黑猫縮圖文案全數同步對齊 R44 `source_hash`（零缺漏、零舊雜湊）。
2. **盲測 14 題敘事審查與前 300 秒三角色嚴苛審稿（皆滿票通過）**：
   - `review/narrative.json`（`narrative_hash: a3241313b49ea458`）：兩名獨立盲測讀者 `14/14` 全數 `YES`（`passed: true`）。
   - `review/opening-review.json`（`opening_hash: 872109256fe36c30541ed921f110478eedd36f8e3d60fe73b1bcafda95387dde`）：三名獨立審查代理（`newcomer 9.2`、`scroller 9.2`、`stickler 9.2`）全數 `would_stay_300: true`、`swipe_at: null`、`problems: []`。
3. **70 張「劇場級動畫光影 × 厚塗水粉質感」關鍵影格與 9 語黑猫滿版縮圖（全數完成，US\$0.00）**：
   - 全數以內建 `generate_image` 搭配 V2 標準 2.5 頭身設定圖（`chief-canon-v2.png` + `kid-canon-v2.png`）繪製並經 2x 四宮格審查，`keyframes import --provider external --usd 0` 匯入，`outline`、`script`、`look`、`storyboard` 四關已核准。
   - 9 語滿版黑猫縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）已透過 `render` 產出並完成字區與人物零遮擋目檢。
4. **暫停原因**：
   - 繁中 Gemini TTS（`Sulafat` + `Leda`）因 2026-11-20 Google AI Ultra 帳號池當日 RPD 配額耗盡（`HTTP 429 video_speech_upstream_busy`，`70` 句中剩 `69` 句待合成）暫停於 `tts` 關卡前。

---

## 2. Gemini TTS 每日配額重置後（或後台切換新 Ultra 帳號後）一鍵續跑指令

```bash
export VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos
export VIDEO_SECOND_OPINION="/home/antigravity/.cache/whisper-venv/bin/python /home/antigravity/x812033727/travel_scanner/tools/video/tts/whisper_second_opinion.py"

# 1. 若從全新雲端 VM 接手，先從 Google Drive 製作檔目錄 1xAfL9Ejlz8zjevh8p5TsGiDHbAiWuEgI 還原工作目錄（含 70 張關鍵影格與 9 語縮圖）
# 2. 合成繁中雙角色 Gemini 旁白並跑雙重轉錄審查：
node tools/video/cli.mjs tts --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs check-audio --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs approve --slug sothatswhy-g653-honey-crystallization --gate audio --workdir "$VIDEO_WORKDIR" --note "zh-TW Sulafat+Leda >=4.4 chars/s & check-audio passed"

# 3. 產生鏡頭表、組裝成片、產生 9 語字幕、合成 8 語 MiniMax 配音與 QA（11/11）：
node tools/video/cli.mjs clips --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs assemble --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs captions --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs dub --slug sothatswhy-g653-honey-crystallization --provider minimax --locale en,ja,ko,es --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs dub --slug sothatswhy-g653-honey-crystallization --provider minimax --locale pt,id,vi,th --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs qa --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"

# 4. 派獨立代理完成成片一般觀眾視角挑刺審查（寫入 review/audience-review.md），如有瑕疵修畢重跑 qa 11/11 後核准打包：
node tools/video/cli.mjs approve --slug sothatswhy-g653-honey-crystallization --gate final --workdir "$VIDEO_WORKDIR" --note "Independent audience review & QA 11/11 passed"
node tools/video/cli.mjs package --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"

# 5. 先將完整工作目錄備份回 Google Drive 製作檔父目錄 1c4tgB6xOEiOoBctYieK9feTDgtyjFQIT 驗證 0 differences，再推上後台 /admin/videos：
node tools/video/cli.mjs review-push --slug sothatswhy-g653-honey-crystallization --gate final --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-push --slug sothatswhy-g653-honey-crystallization --gate publish --workdir "$VIDEO_WORKDIR"
```
