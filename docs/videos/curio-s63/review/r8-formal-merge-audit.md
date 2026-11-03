# S63 R8｜正式雙人盲讀合併審核

2026-10-22 UTC。**PASS：13／13 題通過，無必答否決或非必答建議。**兩位全新讀者在各自寫原票前，只收到同一份 R8 凍結旁白、逐字場景 ID 及官方 13 題；沒有看企劃、史料、畫面、舊票或對方的票。A、B 原票及各自的官方隔離重播均保留，不以合併結果抹去 B 的單人意見。

| 凍結物 | SHA-256 |
| --- | --- |
| `video.json` | `c417bc8c6f0df78e9c4d8e910db038b6f4ea07c760cc7f3c2e69e98224f63f08` |
| `script.md` | `63caedb24623bd8339607dd5b11e249ce1a4e6691779279a6d8c64ef5bbd665e` |
| `claims.md` | `68c4139f38976d09b9b1b21bdb239eaa4ecb0ddd2f053b0ef445b971d636fe5e` |
| 隔離盲讀封包 `/tmp/s63-r8-blind-packet.json` | `9386b749d8380b9fe7ec01ba94e0ae4113d74d1b68f85f166c2c5a32b5e09a5f` |
| [A 原票](r8-isolated-blind-a.raw.json) | `de2a2eb37bd4a2c29cc8e956a5179d76b7f7371c0d23e4356b509a8bcb28d0d7` |
| [B 原票](r8-isolated-blind-b.raw.json) | `fcb22e926296cefcc04d1c95e250b871ca18f7983d251057dadc10a3e7b8ed48` |
| [正式合併答卷](r8-formal-merged-answers.json) | `de2a2eb37bd4a2c29cc8e956a5179d76b7f7371c0d23e4356b509a8bcb28d0d7` |
| [正式合併紀錄](r8-formal-merged-narrative.json) | `10a6fceb7ab5cdb546a3aff58bc27c52121445eccf8114ebfe853344959e2f85` |

兩份原票各有同序 13 題，每題括號 ID 及引句均和凍結封包逐字一致。官方原碼分別跑 `panelVerdict`，再用 `mergePanelVerdicts` **逐題 OR**：一人有效回答「是」即通過，兩人都答「否」才擋下。`narrativeRecord` 記錄兩位個別判定及正式結果。A 為 13／13「是」，B 為 12／13「是」；因此合併答卷的內容和 A 原票相同，SHA-256 也相同，**沒有改寫 B 的原票**。

| 題目 | A | B | 正式合併 |
| --- | --- | --- | --- |
| `no_recap` | 是；`s63025` 指向接下來的家庭風險 | 否；`s63027` 和前一句 `s63026` 都有「五十美元」 | **是**，依官方逐題 OR |
| 其餘 12 題 | 全是 | 全是 | 全是 |

B 的具體顧慮保留：`s63026` 是 Brown **先付的一筆 50 美元**，`s63027` 是此後**每年另付的 50 美元**，原文 [B02 L1245–1257](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1245-L1257) 明確分為不同付款。兩句相鄰且已標明「先」與「每年」；保留目前忠於原文的區別，不對已通過的凍結稿再作主觀修稿。

官方 `node tools/video/cli.mjs narrative --slug curio-s63 --answers <原票或正式合併答卷> --workdir <全新隔離目錄> --json` 各跑一次。A exit **0**、B exit **1**（只否決 `no_recap`）、正式合併 exit **0**，failed 與 advisory 均空；三份 [CLI 回條](r8-formal-merged-cli-status.json)分別列出原票雜湊、命令、隔離工作目錄、exit、失敗 ID、輸出雜湊。另保存個別 `bound.json`、`cli.stdout.json`、`cli.stderr.txt`、`cli.exit.txt`、`receipt.json` 和正式合併同樣的原始檔。每次隔離重播 `round=1`；正式合併紀錄為 R8。

三次官方綁定同屬完全相同的腳本雜湊 `c9aca3a2a7aee85b7da8c092681eb3256d4d64bc0d40b56f8b4b572d25941b6a`、規則雜湊 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、旁白雜湊 `1c16f2729eb05749a3dc0172a89fd0e4cd8dc370346a0b34c4485e5edcb6a633`，敘事雜湊 `09e2ab55b95db7c1`。正式合併官方綁定檔 SHA-256 `dcc8b360f73b893c800b37a0a0f8b529562912f57115cf5ce02746c35882db3d`；`passed: true`。

[R8 獨立史料／書面畫面回條](r8-source-visual-independent.md)在相同三檔凍結雜湊下也是 **PASS**。這兩關只核准稿件與尚未產圖的書面畫面，不代表實際插圖、語音、成片、Short、上傳或片尾 Studio 連結已製作或核准；後續媒體仍須各自照流程驗收。
