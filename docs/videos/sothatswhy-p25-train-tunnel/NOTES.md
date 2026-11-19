# 製作交接紀錄：`sothatswhy-p25-train-tunnel`（原來如此事務所 Ep 25）

- **題目**：為什麼高鐵車頭要做成長鼻子？（上架標題：`高鐵車頭拉那麼長，居然不是為了防風？｜原來如此事務所`）
- **更新日期**：2026-11-18
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1TxaxA5sx5Ksw5kdAJTYQv1CR8Dz6aKNZ`（`AI/備份/AI劇/原來如此事務所/建築交通與商業制度/P25`）
  - 製作檔目錄（`workDir`）：`1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`（`P25/製作檔/sothatswhy-p25-train-tunnel`）

---

## 1. 已完成階段與雜湊（100% 備份至 Google Drive）

1. **企劃、查核清單與劇本定稿**：
   - `brief.md`（SHA-256 `b9515e01d0894990065ee513a655dd67bbe64bec4f998605f828199da675b08a`）：已推上 `/admin/videos` `outline` 待審（Review ID `36fda6b3-e656-4272-a991-6219b75d3060`）。
   - `claims.md`（SHA-256 `a00bd71151ca72461265fb183fcbaf8a11497a0129ce7c744630066938798e4a`）：19 筆一手文獻（JR 西日本、JR 東海、JR 東日本、RTRI、NASA、台灣高鐵、仲津英治專訪與論文等）。
   - `video.json`（SHA-256 `18623ea7ef6385e2f9e0c04b946b966d4b889037e96aacbc51b8bb0df8807779`）：共 **106 鏡、107 句、2,931 口語字元**，`nobody: true` 純原理／機構／物件鏡共 **64 / 106（60.4%）**，14 組開放懸念（`loops[]`），`thumbnail.data.layout: "heimao"`，`node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel` **0 errors（含 8 語 i18n 零警告）**。
   - `script.md`（SHA-256 `fe86b114b2afaf72b25d0ac2f2e863f69c56c424f237df214af6b2b8af7426ab`，`narrative 081c62333b99a9b4`，`speech 8aa7b9b763bc411e`）：已推上 `/admin/videos` `script` 待審（Review ID `8c062139-1b36-432d-96cf-50da1dd34597`）。
   - `story-lexicon/current.json`（`lexicon_sha256`: `f81576a81ffac051cae8e8e413bace9e414b58b1222effa4ba24eab7a9d76501`）。
2. **獨立查核與盲測敘事評審（皆通過）**：
   - `verify-3.md`：獨立查核代理逐句對照 19 筆來源與 8 語翻譯，結論 **`Overall Verdict: PASS`（`0 NOT FOUND`）**。
   - `review/narrative.json`：兩名盲測讀者獨立審閱通過（Reader H `14/14`、Reader G `13/14`，`storytelling panel: passed`）。
3. **系列 V2 標準角色設定圖（`look` 關卡已核准，花費 US\$0.00）**：
   - 已於 `characters/` 綁定系列正式 2.5 頭身設定圖 `chief-canon-v2.png`（`f216bce4775c3b1e`）與 `kid-canon-v2.png`（`c8e05148dad3375c`），`approvals.json` 已蓋 `look`。
4. **繁中雙角色 Gemini 旁白、分軌音檔、配樂與八語翻譯稿**：
   - `narration.wav`（`09:52`，全片平均 **5.15 字／秒**；所長 `gemini:Sulafat` 約 **5.04 字／秒**，小問 `gemini:Leda` `tempo: 1.12` 約 **5.89 字／秒**，皆高於 `>= 4.4 字／秒` 門檻）。
   - `timeline.json`（`speech_hash: 8aa7b9b763bc411e`）、`audio/`（107 句單句 WAV 與快取）、`recordings/`（`zh-TW.wav` + `manifest.json`）、`music/0.mp3` 已完整產出並備份至雲端。
   - `i18n/{en,ja,ko,es,pt,id,vi,th}.json`：8 語完整口語化配音稿、標題、說明欄、章節與黑猫版縮圖大字皆已對齊真實 `timeline.json` 字數上限（`over max_chars: 0`）並寫入 Repo。

---

## 2. 暫停原因與待續事項

1. **內建 `generate_image`（`gemini-3.1-flash-image`）配額冷卻（約 48 小時）**：
   - 依站主鐵律（`docs/videos/lessons/sothatswhy.md`），**嚴禁改用 MiniMax `image-01` 或任何程式佔位圖**，因此停在 `keyframes` 前，等待內建生圖配額恢復後直接繪製 106 張「劇場級動畫光影 × 厚塗水粉質感」插圖與 1 張黑猫滿版縮圖底圖（`heimao-hero.png`）。
2. **配音與後台儲存池備註**：
   - `dub --provider minimax` 與 `captions` 在產線架構上須等 `assemble` 寫出含片頭片尾幀數的 `checks.json`（`brandingCurrent`）後執行；8 語 `i18n/*.json` 已全數就緒，成片組裝後即可直接一鍵合成 8 語 MiniMax 配音與 9 語字幕。
   - 繁中 `check-audio --second-opinion` 107 句已有 101 句直接通過；剩餘 6 句（`p047, p057, p079, p091, p101, p103`，多為日文學者姓氏「原田巌／仲津英治／石塚理」同音辨識差異）因 Gemini TTS 當日配額達上限暫保留既有音檔，配額恢復後可先選擇性重錄或人工試聽確認。
   - 後台 `/admin/videos` 目前回傳 `HTTP 507 video_review_store_full`（`the review store is full; publish or delete videos`），因此含大型二進位檔的 `look`／`audio`（以及 `sothatswhy-p29-https` 的 `publish`）暫不硬塞亦不刪除後台任何舊審核項目，待站主將已核准集數上架釋出空間後再補推。

---

## 3. 配額恢復後續跑指令（Copy-Paste 即可接手）

```bash
# 1. 從 Google Drive 還原工作目錄至本機 /tmp/mokaair-work/videos/sothatswhy-p25-train-tunnel
export VIDEO_WORKDIR=/tmp/mokaair-work/videos
mkdir -p "$VIDEO_WORKDIR/sothatswhy-p25-train-tunnel" "$VIDEO_WORKDIR/_series/sothatswhy"
cp -r docs/videos/so-thats-why/series-sheets/characters "$VIDEO_WORKDIR/_series/sothatswhy/"
# （用 gdrive readonly download 從 workDir 1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd 拉回 narration.wav, timeline.json, audio/, recordings/, characters/, music/, approvals.json, branding.json, languages.json, review/, state.json）

# 2. 用內建 generate_image (AspectRatio "16:9") 繪製 106 鏡插圖：
#    - 有 chief 傳 docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png 至 ImagePaths
#    - 有 kid   傳 docs/videos/so-thats-why/series-sheets/characters/kid/kid-canon-v2.png 至 ImagePaths
#    - nobody: true (64 鏡) 不傳人物圖
#    匯入並派獨立代理做 2x 四宮格審圖：
node tools/video/cli.mjs keyframes import --slug sothatswhy-p25-train-tunnel --dir /tmp/p25-kf --provider external --model built-in-image-gen --usd 0 --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs approve --slug sothatswhy-p25-train-tunnel --gate storyboard --workdir "$VIDEO_WORKDIR" --note "2x quadrant audit passed"

# 3. 繪製黑猫滿版縮圖底圖 (keyframes/heimao-hero.png，上半 28% 明亮乾淨天空留字區、下半 72% 15m 翠鳥尖鼻 vs 8m 短鼻衝進山洞氣壓波對比 + 小問摀耳驚呼，零文字)

# 4. 渲染、組裝成片、產生 9 語字幕與 8 語 MiniMax 配音、跑 QA：
node tools/video/cli.mjs render --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs assemble --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs captions --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
NODE_USE_ENV_PROXY=1 node tools/video/cli.mjs dub --slug sothatswhy-p25-train-tunnel --provider minimax --locale en,ja,ko,es,pt,id,vi,th --workdir "$VIDEO_WORKDIR"
NODE_USE_ENV_PROXY=1 node tools/video/cli.mjs check-audio --slug sothatswhy-p25-train-tunnel --locale en,ja,ko,es,pt,id,vi,th --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs qa --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"

# 5. 派獨立代理完成一般觀眾視角成片審查 (review/audience-review.md)，修畢重跑 qa 後打包上架包、備份雲端並推後台：
node tools/video/cli.mjs approve --slug sothatswhy-p25-train-tunnel --gate audio --workdir "$VIDEO_WORKDIR" --note "9-locale audio verified"
node tools/video/cli.mjs approve --slug sothatswhy-p25-train-tunnel --gate final --workdir "$VIDEO_WORKDIR" --note "audience review & qa passed"
node tools/video/cli.mjs package --slug sothatswhy-p25-train-tunnel --workdir "$VIDEO_WORKDIR"
# 同步至 epDir 1TxaxA5sx5Ksw5kdAJTYQv1CR8Dz6aKNZ 與 workDir 1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd 並驗證 0 差異，再推 review-push --gate final / publish / languages
