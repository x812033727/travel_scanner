---
id: 2026-09-11-offline-day-view-needs-an-app
title: 當日檢視要真的離線可用，需要預先快取 app shell
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-offline-day
claimed_at: 2026-10-02T16:26:35Z
created_at: 2026-09-11T22:18:30Z
completed_at:
branch: claude/offline-day-view-shell
depends_on: []
scope:
  - apps/web/public/sw.js
  - apps/web/components/offline-trip-cache.tsx
  - apps/web/components/offline-trip-cache.test.tsx
  - apps/web/components/offline-trip-worker.test.ts
  - apps/web/e2e/offline-day-view.spec.ts
  - .github/workflows/ci.yml
  - .agents/skills/web-i18n-e2e/references/e2e-local.md
  - .agents/skills/web-i18n-e2e/references/flake-lessons.md
---

# 當日檢視要真的離線可用，需要預先快取 app shell

## Why

`public/sw.js` 的註解說「the day the traveller last opened is still readable」，
`app/[locale]/trips/[id]/page.tsx` 的註解說當日檢視是「readable without a signal」。
在真的 Chromium 裡量過之後，這兩句話**只在分頁沒有被關掉的前提下成立**。

worker 只快取一樣東西：`/api/travel/trips/{id}` 的回應。**document 沒有快取，JavaScript
沒有快取。** 所以真的沒有訊號時，瀏覽器連頁面都載不到——`page.reload()` 直接
`net::ERR_INTERNET_DISCONNECTED`，快取裡有什麼完全無關。

實際會發生的情況：旅客站在月台上打開當日檢視，把手機收進口袋，走進地鐵。再拿出來時，
分頁很可能已經被系統回收了。他看到的是瀏覽器的離線頁，不是今天的行程——而這正是這個功能
存在的理由。

完整的量測過程（包含 Playwright 的兩個限制）寫在
`tasks/done/2026-09-11-offline-today-e2e.md`。

## 要先決定的事

**這是不是想做的功能？** 預先快取 app shell 是一個真的 PWA，不是一個小修補：

- 要快取 document 殼、Next 的 JS chunk、CSS。chunk 的檔名每次 build 都會變，所以需要
  build 時產生的資產清單，或是一個 stale-while-revalidate 的策略。
- 快取版本要跟著部署失效，否則使用者會被鎖在舊版前端。
- 爆炸半徑會從「一個 URL 形狀」變成「整個站」。現在的 worker 刻意寫得極小，就是為了
  「這裡有 bug 也只會影響一個 URL」——那份保證會消失。

**或者換個方向**：不做 app shell，改成把註解與文案講清楚——當日檢視是「開著就不怕斷線」，
不是「離線可開」。這個選擇便宜很多，而且誠實。

## Definition of done

- [x] 站主決定方向：做 app shell，或改成如實描述現有能力。→ 派工單選了 app shell（PR 標題
      「the day view works offline by precaching the app shell」）。站主若改選「如實描述」，關掉這個
      PR 即可，main 不受影響。
- [x] 若做 app shell：沒有訊號時冷開 `?view=today` 仍看得到今天的安排，且部署後不會卡舊版。
- [ ] ~~若不做：……~~ 不適用。`trips/[id]/page.tsx` 的「readable without a signal」與
      `trips.todayEntryHint` 的「路上沒訊號也讀得到」在這個改動之後成立，沒有改。

## Notes

- 現有保護：`components/offline-trip-cache.test.tsx` 釘住「worker 回報 ready 之後才抓行程」。
  快取確實會被寫入，這一點沒有問題。
- Playwright 1.62 沒辦法測這件事：`page.route` / `context.route` 攔不到 worker 的 fetch，
  `context.setOffline(true)` 也到不了 worker。要驗證得用獨立的 Node + Chromium 腳本，
  或改用其他工具。→ **1.63 已經不是這樣**，見下面。

### 做了什麼（claude-opus-5-5-offline-day, 2026-10-03）

**worker 多存兩樣東西**，都放在原本那個以會員命名的快取裡（`mokaair-trip-v2-<member>`）：
當日檢視的 document，以及那份 document 點名的 `/_next/static` 檔（script、stylesheet、
預載的字型）。頁面在告訴 worker 會員是誰、抓過行程之後，送一個 `keep-day`，由 worker 自己
重抓 document、解析出它點名的檔案、先存檔案再存 document。

決定與理由：

- **線上時 worker 什麼都不改。** document、行程、static 檔一律先走網路，只有網路失敗才讀快取。
  所以部署後不會有人被留在舊前端，其他頁面也不會拿到舊 HTML。代價是慢網路（lie-fi）時不會
  提早退回快取，要等瀏覽器自己逾時。
