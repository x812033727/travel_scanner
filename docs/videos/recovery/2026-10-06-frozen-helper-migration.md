# 凍結 Embedding helper 保全與遷移核對（2026-10-11）

關聯票：`2026-10-11-migrate-frozen-embedding-helper-dependency`。本文件是清理所需的保存與隔離方案；**b136 目前保留，正式操作遷移尚未完成**。證據與離線 fixture 寫入清理 scratch；本文件納入共享 PR，沒有修改 repository helper、任何原始 manifest／wrapper／STOP／lease／paid receipt，也沒有啟動 producer、dispatch、provider 或主機操作。

## 保存的原件

完整原件、來源路徑、SHA-256、大小與逐位元組還原結果在 `<home>/.codex/scratch/codex-closeout-20261011/helper-recovery/dependency-proof.json`。四份原件均已保存到該 recovery 目錄，並由保存副本還原到獨立的 `restored/` 檔案，完整 bytes／SHA／size 全部 PASS。原件仍在原位置；fixture 前後再次核對一致。

| 原件 | 原始完整 SHA-256 | bytes |
| --- | --- | ---: |
| `root-current-worker-finite-READY-e93108ffca5a4ab5b30729e3188ef82b.json` | `782d193121b97d04a6a72cca96f6275112852885e54adf939bdcbb9f14a0493c` | 1,011,889 |
| `scoped-audio-cap40-native-CODE-DRAFT-20261006/normal-audio-check-post-merge-v5-budget40.DRAFT.mjs` | `eeca80b0aa7b960a36e3ca85725b54c892e08732da946be66718090ada074acf` | 29,442 |
| `b136/travel_scanㄐ/tools/tasks.mjs` | `abae88f61bf529390b76e196485264e278922d1f1bcebbca07c507e3e871a4b1` | 28,653 |
| `root-current-worker-immutable-launch-handoff-e93108ffca5a4ab5b30729e3188ef82b.json` | `86da79fc4f7a08096e487f8d82a74cfadf57af8e0d1a1cadc41dd269f00eddf0` | 5,096 |

manifest、executor 與 immutable handoff 三個外部製作檔位於 `<home>/mokaair-work/ai-series-continuation-20261004/`；helper 原始絕對位置是 `<home>/.codex/worktrees/b136/travel_scanㄐ/tools/tasks.mjs`。實際 worker binding `35af8fcc…`／581 bytes 與原 neutral wrapper `81f5630d…`／9,869 bytes 亦已保存並 exact readback PASS。

## 真正的依賴邊界

原 manifest 的 `/private_file_pins/373` 是唯一指向 b136 的 path pin，恰好是上述 helper 的完整 SHA／size。executor line 29 的 `checkLocal()` 驗證這些 pins；line 83 的 `freshDispatchGuard()` 與 line 88 的 context provider 會再次呼叫 `checkLocal()`。所以保存副本不會自動改變原 executor 的檔案查找位置。

另有實際的 module import，不能漏掉：manifest 的 `root_read_only_stage_guard` 指向 `scoped-audio-cap40-compat-DRAFT/guard.DRAFT.mjs`（`b463b35d…`）。該 guard line 4 import `captured-main-native-GP-CODE-DRAFT-2030-84f62ca1/full15-captured-main-current.DRAFT.mjs`；collector line 2 直接從 b136 helper import `parseTask`、`scopesOverlap`、`isStale`。collector 本身也在原 manifest 的 `/private_file_pins/1153`，SHA `a70ef57e097ca2619036e0056eaddb9d3831bc8f1c92ee61cd20fa34f501f897`、30,753 bytes。移動 helper 後若要讓正式 successor 不再讀 b136，必須另建經審查的 collector／guard／manifest，而不是改舊 pins。

`ai-terms-resume-20261006/scoped-episode-cap40-DRAFT/image-guard-DRAFT/collector.mjs` 與 `image-guard-v2-DRAFT/collector.mjs` 也 import 相同 helper；這是 inert IMAGE CODE 的依賴，仍屬 `LIVE_NOT_READY`，不是圖片製作已啟動或 successor 已採用的證明。

已記錄的 e931 one-use launch chain 是 immutable handoff → binding／neutral wrapper → executor／manifest → helper verification 與 guard collector import。舊 wrapper 有新 receipt／exact hash／native actor 等守門，且該次執行已 stopped HOLD；不得重放任何舊 wrapper來驗證本票。

36fa 的 `observe_current_stage.py` 則只核對 handoff 與完整 manifest 的 SHA／size，再讀取 stage terminal／cache；完整靜態源碼沒有 `private_file_pins`、`tasks.mjs` 或 b136 lookup。保存原 manifest bytes 可供這個 observer 做歷史觀察，無需執行 helper。但這不能代替 production successor 的依賴釋出。

## 當前狀態與歷史引用

