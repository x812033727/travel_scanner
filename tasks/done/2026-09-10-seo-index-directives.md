---
id: 2026-09-10-seo-index-directives
title: 校正私人頁與功能關閉頁的索引指令
status: done
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T17:26:31Z
created_at: 2026-09-10T16:43:33Z
completed_at: 2026-09-11T14:39:07Z
branch: claude/seo-optimization-planning-xq1vjl
depends_on:
  - 2026-09-10-seo-canonical-hreflang
scope:
  - apps/web/app/[locale]/admin/layout.tsx
  - apps/web/app/[locale]/hotspots/layout.tsx
  - apps/web/app/[locale]/trips/layout.tsx
  - apps/web/app/[locale]/alerts/layout.tsx
  - apps/web/app/[locale]/pricing/layout.tsx
  - apps/web/app/[locale]/flights/status/layout.tsx
  - apps/web/app/[locale]/labs/airlines/layout.tsx
  - apps/web/app/[locale]/search/page.tsx
  - apps/web/app/[locale]/search/new/page.tsx
  - apps/web/app/[locale]/login/page.tsx
  - apps/web/app/[locale]/register/page.tsx
  - apps/web/app/[locale]/account/page.tsx
  - apps/web/app/[locale]/share/[token]/page.tsx
  - apps/web/app/[locale]/line/link/page.tsx
  - apps/web/app/[locale]/robots-directives.test.ts
---

# 校正私人頁與功能關閉頁的索引指令

## Why

目前 `robots: { index: false }` 的分布跟實際需求對不起來。

**該擋卻沒擋**（全部沒有任何 robots 指令，等於預設可索引）：

| 路徑 | 問題 |
| --- | --- |
| `/{locale}/search`、`/{locale}/search/new` | 比價結果頁，query 組合無限展開 |
| `/{locale}/login`、`/{locale}/register` | 登入註冊頁沒有搜尋價值，還會稀釋站台主題 |
| `/{locale}/account` | 帳號設定 |
| `/{locale}/trips`、`/{locale}/trips/[id]` | 使用者自己的行程（`/trips/[id]/print` 有擋，主頁沒有） |
| `/{locale}/alerts` | 價格通知設定 |
| `/{locale}/share/[token]` | 公開分享的行程快照，token 不可預測、屬於「未公開連結」，不該進索引 |
| `/{locale}/line/link` | LINE 綁定頁，連 metadata 都沒有 |
| `/{locale}/admin/**` 約 20 頁 | 只有 `admin/community` 與 `admin/pet-friendly` 有擋，其餘全裸 |

**另一個獨立問題**：`components/public-feature-gate.tsx` 在 `getSiteVisibility()` 回 `unavailable`
（後端 `/api/v1/runtime/site-visibility` 失敗）時渲染一個「暫停服務」頁，但那是 HTTP 200 加上該頁原本
可索引的 metadata。後端抖動期間被爬到，等於把空白頁收進索引。同樣情況也發生在功能被管理員關閉時。

## Definition of done

- [x] 上表每一條路徑都輸出 `noindex`。
- [x] `/{locale}/admin/**` 全部 `noindex, nofollow`，而且**不是**逐頁加上去的。
- [x] 功能被關閉或 `site-visibility` 查詢失敗時，六個 gated 路由（`hotspots`、`trips`、`pricing`、
      `alerts`、`flights/status`、`labs/airlines`）輸出 `noindex`；功能正常時不受影響。
- [x] 這些頁面仍然可被爬取（沒有被 robots.txt `Disallow`），爬蟲才看得到 `noindex`。

## Steps

- [x] 新增 `apps/web/app/[locale]/admin/layout.tsx` 的
      `export const metadata = { robots: { index: false, follow: false } }`。
      該檔目前只有 default export，加一個 metadata export 即可覆蓋整棵 admin 樹。
- [x] 逐頁在既有的 `generateMetadata` 回傳值加上 `robots: { index: false, follow: true }`
      （`share/[token]` 與 `line/link` 用 `follow: false`）。
- [x] 六個 gated 路由各自已經有 `layout.tsx`（內容只是包一層 `PublicFeatureGate`），在裡面加：

      ```ts
      export async function generateMetadata(): Promise<Metadata> {
        const visibility = await getSiteVisibility();
        return featureEnabled(visibility, "hotspots") ? {} : { robots: { index: false } };
      }
      ```

      頁面自己的 `generateMetadata` 只回 `{ title, description }`，不會蓋掉 layout 的 `robots`。
- [x] 補上覆蓋這些行為的單元測試（新檔，不要動 `metadata.test.ts`）。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks
npm run build:web && npm run start --workspace @travel-scanner/web
for p in en/login en/register en/search en/account en/trips en/alerts en/admin; do
  echo -n "$p: "; curl -s "http://localhost:3000/$p" | grep -o '<meta name="robots"[^>]*>' | head -1
