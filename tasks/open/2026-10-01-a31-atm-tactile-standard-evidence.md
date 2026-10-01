---
id: 2026-10-01-a31-atm-tactile-standard-evidence
title: 修正 A31 舊查核把 ATM 5 鍵觸覺規定誤寫成電梯凸點規定
status: in-progress
priority: P2
area: docs
owner: codex-a31-evidence
claimed_at: 2026-10-01T05:16:26Z
created_at: 2026-10-01T05:16:24Z
completed_at:
branch: codex/sothatswhy-season2-batch01
depends_on: []
scope:
  - docs/videos/so-thats-why/topic-checks/s2-A26-A38.md
---

# 修正 A31 舊查核把 ATM 5 鍵觸覺規定誤寫成電梯凸點規定

## Why

2026-09-29 的 A31 題目查核把美國 ADA 707.6.2（ATM／fare machines）誤寫為數字5必須有單一凸點。2026-10-01 製作包重新開官方原文發現：707.6.2只要求觸覺可區分；單一凸點在電梯鍵盤407.4.7.2。沿用舊證據會讓旁白和字幕錯引法規。

## Definition of done

- [x] 舊報告的A31列改成正確條號、適用機器與限定，保留原查核日期，明記2026-10-01更正。
- [x] 舊包入口留新製作包路徑，1998 ETSI 不說成現行通用法律。

## Steps

- [x] claim精確報告scope，不改其他題的內容。
- [x] root重新讀 Access Board 官方707.6.2和407.4.7.2，與A31撰稿者的獨立發現一致。
- [x] 更正舊列；候選題的原facts_to_verify由母票更新，不超出本票scope。

## How to verify

重新讀 `https://www.access-board.gov/ada/#ada-707` 及 `#ada-407` 兩段原文；`git diff -- docs/videos/so-thats-why/topic-checks/s2-A26-A38.md` 只有A31列與更正註記；`npm run check:tasks`。

## Notes

- 2026-10-01：網頁原文直接可讀；只修正內容引用，沒有變更正式站、機器或合規狀態。原主張與新原文的差異也寫進A31獨立審稿。
