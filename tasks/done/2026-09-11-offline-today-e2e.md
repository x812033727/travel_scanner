---
id: 2026-09-11-offline-today-e2e
title: 當日檢視的離線 e2e 與 CI 接線
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T22:12:42Z
created_at: 2026-09-11T18:38:25Z
completed_at: 2026-09-11T22:18:57Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/e2e/offline-today.spec.ts
  - .github/workflows/ci.yml
  - tools/e2e-runtime-api.mjs
---

# 當日檢視的離線 e2e 與 CI 接線

## Why

`2026-09-11-planner-mobile-navigation-and-offline` 修好了當日檢視的離線快取競態（worker 回報就緒後由 `OfflineTripCache` 自己再抓一次行程），並用元件測試釘住了「順序正確、確實有抓」。但**「斷網後重新載入仍看得到內容」這件事只有瀏覽器能證明**，那張任務沒有做，原因兩個：

1. 新的 spec 檔在 CI 跑不到——`.github/workflows/ci.yml` 逐一列出要跑哪些 spec，而那個檔當時在兩張 review 中任務的 scope 裡。
2. 既有的 spec 用 `page.route` 攔 API，而 service worker 發出的請求不走那條路；把 worker 放進那些 spec 的環境，很可能讓原本穩定的 mock 開始不穩。

## Definition of done

- [ ] ~~一個 e2e：登入後開 `?view=today`，`context.setOffline(true)`，重新載入，畫面仍有今天的安排。~~
      **這個 DoD 本身不成立**，兩個地方都不成立，量測結果見下面的調查紀錄。
- [ ] 這個 spec 真的會在 CI 執行。→ 沒有 spec 可以加。

## Steps

- [ ] 新增 `apps/web/e2e/offline-today.spec.ts`，用自己的 context（`serviceWorkers: "allow"`），不要共用其他 spec 的 `page.route` mock。
- [ ] 等 `navigator.serviceWorker.controller` 出現、且 `OfflineTripCache` 的補抓完成，再 `setOffline(true)`。
- [ ] 把它加進 `.github/workflows/ci.yml` 的 browser spec 清單。
- [ ] 順手確認 worker 只攔 `^/api/travel/trips/[^/]+$`，不會影響同一個 context 裡其他 spec 的請求。

## How to verify

```bash
cd apps/web && npx playwright test e2e/offline-today.spec.ts
```

## Notes

- 已經有的保護：`components/offline-trip-cache.test.tsx` 釘住「worker 回報 ready 之後才抓行程」，包含 `/auth/me` 必須排在 `/trips/` 之前。缺的是真的斷網那一段。
- `sw.js` 只攔 GET 且只攔單一 URL 形狀，所以爆炸半徑很小；這也是為什麼可以用一個獨立 context 測。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

`.github/workflows/ci.yml` 與 `tools/e2e-runtime-api.mjs` 落在兩張 in-review 任務的 scope 裡：
`2026-09-09-clarify-stay22-module-switch`（codex-stay22-module，claim 於 09-09，已 stale）與
`2026-09-11-pr388-seo-review`（codex-pr388-review）。兩張的遠端分支都已不存在、工作都已合併
進 main（PR #388 的 `ad2ab2e`／`9724df0`），只是沒標 `done`。

## 調查紀錄：這張任務問錯了問題（claude-opus-5, 2026-09-11）

**沒有做出 e2e，也沒有留下任何程式碼。** 花在這上面的時間換到的是三個量測結果，
其中一個把整張任務的前提推翻了。全部都在真的 Chromium 裡量的，用的是 repo 裡真正的
`apps/web/public/sw.js`，不是複製品。

### 一、`page.route` 與 `context.route` 看不到 service worker 的 fetch

寫一個最小頁面註冊 worker、由 worker 代答 `/api/thing`，同時掛
`context.route('**/api/thing')`。結果：route handler 一次都沒被呼叫，頁面拿到的是伺服器的
真實回應。

所以**任何用 route mock 來讓 worker 的請求失敗的寫法都不成立**。這也順帶解釋了任務 Why
第 2 點的擔心——不是「可能不穩」，是根本攔不到。

### 二、`context.setOffline(true)` 也到不了 service worker

同一支探針，`setOffline(true)` 之後由 worker 代答的 fetch **仍然打到活著的伺服器**
（伺服器的計數從 1 變成 2）。Playwright 1.62。

把伺服器真的關掉，worker 才走進 cache fallback，回傳先前快取的內容（計數停在 2）。
所以「斷網」對 worker 而言只有一種做法：讓來源真的連不上。

### 三、最重要的一項：**冷啟動的離線畫面本來就不可能成立**

`public/sw.js` 只快取一個東西——`/api/travel/trips/{id}` 的回應。**document 沒有快取，
JavaScript 沒有快取。** 所以真的沒有訊號的時候，瀏覽器連頁面都載不到，快取裡有什麼都無關：
探針裡 `page.reload()` 直接 `net::ERR_INTERNET_DISCONNECTED`。

DoD 寫的「`context.setOffline(true)`，重新載入，畫面仍有今天的安排」因此有兩個地方不成立：
`setOffline` 到不了 worker，而重新載入在真正斷網時根本不會發生。

再往下追一層更清楚。我做過一版 e2e：讓 e2e API 伺服器對那個行程端點**直接砍掉 socket**
（因為 503 是一次完成的交握，`sw.js` 的 `fetch` 不會 throw，會照原樣把錯誤傳下去——這是對的
設計）。結果頁面顯示的是「讀取這趟行程時出了問題」，不是快取內容。原因是請求要經過 Next dev
server 的 `/api/travel/**` proxy，proxy 把斷掉的連線轉成一個有狀態碼的錯誤回應，worker 的
`fetch` 因此沒有 throw。

也就是說，在這個架構下：

| 情況 | 結果 |
| --- | --- |
| 來源連得到（proxy 活著） | 錯誤有狀態碼，worker 依設計原樣傳下去，快取用不到 |
| 來源連不到（真的斷網） | document 載不到，頁面根本不存在 |

**兩條路都到不了「冷啟動讀快取」。** 這個 worker 能做到的只有一件事：
**分頁一直開著**的時候，失去訊號後那一頁仍然讀得到行程——這一點探針驗證過了，是成立的。

### 所以這張任務該變成什麼

不是「補一支 e2e」，是一個產品問題：**當日檢視的離線能力，目前只在分頁沒有關掉的情況下有效。**
一個站在月台上、把手機收進口袋又拿出來、分頁已經被系統回收的旅客，看到的是瀏覽器的離線頁。

要真的做到「沒有訊號也打得開」，需要把 app shell（document + JS + CSS）也預先快取起來——
那是另一個功能，不是一支測試。另開 `2026-09-11-offline-day-view-needs-an-app-shell`。

至於「已經開著的分頁」那一段，能不能寫成 CI 跑得動的 e2e：以 Playwright 1.62 而言**不能**，
因為沒有任何槓桿可以只讓 worker 那一條連線斷掉。`components/offline-trip-cache.test.tsx`
已經釘住快取有被寫入；剩下的「快取真的被讀出來」我是在一支獨立的 Node + Chromium 腳本裡
驗證的，那不是 CI 跑得到的東西。

### 為什麼沒有留下那支寫到一半的 e2e

它會綠——但綠的理由是 fixture 的錯誤回應剛好被 `TodayView` 當成錯誤顯示，或是被我調整斷言
去迎合。留一支斷言比它名字弱的測試，比沒有測試更糟：下一個人會以為離線是有保障的。
