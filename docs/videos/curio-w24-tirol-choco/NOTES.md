# curio-w24-tirol-choco（N9112，滋露巧克力）製作紀錄

- **題目池編號**：`N9112`（`W-商業與品牌奇聞`，總分 `9.73`，`base = 9.68`，`demand = 10`，全池第 2 高分）
- **分支**：`antigravity/curio-w24-tirol-choco`
- **Google Drive 備份**：
  - `AI/備份/AI劇/奇聞檔案局/W24/` (`1TnmyGA4a1vVFSwvHGgO3teidg43yUISt`)
  - `AI/備份/AI劇/奇聞檔案局/W24/製作檔/` (`10PHqGhgejPzZIxitTJncfEhc135uIbh5`)

## 已完成里程碑（2026-11-22）

1. **一手查核與紅線檢核**：
   - 9 條一手／官媒來源全數實地讀取與交叉驗證（`verify-1.md`、`verify-2.md` **VERDICT: PASS**，14/14 條事實確認、0 誤差）。
   - **1956 真人紅線**：`0` 位在世或 1956 年後過世真人入名／入畫。
   - **品牌／IP 視覺安全**：62 張影格提示詞與縮圖皆無 `チロルチョコ`／`TIROL` 字樣、無條碼數字、無版權聯名角色。
2. **劇本與三道獨立審查（v3.9 鎖定）**：
   - `62` 鏡頭、`123` 句、`2,355` 口語單位（估計 9.6 分鐘）、`44/62 = 71.0%` `nobody: true`、`5` 張 Ada 影格、`0` 卡片、`0` 英文單字（不改動 `lexicon.json`）。
   - `node tools/video/cli.mjs lint --slug curio-w24-tirol-choco`：**`0 errors, 0 warnings`**（含全 9 語系）。
   - 前 300 秒獨立三觀眾審查（`opening-review --check`）：**PASSED**（Newcomer `9.2` / Scroller `9.0` / Stickler `9.2`，`problems: []`，`opening_hash: d52a07dd03529de0484eea32b8b250d7eff9ad2487f2536d633e723595bad903`）。
   - 官方 14 題敘事審查（`review/narrative.json`）：**PASSED**（兩位獨立審查員 28/28 全數 YES）。
3. **關鍵影格與 2x 四象限獨立視覺稽核**：
   - 5 張 Ada 影格（`05, 22, 37, 51, 62`）由內建 `generate_image`（`$0`）鎖定 `ada-canon-v2.png` 繪製，雙手掌心朝下五指自然。
   - 57 張非 Ada 影格以 `gemini-3.1-flash-image` 2K 繪製；248 象限獨立 2x 稽核共經三輪重繪（R1 26 張 → R2 7 張 → R3 2 張），**62/62 = 100% PASS**。
   - 全數以 `keyframes import --provider external --usd 0` 匯入（`[x] keyframes drawn`）。
4. **8 語系翻譯、獨立稽核與 9 語縮圖**：
   - `en, ja, ko, es, pt, id, vi, th` 全數完成翻譯並通過獨立 8 語系稽核（修正 `id` `Diperbesar`、`pt` `couberam`、`es/pt/vi` `23` 日圓調價一致、2018 秋葉原專賣店過去式、`ja` 四位數年份與位元組上限、`en` 語法與精準詞彙、`th` `2,003 bytes <= 2,150` 等所有項目），重併 `lint` **`0 errors, 0 warnings`**。
   - 9 張 `heimao-left` 縮圖（`thumbnail.jpg` + `thumbnails/{en,ja,ko,es,pt,id,vi,th}.jpg`）全部渲染並逐張目視驗收通過。
5. **後台送審與配音進度**：
   - `/admin/videos` 已推送 `script` 與 `storyboard` 關卡（`pending`）。
   - 中文 Gemini `Sulafat` TTS 已完成並快取 **79/123 句**（剩餘 44 句待站台 API 單日配額重置後續跑；接著執行 `check-audio` → `music` → 8 語系 MiniMax `dub` → `clips` → `assemble --adopt-branding` → `captions` → `qa` 11/11 → 獨立觀眾盲評 `review/audience-review.md` → 零差異備份 → `review-push --gate final`）。