- **不需要 build 時的資產清單。** Next 的 chunk 檔名每次 build 都變，但它們都在 document 裡：
  `<script src>`、`<link href>`，以及 React payload 裡的 `"static/chunks/…"`。worker 從存下
  的 document 讀出清單，所以 document 與它要的檔案永遠是同一個 build。e2e 斷言「頁面線上時
  載入的每一個 .js/.css 都在快取裡」，證明這份解析沒有漏。
- **部署後怎麼清：** 每次 `keep-day` 之後，刪掉所有已存 document 都沒點名的 static 檔。新 build
  的檔案只要有一支 script 抓不到，就保留舊 document 與舊檔案（兩者一致），不存半套。
- **快取名稱有版本**（`CACHE_VERSION = 2`）。新 worker activate 時刪掉同家族、舊版本的快取，
  包括 v1 的 `mokaair-trip-<member>`。所以部署後第一次載入任何頁面，舊的行程快取會被刪掉，
  直到下一次線上打開當日檢視才重新存——那一段時間只有「分頁開著」的保護也沒有。
- **重啟過的 worker 也讀得到。** `cacheName` 是 module state，瀏覽器每次重啟 worker 都會歸零；
  冷開時沒有任何頁面能先告訴它會員是誰。所以 worker 啟動時找唯一一個 v2 會員快取，只拿來
  「讀」；「寫」仍然要等頁面宣告。登出刪光、換會員刪掉前一個，規則沒變。
- **規劃器從不讀快取的行程**（`trips/[id]/page.tsx` 的註解一直這樣說，但舊 worker 只要有
  cacheName 就會回快取給任何頁面）。現在只有 client 是當日檢視時才回。
- **頁面等到被 worker 控制才補抓行程**（`controlled()`，最多 3 秒）。第一次造訪時 worker 啟用後
  才 claim 頁面，在那之前發出的請求不經過 worker，也就不會被存。
- **`keep-day` 一次只跑一個。** 兩個同時跑、中間剛好部署時，先跑完的會把後一個剛存的檔案當成
  沒人點名而刪掉，後一個再存 document 就會點名不存在的檔案。`offline-trip-worker.test.ts`
  有一個測試拿掉排隊就會紅。
- CSP：document 連同回應標頭一起快取，nonce 與內嵌 script 一致；worker 沒有新增任何內嵌 script。
- 不用 lookbehind 正則：舊的 iOS Safari 解析失敗會讓整支 worker 裝不起來。

### 驗證

- `components/offline-trip-worker.test.ts`（新）：把 `public/sw.js` 跑在記憶體裡的 Cache
  Storage 與可以斷線的假網路上，同一份快取啟動兩次 worker 就是「重啟後冷開」。11 個案例；換回
  main 的 `sw.js` 全紅。
- `components/offline-trip-cache.test.tsx`：多兩個案例（送 `keep-day`、等被控制才補抓）；換回
  main 的元件這兩個紅。
- `e2e/offline-day-view.spec.ts`（新，已加進 `ci.yml` 的 `web` job）：build 好的 app（webpack
  模式），線上開當日檢視 → 等快取完成 → 斷言線上載入的 .js/.css 全在快取 → `unrouteAll` +
  `setOffline(true)` → **斷言 worker 自己的 fetch 也失敗** → CDP `ServiceWorker.stopAllWorkers`
  → 關分頁開新分頁冷開 → 看得到行程名稱與今天的站、沒有任何 `/_next/static` 請求失敗 →
  規劃器網址 `ERR_INTERNET_DISCONNECTED`（其他頁面沒有被快取）。
  反向驗證：換回 main 的 `sw.js` 在等快取那一步紅；在新的 worker 下刪掉快取的 document 再冷開，
  得到 `net::ERR_FAILED`（所以綠燈不是網路給的）。
- 本機 `--repeat-each=5 --workers=1` 10/10、`--repeat-each=4 --workers=2` 8/8、
  `--repeat-each=3 --workers=2` 6/6。預設 worker 數、冷的 `next start` 上同時跑五支時有四支
  在第一個 `goto` 逾時 30 秒——那是這台機器的負載，序列跑每支 3–6 秒。
- 本機 build 的兩個坑：Turbopack 不吃 node_modules junction，要 `next build --webpack`；webpack
  模式產生的 `.next/types` 會讓兩個 `app/api/video/*/route.ts` 型別檢查失敗（main 就這樣，
  與這張票無關），本機 build 時暫時加 `typescript.ignoreBuildErrors`、跑完還原，之後刪掉
  `.next/types` 再跑 `typecheck:web`。

### 範圍追加

- `components/offline-trip-worker.test.ts`、`e2e/offline-day-view.spec.ts`：新的測試檔。
- `.github/workflows/ci.yml`：新 spec 不列進清單就永遠不會在 CI 跑。
- `.agents/skills/web-i18n-e2e/references/e2e-local.md`、`flake-lessons.md`：兩處寫著
  「setOffline／context.route 碰不到 worker」，在 Playwright 1.63 已經不成立，留著會讓下一個人
  以為這件事測不了。
