---
id: 2026-10-11-reconcile-hanoi-localization
title: 恢復河內舊城來源查證與四語翻譯待辦
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T13:45:45Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-hanoi-localization.md
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
  - apps/web/public/guides/hanoi-old-quarter-walking-guide
  - docs/article-localization/reconciliations/hanoi
---

## Why

河內舊城步行攻略的四語作者交接與來源連結修復只保留在歷史分支，未進入共享看板。核對 73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b 時，`hanoi-old-quarter-walking-guide.json` 仍只有 zh-TW；原四份 en、ja、ko、zh-CN 工作曾準備完成，但沒有獨立核准、內容 PR 或版本重新綁定的完成證據。

本票恢復這兩個實際缺件：官方來源的有效性與主張支持，以及修正後來源綁定的四語文件／圖解。原 Batch006 的 KL 和兩篇 Singapore 已完成，不納入本票。

## Done when

- [ ] 找到原四語未簽稿、圖解與交接包的實際保留／備份位置，記錄內容雜湊；若確定已無資料，明確記錄缺件後重建，保留可找到的原嘗試。
- [ ] 重新查證 Vietnam Tourism 引用 URL 與 Hanoi／Hoan Kiem 主張支持，取得獨立覆核的最小修正或保留理由；不得把 2026-09-20 的 HTTP 404 當成本日已重新查證。
- [ ] 取得目前正式站 zh-TW 的版本與正規化 hash，確認 #599 句子修正是否已發布；候選若變更來源，四語一律重綁核准後的來源版本。
- [ ] 四語每個可見文字欄位、數字／條件、credit、來源標題、連結及 SVG 文字完整，逐語獨立文字與視覺審稿綁定最終 hash，無未解 finding。
- [ ] 必要來源修正與四語 pack／asset 經相關檢查及 PR 審查納入 main。未完成的正式發布／匯入／public QA 留在獨立 release 票，不能以本票的作者完成宣稱已公開。

## Steps

- [ ] 先讀 article-localization 與 task-board skill，確認原作者／active session 與 pack／asset scope；認領窄 scope 後才修改。
- [ ] 從原分支與外部交接記錄定位四語 jobs、review-handoff 與候選 SVG，核對來源版本與 hash，記錄可復用及需重建部分。
- [ ] 查證既有 `https://vietnam.travel/places-to-go/northern-vietnam/ha-noi`，及已引用的 `https://vietnam.travel/node/915` 是否支持所需主張；不得未讀內容就以重複引用替換。必要時提出最小來源修正並獨立覆核。
- [ ] 以新來源版本重新綁定四語文件與圖解，使用現有工具處理受控同站 locale links；翻譯與覆核者分開。
- [ ] 驗證完整文件與圖解，開 scoped PR；若需要正式站來源發布，先建立／沿用獨立 release 票與既有 guard，不在作者檢查中順手發布。

## Verification

依 article-localization skill 驗證 GuideDocument、來源／文件／asset hashes、完整欄位覆蓋、SVG 1600×900 與手機 scroll render、credit、link outcomes。執行受影響的 content-pack／links 測試、`npm run check:tasks` 與 `git diff --check`。目前公開來源只可作有記錄的唯讀版本擷取；正式寫入、部署、備份、匯入與發布另依 release 票處理。結案記錄必須區分 authored、reviewed、merged 與 published。

## Notes

- 建票日期：2026-10-11。本票依歷史分支核對補回共享 queue；本次草稿未修改來源或連線正式站。
- 原分支：`codex/article-localization-batch-006`；保留 HEAD：`56d98e4decce9f760179665119c2821c350b7613`。原作者：`codex-batch006-author`；原票 `2026-09-20-article-localization-batch-006` 與 `2026-09-20-hanoi-old-quarter-vietnam-tourism-source` 未存在於核對的 main。本票承接其剩餘工作，不能視為原 scope 的自動認領。
- 核對 main：`73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b`。證據：`C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/locale-audit.json` 與 `locale-content-comparison.json`，包含兩個 unique metadata commits、完整舊交接及產品 path history。
- [PR #599](https://github.com/x812033727/travel_scanner/pull/599) 已 merged `e8ad6c1d3c9116bd4ee61e8172b76aea92629bf4`，只完成 zh-TW 句子修正；main done 來源票明示發布、四語 rebind 與 citation 維護仍是後續工作。不要重做該句子 patch。
- KL／Singapore 已由 [#602](https://github.com/x812033727/travel_scanner/pull/602)、[#605](https://github.com/x812033727/travel_scanner/pull/605)、[#607](https://github.com/x812033727/travel_scanner/pull/607) 與 [#617](https://github.com/x812033727/travel_scanner/pull/617) 完成；既有 done task 記錄 15 public routes、31 browser cases 與 hold clear，不重開。

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。
