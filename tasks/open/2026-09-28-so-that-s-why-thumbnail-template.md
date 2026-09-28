---
id: 2026-09-28-so-that-s-why-thumbnail-template
title: So That's Why: thumbnail template gaps (series palette, stamp, pillar accent, brand, headline check)
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-28T10:30:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/
  - tools/video/templates/theme.css
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

- [ ] `thumb` 可以選系列主題（色盤、字標、印章、主軸強調色），不影響其他影片現有的縮圖（雜湊不變的測試）。
- [ ] 可以一次畫出多個版型給 YouTube「測試與比較」。
- [ ] lint 依系列檢查 headline 字數與行數。
- [ ] `thumbnails.md` 的缺口一節改成已支援。

## Steps

- [ ] 讀 `thumbnails.md` 的「欄位對照」與「缺口」。
- [ ] 版型與主題、lint、測試。

## How to verify

`npm run test:tools`；用 `tools/video/core/fixtures/explainer/` 畫一張縮圖看。

## Notes

2026-09-28 開票；規格由規劃代理寫在 `thumbnails.md`，沒有改程式。
