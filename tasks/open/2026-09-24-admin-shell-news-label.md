---
id: 2026-09-24-admin-shell-news-label
title: 後台頂列麵包屑、窄版標題與 ⌘K 面板把「AI 自動新聞」顯示成原始鍵 news
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-24T04:51:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/components/admin-shell.test.tsx
  - apps/web/lib/admin-news-copy.ts
  - apps/web/components/admin-news-workspace.test.tsx
---

# 後台頂列麵包屑、窄版標題與 ⌘K 面板把「AI 自動新聞」顯示成原始鍵 news

## Why

檢視 PR #694（每小時 AI 自動新聞，2026-09-23 合併）時發現，2026-09-24 在 main `692dcf5a` 上重驗，問題仍在。

打開 `/admin/news` 後，左側欄寫的是「AI 自動新聞」，頂列麵包屑卻是「營運控制台 / news」（寬度 1024 px 以上）。寬度在 521 到 1023 px 之間時，麵包屑會被藏起來，改顯示一行標題 `.admin-topbar-mobile-title`，這行也是 `news`（`apps/web/app/globals.css:939,952-953`）。520 px 以下這行標題本來就不顯示（`globals.css:958,960`），所以手機直向看不到頂列的錯字。⌘K 命令面板和「最近開啟」列出來的同樣是 `news`。更麻煩的是面板的篩選比對的是 label 加群組（`apps/web/components/admin-shell.tsx:101-105`），所以在面板輸入「新聞」或「AI」都找不到這一頁，只有打英文 `news` 才找得到。五個語系都一樣。

原因是兩個元件各自解析導覽名稱，只有一個知道 news：

- `AdminNav` 的 `label()`（`apps/web/components/admin-nav.tsx:97-99`）先特判 `item.key === "news"`，回傳 `adminNewsCopy(locale).nav`（`admin-nav.tsx:16,66`；字串在 `apps/web/lib/admin-news-copy.ts:2,22,39,53,67`）。
- `AdminShell` 的 `label()`（`admin-shell.tsx:46-47`）只特判 `sitePages`，接著依序找「後端給的 `label`」→「`copy.nav[key]`」→「`admin.navigation` 訊息目錄」→「原始鍵」。news 在前三處都找不到：
  - 後端不送 `label`。`AdminNavigationItem` 只有 `label_key`（`apps/api/app/admin/operations_schemas.py:10-16`），news 那筆的 `label_key="news"`（`apps/api/app/admin/operations_service.py:61-63`）。前端正規化之後 `label` 是 `undefined`（`apps/web/lib/admin-operations.ts:72,89`），離線備援那筆（`:34`）也沒有 label。
  - `adminOperationsCopy().nav` 五個語系都沒有 news（`apps/web/lib/admin-operations-copy.ts:16,20,28-30`，在 `:48` 取用）。
  - 五個 `apps/web/messages/*/admin.json` 的 `navigation`（從第 2 行開始）有 19 個鍵，有 `guides`（zh-TW 第 16 行），沒有 `news`。
- `AdminShell` 會先問 `navigationCopy.has(key)`（`admin-shell.tsx:47`）才取值，next-intl 不會報缺鍵，console 也沒有錯誤，所以一直沒人發現。
- 用到這個 label 的地方有四處：麵包屑 `admin-shell.tsx:112`、窄版標題 `:113`、命令清單 `:103`、最近開啟 `:132`。
- 測試只涵蓋側欄（`apps/web/components/admin-nav.test.tsx:55-64`），沒有 `admin-shell.test.tsx`。`apps/web/e2e/admin-operations-full-stack.spec.ts:4,16` 把 `/admin/news` 列在導覽清單裡，但不檢查麵包屑文字。
- `admin-shell.tsx` 最後一次修改是 `a92dc3e8`（2026-09-12）。#694 之後的提交只動過 `admin-news-copy.ts`（`827c74bd`，加模型選單字串），沒碰這個解析順序。

### 決定：名稱放進 `admin.navigation.news`

