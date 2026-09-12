---
id: 2026-09-12-admin-section-filter-keeps-topic
title: 後台文章清單：切換專區沒有清掉主題篩選
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-12T16:57:07Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-guides-list.tsx
---

# 後台文章清單：切換專區沒有清掉主題篩選

## Why

`/admin/guides` 的「專區」下拉在 PR #438 加入。它的 onChange 會重設 `kind` 與 `page`，
但不動 `topic`——而主題只屬於一個專區。

管理者停在 `?topic=transport`（旅遊文章、篩交通）再把專區切成「生活分享」，網址變成
`section=life&topic=transport`。`admin_service._resolve_topics` 用 `guide_topic_section_mismatch`
拒絕跨專區的主題，所以沒有任何 life 文章能帶 transport，API 必定回 total=0，畫面顯示
「沒有文章」。主題下拉是用 `/admin/guides/topics?locale=…` 取的、沒帶 `section`（雖然這個
PR 已經替該端點加了 section 參數），所以兩套詞彙都列在裡面，交通仍然顯示為選中。

同樣的不對稱也讓 `section=travel` 配上 `kind=life`，由 `list_articles` 那個刻意的空結果
早退處理掉。

這張票被列為 P3 而不是直接修，是因為「該不該重設」有正反兩面：重設掉使用者剛設的篩選
本身也會惹人厭，而且如果改成依專區重新抓主題清單，交通那個選項會消失、下拉會退回顯示
「全部主題」，但網址上的篩選還在——那是更糟的騙人介面。這個 admin 介面其他篩選（狀態、
目的地、關鍵字）換條件時也都不互相清除，所以要改就該一起想清楚規則，而不是只補這一對。

## Definition of done

- [ ] 切換專區後，畫面上顯示的篩選條件與實際送出的查詢一致——不會出現一個永遠查不到
      東西、而使用者看不出原因的組合。
- [ ] 決定寫進註解：這個 admin 的多篩選互動規則是什麼（互不清除／依賴關係才清除）。

## Steps

- [ ] 決定規則：切專區時清掉 `topic`，或把主題下拉改成依 `section` 取、且同步清掉不合的值。
- [ ] 一併看 `kind` 下拉：它現在不分專區列出全部三種 kind。
- [ ] 補 `admin-guides-list.test.tsx` 的案例（現有 fixture 只有一個旅遊主題，沒有專區篩選覆蓋）。

## How to verify

`npm run test:web`，並在後台實際操作：`/zh-TW/admin/guides?topic=transport` → 專區切「生活分享」
→ 畫面顯示的主題與結果不應自相矛盾。

## Notes

來源：PR #438 合併前的多角度審查，三個驗證視角裡兩個認定成立、第三個（影響面）以
「空結果是正確的、陳舊篩選就顯示在旁邊、一鍵可復原」為由反對。程式面事實三方一致，
分歧只在值不值得改，所以留成票而不是直接動手。

編輯器那側已經是專區感知的：`admin-guides-panel.tsx` 會用 `topic.section ?? "travel"` 過濾
主題勾選框，並在 kind 跨專區時清掉主題。沒跟上的是清單的篩選列。
