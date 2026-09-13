---
id: 2026-09-13-adsense-article-slot
title: 文章頁 AdSense 版位、載入器與文章路由 CSP
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T08:08:46Z
created_at: 2026-09-13T05:16:19Z
completed_at: 2026-09-13T08:38:55Z
branch: claude/google-adsense-integration-plan-650u03
depends_on:
  - 2026-09-13-adsense-privacy-policy-section
  - 2026-09-13-adsense-admin-config
  - 2026-09-12-attribute-affiliate-clicks-to-the-guide
scope:
  - apps/web/components/ads
  - apps/web/lib/adsense.ts
  - apps/web/lib/adsense.test.ts
  - apps/web/lib/adsense-config.ts
  - apps/web/lib/adsense-config.test.ts
  - apps/web/lib/adsense.server.ts
  - apps/web/app/[locale]/layout.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/app/(ads-public)
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.tsx
  - apps/web/app/[locale]/life/[slug]/page.tsx
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/proxy.ts
  - apps/web/public/ads.txt
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/guides-adsense.spec.ts
  - .github/workflows/ci.yml
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - docs/travel-guides.md
  - docs/adsense-feasibility.md
---

# 文章頁 AdSense 版位、載入器與文章路由 CSP

## Why

評估全文在 `docs/adsense-feasibility.md`。這張是真正把廣告放上頁面的那一步，只限
旅遊情報攻略與生活分享的**文章頁**（`/{locale}/guides/{kind}/{slug}`、`/{locale}/life/{slug}`）。
其他頁都不放：分享頁、社群、hub、帳號、行程。

依賴三張票：隱私政策揭露（沒有就違反 AdSense 政策）、後台設定與匿名設定端點、
分潤點擊記到文章（沒有就量不出廣告有沒有吃掉分潤點擊）。另外要等站主做完 D1–D5，
並且 AdSense 審核通過、slot ID 已填進後台。

## Definition of done

- [x] **只在文章頁**、而且伺服器端判斷可以時才輸出版位。條件：
      設定端點回開啟；請求沒有 `Sec-GPC: 1` 或 `DNT: 1`；該語系的文章可讀，
      也就是不是 unavailable、不是「沒有你的語言」頁。關閉時連預留空間都不輸出。
- [x] 版位規則：
      - 數量照 D3（1–2 個）。
      - 不在第一屏（hero 是 LCP，`article.tsx:116-137`）。
      - 不貼著 offer island 或文末合作區塊，中間至少隔一個內容段落；政策禁止廣告放在互動元素旁。
      - 預留固定最小高度，避免 CLS。
      - 上方標示「廣告」：新 key 放 `common.json` 的 `guides.*`，五語系。
- [x] 載入器是 client island：`next/script` 載入
      `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=<ca-pub>`（`crossOrigin="anonymous"`）。
      每個 `<ins class="adsbygoogle">` mount 時 push 一次；D1 選非個人化時先設
      `requestNonPersonalizedAds = 1`（見 AdSense「廣告個人化設定」的程式碼範例）。
      開發模式 StrictMode 會跑兩次 effect，用 `data-adsbygoogle-status` 防重複 push。
- [x] **document 邊界**：比照 Stay22 的前例（`docs/stay22-module-switch.md:41-62`、
      `app/(stay22-public)/[locale]/layout.tsx`），有廣告的文章頁放在獨立的 root layout（`app/(ads-public)`）。
      - 從文章頁到私人頁面一定是整頁導覽，已執行的廣告腳本不會留在帳號、行程頁的 document 裡。
      - 載入前去掉 query。
      - 這個 layout 不掛讀取 session 的 provider。
      - 設定關閉時退回原本的 layout。
- [x] **CSP（D5）**：`proxy.ts` 只對文章路由產生 AdSense 版政策。
      依 Google 說明是 `script-src 'nonce-…' 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:`，
      `frame-src`、`connect-src` 放寬到 `https:`；其他路由的政策一個字都不變。
      `lib/csp.test.ts` 加一組文章路由的斷言，既有斷言（`:9`、`:46`）保留給非文章路由。
- [x] `apps/web/public/ads.txt`：`google.com, pub-<16 位數字>, DIRECT, f08c47fec0942fa0`。
- [x] 測試：
      - `tools/e2e-runtime-api.mjs` 的新設定端點回關閉，所以既有 8 支「零外部請求」規格不變。
      - 新規格 `e2e/guides-adsense.spec.ts`：設定開啟時出現有標籤、有預留高度的版位，對 `pagead2.googlesyndication.com` 的請求在測試裡攔下；
        GPC 時沒有版位；hub、分享頁沒有版位。
      - 把新規格加進 `.github/workflows/ci.yml` 的 Playwright 清單。
