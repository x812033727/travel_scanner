---
id: 2026-09-12-usemodalsheet-effect-ref
title: useModalSheet 的 effect 在 ref 還沒掛上時會靜靜地永久放棄
status: in-progress
priority: P2
area: web
owner: claude-opus-5-testfixes
claimed_at: 2026-09-12T02:34:16Z
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

## 完成（claude-opus-5-testfixes, 2026-09-12）

### 會紅的測試先寫出來了

`lib/modal-sheet.test.tsx` 新增「guards a sheet whose element arrives after the first commit」：
`open` 全程是 `true`，但元素要等一個 promise 解析才渲染（就是彈層藏在 loading 後面的形狀）。
在修正前它會紅，而且是紅在對的地方——`body.style.overflow` 是空字串，代表彈層根本沒註冊：

```
AssertionError: expected '' to be 'hidden'
```

### 修法，以及中途撞到的回歸

**第一版是錯的，測試抓到了。** 一開始把 ref 換成 callback ref、元素放進 state、effect 依賴
`[open, sheet]`。新測試綠了，但 `admin-deployments-panel` 與另一個檔各紅一條**焦點**斷言：

```
expected <button …> to be <input id="deploy-password" …>
```

因為那樣寫會讓**每一個**呼叫點的 effect 都晚一個 commit 才跑，於是原語在呼叫端自己把焦點設好
之後又搶回關閉鈕。**這正是 `#406` 在 `route-mode-panel` 修掉的那一類毛病**，差點自己再造一個。

改成只在 effect **真的撲空過**的時候才喚醒：

```ts
const sheetRef = useRef<T | null>(null);
const [lateSheet, setLateSheet] = useState<T | null>(null);
const missedSheet = useRef(false);

useEffect(() => {
  if (!open) return;
  const sheet = sheetRef.current;
  if (!sheet) { missedSheet.current = true; return; }   // ← 記下撲空
  ...
}, [open, lateSheet]);

return useCallback((node: T | null) => {
  sheetRef.current = node;
  if (node && missedSheet.current) { missedSheet.current = false; setLateSheet(node); }
}, []);
```

元素本來就在第一個 commit 裡的時候（二十一個呼叫點目前全部如此），`missedSheet` 永遠是 false，
`setLateSheet` 一次都不會呼叫——**時序與多出來的 render 都和改之前完全相同**。只有撲空過的
那條路徑會多一次喚醒。

### 回傳型別改了，有一個呼叫點要跟著動

`RefObject<T>` → `RefCallback<T>`。**typecheck 抓出一個我先前人工掃描漏掉的呼叫點**：
`travel-services/booking-panel.tsx:248` 會讀 `ref.current`（提交被擋下時把焦點移到第一個未通過
驗證的欄位）。那個檔改成自己留一份 `sheetRef` 再餵給 hook。

另一個選項是讓 hook 回傳「可呼叫又帶 `.current`」的混合型別，二十一個呼叫點都不用動——沒有採用，
那會留下一個以後每個讀者都要解碼的怪型別，而真正需要元素的只有一個呼叫點。

### 驗證

- 還原修正 → 新測試紅（`expected '' to be 'hidden'`）；放回去 → 綠。做過兩次，測試形狀改過之後重做。
- 二十一個呼叫點所屬的 18 個測試檔：205 條全過。
- 整套 233 檔 / 2382 測試全綠。
