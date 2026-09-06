---
id: 2026-09-06-readable-foundation
title: 看得見：連結顏色被吃掉、對比不足與字級下限
status: in-progress
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T13:02:56Z
created_at: 2026-09-06T13:01:59Z
completed_at:
branch: claude/ui-ux-simplification-72afb9
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/e2e/readability.spec.ts
  - apps/web/components/flight-status-search.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - .github/workflows/ci.yml
---

# 看得見：連結顏色被吃掉、對比不足與字級下限

## Why

2026-09-06 用 Playwright 掃過線上 mokaair.com 的 12 個公開頁（桌機 1440×900 與手機
390×844）＋ 本機掛假資料的 10 個後台頁，量到三件會直接讓長輩看不清楚的事：

1. **連結的顏色被全域規則吃掉。** `globals.css` 有一條沒有包在任何 layer 裡的
   `a { color: inherit }`。Tailwind v4 的 utility 都在 `@layer utilities`，而沒有
   layer 的規則優先權高於所有 layer，所以每一個 `<a class="… text-white">` 的
   `text-white` 都不會生效，改成繼承父層顏色。實測後果：
   - 「前往登入」「返回首頁」等深綠底按鈕的字是深墨色，對比 **2.39**（需 4.5）。
   - 熱門景點／城市美食的分頁膠囊，選中那顆同樣是 2.39。
   - 後台側邊欄「目前所在頁」的膠囊是 `bg-[var(--ink)] text-white`，實際算出來
     `color: rgb(16,42,43)` 疊在 `rgb(16,42,43)` 上，對比 **1.0 —— 完全看不到自己
     在哪一頁**。
2. **`--muted` 的對比不到 4.5。** `#607676` 疊在 `--paper #f5f7f2` 是 4.48、疊在
   `--surface-tint` 是 4.32，全站的說明文字、底部導覽列文字都踩在這條線下面。
   `--coral #ed735d` 當按鈕底色配白字只有 **2.91**（航班動態的主要 CTA 就是它）。
3. **字級下限太低。** `globals.css` 有 28 條 `font-size` 小於 0.8rem，最小 0.62rem；
   底部導覽列的「探索／規劃／旅程／通知／我的」量到 **10.4px**，熱門景點卡的
   「收藏／加入行程／分享」12.2px，首頁快速開始卡的副標 11.5px。Tailwind 的
   `text-xs`（12px）在 `apps/web` 出現 540 次。

## Definition of done

- [ ] 任何 `<a>` 自己寫的文字顏色會生效；上面列的 2.39 與 1.0 對比全部消失。
- [ ] 淺色與深色兩個主題下，正文與說明文字對 `--paper`／`--surface`／`--surface-tint`
      的對比都 ≥ 4.5；當底色用的按鈕（coral、teal）配白字 ≥ 4.5。
- [ ] 全站沒有小於 13px 的可讀文字；底部導覽列的標籤 ≥ 13px。
- [ ] 既有版面沒有走鐘：12 個公開頁的桌機／手機截圖與修改前相比只有顏色與字級變化。

## Steps

- [ ] 把 `button/input/textarea/select`、`button`、`a` 的元素預設值包進 `@layer base`。
- [ ] 調 `--muted`、新增按鈕底色用的 coral，深色主題同步檢查。
- [ ] 用 `@theme` 把 Tailwind 的 `--text-xs`／`--text-sm` 拉到 13px／15px，並把
      `globals.css` 裡 28 條 0.62–0.79rem 的字級換成語意變數。
- [ ] 補一支 e2e：讀 DOM 算對比與字級，任何按鈕／連結低於 4.5 或文字小於 13px 就失敗。

## How to verify

```bash
cd apps/web && npx playwright test e2e/readability.spec.ts --project=desktop-chromium
cd apps/web && npx playwright test e2e/readability.spec.ts --project=mobile-chromium
npm run lint:web && npm run typecheck:web && npm run test:web
```

## Notes

- 稽核腳本放在 scratchpad：`ux_audit.mjs`（線上公開頁）、`admin_audit.mjs`（本機
  ＋假資料的後台頁）、`contrast_sweep.mjs`（比對修改前後的對比清單）。後台頁要
  在本機 `next dev` 上跑，並用 `page.route("**/api/travel/**")` 餵假資料；公開頁
  可以把 `/api/travel/**` 轉發到 mokaair.com 拿真資料。
- `Moka air` 字標量出來 1.39 是誤判：它用漸層字，背景是透明的，往上找到的底色不是
  實際畫出來的顏色。判讀報告時要跳過它。
- 修改前後的對比差異（手機 390px）已經量過：所有 2.39 的按鈕消失，標題列的圖示
  連結從 1.39 變成它本來就宣告的 3.32（圖示只需 3:1，可接受）。
