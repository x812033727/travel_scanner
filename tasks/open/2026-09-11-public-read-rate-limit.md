---
id: 2026-09-11-public-read-rate-limit
title: 公開讀取端點沒有任何速率上限，整站可被匿名爬走
status: in-progress
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T22:14:42Z
created_at: 2026-09-11T22:14:37Z
completed_at:
branch: claude/prevent-web-scraping-6xj3dg
depends_on: []
scope:
  - apps/api/app/middleware.py
  - apps/api/app/infra.py
  - apps/api/app/config.py
  - apps/api/app/problems.py
  - apps/api/app/main.py
  - apps/api/tests/conftest.py
  - apps/api/tests/test_public_read_rate_limit.py
  - apps/web/lib/client-address.ts
  - apps/web/lib/client-address.test.ts
  - apps/web/lib/public-server-fetch.ts
  - apps/web/lib/public-server-fetch.test.ts
  - apps/web/lib/foods.server.ts
  - apps/web/lib/hotspots.server.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/destinations.server.ts
  - apps/web/lib/site-pages.server.ts
  - apps/web/lib/foods.server.test.ts
  - apps/web/lib/hotspots.server.test.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/destinations.server.test.ts
  - apps/web/lib/site-pages.server.test.ts
  - apps/web/components/site-information-page.test.tsx
  - apps/web/app/api/travel/[...path]/proxy-security.ts
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - .env.example
  - .github/workflows/ci.yml
  - docs/anti-scraping.md
---

# 公開讀取端點沒有任何速率上限，整站可被匿名爬走

## Why

`enforce_named_rate_limit`（`apps/api/app/infra.py:38`）有大約三十個呼叫點，但全部寫在 handler 裡，而且幾乎都以 `user.id` 為 key。**匿名的公開讀取端點一個都沒有納入**：`/hotspots/rankings`、`/foods/merchants`、`/guides`、`/discovery/feed` 都可以無限次抓。

更便宜的目標是不分頁、一次回傳整份資料集的端點——`GET /guides/sitemap`（`app/guides/router.py:58`，全部已發布文章的索引）、`/discovery/suggestions`、`/hotspots/facets`、`/foods/cities`、`/foods/categories`、`/guides/topics`、`/travel-services`。這些幾乎都設 `Cache-Control: no-store`，沒有任何快取層吸收重複請求。

`docs/security-audit-2026-09.md` 的 INF-10 與 `docs/security-audit-2026-09-04.md:104`（「限流／DoS 全面盤點」）早就把這個缺口記在案上，只是一直沒人做。

要留意的是本站**刻意要被搜尋引擎索引**（`docs/seo.md`：五語系、最多 365 URL 的 runtime sitemap、schema.org）。所以目標不是「擋掉機器人」，而是「留下搜尋引擎，擋掉大量複製」。

## Definition of done

- [x] 單一來源大量抓取公開讀取端點時會拿到 429；一般訪客與 Googlebot 完全無感。
- [x] 伺服器端渲染的頁面不會因為這個上限而自我封鎖。
- [x] Redis 不可用時公開讀取照常放行，不會變成全站故障。
- [x] robots.txt 對 AI 訓練爬蟲宣告拒絕，且不影響 Googlebot 的檢索與排名。

驗證過的實際行為：

- `/robots.txt` 的 `*` 群組仍是第一條且未更動，後面才是十一個 harvester 群組。
- 五個語系以 `Twitterbot/1.0`、關閉 JS 取回都是 200，內容 300KB 以上，目的地連結在
  伺服器 HTML 裡（`e2e/seo.spec.ts` 的不變式）。
- 帶 `X-Forwarded-For: 10.0.0.1, 198.51.100.77` 請求 `/zh-TW/foods`，三個內容讀取
  （`foods/cities`、`foods/categories`、`foods/merchants`）都帶著 `198.51.100.77`
  ——最右邊那段，不是可偽造的 `10.0.0.1`——而 `site-visibility`、`usage-catalog`、
  `community/status`、`ui-text` 四個旗標探針都沒帶，正是刻意的區分。
- `/[locale]/destinations`、`/foods`、`/hotspots`、`/guides` 改動前後都是 dynamic，
  沒有把任何頁面的算繪模式改掉（用 stash 後重建比對過）。

## Steps