`guides` 已經是這樣做的（`admin-nav.tsx:68` 的註解、`admin-nav.test.tsx:42-53`）。兩個元件最後都會退回去讀 `admin.navigation`，所以只要在五個 `admin.json` 加上 `navigation.news`，`AdminShell` 不用改任何一行就會顯示正確。這樣 `AdminNav` 的 news 特例和 `adminNewsCopy().nav` 就都多餘了，一起拿掉，名稱只剩一個來源。

附帶的好處：`admin` 是可編輯的命名空間（`apps/web/lib/ui-text.ts:13-15`），站主可以在 `/admin/ui-text` 改這個名稱，側欄和頂列會一起跟著變。

否決的做法：

- **把 news 加進 `admin-operations-copy.ts` 的 nav 表**：CI 的 `check:i18n` 會紅。`tools/check-i18n.mjs:119-143` 在 CI 上（或本機有 staged 變更時）逐檔比對 `apps/web/{app,components,lib}` 底下的非測試檔，任何漢字連續字串的出現次數只要變多就擋下。這個檔目前「自動新聞」「自动新闻」「自動」都出現 0 次（已用 grep 確認），加進去就會報 `newly added display text '自動新聞' must use a message catalog`。
- **在 `AdminShell.label()` 也加 news 特例**（`key === "news" ? adminNewsCopy(locale).nav : …`）：過得了 check:i18n，但兩個元件各留一份特例，下一個新增的導覽頁還會再出同樣的問題。只有訊息目錄的做法走不通時才退回這條，到時要把 `apps/web/components/admin-shell.tsx` 加進 scope。

## Definition of done

- [ ] 在 `/zh-TW/admin/news`，頂列麵包屑的 `aria-current="page"` 和窄版標題（`.admin-topbar-mobile-title`，寬度 521–1023 px 時顯示）都是「AI 自動新聞」，不是 `news`。其他四個語系顯示各自的名稱：en `AI News`、zh-CN `AI 自动新闻`、ja `AI 自動ニュース`、ko `AI 자동 뉴스`。
- [ ] ⌘K 命令面板和「最近開啟」列出的是同一個名稱；在面板輸入「新聞」找得到 `/admin/news`。
- [ ] 側欄的名稱和待審徽章都不變（`admin-nav.test.tsx` 的 news 測試仍然通過）。
- [ ] news 的導覽名稱只剩 `admin.navigation.news` 一個來源：`admin-nav.tsx` 裡沒有 `"news"` 特例，`admin-shell.tsx` 也沒有，`adminNewsCopy()` 不再有 `nav`。
- [ ] 新增的 `admin-shell.test.tsx` 在 news 名稱退回原始鍵時會失敗。
- [ ] `check:i18n`（含 staged 時才跑的漢字檢查）、`lint:web`、`typecheck:web`、`test:web` 全綠。

## Steps

- [ ] 在五個 `apps/web/messages/*/admin.json` 的 `navigation` 加上 `"news"`，值沿用 `admin-news-copy.ts` 目前的 `nav`：en `AI News`、zh-TW `AI 自動新聞`、zh-CN `AI 自动新闻`、ja `AI 自動ニュース`、ko `AI 자동 뉴스`。五個檔的 `navigation` 鍵順序相同，最後一個都是 `uiText`，新鍵放在它後面。
- [ ] `admin-nav.tsx`：刪掉 `:16` 的 import、`:66` 的 `newsCopy` 和 `:97` 的 news 分支，`:68` 的註解改成同時涵蓋 guides 與 news。`:19` 的 icon 對照表不用動。
- [ ] `admin-news-copy.ts`：五個語系都拿掉 `nav`。同時把 `admin-news-workspace.test.tsx:120` 的 `expect(copy.nav).not.toBe("AI News")` 改成檢查 `copy.title` 不等於英文，否則 typecheck 會紅。
- [ ] 新增 `apps/web/components/admin-shell.test.tsx`：
  - 用 `AdminOperationsProvider` 包住 `AdminShell`，bootstrap 給 dashboard 和 news 兩筆（寫法照 `admin-nav.test.tsx:7-24`）。
  - `apps/web/vitest.setup.tsx:70-75` 把 `@/i18n/navigation` 全域 mock 掉，`usePathname` 固定回傳 `/`（`:73`）。這個檔要自己 `vi.mock("@/i18n/navigation", …)` 把路徑設成 `/admin/news`，覆寫方式參考 `language-switcher.test.tsx:6`。要注意連 `Link` 也要一起提供，`AdminShell` 和 `AdminNav` 都會用到它。
  - `AdminShell` 會渲染 `LanguageSwitcher`，它會呼叫 `next/navigation` 的 `useSearchParams`。比照 `site-header.test.tsx:6` 把 `./language-switcher` mock 成空元件最省事。
  - 斷言 `within(screen.getByRole("navigation", { name: "Breadcrumb" }))` 裡 `aria-current="page"` 的文字，以及 `.admin-topbar-mobile-title` 的文字，都是「AI 自動新聞」。`AdminShell` 裡面也會渲染 `AdminNav`，它的側欄連結同樣帶 `aria-current="page"`，所以不要用全頁的 `getByText` 或 `[aria-current]` 選擇器。
  - 打開命令面板、輸入「新聞」，斷言出現指向 `/admin/news` 的連結。
