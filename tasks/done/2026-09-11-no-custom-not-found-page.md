---
id: 2026-09-11-no-custom-not-found-page
title: 全站沒有自訂的找不到頁面
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T13:17:20Z
created_at: 2026-09-11T03:20:59Z
completed_at: 2026-09-11T16:19:38Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/app/[locale]/not-found.tsx
  - apps/web/app/[locale]/[...rest]/page.tsx
  - apps/web/e2e/signed-out.spec.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/messages/en/errors.json
  - apps/web/messages/ja/errors.json
  - apps/web/messages/ko/errors.json
  - apps/web/messages/zh-CN/errors.json
  - apps/web/messages/zh-TW/errors.json
---

# 全站沒有自訂的找不到頁面

## Why

`find apps/web/app -name "not-found*"` 沒有任何結果。任何打錯的網址、任何失效的舊連結、任何被刪掉的行程分享連結，都會落到 Next.js 的預設 404 畫面：純英文、沒有站台導覽、沒有回首頁的路。

`app/[locale]/error.tsx:8-13` 的存在正是為了避免這件事——它接住渲染錯誤並給出一個像樣的頁面——但 404 不走 error boundary，所以沒被涵蓋。

具體會踩到的路徑之一：`/flights` 本身沒有 page（`app/[locale]/flights/` 底下只有 `status/`），任何人從舊連結或手打進來就是預設 404。

## Definition of done

- [x] `/zh-TW/<不存在的路徑>` 顯示站台自己的 404 頁，有頁首、有回首頁的連結。
- [x] 五語系都正確。

## Steps

- [x] 新增 `app/[locale]/not-found.tsx`，版面沿用 `error.tsx` 的作法。
- [x] 文案放 `messages/*/errors.json`（`error.tsx` 的文案已經在那裡，同一個命名空間）。
- [x] 給幾個實際有用的出口：首頁、探索、我的旅程。
- [x] 確認 `/flights` 這類「有子路徑但沒有自己 page」的情況也會落到這頁。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run build
npx playwright test e2e/signed-out.spec.ts --grep "mistyped"   # CI 已經在跑這支 spec
```

手動：`/zh-TW/nope`、`/ja/nope`、`/en/flights` 各開一次。

## Notes

- 站主刻意關閉的四個功能（`/alerts`、`/flights/status`、`/labs/airlines`、`/pricing`）走的是另一套「暫停開放」頁，不是 404，不要混在一起。

## 完成紀錄（claude-opus-5, 2026-09-11）

改了三個地方：

1. `app/[locale]/not-found.tsx` —— 五語系的 404 頁，版面照 `error.tsx`，出口是首頁／探索／我的旅程。頁首要自己 render：這個 app 的 `<SiteHeader />` 在每一頁裡，不在 layout 裡，第一版漏掉就沒有導覽。
2. `app/[locale]/[...rest]/page.tsx` —— 只呼叫 `notFound()`。**沒有這個檔案，上面那一頁根本不會被用到。**完全不匹配的網址不會進到 `[locale]` 區段，Next 會用 app 根層級的 not-found，那裡沒有語系也沒有 provider，所以畫面就是 Next 自己的英文 404。Next 的文件（`next/dist/docs/01-app/03-api-reference/03-file-conventions/not-found.md`）把「根 layout 用頂層動態區段」列為 `not-found.js` 組不出全站 404 的兩種情況之一，官方解法是實驗性的 `global-not-found.js`——但那支會跳過 layout，語系、主題、provider 全都拿不到，所以這裡用 catch-all 把路徑拉回 `[locale]` 底下。
3. `e2e/signed-out.spec.ts` 加一個案例。放這支是因為 CI 的 e2e 清單裡，scope 沒有被別人持有的只有它和 `readability.spec.ts`（`navigation.spec.ts` 被兩張 review 中的任務蓋住，`.github/workflows/ci.yml` 也是），而「打錯網址的訪客看到什麼」本來就屬於未登入的情境。

### 驗證

先重現再修，修完把修正還原確認測試真的會失敗：

| 還原的東西 | 測試結果 |
| --- | --- |
| 拿掉 `[...rest]/page.tsx` | ✘ `Received: "404"`，`<h1 class="next-error-h1">` —— Next 的預設畫面 |
| 拿掉 `<SiteHeader />` | ✘ `header.site-header` element(s) not found |
| 都復原 | ✓ 6 passed（desktop-chromium + mobile-chromium） |

實機確認過五個語系都對，狀態碼都是 404，390px 與 1440px 都一樣：

```
/zh-TW/nope   404  h1="找不到這個頁面"
/en/nope      404  h1="We couldn't find that page"
/ja/nope      404  h1="ページが見つかりません"
/ko/nope      404  h1="페이지를 찾을 수 없습니다"
/zh-CN/nope   404  h1="找不到这个页面"
/zh-TW/flights 404 h1="找不到這個頁面"
```

### 動到了別人 scope 裡的一個檔案

`apps/web/app/sitemap.test.ts` 在 `2026-09-10-seo-robots-sitemap` 與 `2026-09-11-pr388-seo-review` 的 scope 裡，但這一行非改不可：

它的 `routeExists()` 把任何 `[...]` 資料夾當成「可以吃掉一個路段」的萬用比對。`[...rest]` 是 catch-all，會吃掉**所有**剩下的路段，所以加了它之後 `routeExists()` 對任何網址都回 true——`would notice a path that has no page` 因此變紅，而它上面那條「sitemap 每一條都要對到真的 page」的守門就默默失效了（失效比變紅嚴重：改名會讓 sitemap 變成一串 404 而沒有人會發現）。

改的內容是把 catch-all 從候選名單排除，三行註解說明原因，沒有動任何斷言。不這樣做的替代方案只有 `global-not-found.js`（實驗性，且跳過 layout 就拿不到語系），等於放棄這張任務。

### 一個踩到的坑，留給後面的人

`npm run start`（`next start`）配上 `output: "standalone"` 會印一行警告然後**安靜地服務錯的東西**——我照它跑了一輪，`/zh-TW/nope` 明明已經有自訂頁還是回 Next 的預設畫面，白花了一次除錯。要驗證 production 行為請跑 `node .next/standalone/apps/web/server.js`（記得先把 `.next/static` 和 `public` 複製進去）。`playwright.config.ts` 的 `PLAYWRIGHT_SERVE_BUILD` 走的也是 `npm run start`，同一個坑。

### 順帶記下來的事實

404 頁的 HTML 主體是空的，內容只在 RSC payload 裡，靠客戶端算出來（一般頁面會 SSR 出內容）。`notFound()` 會讓該子樹的 SSR HTML 中止。對讀者沒有影響——瀏覽器實測畫面正常、狀態碼正常——對 404 頁的 SEO 也沒有影響，所以這裡不處理，只是寫下來免得後面有人以為是自己改壞的。
