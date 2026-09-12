---
id: 2026-09-11-itinerary-item-delete-no-confirm
title: 【撤回】刪除行程項目的復原視窗其實是有效的
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T17:37:39Z
created_at: 2026-09-11T03:21:00Z
completed_at: 2026-09-11T17:39:31Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
---

# 刪除行程項目沒有確認而且復原視窗短於自動儲存

## Why

`trip-editor.tsx:1281-1293` 刪除行程項目時直接移除，沒有任何確認。取而代之的是一個「復原」提示，但兩個計時器互相矛盾：

- 復原提示 8 秒後過期（`:558-561`、`:563-567`）。
- 自動儲存 1 秒後就把刪除寫進後端（`:782-786`）。

所以在第 2 到第 8 秒之間，畫面上還掛著「復原」，但資料早就存下去了。使用者以為還有退路。

對照組就在同一個產品裡：`/trips` 刪除整筆行程**是有確認的**（`account-list.tsx:515-537`）。刪一整趟旅程要確認，刪掉排了半天的某一站不用——這個輕重是反的。

## Definition of done

- [x] 刪除行程項目要嘛有確認，要嘛復原視窗確實有效（撤銷後後端狀態也跟著回復）。
- [x] 畫面上不會出現一個實際上已經無效的「復原」。

## Steps

- [x] 二選一：
      **(a)** 加確認框，沿用 `account-list.tsx:515-537` 的樣式；或
      **(b)** 保留無確認的快速刪除，但讓自動儲存在復原視窗內延後（把 debounce 拉到 8 秒），並讓「復原」真的能還原後端狀態。
- [x] 建議 (b)——快速刪除對排行程是對的互動，問題出在兩個計時器沒對齊。
- [x] 加測試釘住：刪除後 3 秒按復原，重新載入頁面該項目仍在。

## How to verify

```bash
cd apps/web && npm run test:web -- trip-editor
```

手動：在規劃器刪一站，數到 3 秒按復原，重新整理頁面確認那一站還在。

## Notes

- 與 `2026-09-11-usage-exhausted-dead-end` 共用 `trip-editor.tsx`，兩張任務不要同時認領。
- 規劃器的未存檔保護做得很好（`lib/navigation-guard.ts` 攔截點擊、popstate 與 `beforeunload`，`trip-editor.tsx:964-981` 的 `requestExit` 涵蓋草稿項目、偏好、備註、出發與設定），這個刪除路徑是少數的例外。

## claim 用了 --force，理由寫在這裡（claude-opus-5, 2026-09-11）

`trip-editor.tsx` 在 `2026-09-10-seoul-day2-transport-ux`（codex-seoul-day2-release）的 scope 裡。理由與本分支前面幾張相同：claim 已逾 34 小時（board 標為 stale），且其工作已合併進 main（`5f34f77`），遠端分支已不存在。

## 撤回紀錄（claude-opus-5, 2026-09-11）

**這張任務的核心主張不成立，沒有改任何產品程式碼。**

原主張：復原提示掛 8 秒、自動儲存 1 秒就寫進後端，所以第 2 到第 8 秒之間畫面上那個「復原」是假的。

實際：**復原是真的。** `undoDelete()`（`:1301-1306`）走的是 `applyOrder()` → `updateItems()` → `markEdited()`，也就是把項目放回 `items` 之後**再存一次**。刪除先被寫進後端沒錯，但按下復原會把它寫回去。使用者不會失去那一站。

兩個計時器不一致是事實，但它造成的是「多一次往返」，不是「復原失效」。任務 DoD 的兩條——「復原視窗確實有效（撤銷後後端狀態也跟著回復）」和「畫面上不會出現一個實際上已經無效的復原」——原本就已經成立。

### 怎麼確認的

寫了兩個測試，都是先跑起來確認**現況就會通過**，再把 `undoDelete` 的持久化拿掉、確認它們真的會紅：

| 測試 | 情境 | 現況 | 拿掉持久化 |
| --- | --- | --- | --- |
| `still has a way back after the autosave has already written the delete` | 刪除 → 等 PUT 真的送出並讓伺服器只剩 0 個項目 → 按復原 | ✓ 伺服器最後又有那一站 | ✘ |
| `does not lose the undone stop when it is clicked while the delete is still in flight` | 刪除 → 第一個 PUT 卡住不回應 → 按復原 → 才放行 | ✓ | ✘ |

第二個是我另外想到的、比原主張更窄的競態窗口：刪除已送出但還沒回來時按復原。這個也沒問題。

### 留下來的東西

兩個測試都留在 `trip-editor.test.tsx`。原本這個行為沒有任何測試守著——既有的 `keeps delete recoverable from the mobile-friendly editor` 是在自動儲存觸發**之前**就按復原，所以它從來沒有碰到這張任務擔心的那段時間。現在有了。

### 沒有加確認框

任務的 Steps 自己建議 (b)「保留無確認的快速刪除」，理由是快速刪除對排行程是對的互動。既然復原本來就有效，加確認框只會讓排行程變慢。`/trips` 刪整趟旅程需要確認、刪一站不用——這個差別是合理的：前者沒有復原，後者有。
