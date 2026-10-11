---
id: 2026-10-11-restore-frontend-flow-polish
title: 補回手機旅程繼續入口與收藏篩選文案改善
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-11T13:46:05Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-frontend-flow-polish.md
  - apps/web/components/account-list.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/components/account-list-i18n.test.tsx
  - apps/web/components/discovery/collections.tsx
  - apps/web/components/discovery/discovery.test.tsx
  - apps/web/components/discovery/frontend-flow.test.tsx
  - apps/web/lib/discovery-copy.ts
  - apps/web/lib/frontend-flow-copy.ts
---

## Why

前端 Explore → Saved → My trips 原實作及發布已完成，但兩個非阻擋 UX 改善只存在歷史分支的 post-deploy-polish 票，未保留在共享 queue。對照 frozen main後，兩項仍存在：手機 My trips 的「繼續」文字被隱藏，以及 Collections 同時提供 merchant／restaurant 篩選卻使用同一個名稱。

本票只處理這兩項，不重做已完成發布或已修復的 Escape 調查，不改收藏／旅程 API、enum或planner行為。

## Done when

- [ ] My trips 在 390px 等手機寬度有可見、清楚且可觸達的「繼續」入口，五語完整；不遮住旅程標題、狀態、More或刪除動作。
- [ ] Collections 的 merchant 與 restaurant 有不同且符合既有類型意義的五語 label，原 enum、URL filter與service行為保持正確。
- [ ] 有相應的元件回歸與桌機／手機文案／layout檢查，keyboard操作與accessible names通過。
- [ ] scoped PR 通過相關檢查並納入 main；本票不得以完成小型文案修正宣稱新增正式站部署。

## Steps

- [ ] 讀 task-board 與 web-i18n-e2e skill，確認這些窄 scope沒有其他active claim後認領。
- [ ] 重新讀現有 AccountList、Collections 與文案來源，確認主分支是否在本票建立後已更動，保留目前既有features／enum。
- [ ] 為手機「繼續」入口選可容納五語且不遮擋其他動作的布局，更新必要的元件與回歸。
- [ ] 根據既有 merchant／restaurant類型給出不同五語 label，覆核篩選選項、URL與keyboard結果。
- [ ] 執行scoped檢查、review與PR；若需正式站部署，走既有release流程獨立記錄。

## Verification

以對應元件測試確認 My trips 的繼續動作仍連到原旅程、more/delete互動與 keyboard正常；Collections各類型保持既有 URL filter values。檢查五語與390px／桌機呈現，跑受影響的 Vitest、web lint、i18n、typecheck、`npm run check:tasks` 與 `git diff --check`。測試保留原 Escape、focus trap、body scroll與no-commit斷言，不新增generic flake investigation。

## Notes

- 建票日期：2026-10-11。原分支：`codex/frontend-flow-release-record-a899437a`；保留 HEAD：`2cfb1acab8f4f9bad565b54fa194bd5a3cbd90d4`。原缺件票 `2026-09-09-frontend-flow-post-deploy-polish` 只存在該歷史分支，本票補回其兩個實際UX項目。
- 核對 main：`73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b`；證據：`C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/locale-audit.json`。
- 具體現況：`apps/web/components/account-list.tsx:436` 的 `flowCopy.continue` 是 `className="hidden text-sm font-semibold text-[var(--teal)] sm:inline"`，手機隱藏；`apps/web/components/discovery/collections.tsx:109` 同時列 merchant／restaurant，但 restaurant映射 `c.kinds.merchant`。`apps/web/lib/discovery-copy.ts:17` 的zh-TW merchant名稱為「特色店家」。行號只對上述frozen SHA有效。
- 窄修改範圍應從 AccountList、Collections、實際五語copy來源與相應tests選取；`discovery-copy.ts` 是本次確認的文案來源，不因舊票scope列frontend-flow-copy就跳過它。root會依當前claim再分配scope。
- [#374](https://github.com/x812033727/travel_scanner/pull/374) 已 merged `a899437aaf2f60c7affe2e944d49d62216537c90` 並有完整發布收據；原4個frontend-flow tasks均main done。Discovery card handoff已由 [#378](https://github.com/x812033727/travel_scanner/pull/378)與main done task取代，這些不重開。
- 原Escape失效調查已有確定rootcause與回歸：[PR #493](https://github.com/x812033727/travel_scanner/pull/493) merged `46298e2863e9c2c4d6776e9d58a821be683a4b32`，修復 default-lane DOM commit與passive effect間隔，五個確定性回歸與四輪CI／本機全套通過。main `2026-09-11-modal-escape-flake-under-load` 已done；不要把這項再列未完或放寬斷言。

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。
