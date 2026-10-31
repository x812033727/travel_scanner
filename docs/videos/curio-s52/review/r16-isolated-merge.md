# S52 R16｜兩位隔離讀者的正式敘事合併

凍結 `script.md` 原檔 SHA-256：`a5e75f568c542b6918b393c3485f2a1a18eb23c3b53dabbddf5f50f9d7c3747a`。兩人各自只讀同一份最新版劇本與固定 13 題，先交卷再合併；未請任何人看對方答案後改票。

| 審查 | 檔案 SHA-256 | 是／否 |
| --- | --- | --- |
| A | `r16-isolated-blind-a.json`：`c6d56759deb635dae8d650da8b7530a2f65e0613a5c09e208474281661cec93b` | 13／0 |
| B | `r16-isolated-blind-b.json`：`4cbd197a053230de87e5b1ccdf7e3b607a2c8cd6288bedb406a91c63359f4b27` | 10／3 |
| 正式 OR 輸入 | `r16-isolated-merged-answers.json`：`c6d56759deb635dae8d650da8b7530a2f65e0613a5c09e208474281661cec93b` | **13／0 PASS** |

正式規則是兩位讀者**都答否**才判該題未過。B 對 `no_toc` 的 `s52206`「接下來」、`no_recap` 的 `s52063` 重提三人，以及 `no_detour` 的 `s52071` 同船乘客各投否；A 對這三題各投是。三項異議保留在 B 原答卷，作為剪輯時的文字提醒，不擅自把正式規則改成單人否決，也不為此再改已鎖稿。合併輸入 13 題全部取 A 已凍結的「是」及原證據，因為 A 對每題均投是。

實跑 `VIDEO_WORKDIR=/tmp/curio-s52-r16-official NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s52 --answers /workspace/travel_scanner/docs/videos/curio-s52/review/r16-isolated-merged-answers.json`，退出碼 **0**；原始 verdict 存在 `r16-isolated-cli-receipt.json`，`passed: true`、`failed: []`、`advisory: []`。這只通過劇本敘事關；[R16 來源與書面畫面](r16-source-independent.md)另已 PASS，R16 尚未合成新語音、未完成聽音與音訊站台審核，也沒有插圖或成片。
