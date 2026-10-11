---
id: 2026-10-11-migrate-frozen-embedding-helper-dependency
title: Preserve and migrate the frozen Embedding task helper before retiring b136
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T15:08:01Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/recovery/2026-10-06-frozen-helper-migration.md
---

# Preserve and migrate the frozen Embedding task helper before retiring b136

## Why

`codex/ai-series-continuation-20261004` 的產品原始碼、LLM 收據已整合；`b136` 目前僅有產生的環境 metadata 未提交。仍不可僅憑已合併就移除 checkout：外部凍結的 Embedding e931 證據包將 `b136/tools/tasks.mjs` 的絕對路徑列入 `private_file_pins`，其 executor 確實驗證该檔。這張票只處理清理所需的依賴保全、隔離方案及驗證紀錄。

既有 `2026-10-04-ai-term-embedding` 與 `2026-10-11-rewrite-ai-term-embedding` 是製作／內容重寫票；本票不重新開製作、宣稱影片未公開或接管其 owner。main 的重寫票已記錄 YouTube id `a10UMT6xqws`；舊 e931 的 stopped HOLD 收據亦須保留，兩者不能混作同一批目前製作狀態。

## Definition of done

- [ ] 紀錄並保存 original manifest、immutable handoff、executor 與唯一 b136 helper 的原始完整位元組、SHA-256、大小及安全還原結果；保留原件。
- [ ] 在不執行 producer、不連網、不改舊 frozen pins 的前提下，完整列出引用此絕對路徑的 manifest / guard / launcher，區分封存證據、可執行但已停止的舊 wrapper 與真正仍被 successor 依賴的路徑。
- [ ] 說明獨立於 b136 checkout 的 helper 保留位置及可重現還原方式；對原始副本做 exact bytes / SHA / size readback。若需新 successor guard / manifest，另走正式 owner、scope 及 review，不在這張 docs 票直接改寫或授權啟動。
- [ ] 用不含 dispatch、provider、主機寫入的離線 fixture 證明新方案不再以 b136 作為即時輸入，且仍能檢出缺檔與 hash 漂移；保留停止狀態與所有原證據。
- [ ] 交付清理前的依賴清單與 root 判準：沒有真正持續依賴、source / receipt 已保全、fresh process / app ownership / exact HEAD / status CAS 都通過後，才可由清理流程另行移除；本票本身不刪 checkout。

## Steps

- [ ] 唯讀核對凍結證據與本票 hash；對任何漂移停止此清理判定。
- [ ] 建立 helper / manifest / executor 的完整封存與還原紀錄，列出所有 direct 與 transitive path dependencies。
- [ ] 撰寫穩定位置與 successor 遷移／封存方案，請現任實際 owner 審閱依賴邊界。
- [ ] 僅執行離線、zero-provider fixture 檢查並保存結果；回填可否解除 checkout 依賴的精確結論。

## How to verify

本票允許變更的 repository 檔案僅 `docs/videos/recovery/2026-10-06-frozen-helper-migration.md` 與本票本身。備份及離線還原可使用清理 scratch／受控外部 archive；不得修改原外部 production manifest、wrapper、原媒體、STOP、lease、provider receipt 或 repository helper。以檔案 readback、SHA-256、size、無 provider / dispatch 的 fixture、引用圖及 owner readback 驗證；不要 import / run 真正 producer。

## Notes

- Frozen main：`9c46c14ed5c22388be68dec8301695667a226bee`；b136 branch HEAD `3b870bc37286f6e8accdaf30a27de3cbd3a7cb9e`；來源稽核為 `video-audit.json` / `extra-video-proofs.json`。原產品 PR #1207 已合併，沒有這支 branch 的 open PR。
- Original manifest：`<home>/mokaair-work/ai-series-continuation-20261004/root-current-worker-finite-READY-e93108ffca5a4ab5b30729e3188ef82b.json`；SHA-256 `782d193121b97d04a6a72cca96f6275112852885e54adf939bdcbb9f14a0493c`；1,011,889 bytes。
- Manifest `private_file_pins` 的唯一 b136 路徑是 `<home>/.codex/worktrees/b136/travel_scanㄐ/tools/tasks.mjs`；SHA-256 `abae88f61bf529390b76e196485264e278922d1f1bcebbca07c507e3e871a4b1`；28,653 bytes；本輪唯讀實際檔案 hash / size 相同。
- Executor：`<home>/mokaair-work/ai-series-continuation-20261004/scoped-audio-cap40-native-CODE-DRAFT-20261006/normal-audio-check-post-merge-v5-budget40.DRAFT.mjs`；SHA-256 `eeca80b0aa7b960a36e3ca85725b54c892e08732da946be66718090ada074acf`；29,442 bytes。line 29 的 `verifyPinned` 驗證 `private_file_pins`，line 83 的 `freshDispatchGuard` 在每次 dispatch 前呼叫 `checkLocal()`。
- ai-g 實際 automation TOML 為 PAUSED；原 b136 owner thread `01a1066c-b865-7c03-b19e-b5fb32607794` 已交接給 36fa thread `01a10f55-db5e-7c31-a54f-771933d22909`。這是已記錄交接，不能把旧 STATUS 的 ACTIVE 字樣當目前 liveness。
- e931 舊單位已 CLOSED / stopped HOLD（`PRIVATE_STAGE_FAILED_PRESERVE_EVIDENCE`，exit 4）；保留 31 old + 4 new ASR，未知第 5 筆 reservation 沒有已知 provider response。不 replay 舊 wrapper、不放鬆 pins、不釋放 reservation、不改 paid counter、不啟動 provider。
- Embedding 的原 source checkout 為 `ai-series-next-20261004`，其他 successor、媒體與外部收據另有位置。G 備份、原媒體／共用 Shorts 清理、owner listening、上傳／公開、內容重寫均留在既有任務。
- 本票 `open` / unclaimed；只有完成 owner/scope/review 手續才可另做實際 production successor 改動。清理復原並不授權更改任何生產狀態。