done
```

每一條都要看到 `noindex`。再把後端停掉重打 `/en/hotspots`，確認 gated 頁也變成 `noindex`。

## Notes

- 修正**不要**寫在 `components/public-feature-gate.tsx` 裡：它是 component，拿不到 metadata。
  正確位置是六個 gated 路由各自的 `layout.tsx`。
- `apps/web/app/[locale]/admin/layout.tsx` 沒有被任何任務認領；`admin/site-pages`、`admin/community`、
  `admin/pet-friendly`、`admin/travel-services` 這幾個子目錄有人認領，但都不含 layout，不衝突。
- `apps/web/app/[locale]/account/page.tsx` 與 `2026-09-07-mokaair-community-web`（open）重疊，
  該任務不是 active 狀態所以不鎖 scope。
- 這些頁面**不要**同時寫進 `robots.txt` 的 `Disallow`（見 `2026-09-10-seo-robots-sitemap`）：
  被 Disallow 的網址爬蟲讀不到 `noindex`，已收錄的反而移不掉。
- `/{locale}/admin/**` 兩邊都做（robots.txt Disallow + `noindex`）是刻意的：後台從來沒打算被收錄，
  也沒有既有索引需要清除，擋在門口最省爬取預算。

### 實作結果（2026-09-10, claude-opus-5-seo）

- **私人樹用 layout 一次蓋掉，不逐頁加。** `trips/layout.tsx` 與 `alerts/layout.tsx` 加
  `export const metadata = { robots: { index: false, follow: true } }`，就涵蓋了
  `/trips`、`/trips/new`、`/trips/[id]`、`/trips/[id]/print`、`/alerts`。
  頁面自己的 `generateMetadata` 只回 `{ title, description }`，淺層合併不會蓋掉 layout 的 `robots`，
  實測 `/en/trips/new` 確實繼承到。所以 scope 裡原本列的 `trips/page.tsx`、`trips/[id]/page.tsx`、
  `alerts/page.tsx` 最後都沒有動，scope 已收斂成實際變更的檔案。
- **`admin/layout.tsx` 同樣一個 export 蓋掉約 20 頁**，用 `follow: false`——登入牆後面沒有值得爬蟲排隊的東西。
  `admin/community` 與 `admin/pet-friendly` 自己的 `communityMetadata()` 仍然優先，行為不變。
- **功能開關頁的修正不在 gate 元件裡。** `PublicFeatureGate` 是 component，拿不到 metadata。
  改成在四個公開 gated 路由的 `layout.tsx` 加條件式 `generateMetadata`，用既有的
  `featureEnabled(state, feature)`——它同時涵蓋「管理員關閉」與「settings API 讀不到」兩種狀態。
- `line/link/page.tsx` 原本連 `generateMetadata` 都沒有，等於繼承站台標題且開放索引，已補上。
- `share/[token]` 與 `line/link` 用 `follow: false`：這兩條路徑的內容屬於特定使用者，
  不該把裡面的連結餵進爬取佇列。其餘私人頁用 `follow: true`，上面的連結是一般公開導覽。
- **已知取捨**：`sitemap.ts` 列了 `/hotspots`、`/pricing`、`/flights/status`、`/labs/airlines`，
  若這些功能被長期關閉，那些網址會在 Search Console 累積「已被 noindex 排除」。
  讓 sitemap 感知開關需要打 API，而 `2026-09-10-seo-robots-sitemap` 已論證那條路不可行
  （build 期沒有後端）。判斷是：這幾個是產品核心功能，正常情況都開著，不值得為此把 sitemap 複雜化。

### 驗證紀錄

`npm run lint:web`、`npm run check:i18n`、`npm run typecheck:web` 通過；
`npm run test:web` 198 個檔案 1705 個測試全綠；`npm run build:web` 通過。

新增 `app/[locale]/robots-directives.test.ts`（28 個測試）：對每條私人路由，斷言它自己的 `page.tsx`
或它上面任何一層 `layout.tsx` 宣告了 `index: false`；對公開路由斷言頁面本身沒有宣告。
另有一個「守門的守門」用 `/foods` 當對照組——**不能用 `/hotspots`**，因為它的 layout 裡有條件式的
`index: false`，讀原始碼分不出條件式與無條件式。這一點是寫測試時才發現的。

對 production build 實測（後端刻意不啟動）：

```
/en/login /en/register /en/search /en/search/new /en/account
/en/trips /en/trips/new /en/alerts /en/my            → noindex, follow
/en/admin /en/line/link /en/share/abc123             → noindex, nofollow
/en /en/foods /zh-TW/foods                           → 無 robots meta（可索引）
/en/hotspots /en/pricing /en/flights/status
/en/labs/airlines                                    → noindex（settings API 讀不到）
```

最後一組正是這個任務要防的情境：後端抖動時爬蟲抓到的「暫停服務」頁不再是可索引的 HTTP 200。
`/en/pricing` 在該狀態下仍然輸出正確的 canonical。

驗證時第二次踩到同一個坑：舊的 `next start` 還佔著 3000 埠，新的啟動失敗但 curl 仍有回應，
量到的是上一版 build。看到「改了卻沒生效」時，先 `ps aux | grep next-server` 確認。

## 標記完成（由站主授權，非原持有者）

這張任務的工作已隨 PR #388（`d0ec33e`）合併進 main——`site-footer.tsx` 由 `ad2ab2e` 改過，各 `layout.tsx` 的索引指令也都在 main 上——但狀態一直停在 `review`，持有的 scope 因此擋住後續任務。

站主指示標記完成以解開 scope。若原持有者 `claude-opus-5-seo` 尚有未推送的後續工作，請重新開一張任務，不要把這張改回 review。
