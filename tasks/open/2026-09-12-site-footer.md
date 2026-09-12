---
id: 2026-09-12-site-footer
title: site-footer 有一條測試繼承別人留下的路徑，打亂順序就紅
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-12T01:37:09Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/site-footer.test.tsx
---

# site-footer 有一條測試繼承別人留下的路徑，打亂順序就紅

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

# site-footer 有一條測試繼承別人留下的路徑，打亂順序就紅

## Why

`components/site-footer.test.tsx:55`「carries the only entry point to the guides that
survives a first paint」在打亂順序 + 負載下紅過：

```
❯ components/site-footer.test.tsx (16 tests | 1 failed)
   × carries the only entry point to the guides that survives a first paint
```

**種子可以重放**：`npx vitest run --sequence.shuffle --sequence.seed=1789176414571`

## 成因（已確認，不是推測）

檔案頂端的路徑是模組層的可變狀態：

```ts
const pathname = vi.hoisted(() => ({ value: "/" }));
vi.mock("@/i18n/navigation", () => ({ usePathname: () => pathname.value, ... }));
function renderAt(path: string) { pathname.value = path; return render(<SiteFooter year={2026} />); }
```

其他十五條都走 `renderAt(...)`，會先把路徑設好。只有第 55 行這條直接 `render(<SiteFooter
year={2026} />)`，**沒有設定路徑**，所以它拿到的是上一條測試留下來的值。

第 70 行的 `it.each` 會把它設成 `/admin`、`/admin/settings`、`/trips/abc123`——而頁尾在這三個
路徑上是刻意不渲染的（「stays out of」就是在測這件事）。只要順序把那三條排到第 55 行前面，
`screen.getByRole("contentinfo")` 就找不到東西，整條倒掉。

預設順序下 `it.each` 排在後面，所以平常是綠的；CI 也沒有開 shuffle。**這不是 flake，是這條
測試在斷言一件它自己沒有設定的前提。**

## 修法

一行：

```diff
-    render(<SiteFooter year={2026} />);
-    const footer = screen.getByRole("contentinfo");
+    const footer = within(renderAt("/").container).getByRole("contentinfo");
```

或更直接，照其他十五條的寫法先 `renderAt("/")` 再 `screen.getByRole("contentinfo")`。

## Definition of done

- [ ] 用上面的種子重放，確認修好之前會紅、修好之後會綠。
- [ ] 順手看一下同一個檔裡還有沒有別條沒設路徑就斷言的（`grep -n 'render(<SiteFooter'`）。
- [ ] `npm run test:web` 全綠。

## Notes

查 `2026-09-11-modal-escape-flake-under-load` 的時候，用 `--sequence.shuffle` 找 Escape flake
順手撞到的。和那張沒有關係：同一份日誌裡四筆 MODALPROBE 全是 `isTop=true depth=1
defaultPrevented=false foreignOpenDialogs=0`，彈層那邊一切正常。

打亂順序是個便宜又有效的手法，值得偶爾拿來掃一遍——這次一跑就抓到一條真的順序相依。
