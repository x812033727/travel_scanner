---
id: 2026-09-10-seo-lighthouse-workflow
title: Lighthouse SEO 與效能門檻 workflow
status: in-progress
priority: P3
area: ops
owner: claude-opus-5
claimed_at: 2026-09-14T13:49:17Z
created_at: 2026-09-10T16:43:50Z
completed_at:
branch: claude/gifted-archimedes-1zfznf
depends_on:
  - 2026-09-10-seo-robots-sitemap
  - 2026-09-10-seo-destination-landing-pages
  - 2026-09-10-seo-server-render-home-and-explore
scope:
  - .github/workflows/seo-audit.yml
  - apps/web/lighthouserc.json
  - docs/seo.md
  - .gitignore
---

# Lighthouse SEO 與效能門檻 workflow

## Why

CI 目前沒有任何效能或 SEO 迴歸的守門。`.github/workflows/ci.yml` 跑 lint、i18n、任務檢查、typecheck、
vitest、build 與一份固定的 Playwright spec 清單，但沒有任何一項會在 LCP 變差、canonical 被改壞或
`noindex` 誤掛時擋下來。

前面幾個 SEO 任務會把 canonical、hreflang、sitemap、結構化資料與伺服器端渲染一一補上；沒有守門，
下一次重構就會把它們一一弄回去，而且沒有人會在 Search Console 掉排名之前發現。

## Definition of done

- [x] 一個獨立的 workflow 對 production build 起 `next start`，跑 Lighthouse 並上傳報告 artifact。
- [x] 涵蓋五個代表性網址：`/en`、`/zh-TW`、`/en/destinations`、`/en/hotspots`，
      第五個以 `/zh-TW/destinations` 代替 `/en/destinations/tokyo`（理由見 Notes，這是本票唯一的偏離）。
- [x] 預算寫在 `apps/web/lighthouserc.json` 裡，而不是散在 workflow 的參數。
- [x] 前兩週先 `continue-on-error: true` 收集基準線，之後再收緊成硬門檻。
- [x] **完全不動 `.github/workflows/ci.yml`。**

## Steps

- [x] `.github/workflows/seo-audit.yml`：checkout → `npm ci` → `npm run build:web` →
      `npm --workspace @travel-scanner/web run start` → `treosh/lighthouse-ci-action` → 上傳報告。
- [x] `apps/web/lighthouserc.json` 設定網址清單與 assertion；先只對 SEO 與 Accessibility 類別
      設硬門檻（那兩項穩定），performance 先觀察。
- [x] 在 `docs/seo.md` 補一段說明門檻怎麼調整、基準線在哪裡看。

## How to verify

開一個 PR，確認 workflow 綠燈且報告 artifact 下載得到，裡面的 SEO 分數與 canonical/hreflang 稽核項目
符合預期。

## Notes

### 收尾紀錄（claude-opus-5, 2026-09-14）

**門檻是量出來的，不是猜的。** 用 /opt/pw-browsers 的 Chromium 跑真的 Lighthouse 12.6.1，
五個網址各三次、照 workflow 自己的設定（production build、無後端），得到中位數：

| URL | SEO | A11y | Best practices | Performance |
| --- | --- | --- | --- | --- |
| `/en` | 1.00 | 1.00 | 0.96 | 0.89 |
| `/zh-TW` | 1.00 | 1.00 | 0.96 | 0.86 |
| `/en/destinations` | 1.00 | 1.00 | 0.96 | 0.97 |
| `/zh-TW/destinations` | 1.00 | 1.00 | 0.96 | 0.97 |
| `/en/hotspots` | 0.66 | 1.00 | 0.96 | 0.91 |

SEO 與 A11y 三次之間毫無變異。**所以 SEO 門檻定在 1.0 而不是 0.9**：這些是決定性的標記檢查，
不是計時；0.9 會留下足夠空隙讓「canonical 掉了」或「誤掛 noindex」安全通過，而那正是本票說
要擋的兩件事。原本先寫 0.9，是量完才發現門檻鬆到擋不住它存在的理由。A11y 留 0.95，因為少數
稽核項（對比、點擊目標）看算繪而不是標記。performance 只觀察。

