---
id: 2026-09-11-ux-dead-ends-and-empty-states
title: 六處死路與缺空狀態合集
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/shared-trip-view.tsx
  - apps/web/components/today-view.tsx
  - apps/web/components/community/home.tsx
  - apps/web/components/discovery/collections.tsx
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

- [ ] 上列六處各有一個說得出原因、給得出下一步的狀態。
- [ ] 每個停用的按鈕旁邊都看得到它為什麼被停用。

## Steps

- [ ] `shared-trip-view.tsx`：區分 404（連結失效）與其他錯誤（可重試），失敗時保留後續 CTA。
- [ ] `today-view.tsx`：同樣區分，並加重試與回 `/trips` 的連結。
- [ ] `search-experience.tsx`：篩選列加「清除全部」。
- [ ] `itinerary-timeline.tsx`：加空狀態。
- [ ] `community/home.tsx`：未登入時加一句說明。
- [ ] `search-workbench.tsx`：零推薦時給訊息。
- [ ] 停用按鈕旁渲染 `unavailableHelp`。

## How to verify

```bash
cd apps/web && npm run test:web
```

## Notes

- 第 4、6 兩項分別與 `2026-09-11-itinerary-timeline-hardcoded-zh-tw`、`2026-09-11-wizard-crash-when-all-criteria-any` 同檔。那兩張的 scope 各自佔住了 `itinerary-timeline.tsx` 與 `search-workbench.tsx`，本任務的 scope 刻意不含這兩個檔——請在做那兩張時順手處理，或等它們完成後再開一張補這兩項。
