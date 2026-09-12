---
id: 2026-09-11-ux-dead-ends-and-empty-states
title: 六處死路與缺空狀態合集
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T19:02:40Z
created_at: 2026-09-11T03:21:17Z
completed_at: 2026-09-11T19:24:51Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/shared-trip-view.tsx
  - apps/web/components/shared-trip-view.test.tsx
  - apps/web/components/today-view.tsx
  - apps/web/components/today-view.test.tsx
  - apps/web/components/community/home.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
  - apps/web/messages/en/community.json
  - apps/web/messages/ja/community.json
  - apps/web/messages/ko/community.json
  - apps/web/messages/zh-CN/community.json
  - apps/web/messages/zh-TW/community.json
---

# 六處死路與缺空狀態合集

## Why

散落各處、單獨都不大，但都是同一種病：使用者走到某個狀態，畫面沒有解釋、也沒有下一步。

1. **`/share/[token]` 所有失敗都說「連結不存在」。** `shared-trip-view.tsx:252-255` 對 500、網路瞬斷、真的被撤銷的 token 一視同仁顯示 `t("shareNotFound")`，而且提前 return，連 `:264-280` 的後續 CTA 都一起消失。收到朋友連結的人沒有重試，也不知道是自己網路的問題還是連結真的失效了。
2. **當日檢視把所有錯誤標成「離線」。** `today-view.tsx:52-56` 的 `.catch(() => setOffline(true))`，401、404、500 全部顯示 `t("unavailable")`（`:58-62`），沒有重試，也沒有回 `/trips` 的路。
3. **篩選可以把結果清空卻沒有清除鈕。** `search-experience.tsx:2003-2010` 會顯示 `emptyCategory`，但 `:1698-1844` 的篩選列沒有任何重置。使用者勾了幾個條件、畫面空了，不知道要取消哪一個。
4. **行程時間軸沒有空狀態。** `itinerary-timeline.tsx:87-88` 直接回傳空的 `<div className="space-y-6">`。剛建好還沒排東西的行程分享出去，對方看到標題、一片空白、然後一個 CTA。
5. **`/my` 對未登入者沒有任何說明。** `community/home.tsx:37-46` 渲染一排連結，`:44` 附一個沒頭沒尾的「登入」，全頁沒有一句話說明這裡需要登入。
6. **精靈零推薦時畫面毫無變化。** `search-workbench.tsx:200` 用 `recommendations.length > 0` 包住整段。把日期壓窄、最短天數拉高，`places/router.py:484-485` 對每個 profile 都算不出 `best` → 回傳 `recommendations: []` → 轉圈停了，什麼都沒出現，沒有任何訊息。

另外：**停用按鈕不說明原因。** `trip-editor.tsx:1830`（桌面 AI 助手）與 `:1974`（手機 dock）是 `disabled={busy("ai") || aiCharge.status !== "ready"}`，但 `aiCharge.unavailableHelp`（`usage-catalog-provider.tsx:80`）從來沒有渲染在旁邊。`search-experience.tsx:1371-1377` 的開始鈕在 `tripBlocked` 時停用，`:1409-1411` 的說明只解釋扣次狀態，不解釋為什麼被擋。

## Definition of done

- [x] 上列六處各有一個說得出原因、給得出下一步的狀態。
- [x] 每個停用的按鈕旁邊都看得到它為什麼被停用。

## Steps

- [x] `shared-trip-view.tsx`：區分 404（連結失效）與其他錯誤（可重試），失敗時保留後續 CTA。
- [x] `today-view.tsx`：同樣區分，並加重試與回 `/trips` 的連結。
- [x] `search-experience.tsx`：篩選列加「清除全部」。
- [x] `itinerary-timeline.tsx`：加空狀態。
- [x] `community/home.tsx`：未登入時加一句說明。
- [x] `search-workbench.tsx`：零推薦時給訊息。
- [x] 停用按鈕旁渲染 `unavailableHelp`。

## How to verify

