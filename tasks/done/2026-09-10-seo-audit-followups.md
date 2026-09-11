---
id: 2026-09-10-seo-audit-followups
title: SEO 稽核補漏：404 metadata、sitemap lastmod 與文件準確性
status: done
priority: P2
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T23:41:14Z
created_at: 2026-09-10T23:41:13Z
completed_at: 2026-09-11T15:54:09Z
branch: claude/seo-optimization-planning-xq1vjl
depends_on: []
scope:
  - docs/seo.md
  - README.md
---

# SEO 稽核補漏：404 metadata、sitemap lastmod 與文件準確性

## Why

前兩階段交付 7 個任務後重新稽核，找到數個漏掉的地方——其中兩個是我自己造成的。

## Definition of done

- [x] sitemap 不再輸出每次請求都變動的 `lastmod`。
- [x] `robots.ts` / `sitemap.ts` 的 `force-dynamic` 移除（它沒有作用，見 Notes）。
- [x] `lib/seo.ts` 的死碼 `pageMetadata` 刪除。
- [x] `routePathFromRequest` 不會讓重複斜線進入 canonical。
- [x] `docs/seo.md` 與實際出貨內容一致，且從 README 連得到。
- [x] 目的地解析器的三個缺陷修正（見 Notes）。
- [x] `TouristDestination` 不再輸出不合法的 `inLanguage`。
- [x] **實際跑過 CI 會跑的 Playwright spec**，而不是只讀過。

## Steps

- [x] 全部如上。

## How to verify

見「驗證紀錄」。

## Notes

### 我自己造成的兩個問題

**1. `force-dynamic` 是基於誤判加上去的，而且引進了一個真實缺陷。**
當初把 `robots.ts` / `sitemap.ts` 改成 `force-dynamic`，理由是「漏帶 build arg 的 build 會產出
localhost 的 sitemap」。實測推翻了這個理由：

```
build 時 NEXT_PUBLIC_SITE_URL=https://build-time.example
啟動時 NEXT_PUBLIC_SITE_URL=https://run-time.example
→ robots / sitemap / canonical 全部輸出 build-time.example
```

`NEXT_PUBLIC_*` 會被 inline 進 **server** bundle，所以 dynamic 讀到的是同一個 baked 值——
一點 runtime 彈性都沒買到。而且 `apps/web/Dockerfile:11` 本來就 `test -n "$NEXT_PUBLIC_SITE_URL" || exit 1`，
那個「漏帶 arg」的情境根本不可能發生。

當初之所以觀察到「runtime 值生效」，是因為那次 build **完全沒有**設這個變數——沒有值可以 inline，
才退化成 runtime 查詢。有值時就是 baked。兩次觀察都是真的，我當時的結論是錯的。

`force-dynamic` 唯一的實際效果是讓 `new Date()` 每次請求重新求值，也就是下面這個缺陷。

**2. `lastmod` 每次抓取都是「現在」。** 365 個網址每次被抓都宣稱剛剛更新過，而且和同一個
`<url>` 區塊裡的 `changeFrequency: "monthly"` 自相矛盾。Google 只在 `lastmod` 持續準確時才採用，
否則會整份不信任。**已整個拿掉**：沒有訊號好過假訊號，而真正的時間戳在 sitemap 刻意不打的 API 後面。

### 目的地解析器的三個缺陷

- **`recommended_days: {min: 3}` 會在目的地索引頁渲染成「3–0 天」**（五個語系都是）。
  索引頁只用 `min` 判斷卻同時渲染 `min` 與 `max`，而解析器把缺漏的值補成 `0`，
  抹掉了「沒提供」與「零」的差別。型別改成 `| null` 之後 TypeScript 直接把兩個呼叫端都標出來。
- **`{"items":[null]}` 會讓頁面 500。** `toSummary` 在 `try/catch` 外面執行，一筆 null 就拋例外——
  而這個模組的整個設計就是「壞掉的 payload 不可以把頁面弄倒」。
- **`key={entry.name}` 會撞 key。** 同一座城市裡連鎖店同名是常態（7-Eleven），
  loader 卻把 API 的 id 丟掉了。已改成保留 id，API 沒給就用 `name-index`。

另外：`text()` 現在會 trim（原本 padding 會進 DOM 與 JSON-LD）、`areas` 的空字串會被濾掉、
`country` 為空時不會再產生一個空的 `<h2>`。

### 結構化資料

