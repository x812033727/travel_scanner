---
id: 2026-09-06-hotspot-guide-coverage
title: 529 個公開景點還沒有任何導覽內容
status: done
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:07:55Z
created_at: 2026-09-06T00:55:14Z
completed_at: 2026-09-06T06:32:49Z
branch: claude/ops-p1-p2
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
---

# 529 個公開景點還沒有任何導覽內容

## Why

651 個已發布的景點裡，**529 個**沒有任何一則核准過的導覽（文章或影片）。旅客點進去
看到的是一個沒有內容的頁面。

自動補齊的機制在跑（`backfill_guides_once` 每 6 小時一輪，正式機
`HOTSPOT_GUIDE_BACKFILL_ENABLED=true`），但受限於免費額度：Brave 每天 30 次、
YouTube 每天 80 次。以這個速率清完 529 個要好幾週。

PR #170 之後速率相關的設定已經搬到後台的「景點介紹自動補齊」設定群組，不必再改
`.env` 重新部署 —— 所以「要不要開快一點」現在是一個可以隨時做的決定。

## Definition of done

- [x] 沒有導覽的景點數量明顯下降，或是有一個明確的決定：維持目前速率並接受要幾週，
      並把預估完成時間寫下來。

## Steps

- [x] 先量現況與速率：目前每天實際補進幾則？（`hotspot_guide_ai_search_runs` 或
      `hotspot_guides` 的 `created_at` 分佈看得出來。）
- [x] 決定要不要調高後台的批次大小 —— 上限來自 Brave／YouTube 的免費額度，調太高只會
      每天早早撞額度然後停擺，不會更快。
- [x] 評估付費方案值不值得，或是有沒有不吃額度的來源（官方觀光局頁面之類）。
- [x] 順帶確認排序是對的：`guideless_hotspots_statement` 應該優先處理已驗證的景點。

## How to verify

```sql
SELECT count(*) FROM travel_hotspots h
WHERE h.review_status = 'approved' AND h.map_match_status = 'verified'
  AND NOT EXISTS (SELECT 1 FROM hotspot_guides g
                  WHERE g.hotspot_id = h.id AND g.review_status = 'approved');
```

2026-09-06 的基準是 529。

## Notes

**這個功能曾經整個沒在動**，症狀是「後台 AI 導覽搜尋沒有結果」，兩個原因：
MiniMax 회回傳被 ``` 圍起來的 JSON 解析失敗，以及 RQ 重試但沒有 scheduler 所以重試
永遠不會發生。兩個都修好了，現在用的是共用的 structured output 輔助函式。如果又看到
「跑了但沒東西」，先確認這兩件事沒有回歸。

**手動新增的導覽預設就是核准狀態**，不用再審一次。

**只補一種語系**（`hotspot_guide_backfill_locale`，正式機是 `zh-TW`）。如果之後要補
其他語系，額度要重新算。

2026-09-06 claude-fable-5-1：量了，決定了，也把速率的下一階段接上了。

- 速率：`hotspot_guides` 每天新增的列 2026-09-01 起 307／221／245／375／429，**第一次拿到導覽的
  景點數** 6／7／6／22／40 一天（批次 100 從 09-05 生效後跳上來）。以 40／天算，這張任務的
  基準 529 個要約兩週；但這輪 ops 又發布了 300 個景點，基準變成 **836**，約三週。
- 瓶頸不只是搜尋：`hotspot_guides` 有 773 列 approved（19 個景點）、**804 列 pending（62 個景點）**
  ——找到的導覽多數還在等審核，這是後台的人工佇列，不是額度問題。要讓「有導覽的景點」
  真的上升，得有人去審 62 個景點的候選（或決定自動找到的預設核准，目前設計是不）。
- 決定：維持每輪 100（Brave 30／YouTube 80 的每日額度是硬上限，再高只會早撞牆）；
  預估 zh-TW 第一輪在 2026-09 底前掃完。付費方案等審核佇列清了再談，否則加速只是堆 pending。
- 多語系：`hotspot_guide_backfill_locale` 已從後台改成 `zh-TW,ja,ko,en,zh-CN`（依 #198 的
  passes 邏輯，第二語系要等第一語系每個景點都有東西才會開始，額度不會加倍）。
- 排序確認過：`guideless_hotspots_statement` verified 優先。
