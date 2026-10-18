---
id: 2026-10-11-reconcile-nami-seoul-localization
title: 保留並恢復 Nami／首爾翻譯候選與來源 HOLD
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T13:46:05Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-nami-seoul-localization.md
  - apps/api/app/guides/content/nami-island-petite-france-day-trip.json
  - apps/api/app/guides/content/seoul-where-to-stay.json
  - apps/web/public/guides/nami-island-petite-france-day-trip
  - apps/web/public/guides/seoul-where-to-stay
  - docs/article-localization/reconciliations/nami-seoul
---

## Why

原三篇 Korea localization 已把 Jeju 完成並另行合併／發布，剩下 Nami 和 Seoul。這兩篇各四語文件與八份 localized SVG 存於有未提交修改的作者 worktree，main 仍只有 zh-TW。原任務在本機已縮為兩篇並標示 HOLD，共享看板缺少這個剩餘交接。

本票保留完整候選與來源限制，恢復可繼續的 queue。不能把有實際缺件的工作當成純完成收據清掉，也不能把未審核候選當成已完成翻譯。

## Done when

- [ ] 17 個現存變更全部保留並有路徑／hash／狀態清單；在核對 owner、active session、原 scope 前，不改動原 checkout 或刪檔。
- [ ] Nami 的來源修正及未滿 36 個月免費條件取得精確來源查證與獨立核准；Gapyeong 公車時刻圖的未解項目有實際圖像覆核證據。
- [ ] Seoul T-Luggage 的服務站、尺寸與機場 terminal 提案取得允許的獨立覆核，先前未核准 finding 有明確處理結果。
- [ ] 每篇四語候選與四語 SVG 重新綁定核准後的來源版本，完整文字／數字／條件／credit／link／視覺審稿通過且綁最終 hash。
- [ ] Nami／Seoul 的 scoped 內容 PR 通過相關檢查並納入 main；正式來源發布、target publication 與 public QA 若未完成，以獨立 release 票追蹤。Jeju 不重新翻譯、審稿或發布。

## Steps

- [ ] 讀 article-localization／task-board skill，確認原作者與 session 狀態；新票只認領 Nami／Seoul pack 與其 asset directories，保留原 worktree，避免覆蓋平行工作。
- [ ] 先核對保留清單與雜湊，整理可復用候選；保留所有初稿、審稿 finding、HOLD、拒絕與修正嘗試。
- [ ] Nami：查證 rail-bike 13:30 班次、當日取消扣 50%、Namisum 未滿 36 個月且家長陪同／證明／一般渡輪條件，與 Gapyeong 官方公車時刻圖。這些是待覆核候選主張，不能直接以舊查證日期宣稱當前有效。
- [ ] 重新對齊目前 main 的 Nami source，保留 #1272 新插入的楓葉文章互連；不得直接以舊整個 pack 覆蓋新 main。
- [ ] Seoul：定位 T-Luggage source-correction proposal v2 與官方來源欄位，按允許的流程取得真正獨立覆核；HOLD 未解前不套來源 proposal、開發布 PR 或進行正式站寫入。
- [ ] 來源核准後重綁八份 target documents 與八 SVG，完整獨立審稿、檢查與 scoped PR；另追蹤正式發布 gate。

## Verification

對照保存的 17 檔 manifest/hash；對來源與候選分別做 JSON scalar diff，檢查新 main 的互連與 metadata 保留。依 skill 驗證 GuideDocument、來源版本／hash、每語 artifact hash、所有數值條件、credit、same-language links、SVG 原尺寸與手機 scroll render。執行 scoped pack lint、content-pack／links／artifact integrity 測試、`npm run check:tasks` 及 `git diff --check`。核准與結案收據需保留獨立 reviewer 身份、scope與真正完成 stage。

## Notes

- 建票日期：2026-10-11。原分支：`codex/article-localization-batch-011-korea`；保留 HEAD：`1fbd57ac8845c8d4f465be7a1914669386f26ee7`。原 owner：`codex-batch011-korea-author`。原票 `2026-09-21-localize-three-korea-travel-guides-in` 的本機 scope 已縮 Nami／Seoul，本票承接該剩餘交接，保留 HOLD。
- Worktree：`<home>/.codex/worktrees/article-localization-batch-011-korea/travel_scanㄐ`。核對有 5 tracked + 12 untracked = 17 個變更；本票不授權清掉該 checkout。
- 證據：`<home>/.codex/scratch/uncertain-branches-followup-20261011/locale-audit.json`、`locale-working-evidence.json`。核對 main：`73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b`。manifest 已列每檔 SHA-256 與 frozen main 對照。
- 五個 tracked：`apps/api/app/guides/content/jeju-car-rental-guide.json`、`nami-island-petite-france-day-trip.json`、`seoul-where-to-stay.json`、`apps/web/public/guides/nami-island-petite-france-day-trip/diagram-1.svg`、`tasks/open/2026-09-21-localize-three-korea-travel-guides-in.md`。
- 十二個 untracked：Jeju、Nami、Seoul 每個 asset directory 的 `diagram-1-en.svg`、`diagram-1-ja.svg`、`diagram-1-ko.svg`、`diagram-1-zh-cn.svg`。全部先保留；本票新修改 scope 不含 Jeju。
- Jeju 已由 [PR #643](https://github.com/x812033727/travel_scanner/pull/643) merged `222a6a0d385eae989c0736ae8ace2a0df066f1f1`，main done Jeju-only task與 2026-09-22 release receipts 已記錄完成。本機 Jeju 五語 pack及四 SVG 在 CRLF 正規化後與 frozen main 相同；不要當成 Jeju 未完成或再發布。
- Nami 的 unique commit `1fbd57ac` source correction 尚未被 main 取代，主分支仍含舊 rail-bike 時間／退款敘述；本機又有未簽的 Namisum 條件修正。Seoul source proposal尚未核准。這兩項 HOLD 是實際缺件。
- 原本機 task 記錄獨立 Seoul source-review receipt 的寫入曾被自動政策審查以 `blocked by policy` 拒絕。保留這個歷史拒絕及 scope；缺件交由允許的獨立覆核流程處理，不以改工具、路徑或身份繞過。這不是本次草稿執行的新拒絕。

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。
