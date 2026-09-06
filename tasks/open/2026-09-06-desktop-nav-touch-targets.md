---
id: 2026-09-06-desktop-nav-touch-targets
title: 桌機主導覽文字連結只有 20px 高
status: in-progress
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T07:55:00Z
created_at: 2026-09-06T00:54:01Z
completed_at:
branch: claude/p3-polish
depends_on: []
scope:
  - apps/web/components/site-navigation.tsx
---

# 桌機主導覽文字連結只有 20px 高

## Why

`site-navigation.tsx` 的七個主連結是裸的 `<Link>`，沒有 padding 也沒有 min-height：

```tsx
<Link key={item.href} href={item.href}>{t(item.key)}</Link>
```

實測（Playwright，1440×900）每個是 **56×20 px**。桌機用滑鼠還可以，但這是全站唯一
一組不遵守 44px 準則的主要導覽，而且平板（lg 以上、觸控）也會用到它。

`globals.css` 已經有 `.app-filter-chip`（min-height 2.75rem）與 `.app-icon-button`（44×44）
這類 primitive，這裡沒有採用。

## Definition of done

- [ ] 1440×900 量測每個主導覽連結的 `boundingBox().height` ≥ 44。
- [ ] header 高度不因此暴增（連結變高但整列還是一行）。
- [ ] hover／focus 狀態仍清楚可見。

## Steps

- [ ] 給連結加 `inline-flex min-h-11 items-center px-2`（或改用既有 primitive）。
- [ ] 確認 lg（1024px）到 1280px 之間七個連結加上帳號區還是一行，
      不會因為多出的 padding 而換行 —— 2026-09-06 才把斷點從 md 提到 lg 就是為了這個。

## How to verify

```bash
cd apps/web && npx playwright test e2e/navigation.spec.ts --project=desktop-chromium
```

或直接量：

```js
const box = await page.getByRole("link", { name: "熱門景點" }).boundingBox();
expect(Math.round(box.height)).toBeGreaterThanOrEqual(44);
```

（`e2e/navigation.spec.ts` 已有兩處用 `Math.round()` 再比 44 的先例 —— 版面引擎在某些
runner 會回報 43.99993896484375，不 round 會偽紅。）

## Notes

**2026-09-06 已經改過這個檔案**：主連結列的斷點從 `md:flex` 提到 `lg:flex`
（768–1023px 在英文／日文會擠成兩行 sticky header），連結清單抽到
`lib/nav-links.ts` 與手機選單共用，並改用 `featureVisible()`（讀不到設定時保留連結，
而不是整排消失）。**不要把這些改回去。**

同一輪已經修好、不要重做的觸控目標：首頁城市晶片 32→44px、
「回到搜尋條件」36→`min-h-11`、精靈步驟藥丸→真按鈕且 `min-h-11`、
精靈核取方塊→44px 列 + 20px 方塊。
