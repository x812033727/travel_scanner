---
id: 2026-09-06-place-picker-reopens-after-escape
title: 地點建議清單會在 Escape 之後自己打開
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T15:00:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/place-picker.tsx
  - apps/web/components/place-picker.test.tsx
---

# 地點建議清單會在 Escape 之後自己打開

## Why

`place-picker.tsx` 的建議清單有兩個關掉的方法：按 Escape，或選一筆。**點旁邊沒有用**——
元件沒有 outside-click 處理。而 `useEffect` 裡防抖 320 毫秒後回來的搜尋結果無條件呼叫 `setOpen(true)`
（成功與失敗兩條路都有），所以在結果回來之前按的 Escape 會被推翻，清單自己彈回來。

清單是 `absolute z-30 max-h-64`，蓋住它下面 256 像素的東西。在 `/trips/new` 手機版，
那正好是日曆的月份切換列。

2026-09-06 這件事讓 `full-stack.spec.ts` 的手機版旅程整整卡到逾時：Playwright 判定被遮住的點擊
不會真的送出，所以永遠不會產生「點旁邊」這個關掉清單的動作，而 Escape 又會被搜尋結果推翻。
當時的處理是把測試的順序改成先選日期再打目的地，只是繞開，元件本身沒修。

## Definition of done

- [ ] 按 Escape 之後，即使搜尋結果稍後才回來，清單也維持關閉。
- [ ] 點清單以外的地方會關閉清單（再點回輸入框會重新打開）。
- [ ] 鍵盤操作不變：ArrowDown 會重新打開、Enter 選取、選完關閉。
- [ ] `place-picker.test.tsx` 有案例釘住「Escape 後結果才回來」與「點外面」兩種。

## Steps

- [ ] 用一個 ref 記住使用者已經主動關掉這一輪搜尋（值變更時重置），結果回來時尊重它。
- [ ] outside click 用 `pointerdown` 監聽 document，判斷 target 是否在容器內；
      注意選項按鈕上已經有 `onMouseDown={(event) => event.preventDefault()}`，不要跟它打架。
- [ ] 順手確認 `/trips/new` 手機版：目的地輸入之後，日曆的「下個月」仍然點得到。

## How to verify

```bash
cd apps/web && npx vitest run components/place-picker
cd apps/web && npx playwright test e2e/full-stack.spec.ts --project=mobile-chromium
```

手機版 390×844 開 `/zh-TW/trips/new`，先打目的地再馬上點日曆的「下個月」，應該一次就點得到。

## Notes

`full-stack.spec.ts` 目前刻意先選日期再打目的地，並在註解寫了原因；這張修好之後那個順序可以還原，
但沒有還原的必要——那個順序本身也合理。
