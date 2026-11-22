# curio-w25-qb-house（N9103，QB House）製作紀錄

- 題目池編號：`N9103`（`score = 9.63`，`base = 10`，`demand = 7.75`，`W-商業與品牌奇聞`）
- 分支：`antigravity/curio-w25-qb-house`
- Google Drive：
  - `W25/`：`1hvrusCImCSsxGWf7lYdysFgHYIyntVcV`
  - `W25/製作檔/`：`1eEJvfD5qBF_XEj-XZpWlq0qO8vRfMrtg`

## Pre-TTS 階段收據（2026-11-22）

1. **一次來源事實查核（`verify-2.md`）**：**`VERDICT: PASS`**
   - 9/9 公開來源實測存活（含 FY2026/6 營收 `271.54 億日圓`、`+6.3% YoY`；`https://www.beautopia.jp/216358/`）。
   - 14/14 條主張逐行對齊；零在世或 1956 年後過世真人入畫/具名；零品牌字樣與版權 IP 違規。
2. **腳本與說書鎖定（`v26`，`9.4 min` / `119` 句 / `2,297` 發音單位）**：
   - `node tools/video/cli.mjs lint --slug curio-w25-qb-house`：**`0 errors, 0 warnings`**（9 語系全通過）。
   - 開場盲測（`opening-review --check`）：**`PASSED`**（`opening_hash: ea82bf0820ce951a814eeabb369d18f12d9e16f699860be3b4d3ade32af14992`；Newcomer `9.2` / Scroller `9.1` / Stickler `9.1`，`would_stay_300: true`，`swipe_at: null`，`problems: []`）。
   - 14 題故事體檢（`narrative --answers`）：**`passed`**（Reader 1 `14/14` + Reader 2 `14/14` = `28/28` 全數 YES）。
3. **關鍵影格與 2x 四象限獨立審圖（`60 / 60 = 100% PASS`）**：
   - 全 60 張關鍵影格經 5 輪共 240 張 `960×540` 象限獨立審圖（`32 -> 51 -> 57 -> 59 -> 60/60`），零白邊/黑邊、零亂碼字樣；5 張 Ada 鏡頭（`S05, S21, S32, S41, S60`）嚴格鎖定 `ada-canon-v2.png`；`S07, S21, S25, S29, S60` 以內建 `generate_image`（`$0`）重繪補齊；全 60 張已透過 `keyframes import` 匯入。
4. **多語系翻譯與 9 語系縮圖（`zh-TW` + `en, ja, ko, es, pt, id, vi, th`）**：
   - 8 語系翻譯經獨立多語審稿代理逐語挑錯並全部修正（泰語 Ada 女性語尾 `คะ`/`ค่ะ`/`นะคะ` 與 `300 ล้านครั้ง`、葡語 `lojas imitadoras`、印尼語 `dua mesin yang saling mencadangkan` 與 5,009B->4,319B、日語 `吸引ホース`/`北米`、西語時態修正、越語 `q001` 與 5,602B->4,667B、6 語標題寬度與全形 `｜` 分隔）。
   - 9 張 `heimao-left` 縮圖已渲染並逐張視覺驗收（字體清晰、無裁切、無遮擋 Ada、泰韓日越字形零破字）。
5. **後台送審（`/admin/videos`）**：
   - `review-push --slug curio-w25-qb-house --gate script`：`pending`
   - `review-push --slug curio-w25-qb-house --gate storyboard`：`pending`

## 下一步（Gemini TTS 配額重置後）

- 以 Gemini `Sulafat` 合成 `119` 句繁中旁白 -> MiniMax 合成 8 語配音 -> `assemble` 成片 -> 獨立一般觀眾視角審片（`review/audience-review.md`）修正並重跑 `qa` -> Google Drive 零差異備份 -> `review-push --gate final`。
