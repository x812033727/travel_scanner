---
id: 2026-09-12-admin-usage-settings-url
title: admin-usage-settings 的分頁存在 URL，測試之間沒有重設就互相影響
status: done
priority: P2
area: web
owner: claude-opus-5-testfixes
claimed_at: 2026-09-12T02:34:15Z
created_at: 2026-09-12T01:40:33Z
completed_at: 2026-09-12T03:09:00Z
branch:
depends_on: []
scope:
  - apps/web/components/admin-usage-settings-panel.test.tsx
---

# admin-usage-settings 的分頁存在 URL，測試之間沒有重設就互相影響

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

# admin-usage-settings 的分頁存在 URL，測試之間沒有重設就互相影響

## Why

`components/admin-usage-settings-panel.test.tsx:47`「loads all four tabs and saves trial
and operation costs」在打亂順序 + 負載下紅過：

```
AssertionError: expected 'false' to be 'true'
 ❯ components/admin-usage-settings-panel.test.tsx:47
   expect((await screen.findByRole("tab", { name: "註冊體驗" })).getAttribute("aria-selected")).toBe("true")
```

**種子可以重放**：`npx vitest run --sequence.shuffle --sequence.seed=1789176414571`
（同一次跑還會紅 `site-footer`，見 `2026-09-12-site-footer`，是同一類但不同檔。）

## 成因（已確認）

`admin-usage-settings-panel.tsx:77`：

```ts
const [tab, setTab] = useAdminQueryState("tab", TAB_KEYS, "trial");
```

分頁狀態存在 **URL 的 query string**，不是元件 state。同一個測試檔共用一個 jsdom，
`window.location` 於是跨測試存活。而這個檔的 `afterEach` 只有：

```ts
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });
```

**沒有重設 URL。**

第 47 行斷言第一個分頁（`trial`）是選中的——這只有在 URL 沒有 `tab` 參數時才成立。但同一條
測試自己在第 53 行就 `fireEvent.click(screen.getByRole("tab", { name: "功能扣次" }))`，留下
`?tab=costs`；另外兩條也會切到各自的分頁。

預設順序下它排在第一個，拿到乾淨的 URL，所以永遠是綠的。順序一打亂，只要有任何一條先跑過並
切了分頁，它就紅。**不是 flake，是這條測試斷言了一件它自己沒有設定的前提。**

## 修法

在檔案層加一個重設，讓每條測試從乾淨的 URL 開始：

```ts
beforeEach(() => { window.history.replaceState(null, "", "/"); });
```

（`travel-card-actions.test.tsx` 已經是這個寫法，可以照抄。）

## Definition of done

- [ ] 用上面的種子重放，確認修好之前會紅、修好之後會綠。
- [ ] 不要改第 47 行的斷言——要修的是前提沒被設定，不是斷言太嚴。
- [ ] 掃一下還有哪些測試檔在測 `useAdminQueryState` 的元件卻沒有重設 URL：
      `grep -rln useAdminQueryState apps/web/components` 再對照各檔有沒有 `replaceState`。
- [ ] `npm run test:web` 全綠。

## Notes

查 `2026-09-11-modal-escape-flake-under-load` 時用 `--sequence.shuffle` 順手撞到的第二條。
和 `2026-09-12-site-footer` 是同一個形狀——測試斷言了自己沒設定的前提——只是外洩的載體不同：
那邊是 `vi.hoisted` 的模組變數，這邊是 URL。值得順手把兩張一起做掉。

## 完成（claude-opus-5-testfixes, 2026-09-12）

加了 `beforeEach(() => window.history.replaceState(null, "", "/"))`，照 `travel-card-actions.test.tsx`
的寫法。斷言一個字都沒改——要修的是前提沒被設定，不是斷言太嚴。

先確認過 `useAdminQueryState` 是透過 `useSyncExternalStore` 讀 `window.location.href`
（`lib/admin-workspace-navigation.ts:64-65`），所以重設 URL 確實是對的地方，不是猜的。

DoD 要求的掃描做了——所有用 `useAdminQueryState`／`useAdminQueryValue` 的元件，其測試檔現在
都有重設 URL：`admin-settings-panel`、`admin-catalog-review-panel`、`admin-usage-settings-panel`、
`community/admin`。只有這一個漏掉。

種子 `1789176414571` 驗證：改之前紅、改之後綠。