拿現成的 15 份報告重跑 `lhci assert`：exit 0，唯一輸出是 `/en/hotspots` 的 SEO 0.66 警告，
跟設計一致。

**`/en/destinations/tokyo` 拿掉了，這是本票唯一偏離 DoD 的地方。** 沒有後端時它是硬 500——
`page.tsx` 刻意在讀不到目的地目錄時 throw（停機要回 5xx，回 404 會請 Google 把真頁面丟掉），
而 `loadDestinations()` 對「空目錄」也回 null，所以光有後端還不夠，要有種好的 destination 資料。
更關鍵的是讀過 pinned action 的原始碼：collect 迴圈遇到失敗的主文件會中止**整個** run，
所以留著它不是多一個難看的分數，是另外四個網址一起收不到報告。改用 `/zh-TW/destinations`
（降級行為與 `/en/destinations` 相同，又多一個語言的內容路由）。三個地方都寫了怎麼加回來。

**加回網址時要同時加 pattern。** 只加進 `collect.url` 而沒有對應的 `matchingUrlPattern`，
LHCI 會照收、然後什麼都不斷言，日誌上跟通過一模一樣。

**其他實測到、與直覺相反的幾點：**

- 報告**不是**在斷言之前上傳的。pinned action 的順序是 collect → assert → upload；
  一開始註解寫反了。現在改成自己用 `if: always()` 的 upload 步驟，順序就不重要了，
  也順便讓 artifact 有跟全 repo 一致的 `retention-days: 7`。
- `timeout-minutes: 20` 不夠。單是 5 網址 × 3 次就量到約 13 分鐘，還沒算 `npm ci` 與 build。改成 45。
- `ci.upload` 區塊 action 根本不看（它自己硬寫 filesystem upload 且不傳 `--config`），
  留著只為本機 `lhci autorun`，已在 `"//"` 註明。
- `cancel-in-progress` 原本無條件開，會把 main 上的基準線 run 取消掉——正是本票要累積的東西。
  改成只在非 main 取消。
- 上游 tag 是 `12.6.2`，沒有 `v12.6.2`。pin 註解照實寫 `# 12.6.2`，仍通過
  `tools/workflow-pins.test.mjs` 的 `#\s*v?\d+\.\d+`。
- `chromeFlags` 必須是字串；寫成陣列會被默默弄壞。
- 頂層 `"//"` 鍵確認無害：`loadRcFile` 只讀 `ci`，action 的 `hasAssertConfig` 也只看 `ci.assert`。
- workflow 標頭原本宣稱 ci.yml 抓不到 canonical/noindex 迴歸，這是錯的——`e2e/seo.spec.ts`
  已經在測。已改成只主張本 workflow 真正新增的東西：分類分數。

**還沒做、留給後續：**

- 門檻尚未在 GitHub runner 上驗證過，只在本機量過。前兩週 `continue-on-error` 的用途就是這個；
  確認 runner 上的數字站得住之後再把那一行刪掉。
- 想量到「有後端」的真實分數，得另外起 postgres + redis + API 並種資料，那時再把
  `/en/destinations/tokyo` 加回去，並重新校準（`/en/hotspots` 屆時會長出真的 explorer，
  現在 1.00 的 A11y 是因為那頁幾乎是空的）。

- **`.github/workflows/ci.yml` 被 `2026-09-09-clarify-stay22-module-switch`（review）鎖住，不可觸碰。**
  這也是為什麼要開新檔而不是加一個 job：`.github/workflows/seo-audit.yml` 與那條 scope 沒有前綴關係。
- 同理，CI 的 Playwright spec 清單也寫死在那個檔裡，加不進去。所有 SEO 斷言請寫成 vitest
  （`vitest.config.ts` 只排除 `e2e/**`，新的 `*.test.ts` 會自動被收），這比 Playwright 更快也更精準。
- **在 `2026-09-10-seo-server-render-home-and-explore` 之前跑 Lighthouse 沒有意義**：
  首頁的伺服器端輸出目前是一塊骨架，量到的是骨架的分數。這就是本任務 `depends_on` 它的原因。
- 需要一個能連到 API 的環境才量得準。若 workflow 裡不方便起完整後端，就接受降級狀態下的量測，
  並在 `lighthouserc.json` 註明門檻是在無後端狀態下訂的。
