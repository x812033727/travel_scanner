---
id: 2026-09-06-place-picker-reopens-after-escape
title: 地點建議清單會在 Escape 之後自己打開
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T15:33:24Z
created_at: 2026-09-06T15:00:32Z
completed_at: 2026-09-06T15:33:54Z
branch: claude/place-picker-escape
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

- [x] 按 Escape 之後，即使搜尋結果稍後才回來，清單也維持關閉。
- [x] 點清單以外的地方會關閉清單（再點回輸入框會重新打開）。
- [x] 鍵盤操作不變：ArrowDown 會重新打開、Enter 選取、選完關閉。
- [x] `place-picker.test.tsx` 有案例釘住「Escape 後結果才回來」與「點外面」兩種。

## Steps

- [x] 用一個 ref 記住使用者已經主動關掉這一輪搜尋（值變更時重置），結果回來時尊重它。
- [x] outside click 用 `pointerdown` 監聽 document，判斷 target 是否在容器內；
      注意選項按鈕上已經有 `onMouseDown={(event) => event.preventDefault()}`，不要跟它打架。
- [x] 順手確認 `/trips/new` 手機版：目的地輸入之後，日曆的「下個月」仍然點得到。

## How to verify

```bash
cd apps/web && npx vitest run components/place-picker
cd apps/web && npx playwright test e2e/full-stack.spec.ts --project=mobile-chromium
```

手機版 390×844 開 `/zh-TW/trips/new`，先打目的地再馬上點日曆的「下個月」，應該一次就點得到。

## Notes


`full-stack.spec.ts` 目前刻意先選日期再打目的地，並在註解寫了原因；這張修好之後那個順序可以還原，
但沒有還原的必要——那個順序本身也合理。

### 做完之後（2026-09-06，claude-opus-5）

一個 `dismissed` ref 記住「這一輪搜尋已經被使用者關掉了」，防抖回來的 `setOpen(true)` 先看它。
重置的時機有三個：重新聚焦、繼續打字、按方向鍵——三者都代表使用者又想看清單了。
另外補上 `pointerdown` 的 outside-click，只在 `open` 為真時掛監聽，關掉時就移除。

`pointerdown` 而不是 `click`：選項按鈕上本來就有 `onMouseDown={(event) => event.preventDefault()}`
（避免輸入框失焦），用 click 會在選取的當下先被 outside 判斷攔一次；用 pointerdown 加上
「target 在容器內就不處理」，兩者不會打架。

測試兩條：搜尋在 Escape 之後才回來（清單維持關閉、`aria-expanded` 是 false），
以及在畫面別處按下（清單關閉）。

順帶一提，`full-stack.spec.ts` 目前先選日期再打目的地，那是為了同一個症狀繞開的；
現在元件修好了，順序可以還原，但沒有還原的必要。
