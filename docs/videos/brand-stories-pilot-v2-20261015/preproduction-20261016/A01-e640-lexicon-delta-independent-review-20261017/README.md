# A01 `e640` 詞庫差異獨立唯讀診斷（2026-10-17）

**結論：現有快照維持 HOLD。** 我獨立解析舊詞庫與 2026-10-17 A01 唯讀快照的 JSON，而非沿用差異摘要的計數。詞庫由 295 筆變為 318 筆：精確新增 23 筆、刪除 0 筆、舊鍵的值變更 0 筆。新詞在快照 A01 的實際旁白欄位及 round20 隔離候選旁白均無命中；這只支持本機文字層面的「新增詞未改動這兩份旁白的詞庫匹配」，不證明正式機工人的發音結果、來源轉移安全性、稿件審核或可續製。

## 釘選的輸入

| 輸入 | SHA-256 |
| --- | --- |
| `A01-round10-candidate/evidence/round9-lexicon.json`，80-link tip 錨定的舊詞庫 | `ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9` |
| 本機唯讀擷取 `A01-20261017-095816-2a72b1e1/snapshot-80/docs/videos/lexicon.json` | `e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30` |
| 同次擷取 `capture-receipt.json` | `d15566f3ec2a9792975823347bebe750bd2aa951281a0acb38c1d6776277149d` |
| 同次擷取原始 tar（依擷取收據） | `02b8631af6133227088a86d6eae7bff0bd152aa2e72b48198cec30741e964499` |
| `A01-round20-i17-fact-index-candidate/manifest.json` | `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549` |
| 本機比對所用 `tools/video/core/lexicon.mjs` | `b9869497afbbd8dfbfce273e9856fab45beadf7b341aa3da17c6685b4509386d` |

本機擷取保存在 `C:/Users/x8120/.codex/captures/A01-20261017-095816-2a72b1e1/`，未放入 Git。`A01-live-readback-20261017.md` 記錄主機取得方式、199/199 檔案雜湊讀回及兩次相同的 SQL／預算；我此輪沒有再次連上主機，因此不能把快照當作當下仍不變的正式機狀態。

新增鍵及值逐筆如下；`null` 是沒有指定發音替換，不代表沒有術語匹配影響：

| `null` 值（9） | 有指定發音（14） |
| --- | --- |
| `pull`, `request`, `Eiliko`, `Energize`, `Lab`, `K`, `Star`, `Swatch`, `Group` | `CVE`→`C V E`, `IP`→`I P`, `Seiko`→`精工`, `Quartz`→`夸茲`, `Astron`→`阿斯特朗`, `CEH`→`C E H`, `IEEE`→`I triple E`, `Beta`→`貝塔`, `swissinfo`→`swiss info`, `Europa`→`歐羅巴`, `Donz`→`東澤`, `SSIH`→`S S I H`, `ASUAG`→`A S U A G`, `Hayek`→`海耶克` |

`snapshot-80` 六章與 `video.json` 合計 126 場景、184 行，`say` 欄位 0 行；所以實際朗讀內容全由 `text` 欄位提供。以本機 `termPattern()` 的 ASCII 邊界規則逐行搜尋，新增詞命中 0。`termsUsed()`、`entriesUsed()` 與每行 `unknownTermsFor(..., 'zh-TW')` 的舊新輸出逐項相同；已用到而有替換的舊詞仍只有 `Macy's`、`Sadow`、`Samsonite`。round20 隔離候選的六章是另一份 79 場景、108 行、`say` 0 行的稿，另以不區分大小寫的同類詞邊界搜尋，新增詞命中也為 0。**round20 的 `changed_spoken_lines: 0` 僅相對 round19；不能說 round20 與正式機 round9 旁白相同。**

## 橋接假設的核對與缺口

