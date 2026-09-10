---
id: 2026-09-10-seo-home-ssr-and-internal-links
title: 首頁伺服器端輸出真正的內容，並把目的地頁接進連結結構
status: review
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T23:03:21Z
created_at: 2026-09-10T23:03:20Z
completed_at:
branch: claude/seo-optimization-planning-xq1vjl
depends_on: []
scope:
  - apps/web/lib/discovery-status.server.ts
  - apps/web/lib/discovery-status.server.test.ts
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
---

# 首頁伺服器端輸出真正的內容，並把目的地頁接進連結結構

## Why

上一階段做出 33 個城市指南（166 個網址）之後才發現兩個互相牽連的缺口。

**一、那 166 個頁面是孤兒。** 全站 `grep` 只找得到目的地頁彼此互連，沒有任何一處連到
`/destinations`。首頁的城市 chip 仍指向 `/hotspots?destination_id={id}`。只靠 sitemap 進索引
的頁面拿不到內部連結權重，也會被排到很後面才爬。

**二、想在首頁補連結也沒用，因為首頁的 body 根本不在伺服器輸出裡。**
`lib/discovery.ts` 的 `useSyncExternalStore` 第三個參數（`getServerSnapshot`）永遠回
`{ enabled: false, loading: true }`，所以 `DiscoveryHomeGate` 在伺服器上一律渲染骨架，
`<h1>`、hero 文案、七國十九城的連結列全部不在回應內容裡——**不分功能開關狀態**。

## Definition of done

- [x] discovery 關閉時（`DISCOVERY_ENABLED` 預設 false，即正式環境現況），首頁的伺服器輸出
      含 hero `<h1>` 與目的地連結列，且不再送出骨架。
- [x] discovery 開啟時行為完全不變，仍由 `DiscoveryHomeGate` 接手。
- [x] 每一個公開頁都有一條通往 `/destinations` 的連結，且文案依語系在地化。
- [x] 首頁城市 chip 改指 `/destinations/{id}`。
- [x] 不修改被鎖住的 `lib/discovery.ts`、`components/discovery/explorer.tsx`、
      `app/[locale]/page.test.tsx`，且那個測試維持通過。

## Steps

- [x] 新增 `lib/discovery-status.server.ts`：`API_INTERNAL_URL` + `cache: "no-store"` +
      `try/catch` 回 `{ enabled: false }` + React `cache()`，形態照抄 `lib/site-visibility.server.ts`。
- [x] `app/[locale]/page.tsx` 把 `<main>` 抽成 `body`，改成
      `{discovery.enabled ? <DiscoveryHomeGate>{body}</DiscoveryHomeGate> : body}`。
- [x] `components/site-footer.tsx` 加一條 `/destinations`，文案取自 `lib/destinations-copy.ts`。
- [x] 補測試。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web && npm run build:web
curl -s localhost:3000/zh-TW | grep -c '<h1'          # discovery 關閉時期望 >= 1
curl -s localhost:3000/en/foods | grep -c 'href="/en/destinations"'
```

## Notes

**繞道為什麼是安全的。** `DiscoveryHomeGate`（`explorer.tsx:22-30`）除了那個三元判斷之外
只有一個 `useEffect`，而且**只在 `enabled` 為真時**才把 `#trip-search` 導去 `/search/new`。
discovery 關閉時它除了透傳 `children` 什麼也沒做，所以關閉時繞過它不會失去任何行為。
開啟時仍然照舊包進 gate，行為一模一樣。

**這修的是真實的正式環境首頁，不是假設情境。** `DISCOVERY_ENABLED` 在
`.env.example:287` 與 `apps/api/app/config.py:96` 都預設 false。

**`GET /api/v1/discovery/status` 是公開且不碰資料庫的**（`apps/api/app/discovery/router.py:38-41`
只回 `{"enabled": get_settings().discovery_enabled}`），所以 `no-store` 的成本可以忽略。
用 `no-store` 而不是 `revalidate`：這是功能開關不是內容，切換要立即生效。

**`app/[locale]/page.test.tsx` 被 `2026-09-09-frontend-flow-discovery-web`（review）鎖住，
沒有修改，仍然通過。** 它把全域 `fetch` stub 成一律回 401，所以新 helper「fetch 失敗就回
`enabled: false`」這條分支正是它能繼續綠燈的原因——已寫成獨立測試案例釘住。
它也不斷言任何 `href`，所以 chip 改指沒有影響。

**footer 為什麼是正確的位置。** 它在 layout 裡是 `{children}` 的兄弟節點，不在任何 gate 之內，
所以無論 discovery 開關如何都會 SSR。文案用 `lib/destinations-copy.ts` 既有的 `breadcrumb`
（五語系齊備），**不動 `messages/`**——`navigation.json` 被兩個 open 任務認領，而新增 namespace
會牽動 `check-i18n` 交叉比對的兩份 allowlist（其中一份在 `apps/api`）。

**跨任務落地**：`app/[locale]/page.tsx` 的兩處修改（繞道、chip 改指）落在
`2026-09-10-seo-structured-data`（review、同一 owner、同一分支）的 scope 底下，處理方式與上一階段
把 sitemap 條目記在 `2026-09-10-seo-robots-sitemap` 一致。
`components/site-footer.tsx` 與其測試只被 `2026-09-09-site-experience-settings`（**blocked**）
認領，blocked 不鎖 scope。

**已評估後不做**：景點／店家詳情頁。549 個景點 slug 裡有 **279 個是 Wikidata QID 形式**
（`rmq-q3847114`），一半的網址沒有關鍵字價值，而每頁可用的公開內容只有名稱、區域、分類，
是典型的薄內容。與其新開 549 個薄頁，不如先把目的地頁的連結與內容做紮實。

## 驗證紀錄

`npm run lint:web`、`check:i18n`、`typecheck:web`、`build:web` 通過；
`npm run test:web` 207 個檔案 **1800 個測試全綠**（新增 9 個）。
被鎖住的 `app/[locale]/page.test.tsx` 單獨跑也通過。

對 production build 實測（stub API，discovery 兩種狀態各測一次）：

| | h1 | 骨架 | 城市連結 | JSON-LD | footer 入口 |
| --- | --- | --- | --- | --- | --- |
| discovery **關閉**（正式環境預設） | 1 | 0 | 19 | 1 | 1 |
| discovery **開啟** | 0 | 18 | — | 1 | 1 |

關閉時首頁終於送出 `<h1>少開十個分頁，多看懂一趟旅行。</h1>` 與 19 條 `/destinations/{id}`；
開啟時與修改前完全一致（gate + 骨架），代表沒有回歸。兩種狀態下 JSON-LD 與 footer 入口都在，
因為它們都在 gate 外面。

footer 入口在 `/en`、`/en/foods`、`/en/hotspots`、`/en/destinations`、`/en/pricing`、
`/en/flights/status`、`/en/destinations/tokyo` 各出現一次，標籤依語系為
Destinations／目的地／旅行先／여행지。

回歸稽核：整份 sitemap **365 個網址仍然全部 200，沒有任何一條帶 `noindex`**。
