---
id: 2026-10-03-render-svg-full-chrome-crop
title: render_svg crops about 88px when CHROMIUM_BIN points at full Chrome
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-03T12:04:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
---

# render_svg crops about 88px when CHROMIUM_BIN points at full Chrome

## Why

`render_svg` 把 SVG 截成 1600×900 的 PNG（hero.jpg 也從這裡來）。預設挑 `chromium_headless_shell`，截圖完整；
但 `CHROMIUM_BIN` 指到完整版 `/opt/pw-browsers/chromium-*/chrome-linux/chrome` 時，`--window-size=1600,900` 含視窗外框，
截圖底部約 88 px 變白邊（2026-10-03 多位撰稿代理照舊指令設了它，回報 hero 頁尾被截）。目前 ingest 沒設 `CHROMIUM_BIN`，所以正式產物沒受影響。

## Definition of done

- [ ] 用完整版 chrome 也產出完整 1600×900（例如偵測非 headless-shell 時多加視窗高度、或改用 `--screenshot` 配 viewport 參數），或明確拒絕該 binary。
- [ ] 測試涵蓋：產出 PNG 的尺寸與最底一列像素不是空白。

## Steps

- [ ] 重現、修、加測試。

## How to verify

`CHROMIUM_BIN=/opt/pw-browsers/chromium-1194/chrome-linux/chrome` 下 render 一張頁尾有字的 SVG，檢查 PNG 底部。

## Notes

- `pack_ingest.py` 目前在 `2026-09-14-codex-learning-series`（blocked）的 scope 裡，認領會被拒，要先和那張票協調。