- [x] 文件：`docs/travel-guides.md:98-100`「文章永遠不會讓瀏覽器向第三方抓圖」改成照實描述；
      `docs/adsense-feasibility.md` 記下 D1–D5 的最終答案。

## Steps

- [x] 開工前重讀 Google 的 AdSense CSP 說明與廣告個人化設定，確認寫法沒變（連結在評估文件第十節）。
- [x] `lib/adsense.server.ts`：伺服器端讀設定，比照 `lib/stay22-script.server.ts`。
- [x] `app/(ads-public)` layout、兩個文章路由搬過去或改掛；確認切換 layout 時是整頁導覽。
- [x] `components/ads`：版位元件與載入器。
- [x] `article.tsx` 在段落之間插版位；`article-page.tsx` 傳入是否可放。
- [x] `proxy.ts`＋`csp.ts` 的文章路由 CSP 與測試。
- [x] `ads.txt`、e2e fixture、新規格、ci.yml。
- [ ] （開啟後兩週）比較文章頁分潤點擊率（`GET /admin/analytics/affiliates` 的 by_article）與 CLS，結果寫進 Notes。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/guides-adsense.spec.ts e2e/site-experience.spec.ts e2e/stay22-script.spec.ts
```

CLS 要在頂層頁用 Playwright 量（`chromium.launch()`，`addInitScript` 先裝 `PerformanceObserver`），
而且要先對一個故意位移的對照頁跑一次，確認量得出非零值；內建瀏覽器 pane 永遠量到 0。

正式站：`curl -s https://mokaair.com/ads.txt`；開一篇文章看到「廣告」版位；
開 GPC（例如 Brave）再開同一篇，沒有版位也沒有對 googlesyndication 的請求。

## Notes

### 這次實作與票面規格的差異

- **依賴 `2026-09-12-attribute-affiliate-clicks-to-the-guide` 沒有等**（`--force` 認領的理由）。
  那是量測依賴，不是功能依賴：要比較的是「開啟前後」的分潤點擊率，而廣告預設關閉，
  程式碼可以先落地。它變成**開啟前的關卡**，寫進了評估文件第七節的站主步驟。
- **CSP 多了一個 `&& enabled` 判斷。** 票面是「文章路由一律套 AdSense 版政策」，那會讓 30 篇
  文章在廣告關閉時也永久失去 `'unsafe-eval'` 限制，而 `docs/security-audit-2026-09.md:210`
  正計畫把政策轉成強制。改成只有文章路由**且**廣告開啟才放寬，所以現況下 CSP 一個字都沒變
  （`lib/csp.test.ts` 有一條斷言就是在證明這件事）。
  代價：站主開啟後最多 60 秒內的文章請求仍帶嚴格政策（現在是 Report-Only，無影響）。
- **`app/(ads-public)` 不自己蓋一套 chrome。** Stay22 的 layout 自建精簡頁首頁尾，因為那頁
  本來就匿名；文章頁不行，讀者要有正常的頁首、頁尾與底部導覽。改成 `app/[locale]/layout.tsx`
  多收一個 `ads` prop（Next.js 自己永遠不會傳，所以其他路由逐字不變），廣告開啟時才
  不掛 `HeaderSessionProvider` 與 `SavedItemsProvider`——這兩個會打 `/auth/me`，
  不掛就等於那份 document 裡從來不存在關於讀者的答案可以被廣告腳本讀到。
  已知代價寫在 `docs/travel-guides.md` 的 Advertising 一節：跨 root layout 的導覽一律整頁重載，
  **廣告關閉時也一樣**，所以 hub → 文章會從 client 導覽變成整頁載入。
- **版位規則**在 `lib/adsense.ts` 的 `adsenseSplit`：第一個 level-2 標題與其第一段之後切開，
  切點之後至少要剩 `MIN_BLOCKS_AFTER`（6）個 block——這一條同時擋住薄文章，也保證了
  離 offer 區塊的距離（第一段 segment 就是到第一個 offer 為止）。`headingStart` 要接續，
  否則切開後第二半的 h2 會從 `section-1` 重編，目錄連結全部失效。
