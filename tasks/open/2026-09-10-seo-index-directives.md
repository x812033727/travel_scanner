---
id: 2026-09-10-seo-index-directives
title: 校正私人頁與功能關閉頁的索引指令
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-10T16:43:33Z
completed_at:
branch:
depends_on:
  - 2026-09-10-seo-canonical-hreflang
scope:
  - apps/web/app/[locale]/admin/layout.tsx
  - apps/web/app/[locale]/search/page.tsx
  - apps/web/app/[locale]/search/new/page.tsx
  - apps/web/app/[locale]/login/page.tsx
  - apps/web/app/[locale]/register/page.tsx
  - apps/web/app/[locale]/account/page.tsx
  - apps/web/app/[locale]/trips/page.tsx
  - apps/web/app/[locale]/trips/[id]/page.tsx
  - apps/web/app/[locale]/alerts/page.tsx
  - apps/web/app/[locale]/share/[token]/page.tsx
  - apps/web/app/[locale]/line/link/page.tsx
  - apps/web/app/[locale]/hotspots/layout.tsx
  - apps/web/app/[locale]/trips/layout.tsx
  - apps/web/app/[locale]/alerts/layout.tsx
  - apps/web/app/[locale]/pricing/layout.tsx
  - apps/web/app/[locale]/flights/status/layout.tsx
  - apps/web/app/[locale]/labs/airlines/layout.tsx
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

- [ ] 上表每一條路徑都輸出 `noindex`。
- [ ] `/{locale}/admin/**` 全部 `noindex, nofollow`，而且**不是**逐頁加上去的。
- [ ] 功能被關閉或 `site-visibility` 查詢失敗時，六個 gated 路由（`hotspots`、`trips`、`pricing`、
      `alerts`、`flights/status`、`labs/airlines`）輸出 `noindex`；功能正常時不受影響。
- [ ] 這些頁面仍然可被爬取（沒有被 robots.txt `Disallow`），爬蟲才看得到 `noindex`。

## Steps

- [ ] 新增 `apps/web/app/[locale]/admin/layout.tsx` 的
      `export const metadata = { robots: { index: false, follow: false } }`。
      該檔目前只有 default export，加一個 metadata export 即可覆蓋整棵 admin 樹。
- [ ] 逐頁在既有的 `generateMetadata` 回傳值加上 `robots: { index: false, follow: true }`
      （`share/[token]` 與 `line/link` 用 `follow: false`）。
- [ ] 六個 gated 路由各自已經有 `layout.tsx`（內容只是包一層 `PublicFeatureGate`），在裡面加：

      ```ts
      export async function generateMetadata(): Promise<Metadata> {
        const visibility = await getSiteVisibility();
        return featureEnabled(visibility, "hotspots") ? {} : { robots: { index: false } };
      }
      ```

      頁面自己的 `generateMetadata` 只回 `{ title, description }`，不會蓋掉 layout 的 `robots`。
- [ ] 補上覆蓋這些行為的單元測試（新檔，不要動 `metadata.test.ts`）。

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