`TouristDestination` 的 `inLanguage` **不是合法的 schema.org**——它衍生自 `Place`，
而 `inLanguage` 是 `CreativeWork` 的屬性。已移除（`WebSite` 上的那個是對的，保留）。
`breadcrumbs` / `itemList` 收到空陣列時改回 `null` 而不是空的 `itemListElement`（Rich Results 視為無效物件），
元件會把 null 濾掉。

### 刻意沒做的事

- **沒有替 `/pricing`、`/flights/status`、`/labs/airlines` 加麵包屑。** 後兩者是同步元件、
  沒有 locale，要加得先改成 async 並接 params，而 `flights/status` 還有一段關於 Suspense
  與靜態渲染邊界的註解。為了一個兩層的「首頁 › 方案」麵包屑去動它們，代價不成比例。
  改成**修正文件**去描述現況：麵包屑放在內容頁，工具頁不放。
- **沒有做自訂 404。** 稽核時被指出「404 會輸出自我 canonical 與六條 hreflang、沒有 robots」，
  **實測證明這是錯的**：Next 16 對 404 回應會自動注入 `<meta name="robots" content="noindex">`，
  而且完全不輸出 canonical 或 hreflang。實測 `/en/this-page-does-not-exist` → HTTP 404、
  `noindex`、0 條 hreflang。沒有東西要修。
  （`not-found.tsx` 的預設畫面是英文的，那是 UX 議題不是 SEO，留給別的任務。）

### 跨任務落地

`app/sitemap.ts`+test → `2026-09-10-seo-robots-sitemap`；`lib/seo.ts`+test →
`2026-09-10-seo-canonical-hreflang`；`lib/destinations.server.ts`、`components/destination-guide.tsx`、
`app/[locale]/destinations/page.tsx` → `2026-09-10-seo-destination-landing-pages`；
`lib/structured-data.ts`、`components/structured-data.tsx` → `2026-09-10-seo-structured-data`。
全部由本人持有、同一分支，與前兩階段一致。

### 修不了的，已記進 docs/seo.md

`app/(stay22-public)` 整棵樹（365 筆 sitemap 網址裡的 165 筆）被
`2026-09-09-isolate-public-stay22-script`（review）鎖住。已查證並記錄：該頁自建 `alternates`
且**漏掉 `x-default`**（與 sitemap 宣告的不一致）、165 個網址**共用同一句 meta description**、
`/destinations/osaka/services` 與 `/kyoto/services` 會解析但其指南頁 404、整棵樹沒有 JSON-LD
也沒有 `SiteFooter`。

## 驗證紀錄

`npm run lint:web`、`check:i18n`、`typecheck:web` 通過；`npm run test:web` **1811 個測試全綠**
（比上一輪多 11 個回歸測試）。

**第一次真的跑了 CI 會跑的 Playwright**（這個 image 的 Chromium 版本與專案 pin 的不符，
用 scratchpad 裡的 config 覆寫 `executablePath` 指到 `/opt/pw-browsers/chromium-1194`）：

| spec | 結果 |
| --- | --- |
| `readability.spec.ts` | **21 passed** —— 它掃的六條路由我全部動過 |
| `navigation.spec.ts` | 1 failed / 69 passed |
| `site-experience.spec.ts` | 6 failed |

失敗的那些**不是我造成的**：把變更 `git stash` 之後對 `ad2ab2e` 重跑，失敗數與**失敗的測試名稱
逐字相同**（navigation 1 failed/69 passed、site-experience 6 failed）。屬於既有問題。

build 後實測：`/robots.txt` 與 `/sitemap.xml` 都回到 `○`（預先產生）、365 筆 `<loc>`、
**0 筆 `<lastmod>`**、origin 正確。`TouristDestination` 不再有 `inLanguage`。
整份 sitemap 重新稽核：**365 個網址全部 200、沒有一條帶 `noindex`**。

## 標記完成（由站主授權，非原持有者）

這張任務的工作已隨 PR #388 於 2026-09-11 合併進 main：merge commit `d0ec33e` 的第二個 parent 就是分支 head `999dbc5`，分支上每個 commit 都在 main 裡，分支也已刪除。該 head 的每個 check 都通過（`api`、`web`、`containers`、`full-stack-smoke`、`discovery-browser`、`planner-browser`）。狀態卻一直停在 `review`，持有的 scope 因此擋住後續任務，2026-09-11 由 claude-opus-5 移到 done。

若原持有者 `claude-opus-5-seo` 尚有未推送的後續工作，請重新開一張任務，不要把這張改回 review。
