---
id: 2026-09-11-release-reservation-on-cancel
title: 取消或逾時搜尋時釋放已保留的次數
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-11T14:57:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/search/router.py
  - apps/api/app/usage/service.py
---

# 取消或逾時搜尋時釋放已保留的次數

## Why

`2026-09-11-search-result-dead-ends` 加了搜尋的取消鈕與 150 秒逾時，但**前端只關掉串流，沒有通知後端釋放保留的次數**。

`POST /searches` 會先 `reserve_use()` 佔用額度（`apps/api/app/usage/service.py:220`），正常完成或失敗時由既有流程結算。取消與逾時是新增的路徑，目前走不到結算，保留會留在帳上直到（如果有的話）過期機制回收。

線上每個操作目前扣 0 次（`GET /usage-catalog` 的 `operation_costs` 全為 0），所以實際上沒有人損失次數。**但那是設定值，不是保證**——任何人把扣次調成非 0，這個漏洞立刻生效。

## Definition of done

- [ ] 取消或逾時的搜尋，其保留的次數會回到使用者帳上。
- [ ] 重複取消、或取消與完成同時發生，不會重複釋放或誤釋放。

## Steps

- [ ] 後端加一個釋放端點（或讓既有的搜尋狀態端點接受取消）。`usage/service.py` 已有保留的資料結構，需要的是對外的入口。
- [ ] **冪等與競態要想清楚**：使用者按取消的同一刻，搜尋可能剛好完成並結算。釋放必須只在「尚未結算」時生效，且重複呼叫無害。
- [ ] 前端 `search-experience.tsx` 的 `cancelSearch()` 與逾時處理各呼叫一次。
- [ ] 測試涵蓋：取消後餘額回復、完成後再取消不會多還、連按兩次取消只釋放一次。

## How to verify

```bash
cd apps/api && uv run pytest tests -k "usage or search" -q
cd apps/web && npm run test:web -- search-experience
```

## Notes

- 不要用「反正現在扣 0 次」當作不做的理由。那個設定隨時可能改，而額度錯誤對使用者是直接的信任損失。
- 取消的 UI 已經在了，只差後端這一段。
