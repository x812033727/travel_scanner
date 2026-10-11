---
id: 2026-10-11-video-held-retry-status
title: Show retained failure and concurrent STOP beside pending video retry
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-11T14:18:54Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-video-held-retry-status.md
  - apps/api/app/video_reviews/producer_state.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_producer_state.py
  - apps/web/components/admin-video-production-state.tsx
  - apps/web/components/admin-video-production-state.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

## Why

保留並恢復原未共享票 2026-10-05-video-held-retry-status；不要另開第二張 generic reconciliation 或同義顯示票。原稿是 news-recovery worktree 的 scope 外 untracked file：C:/Users/x8120/.codex/worktrees/6f71/travel_scanㄐ/tasks/open/2026-10-05-video-held-retry-status.md。它是影片狀態顯示問題，不屬 news source recovery，也不接管任何影片生產。

2026-10-11 read-only 對 current frozen main 1f183e4d1f3bb493b5412ca242f2cbb98da4f9bf 再驗：producer_state.py 的 WorkerView 只有 state/tidied_at；blocked/dropped 在讀 project/global STOP 前先 return。admin_service.py 把單一 worker_state 回傳，review-card 的 PublishPill 只把此 state 交给 VideoProductionState，元件只顯示一個狀態。admin-video-reviews.tsx 的 RetryVideo 只用 pending 判斷並顯示 retryVideoPending；繁中仍為「已提出重試，工人下一輪會接手。」。現有 test 也只斷言這段文案。

較新的 project STOP/shared lease、policy-hold guard 已實作：原 native-video-project-stop-and-producer-exclusion、the-worker-passes-over-a-video、retain-video-policy-holds-without-new 與 look-clips-music-and-speech-commands 都是 main done。它們讓 client/worker 在 STOP 下不承認/執行 retry，並保留 failed receipts、source/owner guards；沒有新增 blocked/dropped 的 concurrent STOP readback 或修正 pending 文案。因此那些 done 票不取代本票的顯示驗收。長時間 lease 顯示是另一個 optional 功能，不把它混入本票。

## Definition of done

- [ ] 原 blocked/dropped state 與原 failure/reason 保持，另顯示 independently observed project/global STOP。不能只是把 stopped 優先次序換到 failure 前方；那會遮掉故障。
- [ ] 使用 bounded、read-only、安全路徑解析的 additive/backward-compatible API contract；明確分辨「觀察到 STOP」與「worker mount/producer information 不可用」。缺 API 欄位或不可用不能推成無 hold、running、retry 已開始。
- [ ] current detail/list/browse 真正透過 admin_service/schema 回傳附加 hold evidence，review-card/production-state 真正顯示 failure 加 hold；retained tidied_at、Shorts 既有省略和旧 API 行為保持。
- [ ] pending retry 的提示只表達 request 已記錄、尚待處理；有 STOP 或未知 producer 時不承諾下一輪必開始。一般沒有 hold 的 pending 也不能被當 process heartbeat 或 completed production。
- [ ] 此顯示修補不 acknowledge/reset retry IDs、不移除/建立 STOP、不取 lease、不改 source/approval/media/budget、不 dispatch stage/model、不啟動 worker，原 client/flow STOP guards不變。
- [ ] 五個 admin message catalogs 的 key/ICU 保持一致；video 四語產線政策不影響 admin 的五語 UI catalog。
- [ ] source reviewer 與獨立 duration reviewer 分工；本 scope 裡 admin_service.py、schemas.py、review-card.tsx、reviews.test.tsx 與五 catalog 是 current-main duration-bound 路徑，變更只可由獨立 review 增量更新 docs/videos/long-form/review.md/json，不複製舊 receipt 或宣稱未審查 PASS。

## Steps

- [ ] 開共享票前先查當時 current main、所有 open tasks/PR 與 active claims。此 snapshot main 的同 ID absent，也沒有找到相同 concurrent STOP/retry copy 的 open 票；如果已有 owner/successor，用原 ID 或連回同一張，不另生重複票。
- [ ] 保全 6f71 原 untracked body/metadata/hash；不要改該 news owner 的 worktree、claim 或原 dirty files。以新共享 ID 恢復原稿，保留原始 ID 作追溯，這輪只恢復待辦，不接管 implementation。
- [ ] 要實作時再用具識別性的 owner claim 核對本次 14 產品/測試/catalog 檔與 2 receipt 檔的 overlap；真實 caller 已補在 scope，而不只改孤立 production-state 元件。
- [ ] 用 offline canonical workspace/API/UI fixtures 對 blocked/dropped + project/global STOP、無 STOP、missing/unreadable worker state、未採用 project、旧 API、tidied video/Shorts 做 read-only contract 測試。

## How to verify

API fixture 使用 auto.json 的 blocked/dropped state 與有/無 project/global STOP，同時讀 detail/list/browse，原 failure 與独立 hold 一起可見；對比原 auto.json/STOP/retry bytes 無寫入。UI fixture 測 pending retry under hold、pending without hold、unknown/old API；既有生产 state 的 labels/helps 保持。跑 focused test_video_producer_state、production-state/reviews UI tests，check:i18n、web typecheck、long-form check/review、check:tasks 和受影響 required CI。只使用 fake/local fixture，不呼叫 production/video provider。

## Notes

重新驗證依據：current main producer_state.py 的 blocked/dropped early return；schemas.py 的單 WorkerState；admin_service.py worker_view 三處呼叫和 summary worker_state；admin-video-review-card.tsx:214 只傳 state；admin-video-production-state.tsx:13 接受一個 state；admin-video-reviews.tsx:53 用 pending 選文案；zh-TW/admin.json:2194 保留下一輪承諾；client.mjs:356/396 的 STOP prevents this owner retry 與 automation.test 的 policy retries respect project STOP 證明執行 guard 已在主線，不能混成待修 guard bug。

核對只是 source/metadata read-only audit，沒有測正式 mount/活躍 process 或修改正式站；本票沒有把 historical Skills/SEC prompt repair 當 production 完成。2026-10-05-video-writer-pending-transport-reason 是別的 durable transport reason，不能用本票代替。

原始保留分支／核對HEAD：
- `codex/news-recovery-20261010@1b7be83e6cc65a308e2c21b785c7e37c8ac966f7`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