- [x] `apps/web`：新增 `lib/client-address.ts`（從 `proxy-security.ts:64` 搬出 `forwardedClientAddress`，原處改 re-export）與 `lib/public-server-fetch.ts`，讓 SSR loader 比照 BFF 轉送 `X-Travel-Client-IP` / `X-Travel-User-Agent`。
- [x] 套用到 `foods.server.ts`、`hotspots.server.ts`、`guides.server.ts`、`site-pages.server.ts`、`destinations.server.ts` 的 `no-store` 路徑。**不要**套到走 `revalidate` 的目錄請求，也不要套到旗標探針。
- [x] `apps/api`：`infra.py` 抽出 `_incr_window`，新增 fail-open 的公開讀取計數；`problems.py` 讓 `AppError` 帶 headers；`middleware.py` 新增 `PublicReadRateLimitMiddleware`；`main.py` 註冊在 `RequestBodyLimitMiddleware` 與 `RequestContextMiddleware` 之間。
- [x] `config.py` 加 `public_read_rate_limit_mode`（預設 `observe`）、`public_read_ip_limit`、`public_read_ip_hour_limit`，一律有 `ge`/`le` 界限。
- [x] `robots.ts` 在現有 `*` 規則**之後**追加 AI 訓練爬蟲的拒絕群組。
- [x] 測試、`.env.example`、CI 的 `full-stack-smoke` 環境變數、`docs/anti-scraping.md`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test:web && npm run test:tools && npm run check:tasks && npm run build:web
cd apps/web && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/seo.spec.ts
```

`e2e/seo.spec.ts` 以 `userAgent: "Twitterbot/1.0"` 且關掉 JS 跑五語系，是這次的金絲雀。

## Notes

- **SSR 會繞過 BFF**，這是整個設計的樞紐。瀏覽器的 JSON 呼叫走 BFF（`app/api/travel/[...path]/route.ts:107` 設 `X-Travel-Client-IP`），但 SSR 的 11 個 loader 直接打 `API_INTERNAL_URL`，不帶訪客位址。天真地加 per-IP middleware 會把所有 SSR 流量算進 web 容器的同一個 IP，整站當場自我封鎖。所以 middleware **只對帶有轉送位址的請求計數**，沒有位址的視為第一方內部流量放行。
- `apps/web/lib/stay22-script.server.ts:8` 是現成前例：server module 裡 `await headers()` 並包在 React `cache()` 裡。
- **公開讀取必須 fail-open。** `enforce_named_rate_limit` 目前 Redis 一出問題就丟 503，那對登入是對的，對公開頁面等於 Redis 一抖全站掛掉。
- **先出 `observe` 模式**（只計數不阻擋）。一個 foods 頁面就是 3 個 API 呼叫，加上 client 端掛載後重抓約 5 次；但企業 NAT 與電信 CGNAT 會把很多人壓在同一個 IP 上，門檻要先用真實流量驗證過才能轉 `enforce`。
- **robots 的新規則群要接在 `*` 之後**：`app/robots.test.ts:10-17` 的 `disallows()` 只讀 `rules[0]`，放前面會讓 `/en`、`/zh-TW/foods` 被判為 disallow，整個檔案會紅。
- `Google-Extended` 與 `Applebot-Extended` 是純訓練用 token，擋它們不影響 Googlebot 檢索排名與 Applebot 搜尋。不擋 `ChatGPT-User`、`OAI-SearchBot` 這類使用者觸發或引用用途的 agent。
- **這次不做 UA 封鎖**：UA 可以隨手偽造，而任何 UA 規則都會擦到上面那個 Twitterbot 金絲雀。宣告交給 robots.txt，實際流量交給速率上限。
- `apps/api/tests/conftest.py` 存在的唯一理由就是「整套測試從同一個 IP 打同一個 Redis」而把 `AUTH_REGISTER_IP_LIMIT` 拉到 500。新的上限不補同樣一行，整套 API 測試會自己把自己 429。
- 後續（尚未開單）：邊緣層 nginx 的 `limit_req` 與「剝掉外部送進來的 `X-Travel-Client-IP` / `X-Forwarded-For`」——目前 `TRUST_PROXY_CLIENT_IP=true` 之下，compose 網路內任何容器都能偽造這個標頭（審計編號 API-11），**每來源計數的正確性完全建立在這一層之上**。
