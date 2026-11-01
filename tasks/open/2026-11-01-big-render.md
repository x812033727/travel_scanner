---
id: 2026-11-01-big-render
title: big 卡片長引文第三行被裁掉，render 的版面檢查沒抓到
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T16:36:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/theme.css
---

# big 卡片長引文第三行被裁掉，render 的版面檢查沒抓到

## Why

2026-11-01 重建 curio-s31-v2 時看到：`big` 卡片的 `text` 一長（約 22 字以上、會排成三行），第三行被 `.t-big .word` 的 `max-height: 440px` 裁掉一半、
壓到 `sub` 上，但 `render` 回報「no layout, glyph or font problem」，qa 的 render 項也打勾。不是紙底主題造成的：Codex 送審的深色版
（站上 final/contact_sheet.png，2026-10-27）同樣五張（bai-days、guoshibu、wu-fuzhou、seven-days、chen-quote）都被裁。

## Definition of done

- [ ] 三行以上的 `big.text` 會自動縮字到放得下，或 render 的版面檢查把被 max-height 裁掉的字當成版面問題報出來（lint 也可在字數超過時警告）
- [ ] 附測試：一張 26 字的 big 卡片不再通過檢查（或縮字後整段可見）

## Steps

- [ ] 看 `tools/video/render` 的版面檢查怎麼量 overflow（目前似乎只看水平或只看父層）
- [ ] 決定修法：縮字（fit）或報錯

## How to verify

對 curio-s31-v2 在 2026-11-01 前的 video.json（Codex 分支 3f624c874）跑 render，應報版面問題。

## Notes

curio-s31-v2 已改成較短的節錄（帶「……」），不再依賴這個修正。
