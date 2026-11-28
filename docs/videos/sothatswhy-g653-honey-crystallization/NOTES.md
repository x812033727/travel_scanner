# 製作交接紀錄：`sothatswhy-g653-honey-crystallization`（原來如此事務所 G653 — 黑猫十步成片交付版）

- **題目**：為什麼純蜂蜜放久會變白結塊？（上架標題：`蜂蜜放久變白結塊，竟然不是摻了假糖？｜原來如此事務所`）
- **更新日期**：2026-11-21
- **Google Drive 備份目錄**：
  - 集數根目錄（`epDir`）：`1HtZhPqx62cGU1eLJwUNn5kXyWQRA-7S8`（`AI/備份/AI劇/原來如此事務所/飲食與廚房科學/G653`）
  - 製作檔父目錄（`製作檔`）：`1c4tgB6xOEiOoBctYieK9feTDgtyjFQIT`
  - 製作檔目錄（`workDir`）：`1xAfL9Ejlz8zjevh8p5TsGiDHbAiWuEgI`（`G653/製作檔/sothatswhy-g653-honey-crystallization`）

---

## 1. 已完成階段與驗證收據（備份至 Google Drive `0 differences` 並推送 `/admin/videos`）

1. **黑猫十步劇本（R45 定稿）、8 語 i18n、V184 紅線與查核清單**：
   - `brief.md`（SHA-256 `82cfd3c553c5e2934933ac88c79a06c2f001346b21412c13256784fe9d7f3046`）
   - `claims.md`（SHA-256 `0e84ff32a91eb6363a5f56b8d04c5943e09e2a529d411886d6e0759948d759b8`，100% 遵守 V184 食品標示與科學邊界：僅談結晶物理化學、水糖比例、HMF 四十毫克國際品質界線、紅外線光譜與 14°C 控溫晶種法，零療效／零殺菌／零保健宣稱）
   - `verify-1.md`：獨立來源查核 `PASS`。
   - `review/narrative.json`（`narrative_hash: cbd588635358db9f`）：兩名獨立盲測讀者 `14/14` 全數 `YES`（`passed: true`）。
   - `review/opening-review.json`（`opening_hash: 44c541b3e708...`）：前 300 秒三角色嚴苛審查通過（`9.2 / 9.2 / 9.2`，`problems: []`）。
2. **70 張「劇場級動畫光影 × 厚塗水粉質感」關鍵影格與 9 語黑猫滿版縮圖**：
   - 全數以內建 `generate_image` 搭配 V2 標準 2.5 頭身設定圖（`chief-canon-v2.png` + `kid-canon-v2.png`）繪製並經 2x 四宮格審查，`nobody: true` 純機制／實物對照鏡共 **44 / 70 鏡（62.9%）**，零 MiniMax 生圖（US\$0.00）。
   - 9 語滿版黑猫縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）單行不換行、越語與泰語重音零削頂、零壓臉遮眼。
3. **繁中雙角色 Gemini 旁白、成片組裝、QA `11/11` 與獨立成片觀眾視角審查**：
   - 繁中旁白（所長 `gemini:Sulafat` `tempo: 1.08` ＋ 小問 `gemini:Leda` `tempo: 1.12`）：全片 70 句合成完成，平均語速 **`4.54`／`4.44 字／秒`**（≥ `4.4` 字／秒），並將易同音誤聽處修正為「擁擠的…糖晶」與「天然白色糖晶」（R45），雙重轉錄審查 `0` 標記通過。
   - `final.mp4`（`sha256: 4287e924c834`，`18362` frames，`-14 LUFS`）與 9 語 `.srt` 字幕（`zh-TW, en, ja, ko, es, pt, id, vi, th`）通過 **`qa` `11 of 11 checks passed`**。
   - `review/audience-review.md`：獨立審查子代理（`285d023e38a795f58d870ff45e08b506`）確認 44 張無人機制鏡 100% 零裁邊與 V184 紅線 100% 通過；針對首輪檢出之 `#69` 原圖頭頂零留白與角色鏡頭頂／呆毛留白裁切共 10 項調整，已完成 `#69` 胸上留白構圖重繪並將 `#03, #06, #17, #24, #25, #26, #41, #42, #48, #69` 改為 `"static camera"`／`"pull out"` 重組且複驗全數通過，六維度評分全數 `≥ 9.1`、總平均 **`9.18 / 10`** 正式放行。
   - `upload/` 上架包已透過 `package` 產出並通過 `4/4` 核對（`metadata.json` SHA-256 `8702534266fb`）。
4. **8 語多語配音（全數 8/8 完成）**：
   - `dubs/{en,ja,ko,es,pt,id,vi,th}.m4a`（**全數 8 語對齊片尾 `branding.json` 並含背景配樂混音**，`vi` 小問已完成 Gemini `Leda` 合成，`max 1.12x`）全數收入 `upload/dubs/`，並完成 Google Drive 完整備份核驗（**`1852 files, 0 differences`**）與 `/admin/videos` `outline`、`script`、`final`、`publish` 推送。

---

## 2. 本集製作經驗教訓（2.5 頭身角色頭頂留白 `< 9%` 時之運鏡規則與 `branding.json` 配音順序）

- **問題 1（2.5 頭身頭頂留白 `< 9%` 禁用 `"push in"`／`"pan"`）**：`"push in"` 結尾放大 `1.22x`（上下各裁 `9.02%`），`"pan left/right"` 全程放大 `1.20x`（上下各裁 `8.33%`）；若 2.5 頭身 Q 版角色頭頂或小問呆毛距離上緣小於 `9%`，套用 `"push in"` 或 `"pan"` 會在結尾定格切斷頭頂／呆毛。此類鏡頭應改設 **`"pull out"`** 或 **`"static camera"`**，生圖時亦應保留 `≥ 15%` 頭頂留白。
- **問題 2（先跑一次 `assemble` 產生 `branding.json` 再輸出最終 `dub` 母帶）**：`qa` 會核對 `dubs/<locale>.m4a` 長度是否與 `branding.json` 片尾書籤一致；若在首次 `assemble` 寫入 `branding.json` 前先合成配音，成片組裝後只需零 API 成本重跑一次 `dub` 即可瞬間對齊片尾長度。

---

## 3. 站主核准 `final`/`publish` 後推送 `languages` 關卡指令

```bash
export VIDEO_WORKDIR=/home/antigravity/mokaair-work/videos

# 站主於 /admin/videos 核准 final 與 publish 後，拉回核准狀態並推送 8 語 languages 批次：
node tools/video/cli.mjs review-pull --slug sothatswhy-g653-honey-crystallization --workdir "$VIDEO_WORKDIR"
node tools/video/cli.mjs review-push --slug sothatswhy-g653-honey-crystallization --gate languages --workdir "$VIDEO_WORKDIR"
```
