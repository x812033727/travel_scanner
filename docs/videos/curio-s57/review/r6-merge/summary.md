# S57 R6｜雙盲固定 OR 正式敘事合併

2026-10-21 UTC。**正式敘事 HOLD：12／13 YES，兩位讀者共同否決 `no_recap`。**此合併只轉錄兩份已寫定的 R6 隔離盲讀原票，沒有重讀、改票或更動五份創作檔。[R6 獨立來源與書面畫面報告](../r6-source-independent.md)另判史料／逐句主張 PASS、書面畫面 `s57150` HOLD；敘事與畫面均未放行媒體製作。

| 凍結檔 | R6 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `48f287375b22a77929130046c15c55079c78d9376996a033709dc7a1d625b933` |
| `claims.md` | `71b0f3405bd254e7be0d464d34d81c98fb78b08951e046b331ec79a34af03919` |
| `video.json` | `e766dbe4ac40932abfa5bea1a89713604b2fbb64158bf3523376bde0aa0131cc` |
| `script.md` | `f2d8c42f6b71698121199d7c3c26ddde958eddf1d25be96783356c8ef404ef87` |

## 原票與合併

[A 原票](raw-ballot-a.md)逐位元組複製自 `r6-blind-a.md`，SHA-256 `2eaf9b5d83b8a18bad1af7ce4681fac84a57f499c10b5a84efc09760de707204`：**11 YES／2 NO**，`no_recap`、`no_detour`。 [B 原票](raw-ballot-b.md)複製自 `r6-blind-b.md`，SHA-256 `b8e61b198ad7bc14981a2ec47df16aaa120a5e92f929856c1405e7ba25673f7a`：**12 YES／1 NO**，`no_recap`。兩票以 `script.md` **行號**給理由；為符合官方 CLI 的場景 ID 引用格式，[轉錄稽核](merge-audit.json)逐題保存原理由、行號、對應 ID 與該行逐字旁白，不更動 YES／NO。

[A 答案](ballot-a.json) SHA-256 `cde2506f4331ba251a2cb5a37a03cd479a4d9249345e93ed3a827395c69a8990`；[B 答案](ballot-b.json) SHA-256 `eff17c6c91ff4ea71dc6575af1872fe7297c11528eb9f866709ff8e50e28160a`。以 `panelVerdict`、`mergePanelVerdicts` 的**固定 OR**（同題任一讀者有帶 ID 的 YES 即過）產生[合併答案](merged-answers.json)，SHA-256 `380539f388a93472bd23dcd29aca9c6a70dfc29bf7b257964beb08e13258fab2`；panel 規則雜湊 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。A 的 `no_detour` 異議保留，但 B 投 YES，故正式 OR 過；`no_recap` 兩人均 NO，正式阻擋。

| 診斷 | 凍結 R6 原票理由 |
| --- | --- |
| **`no_recap`，A、B 均 NO** | A 指補給到手後「繼續考察／不返家」在 `script.md` 541、545、557 行於同章重說。B 又指出同決定早見 279、405 行，545–557 行重述，687 行結尾再說。`s57148`、`s57149`、`s57153` 尤須拆開，只保留能帶出新事實的說法。 |
| `no_detour`，A NO、B YES | A 指 377–389 行連續三拍美國領事信、亞丁舊電報、李無同類信件未改變主線行動；B 認為湖行及東行仍服務回家或留下的問題。兩判讀原樣保留；修稿可收束那段書信資訊，不能倒說兩票一致。 |

## 官方 CLI 與 R7 交接

正式執行 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r6-merge/merged-answers.json --workdir /tmp/curio-s57-r6-merge-formal-20261020 --json`，**exit 1、`passed:false`、必答失敗僅 `no_recap`、0 advisory fail**。創作五檔 CLI 前後 SHA 均與表中完全相同。存有[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[命令／前後雜湊](cli-status.json)、[官方紀錄](official-narrative-record.json)；正式紀錄 SHA-256 `6d7908ac0cb8357ae7c42360a077b7be1a508fb882958fa822452f62857a7152`，其中 `panel_narration_sha256` 為 `fd69bcb57d6ba68633ea86189ee59c699a638f7e3658d84407500cff210d8fae`。

**R7 作者界線：**把 `s57150` 書面提示改成單一人物／單一動作，不讓畫面顯示人手已抵達；精簡多次「先完成考察、不返家」的重播與可刪書信岔段。保留 S／L 史料層級、2 月 18→19→20 日順序與八分鐘以上正文。R7 須重凍五檔，重新接受獨立來源／書面畫面覆核與兩位全新隔離盲讀；本合併不能替 R7 判 PASS。未進政策、語音、插圖、配樂、組片或發布。
