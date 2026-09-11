---
id: 2026-09-11-itinerary-item-delete-no-confirm
title: 刪除行程項目沒有確認而且復原視窗短於自動儲存
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
---

# 刪除行程項目沒有確認而且復原視窗短於自動儲存

## Why

`trip-editor.tsx:1281-1293` 刪除行程項目時直接移除，沒有任何確認。取而代之的是一個「復原」提示，但兩個計時器互相矛盾：

- 復原提示 8 秒後過期（`:558-561`、`:563-567`）。
- 自動儲存 1 秒後就把刪除寫進後端（`:782-786`）。

所以在第 2 到第 8 秒之間，畫面上還掛著「復原」，但資料早就存下去了。使用者以為還有退路。

對照組就在同一個產品裡：`/trips` 刪除整筆行程**是有確認的**（`account-list.tsx:515-537`）。刪一整趟旅程要確認，刪掉排了半天的某一站不用——這個輕重是反的。

## Definition of done

- [ ] 刪除行程項目要嘛有確認，要嘛復原視窗確實有效（撤銷後後端狀態也跟著回復）。
- [ ] 畫面上不會出現一個實際上已經無效的「復原」。

## Steps

- [ ] 二選一：
      **(a)** 加確認框，沿用 `account-list.tsx:515-537` 的樣式；或
      **(b)** 保留無確認的快速刪除，但讓自動儲存在復原視窗內延後（把 debounce 拉到 8 秒），並讓「復原」真的能還原後端狀態。
- [ ] 建議 (b)——快速刪除對排行程是對的互動，問題出在兩個計時器沒對齊。
- [ ] 加測試釘住：刪除後 3 秒按復原，重新載入頁面該項目仍在。

## How to verify

```bash
cd apps/web && npm run test:web -- trip-editor
```

手動：在規劃器刪一站，數到 3 秒按復原，重新整理頁面確認那一站還在。

## Notes

- 與 `2026-09-11-usage-exhausted-dead-end` 共用 `trip-editor.tsx`，兩張任務不要同時認領。
- 規劃器的未存檔保護做得很好（`lib/navigation-guard.ts` 攔截點擊、popstate 與 `beforeunload`，`trip-editor.tsx:964-981` 的 `requestExit` 涵蓋草稿項目、偏好、備註、出發與設定），這個刪除路徑是少數的例外。
