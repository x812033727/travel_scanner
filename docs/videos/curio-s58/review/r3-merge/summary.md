# S58 R3｜正式雙盲敘事 OR 合併診斷

2026-10-21 UTC。**敘事 HOLD：固定 OR 合併 11／13 YES；`no_recap`、`no_detour` 兩個必答題未過。**兩位無前情讀者均為 11 YES／2 NO，兩票對這兩題均投 NO。此版[獨立史料與書面畫面覆核](../r3-source-independent.md)另為 HOLD。沒有修改五份創作檔，也沒有進入政策、站主核准或付費媒體步驟。

| R3 凍結創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `27bebfb771aa8a901cf69528fb23401d351dcc35bdf584ab5e70c2163bfa0ea7` |
| `brief.md` | `49a1bd7cf68e2db074cc128bd08f60739da9ce85f63aa1ba4f7abab9f044e0d4` |
| `claims.md` | `73dcedbcbf30d5abd2db92fd34b789718e61938e8b4a86fe528d109851d332ec` |
| `video.json` | `7283ea2a7e444e2e58e83bb52a40da9548a1dddc1c2d74740971100f33936c48` |
| `script.md` | `6fd7c0585ebb1a47f518d70d769a1094deb54dc90404362df0ce0ed821ef1816` |

## 原票、OR 規則、正式回條

[A 原票](raw-ballot-a.md)與 [B 原票](raw-ballot-b.md)從 `../r3-blind-a.md` 和 `../r3-blind-b.md` 逐位元組複製，SHA-256 為 `568b28a0e0501f02420d5d83c1a00c93c6019a66858ab10e4629dfd7fba3ee9a`、`91c1f5019202cb827291bf1522764a455c8a57defae3011de64ee5041693efbc`；複本與原本雜湊一致。以[轉錄程式](build-merge.mjs)保留原票順序、每題原理由和 YES／NO，產生[官方形狀 A](ballot-a.json)與 [B](ballot-b.json)答卷及[稽核](merge-audit.json)。稽核 SHA-256 `ec394e0af214858ba3b82a6c238861f9ca3f3d82e26704e62830b343d2c7d749`。場景引用取各理由所指的代表句；對跨段理由仍以原票文字為準，未改一票的判定。官方 `PANEL_RULES_SHA256` 為 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

以正式 `mergePanelVerdicts` 的固定 **OR** 規則合併：任一讀者有帶場景 ID 的 YES，該題為 YES；兩票都 NO 才不過。[合併答案](merged-answers.json) SHA-256 `540114fd64f8222c139069fc3c464e62fabe1bbd932ebc2be8ff1cf24fa4a026`，11 YES、2 required NO、0 advisory NO。R3 五檔 SHA 在正式 CLI **之前與之後**均與上表一致。

[CLI 執行回條](cli-status.json)留存命令、隔離 `/tmp` 工作目錄、前後五 SHA、原票與輸出雜湊。正式執行 `node tools/video/cli.mjs narrative --slug curio-s58 --answers docs/videos/curio-s58/review/r3-merge/merged-answers.json --workdir /tmp/curio-s58-r3-merge-formal-nPmPoh --json`，**CLI exit 1、`passed:false`、兩個 required fail、零 advisory fail**。[原樣 stdout](cli.stdout.json) SHA-256 `428f955ad764d4e53586741277175f3588d11a49ebe2eeda2e60b7a85560542b`；[空 stderr](cli.stderr.txt)、[退出碼](cli.exit-code.txt)、[官方敘事紀錄](official-narrative-record.json)（SHA-256 `a714bb4d9aac287dd78069a6085d1fea78b1097eb9fcaca479892b0a6bda17a9`）均封存。官方紀錄 `round=1`、`narrative_hash=fbe53f255da25ff5`、`panel_narration_sha256=7aff34106a561026e2f2155a890918cc7ef652f6201de533ac48b4660f91bbdb`。

## 兩項雙票共同 NO

| 必答題 | 原票指出的斷點與 R4 修訂方向 |
| --- | --- |
| `no_recap` | A 指 `s58131–s58132` 連續兩句重說「六次」，第二句雖補原因仍未明確點名回呼；B 同指此重複，另指 `s58042` 與 `s58044` 重報被俘球帶走郵件與器材。保留一次事實，其餘句改為新的後果或刪去，不把兩個讀者的異議縮成一處。 |
| `no_detour` | A、B 均指 `s58054–s58056` 在墜球後花三句說繩勒同伴、沉箱險撞頭及女婿拉人，直到 `s58057–s58058` 才回到器材去留。短述迫降後直接追倖存的箱子，將正文時間用在有來源的通信工序上。 |

**交接：**R3 的正式敘事與獨立來源／書面畫面均 HOLD。R4 作者可在此完整封存之後修訂；新五檔須另建 SHA 收據，再交非作者來源覆核及兩位新盲讀，不能沿用 R3 票放行。
