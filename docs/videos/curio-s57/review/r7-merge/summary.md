# S57 R7｜雙盲固定 OR 正式敘事合併

2026-10-21 UTC。**正式敘事 HOLD：11／13 YES；兩位新讀者共同否決 `no_recap`、`no_detour`。**[R7 獨立史料與書面畫面](../r7-source-independent.md)均為 PASS，但不能覆蓋此敘事阻擋。本次僅轉錄已定稿原票與執行正式工具；未改創作五檔。

| 凍結檔 | R7 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0474bc0e793cbda07021da98b3ea972a50b60fe87eacb708baf85457bdf554f6` |
| `claims.md` | `d4b8958f6f9c7b7fd62ec172ae39279d096086f22f4bdcc1fb2c07ef79401d38` |
| `video.json` | `f3befaaeb100cb0d9c275be56851691b174ef423777f1955375e520119bb71e7` |
| `script.md` | `185558e4d0e0ca51794126d8289ffb0d54065191d00cc010a2a6b72ff4d0245f` |

## 原票與固定 OR

[A 原票](raw-ballot-a.md)與[B 原票](raw-ballot-b.md)分別逐位元組複製自 `r7-blind-a.md`、`r7-blind-b.md`；SHA-256 分別為 `0896e27eeb013bfaca4c5255f005f3d424755f6e53742bc5176bf2ec7368d6a8`、`7cd69b0665b4391ae86b39d849f1a02a2f49e16609ad6e5f794600ba57aeb0a5`。兩份都是 **11 YES／2 NO**，共同 NO 即 `no_recap`、`no_detour`。讀者以稿件行號定位；[轉錄稽核](merge-audit.json)保留原理由、行號、所屬 scene ID 及逐字旁白，YES／NO 未變。[A 答案](ballot-a.json)與[B 答案](ballot-b.json)由原票轉錄；`panelVerdict` 與 `mergePanelVerdicts` 執行規定的固定 OR，[合併答案](merged-answers.json) SHA-256 `da40df698e61865330a8bc35febae4de757a5747d4222c7e0f2996714bb53417`，panel 規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

| 共同 NO | 原票所指的可修範圍 |
| --- | --- |
| `no_recap` | A：`s57100` 已說兩人回烏吉吉，緊接 `s57101` 又說「十三日回村」。B：`s57143` 已說二十日藏布拿出，`s57144` 再說布包追回；後句也重提十八日新援助。十八日抵達與新援助本是不同事件，僅刪後句重播。 |
| `no_detour` | A、B 均指 `s57101,s57104,s57105` 的領事信、亞丁電報、未收同類信件三拍沒有推動返家抉擇、東行取貨或最後分路。 |

## 官方紀錄與政策停點

執行 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r7-merge/merged-answers.json --workdir /tmp/curio-s57-r7-merge-formal-20261020 --json`，得到 **exit 1、`passed:false`、必答失敗僅 `no_recap,no_detour`、0 advisory fail**。創作五檔 CLI 前後 SHA 皆與上表相同。[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[命令與雜湊](cli-status.json)、[官方 narrative 紀錄](official-narrative-record.json)已存；官方紀錄 SHA-256 `0dd0e7cf9d4299fcab0b3eb020472089d702e028a6c822bcad86a69de9102c98`。

**政策門檻止於敘事 HOLD；未執行後續 policy 核准，未取得作者或站主通過。**語音、插圖、配樂、組片、上傳與發布均未執行。R8 作者只修上述重播與岔段，保留 2 月 18 日新援助→19 日藥品→20 日藏布、S／L 來源層級與八分鐘以上正文。R8 新雜湊須重新接受獨立史料／書面畫面及兩位新讀者盲評。
