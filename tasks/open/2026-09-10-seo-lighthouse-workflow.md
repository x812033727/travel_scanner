---
id: 2026-09-10-seo-lighthouse-workflow
title: Lighthouse SEO 與效能門檻 workflow
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-10T16:43:50Z
completed_at:
branch:
depends_on:
  - 2026-09-10-seo-robots-sitemap
  - 2026-09-10-seo-destination-landing-pages
  - 2026-09-10-seo-server-render-home-and-explore
scope:
  - .github/workflows/seo-audit.yml
  - apps/web/lighthouserc.json
---

# Lighthouse SEO 與效能門檻 workflow

## Why

CI 目前沒有任何效能或 SEO 迴歸的守門。`.github/workflows/ci.yml` 跑 lint、i18n、任務檢查、typecheck、
vitest、build 與一份固定的 Playwright spec 清單，但沒有任何一項會在 LCP 變差、canonical 被改壞或
`noindex` 誤掛時擋下來。

前面幾個 SEO 任務會把 canonical、hreflang、sitemap、結構化資料與伺服器端渲染一一補上；沒有守門，
下一次重構就會把它們一一弄回去，而且沒有人會在 Search Console 掉排名之前發現。

## Definition of done

- [ ] 一個獨立的 workflow 對 production build 起 `next start`，跑 Lighthouse 並上傳報告 artifact。
- [ ] 涵蓋五個代表性網址：`/en`、`/zh-TW`、`/en/destinations`、`/en/destinations/tokyo`、`/en/hotspots`。
- [ ] 預算寫在 `apps/web/lighthouserc.json` 裡，而不是散在 workflow 的參數。
- [ ] 前兩週先 `continue-on-error: true` 收集基準線，之後再收緊成硬門檻。
- [ ] **完全不動 `.github/workflows/ci.yml`。**

## Steps

- [ ] `.github/workflows/seo-audit.yml`：checkout → `npm ci` → `npm run build:web` →
      `npm --workspace @travel-scanner/web run start` → `treosh/lighthouse-ci-action` → 上傳報告。
- [ ] `apps/web/lighthouserc.json` 設定網址清單與 assertion；先只對 SEO 與 Accessibility 類別
      設硬門檻（那兩項穩定），performance 先觀察。
- [ ] 在 `docs/seo.md` 補一段說明門檻怎麼調整、基準線在哪裡看。

## How to verify

開一個 PR，確認 workflow 綠燈且報告 artifact 下載得到，裡面的 SEO 分數與 canonical/hreflang 稽核項目
符合預期。

## Notes

- **`.github/workflows/ci.yml` 被 `2026-09-09-clarify-stay22-module-switch`（review）鎖住，不可觸碰。**
  這也是為什麼要開新檔而不是加一個 job：`.github/workflows/seo-audit.yml` 與那條 scope 沒有前綴關係。
- 同理，CI 的 Playwright spec 清單也寫死在那個檔裡，加不進去。所有 SEO 斷言請寫成 vitest
  （`vitest.config.ts` 只排除 `e2e/**`，新的 `*.test.ts` 會自動被收），這比 Playwright 更快也更精準。
- **在 `2026-09-10-seo-server-render-home-and-explore` 之前跑 Lighthouse 沒有意義**：
  首頁的伺服器端輸出目前是一塊骨架，量到的是骨架的分數。這就是本任務 `depends_on` 它的原因。
- 需要一個能連到 API 的環境才量得準。若 workflow 裡不方便起完整後端，就接受降級狀態下的量測，
  並在 `lighthouserc.json` 註明門檻是在無後端狀態下訂的。
