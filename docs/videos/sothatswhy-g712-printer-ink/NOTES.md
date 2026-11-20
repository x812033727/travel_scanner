# 製作交接紀錄：`sothatswhy-g712-printer-ink`（原來如此事務所 G712 — 黑猫十步成片交付版）

- **題目**：為什麼印表機賣得比墨水還便宜？（上架標題：`印表機賣得比墨水還便宜，廠商到底靠什麼賺回來？｜原來如此事務所`）
- **更新日期**：2026-11-20
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1e0pHfJjstqauJfRwaNvgPrbRPxDO2HiA`（`AI/備份/AI劇/原來如此事務所/建築交通與商業制度/G712`）
  - 製作檔父目錄（`製作檔`）：`1PI1d5-3xNz-ZxhYmBONibeBGhAC0s8Np`
  - 製作檔目錄（`workDir`）：`1lyP9SkklYSOzsNOQSRmVH_-gChR3EHr_`（`G712/製作檔/sothatswhy-g712-printer-ink`）

---

## 1. 已完成階段與驗證收據（備份至 Google Drive `0 differences` 並推送 `/admin/videos`）

1. **黑猫十步劇本、來源查核與雙盲／開場審查**：
   - `brief.md`（SHA-256 `229043462592abf9d29e0686a9f21d8e13e6b1ecd53d7acc7c2368b1c8964759`）
   - `claims.md`（SHA-256 `a1abf4415a83cacbefd0120bd7aa4691018ddd108a146d6ee2edfd76e93b1420`）
   - `script.md`（SHA-256 `ce6cfa06a9122e94eb3bd01b95cc027bba0cf75d203bee9c699f4348c0eaef05`）
   - `verify-1.md`：10/10 命題獨立查核 `PASS`。
   - `review/narrative.json`：兩名獨立盲測讀者 `14/14` 全數 `YES`（`passed: true`）。
   - `review/opening-review.json`（`opening_hash: 7ccca3941824...`）：前 300 秒三角色嚴苛審查通過（`problems: []`）。
2. **76 張「劇場級動畫光影 × 厚塗水粉質感」關鍵影格與 9 語黑猫滿版縮圖**：
   - 全數以內建 `generate_image` 搭配 V2 標準 2.5 頭身設定圖（`chief-canon-v2.png` + `kid-canon-v2.png`）繪製並經 2x 四宮格審查，`nobody: true` 純機制／物件鏡共 **47 / 76 鏡（61.8%）**，零 MiniMax 生圖（US\$0.00）。
   - 9 語滿版黑猫縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）單行不換行、零壓臉遮眼。
3. **繁中雙角色 Gemini 旁白、成片組裝、QA `11/11` 與獨立成片觀眾視角審查**：
   - 繁中旁白（所長 `gemini:Sulafat` `tempo: 1.08` ＋ 小問 `gemini:Leda` `tempo: 1.12`）：76/76 句雙重轉錄審查 `0` 標記通過，全片平均語速 **`4.66 字／秒`**（≥ `4.4` 字／秒）。
   - `final.mp4`（`sha256: 398669167fa5`，`19567` frames，`-14 LUFS`，true peak `-2 dBFS`，music bed `-32.9 LUFS`）與 9 語 `.srt` 字幕（`zh-TW, en, ja, ko, es, pt, id, vi, th`）通過 **`qa` `11 of 11 checks passed`**。
   - `review/audience-review.md`：獨立審查子代理抓出 `#04, #31, #56, #58, #65, #67` 共 6 張左右對照鏡在 `pan left/right`（`panZoom: 1.2`）下裁切左右 `16.7%` 邊緣，已全數改為 `"pull out"` 重組並複驗 `build/last-*.png` 結尾定格 100% 完整在框，六維度評分全數 `≥ 8.9`、總平均 **`9.12 / 10`** 正式放行。
   - `upload/` 上架包已透過 `package` 產出並通過全項核對，`outline`、`script`、`final`、`publish` 已推送 `/admin/videos` 待審。
4. **多語 MiniMax 配音進度**：
   - `dubs/{en,ja,ko,es,pt,id,th}.m4a`（**7 語純 MiniMax 雙聲道配音含背景配樂混音**）已全數合成通過並收入 `upload/dubs/` 與 Google Drive。
   - 僅剩 **`vi`（越南語）**：因 `tools/video/dubs/plan.mjs` 中 `DUB_MINIMAX_VOICES.vi` 僅設 1 組女聲（`Vietnamese_kindhearted_girl`），雙人對話的第二角色（小問 19 句）自動回退至 Gemini `Leda`，受 2026-11-20 當日 Google AI Ultra Gemini TTS RPD 配額限制暫待重置。

---

## 2. 本集製作經驗教訓（寬幅左右並排對照鏡運鏡規則）

- **問題**：`still_motion: "beat"`（`beat-motion-v5`）對 `"pan left"` 與 `"pan right"` 採用 `panZoom: 1.2`，會在鏡頭後段永久裁掉畫面最右或最左 `16.7%` 寬度；若關鍵影格為「左 A 對比右 B」且硬幣堆、長條圖或箭頭落在 `x < 16%` 或 `x > 84%`，成片落點會把一側證據裁出框外，造成靜音看圖比例顛倒。
- **解法**：凡寬幅左右並排對照鏡（天平、雙機對照、雙邊硬幣堆、雙柱長條圖），`scene.data.camera` 一律優先選用 **`"pull out"`**（前 0.8s `1.22x` 居中聚焦、2.2s 拉開至 `1.0x` 全幅定格）或 `"drift"`，既保有動態重拍又確保左右兩端關鍵證據 100% 同框不裁切。

---

## 3. 站主核准 `final`/`publish` 並待 Gemini TTS RPD 重置後補齊 `vi` 配音與 `languages` 關卡指令

```bash
export VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos

# 1. Gemini TTS 每日配額重置後補齊 vi 配音並重新打包：
node tools/video/cli.mjs dub --slug sothatswhy-g712-printer-ink --provider minimax --locale vi --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs captions --slug sothatswhy-g712-printer-ink --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs qa --slug sothatswhy-g712-printer-ink --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs package --slug sothatswhy-g712-printer-ink --workdir "$VIDEO_WORKDIR"

# 2. 站主於 /admin/videos 核准 final 與 publish 後，同步拉回核准狀態、推送 8 語 languages 批次並同步雲端 0 differences：
node tools/video/cli.mjs review-pull --slug sothatswhy-g712-printer-ink --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-push --slug sothatswhy-g712-printer-ink --gate languages --workdir "$VIDEO_WORKDIR"
```
