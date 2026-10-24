# S55 R7｜隔離盲評官方合併

2026-10-20 UTC。兩位新讀者各自凍結 [A](r7-isolated-blind-a.md)／[A JSON](r7-isolated-blind-a.json) 和 [B](r7-isolated-blind-b.md)／[B JSON](r7-isolated-blind-b.json)，均讀取 `script.md` SHA-256 `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899`。原始判斷和引句沒有修改。兩人各為 11 Yes／2 No。

依正式 `panelVerdict` 和 `mergePanelVerdicts`，任一讀者附場景 ID 判 Yes，該題合併為 Yes。A 的 `no_detour` No 和 B 的 `payoffs` No 都保留在原件與稽核檔；另一位讀者各判 Yes，因此不是合併失敗項。雙方共同判 No 的必答題只有 `no_recap`。**官方結果 FAIL，12/13 Yes。**

| 題目 | A | B | 合併 |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | **Yes** |
| `no_spoiler` | Yes | Yes | **Yes** |
| `one_line` | Yes | Yes | **Yes** |
| `no_toc` | Yes | Yes | **Yes** |
| `chapters_link` | Yes | Yes | **Yes** |
| `open_loops` | Yes | Yes | **Yes** |
| `payoffs` | Yes | No | **Yes** |
| `no_recap` | No | No | **No** |
| `chapters_are_events`（參考題） | Yes | Yes | **Yes** |
| `outro_no_next` | Yes | Yes | **Yes** |
| `opening_hooks` | Yes | Yes | **Yes** |
| `one_thread` | Yes | Yes | **Yes** |
| `no_detour` | No | Yes | **Yes** |

**編修依據：**兩人均指出 `s55046` 已說十月八日預告的詳報未出，`s55047` 又重說未出版。A 另認為 `s55046`–`s55048` 的冊子與圖畫拖慢動物著地的安全問題；B 另認為 `s55040` 的較大球落地問題到 `s55132` 才解答，長距離回收缺少點名。R8 作者應修共同失敗，也可收緊 A 指出的圖畫岔路；B 的少數異議並非官方額外失敗。

## 可重算收據

[合併稽核檔](r7-isolated-merge-audit.json)保存原始檔 SHA、兩份原始判斷，以及 `panelVerdict`／`mergePanelVerdicts` 的逐題結果。[合併答案](r7-isolated-merged-answers.json)直接取官方合併結果的 Yes／No 和引句，沒有正規化或改寫原始引句。用下列命令重算：

`VIDEO_WORKDIR=/tmp/curio-s55-r7-isolated-merge node tools/video/cli.mjs narrative --slug curio-s55 --answers docs/videos/curio-s55/review/r7-isolated-merged-answers.json --json`

CLI 因必答 No 預期退出 **1**；[CLI verdict](r7-isolated-cli-verdict.json)和 [CLI receipt](r7-isolated-cli-receipt.json)均為 `passed: false`、`failed: ["no_recap"]`。收據為 round 1；script check hash `99fe298e4dac9cf44149e7bb06d38cc94a3bdb63f626d708652e8ae102b4b052`，panel 規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，panel narration SHA-256 `7a11553366e7560e43f69b618a64b00af525a6c0af1f18d539ce78bf8aa291ed`。

| 歸檔原件 | SHA-256 |
| --- | --- |
| A Markdown | `7f5c0c713a2afe082cf00181dbfaa6162a1fc570daefbe181c6f8a7c6308a49a` |
| A JSON | `c4c67706e0b120a8ffa78f8759eb0b574bc59c64f56dcbf691fd363477b4018c` |
| B Markdown | `7c96331ec4329b2c8b2251f48980b700d31c8cd2c00d0e0a5c6b301351e3dda7` |
| B JSON | `c5c112837e30d33efd70d3dc9dea138fd2c471e359cb075a6b55372ca2caf485` |
| Merge audit | `12415bfcf0edf98e47d6b20714834f967efb58324e753cd97ab2a49172914ecf` |
| Merged answers | `ddba2bc6f744d0e581d9a5f6841631e1ef30feb770416c4ef1d0e5676a0bc284` |
| CLI verdict | `33186f91cb8771739e611c2b9c93f709b4d0fb3abb259044ed9f842d33585bbe` |
| CLI receipt | `21f2503f5b4b93d74ddd7341d4c379e0669712c7484de0b1cbc75c6d3481eb4a` |

這份 R7 FAIL 不修改作者五檔或媒體；修稿須新 SHA 與兩位新讀者隔離盲評。