1. 本機重新執行 `A01-lexicon-rebaseline-e640-candidate/rebaseline.mjs` 的唯讀 `--snapshot`，產生 80→81 **提案** `lexicon-rebaseline-e6403c824aac13b4`，plan SHA-256 `b76ed8f0dc99ff392535dada601a599ba51fd0f5464aab39dcdc6cfdd6aef24f`；它只把來源 composite 從舊 tip `cf39296d…` 指向擷取值 `90b82e2f…`，沒有新增 audit event。歷史 80-link index／manifest pins 仍是 `c7ddb6b5…`／`ada7ff18…`。先前針對**兩詞** `835e09df…` 的審查不能搬到此 23 詞提案。
2. 真實 `capture-receipt.json` 經 `A01-e640-round20-offline-bridge-20261017/capture-gate.mjs` 回傳 exit 1、`REJECTED/HOLD`：`NO_VERIFIED_81_EVENT`、`CAPTURED_CONTROLS_ABSENT`、`UNCERTAIN_STAGE_JOB`、`AUDIT_SOURCE_NOT_REBASELINED`。唯讀快照是 80 個事件、三個控制檔未出現、一筆結果不確定的 stage job；因此沒有可交給 81→82 橋接工具的真正 81-link after 擷取。擷取當時 STOP 不存在，也不能從事後文件推定已取得排他寫入窗口。
3. `inspect-host-plan.mjs` 只組合 **外部提供**的 80/81 擷取、pins、SQL／預算投影與 round20 package；即使得到 `LOCAL_82_PLAN_BOUND_TO_SUPPLIED_EXPORT`，結果仍固定 `production_status: HOLD`、`installation_allowed: false`、`paid_work_allowed: false`。它對兩次本機讀回相同的檢查不是跨主機 docs/work 兩個掛載點的原子鎖。`suppliedStateQuiet()` 僅檢查 `run_receipts` 是陣列，沒有解析各收據狀態；我傳入一筆非空 `run_receipts` 的最小合成投影，仍得到 `quiet: true`。未解收據仍須在獨立主機前檢中查明，不能由該布林值代替。程式內字串形式的 reviewer、operator 或 approval reference 也不驗證人的身分或核准來源。
4. 目前詞庫命中為零只基於本機 `lexicon.mjs`（上表雜湊）；正式機 worker 的已記錄 SHA-256 為 `0ff27096862a9e22698aed8cc043e3b56db88a5a8f419a77dc1fa37b0d4c72dd`，此輪未取得並比對其實際 TTS／glossary 實作。任何新詞庫或 A01 章稿再次變動都會使此結論過期。round20 仍需獨立實稿審核、正式 verifier／listener／narrative panel 與審稿收據，不能以此診斷替代。

## 重跑指令與實際結果

以下在 `a01-branch-sync/travel_scanㄐ` 執行；第一個命令的輸出是本機提案，不是已發生的主機事件。JSON 差異、184 行與 108 行的獨立逐行檢查另以 `ConvertFrom-Json -AsHashtable` 的 `GetEnumerator()` 及直接匯入 `tools/video/core/lexicon.mjs` 完成；計數與上文一致。

```powershell
$old = (Resolve-Path -LiteralPath 'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round10-candidate/evidence/round9-lexicon.json').Path
$capture = 'C:/Users/x8120/.codex/captures/A01-20261017-095816-2a72b1e1'
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-e640-candidate/rebaseline.mjs --snapshot "$capture/snapshot-80" --old-lexicon $old
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/capture-gate.mjs --receipt "$capture/capture-receipt.json"
Get-FileHash -Algorithm SHA256 -LiteralPath $old,"$capture/snapshot-80/docs/videos/lexicon.json","$capture/capture-receipt.json",'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round20-i17-fact-index-candidate/manifest.json'
```

第二個命令實際 exit 1 並顯示上述四個拒絕理由。我也執行了 `node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/inspect-host-plan.test.mjs`：6/6 通過；它們使用合成資料，不能驗證本次真實主機已發生 81st event。這份文件只診斷已取得快照；**不是** 81st event 的獨立正式審查、審稿收據、主機寫入核准、81→82 安裝核准或付費續製指示。
