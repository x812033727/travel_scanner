---
id: 2026-09-12-guides-sitemap-followup
title: Carry the guides sitemap follow-ups into main
status: in-progress
priority: P2
area: web
owner: claude-opus-5-guides-sitemap
claimed_at: 2026-09-12T02:36:44Z
created_at: 2026-09-12T02:36:44Z
completed_at:
branch: claude/guides-sitemap-followup
depends_on: []
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/e2e/seo.spec.ts
  - tools/e2e-runtime-api.mjs
  - docs/seo.md
  - docs/travel-guides.md
---

# Carry the guides sitemap follow-ups into main

## Why

`/guides` 的 sitemap 由 PR #404 做完並合併。這個 session 在不知情的情況下平行做了同一件事
（PR #401，已關閉，分支 `claude/distracted-lumiere-260705` 保留）。兩邊逐項比對之後，剩下的是
main 真的缺、而且通過對抗式驗證的幾項。三個重點：

- **CI 從來沒有把文章渲染成真的 XML。** `tools/e2e-runtime-api.mjs` 完全沒有 guides 端點，
  `guideSitemapEntries()` 因此一律退回空陣列，`<lastmod>` 的序列化與「每篇只列自己已發布的語系」
  都沒有被跑到過——而靜態條目全都沒有 lastmod、全都帶五語系加 x-default，所以單元測試也代替不了。
- **一筆無法解析的日期會讓整份 `/sitemap.xml` 回 500。** loader 只檢查 `published_at` 是不是字串，
  Invalid Date 是 truthy 而且是 Date，Next 的序列化器會對它呼叫 `toISOString()` 並丟 RangeError。
  路由是 `force-dynamic`，所以那是請求時的 500，不是少一個網址。
- **`lastmod` 凍結在首次發布日這件事，main 上沒有任何地方記錄。**

## Definition of done

- [x] e2e 的 mock API 提供三筆合成文章；`seo.spec.ts` 檢查實際輸出 XML 的 `<lastmod>` 與每篇的
      hreflang（其中一篇沒有英文版，所以不該有 x-default）。
- [x] loader 丟掉無法解析的日期與不符 API grammar 的 slug，並有對應測試。
- [x] 上限測試檢查「留下的是哪幾筆」而不只是「留幾筆」；sitemap 端點的路徑有斷言。
- [x] `sitemap.test.ts` 在有文章的情況下釘住靜態前綴，並檢查 alternates 的實際網址，不只是 key。
- [x] `docs/seo.md` 補上 lastmod 凍結、失敗時退回靜態清單、x-default 的條件；
      `docs/travel-guides.md` 三處過時敘述更正。
- [x] `2026-09-11-guide-lastmod-republication` 進到 main 的 `tasks/open/`。
- [ ] PR 的 `api`、`web`、`containers`、`full-stack-smoke` 全綠（推送時 CI 還沒跑完，
      由分支保護在合併時把關）。

## Steps

- [x] `lib/guides.server.ts`：slug grammar 與日期可解析兩個條件，附上「為什麼這會毀掉整份檔案」的註解。
- [x] `app/sitemap.ts`：文章網址去重，讓同名的既有測試真的會失敗。
- [x] `lib/guides.server.test.ts`：畸形列補三種壞 slug 與壞日期；上限測試釘首尾；端點路徑斷言。
- [x] `app/sitemap.test.ts`：靜態前綴深度比對、alternates 網址逐一比對、重複列的去重案例。
- [x] `tools/e2e-runtime-api.mjs` + `e2e/seo.spec.ts`：合成文章與 XML 斷言，網址數改成 `5 * (10 + 33 + 33) + 3`。
- [x] `docs/seo.md`、`docs/travel-guides.md`。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks && npm run build:web
# 本機沒有 Docker／Postgres：production build 對 e2e 的 mock API
node tools/e2e-runtime-api.mjs &
API_INTERNAL_URL=http://127.0.0.1:8000 npm run start --workspace @travel-scanner/web -- --port 3000 &
curl -s localhost:3000/sitemap.xml | grep guides
cd apps/web && PLAYWRIGHT_REUSE_EXISTING=true PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/seo.spec.ts
```

## Notes

- **比對方法。** 六個面向各一個 agent 讀 `origin/main` 與 PR #401 的同一批檔案，共 51 項發現；
  每一項再交給一個獨立 agent 試著推翻，24 項存活。以下決定都來自存活的那些。
- **刻意沒有搬過來的：**
  - main 在 loader 算每篇的 `locales`，PR #401 在 route 算。行為相同，只是分層不同，不動它。
  - 拿掉 sitemap 讀取的 `X-Travel-Locale` 不是強化：middleware 本來就把 locale 綁成 `zh-TW`，
    兩種寫法送到 handler 的東西一樣，而 handler 根本不看。
  - 把 `"en"` 換成 `HREFLANG_DEFAULT`：文章頁 `page.tsx` 同樣寫死 `"en"`，只改 sitemap 反而會讓
    兩邊在常數改變時不一致，而那正是 Google 會交叉比對的地方。
  - PR #401 整份 `sitemap.test.ts`：它的 `routeExists` 是 #406 之前的版本，搬過來會讓
    `app/[locale]/[...rest]` 冒充字面路徑，弄壞「不存在的路徑要回 false」那道守門。
- **main 上的高嚴重度缺陷不在本 PR 修。** `published_at` 只記首次發布，改文重發不會前進
  （`admin_service.py:210` 是唯一寫入處，`test_published_at_records_the_first_publication_not_the_latest`
  釘住這個行為）。修它要動 API：改讀目前公開版本 revision 的 `created_at`，不要解凍這個欄位，
  因為列表排序與游標都依賴它。見 `2026-09-11-guide-lastmod-republication`。
- **另外建檔：** `2026-09-12-guide-slug-casing-shows-a-fake-outage`——大小寫不同的 slug 會讓讀者看到
  紅色的「暫時無法取得」，但文章其實是好的。比 #398 還早，兩邊都有。
