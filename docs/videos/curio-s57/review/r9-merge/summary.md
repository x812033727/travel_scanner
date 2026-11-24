# S57 R9｜真正隔離雙讀者固定 OR 正式合併

2026-10-21 UTC。**正式敘事 HOLD：12／13 YES，唯一必答失敗 `no_recap`。**[R9 獨立史料與書面畫面](../r9-source-independent.md)為 PASS／PASS，但不能覆蓋敘事阻擋。兩位讀者均由 `fork_turns:none` 全新啟動，先只讀固定 `script.md` 與 13 題，分別凍結原票；本合併未修改五份創作檔。

| 凍結檔 | R9 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `c7900d23f61699c506abbde288aadbe2d32c0e5020721a2e2c44ee04ff2876ea` |
| `claims.md` | `241f5a2fa4b25e977baf832907213b7be98cda7a9cfa55ea58331f0a31466beb` |
| `video.json` | `940046297c87511a82c9e42eb5d0c0fbcf8bdaa9b5528ce17234ac77c7cf8588` |
| `script.md` | `7edc924366e588787794e9c2ceac53ce8f5131188f19aa9c0a71a3543c326b43` |

## 原票、轉錄與固定 OR

[A 原票](raw-ballot-a.md)逐位元組複製自 `r9-blind-a.md`，SHA-256 `ac7e4aa9bbbff21bd96570e57a51af737f36b60da62a87ecffaa0ee14302a656`：**11 YES、2 NO**（`no_spoiler,no_recap`）。[B 原票](raw-ballot-b.md)複製自 `r9-blind-b.md`，SHA-256 `540740845cd2c5332d93574310a8a38a860633ca6c0865bcb029b28077072279`：**12 YES、1 NO**（`no_recap`）。A 原票本身是含每題原因的 JSON；B 原票是 13 題 Markdown 表，僅把每題票轉成[工具可讀的 B 答案](ballot-b.json)，由稿中該題所引的 `[sxxxxx]` 補上逐字旁白。A 的[工具答案](ballot-a.json)逐題沿用原 `yes/evidence`。[轉錄稽核](merge-audit.json)保留原理由、選取的 ID、原句與前後版 SHA，未改 YES／NO。

以 `panelVerdict(A/B)`、`mergePanelVerdicts([A,B])` 執行規定的**固定 OR**：同題任一讀者有帶 ID 的 YES 就通過。`no_spoiler` A 的 NO 由 B 的 YES 正式 OR 通過，A 的品質異議仍保存；兩票共同 NO 的 `no_recap` 阻擋。panel 規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。[合併答案](merged-answers.json) SHA-256 `5f1d2e6eb37207c5b8b1348b0a51daa93093ac5c9b4562ee00c10f7962a5bcc4`；`no_recap` 的證據欄僅壓縮兩票已有理由，以在官方工具 200 字上限內同時保留 A/B 修稿點，沒有改票。

| 票 | 可局部修的原票理由 |
| --- | --- |
| 共同 `no_recap` NO | A 指 `s57053` 已說長久缺歐洲消息，`s57055` 再以「兩年」重述缺消息；B 指開場 `s57002` 日記已交史丹利，正文 `s57167` 再講同一交付卻未當場點名回扣開場。 |
| A 單票 `no_spoiler` NO，B YES | A 指開場 `s57007` 已明說補給幾乎全失，搶先揭曉後章的失貨；B 認為開場仍留住去向與分路結果。R10 可窄改該句，不能抹掉 A 的異議或宣稱兩票一致。 |

## 官方 CLI、政策與 R10 交接

正式執行 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r9-merge/merged-answers.json --workdir /tmp/curio-s57-r9-formal-merge-20261021 --json`，得 **exit 1、`passed:false`、`failed:["no_recap"]`、0 advisory fail**。存有[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[前後 SHA 與命令](cli-status.json)、[官方 narrative 紀錄](official-narrative-record.json)；官方紀錄 SHA-256 `37cef1007d6583a55e62babcf1b5ad0c56faf012964b3f62343582e15b8a3ceb`。CLI 前後五檔 SHA 均與上表完全相同。

**政策門檻止於敘事 HOLD；未執行 policy 核准、付費語音、插圖、配樂、組片、上傳或發布。**R10 作者應只修開場 `s57007` 的預告界線、`s57053/s57055` 的重述及 `s57167` 對開場日記交付的明確回扣。保留 S／L 來源層級、2 月 18→19→20 日次序與八分鐘以上正文，再凍結新五檔，重交非作者來源／書面畫面覆核和兩位全新 `fork_turns:none` 隔離盲讀。
