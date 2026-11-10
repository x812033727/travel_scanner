# S57 R8｜雙讀者固定 OR 正式敘事合併

2026-10-21 00:27 UTC。**正式敘事 HOLD：12／13，唯一必答失敗 `no_recap`。**R8 的[獨立史料與書面畫面覆核](../r8-source-independent.md)為 PASS／PASS，不能覆蓋敘事失敗。本次只封存兩份已投票的讀者資料、按既定固定 OR 規則合併、跑官方工具；沒有修改五份創作檔、媒體或網站審核。

| 凍結創作檔 | R8 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd` |
| `claims.md` | `cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861` |
| `video.json` | `bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4` |
| `script.md` | `d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d` |

## 原票、轉錄及固定 OR

[讀者 A 原票](raw-ballot-a.md)與[讀者 B 原票](raw-ballot-b.md)逐位元組複製自 `../r8-blind-a.md`、`../r8-blind-b.md`，SHA-256 各為 `933ff949a225322669fda7f457e4580e3ab8a466f2417da55a870ce18c369dcc`、`00e1678f9e869c2497a3a30ce1a488ad88853b627cdb0f8d85241774324cc694`。原始結構化 [A 答案](ballot-a.json)／[B 答案](ballot-b.json)各十三題均聲稱 12 YES、`no_recap` 1 NO；A 的參考題 `chapters_are_events` 雖投 YES，原證據漏了方括號場景 ID，`panelVerdict` 按規定把該**參考題**正規化為 NO，對必答結論沒有影響。B 在該參考題有有效引用，所以合併後也無參考題失敗。原票未被改寫。

程式的 `panelVerdict(A/B)` 後接 `mergePanelVerdicts([A,B])`，規則是**任一讀者附有效引用的 YES 即通過該題**；兩人同為 NO 才失敗。[轉錄稽核](merge-audit.json)逐題保存每票、引用與合併後的 `yes_readers`；panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。[合併答案](merged-answers.json) SHA-256 `1a54d00037e1c95b9d27cda53ab4d1fa42e9db917aa7c11c17b679838c3aa989`，只在 `no_recap` 精簡兩位讀者的引用，以便官方工具 200 字證據欄保留 A/B 的具體退件點；YES／NO 一題也未變。

| 共同 NO | 已有原票中可局部修的重述 |
| --- | --- |
| `no_recap` | A：[s57016](../../script.md) 與 [s57018](../../script.md) 重述市集有食物、希望休養；[s57029](../../script.md) 與 [s57032](../../script.md) 重述班奈特的尋人任務。B：[s57161–s57163](../../script.md) 連續三句反覆說三月寫信；[s57179–s57180](../../script.md) 先說蘇西、楚馬在告別隊伍，隨即再說路上不只兩人。 |

## 官方結果與限制

執行 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r8-merge/merged-answers.json --workdir /tmp/curio-s57-r8-formal-merge --json`，得到 **exit 1、`passed:false`、`failed:["no_recap"]`、0 advisory fail**；[stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[命令及雜湊](cli-status.json)、[官方 narrative 紀錄](official-narrative-record.json)已封存。官方紀錄 SHA-256 `7cca5179a334d9382b3e5172d64a859f0b3d5d3563e6d64c2b9b1877c09dacac`；CLI 前後五檔雜湊均與上表相同。

讀者 B 的分派承襲了前一輪 **R7 的高層狀態摘要**，雖在投票前未開作者或任何前輪評語檔；讀者 A 的隔離程度也沒有本合併程序可證實的 `fork_turns:none` 紀錄。此透明限制**不能轉成敘事 PASS**；本輪兩票及正式工具都已 HOLD。若 R9 修稿後想宣布過關，應用兩位 `fork_turns:none`、只讀新稿與固定題目的讀者重新投票。

**政策門檻止於敘事 HOLD，policy 未執行或核准。**接手作者可窄修上述四組重述，保留有來源的新資訊及最快語速八分鐘以上的正文，然後凍結新的五檔雜湊，重新查源與雙盲。付費語音、插圖、組片、上傳及站主網站卡均仍未完成。
