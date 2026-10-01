---
id: 2026-10-01-sothatswhy-season2-batch01
title: 原來如此第二季首批：B26 S26 T26 A31 四集製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch01
claimed_at: 2026-10-01T05:10:09Z
created_at: 2026-10-01T05:10:08Z
completed_at: 2026-10-01T05:39:20Z
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B26.md
  - docs/videos/so-thats-why/season2/S26.md
  - docs/videos/so-thats-why/season2/T26.md
  - docs/videos/so-thats-why/season2/A31.md
  - docs/videos/so-thats-why/season2/reviews/batch01/
  - docs/videos/so-thats-why/season2/batch01-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季首批：B26 S26 T26 A31 四集製作包與獨立審稿

## Why

第二季有100個已做題目查核的候選題，尚未變成第一季格式的逐集製作包。先從四軸各做一題 B26、S26、T26、A31，建立可交接的格式、今天的來源證據、兩支 Shorts 及五語包裝；A26 與既有 AI 上下文視窗影片重疊，本批選 A31。

## Definition of done

- [x] 四份完整包：今天來源表、8分鐘章節大綱、前提／備註、兩支180–220中文單位 Shorts、五語長短片包裝、畫面與不做事項。
- [x] 每包由非撰稿者查核／聽眾審稿，修正已套用；review 報告與 JSON 收據綁當前包 SHA-256，沒有未處理的入片主張。
- [x] `batch01-packaging.json` 可從四包生成且與原文一致；`validate.mjs` 檢查id、五語、後台上限、Shorts估時、來源入口及審稿雜湊。
- [x] 狀態標清只有文字包完成，媒體／平台／站主聽片尚未驗收；已知舊來源錯誤有獨立票修正。

## Steps

- [x] 看碰撞、claim；按四軸選首批，讀技能與第一季格式。
- [x] 不同撰稿者寫四包；新事實與今日來源逐條確認。
- [x] 換代理查核／聽眾文字審稿，處理新發現，再產雜湊收據。
- [x] 生成五語包裝索引、跑機械檢查；提交以草稿 PR 交接（依賴#1073）。

## How to verify

`node docs/videos/so-thats-why/season2/validate.mjs`、`npm run check:tasks`、`git diff --check`。每個採用主張有今日讀到的來源；不同作者／查核者，收據指向的檔案 SHA-256 相符。沒有成片，不跑或宣稱媒體 lint／QA已驗收。

## Notes

- 2026-10-01 驗證：100個原候選id、4包、8Shorts、60組五語、後台欄位上限與480秒章長、所有收據雜湊通過；隔離暫存副本的正文改動、審稿報告改動、包裝漂移三種測試均正確拒絕。初次Node子程序測試未正常回報，改PowerShell直接執行並讀exit code後全部通過。
- 審稿分工：B26 write_b26→root，S26 root→write_b26，T26 write_t26→write_a31，A31 write_a31→write_t26；初輪圖像prompt、日文等價、來源歸屬FIX皆有複審閉合。沒有真人音檔人聽或生成圖的視覺QA。

- 2026-10-01 user「開始」後接續；基於草稿 PR #1073 的票務提交，不自動合併或進正式站。
- 母票 `2026-10-01-sothatswhy-season2-production-packages` 只改索引／候選題入口；本票持有四包與收據。
- A31 原報告把 ATM 的5鍵觸覺可區分與電梯的單一凸點混用；獨立修正票 `2026-10-01-a31-atm-tactile-standard-evidence` 承接舊報告。
