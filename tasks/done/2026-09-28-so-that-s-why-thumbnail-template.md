---
id: 2026-09-28-so-that-s-why-thumbnail-template
title: So That's Why: thumbnail template gaps (series palette, stamp, pillar accent, brand, headline check)
status: done
priority: P3
area: tools
owner: claude-opus
claimed_at: 2026-09-28T10:50:50Z
created_at: 2026-09-28T10:30:50Z
completed_at: 2026-09-28T12:29:01Z
branch: claude/knowledge-series-planning-v84n79
depends_on: []
scope:
  - tools/video/templates/
  - tools/video/templates/theme.css
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - tools/video/core/fixtures/explainer/video.json
  - docs/videos/so-thats-why/thumbnails.md
  - tools/video/core/schema.mjs
---

# So That's Why: thumbnail template gaps (series palette, stamp, pillar accent, brand, headline check)

## Why

`docs/videos/so-thats-why/thumbnails.md` 定了「原來如此事務所」的縮圖規格（奶油／墨藍／印章紅／芥末黃、紅色印章、各主軸強調色、三種 A/B 版型），但 `tools/video/templates/templates.mjs` 的 `thumb` 版型做不到其中幾項，現在只能用規格裡寫的替代做法（例如 `tag` 寫「原來如此」代替印章）。缺口編號照規格的「缺口」一節：

- G1 色盤：`thumb` 用頻道深青主題（`#0e2627`、`#f7f1e8`、`#f0a04b`），不是系列色盤。
- G2 印章：沒有印章元素。
- G3 主軸強調色：`tag` 顏色固定。
- G4 A/B：一支影片只畫一張縮圖，三個版型要改 `thumbnail.data` 重畫。
- G5 品牌：左下角字標寫死 MOKAAIR。
- G6 字數：headline 長度與行數沒檢查（撰稿提示允許 ≤ 12 字，這個系列要 ≤ 10 字、最多 2 行）。
- G7 版面：遮罩與文字欄固定在左邊。

## Definition of done

- [x] `thumb` 可以選系列主題（色盤、字標、印章、主軸強調色），不影響其他影片現有的縮圖（沒有系列時輸出不變的測試）。
- [x] 可以一次畫出多個版型給 YouTube「測試與比較」（render 端；上架包與審片頁在票 `2026-09-28-thumbnail-variants-in-the-upload-package`）。
- [x] lint 依系列檢查 headline 字數與行數。
- [x] `thumbnails.md` 的缺口一節改成支援狀態表。

## Steps

- [x] 讀 `thumbnails.md` 的「欄位對照」與「缺口」。
- [x] 版型與主題、lint、測試（G1–G3、G5–G7）。
- [x] G4：`thumbnail.variants`（B、C，蓋在 A 的 data 上），`render` 出 `thumbnail-b.jpg`、`thumbnail-c.jpg`，manifest 記 `thumbnail_variants`。

## How to verify

`npm run test:tools`；用 `tools/video/core/fixtures/explainer/` 畫一張縮圖看。

## Notes

2026-09-28 開票；規格由規劃代理寫在 `thumbnails.md`。
- 2026-09-28：G1–G3、G5–G7 做完。系列 CSS 內嵌在頁面（跟關鍵影格底圖的 CSS 一樣），`theme.css` 沒動，所以其他影片的縮圖鍵不變；`render/plan.mjs` 的 `thumbnailSeries(doc)` 依 `isExplainer` 決定。用本機 Chromium（`/opt/pw-browsers/chromium-1194`）實際畫過左右兩種版面檢查。G4 牽涉 `render`、`package`、`qa` 三處，留在這張票。
- 沒改 `automation/prompts.mjs`（其他代理的票正在改它）：解說版撰稿提示仍寫 headline ≤ 12 字，超過 10 字時 lint 擋下、撰稿的 lint 修正迴圈會改短。提示詞的字數與 `pillar`／`layout` 說明等那幾張票結束後再補。
- 2026-09-28：G4 的 render 端做完。A 仍是 `thumbnail.jpg`（上架包、審片、qa 都不用改就照舊），B、C 是 `thumbnail-b.jpg`、`thumbnail-c.jpg`；變體的 `data` 蓋在 A 上，lint 每個變體都跑同樣檢查並回報 `variant b: ...`，變體的 `shot` 要是本集鏡頭，字型覆蓋也逐張查。沒有 `variants` 的影片 plan 與 manifest 完全不變（測試有比）。`tools/video/package` 當時在 `2026-09-26-video-dubs-worker` 的 scope，所以上架包與審片頁帶 B、C 另開票 `2026-09-28-thumbnail-variants-in-the-upload-package`。用本機 Chromium 畫過 fixture 的 B（同圖、事實大字）與 C（右版、換鏡頭、加 sub）檢查。
- 2026-09-28 補：解說版撰稿提示的縮圖說明後來在票 `2026-09-28-sothatswhy-shorts-from-episode` 補上（≤ 10 字 2 行、pillar、layout、variants）。
