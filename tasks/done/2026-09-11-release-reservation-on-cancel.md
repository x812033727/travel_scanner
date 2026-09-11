---
id: 2026-09-11-release-reservation-on-cancel
title: 取消或逾時搜尋時釋放已保留的次數
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T21:43:45Z
created_at: 2026-09-11T14:57:31Z
completed_at: 2026-09-11T21:56:52Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/api/app/search/router.py
  - apps/api/app/usage/service.py
  - apps/api/tests/test_usage_release.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-experience.test.tsx
---

# 取消或逾時搜尋時釋放已保留的次數

## Why

`2026-09-11-search-result-dead-ends` 加了搜尋的取消鈕與 150 秒逾時，但**前端只關掉串流，沒有通知後端釋放保留的次數**。

`POST /searches` 會先 `reserve_use()` 佔用額度（`apps/api/app/usage/service.py:220`），正常完成或失敗時由既有流程結算。取消與逾時是新增的路徑，目前走不到結算，保留會留在帳上直到（如果有的話）過期機制回收。

線上每個操作目前扣 0 次（`GET /usage-catalog` 的 `operation_costs` 全為 0），所以實際上沒有人損失次數。**但那是設定值，不是保證**——任何人把扣次調成非 0，這個漏洞立刻生效。

## Definition of done

- [x] 取消或逾時的搜尋，其保留的次數會回到使用者帳上。
- [x] 重複取消、或取消與完成同時發生，不會重複釋放或誤釋放。

## Steps

- [x] 後端加一個釋放端點：`POST /searches/{search_id}/cancel`。
- [x] 冪等與競態。→ `release_reservation` / `commit_reservation` 既有的 `FOR UPDATE` +
      「只在 reserved 時動作」就足夠，不必新做；三種情況寫在完成紀錄。
- [x] 前端 `cancelSearch()` 與逾時各呼叫一次。
- [x] 測試涵蓋三種情況。**整合測試在本機驗不到**（沒有 Postgres／Redis），詳見完成紀錄。

## How to verify

```bash
cd apps/api && uv run pytest tests -k "usage or search" -q
cd apps/web && npm run test:web -- search-experience
```

## Notes

- 不要用「反正現在扣 0 次」當作不做的理由。那個設定隨時可能改，而額度錯誤對使用者是直接的信任損失。
- 取消的 UI 已經在了，只差後端這一段。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 端點

`POST /searches/{search_id}/cancel`（`app/search/router.py`）。做的事只有一件：把那次搜尋
保留的次數還回去。**不叫停 worker**——已經丟進佇列的 job 收不回來，它寫出來的結果也照樣讀得到。
還的是保留，因為取消或逾時的人不該為一個他沒看到的答案付費。

`search.status` 刻意不動：orchestrator 在跑完時會無條件寫入真正的結果，這裡寫一個
`cancelled` 只會被蓋掉，等於在資料裡留一句不成立的話。

### 冪等與競態：不必新做，既有的鎖就夠

Steps 要求「釋放必須只在尚未結算時生效，且重複呼叫無害」。`release_reservation` 與
`commit_reservation` 都已經是這樣寫的——各自 `SELECT … FOR UPDATE` 取保留那一列，
而且只在 `status == "reserved"` 時動作：

- 取消和 worker 的結算同時發生 → 誰先拿到鎖誰算數，另一邊什麼都不做。
- 連按兩次取消 → 第二次看到 `released`，什麼都不做。
- 已經結算（charged）之後才取消 → 什麼都不做，帳面不變。

所以這張任務真正缺的只是「對外的入口」，如 Why 所寫。

### 一個刻意的取捨

如果使用者取消的同一刻 worker 剛好跑完，順序是「取消先」的話：保留被釋放，worker 的
`commit_reservation` 變成 no-op，結果寫進 DB 但沒有扣次——使用者得到一次免費的搜尋結果。
反過來（worker 先）則是正常扣次。

選擇容忍前者，因為兩害相權：對一個已經按下取消的人多收一次，比偶爾少收一次糟得多。

### 前端

`search-experience.tsx` 的 `cancelSearch()` 與 150 秒逾時各呼叫一次。搜尋 id 放在
`pending` ref 而不是讀 `searchId` state——逾時的 callback 是在搜尋還不存在的時候建立的
closure，讀不到後來才 set 的 state。搜尋自己走完（completed／failed／串流關閉）時把
`pending` 清掉，就不會為一個已經結算的搜尋送沒有意義的請求。

錯誤刻意吞掉：按下取消的人已經離開這次搜尋了，跳一個「取消失敗」對他沒有意義，而且端點
本來就可以安全地再呼叫一次。

### 驗證，以及本機驗不到的部分

- `tests/test_usage_release.py`（新）——三條，本機跑得到：保留的次數回到帳上而餘額不變、
  已 committed 的不動、已 released 的不動。
- `components/search-experience.test.tsx`——取消與逾時各一條，都斷言真的送出了 POST，
  而且取消只送一次。把 `releaseSearch()` 裡那行 `api(...)` 拿掉，兩條都轉紅（實測）。
- `tests/test_integration_postgres_redis.py`（新增兩條）——完整的端點行為：取消後
  `reserved_uses` 歸零且可用次數 +1、連續兩次併發取消不會多還、別人的搜尋回 404、
  已扣次之後才取消不會把帳退回去。

**這兩條整合測試在本機驗不到**：這個環境沒有 Postgres 與 Redis，整份
`test_integration_postgres_redis.py` 的 23 條全部 skip。所以那兩條是照著同檔既有的寫法寫的，
由 CI 實際執行；unit 與前端那五條是本機跑過、也做過「還原修正 → 轉紅」確認的。