- **e2e 自己起伺服器**（比照 `stay22-script.spec.ts`）。設定是伺服器端決定、per-process 快取 60 秒、
  而且綁正式站 origin，用共用 fixture 沒辦法乾淨地開關，會污染其他規格。
  共用 fixture（`tools/e2e-runtime-api.mjs`）照樣要回應 `/api/v1/ads/config` 並回關閉，
  否則 404 會讓 `admin-operations`（數 4xx）與 `korea-dual-maps`（數 console 錯誤）變紅。

### 合併前的覆核抓到的四件事（都已修）

PR #449 開出來之後跑了一輪對抗式覆核，四個都是真的，修在同一條分支上：

1. **（高）廣告會出現在「找不到這篇文章」的頁面。** `loadAdsenseSlot` 只看路徑形狀，
   不看文章在不在。頁面雖然在 `article-page.tsx:169` 就先 return 了無內容畫面，
   但 **layout 比頁面更早決定要不要載入標籤**，所以 `adsbygoogle.js` 照樣會載入在一個
   沒有內容的頁面上——正好是 Google 的「無內容畫面」政策。
   改成 layout 也查 `getGuideArticle`（React cache，跟頁面共用同一次讀取）。
2. **（中）proxy 與 renderer 的閘門寬度不一樣。** proxy 只看路徑與開關，所以 DNT／GPC 的請求
   和非正式站 host 都會拿到放寬的 CSP，即使它們永遠不會收到廣告程式碼。
   抽出共用的 `adsenseRequestGate`，兩邊走同一個判斷。
   剩下唯一不同的是「文章存不存在」，那需要一次 API 讀取，proxy 每個請求都做不起。
3. **（中）設定快取失敗時會重新蓋時間戳。** 於是 API 一掛，舊的「開啟」永遠不會過期，
   站主的關閉開關按不動。改成失敗時不蓋章，而且超過 `MAX_STALE_MS` 就 fail closed。
   順手補了一個 `.catch`：proxy 每個請求都 await 它，一個被毒化的 in-flight promise
   會讓整站 500。
4. **（中）沒有主圖的文章，版位會落在第一屏。** hero 是選填的，而它是標題到第一節之間的
   主要高度來源。沒有 hero 時改成要求 `MIN_BLOCKS_BEFORE_WITHOUT_HERO` 的內文在版位之上。

前三項都做了變異驗證（把修正回退，確認對應的測試會紅）。

### 還沒做的

- CLS 沒有量。版位有固定最小高度、e2e 斷言了預留高度不為零，但真正的 CLS 量測要照
  How to verify 的寫法（`chromium.launch()` 加 `addInitScript` 裝 `PerformanceObserver`，
  而且先跑一個故意位移的對照頁確認量得出非零值）。這件事等站主真的開啟廣告後再做，
  跟上面那條分潤點擊率比較同一批。

- 為什麼要獨立 document：移除 React `<Script>` 收不回已經執行的第三方 observer 和 timer（Stay22 文件原話的意思）。
  文章頁跟帳號、行程共用 root layout 時，讀完文章用 client-side 導覽進私人頁，廣告腳本仍然在跑。
- `ads.txt` 可能已經在站主送審時先單獨上線了（評估文件第七節第 2 步），那就只要確認內容，不用重做。
- 分享頁 `/share/{token}` 絕對不要放：網址本身是秘密 token，同頁第三方腳本讀得到。
- 手機的 sticky header（z-40）與固定底部導覽（z-60）會跟錨定、插頁廣告撞在一起，所以要在 AdSense 後台關閉這兩種（D3）。
- Travelpayouts Drive 已經在每一頁載入（`app/[locale]/layout.tsx:109`）；獨立 layout 要決定帶不帶它，比照 Stay22 layout 是不帶。
- 範圍重疊：
  - `components/guides/article.tsx` 也在 `2026-09-12-attribute-affiliate-clicks-to-the-guide` 的 scope 裡，那張是依賴，先做完它。
  - `2026-09-13-content-partner-links-in-articles-non`（claude-opus-5，PR #450，rebase 在本票合併之後）讓文章內文多了
    `partner_link` 島（`components/guides/partner-link.tsx`，`splitGuideBlocks` 的 `segment.partner`），主圖下方的揭露句
    在有合作連結時改用 `guides.partnerDisclosure`。合作夥伴連結跟 offer 一樣會切段，所以 `adsenseSplit` 的
    `MIN_BLOCKS_AFTER` 間距同樣擋在第一個合作夥伴連結之前，不必另外處理；`article.test.tsx` 的
    "keeps the same distance from a partner link" 守著這一條。
  - `lib/csp.ts` 在 `2026-09-07-mokaair-community-web` 的 scope 裡；claim 前用 `npm run tasks -- list` 看它是不是 in-progress。
