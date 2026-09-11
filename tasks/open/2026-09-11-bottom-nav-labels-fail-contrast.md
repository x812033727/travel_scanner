---
id: 2026-09-11-bottom-nav-labels-fail-contrast
title: 底部主導覽的文字標籤未達對比度標準
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T13:17:19Z
created_at: 2026-09-11T13:05:04Z
completed_at:
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/app-bottom-nav.tsx
---

# 底部主導覽的文字標籤未達對比度標準

## Why

實測 162 個頁面的文字對比度（取 computed color 與實際背景色計算），共發現 766 處未達 WCAG AA、98 種不同組合。**最嚴重的是底部主導覽本身**：

| 文字 | 實測對比 | 需要 | 出現頁數 |
| --- | --- | --- | --- |
| 「探索」「收藏」「我的旅程」 | **3.62:1** | 4.5:1 | 40+ |
| 「我的」 | **3.30:1** | 4.5:1 | 27 |
| Logo「Moka」 | **2.65:1** | 3:1（大字） | 65 |

英文「Saved」與日文「保存」量到同樣的 3.62:1，所以這不是文案問題，是**色彩 token 的問題**。

關鍵證據：**同樣 8 條路由切到深色模式，對比不足從 43 處降到 0 處**。

```
設定           對比不足   文字截斷   小目標
手機 標準           43       19      48   (8頁)
手機 深色            0       19      48
桌面 標準           44       21      48
桌面 深色            0       21      48
```

深色配色證明這個設計系統做得到 —— 問題只在淺色配色的前景色 token，而且是可以單點修正的。

## Definition of done

- [ ] 底部導覽的文字標籤在淺色模式達到 4.5:1。
- [ ] Logo 達到 3:1。
- [ ] 深色模式維持現狀（目前 0 處不合格，不要改壞）。

## Steps

- [ ] 找出底部導覽標籤與 Logo 用的前景色 token，在淺色配色下調深到通過 4.5:1／3:1。
- [ ] 三種配色（經典摩卡、海島藍、森旅綠）都要檢查——`globals.css` 裡 `[data-palette="lagoon"]`、`[data-palette="forest"]` 各只覆寫 2 條規則，很可能共用同一組前景色。
- [ ] 順帶處理 `/my` 的「經典摩卡」配色名稱標籤，實測只有 **1.38:1**。
- [ ] 加一個對比度的自動化檢查，涵蓋淺色與深色。

## How to verify

實測腳本的做法：對每個可見文字節點取 `getComputedStyle().color`，沿祖先鏈找第一個非透明背景色，算相對亮度比，依字級與粗細決定門檻（≥24px 或 ≥18.66px 粗體為 3:1，其餘 4.5:1）。

## Notes

- 「經典摩卡」1.38:1 是全站最低的一處。
- 這張任務只處理淺色配色的前景色 token，不動版面。
