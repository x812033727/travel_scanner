---
id: 2026-09-06-chosen-state-and-menu-values
title: 選中的國家只靠底色表示，選單裡的外觀與語言看不出目前設定
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T23:39:29Z
created_at: 2026-09-06T23:39:29Z
completed_at: 2026-09-07T00:13:09Z
branch: claude/ux-chips-and-menu
depends_on: []
scope:
  - apps/web/components/search-workbench.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 選中的國家只靠底色表示，選單裡的外觀與語言看不出目前設定

## Why

長輩情境稽核在規劃精靈的「目的地」那一步量到：`日本` 一進來就是選中的
（`aria-pressed="true"`，城市下拉裡有十個選項），但選中與沒選中的差別只有底色與邊框
顏色——沒有勾、沒有字、字重也一樣。一個以為「還沒選」的人按下去，日本被取消，城市
下拉瞬間只剩「我不介意」，畫面上沒有任何一句話說發生了什麼；再往下走，推薦的城市
從東京變成高雄，而中間沒有任何一頁會複述目的地。

同一輪也記到：手機選單裡的「外觀主題」與「語言」只有圖示，永遠不顯示目前是哪一個；
選了特大字之後，選單第一次需要捲動，而「語言」被推到畫面外。

## Definition of done

- [x] 選中的國家／偏好／住宿膠囊除了底色，還有一個勾。
- [x] 沒選任何國家時，城市下拉底下說明為什麼只剩「我不介意」。
- [x] 選單裡「外觀主題」「語言」各自顯示目前的值（跟文字大小一樣）。
- [x] 顯示設定移到選單最上面——看不清楚字的人最先需要的是這一區。

## Notes

WCAG 1.4.1：狀態不能只用顏色表示。這裡原本的邊框對比是 6.33:1，過得了 1.4.11 的
非文字對比，但那是「看得到有個框」，不是「看得出來它被選中」。
