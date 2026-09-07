---
id: 2026-09-07-intro-generate-trigger
title: 後台沒有「產生介紹」的按鈕，所以介紹佇列永遠是空的
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T00:39:02Z
created_at: 2026-09-07T00:38:30Z
completed_at: 2026-09-07T01:02:42Z
branch: claude/intro-generate-button
depends_on: []
scope:
  - apps/web/components/admin-hotspot-intro-generator.tsx
  - apps/web/components/admin-hotspot-intro-generator.test.tsx
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-hotspot-intros-panel.tsx
  - apps/web/messages/en/hotspotThemes.json
  - apps/web/messages/ja/hotspotThemes.json
  - apps/web/messages/ko/hotspotThemes.json
  - apps/web/messages/zh-TW/hotspotThemes.json
  - apps/web/messages/zh-CN/hotspotThemes.json
---

# 後台沒有「產生介紹」的按鈕，所以介紹佇列永遠是空的

## Why

介紹這條線在 production 上是**完整但摸不到的**：`POST /admin/hotspots/{id}/intros/generate`
在、RQ 佇列 `hotspot-intros` 在（worker 有訂閱）、每日額度守衛在、禁止捏造事實的正則在、
後台選供應商與模型的設定卡也在——**就是沒有任何一個地方會呼叫它**。

實際後果：線上 `hotspot_intros = 0`、`hotspot_intro_runs = 0`，而且會一直是 0。
管理員打開「景點 → 專門介紹」看到的是「待審 0・已核准 0」「沒有符合的介紹」，
外加三個篩選器和一顆重新整理鍵——一個進得去、但做不了事的畫面。
讀者那邊 `HotspotIntro` 對每一張卡都回 `null`，所以沒有人會看到任何一段介紹。

2026-09-07 上線後稽核發現。

## Definition of done

- [x] 後台可以為一個景點按下產生，草稿會出現在待審佇列。
- [x] 已核准的段落預設不動，要重寫必須明確勾選。
- [x] 執行中的狀態、寫了哪些語言、哪些被退回，畫面上看得到。

## Steps

- [x] `admin-hotspot-intro-generator.tsx`（新）：自帶觸發按鈕 + dialog，開啟前先讀
      `GET /admin/hotspots/{id}/intros` 的五語覆蓋，預設只勾「還沒有的語言」；
      送出後每 1.5 秒輪詢 `GET /admin/hotspots/intros/runs/{run_id}`，照 guides panel 的作法。
- [x] `admin-hotspots-panel.tsx`：每一列掛上去，就放在既有的主題編輯器下面。
- [x] `admin-hotspot-intros-panel.tsx`：空佇列時多一句話，說草稿是從哪裡來的。
- [x] `messages/*/hotspotThemes.json` ×5。
- [x] 測試五個。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

`/admin/hotspots`：找一個景點按「產生介紹」，確認預設只勾沒有的語言、run 狀態會更新、
完成後草稿出現在「專門介紹」分頁的待審佇列。

## Notes

- **預設只勾「還沒有的語言」**：補洞是常見情境，對一個已經寫好的語言再要一次，就是花一次
  模型呼叫把同一件事再說一遍。
- **「連已核准的也重寫」只在真的有已核准的語言時才出現**，而且預設不勾：重新產生不是丟掉
  別人審核決定的理由。
- **被退回的草稿會列出來**，不是默默消失——一個看起來很合理的假事實比缺一段話糟糕得多，
  編輯應該知道有一份被丟掉了、為什麼。
- 按鈕放在「景點審核」每一列，而不是介紹分頁：介紹分頁列的是「介紹」，沒有景點清單可選；
  景點列表本來就有搜尋與篩選，目標景點在那裡是明確的。空佇列的那句話就是為了指路。