- [ ] `admin-nav.test.tsx:55` 的測試名稱（"isolated localized copy"）改成反映現在讀的是訊息目錄，斷言本身不用改。

## How to verify

```bash
npm run test:web -- admin-shell admin-nav admin-news-workspace
npm run lint:web && npm run typecheck:web
git add -A && npm run check:i18n   # commit 前跑：有 staged 變更時才會做漢字檢查，和 CI 行為一致
node -e 'for (const l of ["en","ja","ko","zh-CN","zh-TW"]) console.log(l, require("./apps/web/messages/"+l+"/admin.json").navigation.news)'
# 預期：五行都印出名稱，沒有 undefined
grep -n '"news"' apps/web/components/admin-nav.tsx apps/web/components/admin-shell.tsx
# 預期：沒有輸出（admin-nav.tsx:19 的 icon 寫法是 news: 不帶引號）
```

部署後用 owner 帳號檢查：

1. 打開 `https://mokaair.com/zh-TW/admin/news`，視窗寬 1024 px 以上，頂列是「營運控制台 / AI 自動新聞」。
2. 按 Ctrl+K 輸入「新聞」，出現「AI 自動新聞」，群組是「內容」。
3. 打開 `/en/admin/news`，頂列是「Operations console / AI News」。
4. 把視窗縮到 521–1023 px（例如 768 px），麵包屑會消失，換成一行標題，內容同樣是這個名稱。520 px 以下這行標題本來就不顯示，那裡看不到不算失敗。

## Notes

- 檢視 PR #694 時發現，2026-09-24 在 main `692dcf5a` 上逐一用 file:line 重驗。#694 那張票 `2026-09-23-ai-hourly-news-automation`（已在 tasks/done）只把名稱接到了側欄。
- 和其他票碰到同一批檔案，但不是同一件事：
  - `2026-09-11-admin-shell-modal-layer`（open）的 scope 也列了 `admin-shell.test.tsx`。這張票和它誰後落地，誰就在已經存在的檔案上追加測試。
  - `2026-09-24-keep-every-news-review-item-reachable`（open，P2）的 scope 含 `admin-news-workspace.test.tsx`。claim 時如果它已經是 in-progress，就把 `admin-news-copy.ts` 和 `admin-news-workspace.test.tsx` 從這張票的 scope 移掉，先保留 `nav`（留著無害），再另開一張小票清掉它。反過來，這張票 in-progress 的期間，那張 P2 也 claim 不了，所以這張要一次做完、盡快合併。
  - 另外 `2026-09-07-contextual-travel-services`、`2026-09-07-mokaair-community-web`、`2026-09-09-site-experience-settings` 的 scope 都含 `admin-nav.tsx` 或 `apps/web/messages`，`2026-09-07-merchant-style-discovery`、`2026-09-14-preview-never-charged` 含 `admin.json`。這些票目前都沒人認領，但這張票 in-progress 的期間，它們一樣 claim 不了。
- `useLocale` 在測試裡固定是 zh-TW（`vitest.setup.tsx:59`），另外四個語系靠 `check:i18n` 的鍵一致性檢查和上面那行 node 命令確認。
- jsdom 不套 CSS，所以單元測試抓得到 `.admin-topbar-mobile-title`，不論視窗寬度。斷點行為只能在部署後的步驟 4 用瀏覽器看。
