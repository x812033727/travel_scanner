---
id: 2026-10-08-ou-de-jianghu-external-look-import
title: 《偶的江湖》角色設定圖外部匯入：採用畫像接入正常look與跨集參照
status: done
priority: P1
area: tools
owner: codex-ou-import
claimed_at: 2026-10-08T14:20:54Z
created_at: 2026-10-08T10:52:23Z
completed_at: 2026-10-08T15:33:31Z
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-visual-preproduction
scope:
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/series-store.mjs
  - tools/video/media/series-store.test.mjs
  - tools/video/cli.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/series-plans/ou-de-jianghu/visual-development/import-contract
---

# 《偶的江湖》角色設定圖外部匯入：採用畫像接入正常look與跨集參照

## Why

目前look沒有PNG匯入；--file讀video.json，sheetPrompt只使用base appearance。外部採用圖還不能被證明進入實際動畫流程。

## Definition of done

- [x] 設計及實作窄範圍base角色設定圖匯入：明確分開專案JSON與PNG參數，驗角色、格式／尺寸、來源及媒體hash，不悄悄觸發生成。
- [x] 走正常look judge／選用／核准／series-store，保留來源；不手寫通過分數或繞過關卡。同hash安全重跑，換圖／appearance／style時舊核准與下游正確失效。
- [x] 測試非法角色／壞檔、重跑去重、hash變更失效、跨集reuse及reference選取；清楚寫明shot_looks仍為文字覆寫，沒有每造型獨立圖像引用。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [x] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

執行 Notes 所列測試及相關 tools 檢查。

`npm run check:tasks`

## Notes

- 2026-10-08：本輪由主控分工授權完整離線工程；已讀 task-board、dev-and-ci、youtube-video 及 drama 參考。`look import --image PNG --source JSON` 預設只建 pending candidate；新增 SHA 綁定、完整 PNG CRC/解壓/尺寸驗證、正常 judge（只送一次，未知結果保留 submitted）、owner choice/approval 與 review gate 防護，以及跨集原件／來源共用。完整操作與限制見 [import-contract/README.md](../../docs/videos/series-plans/ou-de-jianghu/visual-development/import-contract/README.md)。
- 2026-10-08 驗證：bundled Node `C:/Users/x8120/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe` v24.19.0；`--test tools/video/media/look-keyframes.test.mjs tools/video/media/series-store.test.mjs tools/video/review/sync.test.mjs` **153 tests / 153 pass / exit 0**；`tools/tasks.mjs check` exit 0（只有既有過期認領警告）；`git diff --check` exit 0。首次套件唯一失敗是既有 outline-lost 測試硬編 `/`，已只在測試正規化 Windows 路徑，重跑全套通過。
- 最後工程版本加上既有 automation/series 回歸：`--test tools/video/media/look-keyframes.test.mjs tools/video/media/series-store.test.mjs tools/video/review/sync.test.mjs tools/video/automation/series.test.mjs` **229 tests / 229 pass / exit 0**（`TEMP/ou-external-look-final-four.log`）。生成圖 legacy 相容問題已修，嚴格原圖 SHA 檢查限定外部候選；正常生成圖介面保持。
- 全 tools 回歸：**2162 tests / 2141 pass / 8 fail / 13 skip / exit 1**（`TEMP/ou-external-look-all-tools.log`）。其中 generated series store 相容失敗已由上述 229 項重跑驗證修好；另三個變更檔使 duration review binding 過期，交由主控獨立覆核更新，不能自行捏造 PASS。其餘 6 項為本次 scope 外的 Windows／ffmpeg 相容問題：reference-analysis `--compare` 無影格分支；automation 子程序 `C:` ESM import 後無 exit handler 永久等待；project-lease 兩例同類 ESM 路徑；stock 測試斜線；brightness 測試在 Windows 拼接含磁碟代號路徑。automation 卡住超過 7 分鐘後僅停止已核對本次 runner 父子關係的該子測試 PID 34596 收回總結，其餘測試未中止。全庫不是綠燈；範圍外問題已交主控追蹤。
- 本票沒有呼叫真實圖片生成或付費 judge、沒有寫首集 owner approval、沒有 commit/push 或部署。測試中的 judge／核准均為隔離 fixture。後續主控另授權九張既有全身原圖做隔離 pending staging，已完成；正常 runtime 未匯入，個別圖像採用仍由畫像／handoff 票完成。
- 真實 staging：九張 `full-body-v1` 原圖、12 來源檔現查 SHA 與製圖收據一致；九份 source sidecar 綁 v3 working video 的 look_hash。兩轮合計54次 CLI dry-run/import/原樣重跑全exit0；首輪驗證器最後誤拒自身 LEASE exit1，修正後明確續跑並最終exit0。fetch攔截器0次呼叫；每角色一個judge:null/suggested:null/needs_review:true候選，manifest重跑bytes不變；無choice/approvals/ledger。證據見 [pending-staging-receipt.json](../../docs/videos/series-plans/ou-de-jianghu/visual-development/import-contract/pending-staging-receipt.json)。`selection_for_offline_candidate_validation_only=true`，全部1024×1536，尚未達2048美術長邊目標，沒有採用或normal-runtime整合。
- 主控已獨立讀三檔完整 delta，判定未改duration行為；但原 `docs/videos/long-form/review.*` 與活躍PR #1387碰撞，未搶改或偽造原receipt綠燈。增量覆核與待整合限制由主控保存在本票import-contract；本工程功能完成不代表全工具/CI綠或可部署。

- 2026-10-08 實作中經主控同意擴入 review/sync.mjs 與測試：既有 review 管線容許 judge:null 選項，須防止未判圖的外部候選經 review-push/pull 被核准。兩檔 who-is-on-it 查無 active scope 或其他 open PR，工作目錄亦無先存修改；既有生成圖行為保持。

原開票規劃：可用離線測試圖與美術並行；新增檔/schema/API前先擴窄scope及查碰撞，不擴成多參考架構。本輪新增工程授權與完成證據如上。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
