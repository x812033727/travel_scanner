---
id: 2026-10-13-allow-audited-source-refresh-after-legacy
title: Allow audited source refresh after legacy navigation repair
status: in-progress
priority: P2
area: api
owner: codex-news-hourly-backlog
claimed_at: 2026-10-13T07:09:32Z
created_at: 2026-10-13T06:34:59Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on:
  - 2026-10-10-add-audited-repair-for-legacy-navigation
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/tests/test_news_review_actions.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages/en.json
  - apps/web/lib/admin-news-messages/ja.json
  - apps/web/lib/admin-news-messages/ko.json
  - apps/web/lib/admin-news-messages/zh-CN.json
  - apps/web/lib/admin-news-messages/zh-TW.json
---

# Allow audited source refresh after legacy navigation repair

## Why

Kalshi 候選 `cf07bd04-7f3f-4b0d-89b9-37a715f1ecc9` 的五語 Guide 已修正並通過新事實判斷，但仍有一筆舊版 CoinDesk `/markets` 導覽頁證據 `source_became_unreadable`，另有正文與作者頁 `source_content_changed`。既有 `2026-10-10-add-audited-repair-for-legacy-navigation` 工具能稽核修復導覽頁，然而修復後標記 `news_navigation_evidence_repaired`；目前 `refresh_candidate_evidence` 只接受 `news_evidence_changed`，形成已修復的候選不能走正常來源刷新與重新查核的斷層。不能讓這個斷層變成略過來源、AI judge 或直接發布的理由。

## Definition of done

- [ ] 已稽核修復導覽證據、且保留的真實正文來源可原生讀取的候選，可以在後台明確選擇刷新**保留的真實來源**，留下人工原因／稽核並重新通過既有事實、五語及最後一關查核；未通過者仍保留待審。
- [ ] 未修復導覽列、HTTP 非 200／殼頁、正文或 claim ledger 仍依賴被移除證據、錯誤狀態碼及並行競態都被拒絕；不放寬原有修復與發布閘。

## Steps

- [ ] 先查 `service.py` 的導覽修復原因碼、`refresh_candidate_evidence` 前置條件與現有後台按鈕；確認 `/markets` 的原生抓取診斷。當下 Kalshi URL 不可讀，不能僅為通過測試而降低 HTTP 200 條件。
- [x] 實作修復後可審計的來源刷新路徑及後台文案／狀態，保留單候選、人工原因、原始快照與 run／稽核鏈。
- [x] 補成功、來源不可讀、證據仍被引用、競態與反覆刷新本地測試；刷新動態側欄導致再次 `source_content_changed` 另由既有解析修復票處理，正式站關卡未驗。

## How to verify

執行所涉 API 單元測試與 `apps/web/components/admin-news-workspace.test.tsx`，再跑 `npm run check:tasks`。在後台用已修復的測試候選驗證「人工原因 → 真實正文來源刷新 → 原有查核 → 候選終態」的持久 readback；失敗樣本需維持保留狀態且有明確錯誤碼。正式站 Kalshi 的 `/markets` 現仍不可讀，部署前不得將此票的本地測試稱作該候選已解決。

## Notes

2026-10-13 現場：Kalshi 正文、作者頁變動，舊 `/markets` 導覽列不可讀；修復工具要求原生 HTTP 200 全文及沒有任何已保存 Guide／五語／claim ledger 引用，目前不符合，不可盲按全來源刷新。Meta 眼鏡另有 `2026-10-11-add-audited-correction-for-obsolete-held` 與 `2026-10-11-recover-two-verge-held-stories-after` 兩票，不把它們併入本票。此票 `service.py` scope 與未認領的 claim ledger 工作可能重疊，認領前須依 task-board 流程查其他 worktree、遠端枝與 PR。

唯讀程式追查：`service.py` 導覽修復寫入 `news_navigation_evidence_repaired`，但 `refresh_candidate_evidence` 只接受 `news_evidence_changed`；後台狀態分類也把前者落入一般修文章流程。實作時應驗同一候選正式修復稽核、保留證據 ID／hash 未漂移、沒有執行中 job／run，以及五語稿與 claim ledger 未引用被刪的導覽 URL；成功後才沿既有原子化刷新與 `_queue_reverify` 路徑。不應以新入口繞過 `/markets` 原生 HTTP 200 的前置條件。

2026-10-13 本機實作：後端僅對 `manual_review/news_navigation_evidence_repaired` 開放既有刷新路徑，先以完整 held-state NOWAIT 快照核對同候選真人修補稽核、保留證據列與 hash、五語未發布草稿、claim ledger、沒有 live job／running run，並拒絕已移除網址再次被引用。來源刷新失敗完整 rollback；成功稽核連到修補稽核 ID 並留下刷新前後證據，仍經原本的五語 `_queue_reverify`。後台五語狀態文案只提供刷新或退件。未部署、未在正式站套用，也未對 Kalshi 候選執行；`/markets` 不可讀時，前置導覽修補仍會拒絕。來源頁動態側欄的長期穩定性需另依既有來源解析工作驗證，不能以這次本機成功案例宣稱已解決。

本機檢查：`tests/test_news_review_actions.py` 62 passed；新增候選列首把鎖 NOWAIT 衝突回傳 409 的測試；`admin-news-workspace.test.tsx` 67 passed；所涉 API Ruff、mypy、Web lint、typecheck、`check:i18n`、`check:tasks` 通過。PR／正式站結果待獨立驗證。