```bash
cd apps/web && npm run test:web
```

## Notes

- 第 4、6 兩項分別與 `2026-09-11-itinerary-timeline-hardcoded-zh-tw`、`2026-09-11-wizard-crash-when-all-criteria-any` 同檔。那兩張的 scope 各自佔住了 `itinerary-timeline.tsx` 與 `search-workbench.tsx`，本任務的 scope 刻意不含這兩個檔——請在做那兩張時順手處理，或等它們完成後再開一張補這兩項。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

`2026-09-09-frontend-flow-discovery-web`（codex-discovery-flow-web）的 scope 擋著。claim 是 2026-09-09T04:37，已逾 62 小時（board 標為 stale），遠端分支 `codex/frontend-explore-flow` 已不存在，工作已合併進 main（`a899437 feat: streamline Explore → Saved → My trips (#374)`，正是最後一次動到 `discovery/collections.tsx` 的 commit）。

## 完成紀錄（claude-opus-5, 2026-09-11）

六處加上停用按鈕那一項，逐項的實際狀況：

| # | 內容 | 結果 |
| --- | --- | --- |
| 1 | `/share/[token]` 所有失敗都說「連結不存在」 | 修了。404／410 → 「連結已失效，向對方要新的」；其他 → 「打不開」＋重試鈕。兩種情況都保留回首頁的連結（原本會提前 return，把後續 CTA 一起帶走） |
| 2 | 當日檢視把所有錯誤標成離線 | 修了。分成 `offline`（請求根本沒送達）與 `error`（伺服器回了但不是 200），各有自己的句子，兩者都有重試 |
| 3 | 篩選可以清空結果卻沒有清除鈕 | 修了。八個篩選任一非預設時，篩選列右側出現「清除全部篩選」 |
| 4 | 行程時間軸沒有空狀態 | **先前已修**（`2026-09-11-itinerary-timeline-hardcoded-zh-tw`，本分支 commit 17cd7b2） |
| 5 | `/my` 對未登入者沒有說明 | 修了。未登入時在連結列上方加一段說明：這些東西屬於你的帳號，但下面的外觀與語言設定不用登入 |
| 6 | 精靈零推薦時畫面毫無變化 | **先前已修**（`4641498`，就是那張精靈崩潰任務） |
| — | 停用按鈕不說明原因 | 規劃器修了；搜尋頁**本來就有** |

### 搜尋頁那一項，原描述不準確

任務說「`search-experience.tsx` 的開始鈕在 `tripBlocked` 時停用，說明只解釋扣次狀態，不解釋為什麼被擋」。實際上 `:1369`、`:1397`、`:1418` 針對 `tripIssues.origin`、`.destination`、`.dates` 三種情況各有自己的說明區塊，而 `tripBlocked` 就是由這三個組成的。所以那裡沒有問題，沒有動它。

規劃器則是真的：兩顆 AI 按鈕（桌面 `:1835`、手機 dock `:1979`）在 `aiCharge.status !== "ready"` 時變灰，而 `usage-catalog-provider` 早就備好了 `unavailableHelp` 這句話，從來沒有被渲染。現在在日期列上方顯示一次——這是頁面層級的狀態，不是每顆按鈕各自的。

### 驗證

四個新案例（`shared-trip-view.test.tsx` 兩個、`today-view.test.tsx` 兩個）：500 給重試且重試真的會再打一次 API、404 不給重試、當日檢視分得出兩種失敗、離線那條的重試也會再送。

把兩個判斷式分別退化成「一律 gone」與「一律 offline」之後，對應的兩條變紅；復原後 16 passed，整套 230 files / 2335 tests 全過。

### 一個 lint 學到的東西

第一版把 `setError(undefined)` 放在 effect 開頭重置狀態，eslint 擋下來：「Calling setState synchronously within an effect can trigger cascading renders」。改成在重試按鈕的 handler 裡重置——反正 `attempt` 只會從那裡改變，語意一樣而且沒有多餘的 render。