2026-10-11 實際 automation TOML 的 `ai-g` 是 **PAUSED**。它仍記錄原 thread `01a1066c-b865-7c03-b19e-b5fb32607794`，prompt 指示由 36fa thread `01a10f55-db5e-7c31-a54f-771933d22909` 接續。36fa 最新可讀 final 明確說舊製作程序已在 2026-10-06 13:57 停止、35/156，保留現場、未重啟。舊 STATUS／stop snapshot 中的 `ACTIVE` 是當時排程資料，不是目前 liveness。

實際 terminal `f364bf52…`／356 bytes 已再次 exact 核對：`HOLD`、`normal_main_exit=4`、`PRIVATE_STAGE_FAILED_PRESERVE_EVIDENCE`。既有 stop receipt `9ee18f64…` 記錄四筆新 ASR 已知回應、第五筆 reservation 沒有已知 provider response。這些原始控制均保持，沒有 retry、釋放 reservation 或更改付費計數。

此次索引僅限兩個已知 continuation／resume 根，完整清單在 `bounded-reference-index.json`。實際 checkout path、helper pin、舊審查快照、離線 fixture與可执行源碼分開；hex hash 本身包含 `b136` 的假匹配已排除。索引共有 277 個相關檔案、75 個 exact helper pin nodes；123 個源碼檔有 b136 路徑，其中 24 個檔案還包含 tasks helper 字串（含歷史 RUN，不能當成 24 個 active launcher）。所有匹配均沒有被機械計作 active。

兩個大型 LLM timing snapshot（`llm-final-timing-independent-2030-probes/final.json`、`body.json`，各約 17 MiB）未做完整 JSON 結構分類，已明列缺件。除此之外，本輪沒有掃描其他專案、Claude、媒體或《偶的江湖》。目前也沒有現任 owner 明確釋出原 helper 依賴、或採用新 production successor 的收據；`notLoaded` 不作為釋出證據。

主線 `2026-10-11-rewrite-ai-term-embedding` 的 YouTube id 與新內容屬另一既有工作，本票不把舊 e931 的停止狀態當成今日 Embedding 尚未發布，也不接管重寫／製作 owner。

## 獨立保存與離線 fixture

獨立於 b136 的 helper 保存位置：

`<home>/.codex/scratch/codex-closeout-20261011/helper-recovery/objects/sha256/abae88f61bf529390b76e196485264e278922d1f1bcebbca07c507e3e871a4b1/tasks.mjs`

先核對該檔完整 SHA／28,653 bytes，再從 recovery 原件還原即可重現原 helper。完整 manifest／executor／handoff 必須依原名與原 hash 保存，不得把恢復位置写回 frozen 原件。這些保存副本目前位於 C 本機 scratch，不是已驗證的外部／雲端備份；清理 scratch 時必須繼續保留或先移交同等可還原 archive。

純資料 `offline_lookup_fixture.py` 的 7/7 案例 PASS：archive-only lookup、缺檔拒絕、同大小 hash 漂移拒絕、size 漂移拒絕、錯誤預期 hash 拒絕、原 checkout path escape 拒絕、所有實際讀取限於 recovery。它不 import helper／producer，也沒有 dispatch／網路。

`archived-helper-api-fixture.mjs` 另用 bundled Node v24.19.0 **只 import exact 保存 helper library**，以純合成輸入驗證 `parseTask`、`scopesOverlap`、`isStale` 的 API與錯誤邊界，5/5 PASS。啟用的 fixture barrier 記錄原 checkout reads、provider calls、subprocess、檔案寫入皆為 0；未 import producer 或 launcher。第一個 fixture 的 file-URL normalization 錯誤另有 failed-attempt 收據，修正後通過；不是 helper 或正式管線失敗。

合計 12 個离线案例完成。這證明保存副本可供新 caller 使用，**不代表既有 collector／guard／launcher 已轉用保存位置**。

## 後續方案及本輪結論

現任實際 owner 可選擇確認舊 stopped package 僅供封存，且無現行 successor 仍消費其 b136 路徑；或在另外的 scope／owner／review 流程中採用保存 helper，另建新 collector／guard／manifest及新 immutable handoff。後者須完整核對所有 direct/transitive imports、原 helper 行為與新 pins，仍不因此授權啟動 provider。舊 frozen manifest／CODE／STOP／paid receipts不更改。

根據已取得的證據，本輪结论是 **保留 b136**：保存與離線方案完成，但真正 current dependency release／new production adoption 未完成。清理流程只有在沒有持續依賴、原 source／receipt 已可還原、fresh process／app ownership／exact HEAD／status CAS 全部通過後，才能另行處理 checkout；本票本身不刪除 checkout。

DoD 進度：第1項原件保全與還原完成；第3項獨立保存位置／遷移方案完成（無正式 adoption）；第4項離線 fixture完成；第5項 root 判準與明確 keep決定完成。第2項已交付已採用 old chain、observer 與 bounded 引用清單，但兩份大型 snapshot及真正 successor／owner 釋出仍待核對，不能勾作已完全解除依賴。
