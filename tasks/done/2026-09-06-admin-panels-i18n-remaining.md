---
id: 2026-09-06-admin-panels-i18n-remaining
title: 後台其餘三個面板文案硬編碼繁中
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T14:22:59Z
created_at: 2026-09-06T09:04:16Z
completed_at: 2026-09-06T14:57:07Z
branch: claude/admin-panels-i18n
depends_on: []
scope:
  - apps/web/components/admin-hotspot-places-panel.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-users-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/app/[locale]/admin/page.tsx
  - apps/web/app/[locale]/admin/settings/page.tsx
  - apps/web/app/[locale]/admin/system-settings/page.tsx
  - apps/web/app/[locale]/admin/hotspots/page.tsx
  - apps/web/app/[locale]/admin/foods/page.tsx
  - apps/web/app/[locale]/admin/users/page.tsx
  - apps/web/app/[locale]/admin/deployments/page.tsx
  - apps/web/app/[locale]/admin/analytics/page.tsx
  - apps/web/app/[locale]/admin/usage-settings/page.tsx
  - apps/web/app/[locale]/admin/layout-settings/page.tsx
---

# 後台其餘三個面板文案硬編碼繁中

## Why

`2026-09-06-admin-panels-i18n` 把最大的三個後台面板（settings／hotspots／food merchants）的文案搬進
`messages/*/admin.json` 之後，剩下三個還是寫死繁中：`admin-hotspot-places-panel.tsx` 約 55 句、
`admin-deployments-panel.tsx` 約 51 句、`admin-users-panel.tsx` 約 47 句。切到 `/en/admin` 這幾頁仍是中英夾雜。

跟上一張一樣是 P3：後台目前只有站長在用，繁中對他不是問題；列出來是為了讓「站台支援五語言」有一天能成立。

## Definition of done

- [x] 三個面板在 `/en/admin` 沒有繁體中文（資料本身除外）。
- [x] 新字串進 `messages/*/admin.json`，五語系鍵一致，照面板分組（`hotspotPlacesPanel`／`deploymentsPanel`／`usersPanel`）。
- [x] 三個面板各自的 `.test.tsx` 通過。
- [x] `CI=1 npm run check:i18n`、`lint:web`、`typecheck:web`。

## Steps

- [x] 一個檔案一個 commit，不要一次三個。
- [x] 沿用上一張的手法：`const t = useTranslations("admin")`，zh-TW 的值逐字照抄搬走的字面，
      測試裡的中文 accessible name 查詢就不用改；帶數字的句子用簡單 `{name}` 參數（vitest 的 mock 是 `replaceAll`，
      別用 plural／select）。
- [x] `admin.json` 用純文字插入，不要 JSON round-trip（會重排整份檔案、默默吃掉重複鍵）。
- [x] 可有可無的說明文字用 `t.has()`（`vitest.setup.tsx` 的 mock 已支援）。
- [x] 各後台頁 `page.tsx` 的標題與說明（「系統設定」「API 與供應商設定」「集中管理即時航班…」等）也還是寫死繁中，
      2026-09-06 部署後在 `/en/admin/*` 看得到；一起搬進 `admin.json`（例如 `pages.<route>.title/description`）。
- [x] `usersPanel` 已經有一個物件（帳號面板的部分字串），新鍵併進去，不要另開同名的第二個。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-hotspot-places-panel components/admin-deployments-panel components/admin-users-panel
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

## Notes

### 做完之後（2026-09-06，claude-opus-5）

三個面板（地點資料 55 句、部署中心 51 句、會員 47 句）與六個後台頁的標題／說明都搬進 `admin.json`，
新增 `hotspotPlacesPanel`、`deploymentsPanel`、`pageHeaders` 三個群組，並把新鍵併進既有的 `usersPanel`。
73 個後台測試沒有改一行就通過，因為 zh-TW 的值逐字照抄。

四個值得記下來的點：

- **`pages` 這個群組名不能用。** `analytics.rankings.pages`（「熱門頁面」）已經存在，插入時的重複鍵檢查會擋下來；
  改名 `pageHeaders`。往 `admin.json` 加群組前先 grep 一次名字。
- **後台頁是 server component。** 六個 `page.tsx` 都是同步的 `export default function`，
  改成 `async` 後用 `getTranslations("admin.pageHeaders.<key>")`，比照早就這樣寫的 `admin/analytics/page.tsx`。
- **模組層常數換成 key stem 之後，helper 要收 translator。** `labels`／`statusLabels`／`entryLabel`／`auditLabel`
  都改成 key 集合，`StatusPill` 這種模組層元件自己呼叫 `useTranslations`；
  `Intl.DateTimeFormat("zh-TW")`／`NumberFormat("zh-TW")` 一併改成 `useMemo` 綁 `useLocale()`。
  eslint 的 `exhaustive-deps` 會要求把 `t` 和 `dateTime` 補進 `useMemo` 的相依陣列，`--max-warnings=0` 擋得很硬。
- **全形斜線也要搬。** 會員面板的「可用 ／ 保留」用的是 `／`，`check:i18n` 只掃漢字所以不會抱怨，
  但英文讀者會看到 `12 ／ 3`。這類全形標點跟著句子一起進 catalog。

剩下沒做、但同一份掃描看得到的：`admin-dashboard.tsx` 與 `admin-analytics-panel.tsx` 已經是翻好的；
`admin-hotspots-workspace.tsx` 的分頁標籤走 `hotspotTabs`，也已經好了。後台這條線到此收乾淨。
