---
id: 2026-09-12-usemodalsheet-effect-ref
title: useModalSheet 的 effect 在 ref 還沒掛上時會靜靜地永久放棄
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-12T01:18:15Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/modal-sheet.test.tsx
---

# useModalSheet 的 effect 在 ref 還沒掛上時會靜靜地永久放棄

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

# useModalSheet 的 effect 在 ref 還沒掛上時會靜靜地永久放棄

## Why

`apps/web/lib/modal-sheet.ts`：

```ts
useEffect(() => {
  if (!open) return;
  const sheet = sheetRef.current;
  if (!sheet) return;   // ← 靜靜地放棄
  ...registerModalLayer / keydown / focus trap...
}, [open]);
```

deps 只有 `[open]`。`open` 沒再變的話，這個 effect 不會重跑。所以只要 effect 執行的那一刻
`sheetRef.current` 還是 null，那個彈層就**永久**沒有 Escape、沒有 Tab trap、沒有捲動鎖、
也沒有進 `layers`——畫面上看起來是一個正常的對話框，鍵盤上什麼都不回應，而且不出任何聲音。

風險最高的是四個把 `open` 寫死 `true` 的呼叫點，因為 effect 只在掛載時跑那一次：

| 呼叫點 | hook | ref | 現況 |
| --- | --- | --- | --- |
| `hotspot-restaurants-panel.tsx` | 153 | 321 | 安全（中間沒有提前 return） |
| `admin-hotspot-guides-panel.tsx` | 945 | 956 | 安全 |
| `travel-services/booking-panel.tsx` | 125 | 165 | 安全 |
| `travel-services/stay22-public-hotels.tsx` | 38 | 56 | 安全（loading 狀態在 div **裡面**） |

**二十一個呼叫點目前都沒踩到**，所以這不是現在的 bug，是下一個人踩得到的地雷：只要有人把
彈層藏在 loading 狀態後面（`{data ? <div ref={ref}>…</div> : <Spinner/>}`），就中了。
查 `2026-09-11-modal-escape-flake-under-load` 的時候順手驗出來的。

## Definition of done

- [ ] 有一個會紅的測試：`open` 從頭到尾是 `true`，但 ref 要等一個 async tick 才掛上，
      斷言 Escape 會關掉彈層。這條測試在現在的程式碼上必須是紅的。
- [ ] 修好。可能的方向是改用 callback ref 並把元素放進 state，讓 effect 在元素掛上時重跑。
      **注意**這會改掉回傳型別（`RefObject<T>` → `RefCallback<T>`）並讓二十一個呼叫點各多
      一次 render，所以要確認沒有呼叫點在讀回傳 ref 的 `.current`。
- [ ] 把修正還原，確認那條測試真的會紅。
- [ ] `npm run test:web` 全綠。

## Notes

不要為了修這個而放寬既有的斷言。`useModalSheet` 現在有二十一個呼叫點、十一個是 `#406`
才搬過來的，改動要保守。
